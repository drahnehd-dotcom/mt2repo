#-*- coding: iso-8859-1 -*-
import ui
import player
import mouseModule
import net
import app
import snd
import item
import chat
import grp
import uiScriptLocale
import uiRefine
import uiAttachMetin
import dbg
import uiPickMoney
import uiCommon
import uiPrivateShopBuilder
import localeInfo
import constInfo
import settings
import ime
import wndMgr
import uiToolTip
import emoji
import uiDeposit
import grid
import itemWrapper
import safebox
import math
from _weakref import proxy
from uiFishWiki import GetFishMissionData

if app.ENABLE_AURA_SYSTEM:
	import aura
if app.ENABLE_NEW_STONE_DETACH:
	import uistonedetach
if app.ENABLE_CHEQUE_SYSTEM:
	import uiPickETC
if app.ENABLE_OFFLINE_SHOP_SYSTEM:
	import uiOfflineShopBuilder
	import uiOfflineShop
if app.ENABLE_ACCE_COSTUME_SYSTEM:
	import acce
if app.ITEM_CHECKINOUT_UPDATE:
	import exchange

if app.ENABLE_PREMIUM_PRIVATE_SHOP_OFFICIAL:
	import uiPrivateShop
	import privateShop
if app.ENABLE_OFFLINE_SHOP:
	import offlineshop, uiOfflineShop

if app.WJ_SPLIT_INVENTORY_SYSTEM:
	SPECIAL_INV_NAMES = [localeInfo.SPECIAL_INVENTORY_BOOKS, 
					  localeInfo.SPECIAL_INVENTORY_REFINE, 
					  localeInfo.SPECIAL_INVENTORY_STONES_ALCHEMY, 
					  localeInfo.SPECIAL_INVENTORY_CHESTS, 
					  localeInfo.SPECIAL_INVENTORY_USABLE,
					  localeInfo.SPECIAL_INVENTORY_DEWS]
	start_val_table = [item.SKILL_BOOK_INVENTORY_SLOT_START, item.UPGRADE_ITEMS_INVENTORY_SLOT_START, item.STONE_INVENTORY_SLOT_START, item.BOX_INVENTORY_SLOT_START, item.EFSUN_INVENTORY_SLOT_START, item.CICEK_INVENTORY_SLOT_START]
	end_val_table = [item.SKILL_BOOK_INVENTORY_SLOT_END, item.UPGRADE_ITEMS_INVENTORY_SLOT_END, item.STONE_INVENTORY_SLOT_END, item.BOX_INVENTORY_SLOT_END, item.EFSUN_INVENTORY_SLOT_END, item.CICEK_INVENTORY_SLOT_END]
		
INSTANT_OPEN_COUNT = 1000

# Karmniki towarzysza (ITEM::USE_COMPANION_EXP_VOUCHER). -1 gdy klient zbudowany
# bez ENABLE_MOUNT_SYSTEM - wtedy Shift+PPM zachowuje sie jak zwykle PPM.
COMPANION_EXP_VOUCHER_SUBTYPE = getattr(item, "USE_COMPANION_EXP_VOUCHER", -1)

SYSTEMS_WINDOW=1
ITEM_MALL_BUTTON_ENABLE = True
ITEM_FLAG_APPLICABLE = 1 << 14

ALLOWED_TYPES = [
"USE_ADD_ATTRIBUTE", "USE_CHANGE_ATTRIBUTE",
"USE_ADD_ATTRIBUTE_SPECIAL_1", "USE_ADD_ATTRIBUTE",
"USE_CHANGE_ATTRIBUTE2", "USE_TUNING", "USE_ADD_IS_BONUS",
"USE_ADD_NEW_BONUS", "USE_ADD_EXTRA_BONUS", "USE_FISHING_ROD_ADD_ATTRIBUTE"
]

# Podtypy itemow otwierajacych okno zmiennika bonusow (uibonuschanger).
# Wczesniej bylo to zahardkodowane na vnum 71084, przez co 71151 (Zielony Czar)
# i inne zmianki (39028 / 76014 / 76023) omijaly okno.
CHANGER_USE_TYPES = frozenset(("USE_CHANGE_ATTRIBUTE", "USE_CHANGE_ATTRIBUTE2"))

INVENTORY_SLOT_TYPES = frozenset((
	player.SLOT_TYPE_INVENTORY,
	player.SLOT_TYPE_SKILL_BOOK_INVENTORY,
	player.SLOT_TYPE_UPGRADE_ITEMS_INVENTORY,
	player.SLOT_TYPE_STONE_INVENTORY,
	player.SLOT_TYPE_BOX_INVENTORY,
	player.SLOT_TYPE_EFSUN_INVENTORY,
	player.SLOT_TYPE_CICEK_INVENTORY,
))

class SystemsWindow(ui.ScriptWindow):
	def __init__(self, wndInventory, tooltip):
		import exception

		if not wndInventory:
			return
			 	 
		ui.ScriptWindow.__init__(self)

		self.isLoaded = 0
		self.selectedSlotPos=0
		self.wndInventory = wndInventory;
		self.expandBtn = None
		self.minBtn = None
		self.toolTip = tooltip

		self.__LoadWindow()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def SetTooltip(self, tooltip):
		self.toolTip = tooltip

	def Show(self, gelen):
		self.__LoadWindow()

		ui.ScriptWindow.Show(self)
		
		if gelen == 1:
			constInfo.SYSTEMS_WINDOW_OPEN=1
			self.OpenInventory()
		else:
			constInfo.SYSTEMS_WINDOW_OPEN=0
			self.CloseInventory()

	def BindInterfaceClass(self, interface):
		self.interface = interface

	def Close(self):
		constInfo.SYSTEMS_WINDOW_OPEN=0
		for i in range(1,self.TOOLTIP_VALUE_MAX):
			self.toolTip[i].HideToolTip()
		self.Hide()

	def Destroy(self):
		constInfo.SYSTEMS_WINDOW_OPEN=0
		self.interface = None
		for i in range(1,self.TOOLTIP_VALUE_MAX):
			self.toolTip[i].HideToolTip()
		self.Hide()
		
	def IsOpeningInventory(self):
		return self.wndSystemsWindowLayer.IsShow()
		
	def OpenInventory(self):
		global SYSTEMS_WINDOW
		self.wndSystemsWindowLayer.Show()
		self.expandBtn.Hide()
		SYSTEMS_WINDOW = 1

		self.AdjustPositionAndSize()

	def CloseInventory(self):
		global SYSTEMS_WINDOW
		self.wndSystemsWindowLayer.Hide()
		self.expandBtn.Show()
		SYSTEMS_WINDOW = 0
		
		self.AdjustPositionAndSize()

	def _readLayoutMode(self):
		# Cache layout mode — bez tego open("lib/settings") leci na dysk co frame
		# z OnUpdate->AdjustPositionAndSize->GetBasePosition (3x file read/frame).
		cached = getattr(self, "_layoutModeCache", None)
		if cached is not None:
			return cached
		try:
			cached = int(open("lib/settings", "r").readlines()[0])
		except:
			cached = 1
		self._layoutModeCache = cached
		return cached

	def GetBasePosition(self):
		x, y = self.wndInventory.GetGlobalPosition()
		if self._readLayoutMode() == 1:
			return x - 160 + 15, y + 100
		else:
			return x - 160 + 90, y + 100 - 30

	def AdjustPositionAndSize(self):
		bx, by = self.GetBasePosition()
		byEK = 37
		isNewLayout = (self._readLayoutMode() == 1)
		if self.IsOpeningInventory():
			if isNewLayout:
				self.SetPosition(bx, by + 6 - byEK)
			else:
				self.SetPosition(bx - 17, by + 6 - byEK)
			self.SetSize(self.ORIGINAL_WIDTH, self.GetHeight())
		else:
			if isNewLayout:
				self.SetPosition(bx + 158 - 15, by + 10 - byEK)
			else:
				self.SetPosition(bx + 158 - 90, by + 6 - byEK)
			self.SetSize(10, self.GetHeight())

	def __LoadWindow(self):
		if self.isLoaded == 1:
			return

		self.isLoaded = 1

		try:
			pyScrLoader = ui.PythonScriptLoader()
			layoutMode = self._readLayoutMode()
			if layoutMode == 0:
				constInfo.MenuSelectModel2 = 0
				pyScrLoader.LoadScriptFile(self, "UIScript/SystemsWindow.py")
			else:
				constInfo.MenuSelectModel1 = 0
				pyScrLoader.LoadScriptFile(self, "uiscript/systemswindow_new.py")
		except:
			import exception
			exception.Abort("SystemsWindow.LoadWindow.LoadObject")

		try:
			self.ORIGINAL_WIDTH = self.GetWidth()
			self.wndSystemsWindowLayer = self.GetChild("SystemsWindowLayer")
			self.expandBtn = self.GetChild("ExpandBtn")
			self.minBtn = self.GetChild("MinimizeBtn")
			self.expandBtn.SetEvent(ui.__mem_func__(self.OpenInventory))
			self.minBtn.SetEvent(ui.__mem_func__(self.CloseInventory))


			gc = self.GetChild
			m = ui.__mem_func__
			t = uiToolTip.ToolTipNew
			i = self.wndInventory

			BUTTON_DEFS = (
				("Mapa_Button", "ToggleMap", 120, localeInfo.INVENTORY_PANEL_TELEPORTATION, None),
				("Localizacja_Button", "ToggleLokalizacja", 120, localeInfo.INVENTORY_PANEL_SAVE_POSITION, "icon/emoji/key_f7.png"),
				("ShopButton", "OpenPrivateShopBuilder", 98, localeInfo.INVENTORY_PANEL_SHOP, None),
				("aExp_Button", "ToggleAntyExp", 150, localeInfo.INVENTORY_PANEL_BLOCK_EXP, None),
				("Dodatkowe_Button", "ToggleDodatkowy", 150, localeInfo.INVENTORY_PANEL_SPECIAL_INV, "icon/emoji/key_k.png"),
				("Pet_Button", "TogglePet", 132, localeInfo.INVENTORY_PANEL_PET_WINDOW, "icon/emoji/key_p.png"),
				("Ranking_Button", "ToggleRanking", 147, localeInfo.INVENTORY_PANEL_WEEKLY_RANK, None),
				("Dopek_Button", "ToggleWspomagacze", 132, localeInfo.INVENTORY_PANEL_BOOSTERS, "ACTIVATE:icon/emoji/key_f5.png"),
				("TabelaBon_Button", "ToggleBonus", 129, localeInfo.INVENTORY_PANEL_BONUS_TABLE, None),
				("Switcher_Button", "ToggleSwitcher", 129, localeInfo.INVENTORY_PANEL_SWITCH_BOT, None),
				("Shaman_Button", "ToggleShaman", 134, localeInfo.INVENTORY_PANEL_AUTO_BUFF, None),
				("ShopSearch_Button", "ToggleSearchShop", 144, localeInfo.INVENTORY_PANEL_POLY_SHOP, "icon/emoji/key_f9.png"),
				("Kosz_Button", "ToggleKosz", 55, localeInfo.INVENTORY_PANEL_TRASH_BIN, None),
				("BiologButton", "ToggleCollectWindow", 132, localeInfo.INVENTORY_PANEL_MISSIONS, "icon/emoji/key_f11.png"),
				("Artifact_Button", "ToggleArtifact", 80, localeInfo.INVENTORY_PANEL_ARTIFACTS, None),
				("Mount_Button", "ToggleMount", 178, localeInfo.INVENTORY_PANEL_MOUNT, None),
				("Dung_Button", "ToggleDungeon", 118, localeInfo.INVENTORY_PANEL_DUNGEONS, "icon/emoji/key_f10.png"),
			)

			self.TOOLTIP_VALUE_MAX = len(BUTTON_DEFS) + 1
			self.button = {}
			self.toolTip = {}
			for idx, (childName, methodName, ttWidth, ttTitle, hotkey) in enumerate(BUTTON_DEFS, 1):
				self.button[idx] = gc(childName)
				self.button[idx].SetEvent(m(getattr(i, methodName)))
				self.toolTip[idx] = t(ttWidth)
				self.toolTip[idx].SetTitle(ttTitle)
				if hotkey:
					self.toolTip[idx].AppendHorizontalLine()
					if hotkey.startswith("ACTIVATE:"):
						self.toolTip[idx].AppendTextLine(localeInfo.INVENTORY_PANEL_ACTIVATE.format(emoji.AppendEmoji(hotkey[9:])))
					else:
						self.toolTip[idx].AppendTextLine(localeInfo.INVENTORY_PANEL_USE.format(emoji.AppendEmoji(hotkey)))
		except:
			import exception
			exception.Abort("SystemsWindow.LoadWindow.BindObject")

	def OpenSafeBox(self):
		self.wndDeposit.Open()

	def OnUpdate(self):
		for i in range(1,self.TOOLTIP_VALUE_MAX):
			if self.button[i].IsIn():
				self.toolTip[i].Show()
			else:
				self.toolTip[i].HideToolTip()

		self.AdjustPositionAndSize()

		if constInfo.SYSTEMS_WINDOW_CLOSE==1:
			self.Close()
			constInfo.SYSTEMS_WINDOW_CLOSE=0

class CostumeWindow(ui.ScriptWindow):

	def __init__(self, wndInventory):
		import exception

		if not app.ENABLE_COSTUME_SYSTEM:
			exception.Abort("What do you do?")
			return

		if not wndInventory:
			exception.Abort("wndInventory parameter must be set to InventoryWindow")
			return

		ui.ScriptWindow.__init__(self)

		self.isLoaded = 0
		self.wndInventory = wndInventory;

		if app.ENABLE_HIDE_COSTUME_SYSTEM:
			self.visibleButtonList = []

		self.__LoadWindow()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def Show(self):
		self.__LoadWindow()
		self.RefreshCostumeSlot()

		ui.ScriptWindow.Show(self)

	def Close(self):
		self.Hide()

	def GetBasePosition(self):
		x, y = self.wndInventory.GetGlobalPosition()
		return x - 147, y

	def AdjustPositionAndSize(self):
		bx, by = self.GetBasePosition()

		self.SetPosition(bx, by)
		self.SetSize(self.GetWidth(), self.GetHeight())

	def __LoadWindow(self):
		if self.isLoaded == 1:
			return

		self.isLoaded = 1

		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "UIScript/CostumeWindow.py")
		except:
			import exception
			exception.Abort("CostumeWindow.LoadWindow.LoadObject")

		try:
			wndEquip = self.GetChild("CostumeSlot")
			self.GetChild("TitleBar").SetCloseEvent(ui.__mem_func__(self.Close))

			if app.ENABLE_HIDE_COSTUME_SYSTEM:
				for name in ("BodyToolTipButton", "HairToolTipButton", "AcceToolTipButton", "WeaponToolTipButton", "AuraToolTipButton", "StoleToolTipButton"):
					self.visibleButtonList.append(self.GetChild(name))

		except:
			import exception
			exception.Abort("CostumeWindow.LoadWindow.BindObject")

		wndEquip.SetOverInItemEvent(ui.__mem_func__(self.wndInventory.OverInItem))
		wndEquip.SetOverOutItemEvent(ui.__mem_func__(self.wndInventory.OverOutItem))
		wndEquip.SetUnselectItemSlotEvent(ui.__mem_func__(self.wndInventory.UseItemSlot))
		wndEquip.SetUseSlotEvent(ui.__mem_func__(self.wndInventory.UseItemSlot))
		wndEquip.SetSelectEmptySlotEvent(ui.__mem_func__(self.wndInventory.SelectEmptySlot))
		wndEquip.SetSelectItemSlotEvent(ui.__mem_func__(self.wndInventory.SelectItemSlot))

		self.wndEquip = wndEquip

		if app.ENABLE_HIDE_COSTUME_SYSTEM:
			for idx, btn in enumerate(self.visibleButtonList):
				btn.SetToggleUpEvent(ui.__mem_func__(self.VisibleCostume), idx + 1, 0)
				btn.SetToggleDownEvent(ui.__mem_func__(self.VisibleCostume), idx + 1, 1)

	def RefreshCostumeSlot(self):
		getItemVNum=player.GetItemIndex

		for i in range(item.COSTUME_SLOT_COUNT):
			slotNumber = item.COSTUME_SLOT_START + i
			self.wndEquip.SetItemSlot(slotNumber, getItemVNum(slotNumber), 0)

		if app.ENABLE_WEAPON_COSTUME_SYSTEM:
			self.wndEquip.SetItemSlot(item.COSTUME_SLOT_WEAPON, getItemVNum(item.COSTUME_SLOT_WEAPON), 0)

		self.wndEquip.RefreshSlot()

	if app.ENABLE_HIDE_COSTUME_SYSTEM:
		def RefreshVisibleCostume(self):
			costumeStates = (
				constInfo.HIDDEN_BODY_COSTUME,
				constInfo.HIDDEN_HAIR_COSTUME,
				constInfo.HIDDEN_ACCE_COSTUME,
				constInfo.HIDDEN_WEAPON_COSTUME,
				constInfo.HIDDEN_AURA_COSTUME,
				constInfo.HIDDEN_STOLE_COSTUME,
			)
			for i, hidden in enumerate(costumeStates):
				if hidden == 1:
					self.visibleButtonList[i].Down()
				else:
					self.visibleButtonList[i].SetUp()

		def VisibleCostume(self, part, hidden):
			net.SendChatPacket("/hide_costume %d %d" % (part, hidden))

