import ui
import player
import net
import localeInfo
import uicommon
import background
import app

class Event:
    def __init__(self, event, *args):
        self.event = event
        self.args = args

    def __call__(self, *args, **kwargs):
        self.event(*self.args)

class SaveMapDialog(ui.ScriptWindow):
    def __init__(self):
        self.__page = 0
        self.__inputDialog = None
        self.__previewDialog = None
        ui.ScriptWindow.__init__(self)
        self.__LoadWindow()

    def __del__(self):
        ui.ScriptWindow.__del__(self)

    def __LoadWindow(self):
        try:
            pyScrLoader = ui.PythonScriptLoader()
            pyScrLoader.LoadScriptFile(self, "uiscript/savemapdialog.py")

        except:
            import exception

            exception.Abort("SaveMapsDialog.__LoadWindow.LoadObject")

        self.GetChild("TitleBar").SetCloseEvent(ui.__mem_func__(self.Hide))
        self.PageText = self.GetChild("PageText")
        PageBtns = {
            0 : self.GetChild("PrevPageBtn"),
            1 : self.GetChild("NextPageBtn"),
        }
        for i in range(2):
            PageBtns[i].SetEvent(ui.__mem_func__(self.__OnClickPageButton), i)
            
        self.__inputSlotList = []
        for i in range(5):
            inputSlot = {
                "name": self.GetChild("input_name_%02d" % (i + 1)),
                "cord": self.GetChild("input_cord_%02d" % (i + 1)),
                "mark": self.GetChild("qmark_%02d" % (i + 1)),
                "save_button": self.GetChild("save_button_%02d" % (i + 1)),
                "teleport_button": self.GetChild("teleport_button_%02d" % (i + 1)),
            }

            inputSlot["save_button"].SetEvent(
                ui.__mem_func__(self.__OnClickSaveButton), i
            )
            inputSlot["teleport_button"].SetEvent(
                ui.__mem_func__(self.__OnClickTeleportButton), i
            )
            inputSlot["mark"].OnMouseOverIn = Event(
                ui.__mem_func__(self.__OnMarkOverIn), i
            )
            inputSlot["mark"].OnMouseOverOut = Event(
                ui.__mem_func__(self.__OnMarkOverOut)
            )

            self.__inputSlotList.append(inputSlot)

        self.__previewDialog = SaveMapPreviewDialog()
        self.__previewDialog.Hide()

        self.PageText.SetText(str(self.__page))
        self.SetCenterPosition()

    def Hide(self):
        ui.ScriptWindow.Hide(self)
        self.__OnCloseInputDialog()

    def Destroy(self):
        self.ClearDictionary()

        if self.__previewDialog:
            self.__previewDialog.Destroy()

        self.__inputSlotList = []

        self.__OnCloseInputDialog()

    def RefreshWindow(self):
        start = self.__page * player.SAVE_MAP_PAGE_ITEM_COUNT
        stop = (self.__page + 1) * player.SAVE_MAP_PAGE_ITEM_COUNT

        for i in range(start, stop):
            index = i - (self.__page * player.SAVE_MAP_PAGE_ITEM_COUNT)
            name, x, y, map_index = player.GetSaveMap(i)

            if not len(name) or x < 0 or y < 0 or map_index < 0:
                name = localeInfo.SAVE_MAPS_EMPTY
                x, y = 0, 0
            else:
                name = localeInfo.SAVE_MAPS_BUSY % name
                (_, xBase, yBase) = background.GlobalPositionToMapInfo(x, y)
                x = int(x - xBase) // 100
                y = int(y - yBase) // 100

            inputSlot = self.__inputSlotList[index]
            inputSlot["name"].SetText("%d. %s" % (i + 1, name))
            inputSlot["cord"].SetText("(%d, %d)" % (x, y))

    def __OnClickPageButton(self, index):
        if index == 0:
            if self.__page == 0:
                return
            self.__page -= 1
        else:
            if self.__page == player.SAVE_MAP_PAGE_MAX_NUM:
                return
            self.__page += 1

        self.PageText.SetText(str(self.__page))
        self.RefreshWindow()

    def __OnClickSaveButton(self, index):
        name, x, y, map_index = player.GetSaveMap(index)

        inputDialog = uicommon.InputDialogWithDescription()
        inputDialog.SetTitle(localeInfo.SAVE_MAPS_SAVE_TITLE)
        inputDialog.SetAcceptEvent(ui.__mem_func__(self.__OnAcceptInputDialog))
        inputDialog.SetCancelEvent(ui.__mem_func__(self.__OnCloseInputDialog))
        inputDialog.SetMaxLength(player.SAVE_MAP_NAME_MAX_NUM)
        inputDialog.SetBoardWidth(310)
        inputDialog.index = index
        inputDialog.Open()

        if not len(name) or x < 0 or y < 0 or map_index < 0:
            inputDialog.SetDescription(localeInfo.SAVE_MAPS_SAVE_DESC)
        else:
            inputDialog.SetDescription(localeInfo.SAVE_MAPS_OVERWRITE_DESC)

        self.__inputDialog = inputDialog

    def __OnAcceptInputDialog(self):
        index = self.__inputDialog.index + (
            self.__page * 5
        )
        name = self.__inputDialog.GetText()

        net.SendSaveMapPacket(index, name)

        self.__OnCloseInputDialog()

    def __OnCloseInputDialog(self):
        if self.__inputDialog:
            self.__inputDialog.Close()

    def __OnClickTeleportButton(self, index):
        net.SendTeleportMapPacket(index)

    def __OnMarkOverIn(self, index):
        index = index + (self.__page * 5)

        _, x, y, _ = player.GetSaveMap(index)

        if x < 0 or y < 0:
            return

        if self.__previewDialog:
            self.__previewDialog.Open(x, y)
            self.OnMoveWindow(*self.GetGlobalPosition())

    def __OnMarkOverOut(self):
        if self.__previewDialog and self.__previewDialog.IsShow():
            self.__previewDialog.Hide()

    def OnMoveWindow(self, x, y):
        self.__previewDialog.SetPosition(
            x + self.GetWidth(),
            y + (self.GetHeight() - self.__previewDialog.GetHeight()) // 2,
        )

