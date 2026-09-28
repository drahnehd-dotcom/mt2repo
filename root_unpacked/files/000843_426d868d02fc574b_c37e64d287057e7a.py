"""Respawn dialog - boss/metin tracking, teleportation, and drop info."""

import math
import os

import app
import background
import dbg
import item
import localeInfo
import net
import nonplayer
import renderTarget
import constInfo
import settings
import uiChestDropInfo
import exception

import json
import io

import ui

ROOT_PATH = "d:/ymir work/ui/game/resp/"
RESP_WAIT_TEXT_COLOR = 0xffbb8585
RESP_AVAILABLE_TEXT_COLOR = 0xff85bb99
TOOLTIP_TITLE_TEXT_COLOR = 0xffd4c39f
CONFIG_FILENAME = "lib/respdialop.pcl"
RESP_SLOT_COUNT = 10

TOOLTIP_TEXT_DICT = {
    "HEADER_MOB": {
        "title": localeInfo.RESP_MOB_TITLE,
        "text": localeInfo.RESP_MOB_TEXT,
    },
    "HEADER_RESP": {
        "title": localeInfo.RESP_RESP_TITLE,
        "text": localeInfo.RESP_RESP_TEXT,
    },
    "DROP_BUTTON": {
        "title": localeInfo.RESP_DROP_TITLE,
        "text": localeInfo.RESP_DROP_TEXT,
    },
}

RACE_FLAG_DICT = {
    nonplayer.RACE_FLAG_ANIMAL: localeInfo.TARGET_RACE_FLAG_ANIMAL,
    nonplayer.RACE_FLAG_UNDEAD: localeInfo.TARGET_RACE_FLAG_UNDEAD,
    nonplayer.RACE_FLAG_DEVIL: localeInfo.TARGET_RACE_FLAG_DEVIL,
    nonplayer.RACE_FLAG_HUMAN: localeInfo.TARGET_RACE_FLAG_HUMAN,
    nonplayer.RACE_FLAG_ORC: localeInfo.TARGET_RACE_FLAG_ORC,
    nonplayer.RACE_FLAG_MILGYO: localeInfo.TARGET_RACE_FLAG_MILGYO,
    nonplayer.RACE_FLAG_INSECT: localeInfo.TARGET_RACE_FLAG_INSECT,
    nonplayer.RACE_FLAG_FIRE: localeInfo.TARGET_RACE_FLAG_FIRE,
    nonplayer.RACE_FLAG_ICE: localeInfo.TARGET_RACE_FLAG_ICE,
    nonplayer.RACE_FLAG_DESERT: localeInfo.TARGET_RACE_FLAG_DESERT,
    nonplayer.RACE_FLAG_TREE: localeInfo.TARGET_RACE_FLAG_TREE,
}

log = dbg.TraceError


