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
import uiPickMoney
import uiCommon
import uiPrivateShopBuilder
import localeInfo
import constInfo
import ime
import uiInventory
import uiToolTip
import sys
import emoji
ITEM_FLAG_APPLICABLE = 1 << 14

class DragonSoulWindow(ui.ScriptWindow):
	KIND_TAP_TITLES = [uiScriptLocale.DRAGONSOUL_TAP_TITLE_1, uiScriptLocale.DRAGONSOUL_TAP_TITLE_2,
			uiScriptLocale.DRAGONSOUL_TAP_TITLE_3, uiScriptLocale.DRAGONSOUL_TAP_TITLE_4, uiScriptLocale.DRAGONSOUL_TAP_TITLE_5, uiScriptLocale.DRAGONSOUL_TAP_TITLE_6]


	if app.ENABLE_DS_GRADE_MYTH:
		PAGE_TAB_TITLES = [
			uiScriptLocale.DRAGONSOUL_GRADE_0,
			uiScriptLocale.DRAGONSOUL_GRADE_1,
			uiScriptLocale.DRAGONSOUL_GRADE_2,
			uiScriptLocale.DRAGONSOUL_GRADE_3,
			uiScriptLocale.DRAGONSOUL_GRADE_4,
			uiScriptLocale.DRAGONSOUL_GRADE_5
		]
		
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.questionDialog = None
		self.tooltipItem = None
		self.sellingSlotNumber = -1
		self.isLoaded = 0
		self.isActivated = False
		self.DSKindIndex = 0
		self.tabDict = None
		self.tabButtonDict = None
		self.deckPageIndex = 0
		self.inventoryPageIndex = 0
		self.SetWindowName("DragonSoulWindow")
		self.__LoadWindow()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def Show(self):
		self.__LoadWindow()

		# refresh robimy tu, bo RefreshItemSlot pomija ukryte okno (patrz nizej)
		self.RefreshBagSlotWindow()
		self.RefreshEquipSlotWindow()

		ui.ScriptWindow.Show(self)
	def __LoadWindow(self):
		if self.isLoaded == 1:
			return
		self.isLoaded = 1
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "uiscript/dragonsoulwindow.py")

		except:
			import exception
			exception.Abort("dragonsoulwindow.LoadWindow.LoadObject")
		try:
			wndItem = self.GetChild("ItemSlot")
			wndEquip = self.GetChild("EquipmentSlot")
			self.activateButton = self.GetChild("activate")
			self.renewbtn = self.GetChild("renew_btn")
			self.deckTab = []
			self.deckTab.append(self.GetChild("deck1"))
			self.deckTab.append(self.GetChild("deck2"))
			self.GetChild("TitleBar").SetCloseEvent(ui.__mem_func__(self.Close))
			self.listCantMouseSlot = []
			self.inventoryTab = []

			for i in range(6 if app.ENABLE_DS_GRADE_MYTH else 5):
				self.inventoryTab.append(self.GetChild("Inventory_Tab_0{}".format(i + 1)))

			tabCount = 6

			self.tabDict = {}
			self.tabButtonDict = {}

			for tab in range(tabCount):
				self.tabDict.update({tab : self.GetChild("Tab_0{}".format(tab + 1))})
				self.tabButtonDict.update({tab : self.GetChild("Tab_Button_0{}".format(tab + 1))})
				
			self.tabText = self.GetChild("tab_text_area")
		except:
			import exception
			exception.Abort("InventoryWindow.LoadWindow.BindObject")
		for (tabKey, tabButton) in self.tabButtonDict.items():
			tabButton.SetEvent(ui.__mem_func__(self.SetDSKindIndex), tabKey)
		wndItem.SetOverInItemEvent(ui.__mem_func__(self.OverInItem))
		wndItem.SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))
		wndItem.SetSelectItemSlotEvent(ui.__mem_func__(self.SelectItemSlot))
		wndItem.SetSelectEmptySlotEvent(ui.__mem_func__(self.SelectEmptySlot))
		wndItem.SetUnselectItemSlotEvent(ui.__mem_func__(self.UseItemSlot))
		wndItem.SetUseSlotEvent(ui.__mem_func__(self.UseItemSlot))

		wndEquip.SetSelectEmptySlotEvent(ui.__mem_func__(self.SelectEmptyEquipSlot))
		wndEquip.SetSelectItemSlotEvent(ui.__mem_func__(self.SelectEquipItemSlot))
		wndEquip.SetUnselectItemSlotEvent(ui.__mem_func__(self.UseEquipItemSlot))
		wndEquip.SetUseSlotEvent(ui.__mem_func__(self.UseEquipItemSlot))
		wndEquip.SetOverInItemEvent(ui.__mem_func__(self.OverInEquipItem))
		wndEquip.SetOverOutItemEvent(ui.__mem_func__(self.OverOutEquipItem))

		for i in range(2):
			self.deckTab[i].SetToggleDownEvent(lambda arg=i: self.SetDeckPage(arg))
			self.deckTab[i].SetToggleUpEvent(lambda arg=i: self.__DeckButtonDown(arg))
		self.deckTab[0].Down()

		for i in range(6 if app.ENABLE_DS_GRADE_MYTH else 5):
			if i < len(self.inventoryTab) and self.inventoryTab[i]:
				self.inventoryTab[i].SetEvent(lambda arg=i: self.SetInventoryPage(arg))
		if self.inventoryTab and self.inventoryTab[0]:
			self.inventoryTab[0].Down()
		
		self.wndItem = wndItem
		self.wndEquip = wndEquip

		self.dlgQuestion = uiCommon.QuestionDialog2()
		self.dlgQuestion.Close()

		self.activateButton.SetToggleDownEvent(ui.__mem_func__(self.ActivateButtonClick))
		self.activateButton.SetToggleUpEvent(ui.__mem_func__(self.ActivateButtonClick))

		self.renewbtn.SetEvent(ui.__mem_func__(self.DoRenew))

		t = uiToolTip.ToolTipNew
		self.toolTip = {
			1:t(150),
		}

		self.toolTip[1].SetTitle(localeInfo.DRAGONSOUL_RENEW_TIME)
		self.toolTip[1].AppendSpace(3)
		self.toolTip[1].AppendHorizontalLine()
		self.toolTip[1].AppendSpace(3)
		self.toolTip[1].AppendTextLine(localeInfo.DRAGONSOUL_PRICE.format(emoji.AppendEmoji("icon/emoji/money_icon.png")))
		self.wndPopupDialog = uiCommon.PopupDialog()

		self.listHighlightedSlot = []

		self.SetInventoryPage(0)
		self.RefreshItemSlot()
		self.RefreshEquipSlotWindow()
		self.RefreshBagSlotWindow()
		self.SetDSKindIndex(0)
		self.activateButton.Enable()
		self.deckTab[self.deckPageIndex].Down()
		self.activateButton.SetUp()

	def IsDlgQuestionShow(self):
		if self.dlgQuestion.IsShow():
			return True
		else:
			return False

	def ExternQuestionDialog_Close(self):
		self.__Cancel()

	def Destroy(self):
		self.ClearDictionary()
		self.tooltipItem = None
		self.wndItem = 0
		self.wndEquip = 0
		self.activateButton = 0
		self.questionDialog = None
		self.mallButton = None
		self.inventoryTab = []
		self.deckTab = []
		self.equipmentTab = []
		self.tabDict = None
		self.tabButtonDict = None
	def Close(self):
		if None != self.tooltipItem:
			self.tooltipItem.HideToolTip()
		self.toolTip[1].Hide()
		self.Hide()

	def __DeckButtonDown(self, deck):
		self.deckTab[deck].Down()

	def SetInventoryPage(self, page):
		try:
			if self.wndDragonSoulRefine.IsShow():
				self.wndDragonSoulRefine.FastRefineCancel()
		except:
			pass

		if self.inventoryPageIndex != page:
			self.__HighlightSlot_ClearCurrentPage()
			
		self.inventoryPageIndex = page
	
		pageCount = 6 if app.ENABLE_DS_GRADE_MYTH else 5
		for i in range(1, pageCount):
			self.inventoryTab[(page+i) % pageCount].SetUp()
			self.inventoryTab[page].Down()
		self.RefreshBagSlotWindow()

	def SetItemToolTip(self, tooltipItem):
		self.tooltipItem = tooltipItem

	def RefreshItemSlot(self):
		# Wolane z interfacemodule.RefreshInventory przy KAZDEJ zmianie ekwipunku (autoloot!),
		# a skan strony DS + petle item.GetLimit sa czysto wizualne. Przy ukrytym oknie to
		# czysta strata - stan i tak odtwarzamy w Show().
		if not self.IsShow():
			return

		self.RefreshBagSlotWindow()
		self.RefreshEquipSlotWindow()

	if app.ENABLE_DS_GRADE_MYTH:
		def OverInInventoryTab(self, page):
			if self.toolTip:
				tooltip = self.PAGE_TAB_TITLES[page]
				arglen = len(tooltip)
				self.toolTip.ClearToolTip()
				self.toolTip.SetThinBoardSize(11 * arglen)
				self.toolTip.AppendTextLine(tooltip)
				self.toolTip.Show()

		def OverOutInventoryTab(self):
			if self.toolTip:
				
				self.toolTip.Hide()

	def RefreshEquipSlotWindow(self):
		for i in range(6):
			slotNumber = self.__InventoryLocalSlotPosToGlobalSlotPos(player.INVENTORY, player.DRAGON_SOUL_EQUIPMENT_SLOT_START + i)
			itemVnum = player.GetItemIndex(slotNumber)
			self.wndEquip.SetItemSlot(player.DRAGON_SOUL_EQUIPMENT_SLOT_START + i, itemVnum, 0)
			self.wndEquip.EnableSlot(player.DRAGON_SOUL_EQUIPMENT_SLOT_START + i)

			if itemVnum != 0:
				item.SelectItem(itemVnum)
				for j in range(item.LIMIT_MAX_NUM):
					(limitType, limitValue) = item.GetLimit(j)

					remain_time = 999
					if item.LIMIT_REAL_TIME == limitType:
						remain_time = player.GetItemMetinSocket(player.INVENTORY, slotNumber, 0) - app.GetGlobalTimeStamp()
					elif item.LIMIT_REAL_TIME_START_FIRST_USE == limitType:
						remain_time = player.GetItemMetinSocket(player.INVENTORY, slotNumber, 0) - app.GetGlobalTimeStamp()
					elif item.LIMIT_TIMER_BASED_ON_WEAR == limitType:
						remain_time = player.GetItemMetinSocket(player.INVENTORY, slotNumber, 0)

					if remain_time <= 0:
						self.wndEquip.DisableSlot(player.DRAGON_SOUL_EQUIPMENT_SLOT_START + i)
						break

		self.wndEquip.RefreshSlot()
	def ActivateEquipSlotWindow(self, deck):
		for i in range(6):
			if deck == 2:
				plusCount = 6
			else:
				plusCount = 0

			self.wndEquip.ActivateSlot(player.DRAGON_SOUL_EQUIPMENT_SLOT_START + i + plusCount)

	def DeactivateEquipSlotWindow(self):
		for i in range(12):
			self.wndEquip.DeactivateSlot(player.DRAGON_SOUL_EQUIPMENT_SLOT_START + i)
	
	def RefreshStatus(self):
		self.RefreshItemSlot()

	def __InventoryLocalSlotPosToGlobalSlotPos(self, window_type, local_slot_pos):
		if player.INVENTORY == window_type:
			return self.deckPageIndex * player.DRAGON_SOUL_EQUIPMENT_FIRST_SIZE + local_slot_pos

		if app.ENABLE_DS_GRADE_MYTH:
			return (self.DSKindIndex * 6 * player.DRAGON_SOUL_PAGE_SIZE) + self.inventoryPageIndex * player.DRAGON_SOUL_PAGE_SIZE + local_slot_pos
		else:
			return (self.DSKindIndex * 5 * player.DRAGON_SOUL_PAGE_SIZE) + self.inventoryPageIndex * player.DRAGON_SOUL_PAGE_SIZE + local_slot_pos

	def RefreshBagSlotWindow(self):
		getItemVNum=player.GetItemIndex
		getItemCount=player.GetItemCount
		setItemVnum=self.wndItem.SetItemSlot
		for i in range(player.DRAGON_SOUL_PAGE_SIZE):
			self.wndItem.EnableSlot(i)
			slotNumber = self.__InventoryLocalSlotPosToGlobalSlotPos(player.DRAGON_SOUL_INVENTORY, i)

			itemCount = getItemCount(player.DRAGON_SOUL_INVENTORY, slotNumber)
			if 0 == itemCount:
				self.wndItem.ClearSlot(i)
				continue
			elif 1 == itemCount:
				itemCount = 0
			itemVnum = getItemVNum(player.DRAGON_SOUL_INVENTORY, slotNumber)

			setItemVnum(i, itemVnum, itemCount)

			if itemVnum != 0:
				item.SelectItem(itemVnum)
				for j in range(item.LIMIT_MAX_NUM):
					(limitType, limitValue) = item.GetLimit(j)

					remain_time = 999
					if item.LIMIT_REAL_TIME == limitType:
						remain_time = player.GetItemMetinSocket(player.DRAGON_SOUL_INVENTORY, slotNumber, 0)
					elif item.LIMIT_REAL_TIME_START_FIRST_USE == limitType:
						remain_time = player.GetItemMetinSocket(player.DRAGON_SOUL_INVENTORY, slotNumber, 0)
					elif item.LIMIT_TIMER_BASED_ON_WEAR == limitType:
						remain_time = player.GetItemMetinSocket(player.DRAGON_SOUL_INVENTORY, slotNumber, 0)

					if remain_time <= 0:
						self.wndItem.DisableSlot(i)
						break

		self.__HighlightSlot_RefreshCurrentPage()
		self.wndItem.RefreshSlot()

	def ShowToolTip(self, window_type, slotIndex):
		if None != self.tooltipItem:
			if player.INVENTORY == window_type:
				self.tooltipItem.SetInventoryItem(slotIndex)
			else:
				self.tooltipItem.SetInventoryItem(slotIndex, player.DRAGON_SOUL_INVENTORY)

	def OnPressEscapeKey(self):
		self.Close()
		return True

	def OnTop(self):
		if None != self.tooltipItem:
			self.tooltipItem.SetTop()
	def OverOutItem(self):
		self.wndItem.SetUsableItem(False)
		if None != self.tooltipItem:
			self.tooltipItem.HideToolTip()

	def OverInItem(self, overSlotPos):
		self.wndItem.DeactivateSlot(overSlotPos)
		overSlotPos = self.__InventoryLocalSlotPosToGlobalSlotPos(player.DRAGON_SOUL_INVENTORY, overSlotPos)
		try:
			self.listHighlightedSlot.remove(overSlotPos)
		except:
			pass

		self.wndItem.SetUsableItem(False)
		self.ShowToolTip(player.DRAGON_SOUL_INVENTORY, overSlotPos)

	def __UseItem(self, slotIndex):
		ItemVNum = player.GetItemIndex(player.DRAGON_SOUL_INVENTORY, slotIndex)
		if 0 == player.GetItemMetinSocket(player.DRAGON_SOUL_INVENTORY, slotIndex, 0):
			self.wndPopupDialog.SetText(localeInfo.DRAGON_SOUL_EXPIRED)
			self.wndPopupDialog.Open()
			return

		self.__EquipItem(slotIndex)

	def __EquipItem(self, slotIndex):
		ItemVNum = player.GetItemIndex(player.DRAGON_SOUL_INVENTORY, slotIndex)
		item.SelectItem(ItemVNum)
		subType = item.GetItemSubType()
		equipSlotPos = player.DRAGON_SOUL_EQUIPMENT_SLOT_START + self.deckPageIndex * player.DRAGON_SOUL_EQUIPMENT_FIRST_SIZE + subType
		srcItemPos = (player.DRAGON_SOUL_INVENTORY, slotIndex)
		dstItemPos = (player.INVENTORY, equipSlotPos)
		self.__OpenQuestionDialog(True, srcItemPos, dstItemPos)

	def SelectItemSlot(self, itemSlotIndex):
		if constInfo.GET_ITEM_QUESTION_DIALOG_STATUS() == 1:
			return

		itemSlotIndex = self.__InventoryLocalSlotPosToGlobalSlotPos(player.DRAGON_SOUL_INVENTORY, itemSlotIndex)

		if app.IsPressed(app.DIK_LALT):
			link = player.GetItemLink(player.DRAGON_SOUL_INVENTORY, itemSlotIndex)
			ime.PasteString(link)	
			return

		if mouseModule.mouseController.isAttached():
			attachedSlotType = mouseModule.mouseController.GetAttachedType()
			attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
			attachedItemVID = mouseModule.mouseController.GetAttachedItemIndex()

			attachedInvenType = player.SlotTypeToInvenType(attachedSlotType)
			if player.SLOT_TYPE_INVENTORY == attachedSlotType:
				if player.IsDSEquipmentSlot(attachedInvenType, attachedSlotPos):
					srcItemPos = (attachedInvenType, attachedSlotPos)
					dstItemPos = (player.DRAGON_SOUL_INVENTORY, itemSlotIndex)
					self.__OpenQuestionDialog(False, srcItemPos, dstItemPos)
				else:
					ITEM_USE = 3
					ITEM_EXTRACT = 31
					item.SelectItem(attachedItemVID)
					if item.GetItemType(attachedItemVID) == ITEM_EXTRACT or\
						item.GetItemType(attachedItemVID) == ITEM_USE and\
						item.GetItemSubType(attachedItemVID) in (item.USE_TIME_CHARGE_PER, item.USE_TIME_CHARGE_FIX):
						net.SendItemUseToItemPacket(attachedInvenType, attachedSlotPos, player.DRAGON_SOUL_INVENTORY, itemSlotIndex)

			elif player.SLOT_TYPE_DRAGON_SOUL_INVENTORY == attachedInvenType:
				net.SendItemUseToItemPacket(attachedInvenType, attachedSlotPos, player.DRAGON_SOUL_INVENTORY, itemSlotIndex)

			mouseModule.mouseController.DeattachObject()

		else:
			curCursorNum = app.GetCursor()

			if app.SELL == curCursorNum:
				self.__SellItem(itemSlotIndex)
			elif app.BUY == curCursorNum:
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.SHOP_BUY_INFO)
			elif app.IsPressed(app.DIK_LCONTROL):
				itemIndex = player.GetItemIndex(itemSlotIndex)
				
			else:
				selectedItemVNum = player.GetItemIndex(player.DRAGON_SOUL_INVENTORY, itemSlotIndex)
				itemCount = player.GetItemCount(player.DRAGON_SOUL_INVENTORY, itemSlotIndex)
				mouseModule.mouseController.AttachObject(self, player.SLOT_TYPE_DRAGON_SOUL_INVENTORY, itemSlotIndex, selectedItemVNum, itemCount)
				self.wndItem.SetUseMode(False)
				snd.PlaySound("sound/ui/pick.wav")

	def __SellItem(self, itemSlotPos):
		if not player.IsDSEquipmentSlot(player.DRAGON_SOUL_INVENTORY, itemSlotPos):
			self.sellingSlotNumber = itemSlotPos
			itemIndex = player.GetItemIndex(player.DRAGON_SOUL_INVENTORY, itemSlotPos)
			itemCount = player.GetItemCount(player.DRAGON_SOUL_INVENTORY, itemSlotPos)

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
				itemPrice = itemCount // itemPrice / 2
			else:
				itemPrice = itemPrice * itemCount  // 2

			item.GetItemName(itemIndex)
			itemName = item.GetItemName()

			self.questionDialog = uiCommon.QuestionDialog()
			self.questionDialog.SetText(localeInfo.DO_YOU_SELL_ITEM(itemName, itemCount, itemPrice))
			self.questionDialog.SetAcceptEvent(ui.__mem_func__(self.SellItem))
			self.questionDialog.SetCancelEvent(ui.__mem_func__(self.OnCloseQuestionDialog))
			self.questionDialog.Open()
			self.questionDialog.count = itemCount

	def SellItem(self):

		net.SendShopSellPacketNew(self.sellingSlotNumber, self.questionDialog.count, player.DRAGON_SOUL_INVENTORY)
		snd.PlaySound("sound/ui/money.wav")
		self.OnCloseQuestionDialog()

	def OnCloseQuestionDialog(self):
		if self.questionDialog:
			self.questionDialog.Close()

		self.questionDialog = None

	def __OnClosePopupDialog(self):
		self.pop = None

	def SelectEmptySlot(self, selectedSlotPos):
		if constInfo.GET_ITEM_QUESTION_DIALOG_STATUS() == 1:
			return

		selectedSlotPos = self.__InventoryLocalSlotPosToGlobalSlotPos(player.DRAGON_SOUL_INVENTORY, selectedSlotPos)
		if mouseModule.mouseController.isAttached():

			attachedSlotType = mouseModule.mouseController.GetAttachedType()
			attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
			attachedItemCount = mouseModule.mouseController.GetAttachedItemCount()
			attachedItemIndex = mouseModule.mouseController.GetAttachedItemIndex()

			attachedInvenType = player.SlotTypeToInvenType(attachedSlotType)

			if player.SLOT_TYPE_PRIVATE_SHOP == attachedSlotType:
				mouseModule.mouseController.RunCallBack("INVENTORY")

			elif player.SLOT_TYPE_SHOP == attachedSlotType:
				net.SendShopBuyPacket(attachedSlotPos)

			elif player.SLOT_TYPE_SAFEBOX == attachedSlotType:
				if player.ITEM_MONEY == attachedItemIndex:
					net.SendSafeboxWithdrawMoneyPacket(mouseModule.mouseController.GetAttachedItemCount())
					snd.PlaySound("sound/ui/money.wav")

				else:
					net.SendSafeboxCheckoutPacket(attachedSlotPos, player.DRAGON_SOUL_INVENTORY, selectedSlotPos)

			elif player.SLOT_TYPE_MALL == attachedSlotType:
				net.SendMallCheckoutPacket(attachedSlotPos, player.DRAGON_SOUL_INVENTORY, selectedSlotPos)

			elif player.SLOT_TYPE_INVENTORY == attachedSlotType:
				if player.IsDSEquipmentSlot(attachedInvenType, attachedSlotPos):
					srcItemPos = (attachedInvenType, attachedSlotPos)
					dstItemPos = (player.DRAGON_SOUL_INVENTORY, selectedSlotPos)
					self.__OpenQuestionDialog(False, srcItemPos, dstItemPos)

			elif player.SLOT_TYPE_DRAGON_SOUL_INVENTORY == attachedSlotType:
				itemCount = player.GetItemCount(attachedInvenType, attachedSlotPos)
				attachedCount = mouseModule.mouseController.GetAttachedItemCount()

				self.__SendMoveItemPacket(player.DRAGON_SOUL_INVENTORY, attachedSlotPos, player.DRAGON_SOUL_INVENTORY, selectedSlotPos, attachedCount)

			mouseModule.mouseController.DeattachObject()

	def UseItemSlot(self, slotIndex):
		if constInfo.GET_ITEM_QUESTION_DIALOG_STATUS():
			return

		slotIndex = self.__InventoryLocalSlotPosToGlobalSlotPos(player.DRAGON_SOUL_INVENTORY, slotIndex)
		try:
			if self.wndDragonSoulRefine.IsShow():
				if uiPrivateShopBuilder.IsBuildingPrivateShop():
					chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.MOVE_ITEM_FAILURE_PRIVATE_SHOP)
					return
				self.wndDragonSoulRefine.AutoSetItem((player.DRAGON_SOUL_INVENTORY, slotIndex), 1)
				return
		except:
			pass

		self.__UseItem(slotIndex)

		mouseModule.mouseController.DeattachObject()
		self.OverOutItem()

	def UseItemFastSlot(self, slotIndex):
		if constInfo.GET_ITEM_QUESTION_DIALOG_STATUS():
			return

		try:
			if self.wndDragonSoulRefine.IsShow():
				if uiPrivateShopBuilder.IsBuildingPrivateShop():
					chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.MOVE_ITEM_FAILURE_PRIVATE_SHOP)
					return
				self.wndDragonSoulRefine.AutoSetItem((player.DRAGON_SOUL_INVENTORY, slotIndex), 1)
		except:
			pass

	def UseItemFastSlotTest(self, slot):
		if self.inventoryPageIndex >= 0:
			return self.__InventoryLocalSlotPosToGlobalSlotPos(player.DRAGON_SOUL_INVENTORY, slot)

	def InventoryPageIndexDS(self):
		return self.inventoryPageIndex

	def __SendMoveItemPacket(self, srcSlotWindow, srcSlotPos, dstSlotWindow, dstSlotPos, srcItemCount):
		if uiPrivateShopBuilder.IsBuildingPrivateShop():
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.MOVE_ITEM_FAILURE_PRIVATE_SHOP)
			return
		net.SendItemMovePacket(srcSlotWindow , srcSlotPos, dstSlotWindow, dstSlotPos, srcItemCount)

	def OverOutEquipItem(self):
		self.OverOutItem()

	def OverInEquipItem(self, overSlotPos):
		overSlotPos = self.__InventoryLocalSlotPosToGlobalSlotPos(player.INVENTORY, overSlotPos)
		self.wndItem.SetUsableItem(False)
		self.ShowToolTip(player.INVENTORY, overSlotPos)

	def UseEquipItemSlot(self, slotIndex):
		if constInfo.GET_ITEM_QUESTION_DIALOG_STATUS():
			return

		slotIndex = self.__InventoryLocalSlotPosToGlobalSlotPos(player.INVENTORY, slotIndex)

		self.__UseEquipItem(slotIndex)
		mouseModule.mouseController.DeattachObject()
		self.OverOutEquipItem()

	def __UseEquipItem(self, slotIndex):
		if uiPrivateShopBuilder.IsBuildingPrivateShop():
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.USE_ITEM_FAILURE_PRIVATE_SHOP)
			return

		self.__OpenQuestionDialog(False, (player.INVENTORY, slotIndex), (1, 1))


	def SelectEquipItemSlot(self, itemSlotIndex):

		curCursorNum = app.GetCursor()
		if app.SELL == curCursorNum:
			return
		elif app.BUY == curCursorNum:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.SHOP_BUY_INFO)
			return

		elif app.IsPressed(app.DIK_LALT):
			link = player.GetItemLink(player.INVENTORY, itemSlotIndex)
			ime.PasteString(link)	
			return

		if constInfo.GET_ITEM_QUESTION_DIALOG_STATUS() == 1:
			return

		itemSlotIndex = self.__InventoryLocalSlotPosToGlobalSlotPos(player.INVENTORY, itemSlotIndex)

		if mouseModule.mouseController.isAttached():
			attachedSlotType = mouseModule.mouseController.GetAttachedType()
			attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
			if player.SLOT_TYPE_INVENTORY == attachedSlotType and itemSlotIndex == attachedSlotPos:
				mouseModule.mouseController.DeattachObject()
				return

			attachedItemVID = mouseModule.mouseController.GetAttachedItemIndex()
			attachedInvenType = player.SlotTypeToInvenType(attachedSlotType)
			if player.SLOT_TYPE_INVENTORY == attachedSlotType:
				ITEM_USE = 3
				ITEM_EXTRACT = 31
				item.SelectItem(attachedItemVID)
				if item.GetItemType(attachedItemVID) == ITEM_EXTRACT or\
					item.GetItemType(attachedItemVID) == ITEM_USE and\
					item.GetItemSubType(attachedItemVID) in (item.USE_TIME_CHARGE_PER, item.USE_TIME_CHARGE_FIX):
					net.SendItemUseToItemPacket(attachedInvenType, attachedSlotPos, player.INVENTORY, itemSlotIndex)

			mouseModule.mouseController.DeattachObject()
		else:
			selectedItemVNum = player.GetItemIndex(player.INVENTORY, itemSlotIndex)
			itemCount = player.GetItemCount(player.INVENTORY, itemSlotIndex)
			mouseModule.mouseController.AttachObject(self, player.SLOT_TYPE_INVENTORY, itemSlotIndex, selectedItemVNum, itemCount)
			self.wndItem.SetUseMode(False)
			snd.PlaySound("sound/ui/pick.wav")

	def SelectEmptyEquipSlot(self, selectedSlot):
		if constInfo.GET_ITEM_QUESTION_DIALOG_STATUS() == 1:
			return

		selectedSlotPos = self.__InventoryLocalSlotPosToGlobalSlotPos(player.INVENTORY, selectedSlot)

		if mouseModule.mouseController.isAttached():
			attachedSlotType = mouseModule.mouseController.GetAttachedType()
			attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
			attachedItemCount = mouseModule.mouseController.GetAttachedItemCount()
			attachedItemIndex = mouseModule.mouseController.GetAttachedItemIndex()

			if player.SLOT_TYPE_DRAGON_SOUL_INVENTORY == attachedSlotType:
				if 0 == player.GetItemMetinSocket(player.DRAGON_SOUL_INVENTORY, attachedSlotPos, 0):
					self.wndPopupDialog.SetText(localeInfo.DRAGON_SOUL_EXPIRED)
					self.wndPopupDialog.Open()
					return

				item.SelectItem(attachedItemIndex)
				subType = item.GetItemSubType()
				if subType != (selectedSlot - player.DRAGON_SOUL_EQUIPMENT_SLOT_START):
					self.wndPopupDialog.SetText(localeInfo.DRAGON_SOUL_UNMATCHED_SLOT)
					self.wndPopupDialog.Open()
				else:
					srcItemPos = (player.DRAGON_SOUL_INVENTORY, attachedSlotPos)
					dstItemPos = (player.INVENTORY, selectedSlotPos)
					self.__OpenQuestionDialog(True, srcItemPos, dstItemPos)

			mouseModule.mouseController.DeattachObject()

	def __OpenQuestionDialog(self, Equip, srcItemPos, dstItemPos):
		self.srcItemPos = srcItemPos
		self.dstItemPos = dstItemPos

		self.dlgQuestion.SetAcceptEvent(ui.__mem_func__(self.__Accept))
		self.dlgQuestion.SetCancelEvent(ui.__mem_func__(self.__Cancel))

		if Equip:
			self.dlgQuestion.SetText1(localeInfo.DRAGON_SOUL_EQUIP_WARNING1)
			self.dlgQuestion.SetText2(localeInfo.DRAGON_SOUL_EQUIP_WARNING2)
		else:
			self.dlgQuestion.SetText1(localeInfo.DRAGON_SOUL_UNEQUIP_WARNING1)
			self.dlgQuestion.SetText2(localeInfo.DRAGON_SOUL_UNEQUIP_WARNING2)

		self.dlgQuestion.Open()

	def __Accept(self):
		if (-1, -1) == self.dstItemPos:
			net.SendItemUsePacket(*self.srcItemPos)
		else:
			self.__SendMoveItemPacket(*(self.srcItemPos + self.dstItemPos + (0,)))
		self.dlgQuestion.Close()

	def __Cancel(self):
		self.srcItemPos = (0, 0)
		self.dstItemPos = (0, 0)
		self.dlgQuestion.Close()


	def SetDSKindIndex(self, kindIndex):
		if self.DSKindIndex != kindIndex:
			self.__HighlightSlot_ClearCurrentPage()

		self.DSKindIndex = kindIndex

		for (tabKey, tabButton) in self.tabButtonDict.items():
			if kindIndex!=tabKey:
				tabButton.SetUp()

		for tabValue in self.tabDict.values():
			tabValue.Hide()

		self.tabDict[kindIndex].Show()
		self.tabText.SetText(DragonSoulWindow.KIND_TAP_TITLES[kindIndex])

		self.RefreshBagSlotWindow()

	def SetDeckPage(self, page):
		if page == self.deckPageIndex:
			return

		if self.isActivated:
			self.DeactivateDragonSoul()
			net.SendChatPacket("/dragon_soul deactivate")
		self.deckPageIndex = page
		self.deckTab[page].Down()
		self.deckTab[(page+1)%2].SetUp()

		self.RefreshEquipSlotWindow()

	def ActivateDragonSoulByExtern(self, deck):
		self.isActivated = True
		self.activateButton.Down()
		self.deckPageIndex = deck
		self.deckTab[deck].Down()
		self.deckTab[(deck+1)%2].SetUp()
		self.RefreshEquipSlotWindow()
		self.ActivateEquipSlotWindow(deck)
		if self.interface:
			self.interface.UseDSSButtonEffect(self.isActivated)

	def DeactivateDragonSoul(self):
		self.isActivated = False
		self.activateButton.SetUp()
		self.DeactivateEquipSlotWindow()
		if self.interface:
			self.interface.UseDSSButtonEffect(self.isActivated)

	def DoRenew(self):
		net.SendChatPacket("/renew_ds")

	def ActivateButtonClick(self):
		self.isActivated = self.isActivated ^ True
		if self.isActivated:
			if self.__CanActivateDeck():
				net.SendChatPacket("/dragon_soul activate " + str(self.deckPageIndex))
			else:
				self.isActivated = False
				self.activateButton.SetUp()
		else:
			net.SendChatPacket("/dragon_soul deactivate")

	def __CanActivateDeck(self):
		canActiveNum = 0
		for i in range(6):
			slotNumber = self.__InventoryLocalSlotPosToGlobalSlotPos(player.INVENTORY, player.DRAGON_SOUL_EQUIPMENT_SLOT_START + i)
			itemVnum = player.GetItemIndex(slotNumber)

			if itemVnum != 0:
				item.SelectItem(itemVnum)
				isNoLimit = True
				for i in range(item.LIMIT_MAX_NUM):
					(limitType, limitValue) = item.GetLimit(i)

					if item.LIMIT_TIMER_BASED_ON_WEAR == limitType:
						isNoLimit = False
						remain_time = player.GetItemMetinSocket(player.INVENTORY, slotNumber, 0)
						if 0 != remain_time:
							canActiveNum += 1
							break
				if isNoLimit:
					canActiveNum += 1

		return canActiveNum > 0


	def __HighlightSlot_ClearCurrentPage(self):
		for i in range(self.wndItem.GetSlotCount()):
			slotNumber = self.__InventoryLocalSlotPosToGlobalSlotPos(player.DRAGON_SOUL_INVENTORY, i)
			if slotNumber in self.listHighlightedSlot:
				self.wndItem.DeactivateSlot(i)
				self.listHighlightedSlot.remove(slotNumber)

	def __HighlightSlot_RefreshCurrentPage(self):
		for i in range(self.wndItem.GetSlotCount()):
			slotNumber = self.__InventoryLocalSlotPosToGlobalSlotPos(player.DRAGON_SOUL_INVENTORY, i)
			if slotNumber in self.listHighlightedSlot:
				self.wndItem.ActivateSlot(i)

	def HighlightSlot(self, slot):
		if not slot in self.listHighlightedSlot:
			self.listHighlightedSlot.append (slot)

	def SetDragonSoulRefineWindow(self, wndDragonSoulRefine):
		if app.ENABLE_DRAGON_SOUL_SYSTEM:
			from _weakref import proxy
			self.wndDragonSoulRefine = proxy(wndDragonSoulRefine)

	def MouseSlotEventRefresh(self):
		for i in range(self.wndItem.GetSlotCount()):
			slotNumber = self.__InventoryLocalSlotPosToGlobalSlotPos(player.DRAGON_SOUL_INVENTORY, i)
			if slotNumber in self.listCantMouseSlot:
				self.wndItem.SetCantMouseEventSlot(i)
					
	def MouseSlotEventClear(self):
		for i in range(self.wndItem.GetSlotCount()):
			slotNumber = self.__InventoryLocalSlotPosToGlobalSlotPos(player.DRAGON_SOUL_INVENTORY, i)
			if slotNumber in self.listCantMouseSlot:
				self.wndItem.SetCanMouseEventSlot(i)
				self.listCantMouseSlot.remove(slotNumber)
					
	def SetCantMouseSlot(self, slot):
		if slot > player.DRAGON_SOUL_PAGE_SIZE:
			return
		
		if not slot in self.listCantMouseSlot:
			self.listCantMouseSlot.append(slot)

	def SetCanMouseSlot(self, inventorylocalslot):
		if inventorylocalslot in self.listCantMouseSlot:
			if inventorylocalslot >= player.DRAGON_SOUL_PAGE_SIZE*self.inventoryPageIndex:
				self.wndItem.SetCanMouseEventSlot(inventorylocalslot-player.DRAGON_SOUL_PAGE_SIZE*self.inventoryPageIndex)
			else:
				self.wndItem.SetCanMouseEventSlot(inventorylocalslot)

			self.listCantMouseSlot.remove(inventorylocalslot)
			
	def BindInterfaceClass(self, interface):
		from _weakref import proxy
		self.interface = proxy(interface)

	def OnUpdate(self):
		if self.renewbtn.IsIn():
			self.toolTip[1].Show()
		else:
			self.toolTip[1].Hide()
			