if app.WJ_SPLIT_INVENTORY_SYSTEM:
	class ExtendedInventoryWindow(ui.ScriptWindow):
		tooltipItem = None
		dlgPickMoney = None

		dlgPickItem = None
		sellingSlotNumber = -1
		isLoaded = 0
		if app.ENABLE_HIGHLIGHT_NEW_ITEM:
			liHighlightedItems = []

		INVENTORY_TYPE_CONFIG = (
			(player.SKILL_BOOK_INVENTORY_SLOT_COUNT, item.SKILL_BOOK_INVENTORY_SLOT_START, player.SLOT_TYPE_SKILL_BOOK_INVENTORY),
			(player.UPGRADE_ITEMS_INVENTORY_SLOT_COUNT, item.UPGRADE_ITEMS_INVENTORY_SLOT_START, player.SLOT_TYPE_UPGRADE_ITEMS_INVENTORY),
			(player.STONE_INVENTORY_SLOT_COUNT, item.STONE_INVENTORY_SLOT_START, player.SLOT_TYPE_STONE_INVENTORY),
			(player.BOX_INVENTORY_SLOT_COUNT, item.BOX_INVENTORY_SLOT_START, player.SLOT_TYPE_BOX_INVENTORY),
			(player.EFSUN_INVENTORY_SLOT_COUNT, item.EFSUN_INVENTORY_SLOT_START, player.SLOT_TYPE_EFSUN_INVENTORY),
			(player.CICEK_INVENTORY_SLOT_COUNT, item.CICEK_INVENTORY_SLOT_START, player.SLOT_TYPE_CICEK_INVENTORY),
		)
		PAGE_MULTIPLIERS = (0, 0.3334, 0.6668)
		PAGE_OFFSETS = (0, 45, 90)
		TYPE_TITLES = (
			localeInfo.INVENTORY_SKILL_BOOK_TOOLTIP,
			localeInfo.INVENTORY_UPGRADE_ITEM_TOOLTIP,
			localeInfo.INVENTORY_STONE_TOOLTIP,
			localeInfo.INVENTORY_BOX_TOOLTIP,
			localeInfo.INVENTORY_EFSUN_TOOLTIP,
			localeInfo.INVENTORY_CICEK_TOOLTIP,
		)

		def __init__(self):
			ui.ScriptWindow.__init__(self)
			self.inventoryPageIndex = 0
			self.__LoadWindow()
			
		def __del__(self):
			ui.ScriptWindow.__del__(self)

		def __LocalSlotToGlobal(self, localSlot):
			cfg = self.INVENTORY_TYPE_CONFIG[self.inventoryType]
			return localSlot + cfg[1] + self.PAGE_OFFSETS[self.GetInventoryPageIndex()]

		def Show(self):
			constInfo.EXTENDED_INVENTORY_IS_OPEN = 1
			self.__LoadWindow()
			# refresh robimy tu, bo RefreshItemSlot pomija ukryte okno (patrz nizej)
			self.RefreshBagSlotWindow()
			ui.ScriptWindow.Show(self)
			
		def BindInterfaceClass(self, interface):
			self.interface = interface

		def __LoadWindow(self):
			if self.isLoaded == 1:
				return

			self.isLoaded = 1

			try:
				pyScrLoader = ui.PythonScriptLoader()
				pyScrLoader.LoadScriptFile(self, "UIScript/ExtendedInventoryWindow.py")
			except:
				import exception
				exception.Abort("ExtendedInventoryWindow.LoadWindow.LoadObject")

			try:
				self.wndItem = self.GetChild("ItemSlot")
				self.__BindWidgets()
			except:
				import exception
				exception.Abort("ExtendedInventoryWindow.LoadWindow.BindObject")

			self.__SetupTooltips()
			self.__SetupEvents()
			self.__SetupDialogs()

			self.SetInventoryType(0)
			self.SetInventoryPage(0)
			self.wndCostume = None

		def __BindWidgets(self):
			gc = self.GetChild
			gc("TitleBar").SetCloseEvent(ui.__mem_func__(self.Close))
			self.titleName = gc("inventory_title")

			self.SkillBookButton = gc("SkillBookButton")
			self.UpgradeItemsButton = gc("UpgradeItemsButton")
			self.stoneButton = gc("StoneButton")
			self.boxButton = gc("BoxButton")
			self.efsunButton = gc("EfsunButton")
			self.cicekButton = gc("CicekButton")
			self.typeButtons = [self.SkillBookButton, self.UpgradeItemsButton, self.stoneButton, self.boxButton, self.efsunButton, self.cicekButton]

			self.SettingsButton = gc("SettingsButton")
			self.window_settings = gc("window_settings")
			self.DirectUseButton = gc("DirectUseButton")
			self.OpenWithInventoryButton = gc("OpenWithInventoryButton")
			self.OpenWhenFastMoveButton = gc("OpenWhenFastMoveButton")

			self.inventoryTab = [gc("Inventory_Tab_%02d" % (i+1)) for i in range(3)]
			self.sortinv = gc("RefreshButton")
			self.packall = gc("PackAllButton")
			self.listCantMouseSlot = []

		def __SetupTooltips(self):
			t = uiToolTip.ToolTipNew

			TOOLTIP_WIDTHS = (180, 140, 50, 180, 180, 60, 130, 60, 190, 225, 240, 233)
			self.tt = {i+1: t(w) for i, w in enumerate(TOOLTIP_WIDTHS)}

			TOOLTIP_CONTENT = (
				(1, localeInfo.INVENTORY_STACK_ITEMS, (
					("space", 2), ("hline",),
					("text", localeInfo.INVENTORY_STACK_ITEMS_IN_CATEGORY.format(emoji.AppendEmoji("icon/emoji/key_lclick.png"))),
					("text", localeInfo.INVENTORY_STACK_ALL.format(emoji.AppendEmoji("icon/emoji/key_shift.png"), emoji.AppendEmoji("icon/emoji/key_lclick.png"))),
				)),
				(9, localeInfo.INVENTORY_OPEN_TOGETHER_WITH_EQUIPMENT, ()),
				(10, localeInfo.INVENTORY_DROP_TO_INVENTORY, (
					("space", 2), ("hline",),
					("text", localeInfo.INVENTORY_DROP_TO_INVENTORY_DESC1),
					("text", localeInfo.INVENTORY_DROP_TO_INVENTORY_DESC2),
				)),
				(11, localeInfo.INVENTORY_OPENING_WHILE_MOVING, (
					("space", 2), ("hline",),
					("text", localeInfo.INVENTORY_OPTION_INFO_1),
					("text", localeInfo.INVENTORY_OPTION_INFO_2),
					("text", localeInfo.INVENTORY_OPTION_INFO_3),
					("text", localeInfo.INVENTORY_OPTION_INFO_4.format(emoji.AppendEmoji("icon/emoji/key_shift.png"), emoji.AppendEmoji("icon/emoji/key_rclick.png"))),
				)),
				(12, localeInfo.INVENTORY_MOVE_ALL, (
					("space", 2), ("hline",),
					("text", localeInfo.INVENTORY_MOVE_ALL_DESC_1),
					("text", localeInfo.INVENTORY_MOVE_ALL_DESC_2),
				)),
			)

			for key, title, lines in TOOLTIP_CONTENT:
				self.tt[key].SetTitle(title)
				for entry in lines:
					if entry[0] == "space":
						self.tt[key].AppendSpace(entry[1])
					elif entry[0] == "hline":
						self.tt[key].AppendHorizontalLine()
					elif entry[0] == "text":
						self.tt[key].AppendTextLine(entry[1])

			for idx, name in enumerate(SPECIAL_INV_NAMES):
				self.tt[idx + 3].SetTitle(name)

			self.tlInfo = uiToolTip.ItemToolTip()
			self.tlInfo.Hide()
			self.tooltipInfo = [self.tlInfo] * 7
			self.InformationText = [
				localeInfo.MALZEME_DEPOSU, localeInfo.BK_ENVANTER_TEXT1,
				localeInfo.BK_ENVANTER_TEXT2, "",
				localeInfo.BK_ENVANTER_TEXT4, localeInfo.BK_ENVANTER_TEXT5, "",
			]
			TITLE_COLOR = grp.GenerateColor(0.9490, 0.9058, 0.7568, 1.0)
			for i in range(7):
				self.tooltipInfo[i].SetFollow(True)
				self.tooltipInfo[i].AlignHorizonalCenter()
				if i == 0:
					self.tooltipInfo[i].AutoAppendTextLine(self.InformationText[i], TITLE_COLOR)
				else:
					self.tooltipInfo[i].AutoAppendTextLine(self.InformationText[i])
				self.tooltipInfo[i].Hide()
				self.tooltipInfo[i].toolTipWidth += 10

		def __SetupEvents(self):
			m = ui.__mem_func__
			self.wndItem.SetSelectEmptySlotEvent(m(self.SelectEmptySlot))
			self.wndItem.SetSelectItemSlotEvent(m(self.SelectItemSlot))
			self.wndItem.SetUnselectItemSlotEvent(m(self.UseItemSlot))
			self.wndItem.SetUseSlotEvent(m(self.UseItemSlot))
			self.wndItem.SetOverInItemEvent(m(self.OverInItem))
			self.wndItem.SetOverOutItemEvent(m(self.OverOutItem))

			self.sortinv.SetEvent(m(self.sortInventory))
			self.packall.SetEvent(m(self.onclickpackall))
			self.SettingsButton.SetEvent(m(self.OpenSettings))

			self.OpenWithInventoryButton.SetToggleUpEvent(m(self.__OnClickEnableInventoryAutoOpen))
			self.OpenWithInventoryButton.SetToggleDownEvent(m(self.__OnClickEnableInventoryAutoOpen))
			self.OpenWhenFastMoveButton.SetToggleUpEvent(m(self.__OnClickEnableFastMoveOpen))
			self.OpenWhenFastMoveButton.SetToggleDownEvent(m(self.__OnClickEnableFastMoveOpen))
			self.DirectUseButton.SetToggleUpEvent(m(self.__OnClickEnableWpadanie))
			self.DirectUseButton.SetToggleDownEvent(m(self.__OnClickEnableWpadanie))
			self.window_settings.Hide()

			if settings.inventory_auto_open == 1:
				self.OpenWithInventoryButton.Down()
			if settings.enable_fast_open == 1:
				self.OpenWhenFastMoveButton.Down()
			if settings.extended_inventory_auto_use == 0:
				self.DirectUseButton.Down()

			for idx, btn in enumerate(self.typeButtons):
				btn.SetEvent(lambda arg=idx: self.SetInventoryType(arg))
			self.typeButtons[0].Down()

			for idx, tab in enumerate(self.inventoryTab):
				tab.SetEvent(lambda arg=idx: self.SetInventoryPage(arg))
			self.inventoryTab[0].Down()

			self._buttonTooltipMap = (
				(self.SkillBookButton, 3), (self.UpgradeItemsButton, 4),
				(self.stoneButton, 5), (self.boxButton, 6),
				(self.efsunButton, 7), (self.cicekButton, 8),
				(self.DirectUseButton, 10), (self.OpenWithInventoryButton, 9),
				(self.OpenWhenFastMoveButton, 11), (self.sortinv, 1), (self.packall, 12),
			)

		def __SetupDialogs(self):
			self.dlgPickMoney = uiPickMoney.PickMoneyDialog()
			self.dlgPickMoney.LoadDialog()
			self.dlgPickMoney.Hide()

			self.dlgPickItem = uiPickETC.PickETCDialog()
			self.dlgPickItem.LoadDialog()
			self.dlgPickItem.Hide()
			
		def Destroy(self):
			self.ClearDictionary()
			self.dlgPickMoney.Destroy()
			self.dlgPickItem.Destroy()
			self.dlgPickItem = 0
			self.dlgPickMoney = 0
			self.tooltipItem = None
			self.wndItem = 0
			self.interface = None
			self.inventoryTab = []

		def __ToggleSetting(self, attr, msg_off, msg_on):
			cur = getattr(settings, attr)
			setattr(settings, attr, 1 - cur)
			chat.AppendChat(chat.CHAT_TYPE_INFO, msg_off if cur else msg_on)

		def __OnClickEnableInventoryAutoOpen(self):
			self.__ToggleSetting("inventory_auto_open", localeInfo.INVENTORY_OPEN_WITH_INVENTORY_1, localeInfo.INVENTORY_OPEN_WITH_INVENTORY_2)

		def __OnClickEnableFastMoveOpen(self):
			self.__ToggleSetting("enable_fast_open", localeInfo.INVENTORY_OPENING_WHILE_FAST_MOVING_1, localeInfo.INVENTORY_OPENING_WHILE_FAST_MOVING_2)

		def __OnClickEnableWpadanie(self):
			net.SendChatPacket("/extended_inventory_status")

		def OpenSettings(self):
			if self.window_settings.IsShow():
				self.window_settings.Hide()
			else:
				self.window_settings.Show()

		def sortInventory(self):
			if app.IsPressed(app.DIK_LSHIFT):
				net.SendChatPacket("/sort_special_inventory 6")
			else:
				net.SendChatPacket("/sort_special_inventory %d" % self.inventoryType)

		def GetEmptyItemPosPack(self, type, itemHeight, blocked_slots):
			start_val = start_val_table[type - 1]
			end_val = end_val_table[type - 1]
			GetBlockedSlots = lambda slot, size: [slot + (round * 3) for round in range(size)]
			free_slots = [
				slot for slot in range(start_val, end_val)
				if slot not in blocked_slots and
				all(e not in blocked_slots for e in GetBlockedSlots(slot, itemHeight))
			]
			return free_slots if free_slots else -1

		def onclickpackall(self):
			inventory_size = player.INVENTORY_PAGE_SIZE * player.INVENTORY_PAGE_COUNT
			blocked_slots = []

			for i in range(inventory_size):
				itemVnum = player.GetItemIndex(i)
				itemCount = player.GetItemCount(i)
				item.SelectItem(itemVnum)

				if item.GetSpecialInvType() != self.inventoryType + 1:
					continue

				(w, h) = item.GetItemSize()
				emptyInvenSlots = self.GetEmptyItemPosPack(self.inventoryType + 1, h, blocked_slots)
				if emptyInvenSlots == -1:
					continue

				self.__SendMoveItemPacket(i, emptyInvenSlots[0], itemCount)

				for round in range(h):
					blocked_slot = emptyInvenSlots[0] + (round * 3)
					if blocked_slot not in blocked_slots:
						blocked_slots.append(blocked_slot)

		def Hide(self):
			if self.tooltipItem:
				self.tooltipItem.HideToolTip()
				self.tlInfo.Hide()
			if self.dlgPickItem:
				self.dlgPickItem.Close()
			wndMgr.Hide(self.hWnd)
			
		def Close(self):
			constInfo.EXTENDED_INVENTORY_IS_OPEN = 0
			for i in range(1, 13):
				self.tt[i].Hide()
			if self.tooltipItem:
				self.tooltipItem.HideToolTip()
			self.tlInfo.Hide()
			self.Hide()


		def SetInventoryType(self, type):
			self.inventoryType = type
			for i, btn in enumerate(self.typeButtons):
				if i == type:
					btn.Down()
				else:
					btn.SetUp()
			self.titleName.SetText(self.TYPE_TITLES[type])
			self.RefreshBagSlotWindow()
			
		def SetInventoryPage(self, page):
			self.inventoryPageIndex = page
			for tab in self.inventoryTab:
				tab.SetUp()
			self.inventoryTab[page].Down()
			self.RefreshBagSlotWindow()

		def OnPickItem(self, count):
			itemSlotIndex = self.dlgPickItem.itemGlobalSlotIndex
			if app.ENABLE_OFFLINE_SHOP:
				if uiOfflineShop.IsBuildingShop() and uiOfflineShop.IsSaleSlot(player.INVENTORY, itemSlotIndex):
					chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.CANNOT_DOING_PRIVATE_SHOP_OPEN)
					return
			selectedItemVNum = player.GetItemIndex(itemSlotIndex)
			_, _, slotType = self.INVENTORY_TYPE_CONFIG[self.inventoryType]
			mouseModule.mouseController.AttachObject(self, slotType, itemSlotIndex, selectedItemVNum, count)

		if app.ENABLE_EXTENDED_BLEND:
			def __CanAttachThisItem(self, itemVNum, itemSlotIndex):
				if constInfo.IS_PERMANANET_BLEND_ITEM(itemVNum):
					isActivated = player.GetItemMetinSocket(itemSlotIndex, 1)
					if isActivated == 1:
						return False


				return True
				

		def MouseSlotEventRefresh(self):
			for i in range(self.wndItem.GetSlotCount()):
				slotNumber = self.__InventoryLocalSlotPosToGlobalSlotPos(i)
				if slotNumber in self.listCantMouseSlot:
					itemInvenPage = slotNumber // player.INVENTORY_PAGE_SIZE
					localSlotPos = slotNumber - (itemInvenPage * player.INVENTORY_PAGE_SIZE)
	
					self.wndItem.SetCantMouseEventSlot(localSlotPos)
					self.wndItem.RefreshSlot()
	
		def MouseSlotEventClear(self):
			for i in range(self.wndItem.GetSlotCount()):
				slotNumber = self.__InventoryLocalSlotPosToGlobalSlotPos(i)
				if slotNumber in self.listCantMouseSlot:
					self.wndItem.SetCanMouseEventSlot(i)
					self.listCantMouseSlot.remove(slotNumber)
	
		def SetCantMouseSlot(self, slot):
			if slot > player.INVENTORY_PAGE_SIZE * player.INVENTORY_PAGE_COUNT:
				return
	
			if not slot in self.listCantMouseSlot:
				self.listCantMouseSlot.append(slot)
	
		def SetCanMouseSlot(self, inventorylocalslot):
			if inventorylocalslot in self.listCantMouseSlot:
				if inventorylocalslot >= player.INVENTORY_PAGE_SIZE*self.inventoryPageIndex:
					self.wndItem.SetCanMouseEventSlot(inventorylocalslot-player.INVENTORY_PAGE_SIZE*self.inventoryPageIndex)
				else:
					self.wndItem.SetCanMouseEventSlot(inventorylocalslot)
	
				self.listCantMouseSlot.remove(inventorylocalslot)
				
		def __InventoryLocalSlotPosToGlobalSlotPos(self, local):
			if 0 <= self.inventoryType < len(self.INVENTORY_TYPE_CONFIG):
				slotCount, slotStart, _ = self.INVENTORY_TYPE_CONFIG[self.inventoryType]
				return int(self.PAGE_MULTIPLIERS[self.inventoryPageIndex] * slotCount + local + slotStart)

			if player.IsSkillBookInventorySlot(local) or player.IsUpgradeItemsInventorySlot(local) or player.IsStoneInventorySlot(local) or player.IsBoxInventorySlot(local) or player.IsEfsunInventorySlot(local) or player.IsCicekInventorySlot(local):
				return local

		def GetInventoryPageIndex(self):
			return self.inventoryPageIndex
			
		def __ApplySlotEffects(self, localSlot, globalSlot, itemVnum):
			if constInfo.IS_BLEND_ITEM(itemVnum):
				isActivated = player.GetItemMetinSocket(globalSlot, 1) != 0
				if isActivated:
					self.wndItem.ActivateSlot(localSlot)
				else:
					self.wndItem.DeactivateSlot(localSlot)
			item.SelectItem(itemVnum)
			itemType = item.GetItemType()
			if itemType == item.TOGGLE:
				displaySlot = localSlot
				if self.inventoryPageIndex > 0:
					displaySlot = globalSlot % (player.INVENTORY_PAGE_SIZE * self.inventoryPageIndex)
				isActivated = player.GetItemMetinSocket(globalSlot, 3) != 0
				if isActivated:
					self.wndItem.ActivateSlot(displaySlot)
				else:
					self.wndItem.DeactivateSlot(displaySlot)
			if itemType == item.FISH:
				fishData = GetFishMissionData(itemVnum)
				if fishData and player.GetItemMetinSocket(globalSlot, 0) >= fishData[1] * 100:
					self.wndItem.SetFishAddonOnSlot(localSlot)

		def RefreshBagSlotWindow(self):
			getItemVNum=player.GetItemIndex
			getItemCount=player.GetItemCount
			setItemVNum=self.wndItem.SetItemSlot
			
			slotCount, slotStart, _ = self.INVENTORY_TYPE_CONFIG[self.inventoryType]
			pageOffset = self.PAGE_OFFSETS[self.GetInventoryPageIndex()]

			for i in range(slotCount):
				slotNumber = slotStart + i + pageOffset
				itemCount = getItemCount(slotNumber)
				if 0 == itemCount:
					self.wndItem.ClearSlot(i)
					continue
				elif 1 == itemCount:
					itemCount = 0
				itemVnum = getItemVNum(slotNumber)
				setItemVNum(i, itemVnum, itemCount)

			self.wndItem.RefreshSlot()	
			if app.ENABLE_HIGHLIGHT_NEW_ITEM:
				self.__RefreshHighlights()
				for i in range(135):
					slotNumber = self.__InventoryLocalSlotPosToGlobalSlotPos(i)
					if not slotNumber in self.liHighlightedItems:
						itemVnum = player.GetItemIndex(slotNumber)
						if not itemVnum:
							continue
						if constInfo.IS_AUTO_POTION(itemVnum) or constInfo.IS_BLEND_ITEM(itemVnum):
							continue
						try:
							item.SelectItem(itemVnum)
							if item.GetItemType() == item.TOGGLE:
								continue
						except:
							continue
						self.wndItem.DeactivateSlot(i)

			for i in range(135):
				slotNumber = self.__InventoryLocalSlotPosToGlobalSlotPos(i)
				itemVnum = getItemVNum(slotNumber)
				self.__ApplySlotEffects(i, slotNumber, itemVnum)

			if hasattr(constInfo, 'listRemoveItem') and constInfo.listRemoveItem:
				for i in range(135):
					slotNumber = self.__InventoryLocalSlotPosToGlobalSlotPos(i)
					if slotNumber in constInfo.listRemoveItem:
						self.wndItem.ActivateSlot(i, 1.0, 0.0, 0.0)

		if app.ENABLE_HIGHLIGHT_NEW_ITEM:
			def HighlightSlot(self, slot):
				if not slot in self.liHighlightedItems:
					self.liHighlightedItems.append(slot)

			def __RefreshHighlights(self):		
				for i in range(135):
					slotNumber = self.__InventoryLocalSlotPosToGlobalSlotPos(i)

					if slotNumber in self.liHighlightedItems:
						self.wndItem.ActivateSlot(i)

		def RefreshItemSlot(self):
			# Wolane z interfacemodule.RefreshInventory przy KAZDEJ zmianie ekwipunku (autoloot!).
			# RefreshBagSlotWindow to trzy petle po 135 slotow - czysto wizualne, wiec przy
			# ukrytym oknie nie ma czego odswiezac; stan odtwarzamy w Show().
			if not self.IsShow():
				return

			self.RefreshBagSlotWindow()

		def RefreshStatus(self):
			pass

		def SetItemToolTip(self, tooltipItem):
			self.tooltipItem = tooltipItem
			
		def SelectEmptySlot(self, selectedSlotPos):
			if constInfo.GET_ITEM_QUESTION_DIALOG_STATUS() == 1:
				return

			if constInfo.IS_BONUS_CHANGER:
				return

			selectedSlotPos = self.__LocalSlotToGlobal(selectedSlotPos)

			if mouseModule.mouseController.isAttached():
				attachedSlotType = mouseModule.mouseController.GetAttachedType()
				if player.SLOT_TYPE_DRAGON_SOUL_INVENTORY == attachedSlotType:
					mouseModule.mouseController.DeattachObject()
					return
				attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
				attachedItemCount = mouseModule.mouseController.GetAttachedItemCount()
				attachedItemIndex = mouseModule.mouseController.GetAttachedItemIndex()

				if app.ENABLE_OFFLINE_SHOP and uiOfflineShop.IsBuildingShop() and uiOfflineShop.IsSaleSlot(player.SlotTypeToInvenType(attachedSlotType), attachedSlotPos):
					chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.CANNOT_DOING_PRIVATE_SHOP_OPEN)
					return

				if attachedSlotType in INVENTORY_SLOT_TYPES:
					itemCount = player.GetItemCount(attachedSlotPos)
					attachedCount = mouseModule.mouseController.GetAttachedItemCount()

					if self.dlgPickItem and self.dlgPickItem.IsSplitAll():
						net.SendChatPacket("/split_items %d %d %d" % (attachedSlotPos, attachedCount, selectedSlotPos))
						self.dlgPickItem.SplitClear()
					else:
						self.__SendMoveItemPacket(attachedSlotPos, selectedSlotPos, attachedCount)

					if item.IsRefineScroll(attachedItemIndex):
						self.wndItem.SetUseMode(False)

				elif player.SLOT_TYPE_PRIVATE_SHOP == attachedSlotType:
					mouseModule.mouseController.RunCallBack("INVENTORY")

				elif player.SLOT_TYPE_BUFF_EQUIPMENT == attachedSlotType and app.ENABLE_ASLAN_BUFF_NPC_SYSTEM:
					attachedCount = mouseModule.mouseController.GetAttachedItemCount()
					net.SendItemMovePacket(player.BUFF_EQUIPMENT, attachedSlotPos, player.INVENTORY, selectedSlotPos, attachedCount)

				elif player.SLOT_TYPE_SHOP == attachedSlotType:
					net.SendShopBuyPacket(attachedSlotPos)

				elif player.SLOT_TYPE_SAFEBOX == attachedSlotType:

					if player.ITEM_MONEY == attachedItemIndex:
						net.SendSafeboxWithdrawMoneyPacket(mouseModule.mouseController.GetAttachedItemCount())
						snd.PlaySound("sound/ui/money.wav")

					else:
						net.SendSafeboxCheckoutPacket(attachedSlotPos, selectedSlotPos)

				elif player.SLOT_TYPE_MALL == attachedSlotType:
					net.SendMallCheckoutPacket(attachedSlotPos, selectedSlotPos)

				mouseModule.mouseController.DeattachObject()
				
		def IsChanger(self, itemVnum):
			if not itemVnum:
				return False
			return item.GetUseType(itemVnum) in CHANGER_USE_TYPES

		def SelectItemSlot(self, itemSlotIndex):
			if constInfo.GET_ITEM_QUESTION_DIALOG_STATUS() == 1:
				return

			if constInfo.IS_BONUS_CHANGER:
				return

			itemSlotIndex = self.__LocalSlotToGlobal(itemSlotIndex)

			if mouseModule.mouseController.isAttached():
				attachedSlotType = mouseModule.mouseController.GetAttachedType()
				attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
				attachedItemVID = mouseModule.mouseController.GetAttachedItemIndex()
				attachedItemCount = mouseModule.mouseController.GetAttachedItemCount()
				
				if self.IsChanger(attachedItemVID) and not player.IsEquipmentSlot(itemSlotIndex):
					itemVnum = player.GetItemIndex(itemSlotIndex)
					item.SelectItem(itemVnum)
					if item.GetItemType() == item.WEAPON or item.GetItemType() == item.ARMOR:
						self.interface.AddToBonusChange(itemSlotIndex, attachedSlotPos)
						mouseModule.mouseController.DeattachObject()
						return

				
				if attachedSlotType in INVENTORY_SLOT_TYPES:
					self.__SendMoveItemPacket(attachedSlotPos, itemSlotIndex, attachedItemCount)
		
				mouseModule.mouseController.DeattachObject()
			else:

				curCursorNum = app.GetCursor()
					
				if app.BUY == curCursorNum:
					chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.SHOP_BUY_INFO)

				elif app.IsPressed(app.DIK_LALT):
					link = player.GetItemLink(itemSlotIndex)
					ime.PasteString(link)

				elif app.IsPressed(app.DIK_LSHIFT):
					itemCount = player.GetItemCount(itemSlotIndex)
				
					if itemCount > 1:
						self.dlgPickItem.SetTitleName(localeInfo.PICK_ITEM_TITLE)
						self.dlgPickItem.SetAcceptEvent(ui.__mem_func__(self.OnPickItem))
						self.dlgPickItem.Open(itemCount)
						self.dlgPickItem.itemGlobalSlotIndex = itemSlotIndex

				elif app.IsPressed(app.DIK_LCONTROL):
					itemIndex = player.GetItemIndex(itemSlotIndex)

					if item.CanAddToQuickSlotItem(itemIndex):
						player.RequestAddToEmptyLocalQuickSlot(player.SLOT_TYPE_INVENTORY, itemSlotIndex)
					else:
						chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.QUICKSLOT_REGISTER_DISABLE_ITEM)
				else:

					selectedItemVNum = player.GetItemIndex(itemSlotIndex)
					itemCount = player.GetItemCount(itemSlotIndex)
					_, _, slotType = self.INVENTORY_TYPE_CONFIG[self.inventoryType]
					mouseModule.mouseController.AttachObject(self, slotType, itemSlotIndex, selectedItemVNum, itemCount)
					self.wndItem.SetUseMode(True)

					if app.ENABLE_EXTENDED_BLEND:
						if self.__CanAttachThisItem(selectedItemVNum, itemSlotIndex):
							mouseModule.mouseController.AttachObject(self, player.SLOT_TYPE_CICEK_INVENTORY, itemSlotIndex, selectedItemVNum, itemCount)

					snd.PlaySound("sound/ui/pick.wav")

		def OnCloseQuestionDialog(self):
			if not self.questionDialog:
				return
			
			self.questionDialog.Close()
			self.questionDialog = None
			constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(0)

		def Sat(self):
			if self.sellingSlotitemIndex == player.GetItemIndex(self.sellingSlotNumber):
				if self.sellingSlotitemCount == player.GetItemCount(self.sellingSlotNumber):
					net.SendShopSellPacketNew(self.sellingSlotNumber, self.questionDialog.count, player.INVENTORY)
					snd.PlaySound("sound/ui/money.wav")
			self.OnCloseQuestionDialog()
			
		def OverOutItem(self):
			self.wndItem.SetUsableItem(False)
			if self.tooltipItem:
				if self.__IsCursorOnInventorySlotWindow() and hasattr(self.tooltipItem, "HideToolTipWithoutModelPreview"):
					self.tooltipItem.HideToolTipWithoutModelPreview()
				else:
					self.tooltipItem.HideToolTip()

		def OverInItem(self, overSlotPos):
			self.wndItem.SetUsableItem(False)
			globalSlotPos = self.__InventoryLocalSlotPosToGlobalSlotPos(overSlotPos)
			self.ShowToolTip(globalSlotPos)

			if app.ENABLE_HIGHLIGHT_NEW_ITEM:
				if globalSlotPos in self.liHighlightedItems:
					self.liHighlightedItems.remove(globalSlotPos)
					self.wndItem.DeactivateSlot(overSlotPos)
			
		def ShowToolTip(self, slotIndex):
			if self.tooltipItem:
				self.tooltipItem.SetInventoryItem(slotIndex)
				if app.ENABLE_OFFLINE_SHOP:
					if uiOfflineShop.IsBuildingShop():
						self.__AddTooltipSaleMode(slotIndex)

		if app.ENABLE_OFFLINE_SHOP:
			def __AddTooltipSaleMode(self, slot):
				if player.IsEquipmentSlot(slot):
					return

				itemIndex = player.GetItemIndex(slot)
				if itemIndex !=0:
					item.SelectItem(itemIndex)
					if item.IsAntiFlag(item.ANTIFLAG_MYSHOP) or item.IsAntiFlag(item.ANTIFLAG_GIVE):
						return

					self.tooltipItem.AddRightClickForSale()

		def __IsCursorOnInventorySlotWindow(self):
			return self.wndItem and self.wndItem.IsIn()

		def OnPressEscapeKey(self):
			self.Close()
			return True	
		
		def GetEmptyItemPos(self, itemHeight):
			inventory_size = player.INVENTORY_PAGE_SIZE * player.INVENTORY_PAGE_COUNT
			COLS = 5
			blocked = set()
			for slot in range(inventory_size):
				if not player.isItem(slot):
					continue
				item.SelectItem(player.GetItemIndex(slot))
				_, h = item.GetItemSize()
				for row in range(h):
					blocked.add(slot + row * COLS)
			if itemHeight > 1:
				for div in range(1, 3):
					boundary = inventory_size // div
					for slot in range(boundary - (itemHeight - 1) * COLS, boundary):
						blocked.add(slot)
			free = [s for s in range(inventory_size)
				if s not in blocked and
				all(s + r * COLS not in blocked for r in range(itemHeight))]
			return free if free else -1

		def UseItemSlot(self, slotIndex):
			if constInfo.GET_ITEM_QUESTION_DIALOG_STATUS():
				return

			globalSlot = self.__InventoryLocalSlotPosToGlobalSlotPos(slotIndex)
			itemVnum1 = player.GetItemIndex(globalSlot)
			item.SelectItem(itemVnum1)

			# Ctrl+PPM: gdy magazyn otwarty, wrzuc item do magazynu
			if app.IsPressed(app.DIK_LCONTROL) and itemVnum1 != 0 and self.interface:
				wndSafebox = getattr(self.interface, "wndSafebox", None)
				if wndSafebox and wndSafebox.IsShow():
					if item.IsAntiFlag(item.ANTIFLAG_SAFEBOX):
						chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.SAFEBOX_CANNOT_DEPOSIT)
						return
					(w, h) = item.GetItemSize()
					if h <= 0:
						h = 1
					sbSize = safebox.GetCurrentSafeboxSize()
					sbPageSize = safebox.SAFEBOX_PAGE_SIZE
					sbRowWidth = safebox.SAFEBOX_SLOT_X_COUNT
					sbPageCount = max(1, sbSize // sbPageSize)
					# Budujemy mape zajetosci safeboxa (uwzgledniajac wysokosc itemow)
					sbGrid = [[False for _ in range(sbPageSize)] for _ in range(sbPageCount)]
					for pg in range(sbPageCount):
						for sl in range(sbPageSize):
							idx = pg * sbPageSize + sl
							if idx >= sbSize:
								continue
							occVnum = safebox.GetItemID(idx)
							if occVnum != 0:
								item.SelectItem(occVnum)
								(ow, oh) = item.GetItemSize()
								if oh <= 0:
									oh = 1
								for dy in range(oh):
									s = sl + dy * sbRowWidth
									if s < sbPageSize:
										sbGrid[pg][s] = True
					item.SelectItem(itemVnum1)
					freeSafeboxSlot = -1
					for page in range(sbPageCount):
						for slot in range(sbPageSize):
							fits = True
							for dy in range(h):
								checkLocal = slot + dy * sbRowWidth
								if checkLocal >= sbPageSize or sbGrid[page][checkLocal]:
									fits = False
									break
							if fits:
								freeSafeboxSlot = page * sbPageSize + slot
								break
						if freeSafeboxSlot != -1:
							break
					if freeSafeboxSlot != -1:
						net.SendSafeboxCheckinPacket(player.INVENTORY, globalSlot, freeSafeboxSlot)
					else:
						chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.SAFEBOX_FULL)
					return

			if item.CanUseInSpecialInv() == 1:
				self.__UseItem(globalSlot)
				return

			if app.ENABLE_OFFLINE_SHOP:
				if uiOfflineShop.IsBuildingShop():
					itemIndex = player.GetItemIndex(globalSlot)
					item.SelectItem(itemIndex)

					if app.IsPressed(app.DIK_LCONTROL):
						if not item.IsAntiFlag(item.ANTIFLAG_GIVE) and not item.IsAntiFlag(item.ANTIFLAG_MYSHOP):
							self.interface.wndShopOffline.SetFastAddItem(True)
							offlineshop.ShopBuilding_AddItem(player.INVENTORY, globalSlot)
						else:
							chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.CANNOT_DOING_PRIVATE_SHOP_OPEN)
						return
					else:
						if not item.IsAntiFlag(item.ANTIFLAG_MYSHOP):
							offlineshop.ShopBuilding_AddItem(player.INVENTORY, globalSlot)
						else:
							chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.CANNOT_DOING_PRIVATE_SHOP_OPEN)
						return

			if not app.IsPressed(app.DIK_LSHIFT):
				if not app.IsPressed(app.DIK_LCONTROL):
					if mouseModule.mouseController.isAttached():
						mouseModule.mouseController.DeattachObject()

					itemCount = player.GetItemCount(globalSlot)
					item.SelectItem(itemVnum1)
					(w, h) = item.GetItemSize()
					emptyInvenSlots = self.GetEmptyItemPos(h)
					if emptyInvenSlots == -1:
						return
					self.__SendMoveItemPacket(globalSlot, emptyInvenSlots[0], itemCount)

			if constInfo.IS_BONUS_CHANGER:
				return

			slotIndex = self.__LocalSlotToGlobal(slotIndex)

			if app.IsPressed(app.DIK_LSHIFT) and self.interface.wndRemoveItem.IsShow():
				self.interface.wndRemoveItem.AppendSlot(player.INVENTORY, slotIndex)
				return

			if app.ENABLE_ODLAMKI_SYSTEM:
				if app.IsPressed(app.DIK_LSHIFT) and self.interface.wndFragments.IsShow():
					itemType = item.GetItemType()
					if not item.METIN == itemType:
						chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.INVENTORY_SOUL_STONE_ONLY)
						return
					else:
						self.interface.wndFragments.AppendSlot(player.INVENTORY, slotIndex)
						return

			if app.IsPressed(app.DIK_LCONTROL) and app.IsPressed(app.DIK_X):
				shopSearch = self.interface.GetShopSearchWindow()
				if not shopSearch:
					return
				if not shopSearch.IsShow():
					shopSearch.Show(True)
				item.SelectItem(itemVnum1)
				shopSearch.sItemName.SetText(item.GetItemName())
				shopSearch.OnSearch()

				self.__UseItem(slotIndex)
				mouseModule.mouseController.DeattachObject()
				self.OverOutItem()

		def __UseItem(self, slotIndex):
			if app.ENABLE_OFFLINE_SHOP and uiOfflineShop.IsBuildingShop() and uiOfflineShop.IsSaleSlot(player.INVENTORY, slotIndex):
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.CANNOT_DOING_PRIVATE_SHOP_OPEN)
				return
			ItemVNum = player.GetItemIndex(slotIndex)

			getItemCount=player.GetItemCount
			itemCount = getItemCount(slotIndex)

			item.SelectItem(ItemVNum)

			if item.IsFlag(item.ITEM_FLAG_CONFIRM_WHEN_USE):
				self.questionDialog = uiCommon.QuestionDialog()
				self.questionDialog.SetText(localeInfo.INVENTORY_REALLY_USE_ITEM)
				self.questionDialog.SetAcceptEvent(ui.__mem_func__(self.__UseItemQuestionDialog_OnAccept))
				self.questionDialog.SetCancelEvent(ui.__mem_func__(self.__UseItemQuestionDialog_OnCancel))
				self.questionDialog.Open()
				self.questionDialog.slotIndex = slotIndex

				constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(1)
				# Patrz InventoryWindow.__UseItem - bez return pakiet uzycia szedl przed
				# potwierdzeniem, a klikniecie "Tak" wysylalo go po raz drugi.
				return

			if app.ENABLE_INSTANT_CHEST_OPEN:
				if (item.GetItemType() == item.GIFTBOX) or (item.GetItemType() == item.GACHA):
					if app.IsPressed(app.DIK_LALT) and not app.IsPressed(app.DIK_LCONTROL):
						itemUseCount = player.GetItemCount(slotIndex) if player.GetItemCount(slotIndex) <= INSTANT_OPEN_COUNT else INSTANT_OPEN_COUNT
						net.SendOpenChestPacket(slotIndex, itemUseCount)
						return

			# Ctrl+PPM = podglad dropu skrzyni (Ctrl+Shift = lista dodatkowa), item sie NIE uzywa.
			if app.__BL_CHEST_DROP_INFO__ and app.IsPressed(app.DIK_LCONTROL):
				isMain = not app.IsPressed(app.DIK_LSHIFT)
				if item.HasDropInfo(ItemVNum, isMain) and self.interface:
					self.interface.OpenChestDropWindow(ItemVNum, isMain)
				return

			# Wysylka poza warunkiem __BL_CHEST_DROP_INFO__ - patrz InventoryWindow.__UseItem.
			self.__SendUseItemPacket(slotIndex)

		def __UseItemQuestionDialog_OnCancel(self):
			self.OnCloseQuestionDialog()

		def __UseItemQuestionDialog_OnAccept(self):
			self.__SendUseItemPacket(self.questionDialog.slotIndex)
			self.OnCloseQuestionDialog()	
			
		def __SendUseItemPacket(self, slotPos):
			if uiPrivateShopBuilder.IsBuildingPrivateShop():
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.USE_ITEM_FAILURE_PRIVATE_SHOP)
				return
				
			if self.interface.wndRemoveItem.IsShow():
				return

			if app.ENABLE_ODLAMKI_SYSTEM:
				if self.interface.wndFragments.IsShow():
					return

			net.SendItemUsePacket(slotPos)

		def __SendMoveItemPacket(self, srcSlotPos, dstSlotPos, srcItemCount):
			if uiPrivateShopBuilder.IsBuildingPrivateShop():
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.MOVE_ITEM_FAILURE_PRIVATE_SHOP)
				return
			if app.ENABLE_OFFLINE_SHOP:
				if uiOfflineShop.IsBuildingShop():
					chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.CANNOT_DOING_PRIVATE_SHOP_OPEN)
					return
			net.SendItemMovePacket(srcSlotPos, dstSlotPos, srcItemCount)

		def OnUpdate(self):
			if settings.extended_inventory_auto_use == 0:
				self.DirectUseButton.Down()
			else:
				self.DirectUseButton.SetUp()

			for i in range(1, 13):
				self.tt[i].Hide()

			for btn, ttIdx in self._buttonTooltipMap:
				if btn.IsIn():
					self.tt[ttIdx].Show()

