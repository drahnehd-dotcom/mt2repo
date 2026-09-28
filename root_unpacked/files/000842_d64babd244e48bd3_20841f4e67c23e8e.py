import ui
import mouseModule
import net
import uiCommon
import localeInfo
import player
import item
import snd
import constInfo
from _weakref import proxy
import app

player.REMOVE_ITEM_SLOT_COUNT_X = 8
player.REMOVE_ITEM_SLOT_COUNT_Y = 6

class RemoveItemDialog(ui.ScriptWindow):
    def __init__(self):
        self.tooltipItem = None
        self.__questionDialog = None
        self.__itemPos = [[player.INVENTORY, -1] for _ in range(player.REMOVE_ITEM_SLOT_COUNT_X * player.REMOVE_ITEM_SLOT_COUNT_Y)]
        self.__grid = None
        self.__loaded = False
        self.wndInventory = None
        ui.ScriptWindow.__init__(self)
        self.__LoadWindow()

    def __del__(self):
        ui.ScriptWindow.__del__(self)

    def SetItemToolTip(self, itemToolTip):
        self.tooltipItem = proxy(itemToolTip)

    def __LoadWindow(self):
        try:
            pythonScriptLoader = ui.PythonScriptLoader()
            pythonScriptLoader.LoadScriptFile(self, "uiscript/removeitemdialog.py")
        except:
            import exception
            exception.Abort("RemoveItemDialog.__LoadWindow.LoadObject")

        self.wndItem = self.GetChild("item_slot")
        self.removeButton = self.GetChild("remove_button")
        self.clearButton = self.GetChild("clear_button")

        self.wndItem.SetSelectItemSlotEvent(ui.__mem_func__(self.SelectItemSlot))
        self.wndItem.SetUseSlotEvent(ui.__mem_func__(self.SelectItemSlot))
        self.wndItem.SetSelectEmptySlotEvent(ui.__mem_func__(self.SelectEmptySlot))
        self.wndItem.SetOverInItemEvent(ui.__mem_func__(self.OverInItem))
        self.wndItem.SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))

        self.removeButton.SetEvent(ui.__mem_func__(self.__OnClickRemoveButton))
        self.clearButton.SetEvent(ui.__mem_func__(self.__OnClickClearButton))

        self.GetChild("board").SetCloseEvent(ui.__mem_func__(self.Hide))
        self.__grid = Grid(player.REMOVE_ITEM_SLOT_COUNT_X, player.REMOVE_ITEM_SLOT_COUNT_Y)

        self.__loaded = True

        self.SetCenterPosition()

    def __OnClickRemoveButton(self):
        if not len(self.__itemPos):
            return
        self.__questionDialog = uiCommon.QuestionDialog()
        self.__questionDialog.SetText(localeInfo.REMOVE_ITEM_DO_YOU_REMOVE)
        self.__questionDialog.SetAcceptEvent(lambda arg=True: self.__AnswerQuestionDialog(arg))
        self.__questionDialog.SetCancelEvent(lambda arg=False: self.__AnswerQuestionDialog(arg))
        self.__questionDialog.Open()

    def __OnClickClearButton(self):
        self.__itemPos = [[player.INVENTORY, -1] for _ in range(player.REMOVE_ITEM_SLOT_COUNT_X * player.REMOVE_ITEM_SLOT_COUNT_Y)]
        self.__grid.reset()
        self.RefreshSlot()
        
        constInfo.itemRemoveGrid = []
        constInfo.listRemoveItem = []
        if self.wndInventory:
            self.wndInventory.RefreshBagSlotWindow()

    def __AnswerQuestionDialog(self, flag):
        self.__questionDialog.Close()

        if flag:
            out = []

            for slot in self.__itemPos:
                if slot[0] == player.INVENTORY and slot[1] == -1:
                    continue

                out.append(slot)

            net.SendRemoveItemPacket(out)
            
            constInfo.listRemoveItem = []
            self.wndInventory.RefreshBagSlotWindow()

    def ClearWindow(self):
        self.__OnClickClearButton()

    def AppendSlot(self, wnd, cell):
        itemVnum = player.GetItemIndex(wnd, cell)
        if not itemVnum:
            return

        itemPos = [wnd, cell]
        if itemPos in self.__itemPos:
            return

        item.SelectItem(itemVnum)
        (width, height) = item.GetItemSize()

        pos = self.__grid.find_blank(width, height)

        if pos != -1:
            self.__itemPos[pos] = itemPos

            self.__grid.put(pos, width, height)

            self.RefreshSlot()
            
            constInfo.itemRemoveGrid.append([pos, cell])
            constInfo.listRemoveItem.append(cell)
            self.wndInventory.RefreshBagSlotWindow()

    def RefreshSlot(self):
        if not self.__loaded:
            return

        for i in range(self.wndItem.GetSlotCount()):
            itemVnum = player.GetItemIndex(self.__itemPos[i][0], self.__itemPos[i][1])
            itemCount = player.GetItemCount(self.__itemPos[i][0], self.__itemPos[i][1])

            if not itemCount:
                self.wndItem.ClearSlot(i)
                continue

            self.wndItem.SetItemSlot(i, itemVnum, 0 if itemCount == 1 else itemCount)

        self.wndItem.RefreshSlot()

    def SelectItemSlot(self, slotIndex):
        isAttached = mouseModule.mouseController.isAttached()
        if isAttached:
            snd.PlaySound("sound/ui/loginfail.wav")
            mouseModule.mouseController.DeattachObject()
            return

        item.SelectItem(mouseModule.mouseController.GetAttachedItemIndex())
        (width, height) = item.GetItemSize()

        self.__grid.clear(slotIndex, width, height)
        
        self.__itemPos[slotIndex][0] = player.INVENTORY
        self.__itemPos[slotIndex][1] = -1

        for removeGrid in constInfo.itemRemoveGrid:
            if slotIndex == removeGrid[0]:
                constInfo.itemRemoveGrid.remove(removeGrid)
                constInfo.listRemoveItem.remove(removeGrid[1])
                self.wndInventory.RefreshBagSlotWindow()

        self.__grid.reset()
        self.RefreshSlot()

    def SelectEmptySlot(self, slotIndex):
        isAttached = mouseModule.mouseController.isAttached()
        if isAttached:
            attachedSlotType = mouseModule.mouseController.GetAttachedType()
            attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
            attachedInvenType = player.SlotTypeToInvenType(attachedSlotType)
            mouseModule.mouseController.DeattachObject()

            if player.SLOT_TYPE_INVENTORY != attachedSlotType and player.SLOT_TYPE_DRAGON_SOUL_INVENTORY != attachedSlotType:
                return

            item.SelectItem(player.GetItemIndex(attachedInvenType, attachedSlotPos))
            (width, height) = item.GetItemSize()

            if not self.__grid.is_empty(slotIndex, width, height):
                return

            itemPos = [attachedInvenType, attachedSlotPos]
            if itemPos in self.__itemPos:
                return


            self.__itemPos[slotIndex] = itemPos

            self.__grid.put(slotIndex, width, height)

            self.RefreshSlot()
			
            constInfo.itemRemoveGrid.append([slotIndex, attachedSlotPos])
            constInfo.listRemoveItem.append(attachedSlotPos)
            self.wndInventory.RefreshBagSlotWindow()

    def OverInItem(self, slotIndex):
        if self.tooltipItem:
            self.tooltipItem.SetInventoryItem(self.__itemPos[slotIndex][1], self.__itemPos[slotIndex][0])

    def OverOutItem(self):
        if self.tooltipItem:
            self.tooltipItem.HideToolTip()

    def OpenWindow(self, wndInventory):
        self.Show()
        self.wndInventory = wndInventory
        self.RefreshSlot()

        # Tooltip przedmiotu czyta te flage, zeby pokazac skrot "shift + PPM - wrzuc do kosza"
        constInfo.REMOVE_ITEM_OPENED = True

    def Hide(self):
        if self.__loaded:
            self.ClearWindow()

        constInfo.REMOVE_ITEM_OPENED = False

        ui.ScriptWindow.Hide(self)

        if self.tooltipItem:
            if self.tooltipItem.IsShow():
                self.tooltipItem.HideToolTip()

        if self.__questionDialog:
            self.__questionDialog.Close()

    def OnPressExitKey(self):
        self.Hide()
        return True

    def OnPressEscapeKey(self):
        self.Hide()
        return True

    def Destroy(self):
        self.Hide()
        self.ClearDictionary()

        if self.__questionDialog:
            self.__questionDialog = None

