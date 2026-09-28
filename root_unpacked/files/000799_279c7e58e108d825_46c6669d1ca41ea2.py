import ui
import chat
import localeInfo
import net
import uiToolTip
import player
import wndMgr
import app
import item
import chr


NOTICE_BOARD_CAN_CLOSE_WITH_ESC = True
NOTICE_BOARD_AUTO_CLOSE_TIME_SEC = 5

ENLIGNTENMENT_LVL_MAX = 5

# Modul player nie ma GetEnlightLevel(). chr.GetEnlightLevelByVID() mimo nazwy nie przyjmuje VID -
# czyta poziom z instancji wybranej przez chr.SelectInstance, wiec wybieramy postac gracza.
def GetEnlightLevel():
	chr.SelectInstance(player.GetMainCharacterIndex())
	return chr.GetEnlightLevelByVID()

ENLIGNTENMENT_DATA = {
	0 : [0, 0, 0, [], []],
	1 : [0, 0, 0, [], [(localeInfo.ENLIGHTENMENT_MAX_HP, "+10.000"), (localeInfo.ENLIGHTENMENT_AVG_DAMAGE, "+2%"), (localeInfo.ENLIGHTENMENT_SKILL_DAMAGE, "+5%"), (localeInfo.ENLIGHTENMENT_HUMAN_RESIST, "+4%"), (localeInfo.ENLIGHTENMENT_HUMAN_RESIST_PIERCE, "+4%")]],
	2 : [0, 50, 250000, [(90029,50),(90033,500),(30502,500),(34000,50)], [(localeInfo.ENLIGHTENMENT_MAX_SP, "+20.000"), (localeInfo.ENLIGHTENMENT_AVG_DAMAGE, "+4%"), (localeInfo.ENLIGHTENMENT_SKILL_DAMAGE, "+10%"), (localeInfo.ENLIGHTENMENT_HUMAN_RESIST, "+8%"), (localeInfo.ENLIGHTENMENT_HUMAN_RESIST_PIERCE, "+8%")]],
	3 : [0, 100, 500000, [(90029,50),(90033,500),(30502,500),(34000,50)], [(localeInfo.ENLIGHTENMENT_MAX_SP, "+30.000"), (localeInfo.ENLIGHTENMENT_AVG_DAMAGE, "+6%"), (localeInfo.ENLIGHTENMENT_SKILL_DAMAGE, "+20%"), (localeInfo.ENLIGHTENMENT_HUMAN_RESIST, "+12%"), (localeInfo.ENLIGHTENMENT_HUMAN_RESIST_PIERCE, "+12%")]],
}