class BeltInventoryWindow(ui.ScriptWindow):

	def __init__(self, wndInventory):
		import exception

		if not app.ENABLE_NEW_EQUIPMENT_SYSTEM:
			exception.Abort("What do you do?")
			return

		if not wndInventory:
			exception.Abort("wndInventory parameter must be set to InventoryWindow")
			return

		ui.ScriptWindow.__init__(self)

		self.isLoaded = 0
		self.wndInventory = wndInventory;

		self.ltInventoryLayer = None
		self.wndBeltInventorySlot = None
		self.expandBtn = None
		self.minBtn = None

		self.__LoadWindow()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def Show(self, openBeltSlot = False):
		self.__LoadWindow()
		self.RefreshSlot()

		ui.ScriptWindow.Show(self)

		if openBeltSlot:
			self.OpenInventory()
		else:
			self.CloseInventory()

	def Close(self):
		self.Hide()

	def IsOpeningInventory(self):
		return self.wndBeltInventoryLayer.IsShow()

	def OpenInventory(self):
		self.wndBeltInventoryLayer.Show()
		self.expandBtn.Hide()

		self.AdjustPositionAndSize()

	def CloseInventory(self):
		self.wndBeltInventoryLayer.Hide()
		self.expandBtn.Show()

		self.AdjustPositionAndSize()

	def GetBasePosition(self):
		x, y = self.wndInventory.GetGlobalPosition()
		return x - 148, y + 241

	def AdjustPositionAndSize(self):
		bx, by = self.GetBasePosition()

		if self.IsOpeningInventory():
			self.SetPosition(bx, by)
			self.SetSize(self.ORIGINAL_WIDTH, self.GetHeight())

		else:
			self.SetPosition(bx + 138, by);
			self.SetSize(10, self.GetHeight())

	def __LoadWindow(self):
		if self.isLoaded == 1:
			return

		self.isLoaded = 1

		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "UIScript/BeltInventoryWindow.py")
		except:
			import exception
			exception.Abort("CostumeWindow.LoadWindow.LoadObject")

		try:
			self.ORIGINAL_WIDTH = self.GetWidth()
			wndBeltInventorySlot = self.GetChild("BeltInventorySlot")
			self.wndBeltInventoryLayer = self.GetChild("BeltInventoryLayer")
			self.expandBtn = self.GetChild("ExpandBtn")
			self.minBtn = self.GetChild("MinimizeBtn")

			self.expandBtn.SetEvent(ui.__mem_func__(self.OpenInventory))
			self.minBtn.SetEvent(ui.__mem_func__(self.CloseInventory))

			for i in range(item.BELT_INVENTORY_SLOT_COUNT):
				slotNumber = item.BELT_INVENTORY_SLOT_START + i
				wndBeltInventorySlot.SetCoverButton(slotNumber,	"d:/ymir work/ui/game/quest/slot_button_01.sub",\
												"d:/ymir work/ui/game/quest/slot_button_01.sub",\
												"d:/ymir work/ui/game/quest/slot_button_01.sub",\
												"d:/ymir work/ui/game/belt_inventory/slot_disabled.tga", False, False)

		except:
			import exception
			exception.Abort("CostumeWindow.LoadWindow.BindObject")

		wndBeltInventorySlot.SetOverInItemEvent(ui.__mem_func__(self.wndInventory.OverInItem))
		wndBeltInventorySlot.SetOverOutItemEvent(ui.__mem_func__(self.wndInventory.OverOutItem))
		wndBeltInventorySlot.SetUnselectItemSlotEvent(ui.__mem_func__(self.wndInventory.UseItemSlot))
		wndBeltInventorySlot.SetUseSlotEvent(ui.__mem_func__(self.wndInventory.UseItemSlot))
		wndBeltInventorySlot.SetSelectEmptySlotEvent(ui.__mem_func__(self.wndInventory.SelectEmptySlot))
		wndBeltInventorySlot.SetSelectItemSlotEvent(ui.__mem_func__(self.wndInventory.SelectItemSlot))

		self.wndBeltInventorySlot = wndBeltInventorySlot

	def RefreshSlot(self):
		getItemVNum=player.GetItemIndex

		for i in range(item.BELT_INVENTORY_SLOT_COUNT):
			slotNumber = item.BELT_INVENTORY_SLOT_START + i
			self.wndBeltInventorySlot.SetItemSlot(slotNumber, getItemVNum(slotNumber), player.GetItemCount(slotNumber))
			self.wndBeltInventorySlot.SetAlwaysRenderCoverButton(slotNumber, True)

			avail = "0"

			if player.IsAvailableBeltInventoryCell(slotNumber):
				self.wndBeltInventorySlot.EnableCoverButton(slotNumber)
			else:
				self.wndBeltInventorySlot.DisableCoverButton(slotNumber)

		self.wndBeltInventorySlot.RefreshSlot()


