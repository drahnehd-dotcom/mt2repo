#-*- coding: iso-8859-1 -*-
import ui
import uiScriptLocale
import wndMgr
import player
import miniMap
import nonplayer
import localeInfo
import net
import app
import constInfo
import uiToolTip
import interfaceModule
import time

def StripWarpTargetCoords(name):
	# Warp-NPC maja nazwe w formacie "<Nazwa> <X> <Y>" - koordy sa danymi dla serwera
	# (parsuje je FuncCheckWarp), gracz ma widziec sama nazwe. Ucinamy WYLACZNIE
	# sufiks z dwoma liczbami, nie na pierwszej spacji - inaczej "Brama Zamku" -> "Brama".
	if not name:
		return name

	parts = name.rsplit(" ", 2)
	if len(parts) == 3 and parts[1].lstrip("-").isdigit() and parts[2].lstrip("-").isdigit():
		return parts[0]

	return name

def ResolveMiniMapMobNameToken(name):
	if not name:
		return name

	while True:
		posBegin = name.find("[MN;")
		if posBegin < 0:
			break

		posEnd = name.find("]", posBegin)
		if posEnd < 0:
			break

		vnumText = name[posBegin + 4:posEnd]
		try:
			vnum = int(vnumText)
			mobName = nonplayer.GetMonsterName(vnum)
			if not mobName:
				break
			name = name[:posBegin] + mobName + name[posEnd + 1:]
		except Exception:
			break

	return StripWarpTargetCoords(name)

class MapTextToolTip(ui.Window):
	def __init__(self):
		ui.Window.__init__(self)

		textLine = ui.TextLine()
		textLine.SetParent(self)
		textLine.SetHorizontalAlignCenter()
		textLine.SetOutline()
		textLine.SetHorizontalAlignRight()
		textLine.Show()
		self.textLine = textLine

	def __del__(self):
		ui.Window.__del__(self)

	def SetText(self, text):
		self.textLine.SetText(text)

	def SetTooltipPosition(self, PosX, PosY):
		self.textLine.SetPosition(PosX - 5, PosY)

	def SetTextColor(self, TextColor):
		self.textLine.SetPackedFontColor(TextColor)

	def SetHorizontalAlignLeft(self):
		if self.textLine:
			self.textLine.SetHorizontalAlignLeft()

	def GetTextSize(self):
		return self.textLine.GetTextSize()