class RespawnDialog(ui.ScriptWindow):
    """Main respawn tracking dialog with mob list, drop info, and teleport."""

    class Grid:
        """2D grid for tracking item slot occupancy."""

        def __init__(self, width, height):
            self.grid = [False] * (width * height)
            self.width = width
            self.height = height

        def __str__(self):
            output = "Grid {}x{} Information\n".format(self.width, self.height)
            for row in range(self.height):
                for col in range(self.width):
                    idx = row * self.width + col
                    status = "NotEmpty" if self.grid[idx] else "Empty"
                    output += "Status of %d: %s, " % (idx, status)
                output += "\n"
            return output

        def find_blank(self, width, height):
            if width > self.width or height > self.height:
                return -1
            for row in range(self.height):
                for col in range(self.width):
                    index = row * self.width + col
                    if self.is_empty(index, width, height):
                        return index
            return -1

        def put(self, pos, width, height):
            if not self.is_empty(pos, width, height):
                return False
            for row in range(height):
                start = pos + row * self.width
                for col in range(width):
                    self.grid[start + col] = True
            return True

        def clear(self, pos, width, height):
            if pos < 0 or pos >= self.width * self.height:
                return
            for row in range(height):
                start = pos + row * self.width
                for col in range(width):
                    self.grid[start + col] = False

        def is_empty(self, pos, width, height):
            if pos < 0:
                return False
            row = pos // self.width
            if row + height > self.height:
                return False
            if pos + width > row * self.width + self.width:
                return False
            for r in range(height):
                start = pos + r * self.width
                for c in range(width):
                    if self.grid[start + c]:
                        return False
            return True

        def get_size(self):
            return self.width * self.height

        def reset(self):
            self.grid = [False] * (self.width * self.height)

    class MobButton(ui.NewListBoxItem, ui.ExpandedButton):
        """Button representing a mob in the list."""

        def __init__(self, vnum):
            ui.NewListBoxItem.__init__(self)
            ui.ExpandedButton.__init__(self)
            self.event = {"over_in": None, "over_out": None}
            self.OnRender = None
            self.RegisterComponent(self)
            self.vnum = vnum

        def __del__(self):
            self.UnregisterComponent(self)
            ui.NewListBoxItem.__del__(self)
            ui.ExpandedButton.__del__(self)

        def OnMouseOverIn(self):
            ui.ExpandedButton.OnMouseOverIn(self)
            self.event["over_in"](self.vnum)

        def OnMouseOverOut(self):
            ui.ExpandedButton.OnMouseOverOut(self)
            self.event["over_out"]()

    def __init__(self):
        self.__wndRenderTargetWnd = None
        self.__wndRenderMapWnd = None
        ui.ScriptWindow.__init__(self)
        self.__pageCount = {page: {"max": 0, "now": 0} for page in ("resp", "drop")}
        self.chestdropinfo = uiChestDropInfo.ChestDropInfoWindow()
        self.__dropDataDict = {}
        self.__respDataDict = {}
        self.__mobVnum = 0
        self.__itemToolTip = None
        self.__lastUpdate = app.GetTime()
        self._load_window()
        self._load_data()

    def __del__(self):
        ui.ScriptWindow.__del__(self)

    def _load_window(self):
        """Load UI script and bind all components."""
        pythonScriptLoader = ui.PythonScriptLoader()
        pythonScriptLoader.LoadScriptFile(self, "uiscript/respawndialog.py")

        self.board = self.GetChild("board")
        self.dropButton = self.GetChild("drop_button")
        self.dropSlot = self.GetChild("drop_slot")
        self.slotCount = self.dropSlot.GetSlotCount()

        self.dropWnd = self.GetChild("drop_window")
        self.respWnd = self.GetChild("resp_window")

        self.leftButton = self.GetChild("left_button")
        self.rightButton = self.GetChild("right_button")
        self.pageCountValue = self.GetChild("page_count_value")

        self.headerRespText = self.GetChild("header_resp_text")
        self.badgeTimeValue = self.GetChild("badge_time_value")
        self.badgeLevelValue = self.GetChild("badge_level_value")
        self.badgeAffectValue = self.GetChild("badge_affect_value")

        self.headerMobCheckbox = self.GetChild("header_mob_checkbox")
        self.headerRespCheckbox = self.GetChild("header_resp_checkbox")

        self.loadingBar = self.GetChild("loading_bar")
        self.OpenWhenTeleportButton = self.GetChild("OpenWhenTeleportButton")

        self.respSlotList = [
            {
                "slot": self.GetChild("resp_slot_%02d" % (i + 1)),
                "count": self.GetChild("count_value_%02d" % (i + 1)),
                "time": self.GetChild("time_value_%02d" % (i + 1)),
                "cord": self.GetChild("cord_value_%02d" % (i + 1)),
                "button": self.GetChild("teleport_button_%02d" % (i + 1)),
                "time_value": 0,
            } for i in range(RESP_SLOT_COUNT)
        ]

        self.infoWndDict = {
            "HEADER_MOB": self.GetChild("header_mob_wnd"),
            "HEADER_RESP": self.GetChild("header_resp_wnd"),
            "DROP_BUTTON": self.GetChild("drop_button"),
        }

        self.respErrorText = self.GetChild("resp_error_text")

        self.listBox = ui.NewListBox()
        self.listBox.SetParent(self.GetChild("mob_board"))
        self.listBox.SetPosition(7, 28)
        self.listBox.SetSize(180, 305)
        self.listBox.itemStep = 3
        self.listBox.Show()

        self.board.SetCloseEvent(ui.__mem_func__(self.Hide))
        self.dropButton.SetEvent(ui.__mem_func__(self._on_click_drop_button))
        self.dropSlot.SetOverInItemEvent(ui.__mem_func__(self._on_over_in_item))
        self.dropSlot.SetOverOutItemEvent(ui.__mem_func__(self._on_over_out_item))
        self.dropSlot.SAFE_SetButtonEvent("RIGHT", "EXIST", self.UseSlotEvent)

        self.leftButton.SetEvent(ui.__mem_func__(self._on_click_left_button))
        self.rightButton.SetEvent(ui.__mem_func__(self._on_click_right_button))

        self.OpenWhenTeleportButton.SetToggleUpEvent(ui.__mem_func__(self._on_click_enable_fast_open))
        self.OpenWhenTeleportButton.SetToggleDownEvent(ui.__mem_func__(self._on_click_enable_fast_open))

        for i, respSlot in enumerate(self.respSlotList):
            respSlot["button"].SetEvent(ui.__mem_func__(self.OnClickTeleportButton), i)
            respSlot["button"].ShowToolTip = lambda arg=i: self.OnOverInTeleportButton(arg)
            respSlot["button"].HideToolTip = self.OnOverOutTeleportButton

        for key, wnd in self.infoWndDict.items():
            if type(wnd).__name__ == "Button":
                wnd.ShowToolTip = lambda arg=key: self.OnOverInInfo(arg)
                wnd.HideToolTip = self.OnOverOutInfo
            else:
                wnd.OnMouseOverIn = lambda arg=key: self.OnOverInInfo(arg)
                wnd.OnMouseOverOut = self.OnOverOutInfo

        self.dropButton.CallEvent()

        self.__wndRenderMapWnd = RenderMapDialog()
        self.__wndRenderMapWnd.Hide()

        self.__wndRenderTargetWnd = RenderTargetDialog()
        self.__wndRenderTargetWnd.Hide()

        self.OnMoveWindow(*self.GetGlobalPosition())

        if settings.remember_boss_tp_window:
            self.OpenWhenTeleportButton.Down()

    def _on_click_enable_fast_open(self):
        settings.remember_boss_tp_window = not settings.remember_boss_tp_window

    def _set_loading(self, state):
        if state:
            self.loadingBar.Show()
        else:
            self.loadingBar.Hide()

    def UseSlotEvent(self, selectedSlotPos):
        """Handle right-click on drop slot for chest drop info."""
        drop_dict = self.__dropDataDict.get(self.__mobVnum)
        if not drop_dict:
            return

        global_pos = self._local_slot_to_global(selectedSlotPos)
        item.SelectItem(drop_dict[global_pos]["vnum"])
        if item.GetItemType() in (item.GIFTBOX, item.GACHA):
            if app.IsPressed(app.DIK_LCONTROL):
                isMain = not app.IsPressed(app.DIK_LSHIFT)
                if item.HasDropInfo(drop_dict[global_pos]["vnum"], isMain):
                    self.chestdropinfo.Open(drop_dict[global_pos]["vnum"], isMain)

    @property
    def _current_page(self):
        return "drop" if self.dropWnd.IsShow() else "resp"

    def _local_slot_to_global(self, slotIndex):
        if self._current_page == "drop":
            return slotIndex + self.slotCount * self.__pageCount["drop"]["now"]
        return slotIndex + len(self.respSlotList) * self.__pageCount["resp"]["now"]

    def _global_slot_to_local(self, slotIndex):
        if self._current_page == "drop":
            return slotIndex % self.slotCount
        return slotIndex % len(self.respSlotList)

    def _refresh_drop_slot(self):
        """Refresh item drop display slots."""
        if self._current_page != "drop":
            return True

        drop_data = self.__dropDataDict.get(self.__mobVnum)
        if not drop_data:
            for i in range(self.slotCount):
                self.dropSlot.ClearSlot(i)
            self.dropSlot.RefreshSlot()
            self.__pageCount["drop"]["now"] = 0
            self.__pageCount["drop"]["max"] = 1
            if self.__mobVnum:
                net.SendRespFetchDropPacket(self.__mobVnum)
                return False
            return True

        maxPage = int(math.ceil(float(max(drop_data.keys())) / float(self.slotCount)))
        self.__pageCount["drop"]["max"] = maxPage

        start = self._local_slot_to_global(0)
        end = self._local_slot_to_global(self.slotCount)
        data_sliced = {k: drop_data.get(k, {"vnum": 0, "count": 0}) for k in range(start, end)}

        for slotIndex, itemData in data_sliced.items():
            local = self._global_slot_to_local(slotIndex)
            if not itemData["vnum"]:
                self.dropSlot.ClearSlot(local)
                continue
            self.dropSlot.SetItemSlot(
                local, itemData["vnum"],
                itemData["count"] if itemData["count"] > 1 else 0,
            )

        self.dropSlot.RefreshSlot()
        self._refresh_page_button()
        return True

    def _refresh_resp_slot(self):
        """Refresh respawn slot display."""
        if self._current_page != "resp":
            return True

        resp_data = self.__respDataDict.get(self.__mobVnum)
        if not resp_data:
            for respSlot in self.respSlotList:
                respSlot["slot"].Hide()
            self.respErrorText.Show()
            self.__pageCount["resp"]["now"] = 0
            self.__pageCount["resp"]["max"] = 1
            if self.__mobVnum:
                net.SendRespFetchRespPacket(self.__mobVnum)
                return False
            return True

        self.respErrorText.Hide()
        maxPage = int(math.ceil(float(len(resp_data)) / float(len(self.respSlotList))))
        self.__pageCount["resp"]["max"] = maxPage

        start = self._local_slot_to_global(0)
        end = self._local_slot_to_global(len(self.respSlotList))
        data_sliced = resp_data[start:end]

        for respSlot in self.respSlotList:
            respSlot["slot"].Hide()

        for i, respData in enumerate(data_sliced):
            xPos, yPos = respData["cord"]
            _, xBase, yBase = background.GlobalPositionToMapInfo(xPos, yPos)

            xPoint = str(int(xPos - xBase))[:-2]
            yPoint = str(int(yPos - yBase))[:-2]

            respSlot = self.respSlotList[i]
            respSlot["slot"].Show()
            respSlot["count"].SetText(str(self._local_slot_to_global(i) + 1))
            respSlot["cord"].SetText("({}, {})".format(xPoint, yPoint))
            respSlot["time_value"] = respData["resp"]

        self._refresh_page_button()
        return True

    def _refresh_resp_time(self):
        resp_data = self.__respDataDict.get(self.__mobVnum)
        if not resp_data:
            return

        times = [data["time"] for data in resp_data]
        if all(val == times[0] for val in times):
            self.badgeTimeValue.SetText(self._format_time_short(times[0]))
        else:
            self.badgeTimeValue.SetText("{}-{}".format(
                self._format_time_short(min(times)),
                self._format_time_short(max(times)),
            ))

    def _refresh_level(self):
        # Level range intentionally hidden — always show "---" regardless of mob.
        self.badgeLevelValue.SetText("---")

    def _refresh_affect(self):
        data = nonplayer.GetAttElementFlag(self.__mobVnum)
        if data >= 0:
            flags = [text for flag, text in RACE_FLAG_DICT.items() if data & flag]
            self.badgeAffectValue.SetText(", ".join(flags) or "-")
        else:
            self.badgeAffectValue.SetText("-")

    @staticmethod
    def _format_time(seconds):
        h, r = divmod(seconds, 3600)
        m, s = divmod(r, 60)
        return "{:02d}:{:02d}:{:02d}".format(h, m, s)

    @staticmethod
    def _format_time_short(seconds):
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)
        parts = ""
        if h:
            parts += "{}h ".format(h)
        if m or h:
            parts += "{}m ".format(m)
        if (not h and not m) or s:
            parts += "{}s".format(s)
        return parts

    def _load_data(self):
        """Load saved checkbox configuration."""
        if os.path.exists(CONFIG_FILENAME):
            file = io.open(CONFIG_FILENAME, "r", encoding="utf-8")
            try:
                data = json.load(file)
                for key, value in data.items():
                    self.GetChild(key).SetCheck(value)
            except (ValueError, EOFError, TypeError, Exception):
                pass
            file.close()

    def _save_data(self):
        """Save checkbox configuration."""
        data = {}
        for key, obj in self.ElementDictionary.items():
            if key.find("checkbox") >= 0:
                data[key] = obj.IsChecked()
        file = io.open(CONFIG_FILENAME, "w", encoding="utf-8")
        file.write(json.dumps(data))
        file.close()

    def _refresh_page_button(self):
        curPage = self._current_page
        nowPage = self.__pageCount[curPage]["now"]
        maxPage = self.__pageCount[curPage]["max"]

        if nowPage < 1:
            self.leftButton.Disable()
        else:
            self.leftButton.Enable()

        if nowPage + 1 >= maxPage:
            self.rightButton.Disable()
        else:
            self.rightButton.Enable()

        self.pageCountValue.SetText(
            localeInfo.RESP_PAGE_COUNT % (nowPage + 1, max(maxPage, 1)))

    def _on_click_drop_button(self):
        self._set_loading(True)
        if self.dropWnd.IsShow():
            self.dropWnd.Hide()
            self.respWnd.Show()
        else:
            self.dropWnd.Show()
            self.respWnd.Hide()

        if self._refresh_resp_slot() and self._refresh_drop_slot():
            self._set_loading(False)

        self._refresh_resp_time()
        self._refresh_level()
        self._refresh_affect()

    def _on_over_in_item(self, slotIndex):
        if not self.__itemToolTip:
            return
        drop_dict = self.__dropDataDict.get(self.__mobVnum)
        if not drop_dict:
            return
        self.__itemToolTip.SetItemToolTip(drop_dict[self._local_slot_to_global(slotIndex)]["vnum"])

    def _on_over_out_item(self):
        if self.__itemToolTip:
            self.__itemToolTip.ClearToolTip()
            self.__itemToolTip.HideToolTip()

    def OnOverInInfo(self, index):
        if not self.__itemToolTip:
            return
        self.__itemToolTip.ClearToolTip()
        self.__itemToolTip.SetCannotUseItemForceSetDisableColor(False)
        text = TOOLTIP_TEXT_DICT.get(index)
        if text:
            self.__itemToolTip.SetDefaultFontName(localeInfo.UI_DEF_FONT + "b")
            self.__itemToolTip.AppendTextLine(text["title"], TOOLTIP_TITLE_TEXT_COLOR)
            self.__itemToolTip.SetDefaultFontName(localeInfo.UI_DEF_FONT)
            self.__itemToolTip.AppendDescription(text["text"], 26)
        self.__itemToolTip.ShowToolTip()
        self.__itemToolTip.SetCannotUseItemForceSetDisableColor(True)

    def OnOverOutInfo(self):
        if self.__itemToolTip:
            self.__itemToolTip.ClearToolTip()
            self.__itemToolTip.HideToolTip()

    def _on_over_in_mob_button(self, mobVnum):
        if self.headerMobCheckbox.IsChecked():
            self.__wndRenderTargetWnd.Open(mobVnum)

    def _on_over_out_mob_button(self):
        self.__wndRenderTargetWnd.Close()

    def OnOverInTeleportButton(self, index):
        if not self.headerRespCheckbox.IsChecked():
            return
        resp_data = self.__respDataDict.get(self.__mobVnum)
        if not resp_data:
            return
        data = resp_data[self._local_slot_to_global(index)]
        self.__wndRenderMapWnd.Open(*data["cord"])

    def OnOverOutTeleportButton(self):
        self.__wndRenderMapWnd.Hide()

    def _on_click_left_button(self):
        curPage = self._current_page
        if self.__pageCount[curPage]["now"] < 1:
            return
        self.__pageCount[curPage]["now"] -= 1
        self._refresh_page_button()
        self._set_loading(True)
        self._refresh_drop_slot()
        self._refresh_resp_slot()
        self._set_loading(False)

    def _on_click_right_button(self):
        curPage = self._current_page
        nowPage = self.__pageCount[curPage]["now"]
        maxPage = self.__pageCount[curPage]["max"]
        if nowPage + 1 >= maxPage:
            return
        self.__pageCount[curPage]["now"] += 1
        self._refresh_page_button()
        self._set_loading(True)
        self._refresh_drop_slot()
        self._refresh_resp_slot()
        self._set_loading(False)

    def _on_click_mob_button(self, vnum):
        self._set_loading(True)
        self.__mobVnum = vnum

        for mob_item in self.listBox.items:
            if mob_item.vnum == vnum:
                mob_item.Down()
            else:
                mob_item.SetUp()

        name = nonplayer.GetMonsterName(vnum)
        level = nonplayer.GetMonsterLevel(vnum)
        self.headerRespText.SetText("{} (Lv. {})".format(name, level))

        self.__pageCount["drop"]["now"] = 0
        self.__pageCount["resp"]["now"] = 0

        if self._refresh_resp_slot() and self._refresh_drop_slot():
            self._set_loading(False)
        self._refresh_resp_time()
        self._refresh_level()
        self._refresh_affect()

    def OnClickTeleportButton(self, index):
        resp_data = self.__respDataDict.get(self.__mobVnum)
        if not resp_data:
            return
        data = resp_data[self._local_slot_to_global(index)]
        net.SendRespTeleportPacket(data["id"])

    def Show(self):
        ui.ScriptWindow.Show(self)

    def Hide(self):
        ui.ScriptWindow.Hide(self)
        if self.__wndRenderTargetWnd:
            self.__wndRenderTargetWnd.Close()
        if self.__wndRenderMapWnd:
            self.__wndRenderMapWnd.Hide()

    def OpenWindow(self):
        if self.IsShow():
            self.Hide()
        else:
            self.Show()

    def Destroy(self):
        self._save_data()
        self.ClearDictionary()
        self.listBox.ClearItems()

        self.board = None
        self.dropButton = None
        self.dropSlot = None
        self.dropWnd = None
        self.respWnd = None
        self.leftButton = None
        self.rightButton = None
        self.pageCountValue = None
        self.headerRespText = None
        self.badgeTimeValue = None
        self.badgeLevelValue = None
        self.badgeAffectValue = None
        self.headerMobCheckbox = None
        self.headerRespCheckbox = None
        self.loadingBar = None
        self.respSlotList = []
        self.infoWndDict = {}
        self.respErrorText = None
        self.listBox = None

        self.__wndRenderMapWnd.Destroy()
        del self.__wndRenderMapWnd

        self.__wndRenderTargetWnd.Destroy()
        del self.__wndRenderTargetWnd

        self.__pageCount = {}
        self.__dropDataDict = {}
        self.__respDataDict = {}
        self.__itemToolTip = None

    def OnUpdate(self):
        local_time = app.GetTime()
        if local_time - self.__lastUpdate < 0.1:
            return

        if self._current_page == "resp":
            time_now = app.GetGlobalTimeStamp()
            for respSlot in self.respSlotList:
                time_wnd = respSlot["time"]
                delta = respSlot["time_value"] - time_now
                if delta > 0:
                    time_wnd.SetPackedFontColor(RESP_WAIT_TEXT_COLOR)
                    time_wnd.SetText(self._format_time(delta))
                else:
                    time_wnd.SetPackedFontColor(RESP_AVAILABLE_TEXT_COLOR)
                    time_wnd.SetText(localeInfo.RESP_AVAILABLE)

        self.__lastUpdate = local_time

    def OnMoveWindow(self, x, y):
        self.__wndRenderTargetWnd.SetPosition(
            x - self.__wndRenderTargetWnd.GetWidth() - 5,
            y + (self.GetHeight() - self.__wndRenderTargetWnd.GetHeight()) // 2,
        )
        self.__wndRenderMapWnd.SetPosition(
            x + self.GetWidth() + 5,
            y + (self.GetHeight() - self.__wndRenderMapWnd.GetHeight()) // 2,
        )

    def OnPressEscapeKey(self):
        self.Hide()
        return True

    def SetItemToolTip(self, itemToolTip):
        self.__itemToolTip = itemToolTip

    def SetMapData(self, data, currentBossCount, maxBossCount, currentMetinCount, maxMetinCount):
        """Populate mob list from map data."""
        for vnum in sorted(data, key=lambda x: nonplayer.GetMonsterLevel(x) ** nonplayer.GetMonsterGrade(x)):
            button = self.MobButton(vnum)
            button.SetPosition(0, 0)
            button.SetUpVisual(ROOT_PATH + "mob_button_01.sub")
            button.SetOverVisual(ROOT_PATH + "mob_button_02.sub")
            button.SetDownVisual(ROOT_PATH + "mob_button_03.sub")
            button.SetEvent(ui.__mem_func__(self._on_click_mob_button), vnum)
            button.SetText(
                "{} |cffc3e0bf(Lv. {})|r".format(nonplayer.GetMonsterName(vnum), nonplayer.GetMonsterLevel(vnum)))
            button.ButtonText.SetFontName("Tahoma:12")
            button.event["over_in"] = ui.__mem_func__(self._on_over_in_mob_button)
            button.event["over_out"] = ui.__mem_func__(self._on_over_out_mob_button)
            button.Show()
            self.listBox.AppendItem(button)

    def SetMobDropData(self, vnum, data):
        """Process and store mob drop data with grid layout."""
        grid = self.Grid(8, 7)
        page = 0
        drop_list = {}

        for item_data in data:
            item.SelectItem(item_data["vnum"])
            w, h = item.GetItemSize()

            pos = grid.find_blank(w, h)
            if pos >= 0:
                grid.put(pos, w, h)
                drop_list[pos + page * self.slotCount] = item_data
            else:
                page += 1
                grid.reset()
                drop_list[page * self.slotCount] = item_data

        self.__dropDataDict.setdefault(vnum, drop_list)
        self._refresh_drop_slot()
        self._set_loading(False)

    def SetMobRespData(self, vnum, data):
        """Store mob respawn data."""
        self.__respDataDict.setdefault(vnum, data)
        self._refresh_resp_slot()
        self._set_loading(False)

    def RefreshRest(self, id, mobVnum, time, cord):
        """Update a specific respawn entry."""
        resp_data = self.__respDataDict.get(mobVnum)
        if resp_data:
            for data in resp_data:
                if data["id"] == id:
                    data["resp"] = time
                    data["cord"] = cord
                    break
            self._refresh_resp_slot()


