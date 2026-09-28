import ui
import chat
import playerSettingModule
import chr
import localeInfo
import net
import player
import app
import uiToolTip

JOB_NAME_LIST = [localeInfo.JOB_WARRIOR, localeInfo.JOB_ASSASSIN, localeInfo.JOB_SURA, localeInfo.JOB_SHAMAN]
SKILL_GROUP_NAME_DICT = {
	playerSettingModule.JOB_WARRIOR	: { 1 : localeInfo.SKILL_GROUP_WARRIOR_1,	2 : localeInfo.SKILL_GROUP_WARRIOR_2, },
	playerSettingModule.JOB_ASSASSIN	: { 1 : localeInfo.SKILL_GROUP_ASSASSIN_1,	2 : localeInfo.SKILL_GROUP_ASSASSIN_2, },
	playerSettingModule.JOB_SURA		: { 1 : localeInfo.SKILL_GROUP_SURA_1,		2 : localeInfo.SKILL_GROUP_SURA_2, },
	playerSettingModule.JOB_SHAMAN		: { 1 : localeInfo.SKILL_GROUP_SHAMAN_1,	2 : localeInfo.SKILL_GROUP_SHAMAN_2, },
}

class RankingWindow(ui.Window):
	class RankListItem(ui.Window):
		def __init__(self, idx, parent, isMyPosition=False):
			ui.Window.__init__(self)
			self.SetParent(parent)
			self.idx = idx
			self.isMyPosition = isMyPosition

			self.BuildWindow()

		def __del__(self):
			ui.Window.__del__(self)
		
		def BuildWindow(self):
			self.SetSize(401, 32)

			self.bg = ui.ImageBox()
			self.bg.SetParent(self)
			self.bg.SetPosition(0, 0)
			self.bg.LoadImage("kowal/ranking/list_item.png")
			self.bg.Show()

			if not self.isMyPosition:
				self.playerPositionTxt = ui.TextLine("Tahoma:12")
				self.playerPositionTxt.SetParent(self.bg)
				self.playerPositionTxt.SetPackedFontColor(0xFFBBB7BE)
				self.playerPositionTxt.SetPosition(10, 8)
				self.playerPositionTxt.SetOutline()
				self.playerPositionTxt.SetText("%d."%(self.idx+1))
				self.playerPositionTxt.Show()

			self.playerNameTxt = ui.TextLine("Tahoma:12")
			self.playerNameTxt.SetParent(self.bg)
			self.playerNameTxt.SetPackedFontColor(0xFFBBB7BE)
			if self.idx >= 9:
				self.playerNameTxt.SetPosition(25, 8)
			else:
				self.playerNameTxt.SetPosition(20, 8)
			self.playerNameTxt.SetOutline()
			self.playerNameTxt.SetText(localeInfo.RANKING_WINDOW_NO_CHARACTERS)
			self.playerNameTxt.Show()
			if self.isMyPosition:
				self.playerNameTxt.SetPosition(66, 8)
				self.playerNameTxt.SetHorizontalAlignCenter()

			self.playerJobWithSkillGroupNameTxt = ui.TextLine("Tahoma:12")
			self.playerJobWithSkillGroupNameTxt.SetParent(self.bg)
			self.playerJobWithSkillGroupNameTxt.SetPackedFontColor(0xFFBBB7BE)
			self.playerJobWithSkillGroupNameTxt.SetPosition(182, 8)
			self.playerJobWithSkillGroupNameTxt.SetOutline()
			self.playerJobWithSkillGroupNameTxt.SetText("")
			self.playerJobWithSkillGroupNameTxt.SetHorizontalAlignCenter()
			self.playerJobWithSkillGroupNameTxt.Show()

			self.flagImg = ui.ImageBox()
			self.flagImg.SetParent(self.bg)
			self.flagImg.SetPosition(243, 6)
			self.flagImg.LoadImage("kowal/ranking/flag_1.png")
			self.flagImg.Hide()

			self.playerLevelTxt = ui.TextLine("Tahoma:12")
			self.playerLevelTxt.SetParent(self.bg)
			self.playerLevelTxt.SetPackedFontColor(0xFFBBB7BE)
			self.playerLevelTxt.SetPosition(317, 8)
			self.playerLevelTxt.SetOutline()
			self.playerLevelTxt.SetText("")
			self.playerLevelTxt.SetHorizontalAlignCenter()
			self.playerLevelTxt.Show()

			self.playerScoreTxt = ui.TextLine("Tahoma:12")
			self.playerScoreTxt.SetParent(self.bg)
			self.playerScoreTxt.SetPackedFontColor(0xFFBBB7BE)
			self.playerScoreTxt.SetPosition(370, 8)
			self.playerScoreTxt.SetOutline()
			self.playerScoreTxt.SetText("")
			self.playerScoreTxt.SetHorizontalAlignCenter()
			self.playerScoreTxt.Show()

			self.Show()

		def SetData(self, pName, raceWithskillGroup, empire, level, value):
			if empire == 0:
				self.playerNameTxt.SetText(pName)
				self.playerJobWithSkillGroupNameTxt.SetText("")
				self.flagImg.Hide()
				self.playerLevelTxt.SetText("")
				self.playerScoreTxt.SetText("")
			else:
				self.flagImg.Show()
				self.playerNameTxt.SetText(pName)
				self.playerJobWithSkillGroupNameTxt.SetText("")
				self.flagImg.Show()
				self.flagImg.LoadImage("kowal/ranking/flag_%d.png"%empire)
				self.playerLevelTxt.SetText(localeInfo.RANKING_LEVEL_PREFIX.format(level))
				self.playerScoreTxt.SetText("%s"%localeInfo.NumberToString(value))
				
				skillGroup = raceWithskillGroup%10
				race = int(raceWithskillGroup // 10)
				job = chr.RaceToJob(race)

				if job not in SKILL_GROUP_NAME_DICT:
					return
				
				if skillGroup == 1 or skillGroup == 2:
					self.playerJobWithSkillGroupNameTxt.SetText("%s %s"%(JOB_NAME_LIST[job], SKILL_GROUP_NAME_DICT[job][skillGroup]))
				else:
					self.playerJobWithSkillGroupNameTxt.SetText("%s"%JOB_NAME_LIST[job])

	def __init__(self):
		ui.Window.__init__(self)
		
		self.SERVER_RANK_CATEGORIES = [localeInfo.RANKING_WINDOW_CATEGORY_STONES, localeInfo.RANKING_WINDOW_CATEGORY_BOSSES, localeInfo.RANKING_WINDOW_CATEGORY_DUNGEONS, localeInfo.RANKING_WINDOW_CATEGORY_MONSTERS, localeInfo.RANKING_WINDOW_CATEGORY_ALCHEMY, localeInfo.RANKING_WINDOW_CATEGORY_REFINE, localeInfo.RANKING_WINDOW_CATEGORY_DRAGON_COINS]
		
		self.rankData = []
		self.myRankPosData = []
		self.rankNextRefreshTime = []
		for i in self.SERVER_RANK_CATEGORIES:
			self.rankData.append([])
			self.myRankPosData.append([0, 0])
			self.rankNextRefreshTime.append(0)
		
		self.nextUpdateTime = 0

		self.currentCatIdx = 0
		self.isLoading = False
		
		self.lastAddedPos = 0
		
		self.BuildWindow()

	def __del__(self):
		ui.Window.__del__(self)
	
	def BuildWindow(self):
		self.Board = ui.BoardWithTitleBar()
		self.Board.SetSize(460, 644)
		self.Board.SetCenterPosition()
		self.Board.AddFlag('movable')
		self.Board.AddFlag('float')
		self.Board.SetTitleName(localeInfo.RANKING_WINDOW_RANKING_TITLE)
		self.Board.SetCloseEvent(ui.__mem_func__(self.Close))
		
		self.bg = ui.ImageBox()
		self.bg.SetParent(self.Board)
		self.bg.SetPosition(20, 52)
		self.bg.LoadImage("kowal/ranking/bg.png")
		self.bg.Show()

		self.serverRankBtn = ui.Button()
		self.serverRankBtn.SetParent(self.bg)
		self.serverRankBtn.SetPosition(13, 8)
		self.serverRankBtn.SetUpVisual("kowal/ranking/server_rank_btn_norm.png")
		self.serverRankBtn.SetOverVisual("kowal/ranking/server_rank_btn_hover.png")
		self.serverRankBtn.SetDownVisual("kowal/ranking/server_rank_btn_down.png")
		self.serverRankBtn.SetDisableVisual("kowal/ranking/server_rank_btn_hover.png")
		self.serverRankBtn.SAFE_SetEvent(self.OnClickServerRanking)
		self.serverRankBtn.SetText("")
		self.serverRankBtn.Show()

		self.weeklyRankBtn = ui.Button()
		self.weeklyRankBtn.SetParent(self.bg)
		self.weeklyRankBtn.SetPosition(213, 8)
		self.weeklyRankBtn.SetUpVisual("kowal/ranking/weekly_rank_btn_norm.png")
		self.weeklyRankBtn.SetOverVisual("kowal/ranking/weekly_rank_btn_hover.png")
		self.weeklyRankBtn.SetDownVisual("kowal/ranking/weekly_rank_btn_down.png")
		self.weeklyRankBtn.SetDisableVisual("kowal/ranking/weekly_rank_btn_hover.png")
		self.weeklyRankBtn.SAFE_SetEvent(self.OnClickWeeklyRanking)
		self.weeklyRankBtn.SetText("")
		self.weeklyRankBtn.Show()
		
		self.weeklyRankingWindow = WeeklyRankingWindow()
		self.serverRankWindow = ui.Window()
		self.serverRankWindow.SetParent(self.bg)
		self.serverRankWindow.SetPosition(0, 50)
		self.serverRankWindow.SetSize(self.bg.GetWidth(), self.bg.GetHeight()-50)
		self.serverRankWindow.Show()
		
		self.serverRank_catBtns = {}
		for y in range(2):
			for x in range(3):
				i = y*3+x
				self.serverRank_catBtns[i] =  ui.Button()
				self.serverRank_catBtns[i].SetParent(self.serverRankWindow)
				self.serverRank_catBtns[i].SetPosition(24+x*125, 10+y*30)
				self.serverRank_catBtns[i].SetUpVisual("kowal/ranking/category_btn_norm.png")
				self.serverRank_catBtns[i].SetOverVisual("kowal/ranking/category_btn_hover.png")
				self.serverRank_catBtns[i].SetDownVisual("kowal/ranking/category_btn_down.png")
				self.serverRank_catBtns[i].SetDisableVisual("kowal/ranking/category_btn_hover.png")
				self.serverRank_catBtns[i].SAFE_SetEvent(self.OnClickServerRankCatBtn, i)
				self.serverRank_catBtns[i].SetText(self.SERVER_RANK_CATEGORIES[i], -1)
				self.serverRank_catBtns[i].ButtonText.SetOutline()
				self.serverRank_catBtns[i].Show()

		self.serverRank_rankListItems = {}
		for i in range(10):
			self.serverRank_rankListItems[i] = self.RankListItem(i, self.serverRankWindow)
			self.serverRank_rankListItems[i].SetPosition(10, 90+i*31)

		self.serverRank_myPosHeaderImg = ui.ImageBox()
		self.serverRank_myPosHeaderImg.SetParent(self.serverRankWindow)
		self.serverRank_myPosHeaderImg.SetPosition(37, 410)
		self.serverRank_myPosHeaderImg.LoadImage("kowal/ranking/your_pos_header.png")
		self.serverRank_myPosHeaderImg.Show()

		self.serverRank_myRankItem = self.RankListItem(0, self.serverRankWindow, True)
		self.serverRank_myRankItem.SetPosition(10, 456)

		self.serverRank_noCleanTxt = ui.TextLine("Tahoma:14")
		self.serverRank_noCleanTxt.SetParent(self.serverRankWindow)
		self.serverRank_noCleanTxt.SetPackedFontColor(0xFFBBB7BE)
		self.serverRank_noCleanTxt.SetPosition(210, 492)
		self.serverRank_noCleanTxt.SetOutline()
		self.serverRank_noCleanTxt.SetText(localeInfo.RANKING_WINDOW_SERVER_RANKING_DO_NOT_RESET)
		self.serverRank_noCleanTxt.SetHorizontalAlignCenter()
		self.serverRank_noCleanTxt.Show()

		self.serverRank_playerLevelFromTxt = ui.TextLine("Tahoma:12")
		self.serverRank_playerLevelFromTxt.SetParent(self.serverRankWindow)
		self.serverRank_playerLevelFromTxt.SetPackedFontColor(0xFFBBB7BE)
		self.serverRank_playerLevelFromTxt.SetPosition(210, 510)
		self.serverRank_playerLevelFromTxt.SetOutline()
		self.serverRank_playerLevelFromTxt.SetText(localeInfo.RANKING_WINDOW_LEVEL_RANK_LIMIT)
		self.serverRank_playerLevelFromTxt.SetHorizontalAlignCenter()
		self.serverRank_playerLevelFromTxt.Hide()

		self.OnClickServerRanking()

		self.Board.Hide()
		self.Hide()

	def OnClickServerRanking(self):
		self.serverRankBtn.Disable()
		self.serverRankWindow.Show()
		
	def OnClickWeeklyRanking(self):
		self.weeklyRankingWindow.OpenWindow()

	def OnClickServerRankCatBtn(self, catIdx):

		for i in range(len(self.serverRank_catBtns)):
			if i == catIdx:
				self.serverRank_catBtns[i].Disable()
			else:
				self.serverRank_catBtns[i].Enable()

		self.currentCatIdx = catIdx
		
		if catIdx == 0:
			self.serverRank_playerLevelFromTxt.Show()
			self.serverRank_noCleanTxt.SetPosition(210, 492)
		else:
			self.serverRank_playerLevelFromTxt.Hide()
			self.serverRank_noCleanTxt.SetPosition(210, 498)

		if self.rankNextRefreshTime[self.currentCatIdx] >= app.GetGlobalTimeStamp():
			self.ClearCurrentPage()
			for data in self.rankData[self.currentCatIdx]:
				self.LoadData(data)
			self.LoadMyPosition(self.myRankPosData[self.currentCatIdx][0])
			return

		self.isLoading = True
		net.SendLoadServerRanking(catIdx)

	def RecvLoadInfo(self, info):
		chat.AppendChat(1, "load %s"%info)
		self.isLoading = False
		self.nextUpdateTime = app.GetGlobalTime()+10000
		if info == "clear":
			self.rankNextRefreshTime[self.currentCatIdx] = app.GetGlobalTimeStamp() + 60*15 + 6
			del self.rankData[self.currentCatIdx][:]
			self.myRankPosData[self.currentCatIdx][0] = [0, 0]
			self.ClearCurrentPage()

	def ClearCurrentPage(self):
		self.lastAddedPos = 0
		for item in self.serverRank_rankListItems.values():
			item.SetData(localeInfo.RANKING_WINDOW_NO_CHARACTERS, 0, 0, 0, 0)
		self.serverRank_myRankItem.SetData(localeInfo.RANKING_WINDOW_NO_POSITION, 0, 0, 0, 0)

	def RecvLoadData(self, pName, level, raceWithskillGroup, empire, value):
		self.rankData[self.currentCatIdx].append([pName, level, raceWithskillGroup, empire, value])
		self.LoadData(self.rankData[self.currentCatIdx][len(self.rankData[self.currentCatIdx])-1])

	def RecvLoadMyPosition(self, position, value):
		self.myRankPosData[self.currentCatIdx][0] = [position, value]
		self.LoadMyPosition([position, value])
	
	def LoadData(self, data):
		self.serverRank_rankListItems[self.lastAddedPos].SetData(data[0], data[2], data[3], data[1], data[4])
		self.lastAddedPos += 1

	def LoadMyPosition(self, data):
		if data[0] != 0:
			self.serverRank_myRankItem.SetData(localeInfo.RANKING_WINDOW_POSITION %localeInfo.NumberToString(data[0]), net.GetMainActorRace()*10+net.GetMainActorSkillGroup(), net.GetMainActorEmpire(), player.GetStatus(player.LEVEL), data[1])

	def OnUpdate(self):

		if app.GetGlobalTime() > self.nextUpdateTime:
			self.nextUpdateTime = app.GetGlobalTime()+1000
			if app.GetGlobalTimeStamp() > self.rankNextRefreshTime[self.currentCatIdx]:
				self.nextUpdateTime = app.GetGlobalTime()+15000
				self.OnClickServerRankCatBtn(self.currentCatIdx)

	def OpenWindow(self):
		if self.IsShow():
			self.Close()
		else:
			self.Board.Show()
			self.Show()

			self.OnClickServerRankCatBtn(0)
	
	def Close(self):
		self.Board.Hide()
		self.Hide()

	def OnPressEscapeKey(self):
		if self.IsShow():
			self.Close()
			return TRUE
		return FALSE

class WeeklyRankingWindow(ui.Window):
	class RankListItem(ui.Window):
		def __init__(self, idx, parent, rewardEvent):
			ui.Window.__init__(self)
			self.SetParent(parent)
			self.idx = idx
			self.pos = idx+1
			self.rewardClickEvent = rewardEvent

			self.BuildWindow()

		def __del__(self):
			ui.Window.__del__(self)
		
		def BuildWindow(self):
			self.SetSize(398, 24)

			self.playerPositionTxt = ui.TextLine()
			self.playerPositionTxt.SetParent(self)
			self.playerPositionTxt.SetPosition(35, 14)
			self.playerPositionTxt.SetText("%d."%(self.idx+1))
			self.playerPositionTxt.SetHorizontalAlignCenter()
			self.playerPositionTxt.Show()

			self.extraPositionImg = ui.ImageBox()
			self.extraPositionImg.SetParent(self)
			self.extraPositionImg.SetPosition(-166, 14)
			self.extraPositionImg.Hide()

			self.playerNameTxt = ui.TextLine()
			self.playerNameTxt.SetParent(self)
			self.playerNameTxt.SetPosition(56, 13)
			self.playerNameTxt.SetText(localeInfo.RANKING_WINDOW_NO_CHARACTERS)
			self.playerNameTxt.Show()

			self.playerJobNameTxt = ui.TextLine()
			self.playerJobNameTxt.SetParent(self)
			self.playerJobNameTxt.SetPosition(149, 13)
			self.playerJobNameTxt.SetText("")
			self.playerJobNameTxt.Show()

			self.playerLevelTxt = ui.TextLine()
			self.playerLevelTxt.SetParent(self)
			self.playerLevelTxt.SetPosition(233, 13)
			self.playerLevelTxt.SetText("")
			self.playerLevelTxt.Show()

			self.playerScoreTxt = ui.TextLine()
			self.playerScoreTxt.SetParent(self)
			self.playerScoreTxt.SetPosition(271, 13)
			self.playerScoreTxt.SetText("")
			self.playerScoreTxt.Show()

			self.rewardBtn = ui.Button()
			self.rewardBtn.SetParent(self)
			self.rewardBtn.SetPosition(358, 11)
			self.rewardBtn.SetUpVisual("kowal/weekly_rank/reward_btn_norm.png")
			self.rewardBtn.SetOverVisual("kowal/weekly_rank/reward_btn_hover.png")
			self.rewardBtn.SetDownVisual("kowal/weekly_rank/reward_btn_down.png")
			self.rewardBtn.SetDisableVisual("kowal/weekly_rank/reward_btn_disabled.png")
			self.rewardBtn.SetEvent(ui.__mem_func__(self.OnClickRewardBtn))
			self.rewardBtn.Show()

			self.Show()

		def OnClickRewardBtn(self):
			x, y = self.rewardBtn.GetGlobalPosition()
			self.rewardClickEvent(x, y, self.pos)

		def SetData(self, pos, pName, race, level, value):
			if level == 0:
				self.playerNameTxt.SetText(pName)
				self.playerJobNameTxt.SetText("")
				self.playerLevelTxt.SetText("")
				self.playerScoreTxt.SetText("")
			else:
				self.playerNameTxt.SetText(pName)
				self.playerLevelTxt.SetText("%d"%level)
				self.playerScoreTxt.SetText("%s"%localeInfo.NumberToString(value))
				self.playerJobNameTxt.SetText("%s"%JOB_NAME_LIST[chr.RaceToJob(race)])
			
			self.pos = pos
			if pos == 0:
				self.extraPositionImg.Hide()
				sys_err("0 playerPositionTxt - {} ".format(pos))
				self.playerPositionTxt.SetText("?")
				self.rewardBtn.Disable()
			else:
				self.playerPositionTxt.SetText("%d."%pos)
				sys_err("playerPositionTxt - {} ".format(pos))
				if pos >= 1 and pos <= 3:
					self.extraPositionImg.LoadImage("kowal/weekly_rank/top_%d.png"%pos)
					self.extraPositionImg.SetWindowHorizontalAlignCenter()
					self.extraPositionImg.Show()
				if pos > 10:
					self.rewardBtn.Disable()
				else:
					self.rewardBtn.Enable()

	def __init__(self):
		ui.Window.__init__(self)
		
		self.WEEKLY_RANK_BTN_NAMES = ["stones", "bosses", "dungeons", "monsters", "alchemy", "refine", "dragon_coins"]
		
		self.REWARDS = [
			[
				[50117, 10,	80025, 25, 	92062, 1, 	80014, 2],
				[50117, 7, 	80025, 15, 	92061, 1, 	80014, 1],
				[50117, 5, 	80025, 10, 	92060, 1, 	80014, 1],
				[50117, 3, 	80025, 7, 	26913, 1],
				[50117, 2, 	80025, 6, 	26913, 1],
				[50117, 1, 	80025, 5, 	26913, 1],
				[50117, 1, 	80025, 5, 	26913, 1],
				[50117, 1, 	80025, 5, 	26913, 1],
				[50117, 1, 	80025, 5, 	26913, 1],
				[50117, 1, 	80025, 5, 	26913, 1],
			],

			[
				[50117, 1,	80025, 25, 	92059, 1, 	80014, 2],
				[50117, 1, 	80025, 15, 	92058, 1, 	80014, 1],
				[50117, 1, 	80025, 10, 	92057, 1, 	80014, 1],
				[50117, 3, 	80025, 7, 	26913, 1],
				[50117, 2, 	80025, 6, 	26913, 1],
				[50117, 1, 	80025, 5, 	26913, 1],
				[50117, 1, 	80025, 5, 	26913, 1],
				[50117, 1, 	80025, 5, 	26913, 1],
				[50117, 1, 	80025, 5, 	26913, 1],
				[50117, 1, 	80025, 5, 	26913, 1],
			],

			[
				[50117, 1,	80025, 25, 	92065, 1, 	80014, 2],
				[50117, 1, 	80025, 15, 	92064, 1, 	80014, 1],
				[50117, 1, 	80025, 10, 	92063, 1, 	80014, 1],
				[50117, 3, 	80025, 7, 	26913, 1],
				[50117, 2, 	80025, 6, 	26913, 1],
				[50117, 1, 	80025, 5, 	26913, 1],
				[50117, 1, 	80025, 5, 	26913, 1],
				[50117, 1, 	80025, 5, 	26913, 1],
				[50117, 1, 	80025, 5, 	26913, 1],
				[50117, 1, 	80025, 5, 	26913, 1],
			],

			[
				[50117, 1,	80025, 25, 	92056, 1, 	80014, 2],
				[50117, 1, 	80025, 15, 	92055, 1, 	80014, 1],
				[50117, 1, 	80025, 10, 	92054, 1, 	80014, 1],
				[50117, 3, 	80025, 7, 	26913, 1],
				[50117, 2, 	80025, 6, 	26913, 1],
				[50117, 1, 	80025, 5, 	26913, 1],
				[50117, 1, 	80025, 5, 	26913, 1],
				[50117, 1, 	80025, 5, 	26913, 1],
				[50117, 1, 	80025, 5, 	26913, 1],
				[50117, 1, 	80025, 5, 	26913, 1],
			],

			[
				[50117, 1,	80025, 25, 	92074, 1, 	80014, 2],
				[50117, 1, 	80025, 15, 	92073, 1, 	80014, 1],
				[50117, 1, 	80025, 10, 	92072, 1, 	80014, 1],
				[50117, 3, 	80025, 7, 	26913, 1],
				[50117, 2, 	80025, 6, 	26913, 1],
				[50117, 1, 	80025, 5, 	26913, 1],
				[50117, 1, 	80025, 5, 	26913, 1],
				[50117, 1, 	80025, 5, 	26913, 1],
				[50117, 1, 	80025, 5, 	26913, 1],
				[50117, 1, 	80025, 5, 	26913, 1],
			],

			[
				[50117, 1,	80025, 25, 	92077, 1, 	80014, 2],
				[50117, 1, 	80025, 15, 	92076, 1, 	80014, 1],
				[50117, 1, 	80025, 10, 	92075, 1, 	80014, 1],
				[50117, 3, 	80025, 7, 	26913, 1],
				[50117, 2, 	80025, 6, 	26913, 1],
				[50117, 1, 	80025, 5, 	26913, 1],
				[50117, 1, 	80025, 5, 	26913, 1],
				[50117, 1, 	80025, 5, 	26913, 1],
				[50117, 1, 	80025, 5, 	26913, 1],
				[50117, 1, 	80025, 5, 	26913, 1],
			],

			[
				[50117, 1,	80025, 25, 	92080, 1, 	80014, 2],
				[50117, 1, 	80025, 15, 	92079, 1, 	80014, 1],
				[50117, 1, 	80025, 10, 	92078, 1, 	80014, 1],
				[50117, 3, 	80025, 7, 	26913, 1],
				[50117, 2, 	80025, 6, 	26913, 1],
				[50117, 1, 	80025, 5, 	26913, 1],
				[50117, 1, 	80025, 5, 	26913, 1],
				[50117, 1, 	80025, 5, 	26913, 1],
				[50117, 1, 	80025, 5, 	26913, 1],
				[50117, 1, 	80025, 5, 	26913, 1],
			]
		]

		self.rankData = []
		self.myRankPosData = []
		self.rankNextRefreshTime = []
		for i in self.WEEKLY_RANK_BTN_NAMES:
			self.rankData.append([])
			self.myRankPosData.append([0, 0])
			self.rankNextRefreshTime.append(0)
		
		self.nextUpdateTime = 0
		self.nextResetUpdateTime = 0
		
		self.sundayEndTime = 0

		self.currentCatIdx = 0
		self.isLoading = False
		
		self.lastAddedPos = 0

		self.itemTooltip = uiToolTip.ItemToolTip()
		
		self.BuildWindow()

	def __del__(self):
		ui.Window.__del__(self)
	
	def BuildWindow(self):
		self.AddFlag('movable')
		self.AddFlag('float')
		self.SetSize(695, 574)
		self.SetCenterPosition()
		
		self.Board = ui.ImageBox()
		self.Board.AddFlag('attach')
		self.Board.SetParent(self)
		self.Board.SetPosition(0, 0)
		self.Board.LoadImage("kowal/weekly_rank/bg.png")
		self.Board.Show()

		self.closeBtn = ui.Button()
		self.closeBtn.SetParent(self.Board)
		self.closeBtn.SetPosition(642, 90)
		self.closeBtn.SetUpVisual("kowal/weekly_rank/exit_norm.png")
		self.closeBtn.SetOverVisual("kowal/weekly_rank/exit_hover.png")
		self.closeBtn.SetDownVisual("kowal/weekly_rank/exit_down.png")
		self.closeBtn.SetText("")
		self.closeBtn.SetToolTipText(localeInfo.UI_CLOSE)
		self.closeBtn.SetEvent(ui.__mem_func__(self.Close))
		self.closeBtn.Show()

		self.weeklyRank_catBtns = {}
		for i in range(len(self.WEEKLY_RANK_BTN_NAMES)):
			self.weeklyRank_catBtns[i] =  ui.Button()
			self.weeklyRank_catBtns[i].SetParent(self.Board)
			self.weeklyRank_catBtns[i].SetPosition(57, 132+i*39)
			self.weeklyRank_catBtns[i].SetUpVisual("kowal/weekly_rank/cat_%s_norm.png"%self.WEEKLY_RANK_BTN_NAMES[i])
			self.weeklyRank_catBtns[i].SetOverVisual("kowal/weekly_rank/cat_%s_hover.png"%self.WEEKLY_RANK_BTN_NAMES[i])
			self.weeklyRank_catBtns[i].SetDownVisual("kowal/weekly_rank/cat_%s_down.png"%self.WEEKLY_RANK_BTN_NAMES[i])
			self.weeklyRank_catBtns[i].SetDisableVisual("kowal/weekly_rank/cat_%s_hover.png"%self.WEEKLY_RANK_BTN_NAMES[i])
			self.weeklyRank_catBtns[i].SAFE_SetEvent(self.OnClickWeeklyRankCatBtn, i)
			self.weeklyRank_catBtns[i].Show()

		self.weeklyRank_rankListItems = {}
		for i in range(10):
			self.weeklyRank_rankListItems[i] = self.RankListItem(i, self.Board, ui.__mem_func__(self.OnClickRankingRewardsBtn))
			self.weeklyRank_rankListItems[i].SetPosition(261, 149+i*25)

		self.weeklyRank_myRankItem = self.RankListItem(0, self.Board, ui.__mem_func__(self.OnClickRankingRewardsBtn))
		self.weeklyRank_myRankItem.SetPosition(261, 447)

		self.weeklyRank_refreshTxt = ui.TextLine("Tahoma:14")
		self.weeklyRank_refreshTxt.SetParent(self.Board)
		self.weeklyRank_refreshTxt.SetPackedFontColor(0xFFFDEEFF)
		self.weeklyRank_refreshTxt.SetPosition(0, 539)
		self.weeklyRank_refreshTxt.SetOutline()
		self.weeklyRank_refreshTxt.SetText(localeInfo.RANKING_WINDOW_WEEKLY_RANK_RESET_TIME)
		self.weeklyRank_refreshTxt.SetHorizontalAlignCenter()
		self.weeklyRank_refreshTxt.SetWindowHorizontalAlignCenter()
		self.weeklyRank_refreshTxt.Show()
		self.weeklyRank_refreshTxt.clearRefreshTimes = False
		
		self.rewardBg = ui.ImageBox()
		self.rewardBg.SetParent(self)
		self.rewardBg.SetPosition(0, 0)
		self.rewardBg.LoadImage("kowal/weekly_rank/reward_bg.png")
		self.rewardBg.rewardsPosIdx = 555
		self.rewardBg.btnY = 0
		self.rewardBg.Hide()

		self.rewardItemsGrid = ui.GridSlotWindow()
		self.rewardItemsGrid.SetParent(self.rewardBg)
		self.rewardItemsGrid.SetPosition(31, 93)
		self.rewardItemsGrid.ArrangeSlot(0, 3, 2, 32, 32, 3, 2)
		self.rewardItemsGrid.RefreshSlot()
		self.rewardItemsGrid.SetOverInItemEvent(ui.__mem_func__(self.OverInRewardItem))
		self.rewardItemsGrid.SetOverOutItemEvent(ui.__mem_func__(self.OverOutRewardItem))
		self.rewardItemsGrid.SetSlotBaseImage("kowal/weekly_rank/slot.png", 1.0, 1.0, 1.0, 1.0)
		self.rewardItemsGrid.Show()

		self.closeRewardBtn = ui.Button()
		self.closeRewardBtn.SetParent(self.rewardBg)
		self.closeRewardBtn.SetPosition(130, 0)
		self.closeRewardBtn.SetUpVisual("kowal/weekly_rank/exit_norm.png")
		self.closeRewardBtn.SetOverVisual("kowal/weekly_rank/exit_hover.png")
		self.closeRewardBtn.SetDownVisual("kowal/weekly_rank/exit_down.png")
		self.closeRewardBtn.SetToolTipText(localeInfo.UI_CLOSE)
		self.closeRewardBtn.SetEvent(ui.__mem_func__(self.OnClickCloseRewardBtn))
		self.closeRewardBtn.Show()

		self.Hide()

	def OnClickRankingRewardsBtn(self, btnX, btnY, pos):
		if pos < 0 or pos > 10:
			return
		if self.rewardBg.btnY == btnY:
			self.OnClickCloseRewardBtn()
			return
		chat.AppendChat(1, "click reward %d %d %d"%(btnX, btnY, pos))
		boardX, boardY = self.Board.GetGlobalPosition()
		self.rewardBg.SetPosition(btnX-boardX-164, min(btnY-boardY-2, 410))
		self.rewardBg.rewardsPosIdx = pos-1
		self.rewardBg.btnY = btnY
		self.rewardBg.Show()

		rewardItems = self.REWARDS[self.currentCatIdx][pos-1]
		rewardItemsCount = len(rewardItems) // 2
		for i in range(3*2):
			if i < rewardItemsCount and rewardItems[i] != 0:
				self.rewardItemsGrid.SetItemSlot(i, rewardItems[i*2], rewardItems[i*2+1])
			else:
				self.rewardItemsGrid.ClearSlot(i)
		self.rewardItemsGrid.RefreshSlot()

	def OnClickCloseRewardBtn(self):
		self.rewardBg.Hide()
		self.rewardBg.rewardsPosIdx = 555
		self.rewardBg.btnY = 0

	def OverInRewardItem(self, slotIdx):
		self.itemTooltip.SetItemToolTip(self.REWARDS[self.currentCatIdx][self.rewardBg.rewardsPosIdx][slotIdx*2])

	def OverOutRewardItem(self):
		self.itemTooltip.HideToolTip()

	def OnClickWeeklyRankCatBtn(self, catIdx):

		if self.rewardBg.IsShow():
			self.OnClickCloseRewardBtn()

		for i in range(len(self.weeklyRank_catBtns)):
			if i == catIdx:
				self.weeklyRank_catBtns[i].Disable()
			else:
				self.weeklyRank_catBtns[i].Enable()

		self.currentCatIdx = catIdx

		if self.rankNextRefreshTime[self.currentCatIdx] >= app.GetGlobalTimeStamp():
			chat.AppendChat(1, "from memory")
			self.ClearCurrentPage()
			for data in self.rankData[self.currentCatIdx]:
				self.LoadData(data)
			self.LoadMyPosition(self.myRankPosData[self.currentCatIdx][0])
			return

		chat.AppendChat(1, "from server")
		self.isLoading = True
		net.SendLoadRanking(catIdx)

	def RecvLoadInfo(self, info, sundayEndTime):
		chat.AppendChat(1, "load %s"%info)
		self.isLoading = False
		self.nextUpdateTime = app.GetGlobalTime()+10000
		self.nextResetUpdateTime = 0
		self.sundayEndTime = sundayEndTime
		chat.AppendChat(1, "sundayEndTime {}".format(sundayEndTime))
		if info == "clear":
			self.rankNextRefreshTime[self.currentCatIdx] = app.GetGlobalTimeStamp() + 60*15 + 6
			del self.rankData[self.currentCatIdx][:]
			self.myRankPosData[self.currentCatIdx][0] = [0, 0]
			self.ClearCurrentPage()

	def ClearCurrentPage(self):
		self.lastAddedPos = 0
		for i in range(len(self.weeklyRank_rankListItems)):
			self.weeklyRank_rankListItems[i].SetData(i+1, localeInfo.RANKING_WINDOW_NO_CHARACTERS, 0, 0, 0)
		self.weeklyRank_myRankItem.SetData(0, player.GetName(), 0, 0, 0)

	def RecvLoadData(self, pName, level, race, value):
		self.rankData[self.currentCatIdx].append([pName, level, race, value])
		self.LoadData(self.rankData[self.currentCatIdx][len(self.rankData[self.currentCatIdx])-1])

	def RecvLoadMyPosition(self, position, value):
		self.myRankPosData[self.currentCatIdx][0] = [position, value]
		self.LoadMyPosition([position, value])
	
	def LoadData(self, data):
		self.weeklyRank_rankListItems[self.lastAddedPos].SetData(self.lastAddedPos+1, data[0], data[2], data[1], data[3])
		self.lastAddedPos += 1

	def LoadMyPosition(self, data):
		if data[0] != 0:
			self.weeklyRank_myRankItem.SetData(data[0], player.GetName(), net.GetMainActorRace(), player.GetStatus(player.LEVEL), data[1])

	def OnUpdate(self):

		timeStamp = app.GetGlobalTimeStamp()
		if app.GetGlobalTimeStamp() > self.nextResetUpdateTime:
			self.nextResetUpdateTime = app.GetGlobalTimeStamp()+1
			restSec = self.sundayEndTime - app.GetGlobalTimeStamp()
			if restSec > 0:
				chat.AppendChat(1, "Text {}".format(localeInfo.SecondToDHMS(restSec)))
				self.weeklyRank_refreshTxt.SetText(localeInfo.RANKING_WINDOW_WEEKLY_RANK_RESET_TIME_UPDATE % localeInfo.SecondToDHMS(restSec))
			else:
				self.weeklyRank_refreshTxt.SetText(localeInfo.RANKING_WINDOW_WEEKLY_RANK_RESET_TIME_UPDATE % localeInfo.SecondToDHMS(restSec))
			
		if app.GetGlobalTime() > self.nextUpdateTime:
			self.nextUpdateTime = app.GetGlobalTime()+1000
			if timeStamp > self.rankNextRefreshTime[self.currentCatIdx]:
				self.nextUpdateTime = app.GetGlobalTime()+15000
				self.OnClickWeeklyRankCatBtn(self.currentCatIdx)
			else:
				chat.AppendChat(1, "need wait: %d"%(self.rankNextRefreshTime[self.currentCatIdx]-app.GetGlobalTimeStamp()))

	def OpenWindow(self):
		if self.IsShow():
			self.Close()
		else:
			self.Show()
			self.SetTop()
			self.OnClickWeeklyRankCatBtn(0)
	
	def Close(self):
		self.Hide()

		if self.rewardBg.IsShow():
			self.OnClickCloseRewardBtn()

	def OnPressEscapeKey(self):
		if self.IsShow():
			self.Close()
			return TRUE
		return FALSE
