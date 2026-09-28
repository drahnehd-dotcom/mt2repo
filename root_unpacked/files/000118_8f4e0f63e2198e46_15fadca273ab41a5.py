import constInfo
import settings
import systemSetting
import wndMgr
import chat
import app
import player
import uiTaskBar
import net
import uiCharacter
import uiInventory
import uiBonusChanger
if app.ENABLE_VOICE_CHAT:
	import uiVoiceChatConfig
import uiDragonSoul
import uiswitchbot
import uiChat
import uiMessenger
import guild
if app.ENABLE_AURA_SYSTEM:
	import uiaura
if app.ENABLE_EVENT_MANAGER:
	import uiEventCalendar

if app.ENABLE_ODLAMKI_SYSTEM:
	import uiFragments

if app.__AUTO_HUNT__:
	import uiAutoHunt

if app.ENABLE_LOADING_PERFORMANCE:
	import uiWarpShower

if app.ENABLE_LINK_IN_CHAT:
	import os

	

import uiIcons

if app.TAKE_LEGEND_DAMAGE_BOARD_SYSTEM:
	import uiLegendDamageWindow
import uiCasket

import ui
import uiHelp
import uiWhisper
import uiPointReset
import grp
if constInfo.GIFT_CODE_SYSTEM:
	import uigiftcodewindow
import uiShop
import uiBonus
import uiExchange
import uiSystem
import uiRestart
import uiToolTip
import uiMiniMap
import uiParty
import uiSafebox
import uiGuild
import uiWonExchange
import uiQuest
import uiPrivateShopBuilder
import uiCommon
import uiRefine
import uiEquipmentDialog
import uiGameButton
import uiTip
import uiCube
import miniMap
import uiSelectItem
import uiScriptLocale
import event
import localeInfo
import uiremoveitem
import uiCollectWindow
import uiBoosters
if app.ENABLE_RESP_SYSTEM:
	import uiRespawn
if app.ENABLE_ASLAN_BUFF_NPC_SYSTEM:
	import uiBuffNPC
import uiItemShop
import uiGameOption

if app.ENABLE_ACCE_COSTUME_SYSTEM:
	import uiacce
if app.ENABLE_SWITCHBOT:
	import uiSwitchbot
import new_uiWeeklyRank
if app.ENABLE_DUNGEON_INFO_SYSTEM:
	import uiDungeonInfo
if app.ENABLE_NEW_PET_SYSTEM:
	import pet
	import uiPetSystem
	import uicompanion
if app.ENABLE_ARTEFAKT_SYSTEM:
	import uiArtifactSystem
if app.ENABLE_MINIMAP_DUNGEONINFO:
	import uiminimapdungeoninfo
if app.__BL_CHEST_DROP_INFO__:
	import uiChestDropInfo
import uiCards
import chr
if app.ENABLE_SAVE_LOCATION_SYSTEM:
	import uiSaveLocation
if app.ENABLE_MOUNT_SYSTEM:
	import uiMountWindow

import emoji
import uiBattlePass
if app.__ENABLE_POLYMORPH_SYSTEM__:
	import uiPolySystem
import uiRanking
if app.ENABLE_SECONDARY_LEVEL:
	import uiSecondaryLevel
import uiteleport

if app.ENABLE_VS_SHOP_SEARCH:
	import uiShopSearch

if app.ENABLE_OFFLINE_SHOP:
	import uiOfflineShop, uiShopSearch
	import uiShopSearchSimple

if app.ENABLE_OFFLINE_SHOP_SYSTEM:
	import uiOfflineShopBuilder
	import uiOfflineShop

if hasattr(app, "ENABLE_PREMIUM_PRIVATE_SHOP_OFFICIAL") and app.ENABLE_PREMIUM_PRIVATE_SHOP_OFFICIAL:
	import uiPrivateShop
	import uiPrivateShopSearch

