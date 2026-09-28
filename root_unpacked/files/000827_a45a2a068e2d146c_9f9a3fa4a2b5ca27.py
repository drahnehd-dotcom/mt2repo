import ui
import snd
import shop
import mouseModule
import player
import chr
import net
import uiCommon
import localeInfo
import chat
import systemSetting
import item
import app

g_isBuildingOfflineShop = False
g_itemPriceDict = {}
g_offlineShopAdvertisementBoardDict = {}
ITEM_PRICE_LIST_DICT = {}

def Clear():
	global g_itemPriceDict
	global g_isBuildingOfflineShop
	g_itemPriceDict = {}
	g_isBuildingOfflineShop = False
	
def IsOfflineShopItemPriceList():
	global g_itemPriceDict
	if (g_itemPriceDict):
		return True
	else:
		return False
	
def IsBuildingOfflineShop():
	global g_isBuildingOfflineShop
	if (g_isBuildingOfflineShop):
		return True
	else:
		return False
		
def SetOfflineShopItemPrice(itemVnum, itemPrice, itemPrice2):
	global g_itemPriceDict
	g_itemPriceDict[int(itemVnum)] = itemPrice, itemPrice2
	
def GetOfflineShopItemPrice(itemVnum):
	try:
		global g_itemPriceDict
		return g_itemPriceDict[itemVnum]
	except KeyError:
		return 0
		

def UpdateADBoard():
	for key in g_offlineShopAdvertisementBoardDict.keys():
		g_offlineShopAdvertisementBoardDict[key].Show()
		
def DeleteADBoard():
	if (vid not in g_offlineShopAdvertisementBoardDict):
		return
		
	del g_offlineShopAdvertisementBoardDict[vid]
	
def ReadPriceList():
	ITEM_PRICE_LIST_DICT.clear()

	try:
		file = open("_cfg/prices.txt", "r")
	except IOError:
		file = open("_cfg/prices.txt", "w")
		file.close()
		return

	lines = file.readlines()

	for line in lines:
		tokens = line.strip().split("\t")
		if len(tokens) == 3:
			vnum = int(tokens[0])
			price = int(tokens[1])
			price2 = int(tokens[2])
			ITEM_PRICE_LIST_DICT[vnum] = (price, price2)
		elif len(tokens) == 2:
			vnum = int(tokens[0])
			price = int(tokens[1])
			ITEM_PRICE_LIST_DICT[vnum] = (price, None)

	file.close()

def AddPriceToList(vnum, price, price2=None):
	ITEM_PRICE_LIST_DICT[int(vnum)] = (int(price), int(price2) if price2 is not None else None)
	file = open("_cfg/prices.txt", "w")

	for vnum, prices in ITEM_PRICE_LIST_DICT.items():
		price, price2 = prices
		if price2 is not None:
			file.write("{}\t{}\t{}\n".format(vnum, price, price2))
		else:
			file.write("{}\t{}\n".format(vnum, price))

	file.close()

