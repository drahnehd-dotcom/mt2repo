import ui, player, app, chr, constInfo, item, localeInfo, uicommon, grp, chat, math, offlineshop, uitooltip, uiscriptlocale
from _weakref import proxy

import random
from uiFishWiki import GetFishMissionData

PATH = "offlineshop/lightwork/"
PATH_ROOT = "offlineshop/lightwork/searchshop/"
PATH_ROOT2 = "offlineshop/lightwork/shopbuilder/"
PATH_ROOT3 = "offlineshop/lightwork/shopeditor/"
TIME_WAIT = 3
TOTAL_ITEM_PRICE = 0
SELECTED_ITEMS_BUY = {}
FIRST_CHECKBOX = False

MULTI_CATEGORY_ITEMS = {
		item.NONE		: {
		"name" 		: localeInfo.SHOP_SEARCH_ALL,
	},

	item.WEAPON		: {
		"name" : localeInfo.PRIVATESHOPSEARCH_WEAPON,
		"subtypes"	: {
			item.WEAPON_SWORD			:	localeInfo.PRIVATESHOPSEARCH_SWORD,
			item.WEAPON_DAGGER			:	localeInfo.PRIVATESHOPSEARCH_DAGGER,
			item.WEAPON_BOW				:	localeInfo.PRIVATESHOPSEARCH_BOW,
			item.WEAPON_TWO_HANDED		:	localeInfo.PRIVATESHOPSEARCH_TWOSWORD,
			item.WEAPON_BELL			:	localeInfo.PRIVATESHOPSEARCH_BELL,
			item.WEAPON_FAN				:	localeInfo.PRIVATESHOPSEARCH_FAN,
		},
	},

	item.ARMOR		: {
		"name" : localeInfo.PRIVATESHOPSEARCH_ARMOR,
		"subtypes"	: {
			item.ARMOR_BODY			:	localeInfo.PRIVATESHOPSEARCH_BODY,
			item.ARMOR_HEAD			:	localeInfo.PRIVATESHOPSEARCH_HEAD,
			item.ARMOR_SHIELD		:	localeInfo.PRIVATESHOPSEARCH_SHIELD,
			item.ARMOR_WRIST		:	localeInfo.CATEGORY_JEWELRY_ARMOR_WRIST,
			item.ARMOR_FOOTS		:	localeInfo.PRIVATESHOPSEARCH_FOOTS,
			item.ARMOR_NECK			:	localeInfo.PRIVATESHOPSEARCH_NECK,
			item.ARMOR_EAR			:	localeInfo.PRIVATESHOPSEARCH_EAR,
		},
		"extra_subtypes" : {
			item.BELT	:localeInfo.PRIVATESHOPSEARCH_BELT,
			item.ARMOR_GLOVE :localeInfo.PRIVATESHOPSEARCH_GLOVE
		},
	},

	item.COSTUME		: {
		"name" : localeInfo.PRIVATESHOPSEARCH_COSTUME,
		"subtypes"	: {
			item.COSTUME_TYPE_BODY			:	localeInfo.PRIVATESHOPSEARCH_COSTUMEBODY,
			item.COSTUME_TYPE_HAIR			:	localeInfo.PRIVATESHOPSEARCH_COSTUMEHAIR,
			item.COSTUME_TYPE_WEAPON		:	localeInfo.CATEGORY_COSTUMES_COSTUME_WEAPON,
			item.COSTUME_TYPE_ACCE			:	localeInfo.PRIVATESHOPSEARCH_COSTUME_ACCE,
			item.COSTUME_TYPE_STOLE			:	localeInfo.PRIVATESHOPSEARCH_COSTUME_ACCE_SKIN,
			item.COSTUME_TYPE_MOUNT			:	localeInfo.PRIVATESHOPSEARCH_COSTUME_MOUNT,
		},
	},

}

CATEGORY_ITEMS = {

	item.METIN		: {
		"name" : localeInfo.PRIVATESHOPSEARCH_METIN,
	},

	item.FISH		: {
		"name" : localeInfo.PRIVATESHOPSEARCH_FISH,
	},

	item.SKILLBOOK		: {
		"name" : localeInfo.PRIVATESHOPSEARCH_SKILLBOOK,
	},

	item.BLEND		: {
		"name" : localeInfo.PRIVATESHOPSEARCH_BLEND,
	},

	item.GIFTBOX		: {
		"name" : localeInfo.PRIVATESHOPSEARCH_GIFTBOX,
	},

	item.USE		:{
		"name": localeInfo.PRIVATESHOPSEARCH_USEITEM,
	},

	item.MATERIAL		:{
		"name": localeInfo.PRIVATESHOPSEARCH_RESOURCE,
	}
}

MAX_CATEGORY_ITEMS = len(CATEGORY_ITEMS)+ len(MULTI_CATEGORY_ITEMS)


