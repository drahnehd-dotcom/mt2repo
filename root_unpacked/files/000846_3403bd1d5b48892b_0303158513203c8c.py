import ui
import app
import dbg
import net
import player
import background
import localeInfo
import uiCommon
import uiToolTip
import uiScriptLocale
import miniMap
from _weakref import proxy

isShowWindow = False

class AtlasToolTip(uiToolTip.ToolTip):
	class AtlasRender(ui.Window):
		def __init__(self):
			ui.Window.__init__(self)
			self.AddFlag("not_pick")
			self.isLoaded = False

		def __del__(self):
			ui.Window.__del__(self)

		# Klient nie eksportuje miniMap.*ToolTipAtlas (brak implementacji w C++) - bez tych funkcji
		# podglad mapy w tooltipie jest pomijany, zamiast AttributeError przy najechaniu na zapisana lokacje.
		HAS_ATLAS = hasattr(miniMap, "LoadToolTipAtlas")

		def Show(self):
			ui.Window.Show(self)
			if self.HAS_ATLAS:
				miniMap.ShowToolTipAtlas()

		def Hide(self):
			ui.Window.Hide(self)
			if self.HAS_ATLAS:
				miniMap.HideToolTipAtlas()

		def Load(self, x, y):
			self.isLoaded = bool(miniMap.LoadToolTipAtlas(x, y)) if self.HAS_ATLAS else False

		def IsLoad(self):
			return self.isLoaded

		def OnRender(self):
			if not self.IsLoad():
				return

			(x, y) = self.GetGlobalPosition()
			miniMap.RenderToolTipAtlas(float(x), float(y))

	def __init__(self):
		uiToolTip.ToolTip.__init__(self)

	def __del__(self):
		uiToolTip.ToolTip.__del__(self)

	def SetAtlasToolTip(self, x, y):
		(mapZone, iGlobalX, iGlobalY) = background.GlobalPositionToMapInfo(x, y)
		self.ClearToolTip()
		self.AppendTextLine(uiScriptLocale.SAVE_LOCATION_TELEPORT, 0xffC4B58B)
		self.AppendTextLine("{} ({}, {})".format(localeInfo.GetMapNameByZone(mapZone), int(x - iGlobalX) // 100, int(y - iGlobalY) // 100))
		self.AppendAtlasRender(x, y)
		self.ShowToolTip()

	def ClearToolTip(self):
		uiToolTip.ToolTip.ClearToolTip(self)
		self.toolTipWidth = 190

	def AppendAtlasRender(self, x, y):
		self.atlasRender = self.AtlasRender()
		self.atlasRender.Load(x, y)
		if self.atlasRender.IsLoad():
			self.atlasRender.SetParent(self)
			self.atlasRender.Show()

			(iSizeX, iSizeY) = miniMap.GetToolTipAtlasSize()
			self.toolTipWidth = max(iSizeX + 20, self.toolTipWidth)
			self.atlasRender.SetPosition((self.toolTipWidth - iSizeX) // 2, self.toolTipHeight)
			self.toolTipHeight += iSizeY

			self.ResizeToolTip()
			self.AlignHorizonalCenter()

class SaveLocationWindow(ui.ScriptWindow):
	# Rows are built from stock Metin2 assets (public.dds buttons + engine slotbar).
	ROW_COUNT = 10
	ROW_WIDTH = 321
	ROW_HEIGHT = 21
	ROW_STEP = 25

	class LocationElement(ui.ListBoxEx.Item):
		INDEX_WIDTH = 18
		BUTTON_GAP = 4
		NAME_SLOT_HEIGHT = 18
		MIDDLE_BUTTON_WIDTH = 61
		LARGE_BUTTON_WIDTH = 88

		NAME_COLOR = 0xFFEED8C3
		EMPTY_COLOR = 0xFFA4A4A4

		def __init__(self, uiparent, parent, key):
			ui.ListBoxEx.Item.__init__(self)

			self.headParent = proxy(parent)
			self.SetParent(uiparent)
			self.key = key
			self.state = False

			self.indexText = None
			self.nameSlot = None
			self.nameText = None
			self.saveButton = None
			self.teleportButton = None

			self.__BuildObject()

		def __del__(self):
			ui.ListBoxEx.Item.__del__(self)

		def __BuildObject(self):
			rowWidth = SaveLocationWindow.ROW_WIDTH
			rowHeight = SaveLocationWindow.ROW_HEIGHT

			self.SetSize(rowWidth, rowHeight)
			self.SetSelectedRenderColor(None)

			teleportX = rowWidth - self.LARGE_BUTTON_WIDTH
			saveX = teleportX - self.BUTTON_GAP - self.MIDDLE_BUTTON_WIDTH
			nameSlotWidth = saveX - self.BUTTON_GAP - self.INDEX_WIDTH

			indexText = ui.TextLine()
			indexText.SetParent(self)
			indexText.AddFlag("not_pick")
			indexText.SetPosition(self.INDEX_WIDTH - 4, 0)
			indexText.SetWindowVerticalAlignCenter()
			indexText.SetVerticalAlignCenter()
			indexText.SetHorizontalAlignRight()
			indexText.SetText("%d." % (self.key + 1))
			indexText.Show()
			self.indexText = indexText

			nameSlot = ui.SlotBar()
			nameSlot.SetParent(self)
			nameSlot.AddFlag("not_pick")
			nameSlot.SetSize(nameSlotWidth, self.NAME_SLOT_HEIGHT)
			nameSlot.SetPosition(self.INDEX_WIDTH, (rowHeight - self.NAME_SLOT_HEIGHT + 1) // 2)
			nameSlot.Show()
			self.nameSlot = nameSlot

			nameText = ui.TextLine()
			nameText.SetParent(nameSlot)
			nameText.AddFlag("not_pick")
			nameText.SetPosition(5, 0)
			nameText.SetWindowVerticalAlignCenter()
			nameText.SetVerticalAlignCenter()
			nameText.SetText("")
			nameText.Show()
			self.nameText = nameText

			saveButton = ui.Button()
			saveButton.SetParent(self)
			saveButton.SetUpVisual("d:/ymir work/ui/public/middle_button_01.sub")
			saveButton.SetOverVisual("d:/ymir work/ui/public/middle_button_02.sub")
			saveButton.SetDownVisual("d:/ymir work/ui/public/middle_button_03.sub")
			saveButton.SetPosition(saveX, 0)
			saveButton.SetText(uiScriptLocale.SAVEMAP_SAVE)
			saveButton.SAFE_SetEvent(self.Register)
			saveButton.Show()
			self.saveButton = saveButton

			teleportButton = ui.Button()
			teleportButton.SetParent(self)
			teleportButton.SetUpVisual("d:/ymir work/ui/public/large_button_01.sub")
			teleportButton.SetOverVisual("d:/ymir work/ui/public/large_button_02.sub")
			teleportButton.SetDownVisual("d:/ymir work/ui/public/large_button_03.sub")
			teleportButton.SetPosition(teleportX, 0)
			teleportButton.SetText(uiScriptLocale.KEYCHANGE_TELEPORTACJA)
			teleportButton.SAFE_SetEvent(self.Warp)
			teleportButton.Show()
			self.teleportButton = teleportButton

			self.Show()

		def Register(self):
			if self.state:
				self.headParent.OpenSaveLocationQuestionDialog(self.key)
			else:
				self.headParent.OpenSaveLocationInputNameDialog(net.SAVELOCATION_SUB_HEADER_ADD, self.key)

		def Warp(self):
			if self.state:
				self.headParent.SendSaveLocationPacket(net.SAVELOCATION_SUB_HEADER_WARP, self.key)

		def RegisterName(self, text, state):
			self.state = state
			self.nameText.SetText(text)

			if state:
				self.nameText.SetPackedFontColor(self.NAME_COLOR)
				self.saveButton.SetText(uiScriptLocale.SELECT_DELETE)
			else:
				self.nameText.SetPackedFontColor(self.EMPTY_COLOR)
				self.saveButton.SetText(uiScriptLocale.SAVEMAP_SAVE)

	def __init__(self):
		if not app.ENABLE_SAVE_LOCATION_SYSTEM:
			return

		ui.ScriptWindow.__init__(self)

		self.isLoaded = False

		self.xStart = 0
		self.yStart = 0

		self.savePage = 0
		self.Objects = {}
		self.saveLocationDict = {}

		self.atlasToolTip = None
		self.inputDialog = None
		self.questionDialog = None

		self.__LoadWindow()

	def __del__(self):
		ui.ScriptWindow.__del__(self)
		self.Objects = {}

	def __LoadWindow(self):
		if self.isLoaded:
			return

		self.isLoaded = True

		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "uiscript/savelocationwindow.py")
		except Exception as e:
			dbg.TraceError("SaveLocationWindow.__LoadWindow.LoadScript: %s" % str(e))

		try:
			self.GetChild("board").SetCloseEvent(ui.__mem_func__(self.Close))

			container = self.GetChild("ElementContainer")
			container.SetViewItemCount(self.ROW_COUNT)
			container.SetItemSize(self.ROW_WIDTH, self.ROW_HEIGHT)
			container.SetItemStep(self.ROW_STEP)
			self.Objects["ElementContainer"] = container

			for i in range(self.ROW_COUNT):
				item = self.LocationElement(container, self, i)
				container.AppendItem(item)

		except Exception as e:
			dbg.TraceError("SaveLocationWindow.__LoadWindow.BindObject: %s" % str(e))

		self.atlasToolTip = AtlasToolTip()

		self.SetPage(0)

	def Show(self):
		global isShowWindow
		isShowWindow = True

		self.RefreshData()
		ui.ScriptWindow.Show(self)

		(self.xStart, self.yStart, z) = player.GetMainCharacterPosition()

	def Close(self):
		global isShowWindow
		isShowWindow = False

		self.Hide()

	def Destroy(self):
		self.OnCancelInput()
		self.OnCancel()
		self.ClearDictionary()
		self.Objects = {}
		self.atlasToolTip = None
		self.xStart = 0
		self.yStart = 0
		self.saveLocationDict = {}

	def IsShow(self):
		global isShowWindow
		return isShowWindow

	def SetPage(self, arg):
		self.savePage = arg
		self.RefreshData()

	def UpdateSaveLocation(self, pos, name, x, y):
		self.saveLocationDict.update( { pos : [name, x, y] } )
		self.RefreshData()

	def DeleteSaveLocation(self, pos):
		if pos in self.saveLocationDict:
			self.saveLocationDict.pop(pos)
		self.RefreshData()

	def SendSaveLocationPacket(self, subheader, pos):
		pos += (self.savePage*10)
		if pos >= player.SAVE_LOCATION_MAX:
			return
		net.SendSaveLocationPacket(subheader, pos, "")

	def OpenSaveLocationInputNameDialog(self, subheader, pos):
		inputDialog = uiCommon.InputDialog()
		inputDialog.SetTitle(uiScriptLocale.SAVE_LOCATION_INPUT_NAME)
		inputDialog.SetMaxLength(12)
		inputDialog.SetAcceptEvent(lambda arg1=subheader, arg2=pos, r=proxy(self): r.OnAcceptInput(arg1, arg2))
		inputDialog.SetCancelEvent(ui.__mem_func__(self.OnCancelInput))
		inputDialog.Open()

		self.inputDialog = inputDialog

	def OnAcceptInput(self, subheader, pos):
		if not self.inputDialog:
			return True

		if not len(self.inputDialog.GetText()):
			return True

		pos += (self.savePage*10)
		if pos >= player.SAVE_LOCATION_MAX:
			return True

		net.SendSaveLocationPacket(subheader, pos, self.inputDialog.GetText())
		self.OnCancelInput()
		return True

	def OnCancelInput(self):
		if self.inputDialog:
			self.inputDialog.Close()
			self.inputDialog = None

		return True

	def OpenSaveLocationQuestionDialog(self, pos):
		pos += (self.savePage*10)
		if pos >= player.SAVE_LOCATION_MAX:
			return True

		questionDialog = uiCommon.QuestionDialog()
		questionDialog.SetText(uiScriptLocale.SAVE_LOCATION_DELETE_CONFIRM)
		questionDialog.SetAcceptEvent(lambda arg=pos, r=proxy(self): r.OnAccept(arg))
		questionDialog.SetCancelEvent(ui.__mem_func__(self.OnCancel))
		questionDialog.Open()

		self.questionDialog = questionDialog

	def OnAccept(self, pos):
		if not self.questionDialog:
			return

		net.SendSaveLocationPacket(net.SAVELOCATION_SUB_HEADER_DEL, pos, "")
		self.OnCancel()

	def OnCancel(self):
		if self.questionDialog:
			self.questionDialog.Close()
			self.questionDialog = None

	def RefreshData(self):
		if "ElementContainer" not in self.Objects:
			return

		for i in range(self.ROW_COUNT):
			pos = i + (self.savePage*10)
			item = self.Objects["ElementContainer"].GetItem(i)
			if not item:
				continue

			if pos in self.saveLocationDict:
				(name, _x, _y) = self.saveLocationDict.get(pos, ("", 0, 0))
				item.RegisterName(str(name), True)
			else:
				item.RegisterName("--", False)

	def __OverIn(self, pos):
		if pos in self.saveLocationDict:
			(_name, x, y) = self.saveLocationDict.get(pos, ("", 0, 0))
			self.atlasToolTip.SetAtlasToolTip(x, y)
			self.atlasToolTip.Show()

	def __OverOut(self):
		self.atlasToolTip.Hide()

	def OnPressEscapeKey(self):
		self.Close()
		return True
