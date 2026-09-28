import uipickmoney, grp, mouseModule, offlineshop, ui, item, dbg, uicommon, uitooltip, localeInfo, \
		ime, constInfo, time, chat, uishopsearch, player, app, net, renderTarget, chr, uiScriptLocale, wndMgr
import systemSetting

from uiFishWiki import GetFishMissionData

try:
	app.WJ_ENABLE_TRADABLE_ICON
except Exception:
	app.WJ_ENABLE_TRADABLE_ICON = False

PAGE_BUILDER, PAGE_MYSHOP, PAGE_SAFEBOX, PAGE_SHOP = range(4)

OFFLINESHOP_SLOT_COUNT = 10 * 8
OFFLINESHOP_PAGE_COUNT = 3

ITEM_ADDABLE_FAST = False

OFFLINESHOP_EXTEND_TIME_NORMAL = 7 * 24 * 60
OFFLINESHOP_EXTEND_TIME_PREMIUM = 7 * 24 * 60
OFFLINESHOP_CREATE_SHOP_TIME_NORMAL = 7 * 24 * 60
OFFLINESHOP_CREATE_SHOP_TIME_PREMIUM = 7 * 24 * 60
OFFLINESHOP_PREMIUM_EXTEND_DAY = 4
OFFLINESHOP_NORMAL_EXTEND_DAY = 4

CACHE_ITEMS_ID = {}

PATH_SHOP = "offlineshop/lightwork/"
PATH_ROOT = "offlineshop/lightwork/shopeditor/"
PATH_ROOT_BUILD = "offlineshop/lightwork/shopbuilder/"
PATH_ROOT_SEARCH = "offlineshop/lightwork/searchshop/"
PATH_BIO_OBJECTS = "d:/ymir work/ui/game/biolog_system/"

FAST_ADD_TIME = 0.5
	
def IsEditOrBuildMode():
	interface = offlineshop.GetOfflineshopBoard()
	if not interface:
		return False
	return interface.IsBuildingShop()

def IsBuildingShop():
	interface = offlineshop.GetOfflineshopBoard()
	if not interface:
		return False
	return interface.IsBuildingShop()

def IsSaleSlot(win, slot):
	interface = offlineshop.GetOfflineshopBoard()
	if not interface:
		return False

	return False

####################################################################################
# Nazwa sklepu offline wyswietlana nad sklepem w miescie.
# Wyglad jak w sklepach prywatnych (uiprivateshopbuilder.PrivateShopAdvertisementBoard):
# ThinBoard z wysrodkowanym tekstem, zamiast surowego text taila rysowanego w C++.
####################################################################################

g_offlineShopAdvertisementBoardDict = {}

def AppearOfflineShop(vid, text):
	DisappearOfflineShop(vid)

	board = OfflineShopAdvertisementBoard()
	board.Open(vid, text)

def DisappearOfflineShop(vid):
	if vid not in g_offlineShopAdvertisementBoardDict:
		return

	g_offlineShopAdvertisementBoardDict[vid].Close()
	del g_offlineShopAdvertisementBoardDict[vid]

def ClearOfflineShopBoards():
	for board in list(g_offlineShopAdvertisementBoardDict.values()):
		board.Close()

	g_offlineShopAdvertisementBoardDict.clear()