class ListBoxItem(ui.Window):
	class NewItem(ui.Window):
		def __init__(self, parent, index, data, tooltip):
			ui.Window.__init__(self)
			self.background = None
			self.OnClear()
			self.Index = index
			self.InfoData = data
			self.tooltip = tooltip

			Vnum = data["vnum"]
			count = data["count"]
		
			item.SelectItem(Vnum)
			_, self.itemSize = item.GetItemSize()

			price = data["price"]
			priceYangColor = constInfo.GetPriceColor(price)


			textYang = str(localeInfo.NumberToMoneyString(price))
			
			pid = 0

			name 	= data["owner_name"]
			seller = name

			self.background = ui.ExpandedImageBox()
			self.background.SetParent(self)
			self.OnMouseOverOut2()
			
			self.background.OnMouseOverIn = ui.__mem_func__(self.OnMouseOverIn2)
			self.background.OnMouseOverOut = ui.__mem_func__(self.OnMouseOverOut2)
			self.background.OnMouseLeftButtonDown = ui.__mem_func__(self.OnMouseLeftButtonDown)	
			self.background.Show()
			
			self.SetSize(self.background.GetWidth() - 2, self.background.GetHeight())

			countText = str(count) + "x " if count > 1 else ""

			ItemName = item.GetItemName()
			
			if len(ItemName) >= 25:
				ItemName = ItemName[:25] + ".."

			self.ItemSlotBase = ui.ExpandedImageBox()
			self.ItemSlotBase.SetParent(self)
			self.ItemSlotBase.SetPosition(26, 0)
			self.ItemSlotBase.LoadImage("offlineshop/lightwork/slot_32x%d.tga" % (self.itemSize * 32))
			self.ItemSlotBase.SetWindowVerticalAlignCenter()
			self.ItemSlotBase.SetStringEvent("MOUSE_OVER_IN", ui.__mem_func__(self.IconOnMouseOverIn))
			self.ItemSlotBase.SetStringEvent("MOUSE_OVER_OUT", ui.__mem_func__(self.IconOnMouseOverOut))
			self.ItemSlotBase.OnMouseRightButtonDown = ui.__mem_func__(self.ClickItemSlot)
			self.ItemSlotBase.Show()
			if self.itemSize > 2:
				self.ItemSlotBase.SetScale(0.95, 0.95)
				self.ItemSlotBase.SetPosition(26, -3)

			self.ItemIcon = ui.ExpandedImageBox()
			self.ItemIcon.SetParent(self.ItemSlotBase)
			self.ItemIcon.AddFlag("not_pick")
			self.ItemIcon.LoadImage(item.GetIconImageFileName())
			self.ItemIcon.SetWindowVerticalAlignCenter()
			self.ItemIcon.SetWindowHorizontalAlignCenter()
			self.ItemIcon.Show()
			if self.itemSize > 2:
				self.ItemIcon.SetScale(0.95, 0.95)
				
			itemType = item.GetItemType()
			if itemType == item.FISH:
				fishData = GetFishMissionData(Vnum)
				if fishData != None:
					socketValue = data["socket"][0] if len(data["socket"]) > 0 else 0
					if socketValue >= fishData[1]*100:
						self.FishAddonIcon = ui.ExpandedImageBox()
						self.FishAddonIcon.SetParent(self.ItemIcon)
						self.FishAddonIcon.AddFlag("not_pick")
						self.FishAddonIcon.LoadImage("zaris/fish_wiki/fish_addon.png")
						self.FishAddonIcon.SetPosition(0, 0)
						self.FishAddonIcon.Show()
						
			self.wndItemName = ui.TextLine()
			self.wndItemName.SetParent(self)
			self.wndItemName.AddFlag("not_pick")
			self.wndItemName.SetPosition(65, 0)
			self.wndItemName.SetText(str(countText) + ItemName)
			self.wndItemName.SetWindowVerticalAlignCenter()
			self.wndItemName.SetVerticalAlignCenter()
			self.wndItemName.Show()

			self.wndItemPrice = ui.TextLine()
			self.wndItemPrice.SetParent(self)
			self.wndItemPrice.AddFlag("not_pick")
			self.wndItemPrice.SetPosition(24, 0)
			self.wndItemPrice.SetText(textYang)
			self.wndItemPrice.SetWindowHorizontalAlignCenter()
			self.wndItemPrice.SetHorizontalAlignCenter()
			self.wndItemPrice.SetWindowVerticalAlignCenter()
			self.wndItemPrice.SetVerticalAlignCenter()
			self.wndItemPrice.SetTextColor(priceYangColor)
			self.wndItemPrice.Show()


			self.CheckBox = ui.ExpandedImageBox()
			self.CheckBox.SetParent(self)
			self.CheckBox.SetPosition(6, 0)
			self.CheckBox.LoadImage("d:/ymir work/ui/game/biolog_system/select_button01.png")
			self.CheckBox.SetWindowVerticalAlignCenter()
			self.CheckBox.OnMouseLeftButtonDown = ui.__mem_func__(self.OnCheckBox)
			self.CheckBox.OnMouseOverIn = ui.__mem_func__(self.OnMouseOverInCheckbox)
			self.CheckBox.OnMouseOverOut = ui.__mem_func__(self.OnMouseOverOutCheckbox)
			self.CheckBox.Show()
	
			self.wndSellerName = ui.TextLine()
			self.wndSellerName.SetParent(self)
			self.wndSellerName.AddFlag("not_pick")
			self.wndSellerName.SetPosition(79, 0)
			self.wndSellerName.SetText(str(seller))
			self.wndSellerName.SetWindowHorizontalAlignRight()
			self.wndSellerName.SetHorizontalAlignRight()
			self.wndSellerName.SetWindowVerticalAlignCenter()
			self.wndSellerName.SetVerticalAlignCenter()
			self.wndSellerName.Show()

			self.IconWhisperSeller = ui.ExpandedImageBox()
			self.IconWhisperSeller.SetParent(self)
			self.IconWhisperSeller.SetPosition(175+150+120+16, 0)
			self.IconWhisperSeller.LoadImage(PATH_ROOT + "message_icon.tga")
			self.IconWhisperSeller.OnMouseLeftButtonDown = ui.__mem_func__(self.OnMouseLeftWhisperSeller)
			self.IconWhisperSeller.SetStringEvent("MOUSE_OVER_IN", ui.__mem_func__(self.WhisperOverIn))
			self.IconWhisperSeller.SetStringEvent("MOUSE_OVER_OUT", ui.__mem_func__(self.WhisperOverOut))
			self.IconWhisperSeller.SetWindowVerticalAlignCenter()
			self.IconWhisperSeller.Show()

			self.IconPlayerNameItem = ui.ExpandedImageBox()
			self.IconPlayerNameItem.SetParent(self)
			self.IconPlayerNameItem.SetPosition(175+150+120+25+16, 0)
			self.IconPlayerNameItem.LoadImage(PATH_ROOT + "search_btn_norm.tga")
			self.IconPlayerNameItem.SetStringEvent("MOUSE_OVER_IN", ui.__mem_func__(self.PlayerNameOverIn))
			self.IconPlayerNameItem.SetStringEvent("MOUSE_OVER_OUT", ui.__mem_func__(self.PlayerNameOverOut))
			self.IconPlayerNameItem.OnMouseLeftButtonDown = ui.__mem_func__(self.OnMouseLeftSellerName)
			self.IconPlayerNameItem.SetWindowVerticalAlignCenter()
			self.IconPlayerNameItem.Show()


			if self.InfoData["id"] in SELECTED_ITEMS_BUY:
				self.IsSelected = True
				self.CheckBox.LoadImage("d:/ymir work/ui/game/biolog_system/select_button01.png")

			self.OnMouseOverOut2()

		def WikiOverIn(self):
			pass

		def WikirOverOut(self):
			pass

		def WhisperOverIn(self):
			self.IconWhisperSeller.LoadImage(PATH_ROOT + "message_icon_over.tga")

		def WhisperOverOut(self):
			self.IconWhisperSeller.LoadImage(PATH_ROOT + "message_icon.tga")

		def PlayerNameOverIn(self):
			self.IconPlayerNameItem.LoadImage(PATH_ROOT + "search_btn_hover.tga")

		def PlayerNameOverOut(self):
			self.IconPlayerNameItem.LoadImage(PATH_ROOT + "search_btn_norm.tga")

		def ClickItemSlot(self):
			if app.IsPressed(app.DIK_LCONTROL):
				self.tooltip.__ModelPreviewOpen(self.InfoData["vnum"], self.tooltip.__ItemGetRace(), "weapon")
				return

		def OnRender(self):
			xList, yList = self.parent.GetGlobalPosition()
			widthList, heightList = self.parent.GetWidth(), self.parent.GetHeight()	
		
			images = [self.background, self.CheckBox, self.ItemSlotBase, self.ItemIcon, self.IconWhisperSeller, self.IconPlayerNameItem]
			for img in images:
				if img:
					img.SetClipRect(xList, yList, xList + widthList, yList + heightList)
		
			textList = [self.wndItemName, self.wndItemPrice, self.wndSellerName]
			for text in textList:
				if text:
					text.SetClippingMaskWindow(self.parent)
		

		def OnMouseOverIn2(self):
			app.SetCursor(app.BUY)
			if not self.IsSelected:
				self.background.LoadImage(PATH_ROOT + "field_%d_ovein.png" % (self.itemSize))
			

		def OnMouseOverOut2(self):
			if self.IsSelected:
				self.background.LoadImage(PATH_ROOT + "field_%d_selected.png" % (self.itemSize))
				return
		
			colorField = "black"
			if self.Index % 2 == 0:
				colorField = "white"
		
			self.background.LoadImage(PATH_ROOT + "field_%d_%s.png" % (self.itemSize, colorField))
			app.SetCursor(app.NORMAL)

		def SetPopUpDialog(self, msg):
			self.popupMessage = uicommon.PopupDialog()
			self.popupMessage.SetWidth(250)
			self.popupMessage.SetText(msg)
			self.popupMessage.Open()
			self.popupMessage.SetAutoClose(True)

		def SetBlock(self):
			self.bIsBlocked = True

		def SetPopUpDialog(self, msg, boardsize = 250, waitTime = "Normal"):
			self.popupMessage = uicommon.PopupDialog()
			self.popupMessage.SetWidth(boardsize)
			self.popupMessage.SetText(msg)
			self.popupMessage.Open()
			if waitTime == "Long":
				self.popupMessage.SetAutoCloseLong(True)
			else:
				self.popupMessage.SetAutoClose(True)

		def OnCheckBox(self):

			global FIRST_CHECKBOX, TOTAL_ITEM_PRICE

			if not self.IsSelected:
				if int(self.InfoData["price"]) > player.GetMoney():
					self.SetPopUpDialog(localeInfo.SHOP_MONEY_NOT_ENOUGH)
					return

				if int(TOTAL_ITEM_PRICE) + int(self.InfoData["price"]) > player.GetMoney():
					self.SetPopUpDialog(localeInfo.SHOP_MONEY_NOT_ENOUGH2, 385)
					return

			if FIRST_CHECKBOX == False:
				self.SetPopUpDialog(localeInfo.SHOP_SEARCH_MULTIBUY_ACTIVATED, 285, "Long")
				FIRST_CHECKBOX = True

			if self.IsSelected:
				self.IsSelected = False
				self.CheckBox.LoadImage("d:/ymir work/ui/game/biolog_system/select_button01.png")
				
				if self.InfoData["id"] in SELECTED_ITEMS_BUY:
					del SELECTED_ITEMS_BUY[self.InfoData["id"]]
				TOTAL_ITEM_PRICE -= int(self.InfoData["price"])

			else:
				self.IsSelected = True
				self.CheckBox.LoadImage("d:/ymir work/ui/game/biolog_system/select_button02.png")
				TOTAL_ITEM_PRICE += int(self.InfoData["price"])
				SELECTED_ITEMS_BUY[self.InfoData["id"]] = self.InfoData["owner"]
	
			self.OnMouseOverOut2()
			if self.CheckBox.IsIn():
				self.OnMouseOverInCheckbox()

		def OnMouseOverInCheckbox(self):
			if self.IsSelected:
				if self.tooltip:
					self.tooltip.ClearToolTip()
					self.tooltip.AlignHorizonalCenter()
					self.tooltip.AutoAppendNewTextLine(localeInfo.SHOP_SEARCH_REMOVE_FROM_THE_BASKET)
					self.tooltip.Show()
			else:
				if self.tooltip:
					self.tooltip.ClearToolTip()
					self.tooltip.AlignHorizonalCenter()
					self.tooltip.AutoAppendNewTextLine(localeInfo.SHOP_SEARCH_ADD_TO_BASKET)
					self.tooltip.Show()

		def OnMouseOverOutCheckbox(self):
			if self.tooltip:
				self.tooltip.Hide()

		def OnMouseLeftWhisperSeller(self):
			if self.WhisperEvent:
				self.WhisperEvent(self.wndSellerName.GetText())

		def OnMouseLeftSellerName(self):
			if self.PlayerNameSearch:
				self.PlayerNameSearch(self.wndSellerName.GetText())

		def OnMouseLeftWiki(self):
			if self.wikiSearchEvent:
				self.wikiSearchEvent(self.InfoData["vnum"])

		def OnMouseLeftButtonDown(self):
			global SELECTED_ITEMS_BUY

			if self.clickEvent:
				if int(self.InfoData["price"]) > player.GetMoney():
					self.SetPopUpDialog(localeInfo.SHOP_MONEY_NOT_ENOUGH)
					return

				if len(SELECTED_ITEMS_BUY) > 0:
					self.OnCheckBox()
				else:
					self.clickEvent(self.InfoData["owner"], self.InfoData["id"], self.wndItemName.GetText())

		def __del__(self):
			ui.Window.__del__(self)
			self.OnClear()

		def OnClear(self):
			self.IsSelected = False
			self.bIsBlocked = False
			self.vnum = 0
			self.xBase = 0
			self.yBase = 0

			self.overInEventIconImage = None
			self.overOutEventIconImage = None
			self.clickEvent = None
			self.WhisperEvent = None
			self.PlayerNameSearch = None
			self.wikiSearchEvent = None
			if self.background != None:
				self.background.Hide()
			self.background = None
			self.CheckBox = None
			self.ItemSlotBase = None

		def SetParent(self, parent):
			ui.Window.SetParent(self, parent)
			self.parent = proxy(parent)

		def SetBasePosition(self, x, y):
			self.xBase = x
			self.yBase = y
			
		def GetBasePosition(self):
			return (self.xBase, self.yBase)
			
		def SetOverInEvent(self, event):
			self.overInEventIconImage = event
			
		def SetOverOutEvent(self, event):
			self.overOutEventIconImage = event
			
		def SetClickEvent(self, event):
			self.clickEvent = event

		def SetWhisperEvent(self, event):
			self.WhisperEvent = event
			
		def SetPlayerNameSearch(self, event):
			self.PlayerNameSearch = event

		def SetWikiItemSearch(self, event):
			self.wikiSearchEvent = event

		def IconOnMouseOverIn(self):
			if self.overInEventIconImage:
				self.overInEventIconImage(self.InfoData)



		def IconOnMouseOverOut(self):
			if self.overOutEventIconImage:
				self.overOutEventIconImage()
			if self.tooltip:
				self.tooltip.Hide()

	def __init__(self):
		ui.Window.__init__(self)
		self.OnClear()
		
		self.tooltipItem = uitooltip.ItemToolTip()
		self.tooltipItem.Hide()

	def __del__(self):
		ui.Window.__del__(self)
		self.OnClear()
		
		self.tooltipItem = None
		
	def Destroy(self):
		self.tooltipItem = None
		self.OnClear()
		
	def OnClear(self):
		global TOTAL_ITEM_PRICE
		self.SetFuncDown = None
		self.BuyAskEvent = None
		self.WhishperEventFunc = None
		self.itemList = []
		self.scrollBar = None
		self.tooltipItem = None
		self.selectEvent = None
		self.selectedItemVnum = 0
		TOTAL_ITEM_PRICE = 0

	def SetEventBuy(self, event):
		self.BuyAskEvent = event

	def SetEventWhisper(self, event):
		self.WhishperEventFunc = event

	def SetEventPlayerName(self, event):
		self.PlayerNameSearchEvent = event

	def SetEventWikiSearch(self, event):
		self.wikiSearchEventFunc = event

	def SetParent(self, parent):
		ui.Window.SetParent(self, parent)
		
		self.SetPosition(5, 5)
		self.SetSize(parent.GetWidth() - 10, parent.GetHeight() - 10)
		
	def SetScrollBar(self, scrollBar):
		scrollBar.SetScrollEvent(ui.__mem_func__(self.__OnScroll))
		scrollBar.SetScrollStep(0.03)
		self.scrollBar=scrollBar

	def SetSelectEvent(self, event):
		self.selectEvent = event
		
	def __OnScroll(self):
		self.AdjustItemPositions(True)
			
	def GetTotalItemHeight(self):
		totalHeight = 0
		
		if self.itemList:
			for itemH in self.itemList:
				if itemH.bIsBlocked:
					continue
				totalHeight += itemH.GetHeight() -.8
			
		return totalHeight

	def GetItemCount(self):
		return len(self.itemList)

	def AppendItem(self, index, infoData):
		itemL = self.NewItem(self, index, infoData, self.tooltipItem)
		itemL.SetParent(self)

		if len(self.itemList) == 0:
			itemL.SetBasePosition(0, 0)
		else:
			x, y = self.itemList[-1].GetLocalPosition()
			y += 2
			itemL.SetBasePosition(0, y + self.itemList[-1].GetHeight())

		itemL.SetWhisperEvent(ui.__mem_func__(self.OnWhisperName))
		itemL.SetPlayerNameSearch(ui.__mem_func__(self.OnSearchPlayerName))
		itemL.SetWikiItemSearch(ui.__mem_func__(self.OnSearchWikiSearch))
		itemL.SetClickEvent(ui.__mem_func__(self.SelectItem))
		itemL.SetOverInEvent(ui.__mem_func__(self.OverInItem))
		itemL.SetOverOutEvent(ui.__mem_func__(self.OverOutItem))		
		itemL.Show()

		self.itemList.append(itemL)

		self.ResetScrollbar()
		self.AdjustScrollBar()	
		self.AdjustItemPositions()


	def OnWhisperName(self, name):
		if self.WhishperEventFunc:
			self.WhishperEventFunc(name)

	def OnSearchPlayerName(self, name):
		if self.PlayerNameSearchEvent:
			self.PlayerNameSearchEvent(name)

	def OnSearchWikiSearch(self, name):
		if self.wikiSearchEventFunc:
			self.wikiSearchEventFunc(name)

	def OverInItem(self, data):
		if self.tooltipItem and data:
			self.tooltipItem.ClearToolTip()
			metinSlot = [data["socket"][num] for num in range(player.METIN_SOCKET_MAX_NUM)]
			attrSlot	= [(data["attr"][num]['type'], data["attr"][num]['value']) for num in range(player.ATTRIBUTE_SLOT_MAX_NUM)]
			itemPrice, itemCount, pricePerCount = data["price"], data["count"], data["price"] / data["count"]
			self.tooltipItem.AddItemData(data["vnum"], metinSlot, attrSlot)
			self.tooltipItem.AppendSpace(5)
			self.tooltipItem.AppendTextLine(localeInfo.ITEM_PRICE_TITLE, grp.GenerateColor(0.7, 0.7, 0.7, 1.0))
			self.tooltipItem.AppendTextLine(str(localeInfo.NumberToMoneyString(itemPrice)), constInfo.GetPriceColor(itemPrice))
			if itemCount > 1 and pricePerCount > 0:
				self.tooltipItem.AppendSpace(5)
				self.tooltipItem.AppendTextLine(localeInfo.SHOP_SEARCH_ITEM_PRICE_PER_COUNT % (str(localeInfo.NumberToMoneyString(pricePerCount))))

	def OverOutItem(self):
		if self.tooltipItem:
			self.tooltipItem.HideToolTip()

	def SelectItem(self, pID, ItemPos, ItemName):
		if self.BuyAskEvent:
			self.BuyAskEvent(pID, ItemPos, ItemName)

	def AdjustScrollBar(self):
		totalHeight = float(self.GetTotalItemHeight())
		if totalHeight:
			scrollBarHeight = min(float(self.GetHeight()) / totalHeight, 1.0)
		else:
			scrollBarHeight = 1.0
		self.scrollBar.SetMiddleBarSize(scrollBarHeight)
	
	def ResetScrollbar(self):
		self.scrollBar.SetPos(0)
				
	def AdjustItemPositions(self, scrolling = False):		
		scrollPos = self.scrollBar.GetPos()
		totalHeight = self.GetTotalItemHeight() - self.GetHeight()

		idx = 0

		CurIdx, yAccumulate = 0, 0
		for item in self.itemList[idx:]:
			if item.bIsBlocked:
				continue
			
			if scrolling:
				setPos = yAccumulate - int(scrollPos * totalHeight)
				item.SetPosition(0, setPos)
			else:
				item.SetPosition(0, yAccumulate)
				
			item.SetBasePosition(0, yAccumulate)

			CurIdx += 1
			yAccumulate += item.GetHeight() -.75

	def Clear(self):
		range = len(self.itemList)
		
		if range > 0:
			for item in self.itemList:
				item.OnClear()
				item.Hide()
				del item
		
		self.itemList = []
		self.tooltipItem.Hide()

	def RemoveItemBought(self, bOwner, bId):
		itemListRange = len(self.itemList)
		
		if itemListRange > 0:
			for i in range(itemListRange):
				owner = self.itemList[i].InfoData["owner"]
				id = self.itemList[i].InfoData["id"]
				if owner == bOwner and id == bId:
					self.itemList[i].IsSelected = False
					self.itemList[i].Hide()
					self.itemList[i].SetBlock()
					break
				
			self.ReloadSymmetryBackground()
			self.ResetScrollbar()
			self.AdjustScrollBar()
			self.AdjustItemPositions(True)
	
	def ReloadSymmetryBackground(self):
		itemListRange = len(self.itemList)
		
		if itemListRange > 0:
			CntIndex = 0
			for i in range(itemListRange):
				if self.itemList[i].bIsBlocked:
					continue

				colorField = "black"
				if CntIndex % 2 == 0:
					colorField = "white"
				
				self.itemList[i].background.LoadImage(PATH_ROOT + "field_%d_%s.png" % (self.itemList[i].itemSize, colorField))
				
				self.itemList[i].OnMouseOverOut2()
				
				CntIndex += 1



			
			

	def BuySelectedItems(self):

		global SELECTED_ITEMS_BUY, TOTAL_ITEM_PRICE
		range = len(SELECTED_ITEMS_BUY)
		
		if range > 0:
			for id_key in SELECTED_ITEMS_BUY:
				owner = SELECTED_ITEMS_BUY[id_key]
				offlineshop.SendBuyItemFromSearch(owner, id_key)
			TOTAL_ITEM_PRICE = 0