class SaveMapPreviewDialog(ui.ScriptWindow):
    def __init__(self):
        ui.ScriptWindow.__init__(self)
        self.__LoadWindow()

    def __del__(self):
        ui.ScriptWindow.__del__(self)

    def __LoadWindow(self):
        try:
            pyScrLoader = ui.PythonScriptLoader()
            pyScrLoader.LoadScriptFile(self, "uiscript/savemappreviewdialog.py")

        except:
            import exception

            exception.Abort("TeleportDialog.__LoadWindow.LoadObject")
        self.board = self.GetChild("Board")
        self.header = self.GetChild("header")
        self.mapImage = self.GetChild("map_image")
        self.mapName = self.GetChild("map_name")
        self.mapPoint = self.GetChild("map_point")

    def Destroy(self):
        self.ClearDictionary()

        self.board = None
        self.header = None
        self.mapImage = None
        self.mapName = None
        self.mapPoint = None

    def Open(self, xPos, yPos):
        (mapName, xBase, yBase) = background.GlobalPositionToMapInfo(xPos, yPos)

        localeMapName = localeInfo.MINIMAP_ZONE_NAME_DICT.get(mapName, "")

        if localeMapName:
            self.mapName.SetText(
                localeInfo.TOOLTIP_MEMORIZED_POSITION
                % (localeMapName, int(xPos - xBase) // 100, int(yPos - yBase) // 100)
            )
        else:
            self.mapName.SetText(
                localeInfo.TOOLTIP_MEMORIZED_POSITION_ERROR
                % (int(xPos) // 100, int(yPos) // 100)
            )

        fileName = "d:/ymir work/ui/atlas/{}/atlas.sub".format(mapName)

        if not app.IsExistFile(fileName):
            xSize = 8 + 128
            ySize = 30 + 25 + 5
            self.SetSize(xSize, ySize)
            self.board.SetSize(xSize, ySize)
            self.header.SetScale(float(128) / 251.0, 1.0)

            self.mapImage.Hide()
            self.mapPoint.Hide()
        else:
            self.mapImage.LoadImage(fileName)

            xSize = 8 + self.mapImage.GetWidth()
            ySize = 25 + 3 + self.mapImage.GetHeight()
            self.SetSize(xSize, ySize)
            self.board.SetSize(xSize, ySize)
            self.header.SetScale(float(self.mapImage.GetWidth()) / 251.0, 1.0)

            xMap, yMap = background.GlobalPositionToMapSize(xPos, yPos)

            xPoint = int(xPos - xBase)
            yPoint = int(yPos - yBase)

            xPoint /= float(xMap) / float(self.mapImage.GetWidth())
            yPoint /= float(yMap) / float(self.mapImage.GetHeight())

            self.mapPoint.SetPosition(xPoint, yPoint)

            self.mapImage.Show()
            self.mapPoint.Show()
        self.mapName.UpdateRect()

        self.Show()
        self.UpdateRect()