class AtlasWindow(ui.ScriptWindow):

	class AtlasRenderer(ui.Window):
		def __init__(self):
			ui.Window.__init__(self)
			self.AddFlag("not_pick")

		def OnUpdate(self):
			miniMap.UpdateAtlas()

		def OnRender(self):
			(x, y) = self.GetGlobalPosition()
			fx = float(x)
			fy = float(y)
			miniMap.RenderAtlas(fx, fy)

		def HideAtlas(self):
			miniMap.HideAtlas()

		def ShowAtlas(self):
			miniMap.ShowAtlas()

	def __init__(self):
		self.tooltipInfo = MapTextToolTip()
		self.tooltipInfo.Hide()
		self.infoGuildMark = ui.MarkBox()
		self.infoGuildMark.Hide()
		self.AtlasMainWindow = None
		self.mapName = ""
		self.board = 0

		ui.ScriptWindow.__init__(self)

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def SetMapName(self, mapName):
		if 949==app.GetDefaultCodePage():
			try:
				self.board.SetTitleName(localeInfo.MINIMAP_ZONE_NAME_DICT[mapName])
			except:
				pass

	def LoadWindow(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "UIScript/AtlasWindow.py")
		except:
			import exception
			exception.Abort("AtlasWindow.LoadWindow.LoadScript")

		try:
			self.board = self.GetChild("board")

		except:
			import exception
			exception.Abort("AtlasWindow.LoadWindow.BindObject")

		self.AtlasMainWindow = self.AtlasRenderer()
		self.board.SetCloseEvent(self.Hide)
		self.AtlasMainWindow.SetParent(self.board)
		self.AtlasMainWindow.SetPosition(7, 30)
		self.tooltipInfo.SetParent(self.board)
		self.infoGuildMark.SetParent(self.board)
		self.SetPosition(40, 120)
		self.Hide()

		miniMap.RegisterAtlasWindow(self)

	def Destroy(self):
		miniMap.UnregisterAtlasWindow()
		self.ClearDictionary()
		self.AtlasMainWindow = None
		self.tooltipAtlasClose = 0
		self.tooltipInfo = None
		self.infoGuildMark = None
		self.board = None

	def OnUpdate(self):
		(x, y) = self.GetGlobalPosition()
		(mouseX, mouseY) = wndMgr.GetMousePosition()
		(bFind, sName, iPosX, iPosY, dwTextColor, dwGuildID) = miniMap.GetAtlasInfo(mouseX, mouseY)
		sName = ResolveMiniMapMobNameToken(sName)
			
		if not self.tooltipInfo:
			return

		if not self.infoGuildMark:
			return

		self.infoGuildMark.Hide()
		self.tooltipInfo.Hide()

		if self.board.IsIn():
			self.tooltipInfo.SetText("|cFFffffff%s|r (|cFFfcc923%d, %d|r)" % (sName, iPosX, iPosY))
			self.tooltipInfo.SetTooltipPosition(mouseX - x, mouseY - y)
			self.tooltipInfo.Show()
			self.tooltipInfo.SetTop()
		else:
			self.tooltipInfo.Hide()

		if False == self.board.IsIn():
			return

		if False == bFind:
			return

		if "empty_guild_area" == sName:
			sName = localeInfo.GUILD_EMPTY_AREA

		if 0 != dwGuildID:
			textWidth, textHeight = self.tooltipInfo.GetTextSize()
			self.infoGuildMark.SetIndex(dwGuildID)
			self.infoGuildMark.SetPosition(mouseX - x - textWidth - 18 - 5, mouseY - y)
			self.infoGuildMark.Show()

	def Hide(self):
		if self.AtlasMainWindow:
			self.AtlasMainWindow.HideAtlas()
			self.AtlasMainWindow.Hide()
		ui.ScriptWindow.Hide(self)

	def Show(self):
		if self.AtlasMainWindow:
			(bGet, iSizeX, iSizeY) = miniMap.GetAtlasSize()
			if bGet:
				self.SetSize(iSizeX + 15, iSizeY + 38)

				self.board.SetSize(iSizeX + 15, iSizeY + 38)
				self.AtlasMainWindow.ShowAtlas()
				self.AtlasMainWindow.Show()
		ui.ScriptWindow.Show(self)
		self.SetTop()

	def SetCenterPositionAdjust(self, x, y):
		self.SetPosition((wndMgr.GetScreenWidth() - self.GetWidth()) // 2 + x, (wndMgr.GetScreenHeight() - self.GetHeight()) // 2 + y)

	def OnPressEscapeKey(self):
		self.Hide()
		return True

def __RegisterMiniMapColor(type, rgb):
	miniMap.RegisterColor(type, rgb[0], rgb[1], rgb[2])

class MiniMap(ui.ScriptWindow):

	CANNOT_SEE_INFO_MAP_DICT = {
		"metin2_map_monkeydungeon" : False,
		"metin2_map_monkeydungeon_02" : False,
		"metin2_map_monkeydungeon_03" : False,
		"metin2_map_devilsCatacomb" : False,
	}

	def __init__(self):
		ui.ScriptWindow.__init__(self)

		self.__Initialize()

		miniMap.Create()
		miniMap.SetScale(2.0)

		self.AtlasWindow = AtlasWindow()
		self.AtlasWindow.LoadWindow()
		self.AtlasWindow.Hide()

		self.tooltipMiniMapOpen = MapTextToolTip()
		self.tooltipMiniMapOpen.SetText(localeInfo.MINIMAP)
		self.tooltipMiniMapOpen.Show()
		self.tooltipAtlasOpen = MapTextToolTip()
		self.tooltipInfo = MapTextToolTip()
		self.tooltipInfo.Show()

		if not miniMap.IsAtlas():
			self.tooltipAtlasOpen.SetText(localeInfo.MINIMAP_CAN_NOT_SHOW_AREAMAP)

		self.tooltipInfo = MapTextToolTip()
		self.tooltipInfo.Show()

		self.mapName = ""

		self.isLoaded = 0
		self.canSeeInfo = True

		self.imprisonmentDuration = 0
		self.imprisonmentEndTime = 0
		self.imprisonmentEndTimeText = ""


	def __del__(self):
		miniMap.Destroy()
		ui.ScriptWindow.__del__(self)


	def __Initialize(self):
		self.positionInfo = 0
		self.observerCount = 0

		# cache dla OnUpdate (patrz nizej) - resetowane razem z reszta dzieci okna
		self.dayInfo = 0
		self.lastClockUpdateTime = 0
		self.lastPositionText = ""

		self.OpenWindow = 0
		self.CloseWindow = 0
		self.ScaleUpButton = 0
		self.ScaleDownButton = 0
		self.MiniMapHideButton = 0
		self.MiniMapShowButton = 0
		self.AtlasShowButton = 0
		if app.ENABLE_DUNGEON_INFO_SYSTEM:
			self.DungeonInfoShowButton = 0

		self.tooltipMiniMapOpen = 0
		self.tooltipAtlasOpen = 0
		if app.ENABLE_DUNGEON_INFO_SYSTEM:
			self.tooltipDungeonInfoOpen = 0
		self.tooltipInfo = None
		self.serverInfo = None
		

	def BindInterfaceClass(self, interface):
		self.interface = interface

	def SetMapName(self, mapName):
		self.mapName=mapName
		self.AtlasWindow.SetMapName(mapName)

		if mapName in self.CANNOT_SEE_INFO_MAP_DICT:
			self.canSeeInfo = False
			self.HideMiniMap()
			self.tooltipMiniMapOpen.SetText(localeInfo.MINIMAP_CANNOT_SEE)
		else:
			self.canSeeInfo = True
			self.ShowMiniMap()
			self.tooltipMiniMapOpen.SetText(localeInfo.MINIMAP)

	def SetImprisonmentDuration(self, duration):
		self.imprisonmentDuration = duration
		self.imprisonmentEndTime = app.GetGlobalTimeStamp() + duration

		self.__UpdateImprisonmentDurationText()

	def __UpdateImprisonmentDurationText(self):
		restTime = max(self.imprisonmentEndTime - app.GetGlobalTimeStamp(), 0)

		imprisonmentEndTimeText = localeInfo.SecondToDHM(restTime)
		if imprisonmentEndTimeText != self.imprisonmentEndTimeText:
			self.imprisonmentEndTimeText = imprisonmentEndTimeText
			self.serverInfo.SetText("%s: %s" % (uiScriptLocale.AUTOBAN_QUIZ_REST_TIME, self.imprisonmentEndTimeText))

	def Show(self):
		self.__LoadWindow()

		ui.ScriptWindow.Show(self)

	def __LoadWindow(self):
		if self.isLoaded == 1:
			return

		self.isLoaded = 1

		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "UIScript/MiniMap.py")
		except:
			import exception
			exception.Abort("MiniMap.LoadWindow.LoadScript")

		try:
			self.OpenWindow = self.GetChild("OpenWindow")
			self.MiniMapWindow = self.GetChild("MiniMapWindow")
			self.ScaleUpButton = self.GetChild("ScaleUpButton")
			self.ScaleDownButton = self.GetChild("ScaleDownButton")
			self.MiniMapHideButton = self.GetChild("MiniMapHideButton")
			self.AtlasShowButton = self.GetChild("AtlasShowButton")
			self.CloseWindow = self.GetChild("CloseWindow")
			self.MiniMapShowButton = self.GetChild("MiniMapShowButton")
			self.positionInfo = self.GetChild("PositionInfo")
			self.observerCount = self.GetChild("ObserverCount")
			self.serverInfo = self.GetChild("ServerInfo")

			self.buttonChangeChannel = {
				1:self.GetChild("Channel1"),
				2:self.GetChild("Channel2"),
				3:self.GetChild("Channel3"),
				4:self.GetChild("Channel4"),
				5:self.GetChild("Channel5")
			}
		except:
			import exception
			exception.Abort("MiniMap.LoadWindow.Bind")

		if constInfo.MINIMAP_POSITIONINFO_ENABLE==0:
			self.positionInfo.Hide()

		self.serverInfo.SetText(net.GetServerInfo())
		self.ScaleUpButton.SetEvent(ui.__mem_func__(self.ScaleUp))
		self.ScaleDownButton.SetEvent(ui.__mem_func__(self.ScaleDown))
		self.MiniMapHideButton.SetEvent(ui.__mem_func__(self.HideMiniMap))
		self.MiniMapShowButton.SetEvent(ui.__mem_func__(self.ShowMiniMap))

		self.buttonChangeChannel[1].SetEvent(ui.__mem_func__(self.ChangeChannel1))
		self.buttonChangeChannel[2].SetEvent(ui.__mem_func__(self.ChangeChannel2))
		self.buttonChangeChannel[3].SetEvent(ui.__mem_func__(self.ChangeChannel3))
		self.buttonChangeChannel[4].SetEvent(ui.__mem_func__(self.ChangeChannel4))
		self.buttonChangeChannel[5].SetEvent(ui.__mem_func__(self.ChangeChannel5))

		if miniMap.IsAtlas():
			self.AtlasShowButton.SetEvent(ui.__mem_func__(self.ToggleAtlasWindow))

		(ButtonPosX, ButtonPosY) = self.MiniMapShowButton.GetGlobalPosition()
		self.tooltipMiniMapOpen.SetTooltipPosition(ButtonPosX, ButtonPosY)




		(ButtonPosX, ButtonPosY) = self.AtlasShowButton.GetGlobalPosition()
		self.tooltipAtlasOpen.SetTooltipPosition(ButtonPosX, ButtonPosY)

		self.ShowMiniMap()

	def Destroy(self):
		self.HideMiniMap()

		self.AtlasWindow.Destroy()
		self.AtlasWindow = None

		self.ClearDictionary()

		self.__Initialize()

	def UpdateObserverCount(self, observerCount):
		if observerCount>0:
			self.observerCount.Show()
		elif observerCount<=0:
			self.observerCount.Hide()

		self.observerCount.SetText(localeInfo.MINIMAP_OBSERVER_COUNT % observerCount)

	def OnUpdate(self):
		(x, y, z) = player.GetMainCharacterPosition()
		miniMap.Update(x, y)

		# Zegar zmienia sie raz na sekunde, a minimapa jest zawsze widoczna - wczesniej dwa
		# strftime + sklejanie stringa + GetChild (lookup w slowniku) + SetText lecialy CO KLATKE.
		curTime = app.GetGlobalTime()
		if curTime - self.lastClockUpdateTime >= 1000:
			self.lastClockUpdateTime = curTime

			if not self.dayInfo:
				self.dayInfo = self.GetChild("dayInfo")

			if self.dayInfo:
				self.dayInfo.SetText(time.strftime("%d.%m.%y") + " - " + time.strftime("%H:%M:%S"))

		# pozycja zmienia sie dopiero co 1 metr (dzielenie przez 100) - nie odswiezaj bez zmiany
		positionText = "(%.0f, %.0f)" % (x//100, y//100)
		if positionText != self.lastPositionText:
			self.lastPositionText = positionText
			self.positionInfo.SetText(positionText)

		if self.tooltipInfo:
			if True == self.MiniMapWindow.IsIn():
				(mouseX, mouseY) = wndMgr.GetMousePosition()
				(bFind, sName, iPosX, iPosY, dwTextColor) = miniMap.GetInfo(mouseX, mouseY)
				sName = ResolveMiniMapMobNameToken(sName)
				if bFind == 0:
					self.tooltipInfo.Hide()
				elif not self.canSeeInfo:
					self.tooltipInfo.SetText("%s(%s)" % (sName, localeInfo.UI_POS_UNKNOWN))
					self.tooltipInfo.SetTooltipPosition(mouseX - 5, mouseY)
					self.tooltipInfo.SetTextColor(dwTextColor)
					self.tooltipInfo.Show()
				else:
					self.tooltipInfo.SetText("%s(%d, %d)" % (sName, iPosX, iPosY))
					self.tooltipInfo.SetTooltipPosition(mouseX - 5, mouseY)
					self.tooltipInfo.SetTextColor(dwTextColor)
					self.tooltipInfo.Show()
			else:
				self.tooltipInfo.Hide()

			if self.imprisonmentDuration:
				self.__UpdateImprisonmentDurationText()

		if True == self.MiniMapShowButton.IsIn():
			self.tooltipMiniMapOpen.Show()
		else:
			self.tooltipMiniMapOpen.Hide()




		if True == self.AtlasShowButton.IsIn():
			self.tooltipAtlasOpen.Show()
		else:
			self.tooltipAtlasOpen.Hide()


	def OnRender(self):
		(x, y) = self.GetGlobalPosition()
		fx = float(x)
		fy = float(y)
		miniMap.Render(fx + 4.0, fy + 5.0)

	def Close(self):
		self.HideMiniMap()

	def HideMiniMap(self):
		miniMap.Hide()
		self.OpenWindow.Hide()
		self.CloseWindow.Show()

	def ChangeChannel1(self):
		if self.buttonChangeChannel[1]:
			for i in range(1,6):
				self.buttonChangeChannel[i].SetUp()
				self.buttonChangeChannel[1].Down()
			net.MoveChannelGame(1)

	def ChangeChannel2(self):
		if self.buttonChangeChannel[2]:
			for i in range(1,6):
				self.buttonChangeChannel[i].SetUp()
				self.buttonChangeChannel[2].Down()
			net.MoveChannelGame(2)

	def ChangeChannel3(self):
		if self.buttonChangeChannel[3]:
			for i in range(1,6):
				self.buttonChangeChannel[i].SetUp()
				self.buttonChangeChannel[3].Down()
			net.MoveChannelGame(3)

	def ChangeChannel4(self):
		if self.buttonChangeChannel[4]:
			for i in range(1,6):
				self.buttonChangeChannel[i].SetUp()
				self.buttonChangeChannel[4].Down()
			net.MoveChannelGame(4)

	def ChangeChannel5(self):
		if self.buttonChangeChannel[5]:
			for i in range(1,6):
				self.buttonChangeChannel[i].SetUp()
				self.buttonChangeChannel[5].Down()
			net.MoveChannelGame(5)


	def ShowMiniMap(self):
		if not self.canSeeInfo:
			return

		miniMap.Show()
		self.OpenWindow.Show()
		self.CloseWindow.Hide()

	def isShowMiniMap(self):
		return miniMap.isShow()

	def ScaleUp(self):
		miniMap.ScaleUp()

	def ScaleDown(self):
		miniMap.ScaleDown()
		
	if app.BL_MOVE_CHANNEL:
		def RefreshServerInfo(self, channelNumber):
			if net.GetChannelNumber() == 99:
				for i in range(1,6):
					self.buttonChangeChannel[i].Down()
			elif net.GetChannelNumber() == 1:
				self.buttonChangeChannel[1].Down()
			elif net.GetChannelNumber() == 2:
				self.buttonChangeChannel[2].Down()
			elif net.GetChannelNumber() == 3:
				self.buttonChangeChannel[3].Down()
			elif net.GetChannelNumber() == 4:
				self.buttonChangeChannel[4].Down()
			elif net.GetChannelNumber() == 5:
				self.buttonChangeChannel[5].Down()
				
			if net.GetChannelNumber() == 99:
				serverInfoStr = "|cFFe0c18cKowalMT2|r, - Global"
			else:
				serverInfoStr = localeInfo.MINIMAP_SERVER_INFO_REGULAR.format(channelNumber)

			self.serverInfo.SetText(serverInfoStr)
			net.SetServerInfo(serverInfoStr)

	def ShowAtlas(self):
		if not miniMap.IsAtlas():
			return
		if not self.AtlasWindow.IsShow():
			self.AtlasWindow.Show()

	def ToggleAtlasWindow(self):
		if not miniMap.IsAtlas():
			return
		if self.AtlasWindow.IsShow():
			self.AtlasWindow.Hide()
		else:
			self.AtlasWindow.Show()

	if app.ENABLE_LOADING_PERFORMANCE:
		def IsShowingAtlas(self):
			return self.AtlasWindow.IsShow()
			