class OfflineShopAdvertisementBoard(ui.ThinBoard):
	def __init__(self):
		ui.ThinBoard.__init__(self, "UI_BOTTOM")
		self.vid = None
		self.textLine = None
		self.__MakeTextLine()

	def __del__(self):
		ui.ThinBoard.__del__(self)

	def __MakeTextLine(self):
		self.textLine = ui.TextLine()
		self.textLine.SetParent(self)
		self.textLine.SetWindowHorizontalAlignCenter()
		self.textLine.SetWindowVerticalAlignCenter()
		self.textLine.SetHorizontalAlignCenter()
		self.textLine.SetVerticalAlignCenter()
		self.textLine.Show()

	def Open(self, vid, text):
		self.vid = vid
		self.textLine.SetText(text)
		self.textLine.UpdateRect()
		self.SetSize(len(text) * 6 + 10 * 2, 20)
		self.Show()

		g_offlineShopAdvertisementBoardDict[vid] = self

	def Close(self):
		self.vid = None
		self.Hide()

	def OnMouseLeftButtonUp(self):
		if not self.vid:
			return

		# Sklep w miescie ma wlasny pakiet otwarcia - wczesniej robil to hitbox text taila w C++.
		offlineshop.SendOnClickShopEntity(self.vid)
		return True

	def OnUpdate(self):
		if not self.vid:
			return

		# Opcja "Nazwa sklepu" (OPTION_SALESTEXT) - ten sam warunek, ktorym bramkowany byl
		# render text taila sklepu w C++ (PythonTextTail: IsShowSalesText).
		if systemSetting.IsShowSalesText():
			# ShopInstance nie jest postacia, wiec chr.GetProjectPosition tu nie zadziala.
			# Wysokosc nazwy nad sklepem (text tail mial 180 - obnizone dla lepszego wygladu).
			(x, y) = offlineshop.GetProjectPosition(self.vid, 150)
			self.SetPosition(x - self.GetWidth() // 2, y - self.GetHeight() // 2)
			self.Show()
		else:
			self.Hide()

class OfflineShopRenewal(ui.ScriptWindow):
	def __init__(self, wndBind):
		ui.ScriptWindow.__init__(self)
		offlineshop.SetOfflineshopBoard(self)

		self.ShopSafeboxItems = []
		self.ShopSafeboxValuteAmount = 0
		self.ShopSafeboxValuteText = None
		self.shopOfflinePopup = None

		self.ShopItemForSale = []
		self.ShopItemSold = []

		self.ShopOpenInfo = {}
		
		self.wndOffShop = wndBind

		self.listNotification = []
		self.offlineShopNotificationList = []

		self.ShopListItems = []
		self.itemNameMap = {}

	def SetAveragePrice(self, price):
		self.wndOffShop.SetAveragePrice(price)

	def SendNotification(self, dwItemID, dwItemPrice, dwItemCount):

		constInfo.GetInterfaceInstance().wndShopNotification.SetNotification(self.ShowAllNotifications)

		self.AddNotification(dwItemID, dwItemPrice, dwItemCount)

		if not constInfo.GetInterfaceInstance().wndShopNotification.IsShow():
			constInfo.GetInterfaceInstance().wndShopNotification.Open()


	def AddNotification(self, dwItemID, itemPrice, dwItemCount):
		self.listNotification.append([dwItemID, itemPrice, dwItemCount])
		self.offlineShopNotificationList.append(OfflineShopNotification())

	def ShowAllNotifications(self):
		for idx in range(len(self.listNotification)):
			listElems = self.listNotification[idx]
			self.offlineShopNotificationList[idx].Open(idx, listElems[0], listElems[1], listElems[2])

		if constInfo.GetInterfaceInstance().wndShopNotification.IsShow():
			constInfo.GetInterfaceInstance().wndShopNotification.Hide()

	def CloseAllNotifications(self):
		for idx in range(len(self.listNotification)):
			self.offlineShopNotificationList[idx].Hide()

		self.listNotification = []
		self.offlineShopNotificationList = []

	def CloseButtonEvent(self, idx):
		self.listNotification.pop(idx)
		self.offlineShopNotificationList.pop(idx)

	def IsAnyNotification(self):
		return len(self.listNotification) > 0

	def ShopFilterResult(self , size):
		self.wndOffShop.wndSearchShop.ShopFilterResult(size)

	def ShopFilterResultItem_Alloc(self):
		self.wndOffShop.wndSearchShop.ShopFilterResultItem_Alloc()
	
	def ShopFilterResultItem_SetValue( self,  key, index, *args):
		self.wndOffShop.wndSearchShop.ShopFilterResultItem_SetValue(key, index, *args)
	
	def ShopFilterResult_Show(self):
		self.wndOffShop.wndSearchShop.ShopFilterResult_Show()
		
	def SearchFilter_BuyFromSearch(self, ownerid, itemid):
		self.wndOffShop.wndSearchShop.SearchFilter_BuyFromSearch(ownerid, itemid)

	def IsBuildingShop(self):
		if self.wndOffShop.IsShow() == False:
			return False
	
		return self.wndOffShop.wBoard[PAGE_BUILDER].IsShow() or self.wndOffShop.wBoard[PAGE_MYSHOP].IsShow()

	def ShopBuilding_AddItem(self, win, slot, bCanSkipDlg = False):
		global ITEM_ADDABLE_FAST
		if player.GetItemIndex(win, slot) ==0:
			return

		if win == player.INVENTORY and player.IsEquipmentSlot(slot):
			return

		if self.IsForSaleSlot(win, slot):
			return

		itemIndex = player.GetItemIndex(win, slot)
		if itemIndex == 0:
			return False

		item.SelectItem(itemIndex)
		x, y = item.GetItemSize()
		
		page, pos = self.wndOffShop.GetEmptyPosition(y)

		if pos < 0:
			return

		if self.__IsSaleableSlot(win, slot):
			price = self.wndOffShop.LoadInputPrice(player.GetItemIndex(win, slot))
			self.wndOffShop.RightClickTradableIconRefresh(win, slot)
			self.wndOffShop.OpenInputPriceDialog(win, slot, page, pos, False, ITEM_ADDABLE_FAST)

	def IsForSaleSlot(self,win,slot):
		if self.wndOffShop.IsShow() == False:
			return

		if self.wndOffShop.wBoard[PAGE_BUILDER].IsShow():
			if self.wndOffShop.PriceInputBoard:
				if self.wndOffShop.PriceInputBoard.sourceWindowType == win and self.wndOffShop.PriceInputBoard.sourceSlotPos == slot:
					return True
		
			for page in range(OFFLINESHOP_PAGE_COUNT):
				for privatePos, (itemWindowType, itemSlotIndex, priceInfo) in self.wndOffShop.itemStockBuilder[page].items():
					if itemWindowType == win and itemSlotIndex == slot:
						return True
			
		elif self.wndOffShop.wBoard[PAGE_MYSHOP].IsShow():
			if self.wndOffShop.PriceInputBoard:
				if self.wndOffShop.PriceInputBoard.sourceWindowType == win and self.wndOffShop.PriceInputBoard.sourceSlotPos == slot:
					return True

		return False

	def __IsSaleableSlot(self, win , pos):
		if win == player.INVENTORY:
			if player.IsEquipmentSlot(pos):
				return False

		if self.IsBuildingShop() and self.IsForSaleSlot(win, pos):
			return False

		if not win in (player.INVENTORY, player.DRAGON_SOUL_INVENTORY):
			return False

		itemIndex = player.GetItemIndex(win,pos)
		if itemIndex == 0:
			return False

		item.SelectItem(itemIndex)
		if item.IsAntiFlag(item.ITEM_ANTIFLAG_MYSHOP) or item.IsAntiFlag(item.ITEM_ANTIFLAG_GIVE):
			return False

		return True

	def ShopListClear(self):
		self.ShopListItems = []

	def ShopListAddItem(self, owner_id, duration, count, name):
		self.ShopListItems.append({
			"owner_id": owner_id,
			"duration": duration,
			"count": count,
			"name": name,
		})

	def ShopListShow(self):
		pass

	def ShopClose(self):
		if self.wndOffShop:
			self.wndOffShop.Close()

	def ClearItemNames(self):
		self.itemNameMap = {}

	def AppendItemName(self, vnum, name):
		self.itemNameMap[vnum] = name

	def ShopBuilding_AddInventoryItem(self, slot):
		pass

	def Destroy(self):
		self.ClearDictionary()

		self.wndOffShop = None
		self.shopOfflinePopup = None
		offlineshop.SetOfflineshopBoard(None)
		
	def OpenShop( self, owner_id, duration, count, name):
		self.ShopItemSold 		= []
		self.ShopItemForSale 	= []

		self.ShopOpenInfo["owner_id"]	= owner_id
		self.ShopOpenInfo["duration"]	= duration
		self.ShopOpenInfo["count"]		= count
		self.ShopOpenInfo["name"]		= name
		self.ShopOpenInfo["my_shop"]	= False

	def OpenShopItem_Alloc(self):
		self.ShopItemForSale.append({})

	def OpenShopItem_SetValue( self, key,	index,	*args):
		if key == "id":
			self.ShopItemForSale[index][key] = args[0]

		elif key == "vnum":
			self.ShopItemForSale[index][key] = args[0]

		elif key == "count":
			self.ShopItemForSale[index][key] = args[0]

		elif key == "attr":
			if not key in self.ShopItemForSale[index]:
				self.ShopItemForSale[index][key] = {}

			attr_index = args[0]
			attr_type  = args[1]
			attr_value = args[2]

			self.ShopItemForSale[index][key][attr_index] = {}
			self.ShopItemForSale[index][key][attr_index]["type"]  = attr_type
			self.ShopItemForSale[index][key][attr_index]["value"] = attr_value

		elif key == "socket":
			if not key in self.ShopItemForSale[index]:
				self.ShopItemForSale[index][key] = {}

			socket_index = args[0]
			socket_val	 = args[1]

			self.ShopItemForSale[index][key][socket_index] = socket_val

		elif key == "price":
			self.ShopItemForSale[index][key] = args[0]
			
		elif key == "display_pos":
			if not key in self.ShopItemForSale[index]:
				self.ShopItemForSale[index][key] = {}
			self.ShopItemForSale[index][key]["pos"] = args[0]
			self.ShopItemForSale[index][key]["page"] = args[1]

	def OpenShop_End(self):
		self.wndOffShop.RefreshOpenShopPage()
		
		if not self.wndOffShop.IsShow():
			self.wndOffShop.Show()

	def OpenShopOwner_Start( self, owner_id, duration , count , name):
		self.ShopItemSold 		= []
		self.ShopItemForSale 	= []
		self.MyShopOffers		= []

		self.ShopOpenInfo["owner_id"]	= owner_id
		self.ShopOpenInfo["duration"]	= duration
		self.ShopOpenInfo["count"]		= count
		self.ShopOpenInfo["name"]		= name
		self.ShopOpenInfo["my_shop"]	= True

	def OpenShopOwner_End(self):
		self.wndOffShop.RefreshMyShopPage()

		if not self.wndOffShop.IsShow():
			self.wndOffShop.Show()

	def OpenShopOwnerItemSold_Alloc( self ):
		self.ShopItemSold.append({})

	def OpenShopOwnerItemSold_SetValue( self,  key , index , *args):
		if key == "id":
			self.ShopItemSold[index][key] = args[0]

		elif key == "vnum":
			self.ShopItemSold[index][key] = args[0]

		elif key == "count":
			self.ShopItemSold[index][key] = args[0]

		elif key == "attr":
			if not key in self.ShopItemSold[index]:
				self.ShopItemSold[index][key] = {}

			attr_index = args[0]
			attr_type  = args[1]
			attr_value = args[2]

			self.ShopItemSold[index][key][attr_index] = {}
			self.ShopItemSold[index][key][attr_index]["type"]  = attr_type
			self.ShopItemSold[index][key][attr_index]["value"] = attr_value

		elif key == "socket":
			if not key in self.ShopItemSold[index]:
				self.ShopItemSold[index][key] = {}

			socket_index = args[0]
			socket_val	 = args[1]

			self.ShopItemSold[index][key][socket_index] = socket_val

		elif key == "price":
			self.ShopItemSold[index][key] = args[0]

		elif key == "display_pos":
			if not key in self.ShopItemSold[index]:
				self.ShopItemSold[index][key] = {}
			self.ShopItemSold[index][key]["pos"] = args[0]
			self.ShopItemSold[index][key]["page"] = args[1]

	def OpenShopOwnerItemSold_Show(self):
		pass

	def OpenShopOwnerItem_Alloc(self):
		self.ShopItemForSale.append({})

	def OpenShopOwnerItem_SetValue( self, key, index, *args):
		if key == "id":
			self.ShopItemForSale[index][key] = args[0]

		elif key == "vnum":
			self.ShopItemForSale[index][key] = args[0]

		elif key == "count":
			self.ShopItemForSale[index][key] = args[0]

		elif key == "attr":
			if not key in self.ShopItemForSale[index]:
				self.ShopItemForSale[index][key] = {}

			attr_index = args[0]
			attr_type  = args[1]
			attr_value = args[2]

			self.ShopItemForSale[index][key][attr_index] = {}
			self.ShopItemForSale[index][key][attr_index]["type"]  = attr_type
			self.ShopItemForSale[index][key][attr_index]["value"] = attr_value

		elif key == "socket":
			if not key in self.ShopItemForSale[index]:
				self.ShopItemForSale[index][key] = {}

			socket_index = args[0]
			socket_val	 = args[1]

			self.ShopItemForSale[index][key][socket_index] = socket_val

		elif key == "price":
			self.ShopItemForSale[index][key] = args[0]
   
		elif key == "display_pos":
			if not key in self.ShopItemForSale[index]:
				self.ShopItemForSale[index][key] = {}
			self.ShopItemForSale[index][key]["pos"] = args[0]
			self.ShopItemForSale[index][key]["page"] = args[1]

	def OpenShopOwnerItem_Show(self):
		pass

	def OpenShopOwnerNoShop(self):
		for v in self.wndOffShop.wBoard.values():
			v.Hide()

		self.wndOffShop.ResetCreateShopPage()
		
		if not self.wndOffShop.IsShow():
			self.wndOffShop.Show()

	def ShopSafebox_Clear(self):
		self.ShopSafeboxItems = []

	def ShopSafebox_SetValutes(self, yang):
		self.ShopSafeboxValuteAmount = yang
		self.wndOffShop.wndTextYang.SetText("|cFFC5C5C6" + localeInfo.NumberToMoneyString(yang))

	def ShopSafebox_AllocItem(self):
		self.ShopSafeboxItems.append({})

	def ShopSafebox_SetValue(self, key , *args):
		elm = self.ShopSafeboxItems[-1]

		if key in ("id", "vnum", "count"):
			elm[key] = args[0]

		elif key == "socket":
			if not key in elm:
				elm[key] = [0 for x in range(player.METIN_SOCKET_MAX_NUM)]
			elm[key][args[0]] = args[1]

		elif key in ("attr_type", "attr_value"):
			if not 'attr' in elm:
				elm['attr'] = {}

			if not args[0] in elm['attr']:
				elm['attr'][args[0]] = {}

			elm['attr'][args[0]][key.replace('attr_','')] = args[1]

	def ShopSafebox_RefreshEnd(self):
		self.wndOffShop.RefreshSafeboxPage()

class OfflineShopWindow(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		
		self.bIsLoaded = False
		
		self.wndShop = OfflineShopRenewal(self)
		self.wndShop.Hide()
		
		# Wyszukiwarka NIE jest tworzona tutaj - uzywamy jedynego egzemplarza
		# z interfacemodule (przypisanie w BindInterface). Wczesniej powstawal
		# tu drugi, ktory rejestrowal sie przez SetShopSearchBoard, a jego
		# Destroy() wyrejestrowywal plansze wynikow calego interfejsu.
		self.wndSearchShop = None


		self.ShopOpenID = 0

		self.__Reinit()
		self.__Reinit2(True)
		self.__LoadWindow()
		self.SetCenterPosition()

		self.tooltipMisc = uitooltip.ToolTip(140)
		self.tooltipMisc.Hide()

	def SetItemToolTip(self, tooltip):
		self.tooltipItem = tooltip

	def BindInterface(self, interface):
		self.interface = interface

		self.wndSearchShop = getattr(interface, "wndShopSearch", None)
		if self.wndSearchShop:
			self.wndSearchShop.SetInterface(interface)
	
	def __Reinit2(self, isDestroy = False):
		self.wBoard = {}
		self.wBar = {}
		self.dictName = {}
		self.itemStock = {}
		self.ClearStockBuilder(isDestroy)

	def __Reinit(self):
		self.MyShopEditNameDlg = None
		self.WithdrawQuestionDialog = None
		self.QuestionDialog = None
		self.PriceInputBoard = None
		self.ShopName = None
		self.tooltipItem = None
		self.tooltipMisc = None
		self.interface = None
		self.PageGrid = 0
		self.waitTime = 0

		self.editAll = False

	def OnPressEscapeKey(self):
		if self.NameEdit.IsFocus():
			self.NameEdit.KillFocus()
			return False

		if self.QuestionDialog:
			if self.QuestionDialog.IsShow():
				return False
			
		if self.WithdrawQuestionDialog:
			return False

		self.Close()
		return True
	
	def Destroy(self):
		self.ClearDictionary()
		self.CloseDialogs(True)

		self.__Reinit()
		self.__Reinit2(True)

		if self.wndShop:
			self.wndShop.Destroy()
			self.wndShop = None
	
		# Tylko zwalniamy referencje - egzemplarz nalezy do interfacemodule,
		# ktory sam go niszczy. Destroy() tutaj zabijalby cudze okno.
		if self.wndSearchShop:
			self.wndSearchShop = None

		if app.WJ_ENABLE_TRADABLE_ICON:
			if self.interface:
				self.interface.SetOnTopWindow(player.ON_TOP_WND_NONE)
				self.interface.MouseSlotEventClear()
				self.interface.RefreshMarkInventoryBag()

	def CloseDialogs(self, isDestroy=False):
		if self.WithdrawQuestionDialog:
			self.WithdrawQuestionDialog.Close()
			self.WithdrawQuestionDialog = None

		if self.QuestionDialog:
			self.OnCloseQuestionDialog()
			
		self.CancelInputPrice(isDestroy)
	
	def ClearStockBuilder(self, isDestroy=False):
		self.itemStockBuilder = {}
		self.itemStockBuilder[0] = {}
		self.itemStockBuilder[1] = {}
		self.itemStockBuilder[2] = {}
		self.itemStockBuilder[3] = {}

		self.RefreshItemSlotInv(isDestroy)
	
	if app.WJ_ENABLE_TRADABLE_ICON:
		def OnTop(self):
			if self.interface == None:
				return
		
			if self.wBoard[PAGE_BUILDER].IsShow() or self.wBoard[PAGE_MYSHOP].IsShow():
				self.interface.SetOnTopWindow(player.ON_TOP_WND_OFFLINE_SHOP)
			else:
				self.interface.SetOnTopWindow(player.ON_TOP_WND_NONE)
				
			self.interface.RefreshMarkInventoryBag()
	
	def Close(self, isDestroy=False):
		self.CancelInputPrice()
		self.ClearStockBuilder(isDestroy)
		self.CloseDialogs(isDestroy)
			
		if app.WJ_ENABLE_TRADABLE_ICON:
			if self.interface:
				self.interface.SetOnTopWindow(player.ON_TOP_WND_NONE)
				self.interface.MouseSlotEventClear()
				self.interface.RefreshMarkInventoryBag()

		if self.MyShopEditNameDlg:
			self.MyShopEditNameDlg.Hide()
			self.MyShopEditNameDlg = None

		if self.wndShopDecoration.IsShow():
			self.wndShopDecoration.Close()

		offlineshop.SendCloseBoard()
		self.Hide()
	
	def Open(self):
		offlineshop.SendCloseBoard()
		offlineshop.SendOpenShopOwner()

	def Show(self):
		self.__LoadWindow()
		ui.ScriptWindow.Show(self)
		
		self.SetTop()
		if app.WJ_ENABLE_TRADABLE_ICON:
			self.OnTop()

	def __del__(self):
		ui.ScriptWindow.__del__(self)
		self.wndShop = None
		
	def __LoadWindow(self):
		if self.bIsLoaded:
			return
		
		self.bIsLoaded = True
		offlineshop.RefreshItemNameMap()
		
		self.AddFlag("movable")
		self.__InitPage(369, 410, PAGE_MYSHOP, uiScriptLocale.PREMIUM_PRIVATE_SHOP, PATH_ROOT_BUILD + "bg.png")
		self.__InitPage(369, 405, PAGE_BUILDER, uiScriptLocale.SELECT_CREATE, PATH_ROOT_BUILD + "bg.png")
		self.__InitPage(369, 385, PAGE_SAFEBOX, uiScriptLocale.SAFE_TITLE, PATH_ROOT_BUILD + "bg.png")
		self.__InitPage(369, 340, PAGE_SHOP, uiScriptLocale.SHOP_TITLE, PATH_ROOT_BUILD + "viewbg.png")

		self.itemSlot = []
		for xPage in range(OFFLINESHOP_PAGE_COUNT):
			itemSlot = ui.GridSlotWindow()
			itemSlot.SetParent(self)

			itemSlot.SetPosition(23, 140)

			itemSlot.ArrangeSlot(0, 10, 8, 32, 32, 0, 0)
			itemSlot.SetSlotBaseImage("d:/ymir work/ui/public/slot_base.sub", 1.0, 1.0, 1.0, 1.0)
			
			itemSlot.SetSelectItemSlotEvent(ui.__mem_func__(self.SelectItemSlot))
			itemSlot.SetOverInItemEvent(ui.__mem_func__(self.OverInItem))
			itemSlot.SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))
			itemSlot.SetSelectEmptySlotEvent(ui.__mem_func__(self.SelectEmptySlot))
			itemSlot.SetUnselectItemSlotEvent(ui.__mem_func__(self.UseItemSlot))
			itemSlot.SetUseSlotEvent(ui.__mem_func__(self.UseItemSlot))
			itemSlot.SetGridSpecial(10, 8)
			itemSlot.Hide()
			
			if xPage == 0:
				itemSlot.Show()
			
			self.itemSlot.append(itemSlot)

	def __ChangePage(self, page):
		self.CancelInputPrice()
	
		for index in range(len(self.wBoard)):
			if index not in self.wBoard:
				continue
		
			if index == page:
				self.wBoard[page].Show()
				self.SetSize(self.wBoard[page].GetWidth(), self.wBoard[page].GetHeight())
			else:
				self.wBoard[index].Hide()		

		for idxPage in range(len(self.pageList)):
			if page == PAGE_SHOP:
				self.pageList[idxPage].SetPosition(70 + 75*idxPage, 46)
				for slot in self.itemSlot:
					slot.SetPosition(23, 110)
			else:
				self.pageList[idxPage].SetPosition(70 + 75*idxPage, 86)
				for slot in self.itemSlot:
					slot.SetPosition(20, 140)

			self.pageList[idxPage].SetParent(self.wBoard[page])
	
		self.itemSlot[self.PageGrid].Show()

		if app.WJ_ENABLE_TRADABLE_ICON:	
			self.OnTop()

	def __InitPage(self, width, height, page, title, bg = PATH_ROOT + "bg.dds"):

		self.wBoard[page] = ui.ExpandedImageBox()
		self.wBoard[page].SetParent(self)
		self.wBoard[page].AddFlag("not_pick")
		self.wBoard[page].LoadImage(bg)
		self.wBoard[page].Show()

		self.wBar[page] = ui.TitleBar()
		self.wBar[page].SetParent(self.wBoard[page])
		self.wBar[page].MakeTitleBar(self.wBoard[page].GetWidth() - 12, "red")
		self.wBar[page].SetPosition(6, 6)
		self.wBar[page].SetCloseEvent(ui.__mem_func__(self.Close))
		self.dictName[page] = ui.MakeTextLineNew(self.wBar[page], 0, 4, title)
		self.dictName[page].SetWindowHorizontalAlignCenter()
		self.dictName[page].SetHorizontalAlignCenter()
		self.wBar[page].Show()
		
		self.SetSize(self.wBoard[page].GetWidth(), self.wBoard[page].GetHeight())

		if page == PAGE_BUILDER:

			if app.ENABLE_SHOP_DECORATION:
				self.wndShopDecoration = ShopDecoration()

			self.NameSlotBar = ui.MakeImageBox(self.wBoard[page], PATH_ROOT + "shoptitle.png", -25, 45)
			self.NameSlotBar.SetWindowHorizontalAlignCenter()

			self.colorPicker = uicommon.ChatColorMenu()
			self.colorPicker.SetParent(self)
			self.colorPicker.Hide()



			self.NameEdit = ui.EditLine()
			self.NameEdit.SetParent(self.NameSlotBar)
			self.NameEdit.SetMax(40)
			self.NameEdit.SetSize(self.NameSlotBar.GetWidth(), 15)
			self.NameEdit.SetPosition(31, 4)
			self.NameEdit.SetLimitWidth(self.NameEdit.GetWidth())
			self.NameEdit.SetMax(20)
			self.NameEdit.SetEscapeEvent(ui.__mem_func__(self.OnPressNameEscapeKey))
			self.NameEdit.SetOutline()
			self.NameEdit.SetOverlayText("      < " + uiScriptLocale.OPTION_SALESTEXT + ">")
			self.NameEdit.Show()

			if app.ENABLE_SHOP_DECORATION:
				self.btnShopDecoration = ui.MakeButton(self.wBoard[page], 257, 45, False, PATH_ROOT, "btn_cosmetic_01.png", "btn_cosmetic_02.png", "btn_cosmetic_03.png")
				self.btnShopDecoration.SetEvent(ui.__mem_func__(self.OpenShopDecoration))
				self.btnShopDecoration.ShowToolTip = lambda arg="OVERIN": self.overEvent(arg)
				self.btnShopDecoration.HideToolTip = lambda arg="OVEROUT": self.overEvent(arg)


			self.btnGoSafeboxCRT = ui.MakeButton(self.wBoard[page], 295, 45, False, PATH_ROOT,  "safe1.png", "safe2.png", "safe3.png")
			self.btnGoSafeboxCRT.ShowToolTip = lambda arg="OTHER_OVERIN": self.overEvent(arg)
			self.btnGoSafeboxCRT.HideToolTip = lambda arg="OVEROUT": self.overEvent(arg)

			self.btnCreateOk = ui.MakeButton(self.wBoard[page], 103, 406, False, "offlineshop/lightwork/searchshop/", "btn_filter_norm.png", "btn_filter_hover.png", "btn_filter_down.png")
			
			self.btnCreateOk.SetText(uiScriptLocale.SELECT_CREATE)
			
			self.btnGoSafeboxCRT.SetEvent(ui.__mem_func__(self.ManageWindow))
			self.btnCreateOk.SetEvent(ui.__mem_func__(self.OnCreateShop))

		elif page == PAGE_MYSHOP:

			self.wndSlotTotalYang = ui.MakeImageBox(self.wBoard[page], "offlineshop/lightwork/shopeditor/totalyang.png", 20, 45)
			self.wndSlotTotalYang.OnMouseOverIn = lambda arg = localeInfo.OFFLINESHOP_TOTAL_PRICE_OF_SHOP : self.OverInImage(arg)
			self.wndSlotTotalYang.OnMouseOverOut = ui.__mem_func__(self.OverOutImage)


			self.wndTotalPrice = ui.MakeTextLineNew(self.wndSlotTotalYang, 35, 4, "")
			self.wndTotalPrice.SetWindowHorizontalAlignLeft()
			self.wndTotalPrice.SetHorizontalAlignLeft()
			self.wndTotalPrice.SetFontName("Tahoma:14")

			self.btnCloseShop = ui.MakeButton(self.wBoard[page], 219, 45, uiScriptLocale.PREMIUM_PRIVATE_SHOP_SHOP_CLOSE_BUTTON, PATH_ROOT, "btn_close_shop_norm.png", "btn_close_shop_hover.png", "btn_close_shop_down.png")
			self.btnCloseShop.SetEvent(ui.__mem_func__(self.AskClosePrivateShop))
			
			self.btnChangeName = ui.MakeButton(self.wBoard[page], 257, 45, uiScriptLocale.PET_ATTR_CONFIRMATION, PATH_ROOT, "name1.png", "name2.png", "name3.png")
			self.btnChangeName.SetEvent(ui.__mem_func__(self.ChangeNameShop))

			self.btnGoToSafebox = ui.MakeButton(self.wBoard[page], 295, 45, uiScriptLocale.SAFE_TITLE, PATH_ROOT, "safe1.png", "safe2.png", "safe3.png")
			self.btnGoToSafebox.SetEvent(ui.__mem_func__(self.ManageWindow))

			self.btnRefillTime = ui.MakeButton(self.wBoard[page], 280, 400, localeInfo.OFFLINESHOP_REFILL_TIME_BUTTON, PATH_ROOT, "time1.png", "time2.png", "time3.png")
			self.btnRefillTime.SetEvent(ui.__mem_func__(self.AskIncreaseTimeShop))
			self.remainingTimeGauge = ui.Gauge()
			self.remainingTimeGauge.SetParent(self.wBoard[page])
			self.remainingTimeGauge.MakeGauge(200, "white")
			self.remainingTimeGauge.SetPosition(75, 425)
			self.remainingTimeGauge.Show()

			self.wndRemainTime = ui.MakeTextLineNew(self.remainingTimeGauge, 0, -20, localeInfo.OFFLINE_SHOP_REMAINING_TIME)
			self.wndRemainTime.SetWindowHorizontalAlignCenter()
			self.wndRemainTime.SetHorizontalAlignCenter()

			self.pageList = [i for i in range(3)]
			self.pageText = ["I", "II", "III"]

			for i in range(OFFLINESHOP_PAGE_COUNT):
				self.pageList[i] = ui.MakeRadioButton(self.wBoard[page], 0, 0, PATH_ROOT_BUILD, "btn_norm.png", "btn_hover.png", "btn_down.png")
				self.pageList[i].SetText(self.pageText[i])

			for idxPage in range(len(self.pageList)):
				self.pageList[idxPage].SetEvent(ui.__mem_func__(self.ChangeShopPage), idxPage)
				
			self.pageList[0].Down()

		elif page == PAGE_SAFEBOX:
			self.btnGoBack = ui.MakeButton(self.wBoard[page], 100, 45, "", "offlineshop/lightwork/searchshop/", "btn_filter_norm.png", "btn_filter_hover.png", "btn_filter_down.png")
			self.btnGoBack.SetEvent(ui.__mem_func__(self.ManageWindow))
			self.btnGoBack.SetText(uiScriptLocale.CREATE_PREV)

			self.btnWithdrawYang = ui.MakeButton(self.wBoard[page], 205, 406, False, "offlineshop/lightwork/shopbuilder/", "btn_big_default.png", "btn_big_hover.png", "btn_big_down.png")
			self.btnWithdrawYang.SetText(localeInfo.OFFLINE_SHOP_WITHDRAW_YANG)

			self.btnWithdrawYang.SetEvent(ui.__mem_func__(self.WithdrawMoney))

			self.wndYangField = ui.MakeImageBox(self.wBoard[page], "offlineshop/lightwork/searchshop/" + "searchbg.png", 55, 406)
			self.wndTextYang = ui.MakeTextLineNew(self.wndYangField, 8, 4, "|cFF20B2AA" + localeInfo.OFFLINESHOP_YANG_DEFAULT)
			self.wndTextYang.SetWindowHorizontalAlignRight()
			self.wndTextYang.SetHorizontalAlignRight()

	if app.ENABLE_SHOP_DECORATION:
		def OpenShopDecoration(self):

			if self.wndShopDecoration.IsShow():
				self.wndShopDecoration.Hide()
			else:
				self.wndShopDecoration.Open()

	def overEvent(self, event, eventType=""):
		if event=="OVERIN":
			self.tooltipMisc.ClearToolTip()
			self.tooltipMisc.AutoAppendNewTextLine(localeInfo.OFFLINESHOP_SHOP_COLOR if eventType == "TITLE" else  localeInfo.OFFSHOP_DECORATION_SET)
			self.tooltipMisc.Show()
		elif event=="OTHER_OVERIN":
			self.tooltipMisc.ClearToolTip()
			self.tooltipMisc.AutoAppendNewTextLine(uiScriptLocale.SAFE_TITLE)
			self.tooltipMisc.Show()
		else:
			if self.tooltipMisc:
				self.tooltipMisc.ClearToolTip()
				self.tooltipMisc.Hide()

	def ShowChatColorPicker(self):


		if self.colorPicker.IsShow():
			self.colorPicker.Close()
		else:
			self.colorPicker.Open()
			self.colorPicker.SetTop()

	def OpenSearch(self):
		if self.wndSearchShop.IsShow():
			self.wndSearchShop.Hide()
		else:
			self.wndSearchShop.Show()
	
	def ManageWindow(self):
		if self.wBoard[PAGE_SAFEBOX].IsShow():
			offlineshop.SendCloseBoard()
			offlineshop.SendOpenShopOwner()
		else:
			offlineshop.SendCloseBoard()
			offlineshop.SendSafeboxOpen()
		self.ChangeShopPage(0)

		if self.wndShopDecoration.IsShow():
			self.wndShopDecoration.Close()

		if app.WJ_ENABLE_TRADABLE_ICON:
			if self.interface:
				self.interface.SetOnTopWindow(player.ON_TOP_WND_NONE)
				self.interface.MouseSlotEventClear()
				self.interface.RefreshMarkInventoryBag()


	def ChangeShopPage(self, page):

		if page < 0 or page > OFFLINESHOP_PAGE_COUNT - 1:
			return
		self.PageGrid = page
		
		for idxPage in range(len(self.pageList)):
			if idxPage == page:
				self.pageList[idxPage].Down()
			else:
				self.pageList[idxPage].SetUp()
				
		self.RefreshItemSlot()

		for button in self.pageList:
			button.SetUp()
			button.Enable()

		self.pageList[page].Down()
		self.pageList[page].Disable()

	def ChangeNameShop(self):
		if self.MyShopEditNameDlg == None:
			self.MyShopEditNameDlg	= uicommon.InputDialogWithDescription()
			self.MyShopEditNameDlg.SetMaxLength(35)
			self.MyShopEditNameDlg.SetDescription(localeInfo.OFFLINESHOP_EDIT_SHOPNAME_DESCRIPTION2)
			self.MyShopEditNameDlg.SetAcceptEvent(self.__OnAcceptChangeShopNameDlg)
			self.MyShopEditNameDlg.SetCancelEvent(self.__OnCancelChangeShopNameDlg)
			self.MyShopEditNameDlg.SetTitle(localeInfo.OFFLINESHOP_EDIT_SHOPNAME_DESCRIPTION)

		self.MyShopEditNameDlg.inputValue.SetText("")
		self.MyShopEditNameDlg.Open()

	def __OnAcceptChangeShopNameDlg(self):
		newShopName = self.MyShopEditNameDlg.GetText()
		self.MyShopEditNameDlg.Hide()

		offlineshop.SendChangeName(newShopName)

	def __OnCancelChangeShopNameDlg(self):
		self.MyShopEditNameDlg.Hide()	

	def OnPressNameEscapeKey(self):
		if self.OnPressEscapeKey():
			return
	
		if self.NameEdit.IsShowCursor() or self.NameEdit.GetText() != "":
			self.NameEdit.SetText("")
			self.NameEdit.SetOverlayText("< " + uiScriptLocale.OPTION_SALESTEXT + ">")
			self.NameEdit.SetEndPosition()

	def RefreshOpenShopPage(self):
		wasOpen = (self.IsShow() and self.wBoard[PAGE_SHOP].IsShow())
	
		name = self.wndShop.ShopOpenInfo["name"]
		ownerName	= name[:name.find('@')] if '@' in name else "NONAME"		
		name		= name[name.find('@')+1:] if '@' in name else name

		if self.ShopOpenID != self.wndShop.ShopOpenInfo["owner_id"]:
			self.ChangeShopPage(0)
		
		self.ShopOpenID = self.wndShop.ShopOpenInfo["owner_id"]

		self.dictName[PAGE_SHOP].SetText(ownerName + " " + uiScriptLocale.PREMIUM_PRIVATE_SHOP_TITLE)
		self.__ChangePage(PAGE_SHOP)

		self.RefreshItemSlot()
		
		if len(self.wndShop.ShopItemForSale) <= 0:
			self.Close()
			return

	def RefreshMyShopPage(self):
		wasOpen = (self.wBoard[PAGE_MYSHOP].IsShow())
		self.__ChangePage(PAGE_MYSHOP)

		wndRemainTimeLeft = self.wndShop.ShopOpenInfo["duration"]
		self.wndRemainTime.SetText(localeInfo.OFFLINE_SHOP_LEFT_TIME % (localeInfo.SecondToDHM(wndRemainTimeLeft * 60)))

		global OFFLINESHOP_EXTEND_TIME_NORMAL
		self.remainingTimeGauge.SetPercentage(wndRemainTimeLeft, OFFLINESHOP_EXTEND_TIME_NORMAL)

		name = self.wndShop.ShopOpenInfo["name"]
		
		if '@' in name:
			name = name[name.find('@')+1:]
		
		self.ShopName = name
		self.NameEdit.SetText(self.ShopName)

		self.RefreshItemSlot()

	def ResetCreateShopPage(self):
		self.ClearStockBuilder()

		self.__ChangePage(PAGE_BUILDER)
		self.RefreshItemSlot()
		
	def RefreshSafeboxPage(self):
		wasOpen = (self.wBoard[PAGE_SAFEBOX].IsShow())
		self.__ChangePage(PAGE_SAFEBOX)
		
		self.RefreshItemSlot()

	def SetPrivateShopBuilderItemNew(self, invenType, invenPos, price):
		itemVnum = player.GetItemIndex(invenType, invenPos)
		if 0 == itemVnum:
			return

		item.SelectItem(itemVnum)
		self.tooltipItem.ClearToolTip()
		self.tooltipItem.AppendSellingPrice(price)

		metinSlot = []
		for i in range(player.METIN_SOCKET_MAX_NUM):
			metinSlot.append(player.GetItemMetinSocket(invenPos, i))
		attrSlot = []
		for i in range(player.ATTRIBUTE_SLOT_MAX_NUM):
			attrSlot.append(player.GetItemAttribute(invenPos, i))

		self.tooltipItem.AddItemData(itemVnum, metinSlot, attrSlot)

	def OverInImage(self, text):
		if self.tooltipMisc:
			self.tooltipMisc.ClearToolTip()
			self.tooltipMisc.SetThinBoardSize(11 * len(text))
			self.tooltipMisc.AlignHorizonalCenter()
			self.tooltipMisc.AutoAppendTextLine(text)
			self.tooltipMisc.Show()

	def OverOutImage(self):
		if self.tooltipMisc:
			self.tooltipMisc.Hide()

	def OverInItem(self, slotIndex):
		if None == self.tooltipItem:
			return

		if self.wBoard[PAGE_BUILDER].IsShow():
			if slotIndex in self.itemStockBuilder[self.PageGrid]:
				window, pos, price = self.itemStockBuilder[self.PageGrid][slotIndex]
				self.SetPrivateShopBuilderItemNew(window, pos, price)
		elif slotIndex in self.itemStock:
			id, vnum, count, price, sockets, attrs = self.itemStock[slotIndex]
			
			self.tooltipItem.ClearToolTip()
			self.tooltipItem.AddItemData(vnum, sockets, attrs)

			if self.wBoard[PAGE_SAFEBOX].IsShow() == False:
				self.tooltipItem.AppendPrice(price)

			if self.wBoard[PAGE_MYSHOP].IsShow():
				self.tooltipItem.AppendSpace(5)
				self.tooltipItem.AppendTextLine(localeInfo.OFFLINE_SHOP_EMOJI_TOOLTIP2, centerAlign = False)
				self.tooltipItem.AppendSpace(5)
				self.tooltipItem.AppendTextLine(localeInfo.OFFLINE_SHOP_EMOJI_TOOLTIP, centerAlign = False)
			elif self.wBoard[PAGE_SAFEBOX].IsShow():
				self.tooltipItem.AppendSpace(5)
				self.tooltipItem.AppendTextLine(localeInfo.OFFLINE_SHOP_EMOJI_TOOLTIP3, centerAlign = False)
	
	def OverOutItem(self):
		if None != self.tooltipItem:
			self.tooltipItem.HideToolTip()

	def GetEmptyPosition(self, size):
		for page in range(OFFLINESHOP_PAGE_COUNT):
			iPos = self.itemSlot[page].GetEmptyGrid(size)
			if iPos >= 0:
				return (page, iPos)
		return (-1, -1)

	def GetGridCachePosItemID(self, size, item_id):
		for page in range(len(self.itemSlot)):
			if page not in CACHE_ITEMS_ID:
				continue
		
			if item_id in CACHE_ITEMS_ID[page]:
				return (page, CACHE_ITEMS_ID[page][item_id])

		return (self.GetEmptyPosition(size))
	
	def RefreshItemSlot(self):
		items = []
		if self.wBoard[PAGE_MYSHOP].IsShow() or self.wBoard[PAGE_SHOP].IsShow():
			items = self.wndShop.ShopItemForSale
		elif self.wBoard[PAGE_SAFEBOX].IsShow():
			items = self.wndShop.ShopSafeboxItems

		for itemSlotIdx in range(len(self.itemSlot)):
			for index in range(OFFLINESHOP_SLOT_COUNT):
				self.itemSlot[itemSlotIdx].ClearSlot(index)
			
			self.itemSlot[itemSlotIdx].ClearGrid()
			self.itemSlot[itemSlotIdx].Hide()
			
		self.itemSlot[self.PageGrid].Show()
		
		TotalPrice = 0
		self.itemStock = {}
		
		if self.wBoard[PAGE_BUILDER].IsShow():
			for page in range(OFFLINESHOP_PAGE_COUNT):
				for i in range(OFFLINESHOP_SLOT_COUNT):
				
					if not i in self.itemStockBuilder[page]:
						self.itemSlot[page].ClearSlot(i)
						continue

					window, pos, price = self.itemStockBuilder[page][i]
					vnum = player.GetItemIndex(window, pos)
					
					if vnum <= 0:
						continue
					
					self.itemSlot[page].SetItemSlot(i, vnum, player.GetItemCount(window, pos))
					
					item.SelectItem(vnum)
					itemType = item.GetItemType()
					
					if itemType == item.FISH:
						fishData = GetFishMissionData(vnum)
						if fishData != None and player.GetItemMetinSocket(window, pos, 0) >= fishData[1]*100:
							self.itemSlot[page].SetFishAddonOnSlot(i)
							
					x, y = item.GetItemSize()
					self.itemSlot[page].PutItemGrid(i, y)

			self.itemSlot[self.PageGrid].RefreshSlot()
			return

		for index in range(len(items)):
			itemVnum = items[index]["vnum"]
			itemCount = items[index]["count"]
				
			if itemVnum <= 0:
				continue
			
			item.SelectItem(itemVnum)
			x, y = item.GetItemSize()
			

			PageItemSlot, iPos = self.GetGridCachePosItemID(y, items[index]["id"])
			if not self.wBoard[PAGE_SAFEBOX].IsShow():
				iPos = items[index]["display_pos"]["pos"]
				PageItemSlot = items[index]["display_pos"]["page"]

			if iPos < 0:
				chat.AppendChat(1, localeInfo.OFFLINE_SHOP_WARNING)
				return
			
			self.itemSlot[PageItemSlot].PutItemGrid(iPos, y)
			
			itemCountGrid = itemCount if itemCount > 1 else 0
			self.itemSlot[PageItemSlot].SetItemSlot(iPos, itemVnum, itemCountGrid)
			
			itemType = item.GetItemType()
			if itemType == item.FISH:
				fishData = GetFishMissionData(itemVnum)
				if fishData != None:
					socketValue = items[index]["socket"][0] if len(items[index]["socket"]) > 0 else 0
					if socketValue >= fishData[1]*100:
						self.itemSlot[PageItemSlot].SetFishAddonOnSlot(iPos)

			sockets = [items[index]["socket"][num] for num in range(player.METIN_SOCKET_MAX_NUM)]
			attrs	= [(items[index]["attr"][num]['type'], items[index]["attr"][num]['value']) for num in range(player.ATTRIBUTE_SLOT_MAX_NUM)]	

			ItemPrice = 0
			if "price" in items[index]:
				ItemPrice = int(items[index]["price"])
				TotalPrice += int(items[index]["price"])
				

			if PageItemSlot == self.PageGrid:
				self.itemStock[iPos] = (items[index]["id"], itemVnum, itemCount, ItemPrice, sockets, attrs)
			
			if PageItemSlot not in CACHE_ITEMS_ID:
				CACHE_ITEMS_ID[PageItemSlot] = {}
			
			CACHE_ITEMS_ID[PageItemSlot][items[index]["id"]] = iPos

		self.wndTotalPrice.SetText(str(localeInfo.NumberToDecimal(TotalPrice)))

		if self.PriceInputBoard and self.wBoard[PAGE_MYSHOP].IsShow():
			CurrentPageGrid = self.PriceInputBoard.CurrentPageGrid
			targetSlotPos = self.PriceInputBoard.targetSlotPos
			isEditMode = self.PriceInputBoard.isEditMode

		self.itemSlot[self.PageGrid].RefreshSlot()


	def SelectItemSlot(self, itemSlotIndex):
		if constInfo.GET_ITEM_QUESTION_DIALOG_STATUS() == 1:
			return

		if mouseModule.mouseController.isAttached():
			mouseModule.mouseController.DeattachObject()
		
		if itemSlotIndex in self.itemStock == False:
			return
		
		if self.wBoard[PAGE_BUILDER].IsShow():
			return

		id, vnum, count, price, sockets_v, attrs_s = self.itemStock[itemSlotIndex]

		if self.wBoard[PAGE_MYSHOP].IsShow() or self.wBoard[PAGE_SAFEBOX].IsShow():
			if app.IsPressed(app.DIK_LALT):
				sockets = {}
				for num in range(player.METIN_SOCKET_MAX_NUM):
					sockets[num] = (int(sockets_v[num]), 1)
					
				attrs = {}
				for num in range(player.ATTRIBUTE_SLOT_MAX_NUM):
					attrs[num] = (int(attrs_s[num][0]), int(attrs_s[num][1]))

	def SetEditAllState(self, state):
		self.editAll = state

	def UseItemSlot(self, slotIndex):
		if constInfo.GET_ITEM_QUESTION_DIALOG_STATUS() == 1:
			return

		if mouseModule.mouseController.isAttached():
			mouseModule.mouseController.DeattachObject()

		if self.QuestionDialog:
			self.OnCloseQuestionDialog()

		if self.wBoard[PAGE_BUILDER].IsShow():
			if slotIndex in self.itemStockBuilder[self.PageGrid]:
				invenType, invenPos, price = self.itemStockBuilder[self.PageGrid][slotIndex]
				del self.itemStockBuilder[self.PageGrid][slotIndex]
				
				self.RefreshItemSlot()
				self.RefreshItemSlotInv()


			return
		else:
			if slotIndex in self.itemStock == False:
				return

			id, vnum, count, price, sockets, attrs = self.itemStock[slotIndex]

			if self.wBoard[PAGE_SAFEBOX].IsShow():
				# Nie clearuj cache PRZED odpowiedzią servera — patrz OnCancelShopItem.
				offlineshop.SendSafeboxGetItem(id)
				return

			if self.wBoard[PAGE_MYSHOP].IsShow() and not (app.IsPressed(app.DIK_LCONTROL) or app.IsPressed(app.DIK_RCONTROL)):
				self.OpenInputPriceDialog(vnum, count, id, slotIndex, True)
				return

			item.SelectItem(vnum)
			QuestionDialog = uicommon.QuestionDialog()
			
			if self.wBoard[PAGE_SHOP].IsShow():
				if count > 1:
					text = localeInfo.OFFLINE_SHOP_BUY_ITEM % (item.GetItemName(), count, localeInfo.NumberToMoneyString(price))
				else:
					text = localeInfo.OFFLINE_SHOP_BUY_ITEM2 % (item.GetItemName(), localeInfo.NumberToMoneyString(price))

			elif self.wBoard[PAGE_MYSHOP].IsShow():
				offlineshop.SendRemoveItem(id)
				self.ClearCachePos(self.PageGrid, id)
				return
			else:
				return
			
			QuestionDialog.SetText(text)
			QuestionDialog.SetAcceptEvent(ui.__mem_func__(self.OnCancelShopItem))
			QuestionDialog.SetCancelEvent(ui.__mem_func__(self.OnCloseQuestionDialog))
			QuestionDialog.Open()
			self.QuestionDialog = QuestionDialog
			self.QuestionDialog.slotIndex = slotIndex
			self.QuestionDialog.itemStock = self.itemStock[slotIndex]
		
		constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(1)

	def RightClickTradableIconRefresh(self, attachedSlotType, attachedSlotPos):

		if self.PriceInputBoard:
			if self.PriceInputBoard.IsShow():
				return


	def OnCancelShopItem(self):
		if not self.QuestionDialog:
			return True

		id, vnum, count, price, sockets, attrs = self.QuestionDialog.itemStock
		
		if self.wBoard[PAGE_MYSHOP].IsShow():
			offlineshop.SendRemoveItem(id)
			self.ClearCachePos(self.PageGrid, id)
		elif self.wBoard[PAGE_SHOP].IsShow():
			offlineshop.SendBuyItem(self.wndShop.ShopOpenInfo["owner_id"], id)
		else:
			# Safebox GetItem: nie clearuj cache PRZED odpowiedzią servera.
			# Server może odrzucić (np. pełny ekwipunek) — wtedy refresh przyśle
			# ten sam item z powrotem. Bez cached pos klient renderuje na slot 1
			# zamiast oryginalnej pozycji.
			# Gdy serwer się zgodzi, refresh nie zawiera tego itemu = cache entry
			# pozostaje stale ale jest unużywany (item_id już nie istnieje).
			offlineshop.SendSafeboxGetItem(id)
		
		constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(0)
		self.OnCloseQuestionDialog()
		return True

	def FastAddableBlacklist(self, vnum):
		item.SelectItem(vnum)
		itemType = item.GetItemType()
		if itemType == item.ARMOR or itemType == item.WEAPON or item.LIMIT_LEVEL >= 75:
			return True
		return False

	def OnCloseQuestionDialog(self):
		if self.QuestionDialog == None:
			return
			
		self.QuestionDialog.Close()

		self.QuestionDialog.itemStock = None
		self.QuestionDialog = None
		constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(0)

	def SelectEmptySlot(self, selectedSlotPos):
		if self.wBoard[PAGE_SAFEBOX].IsShow() or self.wBoard[PAGE_SHOP].IsShow():
			self.OverOutItem()
		isAttached = mouseModule.mouseController.isAttached()
		attachedSlotType = mouseModule.mouseController.GetAttachedType()
		attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
		attachedInvenType = player.SlotTypeToInvenType(attachedSlotType)

		if isAttached:
			mouseModule.mouseController.DeattachObject()
			if self.wBoard[PAGE_SHOP].IsShow() and self.wndShop.ShopOpenInfo["owner_id"] != player.GetMainCharacterIndex():
				return

			if player.IsAntiFlagBySlot(attachedInvenType, attachedSlotPos, item.ANTIFLAG_GIVE) or player.IsAntiFlagBySlot(attachedInvenType, attachedSlotPos, item.ANTIFLAG_MYSHOP):
				return

			if not self.wBoard[PAGE_SAFEBOX].IsShow():


				self.OpenInputPriceDialog(attachedInvenType, attachedSlotPos, self.PageGrid, selectedSlotPos)

	def OpenInputPriceDialog(self, window, slot, page, EmptyGridPos, editMode = False, skipDlg = False):
		if self.PriceInputBoard:
			return

		global ITEM_ADDABLE_FAST

		if ITEM_ADDABLE_FAST:
			if app.GetTime() < self.waitTime:
				chat.AppendChat(1, localeInfo.MINING_EVENT_RENEWAL_HIT_DELAY)
				return

		if editMode == False:
			itemVNum = player.GetItemIndex(window, slot)
			itemCount = player.GetItemCount(window, slot)


			item.SelectItem(itemVNum)
			(xsize, ysize) = item.GetItemSize()
			if ysize > 1:
				for i in range(ysize-1):
					if self.itemStockBuilder[page].get(EmptyGridPos + ((i*10)+10)):
						return

		else:
			itemVNum = window
			itemCount = slot

		PriceInputBoard = uicommon.OfflineShopInputDialog(itemVNum, itemCount, editMode)
		PriceInputBoard.SetAcceptEvent(ui.__mem_func__(self.AcceptInputPrice))
		PriceInputBoard.SetCancelEvent(ui.__mem_func__(self.CancelInputPrice))
		PriceInputBoard.Open()

		self.PriceInputBoard = PriceInputBoard
		offlineshop.SendAveragePrice(itemVNum)

		self.PriceInputBoard.itemVNum = itemVNum
		self.PriceInputBoard.sourceWindowType = window
		self.PriceInputBoard.sourceSlotPos = slot
		self.PriceInputBoard.targetSlotPos = EmptyGridPos
		self.PriceInputBoard.page = page
		self.PriceInputBoard.CurrentPageGrid = self.PageGrid
		self.PriceInputBoard.isEditMode = editMode

		if editMode == False:
			price = self.LoadInputPrice(player.GetItemIndex(window, slot))
			count = player.GetItemCount(window, slot)

			if price > 0:
				if count > 1:
					self.PriceInputBoard.SetValue(str(price*count))
				else:
					self.PriceInputBoard.SetValue(str(price))
    
				self.PriceInputBoard.inputValue.SetEndPosition()

		self.RefreshItemSlotInv()

		if self.FastAddableBlacklist(itemVNum):
			ITEM_ADDABLE_FAST = False
			return
		else:
			if skipDlg:
				ITEM_ADDABLE_FAST = False
				self.waitTime = app.GetTime() + FAST_ADD_TIME
				self.AcceptInputPrice()

	def SetAveragePrice(self, price):
		if self.PriceInputBoard:
			self.PriceInputBoard.AveragePriceUpdate(price)

	def AcceptInputPrice(self):
		if not self.PriceInputBoard:
			return True

		if self.wBoard[PAGE_MYSHOP].IsShow():
			self.PriceInputBoard.GetEditAllState()

		Text = self.PriceInputBoard.inputValue.GetText()

		if not Text:
			return True

		if Text:
			Text = min(constInfo.ConvertMoneyText(Text), 999999999999999)

		if int(Text) <= 0:
			return True
		
		attachedInvenType = int(self.PriceInputBoard.sourceWindowType) & 0xFF
		sourceSlotPos = self.PriceInputBoard.sourceSlotPos
		targetSlotPos = self.PriceInputBoard.targetSlotPos
		targetPage = self.PriceInputBoard.page
		isEditMode = self.PriceInputBoard.isEditMode

		yang = int(Text)
		count = player.GetItemCount(attachedInvenType, sourceSlotPos)
		if count > 1:
			yang = yang//count
		else:
			yang

		itemVnum = player.GetItemIndex(attachedInvenType, sourceSlotPos)

		self.SaveInputPrice(itemVnum, yang)

		self.OverOutItem()
		
		if self.wBoard[PAGE_BUILDER].IsShow():
			self.PriceInputBoard.ArrangeItemPrices()
	
			for page in range(OFFLINESHOP_PAGE_COUNT):
				for privatePos, (itemWindowType, itemSlotIndex, priceInfo) in self.itemStockBuilder[page].items():
					if itemWindowType == attachedInvenType and itemSlotIndex == sourceSlotPos:
						del self.itemStockBuilder[page][privatePos]
		
			self.itemStockBuilder[targetPage][targetSlotPos] = (attachedInvenType, sourceSlotPos, int(Text))
		else:
			if isEditMode:
				
				offlineshop.SendEditItem(self.PriceInputBoard.page, int(Text), self.editAll)
			else:
				offlineshop.SendAddItem(attachedInvenType, sourceSlotPos, int(Text),targetSlotPos,targetPage)

		self.PriceInputBoard = None
		
		self.RefreshItemSlot()
		self.RefreshItemSlotInv()
		return True

	def ReArrangeItemPrices(self, itemVnum, newPrice):
		for page in range(OFFLINESHOP_PAGE_COUNT):
			for privatePos, (itemWindowType, itemSlotIndex, itemPrice) in self.itemStockBuilder[page].items():
				itemIndex = player.GetItemIndex(itemWindowType, itemSlotIndex)
				itemCount = player.GetItemCount(itemWindowType, itemSlotIndex)
				if itemVnum == itemIndex:
					self.itemStockBuilder[page][privatePos] = (itemWindowType, itemSlotIndex, newPrice*itemCount)
		self.RefreshItemSlotInv()

	def RefreshItemSlotInv(self, isDestroy=False):
		if isDestroy:
			return
			
		if self.interface == None:
			return
	
		if self.interface.wndInventory:
			self.interface.wndInventory.RefreshItemSlot()

		if self.interface.wndExtendedInventory:
			self.interface.wndExtendedInventory.RefreshItemSlot()

	def CancelInputPrice(self, isDestroy = False):

		if self.PriceInputBoard:
			self.PriceInputBoard.Destroy()
		
		self.PriceInputBoard = None
		
		if not isDestroy:
			self.RefreshItemSlot()
			self.RefreshItemSlotInv()
		return True

	def SaveInputPrice(self, vnum, price):
		import os
		path = "UserData/offlineshop_pricelist"

		if not os.path.exists(path):
			os.makedirs(path)

		n = path + "/" + str(vnum) + ".txt"
		f = open(n, "w+")
		f.write(str(price))
		f.close()

	def LoadInputPrice(self, vnum):
		import os
		path = "UserData/offlineshop_pricelist"

		if not os.path.exists(path):
			os.makedirs(path)

		oldPrice = 0

		n = path + "/" + str(vnum) + ".txt"

		if os.path.exists(n):
			fd = open( n,'r')
			oldPrice = int(fd.readlines()[0])

		return oldPrice

	def AskClosePrivateShop(self):
		if self.QuestionDialog:
			self.OnCloseQuestionDialog()

		if not self.QuestionDialog:
			QuestionDialog = uicommon.QuestionDialog()
			QuestionDialog.SetText(localeInfo.PRIVATE_SHOP_CLOSE_QUESTION)
			QuestionDialog.SetAcceptEvent(ui.__mem_func__(self.OnClosePrivateShop))
			QuestionDialog.SetCancelEvent(ui.__mem_func__(self.OnCloseQuestionDialog))
			self.QuestionDialog = QuestionDialog

		self.QuestionDialog.Open()
		return True
	
	def OnClosePrivateShop(self):
		offlineshop.SendForceCloseShop()
		global CACHE_ITEMS_ID
		CACHE_ITEMS_ID = {}
		constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(0)
		self.OnCloseQuestionDialog()

		self.NameEdit.SetText("")
		self.NameEdit.SetOverlayText("         < " + uiScriptLocale.OPTION_SALESTEXT + ">")
		return True

	def SetPopUpDialog(self, msg, waitTime = "Normal"):
		self.popupMessage = uicommon.PopupDialog()
		self.popupMessage.SetWidth(250)
		self.popupMessage.SetText(msg)
		self.popupMessage.Open()
		if waitTime == "Long":
			self.popupMessage.SetAutoCloseLong(True)
		else:
			self.popupMessage.SetAutoClose(True)

	def WithdrawMoney(self):
		if self.WithdrawQuestionDialog:
			return
		
		shopMoney = self.wndShop.ShopSafeboxValuteAmount
		if shopMoney <= 0:
			self.SetPopUpDialog(localeInfo.OFFLINESHOP_NO_MONEY_TO_WITHDRAW)
			return

		WithdrawQuestionDialog = uicommon.MoneyInputDialog()
		WithdrawQuestionDialog.SetTitle(localeInfo.EXCHANGE_MONEY)
		WithdrawQuestionDialog.SetMoneyHeaderText(localeInfo.EXCHANGE_MONEY+":")
		WithdrawQuestionDialog.SetAcceptEvent(ui.__mem_func__(self.SumWithdraw)) 
		WithdrawQuestionDialog.SetCancelEvent(ui.__mem_func__(self.CloseSumWithdraw))
		WithdrawQuestionDialog.Open()
		WithdrawQuestionDialog.SetMaxLength(len(str(shopMoney)))
		WithdrawQuestionDialog.SetValue(shopMoney)
		WithdrawQuestionDialog.inputValue.SetEndPosition()

		self.WithdrawQuestionDialog = WithdrawQuestionDialog

	def SumWithdraw(self):
		if not self.WithdrawQuestionDialog:
			return
		
		shopMoney = min(constInfo.ConvertMoneyText(self.WithdrawQuestionDialog.GetText()), 999999999999999)

		if len(self.WithdrawQuestionDialog.GetText()) <= 0:
			return
		
		if int(shopMoney) > self.wndShop.ShopSafeboxValuteAmount:
			shopMoney = self.wndShop.ShopSafeboxValuteAmount

		offlineshop.SendSafeboxGetValutes(shopMoney)
			
		self.WithdrawQuestionDialog.Close()
		self.WithdrawQuestionDialog = None

	def CloseSumWithdraw(self):
		if not self.WithdrawQuestionDialog:
			return False

		self.WithdrawQuestionDialog.Close()
		self.WithdrawQuestionDialog = None
		return True

	def OnCreateShop(self):
		if not self.NameEdit.GetText():
			self.SetPopUpDialog(localeInfo.OFFLINESHOP_NO_NAME)
			return

		shopName = self.NameEdit.GetText()

		if 0 == len(self.itemStockBuilder):
			return

		itemLst = []
		
		for page in range(4):
			for privatePos, (itemWindowType, itemSlotIndex, itemPrice) in self.itemStockBuilder[page].items():
				tupleinfo = (itemWindowType, itemSlotIndex, itemPrice, privatePos, page)
				itemLst.append(tupleinfo)
		
		if (len(itemLst) == 0):
			chat.AppendChat(1, localeInfo.OFFLINE_SHOP_NO_ITEMS_IN_SHOP)
			return
		

		global OFFLINESHOP_EXTEND_TIME_PREMIUM, OFFLINESHOP_CREATE_SHOP_TIME_NORMAL
		totaltime = OFFLINESHOP_CREATE_SHOP_TIME_NORMAL
		
		itemTuple = tuple(itemLst)

		shopName = self.colorPicker.GetColor() + self.NameEdit.GetText()

		if app.ENABLE_SHOP_DECORATION:
			offlineshop.SendShopCreate(shopName, totaltime, self.wndShopDecoration.selectedNPC, itemTuple)
		else:
			offlineshop.SendShopCreate(shopName, totaltime, itemTuple)

	def remove_prefix(self, text, prefix):
		if text.startswith(prefix):
			return text[len(prefix):]
		return text

	def AskIncreaseTimeShop(self):
		if self.QuestionDialog:
			self.OnCloseQuestionDialog()

		if not self.QuestionDialog:
			QuestionDialog = uicommon.QuestionDialog()
			QuestionDialog.SetText(localeInfo.OFFLINESHOP_REFILL_TIME_QUESTION)
			QuestionDialog.SetAcceptEvent(ui.__mem_func__(self.OnRefillShopTime))
			QuestionDialog.SetCancelEvent(ui.__mem_func__(self.OnCloseQuestionDialog))
			self.QuestionDialog = QuestionDialog

		self.QuestionDialog.Open()
		return True		

	def GetMaxRefill(self, ex_day):
		global OFFLINESHOP_EXTEND_TIME_PREMIUM, OFFLINESHOP_EXTEND_TIME_NORMAL
		while True:
			if self.wndShop.ShopOpenInfo["duration"] + ex_day > OFFLINESHOP_EXTEND_TIME_NORMAL:
				ex_day -= 1
				continue

			break
			
		return ex_day

	def OnRefillShopTime(self):
		global OFFLINESHOP_PREMIUM_EXTEND_DAY, OFFLINESHOP_NORMAL_EXTEND_DAY
		updateDay = OFFLINESHOP_PREMIUM_EXTEND_DAY
		Extend1Day = self.GetMaxRefill(updateDay*60*24)

		if Extend1Day <= 0:
			chat.AppendChat(1, localeInfo.OFFLINESHOP_REFILL_TIME_CANNOT)
			self.OnCloseQuestionDialog()
			return

		offlineshop.SendExtendTime(Extend1Day)

		constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(0)
		self.OnCloseQuestionDialog()
		return True

	def ClearCachePos(self, page, id):
		if page in CACHE_ITEMS_ID:
			if id in CACHE_ITEMS_ID[page]:
				del CACHE_ITEMS_ID[page][id]

	def SetFastAddItem(self, state):
		global ITEM_ADDABLE_FAST
		ITEM_ADDABLE_FAST = state

	if app.WJ_ENABLE_TRADABLE_ICON:
		def CantTradableItem(self, slotIndex, invenType):
			itemIndex = player.GetItemIndex(invenType, slotIndex)

			if itemIndex:
					
				if player.IsAntiFlagBySlot(invenType, slotIndex, item.ANTIFLAG_GIVE) or player.IsAntiFlagBySlot(invenType, slotIndex, item.ANTIFLAG_MYSHOP):
					return True

			return False
			
		def BindInterface(self, interface):
			self.interface = interface

		def OnTop(self):
			if not self.interface:
				return
			
			if IsBuildingShop():
				self.interface.SetOnTopWindow(player.ON_TOP_WND_OFFLINE_SHOP)
				self.interface.RefreshMarkInventoryBag()
			else:
				self.interface.SetOnTopWindow(player.ON_TOP_WND_NONE)
				self.interface.RefreshMarkInventoryBag()