IsQBHide = 0
class Interface(object):
	CHARACTER_STATUS_TAB = 1
	CHARACTER_SKILL_TAB = 2

	class NewGoldChat(ui.Window):
		def __init__(self, parent = None, x = 0, y = 0):
			ui.Window.__init__(self)
			self.texts = {}
			self.before_close = app.GetTime() + 5
			self.parent = parent
			self.SpaceBet = 14
			self.maxY = 0
			self.x = x-745
			self.y = y+1
			self.ColorValue = 0xFFFFFFFF
			self.Show()
			
		def GetMaxY(self):
			return self.maxY

		def AddGoldValue(self, text):
			for i in range(len(self.texts)):
				if len(self.texts) == 5 and i == 0:
					self.texts[i].Hide()
				x, y = self.texts[i].GetLocalPosition()
				self.texts[i].SetPosition(x, y-self.SpaceBet)

			i = 0
			if len(self.texts) == 5:
				for i in range(len(self.texts)-1):
					self.texts[i] = self.texts[i+1]
				i = 4
			else:
				i = len(self.texts)
			
			self.texts[i] = ui.TextLine()
			if self.parent != None:
				self.texts[i].SetParent(self.parent)
			self.texts[i].SetPosition(self.x, self.y)
			self.texts[i].SetPackedFontColor(grp.GenerateColor(255./255, 215./255, 76./255, 1))
			self.texts[i].SetHorizontalAlignLeft()
			self.texts[i].SetOutline(TRUE)
			self.texts[i].SetText(text)
			
			self.texts[i].Show()
			self.before_close = app.GetTime() + 10


		def ClearAll(self):
			self.Hide()
			self.texts = {}

		def OnRender(self):
			if len(self.texts) > 0:
				x, y = self.texts[0].GetGlobalPosition()
				w, h = self.texts[0].GetTextSize()
				grp.SetColor(grp.GenerateColor(0.0, 0.0, 0.0, 0.5))
				self.BOARD_START_COLOR = grp.GenerateColor(0.0, 0.0, 0.0, 0.0)
				self.BOARD_END_COLOR = grp.GenerateColor(0.0, 0.0, 0.0, 0.8)
				grp.RenderGradationBar(x, y+h-50, 150, h*8, self.BOARD_START_COLOR, self.BOARD_END_COLOR)
				
		def OnUpdate(self):
			if app.GetTime() >= self.before_close:
				for i in range(len(self.texts)):
					if len(self.texts) > 0 and i == 0:
						self.texts[i].Hide()
						self.texts = {}
					if i == 0:
						return
					x, y = self.texts[i].GetLocalPosition()
					self.texts[i].SetPosition(x, y-self.SpaceBet)

				i = 0
				if len(self.texts) == 5:
					for i in range(len(self.texts)-1):
						self.texts[i] = self.texts[i+1]
					i = 4
				else:
					i = len(self.texts)
				


	def __init__(self):
		systemSetting.SetInterfaceHandler(self)
		if app.__AUTO_HUNT__:
			self.wndAutoHunt = None
		self.windowOpenPosition = 0
		if app.WJ_ENABLE_TRADABLE_ICON:
			self.onTopWindow = player.ON_TOP_WND_NONE
		self.dlgWhisperWithoutTarget = None
		self.inputDialog = None
		self.tipBoard = None
		self.bigBoard = None
		self.mallPageDlg = None
		if app.ENABLE_EVENT_MANAGER:
			self.wndEventManager = None
			self.wndEventIcon = None
		self.wndWeb = None
		self.wndTaskBar = None
		self.wndCharacter = None
		self.wndInventory = None
		self.wndExpandedTaskBar = None
		self.wndDragonSoul = None
		self.wndDragonSoulRefine = None
		self.wndChat = None
		self.yangText = None
		self.wndMessenger = None
		self.wndMiniMap = None
		self.wndGuild = None
		if app.ENABLE_MOUNT_SYSTEM:
			self.wndMountWindow = None
		if app.__BL_CHEST_DROP_INFO__:
			self.wndChestDropInfo = None
		self.wndGuildBuilding = None

		if app.ENABLE_VOICE_CHAT:
			self.wndVoiceChatConfig = None
			self.wndVoiceChatOverlay = None

		if app.ENABLE_OFFLINE_SHOP:
			self.wndShopOffline = None
			self.wndShopSearch = None
			self.wndShopNotification = None

		self.wndCasketPreview = None
		if app.ENABLE_DUNGEON_INFO_SYSTEM:
			self.wndDungeonInfo = None
		self.wndRemoveItem = None
		if app.WJ_SPLIT_INVENTORY_SYSTEM:
			self.wndExtendedInventory = None
		if app.ENABLE_RESP_SYSTEM:
			self.wndResp = None
		if app.__ENABLE_POLYMORPH_SYSTEM__:
			self.wndPolySystem = None

		self.wndBonus = None
		self.wndBoosters = None
		self.wndCollectWindow = None
		self.wndWeeklyRankWindow_New = None
		if app.ENABLE_SWITCHBOT:
			self.wndSwitchbot = None
		if app.ENABLE_SECONDARY_LEVEL:
			self.wndSecondaryLevel = None
		self.wndgameOption = None

		if app.ENABLE_LINK_IN_CHAT:
			self.OpenLinkQuestionDialog = None
			
		self.wndBattlePassButton = None
		self.wndBattlePass = None
		self.wndRankingWindow = None
		self.wndRankingWindowWeekly = None
		self.wndShopSearch = None
		

		if app.ENABLE_ODLAMKI_SYSTEM:
			self.wndFragments = None
		if app.TAKE_LEGEND_DAMAGE_BOARD_SYSTEM:
			self.wndLegendDamageWindow = None

		if app.ENABLE_OFFLINE_SHOP_SYSTEM:
			self.wndOfflineShopAdminPanel = None
			self.wndOfflineShopLogPanel = None
			self.offlineShopAdvertisementBoardDict = {}

		if hasattr(app, "ENABLE_PREMIUM_PRIVATE_SHOP_OFFICIAL") and app.ENABLE_PREMIUM_PRIVATE_SHOP_OFFICIAL:
			self.wndPrivateShopPanel = None
			self.wndPrivateShopSearch = None
			self.privateShopTitleBoardDict = {}

		self.listGMName = {}
		self.wndQuestWindow = {}
		self.wndQuestWindowNewKey = 0
		if app.ENABLE_MINIMAP_DUNGEONINFO:
			self.wndMiniMapDungeonInfo = None

		self.interfaceWindowList = {}
		if app.ENABLE_ASLAN_BUFF_NPC_SYSTEM:
			self.wndBuffNPCWindow = None
			self.wndBuffNPCCreateWindow = None

		if app.ENABLE_VS_SHOP_SEARCH:
			self.wndOfflineShopSearch = None

		self.privateShopAdvertisementBoardDict = {}
		self.guildScoreBoardDict = {}
		self.equipmentDialogDict = {}
		if app.ENABLE_LOADING_PERFORMANCE:
			self.wndWarpShower = None

		if constInfo.ENABLE_EXPANDED_MONEY_TASKBAR:
			self.wndExpandedMoneyTaskBar = None

		event.SetInterfaceWindow(self)

	def GetShopSearchWindow(self):
		if self.wndShopSearch:
			return self.wndShopSearch

		try:
			import uiShopSearch
			self.wndShopSearch = uiShopSearch.ShopSearch()
			self.wndShopSearch.BindInterface(self)
			if hasattr(self, "tooltipItem") and self.tooltipItem:
				self.wndShopSearch.SetItemToolTip(self.tooltipItem)
		except Exception:
			self.wndShopSearch = None

		return self.wndShopSearch

	def __del__(self):
		systemSetting.DestroyInterfaceHandler()
		event.SetInterfaceWindow(None)

	def AppendQueue(self, vnum, value):
		name = chr.GetNameByVID(vnum)
		if value == 1:
			self.yangText.AddGoldValue("|cFFe4ec98"+emoji.AppendEmoji("icon/emoji/sell.png")+" "+str(name))
		elif value == 0:
			self.yangText.AddGoldValue("|cFFf8a6a6"+emoji.AppendEmoji("icon/emoji/buy.png")+" "+str(name))

	# KowalMT2: wolane z C++ (CPythonSystem::NotifyScreenSizeChanged) po kazdej zmianie
	# rozmiaru okna klienta - gracz rozciaga okno za ramke, wiec HUD przyklejony do krawedzi
	# musi przeskoczyc na nowe miejsce. Okna otwierane pozniej same wezma juz nowy rozmiar,
	# bo PythonScriptLoader czyta SCREEN_WIDTH/SCREEN_HEIGHT z wndMgr przy kazdym ladowaniu.
	def OnScreenSizeChange(self, width, height):
		try:
			if self.wndUICurtain:
				self.wndUICurtain.SetSize(width, height)

			if self.wndTaskBar:
				self.wndTaskBar.RefreshScreenLayout()

			if self.wndMiniMap:
				self.wndMiniMap.SetPosition(width - 136, self.wndMiniMap.GetLocalPosition()[1])

			if self.wndChat:
				chatX = width // 2 - self.wndChat.CHAT_WINDOW_WIDTH // 2
				chatY = height - self.wndChat.EDIT_LINE_HEIGHT - 37
				self.wndChat.SetPosition(chatX, chatY)
				self.wndChat.Refresh()

				if self.yangText:
					self.yangText.SetPosition(chatX + 540, chatY + 9)
		except:
			# Ten callback idzie z petli komunikatow okna. Wyjatek w trakcie ciagniecia
			# ramki poszedlby w gore przez WindowProcedure, wiec zapisujemy go i jedziemy
			# dalej - nieprzestawiony HUD jest lepszy niz przerwana obsluga zdarzen.
			import dbg, traceback
			dbg.TraceError("Interface.OnScreenSizeChange: %s" % traceback.format_exc())

	def __MakeUICurtain(self):
		wndUICurtain = ui.Bar("TOP_MOST")
		wndUICurtain.SetSize(wndMgr.GetScreenWidth(), wndMgr.GetScreenHeight())
		wndUICurtain.SetColor(0x77000000)
		wndUICurtain.Hide()
		self.wndUICurtain = wndUICurtain

	def __MakeMessengerWindow(self):
		self.wndMessenger = uiMessenger.MessengerWindow()

		from _weakref import proxy
		self.wndMessenger.SetWhisperButtonEvent(lambda n,i=proxy(self):i.OpenWhisperDialog(n))
		self.wndMessenger.SetGuildButtonEvent(ui.__mem_func__(self.ToggleGuildWindow))

	def __MakeGuildWindow(self):
		self.wndGuild = uiGuild.GuildWindow()

	def __MakeChatWindow(self):

		wndChat = uiChat.ChatWindow()

		wndChat.SetSize(wndChat.CHAT_WINDOW_WIDTH, 0)
		wndChat.SetPosition(wndMgr.GetScreenWidth()//2 - wndChat.CHAT_WINDOW_WIDTH//2, wndMgr.GetScreenHeight() - wndChat.EDIT_LINE_HEIGHT - 37)
		wndChat.SetHeight(200)
		wndChat.Refresh()
		wndChat.Show()

		yangText = self.NewGoldChat(None, wndMgr.GetScreenWidth()//2 - wndChat.CHAT_WINDOW_WIDTH//2 + 540, wndMgr.GetScreenHeight() - wndChat.EDIT_LINE_HEIGHT - 37 + 9)
		self.yangText = yangText

		self.wndChat = wndChat
		self.wndChat.BindInterface(self)
		self.wndChat.SetSendWhisperEvent(ui.__mem_func__(self.OpenWhisperDialogWithoutTarget))
		self.wndChat.SetOpenChatLogEvent(ui.__mem_func__(self.ToggleChatLogWindow))

		if app.ENABLE_AUTO_SHOUT:
			self.wndChat.SetAutoShoutEvent(ui.__mem_func__(self.AutoShoutButton))

	def OnPickMoneyNew(self, money):
		self.yangText.AddGoldValue("|cFFffd74c"+emoji.AppendEmoji("icon/emoji/money_icon_small.png")+" "+"+%s"%(localeInfo.NumberToGoldNotText(money)))

	def OnPickChequeNew(self, money):
		self.yangText.AddGoldValue("|cFFb8b8b8"+emoji.AppendEmoji("icon/emoji/cheque_icon.png")+" "+"+%s"%(localeInfo.NumberToGoldNotText(money)))

	def OnPickPktOsiagNew(self, money):
		self.yangText.AddGoldValue("|cFF85d455"+emoji.AppendEmoji("d:/ymir work/ui/stone_point/stone_point.tga")+" "+"+%s"%(localeInfo.NumberToGoldNotText(money)))

	def __MakeTaskBar(self):
		wndTaskBar = uiTaskBar.TaskBar()
		wndTaskBar.LoadWindow()
		self.wndTaskBar = wndTaskBar
		self.wndTaskBar.SetToggleButtonEvent(uiTaskBar.TaskBar.BUTTON_CHARACTER, ui.__mem_func__(self.ToggleCharacterWindowStatusPage))
		self.wndTaskBar.SetToggleButtonEvent(uiTaskBar.TaskBar.BUTTON_INVENTORY, ui.__mem_func__(self.ToggleInventoryWindow))
		self.wndTaskBar.SetToggleButtonEvent(uiTaskBar.TaskBar.BUTTON_MESSENGER, ui.__mem_func__(self.ToggleMessenger))
		self.wndTaskBar.SetToggleButtonEvent(uiTaskBar.TaskBar.BUTTON_SYSTEM, ui.__mem_func__(self.ToggleSystemDialog))
		if uiTaskBar.TaskBar.IS_EXPANDED:
			self.wndTaskBar.SetToggleButtonEvent(uiTaskBar.TaskBar.BUTTON_EXPAND, ui.__mem_func__(self.ToggleExpandedButton))
			self.wndExpandedTaskBar = uiTaskBar.ExpandedTaskBar()
			self.wndExpandedTaskBar.LoadWindow()
			self.wndExpandedTaskBar.SetToggleButtonEvent(uiTaskBar.ExpandedTaskBar.BUTTON_DRAGON_SOUL, ui.__mem_func__(self.ToggleDragonSoulWindow))

		else:
			self.wndTaskBar.SetToggleButtonEvent(uiTaskBar.TaskBar.BUTTON_CHAT, ui.__mem_func__(self.ToggleChat))

		self.wndEnergyBar = None
		import app
		if app.ENABLE_ENERGY_SYSTEM:
			wndEnergyBar = uiTaskBar.EnergyBar()
			wndEnergyBar.LoadWindow()
			self.wndEnergyBar = wndEnergyBar
			
		if constInfo.ENABLE_EXPANDED_MONEY_TASKBAR:
			self.wndExpandedMoneyTaskBar = uiTaskBar.ExpandedMoneyTaskBar()
			self.wndExpandedMoneyTaskBar.LoadWindow()
			if self.wndInventory:
				self.wndInventory.SetExpandedMoneyBar(self.wndExpandedMoneyTaskBar)

		if hasattr(app, "ENABLE_PREMIUM_PRIVATE_SHOP_OFFICIAL") and app.ENABLE_PREMIUM_PRIVATE_SHOP_OFFICIAL:
			self.wndTaskBar.SetToggleButtonEvent(uiTaskBar.TaskBar.BUTTON_OFFLINE_SHOP, ui.__mem_func__(self.TogglePrivateShopPanelWindowCheck))

	def __MakeParty(self):
		wndParty = uiParty.PartyWindow()
		wndParty.Hide()
		self.wndParty = wndParty

	def __MakeGameButtonWindow(self):
		wndGameButton = uiGameButton.GameButtonWindow()
		wndGameButton.SetTop()
		wndGameButton.Show()
		wndGameButton.SetButtonEvent("STATUS", ui.__mem_func__(self.__OnClickStatusPlusButton))
		wndGameButton.SetButtonEvent("QUEST", ui.__mem_func__(self.__OnClickQuestButton))
		wndGameButton.SetButtonEvent("BUILD", ui.__mem_func__(self.__OnClickBuildButton))

		self.wndGameButton = wndGameButton

	def __IsChatOpen(self):
		return True

	def __MakeWindows(self):
		app.TracyMsg("__MakeWindows START")
		wndCharacter = uiCharacter.CharacterWindow()
		app.TracyMsg("__MakeWindows: wndCharacter done")
		wndInventory = uiInventory.InventoryWindow()
		wndInventory.BindInterfaceClass(self)
		app.TracyMsg("__MakeWindows: wndInventory done")
		if app.WJ_SPLIT_INVENTORY_SYSTEM:
			wndExtendedInventory = uiInventory.ExtendedInventoryWindow()
			wndExtendedInventory.BindInterfaceClass(self)
		app.TracyMsg("__MakeWindows: wndExtendedInventory done")
		if app.ENABLE_DRAGON_SOUL_SYSTEM:
			wndDragonSoul = uiDragonSoul.DragonSoulWindow()
			wndDragonSoul.BindInterfaceClass(self)
			wndDragonSoulRefine = uiDragonSoul.DragonSoulRefineWindow()
		else:
			wndDragonSoul = None
			wndDragonSoulRefine = None
		app.TracyMsg("__MakeWindows: DragonSoul done")

		wndMiniMap = uiMiniMap.MiniMap()
		app.TracyMsg("__MakeWindows: wndMiniMap done")
		wndSafebox = uiSafebox.SafeboxWindow()
		if app.WJ_ENABLE_TRADABLE_ICON:
			wndSafebox.BindInterface(self)
		wndSafebox.BindInterface(self)
		app.TracyMsg("__MakeWindows: wndSafebox done")
		if app.ENABLE_SWITCHBOT:
			self.wndSwitchbot = uiSwitchbot.SwitchbotWindow()
		app.TracyMsg("__MakeWindows: wndSwitchbot done")
		self.wndCasketPreview = uiCasket.CasketDialog()
		app.TracyMsg("__MakeWindows: wndCasketPreview done")
		self.wndBonus = uiBonus.BonusWindow()
		app.TracyMsg("__MakeWindows: wndBonus done")
		self.wndWeeklyRankWindow_New = new_uiWeeklyRank.WeeklyRankWindow()
		app.TracyMsg("__MakeWindows: wndWeeklyRankWindow_New done")
		self.wndCollectWindow = uiCollectWindow.CollectWindow()
		app.TracyMsg("__MakeWindows: wndCollectWindow done")
		self.wndBoosters = uiBoosters.Boosters()
		app.TracyMsg("__MakeWindows: wndBoosters done")
		wndMall = uiSafebox.MallWindow()
		self.wndMall = wndMall

		self.wndWonExchange = uiWonExchange.WonExchangeWindow()
		self.wndWonExchange.BindInterface(self)
		app.TracyMsg("__MakeWindows: Mall+WonExchange done")


		if app.ENABLE_ODLAMKI_SYSTEM:
			wndFragments = uiFragments.FragmentsWindow()
			wndFragments.BindInterfaceClass(self)
			self.wndFragments = wndFragments
		app.TracyMsg("__MakeWindows: wndFragments done")

		wndChatLog = uiChat.ChatLogWindow()
		wndChatLog.BindInterface(self)
		app.TracyMsg("__MakeWindows: wndChatLog done")

		if app.ENABLE_OFFLINE_SHOP:
			self.wndShopOffline = uiOfflineShop.OfflineShopWindow()
			self.wndShopOffline.Hide()
			app.TracyMsg("__MakeWindows: wndShopOffline done")

			# Uproszczona wyszukiwarka (uklad jak w nostalgii). Stara, rozbudowana
			# wersja zostaje w uishopsearch.py - wystarczy podmienic linijke ponizej.
			self.wndShopSearch = uiShopSearchSimple.ShopSearchSimple()
			self.wndShopSearch.Hide()
			app.TracyMsg("__MakeWindows: wndShopSearch done")

			self.wndShopNotification = uiOfflineShop.SoldNotification()
			self.wndShopNotification.Hide()
			app.TracyMsg("__MakeWindows: wndShopNotification done")

		self.wndCharacter = wndCharacter
		self.wndInventory = wndInventory
		self.wndDragonSoul = wndDragonSoul
		self.wndDragonSoulRefine = wndDragonSoulRefine
		if app.WJ_SPLIT_INVENTORY_SYSTEM:
			self.wndExtendedInventory = wndExtendedInventory
		self.wndMiniMap = wndMiniMap
		self.wndSafebox = wndSafebox
		self.wndChatLog = wndChatLog
		if app.__ENABLE_POLYMORPH_SYSTEM__:
			self.wndPolySystem = uiPolySystem.PolySystemWindow()
		if app.ENABLE_LOADING_PERFORMANCE:
			self.wndWarpShower = uiWarpShower.WarpShowerWindow()
		if app.__BL_CHEST_DROP_INFO__:
			self.wndChestDropInfo = uiChestDropInfo.ChestDropInfoWindow()
		if app.ENABLE_DUNGEON_INFO_SYSTEM:
			self.wndDungeonInfo = uiDungeonInfo.DungeonInfoWindow()
			self.wndMiniMap.BindInterfaceClass(self)

		if app.ENABLE_DRAGON_SOUL_SYSTEM:
			self.wndDragonSoul.SetDragonSoulRefineWindow(self.wndDragonSoulRefine)
			self.wndDragonSoulRefine.SetInventoryWindows(self.wndInventory, self.wndDragonSoul)
			self.wndInventory.SetDragonSoulRefineWindow(self.wndDragonSoulRefine)

		app.TracyMsg("__MakeWindows: poly+warp+chest+dungeon done")

		if app.ENABLE_NEW_PET_SYSTEM:
			self.wndCompanionWindow = uicompanion.CompanionWindow(self.wndInventory)
			self.wndCompanionWindow.Hide()
			self.pets_window = self.wndCompanionWindow
		app.TracyMsg("__MakeWindows: companion done")

		if app.ENABLE_ASLAN_BUFF_NPC_SYSTEM:
			self.wndBuffNPCWindow = uiBuffNPC.BuffNPCWindow()
			self.wndBuffNPCCreateWindow = uiBuffNPC.BuffNPCCreateWindow()


		self.wndgameOption = uiGameOption.OptionDialog()
		app.TracyMsg("__MakeWindows: buffNPC+gameOption done")

		if app.ENABLE_ARTEFAKT_SYSTEM:
			self.wndArtifact = uiArtifactSystem.ArtifactWindow()
			self.wndArtifact.Hide()

		if app.TAKE_LEGEND_DAMAGE_BOARD_SYSTEM:
			self.wndLegendDamageWindow = uiLegendDamageWindow.LegendDamageWindow()
			self.wndLegendDamageWindow.Hide()
			self.wndLegendDamageWindow.BindInterfaceClass(self)

		if app.ENABLE_VS_SHOP_SEARCH:
			self.wndOfflineShopSearch = uiShopSearch.SearchWindow()

		if hasattr(app, "ENABLE_PREMIUM_PRIVATE_SHOP_OFFICIAL") and app.ENABLE_PREMIUM_PRIVATE_SHOP_OFFICIAL:
			self.wndPrivateShopPanel = uiPrivateShop.PrivateShopPanel()
			self.wndPrivateShopPanel.BindInterfaceClass(self)
			self.wndPrivateShopPanel.BindInventoryClass(self.wndInventory)
			self.wndPrivateShopPanel.BindDragonSoulInventoryClass(self.wndDragonSoul)

			self.wndDragonSoul.BindPrivateShopClass(self.wndPrivateShopPanel)
			self.wndDragonSoul.BindPrivateShopSearchClass(self.wndPrivateShopSearch)

			self.wndPrivateShopSearch = uiPrivateShopSearch.PrivateShopSeachWindow()
			self.wndPrivateShopSearch.BindInterfaceClass(self)

			self.wndInventory.BindWindow(self.wndPrivateShopPanel)
			self.wndInventory.BindPrivateShopClass(self.wndPrivateShopPanel)
			self.wndInventory.BindPrivateShopSearchClass(self.wndPrivateShopSearch)
		app.TracyMsg("__MakeWindows END")

	if app.ENABLE_NEW_PET_SYSTEM:
		def pet_window_open(self):
			_obj = self.pets_window
			if not _obj:
				return
			if _obj.IsShow():
				_obj.Close()
			else:
				_obj.SetCenterPosition()
				_obj.Show()
				_obj.SwitchToPetMode()

		def OnPetFullSync(self):
			if self.pets_window:
				self.pets_window.BINARY_PetFullSync()

		def OnPetExpUpdate(self):
			if self.pets_window:
				self.pets_window.BINARY_PetExpUpdate()

		def OnPetSkillUpdate(self, skill_index):
			if self.pets_window:
				self.pets_window.BINARY_PetSkillUpdate(skill_index)

		def OnPetDismissed(self):
			if self.pets_window:
				self.pets_window.BINARY_PetDismissed()

	def __MakeDialogs(self):
		app.TracyMsg("__MakeDialogs START")
		self.dlgExchange = uiExchange.ExchangeDialog()
		if app.WJ_ENABLE_TRADABLE_ICON:
			self.dlgExchange.BindInterface(self)
			self.dlgExchange.SetInven(self.wndInventory)
			self.wndInventory.BindWindow(self.dlgExchange)
		self.dlgExchange.LoadDialog()
		self.dlgExchange.SetCenterPosition()
		self.dlgExchange.Hide()
		app.TracyMsg("__MakeDialogs: dlgExchange done")

		self.dlgPointReset = uiPointReset.PointResetDialog()
		self.dlgPointReset.LoadDialog()
		self.dlgPointReset.Hide()
		app.TracyMsg("__MakeDialogs: dlgPointReset done")

		self.dlgShop = uiShop.ShopDialog()
		if app.WJ_ENABLE_TRADABLE_ICON:
			self.dlgShop.BindInterface(self)
		self.dlgShop.LoadDialog()
		self.dlgShop.BindInterface(self)
		self.dlgShop.Hide()
		app.TracyMsg("__MakeDialogs: dlgShop done")

		if app.ENABLE_OFFLINE_SHOP_SYSTEM:
			self.dlgOfflineShop = uiOfflineShop.OfflineShopDialog()
			self.dlgOfflineShop.LoadDialog()
			self.dlgOfflineShop.BindInterfaceClass(self)
			self.dlgOfflineShop.Hide()

			self.offlineShopBuilder = uiOfflineShopBuilder.OfflineShopBuilder()
			if app.WJ_ENABLE_TRADABLE_ICON:
				self.offlineShopBuilder.BindInterface(self)
				self.offlineShopBuilder.SetInven(self.wndInventory)
				self.wndInventory.BindWindow(self.offlineShopBuilder)
			self.offlineShopBuilder.Hide()

		if app.ENABLE_MINIMAP_DUNGEONINFO:
			self.wndMiniMapDungeonInfo = uiminimapdungeoninfo.MiniMapDungeonInfo()

		app.TracyMsg("__MakeDialogs: offlineShop+miniMapDungeon done")

		self.dlgRestart = uiRestart.RestartDialog()
		self.dlgRestart.LoadDialog()
		self.dlgRestart.Hide()
		app.TracyMsg("__MakeDialogs: dlgRestart done")

		self.dlgSystem = uiSystem.SystemDialog()
		self.dlgSystem.LoadDialog()
		self.dlgSystem.SetOpenHelpWindowEvent(ui.__mem_func__(self.OpenHelpWindow))
		self.dlgSystem.SetOpenItemShopEvent(ui.__mem_func__(self.RequestOpenItemShop))

		self.dlgSystem.Hide()
		app.TracyMsg("__MakeDialogs: dlgSystem done")

		self.dlgPassword = uiSafebox.PasswordDialog()
		self.dlgPassword.Hide()

		if app.ENABLE_SECONDARY_LEVEL:
			self.wndSecondaryLevel = uiSecondaryLevel.SecondaryLevelWindow()
		
		self.hyperlinkItemTooltip = uiToolTip.HyperlinkItemToolTip()
		self.hyperlinkItemTooltip.Hide()

		self.tooltipItem = uiToolTip.ItemToolTip()
		self.tooltipItem.Hide()

		self.tooltipSkill = uiToolTip.SkillToolTip()
		self.tooltipSkill.Hide()

		self.privateShopBuilder = uiPrivateShopBuilder.PrivateShopBuilder()
		self.privateShopBuilder.Hide()
		app.TracyMsg("__MakeDialogs: tooltips+privateShop done")

		self.dlgRefineNew = uiRefine.RefineDialogNew()
		if app.WJ_ENABLE_TRADABLE_ICON:
			self.dlgRefineNew.SetInven(self.wndInventory)
			self.wndInventory.BindWindow(self.dlgRefineNew)
		self.dlgRefineNew.Hide()
		app.TracyMsg("__MakeDialogs: dlgRefineNew done")

		self.wndRemoveItem = uiremoveitem.RemoveItemDialog()
		self.wndRemoveItem.Hide()
		app.TracyMsg("__MakeDialogs: wndRemoveItem done")

		if app.ENABLE_RESP_SYSTEM:
			self.wndResp = uiRespawn.RespawnDialog()
			self.wndResp.Hide()
		app.TracyMsg("__MakeDialogs: wndResp done")

		# wndBattlePass + wndRankingWindow + wndRankingWindowWeekly lazy —
		# patrz _EnsureBattlePass / _EnsureRankingWindow / _EnsureRankingWindowWeekly.
		# Konstrukcja zżerała ~135ms na entry-game; odraczamy do pierwszego
		# otwarcia (klik na ikonki) lub BINARY_BattlePass* server push.
		app.TracyMsg("__MakeDialogs: battlepass+ranking deferred")

		self.wndItemShop = uiItemShop.ItemShopWindow()
		self.wndItemShop.Hide()
		app.TracyMsg("__MakeDialogs: wndItemShop done")
		app.TracyMsg("__MakeDialogs END")

	def __MakeHelpWindow(self):
		self.wndHelp = uiHelp.HelpWindow()
		self.wndHelp.LoadDialog()
		self.wndHelp.SetCloseEvent(ui.__mem_func__(self.CloseHelpWindow))
		self.wndHelp.Hide()

	def __MakeTipBoard(self):
		self.tipBoard = uiTip.TipBoard()
		self.tipBoard.Hide()

		self.bigBoard = uiTip.BigBoard()
		self.bigBoard.Hide()

	def __MakeWebWindow(self):
		if constInfo.IN_GAME_SHOP_ENABLE:
			import uiWeb
			self.wndWeb = uiWeb.WebWindow()
			self.wndWeb.LoadWindow()
			self.wndWeb.Hide()

	def __MakeCubeWindow(self):
		self.wndCube = uiCube.CubeWindow()
		self.wndCube.Hide()

	if constInfo.GIFT_CODE_SYSTEM:
		def __MakeGiftCodeWindow(self):
			self.wndGiftCodeWindow = uigiftcodewindow.UiGiftCodeWindow()
			self.wndGiftCodeWindow.LoadWindow()
			self.wndGiftCodeWindow.Hide()
		
	def __MakeChangerWindow(self):
		self.wndChangerWindow = uiBonusChanger.ChangerWindow()
		self.wndChangerWindow.LoadWindow()
		self.wndChangerWindow.Hide()

	def __MakeCardsInfoWindow(self):
		self.wndCardsInfo = uiCards.CardsInfoWindow()
		self.wndCardsInfo.LoadWindow()
		self.wndCardsInfo.Hide()
		
	def __MakeCardsWindow(self):
		self.wndCards = uiCards.CardsWindow()
		self.wndCards.LoadWindow()
		self.wndCards.Hide()
		
	def __MakeCardsIconWindow(self):
		self.wndCardsIcon = uiCards.IngameWindow()
		self.wndCardsIcon.LoadWindow()
		self.wndCardsIcon.Hide()

	def __MakeIsIconWindow(self):
		self.wndIsIcon = uiIcons.IngameIconPanel()
		self.wndIsIcon.BindInterfaceClass(self)
		self.wndIsIcon.LoadWindow()
		self.wndIsIcon.Show()

	if app.ENABLE_ACCE_COSTUME_SYSTEM:
		def __MakeAcceWindow(self):
			self.wndAcceCombine = uiacce.CombineWindow()
			self.wndAcceCombine.LoadWindow()
			self.wndAcceCombine.Hide()

			self.wndAcceAbsorption = uiacce.AbsorbWindow()
			self.wndAcceAbsorption.LoadWindow()
			self.wndAcceAbsorption.Hide()

			if self.wndInventory:
				self.wndInventory.SetAcceWindow(self.wndAcceCombine, self.wndAcceAbsorption)

		def AcceMaterials(self, id, vnum, count):
			self.wndAcceCombine.SendMaterials(id, vnum, count)

	if app.ENABLE_AURA_SYSTEM:
		def __MakeAuraWindow(self):
			self.wndAuraRefine = uiaura.RefineWindow(self.wndInventory, self)
			self.wndAuraRefine.LoadWindow()
			self.wndAuraRefine.Hide()
	
			self.wndAuraAbsorption = uiaura.AbsorbWindow(self.wndInventory, self)
			self.wndAuraAbsorption.LoadWindow()
			self.wndAuraAbsorption.Hide()
			
			if self.wndInventory:
				self.wndInventory.SetAuraWindow(self.wndAuraAbsorption, self.wndAuraRefine)

	def __MakeItemSelectWindow(self):
		self.wndItemSelect = uiSelectItem.SelectItemWindow()
		self.wndItemSelect.Hide()

	if app.ENABLE_HIDE_COSTUME_SYSTEM:
		def RefreshVisibleCostume(self):
			self.wndInventory.RefreshVisibleCostume()

	if app.ENABLE_MOUNT_SYSTEM:
		def __MountWindow(self):
			if hasattr(self, 'wndCompanionWindow') and self.wndCompanionWindow:
				self.wndMountWindow = self.wndCompanionWindow
			else:
				self.wndMountWindow = uiMountWindow.MountWindow()
				self.wndMountWindow.SetItemToolTip(self.tooltipItem)
			self.wndMountWindow.Hide()

	def MakeInterface(self):
		app.TracyMsg("MakeInterface START")
		self.__MakeMessengerWindow()
		self.__MakeGuildWindow()
		self.__MakeChatWindow()
		self.__MakeParty()

		self.__MakeIsIconWindow()
		app.TracyMsg("MakeInterface: messenger+guild+chat+party+icons done")

		self.__MakeWindows()
		app.TracyMsg("MakeInterface: __MakeWindows done")
		self.__MakeDialogs()
		app.TracyMsg("MakeInterface: __MakeDialogs done")

		self.__MakeUICurtain()
		self.__MakeTaskBar()
		self.__MakeGameButtonWindow()
		self.__MakeHelpWindow()
		self.__MakeTipBoard()
		app.TracyMsg("MakeInterface: curtain+taskbar+gamebutton+help+tip done")

		if app.ENABLE_OFFLINE_SHOP:
			self.wndShopOffline.SetItemToolTip(self.tooltipItem)
			self.wndShopOffline.BindInterface(self)
			self.wndShopSearch.SetItemToolTip(self.tooltipItem)
			self.wndShopSearch.BindInterface(self)

		self.__MakeWebWindow()
		self.__MakeCubeWindow()
		if app.ENABLE_VOICE_CHAT:
			self.wndVoiceChatConfig = uiVoiceChatConfig.VoiceChatConfig()
			self.wndVoiceChatOverlay = uiVoiceChatConfig.SpeakerQueue()
		if constInfo.GIFT_CODE_SYSTEM:
			self.__MakeGiftCodeWindow()
		app.TracyMsg("MakeInterface: web+cube+giftcode done")

		if app.ENABLE_SAVE_LOCATION_SYSTEM:
			self.__MakeSaveLocationWindow()
		if app.ENABLE_MOUNT_SYSTEM:
			self.__MountWindow()
		self.__MakeChangerWindow()
		self.__MakeCardsInfoWindow()
		self.__MakeCardsWindow()
		self.__MakeCardsIconWindow()
		if app.ENABLE_ACCE_COSTUME_SYSTEM:
			self.__MakeAcceWindow()
		if app.ENABLE_AURA_SYSTEM:
			self.__MakeAuraWindow()
		app.TracyMsg("MakeInterface: location+mount+changer+cards+acce+aura done")

		self.__MakeItemSelectWindow()

		self.questButtonList = []
		self.whisperButtonList = []
		self.whisperDialogDict = {}
		self.privateShopAdvertisementBoardDict = {}

		self.wndInventory.SetItemToolTip(self.tooltipItem)
		if app.ENABLE_DRAGON_SOUL_SYSTEM:
			self.wndDragonSoul.SetItemToolTip(self.tooltipItem)
			self.wndDragonSoulRefine.SetItemToolTip(self.tooltipItem)
		self.wndSafebox.SetItemToolTip(self.tooltipItem)
		if app.ENABLE_SWITCHBOT:
			self.wndSwitchbot.SetItemToolTip(self.tooltipItem)

		if app.ENABLE_ACCE_COSTUME_SYSTEM:
			self.wndAcceCombine.SetItemToolTip(self.tooltipItem)
			self.wndAcceAbsorption.SetItemToolTip(self.tooltipItem)

		if app.ENABLE_AURA_SYSTEM:
			self.wndAuraAbsorption.SetItemToolTip(self.tooltipItem)
			self.wndAuraRefine.SetItemToolTip(self.tooltipItem)
		if app.ENABLE_SECONDARY_LEVEL:
			self.wndSecondaryLevel.SetItemToolTip(self.tooltipItem)
		self.wndMall.SetItemToolTip(self.tooltipItem)
		if app.ENABLE_NEW_PET_SYSTEM and hasattr(self, 'wndCompanionWindow') and self.wndCompanionWindow:
			self.wndCompanionWindow.SetItemToolTip(self.tooltipItem)

		self.wndCharacter.SetSkillToolTip(self.tooltipSkill)
		self.wndTaskBar.SetItemToolTip(self.tooltipItem)
		self.wndTaskBar.SetSkillToolTip(self.tooltipSkill)
		self.wndGuild.SetSkillToolTip(self.tooltipSkill)

		if app.ENABLE_ASLAN_BUFF_NPC_SYSTEM:
			self.wndBuffNPCWindow.SetSkillToolTip(self.tooltipSkill)


		self.wndItemSelect.SetItemToolTip(self.tooltipItem)
		self.dlgShop.SetItemToolTip(self.tooltipItem)
		self.dlgExchange.SetItemToolTip(self.tooltipItem)
		self.privateShopBuilder.SetItemToolTip(self.tooltipItem)
		self.wndRemoveItem.SetItemToolTip(self.tooltipItem)
		if app.__ENABLE_POLYMORPH_SYSTEM__:
			self.wndPolySystem.SetToolTip(self.tooltipItem)
		if app.ENABLE_ODLAMKI_SYSTEM:
			self.wndFragments.SetItemToolTip(self.tooltipItem)
		if app.WJ_SPLIT_INVENTORY_SYSTEM:
			self.wndExtendedInventory.SetItemToolTip(self.tooltipItem)
		if app.ENABLE_RESP_SYSTEM:
			self.wndResp.SetItemToolTip(self.tooltipItem)
		if hasattr(app, "ENABLE_PREMIUM_PRIVATE_SHOP_OFFICIAL") and app.ENABLE_PREMIUM_PRIVATE_SHOP_OFFICIAL:
			self.wndPrivateShopPanel.SetItemToolTip(self.tooltipItem)
			self.wndPrivateShopSearch.SetItemToolTip(self.tooltipItem)
			self.privateShopTitleBoardDict = {}
		if app.ENABLE_OFFLINE_SHOP_SYSTEM:
			self.dlgOfflineShop.SetItemToolTip(self.tooltipItem)
			self.offlineShopBuilder.SetItemToolTip(self.tooltipItem)
		app.TracyMsg("MakeInterface: tooltip wiring done")
		self.__InitWhisper()
		app.TracyMsg("MakeInterface: __InitWhisper done")
		self.__InitializeWindow()
		app.TracyMsg("MakeInterface: __InitializeWindow done")
		app.TracyMsg("MakeInterface END")

	def __InitializeWindow(self):
		# DungeonTrack lazy — patrz __EnsureDungeonTrack.
		# Konstrukcja zżerała ~300ms na entry-game (import uidungeontrack +
		# DungeonTrack() ctor); odraczamy do pierwszego ToggleMapWindow /
		# OpenDungeonInfo (z hotkey TAB lub /minimap).
		self.wndDungeonTrack = None

	def __EnsureDungeonTrack(self):
		if self.wndDungeonTrack is None:
			app.TracyMsg("DungeonTrack lazy-create START")
			import uidungeontrack
			self.wndDungeonTrack = uidungeontrack.DungeonTrack()
			self.wndDungeonTrack.Hide()
			self.AppendInterfaceWindow("teleport", self.wndDungeonTrack)
			app.TracyMsg("DungeonTrack lazy-create END")
		return self.wndDungeonTrack

	# Lazy constructors — patrz komentarz w __MakeDialogs.
	# Single underscore: dostępne też z game.py (BINARY_BattlePass*).
	def _EnsureBattlePass(self):
		if self.wndBattlePass is None:
			app.TracyMsg("BattlePass lazy-create START")
			self.wndBattlePass = uiBattlePass.BattlePassWindow()
			self.wndBattlePass.Hide()
			app.TracyMsg("BattlePass lazy-create END")
		return self.wndBattlePass

	def _EnsureRankingWindow(self):
		if self.wndRankingWindow is None:
			app.TracyMsg("RankingWindow lazy-create START")
			self.wndRankingWindow = uiRanking.RankingWindow()
			app.TracyMsg("RankingWindow lazy-create END")
		return self.wndRankingWindow

	def _EnsureRankingWindowWeekly(self):
		if self.wndRankingWindowWeekly is None:
			app.TracyMsg("RankingWindowWeekly lazy-create START")
			self.wndRankingWindowWeekly = uiRanking.WeeklyRankingWindow()
			app.TracyMsg("RankingWindowWeekly lazy-create END")
		return self.wndRankingWindowWeekly

	def AppendInterfaceWindow(self, name, window):
		self.interfaceWindowList[name] = window

	def ToggleMapWindow(self):
		wnd = self.__EnsureDungeonTrack()
		if wnd.IsShow() and getattr(wnd, "currentPage", 1) == 1:
			wnd.Hide()
		else:
			wnd.OpenOnMapPage()

	def ToggleDungeonTrackWindow(self):
		wnd = self.__EnsureDungeonTrack()
		if wnd.IsShow() and getattr(wnd, "currentPage", 0) == 0:
			wnd.Hide()
		else:
			wnd.OpenOnDungeonPage()

	def OpenDungeonInfo(self):
		wnd = self.__EnsureDungeonTrack()
		if wnd.IsShow():
			wnd.Hide()
		else:
			wnd.Open()
 
	def MakeHyperlinkTooltip(self, hyperlink):
		tokens = hyperlink.split(":")
		if tokens and len(tokens):
			type = tokens[0]
			if "item" == type:
				self.hyperlinkItemTooltip.SetHyperlinkItem(tokens)
			elif type in ("whisper", "szept"):
				self.OpenWhisperDialog(str(tokens[1]))

			elif app.ENABLE_LINK_IN_CHAT and "web" == type and (tokens[1].startswith("httpXxX") or tokens[1].startswith("httpsXxX")):
					safeUrl = tokens[1].replace("XxX", "://")
					if not safeUrl.startswith("http://") and not safeUrl.startswith("https://"):
						return
					for c in ['|', '&', ';', '"', "'", '`', '$', '%', '(', ')', '<', '>', '\\']:
						if c in safeUrl:
							return
					OpenLinkQuestionDialog = uiCommon.QuestionDialog2()
					OpenLinkQuestionDialog.SetText1(localeInfo.CHAT_OPEN_LINK_DANGER)
					OpenLinkQuestionDialog.SetText2(safeUrl[:80])
					OpenLinkQuestionDialog.SetAcceptEvent(lambda arg=True: self.AnswerOpenLink(arg))
					OpenLinkQuestionDialog.SetCancelEvent(lambda arg=False: self.AnswerOpenLink(arg))
					self.pendingLinkUrl = safeUrl
					OpenLinkQuestionDialog.Open()
					self.OpenLinkQuestionDialog = OpenLinkQuestionDialog


	if app.ENABLE_LINK_IN_CHAT:
		def AnswerOpenLink(self, answer):
			if not self.OpenLinkQuestionDialog:
				return

			self.OpenLinkQuestionDialog.Close()
			self.OpenLinkQuestionDialog = None

			if not answer:
				return

			import webbrowser
			url = getattr(self, 'pendingLinkUrl', '')
			if url and (url.startswith("http://") or url.startswith("https://")):
				webbrowser.open(url)


	if app.__AUTO_HUNT__:
		def AutoHuntStatus(self, status):
			isActive = True if int(status) else False
			constInfo.AUTO_HUNT_ACTIVE = 1 if isActive else 0
			if self.wndAutoHunt:
				self.wndAutoHunt.SetStatus(isActive)

		def CheckAutoLogin(self):
			if self.wndAutoHunt == None:
				self.wndAutoHunt = uiAutoHunt.Window()
			self.wndAutoHunt.CheckAutoLogin()

		def OpenAutoHunt(self):
			# Auto-hunt tymczasowo wylaczony — panel ma sie NIE otwierac (narazie). Reszta metody martwa.
			return
			if self.wndAutoHunt == None:
				self.wndAutoHunt = uiAutoHunt.Window()
			if self.wndAutoHunt.IsShow():
				self.wndAutoHunt.Close()
			else:
				self.wndAutoHunt.Open()

	def Close(self):
		# Tabela obrazen bossa dopisywala wpis na kazdy VID bossa i nigdy go nie kasowala
		# (zero "del" w calym drzewie), wiec slownik rosl przez cala sesje i przezywal relog.
		# VID-y sa wazne tylko w obrebie jednej sesji gry.
		if app.TAKE_LEGEND_DAMAGE_BOARD_SYSTEM:
			constInfo.LEGEND_DAMAGE_DATA.clear()

		if app.__AUTO_HUNT__:
			if self.wndAutoHunt:
				self.wndAutoHunt.Close()
				self.wndAutoHunt.Destroy()
				self.wndAutoHunt = None
		if app.ENABLE_EVENT_MANAGER:
			if self.wndEventManager:
				self.wndEventManager.Hide()
				self.wndEventManager.Destroy()
				self.wndEventManager = None

			if self.wndEventIcon:
				self.wndEventIcon.Hide()
				self.wndEventIcon.Destroy()
				self.wndEventIcon = None

		if self.wndRankingWindow:
			self.wndRankingWindow.Destroy()

		if self.wndRankingWindowWeekly:
			self.wndRankingWindowWeekly.Destroy()

		if app.ENABLE_SECONDARY_LEVEL:
			if self.wndSecondaryLevel:
				self.wndSecondaryLevel.Destroy()
				
		if self.dlgWhisperWithoutTarget:
			self.dlgWhisperWithoutTarget.Destroy()
			del self.dlgWhisperWithoutTarget

		if "QuestCurtain" in uiQuest.QuestDialog.__dict__:
			uiQuest.QuestDialog.QuestCurtain.Close()

		if self.wndQuestWindow:
			for key, eachQuestWindow in list(self.wndQuestWindow.items()):
				eachQuestWindow.nextCurtainMode = -1
				eachQuestWindow.CloseSelf()
				eachQuestWindow = None
		self.wndQuestWindow = {}

		if self.wndChat:
			self.wndChat.hide_btnChatSizing()
			self.wndChat.Destroy()

		if self.wndTaskBar:
			self.wndTaskBar.Destroy()

		if self.yangText:
			self.yangText.ClearAll()

		if self.wndExpandedTaskBar:
			self.wndExpandedTaskBar.Destroy()

		if self.wndEnergyBar:
			self.wndEnergyBar.Destroy()

		if self.wndCharacter:
			self.wndCharacter.Destroy()

		if self.wndInventory:
			self.wndInventory.Destroy()

		if app.WJ_SPLIT_INVENTORY_SYSTEM:
			if self.wndExtendedInventory:
				self.wndExtendedInventory.Destroy()

		if self.wndDragonSoul:
			self.wndDragonSoul.Destroy()

		if self.wndDragonSoulRefine:
			self.wndDragonSoulRefine.Destroy()

		if self.dlgExchange:
			self.dlgExchange.Destroy()

		if self.dlgPointReset:
			self.dlgPointReset.Destroy()

		if self.dlgShop:
			self.dlgShop.Destroy()

		if self.dlgRestart:
			self.dlgRestart.Destroy()

		if self.dlgSystem:
			self.dlgSystem.Destroy()

		if self.dlgPassword:
			self.dlgPassword.Destroy()

		if app.ENABLE_SAVE_LOCATION_SYSTEM and self.wndSaveLocation:
			self.wndSaveLocation.Destroy()
				
		if app.ENABLE_MOUNT_SYSTEM:
			if self.wndMountWindow:
				self.wndMountWindow.Destroy()

		if self.wndMiniMap:
			self.wndMiniMap.Destroy()

		if self.wndSafebox:
			self.wndSafebox.Destroy()

		if self.wndWeb:
			self.wndWeb.Destroy()
			self.wndWeb = None

		if self.wndMall:
			self.wndMall.Destroy()

		if self.wndParty:
			self.wndParty.Destroy()

		if self.wndHelp:
			self.wndHelp.Destroy()

		if self.wndCardsInfo:
			self.wndCardsInfo.Destroy()

		if self.wndCards:
			self.wndCards.Destroy()

		if self.wndCardsIcon:
			self.wndCardsIcon.Destroy()
				
		if app.ENABLE_ARTEFAKT_SYSTEM:
			if self.wndArtifact:
				self.wndArtifact.Destroy()
				del self.wndArtifact

		if self.wndCube:
			self.wndCube.Destroy()

		if constInfo.GIFT_CODE_SYSTEM:
			if self.wndGiftCodeWindow:
				self.wndGiftCodeWindow.Destroy()

		if app.ENABLE_ACCE_COSTUME_SYSTEM and self.wndAcceCombine:
			self.wndAcceCombine.Destroy()

		if app.ENABLE_ACCE_COSTUME_SYSTEM and self.wndAcceAbsorption:
			self.wndAcceAbsorption.Destroy()

		if app.ENABLE_AURA_SYSTEM:
			if self.wndAuraAbsorption:
				self.wndAuraAbsorption.Destroy()

			if self.wndAuraRefine:
				self.wndAuraRefine.Destroy()

		if app.ENABLE_LOADING_PERFORMANCE:
			if self.wndWarpShower:
				self.wndWarpShower.Destroy()
				del self.wndWarpShower

		if self.wndMessenger:
			self.wndMessenger.Destroy()

		if self.wndGuild:
			self.wndGuild.Destroy()
		
		if app.ENABLE_NEW_PET_SYSTEM and self.pets_window:
			self.pets_window.Destroy()

		if self.privateShopBuilder:
			self.privateShopBuilder.Destroy()

		if self.wndChangerWindow:
			self.wndChangerWindow.Destroy()

		if self.dlgRefineNew:
			self.dlgRefineNew.Destroy()
		

		if self.wndGuildBuilding:
			self.wndGuildBuilding.Destroy()

		if app.ENABLE_VOICE_CHAT:
			if self.wndVoiceChatConfig:
				self.wndVoiceChatConfig.Hide()
				self.wndVoiceChatConfig.Destroy()
				del self.wndVoiceChatConfig
				self.wndVoiceChatConfig = None

			if self.wndVoiceChatOverlay:
				self.wndVoiceChatOverlay.Hide()
				self.wndVoiceChatOverlay.Destroy()
				del self.wndVoiceChatOverlay
				self.wndVoiceChatOverlay = None

		if app.__ENABLE_POLYMORPH_SYSTEM__:
			if self.wndPolySystem:
				self.wndPolySystem.Destroy()

		if self.wndgameOption:
			self.wndgameOption.Hide()
			self.wndgameOption.Destroy()
			del self.wndgameOption

		if self.wndGameButton:
			self.wndGameButton.Destroy()
		if hasattr(app, "ENABLE_PREMIUM_PRIVATE_SHOP_OFFICIAL") and app.ENABLE_PREMIUM_PRIVATE_SHOP_OFFICIAL:
			if self.wndPrivateShopPanel:
				self.wndPrivateShopPanel.Hide()
				self.wndPrivateShopPanel.Destroy()

			if self.wndPrivateShopSearch:
				self.wndPrivateShopSearch.Hide()
				self.wndPrivateShopSearch.Destroy()

			del self.wndPrivateShopPanel
			del self.wndPrivateShopSearch
			self.privateShopTitleBoardDict = {}

		if app.__BL_CHEST_DROP_INFO__:
			if self.wndChestDropInfo:
				del self.wndChestDropInfo



		if self.wndIsIcon:
			self.wndIsIcon.Destroy()


		if self.mallPageDlg:
			self.mallPageDlg.Destroy()

		if app.ENABLE_OFFLINE_SHOP:
			if self.wndShopOffline:
				self.wndShopOffline.Hide()
				self.wndShopOffline.Destroy()
				del self.wndShopOffline

			if self.wndShopSearch:
				self.wndShopSearch.Hide()
				self.wndShopSearch.Destroy()
				del self.wndShopSearch

			if self.wndShopNotification:
				self.wndShopNotification.Hide()
				self.wndShopNotification.Destroy()
				del self.wndShopNotification

		if self.wndItemSelect:
			self.wndItemSelect.Destroy()

		if app.ENABLE_MINIMAP_DUNGEONINFO:
			if self.wndMiniMapDungeonInfo:
				self.wndMiniMapDungeonInfo.Destroy()

		if self.wndRemoveItem:
			self.wndRemoveItem.Destroy()
			del self.wndRemoveItem

		if app.ENABLE_ASLAN_BUFF_NPC_SYSTEM:
			if self.wndBuffNPCWindow:
				self.wndBuffNPCWindow.Destroy()
			if self.wndBuffNPCCreateWindow:
				self.wndBuffNPCCreateWindow.Destroy()

		if app.ENABLE_VS_SHOP_SEARCH:
			if self.wndOfflineShopSearch:
				self.wndOfflineShopSearch.Destroy()

		if app.ENABLE_OFFLINE_SHOP_SYSTEM:
			if (self.dlgOfflineShop):
				self.dlgOfflineShop.Destroy()

			if (self.offlineShopBuilder):
				self.offlineShopBuilder.Destroy()

			if (self.wndOfflineShopAdminPanel):
				self.wndOfflineShopAdminPanel.Destroy()

			if (self.wndOfflineShopLogPanel):
				self.wndOfflineShopLogPanel.Destroy()

		if app.ENABLE_RESP_SYSTEM:
			if self.wndResp:
				self.wndResp.Destroy()

				del self.wndResp

		if app.ENABLE_ODLAMKI_SYSTEM:
			if self.wndFragments:
				self.wndFragments.Destroy()

		if self.wndItemShop:
			self.wndItemShop.Destroy()
			del self.wndItemShop
		
		if self.wndCasketPreview:
			self.wndCasketPreview.Destroy()
			del self.wndCasketPreview

		if app.ENABLE_SWITCHBOT:
			if self.wndSwitchbot:
				self.wndSwitchbot.Destroy()

		if self.wndBonus:
			self.wndBonus.Destroy()
		
		if self.wndCollectWindow:
			self.wndCollectWindow.Destroy()

		if self.wndWeeklyRankWindow_New:
			self.wndWeeklyRankWindow_New.Destroy()

		if self.wndBoosters:
			self.wndBoosters.Destroy()

		if constInfo.ENABLE_EXPANDED_MONEY_TASKBAR:
			if self.wndExpandedMoneyTaskBar:
				self.wndExpandedMoneyTaskBar.Destroy()

		if app.TAKE_LEGEND_DAMAGE_BOARD_SYSTEM:
			if self.wndLegendDamageWindow:
				self.wndLegendDamageWindow.Destroy()
				del self.wndLegendDamageWindow

		if self.wndBattlePassButton:
			self.wndBattlePassButton.Hide(True)
			self.wndBattlePassButton.Destroy()
			del self.wndBattlePassButton
			
		if self.wndBattlePass:
			self.wndBattlePass.Hide()
			self.wndBattlePass.Destroy()
			del self.wndBattlePass

		self.wndChatLog.Destroy()
		if app.ENABLE_DUNGEON_INFO_SYSTEM:
			if self.wndDungeonInfo:
				self.wndDungeonInfo.Destroy()
				del self.wndDungeonInfo

		for btn in self.questButtonList:
			btn.SetEvent(0)
		for btn in self.whisperButtonList:
			btn.SetEvent(0)
		for dlg in self.whisperDialogDict.values():
			dlg.Destroy()
		for brd in self.guildScoreBoardDict.values():
			brd.Destroy()
		for dlg in self.equipmentDialogDict.values():
			dlg.Destroy()

		del self.mallPageDlg
		
		if app.ENABLE_MINIMAP_DUNGEONINFO:
			del self.wndMiniMapDungeonInfo

		del self.wndGuild
		del self.wndMessenger
		del self.wndUICurtain
		del self.wndChat
		del self.yangText
		del self.wndTaskBar
		del self.wndWonExchange
		if self.wndExpandedTaskBar:
			del self.wndExpandedTaskBar
		del self.wndEnergyBar
		del self.wndCharacter
		del self.wndInventory
		if app.__ENABLE_POLYMORPH_SYSTEM__:
			del self.wndPolySystem
		if self.wndDragonSoul:
			del self.wndDragonSoul
		if self.wndDragonSoulRefine:
			del self.wndDragonSoulRefine
		del self.dlgExchange
		del self.dlgPointReset
		del self.dlgShop
		del self.dlgRestart
		del self.dlgSystem
		del self.dlgPassword
		del self.hyperlinkItemTooltip
		del self.tooltipItem
		del self.tooltipSkill
		del self.wndMiniMap
		del self.wndSafebox
		del self.wndMall
		del self.wndParty
		del self.wndHelp

		del self.wndCardsInfo
		del self.wndCards
		del self.wndCardsIcon

		if app.ENABLE_SAVE_LOCATION_SYSTEM:
			del self.wndSaveLocation
		if app.ENABLE_MOUNT_SYSTEM:
			del self.wndMountWindow

		del self.wndCube
		if constInfo.GIFT_CODE_SYSTEM:
			del self.wndGiftCodeWindow
		del self.privateShopBuilder
		del self.inputDialog
		del self.wndChatLog
		del self.dlgRefineNew
		del self.wndGuildBuilding
		if app.ENABLE_NEW_PET_SYSTEM and self.pets_window:
			del self.pets_window
		del self.wndGameButton
		del self.wndIsIcon
		del self.tipBoard
		del self.bigBoard
		del self.wndItemSelect
		del self.wndChangerWindow
		if app.WJ_SPLIT_INVENTORY_SYSTEM:
			if self.wndExtendedInventory:
				del self.wndExtendedInventory
		if app.ENABLE_SWITCHBOT:
			del self.wndSwitchbot	
		del self.wndBonus
		del self.wndCollectWindow
		del self.wndWeeklyRankWindow_New
		del self.wndBoosters

		if app.ENABLE_ODLAMKI_SYSTEM:
			del self.wndFragments

		if app.ENABLE_ACCE_COSTUME_SYSTEM:
			del self.wndAcceCombine
			del self.wndAcceAbsorption

		if app.ENABLE_AURA_SYSTEM:
			del self.wndAuraAbsorption
			del self.wndAuraRefine
			
		if app.ENABLE_SECONDARY_LEVEL:
			del self.wndSecondaryLevel

		del self.wndRankingWindow

		del self.wndRankingWindowWeekly

		if app.ENABLE_ASLAN_BUFF_NPC_SYSTEM:
			del self.wndBuffNPCWindow
			del self.wndBuffNPCCreateWindow

		if app.ENABLE_OFFLINE_SHOP_SYSTEM:
			del self.dlgOfflineShop
			del self.wndOfflineShopAdminPanel
			del self.wndOfflineShopLogPanel
			self.offlineShopAdvertisementBoardDict = {}

		if app.ENABLE_VS_SHOP_SEARCH:
			del self.wndOfflineShopSearch

		if constInfo.ENABLE_EXPANDED_MONEY_TASKBAR:
			if self.wndExpandedMoneyTaskBar:
				del self.wndExpandedMoneyTaskBar

		self.questButtonList = []
		self.whisperButtonList = []
		self.whisperDialogDict = {}
		self.privateShopAdvertisementBoardDict = {}
		self.guildScoreBoardDict = {}
		self.equipmentDialogDict = {}

		uiChat.DestroyChatInputSetWindow()
		
		for window in self.interfaceWindowList.values():
			window.Destroy()
		self.interfaceWindowList.clear()	
  
	def OnUseSkill(self, slotIndex, coolTime):
		self.wndCharacter.OnUseSkill(slotIndex, coolTime)
		self.wndTaskBar.OnUseSkill(slotIndex, coolTime)
		self.wndGuild.OnUseSkill(slotIndex, coolTime)

	def OnActivateSkill(self, slotIndex):
		self.wndCharacter.OnActivateSkill(slotIndex)
		self.wndTaskBar.OnActivateSkill(slotIndex)

	def OnDeactivateSkill(self, slotIndex):
		self.wndCharacter.OnDeactivateSkill(slotIndex)
		self.wndTaskBar.OnDeactivateSkill(slotIndex)

	def OnChangeCurrentSkill(self, skillSlotNumber):
		self.wndTaskBar.OnChangeCurrentSkill(skillSlotNumber)

	def SelectMouseButtonEvent(self, dir, event):
		self.wndTaskBar.SelectMouseButtonEvent(dir, event)

	def RefreshAlignment(self):
		self.wndCharacter.RefreshAlignment()

	def RefreshStatus(self):
		self.wndTaskBar.RefreshStatus()
		self.wndCharacter.RefreshStatus()
		self.wndInventory.RefreshStatus()
		if self.wndEnergyBar:
			self.wndEnergyBar.RefreshStatus()
		if app.WJ_SPLIT_INVENTORY_SYSTEM:
			self.wndExtendedInventory.RefreshStatus()
		if app.ENABLE_DRAGON_SOUL_SYSTEM:
			self.wndDragonSoul.RefreshStatus()
	def RefreshStamina(self):
		self.wndTaskBar.RefreshStamina()

	def RefreshSkill(self):
		self.wndCharacter.RefreshSkill()
		self.wndTaskBar.RefreshSkill()

	def RefreshInventory(self):
		self.wndTaskBar.RefreshQuickSlot()
		self.wndInventory.RefreshItemSlot()
		if constInfo.IS_BONUS_CHANGER:
			self.UpdateBonusChanger()
		if app.ENABLE_DRAGON_SOUL_SYSTEM:
			self.wndDragonSoul.RefreshItemSlot()
		if app.ENABLE_ASLAN_BUFF_NPC_SYSTEM:
			self.wndBuffNPCWindow.RefreshEquipSlotWindow()
		if app.WJ_SPLIT_INVENTORY_SYSTEM:
			self.wndExtendedInventory.RefreshItemSlot()
		if app.ENABLE_ARTEFAKT_SYSTEM:
			self.wndArtifact.RefreshSlot()
	def RefreshCharacter(self):
		self.wndCharacter.RefreshCharacter()
		self.wndTaskBar.RefreshQuickSlot()

	def RefreshQuest(self):
		self.wndCharacter.RefreshQuest()

	def RefreshSafebox(self):
		self.wndSafebox.RefreshSafebox()

	def RefreshMall(self):
		self.wndMall.RefreshMall()

	if app.ENABLE_ARTEFAKT_SYSTEM:
		def OpenArtifactWindow(self):
			if self.wndArtifact.IsShow():
				self.wndArtifact.Hide()
			else:
				self.wndArtifact.Open()

	def OpenItemMall(self):
		if not self.mallPageDlg:
			self.mallPageDlg = uiShop.MallPageDialog()

		self.mallPageDlg.Open()

	def RefreshMessenger(self):
		self.wndMessenger.RefreshMessenger()

	def RefreshGuildInfoPage(self):
		self.wndGuild.RefreshGuildInfoPage()

	def RefreshGuildBoardPage(self):
		self.wndGuild.RefreshGuildBoardPage()

	def RefreshGuildMemberPage(self):
		self.wndGuild.RefreshGuildMemberPage()

	def RefreshGuildMemberPageGradeComboBox(self):
		self.wndGuild.RefreshGuildMemberPageGradeComboBox()

	def RefreshGuildSkillPage(self):
		self.wndGuild.RefreshGuildSkillPage()

	def RefreshGuildGradePage(self):
		self.wndGuild.RefreshGuildGradePage()

	def DeleteGuild(self):
		self.wndMessenger.ClearGuildMember()
		self.wndGuild.DeleteGuild()

	def RefreshMobile(self):
		self.dlgSystem.RefreshMobile()

	def OnMobileAuthority(self):
		self.dlgSystem.OnMobileAuthority()

	def OnBlockMode(self, mode):
		self.dlgSystem.OnBlockMode(mode)

	def OpenPointResetDialog(self):
		self.dlgPointReset.Show()
		self.dlgPointReset.SetTop()

	def ClosePointResetDialog(self):
		self.dlgPointReset.Close()

	def OpenShopDialog(self, vid):
		self.wndInventory.Show()
		self.wndInventory.SetTop()
		self.dlgShop.Open(vid)
		self.dlgShop.SetTop()

	def CloseShopDialog(self):
		self.dlgShop.Close()

	def RefreshShopDialog(self):
		self.dlgShop.Refresh()

	if app.ENABLE_OFFLINE_SHOP_SYSTEM:
		def OpenOfflineShopDialog(self, vid):
			self.wndInventory.Show()
			self.wndInventory.SetTop()
			self.dlgOfflineShop.Open(vid)
			self.dlgOfflineShop.SetTop()

			if self.wndOfflineShopAdminPanel:
				if self.wndOfflineShopAdminPanel.wndOfflineShopAddItem:
					self.wndOfflineShopAdminPanel.wndOfflineShopAddItem.Close()

				if self.wndOfflineShopAdminPanel.wndOfflineShopRemoveItem:
					self.wndOfflineShopAdminPanel.wndOfflineShopRemoveItem.Close()

		def CloseOfflineShopDialog(self):
			self.dlgOfflineShop.Close()

		def RefreshOfflineShopDialog(self):
			self.dlgOfflineShop.Refresh()

		def ToggleOfflineShopLogWindow(self):
			self.wndOfflineShopLogPanel.Open()

		def OpenOfflineShopInputNameDialog(self):
			inputDialog = uiOfflineShop.OfflineShopInputDialog()
			inputDialog.SetAcceptEvent(ui.__mem_func__(self.OpenOfflineShopBuilder))
			inputDialog.SetCancelEvent(ui.__mem_func__(self.CloseOfflineShopInputNameDialog))
			inputDialog.Open()
			self.inputDialog = inputDialog

		def CloseOfflineShopInputNameDialog(self):
			self.inputDialog = None
			return True

		def OpenOfflineShopBuilder(self):
			self.offlineShopBuilder.Open(player.GetName())
			self.CloseOfflineShopInputNameDialog()
			return True

		def AppearOfflineShop(self, vid, text):
			board = uiOfflineShopBuilder.OfflineShopAdvertisementBoard()
			board.Open(vid, text)

			self.offlineShopAdvertisementBoardDict[vid] = board

		def DisappearOfflineShop(self, vid):
			if (vid not in self.offlineShopAdvertisementBoardDict):
				return

			del self.offlineShopAdvertisementBoardDict[vid]
			uiOfflineShopBuilder.DeleteADBoard(vid)

	if app.ENABLE_VS_SHOP_SEARCH:
		def ToggleOfflineShopSearch(self):
			if self.wndOfflineShopSearch.IsShow():
				self.wndOfflineShopSearch.Close()
			else:
				self.wndOfflineShopSearch.Open()
				self.wndOfflineShopSearch.SetTop()

	def OpenCharacterWindowQuestPage(self):
		self.wndCharacter.Show()
		self.wndCharacter.SetState("QUEST")

	def OpenQuestWindow(self, skin, idx):

		wnds = ()

		q = uiQuest.QuestDialog(skin, idx)
		q.SetWindowName("QuestWindow" + str(idx))
		q.Show()
		if skin:
			q.Lock()
			wnds = self.__HideWindows()

			q.AddOnDoneEvent(lambda tmp_self, args=wnds: self.__ShowWindows(args))

		if skin:
			q.AddOnCloseEvent(q.Unlock)
		q.AddOnCloseEvent(lambda key = self.wndQuestWindowNewKey:ui.__mem_func__(self.RemoveQuestDialog)(key))
		self.wndQuestWindow[self.wndQuestWindowNewKey] = q

		self.wndQuestWindowNewKey = self.wndQuestWindowNewKey + 1


	def RemoveQuestDialog(self, key):
		del self.wndQuestWindow[key]

	def StartExchange(self):
		self.dlgExchange.OpenDialog()
		self.dlgExchange.Refresh()

	def EndExchange(self):
		self.dlgExchange.CloseDialog()

	def RefreshExchange(self):
		self.dlgExchange.Refresh()

	if app.WJ_ENABLE_TRADABLE_ICON:
		def CantTradableItemExchange(self, dstSlotIndex, srcSlotIndex):
			self.dlgExchange.CantTradableItem(dstSlotIndex, srcSlotIndex)

	def AddPartyMember(self, pid, name):
		self.wndParty.AddPartyMember(pid, name)

		self.__ArrangeQuestButton()

	def UpdatePartyMemberInfo(self, pid):
		self.wndParty.UpdatePartyMemberInfo(pid)

	def RemovePartyMember(self, pid):
		self.wndParty.RemovePartyMember(pid)

		self.__ArrangeQuestButton()

	def LinkPartyMember(self, pid, vid):
		self.wndParty.LinkPartyMember(pid, vid)

	def UnlinkPartyMember(self, pid):
		self.wndParty.UnlinkPartyMember(pid)

	def UnlinkAllPartyMember(self):
		self.wndParty.UnlinkAllPartyMember()

	def ExitParty(self):
		self.wndParty.ExitParty()

		self.__ArrangeQuestButton()

	def PartyHealReady(self):
		self.wndParty.PartyHealReady()

	def ChangePartyParameter(self, distributionMode):
		self.wndParty.ChangePartyParameter(distributionMode)

	def AskSafeboxPassword(self):
		if self.wndSafebox.IsShow():
			return

		self.dlgPassword.SetTitle(localeInfo.PASSWORD_TITLE)
		self.dlgPassword.SetSendMessage("/safebox_password ")

		self.dlgPassword.ShowDialog()

	def OpenSafeboxWindow(self, size):
		self.dlgPassword.CloseDialog()
		self.wndSafebox.ShowWindow(size)

	def RefreshSafeboxMoney(self):
		self.wndSafebox.RefreshSafeboxMoney()

	def CommandCloseSafebox(self):
		self.wndSafebox.CommandCloseSafebox()

	def AskMallPassword(self):
		if self.wndMall.IsShow():
			return
		self.dlgPassword.SetTitle(localeInfo.MALL_PASSWORD_TITLE)
		self.dlgPassword.SetSendMessage("/mall_password ")
		self.dlgPassword.ShowDialog()

	def OpenMallWindow(self, size):
		self.dlgPassword.CloseDialog()
		self.wndMall.ShowWindow(size)

	def CommandCloseMall(self):
		self.wndMall.CommandCloseMall()

	def OnStartGuildWar(self, guildSelf, guildOpp):
		self.wndGuild.OnStartGuildWar(guildSelf, guildOpp)

		guildWarScoreBoard = uiGuild.GuildWarScoreBoard()
		guildWarScoreBoard.Open(guildSelf, guildOpp)
		guildWarScoreBoard.Show()
		self.guildScoreBoardDict[uiGuild.GetGVGKey(guildSelf, guildOpp)] = guildWarScoreBoard

	def OnEndGuildWar(self, guildSelf, guildOpp):
		self.wndGuild.OnEndGuildWar(guildSelf, guildOpp)

		key = uiGuild.GetGVGKey(guildSelf, guildOpp)

		if key not in self.guildScoreBoardDict:
			return

		self.guildScoreBoardDict[key].Destroy()
		del self.guildScoreBoardDict[key]

	def UpdateMemberCount(self, gulidID1, memberCount1, guildID2, memberCount2):
		key = uiGuild.GetGVGKey(gulidID1, guildID2)

		if key not in self.guildScoreBoardDict:
			return

		self.guildScoreBoardDict[key].UpdateMemberCount(gulidID1, memberCount1, guildID2, memberCount2)

	def OnRecvGuildWarPoint(self, gainGuildID, opponentGuildID, point):
		key = uiGuild.GetGVGKey(gainGuildID, opponentGuildID)
		if key not in self.guildScoreBoardDict:
			return

		guildBoard = self.guildScoreBoardDict[key]
		guildBoard.SetScore(gainGuildID, opponentGuildID, point)

	def OnChangePKMode(self):
		self.wndCharacter.RefreshAlignment()
		self.dlgSystem.OnChangePKMode()

	def OpenRefineDialog(self, targetItemPos, nextGradeItemVnum, cost, cost2, cost3, prob, type, probExtra):
		self.dlgRefineNew.Open(targetItemPos, nextGradeItemVnum, cost, cost2, cost3, prob, type, probExtra)

	def AppendMaterialToRefineDialog(self, vnum, count):
		self.dlgRefineNew.AppendMaterial(vnum, count)

	def AppendMaterialSourceToRefineDialog(self, materialVnum, sourceType, sourceVnum):
		self.dlgRefineNew.AppendMaterialSource(materialVnum, sourceType, sourceVnum)

	def ShowDefaultWindows(self):
		self.wndTaskBar.Show()
		if constInfo.ENABLE_EXPANDED_MONEY_TASKBAR:
			if self.wndExpandedMoneyTaskBar:
				self.wndExpandedMoneyTaskBar.Show()
		self.wndMiniMap.Show()
		self.wndMiniMap.ShowMiniMap()
		if self.wndEnergyBar:
			self.wndEnergyBar.Show()
		if settings.remember_save_window == True:
			self.wndLocationWindow.Show()
		if settings.remember_boss_tp_window == True:
			self.wndResp.Show()

	def ShowAllWindows(self):
		self.wndTaskBar.Show()
		self.wndCharacter.Show()
		self.wndInventory.Show()
		if app.ENABLE_DRAGON_SOUL_SYSTEM:
			self.wndDragonSoul.Show()
			self.wndDragonSoulRefine.Show()
		self.wndChat.Show()
		self.yangText.Show()
		self.wndMiniMap.Show()
		if self.wndEnergyBar:
			self.wndEnergyBar.Show()
		if self.wndWonExchange:
			self.wndWonExchange.Show()
		if self.wndExpandedTaskBar:
			self.wndExpandedTaskBar.Show()
			self.wndExpandedTaskBar.SetTop()
		if constInfo.ENABLE_EXPANDED_MONEY_TASKBAR:
			if self.wndExpandedMoneyTaskBar:
				self.wndExpandedMoneyTaskBar.Show()
				self.wndExpandedMoneyTaskBar.SetTop()

	def HideAllWindows(self):
		if self.wndTaskBar:
			self.wndTaskBar.Hide()

		if self.wndEnergyBar:
			self.wndEnergyBar.Hide()

		if self.wndCharacter:
			self.wndCharacter.Hide()

		if self.wndWonExchange:
			self.wndWonExchange.Hide()
			
		if app.ENABLE_MOUNT_SYSTEM:
			if self.wndMountWindow:
				self.wndMountWindow.Hide()
				
		if self.wndRankingWindow:
			self.wndRankingWindow.Hide()
		
		if self.wndRankingWindowWeekly:
			self.wndRankingWindowWeekly.Hide()

		if app.ENABLE_SECONDARY_LEVEL:
			if self.wndSecondaryLevel:
				self.wndSecondaryLevel.Hide()

		if app.ENABLE_ARTEFAKT_SYSTEM:
			if self.wndArtifact:
				self.wndArtifact.Hide()

		if self.wndInventory:
			self.wndInventory.Hide()

		if constInfo.ENABLE_EXPANDED_MONEY_TASKBAR:
			if self.wndExpandedMoneyTaskBar:
				self.wndExpandedMoneyTaskBar.Hide()

		if app.WJ_SPLIT_INVENTORY_SYSTEM:
			if self.wndExtendedInventory:
				self.wndExtendedInventory.Hide()

		if app.ENABLE_DRAGON_SOUL_SYSTEM:
			self.wndDragonSoul.Hide()
			self.wndDragonSoulRefine.Hide()
		
		if self.wndChat:
			self.wndChat.Hide()

		if app.ENABLE_SAVE_LOCATION_SYSTEM and self.wndSaveLocation:
			self.wndSaveLocation.Hide()

		if self.yangText:
			self.yangText.Hide()

		if self.wndMiniMap:
			self.wndMiniMap.Hide()

		if self.wndMessenger:
			self.wndMessenger.Hide()
			
		if app.ENABLE_MINIMAP_DUNGEONINFO:
			if self.wndMiniMapDungeonInfo:
				self.wndMiniMapDungeonInfo.Hide()

		if self.wndGuild:
			self.wndGuild.Hide()

		if app.__ENABLE_POLYMORPH_SYSTEM__:
			self.wndPolySystem.Hide()

		if self.wndExpandedTaskBar:
			self.wndExpandedTaskBar.Hide()
			
		if app.__BL_CHEST_DROP_INFO__:
			if self.wndChestDropInfo:
				self.wndChestDropInfo.Hide()
			
		if app.ENABLE_DUNGEON_INFO_SYSTEM:
			if self.wndDungeonInfo:
				self.wndDungeonInfo.Hide()
	
		if self.wndRemoveItem:
			self.wndRemoveItem.Hide()

		if app.ENABLE_RESP_SYSTEM:
			if self.wndResp:
				self.wndResp.Hide()
		
		if self.wndCasketPreview:
			self.wndCasketPreview.Hide()

		if app.ENABLE_SWITCHBOT:
			if self.wndSwitchbot:
				self.wndSwitchbot.Hide()

		if self.wndBonus:
			self.wndBonus.Hide()

		if self.wndCollectWindow:
			self.wndCollectWindow.Hide()

		if self.wndWeeklyRankWindow_New:
			self.wndWeeklyRankWindow_New.Hide()

		if app.TAKE_LEGEND_DAMAGE_BOARD_SYSTEM:
			if self.wndLegendDamageWindow:
				self.wndLegendDamageWindow.Close()

		if self.wndBoosters:
			self.wndBoosters.Hide()

		if app.ENABLE_ASLAN_BUFF_NPC_SYSTEM:
			if self.wndBuffNPCWindow:
				self.wndBuffNPCWindow.Hide()
			if self.wndBuffNPCCreateWindow:
				self.wndBuffNPCCreateWindow.Hide()

		if app.ENABLE_VS_SHOP_SEARCH:
			if self.wndOfflineShopSearch:
				self.wndOfflineShopSearch.Hide()

		if hasattr(app, "ENABLE_PREMIUM_PRIVATE_SHOP_OFFICIAL") and app.ENABLE_PREMIUM_PRIVATE_SHOP_OFFICIAL:
			self.wndPrivateShopPanel.Hide()
			self.wndPrivateShopSearch.Hide()

		for window in self.interfaceWindowList.values():
			window.Close()

	def IsShowDlgQuestionWindow(self):
		if self.wndDragonSoul.IsDlgQuestionShow():
			return True
		elif self.dlgShop.IsDlgQuestionShow():
			return True
		elif self.wndWonExchange.IsDlgQuestionShow():
			return True
		else:
			return False

	def CloseDlgQuestionWindow(self):
		if self.wndDragonSoul.IsDlgQuestionShow():
			self.wndDragonSoul.ExternQuestionDialog_Close()
		if self.dlgShop.IsDlgQuestionShow():
			self.dlgShop.ExternQuestionDialog_Close()
		if self.wndWonExchange.IsDlgQuestionShow():
			self.wndWonExchange.ExternQuestionDialog_Close()

	def ShowMouseImage(self):
		self.wndTaskBar.ShowMouseImage()

	def HideMouseImage(self):
		self.wndTaskBar.HideMouseImage()

	def ToggleChat(self):
		if True == self.wndChat.IsEditMode():
			self.wndChat.CloseChat()
		else:
			if self.wndWeb and self.wndWeb.IsShow():
				pass
			else:
				self.wndChat.OpenChat()

	def IsOpenChat(self):
		return self.wndChat.IsEditMode()

	def SetChatFocus(self):
		self.wndChat.SetChatFocus()

	if app.RENEWAL_DEAD_PACKET:
		def OpenRestartDialog(self, d_time):
			self.dlgRestart.OpenDialog(d_time)
			self.dlgRestart.SetTop()
	else:
		def OpenRestartDialog(self):
			self.dlgRestart.OpenDialog()
			self.dlgRestart.SetTop()

	def CloseRestartDialog(self):
		self.dlgRestart.Close()

	def ToggleSystemDialog(self):
		if False == self.dlgSystem.IsShow():
			self.dlgSystem.OpenDialog()
			self.dlgSystem.SetTop()
		else:
			self.dlgSystem.Close()

	def OpenSystemDialog(self):
		self.dlgSystem.OpenDialog()
		self.dlgSystem.SetTop()

	def ToggleMessenger(self):
		if self.wndMessenger.IsShow():
			self.wndMessenger.Hide()
		else:
			self.wndMessenger.SetTop()
			self.wndMessenger.Show()

	if app.ENABLE_MINIMAP_DUNGEONINFO:
		def SetMiniMapDungeonInfo(self, state):
			import dbg
			if state == 1:
				self.wndMiniMap.HideMiniMap()
				self.wndMiniMap.Hide()
				self.wndMiniMapDungeonInfo.Show()
			else:
				self.wndMiniMap.Show()
				self.wndMiniMap.ShowMiniMap()
				self.wndMiniMapDungeonInfo.Hide()
	
		def SetMiniMapDungeonInfoStage(self, cur_stage, max_stage):
			self.wndMiniMapDungeonInfo.SetStage(cur_stage, max_stage)
		
		def SetMiniMapDungeonInfoGauge(self, gauge_type, value1, value2):
			self.wndMiniMapDungeonInfo.SetGauge(gauge_type, value1, value2)
		
		def SetMiniMapDungeonInfoNotice(self, notice):
			self.wndMiniMapDungeonInfo.SetNotice(notice)

		def SetMiniMapDungeonInfoButton(self, status):
			self.wndMiniMapDungeonInfo.SetButton(status)

		def SetMiniMapDungeonInfoTimer(self, status, time):
			self.wndMiniMapDungeonInfo.SetTimer(status, time)

	def ToggleMiniMap(self):
		if app.IsPressed(app.DIK_LSHIFT) or app.IsPressed(app.DIK_RSHIFT):
			if False == self.wndMiniMap.isShowMiniMap():
				self.wndMiniMap.ShowMiniMap()
				self.wndMiniMap.SetTop()
			else:
				self.wndMiniMap.HideMiniMap()

		else:
			self.wndMiniMap.ToggleAtlasWindow()

	def PressMKey(self):
		if app.IsPressed(app.DIK_LALT) or app.IsPressed(app.DIK_RALT):
			self.ToggleMessenger()

		else:
			self.ToggleMiniMap()

	def SetMapName(self, mapName):
		self.wndMiniMap.SetMapName(mapName)

	def MiniMapScaleUp(self):
		self.wndMiniMap.ScaleUp()

	def MiniMapScaleDown(self):
		self.wndMiniMap.ScaleDown()

	def ToggleCharacterWindow(self, state):
		if False == player.IsObserverMode():
			if False == self.wndCharacter.IsShow():
				self.OpenCharacterWindowWithState(state)
			else:
				if state == self.wndCharacter.GetState():
					self.wndCharacter.OverOutItem()
					self.wndCharacter.Hide()
				else:
					self.wndCharacter.SetState(state)

	def OpenCharacterWindowWithState(self, state):
		if False == player.IsObserverMode():
			self.wndCharacter.SetState(state)
			self.wndCharacter.Show()
			self.wndCharacter.SetTop()

	def ToggleCharacterWindowStatusPage(self):
		self.ToggleCharacterWindow("STATUS")

	def ToggleInventoryWindow(self):
		if False == player.IsObserverMode():
			if False == self.wndInventory.IsShow():
				self.wndInventory.Show()
				self.wndInventory.SetTop()
				if 1 == settings.inventory_auto_open:
					if not self.wndExtendedInventory.IsShow():
						self.wndExtendedInventory.Show()
			else:
				self.wndInventory.OverOutItem()
				self.wndInventory.Close()
				if 1 == settings.inventory_auto_open:
					if self.wndExtendedInventory.IsShow():
						self.wndExtendedInventory.Close()





	if app.ENABLE_ODLAMKI_SYSTEM:
		def OpenFragmentsWindow(self):
			if self.wndFragments.IsShow():
				self.wndFragments.Hide()
			else:
				self.wndFragments.Open()


	if app.ENABLE_ASLAN_BUFF_NPC_SYSTEM:
		def BuffNPC_OpenCreateWindow(self):
			if self.wndBuffNPCWindow:
				if False == self.wndBuffNPCCreateWindow.IsShow():
					self.wndBuffNPCCreateWindow.Show()
					self.wndBuffNPCCreateWindow.SetTop()
				
		def BuffNPCOpenWindow(self):
			if self.wndBuffNPCWindow:
				if False == self.wndBuffNPCWindow.IsShow():
					self.wndBuffNPCWindow.Show()
					self.wndBuffNPCWindow.SetTop()
				else:
					self.wndBuffNPCWindow.Close()
				
		def BuffNPC_Summon(self):
			if self.wndBuffNPCWindow:
				self.wndBuffNPCWindow.SetSummon()
				
		def BuffNPC_Unsummon(self):
			if self.wndBuffNPCWindow:
				self.wndBuffNPCWindow.SetUnsummon()
				
		def BuffNPC_Clear(self):
			if self.wndBuffNPCWindow:
				self.wndBuffNPCWindow.SetClear()
				
		def BuffNPC_SetBasicInfo(self, name, sex, intvalue):
			if self.wndBuffNPCWindow:
				self.wndBuffNPCWindow.SetBasicInfo(name, sex, intvalue)
				
		def BuffNPC_SetSkillInfo(self, skill1, skill2, skill3):
			if self.wndBuffNPCWindow:
				self.wndBuffNPCWindow.SetSkillInfo(skill1, skill2, skill3)
				
		def BuffNPC_SetSkillCooltime(self, slot, timevalue):
			if self.wndBuffNPCWindow:
				self.wndBuffNPCWindow.SetSkillCooltime(slot, timevalue)
		
		def BuffNPC_CreatePopup(self, type, value0, value1):
			if self.wndBuffNPCWindow:
				self.wndBuffNPCWindow.CreatePopup(type, value0, value1)

	if app.WJ_SPLIT_INVENTORY_SYSTEM:
		def ToggleExtendedInventoryWindow(self):
			if FALSE == player.IsObserverMode():
				if self.wndExtendedInventory.IsShow():
					self.wndExtendedInventory.OverOutItem()
					self.wndExtendedInventory.Close()
				else:
					self.wndExtendedInventory.Show()

	def ToggleExpandedButton(self):
		if False == player.IsObserverMode():
			if False == self.wndExpandedTaskBar.IsShow():
				self.wndExpandedTaskBar.Show()
				self.wndExpandedTaskBar.SetTop()
			else:
				self.wndExpandedTaskBar.Close()

	if constInfo.ENABLE_EXPANDED_MONEY_TASKBAR:
		def ToggleExpandedMoneyButton(self):
			if False == self.wndExpandedMoneyTaskBar.IsShow():
				self.wndExpandedMoneyTaskBar.Show()
				self.wndExpandedMoneyTaskBar.SetTop()
			else:
				self.wndExpandedMoneyTaskBar.Close()

	def DragonSoulActivate(self, deck):
		if app.ENABLE_DRAGON_SOUL_SYSTEM:
			self.wndDragonSoul.ActivateDragonSoulByExtern(deck)

	def DragonSoulDeactivate(self):
		if app.ENABLE_DRAGON_SOUL_SYSTEM:
			self.wndDragonSoul.DeactivateDragonSoul()

	def Highligt_Item(self, inven_type, inven_pos):
		if player.DRAGON_SOUL_INVENTORY == inven_type:
			if app.ENABLE_DRAGON_SOUL_SYSTEM:
				self.wndDragonSoul.HighlightSlot(inven_pos)

		elif app.ENABLE_HIGHLIGHT_NEW_ITEM and player.SLOT_TYPE_INVENTORY == inven_type:
			self.wndInventory.HighlightSlot(inven_pos)
			self.wndExtendedInventory.HighlightSlot(inven_pos)

	def DragonSoulGiveQuilification(self):
		self.DRAGON_SOUL_IS_QUALIFIED = True
		if (self.wndExpandedTaskBar):
			self.wndExpandedTaskBar.SetToolTipText(uiTaskBar.ExpandedTaskBar.BUTTON_DRAGON_SOUL, uiScriptLocale.TASKBAR_DRAGON_SOUL)

	def ToggleDragonSoulWindow(self):
		if False == player.IsObserverMode():
			if app.ENABLE_DRAGON_SOUL_SYSTEM:
				if False == self.wndDragonSoul.IsShow():
					self.wndDragonSoul.Show()
				else:
					self.wndDragonSoul.Close()

	def FailDragonSoulRefine(self, reason, inven_type, inven_pos):
		if False == player.IsObserverMode():
			if app.ENABLE_DRAGON_SOUL_SYSTEM:
				if True == self.wndDragonSoulRefine.IsShow():
					self.wndDragonSoulRefine.RefineFail(reason, inven_type, inven_pos)

	def SucceedDragonSoulRefine(self, inven_type, inven_pos):
		if False == player.IsObserverMode():
			if app.ENABLE_DRAGON_SOUL_SYSTEM:
				if True == self.wndDragonSoulRefine.IsShow():
					self.wndDragonSoulRefine.RefineSucceed(inven_type, inven_pos)

	if app.ENABLE_DS_CHANGE_ATTR:
		def OpenDragonSoulRefineWindow(self, type):
			if False == player.IsObserverMode():
				if app.ENABLE_DRAGON_SOUL_SYSTEM:
					if False == self.wndDragonSoulRefine.IsShow():
						self.wndDragonSoulRefine.SetWindowType(type)
						self.wndDragonSoulRefine.Show()
						if None != self.wndDragonSoul:
							if False == self.wndDragonSoul.IsShow():
								self.wndDragonSoul.Show()
	else:
		def OpenDragonSoulRefineWindow(self):
			if False == player.IsObserverMode():
				if app.ENABLE_DRAGON_SOUL_SYSTEM:
					if False == self.wndDragonSoulRefine.IsShow():
						self.wndDragonSoulRefine.Show()
						if None != self.wndDragonSoul:
							if False == self.wndDragonSoul.IsShow():
								self.wndDragonSoul.Show()

	def CloseDragonSoulRefineWindow(self):
		if False == player.IsObserverMode():
			if app.ENABLE_DRAGON_SOUL_SYSTEM:
				if True == self.wndDragonSoulRefine.IsShow():
					self.wndDragonSoulRefine.Close()


	def ToggleGuildWindow(self):
		if not self.wndGuild.IsShow():
			if self.wndGuild.CanOpen():
				self.wndGuild.Open()
			else:
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.GUILD_YOU_DO_NOT_JOIN)
		else:
			self.wndGuild.OverOutItem()
			self.wndGuild.Hide()

	def ToggleChatLogWindow(self):
		if self.wndChatLog.IsShow():
			self.wndChatLog.Hide()
		else:
			self.wndChatLog.Show()

	if app.ENABLE_AUTO_SHOUT:
		def AutoShoutButton(self):
			if constInfo.AUTO_SHOUT_ACTIVATED:
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.AUTO_SHOUT_INFO2)
				constInfo.AUTO_SHOUT_ACTIVATED = 0
			else:
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.AUTO_SHOUT_INFO)
				constInfo.AUTO_SHOUT_ACTIVATED = 1
				if constInfo.LAST_SHOUT_MESSAGE == "":
					chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.AUTO_SHOUT_INFO3)

	def ToggleMarmurShopWindow(self):
		if self.wndPolySystem.IsShow():
			self.wndPolySystem.Close()
		else:
			net.SendPolyOpen()

	def ToggleBonusWindow(self):
		if self.wndBonus.IsShow():
			self.wndBonus.Close()
		else:
			self.wndBonus.Open()

	def OpenBlendWindow(self):
		if self.wndBoosters.IsShow():
			self.wndBoosters.Close()
		else:
			self.wndBoosters.Open()

	def ToggleCollectWindow(self):
		if self.wndCollectWindow.IsShow():
			self.wndCollectWindow.Close()
		else:
			self.wndCollectWindow.Open()

	def ToggleWeeklyRankWindow(self):
		if self.wndWeeklyRankWindow_New.IsShow():
			self.wndWeeklyRankWindow_New.Close()
		else:
			self.wndWeeklyRankWindow_New.Open()

	if app.ENABLE_SWITCHBOT:
		def ToggleSwitchbotWindow(self):
			if self.wndSwitchbot.IsShow():
				self.wndSwitchbot.Close()
			else:
				self.wndSwitchbot.Open()
				
		def RefreshSwitchbotWindow(self):
			if self.wndSwitchbot:
				self.wndSwitchbot.RefreshSwitchbotWindow()

		def RefreshSwitchbotItem(self, slot):
			if self.wndSwitchbot:
				self.wndSwitchbot.RefreshSwitchbotItem(slot)

	def OpenRemoveItem(self, inventory):
		if self.wndRemoveItem.IsShow():
			self.wndRemoveItem.Hide()
		else:
			self.wndRemoveItem.OpenWindow(inventory)

	def CheckGameButton(self):
		if self.wndGameButton:
			self.wndGameButton.CheckGameButton()

	def __OnClickStatusPlusButton(self):
		self.ToggleCharacterWindow("STATUS")


	def __OnClickQuestButton(self):
		self.ToggleCharacterWindow("QUEST")

	if app.ENABLE_KEYCHANGE_SYSTEM:
		def ToggleHelpWindow(self):
			if self.wndHelp.IsShow():
				self.CloseHelpWindow()
			else:
				self.OpenHelpWindow()


	def __OnClickBuildButton(self):
		self.BUILD_OpenWindow()

	def OpenHelpWindow(self):
		self.wndUICurtain.Show()
		self.wndHelp.Open()

	def CloseHelpWindow(self):
		self.wndUICurtain.Hide()
		self.wndHelp.Close()

	def OpenWebWindow(self, url):
		self.wndWeb.Open(url)

		self.wndChat.CloseChat()

	if constInfo.GIFT_CODE_SYSTEM:
		def OpenGiftCodeWindow(self):
			if self.wndGiftCodeWindow.IsShow():
				self.wndGiftCodeWindow.Hide()
			else:
				self.wndGiftCodeWindow.Show()

	def ShowGift(self):
		self.wndTaskBar.ShowGift()

	def CloseWbWindow(self):
		self.wndWeb.Close()
		
	def OpenCardsInfoWindow(self):
		self.wndCardsInfo.Open()
		
	def OpenCardsWindow(self, safemode):
		self.wndCards.Open(safemode)
		
	def UpdateCardsInfo(self, hand_1, hand_1_v, hand_2, hand_2_v, hand_3, hand_3_v, hand_4, hand_4_v, hand_5, hand_5_v, cards_left, points):
		self.wndCards.UpdateCardsInfo(hand_1, hand_1_v, hand_2, hand_2_v, hand_3, hand_3_v, hand_4, hand_4_v, hand_5, hand_5_v, cards_left, points)
		
	def UpdateCardsFieldInfo(self, hand_1, hand_1_v, hand_2, hand_2_v, hand_3, hand_3_v, points):
		self.wndCards.UpdateCardsFieldInfo(hand_1, hand_1_v, hand_2, hand_2_v, hand_3, hand_3_v, points)
		
	def CardsPutReward(self, hand_1, hand_1_v, hand_2, hand_2_v, hand_3, hand_3_v, points):
		self.wndCards.CardsPutReward(hand_1, hand_1_v, hand_2, hand_2_v, hand_3, hand_3_v, points)
		
	def CardsShowIcon(self):
		self.wndCardsIcon.Show()

	def OpenCubeWindow(self):
		self.wndCube.Open()

		if False == self.wndInventory.IsShow():
			self.wndInventory.Show()

	def CloseCubeWindow(self):
		self.wndCube.Close()
	
	def GetCubeWindow(self):
		return self.wndCube

	if app.ENABLE_ACCE_COSTUME_SYSTEM:
		def ActAcce(self, iAct, bWindow):
			board = (self.wndAcceAbsorption,self.wndAcceCombine)[int(bWindow)]
			if iAct == 1:
				self.ActAcceOpen(board)
			elif iAct == 2:
				self.ActAcceClose(board)
			elif iAct == 3 or iAct == 4:
				self.ActAcceRefresh(board, iAct)

		def ActAcceOpen(self,board):
			if not board.IsOpened():
				board.Open()
			if not self.wndInventory.IsShow():
				self.wndInventory.Show()
			self.wndInventory.RefreshBagSlotWindow()

		def ActAcceClose(self,board):
			if board.IsOpened():
				board.Close()
			self.wndInventory.RefreshBagSlotWindow()

		def ActAcceRefresh(self,board,iAct):
			if board.IsOpened():
				board.Refresh(iAct)
			self.wndInventory.RefreshBagSlotWindow()

	if app.ENABLE_AURA_SYSTEM:
		def ActAura(self, iAct, bWindow):
			if iAct == 1:
				if bWindow == True:
					if not self.wndAuraRefine.IsOpened():
						self.wndAuraRefine.Open()
				else:
					if not self.wndAuraAbsorption.IsOpened():
						self.wndAuraAbsorption.Open()
				
				self.wndInventory.RefreshBagSlotWindow()
			elif iAct == 2:
				if bWindow == True:
					if self.wndAuraRefine.IsOpened():
						self.wndAuraRefine.Close()
				else:
					if self.wndAuraAbsorption.IsOpened():
						self.wndAuraAbsorption.Close()
				
				self.wndInventory.RefreshBagSlotWindow()
			elif iAct == 3 or iAct == 4:
				if bWindow == True:
					if self.wndAuraRefine.IsOpened():
						self.wndAuraRefine.Refresh(iAct)
				else:
					if self.wndAuraAbsorption.IsOpened():
						self.wndAuraAbsorption.Refresh(iAct)
				
				self.wndInventory.RefreshBagSlotWindow()

	if app.ENABLE_RESP_SYSTEM:
		def OpenRespWindow(self):
			if self.wndResp.IsShow():
				self.wndResp.Hide()
			else:
				self.wndResp.Show()

		def ClearLocationWindow(self):
			self.wndLocationWindow.ClearData()

		def UpdateLocationWindowPos(self, position, index, posx, posy):
			self.wndLocationWindow.AppendPosition(position, index, posx, posy)

		def UpdateLocationWindowName(self, name):
			self.wndLocationWindow.AppendName(name)

	if app.ENABLE_DUNGEON_INFO_SYSTEM:
		def ToggleDungeonInfoWindow(self):
			if False == player.IsObserverMode():
				if False == self.wndDungeonInfo.IsShow():
					self.wndDungeonInfo.Open()
				else:
					self.wndDungeonInfo.Close()

		def DungeonInfoOpen(self):
			try:
				import uidungeontrack
				uidungeontrack.SyncDungeonDataFromServer()
			except:
				pass

		def DungeonRankingRefresh(self):
			if self.wndDungeonInfo:
				self.wndDungeonInfo.OnRefreshRanking()
			try:
				import uidungeontrack
				uidungeontrack.OnRankingRefresh()
			except:
				pass

		def DungeonInfoReload(self, onReset):
			if self.wndDungeonInfo:
				self.wndDungeonInfo.OnReload(onReset)
			try:
				import uidungeontrack
				uidungeontrack.SyncDungeonDataFromServer()
			except:
				pass

	def __HideWindows(self):
		hideWindows = self.wndTaskBar,\
						self.wndCharacter,\
						self.wndInventory,\
						self.wndMiniMap,\
						self.wndGuild,\
						self.wndMessenger,\
						self.yangText,\
						self.wndChat,\
						self.wndParty,\
						self.wndGameButton,

		if self.wndWonExchange:
			hideWindows += self.wndWonExchange,
			
		if self.wndRankingWindow:
			hideWindows += self.wndRankingWindow,
			
		if self.wndRankingWindowWeekly:
			hideWindows += self.wndRankingWindowWeekly,

		if app.ENABLE_SECONDARY_LEVEL:
			hideWindows += self.wndSecondaryLevel,

		if self.wndEnergyBar:
			hideWindows += self.wndEnergyBar,
		
		if self.wndCasketPreview:
			hideWindows += self.wndCasketPreview,

		if self.wndExpandedTaskBar:
			hideWindows += self.wndExpandedTaskBar,

		if self.wndRemoveItem:
			hideWindows += self.wndRemoveItem,

		if app.ENABLE_ODLAMKI_SYSTEM:
			if self.wndFragments:
				hideWindows += self.wndFragments,

		if app.__ENABLE_POLYMORPH_SYSTEM__ and self.wndPolySystem:
			hideWindows += self.wndPolySystem,

		if app.WJ_SPLIT_INVENTORY_SYSTEM:
			if self.wndExtendedInventory:
				hideWindows += self.wndExtendedInventory,

		if app.ENABLE_RESP_SYSTEM and self.wndResp:
			hideWindows += self.wndResp,

		if app.ENABLE_DRAGON_SOUL_SYSTEM:
			hideWindows += self.wndDragonSoul,\
						self.wndDragonSoulRefine,

		for index, window in enumerate(self.interfaceWindowList):
			hideWindows += self.interfaceWindowList[window],
   
		if app.ENABLE_SWITCHBOT and self.wndSwitchbot:
			hideWindows += self.wndSwitchbot,

		if app.ENABLE_ASLAN_BUFF_NPC_SYSTEM:
			if self.wndBuffNPCWindow:
				hideWindows += self.wndBuffNPCWindow,
			if self.wndBuffNPCCreateWindow:
				hideWindows += self.wndBuffNPCCreateWindow,


		if app.ENABLE_DUNGEON_INFO_SYSTEM:
			if self.wndDungeonInfo:
				hideWindows += self.wndDungeonInfo,
				
		if app.ENABLE_MINIMAP_DUNGEONINFO:
			if self.wndMiniMapDungeonInfo:
				hideWindows += self.wndMiniMapDungeonInfo,

		if app.ENABLE_SAVE_LOCATION_SYSTEM:
			hideWindows += self.wndSaveLocation,

		if constInfo.ENABLE_EXPANDED_MONEY_TASKBAR:
			if self.wndExpandedMoneyTaskBar:
				hideWindows += self.wndExpandedMoneyTaskBar,
				
		if self.wndgameOption:
			hideWindows += self.wndgameOption,

		if app.TAKE_LEGEND_DAMAGE_BOARD_SYSTEM:
			if self.wndLegendDamageWindow:
				hideWindows += self.wndLegendDamageWindow,

		if app.ENABLE_OFFLINE_SHOP:
			if self.wndShopOffline:
				hideWindows += self.wndShopOffline,
			if self.wndShopSearch:
				hideWindows += self.wndShopSearch,
			if self.wndShopNotification:
				hideWindows += self.wndShopNotification,

		if app.ENABLE_VS_SHOP_SEARCH:
			if self.wndOfflineShopSearch:
				hideWindows += self.wndOfflineShopSearch,

		if hasattr(app, "ENABLE_PREMIUM_PRIVATE_SHOP_OFFICIAL") and app.ENABLE_PREMIUM_PRIVATE_SHOP_OFFICIAL:
			hideWindows += self.wndPrivateShopPanel,\
						self.wndPrivateShopSearch

		hideWindows = list(filter(lambda x:x.IsShow(), hideWindows))
		# map() w Py3 jest leniwy - bez konsumpcji okna nigdy sie nie chowaly
		for wnd in hideWindows:
			wnd.Hide()

		self.HideAllQuestButton()
		self.HideAllWhisperButton()

		if self.wndChat.IsEditMode():
			self.wndChat.CloseChat()

		return hideWindows

	def ToggleWonExchangeWindow(self):
		if player.IsObserverMode():
			return

		if False == self.wndWonExchange.IsShow():
			self.wndWonExchange.SetPage(uiWonExchange.WonExchangeWindow.PAGE_SELL)
			self.wndWonExchange.Show()
			self.wndWonExchange.SetTop()
		else:
			self.wndWonExchange.Hide()

	def __ShowWindows(self, wnds):
		# map() w Py3 jest leniwy - bez konsumpcji okna nigdy nie wracaly po zamknieciu questa
		for wnd in wnds:
			wnd.Show()
		global IsQBHide
		if not IsQBHide:
			self.ShowAllQuestButton()
		else:
			self.HideAllQuestButton()

		self.ShowAllWhisperButton()

	def BINARY_OpenAtlasWindow(self):
		if self.wndMiniMap:
			self.wndMiniMap.ShowAtlas()


	def BINARY_SetObserverMode(self, flag):
		self.wndGameButton.SetObserverMode(flag)

	if app.ENABLE_REFINE_RENEWAL:
		def CheckRefineDialog(self, isFail):
			self.dlgRefineNew.CheckRefine(isFail)

	def BINARY_OpenSelectItemWindow(self):
		self.wndItemSelect.Open()


	def OpenPrivateShopInputNameDialog(self):

		inputDialog = uiCommon.InputDialog()
		inputDialog.SetTitle(localeInfo.PRIVATE_SHOP_INPUT_NAME_DIALOG_TITLE)
		inputDialog.SetMaxLength(32)
		inputDialog.SetAcceptEvent(ui.__mem_func__(self.OpenPrivateShopBuilder))
		inputDialog.SetCancelEvent(ui.__mem_func__(self.ClosePrivateShopInputNameDialog))
		inputDialog.Open()
		self.inputDialog = inputDialog

	def ClosePrivateShopInputNameDialog(self):
		self.inputDialog = None
		return True

	def OpenPrivateShopBuilder(self):

		if not self.inputDialog:
			return True

		if not len(self.inputDialog.GetText()):
			return True

		self.privateShopBuilder.Open(self.inputDialog.GetText())
		self.ClosePrivateShopInputNameDialog()
		return True

	def AppearPrivateShop(self, vid, text):

		board = uiPrivateShopBuilder.PrivateShopAdvertisementBoard()
		board.Open(vid, text)

		self.privateShopAdvertisementBoardDict[vid] = board

	def DisappearPrivateShop(self, vid):

		if vid not in self.privateShopAdvertisementBoardDict:
			return

		del self.privateShopAdvertisementBoardDict[vid]
		uiPrivateShopBuilder.DeleteADBoard(vid)

	def UpdateBonusChanger(self):
		if self.wndChangerWindow:
			self.wndChangerWindow.OnUpdate()
	
	def AddToBonusChange(self, item1, item2):
		if self.wndChangerWindow:
			self.wndChangerWindow.AddItems(item1, item2)


	def OpenEquipmentDialog(self, vid):
		dlg = uiEquipmentDialog.EquipmentDialog()
		dlg.SetItemToolTip(self.tooltipItem)
		dlg.SetCloseEvent(ui.__mem_func__(self.CloseEquipmentDialog))
		dlg.Open(vid)

		self.equipmentDialogDict[vid] = dlg

	def SetEquipmentDialogItem(self, vid, slotIndex, vnum, count):
		if not vid in self.equipmentDialogDict:
			return
		self.equipmentDialogDict[vid].SetEquipmentDialogItem(slotIndex, vnum, count)

	def SetEquipmentDialogSocket(self, vid, slotIndex, socketIndex, value):
		if not vid in self.equipmentDialogDict:
			return
		self.equipmentDialogDict[vid].SetEquipmentDialogSocket(slotIndex, socketIndex, value)

	def SetEquipmentDialogAttr(self, vid, slotIndex, attrIndex, type, value):
		if not vid in self.equipmentDialogDict:
			return
		self.equipmentDialogDict[vid].SetEquipmentDialogAttr(slotIndex, attrIndex, type, value)

	def CloseEquipmentDialog(self, vid):
		if not vid in self.equipmentDialogDict:
			return
		del self.equipmentDialogDict[vid]


	def BINARY_ClearQuest(self, index):
		btn = self.__FindQuestButton(index)
		if 0 != btn:
			self.__DestroyQuestButton(btn)

	def RecvQuest(self, index, name):
		self.BINARY_RecvQuest(index, name, "file", localeInfo.GetLetterImageName())

	def BINARY_RecvQuest(self, index, name, iconType, iconName):

		btn = self.__FindQuestButton(index)
		if 0 != btn:
			self.__DestroyQuestButton(btn)

		btn = uiWhisper.WhisperButton()

		import item
		if "item"==iconType:
			# iconName przychodzi z pakietu questa - nie musi byc liczba.
			# int() rzucalo wtedy ValueError i przycisk questa w ogole nie powstawal.
			try:
				iconVnum = int(iconName)
			except (TypeError, ValueError):
				import dbg
				dbg.TraceError("BINARY_RecvQuest: nieprawidlowy vnum ikony '%s'" % (iconName,))
				iconVnum = 0
			item.SelectItem(iconVnum)
			buttonImageFileName=item.GetIconImageFileName()
		else:
			buttonImageFileName=iconName

		if iconName and (iconType not in ("item", "file")):
			btn.SetUpVisual("d:/ymir work/ui/game/quest/questicon/%s" % (iconName.replace("open", "close")))
			btn.SetOverVisual("d:/ymir work/ui/game/quest/questicon/%s" % (iconName))
			btn.SetDownVisual("d:/ymir work/ui/game/quest/questicon/%s" % (iconName))
		else:
			btn.SetUpVisual(localeInfo.GetLetterCloseImageName())
			btn.SetOverVisual(localeInfo.GetLetterOpenImageName())
			btn.SetDownVisual(localeInfo.GetLetterOpenImageName())

		listOfTypes = iconType.split(",")
		if "blink" in listOfTypes:
			btn.Flash()

		listOfColors = {
			"golden":	0xFFffa200,
			"green":	0xFF00e600,
			"blue":		0xFF0099ff,
			"purple":	0xFFcc33ff,

			"fucsia":	0xFFcc0099,
			"aqua":		0xFF00ffff,
		}
		for k,v in listOfColors.items():
			if k in listOfTypes:
				btn.ToolTipText.SetPackedFontColor(v)

		if not app.ENABLE_QUEST_RENEWAL:
			btn.SetToolTipText(name, -20, 55)
			btn.ToolTipText.SetHorizontalAlignLeft()

			btn.SetEvent(ui.__mem_func__(self.__StartQuest), btn)
			btn.Show()
		else:
			btn.SetEvent(ui.__mem_func__(self.__StartQuest), btn)
			
		btn.Show()

		btn.index = index
		btn.name = name

		self.questButtonList.insert(0, btn)
		self.__ArrangeQuestButton()

	def __ArrangeQuestButton(self):

		screenWidth = wndMgr.GetScreenWidth()
		screenHeight = wndMgr.GetScreenHeight()

		if self.wndParty.IsShow():
			xPos = 100 + 30
		else:
			xPos = 20

		yPos = 170 * screenHeight // 600
		yCount = (screenHeight - 330) // 63

		count = 0
		for btn in self.questButtonList:
		
			if app.ENABLE_QUEST_RENEWAL:
				btn.SetToolTipText(str(len(self.questButtonList)))
				btn.ToolTipText.SetPosition(13, 37)


			btn.SetPosition(xPos + (int(count//yCount) * 100), yPos + (count%yCount * 63))
			count += 1
			global IsQBHide
			if IsQBHide:
				btn.Hide()
			else:
				if app.ENABLE_QUEST_RENEWAL and count > 0:
					btn.Hide()
				else:
					btn.Show()

	def __StartQuest(self, btn):
		if app.ENABLE_QUEST_RENEWAL:
			self.__OnClickQuestButton()
			self.HideAllQuestButton()
		else:
			event.QuestButtonClick(btn.index)
			self.__DestroyQuestButton(btn)

	def __FindQuestButton(self, index):
		for btn in self.questButtonList:
			if btn.index == index:
				return btn

		return 0

	def __DestroyQuestButton(self, btn):
		btn.SetEvent(0)
		self.questButtonList.remove(btn)
		self.__ArrangeQuestButton()

	def HideAllQuestButton(self):
		for btn in self.questButtonList:
			btn.Hide()

	def ShowAllQuestButton(self):
		for btn in self.questButtonList:
			btn.Show()
			if app.ENABLE_QUEST_RENEWAL:
				break


	def __InitWhisper(self):
		chat.InitWhisper(self)

	def OpenWhisperDialogWithoutTarget(self):
		if not self.dlgWhisperWithoutTarget:
			dlgWhisper = uiWhisper.WhisperDialog(self.MinimizeWhisperDialog, self.CloseWhisperDialog)
			dlgWhisper.BindInterface(self)
			dlgWhisper.LoadDialog()
			dlgWhisper.OpenWithoutTarget(self.RegisterTemporaryWhisperDialog)
			dlgWhisper.SetPosition(self.windowOpenPosition*30,self.windowOpenPosition*30)
			dlgWhisper.Show()
			self.dlgWhisperWithoutTarget = dlgWhisper

			self.windowOpenPosition = (self.windowOpenPosition+1) % 5

		else:
			self.dlgWhisperWithoutTarget.SetTop()
			self.dlgWhisperWithoutTarget.OpenWithoutTarget(self.RegisterTemporaryWhisperDialog)

	def RegisterTemporaryWhisperDialog(self, name):
		if not self.dlgWhisperWithoutTarget:
			return

		btn = self.__FindWhisperButton(name)
		if 0 != btn:
			self.__DestroyWhisperButton(btn)

		elif name in self.whisperDialogDict:
			oldDialog = self.whisperDialogDict[name]
			oldDialog.Destroy()
			del self.whisperDialogDict[name]

		self.whisperDialogDict[name] = self.dlgWhisperWithoutTarget
		self.dlgWhisperWithoutTarget.OpenWithTarget(name)
		self.dlgWhisperWithoutTarget = None
		self.__CheckGameMaster(name)

	def OpenWhisperDialog(self, name):
		dlg = self.__MakeWhisperDialog(name)
		dlg.OpenWithTarget(name)
		dlg.chatLine.SetFocus()
		dlg.Show()

		self.__CheckGameMaster(name)
		btn = self.__FindWhisperButton(name)
		if 0 != btn:
			self.__DestroyWhisperButton(btn)

	def RecvWhisper(self, name):
		if name not in self.whisperDialogDict:
			btn = self.__FindWhisperButton(name)
			if 0 == btn:
				btn = self.__MakeWhisperButton(name)
				btn.Flash()

				chat.AppendChat(chat.CHAT_TYPE_NOTICE, localeInfo.RECEIVE_MESSAGE % (name))

			else:
				btn.Flash()
		elif self.IsGameMasterName(name):
			dlg = self.whisperDialogDict[name]
			dlg.SetGameMasterLook()

	def MakeWhisperButton(self, name):
		self.__MakeWhisperButton(name)

	def ShowWhisperDialog(self, btn):
		try:
			self.__MakeWhisperDialog(btn.name)
			dlgWhisper = self.whisperDialogDict[btn.name]
			dlgWhisper.OpenWithTarget(btn.name)
			dlgWhisper.Show()
			self.__CheckGameMaster(btn.name)
		except:
			import dbg
			dbg.TraceError("interface.ShowWhisperDialog - Failed to find key")

		self.__DestroyWhisperButton(btn)

	def MinimizeWhisperDialog(self, name):

		if 0 != name:
			self.__MakeWhisperButton(name)

		self.CloseWhisperDialog(name)

	def CloseWhisperDialog(self, name):

		if 0 == name:

			if self.dlgWhisperWithoutTarget:
				self.dlgWhisperWithoutTarget.Destroy()
				self.dlgWhisperWithoutTarget = None

			return

		try:
			dlgWhisper = self.whisperDialogDict[name]
			dlgWhisper.Destroy()
			del self.whisperDialogDict[name]
		except:
			import dbg
			dbg.TraceError("interface.CloseWhisperDialog - Failed to find key")

	def __ArrangeWhisperButton(self):

		screenWidth = wndMgr.GetScreenWidth()
		screenHeight = wndMgr.GetScreenHeight()

		xPos = screenWidth - 70
		yPos = 170 * screenHeight // 600
		yCount = (screenHeight - 330) // 63

		count = 0
		for button in self.whisperButtonList:

			button.SetPosition(xPos + (int(count//yCount) * -50), yPos + (count%yCount * 63))
			count += 1

	def __FindWhisperButton(self, name):
		for button in self.whisperButtonList:
			if button.name == name:
				return button

		return 0

	def __MakeWhisperDialog(self, name):
		dlgWhisper = uiWhisper.WhisperDialog(self.MinimizeWhisperDialog, self.CloseWhisperDialog)
		dlgWhisper.BindInterface(self)
		dlgWhisper.LoadDialog()
		dlgWhisper.SetPosition(self.windowOpenPosition*30,self.windowOpenPosition*30)
		self.whisperDialogDict[name] = dlgWhisper

		self.windowOpenPosition = (self.windowOpenPosition+1) % 5

		return dlgWhisper

	def __MakeWhisperButton(self, name):
		whisperButton = uiWhisper.WhisperButton()
		# Notification senders (np. "[Powiadomienia]") — distinctive icon + hot pink tooltip.
		# Reszta whisperow uzywa standardowej mail icon.
		isNotificationSender = name.startswith("[") and name.endswith("]")
		if isNotificationSender:
			# Dedykowana ikonka powiadomien (pack/assets/kowal/whisper/new_message_alert.png)
			whisperButton.SetUpVisual("kowal/whisper/new_message_alert.png")
			whisperButton.SetOverVisual("kowal/whisper/new_message_alert.png")
			whisperButton.SetDownVisual("kowal/whisper/new_message_alert.png")
		else:
			whisperButton.SetUpVisual("d:/ymir work/ui/game/windows/btn_mail_up.sub")
			whisperButton.SetOverVisual("d:/ymir work/ui/game/windows/btn_mail_up.sub")
			whisperButton.SetDownVisual("d:/ymir work/ui/game/windows/btn_mail_up.sub")
		if self.IsGameMasterName(name):
			whisperButton.SetToolTipTextWithColor(name, 0xffffa200)
		elif isNotificationSender:
			# Hot pink (#FFFF69B4) - zgodne z WHISPER_TYPE_SYSTEM kolorem w PythonChat.cpp
			whisperButton.SetToolTipTextWithColor(name, 0xffff69b4)
		else:
			whisperButton.SetToolTipText(name)
		whisperButton.ToolTipText.SetHorizontalAlignCenter()
		whisperButton.SetEvent(ui.__mem_func__(self.ShowWhisperDialog), whisperButton)
		whisperButton.Show()
		whisperButton.name = name

		self.whisperButtonList.insert(0, whisperButton)
		self.__ArrangeWhisperButton()

		return whisperButton

	def __DestroyWhisperButton(self, button):
		button.SetEvent(0)
		self.whisperButtonList.remove(button)
		self.__ArrangeWhisperButton()

	def HideAllWhisperButton(self):
		for btn in self.whisperButtonList:
			btn.Hide()

	def ShowAllWhisperButton(self):
		for btn in self.whisperButtonList:
			btn.Show()

	def __CheckGameMaster(self, name):
		if name not in self.listGMName:
			return
		if name in self.whisperDialogDict:
			dlg = self.whisperDialogDict[name]
			dlg.SetGameMasterLook()

	def RegisterGameMasterName(self, name):
		if name in self.listGMName:
			return
		self.listGMName[name] = "GM"

	def IsGameMasterName(self, name):
		if name in self.listGMName:
			return True
		else:
			return False

	if app.TAKE_LEGEND_DAMAGE_BOARD_SYSTEM:
		def OpenLegendDamageWindow(self, vid):
			import dbg
			dbg.TraceError("OpenLegendDamageWindow: %d " % vid)
			self.wndLegendDamageWindow.Show(vid)

		def SendLegendDamageData(self, vid, pos, name, level, race, empire, damage):
			if vid not in constInfo.LEGEND_DAMAGE_DATA:
				constInfo.LEGEND_DAMAGE_DATA[vid] = {
					"NAME": [None] * 15,
					"LEVEL": [None] * 15,
					"RACE": [None] * 15,
					"EMPIRE": [None] * 15,
					"DAMAGE": [None] * 15
				}

			damage_data = constInfo.LEGEND_DAMAGE_DATA[vid]
			damage_data["NAME"][pos] = name
			damage_data["LEVEL"][pos] = level
			damage_data["RACE"][pos] = race
			damage_data["EMPIRE"][pos] = empire
			damage_data["DAMAGE"][pos] = damage



	def BUILD_OpenWindow(self):
		self.wndGuildBuilding = uiGuild.BuildGuildBuildingWindow()
		self.wndGuildBuilding.Open()
		self.wndGuildBuilding.wnds = self.__HideWindows()
		self.wndGuildBuilding.SetCloseEvent(ui.__mem_func__(self.BUILD_CloseWindow))

	def BUILD_CloseWindow(self):
		self.__ShowWindows(self.wndGuildBuilding.wnds)
		self.wndGuildBuilding = None

	def BUILD_OnUpdate(self):
		if not self.wndGuildBuilding:
			return

		if self.wndGuildBuilding.IsPositioningMode():
			import background
			x, y, z = background.GetPickingPoint()
			self.wndGuildBuilding.SetBuildingPosition(x, y, z)

	def BUILD_OnMouseLeftButtonDown(self):
		if not self.wndGuildBuilding:
			return

		if self.wndGuildBuilding.IsPositioningMode():
			self.wndGuildBuilding.SettleCurrentPosition()
			return True
		elif self.wndGuildBuilding.IsPreviewMode():
			pass
		else:
			return True
		return False

	def BUILD_OnMouseLeftButtonUp(self):
		if not self.wndGuildBuilding:
			return

		if not self.wndGuildBuilding.IsPreviewMode():
			return True

		return False

	def BULID_EnterGuildArea(self, areaID):
		mainCharacterName = player.GetMainCharacterName()
		masterName = guild.GetGuildMasterName()

		if mainCharacterName != masterName:
			return

		if areaID != player.GetGuildID():
			return

		self.wndGameButton.ShowBuildButton()

	def BULID_ExitGuildArea(self, areaID):
		self.wndGameButton.HideBuildButton()
		
	if app.__BL_CHEST_DROP_INFO__:
		def OpenChestDropWindow(self, itemVnum, isMain):
			if self.wndChestDropInfo:
				self.wndChestDropInfo.Open(itemVnum, isMain)

	def RequestOpenItemShop(self):
		self.wndItemShop.RequestOpen()

	def TombolaStart(self, pos, to_pos, to_spin, time):
		self.wndItemShop.StartSpinning(pos, to_pos, to_spin, time)

	def TombolaSetSpinningItem(self, pos, vnum, count):
		self.wndItemShop.SetSpinningItem(pos, vnum, count)

	def TombolaOpen(self):
		self.wndItemShop.Show()

	def TombolaSetPrice(self, group, price, price_type):
		self.wndItemShop.SetPrice(group, price, price_type)

	def TombolaSetItem(self, group, vnum, count, chance):
		self.wndItemShop.SetItem(group, vnum, count, chance)

	def TombolaClear(self):
		self.wndItemShop.TombolaClear()

	def IsEditLineFocus(self):
		if self.ChatWindow.chatLine.IsFocus():
			return 1

		if self.ChatWindow.chatToLine.IsFocus():
			return 1

		return 0

	def ActiveTileNow(self, id):
		self.wndWeeklyRankWindow_New.Active(id)

	def GetActiveTitleNow(self):
		self.wndWeeklyRankWindow_New.GetActiveNow()

	def TitleEnable(self, id, val):
		self.wndWeeklyRankWindow_New.Enable(id, val)

	def OfflineShopLogs(self, id, item, count, price, price2, date, action):
		self.wndOfflineShopLogPanel.SendLogs(id, item, count, price, price2, date, action)

	def SelectPage(self, page, season):
		self.wndWeeklyRankWindow_New.PutPage(page, season)

	def SendWeeklyInfo(self, pos, name, points, empire, job):
		self.wndWeeklyRankWindow_New.LoadPage(pos, name, points, empire, job)


	if app.BL_MOVE_CHANNEL:
		def RefreshServerInfo(self, channelNumber):
			if self.wndMiniMap:
				self.wndMiniMap.RefreshServerInfo(channelNumber)

	def UseDSSButtonEffect(self, enable):
		if self.wndInventory:
			self.wndInventory.UseDSSButtonEffect(enable)
	
	def EmptyFunction(self):
		pass

	def GetInventoryPageIndex(self):
		if self.wndInventory:
			return self.wndInventory.GetInventoryPageIndex()
		else:
			return -1

	if app.WJ_ENABLE_TRADABLE_ICON:
		def SetOnTopWindow(self, onTopWnd):
			self.onTopWindow = onTopWnd

		def GetOnTopWindow(self):
			return self.onTopWindow

		def RefreshMarkInventoryBag(self):
			self.wndInventory.RefreshMarkSlots()

	def MouseSlotEventClear(self):
		if self.wndInventory:
			self.wndInventory.MouseSlotEventClear()
			self.RefreshMarkInventoryBag()
		
		if self.wndDragonSoul:
			self.wndDragonSoul.MouseSlotEventClear()
			self.RefreshMarkInventoryBag()
		
		if self.wndExtendedInventory:
			self.wndExtendedInventory.MouseSlotEventClear()
			self.RefreshMarkInventoryBag()
					
	if app.ENABLE_LOADING_PERFORMANCE:
		def OpenWarpShowerWindow(self):
			if self.wndMiniMap and self.wndMiniMap.IsShowingAtlas():
				self.wndMiniMap.ToggleAtlasWindow()

			if self.dlgSystem:
				self.dlgSystem.Close()
				self.dlgSystem.Destroy()

			self.HideAllQuestButton()
			self.HideAllWhisperButton()

			self.HideAllWindows()

			self.wndWarpShower.Open()

		def CloseWarpShowerWindow(self):
			if self.wndWarpShower:
				self.wndWarpShower.Close()

	if app.ENABLE_EVENT_MANAGER:
		def MakeEventIcon(self):
			if self.wndEventIcon == None:
				self.wndEventIcon = uiEventCalendar.MovableImage()
				self.wndEventIcon.Show()
		def MakeEventCalendar(self):
			if self.wndEventManager == None:
				self.wndEventManager = uiEventCalendar.EventCalendarWindow()
		def OpenEventCalendar(self):
			self.MakeEventCalendar()
			if self.wndEventManager.IsShow():
				self.wndEventManager.Close()
			else:
				self.wndEventManager.Open()
		def RefreshEventStatus(self, eventID, eventStatus, eventendTime, eventEndTimeText):
			if eventendTime != 0:
				eventendTime += app.GetGlobalTimeStamp()
			uiEventCalendar.SetEventStatus(eventID, eventStatus, eventendTime, eventEndTimeText)
			self.RefreshEventManager()
		def ClearEventManager(self):
			uiEventCalendar.server_event_data={}
		def RefreshEventManager(self):
			if self.wndEventManager:
				self.wndEventManager.Refresh()
			if self.wndEventIcon:
				self.wndEventIcon.Refresh()
		def AppendEvent(self, dayIndex, eventID, eventIndex, startTime, endTime, empireFlag, channelFlag, value0, value1, value2, value3, startRealTime, endRealTime, isAlreadyStart):
			self.MakeEventCalendar()
			self.MakeEventIcon()
			if startRealTime != 0:
				startRealTime += app.GetGlobalTimeStamp()
			if endRealTime != 0:
				endRealTime += app.GetGlobalTimeStamp()
			uiEventCalendar.SetServerData(dayIndex, eventID, eventIndex, startTime, endTime, empireFlag, channelFlag, value0, value1, value2, value3, startRealTime, endRealTime, isAlreadyStart)

	def ToggleBattlePass(self):
		if False == player.IsObserverMode():
			bp = self._EnsureBattlePass()
			if False == bp.IsShow():
				bp.Open()
				bp.SetTop()
			else:
				bp.Close()

	def EmptyFunction(self):
		pass

	def GetWindowByType(self, type):
		windows = {
			player.INVENTORY: self.wndInventory,
			player.DRAGON_SOUL_INVENTORY: self.wndDragonSoul
		}
		
		return windows.get(type, None)

	def GetInventory(self):
		return self.wndInventory
		
	if app.ENABLE_SAVE_LOCATION_SYSTEM:
		def __MakeSaveLocationWindow(self):
			self.wndSaveLocation = uiSaveLocation.SaveLocationWindow()
			if self.wndSaveLocation.IsShow():
				self.wndSaveLocation.Show()

		def ToggleSaveLocationWindow(self):
			if not self.wndSaveLocation:
				return

			if player.IsObserverMode():
				return

			if not self.wndSaveLocation.IsShow():
				self.wndSaveLocation.Show()
				self.wndSaveLocation.SetTop()
			else:
				self.wndSaveLocation.Close()

		def UpdateSaveLocation(self, pos, name, x, y):
			if self.wndSaveLocation:
				self.wndSaveLocation.UpdateSaveLocation(pos, name, x, y)

		def DeleteSaveLocation(self, pos):
			if self.wndSaveLocation:
				self.wndSaveLocation.DeleteSaveLocation(pos)

	def MakeSwitchbotWindow(self):
		self.wndSwitchbot = uiswitchbot.SwitchbotWindow()

	def ToggleSwitchbotWindow(self):
		if not self.wndSwitchbot:
			self.MakeSwitchbotWindow()

		if player.IsObserverMode():
			return

		if not self.wndSwitchbot.IsShow():
			self.wndSwitchbot.Show()
			self.wndSwitchbot.SetTop()
		else:
			self.wndSwitchbot.Close()

	def ToggleRankingWindow(self):
		wnd = self._EnsureRankingWindow()
		if wnd.IsShow():
			wnd.Close()
		else:
			wnd.OpenWindow()

	def ToggleRankingWindowWeekly(self):
		wnd = self._EnsureRankingWindowWeekly()
		if wnd.IsShow():
			wnd.Close()
		else:
			wnd.OpenWindow()

	if app.ENABLE_SECONDARY_LEVEL:
		def ToggleSecondaryLevel(self):
			if self.wndSecondaryLevel.IsShow():
				self.wndSecondaryLevel.Close()
			else:
				self.wndSecondaryLevel.Open()

	def AttachItemFromSafebox(self, slotIndex, itemIndex):
		if self.wndInventory and self.wndInventory.IsShow():
			self.wndInventory.AttachItemFromSafebox(slotIndex, itemIndex)

		return True

	def AttachInvenItemToOtherWindowSlot(self, slotWindow, slotIndex):
		if self.wndSafebox and self.wndSafebox.IsShow():
			return self.wndSafebox.AttachItemFromInventory(slotWindow, slotIndex)

		return False

	if hasattr(app, "ENABLE_PREMIUM_PRIVATE_SHOP_OFFICIAL") and app.ENABLE_PREMIUM_PRIVATE_SHOP_OFFICIAL:
		def OpenPrivateShopPanel(self):
			if self.wndPrivateShopPanel:
				self.wndPrivateShopPanel.Open()

			if not self.wndInventory.IsShow():
				self.wndInventory.Show()

		def ClosePrivateShopPanel(self):
			if self.wndPrivateShopPanel:
				self.wndPrivateShopPanel.Close(False)

		def RefreshPrivateShopWindow(self):
			if self.wndPrivateShopPanel:
				self.wndPrivateShopPanel.Refresh()
				self.wndPrivateShopPanel.RefreshWindow()

		def TogglePrivateShopPanelWindow(self):
			if False == player.IsObserverMode():
				if not self.wndPrivateShopPanel.RequestOpen():
					self.wndPrivateShopPanel.Close()

		def TogglePrivateShopPanelWindowCheck(self):
			if False == player.IsObserverMode():
				if not self.wndPrivateShopPanel.RequestOpen(True):
					self.wndPrivateShopPanel.Close()

		def OpenPrivateShopSearch(self, mode):
			if self.wndPrivateShopSearch:
				self.wndPrivateShopSearch.Open(mode)

		def PrivateShopSearchUpdate(self, index, state):
			if self.wndPrivateShopSearch:
				self.wndPrivateShopSearch.UpdateResult(index, state)

		def PrivateShopSearchRefresh(self):
			if self.wndPrivateShopSearch:
				self.wndPrivateShopSearch.RefreshPage()

		def AppendMarketItemPrice(self, gold, cheque):
			if self.wndPrivateShopPanel and self.wndPrivateShopPanel.IsShow():
				self.wndPrivateShopPanel.AppendMarketItemPrice(gold, cheque)

			elif self.privateShopBuilder and self.privateShopBuilder.IsShow():
				self.privateShopBuilder.AppendMarketItemPrice(gold, cheque)

		def AddPrivateShopTitleBoard(self, vid, text, type):
			board = uiPrivateShop.PrivateShopTitleBoard(type)
			board.Open(vid, text)

			self.privateShopAdvertisementBoardDict[vid] = board

		def RemovePrivateShopTitleBoard(self, vid):
			if vid not in self.privateShopAdvertisementBoardDict:
				return

			del self.privateShopAdvertisementBoardDict[vid]
			uiPrivateShop.DeleteTitleBoard(vid)

		def SetPrivateShopPremiumBuild(self):
			if self.wndPrivateShopPanel:
				self.wndPrivateShopPanel.SetPremiumBuildMode()
				self.wndPrivateShopPanel.RefreshWindow()

		def PrivateShopStateUpdate(self):
			if self.wndPrivateShopPanel:
				self.wndPrivateShopPanel.OnStateUpdate()

	# Voice Chat (Opus) — voice-chat/CHANGES_ZARIS.md (Etap 5)
	if app.ENABLE_VOICE_CHAT:
		def ToggleVoiceChatConfigWindow(self):
			if self.wndVoiceChatConfig:
				if self.wndVoiceChatConfig.IsShow():
					self.wndVoiceChatConfig.Hide()
				else:
					self.wndVoiceChatConfig.Show()
					self.wndVoiceChatConfig.SetTop()

_instance = None

def GetInstance():
	global _instance
	return _instance

def SetInstance(instance):
	global _instance
	
	if _instance:
		del _instance
	
	_instance = instance
