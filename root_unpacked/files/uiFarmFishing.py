# -*- coding: utf-8 -*-
"""F8 Auto Fishing controller.

Uses a bait selected directly from the normal inventory.  The fishing action is
left to the native client: bait is used through SendItemUsePacket, the rod is
started with the native attack key, and The fishing skill is activated through player.ClickSkillSlot. The native
OnFishingNotify/Success/Failure callbacks are used as the bite/result boundary.

The native fishing build exposes the chat text "To catch a fish, you must press
%dx Space", but that packet is not currently exposed to Python with the %d
argument.  This module therefore includes a Python chat hook for builds where
the message reaches chat.AppendChat.  A native GetLastChatLine/GetFishingStep
binding is the clean next step if the server sends the instruction directly to
CPythonChat.
"""

import re
import random
import ctypes

import app
import chat
import item
import mouseModule
import net
import player
import settings
import ui


CONFIG_KEY = "F8_FISH_BOT_CONFIG"
BAIT_USE_DELAY = 0.60
CAST_DELAY = 0.35
REEL_USE_DELAY = 0.18
BITE_TIMEOUT = 45.0
RESULT_DELAY = 4.00
MAX_REEL_USES = 3
RESULT_FALLBACK_TIMEOUT = 8.00
PROBE_RESULT_WAIT = 0.65
DEFAULT_RESULT_WAIT = 4.0
DEFAULT_REEL_MIN_MS = 20
DEFAULT_REEL_MAX_MS = 100

_ACTIVE_CONTROLLER = None

def GetActiveController():
    """Return the currently running/available F8 Auto Fish controller."""
    return _ACTIVE_CONTROLLER

# The live client prints, for example:
#   "[Wędkarstwo] > Aby wyłowić rybę, musisz nacisnąć 2x spację."
# Keep the expression deliberately independent of the decorative prefix/colour
# codes so it also works with localized/packed chat strings.
_INSTRUCTION_RE = re.compile(
    r"(?:musisz\s+nacisn[aą]ć|press)\s*(\d+)\s*[xX]\s*(?:spacj(?:ę|e|a)|space)",
    re.I | re.UNICODE,
)
_COLOR_TAG_RE = re.compile(r"\|c[0-9a-fA-F]{6,8}|\|r|\|E[^|]*\|e", re.I)

def _clean_chat_text(text):
    try:
        text = str(text)
        text = _COLOR_TAG_RE.sub("", text)
        return text.replace("\xa0", " ")
    except Exception:
        return ""
_FISH_SUCCESS_RE = re.compile(r"(?:Otrzymałeś|Otrzymales|Zdobyłeś|Zdobyles)\b", re.I | re.UNICODE)
_FISH_FAILURE_RE = re.compile(r"(?:Straciłeś|Straciles)\s+przynętę|(?:za mało|za dużo)\s+razy", re.I | re.UNICODE)


