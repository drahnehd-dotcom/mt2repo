# -*- coding: iso-8859-1 -*-
"""Fragments/Shards crafting window."""

import ui
import exception
import player
import mouseModule
import chat
import emoji
import uiInventory
import item
import net
import uiToolTip
import constInfo
import localeInfo
from _weakref import proxy

SLOT_COUNT = 18
GRID_WIDTH = 6
GRID_HEIGHT = 3


class FragmentsWindow(ui.ScriptWindow):
    """Window for combining soul stone fragments."""

    def __init__(self):
        self.tooltipItem = None
        self.isLoaded = 0
        self.__itemPos = [[player.INVENTORY, -1] for _ in range(SLOT_COUNT)]
        self.__grid = None
        self.wndInventory = uiInventory.InventoryWindow()
        ui.ScriptWindow.__init__(self)
        self._load_window()

    def __del__(self):
        ui.ScriptWindow.__del__(self)

    def Show(self):
        ui.ScriptWindow.Show(self)

    def Open(self):
        self.Show()
        self.RefreshSlot()

    def BindInterfaceClass(self, interface):
        self.interface = interface

    def SetItemToolTip(self, itemToolTip):
        self.tooltipItem = proxy(itemToolTip)

    def _load_window(self):
        """Load and initialize the window UI."""
        if self.isLoaded:
            return

        self.isLoaded = 1
        try:
            ui.PythonScriptLoader().LoadScriptFile(self, "uiscript/fragmentswindow.py")
        except Exception:
            exception.Abort("FragmentsWindow.LoadDialog.LoadScript")

        try:
            self.titleBar = self.GetChild("TitleBar")
            self.titleBar.SetCloseEvent(ui.__mem_func__(self.Close))

            self.text = self.GetChild("fast_add")
            self.text.SetText(localeInfo.STONE_CRAFTING_QUICK_ADD.format(
                emoji.AppendEmoji("icon/emoji/key_shift.png"),
                emoji.AppendEmoji("icon/emoji/key_rclick.png"),
            ))

            self.wndItem = self.GetChild("ItemSlot")
            self.wndItem.SetSelectItemSlotEvent(ui.__mem_func__(self.SelectItemSlot))
            self.wndItem.SetUseSlotEvent(ui.__mem_func__(self.SelectItemSlot))
            self.wndItem.SetSelectEmptySlotEvent(ui.__mem_func__(self.SelectEmptySlot))
            self.wndItem.SetOverInItemEvent(ui.__mem_func__(self.OverInItem))
            self.wndItem.SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))

            self.tt = {0: uiToolTip.ToolTipNew(190)}
            self.tt[0].AppendSpace(10)
            self.tt[0].AppendTextLine(emoji.AppendEmoji("icon/emoji/28961.png"))
            self.tt[0].AppendSpace(10)
            for level, result in ((5, 2), (6, 3), (7, 4), (8, 5), (9, 6)):
                self.tt[0].AppendTextLine(localeInfo.STONE_CRAFTING_DESC.format(level, result))
                self.tt[0].AppendSpace(3)
            self.tt[0].AppendSpace(3)

            self.info = self.GetChild("info")

            self.AcceptButton = self.GetChild("AcceptButton")
            self.AcceptButton.SetEvent(ui.__mem_func__(self.Send))

            self.__grid = Grid(GRID_WIDTH, GRID_HEIGHT)
        except Exception:
            exception.Abort("FragmentsWindow.LoadDialog.BindObject")

        self.SetCenterPosition()
        self.SetTop()

    def Destroy(self):
        self.Hide()
        self.ClearDictionary()

    def Close(self):
        if self.tt[0]:
            self.tt[0].Hide()
        self.Hide()

    def OnPressEscapeKey(self):
        self.Close()
        return True

    def Hide(self):
        ui.ScriptWindow.Hide(self)
        if self.tooltipItem and self.tooltipItem.IsShow():
            self.tooltipItem.HideToolTip()

    def OnUpdate(self):
        if self.info.IsIn():
            self.tt[0].Show()
        else:
            self.tt[0].Hide()

    def OverInItem(self, slotIndex):
        if self.tooltipItem:
            self.tooltipItem.SetInventoryItem(
                self.__itemPos[slotIndex][1], self.__itemPos[slotIndex][0],
            )

    def OverOutItem(self):
        if self.tooltipItem:
            self.tooltipItem.HideToolTip()

    def SelectEmptySlot(self, slotIndex):
        if not mouseModule.mouseController.isAttached():
            return

        attachedSlotType = mouseModule.mouseController.GetAttachedType()
        attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
        attachedInvenType = player.SlotTypeToInvenType(attachedSlotType)
        mouseModule.mouseController.DeattachObject()

        if attachedSlotType not in (player.SLOT_TYPE_INVENTORY, player.SLOT_TYPE_STONE_INVENTORY):
            return

        item.SelectItem(player.GetItemIndex(attachedInvenType, attachedSlotPos))
        if item.GetItemType() != item.METIN:
            chat.AppendChat(chat.CHAT_TYPE_INFO, "Mo\xbfe\xb6z w\xb3o\xbfy\xe6 tylko kamienie dusz!")
            return

        width, height = item.GetItemSize()
        if not self.__grid.is_empty(slotIndex, width, height):
            return

        itemPos = [attachedInvenType, attachedSlotPos]
        if itemPos in self.__itemPos:
            return

        self.__itemPos[slotIndex] = itemPos
        self.__grid.put(slotIndex, width, height)
        self.RefreshSlot()

        constInfo.fragmentGrid.append([slotIndex, attachedSlotPos])
        constInfo.fragmentItems.append(attachedSlotPos)
        self.wndInventory.RefreshBagSlotWindow()

    def SelectItemSlot(self, slotIndex):
        if mouseModule.mouseController.isAttached():
            mouseModule.mouseController.DeattachObject()
            return

        item.SelectItem(mouseModule.mouseController.GetAttachedItemIndex())
        width, height = item.GetItemSize()
        self.__grid.clear(slotIndex, width, height)

        self.__itemPos[slotIndex][0] = player.INVENTORY
        self.__itemPos[slotIndex][1] = -1

        for removeGrid in constInfo.fragmentGrid:
            if slotIndex == removeGrid[0]:
                constInfo.fragmentGrid.remove(removeGrid)
                constInfo.fragmentItems.remove(removeGrid[1])
                self.wndInventory.RefreshBagSlotWindow()

        self.__grid.reset()
        self.RefreshSlot()

    def RefreshSlot(self):
        """Refresh all item slots display."""
        if not self.isLoaded:
            return

        for i in range(self.wndItem.GetSlotCount()):
            itemVnum = player.GetItemIndex(self.__itemPos[i][0], self.__itemPos[i][1])
            itemCount = player.GetItemCount(self.__itemPos[i][0], self.__itemPos[i][1])

            if not itemCount:
                self.wndItem.ClearSlot(i)
                continue

            self.wndItem.SetItemSlot(i, itemVnum, 0 if itemCount == 1 else itemCount)

        self.wndItem.RefreshSlot()

    def AppendSlot(self, wnd, cell):
        """Add an item to the next available slot."""
        itemVnum = player.GetItemIndex(wnd, cell)
        if not itemVnum:
            return

        itemPos = [wnd, cell]
        if itemPos in self.__itemPos:
            return

        item.SelectItem(itemVnum)
        width, height = item.GetItemSize()
        pos = self.__grid.find_blank(width, height)

        if pos != -1:
            self.__itemPos[pos] = itemPos
            self.__grid.put(pos, width, height)
            self.RefreshSlot()

            constInfo.fragmentGrid.append([pos, cell])
            constInfo.fragmentItems.append(cell)
            self.wndInventory.RefreshBagSlotWindow()

    def Send(self):
        """Send selected items for crafting."""
        out = [slot for slot in self.__itemPos
               if not (slot[0] == player.INVENTORY and slot[1] == -1)]

        net.SendOdlamki(out)
        constInfo.fragmentItems = []
        self.wndInventory.RefreshBagSlotWindow()

    def ClearWindow(self):
        """Reset all slots to empty."""
        self.__itemPos = [[player.INVENTORY, -1] for _ in range(SLOT_COUNT)]
        self.__grid.reset()
        self.RefreshSlot()
        constInfo.fragmentGrid = []
        constInfo.fragmentItems = []
        if self.wndInventory:
            self.wndInventory.RefreshBagSlotWindow()


class Grid:
    """2D grid for tracking item slot occupancy."""

    def __init__(self, width: int, height: int):
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

    def find_blank(self, width: int, height: int) -> int:
        """Find first empty region that fits the given dimensions."""
        if width > self.width or height > self.height:
            return -1

        for row in range(self.height):
            for col in range(self.width):
                index = row * self.width + col
                if self.is_empty(index, width, height):
                    return index
        return -1

    def put(self, pos: int, width: int, height: int) -> bool:
        """Mark a region as occupied."""
        if not self.is_empty(pos, width, height):
            return False

        for row in range(height):
            start = pos + row * self.width
            for col in range(width):
                self.grid[start + col] = True
        return True

    def clear(self, pos: int, width: int, height: int):
        """Mark a region as empty."""
        if pos < 0 or pos >= self.width * self.height:
            return

        for row in range(height):
            start = pos + row * self.width
            for col in range(width):
                self.grid[start + col] = False

    def is_empty(self, pos: int, width: int, height: int) -> bool:
        """Check if a region is completely empty."""
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

    def get_size(self) -> int:
        return self.width * self.height

    def reset(self):
        self.grid = [False] * (self.width * self.height)

# Legacy aliases