class RenderTargetDialog(ui.ScriptWindow):
    """Window showing 3D mob preview."""

    def __init__(self):
        ui.ScriptWindow.__init__(self)
        self._load_window()

    def __del__(self):
        ui.ScriptWindow.__del__(self)

    def _load_window(self):
        try:
            pyScrLoader = ui.PythonScriptLoader()
            pyScrLoader.LoadScriptFile(self, "uiscript/respawnrendertargetdialog.py")
        except Exception:
            exception.Abort("RenderTargetDialog._load_window.LoadObject")

        self.renderTarget = self.GetChild("render_target")
        self.headerText = self.GetChild("header_render_text")
        renderTarget.SetBackground(self.renderTarget.number, ROOT_PATH + "image_render.sub")

    def Open(self, mobVnum):
        renderTarget.SelectModel(self.renderTarget.number, mobVnum)
        self.headerText.SetText(
            "%s  (Lv. %d)" % (nonplayer.GetMonsterName(mobVnum), nonplayer.GetMonsterLevel(mobVnum)))
        self.Show()
        renderTarget.SetVisibility(self.renderTarget.number, True)

    def Close(self):
        self.Hide()
        renderTarget.SetVisibility(self.renderTarget.number, False)

    def Destroy(self):
        self.ClearDictionary()
        self.renderTarget = None
        self.headerText = None