class LevelupNoticeBoard(ui.Window):
	def __init__(self):
		ui.Window.__init__(self)
		
		self.closeTime = 0

		self.BuildWindow()

	def __del__(self):
		ui.Window.__del__(self)

	def BuildWindow(self):
		self.AddFlag("float")
		self.AddFlag("not_pick")
		
		self.bg = ui.ImageBox()
		self.bg.SetParent(self)
		self.bg.LoadImage("kowal/enlightenment/msg_bg.png")
		self.bg.SetPosition(0, 0)
		self.bg.Show()
		
		self.enlighLvlImg = ui.ImageBox()
		self.enlighLvlImg.SetParent(self.bg)
		self.enlighLvlImg.Show()

		self.titleTxt = ui.TextLine("Tahoma:14")
		self.titleTxt.SetParent(self.bg)
		self.titleTxt.SetPosition(183, 15)
		self.titleTxt.SetHorizontalAlignCenter()
		self.titleTxt.SetText("�rove� zatracen�")
		self.titleTxt.Show()

		self.infoTxt = ui.TextLine("Tahoma:12")
		self.infoTxt.SetParent(self.bg)
		self.infoTxt.SetPosition(183, 38)
		self.infoTxt.SetHorizontalAlignCenter()
		self.infoTxt.SetOutline()
		self.infoTxt.Show()

		self.infoTxt2 = ui.TextLine("Tahoma:12")
		self.infoTxt2.SetParent(self.bg)
		self.infoTxt2.SetPosition(183, 50)
		self.infoTxt2.SetHorizontalAlignCenter()
		self.infoTxt2.SetOutline()
		self.infoTxt2.Show()

		self.SetSize(295, 81)
		self.SetWindowHorizontalAlignCenter()
		self.SetPosition(0, 150)
		self.Hide()

	def Open(self, pName, pEnlightLvl):
		self.enlighLvlImg.LoadImage("kowal/enlightenment/lvl%d.png"%pEnlightLvl)
		self.enlighLvlImg.SetPosition(41-self.enlighLvlImg.GetWidth() // 2, 40-self.enlighLvlImg.GetHeight() // 2)
		self.infoTxt.SetText("Hr�� %s m�"%pName)
		self.infoTxt2.SetText("nyn� %d �rove� zatracen�!"%pEnlightLvl)

		self.closeTime = app.GetGlobalTimeStamp() + NOTICE_BOARD_AUTO_CLOSE_TIME_SEC

		self.Show()
		self.SetTop()

	def OpenCrafting(self, pName):
		self.enlighLvlImg.LoadImage("icon/talizmany/swiatlo.tga")
		self.enlighLvlImg.SetPosition(41-self.enlighLvlImg.GetWidth() // 2, 40-self.enlighLvlImg.GetHeight() // 2)
		self.infoTxt.SetText("Hr�� %s vytvo�il"%pName)
		self.infoTxt2.SetText("Talisman Sv�tla")

		self.closeTime = app.GetGlobalTimeStamp() + NOTICE_BOARD_AUTO_CLOSE_TIME_SEC

		self.Show()
		self.SetTop()
		
	def OnUpdate(self):
		if app.GetGlobalTimeStamp() >= self.closeTime:
			self.closeTime = 0
			self.Hide()

	def OnPressEscapeKey(self):
		if self.IsShow() and NOTICE_BOARD_CAN_CLOSE_WITH_ESC:
			self.Hide()
			return True
		return False

class BonusListItem(ui.Window):
	def __init__(self):
		ui.Window.__init__(self)

		self.BuildWindow()

	def __del__(self):
		ui.Window.__del__(self)

	def BuildWindow(self):
		self.bg = ui.ImageBox()
		self.bg.SetParent(self)
		self.bg.LoadImage("kowal/enlightenment/bonus_locked_bg.png")
		self.bg.SetPosition(0, 0)
		self.bg.Show()
		
		self.bonusNameTxt = ui.TextLine("Tahoma:14")
		self.bonusNameTxt.SetParent(self.bg)
		self.bonusNameTxt.SetPosition(22, 3)
		self.bonusNameTxt.SetPackedFontColor(0xFFABABAB)
		self.bonusNameTxt.Show()
		
		self.bonusValueTxt = ui.TextLine("Tahoma:14")
		self.bonusValueTxt.SetParent(self.bg)
		self.bonusValueTxt.SetPosition(216, 3)
		self.bonusValueTxt.SetPackedFontColor(0xFF8BDD6E)
		self.bonusValueTxt.SetHorizontalAlignCenter()
		self.bonusValueTxt.Show()

		self.Show()
		self.SetSize(242, 24)

	def SetBonus(self, bonusName, bonusValue):
		if bonusName == "":
			self.bg.LoadImage("kowal/enlightenment/bonus_locked_bg.png")
			self.bonusNameTxt.SetText("")
			self.bonusValueTxt.SetText("")
		else:
			self.bg.LoadImage("kowal/enlightenment/bonus_unlocked_bg.png")
			self.bonusNameTxt.SetText(bonusName)
			self.bonusValueTxt.SetText(bonusValue)

class EnlightenmentWindow(ui.Window):
	def __init__(self):
		ui.Window.__init__(self)

		self.isLevelUping = False
		self.itemTooltip = uiToolTip.ItemToolTip()
		
		self.noticeBoard = None
		self.craftingNoticeBoard = None
		
		self.BuildWindow()

	def __del__(self):
		ui.Window.__del__(self)
	
	def BuildWindow(self):
		self.AddFlag('movable')
		self.AddFlag('float')

		self.Board = ui.BoardWithTitleBar()
		self.Board.SetParent(self)
		self.Board.SetSize(723, 509)
		self.Board.SetPosition(0, 0)
		self.Board.SetTitleName("�rove� zatracen�")
		self.Board.SetCloseEvent(ui.__mem_func__(self.Close))
		self.Board.Show()
		
		self.bg = ui.ImageBox()
		self.bg.AddFlag('attach')
		self.bg.SetParent(self.Board)
		self.bg.LoadImage("kowal/enlightenment/bg.png")
		self.bg.SetPosition(20, 51)
		self.bg.Show()

		self.actualLvlImg = ui.ImageBox()
		self.actualLvlImg.SetParent(self.Board)
		self.actualLvlImg.LoadImage("kowal/enlightenment/lvl0.png")
		self.actualLvlImg.SetPosition(146-self.actualLvlImg.GetWidth() // 2, 125-self.actualLvlImg.GetHeight() // 2)
		self.actualLvlImg.Show()

		self.nextLvlImg = ui.ImageBox()
		self.nextLvlImg.SetParent(self.Board)
		self.nextLvlImg.LoadImage("kowal/enlightenment/lvl0.png")
		self.nextLvlImg.SetPosition(397-self.nextLvlImg.GetWidth() // 2, 125-self.nextLvlImg.GetHeight() // 2)
		self.nextLvlImg.Show()
		
		self.levelUpAnimation = ui.AniImageBox()
		self.levelUpAnimation.SetParent(self.Board)
		self.levelUpAnimation.SetDelay(3)
		for i in range(30):
			self.levelUpAnimation.AppendImage("kowal/enlightenment/anim/%d.png"%i)
		self.levelUpAnimation.SetPosition(20, 336)
		self.levelUpAnimation.SetOnEndFrame(ui.__mem_func__(self.OnEndLevelUpAnimation))
		self.levelUpAnimation.Hide()
		
		self.actualBonusItems = {}
		self.nextBonusItems = {}
		for i in range(8):
			self.actualBonusItems[i] = BonusListItem()
			self.actualBonusItems[i].SetParent(self.Board)
			self.actualBonusItems[i].SetPosition(24, 161+i*21)
			self.actualBonusItems[i].SetBonus("", "")
			self.actualBonusItems[i].Show()

			self.nextBonusItems[i] = BonusListItem()
			self.nextBonusItems[i].SetParent(self.Board)
			self.nextBonusItems[i].SetPosition(275, 161+i*21)
			self.nextBonusItems[i].SetBonus("", "")
			self.nextBonusItems[i].Show()

		self.neededItemsGrid = ui.GridSlotWindow()
		self.neededItemsGrid.SetParent(self.Board)
		self.neededItemsGrid.SetPosition(553, 60)
		self.neededItemsGrid.ArrangeSlot(0, 4, 7, 32, 32, 0, 0)
		self.neededItemsGrid.RefreshSlot()
		self.neededItemsGrid.SetOverInItemEvent(ui.__mem_func__(self.OverInItem))
		self.neededItemsGrid.SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))
		self.neededItemsGrid.Show()
		self.neededItemsGrid.SetItemSlot(0, 19, 5)
		
		self.yangTxt = ui.TextLine("Tahoma:14")
		self.yangTxt.SetParent(self.bg)
		self.yangTxt.SetPosition(620, 253)
		self.yangTxt.SetHorizontalAlignCenter()
		self.yangTxt.Show()

		self.wonTxt = ui.TextLine("Tahoma:14")
		self.wonTxt.SetParent(self.bg)
		self.wonTxt.SetPosition(620, 288)
		self.wonTxt.SetHorizontalAlignCenter()
		self.wonTxt.Show()

		self.poTxt = ui.TextLine("Tahoma:14")
		self.poTxt.SetParent(self.bg)
		self.poTxt.SetPosition(620, 323)
		self.poTxt.SetHorizontalAlignCenter()
		self.poTxt.Show()
		
		self.levelUpBtn = ui.Button()
		self.levelUpBtn.SetParent(self.Board)
		self.levelUpBtn.SetPosition(540, 412)
		self.levelUpBtn.SetUpVisual("kowal/enlightenment/levelup_btn_norm.png")
		self.levelUpBtn.SetOverVisual("kowal/enlightenment/levelup_btn_hover.png")
		self.levelUpBtn.SetDownVisual("kowal/enlightenment/levelup_btn_down.png")
		self.levelUpBtn.SAFE_SetEvent(self.OnClickLevelUpBtn)
		self.levelUpBtn.Show()
		
		self.SetSize(self.Board.GetWidth(), self.Board.GetHeight())
		self.SetCenterPosition()
		self.Hide()

	def OnEndLevelUpAnimation(self):
		if self.isLevelUping:
			self.isLevelUping = False
			self.levelUpAnimation.Hide()
			net.SendChatPacket("/enlight")

	def OnClickLevelUpBtn(self):
		if self.isLevelUping:
			return

		itemsData = ENLIGNTENMENT_DATA[GetEnlightLevel()+1][3]
		for i in range(len(itemsData)):
			if itemsData[i][0] != 0:
				if player.GetItemCountByVnum(itemsData[i][0]) < itemsData[i][1]:
					item.SelectItem(itemsData[i][0])
					chat.AppendChat(1, localeInfo.ENLIGHTENMENT_MISSING_ITEM % (item.GetItemName(), itemsData[i][1]))
					return

		if player.GetElk() < ENLIGNTENMENT_DATA[GetEnlightLevel()+1][0]:
			chat.AppendChat(1, localeInfo.ENLIGHTENMENT_NOT_ENOUGH_YANG)
			return

		if player.GetCheque() < ENLIGNTENMENT_DATA[GetEnlightLevel()+1][1]:
			chat.AppendChat(1, localeInfo.ENLIGHTENMENT_NOT_ENOUGH_WON)
			return

		if player.GetPktOsiag() < ENLIGNTENMENT_DATA[GetEnlightLevel()+1][2]:
			chat.AppendChat(1, localeInfo.ENLIGHTENMENT_NOT_ENOUGH_POINTS)
			return

		self.isLevelUping = True
		self.levelUpAnimation.ResetFrame()
		self.levelUpAnimation.Show()

	def OverInItem(self, slotIdx):
		self.itemTooltip.SetItemToolTip(ENLIGNTENMENT_DATA[GetEnlightLevel()+1][3][slotIdx][0])

	def OverOutItem(self):
		self.itemTooltip.HideToolTip()

	def RefreshWindow(self):
		for i in range(8):
			self.actualBonusItems[i].SetBonus("", "")
			self.nextBonusItems[i].SetBonus("", "")

		for i in range(4*7):
			self.neededItemsGrid.ClearSlot(i)
		self.neededItemsGrid.RefreshSlot()

		enlightLevel = GetEnlightLevel()
		if enlightLevel == ENLIGNTENMENT_LVL_MAX:
			self.actualLvlImg.LoadImage("kowal/enlightenment/lvl5.png")
			self.actualLvlImg.SetPosition(146-self.actualLvlImg.GetWidth() // 2, 125-self.actualLvlImg.GetHeight() // 2)
			self.nextLvlImg.Hide()

			bonusData = ENLIGNTENMENT_DATA[enlightLevel][4]
			for i in range(len(bonusData)):
				self.actualBonusItems[i].SetBonus(bonusData[i][0], bonusData[i][1])
				
			self.yangTxt.SetText("0")
			self.wonTxt.SetText("0")
			self.poTxt.SetText("0")

			self.levelUpBtn.Down()
			self.levelUpBtn.Disable()
		else:
			nextEnlightLevel = enlightLevel+1
			self.actualLvlImg.LoadImage("kowal/enlightenment/lvl%d.png"%enlightLevel)
			self.actualLvlImg.SetPosition(146-self.actualLvlImg.GetWidth() // 2, 125-self.actualLvlImg.GetHeight() // 2)
			
			self.nextLvlImg.LoadImage("kowal/enlightenment/lvl%d.png"%nextEnlightLevel)
			self.nextLvlImg.SetPosition(397-self.nextLvlImg.GetWidth() // 2, 125-self.nextLvlImg.GetHeight() // 2)

			bonusData = ENLIGNTENMENT_DATA[enlightLevel][4]
			for i in range(len(bonusData)):
				self.actualBonusItems[i].SetBonus(bonusData[i][0], bonusData[i][1])

			bonusData = ENLIGNTENMENT_DATA[nextEnlightLevel][4]
			for i in range(len(bonusData)):
				self.nextBonusItems[i].SetBonus(bonusData[i][0], bonusData[i][1])
			
			itemsData = ENLIGNTENMENT_DATA[nextEnlightLevel][3]
			for i in range(len(itemsData)):
				if itemsData[i][0] != 0:
					self.neededItemsGrid.SetItemSlot(i, itemsData[i][0], itemsData[i][1])
			self.neededItemsGrid.RefreshSlot()

			self.yangTxt.SetText(localeInfo.NumberToString(ENLIGNTENMENT_DATA[nextEnlightLevel][0]))
			self.wonTxt.SetText(localeInfo.NumberToString(ENLIGNTENMENT_DATA[nextEnlightLevel][1]))
			self.poTxt.SetText(localeInfo.NumberToString(ENLIGNTENMENT_DATA[nextEnlightLevel][2]))

			self.levelUpBtn.Enable()
			self.levelUpBtn.SetUp()

	def OpenWindow(self):
		self.Show()
		self.SetTop()
		self.RefreshWindow()
		self.SetCenterPosition()

	def Close(self):
		self.Hide()

	def OnPressEscapeKey(self):
		if self.IsShow():
			self.Close()
			return True
		return False

	def OpenNoticeUpgradeBoard(self, pName, pLevel):
		if self.noticeBoard == None:
			self.noticeBoard = LevelupNoticeBoard()
		self.noticeBoard.Open(pName, pLevel)

	def OpenNoticeCraftinBoard(self, pName):
		if self.craftingNoticeBoard == None:
			self.craftingNoticeBoard = LevelupNoticeBoard()
		self.craftingNoticeBoard.OpenCrafting(pName)