class FishingBotWindow(ui.ScriptWindow):
    """Small F8 Auto Fish setup window."""

    def __init__(self, controller):
        ui.ScriptWindow.__init__(self)
        self.controller = controller
        self.slot = None
        self.status = None
        self.startButton = None
        self.stopButton = None
        self._build()
        self.Hide()

    def _build(self):
        self.board = ui.BoardWithTitleBar()
        self.board.SetParent(self)
        self.board.SetSize(560, 500)
        self.board.SetPosition(0, 0)
        self.board.SetTitleName("Auto Fish F8 - diagnostyka")
        self.board.SetCloseEvent(ui.__mem_func__(self.Hide))
        self.board.Show()

        info = ui.TextLine()
        info.SetParent(self.board)
        info.SetPosition(18, 34)
        info.SetText("1. PRZYNĘTA Z EQ:")
        info.Show()

        self.slot = ui.SlotWindow()
        self.slot.SetParent(self.board)
        self.slot.SetPosition(20, 56)
        self.slot.SetSize(32, 32)
        self.slot.AppendSlot(0, 0, 0, 32, 32)
        self.slot.SetSelectEmptySlotEvent(ui.__mem_func__(self._select_bait))
        self.slot.SetSelectItemSlotEvent(ui.__mem_func__(self._select_bait))
        self.slot.Show()

        self.baitName = ui.TextLine()
        self.baitName.SetParent(self.board)
        self.baitName.SetPosition(66, 64)
        self.baitName.SetText("Brak przynęty")
        self.baitName.Show()

        skillInfo = ui.TextLine()
        skillInfo.SetParent(self.board)
        skillInfo.SetPosition(18, 94)
        skillInfo.SetText("2. SKILL ŁOWIENIA Z V:")
        skillInfo.Show()

        self.skillSlot = ui.SlotWindow()
        self.skillSlot.SetParent(self.board)
        self.skillSlot.SetPosition(20, 116)
        self.skillSlot.SetSize(32, 32)
        self.skillSlot.AppendSlot(0, 0, 0, 32, 32)
        self.skillSlot.SetSelectEmptySlotEvent(ui.__mem_func__(self._select_skill))
        self.skillSlot.SetSelectItemSlotEvent(ui.__mem_func__(self._select_skill))
        self.skillSlot.Show()

        self.skillName = ui.TextLine()
        self.skillName.SetParent(self.board)
        self.skillName.SetPosition(66, 124)
        self.skillName.SetText("Brak skilla")
        self.skillName.Show()

        self.status = ui.TextLine()
        self.status.SetParent(self.board)
        self.status.SetPosition(18, 154)
        self.status.SetText("Status: OFF")
        self.status.Show()

        self.stats = ui.TextLine()
        self.stats.SetParent(self.board)
        self.stats.SetPosition(18, 176)
        self.stats.SetText("Łowienia: 0  |  Wyłowione: 0  |  Niepowodzenia: 0")
        self.stats.Show()

        self.resultWaitLabel = ui.TextLine()
        self.resultWaitLabel.SetParent(self.board)
        self.resultWaitLabel.SetPosition(18, 204)
        self.resultWaitLabel.SetText("Czas po wyniku: 4.0 s")
        self.resultWaitLabel.Show()

        self.resultWaitSlider = ui.SliderBar()
        self.resultWaitSlider.SetParent(self.board)
        self.resultWaitSlider.SetPosition(18, 222)
        self.resultWaitSlider.SetSliderPos(0.20)
        self.resultWaitSlider.SetEvent(ui.__mem_func__(self._on_wait_slider))
        self.resultWaitSlider.Show()

        self.minLabel = ui.TextLine()
        self.minLabel.SetParent(self.board)
        self.minLabel.SetPosition(18, 254)
        self.minLabel.SetText("Losowe opóźnienie skilla [ms]:")
        self.minLabel.Show()

        self.minEdit = ui.EditLine()
        self.minEdit.SetParent(self.board)
        self.minEdit.SetPosition(18, 276)
        self.minEdit.SetSize(70, 20)
        self.minEdit.SetText("20")
        self.minEdit.SetMax(5)
        self.minEdit.Show()

        self.maxEdit = ui.EditLine()
        self.maxEdit.SetParent(self.board)
        self.maxEdit.SetPosition(100, 276)
        self.maxEdit.SetSize(70, 20)
        self.maxEdit.SetText("100")
        self.maxEdit.SetMax(5)
        self.maxEdit.Show()

        self.delayInfo = ui.TextLine()
        self.delayInfo.SetParent(self.board)
        self.delayInfo.SetPosition(184, 279)
        self.delayInfo.SetText("min - max ms")
        self.delayInfo.Show()

        self.startButton = ui.Button()
        self.startButton.SetParent(self.board)
        self.startButton.SetPosition(18, 316)
        self.startButton.SetUpVisual("d:/ymir work/ui/public/middle_button_01.sub")
        self.startButton.SetOverVisual("d:/ymir work/ui/public/middle_button_02.sub")
        self.startButton.SetDownVisual("d:/ymir work/ui/public/middle_button_03.sub")
        self.startButton.SetText("Start")
        self.startButton.SetEvent(ui.__mem_func__(self.controller.Start))
        self.startButton.Show()

        self.stopButton = ui.Button()
        self.stopButton.SetParent(self.board)
        self.stopButton.SetPosition(109, 316)
        self.stopButton.SetUpVisual("d:/ymir work/ui/public/middle_button_01.sub")
        self.stopButton.SetOverVisual("d:/ymir work/ui/public/middle_button_02.sub")
        self.stopButton.SetDownVisual("d:/ymir work/ui/public/middle_button_03.sub")
        self.stopButton.SetText("Stop")
        self.stopButton.SetEvent(ui.__mem_func__(self.controller.Stop))
        self.stopButton.Show()

        self.debug = ui.TextLine()
        self.debug.SetParent(self.board)
        self.debug.SetPosition(18, 356)
        self.debug.SetText("Diagnostyka: oczekiwanie")
        self.debug.Show()

        self.tip = ui.TextLine()
        self.tip.SetParent(self.board)
        self.tip.SetPosition(18, 388)
        self.tip.SetText("Logi szczegółowe są wysyłane na czat [F8 Auto Fish].")
        self.tip.Show()

        self.lastAction = ui.TextLine()
        self.lastAction.SetParent(self.board)
        self.lastAction.SetPosition(18, 414)
        self.lastAction.SetText("Ostatnia akcja: -")
        self.lastAction.Show()

        self.SetSize(560, 500)

    def _on_wait_slider(self):
        try:
            value = 1.0 + self.resultWaitSlider.GetSliderPos() * 9.0
            self.controller.result_delay = round(value, 1)
            self.resultWaitLabel.SetText("Czas po wyniku: %.1f s" % self.controller.result_delay)
            self.controller._save_config()
        except Exception:
            pass

    def SetDebug(self, text):
        try:
            self.debug.SetText("Diagnostyka: " + str(text))
            self.lastAction.SetText("Ostatnia akcja: " + str(text))
        except Exception:
            pass

    def RefreshStats(self, attempts, caught, failed):
        try:
            self.stats.SetText("Łowienia: %d  |  Wyłowione: %d  |  Niepowodzenia: %d" % (attempts, caught, failed))
        except Exception:
            pass

    def _select_bait(self, slot_index):
        try:
            if not mouseModule.mouseController.isAttached():
                return
            attached_type = mouseModule.mouseController.GetAttachedType()
            attached_slot = mouseModule.mouseController.GetAttachedSlotNumber()
            if attached_type != player.SLOT_TYPE_INVENTORY:
                mouseModule.mouseController.DeattachObject()
                return
            self.controller.SetBaitSlot(attached_slot)
            mouseModule.mouseController.DeattachObject()
        except Exception:
            try:
                mouseModule.mouseController.DeattachObject()
            except Exception:
                pass

    def _select_skill(self, slot_index):
        try:
            if not mouseModule.mouseController.isAttached():
                return
            attached_type = mouseModule.mouseController.GetAttachedType()
            attached_slot = mouseModule.mouseController.GetAttachedSlotNumber()
            if attached_type != player.SLOT_TYPE_SKILL:
                mouseModule.mouseController.DeattachObject()
                return
            if not self.controller.SetFishingSkillSlot(attached_slot):
                mouseModule.mouseController.DeattachObject()
                return
            mouseModule.mouseController.DeattachObject()
        except Exception:
            try:
                mouseModule.mouseController.DeattachObject()
            except Exception:
                pass

    def _over_skill_in(self, slot_index):
        return

    def _over_skill_out(self):
        return

    def _over_in(self, slot_index):
        return

    def _over_out(self):
        return

    def Refresh(self):
        try:
            slot = self.controller.FindBaitSlot()
            self.slot.ClearSlot(0)
            if slot >= 0:
                vnum = int(player.GetItemIndex(slot))
                count = int(player.GetItemCount(slot))
                if vnum > 0 and count > 0:
                    self.slot.SetItemSlot(0, vnum, count if count > 1 else 0)
                    try:
                        item.SelectItem(vnum)
                        self.baitName.SetText("%s  x%d" % (item.GetItemName(), count))
                    except Exception:
                        self.baitName.SetText("Przynęta VNUM %d  x%d" % (vnum, count))
                else:
                    self.baitName.SetText("Brak przynęty")
            else:
                self.baitName.SetText("Brak przynęty")
            self.slot.RefreshSlot()

            self.skillSlot.ClearSlot(0)
            skill_slot = self.controller.FindFishingSkillSlot()
            if skill_slot >= 0:
                try:
                    skill_idx = int(player.GetSkillIndex(skill_slot))
                    level = int(player.GetSkillLevel(skill_slot))
                    grade = int(player.GetSkillGrade(skill_slot))
                    self.skillSlot.SetSkillSlotNew(0, skill_idx, grade, level)
                    try:
                        import skill as _skill
                        self.skillName.SetText(_skill.GetSkillName(skill_idx))
                    except Exception:
                        self.skillName.SetText("Skill %d" % skill_idx)
                except Exception:
                    self.skillName.SetText("Brak skilla")
            else:
                self.skillName.SetText("Brak skilla")
            self.skillSlot.RefreshSlot()
            self.RefreshStats(self.controller.attempts, self.controller.caught, self.controller.failed)
            self.resultWaitSlider.SetSliderPos((self.controller.result_delay - 1.0) / 9.0)
            self.resultWaitLabel.SetText("Czas po wyniku: %.1f s" % self.controller.result_delay)
            self.minEdit.SetText(str(self.controller.reel_min_ms))
            self.maxEdit.SetText(str(self.controller.reel_max_ms))
        except Exception:
            pass

    def SetStatus(self, text):
        try:
            self.status.SetText("Status: " + str(text))
        except Exception:
            pass

    def Open(self):
        self.Refresh()
        self.Show()
        self.SetTop()

    def Close(self):
        self.Hide()

    def OnPressEscapeKey(self):
        self.Hide()
        return True


