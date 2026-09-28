#-*- coding: iso-8859-1 -*-
import app
import net
import player
import item
import nonplayer
import ui
import uiToolTip
import localeInfo
import uiCommon
import constInfo
import uiChestDropInfo
import emoji
ENABLE_REFINE_ITEM_DESCRIPTION = 1

REFINE_SOURCE_TYPE_MONSTER = 0
REFINE_SOURCE_TYPE_ITEM = 1

if ENABLE_REFINE_ITEM_DESCRIPTION:
	TOOLTIP_DATA = []

class RefineDialog(ui.ScriptWindow):

	makeSocketSuccessPercentage = ( 100, 33, 20, 15, 10, 5, 0 )
	upgradeStoneSuccessPercentage = ( 30, 29, 28, 27, 26, 25, 24, 23, 22 )
	upgradeArmorSuccessPercentage = ( 99, 66, 33, 33, 33, 33, 33, 33, 33 )
	upgradeAccessorySuccessPercentage = ( 99, 88, 77, 66, 33, 33, 33, 33, 33 )
	upgradeSuccessPercentage = ( 99, 66, 33, 33, 33, 33, 33, 33, 33 )

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.__LoadScript()

		self.scrollItemPos = 0
		self.targetItemPos = 0

	def __LoadScript(self):

		self.__LoadQuestionDialog()

		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "uiscript/refinedialog.py")

		except:
			import exception
			exception.Abort("RefineDialog.__LoadScript.LoadObject")

		try:
			self.board = self.GetChild("Board")
			self.titleBar = self.GetChild("TitleBar")
			self.successPercentage = self.GetChild("SuccessPercentage")
			self.GetChild("AcceptButton").SetEvent(self.OpenQuestionDialog)
			self.GetChild("CancelButton").SetEvent(self.Close)
		except:
			import exception
			exception.Abort("RefineDialog.__LoadScript.BindObject")

		if constInfo.ENABLE_REFINE_PCT:
			self.successPercentage.Show()
		else:
			self.successPercentage.Hide()

		toolTip = uiToolTip.ItemToolTip()
		toolTip.SetParent(self)
		toolTip.SetPosition(15, 38)
		toolTip.SetFollow(False)
		toolTip.SetModelShow(False)
		toolTip.Show()
		self.toolTip = toolTip

		self.titleBar.SetCloseEvent(ui.__mem_func__(self.Close))

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __LoadQuestionDialog(self):
		self.dlgQuestion = ui.ScriptWindow()

		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self.dlgQuestion, "uiscript/questiondialog2.py")
		except:
			import exception
			exception.Abort("RefineDialog.__LoadQuestionDialog.LoadScript")

		try:
			GetObject=self.dlgQuestion.GetChild
			GetObject("message1").SetText(localeInfo.REFINE_DESTROY_WARNING)
			GetObject("message2").SetText(localeInfo.REFINE_WARNING2)
			GetObject("accept").SetEvent(ui.__mem_func__(self.Accept))
			GetObject("cancel").SetEvent(ui.__mem_func__(self.dlgQuestion.Hide))
		except:
			import exception
			exception.Abort("SelectCharacterWindow.__LoadQuestionDialog.BindObject")

	def Destroy(self):
		self.ClearDictionary()
		self.board = 0
		self.successPercentage = 0
		self.titleBar = 0
		self.toolTip = 0
		self.dlgQuestion = 0

	def GetRefineSuccessPercentage(self, scrollSlotIndex, itemSlotIndex):

		if -1 != scrollSlotIndex:
			if player.IsRefineGradeScroll(scrollSlotIndex):
				curGrade = player.GetItemGrade(itemSlotIndex)
				itemIndex = player.GetItemIndex(itemSlotIndex)

				item.SelectItem(itemIndex)
				itemType = item.GetItemType()
				itemSubType = item.GetItemSubType()

				if item.METIN == itemType:

					if curGrade >= len(self.upgradeStoneSuccessPercentage):
						return 0
					return self.upgradeStoneSuccessPercentage[curGrade]

				elif item.ARMOR == itemType:

					if item.ARMOR_BODY == itemSubType:
						if curGrade >= len(self.upgradeArmorSuccessPercentage):
							return 0
						return self.upgradeArmorSuccessPercentage[curGrade]
					else:
						if curGrade >= len(self.upgradeAccessorySuccessPercentage):
							return 0
						return self.upgradeAccessorySuccessPercentage[curGrade]

				else:

					if curGrade >= len(self.upgradeSuccessPercentage):
						return 0
					return self.upgradeSuccessPercentage[curGrade]

		for i in range(player.METIN_SOCKET_MAX_NUM+1):
			if 0 == player.GetItemMetinSocket(itemSlotIndex, i):
				break

		return self.makeSocketSuccessPercentage[i]

	def Open(self, scrollItemPos, targetItemPos):
		self.scrollItemPos = scrollItemPos
		self.targetItemPos = targetItemPos

		percentage = self.GetRefineSuccessPercentage(scrollItemPos, targetItemPos)
		if 0 == percentage:
			return
		self.successPercentage.SetText(localeInfo.REFINE_SUCCESS_PROBALITY % (percentage))
		


		itemIndex = player.GetItemIndex(targetItemPos)
		self.toolTip.ClearToolTip()
		metinSlot = []
		for i in range(player.METIN_SOCKET_MAX_NUM):
			metinSlot.append(player.GetItemMetinSocket(targetItemPos, i))

		if metinSlot[0] < 100:
			metinSlot = []
			for i in range(player.METIN_SOCKET_MAX_NUM):
				metinSlot.append(0)
		
		itemIndex = player.GetItemIndex(targetItemPos)
		item.SelectItem(itemIndex)
		import chat
		chat.AppendChat(chat.CHAT_TYPE_INFO, str(itemIndex))
		self.toolTip.AddItemData(itemIndex, metinSlot)

		self.UpdateDialog()
		self.SetTop()
		self.Show()

	def UpdateDialog(self):
		newWidth = self.toolTip.GetWidth() + 30
		newHeight = self.toolTip.GetHeight() + 98
		self.board.SetSize(newWidth, newHeight)
		self.titleBar.SetWidth(newWidth-15)
		self.SetSize(newWidth, newHeight)

		(x, y) = self.GetLocalPosition()
		self.SetPosition(x, y)

	def OpenQuestionDialog(self):
		percentage = self.GetRefineSuccessPercentage(-1, self.targetItemPos)
		if 100 == percentage:
			self.Accept()
			return

		self.dlgQuestion.SetTop()
		self.dlgQuestion.Show()

	def Accept(self):
		net.SendItemUseToItemPacket(self.scrollItemPos, self.targetItemPos)
		self.Close()

	def Close(self):
		self.dlgQuestion.Hide()
		self.Hide()

	def OnPressEscapeKey(self):
		self.Close()
		return True