class InventoryWindow(ui.ScriptWindow):

	USE_TYPE_TUPLE = ("USE_CLEAN_SOCKET", "USE_CHANGE_ATTRIBUTE", "USE_ADD_ATTRIBUTE", "USE_ADD_ATTRIBUTE2", "USE_ADD_ACCESSORY_SOCKET", "USE_PUT_INTO_ACCESSORY_SOCKET", "USE_PUT_INTO_BELT_SOCKET", "USE_PUT_INTO_RING_SOCKET", "USE_ADD_ATTRIBUTE_SPECIAL_1", "USE_ADD_IS_BONUS", "USE_ADD_NEW_BONUS", "USE_ADD_EXTRA_BONUS", "USE_FISHING_ROD_ADD_ATTRIBUTE")
	if app.ENABLE_USE_COSTUME_ATTR:
		USE_TYPE_TUPLE = tuple(list(USE_TYPE_TUPLE) + ["USE_CHANGE_COSTUME_ATTR", "USE_RESET_COSTUME_ATTR"])
	USE_TYPE_TUPLE = USE_TYPE_TUPLE + ("USE_ALCHEMY_CHANGER",)
	USE_TYPE_TUPLE = USE_TYPE_TUPLE + ("USE_SASH_CLEANER",)

	questionDialog = None
	tooltipItem = None
	wndCostume = None
	if app.ENABLE_NEW_STONE_DETACH:
		wndStoneDetach = None
	wndBelt = None
	dlgPickMoney = None
	interface = None
	if app.WJ_ENABLE_TRADABLE_ICON:
		bindWnds = []
	dlgPickItem = None
	if app.ENABLE_CHEQUE_SYSTEM:
		dlgPickETC = None
	wndSystemsWindow = None

	sellingSlotNumber = -1
	isLoaded = 0
	isOpenedCostumeWindowWhenClosingInventory = 0
	isOpenedBeltWindowWhenClosingInventory = 0

	if app.ENABLE_HIGHLIGHT_NEW_ITEM:
		liHighlightedItems = []

	if app.ENABLE_PREMIUM_PRIVATE_SHOP_OFFICIAL:
		wndPrivateShop			= None
		wndPrivateShopSearch	= None

	def __init__(self):
		ui.ScriptWindow.__init__(self)

		self.isOpenedBeltWindowWhenClosingInventory = 0

		self.inventoryPageIndex = 0
		self.wndDeposit = uiDeposit.DepositWindow()

		if constInfo.ENABLE_EXPANDED_MONEY_TASKBAR:
			self.wndExpandedMoneyBar = None
			self.wndPktOsiag = None

		if app.ENABLE_ACCE_COSTUME_SYSTEM:
			self.wndAcceCombine = None
			self.wndAcceAbsorption = None

		self.__LoadWindow()

	def __del__(self):
		ui.ScriptWindow.__del__(self)
		if constInfo.ENABLE_EXPANDED_MONEY_TASKBAR:
			self.wndExpandedMoneyBar = None
			self.wndPktOsiag = None
   
	def ToggleMap(self):
		self.interface.ToggleMapWindow()
		
	def ToggleLokalizacja(self):
		self.interface.ToggleSaveLocationWindow()
		
	def OpenPrivateShopBuilder(self):
		if hasattr(self.interface, 'wndShopOffline') and self.interface.wndShopOffline:
			if self.interface.wndShopOffline.IsShow():
				self.interface.wndShopOffline.Close()
			else:
				net.SendChatPacket("/open_offlineshop")
		else:
			net.SendChatPacket("/open_offlineshop")

	def ToggleWspomagacze(self):
		self.interface.OpenBlendWindow()

	def ToggleAntyExp(self):
		net.SendChatPacket("/toggle_antyexp")

	def ToggleDodatkowy(self):
		self.interface.ToggleExtendedInventoryWindow()

	def TogglePet(self):
		self.interface.pet_window_open()

	def ToggleRanking(self):
		self.interface.ToggleWeeklyRankWindow()

	def ToggleSwitcher(self):
		self.interface.ToggleSwitchbotWindow()

	def ToggleSearchShop(self):
		shopSearch = self.interface.GetShopSearchWindow()
		if shopSearch:
			if not shopSearch.IsShow():
				shopSearch.Show()
			else:
				shopSearch.Close()

	def ToggleBonus(self):
		self.interface.ToggleBonusWindow()

	def ToggleKosz(self):
		self.interface.OpenRemoveItem(self.interface.wndInventory)

	def ToggleShaman(self):
		self.interface.BuffNPCOpenWindow()

	if app.ENABLE_HIDE_COSTUME_SYSTEM:
		def RefreshVisibleCostume(self):
			if self.wndCostume:
				self.wndCostume.RefreshVisibleCostume()
			else:
				self.wndCostume = CostumeWindow(self)
				self.wndCostume.RefreshVisibleCostume()

	def ToggleArtifact(self):
		self.interface.OpenArtifactWindow()

	def ToggleCollectWindow(self):
		net.SendChatPacket("/collect_window")

	def ToggleTpMetkiBossy(self):
		self.interface.OpenRespWindow()

	def ToggleMount(self):
		wnd = getattr(self.interface, 'wndCompanionWindow', None)
		if wnd:
			if wnd.IsShow():
				wnd.Close()
			else:
				wnd.Open()
				wnd.SwitchToMountMode()
		elif hasattr(self.interface, 'wndMountWindow') and self.interface.wndMountWindow:
			self.interface.wndMountWindow.Open()

	def ToggleDungeon(self):
		self.interface.ToggleDungeonTrackWindow()

	def ToggleDeposit(self):
		if self.wndDeposit.IsShow():
			self.wndDeposit.Close()
		else:
			self.wndDeposit.Open()
		
	def Show(self):
		global SYSTEMS_WINDOW
		self.__LoadWindow()

		ui.ScriptWindow.Show(self)
		constInfo.SYSTEMS_WINDOW_CLOSE=0
		self.wndSystemsWindow.Show(1)

		if self.isOpenedCostumeWindowWhenClosingInventory and self.wndCostume:
			self.wndCostume.Show()


	def BindInterfaceClass(self, interface):
		self.interface = interface

	if app.WJ_ENABLE_TRADABLE_ICON:
		def BindWindow(self, wnd):
			self.bindWnds.append(wnd)

	def __LoadWindow(self):
		global SYSTEMS_WINDOW
		if self.isLoaded == 1:
			return

		self.isLoaded = 1
		tooltip = uiToolTip.ToolTip()
		self.toolTip = tooltip
		self.wndSystemsWindow = SystemsWindow(self,tooltip)

		try:
			pyScrLoader = ui.PythonScriptLoader()

			if app.ENABLE_EXTEND_INVEN_SYSTEM:
				pyScrLoader.LoadScriptFile(self, "UIScript/InventoryWindowEx.py")
			else:
				if ITEM_MALL_BUTTON_ENABLE:
					pyScrLoader.LoadScriptFile(self, "uiscript/inventorywindow.py")
				else:
					pyScrLoader.LoadScriptFile(self, "UIScript/InventoryWindow.py")
		except:
			import exception
			exception.Abort("InventoryWindow.LoadWindow.LoadObject")

		try:
			wndItem = self.GetChild("ItemSlot")
			wndEquip = self.GetChild("EquipmentSlot")
			self.GetChild("TitleBar").SetCloseEvent(ui.__mem_func__(self.Close))
			self.wndMoney = self.GetChild("Money")
			self.wndMoneySlot = self.GetChild("Money_Slot")
			self.DSSButton = self.GetChild2("DSSButton")
			self.costumeButton = self.GetChild2("CostumeButton")
			self.MallButton = self.GetChild2("MallButton")
			self.refreshbutton = self.GetChild2("RefreshButton")

			if app.ENABLE_CHEQUE_SYSTEM:
				self.wndCheque = self.GetChild("Cheque")
				self.wndChequeSlot = self.GetChild("Cheque_Slot")
				self.wndChequeIcon = self.GetChild("Cheque_Icon")

			if app.ENABLE_PUNKTY_OSIAGNIEC:
				self.wndPktOsiag = self.GetChild("Pkt_Osiag")
				self.wndPktOsiagSlot = self.GetChild("Pkt_Osiag_Slot")
				self.wndPktOsiagIcon = self.GetChild("Pkt_Osiag_Icon")

			self.wndMoneyIcon = self.GetChild("Money_Icon")
			self.wndMoneyIcon.Hide()
			self.wndMoneySlot.Hide()
			self.wndChequeIcon.Hide()
			self.wndChequeSlot.Hide()
			self.wndPktOsiag.Hide()
			self.wndPktOsiagSlot.Hide()
			self.wndPktOsiagIcon.Hide()

			self.listCantMouseSlot = []
			height = self.GetHeight()
			width = self.GetWidth()
			self.SetSize(width, height - 39)
			self.GetChild("board").SetSize(width, height - 39)

			self.inventoryTab = []
			for i in range(player.INVENTORY_PAGE_COUNT):
				self.inventoryTab.append(self.GetChild("Inventory_Tab_%02d" % (i+1)))

			self.equipmentTab = []
			self.equipmentTab.append(self.GetChild("Equipment_Tab_01"))
			self.equipmentTab.append(self.GetChild("Equipment_Tab_02"))

			if self.costumeButton and not app.ENABLE_COSTUME_SYSTEM:
				self.costumeButton.Hide()
				self.costumeButton.Destroy()
				self.costumeButton = 0



		except:
			import exception
			exception.Abort("InventoryWindow.LoadWindow.BindObject")

		wndItem.SetSelectEmptySlotEvent(ui.__mem_func__(self.SelectEmptySlot))
		wndItem.SetSelectItemSlotEvent(ui.__mem_func__(self.SelectItemSlot))
		wndItem.SetUnselectItemSlotEvent(ui.__mem_func__(self.UseItemSlot))
		wndItem.SetUseSlotEvent(ui.__mem_func__(self.UseItemSlot))
		wndItem.SetOverInItemEvent(ui.__mem_func__(self.OverInItem))
		wndItem.SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))

		wndEquip.SetSelectEmptySlotEvent(ui.__mem_func__(self.SelectEmptySlot))
		wndEquip.SetSelectItemSlotEvent(ui.__mem_func__(self.SelectItemSlot))
		wndEquip.SetUnselectItemSlotEvent(ui.__mem_func__(self.UseItemSlot))
		wndEquip.SetUseSlotEvent(ui.__mem_func__(self.UseItemSlot))
		wndEquip.SetOverInItemEvent(ui.__mem_func__(self.OverInItem))
		wndEquip.SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))

		dlgPickMoney = uiPickMoney.PickMoneyDialog()
		dlgPickMoney.LoadDialog()
		dlgPickMoney.Hide()

		dlgPickItem = uiPickETC.PickETCDialog()
		dlgPickItem.LoadDialog()
		dlgPickItem.Hide()

		self.refineDialog = uiRefine.RefineDialog()
		self.refineDialog.Hide()

		if app.ENABLE_CHEQUE_SYSTEM:
			dlgPickETC = uiPickETC.PickETCDialog()
			dlgPickETC.LoadDialog()
			dlgPickETC.Hide()

		if app.WJ_ENABLE_TRADABLE_ICON:  
			self.attachMetinDialog = uiAttachMetin.AttachMetinDialog(self)
			self.BindWindow(self.attachMetinDialog)
		else:
			self.attachMetinDialog = uiAttachMetin.AttachMetinDialog()
		self.attachMetinDialog.Hide()
		

		self.refreshbutton.SetEvent(ui.__mem_func__(self.StackItem))

		for i in range(player.INVENTORY_PAGE_COUNT):
			self.inventoryTab[i].SetEvent(lambda arg=i: self.SetInventoryPage(arg))
		self.inventoryTab[0].Down()

		self.equipmentTab[0].SetEvent(lambda arg=0: self.SetEquipmentPage(arg))
		self.equipmentTab[1].SetEvent(lambda arg=1: self.SetEquipmentPage(arg))
		self.equipmentTab[0].Down()
		self.equipmentTab[0].Hide()
		self.equipmentTab[1].Hide()

		self.wndItem = wndItem
		self.wndEquip = wndEquip
		self.dlgPickMoney = dlgPickMoney
		self.dlgPickItem = dlgPickItem

		if app.ENABLE_CHEQUE_SYSTEM:
			self.dlgPickETC = dlgPickETC


		if self.DSSButton:
			self.DSSButton.SetEvent(ui.__mem_func__(self.ClickDSSButton))

		if self.costumeButton:
			self.costumeButton.SetEvent(ui.__mem_func__(self.ClickCostumeButton))

		if self.MallButton:
			self.MallButton.SetEvent(ui.__mem_func__(self.ToggleDeposit))

		self.wndCostume = None

		if app.ENABLE_ACCE_COSTUME_SYSTEM:
			self.listAttachedAcces = []
		if app.ENABLE_AURA_SYSTEM:
			self.listAttachedAuras = []
		self.SetInventoryPage(0)
		self.SetEquipmentPage(0)
		self.RefreshItemSlot()
		self.RefreshStatus()

		self.SetTop()



	def Destroy(self):
		self.ClearDictionary()

		self.dlgPickMoney.Destroy()
		self.dlgPickMoney = 0

		if app.ENABLE_CHEQUE_SYSTEM:
			self.dlgPickETC.Destroy()
			self.dlgPickETC = 0
		
		if app.ENABLE_PUNKTY_OSIAGNIEC:
			self.wndPktOsiag = 0

		self.refineDialog.Destroy()
		self.refineDialog = 0


		self.attachMetinDialog.Destroy()
		self.attachMetinDialog = 0

		self.tooltipItem = None
		self.wndItem = 0
		self.wndEquip = 0
		self.dlgPickMoney = 0
		self.wndMoney = 0
		self.wndMoneySlot = 0
		self.dlgPickItem.Destroy()
		self.dlgPickItem = 0
		if app.ENABLE_CHEQUE_SYSTEM:
			self.wndCheque = 0
			self.wndChequeSlot = 0
			self.dlgPickETC = 0
		self.questionDialog = None
		self.DSSButton = None
		self.MallButton = None
		self.DSSButtonEffect = None
		if app.ENABLE_OFFLINE_SHOP:
			self.offlineShopNotificationEffect = None
		self.interface = None
		if app.WJ_ENABLE_TRADABLE_ICON:
			self.bindWnds = []

		if self.wndCostume:
			self.wndCostume.Destroy()
			self.wndCostume = 0


		self.wndSystemsWindow.Destroy()
		self.wndSystemsWindow=None

		if app.ENABLE_ACCE_COSTUME_SYSTEM:
			self.wndAcceCombine = None
			self.wndAcceAbsorption = None

		self.inventoryTab = []
		self.equipmentTab = []
		if constInfo.ENABLE_EXPANDED_MONEY_TASKBAR:
			self.wndExpandedMoneyBar = None

		if app.ENABLE_PREMIUM_PRIVATE_SHOP_OFFICIAL:
			if self.wndPrivateShop:
				self.wndPrivateShop = None

			if self.wndPrivateShopSearch:
				self.wndPrivateShopSearch = None

	def OpenWonExchangeWindow(self):
		self.interface.ToggleWonExchangeWindow()

	def StackItem(self):
		net.SendChatPacket("/sort_inventory")

	def Hide(self):
		if constInfo.GET_ITEM_QUESTION_DIALOG_STATUS():
			self.OnCloseQuestionDialog()
			return
		if self.tooltipItem:
			self.tooltipItem.HideToolTip()

		if self.wndCostume:
			self.isOpenedCostumeWindowWhenClosingInventory = self.wndCostume.IsShow()
			self.wndCostume.Close()


		if self.dlgPickMoney:
			self.dlgPickMoney.Close()
			
		if self.dlgPickItem:
			self.dlgPickItem.Close()

		if app.ENABLE_CHEQUE_SYSTEM:
			if self.dlgPickETC:
				self.dlgPickETC.Close()

		if self.wndSystemsWindow:
			self.wndSystemsWindow.Destroy()


		wndMgr.Hide(self.hWnd)


	def Close(self):
		self.Hide()

	if constInfo.ENABLE_EXPANDED_MONEY_TASKBAR:
		def SetExpandedMoneyBar(self, wndBar):
			self.wndExpandedMoneyBar = wndBar
			if self.wndExpandedMoneyBar:
				self.wndMoneySlot = self.wndExpandedMoneyBar.GetMoneySlot()
				self.wndMoney = self.wndExpandedMoneyBar.GetMoney()
				if app.ENABLE_CHEQUE_SYSTEM:
					self.wndMoneyIcon = self.wndExpandedMoneyBar.GetMoneyIcon()
					self.wndMoneyIcon.SetEvent(ui.__mem_func__(self.SellWon))
					if self.wndMoneySlot:
						self.wndMoneySlot.SetEvent(ui.__mem_func__(self.OpenWonExchangeWindow), 0)
					self.wndChequeIcon = self.wndExpandedMoneyBar.GetChequeIcon()
					self.wndChequeIcon.SetEvent(ui.__mem_func__(self.BuyWon))
					self.wndChequeSlot = self.wndExpandedMoneyBar.GetChequeSlot() 
					if self.wndChequeSlot:
						self.wndChequeSlot.SetEvent(ui.__mem_func__(self.OpenWonExchangeWindow), 1)
					self.wndCheque = self.wndExpandedMoneyBar.GetCheque()
				if app.ENABLE_PUNKTY_OSIAGNIEC:
					self.wndPktOsiagIcon = self.wndExpandedMoneyBar.GetPktOsiagIcon()
					self.wndPktOsiag = self.wndExpandedMoneyBar.GetPktOsiag()
				else:
					if self.wndMoneySlot:
						self.wndMoneySlot.SetEvent(ui.__mem_func__(self.OpenPickMoneyDialog))

	def BuyWon(self):
		net.SendWonExchangeBuyPacket(int(1))

	def SellWon(self):
		net.SendWonExchangeSellPacket(int(1))

	def SetInventoryPage(self, page):
		self.inventoryPageIndex = page
		for i in range(player.INVENTORY_PAGE_COUNT):
			if i!=page:
				self.inventoryTab[i].SetUp()
		self.RefreshBagSlotWindow()

	def SetEquipmentPage(self, page):
		self.equipmentPageIndex = page
		self.equipmentTab[1-page].SetUp()
		self.RefreshEquipSlotWindow()


	def ClickDSSButton(self):
		self.interface.ToggleDragonSoulWindow()

	def UseDSSButtonEffect(self, enable):
		if self.DSSButton:
			DSSButtonEffect = ui.SlotWindow()
			DSSButtonEffect.AddFlag("attach")
			DSSButtonEffect.SetParent(self.DSSButton)
			DSSButtonEffect.SetPosition(3.2, 0)

			DSSButtonEffect.AppendSlot(0, 0, 0, 32, 32)
			DSSButtonEffect.SetRenderSlot(0)
			DSSButtonEffect.RefreshSlot()

			if enable:
				DSSButtonEffect.ActivateSlot(0)
				DSSButtonEffect.Show()
			else:
				DSSButtonEffect.DeactivateSlot(0)
				DSSButtonEffect.Hide()
			self.DSSButtonEffect = DSSButtonEffect

	def ClickCostumeButton(self):
		if self.wndCostume:
			if self.wndCostume.IsShow():
				self.wndCostume.Hide()
			else:
				self.wndCostume.Show()
		else:
			self.wndCostume = CostumeWindow(self)
			self.wndCostume.Show()

	def OpenPickMoneyDialog(self):

		if mouseModule.mouseController.isAttached():

			attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
			if player.SLOT_TYPE_SAFEBOX == mouseModule.mouseController.GetAttachedType():

				if player.ITEM_MONEY == mouseModule.mouseController.GetAttachedItemIndex():
					net.SendSafeboxWithdrawMoneyPacket(mouseModule.mouseController.GetAttachedItemCount())
					snd.PlaySound("sound/ui/money.wav")

			mouseModule.mouseController.DeattachObject()

		else:
			curMoney = player.GetElk()

			if curMoney <= 0:
				return


	if app.ENABLE_CHEQUE_SYSTEM:
		def OnPickMoney(self, money, cheque):
			if cheque > 0 and money > 0:
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.CHEQUE_ONLY_VALUE)
				return
			if cheque > 0:
				mouseModule.mouseController.AttacCheque(self, player.SLOT_TYPE_INVENTORY, cheque)
			else:
				mouseModule.mouseController.AttachMoney(self, player.SLOT_TYPE_INVENTORY, money)
	else:
		def OnPickMoney(self, money):
			mouseModule.mouseController.AttachMoney(self, player.SLOT_TYPE_INVENTORY, money)

	def OnPickItem(self, count):
		if app.ENABLE_OFFLINE_SHOP:
			if uiOfflineShop.IsBuildingShop() and uiOfflineShop.IsSaleSlot(player.INVENTORY, self.dlgPickItem.itemGlobalSlotIndex):
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.CANNOT_DOING_PRIVATE_SHOP_OPEN)
				return
		if self.dlgPickItem.IsSplitAll():
			g = self.BuildGrid()

			slot = self.dlgPickItem.itemGlobalSlotIndex
			vnum = player.GetItemIndex(slot)
			originalCount = player.GetItemCount(slot)
			
			stackCount = int(math.ceil(float(originalCount) / float(count))) - 1
			if stackCount < 1:
				return
			
			item.SelectItem(vnum)
			_, size = item.GetItemSize()
			
			gridItem = grid.SizeItem(size)
			
			for i in range(stackCount):
				pos = g.FindBlank(gridItem)
				if pos == -1:
					break
				
				g.PutGlobal(gridItem, pos)
				
				net.SendItemMovePacket(player.INVENTORY, slot, player.INVENTORY, pos, count)
		else:

			itemSlotIndex = self.dlgPickItem.itemGlobalSlotIndex
			selectedItemVNum = player.GetItemIndex(itemSlotIndex)
			mouseModule.mouseController.AttachObject(self, player.SLOT_TYPE_INVENTORY, itemSlotIndex, selectedItemVNum, count)

		self.dlgPickItem.SplitClear()

	def __InventoryLocalSlotPosToGlobalSlotPos(self, local):
		if player.IsEquipmentSlot(local) or player.IsCostumeSlot(local) or (app.ENABLE_NEW_EQUIPMENT_SYSTEM and player.IsBeltInventorySlot(local)):
			return local

		return self.inventoryPageIndex*player.INVENTORY_PAGE_SIZE + local

	def BuildGrid(self):
		g = grid.Grid(player.INVENTORY_PAGE_COLUMN, player.INVENTORY_PAGE_ROW, player.INVENTORY_PAGE_COUNT)
		
		for i in range(g.GetSize()):
			vnum = player.GetItemIndex(i)
			if vnum == 0:
				continue
			
			count = player.GetItemCount(i)
			if count == 0 and vnum != 71202:
				continue
			
			g.PutGlobal(itemWrapper.ItemGridWrapper(player.INVENTORY, i), i)
		
		return g

	def GetInventoryPageIndex(self):
		return self.inventoryPageIndex

	if app.WJ_ENABLE_TRADABLE_ICON:
		def RefreshMarkSlots(self, localIndex=None):
			if not self.interface:
				return

			onTopWnd = self.interface.GetOnTopWindow()
			if localIndex:
				slotNumber = self.__InventoryLocalSlotPosToGlobalSlotPos(localIndex)
				if onTopWnd == player.ON_TOP_WND_NONE:
					self.wndItem.SetUsableSlotOnTopWnd(localIndex)

				elif onTopWnd == player.ON_TOP_WND_SHOP:
					if player.IsAntiFlagBySlot(slotNumber, item.ANTIFLAG_SELL):
						self.wndItem.SetUnusableSlotOnTopWnd(localIndex)
					else:
						self.wndItem.SetUsableSlotOnTopWnd(localIndex)

				elif onTopWnd == player.ON_TOP_WND_EXCHANGE:
					if player.IsAntiFlagBySlot(slotNumber, item.ANTIFLAG_GIVE):
						self.wndItem.SetUnusableSlotOnTopWnd(localIndex)
					else:
						self.wndItem.SetUsableSlotOnTopWnd(localIndex)

				elif onTopWnd == player.ON_TOP_WND_PRIVATE_SHOP:
					if player.IsAntiFlagBySlot(slotNumber, item.ITEM_ANTIFLAG_MYSHOP):
						self.wndItem.SetUnusableSlotOnTopWnd(localIndex)
					else:
						self.wndItem.SetUsableSlotOnTopWnd(localIndex)

				elif onTopWnd == player.ON_TOP_WND_SAFEBOX:
					if player.IsAntiFlagBySlot(slotNumber, item.ANTIFLAG_SAFEBOX):
						self.wndItem.SetUnusableSlotOnTopWnd(localIndex)
					else:
						self.wndItem.SetUsableSlotOnTopWnd(localIndex)

				return

			for i in range(player.INVENTORY_PAGE_SIZE):
				slotNumber = self.__InventoryLocalSlotPosToGlobalSlotPos(i)

				if onTopWnd == player.ON_TOP_WND_NONE:
					self.wndItem.SetUsableSlotOnTopWnd(i)

				elif onTopWnd == player.ON_TOP_WND_SHOP:
					if player.IsAntiFlagBySlot(slotNumber, item.ANTIFLAG_SELL):
						self.wndItem.SetUnusableSlotOnTopWnd(i)
					else:
						self.wndItem.SetUsableSlotOnTopWnd(i)

				elif onTopWnd == player.ON_TOP_WND_EXCHANGE:
					if player.IsAntiFlagBySlot(slotNumber, item.ANTIFLAG_GIVE):
						self.wndItem.SetUnusableSlotOnTopWnd(i)
					else:
						self.wndItem.SetUsableSlotOnTopWnd(i)

				elif onTopWnd == player.ON_TOP_WND_PRIVATE_SHOP:
					if player.IsAntiFlagBySlot(slotNumber, item.ITEM_ANTIFLAG_MYSHOP):
						self.wndItem.SetUnusableSlotOnTopWnd(i)
					else:
						self.wndItem.SetUsableSlotOnTopWnd(i)

				elif onTopWnd == player.ON_TOP_WND_SAFEBOX:
					if player.IsAntiFlagBySlot(slotNumber, item.ANTIFLAG_SAFEBOX):
						self.wndItem.SetUnusableSlotOnTopWnd(i)
					else:
						self.wndItem.SetUsableSlotOnTopWnd(i)

	def RefreshBagSlotWindow(self):
		if not self.wndItem:
			return
		
		getItemVNum=player.GetItemIndex
		getItemCount=player.GetItemCount
		setItemVNum=self.wndItem.SetItemSlot

		for i in range(player.INVENTORY_PAGE_SIZE):
			slotNumber = self.__InventoryLocalSlotPosToGlobalSlotPos(i)

			itemCount = getItemCount(slotNumber)
			if 0 == itemCount:
				self.wndItem.ClearSlot(i)
				continue
			elif 1 == itemCount:
				itemCount = 0

			itemVnum = getItemVNum(slotNumber)
			setItemVNum(i, itemVnum, itemCount)

			if constInfo.IS_AUTO_POTION(itemVnum):
				metinSocket = [player.GetItemMetinSocket(slotNumber, j) for j in range(player.METIN_SOCKET_MAX_NUM)]
				isActivated = 0 != metinSocket[2]
				potionType = 0
				if constInfo.IS_AUTO_POTION_HP(itemVnum):
					potionType = player.AUTO_POTION_TYPE_HP
				elif constInfo.IS_AUTO_POTION_SP(itemVnum):
					potionType = player.AUTO_POTION_TYPE_SP
				usedAmount = int(metinSocket[1])
				totalAmount = int(metinSocket[2])
				if totalAmount > 0:
					player.SetAutoPotionInfo(potionType, isActivated, (totalAmount - usedAmount), totalAmount, self.__InventoryLocalSlotPosToGlobalSlotPos(i))

			if app.WJ_ENABLE_TRADABLE_ICON:
				self.RefreshMarkSlots(i)

			if constInfo.IS_BLEND_ITEM(itemVnum):
				metinSocket = [player.GetItemMetinSocket(slotNumber, j) for j in range(player.METIN_SOCKET_MAX_NUM)]

				isActivated = 0 != metinSocket[1]
				
				if isActivated:
					self.wndItem.ActivateSlot(i)
				else:
					self.wndItem.DeactivateSlot(i)
					
			item.SelectItem(itemVnum)
			itemType = item.GetItemType()
			itemSubType = item.GetItemSubType()
			isToggleLike = (itemType == item.TOGGLE) or (itemType == item.USE and itemSubType == 10)
			if app.__ENABLE_TOGGLE_ITEMS__:
				if isToggleLike:
					metinSocket = [player.GetItemMetinSocket(slotNumber, j) for j in range(player.METIN_SOCKET_MAX_NUM)]
					isActivated = 0 != metinSocket[3]
					if isActivated:
						self.wndItem.ActivateSlot(i)
						if hasattr(self.wndItem, 'ActivateSlotEffect'):
							self.wndItem.ActivateSlotEffect(i, (36.00 / 255.0), (222.00 / 255.0), (3.00 / 255.0), 1.0)
					else:
						if hasattr(self.wndItem, 'DeactivateSlotEffect'):
							self.wndItem.DeactivateSlotEffect(i)
						elif hasattr(self.wndItem, 'ActivateSlotEffect'):
							self.wndItem.ActivateSlotEffect(i, 0.0, 0.0, 0.0, 0.0)
						self.wndItem.DeactivateSlot(i)
				else:
					if hasattr(self.wndItem, 'DeactivateSlotEffect'):
						self.wndItem.DeactivateSlotEffect(i)
					elif hasattr(self.wndItem, 'ActivateSlotEffect'):
						self.wndItem.ActivateSlotEffect(i, 0.0, 0.0, 0.0, 0.0)


			if app.ENABLE_AURA_SYSTEM:
				slotNumberChecked = 0
				for j in range(aura.WINDOW_MAX_MATERIALS):
					(isHere, iCell) = aura.GetAttachedItem(j)
					if isHere:
						if iCell == slotNumber:
							self.wndItem.ActivateSlotEffect(i, (36.00 / 255.0), (222.00 / 255.0), (3.00 / 255.0), 1.0)
							if not slotNumber in self.listAttachedAuras:
								self.listAttachedAuras.append(slotNumber)
							
							slotNumberChecked = 1
					else:
						if slotNumber in self.listAttachedAuras and not slotNumberChecked:
							self.wndItem.DeactivateSlotEffect(i)
							self.listAttachedAuras.remove(slotNumber)

			if app.ENABLE_ACCE_COSTUME_SYSTEM:
				slotNumberChecked = 0
				if not constInfo.IS_AUTO_POTION(itemVnum) and not constInfo.IS_BLEND_ITEM(itemVnum) and not itemType == item.TOGGLE:
					if app.ENABLE_HIGHLIGHT_NEW_ITEM:
						if not slotNumber in self.liHighlightedItems:
							self.wndItem.DeactivateSlot(i)
					else:
						self.wndItem.DeactivateSlot(i)

				for j in range(acce.WINDOW_MAX_MATERIALS):
					(isHere, iCell) = acce.GetAttachedItem(j)
					if isHere:
						if iCell == slotNumber:
							self.wndItem.ActivateSlot(i, (36.00 / 255.0), (222.00 / 255.0), (3.00 / 255.0), 1.0)
							if not slotNumber in self.listAttachedAcces:
								self.listAttachedAcces.append(slotNumber)

							slotNumberChecked = 1
					else:
						if slotNumber in self.listAttachedAcces and not slotNumberChecked:
							self.wndItem.DeactivateSlot(i)
							self.listAttachedAcces.remove(slotNumber)

			elif app.ENABLE_HIGHLIGHT_NEW_ITEM and not constInfo.IS_AUTO_POTION(itemVnum) and not constInfo.IS_BLEND_ITEM(itemVnum) and not itemType == item.TOGGLE:
				if not slotNumber in self.liHighlightedItems:
					self.wndItem.DeactivateSlot(i)

			if itemType == item.FISH:
				fishData = GetFishMissionData(itemVnum)
				if fishData and player.GetItemMetinSocket(slotNumber, 0) >= fishData[1]*100:
					self.wndItem.SetFishAddonOnSlot(i)

		if app.ENABLE_PREMIUM_PRIVATE_SHOP_OFFICIAL:
			if self.wndPrivateShop and self.wndPrivateShop.IsShow():
				self.wndPrivateShop.RefreshLockedSlot()

		if hasattr(constInfo, 'listRemoveItem') and constInfo.listRemoveItem:
			for i in range(player.INVENTORY_PAGE_SIZE):
				slotNumber = self.__InventoryLocalSlotPosToGlobalSlotPos(i)
				if slotNumber in constInfo.listRemoveItem:
					self.wndItem.ActivateSlot(i, 1.0, 0.0, 0.0)

		self.wndItem.RefreshSlot()
		if app.ENABLE_HIGHLIGHT_NEW_ITEM:
			self.__RefreshHighlights()


		if app.WJ_ENABLE_TRADABLE_ICON:
			# map() w Py3 jest leniwy - bez konsumpcji lambda nigdy sie nie wykonywala
			for wnd in self.bindWnds:
				wnd.RefreshLockedSlot()

	if app.ENABLE_HIGHLIGHT_NEW_ITEM:
		def HighlightSlot(self, slot):
			if not slot in self.liHighlightedItems:
				self.liHighlightedItems.append(slot)

		def __RefreshHighlights(self):
			for i in range(player.INVENTORY_PAGE_SIZE):
				slotNumber = self.__InventoryLocalSlotPosToGlobalSlotPos(i)
				if slotNumber in self.liHighlightedItems:
					itemVnum = player.GetItemIndex(slotNumber)
					if constInfo.IS_AUTO_POTION(itemVnum) or constInfo.IS_BLEND_ITEM(itemVnum):
						continue
					item.SelectItem(itemVnum)
					if item.GetItemType() == item.TOGGLE:
						continue
					self.wndItem.ActivateSlot(i)

	def RefreshEquipSlotWindow(self):
		getItemVNum=player.GetItemIndex
		getItemCount=player.GetItemCount
		setItemVNum=self.wndEquip.SetItemSlot
		for i in range(player.EQUIPMENT_PAGE_COUNT):
			slotNumber = player.EQUIPMENT_SLOT_START + i
			itemCount = getItemCount(slotNumber)
			if itemCount <= 1:
				itemCount = 0
			setItemVNum(slotNumber, getItemVNum(slotNumber), itemCount)

		if app.ENABLE_NEW_EQUIPMENT_SYSTEM:
			for i in range(player.NEW_EQUIPMENT_SLOT_COUNT):
				slotNumber = player.NEW_EQUIPMENT_SLOT_START + i
				itemCount = getItemCount(slotNumber)
				if itemCount <= 1:
					itemCount = 0
				setItemVNum(slotNumber, getItemVNum(slotNumber), itemCount)

		self.wndEquip.RefreshSlot()

		if self.wndCostume:
			self.wndCostume.RefreshCostumeSlot()

	def RefreshItemSlot(self):
		# UWAGA: RefreshBagSlotWindow NIE jest tylko wizualne - ustawia player.SetAutoPotionInfo,
		# wiec tego okna NIE wolno pomijac przy ukrytym stanie (auto-potiony przestalyby dzialac).
		self.RefreshBagSlotWindow()
		self.RefreshEquipSlotWindow()

	def RefreshStatus(self):
		money = player.GetElk()
		self.wndMoney.SetText("|cFFffd74c"+localeInfo.NumberToGoldNotText(money))
		if app.ENABLE_CHEQUE_SYSTEM:
			cheque = player.GetCheque()
			self.wndCheque.SetText("|cFFb8b8b8"+localeInfo.NumberToGoldNotText(cheque))

	def SetItemToolTip(self, tooltipItem):
		self.tooltipItem = tooltipItem

	def SellItem(self):
		if app.ENABLE_OFFLINE_SHOP and uiOfflineShop.IsBuildingShop() and uiOfflineShop.IsSaleSlot(player.INVENTORY, self.sellingSlotNumber):
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.CANNOT_DOING_PRIVATE_SHOP_OPEN)
			return
		if self.sellingSlotitemIndex == player.GetItemIndex(self.sellingSlotNumber):
			if self.sellingSlotitemCount == player.GetItemCount(self.sellingSlotNumber):
				net.SendShopSellPacketNew(self.sellingSlotNumber, self.questionDialog.count, player.INVENTORY)
				snd.PlaySound("sound/ui/money.wav")
		self.OnCloseQuestionDialog()

	def OnDetachMetinFromItem(self):
		if None == self.questionDialog:
			return

		self.__SendUseItemToItemPacket(self.questionDialog.sourcePos, self.questionDialog.targetPos)
		self.OnCloseQuestionDialog()

	def OnCloseQuestionDialog(self):
		if not self.questionDialog:
			return

		self.questionDialog.Close()
		self.questionDialog = None
		constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(0)

	def SelectEmptySlot(self, selectedSlotPos):
		if constInfo.GET_ITEM_QUESTION_DIALOG_STATUS() == 1:
			return

		if constInfo.IS_BONUS_CHANGER:
			return

		selectedSlotPos = self.__InventoryLocalSlotPosToGlobalSlotPos(selectedSlotPos)

		if mouseModule.mouseController.isAttached():

			attachedSlotType = mouseModule.mouseController.GetAttachedType()

			if player.SLOT_TYPE_DRAGON_SOUL_INVENTORY == attachedSlotType:
				mouseModule.mouseController.DeattachObject()
				return

			attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
			attachedItemCount = mouseModule.mouseController.GetAttachedItemCount()
			attachedItemIndex = mouseModule.mouseController.GetAttachedItemIndex()

			if app.ENABLE_OFFLINE_SHOP and uiOfflineShop.IsBuildingShop() and uiOfflineShop.IsSaleSlot(player.SlotTypeToInvenType(attachedSlotType), attachedSlotPos):
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.CANNOT_DOING_PRIVATE_SHOP_OPEN)
				return

			if attachedSlotType in INVENTORY_SLOT_TYPES or player.SLOT_TYPE_DRAGON_SOUL_INVENTORY == attachedSlotType:
				itemCount = player.GetItemCount(attachedSlotPos)
				attachedCount = mouseModule.mouseController.GetAttachedItemCount()
				if self.dlgPickItem and self.dlgPickItem.IsSplitAll():
					net.SendChatPacket("/split_items %d %d %d" % (attachedSlotPos, attachedCount, selectedSlotPos))
				else:
					self.__SendMoveItemPacket(attachedSlotPos, selectedSlotPos, attachedCount)

				attachedInvenType = player.SlotTypeToInvenType(attachedSlotType)
				if player.IsDSEquipmentSlot(attachedInvenType, attachedSlotPos):
					mouseModule.mouseController.DeattachObject()
					return


				if item.IsRefineScroll(attachedItemIndex):
					self.wndItem.SetUseMode(False)

			elif app.ENABLE_SWITCHBOT and player.SLOT_TYPE_SWITCHBOT == attachedSlotType:
				attachedCount = mouseModule.mouseController.GetAttachedItemCount()
				net.SendItemMovePacket(player.SWITCHBOT, attachedSlotPos, player.INVENTORY, selectedSlotPos, attachedCount)

			elif player.SLOT_TYPE_PRIVATE_SHOP == attachedSlotType:
				if app.ENABLE_PREMIUM_PRIVATE_SHOP_OFFICIAL:
					if not uiPrivateShopBuilder.IsBuildingPrivateShop():
						self.wndPrivateShop.SendItemCheckoutPacket(attachedSlotPos, selectedSlotPos)
						mouseModule.mouseController.DeattachObject()
						return

				mouseModule.mouseController.RunCallBack("INVENTORY")
				
			elif player.SLOT_TYPE_BUFF_EQUIPMENT == attachedSlotType and app.ENABLE_ASLAN_BUFF_NPC_SYSTEM:
				attachedCount = mouseModule.mouseController.GetAttachedItemCount()
				net.SendItemMovePacket(player.BUFF_EQUIPMENT, attachedSlotPos, player.INVENTORY, selectedSlotPos, attachedCount)

			elif player.SLOT_TYPE_SHOP == attachedSlotType:
				net.SendShopBuyPacket(attachedSlotPos)

			elif player.SLOT_TYPE_SAFEBOX == attachedSlotType:

				if player.ITEM_MONEY == attachedItemIndex:
					net.SendSafeboxWithdrawMoneyPacket(mouseModule.mouseController.GetAttachedItemCount())
					snd.PlaySound("sound/ui/money.wav")

				else:
					net.SendSafeboxCheckoutPacket(attachedSlotPos, selectedSlotPos)

			elif player.SLOT_TYPE_MALL == attachedSlotType:
				net.SendMallCheckoutPacket(attachedSlotPos, selectedSlotPos)

			mouseModule.mouseController.DeattachObject()

	def IsChanger(self, itemVnum):
		if not itemVnum:
			return False
		return item.GetUseType(itemVnum) in CHANGER_USE_TYPES

	def SelectItemSlot(self, itemSlotIndex):
		if constInfo.GET_ITEM_QUESTION_DIALOG_STATUS() == 1:
			return

		if constInfo.IS_BONUS_CHANGER:
			return

		itemSlotIndex = self.__InventoryLocalSlotPosToGlobalSlotPos(itemSlotIndex)

		if mouseModule.mouseController.isAttached():
			attachedSlotType = mouseModule.mouseController.GetAttachedType()
			attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
			attachedItemVID = mouseModule.mouseController.GetAttachedItemIndex()

			if self.IsChanger(attachedItemVID) and not player.IsEquipmentSlot(itemSlotIndex):
				itemVnum = player.GetItemIndex(itemSlotIndex)
				item.SelectItem(itemVnum)
				if item.GetItemType() == item.WEAPON or item.GetItemType() == item.ARMOR:
					self.interface.AddToBonusChange(itemSlotIndex, attachedSlotPos)
					mouseModule.mouseController.DeattachObject()
					return

			if attachedSlotType in INVENTORY_SLOT_TYPES:
				attachedInvenType = player.SlotTypeToInvenType(attachedSlotType)
				if player.IsDSEquipmentSlot(attachedInvenType, attachedSlotPos):
					mouseModule.mouseController.DeattachObject()
					return
				self.__DropSrcItemToDestItemInInventory(attachedItemVID, attachedSlotPos, itemSlotIndex)

			mouseModule.mouseController.DeattachObject()

		else:

			curCursorNum = app.GetCursor()
			if app.SELL == curCursorNum:
				self.__SellItem(itemSlotIndex)

			elif app.BUY == curCursorNum:
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.SHOP_BUY_INFO)

			elif app.IsPressed(app.DIK_LALT):
				link = player.GetItemLink(itemSlotIndex)
				ime.PasteString(link)

			elif app.IsPressed(app.DIK_LSHIFT):
				itemCount = player.GetItemCount(itemSlotIndex)

				if itemCount > 1:
					self.dlgPickItem.SetTitleName(localeInfo.PICK_ITEM_TITLE)
					self.dlgPickItem.SetAcceptEvent(ui.__mem_func__(self.OnPickItem))
					self.dlgPickItem.Open(itemCount)
					self.dlgPickItem.itemGlobalSlotIndex = itemSlotIndex
					self.OnPickItem(itemCount)
					mouseModule.mouseController.DeattachObject()

			elif app.IsPressed(app.DIK_LCONTROL):
				itemIndex = player.GetItemIndex(itemSlotIndex)

				if app.ENABLE_PREMIUM_PRIVATE_SHOP_OFFICIAL:
					if self.wndPrivateShop and self.wndPrivateShop.IsShow():
						self.wndPrivateShop.AttachItemToPrivateShop(itemSlotIndex, player.SLOT_TYPE_INVENTORY)
						return

					if self.wndPrivateShopSearch and self.wndPrivateShopSearch.IsShow():
						self.wndPrivateShopSearch.SelectItem(itemIndex)

				if True == item.CanAddToQuickSlotItem(itemIndex):
					player.RequestAddToEmptyLocalQuickSlot(player.SLOT_TYPE_INVENTORY, itemSlotIndex)
				else:
					chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.QUICKSLOT_REGISTER_DISABLE_ITEM)

			else:
				selectedItemVNum = player.GetItemIndex(itemSlotIndex)
				itemCount = player.GetItemCount(itemSlotIndex)
				if app.ENABLE_EXTENDED_BLEND:
					if self.__CanAttachThisItem(selectedItemVNum, itemSlotIndex):
						mouseModule.mouseController.AttachObject(self, player.SLOT_TYPE_INVENTORY, itemSlotIndex, selectedItemVNum, itemCount)
				else:
					mouseModule.mouseController.AttachObject(self, player.SLOT_TYPE_INVENTORY, itemSlotIndex, selectedItemVNum, itemCount)

				if self.__IsUsableItemToItem(selectedItemVNum, itemSlotIndex):
					self.wndItem.SetUseMode(True)
				else:
					self.wndItem.SetUseMode(False)

				snd.PlaySound("sound/ui/pick.wav")

	def __DropSrcItemToDestItemInInventory(self, srcItemVID, srcItemSlotPos, dstItemSlotPos):
		if app.ENABLE_OFFLINE_SHOP and uiOfflineShop.IsBuildingShop() and (uiOfflineShop.IsSaleSlot(player.INVENTORY, srcItemSlotPos) or uiOfflineShop.IsSaleSlot(player.INVENTORY , dstItemSlotPos)):
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.CANNOT_DOING_PRIVATE_SHOP_OPEN)
			return
		if srcItemSlotPos == dstItemSlotPos:
			return

		item.SelectItem(player.GetItemIndex(dstItemSlotPos))
		destItemType = item.GetItemType()
		destItemSubType = item.GetItemSubType()
		destItemVnum = player.GetItemIndex(dstItemSlotPos)

		if app.ENABLE_SOULBIND_SYSTEM and item.IsSealScroll(srcItemVID):
			self.__SendUseItemToItemPacket(srcItemSlotPos, dstItemSlotPos)

		elif item.IsRefineScroll(srcItemVID):
			if item.GetUseType(srcItemVID) in ALLOWED_TYPES and\
			item.GetUseType(player.GetItemIndex(dstItemSlotPos))\
			in ALLOWED_TYPES:
				self.__SendMoveItemPacket(srcItemSlotPos, dstItemSlotPos, 0)
			else:
				self.RefineItem(srcItemSlotPos, dstItemSlotPos)
				self.wndItem.SetUseMode(False)

		elif item.GetUseType(srcItemVID) in ALLOWED_TYPES and\
			item.GetUseType(player.GetItemIndex(dstItemSlotPos))\
			in ALLOWED_TYPES:
				self.__SendMoveItemPacket(srcItemSlotPos, dstItemSlotPos, 0)
		elif srcItemVID == 71051 or srcItemVID == 71052:
			self.__SendUseItemToItemPacket(srcItemSlotPos, dstItemSlotPos)
		elif srcItemVID >= 91201 and srcItemVID <= 91205:
			self.__SendUseItemToItemPacket(srcItemSlotPos, dstItemSlotPos)
		elif srcItemVID >= 79015 and srcItemVID <= 79023:
			self.__SendUseItemToItemPacket(srcItemSlotPos, dstItemSlotPos)
		elif srcItemVID == 79014:
			self.__SendUseItemToItemPacket(srcItemSlotPos, dstItemSlotPos)

		# 70082 "Dodanie Czasu (7 dni)" - typ QUEST, wiec nie lapia go galezie ogolne nizej.
		elif srcItemVID == 70082:
			self.__SendUseItemToItemPacket(srcItemSlotPos, dstItemSlotPos)

		elif item.IsMetin(srcItemVID) and not item.IsMetin(player.GetItemIndex(dstItemSlotPos)):
			self.AttachMetinToItem(srcItemSlotPos, dstItemSlotPos)

		elif item.GetUseType(srcItemVID) == "USE_PUT_INTO_ACCESSORY_SOCKET" and not self.__CanPutAccessorySocket(dstItemSlotPos, srcItemVID):
			self.__SendMoveItemPacket(srcItemSlotPos, dstItemSlotPos, 0)

		elif srcItemVID == 39046 and destItemSubType == item.COSTUME_TYPE_ACCE or srcItemVID == 90000 and destItemSubType == item.COSTUME_TYPE_ACCE:
			self.DetachMetinFromItem(srcItemSlotPos, dstItemSlotPos)

		elif item.IsDetachScroll(srcItemVID):
			self.DetachMetinFromItem(srcItemSlotPos, dstItemSlotPos)

		elif item.IsKey(srcItemVID):
			self.__SendUseItemToItemPacket(srcItemSlotPos, dstItemSlotPos)

		elif (player.GetItemFlags(srcItemSlotPos) & ITEM_FLAG_APPLICABLE) == ITEM_FLAG_APPLICABLE:
			self.__SendUseItemToItemPacket(srcItemSlotPos, dstItemSlotPos)

		elif item.GetUseType(srcItemVID) in self.USE_TYPE_TUPLE:
			self.__SendUseItemToItemPacket(srcItemSlotPos, dstItemSlotPos)

		else:

			if player.IsEquipmentSlot(dstItemSlotPos):

				if item.IsEquipmentVID(srcItemVID):
					self.__UseItem(srcItemSlotPos)

			else:
				self.__SendMoveItemPacket(srcItemSlotPos, dstItemSlotPos, 0)

	def __SellItem(self, itemSlotPos):
		if app.ENABLE_OFFLINE_SHOP and uiOfflineShop.IsBuildingShop():
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.CANNOT_DOING_PRIVATE_SHOP_OPEN)
			return
		if not player.IsEquipmentSlot(itemSlotPos):
			self.sellingSlotNumber = itemSlotPos
			itemIndex = player.GetItemIndex(itemSlotPos)
			itemCount = player.GetItemCount(itemSlotPos)


			self.sellingSlotitemIndex = itemIndex
			self.sellingSlotitemCount = itemCount

			item.SelectItem(itemIndex)
			if item.IsAntiFlag(item.ANTIFLAG_SELL):
				popup = uiCommon.PopupDialog()
				popup.SetText(localeInfo.SHOP_CANNOT_SELL_ITEM)
				popup.SetAcceptEvent(self.__OnClosePopupDialog)
				popup.Open()
				self.popup = popup
				return

			itemPrice = item.GetISellItemPrice()

			if item.Is1GoldItem():
				itemPrice = itemCount // itemPrice // 2
			else:
				itemPrice = itemPrice * itemCount  // 2

			itemName = item.GetItemName()

			self.questionDialog = uiCommon.QuestionDialog()
			self.questionDialog.SetText(localeInfo.DO_YOU_SELL_ITEM(itemName, itemCount, itemPrice))
			self.questionDialog.SetAcceptEvent(ui.__mem_func__(self.SellItem))
			self.questionDialog.SetCancelEvent(ui.__mem_func__(self.OnCloseQuestionDialog))
			self.questionDialog.Open()
			self.questionDialog.count = itemCount

			constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(1)

	def __OnClosePopupDialog(self):
		self.pop = None

	def RefineItem(self, scrollSlotPos, targetSlotPos):
		scrollIndex = player.GetItemIndex(scrollSlotPos)
		targetIndex = player.GetItemIndex(targetSlotPos)
		if app.ENABLE_OFFLINE_SHOP and uiOfflineShop.IsBuildingShop():
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.CANNOT_DOING_PRIVATE_SHOP_OPEN)
			return

		if player.REFINE_OK != player.CanRefine(scrollIndex, targetSlotPos):
			return

		if app.ENABLE_REFINE_RENEWAL:
			constInfo.AUTO_REFINE_TYPE = 1
			constInfo.AUTO_REFINE_DATA["ITEM"][0] = scrollSlotPos
			constInfo.AUTO_REFINE_DATA["ITEM"][1] = targetSlotPos

		self.__SendUseItemToItemPacket(scrollSlotPos, targetSlotPos)

	if app.ENABLE_NEW_STONE_DETACH:
		def OpenNewStoneDetachWindow(self, scrollSlotPos, targetSlotPos):
			if not self.wndStoneDetach:
				self.wndStoneDetach = uistonedetach.StoneDetachWindow()

			self.wndStoneDetach.Open(scrollSlotPos, targetSlotPos)

	if app.ENABLE_PREMIUM_PRIVATE_SHOP_OFFICIAL:
		def BindPrivateShopClass(self, window):
			self.wndPrivateShop = window

		def BindPrivateShopSearchClass(self, window):
			self.wndPrivateShopSearch = window

	def DetachMetinFromItem(self, scrollSlotPos, targetSlotPos):
		scrollIndex = player.GetItemIndex(scrollSlotPos)
		targetIndex = player.GetItemIndex(targetSlotPos)

		if not player.CanDetach(scrollIndex, targetSlotPos):
			if app.ENABLE_ACCE_COSTUME_SYSTEM:
				item.SelectItem(scrollIndex)
				if item.GetValue(0) == acce.CLEAN_ATTR_VALUE0:
					chat.AppendChat(chat.CHAT_TYPE_INFO, "Nie mo�esz tego zrobi�.")
				else:
					chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.REFINE_FAILURE_METIN_INSEPARABLE_ITEM)
			else:
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.REFINE_FAILURE_METIN_INSEPARABLE_ITEM)
			return

		self.questionDialog = uiCommon.QuestionDialog()
		self.questionDialog.SetText(localeInfo.REFINE_DO_YOU_SEPARATE_METIN)
		
		item.SelectItem(targetIndex)
		if item.GetItemType() == item.COSTUME and item.GetItemSubType() == item.COSTUME_TYPE_ACCE:
			item.SelectItem(scrollIndex)
			if item.GetValue(0) == acce.CLEAN_ATTR_VALUE0:
				self.questionDialog.SetText(localeInfo.ACCE_CLEAR_ATTR_CONFIRM)
		else:
			self.OpenNewStoneDetachWindow(scrollSlotPos, targetSlotPos)
			return

		self.questionDialog.SetAcceptEvent(ui.__mem_func__(self.OnDetachMetinFromItem))
		self.questionDialog.SetCancelEvent(ui.__mem_func__(self.OnCloseQuestionDialog))
		self.questionDialog.Open()
		self.questionDialog.sourcePos = scrollSlotPos
		self.questionDialog.targetPos = targetSlotPos

	def AttachMetinToItem(self, metinSlotPos, targetSlotPos):
		metinIndex = player.GetItemIndex(metinSlotPos)
		targetIndex = player.GetItemIndex(targetSlotPos)

		item.SelectItem(metinIndex)
		itemName = item.GetItemName()

		result = player.CanAttachMetin(metinIndex, targetSlotPos)

		if player.ATTACH_METIN_NOT_MATCHABLE_ITEM == result:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.REFINE_FAILURE_CAN_NOT_ATTACH(itemName))

		if player.ATTACH_METIN_NO_MATCHABLE_SOCKET == result:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.REFINE_FAILURE_NO_SOCKET(itemName))

		elif player.ATTACH_METIN_NOT_EXIST_GOLD_SOCKET == result:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.REFINE_FAILURE_NO_GOLD_SOCKET(itemName))

		elif player.ATTACH_METIN_CANT_ATTACH_TO_EQUIPMENT == result:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.REFINE_FAILURE_EQUIP_ITEM)

		if player.ATTACH_METIN_OK != result:
			return

		self.attachMetinDialog.Open(metinSlotPos, targetSlotPos)



	def OverOutItem(self):
		self.wndItem.SetUsableItem(False)
		if self.tooltipItem:
			if self.__IsCursorOnInventorySlotWindow() and hasattr(self.tooltipItem, "HideToolTipWithoutModelPreview"):
				self.tooltipItem.HideToolTipWithoutModelPreview()
			else:
				self.tooltipItem.HideToolTip()

	def OverInItem(self, overSlotPos):
		overSlotPosGlobal = self.__InventoryLocalSlotPosToGlobalSlotPos(overSlotPos)
		self.wndItem.SetUsableItem(False)
		self.wndItem.SetUseMode(False)


		if app.ENABLE_HIGHLIGHT_NEW_ITEM and overSlotPosGlobal in self.liHighlightedItems:
			self.liHighlightedItems.remove(overSlotPosGlobal)
			self.wndItem.DeactivateSlot(overSlotPos)


		if mouseModule.mouseController.isAttached():
			attachedItemType = mouseModule.mouseController.GetAttachedType()
			if player.SLOT_TYPE_INVENTORY == attachedItemType or player.SLOT_TYPE_STONE_INVENTORY == attachedItemType or player.SLOT_TYPE_EFSUN_INVENTORY == attachedItemType:

				attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
				attachedItemVNum = mouseModule.mouseController.GetAttachedItemIndex()

				if attachedItemVNum==player.ITEM_MONEY:
					pass
				elif self.__CanUseSrcItemToDstItem(attachedItemVNum, attachedSlotPos, overSlotPosGlobal):
					self.wndItem.SetUsableItem(True)
					self.wndItem.SetUseMode(True)
					self.ShowToolTip(overSlotPosGlobal)
					return

		self.ShowToolTip(overSlotPosGlobal)


	# 70082 "Dodanie Czasu (7 dni)" - serwer przyjmuje go tylko na kostiumy 41001-41999
	USABLE_ITEM_VNUMS = frozenset((71051, 71052, 91201, 91205, 79014, 79015, 79023, 39046, 70082))

	def __IsUsableItemToItem(self, srcItemVNum, srcSlotPos):
		if item.IsRefineScroll(srcItemVNum) or item.IsMetin(srcItemVNum) or item.IsDetachScroll(srcItemVNum) or item.IsKey(srcItemVNum):
			return True
		if srcItemVNum in self.USABLE_ITEM_VNUMS:
			return True
		if (player.GetItemFlags(srcSlotPos) & ITEM_FLAG_APPLICABLE) == ITEM_FLAG_APPLICABLE:
			return True
		if item.GetUseType(srcItemVNum) in self.USE_TYPE_TUPLE:
			return True
		return False

	def __CanUseSrcItemToDstItem(self, srcItemVNum, srcSlotPos, dstSlotPos):
		if srcSlotPos == dstSlotPos and not item.IsMetin(srcItemVNum):
			return False

		item.SelectItem(player.GetItemIndex(dstSlotPos))
		destItemType = item.GetItemType()
		destItemSubType = item.GetItemSubType()

		if item.IsRefineScroll(srcItemVNum):
			if player.REFINE_OK == player.CanRefine(srcItemVNum, dstSlotPos):
				return True
		elif item.IsMetin(srcItemVNum):
			if player.ATTACH_METIN_OK == player.CanAttachMetin(srcItemVNum, dstSlotPos) or (item.IsMetin(player.GetItemIndex(dstSlotPos)) and player.GetItemIndex(dstSlotPos) == srcItemVNum):
				return True
		elif srcItemVNum == 39046 and destItemSubType == item.COSTUME_TYPE_ACCE or srcItemVNum == 90000 and destItemSubType == item.COSTUME_TYPE_ACCE:
			return True
		elif item.IsDetachScroll(srcItemVNum):
			if player.DETACH_METIN_OK == player.CanDetach(srcItemVNum, dstSlotPos):
				return True
		elif item.IsKey(srcItemVNum):
			if player.CanUnlock(srcItemVNum, dstSlotPos):
				return True

		if srcItemVNum == 70082:
			# ten sam zakres kostiumow co Wzmocnienie Kostiumu (33052/33053)
			return 41001 <= player.GetItemIndex(dstSlotPos) <= 41999

		if (srcItemVNum == 33052 or srcItemVNum == 33053) and player.GetItemIndex(dstSlotPos) >= 41001 and player.GetItemIndex(dstSlotPos) <= 41999:
			return True
			
		elif (srcItemVNum == 33054 or srcItemVNum == 33055) and player.GetItemIndex(dstSlotPos) >= 45001 and player.GetItemIndex(dstSlotPos) <= 45999:
			return True
			
		elif (srcItemVNum == 33056 or srcItemVNum == 33057) and player.GetItemIndex(dstSlotPos) >= 40100 and player.GetItemIndex(dstSlotPos) <= 40999:
			return True

		elif (srcItemVNum == 33051 or srcItemVNum == 33050) and player.GetItemIndex(dstSlotPos) >= 53001 and player.GetItemIndex(dstSlotPos) <= 53999:
			return True		
			
		elif srcItemVNum in [33050,33051,33052,33053,33054,33055,33056,33057]:
			return False

		elif (player.GetItemFlags(srcSlotPos) & ITEM_FLAG_APPLICABLE) == ITEM_FLAG_APPLICABLE:
			return True
		elif srcItemVNum == 71051:
			if self.__CanAddRareItemAttr(dstSlotPos):
				return True
		elif srcItemVNum == 71052:
			if self.__CanChangeRareItemAttrList(dstSlotPos):
				return True
		elif srcItemVNum >= 91201 and srcItemVNum <= 91205:
			if self.__CanAddItemAttrToRod(dstSlotPos):
				return True
		elif srcItemVNum >= 79015 and srcItemVNum <= 79023:
			if self.__CanUseRune(dstSlotPos):
				return True
		elif srcItemVNum == 79014:
			if self.__CanUseAlchemyChanger(dstSlotPos):
				return True

		else:
			useType = item.GetUseType(srcItemVNum)
			USE_TYPE_DISPATCH = {
				"USE_CLEAN_SOCKET": self.__CanCleanBrokenMetinStone,
				"USE_SASH_CLEANER": self.__CanUseOnSash,
				"USE_CHANGE_ATTRIBUTE": self.__CanChangeItemAttrList,
				"USE_ADD_ATTRIBUTE": self.__CanAddItemAttr,
				"USE_ADD_ATTRIBUTE2": self.__CanAddItemAttr,
				"USE_ADD_ATTRIBUTE_SPECIAL_1": self.__CanAddItemAttr,
				"USE_ADD_NEW_BONUS": self.__CanAddItemAttr,
				"USE_ADD_EXTRA_BONUS": self.__CanAddItemAttr,
				"USE_ADD_IS_BONUS": self.__CanAddItemAttr,
				"USE_ADD_ACCESSORY_SOCKET": self.__CanAddAccessorySocket,
			}
			if app.ENABLE_USE_COSTUME_ATTR:
				USE_TYPE_DISPATCH["USE_CHANGE_COSTUME_ATTR"] = self.__CanChangeCostumeAttrList
				USE_TYPE_DISPATCH["USE_RESET_COSTUME_ATTR"] = self.__CanResetCostumeAttr

			validator = USE_TYPE_DISPATCH.get(useType)
			if validator:
				if validator(dstSlotPos):
					return True
			elif useType == "USE_PUT_INTO_ACCESSORY_SOCKET":
				if self.__CanPutAccessorySocket(dstSlotPos, srcItemVNum):
					return True
			elif useType == "USE_PUT_INTO_BELT_SOCKET":
				dstItemVNum = player.GetItemIndex(dstSlotPos)
				item.SelectItem(dstItemVNum)
				if item.BELT == item.GetItemType():
					return True

		return False

	def __CanUseOnSash(self, dstSlotPos):
		dstItemVNum = player.GetItemIndex(dstSlotPos)
		if dstItemVNum == 0:
			return False
 
		item.SelectItem(dstItemVNum)
 
		if item.GetItemSubType() == item.COSTUME_TYPE_ACCE:
			return True
 
		return False
		
	def __CanAddRareItemAttr(self, dstSlotPos):
		dstItemVNum = player.GetItemIndex(dstSlotPos)
		if dstItemVNum == 0:
			return False

		item.SelectItem(dstItemVNum)

		if item.GetItemType() not in (item.WEAPON, item.ARMOR):
			return False

		attrCount = 0
		for i in range(player.METIN_SOCKET_MAX_NUM):
			if player.GetItemAttribute(dstSlotPos, i)[0] != 0:
				attrCount += 1

		return player.ATTRIBUTE_SLOT_MAX_NUM - 2 <= attrCount < player.ATTRIBUTE_SLOT_MAX_NUM

	def __CanChangeRareItemAttrList(self, dstSlotPos):
		return self.__CanAddRareItemAttr(dstSlotPos)

	def __CanCleanBrokenMetinStone(self, dstSlotPos):
		dstItemVNum = player.GetItemIndex(dstSlotPos)
		if dstItemVNum == 0:
			return False

		item.SelectItem(dstItemVNum)

		if item.WEAPON != item.GetItemType():
			return False

		for i in range(player.METIN_SOCKET_MAX_NUM):
			if player.GetItemMetinSocket(dstSlotPos, i) == constInfo.ERROR_METIN_STONE:
				return True

		return False

	def __CanChangeItemAttrList(self, dstSlotPos):
		dstItemVNum = player.GetItemIndex(dstSlotPos)
		if dstItemVNum == 0:
			return False

		item.SelectItem(dstItemVNum)

		if not item.GetItemType() in (item.WEAPON, item.ARMOR, item.BELT):
			return False

		for i in range(player.METIN_SOCKET_MAX_NUM):
			if player.GetItemAttribute(dstSlotPos, i)[0] != 0:
				return True

		return False

	if app.ENABLE_USE_COSTUME_ATTR:
		def __CanChangeCostumeAttrList(self, dstSlotPos):
			dstItemVNum = player.GetItemIndex(dstSlotPos)
			if dstItemVNum == 0:
				return False

			item.SelectItem(dstItemVNum)

			if item.GetItemType() != item.COSTUME:
				return False

			for i in range(player.METIN_SOCKET_MAX_NUM):
				if player.GetItemAttribute(dstSlotPos, i)[0] != 0:
					return True

			return False

		def __CanResetCostumeAttr(self, dstSlotPos):
			return self.__CanChangeCostumeAttrList(dstSlotPos)

	def __CanPutAccessorySocket(self, dstSlotPos, mtrlVnum):
		dstItemVNum = player.GetItemIndex(dstSlotPos)
		if dstItemVNum == 0:
			return False

		item.SelectItem(dstItemVNum)

		if item.GetItemType() != item.ARMOR:
			return False

		if not item.GetItemSubType() in (item.ARMOR_WRIST, item.ARMOR_NECK, item.ARMOR_EAR):
			return False

		curCount = player.GetItemMetinSocket(dstSlotPos, 0)
		maxCount = player.GetItemMetinSocket(dstSlotPos, 1)

		if mtrlVnum != constInfo.GET_ACCESSORY_MATERIAL_VNUM(dstItemVNum, item.GetItemSubType()):
			return False

		if curCount>=maxCount:
			return False

		return True

	def __CanAddAccessorySocket(self, dstSlotPos):
		dstItemVNum = player.GetItemIndex(dstSlotPos)
		if dstItemVNum == 0:
			return False

		item.SelectItem(dstItemVNum)

		if item.GetItemType() != item.ARMOR:
			return False

		if not item.GetItemSubType() in (item.ARMOR_WRIST, item.ARMOR_NECK, item.ARMOR_EAR):
			return False

		curCount = player.GetItemMetinSocket(dstSlotPos, 0)
		maxCount = player.GetItemMetinSocket(dstSlotPos, 1)

		ACCESSORY_SOCKET_MAX_SIZE = 3
		if maxCount >= ACCESSORY_SOCKET_MAX_SIZE:
			return False

		return True

	def __CanAddItemAttr(self, dstSlotPos):
		dstItemVNum = player.GetItemIndex(dstSlotPos)
		if dstItemVNum == 0:
			return False

		item.SelectItem(dstItemVNum)

		if not item.GetItemType() in (item.WEAPON, item.ARMOR, item.BELT):
			return False

		attrCount = 0
		for i in range(player.METIN_SOCKET_MAX_NUM):
			if player.GetItemAttribute(dstSlotPos, i)[0] != 0:
				attrCount += 1

		if attrCount<5:
			return True

		return False

	def ShowToolTip(self, slotIndex):
		if self.tooltipItem:
			self.tooltipItem.SetInventoryItem(slotIndex)
			if app.ENABLE_OFFLINE_SHOP:
				if uiOfflineShop.IsBuildingShop():
					self.__AddTooltipSaleMode(slotIndex)

	if app.ENABLE_OFFLINE_SHOP:
		def __AddTooltipSaleMode(self, slot):
			if player.IsEquipmentSlot(slot):
				return

			itemIndex = player.GetItemIndex(slot)
			if itemIndex !=0:
				item.SelectItem(itemIndex)
				if item.IsAntiFlag(item.ANTIFLAG_MYSHOP) or item.IsAntiFlag(item.ANTIFLAG_GIVE):
					return

				self.tooltipItem.AddRightClickForSale()

	def __IsCursorOnInventorySlotWindow(self):
		slotWindows = [self.wndItem, self.wndEquip]

		if self.wndCostume:
			slotWindows.append(getattr(self.wndCostume, "wndEquip", None))

		if self.wndBelt:
			slotWindows.append(getattr(self.wndBelt, "wndBeltInventorySlot", None))

		for wnd in slotWindows:
			if wnd and wnd.IsIn():
				return True

		return False

	def OnTop(self):
		if self.tooltipItem:
			self.tooltipItem.SetTop()

		if app.WJ_ENABLE_TRADABLE_ICON:
			# map() w Py3 jest leniwy - bez konsumpcji lambda nigdy sie nie wykonywala
			for wnd in self.bindWnds:
				wnd.RefreshLockedSlot()
			self.RefreshMarkSlots()

	def OnPressEscapeKey(self):
		self.Close()
		return True

	if app.WJ_SPLIT_INVENTORY_SYSTEM:
		def GetEmptyItemPos(self, type, itemHeight):
			start_val = start_val_table[type - 1]
			end_val = end_val_table[type - 1]

			GetBlockedSlots = lambda slot, size: [slot+(round*3) for round in range(size)] 
			def _slot_height(slot):
				item.SelectItem(player.GetItemIndex(slot))
				return item.GetItemSize()[1]
			blocked_slots = [element for sublist in [GetBlockedSlots(slot, _slot_height(slot)) for slot in range(start_val, end_val) if player.isItem(slot)] for element in sublist] 
			if itemHeight > 1: 
				[[blocked_slots.append(slot) for slot in range(start_val, end_val//round-(itemHeight-1)*3, start_val//round) if not slot in blocked_slots] for round in range(1,3)] 
			free_slots = [slot for slot in range(start_val, end_val) if not slot in blocked_slots and not True in [e in blocked_slots for e in [slot+(round*3) for round in range(itemHeight)]]] 
			return free_slots if free_slots else -1

		def SetPage(self, val):
			calc = val // 45
			page_table = [2,1,0]
			self.interface.wndExtendedInventory.SetInventoryPage(page_table[calc])
		
	def UseItemSlot(self, slotIndex):
		curCursorNum = app.GetCursor()
		if app.SELL == curCursorNum:
			return

		test = self.__InventoryLocalSlotPosToGlobalSlotPos(slotIndex)
		globalSlot 	= self.__InventoryLocalSlotPosToGlobalSlotPos(slotIndex)

		# Ctrl+PPM: gdy magazyn otwarty, wrzuc item do magazynu
		if app.IsPressed(app.DIK_LCONTROL) and self.interface:
			wndSafebox = getattr(self.interface, "wndSafebox", None)
			if wndSafebox and wndSafebox.IsShow():
				itemVnum = player.GetItemIndex(globalSlot)
				if itemVnum != 0:
					item.SelectItem(itemVnum)
					if item.IsAntiFlag(item.ANTIFLAG_SAFEBOX):
						chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.SAFEBOX_CANNOT_DEPOSIT)
						return
					(w, h) = item.GetItemSize()
					if h <= 0:
						h = 1
					sbSize = safebox.GetCurrentSafeboxSize()
					sbPageSize = safebox.SAFEBOX_PAGE_SIZE
					sbRowWidth = safebox.SAFEBOX_SLOT_X_COUNT
					sbPageCount = max(1, sbSize // sbPageSize)
					# Budujemy mape zajetosci safeboxa (uwzgledniajac wysokosc itemow)
					sbGrid = [[False for _ in range(sbPageSize)] for _ in range(sbPageCount)]
					for pg in range(sbPageCount):
						for sl in range(sbPageSize):
							idx = pg * sbPageSize + sl
							if idx >= sbSize:
								continue
							occVnum = safebox.GetItemID(idx)
							if occVnum != 0:
								item.SelectItem(occVnum)
								(ow, oh) = item.GetItemSize()
								if oh <= 0:
									oh = 1
								for dy in range(oh):
									s = sl + dy * sbRowWidth
									if s < sbPageSize:
										sbGrid[pg][s] = True
					item.SelectItem(itemVnum)
					freeSafeboxSlot = -1
					for page in range(sbPageCount):
						for slot in range(sbPageSize):
							fits = True
							for dy in range(h):
								checkLocal = slot + dy * sbRowWidth
								if checkLocal >= sbPageSize or sbGrid[page][checkLocal]:
									fits = False
									break
							if fits:
								freeSafeboxSlot = page * sbPageSize + slot
								break
						if freeSafeboxSlot != -1:
							break
					if freeSafeboxSlot != -1:
						net.SendSafeboxCheckinPacket(player.INVENTORY, globalSlot, freeSafeboxSlot)
					else:
						chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.SAFEBOX_FULL)
					return

		if app.ENABLE_OFFLINE_SHOP:
			if uiOfflineShop.IsBuildingShop():
				itemIndex 	= player.GetItemIndex(globalSlot)
				item.SelectItem(itemIndex)

				if app.IsPressed(app.DIK_LCONTROL):
					if not item.IsAntiFlag(item.ANTIFLAG_GIVE) and not item.IsAntiFlag(item.ANTIFLAG_MYSHOP):
						self.interface.wndShopOffline.SetFastAddItem(True)
						offlineshop.ShopBuilding_AddItem(player.INVENTORY, globalSlot)
					else:
						chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.CANNOT_DOING_PRIVATE_SHOP_OPEN)
					return
				else:
					if not item.IsAntiFlag(item.ANTIFLAG_MYSHOP):
						offlineshop.ShopBuilding_AddItem(player.INVENTORY, globalSlot)
					else:
						chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.CANNOT_DOING_PRIVATE_SHOP_OPEN)
					return
		itemVnum = player.GetItemIndex(test)
		itemCount = player.GetItemCount(test)
		item.SelectItem(itemVnum)
		specialinvtype = item.GetSpecialInvType()

		(w, h) = item.GetItemSize()

		# GetEmptyItemPos zwraca -1 gdy nie ma wolnego miejsca; liczenie page_calculation
		# tutaj robilo emptyInvenSlots[0] na tym -1 (TypeError -> PPM przestawalo dzialac).
		# Dla specialinvtype == 0 (zwykly item) tabele i tak indeksowalyby sie [-1] (zawiniecie
		# na ostatnia zakladke), a wynik nie jest uzywany -> nie liczymy go wcale.
		emptyInvenSlots = self.GetEmptyItemPos(specialinvtype, h) if specialinvtype != 0 else -1

		if app.WJ_SPLIT_INVENTORY_SYSTEM:
			if specialinvtype != 0:
				if not app.IsPressed(app.DIK_LCONTROL):
					if not self.interface.wndRemoveItem.IsShow() and not self.interface.wndFragments.IsShow():
						if app.IsPressed(app.DIK_LSHIFT):
							if mouseModule.mouseController.isAttached():
								mouseModule.mouseController.DeattachObject()

							if settings.enable_fast_open == 1:
								if constInfo.EXTENDED_INVENTORY_IS_OPEN == 0:
									self.interface.ToggleExtendedInventoryWindow()

							if emptyInvenSlots == -1:
								chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.INVENTORY_SPECIAL_INVENTORY_IS_FULL.format(SPECIAL_INV_NAMES[specialinvtype - 1]))
								return
							else:
								self.__SendMoveItemPacket(test, emptyInvenSlots[0], itemCount)
								if settings.enable_fast_open == 1:
									page_calculation = end_val_table[specialinvtype - 1] - emptyInvenSlots[0]
									self.interface.wndExtendedInventory.SetInventoryType(specialinvtype-1)
									self.SetPage(page_calculation)


		if constInfo.GET_ITEM_QUESTION_DIALOG_STATUS():
			return

		if constInfo.IS_BONUS_CHANGER:
			return

		slotIndex = self.__InventoryLocalSlotPosToGlobalSlotPos(slotIndex)
		
		if app.IsPressed(app.DIK_LSHIFT) and self.interface.wndRemoveItem.IsShow():
			self.interface.wndRemoveItem.AppendSlot(player.INVENTORY, slotIndex)
			return

		if app.ENABLE_ODLAMKI_SYSTEM:
			if app.IsPressed(app.DIK_LSHIFT) and self.interface.wndFragments.IsShow():
				itemType = item.GetItemType()
				if not item.METIN == itemType:
					chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.INVENTORY_STONES_ONLY)
					return
				else:
					self.interface.wndFragments.AppendSlot(player.INVENTORY, slotIndex)
					return
			

			
		if app.ENABLE_DRAGON_SOUL_SYSTEM:
			if self.wndDragonSoulRefine.IsShow():
				ItemVNum = player.GetItemIndex(slotIndex)
				if ItemVNum == 100300 or ItemVNum == 100400 or ItemVNum == 100500:
					self.wndDragonSoulRefine.AutoSetItem((player.INVENTORY, slotIndex), player.GetItemCount(slotIndex))
				else:
					self.wndDragonSoulRefine.AutoSetItem((player.INVENTORY, slotIndex), 1)
				return
		if app.ITEM_CHECKINOUT_UPDATE:
			if exchange.isTrading() and slotIndex < player.EQUIPMENT_SLOT_START:
				net.SendExchangeItemAddPacket(player.INVENTORY, slotIndex, -1)
				return
		if app.ENABLE_ACCE_COSTUME_SYSTEM:
			if self.isShowAcceWindow():
				acce.Add(player.INVENTORY, slotIndex, 255)
				return	
		if app.ENABLE_AURA_SYSTEM:
			itemVNum = player.GetItemIndex(slotIndex)
			if self.isShowAuraWindow():
				if itemVNum >= 21900 and itemVNum <= 21999:
					return
				aura.Add(player.INVENTORY, slotIndex, 255)
				return
		if app.IsPressed(app.DIK_LALT):
			net.SendChatPacket("/quick_open {}".format(slotIndex))
			return


		if app.IsPressed(app.DIK_LCONTROL) and app.IsPressed(app.DIK_X):
			shopSearch = self.interface.GetShopSearchWindow()
			if not shopSearch:
				return
			if not shopSearch.IsShow():
				shopSearch.Show(True)
			item.SelectItem(itemVnum)
			shopSearch.sItemName.SetText(item.GetItemName())
			shopSearch.OnSearch()
		

		self.__UseItem(slotIndex)
		mouseModule.mouseController.DeattachObject()
		self.OverOutItem()
		
	def IsQuickOpen(iVnum):
		exceptList = [27987]
		item.SelectItem(iVnum)
		if item.GetItemType() == item.GIFTBOX or iVnum in exceptList:
			return True
			
		return False

	def __UseItem(self, slotIndex):
		if app.ENABLE_OFFLINE_SHOP and uiOfflineShop.IsBuildingShop() and uiOfflineShop.IsSaleSlot(player.INVENTORY, slotIndex):
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.CANNOT_DOING_PRIVATE_SHOP_OPEN)
			return
		if self.interface and self.interface.AttachInvenItemToOtherWindowSlot(player.INVENTORY, slotIndex):
			return
		ItemVNum = player.GetItemIndex(slotIndex)

		item.SelectItem(ItemVNum)

		if item.IsFlag(item.ITEM_FLAG_CONFIRM_WHEN_USE):
			self.questionDialog = uiCommon.QuestionDialog()
			self.questionDialog.SetText(localeInfo.INVENTORY_REALLY_USE_ITEM)
			self.questionDialog.SetAcceptEvent(ui.__mem_func__(self.__UseItemQuestionDialog_OnAccept))
			self.questionDialog.SetCancelEvent(ui.__mem_func__(self.__UseItemQuestionDialog_OnCancel))
			self.questionDialog.Open()
			self.questionDialog.slotIndex = slotIndex

			constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(1)
			# Bez tego pakiet uzycia szedl OD RAZU, a potwierdzenie w dialogu wysylalo go
			# drugi raz - na stosie Kuponow SM (80014-80017, jedyne itemy z ta flaga)
			# jedno PPM zjadalo dwie sztuki.
			return

		if app.IsPressed(app.DIK_LALT):
			net.SendChatPacket("/quick_open {}".format(slotIndex))
			return

		# Shift+PPM na karmniku towarzysza = zuzyj caly stos. Zwykle PPM zjada jedna
		# sztuke (serwer: FeedCompanionVoucher w char_item.cpp).
		if COMPANION_EXP_VOUCHER_SUBTYPE >= 0 and app.IsPressed(app.DIK_LSHIFT) and not app.IsPressed(app.DIK_LCONTROL):
			if item.GetItemType() == item.USE and item.GetItemSubType() == COMPANION_EXP_VOUCHER_SUBTYPE:
				net.SendChatPacket("/feed_stack {}".format(slotIndex))
				return

		# Ctrl+PPM = podglad dropu skrzyni (Ctrl+Shift = lista dodatkowa), item sie NIE uzywa.
		if app.__BL_CHEST_DROP_INFO__ and app.IsPressed(app.DIK_LCONTROL):
			isMain = not app.IsPressed(app.DIK_LSHIFT)
			if item.HasDropInfo(ItemVNum, isMain) and self.interface:
				self.interface.OpenChestDropWindow(ItemVNum, isMain)
			return

		# Wysylka MUSI byc poza warunkiem __BL_CHEST_DROP_INFO__ - wczesniej siedziala w jego
		# galezi else, wiec klient zbudowany bez tej flagi w ogole nie uzywalby itemow z PPM.
		self.__SendUseItemPacket(slotIndex)

	def __GetCurrentItemGrid(self):
		itemGrid = [[False for slot in range(player.INVENTORY_PAGE_SIZE)] for page in range(player.INVENTORY_PAGE_COUNT)]

		for page in range(player.INVENTORY_PAGE_COUNT):
			for slot in range(player.INVENTORY_PAGE_SIZE):
				itemVnum = player.GetItemIndex(slot + page * player.INVENTORY_PAGE_SIZE)
				if itemVnum != 0:
					item.SelectItem(itemVnum)
					(w, h) = item.GetItemSize()
					for i in range(h):
						itemGrid[page][slot + i * 5] = True

		return itemGrid

	def __FindEmptyCellForSize(self, itemGrid, size):
		for page in range(player.INVENTORY_PAGE_COUNT):
			for slot in range(player.INVENTORY_PAGE_SIZE):
				if itemGrid[page][slot] == False:
					possible = True
					for i in range(size):
						p = slot + (i * 5)

						try:
							if itemGrid[page][p]:
								possible = False
								break
						except IndexError:
							possible = False
							break

					if possible:
						return slot + page * player.INVENTORY_PAGE_SIZE

		return -1
		
	def AttachItemFromSafebox(self, slotIndex, itemIndex):
		itemGrid = self.__GetCurrentItemGrid()

		item.SelectItem(itemIndex)
		if item.GetItemType() == item.DS:
			return

		emptySlotIndex = self.__FindEmptyCellForSize(itemGrid, item.GetItemSize()[1])
		if emptySlotIndex != -1:
			net.SendSafeboxCheckoutPacket(slotIndex, player.INVENTORY, emptySlotIndex)

		return True

	def __UseItemQuestionDialog_OnCancel(self):
		self.OnCloseQuestionDialog()

	def __UseItemQuestionDialog_OnAccept(self):
		self.__SendUseItemPacket(self.questionDialog.slotIndex)
		self.OnCloseQuestionDialog()

	def __SendUseItemToItemPacket(self, srcSlotPos, dstSlotPos):
		if uiPrivateShopBuilder.IsBuildingPrivateShop():
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.USE_ITEM_FAILURE_PRIVATE_SHOP)
			return

		if self.interface.wndRemoveItem.IsShow():
			return

		if app.ENABLE_ODLAMKI_SYSTEM:
			if self.interface.wndFragments.IsShow():
				return

		if app.ENABLE_OFFLINE_SHOP_SYSTEM:
			if (uiOfflineShopBuilder.IsBuildingOfflineShop()):
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.USE_ITEM_FAILURE_OFFLINE_SHOP)
				return

			if (uiOfflineShop.IsEditingOfflineShop()):
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.USE_ITEM_FAILURE_OFFLINE_SHOP)
				return

		net.SendItemUseToItemPacket(srcSlotPos, dstSlotPos)

	def __SendUseItemPacket(self, slotPos):
		if uiPrivateShopBuilder.IsBuildingPrivateShop():
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.USE_ITEM_FAILURE_PRIVATE_SHOP)
			return

		if self.interface.wndRemoveItem.IsShow():
			return

		if app.ENABLE_ODLAMKI_SYSTEM:
			if self.interface.wndFragments.IsShow():
				return

		if app.ENABLE_OFFLINE_SHOP_SYSTEM:
			if uiOfflineShopBuilder.IsBuildingOfflineShop():
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.USE_ITEM_FAILURE_OFFLINE_SHOP)
				return

			if uiOfflineShop.IsEditingOfflineShop():
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.USE_ITEM_FAILURE_OFFLINE_SHOP)
				return

		net.SendItemUsePacket(slotPos)

	def __SendMoveItemPacket(self, srcSlotPos, dstSlotPos, srcItemCount):
		if uiPrivateShopBuilder.IsBuildingPrivateShop():
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.MOVE_ITEM_FAILURE_PRIVATE_SHOP)
			return
		if app.ENABLE_OFFLINE_SHOP:
			if uiOfflineShop.IsBuildingShop():
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.CANNOT_DOING_PRIVATE_SHOP_OPEN)
				return

		if app.ENABLE_OFFLINE_SHOP_SYSTEM:
			if uiOfflineShopBuilder.IsBuildingOfflineShop():
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.MOVE_ITEM_FAILURE_OFFLINE_SHOP)
				return

			if uiOfflineShop.IsEditingOfflineShop():
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.MOVE_ITEM_FAILURE_OFFLINE_SHOP)
				return

		net.SendItemMovePacket(srcSlotPos, dstSlotPos, srcItemCount)

	def SetDragonSoulRefineWindow(self, wndDragonSoulRefine):
		if app.ENABLE_DRAGON_SOUL_SYSTEM:
			self.wndDragonSoulRefine = wndDragonSoulRefine

	def OnMoveWindow(self, x, y):
		if self.wndSystemsWindow:
			self.wndSystemsWindow.AdjustPositionAndSize()
		if self.wndCostume:
			self.wndCostume.AdjustPositionAndSize()

	def MouseSlotEventRefresh(self):
		for i in range(self.wndItem.GetSlotCount()):
			slotNumber = self.__InventoryLocalSlotPosToGlobalSlotPos(i)
			if slotNumber in self.listCantMouseSlot:
				itemInvenPage = slotNumber // player.INVENTORY_PAGE_SIZE
				localSlotPos = slotNumber - (itemInvenPage * player.INVENTORY_PAGE_SIZE)

				self.wndItem.SetCantMouseEventSlot(localSlotPos)
				self.wndItem.RefreshSlot()

	def MouseSlotEventClear(self):
		for i in range(self.wndItem.GetSlotCount()):
			slotNumber = self.__InventoryLocalSlotPosToGlobalSlotPos(i)
			if slotNumber in self.listCantMouseSlot:
				self.wndItem.SetCanMouseEventSlot(i)
				self.listCantMouseSlot.remove(slotNumber)

	def SetCantMouseSlot(self, slot):
		if slot > player.INVENTORY_PAGE_SIZE * player.INVENTORY_PAGE_COUNT:
			return

		if not slot in self.listCantMouseSlot:
			self.listCantMouseSlot.append(slot)

	def SetCanMouseSlot(self, inventorylocalslot):
		if inventorylocalslot in self.listCantMouseSlot:
			if inventorylocalslot >= player.INVENTORY_PAGE_SIZE*self.inventoryPageIndex:
				self.wndItem.SetCanMouseEventSlot(inventorylocalslot-player.INVENTORY_PAGE_SIZE*self.inventoryPageIndex)
			else:
				self.wndItem.SetCanMouseEventSlot(inventorylocalslot)

			self.listCantMouseSlot.remove(inventorylocalslot)

	if app.ENABLE_ACCE_COSTUME_SYSTEM:
		def SetAcceWindow(self, wndAcceCombine, wndAcceAbsorption):
			self.wndAcceCombine = wndAcceCombine
			self.wndAcceAbsorption = wndAcceAbsorption

		def isShowAcceWindow(self):
			if self.wndAcceCombine:
				if self.wndAcceCombine.IsShow():
					return 1
			if self.wndAcceAbsorption:
				if self.wndAcceAbsorption.IsShow():
					return 1
			return 0

	if app.ENABLE_AURA_SYSTEM:
		def SetAuraWindow(self, wndAuraAbsorption, wndAuraRefine):
			self.wndAuraRefine = wndAuraRefine
			self.wndAuraAbsorption = wndAuraAbsorption

		def isShowAuraWindow(self):
			if self.wndAuraRefine:
				if self.wndAuraRefine.IsShow():
					return 1

			if self.wndAuraAbsorption:
				if self.wndAuraAbsorption.IsShow():
					return 1
			
			return 0

	def __CanAddItemAttrToTool(self, dstSlotPos, toolType):
		dstItemVNum = player.GetItemIndex(dstSlotPos)
		if dstItemVNum == 0:
			return False

		item.SelectItem(dstItemVNum)

		if item.GetItemType() != toolType:
			return False

		attrCount = sum(1 for i in range(3) if player.GetItemAttribute(dstSlotPos, i)[0] != 0)
		return attrCount < 3

	def __CanAddItemAttrToPick(self, dstSlotPos):
		return self.__CanAddItemAttrToTool(dstSlotPos, item.PICK)

	def __CanAddItemAttrToRod(self, dstSlotPos):
		return self.__CanAddItemAttrToTool(dstSlotPos, item.ROD)
		
	def __CanUseRune(self, dstSlotPos):
		dstItemVNum = player.GetItemIndex(dstSlotPos)
		if dstItemVNum == 0:
			return False

		item.SelectItem(dstItemVNum)

		if item.GetItemType() != item.ARMOR:
			return False

		return item.GetItemSubType() in (item.ARMOR_HEAD, item.ARMOR_SHIELD, item.ARMOR_FOOTS)
		
	def __CanUseAlchemyChanger(self, dstSlotPos):
		dstItemVNum = player.GetItemIndex(dstSlotPos)
		if dstItemVNum == 0:
			return False

		item.SelectItem(dstItemVNum)
		return item.GetItemType() == item.DS

	if app.ENABLE_EXTENDED_BLEND:
		def __CanAttachThisItem(self, itemVNum, itemSlotIndex):
			if constInfo.IS_PERMANANET_BLEND_ITEM(itemVNum):
				isActivated = player.GetItemMetinSocket(itemSlotIndex, 1)
				if isActivated == 1:
					return False


			return True
		
