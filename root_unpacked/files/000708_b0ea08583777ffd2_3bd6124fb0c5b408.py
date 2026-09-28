# -*- coding: utf-8 -*-
import ui
import chat
import localeInfo
import net
import player
import grp
import exception
import playerSettingModule
import emoji
import time
import uiScriptLocale
from datetime import datetime, timedelta

# Face images for different races
FACE_IMAGE_DICT = {
	playerSettingModule.RACE_WARRIOR_M: "icon/face/warrior_m.tga",
	playerSettingModule.RACE_WARRIOR_W: "icon/face/warrior_w.tga",
	playerSettingModule.RACE_ASSASSIN_M: "icon/face/assassin_m.tga",
	playerSettingModule.RACE_ASSASSIN_W: "icon/face/assassin_w.tga",
	playerSettingModule.RACE_SURA_M: "icon/face/sura_m.tga",
	playerSettingModule.RACE_SURA_W: "icon/face/sura_w.tga",
	playerSettingModule.RACE_SHAMAN_M: "icon/face/shaman_m.tga",
	playerSettingModule.RACE_SHAMAN_W: "icon/face/shaman_w.tga",
}

# Title names for different categories and levels
# Kategoria = strona okna = grupa tytulow po stronie serwera (0 potwory, 1 bossy,
# 2 metiny, 3 dungeony, 4 alchemia, 5 ulepszanie, 6 wydane SM) — ta sama kolejnosc
# co TITLE_BONUS_* i titles_bonuses[] w char_titles.cpp. Slot 0 = ranga III.
TITLE_NAMES = {
	0: {0: uiScriptLocale.TITLE_0_0, 1: uiScriptLocale.TITLE_0_1, 2: uiScriptLocale.TITLE_0_2},
	1: {0: uiScriptLocale.TITLE_1_0, 1: uiScriptLocale.TITLE_1_1, 2: uiScriptLocale.TITLE_1_2},
	2: {0: uiScriptLocale.TITLE_2_0, 1: uiScriptLocale.TITLE_2_1, 2: uiScriptLocale.TITLE_2_2},
	3: {0: uiScriptLocale.TITLE_3_0, 1: uiScriptLocale.TITLE_3_1, 2: uiScriptLocale.TITLE_3_2},
	4: {0: uiScriptLocale.TITLE_4_0, 1: uiScriptLocale.TITLE_4_1, 2: uiScriptLocale.TITLE_4_2},
	5: {0: uiScriptLocale.TITLE_5_0, 1: uiScriptLocale.TITLE_5_1, 2: uiScriptLocale.TITLE_5_2},
	6: {0: uiScriptLocale.TITLE_6_0, 1: uiScriptLocale.TITLE_6_1, 2: uiScriptLocale.TITLE_6_2},
}

# Title bonuses for different categories and levels
TITLE_BONUSES = {
	0: {0: uiScriptLocale.TITLE_BONUS_0_0, 1: uiScriptLocale.TITLE_BONUS_0_1, 2: uiScriptLocale.TITLE_BONUS_0_2},
	1: {0: uiScriptLocale.TITLE_BONUS_1_0, 1: uiScriptLocale.TITLE_BONUS_1_1, 2: uiScriptLocale.TITLE_BONUS_1_2},
	2: {0: uiScriptLocale.TITLE_BONUS_2_0, 1: uiScriptLocale.TITLE_BONUS_2_1, 2: uiScriptLocale.TITLE_BONUS_2_2},
	3: {0: uiScriptLocale.TITLE_BONUS_3_0, 1: uiScriptLocale.TITLE_BONUS_3_1, 2: uiScriptLocale.TITLE_BONUS_3_2},
	4: {0: uiScriptLocale.TITLE_BONUS_4_0, 1: uiScriptLocale.TITLE_BONUS_4_1, 2: uiScriptLocale.TITLE_BONUS_4_2},
	5: {0: uiScriptLocale.TITLE_BONUS_5_0, 1: uiScriptLocale.TITLE_BONUS_5_1, 2: uiScriptLocale.TITLE_BONUS_5_2},
	6: {0: uiScriptLocale.TITLE_BONUS_6_0, 1: uiScriptLocale.TITLE_BONUS_6_1, 2: uiScriptLocale.TITLE_BONUS_6_2},
}

# Title IDs mapping
TITLE_IDS = {
	0: {0: 2, 1: 1, 2: 0},
	1: {0: 5, 1: 4, 2: 3},
	2: {0: 8, 1: 7, 2: 6},
	3: {0: 11, 1: 10, 2: 9},
	4: {0: 14, 1: 13, 2: 12},
	5: {0: 17, 1: 16, 2: 15},
	6: {0: 20, 1: 19, 2: 18},
}