class RefineDialogNew(ui.ScriptWindow):

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.__Initialize()
		self.isLoaded = False
		if app.WJ_ENABLE_TRADABLE_ICON:
			self.wndInventory = None
		self.wndChestDropInfo = uiChestDropInfo.ChestDropInfoWindow()

	def __Initialize(self):
		self.dlgQuestion = None
		self.children = []
		self.vnum = 0
		self.targetItemPos = 0
		self.dialogHeight = 0
		self.cost = 0
		self.cost2 = 0
		self.cost3 = 0
		self.percentage = 0
		self.type = 0
		self.materialSlotVnums = []
		self.materialSources = {}
		if app.WJ_ENABLE_TRADABLE_ICON:
			self.lockedItem = (-1,-1)

	def __LoadScript(self):

		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "uiscript/refinedialog.py")

		except:
			import exception
			exception.Abort("RefineDialog.__LoadScript.LoadObject")

		try:
			self.board = self.GetChild("Board")
			self.titleBar = self.GetChild("TitleBar")
			self.probText = self.GetChild("SuccessPercentage")
			self.costText = self.GetChild("Cost")
			self.costText2 = self.GetChild("Cost2")
			self.costText3 = self.GetChild("Cost3")
			self.acceptbtn = self.GetChild("AcceptButton")
			self.cancelbtn = self.GetChild("CancelButton")
			self.successPercentage = self.GetChild("SuccessPercentage")
			self.GetChild("AcceptButton").SetEvent(self.OpenQuestionDialog)
			self.GetChild("CancelButton").SetEvent(self.CancelRefine)
		except:
			import exception
			exception.Abort("RefineDialog.__LoadScript.BindObject")

		if constInfo.ENABLE_REFINE_PCT:
			self.successPercentage.Show()
		else:
			self.successPercentage.Hide()

		toolTip = uiToolTip.ItemToolTip()
		toolTip.SetParent(self)
		toolTip.SetFollow(False)
		toolTip.SetPosition(15, 38)
		toolTip.Show()
		self.toolTip = toolTip

		self.slotList = []
		for i in range(3):
			slot = self.__MakeSlot()
			slot.SetParent(toolTip)
			slot.SetWindowVerticalAlignCenter()
			self.slotList.append(slot)

		itemImage = self.__MakeItemImage()
		itemImage.SetParent(toolTip)
		itemImage.SetWindowVerticalAlignCenter()
		itemImage.SetPosition(-35, 0)
		self.itemImage = itemImage

		self.titleBar.SetCloseEvent(ui.__mem_func__(self.CancelRefine))
		if ENABLE_REFINE_ITEM_DESCRIPTION:
			self.tooltipItem = uiToolTip.ItemToolTip()
			self.tooltipItem.Hide()

		if app.ENABLE_REFINE_RENEWAL:
			self.checkBox = ui.CheckBox()
			self.checkBox.SetParent(self)
			self.checkBox.SetPosition(0, 102)
			self.checkBox.SetWindowHorizontalAlignCenter()
			self.checkBox.SetWindowVerticalAlignBottom()
			self.checkBox.SetEvent(ui.__mem_func__(self.AutoRefine), "ON_CHECK", True)
			self.checkBox.SetEvent(ui.__mem_func__(self.AutoRefine), "ON_UNCKECK", False)
			self.checkBox.SetCheckStatus(constInfo.IS_AUTO_REFINE)
			self.checkBox.SetTextInfo(localeInfo.REFINEWINDOW_DO_NOT_CLOSE_WINDOW)
			self.checkBox.Show()

		self.isLoaded = True

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __MakeSlot(self):
		slot = ui.ImageBox()
		slot.LoadImage("d:/ymir work/ui/public/slot_base.sub")
		slot.Show()
		self.children.append(slot)
		return slot

	def __MakeItemImage(self):
		itemImage = ui.ImageBox()
		itemImage.Show()
		self.children.append(itemImage)
		return itemImage

	def __MakeThinBoard(self):
		thinBoard = ui.ThinBoard()
		thinBoard.SetParent(self)
		thinBoard.Show()
		self.children.append(thinBoard)
		return thinBoard

	def Destroy(self):
		self.ClearDictionary()
		self.dlgQuestion = None
		self.board = 0
		self.probText = 0
		self.costText = 0
		self.costText2 = 0
		self.costText3 = 0
		self.titleBar = 0
		self.toolTip = 0
		self.checkBox = 0
		self.successPercentage = None
		self.slotList = []
		self.children = []
		if app.WJ_ENABLE_TRADABLE_ICON:
			self.wndInventory = None
			self.lockedItem = (-1,-1)

	if app.ENABLE_REFINE_RENEWAL:
		def __InitializeOpen(self):
			self.children = []
			self.vnum = 0
			self.targetItemPos = 0
			self.dialogHeight = 0
			self.cost = 0
			self.cost2 = 0
			self.cost3 = 0
			self.percentage = 0
			self.percentageExtra = 0
			self.type = 0
			self.xRefineStart = 0
			self.yRefineStart = 0
			self.materialSlotVnums = []
			self.materialSources = {}

	def FormatCostText(self, cost, color, emoji_path):
		if cost == 0:
			return None
		cost_str = str(cost)
		formatted_cost = '.'.join([cost_str[max(i - 3, 0):i] for i in range(len(cost_str) % 3, len(cost_str) + 1, 3) if i])
		return "|c{color}{formatted_cost} {emoji}".format(
			color=color,
			formatted_cost=formatted_cost,
			emoji=emoji.AppendEmoji(emoji_path)
		)
		
	def GetUpgradeChanceText(self, percentage, percentageExtra=0):
		if percentage > 75:
			color = "FF84f05d"
		elif 50 < percentage <= 75:
			color = "FFffa12e"
		else:
			color = "FFf25757"
	
		if percentageExtra == 0:
			return localeInfo.UPGRADE_CHANCE.format(color=color, percentage=percentage)
		else:
			return localeInfo.UPGRADE_CHANCE_EXTRA.format(color=color, percentage=percentage, percentageExtra=percentageExtra)

	def UpdateCostTexts(self):
		main_cost_text = self.FormatCostText(self.cost, "FFffc700", "icon/emoji/money_icon.png")
		if main_cost_text:
			self.costText.SetText(localeInfo.REFINEWINDOW_PRICE_1.format(main_cost_text))
		self.costText2.Hide()
		self.costText3.Hide()

		if self.cost2 != 0:
			cost2_text = self.FormatCostText(self.cost2, "FFb8b8b8", "icon/emoji/cheque_icon.png")
			self.costText2.Show()
			self.costText2.SetText(cost2_text)

		if self.cost3 != 0:
			cost3_text = self.FormatCostText(self.cost3, "FF85d455", "d:/ymir work/ui/stone_point/stone_point.tga")
			self.costText3.Show()
			self.costText3.SetText(cost3_text)
			
	def Open(self, targetItemPos, nextGradeItemVnum, cost, cost2, cost3, prob, type, probExtra):

		if False == self.isLoaded:
			self.__LoadScript()

		if ENABLE_REFINE_ITEM_DESCRIPTION:
			global TOOLTIP_DATA
			TOOLTIP_DATA = []

		if app.ENABLE_REFINE_RENEWAL:
			self.__InitializeOpen()
		else:
			self.__Initialize()

		self.targetItemPos = targetItemPos
		self.vnum = nextGradeItemVnum
		self.cost = cost
		self.cost2 = cost2
		self.cost3 = cost3
		self.percentage = prob
		self.percentageExtra = probExtra
		self.type = type


		self.probText.SetText(self.GetUpgradeChanceText(self.percentage, self.percentageExtra))

		self.UpdateCostTexts()

		if app.WJ_ENABLE_TRADABLE_ICON:
			self.SetCantMouseEventSlot(targetItemPos)

		self.toolTip.ClearToolTip()
		metinSlot = []
		for i in range(player.METIN_SOCKET_MAX_NUM):
			metinSlot.append(player.GetItemMetinSocket(targetItemPos, i))

		if metinSlot[0] < 100:
			metinSlot = []
			for i in range(player.METIN_SOCKET_MAX_NUM):
				metinSlot.append(0)

		attrSlot = []
		for i in range(player.ATTRIBUTE_SLOT_MAX_NUM):
			attrSlot.append(player.GetItemAttribute(targetItemPos, i))

		item.SelectItem(nextGradeItemVnum)

		if item.GetItemType() == item.ARMOR and item.GetItemSubType() == item.ARMOR_GLOVE:
			self.toolTip.AddGloveItemData(nextGradeItemVnum, metinSlot, attrSlot)
		else:
			self.toolTip.AddRefineItemData(nextGradeItemVnum, metinSlot, attrSlot)

		self.itemImage.LoadImage(item.GetIconImageFileName())
		xSlotCount, ySlotCount = item.GetItemSize()
		for slot in self.slotList:
			slot.Hide()
		for i in range(min(3, ySlotCount)):
			self.slotList[i].SetPosition(-35, i*32 - (ySlotCount-1)*16)
			self.slotList[i].Show()

		self.dialogHeight = self.toolTip.GetHeight() + 46
		self.UpdateDialog()

		self.SetTop()
		self.Show()

	def Close(self):
		if self.dlgQuestion:
			self.dlgQuestion.Close()

		self.dlgQuestion = None
		if ENABLE_REFINE_ITEM_DESCRIPTION and self.tooltipItem:
			self.tooltipItem.HideToolTip()
		self.Hide()

		if app.WJ_ENABLE_TRADABLE_ICON:
			self.lockedItem = (-1, -1)
			self.SetCanMouseEventSlot(self.targetItemPos)

	if ENABLE_REFINE_ITEM_DESCRIPTION:
		def __MakeItemSlot(self, slotIndex):
			slot = ui.SlotWindow()
			slot.SetParent(self)
			slot.SetSize(32, 32)
			slot.SetSlotBaseImage("d:/ymir work/ui/public/Slot_Base.sub", 1.0, 1.0, 1.0, 1.0)
			slot.AppendSlot(slotIndex, 0, 0, 32, 32)
			slot.SetOverInItemEvent(ui.__mem_func__(self.OverInItem))
			slot.SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))
			slot.SetSelectItemSlotEvent(ui.__mem_func__(self.SearchShop))
			slot.RefreshSlot()
			slot.Show()
			self.children.append(slot)
			return slot
			
		def SearchShop(self, slotIndex):
			if app.__BL_CHEST_DROP_INFO__:
				if app.IsPressed(app.DIK_LCONTROL):
					isMain = not app.IsPressed(app.DIK_LSHIFT)
					if item.HasDropInfo(TOOLTIP_DATA[slotIndex], isMain):
						self.wndChestDropInfo.Open(TOOLTIP_DATA[slotIndex], isMain)
					return

			if not app.IsPressed(app.DIK_LCONTROL):
				if not app.IsPressed(app.DIK_LSHIFT):
					try:
						interface = constInfo.GetInterfaceInstance()
						if interface:
							shopSearch = interface.GetShopSearchWindow()
							if shopSearch:
								if not shopSearch.IsShow():
									shopSearch.Show()
								item.SelectItem(TOOLTIP_DATA[slotIndex])
								shopSearch.sItemName.SetText(item.GetItemName())
								shopSearch.OnSearch()
					except:
						pass
			
		def __GetMaterialVnum(self, slotIndex):
			if slotIndex < 0 or slotIndex >= len(self.materialSlotVnums):
				return 0
			return self.materialSlotVnums[slotIndex]

		def __ResolveMaterialSourceName(self, sourceType, sourceVnum):
			if sourceType == REFINE_SOURCE_TYPE_MONSTER:
				name = nonplayer.GetMonsterName(sourceVnum)
			else:
				item.SelectItem(sourceVnum)
				name = item.GetItemName()
			return name if name else "#{:d}".format(sourceVnum)

		def __AppendMaterialSourcesToolTip(self, materialVnum):
			sourceMap = self.materialSources.get(materialVnum, {})
			if not sourceMap:
				return

			monsterVnums = sourceMap.get(REFINE_SOURCE_TYPE_MONSTER, [])
			itemVnums = sourceMap.get(REFINE_SOURCE_TYPE_ITEM, [])
			if not monsterVnums and not itemVnums:
				return

			self.tooltipItem.AppendSpace(5)
			self.tooltipItem.AppendTextLine(localeInfo.REFINEWINDOW_POSSIBLE_SOURCES, self.tooltipItem.CONDITION_COLOR)

			if monsterVnums:
				self.tooltipItem.AppendSpace(3)
				self.tooltipItem.AppendTextLine(localeInfo.REFINEWINDOW_SOURCE_MONSTERS, self.tooltipItem.SPECIAL_TITLE_COLOR)
				for sourceVnum in monsterVnums:
					self.tooltipItem.AppendTextLine("- {}".format(self.__ResolveMaterialSourceName(REFINE_SOURCE_TYPE_MONSTER, sourceVnum)), self.tooltipItem.NORMAL_COLOR)

			if itemVnums:
				self.tooltipItem.AppendSpace(3)
				self.tooltipItem.AppendTextLine(localeInfo.REFINEWINDOW_SOURCE_ITEMS, self.tooltipItem.SPECIAL_TITLE_COLOR)
				for sourceVnum in itemVnums:
					self.tooltipItem.AppendTextLine("- {}".format(self.__ResolveMaterialSourceName(REFINE_SOURCE_TYPE_ITEM, sourceVnum)), self.tooltipItem.NORMAL_COLOR)

		def OverInItem(self, slotIndex):
			if slotIndex > len(TOOLTIP_DATA):
				return

			if self.tooltipItem:
				self.tooltipItem.ClearToolTip()
				self.tooltipItem.AddItemData(TOOLTIP_DATA[slotIndex], 0, 0, 0, 0, player.INVENTORY)
				self.tooltipItem.AppendSpace(5)
				self.tooltipItem.AppendTextLine("{}".format(emoji.AppendEmoji("icon/emoji/key_lclick.png")))
				self.tooltipItem.AppendTextLine(localeInfo.REFINEWINDOW_FIND_IN_SHOPS)
				materialVnum = self.__GetMaterialVnum(slotIndex)
				if materialVnum:
					self.__AppendMaterialSourcesToolTip(materialVnum)
				self.tooltipItem.AppendSpace(5)
				self.tooltipItem.AlignHorizonalCenter()
				self.tooltipItem.ShowToolTip()

		def OverOutItem(self):
			if self.tooltipItem:
				self.tooltipItem.HideToolTip()

	def AppendMaterial(self, vnum, count):
		if ENABLE_REFINE_ITEM_DESCRIPTION:
			slotIndex = len(TOOLTIP_DATA)

			slot = self.__MakeItemSlot(slotIndex)
			slot.SetPosition(15, self.dialogHeight)
			slot.SetItemSlot(slotIndex, vnum, count)

			TOOLTIP_DATA.append(vnum)
			self.materialSlotVnums.append(vnum)
		else:
			slot = self.__MakeSlot()
			slot.SetParent(self)
			slot.SetPosition(15, self.dialogHeight)

			itemImage = self.__MakeItemImage()
			itemImage.SetParent(slot)
			item.SelectItem(vnum)
			itemImage.LoadImage(item.GetIconImageFileName())

		thinBoard = self.__MakeThinBoard()
		thinBoard.SetPosition(50, self.dialogHeight)
		thinBoard.SetSize(self.toolTip.GetWidth(), 20)

		countByVnum = player.GetItemCountByVnum(vnum)

		textLine = ui.TextLine()
		textLine.SetParent(thinBoard)
		textLine.SetFontName(localeInfo.UI_DEF_FONT)
		textLine.SetPackedFontColor(0xffdddddd)
		textLine.SetText("%s x%d / x%d" % (item.GetItemName(), count, countByVnum))
		textLine.SetOutline()
		textLine.SetFeather(FALSE)
		textLine.SetWindowVerticalAlignCenter()
		textLine.SetVerticalAlignCenter()


		textLine.SetPosition(15, 0)
		if player.GetItemCountByVnum(vnum) >= count:
			textLine.SetFontColor(0.33, 0.80, 0.46)
		else:
			textLine.SetFontColor(0.9, 0.4745, 0.4627)

		textLine.Show()
		self.children.append(textLine)

		self.dialogHeight += 38
		self.UpdateDialog()


	def UpdateDialog(self):
		newWidth = self.toolTip.GetWidth() + 60
		newHeight = self.dialogHeight + 115

		newHeight -= 8

		self.board.SetSize(newWidth, newHeight)
		self.toolTip.SetPosition(15 + 35, 38)
		self.titleBar.SetWidth(newWidth-15)
		self.SetSize(newWidth, newHeight)

		(x, y) = self.GetLocalPosition()
		self.SetPosition(x, y)

	def OpenQuestionDialog(self):

		if 100 == self.percentage+self.percentageExtra:
			self.Accept()
			return

		if 5 == self.type:
			self.Accept()
			return

		dlgQuestion = uiCommon.QuestionDialog()
		dlgQuestion.SetText(localeInfo.REFINE_WARNING2)
		dlgQuestion.SetAcceptEvent(ui.__mem_func__(self.Accept))
		dlgQuestion.SetCancelEvent(ui.__mem_func__(dlgQuestion.Close))

		if 3 == self.type:
			dlgQuestion.SetText(localeInfo.REFINE_DESTROY_WARNING_WITH_BONUS_PERCENT_1)

		self.dlgQuestion = dlgQuestion
		self.dlgQuestion.Open()

	def Accept(self):
		if app.ENABLE_REFINE_RENEWAL:
			net.SendRefinePacket(self.targetItemPos, self.type)
		else:
			net.SendRefinePacket(self.targetItemPos, self.type)
			self.Close()

	if app.ENABLE_REFINE_RENEWAL:	
		def AutoRefine(self, checkType, autoFlag):
			constInfo.IS_AUTO_REFINE = autoFlag
		
		def CheckRefine(self, isFail):
			if constInfo.IS_AUTO_REFINE == True:
				if constInfo.AUTO_REFINE_TYPE == 1:
					if constInfo.AUTO_REFINE_DATA["ITEM"][0] != -1 and constInfo.AUTO_REFINE_DATA["ITEM"][1] != -1:
						scrollIndex = player.GetItemIndex(constInfo.AUTO_REFINE_DATA["ITEM"][0])
						itemIndex = player.GetItemIndex(constInfo.AUTO_REFINE_DATA["ITEM"][1])
						
						if scrollIndex == 0 or (itemIndex % 10 == 8 and not isFail):
							self.Close()
						else:
							net.SendItemUseToItemPacket(constInfo.AUTO_REFINE_DATA["ITEM"][0], constInfo.AUTO_REFINE_DATA["ITEM"][1])
				elif constInfo.AUTO_REFINE_TYPE == 2:
					npcData = constInfo.AUTO_REFINE_DATA["NPC"]
					if npcData[0] != 0 and npcData[1] != -1 and npcData[2] != -1 and npcData[3] != 0:
						itemIndex = player.GetItemIndex(npcData[1], npcData[2])
						if (itemIndex % 10 == 8 and not isFail) or isFail:
							self.Close()
						else:
							net.SendGiveItemPacket(npcData[0], npcData[1], npcData[2], npcData[3])
				else:
					self.Close()
			else:
				self.Close()

	def CancelRefine(self):
		if ENABLE_REFINE_ITEM_DESCRIPTION:
			TOOLTIP_DATA = []
		net.SendRefinePacket(255, 255)
		self.Close()
		
		if app.ENABLE_REFINE_RENEWAL:
			constInfo.AUTO_REFINE_TYPE = 0
			constInfo.AUTO_REFINE_DATA = {
				"ITEM" : [-1, -1],
				"NPC" : [0, -1, -1, 0]
			}

	def OnPressEscapeKey(self):
		self.CancelRefine()
		return True

	if app.WJ_ENABLE_TRADABLE_ICON:
		def SetCanMouseEventSlot(self, slotIndex):
			itemInvenPage = slotIndex // player.INVENTORY_PAGE_SIZE
			localSlotPos = slotIndex - (itemInvenPage * player.INVENTORY_PAGE_SIZE)
			self.lockedItem = (-1, -1)

			if itemInvenPage == self.wndInventory.GetInventoryPageIndex():
				self.wndInventory.wndItem.SetCanMouseEventSlot(localSlotPos)

		def SetCantMouseEventSlot(self, slotIndex):
			itemInvenPage = slotIndex // player.INVENTORY_PAGE_SIZE
			localSlotPos = slotIndex - (itemInvenPage * player.INVENTORY_PAGE_SIZE)
			self.lockedItem = (itemInvenPage, localSlotPos)

			if itemInvenPage == self.wndInventory.GetInventoryPageIndex():
				self.wndInventory.wndItem.SetCantMouseEventSlot(localSlotPos)

		def SetInven(self, wndInventory):
			from _weakref import proxy
			self.wndInventory = proxy(wndInventory)

		def RefreshLockedSlot(self):
			if self.wndInventory:
				itemInvenPage, itemSlotPos = self.lockedItem
				if self.wndInventory.GetInventoryPageIndex() == itemInvenPage:
					self.wndInventory.wndItem.SetCantMouseEventSlot(itemSlotPos)

				self.wndInventory.wndItem.RefreshSlot()

	def AppendMaterialSource(self, materialVnum, sourceType, sourceVnum):
		if materialVnum == 0 or sourceVnum == 0:
			return
		if sourceType not in (REFINE_SOURCE_TYPE_MONSTER, REFINE_SOURCE_TYPE_ITEM):
			return
		sourceMap = self.materialSources.setdefault(materialVnum, {
			REFINE_SOURCE_TYPE_MONSTER: [],
			REFINE_SOURCE_TYPE_ITEM: [],
		})
		if sourceVnum not in sourceMap[sourceType]:
			sourceMap[sourceType].append(sourceVnum)