class RenderMapDialog(ui.ScriptWindow):
    """Window showing map preview with point marker."""

    def __init__(self):
        ui.ScriptWindow.__init__(self)
        self._load_window()

    def __del__(self):
        ui.ScriptWindow.__del__(self)

    def _load_window(self):
        try:
            pyScrLoader = ui.PythonScriptLoader()
            pyScrLoader.LoadScriptFile(self, "uiscript/respawnrendermapdialog.py")
        except Exception:
            exception.Abort("RenderMapDialog._load_window.LoadObject")

        self.board = self.GetChild("map_board")
        self.header = self.GetChild("header_map")
        self.mapImage = self.GetChild("map_image")
        self.headerText = self.GetChild("header_map_text")
        self.mapPoint = self.GetChild("map_point")
        self.headerWidth = self.header.GetWidth()

    def Destroy(self):
        self.ClearDictionary()
        self.board = None
        self.header = None
        self.mapImage = None
        self.headerText = None

    def Open(self, xPos, yPos):
        """Open map dialog centered on the given global position."""
        mapName, xBase, yBase = background.GlobalPositionToMapInfo(xPos, yPos)
        localeMapName = localeInfo.MINIMAP_ZONE_NAME_DICT.get(mapName, "")
        fileName = "d:/ymir work/ui/atlas/{}/atlas.sub".format(mapName)

        if not localeMapName or not app.IsExistFile(fileName):
            dbg.TraceError("test")
            return False

        self.headerText.SetText(localeMapName)
        self.mapImage.LoadImage(fileName)

        xSize = 8 + self.mapImage.GetWidth()
        ySize = 25 + 3 + self.mapImage.GetHeight()
        self.SetSize(xSize, ySize)
        self.board.SetSize(xSize, ySize)
        self.header.SetScale(float(self.mapImage.GetWidth()) / self.headerWidth, 1.0)

        xMap, yMap = background.GlobalPositionToMapSize(xPos, yPos)

        xPoint = int(xPos - xBase)
        yPoint = int(yPos - yBase)
        xPoint /= float(xMap) / float(self.mapImage.GetWidth())
        yPoint /= float(yMap) / float(self.mapImage.GetHeight())

        self.mapPoint.SetPosition(
            xPoint - self.mapPoint.GetWidth() // 4,
            yPoint - self.mapPoint.GetHeight(),
        )

        self.mapImage.Show()
        self.headerText.UpdateRect()
        self.Show()
        self.UpdateRect()
        return True

# Legacy aliases