class FishingBotController(object):
    """State machine for the F8 Auto Fish bot."""

    STATE_IDLE = 0
    STATE_USE_BAIT = 1
    STATE_CAST = 2
    STATE_WAIT_BITE = 3
    STATE_REEL_SKILL = 4
    STATE_RESULT = 5

    def __init__(self, parent=None):
        self.parent = parent
        self.running = False
        self.state = self.STATE_IDLE
        self.state_at = 0.0
        self.bait_slot = -1
        self.bait_vnum = 0
        self.skill_slot = -1
        self.skill_index = 0
        self.reel_uses_done = 0
        self.next_reel_at = 0.0
        self.required_space = 0
        self.space_left = 0
        self.bite_deadline = 0.0
        self.result_at = 0.0
        self.result_watch_until = 0.0
        self.last_error = ""
        self.last_instruction_count = 0
        self.last_instruction_at = 0.0
        self.last_result_at = 0.0
        self.result_delay = DEFAULT_RESULT_WAIT
        self.reel_min_ms = DEFAULT_REEL_MIN_MS
        self.reel_max_ms = DEFAULT_REEL_MAX_MS
        self.attempts = 0
        self.caught = 0
        self.failed = 0
        self.last_bite_name = ""
        self._native_dll = None
        self._native_get_event = None
        self._native_event_seq = 0
        self.window = FishingBotWindow(self)
        global _ACTIVE_CONTROLLER
        _ACTIVE_CONTROLLER = self
        self._load_config()
        self.window.Refresh()
        try:
            self.window.resultWaitSlider.SetSliderPos((self.result_delay - 1.0) / 9.0)
            self.window.resultWaitLabel.SetText("Czas po wyniku: %.1f s" % self.result_delay)
            self.window.minEdit.SetText(str(self.reel_min_ms))
            self.window.maxEdit.SetText(str(self.reel_max_ms))
        except Exception:
            pass
        self._init_native_dll()
        self._install_chat_hook()

    def _init_native_dll(self):
        """Bind to the already-injected FishNative.dll in this client process."""
        try:
            kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
            kernel32.GetModuleHandleW.argtypes = [ctypes.c_wchar_p]
            kernel32.GetModuleHandleW.restype = ctypes.c_void_p
            handle = kernel32.GetModuleHandleW("FishNative.dll")
            if not handle:
                self._native_dll = None
                self._native_get_event = None
                return False
            self._native_dll = ctypes.WinDLL("FishNative.dll", handle=handle)
            self._native_get_event = self._native_dll.GetFishingEvent
            self._native_get_event.argtypes = []
            self._native_get_event.restype = ctypes.c_ulonglong
            return True
        except Exception as exc:
            self._native_dll = None
            self._native_get_event = None
            self.last_error = str(exc)
            return False

    def _native_event_value(self):
        try:
            if self._native_get_event is None:
                if not self._init_native_dll():
                    return 0
            return int(self._native_get_event())
        except Exception:
            self._native_get_event = None
            return 0

    def _sync_native_event_cursor(self):
        value = self._native_event_value()
        self._native_event_seq = int(value >> 2)
        return value

    def _poll_native_fishing_event(self):
        value = self._native_event_value()
        if value == 0:
            return
        seq = int(value >> 2)
        count = int(value & 0x3)
        if seq == self._native_event_seq:
            return
        self._native_event_seq = seq
        if count not in (2, 3):
            return
        self.SetRequiredSpace(count)

    def _load_config(self):
        try:
            cfg = getattr(settings, CONFIG_KEY, {})
            if isinstance(cfg, dict):
                self.bait_slot = int(cfg.get("slot", -1))
                self.bait_vnum = int(cfg.get("vnum", 0))
                self.skill_slot = int(cfg.get("skill_slot", -1))
                self.skill_index = int(cfg.get("skill_index", 0))
                self.result_delay = max(1.0, min(10.0, float(cfg.get("result_delay", DEFAULT_RESULT_WAIT))))
                self.reel_min_ms = max(0, min(5000, int(cfg.get("reel_min_ms", DEFAULT_REEL_MIN_MS))))
                self.reel_max_ms = max(self.reel_min_ms, min(5000, int(cfg.get("reel_max_ms", DEFAULT_REEL_MAX_MS))))
        except Exception:
            pass

    def _save_config(self):
        try:
            setattr(settings, CONFIG_KEY, {
                "slot": int(self.bait_slot),
                "vnum": int(self.bait_vnum),
                "skill_slot": int(self.skill_slot),
                "skill_index": int(self.skill_index),
                "result_delay": float(self.result_delay),
                "reel_min_ms": int(self.reel_min_ms),
                "reel_max_ms": int(self.reel_max_ms),
            })
        except Exception:
            pass

    def _log(self, text):
        try:
            chat.AppendChat(chat.CHAT_TYPE_INFO, "[F8 Auto Fish] " + str(text))
        except Exception:
            pass

    def _install_chat_hook(self):
        try:
            if getattr(chat, "_DRAZE_FISH_HOOK", False):
                chat._DRAZE_FISH_BOT = self
                return
            original = chat.AppendChat

            def _append_chat_hook(chat_type, text):
                try:
                    bot = getattr(chat, "_DRAZE_FISH_BOT", None)
                    if bot:
                        bot.OnChatMessage(text)
                except Exception:
                    pass
                return original(chat_type, text)

            chat.AppendChat = _append_chat_hook
            chat._DRAZE_FISH_HOOK = True
            chat._DRAZE_FISH_BOT = self
            chat._DRAZE_FISH_ORIGINAL = original

            if hasattr(chat, "AppendChatWithDelay") and not getattr(chat, "_DRAZE_FISH_DELAY_HOOK", False):
                original_delay = chat.AppendChatWithDelay

                def _append_chat_delay_hook(chat_type, text, delay):
                    try:
                        bot = getattr(chat, "_DRAZE_FISH_BOT", None)
                        if bot:
                            bot.OnChatMessage(text)
                    except Exception:
                        pass
                    return original_delay(chat_type, text, delay)

                chat.AppendChatWithDelay = _append_chat_delay_hook
                chat._DRAZE_FISH_DELAY_HOOK = True
                chat._DRAZE_FISH_ORIGINAL_DELAY = original_delay
        except Exception:
            pass

    def OnChatMessage(self, text):
        if not self.running:
            return
        raw = _clean_chat_text(text)
        if not raw:
            return

        # Fishing count is read exclusively from FishNative.dll.
        # Chat is used only as a secondary success/failure signal.
        if _FISH_SUCCESS_RE.search(raw) or _FISH_FAILURE_RE.search(raw):
            self._fishing_result("Wynik z czatu")

    def SetRequiredSpace(self, count):
        if not self.running:
            return
        count = int(count)
        if count not in (2, 3):
            return
        self.required_space = count
        self.space_left = count
        self.state = self.STATE_REEL_SKILL
        self.state_at = app.GetTime()
        self.next_reel_at = self.state_at
        self.reel_uses_done = 0
        self.result_watch_until = 0.0
        self.window.SetStatus("BRANIE -> SPACE x%d" % count)
        self.window.SetDebug("DLL: FISHING_COUNT=%d" % count)
        self._log("DLL FISHING_COUNT=%d -> wykonuję dokładnie %d naciśnięcia SPACE." % (count, count))

    def SetBaitSlot(self, slot):
        try:
            slot = int(slot)
            vnum = int(player.GetItemIndex(slot))
            count = int(player.GetItemCount(slot))
            if vnum <= 0 or count <= 0:
                return False
            item.SelectItem(vnum)
            subtype = int(item.GetItemSubType())
            bait_type = int(getattr(item, "USE_BAIT", -999999))
            if subtype != bait_type:
                self._log("Wybrany przedmiot nie jest przynętą.")
                return False
            self.bait_slot = slot
            self.bait_vnum = vnum
            self._save_config()
            self.window.Refresh()
            self._log("Przynęta ustawiona: EQ=%d VNUM=%d." % (slot, vnum))
            return True
        except Exception as exc:
            self.last_error = str(exc)
            self._log("Nie można ustawić przynęty: %s" % exc)
            return False

    def SetFishingSkillSlot(self, slot):
        try:
            slot = int(slot)
            idx = int(player.GetSkillIndex(slot))
            expected = int(getattr(player, "SKILL_INDEX_FISHING", -1))
            if idx <= 0 or (expected > 0 and idx != expected):
                self._log("Wybrany skill nie jest skillem Łowienie.")
                return False
            self.skill_slot = slot
            self.skill_index = idx
            self._save_config()
            self.window.Refresh()
            self._log("Skill łowienia ustawiony: slot=%d VNUM=%d." % (slot, idx))
            return True
        except Exception as exc:
            self._log("Nie można ustawić skilla łowienia: %s" % exc)
            return False

    def FindFishingSkillSlot(self):
        try:
            expected = int(getattr(player, "SKILL_INDEX_FISHING", -1))
            if expected > 0:
                try:
                    slot = int(player.GetSkillSlotIndex(expected))
                    if slot >= 0 and int(player.GetSkillIndex(slot)) == expected:
                        self.skill_slot = slot
                        self.skill_index = expected
                        return slot
                except Exception:
                    pass
        except Exception:
            pass
        try:
            if self.skill_slot >= 0:
                idx = int(player.GetSkillIndex(self.skill_slot))
                if idx > 0 and (self.skill_index <= 0 or idx == self.skill_index):
                    return self.skill_slot
        except Exception:
            pass
        return -1

    def _click_fishing_skill(self):
        slot = self.FindFishingSkillSlot()
        if slot < 0:
            self.window.SetDebug("BRAK SLOTU SKILLA")
            self._log("BŁĄD: brak ustawionego skilla Łowienie.")
            return False
        try:
            idx = int(player.GetSkillIndex(int(slot)))
            level = int(player.GetSkillLevel(int(slot)))
            expected = int(getattr(player, "SKILL_INDEX_FISHING", -1))
            self._log("Próba użycia skilla: slot=%d index=%d level=%d oczekiwany=%d." % (slot, idx, level, expected))
            try:
                cooldown = bool(player.IsSkillCoolTime(int(slot)))
                self._log("Stan skilla: cooldown=%s." % cooldown)
                if cooldown:
                    self.window.SetDebug("SKILL NA COOLDOWN")
                    return False
            except Exception:
                pass
            player.ClickSkillSlot(int(slot))
            self.window.SetDebug("SKILL UŻYTY: slot=%d index=%d" % (slot, idx))
            self._log("OK: ClickSkillSlot(%d) wykonany." % slot)
            return True
        except Exception as exc:
            self.window.SetDebug("BŁĄD CLICK SKILL")
            self._log("BŁĄD ClickSkillSlot: %s" % exc)
            return False

    def OnFishingNotify(self, isFish=False, fishName=""):
        if not self.running:
            return
        now = app.GetTime()
        # The native callback marks the bite boundary. Do not guess 2/3.
        # Wait for the exact FISHING_COUNT event from FishNative.dll.
        self.required_space = 0
        self.space_left = 0
        self.reel_uses_done = 0
        self.state = self.STATE_REEL_SKILL
        self.state_at = now
        self.next_reel_at = now
        self.result_watch_until = now + RESULT_FALLBACK_TIMEOUT
        self.window.SetStatus("BRANIE -> czekam na DLL")
        self.window.SetDebug("BRANIE: oczekiwanie na FISHING_COUNT=2/3")
        self._log("WYKRYTO BRANIE -> czekam na dokładne FISHING_COUNT z FishNative.dll. isFish=%s fish=%s" % (str(isFish), str(fishName)))

    def OnFishingNotifyUnknown(self):
        if not self.running:
            return
        self.window.SetDebug("CALLBACK: OnFishingNotifyUnknown")
        self._log("CALLBACK OnFishingNotifyUnknown: system łowienia zgłosił nieznany stan.")

    def OnFishingSuccess(self, isFish=False, fishName=""):
        if not self.running:
            return
        self.caught += 1
        self.window.RefreshStats(self.attempts, self.caught, self.failed)
        self.window.SetDebug("SUKCES: %s" % (fishName if fishName else "ryba"))
        self._log("CALLBACK SUCCESS: złowiono=%s | statystyka %d/%d/%d" % (str(fishName), self.attempts, self.caught, self.failed))
        self._fishing_result("Złowiono: %s" % fishName if fishName else "Złowiono rybę")

    def OnFishingFailure(self):
        if not self.running:
            return
        self.failed += 1
        self.window.RefreshStats(self.attempts, self.caught, self.failed)
        self.window.SetDebug("NIEPOWODZENIE / STRACONA PRZYNĘTA")
        self._log("CALLBACK FAILURE: stracona przynęta | statystyka %d/%d/%d" % (self.attempts, self.caught, self.failed))
        self._fishing_result("Łowienie nieudane / stracona przynęta")

    def OnFishingWrongPlace(self):
        if not self.running:
            return
        self.window.SetDebug("BŁĄD: NIEPRAWIDŁOWE MIEJSCE")
        self._log("CALLBACK WRONG PLACE: nie można łowić w tym miejscu.")
        self.state = self.STATE_USE_BAIT
        self.state_at = app.GetTime() + 1.0

    def _fishing_result(self, label):
        now = app.GetTime()
        self.reel_uses_done = 0
        self.required_space = 0
        self.space_left = 0
        self.result_watch_until = 0.0
        self.state = self.STATE_RESULT
        # Keep the rod/fishing animation untouched for at least 4 seconds.
        self.result_at = now + float(self.result_delay)
        self.last_result_at = now
        self.window.SetStatus("%s -> czekam %.1fs" % (label, self.result_delay))
        self.window.SetDebug("KONIEC CYKLU: czekam %.1fs" % self.result_delay)
        self._log("%s. Czekam %.1fs na zakończenie animacji." % (label, self.result_delay))

    def FindBaitSlot(self):
        try:
            if self.bait_slot >= 0:
                if int(player.GetItemIndex(self.bait_slot)) == self.bait_vnum and int(player.GetItemCount(self.bait_slot)) > 0:
                    return self.bait_slot
        except Exception:
            pass
        if self.bait_vnum <= 0:
            return -1
        try:
            size = int(player.INVENTORY_PAGE_SIZE * player.INVENTORY_PAGE_COUNT)
        except Exception:
            size = 5 * 45
        try:
            for slot in range(size):
                if int(player.GetItemIndex(slot)) == self.bait_vnum and int(player.GetItemCount(slot)) > 0:
                    self.bait_slot = slot
                    return slot
        except Exception:
            pass
        return -1

    def _bait_count(self):
        slot = self.FindBaitSlot()
        if slot < 0:
            return 0
        try:
            return int(player.GetItemCount(slot))
        except Exception:
            return 0

    def Open(self):
        self.window.Open()

    def Start(self):
        if self.running:
            return
        # Fishing and the Metin route cannot safely control the character at
        # the same time. Stop the active F8 Metin route before fishing starts.
        try:
            if self.parent and getattr(self.parent, "_RespawnDialog__metinFarmRunning", False):
                self.parent.StopMetinFarm()
        except Exception:
            pass
        slot = self.FindBaitSlot()
        skill_slot = self.FindFishingSkillSlot()
        if slot < 0 or self._bait_count() <= 0:
            self._log("Brak wybranej przynęty w EQ.")
            self.window.Refresh()
            return
        if skill_slot < 0:
            self._log("Przeciągnij skill Łowienie z okna V do pola skilla.")
            self.window.Refresh()
            return
        try:
            self.reel_min_ms = max(0, min(5000, int(self.window.minEdit.GetText())))
            self.reel_max_ms = max(self.reel_min_ms, min(5000, int(self.window.maxEdit.GetText())))
            self._save_config()
        except Exception:
            pass
        if not self._init_native_dll():
            self.window.SetStatus("BŁĄD DLL")
            self.window.SetDebug("FishNative.dll nie jest załadowany")
            self._log("BŁĄD: FishNative.dll nie jest załadowany do procesu.")
            return
        self._sync_native_event_cursor()

        self.running = True
        self.attempts = 0
        self.caught = 0
        self.failed = 0
        self.window.RefreshStats(self.attempts, self.caught, self.failed)
        self.state = self.STATE_USE_BAIT
        self.state_at = app.GetTime()
        self.required_space = 0
        self.space_left = 0
        self.reel_uses_done = 0
        self.next_reel_at = 0.0
        self.last_instruction_count = 0
        self.last_instruction_at = 0.0
        self.last_result_at = 0.0
        self.result_watch_until = 0.0
        self.window.SetStatus("START")
        self._log("Start Auto Fish.")

    def Stop(self):
        if not self.running:
            return
        self.running = False
        self.state = self.STATE_IDLE
        self.required_space = 0
        self.space_left = 0
        self.reel_uses_done = 0
        self.next_reel_at = 0.0
        self.last_instruction_count = 0
        self.last_instruction_at = 0.0
        self.result_watch_until = 0.0
        try:
            player.OnKeyUp(app.DIK_SPACE)
        except Exception:
            pass
        try:
            player.SetAttackKeyState(False)
        except Exception:
            pass
        self.window.SetStatus("OFF")
        self._log("Stop Auto Fish.")

    def _use_bait(self):
        slot = self.FindBaitSlot()
        if slot < 0 or self._bait_count() <= 0:
            self._log("Przynęta się skończyła. Bot zatrzymany.")
            self.Stop()
            return
        try:
            self.attempts += 1
            self.window.RefreshStats(self.attempts, self.caught, self.failed)
            self.window.SetDebug("PRÓBA #%d: używam przynęty EQ=%d" % (self.attempts, slot))
            self._log("PRÓBA #%d: używam przynęty slot=%d vnum=%d." % (self.attempts, slot, self.bait_vnum))
            net.SendItemUsePacket(slot)
            self.state = self.STATE_CAST
            self.state_at = app.GetTime() + BAIT_USE_DELAY
            self.window.SetStatus("Używam przynęty")
        except Exception as exc:
            self._log("Błąd użycia przynęty: %s" % exc)
            self.state_at = app.GetTime() + 1.0

    def _cast_rod(self):
        now = app.GetTime()
        if now < self.state_at:
            return
        if self.FindFishingSkillSlot() < 0:
            self._log("Brak skilla Łowienie. Bot zatrzymany.")
            self.Stop()
            return
        if not self._click_fishing_skill():
            self.state = self.STATE_USE_BAIT
            self.state_at = now + 1.0
            return
        self.state = self.STATE_WAIT_BITE
        self.state_at = now + CAST_DELAY
        self.bite_deadline = now + BITE_TIMEOUT
        self.window.SetStatus("Zarzucam skill Łowienie")
        self.window.SetDebug("ZARZUT: skill Łowienie x1")
        self._log("ZARZUT: użyłem skilla Łowienie x1, slot=%d." % self.FindFishingSkillSlot())

    def _finish_cast(self):
        self.window.SetStatus("Czekam na branie")

    def _press_space_once(self):
        try:
            on_down = getattr(player, "OnKeyDown", None)
            on_up = getattr(player, "OnKeyUp", None)
            if on_down is None or on_up is None:
                self._log("BŁĄD: player.OnKeyDown/OnKeyUp nie jest dostępne.")
                return False
            on_down(app.DIK_SPACE)
            on_up(app.DIK_SPACE)
            return True
        except Exception as exc:
            self._log("BŁĄD SPACE: %s" % exc)
            return False

    def _use_reel_skill(self):
        now = app.GetTime()
        if now < self.next_reel_at:
            return

        # Never guess. The DLL must provide exactly 2 or 3.
        if self.required_space not in (2, 3):
            if self.result_watch_until > 0 and now >= self.result_watch_until:
                self._fishing_result("Brak FISHING_COUNT z FishNative.dll")
            return

        target = int(self.required_space)
        if self.reel_uses_done >= target:
            self.state = self.STATE_RESULT
            self.result_at = now + 0.10
            return

        if not self._press_space_once():
            self._fishing_result("Nie udało się nacisnąć SPACE")
            return

        self.reel_uses_done += 1
        self.space_left = max(0, target - self.reel_uses_done)
        self.window.SetStatus("BRANIE -> SPACE %d/%d" % (self.reel_uses_done, target))
        delay_ms = random.randint(int(self.reel_min_ms), int(self.reel_max_ms))
        self.next_reel_at = now + (float(delay_ms) / 1000.0)
        self._log("FISHING_COUNT=%d | SPACE %d/%d | następne za %d ms." % (target, self.reel_uses_done, target, delay_ms))

    def Tick(self):
        if not self.running:
            return
        self._poll_native_fishing_event()
        now = app.GetTime()
        try:
            if self.state == self.STATE_USE_BAIT:
                if now >= self.state_at:
                    self._use_bait()
                return
            if self.state == self.STATE_CAST:
                self._cast_rod()
                return
            if self.state == self.STATE_WAIT_BITE:
                if now >= self.state_at:
                    self._finish_cast()
                if now >= self.bite_deadline:
                    self._log("Brak sygnału brania, ponawiam cykl.")
                    self.state = self.STATE_USE_BAIT
                    self.state_at = now + 1.0
                return
            if self.state == self.STATE_REEL_SKILL:
                self._use_reel_skill()
                return
            if self.state == self.STATE_RESULT:
                if now >= self.result_at:
                    self.required_space = 0
                    self.space_left = 0
                    self.result_watch_until = 0.0
                    self.state = self.STATE_USE_BAIT
                    self.state_at = now
                    self.window.SetStatus("Gotowy -> zakładam przynętę")
                return
        except Exception as exc:
            self._log("Błąd Auto Fish: %s" % exc)
            self.state = self.STATE_USE_BAIT
            self.state_at = now + 1.0

    def Destroy(self):
        global _ACTIVE_CONTROLLER
        self.Stop()
        if _ACTIVE_CONTROLLER is self:
            _ACTIVE_CONTROLLER = None
        try:
            self.window.Hide()
        except Exception:
            pass
        self.window = None