class OfflineShopNotification(ui.Board):

	def __init__(self):
		ui.Board.__init__(self)
		self.SetSize(240, 185)
		self.SetCenterPosition()
		self.interface = constInfo.GetInterfaceInstance()
		self.AddFlag("movable")
		self.PATH_ROOT = "offlineshop/lightwork/shopseller/"

	def CloseAllFunction(self):
		self.interface.wndShopOffline.wndShop.CloseAllNotifications()

	def Open(self, idx, itemVnum, itemPrice, itemCount):
		self.itemVnum = itemVnum
		self.itemPrice = itemPrice
		self.itemCount = itemCount
		self.idx = idx

		item.SelectItem(itemVnum)
		itemName = item.GetItemName()

		self.textLine = ui.TextLine()
		self.textLine.SetParent(self)
		self.textLine.SetPosition(113, 128)
		self.textLine.SetHorizontalAlignCenter()
		self.textLine.SetVerticalAlignCenter()
		self.textLine.SetText(localeInfo.OFFLINESHOP_NOTIF_ITEM_INFO % (itemName, itemCount, itemPrice))
		self.textLine.Show()

		self.boardItem = ui.ExpandedImageBox()
		self.boardItem.SetParent(self)
		self.boardItem.SetPosition(0, 10)
		self.boardItem.AddFlag("not_pick")
		self.boardItem.LoadImage(self.PATH_ROOT + "bg_item.png")
		self.boardItem.SetWindowHorizontalAlignCenter()
		self.boardItem.Show()

		self.ItemIcon = ui.ExpandedImageBox()
		self.ItemIcon.SetParent(self.boardItem)
		self.ItemIcon.SetPosition(0, 0)
		self.ItemIcon.LoadImage(item.GetIconImageFileName())
		self.ItemIcon.SetWindowHorizontalAlignCenter()
		self.ItemIcon.SetWindowVerticalAlignCenter()
		self.ItemIcon.Show()

		self.CloseButton = ui.MakeButton(self, 19, 142, False, "offlineshop/lightwork/shopbuilder/", "btn_big_default.png", "btn_big_hover.png", "btn_big_down.png")
		self.CloseButton.SetText(localeInfo.UI_CLOSE)
		self.CloseButton.SetEvent(ui.__mem_func__(self.Close))

		self.CloseAllButton = ui.MakeButton(self, 19 + self.CloseButton.GetWidth() + 5, 142, False, "offlineshop/lightwork/shopbuilder/", "btn_big_default.png", "btn_big_hover.png", "btn_big_down.png")
		self.CloseAllButton.SetText(localeInfo.OFFLINESHOP_NOTIF_CLOSE_ALL)
		self.CloseAllButton.SetEvent(ui.__mem_func__(self.CloseAllFunction))
		self.Show()

	def __del__(self):
		ui.Board.__del__(self)

	def Destroy(self):

		self.itemVnum = None
		self.itemPrice = None
		self.itemCount = None
		self.idx = None

		self.Hide()

	def OnPressEscapeKey(self):
		self.Close()
		return True

	def Close(self):
		self.interface.wndShopOffline.wndShop.CloseButtonEvent(self.idx)