class FilterWindow(ui.ThinBoardCircle):

	WINDOW_WIDTH = 185
	WINDOW_HEIGHT = 357

	def __init__(self):
		ui.ThinBoardCircle.__init__(self)
		self.loaded = 0

		self.LoadWindow()
		self.generalItems()

	def __del__(self):
		ui.ThinBoardCircle.__del__(self)

	def LoadWindow(self):
		if self.loaded == 1:
			return
		self.loaded = 1	
		self.AddFlag("float")
		self.Hide()

		self.SetSize(self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
		
		self.FilterBgImage = ui.ExpandedImageBox()
		self.FilterBgImage.SetParent(self)
		self.FilterBgImage.SetPosition(-2,0)
		self.FilterBgImage.LoadImage(PATH_ROOT + "filterbg.png")
		self.FilterBgImage.Show()


	def generalItems(self):
		self.itemCountMinBG = ui.MakeImageBox(self, "offlineshop/lightwork/searchshop/searchbgmin.png", 22 - 2, 65 + 35+9)
		self.itemCountMaxBG = ui.MakeImageBox(self, "offlineshop/lightwork/searchshop/searchbgmin.png", 97- 2, 65 + 35+9)

		self.itemLevelMinBG = ui.MakeImageBox(self, "offlineshop/lightwork/searchshop/searchbgmin.png", 22- 2, 65+50 + 13+9)
		self.itemLevelMaxBG = ui.MakeImageBox(self, "offlineshop/lightwork/searchshop/searchbgmin.png", 97- 2,  65+50 + 13+9)

		self.itemAbsMinBG = ui.MakeImageBox(self, "offlineshop/lightwork/searchshop/searchbgmin.png", 22- 2, 65+25*2 +25 + 16+9)
		self.itemAbsMaxBG = ui.MakeImageBox(self, "offlineshop/lightwork/searchshop/searchbgmin.png", 97- 2,  65+25*2+25 +16+9)

		self.itemMinAvgBG = ui.MakeImageBox(self, "offlineshop/lightwork/searchshop/searchbg.png", 26- 5,  65+25*3 + 19+25+9)
		self.itemGoldMinBG = ui.MakeImageBox(self, "offlineshop/lightwork/searchshop/searchbg.png", 26- 5,  65+25*4 + 19+25+9)
		self.itemGoldMaxBG = ui.MakeImageBox(self, "offlineshop/lightwork/searchshop/searchbg.png", 26- 5,  65+25*5 + 22+25+9)

		self.itemCountMin = ui.MakeEditline(self.itemCountMinBG, 4, 4, 111 - self.itemCountMinBG.GetWidth() - 2, 15, 6, self.itemCountMinBG.GetWidth())
		self.itemCountMax = ui.MakeEditline(self.itemCountMaxBG, 4, 4, 111 - self.itemCountMaxBG.GetWidth() - 2, 15, 6, self.itemCountMaxBG.GetWidth())
		
		self.itemMinAbs = ui.MakeEditline(self.itemAbsMinBG, 4, 4, 111 - self.itemAbsMinBG.GetWidth() - 2, 15, 3, self.itemAbsMinBG.GetWidth())
		self.itemMaxAbs = ui.MakeEditline(self.itemAbsMaxBG, 4, 4, 111 - self.itemAbsMaxBG.GetWidth() - 2, 15, 3, self.itemAbsMaxBG.GetWidth())

		self.itemMinLevel = ui.MakeEditline(self.itemLevelMinBG, 4, 4, 111 - self.itemLevelMinBG.GetWidth() - 2, 15, 3, self.itemLevelMinBG.GetWidth())
		self.itemMaxLevel = ui.MakeEditline(self.itemLevelMaxBG, 4, 4, 111 - self.itemLevelMaxBG.GetWidth() - 2, 15, 3, self.itemLevelMaxBG.GetWidth())

		self.itemMinAVG = ui.MakeEditline(self.itemMinAvgBG, 4, 4, 111 - self.itemMinAvgBG.GetWidth() - 2, 15, 3, self.itemMinAvgBG.GetWidth())
		self.itemMinGold = ui.MakeEditline(self.itemGoldMinBG, 4, 4, 111 - self.itemGoldMinBG.GetWidth() - 2, 15, 18, self.itemGoldMinBG.GetWidth())
		self.itemMaxGold = ui.MakeEditline(self.itemGoldMaxBG, 4, 4, 111 - self.itemGoldMaxBG.GetWidth() - 2, 15, 18, self.itemGoldMaxBG.GetWidth())

		self.gradeitemMinAbs = ui.TextLine()
		self.gradeitemMaxAbs = ui.TextLine()

		self.itemPerPage = ui.ComboBoxImage(self, "offlineshop/lightwork/searchshop/searchbg.png", 26- 5, 72)
		self.itemPerPage.ClearItem()
		self.itemPerPage.SetEvent(lambda flag, point=proxy(self): point.OnSelectPageCount(flag))
		self.itemPerPage.SetCurrentItem(localeInfo.OFFLINESHOP_RESULT_PER_PAGE)
		self.pageCounts = ([localeInfo.OFFLINESHOP_RESULT_PER_PAGE_ITEM, 0], [localeInfo.OFFLINESHOP_RESULT_PER_PAGE_ITEM2, 1], [localeInfo.OFFLINESHOP_RESULT_PER_PAGE_ITEM3, 2])
		for page in self.pageCounts:
			self.itemPerPage.InsertItem(page[1], page[0])
		self.itemPerPage.Show()


		self.itemAcceGrade = ui.ComboBoxImage(self, "offlineshop/lightwork/searchshop/searchbg.png", 26- 5,  65+25*8 + 25+25+9)
		self.itemAcceGrade.ClearItem()
		self.itemAcceGrade.SetEvent(lambda flag, point=proxy(self): point.onSelectAcce(flag))
		self.itemAcceGrade.SetCurrentItem(localeInfo.SHOP_SEARCH_ACCE_GRADE_FILTER_TITLE)
		self.acceGrade = ([localeInfo.SHOP_SEARCH_ACCE_GRADE_FILTER_TITLE, 0], [localeInfo.SHOP_SEARCH_ACCE_GRADE_FILTER_0, 1], [localeInfo.SHOP_SEARCH_ACCE_GRADE_FILTER_1, 2],[localeInfo.SHOP_SEARCH_ACCE_GRADE_FILTER_2, 3],[localeInfo.SHOP_SEARCH_ACCE_GRADE_FILTER_3, 4])
		for grade in self.acceGrade:
			self.itemAcceGrade.InsertItem(grade[1], grade[0])
		self.usingAcceGrade = False
		self.itemAcceGrade.Show()

		self.itemDSPurity = ui.ComboBoxImage(self, "offlineshop/lightwork/searchshop/searchbg.png", 26- 5,  65+25*7 + 25+25+9)
		self.itemDSPurity.ClearItem()
		self.itemDSPurity.SetEvent(lambda flag, point=proxy(self): point.onSelectDSPurity(flag))
		self.itemDSPurity.SetCurrentItem(localeInfo.SHOP_SEARCH_DS_CLARITY_FILTER_TITLE)
		self.dsPurities = ([localeInfo.SHOP_SEARCH_DS_CLARITY_FILTER_TITLE, 0], [localeInfo.SHOP_SEARCH_DS_CLARITY_FILTER_0, 1],[localeInfo.SHOP_SEARCH_DS_CLARITY_FILTER_1, 2],[localeInfo.SHOP_SEARCH_DS_CLARITY_FILTER_2, 3],[localeInfo.SHOP_SEARCH_DS_CLARITY_FILTER_3, 4],[localeInfo.SHOP_SEARCH_DS_CLARITY_FILTER_4, 5])
		for category in self.dsPurities:
			self.itemDSPurity.InsertItem(category[1], category[0])
		self.itemDSPurity.Show()

		self.itemDSGrade = ui.ComboBoxImage(self, "offlineshop/lightwork/searchshop/searchbg.png", 26- 5,  65+25*6 + 25+25+9)
		self.itemDSGrade.ClearItem()
		self.itemDSGrade.SetEvent(lambda flag, point=proxy(self): point.onSelectDSGrade(flag))
		self.itemDSGrade.SetCurrentItem(localeInfo.SHOP_SEARCH_DS_GRADE_FILTER_TITLE)
		self.itemDSGradeList = ([localeInfo.SHOP_SEARCH_DS_GRADE_FILTER_TITLE, 0], [uiscriptlocale.DRAGONSOUL_TAP_TITLE_1, 1],[uiscriptlocale.DRAGONSOUL_TAP_TITLE_2, 2],[uiscriptlocale.DRAGONSOUL_TAP_TITLE_3, 3], [uiscriptlocale.DRAGONSOUL_TAP_TITLE_4, 4], [uiscriptlocale.DRAGONSOUL_TAP_TITLE_5, 5], [uiscriptlocale.DRAGONSOUL_TAP_TITLE_6, 6])
		for category in self.itemDSGradeList:
			self.itemDSGrade.InsertItem(category[1], category[0])
		self.itemDSGrade.Show()


		self.wndFilterWarrior = self.CreateFilterRadioButton("", 20, 18, "warrior_no_select.png", "warrior_no_select.png", "warrior_select.png")
		self.wndFilterAssassin = self.CreateFilterRadioButton("", 20 + 37, 18, "assassin_no_select.png", "assassin_no_select.png", "assassin_select.png")
		self.wndFilterSura = self.CreateFilterRadioButton("", 20 + 37*2, 18, "sura_no_select.png", "sura_no_select.png", "sura_select.png")
		self.wndFilterShaman = self.CreateFilterRadioButton("", 20 + 37*3, 18, "shaman_no_select.png", "shaman_no_select.png", "shaman_select.png")

	def Open(self):
		self.SetTop()
		self.Show()

	def Close(self):
		self.Hide()

	def CreateFilterRadioButton(self, text, x, y, up, over, down):
		button = ui.ToggleButton()
		button.SetParent(self)
		button.SetPosition(x, y)
		button.SetUpVisual(PATH + "filter/" + up)
		button.SetOverVisual(PATH + "filter/" + over)
		button.SetDownVisual(PATH + "filter/" + down)
		button.SetToolTipText(text)
		button.SetToggleUpEvent(ui.__mem_func__(self.OnFilterButtonDown), button)
		button.SetToggleDownEvent(ui.__mem_func__(self.OnFilterButtonSetUp), button)
		button.Show()
		button.Down()
		return button

	def onSelectDSGrade(self, id):
		self.itemDSGrade.SetCurrentItem(self.itemDSGradeList[id][0])
		self.itemDSGrade.CloseListBox()

	def onSelectDSPurity(self, id):
		self.itemDSPurity.SetCurrentItem(self.dsPurities[id][0])
		self.itemDSPurity.CloseListBox()


	def OnSelectPageCount(self, id):
		self.itemPerPage.SetCurrentItem(self.pageCounts[id][0])
		self.itemPerPage.CloseListBox()

	def onSelectAcce(self, id):
		self.itemAcceGrade.SetCurrentItem(self.acceGrade[id][0])
		self.itemAcceGrade.CloseListBox()
		self.usingAcceGrade = True if id > 0 else False

		if id == 1:
			self.gradeitemMinAbs.SetText("0")
			self.gradeitemMaxAbs.SetText("4")
		elif id == 2:
			self.gradeitemMinAbs.SetText("5")
			self.gradeitemMaxAbs.SetText("9")
		elif id == 3:
			self.gradeitemMinAbs.SetText("10")
			self.gradeitemMaxAbs.SetText("10")
		elif id == 4:
			self.gradeitemMinAbs.SetText("11")
			self.gradeitemMaxAbs.SetText("25")
		else:
			self.usingAcceGrade is False

	def ResetComboxItems(self):
		self.itemCountMin.SetText("")
		self.itemCountMax.SetText("")
		self.itemMinAbs.SetText("")
		self.itemMaxAbs.SetText("")
		self.itemMinLevel.SetText("")
		self.itemMaxLevel.SetText("")
		self.itemMinAVG.SetText("")
		self.itemMinGold.SetText("")
		self.itemMaxGold.SetText("")
		self.itemDSPurity.SetCurrentItem(self.dsPurities[0][0])
		self.itemAcceGrade.SetCurrentItem(self.acceGrade[0][0])
		self.itemPerPage.SetCurrentItem(localeInfo.OFFLINESHOP_RESULT_PER_PAGE)
		self.itemDSGrade.SetCurrentItem(localeInfo.SHOP_SEARCH_DS_GRADE_FILTER_TITLE)

		self.gradeitemMinAbs.SetText("")
		self.gradeitemMaxAbs.SetText("")

	def OnFilterButtonDown(self, wnd):
		wnd.SetUp()

	def OnFilterButtonSetUp(self, wnd):
		wnd.Down()

	def OnUpdate(self):
		if len(self.itemCountMin.GetText()) > 0:
			self.itemCountMin.SetOverlayText("")
		else:
			self.itemCountMin.SetOverlayText(localeInfo.SHOP_SEARCH_FILTER_0_0)

		if len(self.itemCountMax.GetText()) > 0:
			self.itemCountMax.SetOverlayText("")
		else:
			self.itemCountMax.SetOverlayText(localeInfo.SHOP_SEARCH_FILTER_0_1)

		if len(self.itemMinLevel.GetText()) > 0:
			self.itemMinLevel.SetOverlayText("")
		else:
			self.itemMinLevel.SetOverlayText(localeInfo.SHOP_SEARCH_FILTER_1_0)

		if len(self.itemMaxLevel.GetText()) > 0:
			self.itemMaxLevel.SetOverlayText("")
		else:
			self.itemMaxLevel.SetOverlayText(localeInfo.SHOP_SEARCH_FILTER_1_1)

		if len(self.itemMinAbs.GetText()) > 0:
			self.itemMinAbs.SetOverlayText("")
		else:
			self.itemMinAbs.SetOverlayText(localeInfo.SHOP_SEARCH_FILTER_2_0)

		if len(self.itemMaxAbs.GetText()) > 0:
			self.itemMaxAbs.SetOverlayText("")
		else:
			self.itemMaxAbs.SetOverlayText(localeInfo.SHOP_SEARCH_FILTER_2_1)

		if len(self.itemMinAVG.GetText()) > 0:
			self.itemMinAVG.SetOverlayText("")
		else:
			self.itemMinAVG.SetOverlayText(localeInfo.SHOP_SEARCH_FILTER_3_0)

		if len(self.itemMinGold.GetText()) > 0:
			self.itemMinGold.SetOverlayText("")
		else:
			self.itemMinGold.SetOverlayText(localeInfo.SHOP_SEARCH_FILTER_4_0)

		if len(self.itemMaxGold.GetText()) > 0:
			self.itemMaxGold.SetOverlayText("")
		else:
			self.itemMaxGold.SetOverlayText(localeInfo.SHOP_SEARCH_FILTER_4_1)

	def getFilter(self, data):
		filter = {}
		filter["min_count"] = self.itemCountMin.GetText()
		filter["max_count"] = self.itemCountMax.GetText()
		filter["min_level"] = self.itemMinLevel.GetText()
		filter["max_level"] = self.itemMaxLevel.GetText()
		filter["min_abs"] = self.itemMinAbs.GetText()
		filter["max_abs"] = self.itemMaxAbs.GetText()
		filter["min_avg"] = self.itemMinAVG.GetText()
		filter["min_gold"] = self.itemMinGold.GetText()
		filter["max_gold"] = self.itemMaxGold.GetText()
		filter["ds_purity"] = self.itemDSPurity.GetCurrentItem()
		filter["acce_grade"] = self.itemAcceGrade.GetCurrentItem()
		filter["page_item_count"] = self.itemPerPage.GetCurrentItem()
		filter["warrior"] = self.wndFilterWarrior
		filter["assassin"] = self.wndFilterAssassin
		filter["sura"] = self.wndFilterSura
		filter["shaman"] = self.wndFilterShaman

		return filter[data]

	def AdjustPosition(self):

		(x, y) = self.GetGlobalPosition()
		self.SetPosition(x + self.GetWidth() - 165, y + 134)

	def OnPressEscapeKey(self):
		self.Close()
		return True

class ShopSearch(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.loaded = 0
		self.iCountEnd = 0
		self.currentPage = 1
		self.interface = None
		self.dlgBuyQuestion = None
		self.ListBox = None
		self.CategoryList = None
		self.searchTime = 0
		self.SearchFilterShopItemResult = []
		self.pageCount = 1
		self.searchAnimation = 0
		self.refreshButtons = False

		self.categoryButtons = []
		self.categoryButtonCount = 0

		self.LoadWindow()
		self.toolTipInfo = uitooltip.ToolTip()

		self.filterSettings = FilterWindow()
		self.filterSettings.SetParent(self)
		self.filterSettings.AdjustPosition()

		offlineshop.SetShopSearchBoard(self)

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def Destroy(self):
		self.ClearDictionary()
		if self.ListBox:
			self.ListBox.Destroy()
			self.ListBox.Clear()
			del self.ListBox
			
		if self.CategoryList:
			self.CategoryList.Clear()
			del self.CategoryList
		offlineshop.SetShopSearchBoard(None)
		self.toolTipInfo = None

	def Show(self, bFastSearch = False):
		self.LoadWindow()
		self.SetCenterPosition()
		self.Clear()
		ui.ScriptWindow.Show(self)

		if not bFastSearch == True:
			self.OnSearch()


	def Clear(self):
		self.sLastItemName = None
		self.sCategory = -1
		self.sSubCategory = -1
		self.iPage = 1
		self.iCountEnd = 0
		self.ItemList.Clear()
		self.bCantChangePage = False
		self.FloodPage = 0

	def LoadWindow(self):
		if self.loaded == 1:
			return

		self.loaded = 1		
		self.AddFlag("movable")
		
		self.Board = ui.MakeBoardWithTitleBar(self, "not_pick", localeInfo.SHOP_SEARCH_TITLE, ui.__mem_func__(self.CloseGame), 740, 537)

		self.BoardListBox = ui.ImageBox()
		self.BoardListBox.SetParent(self.Board)
		self.BoardListBox.SetPosition(15, 37)
		self.BoardListBox.LoadImage(PATH_ROOT3 + "subcatbg.png")
		self.BoardListBox.Show()

		self.BoardItemList = ui.ImageBox()
		self.BoardItemList.SetParent(self.Board)
		self.BoardItemList.SetPosition(214, 37)
		self.BoardItemList.LoadImage(PATH_ROOT3 + "item_board.png")
		self.BoardItemList.Show()


		self.SetSize(self.Board.GetWidth(), self.Board.GetHeight())
		
		self.btnBuySelectedItems = ui.MakeButton(self, 214, 500, False, PATH_ROOT, "btn_filter_norm.png", "btn_filter_hover.png", "btn_filter_down.png")
		self.btnBuySelectedItems.SetText(localeInfo.SHOP_SEARCH_BUY_SELECTED_ITEMS)

		self.btnFilterSettings = ui.MakeButton(self, 24, 108, False, PATH_ROOT, "btn_filter_norm.png", "btn_filter_hover.png", "btn_filter_down.png")
		self.btnFilterSettings.SetText(localeInfo.OFFLINESHOP_FILTER_TITLE)

		self.btnFilterSettingsClear = ui.MakeButton(self, 171, 108, False, PATH_ROOT, "resetfilter1.png", "resetfilter2.png", "resetfilter3.png")

		self.LineSearch = ui.MakeImageBox(self.Board, "offlineshop/lightwork/searchshop/search_bg.png", 24, 45)

		self.itemPriceContainer = ui.MakeImageBox(self.Board, "offlineshop/lightwork/shopeditor/totalyang.png", 15, 500)
		self.totalPriceContainer = ui.TextLine()
		self.totalPriceContainer.SetParent(self.itemPriceContainer)
		self.totalPriceContainer.SetPosition(29, 5)
		self.totalPriceContainer.Show()

		self.sItemName = ui.EditLine()
		self.sItemName.SetParent(self.LineSearch)
		self.sItemName.SetMax(20)
		self.sItemName.SetSize(111 - self.LineSearch.GetWidth() - 2, 15)
		self.sItemName.SetPosition(30, 4)
		self.sItemName.SetLimitWidth(self.LineSearch.GetWidth())
		self.sItemName.SetEscapeEvent(ui.__mem_func__(self.OnPressNameEscapeKey))
		self.sItemName.SetUpdateEvent(ui.__mem_func__(self.Search_RefreshTextHint))
		self.sItemName.SetTabEvent(ui.__mem_func__(self.Search_CompleteTextSearch))
		self.sItemName.SetReturnEvent(ui.__mem_func__(self.OnSearch))
		self.sItemName.SetOutline()
		self.sItemName.Show()

		self.searchEditHint = ui.TextLine()
		self.searchEditHint.SetParent(self.sItemName)
		self.searchEditHint.SetPackedFontColor(grp.GenerateColor(1.0, 1.0, 1.0, 0.5))
		self.searchEditHint.Show()

		self.searchTypeImage= ui.MakeImageBox(self.Board, PATH_ROOT + "weaponbutton.png", 30, 48)

		self.CheckBox = ui.ExpandedImageBox()
		self.CheckBox.SetParent(self.Board)
		self.CheckBox.SetPosition(25, 73)
		self.CheckBox.LoadImage(PATH_ROOT+ "playersearch.png")
		self.CheckBox.IsChecked = False
		self.CheckBox.OnMouseLeftButtonDown = ui.__mem_func__(self.OnCheckBox)
		self.CheckBox.Show()

		self.searchPlayerName = ui.TextLine()
		self.searchPlayerName.SetParent(self.CheckBox)
		self.searchPlayerName.SetPosition(50, 4)
		self.searchPlayerName.SetText(localeInfo.SHOP_SEARCH_SEARCH_BY_PLAYERNAME)
		self.searchPlayerName.Show()

		self.btnSearch = ui.MakeButton(self.Board, 176, 48, False, PATH_ROOT, "search_btn_norm.tga", "search_btn_hover.tga", "search_btn_norm.tga")
		self.btnSearch.SetEvent(ui.__mem_func__(self.OnSearch))


		self.btnBuySelectedItems.SetEvent(ui.__mem_func__(self.AskBuySelectedItems))
		self.btnFilterSettings.SetEvent(ui.__mem_func__(self.OpenFilterSettings))
		self.btnFilterSettingsClear.SetEvent(ui.__mem_func__(self.ClearFilterSettings))
	
		self.headerImage = ui.MakeExpandedImageBox(self.BoardItemList, PATH_ROOT+"header.png", 0, 0)
		self.headerItemName = ui.MakeTextLineNew(self.headerImage, 30, 3, localeInfo.OFFLINESHOP_TITLE_NAME)
		self.headerItemPrice = ui.MakeTextLineNew(self.headerImage, 255, 3, localeInfo.OFFLINESHOP_TITLE_PRICE)
		self.headerItemOthers = ui.MakeTextLineNew(self.headerImage, 405, 3, localeInfo.OFFLINESHOP_TITLE_OTHER)

		self.ItemList = ListBoxItem()
		self.ItemList.SetParent(self.BoardItemList)
		self.ItemList.SetSize(510, 430)
		self.ItemList.SetPosition(0, 21)
		self.ItemList.SetEventBuy(ui.__mem_func__(self.AskBuySelectedItem))
		self.ItemList.SetEventWhisper(ui.__mem_func__(self.OnWhisper))
		self.ItemList.SetEventPlayerName(ui.__mem_func__(self.OnPlayerNameSearch))
		self.ItemList.SetEventWikiSearch(ui.__mem_func__(self.OnWikiSearch))
		self.ItemList.Show()
	
		self.ScrollBar = ui.NewSlimScrollBar()
		self.ScrollBar.SetParent(self)
		self.ScrollBar.SetScrollBarSize(461)
		self.ScrollBar.SetPosition(726, 37)
		self.ItemList.SetScrollBar(self.ScrollBar)
		self.ScrollBar.Hide()

		self.nextButton = ui.MakeButton(self, 50 + 453 + 6 + 120 + 60, 293 + 210 - 2+5, False, "offlineshop/lightwork/searchshop/", "content_next_page.tga", "content_next_page_over.tga", "content_next_page_down.tga")
		self.lastButton = ui.MakeButton(self, 50 + 483 + 120 + 60, 293 + 210- 2+5, False, "offlineshop/lightwork/searchshop/", "content_last_page.tga", "content_last_page_over.tga", "content_last_page_down.tga")
		self.prevButton = ui.MakeButton(self, 50 + 260-20 + 120 + 60, 293 + 210- 2+5, False, "offlineshop/lightwork/searchshop/", "content_previous_page.tga", "content_previous_page_over.tga", "content_previous_page_down.tga")
		self.firstButton = ui.MakeButton(self, 50 + 230-20 + 6 + 120 + 60, 293 + 210- 2+5, False, "offlineshop/lightwork/searchshop/", "content_first_page.tga", "content_first_page_over.tga", "content_first_page_down.tga")

		self.pageButtons = []
		for i in range(6):
			self.pageButtons.append(ui.MakeButton(self, 500 + (i*25), 293 + 210 - 2, False, PATH_ROOT, "btn_page_norm.png", "btn_page_hover.png", "btn_page_down.png"))

		for index, item in enumerate(self.pageButtons):
			item.SetText(str((index + 1)))

		self.pageButtons[0].Show()
		self.pageButtons[1].Hide()
		self.pageButtons[2].Hide()
		self.pageButtons[3].Hide()
		self.pageButtons[4].Hide()
		self.pageButtons[5].Hide()
		self.pageButtons[0].Down()
		self.pageButtons[0].Disable()

		self.nextButton.SetEvent(ui.__mem_func__(self.NextPage))
		self.prevButton.SetEvent(ui.__mem_func__(self.PrevPage))
		self.firstButton.SetEvent(ui.__mem_func__(self.FirstPage), 1)
		self.lastButton.SetEvent(ui.__mem_func__(self.LastPage))



		self.searchNotFound = ui.TextLine()
		self.searchNotFound.SetParent(self)
		self.searchNotFound.SetPosition(390, 270)
		self.searchNotFound.SetText(localeInfo.SHOP_SEARCH_NOT_RESULT_FOUND)
		self.searchNotFound.Hide()

		self.searchAnimationBG = ui.MakeExpandedImageBox(self.BoardItemList, PATH_ROOT + "searchanimationbg.png", 0, 20, )
		self.searchAnimationBG.Hide()

		self.searchAnimation = ui.AniImageBox()
		self.searchAnimation.SetParent(self)
		self.searchAnimation.SetPosition(430, 250)
		self.searchAnimation.SetDelay(2)
		for animation in range(1, 30):
			self.searchAnimation.AppendImage("offlineshop/lightwork/searchshop/ani/{}.tga".format(animation))
		self.searchAnimation.Hide()

		self.categoryContainer = ui.Window()
		self.categoryContainer.SetParent(self)
		self.categoryContainer.SetSize(185, 377)
		self.categoryContainer.SetPosition(22, 140)
		self.categoryContainer.Show()

		self.categoryScrollbar = ui.NewSlimScrollBar()
		self.categoryScrollbar.SetParent(self)
		self.categoryScrollbar.SetScrollBarSize(340)
		self.categoryScrollbar.SetPosition(198, 142)
		self.categoryScrollbar.SetScrollEvent(self.OnCategoryScroll)
		self.categoryScrollbar.Show()

		for k, v in MULTI_CATEGORY_ITEMS.items():
			btn = self.AddCategoryButton(v["name"], k)

			if k in MULTI_CATEGORY_ITEMS and 'subtypes' in MULTI_CATEGORY_ITEMS[k]:
				for sub, name in MULTI_CATEGORY_ITEMS[k]['subtypes'].items():
					btn.AddSubButton(name, sub)

			if k in MULTI_CATEGORY_ITEMS and 'extra_subtypes' in MULTI_CATEGORY_ITEMS[k]:
				for sub, name in MULTI_CATEGORY_ITEMS[k]['extra_subtypes'].items():
					btn.AddSubButton(name, sub, True)

			if k in MULTI_CATEGORY_ITEMS and 'skinSubs' in MULTI_CATEGORY_ITEMS[k]:
				for sub, name in MULTI_CATEGORY_ITEMS[k]['skinSubs'].items():
					btn.AddSubButton(name, sub, True)
				for difType, otherElements in MULTI_CATEGORY_ITEMS[k]['differentType'].items():
					(itemSubType, title) = otherElements
					btn.AddSubButton(title, itemSubType, True, difType)


		for k, v in CATEGORY_ITEMS.items():
			btn = self.AddCategoryButton(v["name"], k)

		self.RefreshButtons()


	def SetCategory(self, category, subcategory, makeSearch=False):
		self.sCategory = category
		self.sSubCategory = subcategory

		for i in range(len(self.categoryButtons)):
			self.categoryButtons[i].UpdateSubButtons(category, subcategory)

		if makeSearch:
			self.OnSearch()

	def RefreshButtons(self):
		self.RefreshCategoryButtons(False)

	def AddCategoryButton(self, name, category_id):
		button = CategoryButton(self.categoryContainer, self, name, category_id)
		button.SetPosition(0, len(self.categoryButtons) * 30)

		self.categoryButtons.append(button)

		return button

	def RefreshCategoryButtons(self, isScroll):
		self.categoryButtonCount = 0
  
		for i in range(len(self.categoryButtons)):
			self.categoryButtonCount += 1
			if self.categoryButtons[i].active:
				self.categoryButtonCount += len(self.categoryButtons[i].subButtons)

		pos = int(self.categoryScrollbar.GetPos() * (self.categoryButtonCount - MAX_CATEGORY_ITEMS))

		top = 0
		count = 0
		for i in range(len(self.categoryButtons)):
			if count < pos or count >= (pos + MAX_CATEGORY_ITEMS):
				self.categoryButtons[i].SetPositionHelper(0, top - (pos - count) * 30)
				self.categoryButtons[i].Hide()
			else:
				self.categoryButtons[i].SetPositionHelper(0, top)
				self.categoryButtons[i].Show()
				top += 30

			if self.categoryButtons[i].active:
				for sub in range(len(self.categoryButtons[i].subButtons)):
					count += 1

					if count < pos or count >= (pos + MAX_CATEGORY_ITEMS):
						self.categoryButtons[i].subButtons[sub][0].Hide()
					else:
						self.categoryButtons[i].subButtons[sub][0].Show()

						top += 32
			count += 1

		if not isScroll:
			self.categoryScrollbar.SetMiddleBarSize(float(MAX_CATEGORY_ITEMS) / float(self.categoryButtonCount))

		if self.categoryButtonCount > 13:
			self.categoryScrollbar.Show()
		else:
			self.categoryScrollbar.Hide()

	def OnCategoryScroll(self):
		self.RefreshCategoryButtons(True)

	def OverInButton(self):
		pass

	def OverOutButton(self):
		if self.toolTipInfo:
			self.toolTipInfo.Hide()

	def OnCheckBox(self):
		if self.CheckBox.IsChecked:
			self.CheckBox.IsChecked = False
			self.CheckBox.LoadImage(PATH_ROOT+ "playersearch.png")
			self.searchTypeImage.LoadImage(PATH_ROOT + "weaponbutton.png")
		else:
			self.CheckBox.IsChecked = True
			self.CheckBox.LoadImage(PATH_ROOT+ "playersearch_2.png")
			self.searchTypeImage.LoadImage(PATH_ROOT + "playerbutton.png")

		self.Search_RefreshTextHint()


		self.Search_RefreshTextHint()

	def OnUpdate(self):
		global TOTAL_ITEM_PRICE
		if len(self.sItemName.GetText()) > 0:
			self.sItemName.SetOverlayText("")
		else:
			if self.CheckBox.IsChecked:
				self.sItemName.SetOverlayText(localeInfo.SHOP_SEARCH_SEARCH_BY_PLAYERNAME2)
			else:
				self.sItemName.SetOverlayText(localeInfo.SHOP_SEARCH_ENTER_ITEMNAME)

		self.Search_RefreshTextHint()

		self.totalPriceContainer.SetText(localeInfo.OFFLINESHOP_TOTAL_YANG_AMOUNT.format(localeInfo.NumberToDecimal(TOTAL_ITEM_PRICE)))

		if app.GetTime() < self.searchTime:
			self.SetPhase("Loading")
		else:
			self.SetPhase("Completed")

	def SetItemToolTip(self, tooltip):
		self.tooltipItem = tooltip

	def BindInterface(self, interface):
		self.interface = interface

	def OnPressNameEscapeKey(self):
		if not self.sItemName:
			return
		
		if not self.sItemName.IsShowCursor() or self.sItemName.GetText() == "":
			self.OnPressEscapeKey()
		else:
			self.sItemName.SetText("")
			self.searchEditHint.SetText("")	

	def Search_CompleteTextSearch(self):
		if self.searchEditHint.GetText():
			oldText = self.sItemName.GetText()
			self.sItemName.SetText(oldText + self.searchEditHint.GetText()[len(oldText)+1:])
			self.sItemName.SetEndPosition()
			self.Search_RefreshTextHint()

	def Search_RefreshTextHint(self):
		EDIT_TEXT_BASE_COLOR = grp.GenerateColor(0.8549, 0.8549, 0.8549, 1.0)
		EDIT_TEXT_NOT_FOUND_COLOR = grp.GenerateColor(1.0, 0.2, 0.2, 1.0)
		
		self.searchEditHint.SetText("")
		self.sItemName.SetPackedFontColor(EDIT_TEXT_BASE_COLOR)
		
		search_text = self.sItemName.GetText()

		def check_exact_search(real_name, check_name):
			pass
			
			

		if len(search_text) and self.CheckBox.IsChecked == False:
			try:
				(hintName, vnum) = item.GetItemDataByNamePart(search_text)
			except AttributeError:
				(hintName, vnum) = ("", -1)
			
			if vnum == -1:
				self.searchEditHint.SetText("")
				self.sItemName.SetPackedFontColor(EDIT_TEXT_NOT_FOUND_COLOR)
			else:
				self.searchEditHint.SetText(search_text + " " + hintName[len(search_text):])

	def OnMouseWheel(self, nLen):
		scroll = self.ScrollBar
		if self.BoardListBox.IsInPosition():
			scroll = self.categoryScrollbar
		
		if nLen > 0:
			scroll.OnUp()
		else:
			scroll.OnDown()
			
		return True

	def OnWhisper(self, name):
		player.OpenPrivateMessage(name)

	def OnPlayerNameSearch(self, name):
		self.sItemName.SetText(name)
		if not self.CheckBox.IsChecked:
			self.CheckBox.IsChecked = True
			self.CheckBox.LoadImage(PATH_ROOT+ "playersearch_2.png")
			self.searchTypeImage.LoadImage(PATH_ROOT + "playerbutton.png")
		self.OnSearch()

	def OnWikiSearch(self, vnum):
		if self.interface.wndWiki:
			self.interface.wndWiki.searchItemWithName(vnum)

	def SetInterface(self, interface):
		self.interface = interface

	def SearchFilter_BuyFromSearch(self, ownerid, itemid):
		self.ItemList.RemoveItemBought(ownerid, itemid)
	
		for item in self.SearchFilterShopItemResult:
			if item['id'] == itemid and item['owner'] == ownerid:
				self.SearchFilterShopItemResult.remove(item)
				break
				
		global SELECTED_ITEMS_BUY, TOTAL_ITEM_PRICE
		SELECTED_ITEMS_BUY = {}
		TOTAL_ITEM_PRICE = 0

	def SetPopUpDialog(self, msg):
		self.popupMessage = uicommon.PopupDialog()
		self.popupMessage.SetWidth(250)
		self.popupMessage.SetText(msg)
		self.popupMessage.Open()
		self.popupMessage.SetAutoClose(True)

	def AskBuySelectedItems(self):


		global SELECTED_ITEMS_BUY
		count = len(SELECTED_ITEMS_BUY)

		self.BuyQuestionCancel()
		if count == 0:
			self.SetPopUpDialog(localeInfo.SHOP_SEARCH_ADD_ITEMS_TO_THE_CART_FIRST)
			return
		dlgBuyQuestion = uicommon.QuestionDialog()
		dlgBuyQuestion.SetText(localeInfo.SHOP_SEARCH_BUY_SELECTED_ITEMS_CONFIRM % (count))
		dlgBuyQuestion.SetAcceptEvent(ui.__mem_func__(self.BuySelectedItems))
		dlgBuyQuestion.SetCancelEvent(ui.__mem_func__(self.BuyQuestionCancel))
		dlgBuyQuestion.Open()
		self.dlgBuyQuestion = dlgBuyQuestion

	def OpenFilterSettings(self):
		if self.filterSettings.IsShow():
			self.filterSettings.Close()
		else:
			self.filterSettings.Open()

	def ClearFilterSettings(self):
		self.filterSettings.ResetComboxItems()
		self.sItemName.SetText("")
		self.sItemName.SetOverlayText("")
		self.Search_RefreshTextHint()
		if self.CheckBox.IsChecked:
			self.CheckBox.IsChecked = False
			self.CheckBox.LoadImage(PATH_ROOT+ "playersearch.png")
		self.SetCategory(0, 255)


	def BuySelectedItems(self):
		self.ItemList.BuySelectedItems()

		if self.dlgBuyQuestion:
			self.dlgBuyQuestion.Close()
			self.dlgBuyQuestion = None

	
	def AskBuySelectedItem(self, Pid, SlotPos, ItemName):
	
		global SELECTED_ITEMS_BUY
		if len(SELECTED_ITEMS_BUY) > 0:
			self.SetPopUpDialog(localeInfo.SHOP_SEARCH_CLEAR_CART_FIRST)
			return
	
		self.BuyQuestionCancel()
		self.sellOwner = Pid
		self.sellitemID = SlotPos
	
		self.CreateQuestionDialog(localeInfo.SHOP_SEARCH_BUY_CONFIRM % (ItemName), self.BuySelectedItem, self.BuyQuestionCancel)

	def CreateQuestionDialog(self, text, acceptEvent, cancelEvent):
		self.BuyQuestionCancel()
		dlgBuyQuestion = uicommon.QuestionDialog()
		dlgBuyQuestion.SetText(text)
		dlgBuyQuestion.SetAcceptEvent(ui.__mem_func__(acceptEvent))
		dlgBuyQuestion.SetCancelEvent(ui.__mem_func__(cancelEvent))
		dlgBuyQuestion.Open()
		self.dlgBuyQuestion = dlgBuyQuestion
	
	def BuyQuestionCancel(self):
		if self.dlgBuyQuestion:
			self.dlgBuyQuestion.Close()
			self.dlgBuyQuestion = None		

	def BuySelectedItem(self):
		offlineshop.SendBuyItemFromSearch(self.sellOwner, self.sellitemID)
		
		if self.dlgBuyQuestion:
			self.dlgBuyQuestion.Close()
			self.dlgBuyQuestion = None

	def GetSearchFilterSettings(self, type = 0, subtype = 255):
		name = self.sItemName.GetText() if (self.sItemName.GetText() and len(self.sItemName.GetText())) else ""

		raceFlagDct = {
			0	: item.ITEM_ANTIFLAG_WARRIOR,
			1	: item.ITEM_ANTIFLAG_ASSASSIN,
			2	: item.ITEM_ANTIFLAG_SURA,
			3 	: item.ITEM_ANTIFLAG_SHAMAN,
		}
		
		raceflagbtn = [
			self.filterSettings.wndFilterWarrior,
			self.filterSettings.wndFilterAssassin,
			self.filterSettings.wndFilterSura,
			self.filterSettings.wndFilterShaman,
		]
		
		raceflag	= 0
		
		for k,v in raceFlagDct.items():
			if not raceflagbtn[k].IsDown():
				raceflag |= v

		type		= type
		subtype		= subtype
		bIsPlayerName = self.CheckBox.IsChecked

		levelmin	= 0
		levelmax	= 0
		yangmin		= 0
		yangmax		= 0
		countmin	= 0
		countmax	= 0
		absmin 		= 0
		absmax 		= 0
		avgmin 		= 0
		alchemyGrade 		= 0
		alchemyPurity 		= 0
		sashLevel 		= 0

		minLvl	= self.filterSettings.itemMinLevel.GetText()
		maxLvl	= self.filterSettings.itemMaxLevel.GetText()
		minYang	= self.filterSettings.itemMinGold.GetText()
		maxYang	= self.filterSettings.itemMaxGold.GetText()

		minCount = self.filterSettings.itemCountMin.GetText()
		maxCount = self.filterSettings.itemCountMax.GetText()

		if self.filterSettings.usingAcceGrade:
			minAbs = self.filterSettings.gradeitemMinAbs.GetText()
			maxAbs = self.filterSettings.gradeitemMaxAbs.GetText()

			if len(self.filterSettings.itemMinAbs.GetText()) or len(self.filterSettings.itemMaxAbs.GetText()):
				minAbs = self.filterSettings.itemMinAbs.GetText()

		else:
			minAbs = self.filterSettings.itemMinAbs.GetText()
			maxAbs = self.filterSettings.itemMaxAbs.GetText()

		minAvg = self.filterSettings.itemMinAVG.GetText()

		if minLvl and minLvl.isdigit():
			levelmin = int(minLvl)
		if maxLvl and maxLvl.isdigit():
			levelmax = int(maxLvl)
		if minYang and minYang.isdigit():
			yangmin = int(minYang)
		if maxYang and maxYang.isdigit():
			yangmax = int(maxYang)
		if minCount and minCount.isdigit():
			countmin = int(minCount)
		if maxCount and maxCount.isdigit():
			countmax = int(maxCount)
		if minAbs and minAbs.isdigit():
			absmin = int(minAbs)
		if maxAbs and maxAbs.isdigit():
			absmax = int(maxAbs)
		if minAvg and minAvg.isdigit():
			avgmin = int(minAvg)

		if type == -1:
			type = 0
			subtype = 255

		if subtype == -1:
			subtype = 255

		dsGradeObj = self.filterSettings.itemDSGrade
		alchemyGrade = int(dsGradeObj.GetItemIndex(dsGradeObj.GetCurrentItem()))

		dsPurityObj = self.filterSettings.itemDSPurity
		alchemyPurity = int(dsPurityObj.GetItemIndex(dsPurityObj.GetCurrentItem()))

		sashGradeObj = self.filterSettings.itemAcceGrade
		sashLevel = int(sashGradeObj.GetItemIndex(sashGradeObj.GetCurrentItem()))

		return (type, subtype, name, (yangmin, yangmax), (levelmin, levelmax), raceflag, bIsPlayerName, (countmin, countmax), (absmin, absmax), avgmin, alchemyGrade, alchemyPurity, sashLevel)
		
	def OnSearchByValue(self, Type, SubType):

		self.sCategory = Type
		self.sSubCategory = SubType
		self.ItemList.Clear()

		self.searchTime = app.GetTime() + 0.5
		self.refreshButtons = True

		self.SearchFilterLastUsedSetting = self.GetSearchFilterSettings(Type, SubType)
		
		offlineshop.SendFilterRequest(*self.SearchFilterLastUsedSetting)

		self.currentPaginationPage = 1

		global SELECTED_ITEMS_BUY
		SELECTED_ITEMS_BUY = {}

	def OnClearSearchData(self, withSearch = False):
		self.sItemName.SetText("")
		self.sItemName.SetOverlayText("")
		self.Search_RefreshTextHint()

		self.clearCheckBox()
		self.filterSettings.ResetComboxItems()
		if withSearch:
			self.CategoryList.SelectCategory()
			self.OnSearch()

	def clearCheckBox(self):
		if self.CheckBox.IsChecked:
			self.CheckBox.IsChecked = False
			self.Checkbox.LoadImage(PATH_ROOT+ "playersearch.png")

	def OnSearch(self):

		self.ItemList.Clear()

		self.searchAnimation.Show()
		self.searchAnimationBG.Show()
		self.searchTime = app.GetTime() + 0.5
		self.refreshButtons = True

		self.SearchFilterLastUsedSetting = self.GetSearchFilterSettings(self.sCategory, self.sSubCategory)
		offlineshop.SendFilterRequest(*self.SearchFilterLastUsedSetting)
		self.currentPaginationPage = 1
		global SELECTED_ITEMS_BUY, TOTAL_ITEM_PRICE
		SELECTED_ITEMS_BUY = {}
		TOTAL_ITEM_PRICE = 0

	def RefreshPaginationButtons(self):
		self.currentPaginationPage = int(math.ceil(float(self.currentPage) / float(len(self.pageButtons)) ))
		self.shownPages = min(self.pageCount - (len(self.pageButtons) * (self.currentPaginationPage - 1)), len(self.pageButtons))
		for x in range(len(self.pageButtons)):
			currentPage = (x + ((self.currentPaginationPage-1) * len(self.pageButtons)) + 1)
			self.pageButtons[x].SetUp()
			self.pageButtons[x].SetText("%s" % constInfo.NumberToStrRomanNumerals(currentPage))
			self.pageButtons[x].SetEvent(ui.__mem_func__(self.GotoPage), currentPage)
		
		map(ui.Button.Hide, self.pageButtons)
		map(ui.Button.Enable, self.pageButtons)
		
		for x in range(self.shownPages):
			self.pageButtons[x].Show()
			self.pageButtons[x].Enable()

		self.pageButtons[(self.currentPage - ((self.currentPaginationPage - 1) * len(self.pageButtons))) - 1].Down()
		self.pageButtons[(self.currentPage - ((self.currentPaginationPage - 1) * len(self.pageButtons))) - 1].Disable()

		if (self.pageCount <= 1):
			self.nextButton.Hide()
			self.lastButton.Hide()
			self.prevButton.Hide()
			self.firstButton.Hide()
		else:
			self.nextButton.Show()
			self.lastButton.Show()
			self.prevButton.Show()
			self.firstButton.Show()

		pagePos = [519, 559, 579, 599, 619, 639]

		if self.shownPages > 0 and self.shownPages < 6:
			self.nextButton.SetPosition(pagePos[self.shownPages] if self.shownPages < 6 else 689, 506)
			self.lastButton.SetPosition(pagePos[self.shownPages] + 20 if self.shownPages < 6 else 689 - 20, 506)
		else:
			self.nextButton.SetPosition(689-20, 506)
			self.lastButton.SetPosition(713-20, 506)

	def GotoPage(self, page):
		self.currentPage = page
		self.RefreshList()

	def FirstPage(self):
		self.SetPage(1)
		
	def LastPage(self):
		self.SetPage(self.pageCount)

	def NextPage(self):
		if self.currentPage < self.pageCount:
			self.SetPage(self.currentPage + 1)
			
	def PrevPage(self):
		if self.currentPage > 1:
			self.SetPage(self.currentPage - 1)

	def SetPage(self, page):
		self.searchAnimation.Show()
		self.searchAnimationBG.Show()
		self.currentPage = page
		self.RefreshList()

	def ShopFilterResult( self , size):
		self.SearchFilterShopItemResult = []
	
	def ShopFilterResultItem_Alloc(self):
		self.SearchFilterShopItemResult.append({})

	def ShopFilterResultItem_SetValue( self,  key, index, *args):
		if key in ( "id", "vnum", "count", "price", "owner", "owner_name", 'trans'):
			self.SearchFilterShopItemResult[index][key] = args[0]
		
		elif key == "attr":
			if not key in self.SearchFilterShopItemResult[index]:
				self.SearchFilterShopItemResult[index][key] = {}
			
			attr_index = args[0]
			attr_type  = args[1]
			attr_value = args[2]
			
			self.SearchFilterShopItemResult[index][key][attr_index] = {}
			self.SearchFilterShopItemResult[index][key][attr_index]["type"]  = attr_type
			self.SearchFilterShopItemResult[index][key][attr_index]["value"] = attr_value
		
		elif key == "socket":
			if not key in self.SearchFilterShopItemResult[index]:
				self.SearchFilterShopItemResult[index][key] = {}
			
			socket_index = args[0]
			socket_val	 = args[1]
			
			self.SearchFilterShopItemResult[index][key][socket_index] = socket_val

	def ShopFilterResult_Show(self):

		try:
			try:
				self.maxItemPerPage = int(self.filterSettings.itemPerPage.GetCurrentItem()[:3])
			except Exception:
				self.maxItemPerPage = int(self.filterSettings.itemPerPage.GetCurrentItem()[:2])
		except Exception:
			self.maxItemPerPage = 25

		self.itemCount = len(self.SearchFilterShopItemResult)
		self.pageCount = int(math.ceil(float(self.itemCount) / float(self.maxItemPerPage)))
		self.currentPaginationPage = 1
		self.paginationPageCount = int(math.ceil(float(self.pageCount) / float(len(self.pageButtons)) ))
		self.RefreshPaginationButtons()
		self.currentPage = 1
		self.RefreshList()

	def RefreshList(self):
		self.ItemList.Clear()
		self.RefreshPaginationButtons()

		random.shuffle(self.SearchFilterShopItemResult)
		size = len(self.SearchFilterShopItemResult)
		start = (self.currentPage - 1) * self.maxItemPerPage
		end = ((self.currentPage - 1) * self.maxItemPerPage) + self.maxItemPerPage
		for x in range(size):
			if start + x >= end:
				break

			if start + x < len(self.SearchFilterShopItemResult):
				self.ItemList.AppendItem(start + x, self.SearchFilterShopItemResult[start + x])

		if len(self.SearchFilterShopItemResult):
			self.ScrollBar.Show()
		else:
			self.ScrollBar.Hide()

	def Close(self, IsFromGame = False):
		self.ItemList.Clear()
		
		if self.dlgBuyQuestion:
			self.dlgBuyQuestion.Close()
			self.dlgBuyQuestion = None
		
		self.Hide()
		app.SetCursor(app.NORMAL)
		if self.toolTipInfo:
			self.toolTipInfo.Hide()
		
		if self.filterSettings:
			self.filterSettings.Hide()
			self.filterSettings.ResetComboxItems()

	def CloseGame(self):
		self.Close(True)
	
	def OnPressEscapeKey(self):
		self.Close(True)
		return True	

	def SetPhase(self, phase):
		if self.searchNotFound.IsShow(): self.searchNotFound.Hide()
		if self.searchAnimation.IsShow(): self.searchAnimation.Hide()
		if self.searchAnimationBG.IsShow(): self.searchAnimationBG.Hide()

		if phase == "Loading":
			self.searchAnimation.Show()
			self.searchAnimationBG.Show()
			self.ItemList.Hide()
			self.ScrollBar.Hide()
			self.nextButton.Hide()
			self.lastButton.Hide()
			self.prevButton.Hide()
			self.firstButton.Hide()
			self.pageButtons[0].Hide()
			self.pageButtons[1].Hide()
			self.pageButtons[2].Hide()
			self.pageButtons[3].Hide()
			self.pageButtons[4].Hide()
			self.pageButtons[5].Hide()
		else:
			if self.ItemList.GetItemCount() == 0:
				self.NoItemsWereFound()
			else:
				self.searchAnimation.Hide()
				self.searchAnimationBG.Hide()
				self.ItemList.Show()
				self.ScrollBar.Show()

				if (self.pageCount > 1):
					self.nextButton.Show()
					self.lastButton.Show()
					self.prevButton.Show()
					self.firstButton.Show()

				if self.refreshButtons:
					self.RefreshPaginationButtons()
					self.refreshButtons = False

	def NoItemsWereFound(self):
		if self.searchAnimation.IsShow():
			self.searchAnimation.Hide()
			self.searchAnimationBG.Hide()

		if app.GetTime() > self.searchTime:
			self.searchNotFound.Show()
		self.ScrollBar.Hide()

class CategoryButton(ui.Button):
	def __init__(self, parent, parentClass, name, category_id):
		ui.Button.__init__(self)

		self.active = False
		self.categoryId = category_id

		self.subButtons = []

		self.parent = parentClass
		self.parentNode = parent
		self.SetParent(parent)
		self.SetUpVisual( PATH_ROOT +"category_bg.png")
		self.SetOverVisual(PATH_ROOT +"category_bg_hover.png")
		self.SetDownVisual(PATH_ROOT +"category_bg_down.png")
		self.SetDisableVisual(PATH_ROOT +"category_bg.png")
		self.SAFE_SetEvent(self.ClickCategoryEvent)

		icons = [1, 2, 5, 16, 26, 27, 28, 38, 11]
		iconspng = [0, 9, 11, 22, 33, 240]

		if (category_id in icons):
			self.icon = ui.ImageBox()
			self.icon.SetParent(self)
			self.icon.SetPosition(185//2-85, 5)
			self.icon.LoadImage("d:/ymir work/offlineshop/shopsearchp2p/icon/%d.dds" % category_id)
			self.icon.Show()

		if (category_id in iconspng):
			self.icon = ui.ImageBox()
			self.icon.SetParent(self)
			self.icon.SetPosition(185//2-85, 5)
			self.icon.LoadImage("d:/ymir work/offlineshop/shopsearchp2p/icon/%d.png" % category_id)
			self.icon.Show()

		self.valueName = ui.TextLine()
		self.valueName.SetParent(self)
		self.valueName.SetPosition(185//2-60, 5)
		self.valueName.SetText(name)
		self.valueName.Show()

		self.Show()

	def SetPositionHelper(self, x, y):
		self.SetPosition(x, y)

		for i in range(len(self.subButtons)):
			y += 30
			self.subButtons[i][0].SetPosition(2, 5+y)

	def UpdateSubButtons(self, category, subcategory):
		for i in range(len(self.subButtons)):
			if self.subButtons[i][1] == subcategory and self.categoryId == category:
				self.subButtons[i][0].Disable()
				self.subButtons[i][0].Down()
			else:
				self.subButtons[i][0].Enable()
				self.subButtons[i][0].SetUp()

	def ClickCategoryEvent(self):



		if self.active:
			for i in range(len(self.subButtons)):
				self.subButtons[i][0].Hide()

			self.active = False
		else:
			self.active = True

			for i in range(len(self.subButtons)):
				self.subButtons[i][0].Show()
			

		if not len(self.subButtons):
			self.parent.SetCategory(self.categoryId, 255)
			self.parent.OnSearch()

		self.parent.RefreshButtons()

	def __del__(self):
		ui.Button.__del__(self)

	def AddSubButton(self, name, subcategory, isMainCat=False, differentCategory=0):
		button = ui.Button()
		button.SetParent(self.parentNode)
		button.SetUpVisual(PATH_ROOT + "button_01.png")
		button.SetOverVisual(PATH_ROOT + "button_02.png")
		button.SetDownVisual(PATH_ROOT + "button_03.png")
		button.SetDisableVisual(PATH_ROOT + "button_01.png")
		button.SetText(name)
		if isMainCat:
			button.SAFE_SetEvent(self.parent.SetCategory, subcategory, 255, True)
		else:
			button.SAFE_SetEvent(self.parent.SetCategory, differentCategory if differentCategory != 0 else self.categoryId, subcategory, True)
		button.Hide()

		self.subButtons.append([button, subcategory])

		return button