class DragonSoulRefineWindow(ui.ScriptWindow):
	REFINE_TYPE_GRADE, REFINE_TYPE_STEP, REFINE_TYPE_STRENGTH = range(3)
	DS_SUB_HEADER_DIC = {
		REFINE_TYPE_GRADE : player.DS_SUB_HEADER_DO_REFINE_GRADE,
		REFINE_TYPE_STEP : player.DS_SUB_HEADER_DO_REFINE_STEP,
		REFINE_TYPE_STRENGTH : player.DS_SUB_HEADER_DO_REFINE_STRENGTH
	}
	if app.ENABLE_DS_CHANGE_ATTR:
		REFINE_TYPE_CHANGE_ATTR = 3
		DS_SUB_HEADER_DIC.update({ REFINE_TYPE_CHANGE_ATTR : player.DS_SUB_HEADER_DO_CHANGE_ATTR })
	REFINE_STONE_SLOT, DRAGON_SOUL_SLOT = range(2)

	INVALID_DRAGON_SOUL_INFO = -1

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.tooltipItem = None
		self.sellingSlotNumber = -1
		self.isLoaded = 0
		self.refineChoiceButtonDict = None
		if app.ENABLE_DS_CHANGE_ATTR:
			self.refineChoiceButtonTitleDict = None
		self.doRefineButton = None

		self.doFastRefineButton = None
		self.FastRefine = False
		self.FastRefineTime = 0
		self.lastFastRefineCount = 0
		self.fastRefineLockedKey = None

		self.wndMoney = None

		self.wndPercent = None
		self.firstItem = -1
		self.secondItem = -1

		self.SetWindowName("DragonSoulRefineWindow")
		self.__LoadWindow()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def Show(self):
		self.__LoadWindow()
		ui.ScriptWindow.Show(self)

	def __LoadWindow(self):
		if self.isLoaded == 1:
			return
		self.isLoaded = 1
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "uiscript/dragonsoulrefinewindow.py")

		except:
			import exception
			exception.Abort("dragonsoulrefinewindow.LoadWindow.LoadObject")
		try:
			wndRefineSlot = self.GetChild("RefineSlot")
			wndResultSlot = self.GetChild("ResultSlot")
			self.wndPercent = self.GetChild("Percent_Text")
			self.GetChild("TitleBar").SetCloseEvent(ui.__mem_func__(self.Close))
			self.refineChoiceButtonDict = {
				self.REFINE_TYPE_GRADE	: self.GetChild("GradeButton"),
				self.REFINE_TYPE_STEP: self.GetChild("StepButton"),
				self.REFINE_TYPE_STRENGTH	: self.GetChild("StrengthButton"),
			}
			self.doRefineButton = self.GetChild("DoRefineButton")
			self.doFastRefineButton = self.GetChild("DoFastRefineButton")
			self.wndMoney = self.GetChild("Money_Slot")
			self.DoRefineWithEnter = self.GetChild("DoRefineWithEnter")
			if app.ENABLE_DS_CHANGE_ATTR:
				self.refineChoiceButtonTitleDict = {
					self.REFINE_TYPE_GRADE : self.GetChild("GradeSlotTitle"),
					self.REFINE_TYPE_STEP : self.GetChild("StepSlotTitle"),
					self.REFINE_TYPE_STRENGTH : self.GetChild("RefineSlotTitle")
				}

		except:
			import exception
			exception.Abort("DragonSoulRefineWindow.LoadWindow.BindObject")

		self.DoRefineWithEnter.SetToggleUpEvent(ui.__mem_func__(self.__OnClickEnableRefineWithEnter))
		self.DoRefineWithEnter.SetToggleDownEvent(ui.__mem_func__(self.__OnClickEnableRefineWithEnter))
		if constInfo.IS_DRAGON_SOUL_OPEN == True:
			self.DoRefineWithEnter.Down()

		wndRefineSlot.SetOverInItemEvent(ui.__mem_func__(self.__OverInRefineItem))
		wndRefineSlot.SetOverOutItemEvent(ui.__mem_func__(self.__OverOutItem))
		wndRefineSlot.SetSelectEmptySlotEvent(ui.__mem_func__(self.__SelectRefineEmptySlot))
		wndRefineSlot.SetSelectItemSlotEvent(ui.__mem_func__(self.__SelectRefineItemSlot))
		wndRefineSlot.SetUseSlotEvent(ui.__mem_func__(self.__SelectRefineItemSlot))
		wndRefineSlot.SetUnselectItemSlotEvent(ui.__mem_func__(self.__SelectRefineItemSlot))

		wndResultSlot.SetOverInItemEvent(ui.__mem_func__(self.__OverInResultItem))
		wndResultSlot.SetOverOutItemEvent(ui.__mem_func__(self.__OverOutItem))
		self.wndRefineSlot = wndRefineSlot
		self.wndResultSlot = wndResultSlot

		self.refineChoiceButtonDict[self.REFINE_TYPE_GRADE].SetToggleDownEvent(self.__ToggleDownGradeButton)
		self.refineChoiceButtonDict[self.REFINE_TYPE_STEP].SetToggleDownEvent(self.__ToggleDownStepButton)
		self.refineChoiceButtonDict[self.REFINE_TYPE_STRENGTH].SetToggleDownEvent(self.__ToggleDownStrengthButton)
		self.refineChoiceButtonDict[self.REFINE_TYPE_GRADE].SetToggleUpEvent(lambda : self.__ToggleUpButton(self.REFINE_TYPE_GRADE))
		self.refineChoiceButtonDict[self.REFINE_TYPE_STEP].SetToggleUpEvent(lambda : self.__ToggleUpButton(self.REFINE_TYPE_STEP))
		self.refineChoiceButtonDict[self.REFINE_TYPE_STRENGTH].SetToggleUpEvent(lambda : self.__ToggleUpButton(self.REFINE_TYPE_STRENGTH))
		self.doRefineButton.SetEvent(self.PressDoRefineButton)
		self.doFastRefineButton.SetEvent(self.__PressDoFastRefineButton)

		self.wndPopupDialog = uiCommon.PopupDialog()

		self.currentRefineType = self.REFINE_TYPE_GRADE
		self.refineItemInfo = {}
		self.fasolka = {}
		self.resultItemInfo = {}
		self.currentRecipe = {}

		self.wndMoney.SetText(localeInfo.NumberToMoneyString(0))

		self.wndPercent.SetText(localeInfo.DRAGONSOUL_CHANCE.format(0))

		self.refineChoiceButtonDict[self.REFINE_TYPE_GRADE].Down()

		self.__Initialize()

	def __OnClickEnableRefineWithEnter(self):
		if constInfo.IS_DRAGON_SOUL_OPEN == False:
			constInfo.IS_DRAGON_SOUL_OPEN = True
		else:
			constInfo.IS_DRAGON_SOUL_OPEN = False

	def Destroy(self):
		self.ClearDictionary()
		self.tooltipItem = None
		self.wndItem = 0
		self.wndEquip = 0
		self.activateButton = 0
		self.questionDialog = None
		self.mallButton = None
		self.inventoryTab = []
		self.deckTab = []
		self.equipmentTab = []
		self.tabDict = None
		self.tabButtonDict = None

		self.FastRefine = False
		self.FastRefineTime = 0

	def Close(self):
		self.fasolka = {}
		constInfo.IS_DRAGON_SOUL_OPEN = False
		self.FastRefine = False
		self.FastRefineTime = 0

		if None != self.tooltipItem:
			self.tooltipItem.HideToolTip()

		self.__FlushRefineItemSlot()
		player.SendDragonSoulRefine(player.DRAGON_SOUL_REFINE_CLOSE)
		self.Hide()

	def Show(self):
		constInfo.IS_DRAGON_SOUL_OPEN = True
		if app.ENABLE_DS_CHANGE_ATTR:
			ui.ScriptWindow.Show(self)
			return
		self.currentRefineType = self.REFINE_TYPE_GRADE
		self.wndMoney.SetText(localeInfo.NumberToMoneyString(0))
		self.wndPercent.SetText(localeInfo.DRAGONSOUL_CHANCE.format(0))
		self.refineChoiceButtonDict[self.REFINE_TYPE_GRADE].Down()
		self.refineChoiceButtonDict[self.REFINE_TYPE_STEP].SetUp()
		self.refineChoiceButtonDict[self.REFINE_TYPE_STRENGTH].SetUp()

		self.Refresh()

		ui.ScriptWindow.Show(self)

	def SetItemToolTip(self, tooltipItem):
		self.tooltipItem = tooltipItem

	def __Initialize(self):
		self.currentRecipe = {}
		self.refineItemInfo = {}
		self.resultItemInfo = {}

		if self.REFINE_TYPE_STRENGTH == self.currentRefineType:
			self.refineSlotLockStartIndex = 2
		else:
			self.refineSlotLockStartIndex = 1

		for i in range(self.refineSlotLockStartIndex):
			self.wndRefineSlot.HideSlotBaseImage(i)

		self.wndMoney.SetText(localeInfo.NumberToMoneyString(0))
		self.wndPercent.SetText(localeInfo.DRAGONSOUL_CHANCE.format(0))

	def __FlushRefineItemSlot(self):
		if app.ENABLE_DS_CHANGE_ATTR:
			if DragonSoulRefineWindow.REFINE_TYPE_CHANGE_ATTR == self.currentRefineType:
				if self.refineItemInfo:
					invenType, invenPos, itemCount = self.refineItemInfo[self.REFINE_STONE_SLOT]
					remainCount = player.GetItemCount(invenType, invenPos)
					player.SetItemCount(invenType, invenPos, remainCount + itemCount)

				self.__Initialize()
				return
		for invenType, invenPos, itemCount in self.refineItemInfo.values():
			remainCount = player.GetItemCount(invenType, invenPos)
			player.SetItemCount(invenType, invenPos, remainCount + itemCount)
		self.__Initialize()

	def __ToggleUpButton(self, idx):
		self.refineChoiceButtonDict[idx].Down()

	def __ToggleDownGradeButton(self):
		if self.REFINE_TYPE_GRADE == self.currentRefineType:
			return
		self.refineChoiceButtonDict[self.currentRefineType].SetUp()
		self.currentRefineType = self.REFINE_TYPE_GRADE
		self.__FlushRefineItemSlot()
		self.Refresh()

	def __ToggleDownStepButton(self):
		if self.REFINE_TYPE_STEP == self.currentRefineType:
			return
		self.refineChoiceButtonDict[self.currentRefineType].SetUp()
		self.currentRefineType = self.REFINE_TYPE_STEP
		self.__FlushRefineItemSlot()
		self.Refresh()

	def __ToggleDownStrengthButton(self):
		if self.REFINE_TYPE_STRENGTH == self.currentRefineType:
			return
		self.refineChoiceButtonDict[self.currentRefineType].SetUp()
		self.currentRefineType = self.REFINE_TYPE_STRENGTH
		self.__FlushRefineItemSlot()
		self.Refresh()

	def __PopUp(self, message):
		self.wndPopupDialog.SetText(message)
		self.wndPopupDialog.Open()


	def __SetItem(self, inven, dstSlotIndex, itemCount):
		invenType, invenPos = inven
	
		if app.ENABLE_DS_CHANGE_ATTR:
			if DragonSoulRefineWindow.REFINE_TYPE_CHANGE_ATTR == self.currentRefineType:
				# For attribute change: slot 0 = dragon soul, slot 1 = material
				if dstSlotIndex >= 2:  # Only allow 2 slots for attribute change
					return False
			else:
				if dstSlotIndex >= self.refineSlotLockStartIndex:
					return False
		else:
			if dstSlotIndex >= self.refineSlotLockStartIndex:
				return False
	
		itemVnum = player.GetItemIndex(invenType, invenPos)
		maxCount = player.GetItemCount(invenType, invenPos)
	
		if itemCount > maxCount:
			raise Exception(("Invalid attachedItemCount(%d). (base pos (%d, %d), base itemCount(%d))" % (itemCount, invenType, invenPos, maxCount))
)
	
		if DragonSoulRefineWindow.REFINE_TYPE_STRENGTH == self.currentRefineType:
			if self.__IsDragonSoul(itemVnum):
				dstSlotIndex = 1
			else:
				dstSlotIndex = 0
		elif app.ENABLE_DS_CHANGE_ATTR and DragonSoulRefineWindow.REFINE_TYPE_CHANGE_ATTR == self.currentRefineType:
			# For attribute change: determine slot based on item type
			if self.__IsDragonSoul(itemVnum):
				dstSlotIndex = 0  # Dragon soul goes to slot 0
			else:
				dstSlotIndex = 1  # Material goes to slot 1
	
		if dstSlotIndex in self.refineItemInfo:
			return False
	
		if False == self.__CheckCanRefine(itemVnum):
			return False
	
		player.SetItemCount(invenType, invenPos, maxCount - itemCount)
		self.refineItemInfo[dstSlotIndex] = (invenType, invenPos, itemCount)
		if itemVnum == 100300 or itemVnum == 100400 or itemVnum == 100500:
			self.fasolka = (invenType, invenPos, itemCount)
		self.Refresh()
	
		return True

	def __CheckCanRefine(self, vnum):
		if app.ENABLE_DS_CHANGE_ATTR:
			if self.REFINE_TYPE_CHANGE_ATTR == self.currentRefineType:
				return self.__CanRefineChangeAttr(vnum)
		if self.REFINE_TYPE_GRADE == self.currentRefineType:
			return self.__CanRefineGrade(vnum)

		elif self.REFINE_TYPE_STEP == self.currentRefineType:
			return self.__CanRefineStep(vnum)

		elif self.REFINE_TYPE_STRENGTH == self.currentRefineType:
			return self.__CanRefineStrength(vnum)

		else:
			return False

	def __CanRefineGrade(self, vnum):
		ds_info = self.__GetDragonSoulTypeInfo(vnum)

		if DragonSoulRefineWindow.INVALID_DRAGON_SOUL_INFO == ds_info:
			self.__PopUp(localeInfo.DRAGON_SOUL_IS_NOT_DRAGON_SOUL)
			return False

		if self.currentRecipe:
			ds_type, grade, step, strength = ds_info
			cur_refine_ds_type, cur_refine_grade, cur_refine_step, cur_refine_strength = self.currentRecipe["ds_info"]
			if not (cur_refine_ds_type == ds_type and cur_refine_grade == grade):
				self.__PopUp(localeInfo.DRAGON_SOUL_INVALID_DRAGON_SOUL)
				return False
		else:
			self.currentRecipe = self.__GetRefineGradeRecipe(vnum)

			if self.currentRecipe:
				self.refineSlotLockStartIndex = self.currentRecipe["need_count"]
				self.wndMoney.SetText(localeInfo.NumberToMoneyString(self.currentRecipe["fee"]))
				self.wndPercent.SetText(localeInfo.DRAGONSOUL_CHANCE.format(self.currentRecipe["percent"]))
				return True
			else:
				self.__PopUp(localeInfo.DRAGON_SOUL_CANNOT_REFINE)
				return False

	def __CanRefineStep (self, vnum):
		ds_info = self.__GetDragonSoulTypeInfo(vnum)

		if DragonSoulRefineWindow.INVALID_DRAGON_SOUL_INFO == ds_info:
			self.__PopUp(localeInfo.DRAGON_SOUL_IS_NOT_DRAGON_SOUL)
			return False

		if self.currentRecipe:
			ds_type, grade, step, strength = ds_info
			cur_refine_ds_type, cur_refine_grade, cur_refine_step, cur_refine_strength = self.currentRecipe["ds_info"]
			if not (cur_refine_ds_type == ds_type and cur_refine_grade == grade and cur_refine_step == step):
				self.__PopUp(localeInfo.DRAGON_SOUL_INVALID_DRAGON_SOUL)
				return False
		else:
			self.currentRecipe = self.__GetRefineStepRecipe(vnum)

			if self.currentRecipe:
				self.refineSlotLockStartIndex = self.currentRecipe["need_count"]
				self.wndMoney.SetText(localeInfo.NumberToMoneyString(self.currentRecipe["fee"]))
				self.wndPercent.SetText(localeInfo.DRAGONSOUL_CHANCE.format(self.currentRecipe["percent"]))
				return True

			else:
				self.__PopUp(localeInfo.DRAGON_SOUL_CANNOT_REFINE)
				return False

	def __CanRefineStrength (self, vnum):
		if self.__IsDragonSoul(vnum):
			ds_type, grade, step, strength = self.__GetDragonSoulTypeInfo(vnum)

			import dragon_soul_refine_settings
			if strength >= dragon_soul_refine_settings.dragon_soul_refine_info[ds_type]["strength_max_table"][grade][step]:
				self.__PopUp(localeInfo.DRAGON_SOUL_CANNOT_REFINE_MORE)
				return False

			else:
				self.AppendStrengthPercent(strength = strength)
				return True

		else:
			if self.currentRecipe:
				self.__PopUp(localeInfo.DRAGON_SOUL_IS_NOT_DRAGON_SOUL)
				return False
			else:
				refineRecipe = self.__GetRefineStrengthInfo(vnum)
				if refineRecipe:
					self.currentRecipe = refineRecipe
					self.wndMoney.SetText(localeInfo.NumberToMoneyString(self.currentRecipe["fee"]))
					self.AppendStrengthPercent(vnum = vnum)
					return True
				else:
					self.__PopUp(localeInfo.DRAGON_SOUL_NOT_DRAGON_SOUL_REFINE_STONE)
					return False

	def AppendStrengthPercent(self, strength = -1, vnum = -1):
		if strength > -1:
			self.firstItem = strength

		if vnum > -1:
			self.secondItem = vnum

		if self.firstItem >= 0 and self.secondItem > 0:
			percent = self.__GetRefineStrengthPercent(self.firstItem, self.secondItem)

			self.wndPercent.SetText(localeInfo.DRAGONSOUL_CHANCE.format(percent))

	def __GetRefineGradeRecipe (self, vnum):
		ds_type, grade, step, strength = self.__GetDragonSoulTypeInfo(vnum)
		try:
			import dragon_soul_refine_settings

			return	{
				"ds_info"		: (ds_type, grade, step, strength),
				"need_count"	: dragon_soul_refine_settings.dragon_soul_refine_info[ds_type]["grade_need_count"][grade],
				"fee"			: dragon_soul_refine_settings.dragon_soul_refine_info[ds_type]["grade_fee"][grade],
				"percent"		: dragon_soul_refine_settings.dragon_soul_refine_info[ds_type]["grade_percent"][grade]
					}
		except:
			return None

	def __GetRefineStepRecipe (self, vnum):
		ds_type, grade, step, strength = self.__GetDragonSoulTypeInfo(vnum)
		try:
			import dragon_soul_refine_settings

			return	{
				"ds_info"		: (ds_type, grade, step, strength),
				"need_count"	: dragon_soul_refine_settings.dragon_soul_refine_info[ds_type]["step_need_count"][step],
				"fee"			: dragon_soul_refine_settings.dragon_soul_refine_info[ds_type]["step_fee"][step],
				"percent"		: dragon_soul_refine_settings.dragon_soul_refine_info[ds_type]["step_percent"][step]
					}
		except:
			return None

	def __GetRefineStrengthInfo (self, itemVnum):
		try:
			item.SelectItem(itemVnum)
			if not (item.MATERIAL == item.GetItemType() \
					and (item.MATERIAL_DS_REFINE_NORMAL <= item.GetItemSubType() and item.GetItemSubType() <= item.MATERIAL_DS_REFINE_HOLLY)):
				return None

			import dragon_soul_refine_settings
			return { "fee" : dragon_soul_refine_settings.strength_fee[item.GetItemSubType()] }
		except:
			return None

	def __GetRefineStrengthPercent (self, strength, itemVnum):
		try:
			item.SelectItem(itemVnum)
			if not (item.MATERIAL == item.GetItemType() \
					and (item.MATERIAL_DS_REFINE_NORMAL <= item.GetItemSubType() and item.GetItemSubType() <= item.MATERIAL_DS_REFINE_HOLLY)):
				return None

			import dragon_soul_refine_settings

			return dragon_soul_refine_settings.STRENGTH_PERCENTS[item.GetItemSubType()][strength]
		except:
			return None

	def __IsDragonSoul(self, vnum):
		item.SelectItem(vnum)
		return item.GetItemType() == item.DS

	def __GetDragonSoulTypeInfo(self, vnum):
		if not self.__IsDragonSoul(vnum):
			return DragonSoulRefineWindow.INVALID_DRAGON_SOUL_INFO
		ds_type = vnum // 10000
		grade = vnum % 10000 // 1000
		step = vnum % 1000 // 100
		strength = vnum % 100 // 10

		return (ds_type, grade, step, strength)

	def __MakeDragonSoulVnum(self, ds_type, grade, step, strength):
		return ds_type * 10000 + grade * 1000 + step * 100 + strength * 10

	def __SelectRefineEmptySlot(self, selectedSlotPos):
		try:
			if constInfo.GET_ITEM_QUESTION_DIALOG_STATUS() == 1:
				return

			if selectedSlotPos >= self.refineSlotLockStartIndex:
				return

			if mouseModule.mouseController.isAttached():
				attachedSlotType = mouseModule.mouseController.GetAttachedType()
				attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
				attachedItemCount = mouseModule.mouseController.GetAttachedItemCount()
				attachedItemIndex = mouseModule.mouseController.GetAttachedItemIndex()
				mouseModule.mouseController.DeattachObject()

				if uiPrivateShopBuilder.IsBuildingPrivateShop():
					chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.MOVE_ITEM_FAILURE_PRIVATE_SHOP)
					return

				attachedInvenType = player.SlotTypeToInvenType(attachedSlotType)

				if player.INVENTORY == attachedInvenType and player.IsEquipmentSlot(attachedSlotPos):
					return

				if player.INVENTORY != attachedInvenType and player.DRAGON_SOUL_INVENTORY != attachedInvenType:
					return

				if True == self.__SetItem((attachedInvenType, attachedSlotPos), selectedSlotPos, attachedItemCount):
					self.Refresh()

		except Exception as e:
			import dbg
			dbg.TraceError("Exception : __SelectRefineEmptySlot, %s" % e)

	def __SelectRefineItemSlot(self, selectedSlotPos):
		if constInfo.GET_ITEM_QUESTION_DIALOG_STATUS() == 1:
			return

		try:
			if not selectedSlotPos in self.refineItemInfo:
				if mouseModule.mouseController.isAttached():
					attachedSlotType = mouseModule.mouseController.GetAttachedType()
					attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
					attachedItemCount = mouseModule.mouseController.GetAttachedItemCount()
					attachedItemIndex = mouseModule.mouseController.GetAttachedItemIndex()
					mouseModule.mouseController.DeattachObject()

					if uiPrivateShopBuilder.IsBuildingPrivateShop():
						chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.MOVE_ITEM_FAILURE_PRIVATE_SHOP)
						return

					attachedInvenType = player.SlotTypeToInvenType(attachedSlotType)

					if player.INVENTORY == attachedInvenType and player.IsEquipmentSlot(attachedSlotPos):
						return

					if player.INVENTORY != attachedInvenType and player.DRAGON_SOUL_INVENTORY != attachedInvenType:
						return

					self.AutoSetItem((attachedInvenType, attachedSlotPos), 1)
				return
			elif mouseModule.mouseController.isAttached():
				return
			if app.ENABLE_DS_CHANGE_ATTR:
				if DragonSoulRefineWindow.REFINE_TYPE_CHANGE_ATTR == self.currentRefineType:
					if selectedSlotPos == self.DRAGON_SOUL_SLOT:
						return

			attachedInvenType, attachedSlotPos, attachedItemCount = self.refineItemInfo[selectedSlotPos]
			selectedItemVnum = player.GetItemIndex(attachedInvenType, attachedSlotPos)

			invenType, invenPos, itemCount = self.refineItemInfo[selectedSlotPos]
			remainCount = player.GetItemCount(invenType, invenPos)
			player.SetItemCount(invenType, invenPos, remainCount + itemCount)
			if app.ENABLE_DS_CHANGE_ATTR:
				if DragonSoulRefineWindow.REFINE_TYPE_CHANGE_ATTR == self.currentRefineType:
					if selectedSlotPos == self.REFINE_STONE_SLOT:
						self.__Initialize()
						self.Refresh()
						return
			del self.refineItemInfo[selectedSlotPos]

			if not self.refineItemInfo:
				self.__Initialize()
			else:
				item.SelectItem(selectedItemVnum)
				if (item.MATERIAL == item.GetItemType() \
					and (item.MATERIAL_DS_REFINE_NORMAL <= item.GetItemSubType() and item.GetItemSubType() <= item.MATERIAL_DS_REFINE_HOLLY)):
					self.currentRecipe = {}
					self.wndMoney.SetText(localeInfo.NumberToMoneyString(0))
					self.wndPercent.SetText(localeInfo.DRAGONSOUL_CHANCE.format(0))
				else:
					pass

		except Exception as e:
			import dbg
			dbg.TraceError("Exception : __SelectRefineItemSlot, %s" % e)

		self.Refresh()

	def __OverInRefineItem(self, slotIndex):
		if slotIndex in self.refineItemInfo:
			inven_type, inven_pos, item_count = self.refineItemInfo[slotIndex]
			self.tooltipItem.SetInventoryItem(inven_pos, inven_type)

	def __OverInResultItem(self, slotIndex):
		if slotIndex in self.resultItemInfo:
			inven_type, inven_pos, item_count = self.resultItemInfo[slotIndex]
			self.tooltipItem.SetInventoryItem(inven_pos, inven_type)

	def __OverOutItem(self):
		if self.tooltipItem:
			self.tooltipItem.HideToolTip()

	def PressDoRefineButton(self):
		for i in range(self.refineSlotLockStartIndex):
			if not i in self.refineItemInfo:
				self.wndPopupDialog.SetText(localeInfo.DRAGON_SOUL_NOT_ENOUGH_MATERIAL)
				self.wndPopupDialog.Open()

				if self.FastRefine == True:
					self.FastRefine = False

				return
		if app.ENABLE_DS_CHANGE_ATTR:
			if DragonSoulRefineWindow.REFINE_TYPE_CHANGE_ATTR == self.currentRefineType:
				if not self.__CheckDoRefineChangeAttr():
					self.wndPopupDialog.SetText(localeInfo.DRAGON_SOUL_NOT_ENOUGH_MATERIAL)
					self.wndPopupDialog.Open()
					return

		player.SendDragonSoulRefine(DragonSoulRefineWindow.DS_SUB_HEADER_DIC[self.currentRefineType], self.refineItemInfo)

	def __PressDoFastRefineButton(self):
		if self.FastRefine == True:
			self.FastRefine = False
			self.fastRefineLockedKey = None
		else:
			self.FastRefine = True
			self.lastFastRefineCount = 0
			self.fastRefineLockedKey = None

	def __PressDoFastRefineStart(self):
		if not self.wndDragonSoul.IsShow():
			return

		if not self.IsShow():
			return

		if self.REFINE_TYPE_STRENGTH == self.currentRefineType:
			return

		isStepRefine = (self.REFINE_TYPE_STEP == self.currentRefineType)

		# Pass 1 — collect all DS items with their (type, grade, step) info
		items = []
		for i in range(player.DRAGON_SOUL_PAGE_SIZE):
			slotIndex = self.wndDragonSoul.UseItemFastSlotTest(i)
			if slotIndex == -1:
				break
			itemVnum = player.GetItemIndex(player.DRAGON_SOUL_INVENTORY, slotIndex)
			if itemVnum <= 0:
				continue
			ds_type, grade, step, strength = self.__GetDragonSoulTypeInfo(itemVnum)
			if ds_type == 0:
				continue
			items.append((slotIndex, ds_type, grade, step))

		# Pass 2 — group items by compatibility key.
		# STEP refine: key = (type, grade, step) — server requires identical triplet.
		# GRADE refine: key = (type, grade); Legendary (4) only Wyborna (step=4) is eligible.
		groups = {}
		for slotIndex, ds_type, grade, step in items:
			if isStepRefine:
				key = (ds_type, grade, step)
			else:
				if grade == 4 and step != 4:
					continue
				key = (ds_type, grade)
			groups.setdefault(key, []).append(slotIndex)

		# Pass 3 — pick group to refine.
		# Session locks onto the LOWEST tier (step for STEP refine, grade for GRADE) on first call.
		# Stays on that group until exhausted (<2 items left), then stops — user must click again
		# to lock onto the next-lowest available tier.
		chosenSlots = None

		if self.fastRefineLockedKey is not None:
			# Continue with locked group from previous calls in this session.
			chosenSlots = groups.get(self.fastRefineLockedKey)
			if chosenSlots is None or len(chosenSlots) < 2:
				# Locked tier is exhausted. Stop and wait for next user click.
				self.FastRefineCancel()
				return
		else:
			# First call this session — pick lowest tier with >= 2 items.
			# STEP key = (type, grade, step), sort by (step, grade, type).
			# GRADE key = (type, grade), sort by (grade, type).
			if isStepRefine:
				sortFn = lambda k: (k[2], k[1], k[0])
			else:
				sortFn = lambda k: (k[1], k[0])

			for key in sorted(groups.keys(), key=sortFn):
				if len(groups[key]) >= 2:
					self.fastRefineLockedKey = key
					chosenSlots = groups[key]
					break

			if chosenSlots is None:
				self.FastRefineCancel()
				return

		for slotIndex in chosenSlots[:2]:
			self.wndDragonSoul.UseItemFastSlot(slotIndex)

		self.PressDoRefineButton()

	def FastRefineCancel(self):
		if self.FastRefine == True:
			self.FastRefine = False
		self.fastRefineLockedKey = None


	def __CountRefineItem(self):
		if not self.wndDragonSoul.IsShow():
			return 0

		if not self.IsShow():
			return 0


		count = 0

		for i in range(player.DRAGON_SOUL_PAGE_SIZE):
			slotIndex = self.wndDragonSoul.UseItemFastSlotTest(i)

			itemVnum = player.GetItemIndex(player.DRAGON_SOUL_INVENTORY, slotIndex)
			if itemVnum > 0:
				count += 1

		return count

	def OnUpdate(self):
		if constInfo.IS_DRAGON_SOUL_OPEN == True:
			self.DoRefineWithEnter.Down()
		else:
			self.DoRefineWithEnter.SetUp()

		if self.FastRefine == True:
			if (app.GetTime() < self.FastRefineTime + 0.3):
				return

			currentCount = self.__CountRefineItem()

			# Detect stuck state — server rejected previous attempt and items returned to inventory.
			# Without this, e.g. Legendary→Mythical with non-Wyborna stones spams [LS;10069] forever.
			if self.lastFastRefineCount > 0 and currentCount >= self.lastFastRefineCount:
				self.FastRefine = False
				self.lastFastRefineCount = 0
				self.fastRefineLockedKey = None
				self.FastRefineTime = app.GetTime()
				return

			if currentCount >= 2:
				if not self.REFINE_TYPE_STRENGTH == self.currentRefineType:
					self.lastFastRefineCount = currentCount
					self.__PressDoFastRefineStart()
			else:
				self.FastRefine = False
				self.lastFastRefineCount = 0
				self.fastRefineLockedKey = None

			self.FastRefineTime = app.GetTime()

	def OnPressEscapeKey(self):
		self.Close()
		return True

	def Refresh(self):
		if self.REFINE_TYPE_STRENGTH == self.currentRefineType:
			self.doFastRefineButton.Hide()
		else:
			self.doFastRefineButton.Show()

		self.__RefreshRefineItemSlot()
		self.__ClearResultItemSlot()

	def __RefreshRefineItemSlot(self):
		try:
			for slotPos in range(self.wndRefineSlot.GetSlotCount()):
				self.wndRefineSlot.ClearSlot(slotPos)
				
				# Determine how many slots to show based on refine type
				maxSlots = self.refineSlotLockStartIndex
				if app.ENABLE_DS_CHANGE_ATTR and DragonSoulRefineWindow.REFINE_TYPE_CHANGE_ATTR == self.currentRefineType:
					maxSlots = 2  # Always show 2 slots for attribute change
				
				if slotPos < maxSlots:
					if slotPos in self.refineItemInfo:
						invenType, invenPos, itemCount = self.refineItemInfo[slotPos]
						itemVnum = player.GetItemIndex(invenType, invenPos)
	
						if itemVnum:
							self.wndRefineSlot.SetItemSlot(slotPos, player.GetItemIndex(invenType, invenPos), itemCount)
						else:
							del self.refineItemInfo[slotPos]
	
					if not slotPos in self.refineItemInfo:
						try:
							reference_vnum = 0
							if DragonSoulRefineWindow.REFINE_TYPE_STRENGTH == self.currentRefineType:
								if DragonSoulRefineWindow.REFINE_STONE_SLOT == slotPos:
									reference_vnum = 100300
							elif app.ENABLE_DS_CHANGE_ATTR and DragonSoulRefineWindow.REFINE_TYPE_CHANGE_ATTR == self.currentRefineType:
								if 0 == slotPos:  # Dragon soul slot
									if self.currentRecipe:
										reference_vnum = self.__MakeDragonSoulVnum(*self.currentRecipe["ds_info"])
									else:
										reference_vnum = 110000  # Generic myth dragon soul for preview
								elif 1 == slotPos:  # Material slot
									reference_vnum = 100700
							else:
								if self.currentRecipe:
									reference_vnum = self.__MakeDragonSoulVnum(*self.currentRecipe["ds_info"])
									
							if 0 != reference_vnum:
								item.SelectItem(reference_vnum)
								itemIcon = item.GetIconImage()
								(width, height) = item.GetItemSize()
								self.wndRefineSlot.SetSlot(slotPos, 0, width, height, itemIcon, (1.0, 1.0, 1.0, 0.5))
								self.wndRefineSlot.SetSlotCount(slotPos, 0)
						except:
							pass
					self.wndRefineSlot.HideSlotBaseImage(slotPos)
				else:
					if slotPos in self.refineItemInfo:
						invenType, invenPos, itemCount = self.refineItemInfo[slotPos]
						remainCount = player.GetItemCount(invenType, invenPos)
						player.SetItemCount(invenType, invenPos, remainCount + itemCount)
						del self.refineItemInfo[slotPos]
					self.wndRefineSlot.ShowSlotBaseImage(slotPos)
	
			if not self.refineItemInfo:
				self.__Initialize()
	
			self.wndRefineSlot.RefreshSlot()
		except Exception as e:
			import dbg
			dbg.TraceError("Exception : __RefreshRefineItemSlot, %s" % e)

	def __GetEmptySlot(self, itemVnum = 0):
		if DragonSoulRefineWindow.REFINE_TYPE_STRENGTH == self.currentRefineType:
			if 0 == itemVnum:
				return -1
	
			if self.__IsDragonSoul(itemVnum):
				if not DragonSoulRefineWindow.DRAGON_SOUL_SLOT in self.refineItemInfo:
					return DragonSoulRefineWindow.DRAGON_SOUL_SLOT
			else:
				if not DragonSoulRefineWindow.REFINE_STONE_SLOT in self.refineItemInfo:
					return DragonSoulRefineWindow.REFINE_STONE_SLOT
		elif app.ENABLE_DS_CHANGE_ATTR and DragonSoulRefineWindow.REFINE_TYPE_CHANGE_ATTR == self.currentRefineType:
			if 0 == itemVnum:
				return -1
				
			if self.__IsDragonSoul(itemVnum):
				if not 0 in self.refineItemInfo:  # Dragon soul slot
					return 0
			else:
				if not 1 in self.refineItemInfo:  # Material slot
					return 1
		else:
			for slotPos in range(self.wndRefineSlot.GetSlotCount()):
				if not slotPos in self.refineItemInfo:
					return slotPos
	
		return -1

	def AutoSetItem(self, inven, itemCount):
		invenType, invenPos = inven
		itemVnum = player.GetItemIndex(invenType, invenPos)
		emptySlot = self.__GetEmptySlot(itemVnum)
		if -1 == emptySlot:
			return

		self.__SetItem((invenType, invenPos), emptySlot, itemCount)

	def __ClearResultItemSlot(self):
		self.wndResultSlot.ClearSlot(0)
		self.resultItemInfo = {}

	def RefineSucceed(self, inven_type, inven_pos):
		self.__Initialize()
		self.Refresh()

		itemCount = player.GetItemCount(inven_type, inven_pos)
		if itemCount > 0:
			self.resultItemInfo[0] = (inven_type, inven_pos, itemCount)
			self.wndResultSlot.SetItemSlot(0, player.GetItemIndex(inven_type, inven_pos), itemCount)
		
		if self.REFINE_TYPE_STRENGTH == self.currentRefineType:
			invenType, invenPos, count = self.fasolka
			self.AutoSetItem((invenType, invenPos), count-1)

	def	RefineFail(self, reason, inven_type, inven_pos):
		if net.DS_SUB_HEADER_REFINE_FAIL == reason:
			self.__Initialize()
			self.Refresh()
			itemCount = player.GetItemCount(inven_type, inven_pos)
			if itemCount > 0:
				self.resultItemInfo[0] = (inven_type, inven_pos, itemCount)
				self.wndResultSlot.SetItemSlot(0, player.GetItemIndex(inven_type, inven_pos), itemCount)
		else:
			self.Refresh()

		if self.REFINE_TYPE_STRENGTH == self.currentRefineType:
			invenType, invenPos, count = self.fasolka
			self.AutoSetItem((invenType, invenPos), count-1)

	def SetInventoryWindows(self, wndInventory, wndDragonSoul):
		self.wndInventory = wndInventory
		self.wndDragonSoul = wndDragonSoul
		
	if app.ENABLE_DS_CHANGE_ATTR:
		def SetWindowType(self, type):
			self.currentRefineType = type

			if type == self.REFINE_TYPE_CHANGE_ATTR:
				for btn in self.refineChoiceButtonDict.values():
					btn.SetUp()
					btn.Disable()

				for btnTitle in self.refineChoiceButtonTitleDict.values():
					btnTitle.SetText("")

				self.refineChoiceButtonDict[self.REFINE_TYPE_STRENGTH].Down()
				self.refineChoiceButtonTitleDict[self.REFINE_TYPE_STRENGTH].SetText(uiScriptLocale.CHANGE_ATTR_SELECT)
			else:
				for btn in self.refineChoiceButtonDict.values():
					btn.SetUp()
					btn.Enable()

				self.refineChoiceButtonDict[self.REFINE_TYPE_GRADE].Down()
				self.refineChoiceButtonTitleDict[self.REFINE_TYPE_GRADE].SetText(uiScriptLocale.GRADE_SELECT)
				self.refineChoiceButtonTitleDict[self.REFINE_TYPE_STEP].SetText(uiScriptLocale.STEP_SELECT)
				self.refineChoiceButtonTitleDict[self.REFINE_TYPE_STRENGTH].SetText(uiScriptLocale.STRENGTH_SELECT)

			self.__Initialize()
			self.Refresh()

		def __CanRefineChangeAttr(self, vnum):
			# Check if it's a dragon soul
			if self.__IsDragonSoul(vnum):
				ds_info = self.__GetDragonSoulTypeInfo(vnum)
		
				if DragonSoulRefineWindow.INVALID_DRAGON_SOUL_INFO == ds_info:
					self.__PopUp(localeInfo.DRAGON_SOUL_IS_NOT_DRAGON_SOUL)
					return False
		
				ds_type, grade, step, strength = ds_info
				if grade < 5:  # Only grade 5+ dragon souls can change attributes
					
					self.__PopUp(localeInfo.DRAGONSOUL_ONLY_MYTHIC_CAN_BE_SWITCHED)
					return False
		
				# Set recipe if not already set
				if not self.currentRecipe:
					self.currentRecipe = { 
						"ds_info" : ds_info, 
						"need_count" : 2, 
						"fee" : 500000000, 
						"material_count" : (1, 1, 1, 1, 1) 
					}
					self.refineSlotLockStartIndex = 2
					self.wndMoney.SetText(localeInfo.NumberToMoneyString(self.currentRecipe["fee"]))
					self.wndPercent.SetText("100%")  # Attribute change is usually 100% success
		
				return True
				
			# Check if it's the material (100700)
			elif vnum == 100700:
				if not self.currentRecipe:
					self.__PopUp(localeInfo.DRAGONSOUL_PLACE_DRAGON_SOUL_FIRST)
					return False
				return True
			else:
				self.__PopUp(localeInfo.DRAGONSOUL_WRONG_ATTR_CHANGE_ITEM)
				return False

		def __CheckDoRefineChangeAttr(self):
			if not self.currentRecipe:
				return False
		
			# Check if we have both dragon soul and material
			if 0 not in self.refineItemInfo or 1 not in self.refineItemInfo:
				return False
		
			ds_type, grade, step, strength = self.currentRecipe["ds_info"]
			material_count = self.currentRecipe["material_count"][step]
			
			# Check if we have enough material
			invenType, invenPos, itemCount = self.refineItemInfo[1]  # Material slot
			if player.GetItemIndex(invenType, invenPos) == 100700 and itemCount >= material_count:
				return True
		
			return False