if app.ENABLE_SHOP_DECORATION:
	class ShopDecoration(ui.Board):

		RENDER_TARGET_INDEX = 25
		RENDER_TARGET_INDEX_BOARD = 26

		def __init__(self):
			ui.Board.__init__(self)
			self.loaded = 0
			self.SetDefaultData()
			self.loadWindow()

		def __del__(self):
			ui.Board.__del__(self)

		def loadWindow(self):
			if self.loaded:
				return
			self.loaded = 1
			self.AddFlag("float")
			self.AddFlag("movable")
			self.Hide()

			self.SetSize(480, 350)
			self.SetCenterPosition()

			self.loadBackgroundImages()
			self.loadRenderTarget()

		def loadBackgroundImages(self):
			self.mainBorder = ui.BorderA()
			self.mainBorder.SetParent(self)
			self.mainBorder.SetPosition(15, 15)
			self.mainBorder.SetSize(450, 280)
			self.mainBorder.Show()

			self.titleImg = ui.ExpandedImageBox()
			self.titleImg.SetParent(self.mainBorder)
			self.titleImg.LoadImage("offlineshop/lightwork/shopeditor/shoptitle.png")
			self.titleImg.SetPosition(16, 20)
			self.titleImg.Show()

			self.titleText = ui.TextLine()
			self.titleText.SetParent(self.titleImg)
			self.titleText.SetPosition(0, 0)
			self.titleText.SetText(localeInfo.OFFLINESHOP_SHOP_DECO_TITLE)
			self.titleText.SetHorizontalAlignCenter()
			self.titleText.SetVerticalAlignCenter()
			self.titleText.SetWindowHorizontalAlignCenter()
			self.titleText.SetWindowVerticalAlignCenter()
			self.titleText.Show()

			self.btnSelect = ui.MakeButton(self, 175, 308, False, PATH_ROOT_BUILD, "btn_norm.png", "btn_hover.png", "btn_down.png")
			self.btnSelect.SetText(localeInfo.UI_OK)
			self.btnSelect.SetEvent(ui.__mem_func__(self.Confirm))

			self.btnClose = ui.MakeButton(self, 250, 308, False, PATH_ROOT_BUILD, "btn_norm.png", "btn_hover.png", "btn_down.png")
			self.btnClose.SetText(localeInfo.UI_CANCEL)
			self.btnClose.SetEvent(ui.__mem_func__(self.Close))

			self.decorationBtns = []
			self.decorationNames = [
				localeInfo.OFFLINESHOP_SHOP_DECO_0,
				localeInfo.OFFLINESHOP_SHOP_DECO_1,
				localeInfo.OFFLINESHOP_SHOP_DECO_2,
				localeInfo.OFFLINESHOP_SHOP_DECO_3,
				localeInfo.OFFLINESHOP_SHOP_DECO_4,
				localeInfo.OFFLINESHOP_SHOP_DECO_5
			]
			for i in range(6):
				self.decorationBtns.append(i)
				self.decorationBtns[i] = ui.RadioButton()
				self.decorationBtns[i].SetParent(self.mainBorder)
				self.decorationBtns[i].SetPosition(35, 60 + (i * 35))
				self.decorationBtns[i].SetUpVisual("offlineshop/lightwork/searchshop/btn_filter_norm.png")
				self.decorationBtns[i].SetOverVisual("offlineshop/lightwork/searchshop/btn_filter_hover.png")
				self.decorationBtns[i].SetDownVisual("offlineshop/lightwork/searchshop/btn_filter_down.png")
				self.decorationBtns[i].Show()
				self.decorationBtns[i].SetText(self.decorationNames[i])

				self.decorationBtns[i].SetEvent(lambda arg=i: self.SelectDecoration(arg))
				self.decorationBtns[0].Down()

		def loadRenderTarget(self):

			self.wndRender = ui.BorderA()
			self.wndRender.SetParent(self.mainBorder)
			self.wndRender.SetSize(224, 232)
			self.wndRender.SetPosition(215, 25)
			self.wndRender.Show()

			self.ModelPreview = ui.RenderTarget()
			self.ModelPreview.SetParent(self.wndRender)
			self.ModelPreview.SetWindowHorizontalAlignCenter()
			self.ModelPreview.SetSize(218, 228)
			self.ModelPreview.SetPosition(1, 2)
			self.ModelPreview.SetRenderTarget(self.RENDER_TARGET_INDEX)
			self.ModelPreview.Show()

			renderTarget.SetBackground(self.RENDER_TARGET_INDEX, "d:/ymir work/ui/game/myshop_deco/model_view_bg.sub")
			renderTarget.SetVisibility(self.RENDER_TARGET_INDEX, True)
			renderTarget.SelectModel(self.RENDER_TARGET_INDEX, self.selectedNPC)

		def Destroy(self):
			self.SetDefaultData()
			self.Close()

		def Open(self):
			self.SetTop()
			self.Show()
			renderTarget.SetVisibility(self.RENDER_TARGET_INDEX, True)
			self.selectedNPC = 30000

		def Close(self):
			# Wylaczenie bylo tylko w OnPressEscapeKey, wiec zamkniecie przyciskiem (OnPressExitKey
			# -> Close) zostawialo podglad wlaczony, a silnik deformowal jego model co klatke.
			renderTarget.SetVisibility(self.RENDER_TARGET_INDEX, False)
			self.Hide()

		def OnPressEscapeKey(self):
			self.Close()
			return True

		def OnPressExitKey(self):
			self.Close()
			return True

		def SetDefaultData(self):
			self.selectedNPC = 30000
			self.decorationBtns = []
			self.decorationNPC = [30000, 30002, 30003, 30004, 30005, 30006]
			self.interface = None
			self.temp = 0

		def SelectDecoration(self, selected):
			self.selectedIdx = selected
			for index in range(len(self.decorationBtns)):
				self.decorationBtns[index].SetUp()
			self.decorationBtns[selected].Down()
			self.temp = self.decorationNPC[selected]
			renderTarget.SelectModel(self.RENDER_TARGET_INDEX, self.temp)

		def Confirm(self):
			self.selectedNPC = self.temp
			self.Close()

class SoldNotification(ui.Button):

	def __init__(self):
		ui.Button.__init__(self)
		self.SetPosition(wndMgr.GetScreenWidth() - 278, 110)
		self.eventType = None

	def __del__(self):
		ui.Button.__del__(self)

	def Open(self):
		self.SetUpVisual("offlineshop/lightwork/notification/new_shop_inventory_button_base.tga")
		self.SetDownVisual("offlineshop/lightwork/notification/new_shop_inventory_button_down.tga")
		self.SetOverVisual("offlineshop/lightwork/notification/new_shop_inventory_button_over.tga")
		self.SetEvent(ui.__mem_func__(self.eventType))
		self.EnableFlash()
		self.Show()

	def SetNotification(self, event):
		self.eventType = event
