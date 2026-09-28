import ui
import player
import item
import uiToolTip
import chat
import localeInfo
import net

BROKEN_STONE_VNUM = 28960

class StoneDetachWindow(ui.ScriptWindow):
    def __init__(self):
        self.tooltip = uiToolTip.ItemToolTip()
        self.itemStoneImages = {}
        ui.ScriptWindow.__init__(self)

    def __del__(self):
        self.tooltip = None
        self.itemStoneImages = {}
        ui.ScriptWindow.__del__(self)

    def Open(self, scrollSlotPos, targetSlotPos):
        self.scrollSlotPos = scrollSlotPos
        self.targetSlotPos = targetSlotPos

        if not self.IsStoneToDetach():
            return

        self.__LoadDialog()
        self.Show()

    def Close(self):
        self.ResetDialog()
        self.Hide()

    def OnPressEscapeKey(self):
        self.Close()
        return True

    def IsStoneToDetach(self):
        hasStone = False
        for x in range(player.METIN_SOCKET_MAX_NUM):
            socket = player.GetItemMetinSocket(self.targetSlotPos, x)
            if socket > 2 and socket != BROKEN_STONE_VNUM:
                hasStone = True

        if not hasStone:
            chat.AppendChat(1, localeInfo.THERE_IS_NO_STONE_TO_DETACH)

        return hasStone

    def ResetDialog(self):
        self.itemStoneImages = {}

        for idx, text in self.metinNames.items():
            text.SetText("")

        for idx, text in self.metinBonuses.items():
            text.SetText("")

    def __LoadDialog(self):
        try:
            pyScrLoader = ui.PythonScriptLoader()
            pyScrLoader.LoadScriptFile(self, "uiscript/stonedetach.py")
        except:
            import exception
            exception.Abort("StoneDetachWindow.LoadDialog.LoadScript")

        try:
            self.GetChild("TitleBar").SetCloseEvent(ui.__mem_func__(self.Close))
            self.metinImages = {
                0: self.GetChild("MetinImage1"),
                1: self.GetChild("MetinImage2"),
                2: self.GetChild("MetinImage3"),
            }
            self.metinNames = {
                0: self.GetChild("MetinName1"),
                1: self.GetChild("MetinName2"),
                2: self.GetChild("MetinName3"),
            }
            self.metinBonuses = {
                0: self.GetChild("MetinBonus1"),
                1: self.GetChild("MetinBonus2"),
                2: self.GetChild("MetinBonus3"),
            }
            self.buttons = {
                0: self.GetChild("MetinButton1"),
                1: self.GetChild("MetinButton2"),
                2: self.GetChild("MetinButton3"),
            }

            for idx, btn in self.buttons.items():
                btn.SetEvent(ui.__mem_func__(self.__OnClickDetachButton), idx)

        except:
            import exception
            exception.Abort("StoneDetachWindow.LoadDialog.GetChild")

        self.__LoadStones()

    def __LoadStones(self):
        for x in range(player.METIN_SOCKET_MAX_NUM):
            itemVnum = player.GetItemMetinSocket(self.targetSlotPos, x)
            if itemVnum > 2:
                item.SelectItem(itemVnum)
                name = item.GetItemName()
                affectType, affectValue = item.GetAffect(0)
                bonus = self.tooltip.GetAffectStrings(affectType, affectValue)
                self.metinNames[x].SetText(name)
                self.metinBonuses[x].SetText(bonus)
                self.itemStoneImages[itemVnum] = ui.MakeImageBox(self.metinImages[x], item.GetIconImageFileName(), 5, 4)
            elif itemVnum == 1:
                self.buttons[x].Disable()
                self.buttons[x].Down()

    def __OnClickDetachButton(self, socket):
        net.SendChatPacket("/detach_stone %d %d %d" % (socket, self.scrollSlotPos, self.targetSlotPos))
        self.Close()