# Nazwy indeksowane ID tytulu z serwera (0-20), takie samo mapowanie jak TITLE_IDS:
# id = grupa*3 + ranga, gdzie ranga 0 = I, 1 = II, 2 = III, a w locale slot 0 trzyma
# ranga najwyzsza (III). Stad w kazdej trojce kolejnosc _2, _1, _0 — odwrotnie niz
# numeracja kluczy. Uzywane przez Active() do pokazania aktualnie noszonego tytulu.
TITLE_NAME = [
	uiScriptLocale.TITLE_0_2, uiScriptLocale.TITLE_0_1, uiScriptLocale.TITLE_0_0,
	uiScriptLocale.TITLE_1_2, uiScriptLocale.TITLE_1_1, uiScriptLocale.TITLE_1_0,
	uiScriptLocale.TITLE_2_2, uiScriptLocale.TITLE_2_1, uiScriptLocale.TITLE_2_0,
	uiScriptLocale.TITLE_3_2, uiScriptLocale.TITLE_3_1, uiScriptLocale.TITLE_3_0,
	uiScriptLocale.TITLE_4_2, uiScriptLocale.TITLE_4_1, uiScriptLocale.TITLE_4_0,
	uiScriptLocale.TITLE_5_2, uiScriptLocale.TITLE_5_1, uiScriptLocale.TITLE_5_0,
	uiScriptLocale.TITLE_6_2, uiScriptLocale.TITLE_6_1, uiScriptLocale.TITLE_6_0,
]

# Constants
MAX_RANK_ENTRIES = 11
MAX_CATEGORIES = 6
MAX_TITLE_LEVELS = 3

# Global saved data
savedData = {
	"elements": {"info": {}}
}

def get_week_timestamps():
	"""
	Get the start and end timestamps for the current week.
	
	Returns:
		tuple: (start_timestamp, end_timestamp)
	"""
	now = datetime.now()
	start_of_week = now - timedelta(days=now.weekday())
	start_of_week = start_of_week.replace(hour=0, minute=0, second=0, microsecond=0)
	end_of_week = start_of_week + timedelta(days=6, hours=23, minutes=59, seconds=58)
	start_timestamp = int(time.mktime(start_of_week.timetuple()))
	end_timestamp = int(time.mktime(end_of_week.timetuple()))
	return start_timestamp, end_timestamp

