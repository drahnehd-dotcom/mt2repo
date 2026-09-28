import ui, net, localeInfo, player, item, nonplayer, uiToolTip, renderTarget, app

from _weakref import proxy

COLLECT_PATH = "d:/ymir work/ui/poly_window/{}"
PATH = "d:/ymir work/ui/itemshop/"
SKINS_RENDER_INDEX = 7
SHOP_REDNER_INDEX = 8
AFFECT_DICT = uiToolTip.ItemToolTip.AFFECT_DICT_POLY

class PolySystemWindow(ui.ScriptWindow):

	MAX_COLLECT_SHOW = 6
	DEFAULT_MOB_SKIN = 636

	COLLECTION_SIZE_X = 420
	SHOP_SIZE_X = 420

	class SkinButton(ui.RadioButton):
		BUTTON_SIZE = (197, 23)
		LOCKED_IMAGE = COLLECT_PATH.format("locked_btn0.png")
		UNLOCKED_IMAGE = (COLLECT_PATH.format("unlocked_btn0.png"), COLLECT_PATH.format("unlocked_btn1.png"), COLLECT_PATH.format("unlocked_btn2.png"))
		SELECTED_IMAGE = (COLLECT_PATH.format("skin_collect_actual.png"), COLLECT_PATH.format("skin_collect_actual_hover.png"), COLLECT_PATH.format("skin_collect_actual_down.png"))
		def __init__(self, index, skinVnum, unlockItem):
			super(PolySystemWindow.SkinButton, self).__init__()

			self.__Index = index
			self.__SkinVnum = skinVnum
			self.__UnlockItem = unlockItem

			self.SetUpVisual(self.LOCKED_IMAGE)
			self.SetOverVisual(self.LOCKED_IMAGE)
			self.SetDownVisual(self.LOCKED_IMAGE)
			self.VisualUpdate()
			self.SetText(nonplayer.GetMonsterName(int(self.__SkinVnum)))
			self.Show()

		def __del__(self):
			super(PolySystemWindow.SkinButton, self).__del__()

		def VisualUpdate(self):
			if player.IsUnlockedSkin(self.__Index):
				self.SetUpVisual(self.UNLOCKED_IMAGE[0])
				self.SetOverVisual(self.UNLOCKED_IMAGE[1])
				self.SetDownVisual(self.UNLOCKED_IMAGE[2])
			else:
				self.SetUpVisual(self.LOCKED_IMAGE)
				self.SetOverVisual(self.LOCKED_IMAGE)
				self.SetDownVisual(self.LOCKED_IMAGE)

			if player.GetPolySkin() == self.__Index:
				self.SetUpVisual(self.SELECTED_IMAGE[0])
				self.SetOverVisual(self.SELECTED_IMAGE[1])
				self.SetDownVisual(self.SELECTED_IMAGE[2])
				return

		def GetSkinVnum(self):
			return self.__SkinVnum

		def GetUnlockItem(self):
			return self.__UnlockItem

		def GetIndex(self):
			return self.__Index

		def OnSelect(self):
			pass
		
		def OnUnselect(self):
			pass

	def __init__(self):
		super(PolySystemWindow, self).__init__()
		self.__ActualCategory = 0
		self.__ActualStage = 0
		self.__ActualSkin = None
		self.__Stages = {}
		self.__StageButtons = []
		self.__BonusImages = []
		self.__BonusText = []
		self.__LoadWindow()

	def __del__(self):
		super(PolySystemWindow, self).__del__()

	def __LoadWindow(self):
		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, "uiscript/polysystemwindow.py")

		self.__TitleBar = self.GetChild("TitleBar")
		self.__TitleBar.SetCloseEvent(ui.__mem_func__(self.Close))

		self.__PageShop = self.GetChild("PageShop")
		self.__PageCollections = self.GetChild("PageCollections")

		self.__PageButton = self.GetChild("PageButton")
		self.__PageButton.SetEvent(ui.__mem_func__(self.__OnPageButton))

		self.__BuyButton = self.GetChild("BuyButton")
		self.__BuyButton.SetEvent(ui.__mem_func__(self.__OnBuy))

		self.__ItemsSlot = self.GetChild("ItemsSlot")
		self.__ItemsSlot.SetOverInItemEvent(ui.__mem_func__(self.__OverInItem))
		self.__ItemsSlot.SetOverOutItemEvent(ui.__mem_func__(self.__OverOutItem))

		self.__SkinSlot = self.GetChild("SkinSlot")
		self.__SkinSlot.SetOverInItemEvent(ui.__mem_func__(self.__OverInSkin))
		self.__SkinSlot.SetOverOutItemEvent(ui.__mem_func__(self.__OverOutItem))

		self.BackButton = self.GetChild("BackButton")
		self.BackButton.SetEvent(ui.__mem_func__(self.__OnPageButton))

		self.__CollectionScroll = ScrollBar()
		self.__CollectionScroll.SetParent(self.__PageCollections)
		self.__CollectionScroll.SetScrollBarSize(198)
		self.__CollectionScroll.SetPosition(202, 2)
		self.__CollectionScroll.EnableSmoothMode()
		self.__CollectionScroll.Show()

		self.__CollectionsBox = self.GetChild("CollectBox")
		self.__CollectionsBox.SetItemSize(*self.SkinButton.BUTTON_SIZE)
		self.__CollectionsBox.SetViewItemCount(self.MAX_COLLECT_SHOW)
		self.__CollectionsBox.SetItemStep(self.SkinButton.BUTTON_SIZE[1]+3)
		self.__CollectionsBox.SetScrollBar(self.__CollectionScroll)
		self.__CollectionsBox.SetSelectEvent(ui.__mem_func__(self.__OnSelectSkin))

		self.__CollectionsBox.SetScrollBar(self.__CollectionScroll)
		self.__CollectionsBox.OnMouseWheel = self.__CollectionScroll.OnMouseWheel

		self.__CollectRender = self.GetChild("Render")
		self.__CollectRender.SetRenderTarget(SKINS_RENDER_INDEX)

		self.money_text = self.GetChild("money_text")
		self.cheque_text = self.GetChild("cheque_text")
		self.buy_board = self.GetChild("buy_board")

		self.count_window = self.GetChild("count_window")
		self.count_window.Hide()

		self.__StageButtons = []
		for i in range(3):
			stageButton = self.GetChild("StageButton{}".format(i+1))
			stageButton.SetEvent(ui.__mem_func__(self.__OnSelectStage), i)
			self.__StageButtons.append(stageButton)

		self.__BonusImages = []
		self.__BonusText = []
		for i in range(2):
			self.__BonusImages.append(self.GetChild("BonusImage{}".format(i+1)))
			self.__BonusText.append(self.GetChild("BonusText{}".format(i+1)))

		self.__SkinButton = self.GetChild("SkinButton")
		self.__SkinButton.SetEvent(ui.__mem_func__(self.__OnClickSkin))
		self.__OnShopPage()

	def __GetSkinItem(self):
		actualSkin = player.GetPolySkin()
		for skinItem in self.__CollectionsBox.itemList:
			if skinItem.GetIndex() == actualSkin:
				return skinItem.GetUnlockItem()

		return 0

	def __GetSkinVnum(self):
		actualSkin = player.GetPolySkin()
		for skinItem in self.__CollectionsBox.itemList:
			if skinItem.GetIndex() == actualSkin:
				return skinItem.GetSkinVnum()

		return 0

	def __GetNeedItem(self, slot):
		actualStage = self.__ActualStage + 1
		stageData = self.__Stages.get(actualStage, None)
		if not stageData:
			return 0

		itemList = stageData[1]
		return itemList[slot][0]

	def __GetApplyName(self, affectType, affectValue):
		if 0 == affectType:
			return None
		if 0 == affectValue:
			return None
		try:
			return AFFECT_DICT[affectType] % (affectValue)
		except TypeError:
			return "UNKNOWN_VALUE[%s] %s" % (affectType, affectValue)
		except KeyError:
			return "UNKNOWN_TYPE[%s] %s" % (affectType, affectValue)

	def __OverInItem(self, slot=0):
		if not self.__TTip:
			return

		vnum = self.__GetNeedItem(slot)
		if not vnum:
			return

		self.__TTip.SetItemToolTip(vnum)

	def __OverInSkin(self, slot=0):
		if not self.__TTip:
			return

		vnum = self.__GetSkinItem()
		if not vnum:
			return

		self.__TTip.SetItemToolTip(vnum)

	def __OverOutItem(self):
		if self.__TTip:
			self.__TTip.HideToolTip()

	def __OnSelectStage(self, stageId):
		self.__StageButtons[self.__ActualStage].SetUp()
		self.__ActualStage = stageId
		self.__StageButtons[stageId].Down()
		self.__OnRefreshStage()

	def __OnRefreshStage(self):
		stageId = self.__ActualStage + 1
		stageData = self.__Stages.get(stageId, None)
		if not stageData:
			return

		self.__SkinSlot.ClearSlot(0)
		skinItem = self.__GetSkinItem()
		if skinItem:
			self.__SkinSlot.SetItemSlot(0, skinItem, 0)
		self.__SkinSlot.RefreshSlot()

		bonusList = stageData[0]
		for idx, (bonusType, bonusValue) in enumerate(bonusList):
			if bonusType == 0 or bonusValue == 0:
				self.__BonusImages[idx].Hide()
				self.__BonusText[idx].SetText("-")
				self.__BonusText[idx].SetPackedFontColor(0xff4a4a48)
				continue

			self.__BonusImages[idx].Show()
			self.__BonusText[idx].SetText("{}".format(self.__GetApplyName(bonusType, bonusValue)))
			self.__BonusText[idx].SetPackedFontColor(uiToolTip.ItemToolTip.SPECIAL_POSITIVE_COLOR)

		itemList = stageData[1]
		for idx, (vnum, count) in enumerate(itemList):
			self.__ItemsSlot.SetItemSlot(idx, vnum, count)

		self.__ItemsSlot.RefreshSlot()

	def __OnBuy(self):
		stageId = self.__ActualStage + 1
		net.SendPolyBuy(stageId)

	def __OnCollectionPage(self):
		self.__PageShop.Hide()
		self.__PageCollections.Show()
		self.buy_board.Hide()
		for i in range(3):
			self.__StageButtons[i].Hide()
		for i in range(2):
			self.__BonusImages[i].Hide()
		self.__UpdateRender()

	def __OnShopPage(self):
		self.__PageShop.Show()
		self.__PageCollections.Hide()
		self.buy_board.Show()
		for i in range(3):
			self.__StageButtons[i].Show()
		self.__OnRefreshStage()
		self.__UpdateRender()

	def __UpdateRender(self):
		bStatus = self.__PageCollections.IsShow()
		renderTarget.SetVisibility(SKINS_RENDER_INDEX, True)
		renderTarget.SetBackground(SKINS_RENDER_INDEX, "d:/ymir work/ui/game/myshop_deco/model_view_bg.sub")
		if bStatus:
			monsterVnum = self.__GetSkinVnum()
			if self.__ActualSkin:
				monsterVnum = self.__ActualSkin.GetSkinVnum()

			renderTarget.SelectModel(SKINS_RENDER_INDEX, monsterVnum)
		else:
			renderTarget.SelectModel(SKINS_RENDER_INDEX, self.DEFAULT_MOB_SKIN)

	def __OnPageButton(self):
		if self.__PageShop.IsShow():
			self.__OnCollectionPage()
		else:
			self.__OnShopPage()

	def __OnSelectSkin(self, selectedSkin = None):
		if self.__ActualSkin:
			self.__ActualSkin.SetUp()

		renderTarget.SelectModel(SKINS_RENDER_INDEX, selectedSkin.GetSkinVnum())
		self.__ActualSkin = selectedSkin
		self.__ActualSkin.Down()

	def __OnClickSkin(self):
		if self.__ActualSkin == None:
			return

		if not player.IsUnlockedSkin(self.__ActualSkin.GetIndex()):
			self.__ActualSkin.SetUp()
			return
	
		net.SendPolySkin(self.__ActualSkin.GetIndex())

	def Refresh(self):
		self.RefreshSkins()
		self.__OnSelectStage(0)
		self.__UpdateRender()

	def RefreshSkins(self):
		for skinButton in self.__CollectionsBox.itemList:
			skinButton.VisualUpdate()

		self.__SkinSlot.ClearSlot(0)
		skinItem = self.__GetSkinItem()
		if skinItem:
			self.__SkinSlot.SetItemSlot(0, skinItem, 0)
		self.__SkinSlot.RefreshSlot()
		self.__UpdateRender()

	def AppendStages(self, polyStages):
		self.__Stages = {}
		for stageId, monsterVnum, dwItem, stageBonuses, stageItems in polyStages:
			self.__Stages[stageId] = (stageBonuses, stageItems)

		self.__OnRefreshStage()

	def AppendSkins(self, polySkins):
		self.__ActualSkin = None
		self.__CollectionsBox.RemoveAllItems()
		for index, skin, ivnum in polySkins:
			if not isinstance(index, int) or not isinstance(skin, int) or not isinstance(ivnum, int):
				sys_err("Bad type in polySkins: index={} ({}), skin={} ({}), ivnum={} ({})".format(
					index, type(index), skin, type(skin), ivnum, type(ivnum)
				))
		
			self.__CollectionsBox.AppendButton(self.SkinButton(index, skin, ivnum), True)

	def Open(self):
		self.RefreshSkins()
		self.__UpdateRender()
		self.Show()

	def Close(self):
		# Podglad 3D musi zgasnac razem z oknem - dopoki render target jest "widoczny",
		# silnik deformuje jego model CO KLATKE (do 53 ms/klatke wg hitch_log).
		renderTarget.SetVisibility(SKINS_RENDER_INDEX, False)
		net.SendPolyClose()
		self.Hide()

	def CloseByServer(self):
		renderTarget.SetVisibility(SKINS_RENDER_INDEX, False)
		self.Hide()

	def SetToolTip(self, tip):
		self.__TTip = proxy(tip)

	def OnPressEscapeKey(self):
		self.Close()
		return True

	def Destroy(self):
		renderTarget.SetVisibility(SKINS_RENDER_INDEX, False)
		self.__TTip = None
		self.__ActualSkin = None
		self.__ActualCategory = 0
		self.__BonusImages = []
		self.__BonusText = []
		self.__StageButtons = []
		self.ClearDictionary()
		self.Hide()