class Grid:
    """
        Args:
            width (int): Grid's width.
            height (int): Grid's height.

        Attributes:
            grid (list): The list will hold the position empty or not information.
            width (int): Grid's width
            height (int): Grid's height
    """

    def __init__(self, width, height):
        self.grid = [False] * (width * height)
        self.width = width
        self.height = height

    def __str__(self):
        output = "Grid {}x{} Information\n".format(self.width, self.height)
        for row in range(self.height):
            for col in range(self.width):
                output += "Status of %d: " % (row * self.width + col)
                output += "NotEmpty, " if self.grid[row *
                                                   self.width + col] else "Empty, "
            output += "\n"

        return output

    def find_blank(self, width, height):
        """
            Args:
                width (int): The item's width you can call width item.GetItemSize()[0]
                height (int): The item's height you can call width item.GetItemSize()[1]

            Returns:
                int: The return value would be an int if successful. Otherwise -1.
        """
        if width > self.width or height > self.height:
            return -1

        for row in range(self.height):
            for col in range(self.width):
                index = row * self.width + col
                if self.is_empty(index, width, height):
                    return index

        return -1

    def put(self, pos, width, height):
        """
            Args:
                pos (int): Position of the item to put.
                width (int): The item's width you can call width item.GetItemSize()[0]
                height (int): The item's height you can call width item.GetItemSize()[1]

            Returns:
                bool: The return value. True for success, False otherwise.
        """
        if not self.is_empty(pos, width, height):
            return False

        for row in range(height):
            start = pos + (row * self.width)
            self.grid[start] = True
            col = 1
            while col < width:
                self.grid[start + col] = True
                col += 1

        return True

    def clear(self, pos, width, height):
        """
            Args:
                pos (int): Position of the item to put.
                width (int): The item's width you can call width item.GetItemSize()[0]
                height (int): The item's height you can call width item.GetItemSize()[1]

            Returns:
                There is nothing to return
        """
        if pos < 0 or pos >= (self.width * self.height):
            return

        for row in range(height):
            start = pos + (row * self.width)
            self.grid[start] = False
            col = 1
            while col < width:
                self.grid[start + col] = False
                col += 1

    def is_empty(self, pos, width, height):
        """
            Args:
                pos (int): Position of the item to put.
                width (int): The item's width you can call width item.GetItemSize()[0]
                height (int): The item's height you can call width item.GetItemSize()[1]

            Returns:
                bool: The return value. True for success, False otherwise.
        """
        if pos < 0:
            return False

        row = pos // self.width
        if (row + height) > self.height:
            return False

        if (pos + width) > ((row * self.width) + self.width):
            return False

        for row in range(height):
            start = pos + (row * self.width)
            if self.grid[start]:
                return False

            col = 1
            while col < width:
                if self.grid[start + col]:
                    return False
                col += 1

        return True

    def get_size(self):
        """
            Returns:
                int: The return value will give you maximum capacity of grid. (width * height)
        """
        return self.width * self.height

    def reset(self):
        """
            With this function, you can reset instead of deleting it and create again.
        """
        self.grid = [False] * (self.width * self.height)