class WeeklyRankWindow(ui.ScriptWindow):
	"""
	Weekly ranking window for displaying player rankings and titles.
	
	This window shows seasonal rankings, allows title selection,
	and displays player statistics.
	"""
	
	def __init__(self):
		"""Initialize the weekly ranking window."""
		ui.ScriptWindow.__init__(self)
		self.__Initialize()
		self.__LoadWindow()
	
	def __del__(self):
		"""Clean up resources when the window is destroyed."""
		self.ClearDictionary()
		ui.ScriptWindow.__del__(self)
	
	def __Initialize(self):
		"""Initialize window variables."""
		self.isLoaded = False
		self.number_page = 0
		self.window_page = 0
		self.previous_arg = 0
		self.previous_arg1 = 0
		self.active_id = -1
		self.select_id = -1
		
		# UI elements
		self.titleBar = None
		self.titleName = None
		self.titleButton = None
		self.TitleWindow = None
		self.RankWindow = None
		self.info_slot_text1 = None
		self.info_slot_text2 = None
		self.character_slot = None
		self.titleaccept_button = None
		self.bonus_text = None
		self.progressbar = None
		self.progress_text = None
		self.faceImage = None
		
		# Data containers
		self.rankDataBackground = None
		self.rankData = None
		self.title_text = {}
		self.title_accept_btn = {}
		self.title_select_bonus_btn = {}
		self.category_btn = {}
		self.box = {}
	
	def Destroy(self):
		"""Destroy the window and clean up resources."""
		self.__Initialize()
		self.Hide()
		self.ClearDictionary()
	
	def Show(self):
		"""Show the weekly ranking window."""
		self.__LoadWindow()
		ui.ScriptWindow.Show(self)
		self.SelectPage(self.number_page)
	
	def Open(self):
		"""Open the weekly ranking window."""
		self.Show()
	
	def Close(self):
		"""Close the weekly ranking window."""
		self.Hide()
	
	def OnPressEscapeKey(self):
		"""Handle escape key press."""
		self.Close()
		return True
	
	def __LoadWindow(self):
		"""Load the window from UI script file."""
		if self.isLoaded:
			return
		
		self.isLoaded = True
		
		try:
			ui.PythonScriptLoader().LoadScriptFile(self, "uiscript/weeklyrank.py")
		except:
			exception.Abort("WeeklyRankWindow.LoadWindow.LoadScript")
		
		try:
			self.__BindObjects()
			self.__BindEvents()
			self.__CreateRankData()
			self.__SetupPlayerInfo()
		except:
			exception.Abort("WeeklyRankWindow.LoadWindow.BindObject")
		
		self.SetCenterPosition()
		self.SetTop()
	
	def __BindObjects(self):
		"""Bind UI objects from the script."""
		self.titleBar = self.GetChild("TitleBar")
		self.titleName = self.GetChild("TitleName")
		self.titleButton = self.GetChild("title_button")
		self.TitleWindow = self.GetChild("title_window")
		self.RankWindow = self.GetChild("rank_window")
		self.info_slot_text1 = self.GetChild("info_slot_text1")
		self.info_slot_text2 = self.GetChild("info_slot_text2")
		self.character_slot = self.GetChild("character_slot_real")
		self.titleaccept_button = self.GetChild("titleaccept_button")
		self.bonus_text = self.GetChild("bonus_text")
		self.progressbar = self.GetChild("progressbar")
		self.progress_text = self.GetChild("progress_text")
		
		# Bind title elements
		for i in range(MAX_TITLE_LEVELS):
			self.title_text[i] = self.GetChild("title{}_text".format(i))
			self.title_accept_btn[i] = self.GetChild("title{}_accept_button".format(i))
			self.title_select_bonus_btn[i] = self.GetChild("title{}_bonus_button".format(i))
		
		# Bind category buttons
		for i in range(MAX_CATEGORIES):
			self.category_btn[i] = self.GetChild("CategoryButton_{}".format(i))
		
		# Bind rank boxes
		for i in range(MAX_RANK_ENTRIES):
			self.box[i] = self.GetChild("box{}".format(i))
	
	def __BindEvents(self):
		"""Bind events to UI elements."""
		self.titleBar.SetCloseEvent(ui.__mem_func__(self.Close))
		self.titleButton.SetEvent(ui.__mem_func__(self.OpenTitlePage))
		self.titleaccept_button.SetEvent(ui.__mem_func__(self.DetachTitle))
		
		# Bind title button events
		for i in range(MAX_TITLE_LEVELS):
			self.title_select_bonus_btn[i].SetEvent(lambda arg=i: self.OnSelectBonusBtn(arg))
			self.title_accept_btn[i].SetEvent(lambda arg=i: self.OnSelectTitle(arg))
		
		# Bind category button events
		for i in range(MAX_CATEGORIES):
			self.category_btn[i].SetEvent(ui.__mem_func__(self.SelectPage), i)
	
	def __CreateRankData(self):
		"""Create rank data containers and UI elements."""
		self.rankDataBackground = {
			"NAME": [],
			"KILL": [],
			"EMPIRE": [],
			"JOB": [],
		}
		
		self.rankData = {
			"NAME": [],
			"KILL": [],
			"EMPIRE": [],
			"JOB": [],
		}
		
		# Create rank data elements
		for i in range(MAX_RANK_ENTRIES):
			self.__CreateRankEntry(i)
	
	def __CreateRankEntry(self, index):
		"""Create a single rank entry UI elements."""
		# Create background bars
		name_bg = self.__CreateBackgroundBar(self.box[index], 82, 1, 114, 16)
		kill_bg = self.__CreateBackgroundBar(self.box[index], 265, 1, 20, 16)
		empire_bg = self.__CreateBackgroundBar(self.box[index], 329, 1, 20, 16)
		job_bg = self.__CreateBackgroundBar(self.box[index], 367, 1, 20, 16)
		
		# Store backgrounds
		self.rankDataBackground["NAME"].append(name_bg)
		self.rankDataBackground["KILL"].append(kill_bg)
		self.rankDataBackground["EMPIRE"].append(empire_bg)
		self.rankDataBackground["JOB"].append(job_bg)
		
		# Create text and image elements
		name_text = ui.MakeTextLine(name_bg)
		kill_text = ui.MakeTextLine(kill_bg)
		empire_text = ui.MakeTextLine(empire_bg)
		job_image = ui.MakeExpandedImageBox(job_bg, 0, 0, 1, 0)
		job_image.SetScale(0.4, 0.4)
		
		# Store data elements
		self.rankData["NAME"].append(name_text)
		self.rankData["KILL"].append(kill_text)
		self.rankData["EMPIRE"].append(empire_text)
		self.rankData["JOB"].append(job_image)
	
	def __CreateBackgroundBar(self, parent, x, y, width, height):
		"""Create a background bar element."""
		bar = ui.Bar("TOP_MOST")
		bar.SetParent(parent)
		bar.SetPosition(x, y)
		bar.SetSize(width, height)
		bar.SetColor(grp.GenerateColor(0.0, 0.0, 0.0, 0.0))
		bar.Show()
		return bar
	
	def __SetupPlayerInfo(self):
		"""Setup player information display."""
		# Set player name
		self.info_slot_text1.SetText(player.GetName())
		self.info_slot_text2.SetText(localeInfo.WEEKLY_RANK_NO_TITLE)
		
		# Create and setup face image
		self.faceImage = ui.ImageBox()
		self.faceImage.SetParent(self.character_slot)
		self.faceImage.SetPosition(4, 4)
		
		race = net.GetMainActorRace()
		if race in FACE_IMAGE_DICT:
			self.faceImage.LoadImage(FACE_IMAGE_DICT[race])
		self.faceImage.Show()
		
		# Setup player rank entry
		self.__SetupPlayerRankEntry()
		
		# Set initial window page
		if self.window_page == 0:
			self.TitleWindow.Hide()
		else:
			self.TitleWindow.Show()
	
	def __SetupPlayerRankEntry(self):
		"""Setup the player's rank entry (index 10)."""
		player_index = 10
		player_empire = net.GetEmpireID()
		
		# Set player name
		self.rankData["NAME"][player_index].SetText(player.GetName())
		
		# Set empire flag
		empire_flag = self.__GetEmpireFlag(player_empire)
		if empire_flag:
			self.rankData["EMPIRE"][player_index].SetText(empire_flag)
		
		# Set job image
		race = net.GetMainActorRace()
		if race in FACE_IMAGE_DICT:
			self.rankData["JOB"][player_index].LoadImage(FACE_IMAGE_DICT[race])
			self.rankData["JOB"][player_index].SetScale(0.4, 0.4)
	
	def __GetEmpireFlag(self, empire_id):
		"""Get empire flag emoji based on empire ID."""
		if empire_id == 1:
			return emoji.AppendEmoji("icon/emoji/flag_shinsoo.png")
		elif empire_id == 3:
			return emoji.AppendEmoji("icon/emoji/flag_jinno.png")
		return ""
	
	def OnSelectBonusBtn(self, arg):
		"""Handle bonus button selection."""
		# Reset all buttons
		for i in range(MAX_TITLE_LEVELS):
			self.title_select_bonus_btn[i].SetUp()
		
		# Set selected button
		self.title_select_bonus_btn[arg].Down()
		self.previous_arg = arg
		
		# Update bonus text
		if self.number_page in TITLE_BONUSES and arg in TITLE_BONUSES[self.number_page]:
			self.bonus_text.SetText(TITLE_BONUSES[self.number_page][arg])
	
	def OnSelectTitle(self, arg):
		"""Handle title selection."""
		# Reset all buttons
		for i in range(MAX_TITLE_LEVELS):
			self.title_accept_btn[i].SetUp()
		
		self.previous_arg1 = arg
		
		# Send title selection to server
		if self.number_page in TITLE_IDS and arg in TITLE_IDS[self.number_page]:
			net.SendSelectTitle(TITLE_IDS[self.number_page][arg])
	
	def Active(self, title_id):
		"""Activate a title."""
		self.active_id = title_id
		if 0 <= title_id < len(TITLE_NAME):
			self.info_slot_text2.SetText(TITLE_NAME[title_id])
	
	def Enable(self, element_id, value):
		"""Enable a title element."""
		if element_id not in savedData["elements"]:
			savedData["elements"][element_id] = []
		
		savedData["elements"][element_id] = [[element_id, value]]
	
	def DetachTitle(self):
		"""Detach the currently active title."""
		if self.active_id != -1:
			net.SendChatPacket("/detach_title {}".format(self.active_id))
	
	def GetActiveNow(self):
		"""Get the currently active title ID."""
		return self.active_id
	
	def OnUpdate(self):
		"""Update the window display."""
		self.__UpdateSeasonProgress()
		self.__UpdateTitleDisplay()
	
	def __UpdateSeasonProgress(self):
		"""Update the season progress bar."""
		start_timestamp, end_timestamp = get_week_timestamps()
		current_timestamp = int(time.time())
		total_week_time = end_timestamp - start_timestamp
		time_left = max(0, end_timestamp - current_timestamp)
		
		# Update progress bar
		self.progressbar.SetPercentage(time_left, total_week_time)
		
		# Calculate time components
		days = time_left // 86400
		hours = (time_left % 86400) // 3600
		minutes = (time_left % 3600) // 60
		
		# Update progress text
		self.progress_text.SetText(
			localeInfo.WEEKLY_RANK_SEASON_END.format(days, hours, minutes)
		)
	
	def __UpdateTitleDisplay(self):
		"""Update title display based on current state."""
		if self.active_id != -1:
			if (self.active_id in savedData["elements"] and 
				len(savedData["elements"][self.active_id]) > 0 and
				savedData["elements"][self.active_id][0][1] == "Hidden"):
				self.info_slot_text2.SetText(localeInfo.WEEKLY_RANK_NO_TITLE)
	
	def PutPage(self, page, season):
		"""Setup page data for a specific category."""
		if page < 0 or page >= MAX_CATEGORIES:
			return
		
		# Update player score
		score_types = [
			player.WEEKLY1, player.WEEKLY2, player.WEEKLY3, player.WEEKLY4,
			player.WEEKLY5, player.WEEKLY6, player.WEEKLY7
		]
		
		if page < len(score_types):
			score = player.GetStatus(score_types[page])
			self.rankData["KILL"][10].SetText(localeInfo.MoneyFormat(int(score)))
		
		# Update page info
		self.number_page = page
		self.category_btn[page].Down()
		self.titleName.SetText(localeInfo.WEEKLY_RANKING_TITLE.format(season + 1))
		
		# Update title texts and buttons
		for i in range(MAX_TITLE_LEVELS):
			if page in TITLE_NAMES and i in TITLE_NAMES[page]:
				self.title_text[i].SetText(TITLE_NAMES[page][i])
			
			self.title_select_bonus_btn[i].SetUp()
		
		# Set selected bonus button
		if self.previous_arg < MAX_TITLE_LEVELS:
			self.title_select_bonus_btn[self.previous_arg].Down()
		
		# Update bonus text
		if page in TITLE_BONUSES and self.previous_arg in TITLE_BONUSES[page]:
			self.bonus_text.SetText(TITLE_BONUSES[page][self.previous_arg])
	
	def LoadPage(self, pos, name, points, empire, job):
		"""Load rank entry data for a specific position."""
		if pos < 0 or pos >= MAX_RANK_ENTRIES:
			return
		
		# Set player name
		self.rankData["NAME"][pos].SetText(name)
		
		# Set points (only if empire is not 0)
		if empire != 0:
			self.rankData["KILL"][pos].SetText(localeInfo.MoneyFormat(points))
		
		# Set empire flag
		empire_flag = self.__GetEmpireFlag(empire)
		self.rankData["EMPIRE"][pos].SetText(empire_flag)
		
		# Set job image
		if empire != 0 and job in FACE_IMAGE_DICT:
			self.rankData["JOB"][pos].LoadImage(FACE_IMAGE_DICT[job])
			self.rankData["JOB"][pos].SetScale(0.4, 0.4)
		
		# Update player's job image
		player_race = net.GetMainActorRace()
		if player_race in FACE_IMAGE_DICT:
			self.rankData["JOB"][10].LoadImage(FACE_IMAGE_DICT[player_race])
			self.rankData["JOB"][10].SetScale(0.4, 0.4)
	
	def SelectPage(self, page_index):
		"""Select a ranking page."""
		if page_index < 0 or page_index >= MAX_CATEGORIES:
			return
		
		# Send page selection to server
		net.SelectWeeklyRankPage(page_index)
		
		# Reset all category buttons
		for i in range(MAX_CATEGORIES):
			self.category_btn[i].SetUp()
	
	def OpenTitlePage(self):
		"""Toggle between rank and title pages."""
		if self.window_page == 0:
			# Switch to title page
			self.window_page = 1
			self.RankWindow.Hide()
			self.TitleWindow.Show()
			
			# Reset title accept buttons
			for i in range(MAX_TITLE_LEVELS):
				self.title_accept_btn[i].SetUp()
		else:
			# Switch to rank page
			self.window_page = 0
			self.TitleWindow.Hide()
			self.RankWindow.Show()
			
			# Show rank data
			for i in range(MAX_RANK_ENTRIES):
				self.rankData["NAME"][i].Show()