class ScrollBar(ui.Window):
	SCROLLBAR_WIDTH = 17
	SCROLLBAR_MIDDLE_HEIGHT = 9
	SCROLLBAR_BUTTON_HEIGHT = 0
	MIDDLE_BAR_POS = 8
	MIDDLE_BAR_UPPER_PLACE = 3
	MIDDLE_BAR_DOWNER_PLACE = 5
	TEMP_SPACE = MIDDLE_BAR_UPPER_PLACE + MIDDLE_BAR_DOWNER_PLACE
	if app.__BL_SMOOTH_SCROLL__:
		SMOOTH_RATIO = 1

	def __init__(self):
		ui.Window.__init__(self)

		self.pageSize = 1
		self.curPos = 0.0
		self.eventScroll = lambda *arg: None
		self.lockFlag = False
		self.scrollStep = 1
		if app.__BL_SMOOTH_SCROLL__:
			self.smooth_mode = False
			self.actual_pos = 0.0
			self._lastSmoothTime = 0.0   # do skalowania plynnego scrolla czasem
			self.target_pos = 0.0

		self.CreateScrollBar()

	def __del__(self):
		ui.Window.__del__(self)

	def CreateScrollBar(self):
		barSlot = ui.ExpandedImageBox()
		barSlot.SetParent(self)
		barSlot.AddFlag("not_pick")
		barSlot.LoadImage(PATH+"scroll_slot.png")
		barSlot.Show()

		middleBar = ui.DragButton()
		middleBar.SetParent(self)
		middleBar.AddFlag("movable")
		middleBar.SetMoveEvent(ui.__mem_func__(self.OnMove))
		middleBar.SetUpVisual(PATH+"scroll_button.png")
		middleBar.SetOverVisual(PATH+"scroll_button.png")
		middleBar.SetDownVisual(PATH+"scroll_button.png")
		middleBar.Show()

		self.middleBar = middleBar
		self.barSlot = barSlot

		self.SCROLLBAR_WIDTH = self.middleBar.GetWidth()
		self.SCROLLBAR_MIDDLE_HEIGHT = self.middleBar.GetHeight()

	def Destroy(self):
		self.middleBar = None
		self.eventScroll = lambda *arg: None

	def SetScrollEvent(self, event):
		self.eventScroll = event

	def SetMiddleBarSize(self, pageScale):
		pass

	def SetScrollBarSize(self, height):
		self.pageSize = (height - self.SCROLLBAR_BUTTON_HEIGHT * 2) - self.SCROLLBAR_MIDDLE_HEIGHT - (self.TEMP_SPACE)
		self.SetSize(self.SCROLLBAR_WIDTH, height)
		self.middleBar.SetRestrictMovementArea(self.MIDDLE_BAR_POS,
											   self.SCROLLBAR_BUTTON_HEIGHT + self.MIDDLE_BAR_UPPER_PLACE,
											   self.MIDDLE_BAR_POS + 2,
											   height - self.SCROLLBAR_BUTTON_HEIGHT * 2 - self.TEMP_SPACE)
		self.middleBar.SetPosition(self.MIDDLE_BAR_POS, 0)

		self.UpdateBarSlot()

	def UpdateBarSlot(self):
		barHeight = self.barSlot.GetHeight()
		if barHeight <= 0:
			return
		self.barSlot.SetScale(1.0, float(self.GetHeight()) / float(barHeight))

	def GetPos(self):
		return self.curPos

	def SetPos(self, pos):
		pos = max(0.0, pos)
		pos = min(1.0, pos)

		newPos = float(self.pageSize) * pos
		self.middleBar.SetPosition(self.MIDDLE_BAR_POS,
								   int(newPos) + self.SCROLLBAR_BUTTON_HEIGHT + self.MIDDLE_BAR_UPPER_PLACE)
		self.OnMove()

	def SetScrollStep(self, step):
		self.scrollStep = step

	def GetScrollStep(self):
		return self.scrollStep

	def OnMouseWheel(self, nLen):
		if nLen > 0:
			self.OnUp()
			return True
		elif nLen < 0:
			self.OnDown()
			return True
		return False

	def OnUp(self):
		if app.__BL_SMOOTH_SCROLL__ and self.smooth_mode:
			self.actual_pos = min(1.0, max(0.0, self.curPos))
			self.target_pos = min(1.0, max(0.0, self.curPos-self.scrollStep))
		else:
			self.SetPos(self.curPos-self.scrollStep)

	def OnDown(self):
		if app.__BL_SMOOTH_SCROLL__ and self.smooth_mode:
			self.actual_pos = min(1.0, max(0.0, self.curPos))
			self.target_pos = min(1.0, max(0.0, self.curPos+self.scrollStep))
		else:
			self.SetPos(self.curPos+self.scrollStep)

	def OnMove(self):

		if self.lockFlag:
			return

		if 0 == self.pageSize:
			return

		(xLocal, yLocal) = self.middleBar.GetLocalPosition()
		self.curPos = float(yLocal - self.SCROLLBAR_BUTTON_HEIGHT - self.MIDDLE_BAR_UPPER_PLACE) / float(self.pageSize)

		self.eventScroll()

	def OnMouseLeftButtonDown(self):
		(xMouseLocalPosition, yMouseLocalPosition) = self.GetMouseLocalPosition()
		pickedPos = yMouseLocalPosition - self.SCROLLBAR_BUTTON_HEIGHT - self.SCROLLBAR_MIDDLE_HEIGHT // 2
		newPos = float(pickedPos) / float(self.pageSize)
		if app.__BL_SMOOTH_SCROLL__ and self.smooth_mode:
			self.actual_pos = min(1.0, max(0.0, self.curPos))
			self.target_pos = min(1.0, max(0.0, newPos))
		else:
			self.SetPos(newPos)

	def LockScroll(self):
		self.lockFlag = True

	def UnlockScroll(self):
		self.lockFlag = False

	if app.__BL_SMOOTH_SCROLL__:
		def EnableSmoothMode(self):
			self.smooth_mode = True

		def OnUpdate(self):
			if not self.smooth_mode:
				return
			
			if self.lockFlag:
				return
			
			if 0 == self.pageSize:
				return
			
			if self.actual_pos == self.target_pos:
				return

			# Plynne przewijanie liczylo krok NA KLATKE, wiec po odblokowaniu limitu FPS
			# przy 144 Hz scroll dojezdzal do celu 2.4x szybciej. Skalujemy krok czasem.
			scale, self._lastSmoothTime = ui.GetFrameStepScale(self._lastSmoothTime)
			distance = abs(self.actual_pos - self.target_pos)
			smooth_step = max(distance / ScrollBar.SMOOTH_RATIO, 0.005) * scale
		
			if self.actual_pos < self.target_pos:
				self.actual_pos = min(self.actual_pos + smooth_step, self.target_pos)
			elif self.actual_pos > self.target_pos:
				self.actual_pos = max(self.actual_pos - smooth_step, self.target_pos)
			
			self.SetPos(self.actual_pos)