class OfflineShopAdvertisementBoard(ui.ThinBoard):
	def __init__(self):	
		ui.ThinBoard.__init__(self, "UI_BOTTOM")
		self.shopAdvertismentBoardSeen =[]
		self.vid = None
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
		if vid in self.shopAdvertismentBoardSeen:
			self.textLine.SetFontColor(1.0, 0.5, 0.1)
		self.textLine.UpdateRect()
		self.SetSize(len(text) * 6 + 10 * 2, 20)
		self.Show()
		
		g_offlineShopAdvertisementBoardDict[vid] = self
		
	def OnMouseLeftButtonUp(self):
		if (not self.vid):
			return
			
		net.SendOnClickPacket(self.vid)
		if self.vid != player.GetMainCharacterIndex():
			self.textLine.SetFontColor(1.0, 0.5, 0.1)
			self.shopAdvertismentBoardSeen.append(self.vid)
		return TRUE
		
	def OnUpdate(self):
		if (not self.vid):
			return
		
		if (systemSetting.IsShowSalesText()):
			self.Show()
			(x, y) = chr.GetProjectPosition(self.vid, 220)
			self.SetPosition(x - self.GetWidth() // 2, y - self.GetHeight() // 2)
		else:
			for key in g_offlineShopAdvertisementBoardDict.keys():
				g_offlineShopAdvertisementBoardDict[key].Hide()

class OfflineShopBuilder(ui.ScriptWindow):
	def __init__(self):	
		ui.ScriptWindow.__init__(self)
		self.LoadWindow()
		self.itemStock = {}
		self.tooltipItem = None
		self.priceInputBoard = None
		self.title = ""
		if app.WJ_ENABLE_TRADABLE_ICON:
			self.interface = None
			self.wndInventory = None
			self.lockedItems = {i:(-1,-1) for i in range(shop.SHOP_SLOT_COUNT)}
		ReadPriceList()

	def __del__(self):
		ui.ScriptWindow.__del__(self)
		
	def LoadWindow(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "offline/builder.py")
		except:
			import exception
			exception.Abort("OfflineShopBuilderWindow.LoadWindow.LoadObject")
			
		try:
			self.nameLine = self.GetChild("NameLine")
			self.itemSlot = self.GetChild("ItemSlot")
			self.btnOk = self.GetChild("OkButton")
			self.btnClose = self.GetChild("CloseButton")
			self.board = self.GetChild("Board")
		except:
			import exception
			exception.Abort("OfflineShopBuilderWindow.LoadWindow.BindObject")
			
		self.btnOk.SetEvent(ui.__mem_func__(self.OnOk))
		self.btnClose.SetEvent(ui.__mem_func__(self.OnClose))
		self.board.SetCloseEvent(ui.__mem_func__(self.OnClose))
		
		self.itemSlot.SetSelectEmptySlotEvent(ui.__mem_func__(self.OnSelectEmptySlot))
		self.itemSlot.SetSelectItemSlotEvent(ui.__mem_func__(self.OnSelectItemSlot))
		self.itemSlot.SetOverInItemEvent(ui.__mem_func__(self.OnOverInItem))
		self.itemSlot.SetOverOutItemEvent(ui.__mem_func__(self.OnOverOutItem))
	
	def Destroy(self):
		self.ClearDictionary()
		
		self.nameLine = None
		self.itemSlot = None
		self.btnOk = None
		self.btnClose = None
		self.board = None
		self.priceInputBoard = None
		if app.WJ_ENABLE_TRADABLE_ICON:
			self.interface = None
			self.wndInventory = None
			self.lockedItems = {i:(-1,-1) for i in range(shop.SHOP_SLOT_COUNT)}
		
	def Open(self, title):
		self.title = title
		
		if (len(title) > 25):
			self.title = title[:22] + "..."
			
		self.itemStock = {}
		shop.ClearOfflineShopStock()
		self.nameLine.SetText(title)
		self.SetCenterPosition()
		self.Refresh()
		self.Show()
		if app.WJ_ENABLE_TRADABLE_ICON:
			self.lockedItems = {i:(-1,-1) for i in range(shop.SHOP_SLOT_COUNT)}
			self.interface.SetOnTopWindow(player.ON_TOP_WND_PRIVATE_SHOP)
			self.interface.RefreshMarkInventoryBag()
		
		global g_isBuildingOfflineShop
		g_isBuildingOfflineShop = True
		
	def Close(self):
		global g_isBuildingOfflineShop
		g_isBuildingOfflineShop = False
		
		self.title = ""
		shop.ClearOfflineShopStock()
		self.Hide()

		if self.priceInputBoard:
			self.priceInputBoard.Close()
			self.priceInputBoard = None

		if app.WJ_ENABLE_TRADABLE_ICON:
			for privatePos, (itemInvenPage, itemSlotPos) in self.lockedItems.items():
				if itemInvenPage == self.wndInventory.GetInventoryPageIndex():
					self.wndInventory.wndItem.SetCanMouseEventSlot(itemSlotPos)

			self.lockedItems = {i:(-1,-1) for i in range(shop.SHOP_SLOT_COUNT)}
			self.interface.SetOnTopWindow(player.ON_TOP_WND_NONE)
			self.interface.RefreshMarkInventoryBag()
		
	def SetItemToolTip(self, tooltipItem):
		self.tooltipItem = tooltipItem
		
	def Refresh(self):
		for i in range(shop.OFFLINE_SHOP_SLOT_COUNT):
			if (i not in self.itemStock):
				self.itemSlot.ClearSlot(i)
				continue
				
			pos = self.itemStock[i]
			itemCount = player.GetItemCount(*pos)
			if (itemCount <= 1):
				itemCount = 0
			self.itemSlot.SetItemSlot(i, player.GetItemIndex(*pos), itemCount)
		
		self.itemSlot.RefreshSlot()
		if app.WJ_ENABLE_TRADABLE_ICON:
			self.RefreshLockedSlot()
		
	def OnSelectEmptySlot(self, selectedSlotPos):

		isAttached = mouseModule.mouseController.isAttached()
		if (isAttached):
			attachedSlotType = mouseModule.mouseController.GetAttachedType()
			attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
			mouseModule.mouseController.DeattachObject()

			if player.SLOT_TYPE_INVENTORY != attachedSlotType and player.SLOT_TYPE_DRAGON_SOUL_INVENTORY != attachedSlotType and\
				(player.SLOT_TYPE_SKILL_BOOK_INVENTORY != attachedSlotType and\
				player.SLOT_TYPE_UPGRADE_ITEMS_INVENTORY != attachedSlotType and\
				player.SLOT_TYPE_STONE_INVENTORY != attachedSlotType and\
				player.SLOT_TYPE_BOX_INVENTORY != attachedSlotType and\
				player.SLOT_TYPE_EFSUN_INVENTORY != attachedSlotType and\
				player.SLOT_TYPE_CICEK_INVENTORY != attachedSlotType and app.ENABLE_SPLIT_INVENTORY_SYSTEM):
				return

			attachedInvenType = player.SlotTypeToInvenType(attachedSlotType)
				
			itemVNum = player.GetItemIndex(attachedInvenType, attachedSlotPos)
			item.SelectItem(itemVNum)

			if item.IsAntiFlag(item.ANTIFLAG_GIVE) or item.IsAntiFlag(item.ANTIFLAG_MYSHOP):
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.OFFLINE_SHOP_CANNOT_SELL_ITEM)
				return

			if app.WJ_ENABLE_TRADABLE_ICON and player.SLOT_TYPE_INVENTORY == attachedSlotType:
				self.CantTradableItem(selectedSlotPos, attachedSlotPos)

			priceInputBoard = uiCommon.MoneyInputDialog()
			priceInputBoard.SetTitle(localeInfo.OFFLINE_SHOP_INPUT_PRICE_DIALOG_TITLE)
			priceInputBoard.SetAcceptEvent(ui.__mem_func__(self.AcceptInputPrice))
			priceInputBoard.SetCancelEvent(ui.__mem_func__(self.CancelInputPrice))
			priceInputBoard.Open()

			
			itemPrice = GetOfflineShopItemPrice(itemVNum)
			if (itemPrice > 0):
				priceInputBoard.SetValue(itemPrice)
			
			self.priceInputBoard = priceInputBoard
			self.priceInputBoard.itemVNum = itemVNum
			self.priceInputBoard.sourceWindowType = attachedInvenType
			self.priceInputBoard.sourceSlotPos = attachedSlotPos
			self.priceInputBoard.targetSlotPos = selectedSlotPos
			
			if itemVNum in ITEM_PRICE_LIST_DICT.keys():
				price, price2 = ITEM_PRICE_LIST_DICT[itemVNum]
				priceInputBoard.SetValue(price)
				priceInputBoard.SetCheque(price2)

	def OnSelectItemSlot(self, selectedSlotPos):
		isAttached = mouseModule.mouseController.isAttached()
		if (isAttached):
			snd.PlaySound("sound/ui/loginfail.wav")
			mouseModule.mouseController.DeattachObject()

		else:
			if (not selectedSlotPos in self.itemStock):
				return

			invenType, invenPos = self.itemStock[selectedSlotPos]
			shop.DelOfflineShopItemStock(invenType, invenPos)
			snd.PlaySound("sound/ui/drop.wav")
			if app.WJ_ENABLE_TRADABLE_ICON:
				(itemInvenPage, itemSlotPos) = self.lockedItems[selectedSlotPos]
				if itemInvenPage == self.wndInventory.GetInventoryPageIndex():
					self.wndInventory.wndItem.SetCanMouseEventSlot(itemSlotPos)

				self.lockedItems[selectedSlotPos] = (-1, -1)
			del self.itemStock[selectedSlotPos]
			self.Refresh()
			
	def AcceptInputPrice(self):
		if (not self.priceInputBoard):
			return True
			
		text = self.priceInputBoard.GetText()
		text2 = self.priceInputBoard.inputChequeValue.GetText()
		if (not text) or (not text2):
			return True
			
		if (not text.isdigit()) or (not text2.isdigit()):	
			return True
			
		if int(text) <= 0 and int(text2) <= 0:
			return True
		
		if int(text) < 0 or int(text2) < 0:
			return True
			
		attachedInvenType = self.priceInputBoard.sourceWindowType
		sourceSlotPos = self.priceInputBoard.sourceSlotPos
		targetSlotPos = self.priceInputBoard.targetSlotPos

		for privatePos, (itemWindowType, itemSlotIndex) in self.itemStock.items():
			if (itemWindowType == attachedInvenType and itemSlotIndex == sourceSlotPos):
				shop.DelOfflineShopItemStock(itemWindowType, itemSlotIndex)
				del self.itemStock[privatePos]
				
		price = str(self.priceInputBoard.GetText())
		price2 = str(self.priceInputBoard.inputChequeValue.GetText())
		
		if (IsOfflineShopItemPriceList()):
			SetOfflineShopItemPrice(self.priceInputBoard.itemVNum, price, price2)
			
		shop.AddOfflineShopItemStock(attachedInvenType, sourceSlotPos, targetSlotPos, price, price2)
		self.itemStock[targetSlotPos] = (attachedInvenType, sourceSlotPos)
		snd.PlaySound("sound/ui/drop.wav")
		
		AddPriceToList(self.priceInputBoard.itemVNum, price, price2)
		
		self.Refresh()
		self.priceInputBoard = None
		return True
		
	def CancelInputPrice(self):
		if app.WJ_ENABLE_TRADABLE_ICON:
			itemInvenPage = self.priceInputBoard.sourceSlotPos // player.INVENTORY_PAGE_SIZE
			itemSlotPos = self.priceInputBoard.sourceSlotPos - (itemInvenPage * player.INVENTORY_PAGE_SIZE)
			if self.wndInventory.GetInventoryPageIndex() == itemInvenPage:
				self.wndInventory.wndItem.SetCanMouseEventSlot(itemSlotPos)

			self.lockedItems[self.priceInputBoard.targetSlotPos] = (-1, -1)

		if self.priceInputBoard:
			self.priceInputBoard.Close()
		self.priceInputBoard = None
		return 1
		
	def OnOk(self):
		if (not self.title):	
			return
		
		if (len(self.itemStock) == 0):
			return
			
		shop.BuildOfflineShop(player.GetName())
		self.Close()
		
	def OnClose(self):
		self.Close()
		
	def OnPressEscapeKey(self):
		self.Close()
		return True
		
	def OnOverInItem(self, slotIndex):
		if (self.tooltipItem):
			if (slotIndex in self.itemStock):
				if hasattr(self.tooltipItem, 'SetOfflineShopBuilderItem'):
					self.tooltipItem.SetOfflineShopBuilderItem(*self.itemStock[slotIndex] + (slotIndex,))
				else:
					self.tooltipItem.SetInventoryItem(slotIndex)
				
	def OnOverOutItem(self):
		if (self.tooltipItem):
			self.tooltipItem.HideToolTip()

	if app.WJ_ENABLE_TRADABLE_ICON:
		def CantTradableItem(self, destSlotIndex, srcSlotIndex):
			itemInvenPage = srcSlotIndex // player.INVENTORY_PAGE_SIZE
			localSlotPos = srcSlotIndex - (itemInvenPage * player.INVENTORY_PAGE_SIZE)
			self.lockedItems[destSlotIndex] = (itemInvenPage, localSlotPos)
			if self.wndInventory.GetInventoryPageIndex() == itemInvenPage:
				self.wndInventory.wndItem.SetCantMouseEventSlot(localSlotPos)

		def RefreshLockedSlot(self):
			if self.wndInventory:
				for privatePos, (itemInvenPage, itemSlotPos) in self.lockedItems.items():
					if self.wndInventory.GetInventoryPageIndex() == itemInvenPage:
						self.wndInventory.wndItem.SetCantMouseEventSlot(itemSlotPos)

				self.wndInventory.wndItem.RefreshSlot()

		def BindInterface(self, interface):
			self.interface = interface

		def OnTop(self):
			if self.interface:
				self.interface.SetOnTopWindow(player.ON_TOP_WND_PRIVATE_SHOP)
				self.interface.RefreshMarkInventoryBag()

		def SetInven(self, wndInventory):
			from _weakref import proxy
			self.wndInventory = proxy(wndInventory)
			
