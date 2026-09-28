# -*- coding: utf-8 -*-
"""Independent skill selector/controller for F8 Auto Farm.

Reads the same player skill slots used by the character window (V), but does
not reuse Auto Hunt/localAutoHunt state. Selected skills are controlled only by
F8 Farma.
"""
import app
import chat
import net
import player
import skill
import ui


class FarmSkillWindow(ui.ScriptWindow):
    ROW_H = 43
    MAX_SCAN_SLOTS = 96

    def __init__(self, owner=None):
        ui.ScriptWindow.__init__(self)
        self.owner = owner
        self.rows = []
        self.selected = {}
        self.remount_at = 0.0
        self.remount_pending = False
        self.was_mounted = False
        self.pending_skill_slot = -1
        self.pending_skill_idx = 0
        self.last_mount_command = -9999.0
        self.remount_deadline = 0.0
        self.last_cast = {}
        self.SetSize(330, 360)
        self.SetPosition(500, 180)
        self.SetTitleName("Auto Skille F8") if hasattr(self, "SetTitleName") else None
        self._build()
        self.RefreshSkills()
        self.Hide()

    def _build(self):
        self.board = ui.BoardWithTitleBar()
        self.board.SetParent(self)
        self.board.SetSize(330, 360)
        self.board.SetPosition(0, 0)
        self.board.SetTitleName("Auto Skille F8")
        self.board.SetCloseEvent(ui.__mem_func__(self.Hide))
        self.board.Show()

        self.info = ui.TextLine()
        self.info.SetParent(self.board)
        self.info.SetPosition(12, 30)
        self.info.SetText("Skile z okna V. Zaznacz te, ktore Farma ma uzywac.")
        self.info.Show()

        self.refreshBtn = ui.Button()
        self.refreshBtn.SetParent(self.board)
        self.refreshBtn.SetPosition(12, 52)
        self.refreshBtn.SetUpVisual("d:/ymir work/ui/public/middle_button_01.sub")
        self.refreshBtn.SetOverVisual("d:/ymir work/ui/public/middle_button_02.sub")
        self.refreshBtn.SetDownVisual("d:/ymir work/ui/public/middle_button_03.sub")
        self.refreshBtn.SetText("Odswiez skile")
        self.refreshBtn.SetEvent(ui.__mem_func__(self.RefreshSkills))
        self.refreshBtn.Show()

        self.status = ui.TextLine()
        self.status.SetParent(self.board)
        self.status.SetPosition(150, 58)
        self.status.SetText("Wybrano: 0")
        self.status.Show()

        self.rows_board = ui.Window()
        self.rows_board.SetParent(self.board)
        self.rows_board.SetPosition(8, 82)
        self.rows_board.SetSize(314, 265)
        self.rows_board.Show()

    def _skill_type_allowed(self, skill_index):
        try:
            st = skill.GetSkillType(int(skill_index))
            passive = getattr(skill, "SKILL_TYPE_PASSIVE", -9999)
            guild = getattr(skill, "SKILL_TYPE_GUILD", -9998)
            return st not in (passive, guild)
        except Exception:
            return True

    def _collect_skills(self):
        result = []
        riding = getattr(player, "SKILL_INDEX_RIDING", -99999)
        seen = set()
        for slot in range(self.MAX_SCAN_SLOTS):
            try:
                idx = int(player.GetSkillIndex(slot))
                level = int(player.GetSkillLevel(slot))
            except Exception:
                continue
            if idx <= 0 or level <= 0 or idx in seen:
                continue
            if idx == riding:
                continue
            if not self._skill_type_allowed(idx):
                continue
            seen.add(idx)
            try:
                name = skill.GetSkillName(idx)
            except Exception:
                name = "Skill %d" % idx
            result.append((slot, idx, level, name))
        return result

    def RefreshSkills(self):
        for row in self.rows:
            try:
                row[0].Hide()
                row[1].Hide()
                row[2].Hide()
                row[3].Hide()
            except Exception:
                pass
        self.rows = []

        skills = self._collect_skills()
        y = 0
        for slot, idx, level, name in skills:
            icon = ui.SlotWindow()
            icon.SetParent(self.rows_board)
            icon.SetPosition(0, y)
            icon.SetSize(40, 40)
            icon.AppendSlot(0, 0, 0, 40, 40)
            try:
                grade = int(player.GetSkillGrade(slot))
            except Exception:
                grade = 0
            try:
                icon.SetSkillSlotNew(0, idx, grade, level)
            except Exception:
                pass
            icon.Show()

            label = ui.TextLine()
            label.SetParent(self.rows_board)
            label.SetPosition(48, y + 5)
            label.SetText("%s  [slot %d]" % (name, slot))
            label.Show()

            box = ui.RespCheckBox()
            box.SetParent(self.rows_board)
            box.SetPosition(274, y + 8)
            box.SetEvent(ui.__mem_func__(lambda s=slot: self._toggle_slot(s)))
            box.SetUncheckEvent(ui.__mem_func__(lambda s=slot: self._toggle_slot(s)))
            box.SetCheck(bool(self.selected.get(slot, False)))
            box.Show()

            self.rows.append((icon, label, box, slot, idx, name))
            y += self.ROW_H
            if y >= 258:
                break

        self._refresh_status()

    def _toggle_slot(self, slot):
        for row in self.rows:
            if row[3] == slot:
                self.selected[slot] = bool(row[2].IsChecked())
                break
        self._refresh_status()
        self._save_config()

    def _refresh_status(self):
        count = len([x for x in self.selected.values() if x])
        self.status.SetText("Wybrano: %d" % count)

    def Open(self):
        self.RefreshSkills()
        self.Show()
        self.SetTop()

    def GetSelectedSlots(self):
        return [int(slot) for slot, enabled in self.selected.items() if enabled]

    def _save_config(self):
        try:
            cfg = dict(getattr(constInfo, "F8_FARM_SKILL_CONFIG", {}))
        except Exception:
            cfg = {}
        cfg["slots"] = self.GetSelectedSlots()
        try:
            import constInfo
            constInfo.F8_FARM_SKILL_CONFIG = cfg
        except Exception:
            pass

    def GetConfig(self):
        return self.GetSelectedSlots()

    def LoadConfig(self, slots):
        self.selected = {}
        for slot in slots or []:
            try:
                self.selected[int(slot)] = True
            except Exception:
                pass
        self._refresh_status()

    def _can_cast(self, slot):
        try:
            idx = int(player.GetSkillIndex(slot))
            if idx <= 0 or int(player.GetSkillLevel(slot)) <= 0:
                return False, idx
            if player.IsSkillCoolTime(slot):
                return False, idx
            if not skill.CanUseSkill(idx):
                return False, idx
            return True, idx
        except Exception:
            return False, 0

    def Tick(self, farm_running=True, force=True):
        """Run F8 skills independently of whether the selector window is open.

        If a selected skill requires dismounting, the skill is queued, the
        player is dismounted, the skill is activated after the dismount has
        settled, and the horse ride command is retried until mounting succeeds.
        """
        if not farm_running:
            return

        # This controller is intentionally independent from the visibility of
        # the F8 skill-selection window. Closing the window must NOT stop the
        # already selected skills.
        now = app.GetTime()

        # A skill may be waiting for the dismount to finish. Do not try to cast
        # it while the character is still mounted.
        if self.pending_skill_slot >= 0:
            try:
                mounted = bool(player.IsMountingHorse())
            except Exception:
                mounted = False
            if mounted:
                return

            if now < self.remount_at:
                return

            slot = int(self.pending_skill_slot)
            self.pending_skill_slot = -1
            idx = int(self.pending_skill_idx)
            self.pending_skill_idx = 0
            try:
                if idx > 0:
                    player.ClickSkillSlot(slot)
                    self.last_cast[slot] = now
                    chat.AppendChat(chat.CHAT_TYPE_INFO, "[F8 Farma] Uzywam skilla: %s" % skill.GetSkillName(idx))
                    # A skill can move the character away from the Metin.
                    # Immediately ask the F8 controller to correct position
                    # and face the current target again.
                    try:
                        if self.owner and hasattr(self.owner, "_farm_skill_used_reposition"):
                            self.owner._farm_skill_used_reposition()
                    except Exception:
                        pass
                    if self.was_mounted:
                        self.remount_pending = True
                        self.remount_at = now + 0.75
                        self.remount_deadline = now + 8.0
                        self.last_mount_command = -9999.0
                    else:
                        self.was_mounted = False
                    return
            except Exception:
                pass
            # If casting failed, allow the normal selection loop to retry.

        # Retry mounting. The old implementation sent the ride command only
        # once, which could be lost while the server was still processing the
        # skill/dismount packet.
        if self.remount_pending:
            try:
                mounted = bool(player.IsMountingHorse())
            except Exception:
                mounted = False

            if mounted:
                self.remount_pending = False
                self.was_mounted = False
                self.remount_deadline = 0.0
            else:
                # The horse command can be lost while the skill packet is
                # being processed. Retry it until the native horse state is
                # actually back, rather than assuming one command succeeded.
                if now >= self.remount_at and now - float(self.last_mount_command) >= 0.65:
                    try:
                        net.SendChatPacket('/user_horse_ride')
                        self.last_mount_command = now
                    except Exception:
                        pass
                    if self.remount_deadline <= 0.0:
                        self.remount_deadline = now + 8.0
                if self.remount_deadline > 0.0 and now < self.remount_deadline:
                    return
                # If the horse still did not mount after the retry window,
                # clear the state so a later skill cycle can try again.
                if self.remount_deadline > 0.0 and now >= self.remount_deadline:
                    self.remount_pending = False
                    self.was_mounted = False
                    self.remount_deadline = 0.0

        for slot in self.GetSelectedSlots():
            if now - float(self.last_cast.get(slot, -9999.0)) < 0.25:
                continue
            can_cast, idx = self._can_cast(slot)
            if not can_cast:
                continue

            try:
                is_active = bool(player.IsSkillActive(slot))
            except Exception:
                is_active = False

            try:
                if skill.IsToggleSkill(idx):
                    is_attack = False
                else:
                    st = skill.GetSkillType(idx)
                    active_type = getattr(skill, "SKILL_TYPE_ACTIVE", -9999)
                    is_attack = (st == active_type)
            except Exception:
                is_attack = True

            if not is_attack and is_active:
                continue

            if is_attack:
                try:
                    if int(player.GetTargetVID()) <= 0:
                        continue
                except Exception:
                    continue

            try:
                mounted = bool(player.IsMountingHorse())
            except Exception:
                mounted = False

            if mounted:
                # Queue the skill and wait for the dismount before activating
                # it. This fixes the race where ClickSkillSlot was called in
                # the same frame as /unmount.
                try:
                    net.SendChatPacket('/unmount')
                except Exception:
                    continue
                self.was_mounted = True
                self.pending_skill_slot = int(slot)
                self.pending_skill_idx = int(idx)
                self.remount_at = now + 0.75
                return

            try:
                player.ClickSkillSlot(int(slot))
                self.last_cast[slot] = now
                chat.AppendChat(chat.CHAT_TYPE_INFO, "[F8 Farma] Uzywam skilla: %s" % skill.GetSkillName(idx))
                return
            except Exception:
                continue


def GetConfig():
    try:
        import constInfo
        cfg = getattr(constInfo, "F8_FARM_SKILL_CONFIG", {})
        return list(cfg.get("slots", [])) if isinstance(cfg, dict) else []
    except Exception:
        return []
