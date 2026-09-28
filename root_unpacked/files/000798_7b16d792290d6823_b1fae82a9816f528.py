# coding: latin_1

#author: dracaryS

#dyanmic
import app, player, grp, net, chat, event, item, wndMgr

#static
import ui, _weakref, os, json, operator, constInfo, localeInfo, math

#second
LOG_UPDATE_TIME = 1

BOSS_DROP_COLS = 5
BOSS_DROP_SLOT_SIZE = 32
BOSS_DROP_SLOT_PAD = 4
BOSS_DROP_MARGIN = 15

class BossDropWindow(ui.BoardWithTitleBar):
	def __init__(self):
		ui.BoardWithTitleBar.__init__(self)
		self.tooltipItem = None
		self.itemSlots = []
		self.itemVnums = []
		self.itemCounts = []
		self.dungeonKey = -1

	def __del__(self):
		ui.BoardWithTitleBar.__del__(self)

	def Open(self, dungeonKey, dropCount):
		import dungeonInfo
		self.dungeonKey = dungeonKey
		self.itemVnums = []
		self.itemCounts = []

		for i in range(dropCount):
			vnum = dungeonInfo.GetBossDropItemVnum(dungeonKey, i)
			count = dungeonInfo.GetBossDropItemCount(dungeonKey, i)
			if vnum > 0:
				self.itemVnums.append(vnum)
				self.itemCounts.append(count)

		if not self.itemVnums:
			return

		rows = (len(self.itemVnums) + BOSS_DROP_COLS - 1) // BOSS_DROP_COLS
		width = BOSS_DROP_MARGIN * 2 + BOSS_DROP_COLS * (BOSS_DROP_SLOT_SIZE + BOSS_DROP_SLOT_PAD) - BOSS_DROP_SLOT_PAD
		height = 35 + BOSS_DROP_MARGIN + rows * (BOSS_DROP_SLOT_SIZE + BOSS_DROP_SLOT_PAD) + BOSS_DROP_MARGIN

		self.SetSize(width, height)
		self.SetTitleName(localeInfo.DUNGEON_TRACK_BOSS_DROP if hasattr(localeInfo, 'DUNGEON_TRACK_BOSS_DROP') else "Boss Drop")
		self.SetCloseEvent(ui.__mem_func__(self.Close))
		self.AddFlag("movable")
		self.AddFlag("float")
		self.SetCenterPosition()

		for slot in self.itemSlots:
			slot.Hide()
			del slot
		self.itemSlots = []

		interface = constInfo.GetInterfaceInstance()
		if interface and interface.tooltipItem:
			self.tooltipItem = interface.tooltipItem

		for idx, vnum in enumerate(self.itemVnums):
			col = idx % BOSS_DROP_COLS
			row = idx // BOSS_DROP_COLS
			x = BOSS_DROP_MARGIN + col * (BOSS_DROP_SLOT_SIZE + BOSS_DROP_SLOT_PAD)
			y = 35 + BOSS_DROP_MARGIN + row * (BOSS_DROP_SLOT_SIZE + BOSS_DROP_SLOT_PAD)

			item.SelectItem(vnum)
			iconPath = item.GetIconImageFileName()

			slot = ui.ExpandedImageBox()
			slot.SetParent(self)
			slot.SetPosition(x, y)
			try:
				slot.LoadImage(iconPath)
				imgW = slot.GetWidth()
				imgH = slot.GetHeight()
				if imgW > 0 and imgH > 0 and (imgW != BOSS_DROP_SLOT_SIZE or imgH != BOSS_DROP_SLOT_SIZE):
					slot.SetScale(float(BOSS_DROP_SLOT_SIZE) / imgW, float(BOSS_DROP_SLOT_SIZE) / imgH)
			except:
				pass
			slot.OnMouseOverIn = lambda _idx=idx: self.__OnSlotOverIn(_idx)
			slot.OnMouseOverOut = lambda: self.__OnSlotOverOut()
			slot.Show()
			self.itemSlots.append(slot)

		self.Show()

	def __OnSlotOverIn(self, idx):
		if self.tooltipItem and 0 <= idx < len(self.itemVnums):
			self.tooltipItem.ClearToolTip()
			self.tooltipItem.SetItemToolTip(self.itemVnums[idx])

	def __OnSlotOverOut(self):
		if self.tooltipItem:
			self.tooltipItem.HideToolTip()

	def Close(self):
		self.Hide()

	def OnPressEscapeKey(self):
		self.Close()
		return True

IMG_DIR = "kowal/game/warpwindow/dungeon_info/"
IMG_DIR_WARP = "kowal/game/warpwindow/maps/"

BG_IMG_DIR = IMG_DIR+"bg/"
ICON_IMG_DIR = IMG_DIR+"dungeons/"
BG_IMG_DIR_WARP = IMG_DIR_WARP+"bg/"
# NOTIFICATIONS_IMG_DIR = IMG_DIR+"notifications/"

def IsWarpItems(itemVnum):
	return True if itemVnum == 70058 else False
	
class Edit2(ui.EditLine):
	def __init__(self, parent, text, x, y, width, height):
		ui.EditLine.__init__(self)
		self.imageSlot = ui.ImageBox()
		self.imageSlot.SetParent(parent)
		self.imageSlot.SetPosition(x, y)
		self.imageSlot.LoadImage("kowal/game/warpwindow/maps/search_bg.png")
		self.imageSlot.Show()
		self.SetText(text)
		self.main = text
		self.SetEscapeEvent(self.OnPressEscapeKey)
		self.SetMax(15)
		self.SetUserMax(15)
		self.SetParent(self.imageSlot)
		
		self.SetSize(width, height)
		self.SetPosition(8, 8)
		self.Show()
	
	def OnPressEscapeKey(self):
		# MUSI zwracac False. Silnik (PythonUtils.h PyCallClassMemberFunc) traktuje zwrot
		# rozny od bool (np. None z 'pass') jako "ESC skonsumowane", przez co ESC nie
		# propagowal sie do DungeonTrack.OnPressEscapeKey i okna map/teleportu nie dalo sie
		# zamknac. False pozwala ESC dojsc do okna-rodzica, ktore je zamyka.
		return False
	
	def __del__(self):
		ui.EditLine.__del__(self)

def GetCloneDungeonData(infoDict):
	_dict = {
		"name" : "Unknown Dungeon",
		"image" : "ape_dungeon.png",
		"levelrange" : [0, 0],
		"group" : False,
		"cooldown" : 0,
		"ticket": [],
		"server_shop_idx" : 1,
		"listIndex" : 0,
		"static_listIndex" : 0,
		"showStatus" : True,
		"alarm" : False,
		"server_cooldown": 0,
		"server_completed":0,
		"server_fastest":0,
		"server_damage":0,
		"server_daily_count":0,
		"reset_flag":0,
		"selected":True,
		"whisper_info":False,
		"daily_limit" : 0,
	}
	for key, value in infoDict.items():
		_dict[key] = value
	return _dict

def GetCloneMapData(infoDict):
	_dict = {
		"name" : "Unknown Map",
		"image" : "ape_dungeon.png",
		"mapType" : "low",
		"levelrange" : [0, 0],
		"showStatus" : True,
		"selected":True,
		"bonusType" : 0,
		"elementType" : 0,
		"price" : 0,
	}
	for key, value in infoDict.items():
		_dict[key] = value
	return _dict

mapData = {
	1 : GetCloneMapData({"name" : localeInfo.WARP_WINDOW_MAP_1, "image" : "jinno_1.png", "mapType" : "low", "levelrange" : [1, 999], "bonusType" : localeInfo.WARP_WINDOW_RACE_ANIMALS, "price" : 0}),
	2 : GetCloneMapData({"name" : localeInfo.WARP_WINDOW_MAP_2, "image" : "jinno_2.png", "mapType" : "low", "levelrange" : [1, 999], "bonusType" : localeInfo.WARP_WINDOW_RACE_HUMANS, "elementType" : localeInfo.WARP_WINDOW_ELEM_WIND, "price" : 0}),
	3 : GetCloneMapData({"name" : localeInfo.WARP_WINDOW_MAP_3, "image" : "shinsoo_1.png", "mapType" : "low", "levelrange" : [1, 999], "bonusType" : localeInfo.WARP_WINDOW_RACE_ANIMALS, "price" : 0}),
	4 : GetCloneMapData({"name" : localeInfo.WARP_WINDOW_MAP_4, "image" : "shinsoo_2.png", "mapType" : "low", "levelrange" : [1, 999], "bonusType" : localeInfo.WARP_WINDOW_RACE_HUMANS, "elementType" : localeInfo.WARP_WINDOW_ELEM_WIND, "price" : 0}),
	5 : GetCloneMapData({"name" : localeInfo.WARP_WINDOW_MAP_5, "image" : "jinno_1.png", "mapType" : "low", "levelrange" : [1, 999], "price" : 0}),
	6 : GetCloneMapData({"name" : localeInfo.WARP_WINDOW_MAP_6, "image" : "jinno_2.png", "mapType" : "low", "levelrange" : [1, 999], "bonusType" : localeInfo.WARP_WINDOW_RACE_UNDEAD, "elementType" : localeInfo.WARP_WINDOW_ELEM_ICE, "price" : 0}),
	7 : GetCloneMapData({"name" : localeInfo.WARP_WINDOW_MAP_7, "image" : "orcs.png", "mapType" : "low", "levelrange" : [1, 999], "bonusType" : localeInfo.WARP_WINDOW_ORC, "elementType" : localeInfo.WARP_WINDOW_ELEM_WIND, "price" : 0}),
	9 : GetCloneMapData({"name" : localeInfo.WARP_WINDOW_MAP_9, "image" : "spider_cave.png", "mapType" : "high", "levelrange" : [1, 999], "price" : 0}),
	10 : GetCloneMapData({"name" : localeInfo.WARP_WINDOW_MAP_10, "image" : "map_75.png", "mapType" : "high", "levelrange" : [75, 999], "bonusType" : localeInfo.WARP_WINDOW_ORC, "elementType" : localeInfo.WARP_WINDOW_ELEM_ELEC, "price" : 5000000}),
	11 : GetCloneMapData({"name" : localeInfo.WARP_WINDOW_MAP_11, "image" : "map_100.png", "mapType" : "high", "levelrange" : [100, 125], "bonusType" : localeInfo.WARP_WINDOW_RACE_DEVILS, "price" : 5000000}),
	12 : GetCloneMapData({"name" : localeInfo.WARP_WINDOW_MAP_12, "image" : "map_125.png", "mapType" : "high", "levelrange" : [125, 130], "price" : 5000000}),
	15 : GetCloneMapData({"name" : localeInfo.WARP_WINDOW_MAP_15, "image" : "mining.png", "mapType" : "special", "levelrange" : [1, 999], "price" : 0}),
	16 : GetCloneMapData({"name" : localeInfo.WARP_WINDOW_MAP_16, "image" : "mining.png", "mapType" : "special", "levelrange" : [1, 999], "price" : 0}),
	20 : GetCloneMapData({"name" : localeInfo.WARP_WINDOW_MAP_20, "image" : "spider_cave.png", "mapType" : "high", "levelrange" : [1, 999], "bonusType" : localeInfo.WARP_WINDOW_RACE_DEVILS, "elementType" : localeInfo.WARP_WINDOW_ELEM_ELEC, "price" : 0}),
	21 : GetCloneMapData({"name" : localeInfo.WARP_WINDOW_MAP_21, "image" : "ape_dungeon.png", "mapType" : "high", "levelrange" : [1, 999], "elementType" : localeInfo.WARP_WINDOW_ELEM_EARTH, "price" : 0}),
	22 : GetCloneMapData({"name" : localeInfo.WARP_WINDOW_MAP_22, "image" : "ape_dungeon.png", "mapType" : "high", "levelrange" : [1, 999], "bonusType" : localeInfo.WARP_WINDOW_RACE_MILGYO, "elementType" : localeInfo.WARP_WINDOW_ELEM_WIND, "price" : 0}),
	25 : GetCloneMapData({"name" : localeInfo.WARP_WINDOW_MAP_25, "image" : "jinno_2.png", "mapType" : "high", "levelrange" : [1, 999], "elementType" : localeInfo.WARP_WINDOW_ELEM_EARTH, "price" : 0}),
	26 : GetCloneMapData({"name" : localeInfo.WARP_WINDOW_MAP_26, "image" : "map_100.png", "mapType" : "high", "levelrange" : [1, 999], "elementType" : localeInfo.WARP_WINDOW_ELEM_FIRE, "price" : 0}),
	27 : GetCloneMapData({"name" : localeInfo.WARP_WINDOW_MAP_27, "image" : "map_100.png", "mapType" : "low", "levelrange" : [1, 999], "price" : 0}),
}

dungeonData = {
	17 : GetCloneDungeonData({
		"name" : localeInfo.DUNGEON_TRACK_DUNGEON_1 if hasattr(localeInfo, 'DUNGEON_TRACK_DUNGEON_1') else "Spider Queen's Lair",
		"image" : "ape_dungeon.png",
		"levelrange" : [50, 85],
		"group" : False,
		"cooldown" : 0,
		"ticket": [[200040, 1]],
		"server_shop_idx" : 1,
		"listIndex" : 0,
		"static_listIndex" : 0,
		"daily_limit" : 80,
	}),
	21 : GetCloneDungeonData({
		"name" : localeInfo.DUNGEON_TRACK_DUNGEON_2 if hasattr(localeInfo, 'DUNGEON_TRACK_DUNGEON_2') else "Demon Tower",
		"image" : "reaper_dungeon.png",
		"levelrange" : [75, 110],
		"group" : False,
		"cooldown" : 0,
		"ticket": [[200040, 1]],
		"server_shop_idx" : 1,
		"listIndex" : 1,
		"static_listIndex" : 1,
		"daily_limit" : 80,
	}),
	300 : GetCloneDungeonData({
		"name" : localeInfo.DUNGEON_TRACK_DUNGEON_3 if hasattr(localeInfo, 'DUNGEON_TRACK_DUNGEON_3') else "Wukong Temple",
		"image" : "sanctum_dungeon.png",
		"levelrange" : [75, 110],
		"group" : False,
		"cooldown" : 0,
		"ticket": [[200041, 1]],
		"server_shop_idx" : 1,
		"listIndex" : 2,
		"static_listIndex" : 2,
		"daily_limit" : 80,
	}),
	14 : GetCloneDungeonData({
		"name" : localeInfo.DUNGEON_TRACK_DUNGEON_4 if hasattr(localeInfo, 'DUNGEON_TRACK_DUNGEON_4') else "Scorpion Dungeon",
		"image" : "hwang_dungeon.png",
		"levelrange" : [100, 149],
		"group" : False,
		"cooldown" : 0,
		"ticket": [[200042, 1]],
		"server_shop_idx" : 1,
		"listIndex" : 3,
		"static_listIndex" : 3,
		"daily_limit" : 80,
	}),
	16 : GetCloneDungeonData({
		"name" : localeInfo.DUNGEON_TRACK_DUNGEON_5 if hasattr(localeInfo, 'DUNGEON_TRACK_DUNGEON_5') else "Arctic Dungeon",
		"image" : "dragon_dungeon.png",
		"levelrange" : [125, 200],
		"group" : False,
		"cooldown" : 0,
		"ticket": [[200043, 1]],
		"server_shop_idx" : 1,
		"listIndex" : 4,
		"static_listIndex" : 4,
		"daily_limit" : 80,
	}),
	18 : GetCloneDungeonData({
		"name" : localeInfo.DUNGEON_TRACK_DUNGEON_6 if hasattr(localeInfo, 'DUNGEON_TRACK_DUNGEON_6') else "Hell's Gate",
		"image" : "water_dungeon.png",
		"levelrange" : [150, 206],
		"group" : False,
		"cooldown" : 0,
		"ticket": [[200044, 1]],
		"server_shop_idx" : 1,
		"listIndex" : 5,
		"static_listIndex" : 5,
		"daily_limit" : 80,
	}),
	12 : GetCloneDungeonData({
		"name" : localeInfo.DUNGEON_TRACK_DUNGEON_7 if hasattr(localeInfo, 'DUNGEON_TRACK_DUNGEON_7') else "Sanctuary",
		"image" : "hellforge_dungeon.png",
		"levelrange" : [175, 206],
		"group" : False,
		"cooldown" : 0,
		"ticket": [[200045, 1]],
		"server_shop_idx" : 1,
		"listIndex" : 6,
		"static_listIndex" : 6,
		"daily_limit" : 80,
	}),
	15 : GetCloneDungeonData({
		"name" : localeInfo.DUNGEON_TRACK_DUNGEON_8 if hasattr(localeInfo, 'DUNGEON_TRACK_DUNGEON_8') else "Ghost Dungeon",
		"image" : "spider_dungeon.png",
		"levelrange" : [149, 149],
		"group" : True,
		"cooldown" : 0,
		"ticket": [[200046, 2]],
		"server_shop_idx" : 1,
		"listIndex" : 7,
		"static_listIndex" : 7,
		"daily_limit" : 80,
	}),
	24 : GetCloneDungeonData({
		"name" : localeInfo.DUNGEON_TRACK_DUNGEON_9 if hasattr(localeInfo, 'DUNGEON_TRACK_DUNGEON_9') else "Ghost Dungeon II",
		"image" : "crimson_dungeon.png",
		"levelrange" : [200, 200],
		"group" : True,
		"cooldown" : 0,
		"ticket": [[200047, 2]],
		"server_shop_idx" : 1,
		"listIndex" : 8,
		"static_listIndex" : 8,
		"daily_limit" : 80,
	}),
	101 : GetCloneDungeonData({
		"name" : localeInfo.DUNGEON_TRACK_DUNGEON_10 if hasattr(localeInfo, 'DUNGEON_TRACK_DUNGEON_10') else "Desert Canyon",
		"image" : "orc_dungeon.png",
		"levelrange" : [201, 210],
		"group" : False,
		"cooldown" : 0,
		"ticket": [[200048, 1]],
		"server_shop_idx" : 1,
		"listIndex" : 9,
		"static_listIndex" : 9,
		"daily_limit" : 80,
	}),
	91 : GetCloneDungeonData({
		"name" : localeInfo.DUNGEON_TRACK_DUNGEON_11 if hasattr(localeInfo, 'DUNGEON_TRACK_DUNGEON_11') else "Wieza Orkow",
		"image" : "orc_dungeon.png",
		"levelrange" : [30, 65],
		"group" : False,
		"cooldown" : 0,
		"ticket": [[50070, 1]],
		"server_shop_idx" : 1,
		"listIndex" : 10,
		"static_listIndex" : 10,
		"daily_limit" : 80,
	}),
	92 : GetCloneDungeonData({
		"name" : localeInfo.DUNGEON_TRACK_DUNGEON_12 if hasattr(localeInfo, 'DUNGEON_TRACK_DUNGEON_12') else "Kryjowka Baronowej",
		"image" : "spider_dungeon.png",
		"levelrange" : [61, 80],
		"group" : False,
		"cooldown" : 0,
		"ticket": [[70700, 1]],
		"server_shop_idx" : 1,
		"listIndex" : 11,
		"static_listIndex" : 11,
		"daily_limit" : 80,
	}),
}

_activeLogWindow = None

def SetActiveLogWindow(wnd):
	global _activeLogWindow
	_activeLogWindow = wnd

def OnRankingRefresh():
	global _activeLogWindow
	if _activeLogWindow:
		_activeLogWindow.OnServerRankingData()

def UpdateDailyCount(mapIdx, count):
	global dungeonData
	if mapIdx in dungeonData:
		dungeonData[mapIdx]["server_daily_count"] = count

def SyncDungeonDataFromServer():
	try:
		import dungeonInfo
		count = dungeonInfo.GetCount()
		if count == 0:
			return
		global dungeonData
		for key in range(count):
			mapIdx = dungeonInfo.GetMapIndex(key)
			if mapIdx in dungeonData:
				dungeonData[mapIdx]["server_completed"] = dungeonInfo.GetFinish(key)
				dungeonData[mapIdx]["server_fastest"] = dungeonInfo.GetFinishTime(key)
				dungeonData[mapIdx]["server_damage"] = dungeonInfo.GetFinishDamage(key)
	except:
		pass

class DungeonManager(ui.Window):
	def __init__(self):
		ui.Window.__init__(self)
		self.Destroy()
	def Destroy(self):
		self.__children={}
	def AddDungeon(self, dungeonBossIdx):
		global dungeonData
		if not dungeonBossIdx in dungeonData:
			return

	def __Click(self, emptyArg, mobIdx):
		if mobIdx in self.__children:
			leftTime = self.__children[mobIdx].leftTime - app.GetTime()
			self.__children[mobIdx].leftTime = app.GetTime() + (leftTime if leftTime < 1.0 else 1.0)

	def SortWithIndex(self, child):
		return child[1]

	def OnUpdate(self):
		global dungeonData
		(needRemoveList, imageList, now) = ([], [], app.GetTime())
		for key, image in self.__children.items():
			if image.leftTime < now:
				needRemoveList.append(key)
			else:
				imageList.append([key, dungeonData[key]["static_listIndex"], image])

		for mobIdx in needRemoveList:
			self.__children[mobIdx].text = None
			self.__children[mobIdx].Hide()
			del self.__children[mobIdx]

		if len(imageList):
			imageList.sort(key=ui.__mem_func__(self.SortWithIndex))
			xPos, yPos = (wndMgr.GetScreenWidth() / 2) - (119 / 2), 0
			self.SetPosition(xPos, 100)

			for imageListInfo in imageList:
				image = imageListInfo[2]
				image.SetPosition(0, yPos)
				yPos += image.GetHeight() + 4
				leftTime = image.leftTime - now
				if leftTime < 1.0:
					image.SetAlpha(leftTime)
				image.text.Show()
				image.Show()
			self.SetSize(119, yPos)
			self.Show()
		else:
			self.Hide()

class DungeonTrack(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.currentPage = 0
		self.currentMapCategory = "low"
		self.searchText = ""
		self.__LoadWindow()

	def __LoadWindow(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "UIScript/dungeonwindow.py")
		except:
			import exception
			exception.Abort("DungeonTrack.__LoadWindow")

		try:
			self.GetChild("titlebar").SetCloseEvent(ui.__mem_func__(self.Close))
			self.GetChild("clear_btn").SetEvent(ui.__mem_func__(self.__ClearBtn))
			
			self.dungeonPage = self.GetChild("dungeon_page")
			self.listWindow = self.GetChild("list_window")
			self.scrollBar = self.GetChild("scrollbar")
			self.scrollBar.SetScrollEvent(ui.__mem_func__(self.__OnScroll))
			self.listWindow.OnMouseWheel = ui.__mem_func__(self.OnMouseWheel)
			self.listWindow.SetInsideRender(True)
			
			self.rightBG = self.GetChild("right_bg")
			self.titleText = self.GetChild("title")
			self.levelInfo = self.GetChild("level_info")
			self.levelText = self.GetChild("level_text")
			self.cooldownInfo = self.GetChild("cooldown_info")
			self.cooldownText = self.GetChild("cooldown_text")
			self.dailyLimitInfo = self.GetChild("daily_limit_info")
			self.dailyLimitText = self.GetChild("daily_limit_text")
			
			self.ticketSlot = self.GetChild("ticket_slot")
			self.ticketInfo = self.GetChild("ticket_info")
			self.shopBtn = self.GetChild("shop_btn")
			self.shopBtn.SetEvent(ui.__mem_func__(self.__ShopBtn))
			
			self.checkBox = self.GetChild("checkbox")
			self.checkBox.SetEvent(ui.__mem_func__(self.__ClickCheckBox))
			self.checkInfo = self.GetChild("check_info")
			
			self.personalInfo = self.GetChild("personal_info")
			
			self.completedRank = self.GetChild("completed_rank")
			self.completedRank.SAFE_SetEvent(self.__ClickRank, 0)
			self.completedInfo = self.GetChild("completed_info")
			self.completedText = self.GetChild("completed_text")
			
			self.fastRank = self.GetChild("fast_rank")
			self.fastRank.SAFE_SetEvent(self.__ClickRank, 1)
			self.fastInfo = self.GetChild("fast_info")
			self.fastText = self.GetChild("fast_text")
			
			self.damageRank = self.GetChild("damage_rank")
			self.damageRank.SAFE_SetEvent(self.__ClickRank, 2)
			self.damageInfo = self.GetChild("damage_info")
			self.damageText = self.GetChild("damage_text")
			
			self.enterBtn = self.GetChild("enter_btn")
			self.enterBtn.SAFE_SetEvent(self.__ClickQuest, "enter")
			
			self.wikiBtn = self.GetChild("wiki_btn")
			self.wikiBtn.SetEvent(ui.__mem_func__(self.__WikiBtn))
			
			self.mapPage = self.GetChild("map_page")
			self.mapListWindow = self.GetChild("map_list_window")
			self.mapListWindow.OnMouseWheel = ui.__mem_func__(self.OnMouseWheel)
			self.mapListWindow.SetInsideRender(True)
			self.mapScrollBar = self.GetChild("map_scrollbar")
			self.mapScrollBar.SetScrollEvent(ui.__mem_func__(self.__OnScroll))
			self.mapRightBG = self.GetChild("map_right_bg")
			
			self.lowMapsBtn = self.GetChild("low_maps_btn")
			self.lowMapsBtn.SetEvent(ui.__mem_func__(self.__FilterMapsByCategory), "low")
			
			self.highMapsBtn = self.GetChild("high_maps_btn")
			self.highMapsBtn.SetEvent(ui.__mem_func__(self.__FilterMapsByCategory), "high")
			
			self.specialMapsBtn = self.GetChild("special_maps_btn")
			self.specialMapsBtn.SetEvent(ui.__mem_func__(self.__FilterMapsByCategory), "special")
			
			searchContainer = self.GetChild("SearchFieldContainer")
			self.searchTextEdit = Edit2(searchContainer, "", 0, 0, 120, 25)
			self.searchTextEdit.OnIMEUpdate = ui.__mem_func__(self.__OnValueUpdate)
			
			self.searchTextCover = ui.MakeTextLine(self.searchTextEdit)
			self.searchTextCover.SetPosition(-24, -7)
			self.searchTextCover.SetText(localeInfo.WARP_WINDOW_SEARCH_MAPS)
			self.searchTextCover.SetPackedFontColor(0xFF535353)
			
		except:
			import exception
			exception.Abort("DungeonTrack.__LoadWindow.BindObject")
		
		self.dungeonBtnDict = {}
		global dungeonData
		for mobIdx, dataDict in dungeonData.items():
			btn = Dungeon(mobIdx, self)
			btn.SetParent(self.listWindow)
			btn.OnMouseWheel = ui.__mem_func__(self.OnMouseWheel)
			btn.SetEvent(ui.__mem_func__(self.__ClickDungeon), "mouse_click", mobIdx)
			btn.Show()
			self.dungeonBtnDict[str(mobIdx)+"btn"] = btn

		self.mapBtnDict = {}
		global mapData
		for mobIdx, dataDict in mapData.items():
			btnMap = Map(mobIdx, self)
			btnMap.SetParent(self.mapListWindow)
			btnMap.OnMouseWheel = ui.__mem_func__(self.OnMouseWheel)
			btnMap.SetEvent(ui.__mem_func__(self.__ClickMap), "mouse_click", mobIdx)
			btnMap.Show()
			self.mapBtnDict[str(mobIdx)+"btnMap"] = btnMap

		self.ticketImageList = []
		self.logManager = None
		self.lastShopBtnClick = 0
		
		self.SetCenterPosition()
		LoadSettings()
		self.__ShowDungeonPage()
		self.mapPage.Hide() 
		self.Refresh()

	def __ShowDungeonPage(self):
		if self.currentPage == 0:
			return
		self.currentPage = 0
		self.dungeonPage.Show()
		self.mapPage.Hide()
		self.Refresh()
	
	def __ShowMapPage(self):
		if self.currentPage == 1:
			return
		self.currentPage = 1
		self.dungeonPage.Hide()
		self.mapPage.Show()
		self.Refresh()

	def GetCurrentSelectedDungeon(self):
		global dungeonData
		for mobIdx, dungeonInfo in dungeonData.items():
			if dungeonInfo["selected"]:
				return mobIdx
		return -1

	def LoadServerData(self, mobIdx, rankIdx, cmd):
		if self.logManager:
			self.logManager.LoadServerData(int(mobIdx), int(rankIdx), cmd)
	
	def __ClickRank(self, rankIdx):
		if not self.logManager:
			self.logManager = LogWindow()
		self.logManager.Open(self.GetCurrentSelectedDungeon(), rankIdx)

	def __ClickQuest(self, questMode):
		currentDungeon = self.GetCurrentSelectedDungeon()
		if currentDungeon == -1:
			return
		if questMode == "warp" or questMode == "enter":
			try:
				import dungeonInfo
				for key in range(dungeonInfo.GetCount()):
					if dungeonInfo.GetMapIndex(key) == currentDungeon:
						dungeonInfo.Warp(key)
						break
			except:
				chat.AppendChat(chat.CHAT_TYPE_INFO, "Dungeon unavailable.")
		self.Close()
		
	def __FilterMapsByCategory(self, category):
		self.currentMapCategory = category
		self.Refresh()

	def __OnValueUpdate(self):
		ui.EditLine.OnIMEUpdate(self.searchTextEdit)
		import uiScriptLocale
		val = uiScriptLocale.RemoveDiacritic(self.searchTextEdit.GetText())
		
		if len(val) <= 0:
			self.searchTextCover.Show()
			self.searchText = ""
			self.Refresh()
		else:
			self.searchTextCover.Hide()
			self.searchText = val
			self.Refresh()

	def __ShopBtn(self):
		currentDungeon = self.GetCurrentSelectedDungeon()
		if currentDungeon != -1:
			if self.lastShopBtnClick > app.GetGlobalTimeStamp():
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.DUNGEON_TRACK_SLOW_INFO)
				return
			self.lastShopBtnClick = app.GetGlobalTimeStamp() + 2
			global dungeonData
			tickets = dungeonData[currentDungeon].get("ticket", [])
			if not tickets:
				return
			ticketVnum = tickets[0][0]
			item.SelectItem(ticketVnum)
			ticketName = item.GetItemName()
			if not ticketName:
				return
			interface = constInfo.GetInterfaceInstance()
			if not interface:
				return
			searchWnd = interface.GetShopSearchWindow()
			if not searchWnd:
				return
			searchWnd.Show(True)
			searchWnd.SetTop()
			if hasattr(searchWnd, 'sItemName'):
				searchWnd.sItemName.SetText(ticketName)
			searchWnd.OnSearch()

	def __WikiBtn(self):
		currentDungeon = self.GetCurrentSelectedDungeon()
		if currentDungeon == -1:
			return

		import dungeonInfo
		dungeonKey = -1
		for key in range(dungeonInfo.GetCount()):
			if dungeonInfo.GetMapIndex(key) == currentDungeon:
				dungeonKey = key
				break

		if dungeonKey == -1:
			return

		dropCount = dungeonInfo.GetBossDropCount(dungeonKey)
		if dropCount <= 0:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.DUNGEON_TRACK_NO_DROP if hasattr(localeInfo, 'DUNGEON_TRACK_NO_DROP') else "No boss drop info available.")
			return

		if not hasattr(self, 'bossDropWindow') or not self.bossDropWindow:
			self.bossDropWindow = BossDropWindow()
		self.bossDropWindow.Open(dungeonKey, dropCount)
		self.bossDropWindow.SetTop()

	def __ClickCheckBox(self):
		currentDungeon = self.GetCurrentSelectedDungeon()
		if currentDungeon != -1:
			global dungeonData
			dungeonData[currentDungeon]["alarm"] = not dungeonData[currentDungeon]["alarm"]
			self.Refresh(False, False, True)

	def __ClickDungeon(self, emptyArg, mobIdx):
		global dungeonData
		for key, dungeonInfo in dungeonData.items():
			dungeonInfo["selected"] = False
		if mobIdx in dungeonData:
			dungeonData[mobIdx]["selected"] = True
		self.Refresh()
		SaveSettings()

	def __ClickMap(self, emptyArg, mobIdx):
		global mapData
		for key, mapInfo in mapData.items():
			mapInfo["selected"] = False
		if mobIdx in mapData:
			mapData[mobIdx]["selected"] = True
			net.SendChatPacket("/teleport {}".format(mobIdx))
			self.Hide()
		self.Refresh()

	def __OnScroll(self):
		self.Refresh(False, False, False)

	def __ClearBtn(self):
		ClearSettings()
		self.Refresh(True)

	def SortWithIndex(self, child):
		return child.GetIndex()

	def OnMouseWheel(self, length):
		if self.currentPage == 0:
			self.scrollBar.OnMouseWheel(length)
		else:
			self.mapScrollBar.OnMouseWheel(length)
		return True

	def Refresh(self, resetPos = False, refreshItems = True, refreshRightTable = True):
		btnList = []
		btnListMap = []
		for key, dungeonBtn in self.dungeonBtnDict.items():
			dungeonBtn.Refresh()
			if dungeonBtn.GetShowStatus():
				dungeonBtn.Show()
				btnList.append(dungeonBtn)
			else:
				dungeonBtn.Hide()
				
		for key, mapBtn in self.mapBtnDict.items():
			mapBtn.Refresh()
			# Filter by category and search text
			global mapData
			mapIdx = int(key.replace("btnMap", ""))
			if mapIdx in mapData:
				# If search is active, ignore category filter
				if self.searchText:
					matchesSearch = mapBtn.MatchesSearch(self.searchText)
					if matchesSearch and mapBtn.GetShowStatus():
						mapBtn.Show()
						btnListMap.append(mapBtn)
					else:
						mapBtn.Hide()
				else:
					# Only apply category filter when no search text
					matchesCategory = mapData[mapIdx]["mapType"] == self.currentMapCategory
					if matchesCategory and mapBtn.GetShowStatus():
						mapBtn.Show()
						btnListMap.append(mapBtn)
					else:
						mapBtn.Hide()
			else:
				mapBtn.Hide()
		
		btnList.sort(key=ui.__mem_func__(self.SortWithIndex))
		#btnListMap.sort(key=ui.__mem_func__(self.SortWithIndex))
		
		if resetPos:
			self.scrollBar.SetPos(0)
			self.mapScrollBar.SetPos(0)
		
		if len(btnList):
			totalHeight = len(btnList) * (60)
			if totalHeight > 0:
				totalHeight -= 7
			
			windowHeight = 434
			
			if totalHeight > windowHeight:
				self.scrollBar.SetContentHeight(totalHeight)
				pos = self.scrollBar.GetPos()
				basePos = int(pos * (totalHeight - windowHeight))
			else:
				self.scrollBar.SetContentHeight(windowHeight)
				basePos = 0
			
			yPos = 0
			for child in btnList:
				child.SetPosition(0, yPos - basePos)
				yPos += child.GetHeight()
		else:
			self.scrollBar.SetContentHeight(434)
		
		if len(btnListMap):
			btnListMap.sort(key=lambda x: x.GetMinLevel())
			totalHeight = len(btnListMap) * (60)
			if totalHeight > 0:
				totalHeight -= 7

			windowHeight = 400

			if totalHeight > windowHeight:
				self.mapScrollBar.SetContentHeight(totalHeight)
				pos = self.mapScrollBar.GetPos()
				basePos = int(pos * (totalHeight - windowHeight))
			else:
				self.mapScrollBar.SetContentHeight(windowHeight)
				basePos = 0

			yPos = 0
			for child in btnListMap:
				itemY = yPos - basePos
				itemH = child.GetHeight()
				child.SetPosition(0, itemY)
				if itemY + itemH <= 0 or itemY >= windowHeight:
					child.Hide()
				else:
					child.Show()
					child.UpdateTextVisibility(itemY, windowHeight)
				yPos += itemH
		else:
			self.mapScrollBar.SetContentHeight(400)
			
		
		if refreshRightTable:
			currentDungeon = self.GetCurrentSelectedDungeon()
			if currentDungeon != -1:
				global dungeonData
				dungeonInfo = dungeonData[currentDungeon]
				self.titleText.SetText(dungeonInfo["name"])
				self.levelText.SetText(str(dungeonInfo["levelrange"][0]) + " - " + str(dungeonInfo["levelrange"][1]))
				self.cooldownText.SetText(FormatTimeEx(dungeonInfo["cooldown"]))
				dailyCount = dungeonInfo["server_daily_count"]
				dailyLimit = dungeonInfo["daily_limit"]
				resetFlag  = dungeonInfo.get("reset_flag", 0)
				if resetFlag > 0:
					timeLeft = max(0, resetFlag - app.GetGlobalTimeStamp())
					self.dailyLimitText.SetText(FormatTimeEx(timeLeft))
				else:
					self.dailyLimitText.SetText(str(dailyCount) + " / " + str(dailyLimit))
				self.completedText.SetText(NumberToDecimalString(dungeonInfo["server_completed"]))
				self.fastText.SetText(FormatTimeEx(dungeonInfo["server_fastest"]))
				self.damageText.SetText(NumberToDecimalString(dungeonInfo["server_damage"]))

				checkImg = IMG_DIR+"checkbox_empty.png" if not dungeonInfo["alarm"] else IMG_DIR+"checkbox_checked.png"
				self.checkBox.SetUpVisual(checkImg)
				self.checkBox.SetOverVisual(checkImg)
				self.checkBox.SetDownVisual(checkImg)

				for img in self.ticketImageList:
					img.Hide()
				self.ticketImageList = []

				ticketItemList = dungeonInfo["ticket"]
				if len(ticketItemList) > 0:
					self.ticketSlot.Show()
					self.shopBtn.Show()
					for j in range(len(ticketItemList)):
						item.SelectItem(ticketItemList[j][0])
						xCalculate = 163 - (((len(ticketItemList) - 1) - j) * 37)

						itemIcon = ui.ExpandedImageBox()
						itemIcon.SetParent(self.rightBG)
						itemIcon.SetPosition(xCalculate-82, 96+85)
						itemIcon.LoadImage(item.GetIconImageFileName())
						vnum = ticketItemList[j][0]
						itemIcon.OnMouseOverIn = lambda s=self, v=vnum: s.__OverInItem(v)
						itemIcon.OnMouseOverOut = lambda s=self: s.__OverOutItem()
						itemIcon.Show()
						self.ticketImageList.append(itemIcon)

						if ticketItemList[j][1] > 1:
							itemCountText = ui.TextLine()
							itemCountText.SetParent(self.rightBG)
							itemCountText.SetPosition(xCalculate-82+22, 96+85+22)
							itemCountText.SetText(str(ticketItemList[j][1]))
							itemCountText.SetOutline()
							itemCountText.Show()
							self.ticketImageList.append(itemCountText)
				else:
					self.ticketSlot.Hide()
					self.shopBtn.Hide()

	def __OverOutItem(self):
		interface = constInfo.GetInterfaceInstance()
		if interface and interface.tooltipItem:
			interface.tooltipItem.HideToolTip()

	def __OverInItem(self, itemIdx):
		interface = constInfo.GetInterfaceInstance()
		if interface and interface.tooltipItem:
			interface.tooltipItem.ClearToolTip()
			interface.tooltipItem.SetItemToolTip(int(itemIdx))

	def OnUpdate(self):
		for key, dungeonBtn in self.dungeonBtnDict.items():
			dungeonBtn.OnUpdate()

		currentDungeon = self.GetCurrentSelectedDungeon()
		if currentDungeon != -1:
			global dungeonData
			dungeonInfo = dungeonData[currentDungeon]
			resetFlag = dungeonInfo.get("reset_flag", 0)
			if resetFlag > 0:
				timeLeft = max(0, resetFlag - app.GetGlobalTimeStamp())
				self.dailyLimitText.SetText(FormatTimeEx(timeLeft))

	def Open(self):
		try:
			import dungeonInfo
			dungeonInfo.Open()
		except:
			pass
		self.Refresh()
		self.Show()
		self.SetTop()

	def OpenOnMapPage(self):
		try:
			import dungeonInfo
			dungeonInfo.Open()
		except:
			pass
		self.__ShowMapPage()
		self.Refresh()
		self.Show()
		self.SetTop()

	def OpenOnDungeonPage(self):
		try:
			import dungeonInfo
			dungeonInfo.Open()
		except:
			pass
		self.__ShowDungeonPage()
		self.Refresh()
		self.Show()
		self.SetTop()

	def Close(self):
		self.Hide()

	def OnPressEscapeKey(self):
		self.Close()
		return True

	def Destroy(self):
		if self.logManager:
			self.logManager.Close()
			self.logManager.Destroy()
			self.logManager = None
		
		for img in self.ticketImageList:
			img.Hide()
		self.ticketImageList = []
		
		self.dungeonBtnDict = {}
		self.mapBtnDict = {}

class Dungeon(ui.ExpandedImageBox):
	def Destroy(self):
		self.__children={}
	def __init__(self, mobIdx, parent):
		ui.ExpandedImageBox.__init__(self)
		self.__Load(mobIdx, parent)
	
	def GetShowStatus(self):
		global dungeonData
		return dungeonData[self.__children["mobIdx"]]["showStatus"]

	def GetIndex(self):
		global dungeonData
		return dungeonData[self.__children["mobIdx"]]["listIndex"]

	def __Load(self, mobIdx, parent):
		self.Destroy()
		self.__children["mobIdx"] = mobIdx
		self.__children["parent"] = _weakref.proxy(parent)

		global dungeonData
		data = dungeonData[mobIdx]

		self.__children["name"] = CreateWindow(ui.TextLine(), self, (60, 17), data["name"])
		self.__children["name"].SetFontName("Verdana:12b")
		self.__children["name"].SetOutline()
		self.__children["name"].SetPackedFontColor(0xFFe4cbac)
		self.__children["image"] = CreateWindow(ui.ExpandedImageBox(), self, (-24, 0), ICON_IMG_DIR+data["image"])
		self.__children["image"].AddFlag("not_pick")
		self.__children["status"] = CreateWindow(ui.TextLine(), self, (253, 10), "", "horizontal:right")
		self.__children["time"] = CreateWindow(ui.TextLine(), self, (60, 30), "")
		self.__children["time"].SetOutline()
		
		self.__children["level_text_header"] = CreateWindow(ui.TextLine(), self, (16, 17), localeInfo.DUNGEON_TRACK_LV, "horizontal:center")
		self.__children["level_text_header"].SetOutline()
		self.__children["level_text_header"].SetPackedFontColor(0xFFe4cbac)
		self.__children["level_text"] = CreateWindow(ui.TextLine(), self, (16, 29), str(data["levelrange"][0]), "horizontal:center")
		self.__children["level_text"].SetFontName("Verdana:12b")
		self.__children["level_text"].SetOutline()
		self.__children["level_text"].SetPackedFontColor(0xFFe4cbac)

		backBtn = CreateWindow(ui.Button(), self, (331, 6))
		backBtn.SetWindowName("not_render")
		backBtn.SetUpVisual(IMG_DIR+"up_0.png")
		backBtn.SetOverVisual(IMG_DIR+"up_1.png")
		backBtn.SetDownVisual(IMG_DIR+"up_2.png")
		backBtn.SetEvent(ui.__mem_func__(self.__BackBtn))
		backBtn.SetToolTipText(localeInfo.DUNGEON_TRACK_MOVE_UP)
		self.__children["backBtn"] = backBtn

		nextBtn = CreateWindow(ui.Button(), self, (331, 38))
		nextBtn.SetWindowName("not_render")
		nextBtn.SetUpVisual(IMG_DIR+"down_0.png")
		nextBtn.SetOverVisual(IMG_DIR+"down_1.png")
		nextBtn.SetDownVisual(IMG_DIR+"down_2.png")
		nextBtn.SetEvent(ui.__mem_func__(self.__NextBtn))
		nextBtn.SetToolTipText(localeInfo.DUNGEON_TRACK_MOVE_DOWN)
		self.__children["nextBtn"] = nextBtn

		eyeBtn = CreateWindow(ui.Button(), self, (330, 23))
		eyeBtn.SetUpVisual(IMG_DIR+"btn_hide_1.png")
		eyeBtn.SetOverVisual(IMG_DIR+"btn_hide_2.png")
		eyeBtn.SetDownVisual(IMG_DIR+"btn_hide_3.png")
		eyeBtn.SetEvent(ui.__mem_func__(self.__ShowBtn))
		eyeBtn.SetToolTipText(localeInfo.DUNGEON_TRACK_HIDE)
		self.__children["eyeBtn"] = eyeBtn

	def SortWithIndex(self, child):
		return child[1]
		
	def FindIndexInList(self, idx, goingType):
		global dungeonData
		btnList = []
		for mobIdx, dungeonDict in dungeonData.items():
			if not dungeonDict["showStatus"]:
				continue
			btnList.append([mobIdx, dungeonDict["listIndex"]])
		btnList.sort(key=ui.__mem_func__(self.SortWithIndex), reverse=not goingType)
		for child in btnList:
			if goingType:
				if child[1] >= idx:
					return child
			else:
				if child[1] <= idx:
					return child
		return -1

	def __BackBtn(self):
		global dungeonData
		listIdx = dungeonData[self.__children["mobIdx"]]["listIndex"]
		if listIdx <= 0:
			return
		destIndex = self.FindIndexInList(listIdx-1, False)
		if destIndex != -1:
			dungeonData[destIndex[0]]["listIndex"] = listIdx
			dungeonData[self.__children["mobIdx"]]["listIndex"] = destIndex[1]
		else:
			dungeonData[self.__children["mobIdx"]]["listIndex"] -= 1
		self.__children["parent"].Refresh(False, True, False)
		SaveSettings()

	def __NextBtn(self):
		global dungeonData
		listIdx = dungeonData[self.__children["mobIdx"]]["listIndex"]
		if listIdx >= len(dungeonData)-1:
			return
		destIndex = self.FindIndexInList(listIdx+1, True)
		if destIndex != -1:
			dungeonData[destIndex[0]]["listIndex"] = listIdx
			dungeonData[self.__children["mobIdx"]]["listIndex"] = destIndex[1]
		else:
			dungeonData[self.__children["mobIdx"]]["listIndex"] += 1

		self.__children["parent"].Refresh(False, True, False)
		SaveSettings()

	def __ShowBtn(self):
		global dungeonData
		dungeonData[self.__children["mobIdx"]]["showStatus"] = False
		self.__children["parent"].Refresh(True, True, False)
		SaveSettings()

	def Refresh(self):
		global dungeonData
		data = dungeonData[self.__children["mobIdx"]]
	
		isDeactive = True if data["server_cooldown"] > app.GetGlobalTimeStamp() or player.GetStatus(player.LEVEL) < data["levelrange"][0] or player.GetStatus(player.LEVEL) > data["levelrange"][1] else False
	
		#self.__children["status"].SetText(localeInfo.DUNGEON_TRACK_DEACTIVE if isDeactive else localeInfo.DUNGEON_TRACK_ACTIVE)
		
		# Show bonus and element type
		bonusText = ""
		if "bonus" in data and data["bonus"]:
			bonusText = str(data["bonus"])
		if "elementType" in data and data["elementType"]:
			if bonusText:
				bonusText += ", " + str(data["elementType"])
			else:
				bonusText = str(data["elementType"])
		
		if bonusText:
			self.__children["time"].SetText(bonusText)
			self.__children["time"].Show()
		elif isDeactive:
			self.__children["time"].Show()
		else:
			self.__children["time"].Hide()
	
			if not data["whisper_info"]:
				if data["alarm"]:
					game = constInfo.GetGameInstance()
					if game != None:
						game.BINARY_OnRecvBulkWhisper(localeInfo.DUNGEON_TRACK_WHISPER_MESSAGE % data["name"])
	
					interface = constInfo.GetInterfaceInstance()
					if interface != None:
						interface.wndDungeonManager.AddDungeon(self.__children["mobIdx"])
	
				data["whisper_info"] = True
	
		currentImage = IMG_DIR+"bg_select.png" if data["selected"] else IMG_DIR+"bg_norm.png"
		if currentImage != (self.__children["currentImage"] if "currentImage" in self.__children else ""):
			self.__children["currentImage"] = currentImage
			self.LoadImage(currentImage)

	def OnUpdate(self):
		global dungeonData

		lastUpdate = self.__children["lastUpdate"] if "lastUpdate" in self.__children else 0
		if lastUpdate < app.GetTime():
			self.__children["lastUpdate"] = app.GetTime() + 0.3
			leftTime = dungeonData[self.__children["mobIdx"]]["server_cooldown"] - app.GetGlobalTimeStamp()
			if leftTime <= 0:
				self.Refresh()
			else:
				self.__children["time"].SetText(FormatTime(leftTime))

		if self.__children["eyeBtn"].IsIn() or self.__children["backBtn"].IsIn() or self.__children["nextBtn"].IsIn():
			return
		if self.IsIn():
			listIdx = dungeonData[self.__children["mobIdx"]]["listIndex"]
			if listIdx > 0:
				self.__children["backBtn"].Show()
			else:
				self.__children["backBtn"].Hide()
			if listIdx < len(dungeonData)-1:
				self.__children["nextBtn"].Show()
			else:
				self.__children["nextBtn"].Hide()
			self.__children["eyeBtn"].Show()
		else:
			self.__children["backBtn"].Hide()
			self.__children["nextBtn"].Hide()
			self.__children["eyeBtn"].Hide()

class Map(ui.ExpandedImageBox):
	def Destroy(self):
		self.__children={}
	def __init__(self, mobIdx, parent):
		ui.ExpandedImageBox.__init__(self)
		self.__Load(mobIdx, parent)
	
	def GetShowStatus(self):
		global mapData
		return mapData[self.__children["mobIdx"]]["showStatus"]

	def UpdateTextVisibility(self, itemY, windowHeight):
		TEXT_KEYS = ("name", "level_text_header", "level_text", "price", "bonus", "element")
		TEXT_BOTTOM = {"name": 36, "level_text_header": 31, "level_text": 43, "price": 22, "bonus": 36, "element": 50}
		TEXT_TOP = {"name": 22, "level_text_header": 17, "level_text": 29, "price": 8, "bonus": 22, "element": 36}
		global mapData
		data = mapData.get(self.__children.get("mobIdx", 0), {})
		for key in TEXT_KEYS:
			if key not in self.__children:
				continue
			if key == "bonus" and not data.get("bonusType"):
				continue
			if key == "element" and not data.get("elementType"):
				continue
			topAbs = itemY + TEXT_TOP[key]
			bottomAbs = itemY + TEXT_BOTTOM[key]
			if bottomAbs > windowHeight or topAbs < 0:
				self.__children[key].Hide()
			else:
				self.__children[key].Show()

	def __Load(self, mobIdx, parent):
		self.Destroy()
		self.__children["mobIdx"] = mobIdx
		self.__children["parent"] = _weakref.proxy(parent)

		global mapData
		data = mapData[mobIdx]

		self.__children["name"] = CreateWindow(ui.TextLine(), self, (60, 22), data["name"])
		self.__children["name"].SetFontName("Verdana:14b")
		self.__children["name"].SetOutline()
		self.__children["name"].SetPackedFontColor(0xFFe4cbac)
		self.__children["image"] = CreateWindow(ui.ExpandedImageBox(), self, (123, 0), BG_IMG_DIR_WARP+data["image"])
		self.__children["image"].AddFlag("not_pick")
		#self.__children["status"] = CreateWindow(ui.TextLine(), self, (253, 10), "", "horizontal:right")
		#self.__children["time"] = CreateWindow(ui.TextLine(), self, (60, 30), "")
		#self.__children["time"].SetOutline()
		
		self.__children["level_text_header"] = CreateWindow(ui.TextLine(), self, (16, 17), localeInfo.DUNGEON_TRACK_LV, "horizontal:center")
		self.__children["level_text_header"].SetOutline()
		self.__children["level_text_header"].SetPackedFontColor(0xFFe4cbac)
		lvl_min = data["levelrange"][0]
		lvl_max = data["levelrange"][1]
		if 0 < lvl_max < 999:
			lvl_label = "%d-%d" % (lvl_min, lvl_max)
		else:
			lvl_label = "%d+" % lvl_min
		self.__children["level_text"] = CreateWindow(ui.TextLine(), self, (16, 29), lvl_label, "horizontal:center")
		self.__children["level_text"].SetFontName("Verdana:12b")
		self.__children["level_text"].SetOutline()
		self.__children["level_text"].SetPackedFontColor(0xFFe4cbac)
		self.__children["price"] = CreateWindow(ui.TextLine(), self, (33, 8), localeInfo.DUNGEON_TRACK_MAP_PRICE % self.GetFormattedCount(str(data["price"])), "horizontal:right")
		self.__children["price"].SetFontName("Verdana:14")
		self.__children["price"].SetOutline()
		self.__children["price"].SetPackedFontColor(0xFFc8c8c8)
		self.__children["bonus"] = CreateWindow(ui.TextLine(), self, (33, 22), localeInfo.DUNGEON_TRACK_MAP_RACE % str(data["bonusType"]) if data["bonusType"] else "", "horizontal:right")
		self.__children["bonus"].SetFontName("Verdana:14")
		self.__children["bonus"].SetOutline()
		self.__children["bonus"].SetPackedFontColor(0xFFc8c8c8)
		if not data["bonusType"]:
			self.__children["bonus"].Hide()
		self.__children["element"] = CreateWindow(ui.TextLine(), self, (33, 36), localeInfo.DUNGEON_TRACK_MAP_ELEMENT % str(data["elementType"]) if data["elementType"] else "", "horizontal:right")
		self.__children["element"].SetFontName("Verdana:14")
		self.__children["element"].SetOutline()
		self.__children["element"].SetPackedFontColor(0xFFc8c8c8)
		if not data["elementType"]:
			self.__children["element"].Hide()

	def MatchesSearch(self, searchText):
		if not searchText:
			return True
		
		global mapData
		data = mapData[self.__children["mobIdx"]]
		mapName = data["name"].lower()
		
		import uiScriptLocale
		mapNameClean = uiScriptLocale.RemoveDiacritic(mapName)
		searchLower = searchText.lower()
		
		return searchLower in mapNameClean
		
	def GetMinLevel(self):
		global mapData
		return mapData[self.__children["mobIdx"]]["levelrange"][0]
		
	def GetFormattedCount(self, count):
		count = int(count)
		if count <= 0:
			return "0"
		
		count_str = str(count)
		formatted = '.'.join([
			i-3<0 and count_str[:i] or count_str[i-3:i] 
			for i in range(len(count_str)%3, len(count_str)+1, 3) 
			if i
		])
		return formatted

	def Refresh(self):
		global mapData
		data = mapData[self.__children["mobIdx"]]
	
		isDeactive = True if player.GetStatus(player.LEVEL) < data["levelrange"][0] or player.GetStatus(player.LEVEL) > data["levelrange"][1] else False
	
		#self.__children["status"].SetText(localeInfo.DUNGEON_TRACK_DEACTIVE if isDeactive else localeInfo.DUNGEON_TRACK_ACTIVE)
		
		#if isDeactive:
		#	self.__children["time"].Show()
		#else:
		#	self.__children["time"].Hide()
		
		#if player.GetStatus(player.LEVEL) < data["levelrange"][0]:
		#	self.__children["time"].SetText(localeInfo.DUNGEON_TRACK_LOW_LEVEL)
		#	self.__children["time"].Show()
		#elif player.GetStatus(player.LEVEL) > data["levelrange"][1]:
		#	self.__children["time"].SetText(localeInfo.DUNGEON_TRACK_HIGH_LEVEL)
		#	self.__children["time"].Show()
	
		currentImage = IMG_DIR_WARP+"bg_select.png" if data["selected"] else IMG_DIR_WARP+"bg_norm.png"
		if currentImage != (self.__children["currentImage"] if "currentImage" in self.__children else ""):
			self.__children["currentImage"] = currentImage
			self.LoadImage(currentImage)

def NumberToDecimalString(n):
	return str('.'.join([ i-3<0 and str(n)[:i] or str(n)[i-3:i] for i in range(len(str(n))%3, len(str(n))+1, 3) if i ]))

def FormatTimeEx(seconds):
	if seconds <= 0:
		return "0s"
	m, s = divmod(seconds, 60)
	h, m = divmod(m, 60)
	d, h = divmod(h, 24)
	text = ""
	if d > 0:
		text+="{}d ".format(d)
	if h > 0:
		text+="{}h ".format(h)
	if m > 0:
		text+="{}m ".format(m)
	if s > 0:
		text+="{}s ".format(s)
	return text[:len(text)-1] if len(text) > 0 else "0s"

def FormatTime(seconds):
	if seconds <= 0:
		return "00:00:00"
	m, s = divmod(seconds, 60)
	h, m = divmod(m, 60)
	d, h = divmod(h, 24)
	return "%02d:%02d:%02d"% (h, m, s)

def CreateWindow(window, parent, windowPos, windowArgument = "", windowPositionRule = "", windowSize = (-1, -1), windowFontName = -1):
	window.SetParent(parent)
	window.SetPosition(*windowPos)
	if windowSize != (-1, -1):
		window.SetSize(*windowSize)
	if windowPositionRule:
		splitList = windowPositionRule.split(":")
		if len(splitList) == 2:
			(type, mode) = (splitList[0], splitList[1])
			if type == "horizontal":
				if isinstance(window, ui.TextLine):
					if mode == "center":
						window.SetHorizontalAlignCenter()
					elif mode == "right":
						window.SetHorizontalAlignRight()
						window.SetWindowHorizontalAlignRight()
					elif mode == "left":
						window.SetHorizontalAlignLeft()
				else:
					if mode == "center":
						window.SetWindowHorizontalAlignCenter()
					elif mode == "right":
						window.SetWindowHorizontalAlignRight()
					elif mode == "left":
						window.SetWindowHorizontalAlignLeft()
			elif type == "vertical":
				if isinstance(window, ui.TextLine):
					if mode == "center":
						window.SetVerticalAlignCenter()
					elif mode == "top":
						window.SetVerticalAlignTop()
					elif mode == "bottom":
						window.SetVerticalAlignBottom()
				else:
					if mode == "top":
						window.SetWindowVerticalAlignTop()
					elif mode == "center":
						window.SetWindowVerticalAlignCenter()
					elif mode == "bottom":
						window.SetWindowVerticalAlignBottom()
	if windowArgument:
		if isinstance(window, ui.TextLine):
			if windowFontName != -1:
				window.SetFontName(windowFontName)
			window.SetText(windowArgument)
		elif isinstance(window, ui.NumberLine):
			window.SetNumber(windowArgument)
		elif isinstance(window, ui.ExpandedImageBox) or isinstance(window, ui.ImageBox):
			window.LoadImage(windowArgument if windowArgument.find("gr2") == -1 else "icon/item/27995.tga")
	window.Show()
	return window
def ClearSettings():
	global dungeonData
	for mobIdx, dungeonInfo in dungeonData.items():
		dungeonInfo["listIndex"] = dungeonInfo["static_listIndex"]
		dungeonInfo["showStatus"] = True
		#dungeonInfo["alarm"] = False
	SaveSettings()
def LoadSettings():
	global dungeonData
	# JSON zamiast pickle: pickle.load na kontrolowanym pliku pozwala na wykonanie kodu przez __reduce__.
	# JSON deserializuje wylacznie dane (dict/list/str/int/bool) - zadna sciezka do exec.
	try:
		with open("lib/{}_track".format(player.GetName()), "r") as f:
			currentSettings = json.load(f)
		for mobIdxKey, settingData in currentSettings.items():
			# klucze dungeonData sa int; JSON zapisuje klucze jako string -> rzutujemy z powrotem,
			# inaczej "mobIdx in dungeonData" przestalby trafiac (zachowanie musi zostac 1:1)
			try:
				mobIdx = int(mobIdxKey)
			except (ValueError, TypeError):
				mobIdx = mobIdxKey
			if mobIdx in dungeonData:
				dungeonInfo = dungeonData[mobIdx]
				dungeonInfo["listIndex"] = settingData["listIndex"]
				dungeonInfo["showStatus"] = settingData["showStatus"]
				dungeonInfo["alarm"] = settingData["alarm"]
				dungeonInfo["selected"] = settingData["selected"]
	except:
		pass
def SaveSettings():
	global dungeonData
	# zapisujemy tylko 4 pola faktycznie czytane przez LoadSettings, jako czysty JSON
	settings = {}
	for mobIdx, dungeonInfo in dungeonData.items():
		settings[str(mobIdx)] = {
			"listIndex" : dungeonInfo.get("listIndex", dungeonInfo.get("static_listIndex", 0)),
			"showStatus" : dungeonInfo.get("showStatus", True),
			"alarm" : dungeonInfo.get("alarm", False),
			"selected" : dungeonInfo.get("selected", False),
		}
	try:
		with open("lib/{}_track".format(player.GetName()), "w") as f:
			json.dump(settings, f)
	except:
		pass

class ScrollBarSpecial(ui.Window):
	BASE_COLOR = grp.GenerateColor(0.0, 0.0, 0.0, 1.0)
	CORNERS_AND_LINES_COLOR = grp.GenerateColor(0.3411, 0.3411, 0.3411, 1.0)
	BAR_NUMB = 9 #This is static value! Please dont touch in him.
	SCROLL_WIDTH= 8
	class MiddleBar(ui.DragButton):
		MIDDLE_BAR_COLOR = grp.GenerateColor(0.6470, 0.6470, 0.6470, 1.0)
		def __init__(self, horizontal_scroll):
			ui.DragButton.__init__(self)
			self.AddFlag("movable")
			self.horizontal_scroll = horizontal_scroll
			self.middle = ui.Bar()
			self.middle.SetParent(self)
			self.middle.AddFlag("attach")
			self.middle.AddFlag("not_pick")
			self.middle.SetColor(self.MIDDLE_BAR_COLOR)
			self.middle.SetSize(1, 1)
			self.middle.Show()
		def SetStaticScale(self, size):
			(base_width, base_height) = (self.middle.GetWidth(), self.middle.GetHeight())
			if not self.horizontal_scroll:
				ui.DragButton.SetSize(self, base_width, size)
				self.middle.SetSize(base_width, size)
			else:
				ui.DragButton.SetSize(self, size, base_height)
				self.middle.SetSize(size, base_height)
		def SetSize(self, selfSize, fullSize):
			(base_width, base_height) = (self.middle.GetWidth(), self.middle.GetHeight())
			
			if not self.horizontal_scroll:
				ui.DragButton.SetSize(self, base_width, operator.truediv(int(selfSize), int(fullSize)) * selfSize)
				self.middle.SetSize(base_width, operator.truediv(int(selfSize), int(fullSize)) * selfSize)
			else:
				ui.DragButton.SetSize(self, operator.truediv(int(selfSize), int(fullSize)) * selfSize, base_height)
				self.middle.SetSize(operator.truediv(int(selfSize), int(fullSize)) * selfSize, base_height)
		def SetStaticSize(self, size):
			size = max(2, size)
			
			if not self.horizontal_scroll:
				ui.DragButton.SetSize(self, size, self.middle.GetHeight())
				self.middle.SetSize(size, self.middle.GetHeight())
			else:
				ui.DragButton.SetSize(self, self.middle.GetWidth(), size)
				self.middle.SetSize(self.middle.GetWidth(), size)
	def __init__(self, horizontal_scroll = False):
		ui.Window.__init__(self)
		self.horizontal_scroll = horizontal_scroll
		self.scrollEvent = None
		self.scrollSpeed = 50
		self.sizeScale = 1.0
		self.bars = []
		for i in range(self.BAR_NUMB):
			br = ui.Bar()
			br.SetParent(self)
			br.AddFlag("attach")
			br.AddFlag("not_pick")
			br.SetColor([self.CORNERS_AND_LINES_COLOR, self.BASE_COLOR][i == (self.BAR_NUMB-1)])
			if not (i % 2 == 0): br.SetSize(1, 1)
			br.Show()
			self.bars.append(br)
		self.middleBar = self.MiddleBar(self.horizontal_scroll)
		self.middleBar.SetParent(self)
		self.middleBar.SetMoveEvent(ui.__mem_func__(self.OnScrollMove))
		self.middleBar.Show()
	def OnScrollMove(self):
		if not self.scrollEvent:
			return
		arg = float(self.middleBar.GetLocalPosition()[1] - 1) / float(self.GetHeight() - 2 - self.middleBar.GetHeight()) if not self.horizontal_scroll else\
				float(self.middleBar.GetLocalPosition()[0] - 1) / float(self.GetWidth() - 2 - self.middleBar.GetWidth())
		self.scrollEvent(arg)
	def SetScrollEvent(self, func):
		self.scrollEvent = func
	def SetScrollSpeed(self, speed):
		self.scrollSpeed = speed
	def OnMouseWheel(self, length):
		if not self.IsShow():
			return False
		length = int((length * 0.01) * self.scrollSpeed)
		if not self.horizontal_scroll:
			val = min(max(1, self.middleBar.GetLocalPosition()[1] - (length * 0.01) * self.scrollSpeed * self.sizeScale), self.GetHeight() - self.middleBar.GetHeight() - 1)
			self.middleBar.SetPosition(1, val)
		else:
			val = min(max(1, self.middleBar.GetLocalPosition()[0] - (length * 0.01) *  self.scrollSpeed * self.sizeScale), self.GetWidth() - self.middleBar.GetWidth() - 1)
			self.middleBar.SetPosition(val, 1)
		self.OnScrollMove()
		return True
	def GetPos(self):
		return float(self.middleBar.GetLocalPosition()[1] - 1) / float(self.GetHeight() - 2 - self.middleBar.GetHeight()) if not self.horizontal_scroll else float(self.middleBar.GetLocalPosition()[0] - 1) / float(self.GetWidth() - 2 - self.middleBar.GetWidth())
	def OnMouseLeftButtonDown(self):
		(xMouseLocalPosition, yMouseLocalPosition) = self.GetMouseLocalPosition()
		if not self.horizontal_scroll:
			if xMouseLocalPosition == 0 or xMouseLocalPosition == self.GetWidth():
				return
			y_pos = (yMouseLocalPosition - self.middleBar.GetHeight() / 2)
			self.middleBar.SetPosition(1, y_pos)
		else:
			if yMouseLocalPosition == 0 or yMouseLocalPosition == self.GetHeight():
				return
			x_pos = (xMouseLocalPosition - self.middleBar.GetWidth() / 2)
			self.middleBar.SetPosition(x_pos, 1)
		self.OnScrollMove()
	def SetSize(self, w, h):
		(width, height) = (max(3, w), max(3, h))
		ui.Window.SetSize(self, width, height)
		self.bars[0].SetSize(1, (height - 2))
		self.bars[0].SetPosition(0, 1)
		self.bars[2].SetSize((width - 2), 1)
		self.bars[2].SetPosition(1, 0)
		self.bars[4].SetSize(1, (height - 2))
		self.bars[4].SetPosition((width - 1), 1)
		self.bars[6].SetSize((width - 2), 1)
		self.bars[6].SetPosition(1, (height - 1))
		self.bars[8].SetSize((width - 2), (height - 2))
		self.bars[8].SetPosition(1, 1)
		self.bars[1].SetPosition(0, 0)
		self.bars[3].SetPosition((width - 1), 0)
		self.bars[5].SetPosition((width - 1), (height - 1))
		self.bars[7].SetPosition(0, (height - 1))
		if not self.horizontal_scroll:
			self.middleBar.SetStaticSize(width - 2)
			self.middleBar.SetSize(12, self.GetHeight())
		else:
			self.middleBar.SetStaticSize(height - 2)
			self.middleBar.SetSize(12, self.GetWidth())
		self.middleBar.SetRestrictMovementArea(1, 1, width - 2, height - 2)
	def SetScale(self, selfSize, fullSize):
		self.sizeScale = float(selfSize)/float(fullSize)
		if self.sizeScale <= 0.0305:
			self.sizeScale = 0.05
		self.middleBar.SetSize(selfSize, fullSize)
	def SetStaticScale(self, r_size):
		self.middleBar.SetStaticScale(r_size)
	def SetPosScale(self, fScale):
		pos = (math.ceil((self.GetHeight() - 2 - self.middleBar.GetHeight()) * fScale) + 1) if not self.horizontal_scroll else (math.ceil((self.GetWidth() - 2 - self.middleBar.GetWidth()) * fScale) + 1)
		self.SetPos(pos)
	def SetPos(self, pos):
		wPos = (1, pos) if not self.horizontal_scroll else (pos, 1)
		self.middleBar.SetPosition(*wPos)

class MultiTextLine(ui.Window):
	def Destroy(self):
		self.textRules = {}
	def __init__(self):
		ui.Window.__init__(self)
		self.Destroy()
		self.AddFlag("not_pick")
		self.textRules["textRange"] = 15
		self.textRules["text"] = ""
		self.textRules["textType"] = ""
		self.textRules["fontName"] = ""
		self.textRules["hexColor"] = 0
		self.textRules["fontColor"] = 0
		self.textRules["outline"] = 0
	def SetTextType(self, textType):
		self.textRules["textType"] = textType
		self.Refresh()
	def SetTextRange(self, textRange):
		self.textRules["textRange"] = textRange
		self.Refresh()
	def SetOutline(self, outline):
		self.textRules["outline"] = outline
		self.Refresh()
	def SetPackedFontColor(self, hexColor):
		self.textRules["hexColor"] = hexColor
		self.Refresh()
	def SetFontColor(self, r, g, b):
		self.textRules["fontColor"] =[r, g, b]
		self.Refresh()
	def SetFontName(self, fontName):
		self.textRules["fontName"] = fontName
		self.Refresh()
	def SetText(self, newText):
		self.textRules["text"] = newText
		self.Refresh()
	def Refresh(self):
		textRules = self.textRules
		if textRules["text"] == "":
			return
		self.children=[]
		outline = textRules["outline"]
		fontColor = textRules["fontColor"]
		hexColor = textRules["hexColor"]
		yRange = textRules["textRange"]
		fontName = textRules["fontName"]
		textType = textRules["textType"].split("#")
		totalTextList = textRules["text"].split("#")

		(xPosition, yPosition) = (0, 0)
		width = 0
		for text in totalTextList:
			childText = ui.TextLine()
			childText.SetParent(self)
			childText.AddFlag("not_pick")
			childText.SetPosition(xPosition, yPosition)
			if fontName != "":
				childText.SetFontName(fontName)
			if hexColor != 0:
				childText.SetPackedFontColor(hexColor)
			if fontColor != 0:
				childText.SetFontColor(*fontColor)
			if outline:
				childText.SetOutline()
			self.AddTextType(childText, textType)
			childText.SetText(str(text))
			if childText.GetTextSize()[0] > width:
				width = childText.GetTextSize()[0]
			childText.Show()
			self.children.append(childText)
			yPosition+=yRange

	def AddTextType(self, text,  typeArg):
		if len(typeArg) != 2:
			return
		_typeDict = {
			"vertical": {
				"top":text.SetVerticalAlignTop,
				"bottom":text.SetVerticalAlignBottom,
				"center":text.SetVerticalAlignCenter,
			},
			"horizontal": {
				"left":text.SetHorizontalAlignLeft,
				"right":text.SetHorizontalAlignRight,
				"center":text.SetHorizontalAlignCenter,
			},
			"all_align": {
				"1" : [text.SetHorizontalAlignCenter,text.SetVerticalAlignCenter,text.SetWindowHorizontalAlignCenter,text.SetWindowVerticalAlignCenter],
			},
		}
		(firstToken, secondToken) = tuple(typeArg)
		if firstToken in _typeDict:
			textType = _typeDict[firstToken][secondToken] if secondToken in _typeDict[firstToken] else None
			if textType != None:
				if isinstance(textType, list):
					for rule in textType:
						rule()
				else:
					textType()

class LogWindow(ui.BoardWithTitleBar):
	__children = {}
	class LogItem(ui.ExpandedImageBox):
		def Destroy(self):
			self.__children = {}
		def __init__(self, idx, name, val, level, rankIdx):
			ui.ExpandedImageBox.__init__(self)
			self.__LoadWindow(idx, name, val, level, rankIdx)

		def __LoadWindow(self, idx, name, val, level, rankIdx):
			self.Destroy()
			self.LoadImage(IMG_DIR+"log_item.tga")

			indexText = CreateWindow(ui.TextLine(), self, (20, 3), str(idx+1), "horizontal:center")
			self.__children["indexText"] = indexText

			nameText = CreateWindow(ui.TextLine(), self, (110, 3), name, "horizontal:center")
			self.__children["nameText"] = nameText

			levelText = CreateWindow(ui.TextLine(), self, (203, 3), str(level), "horizontal:center")
			self.__children["levelText"] =levelText

			valueComparedTest = FormatTimeEx(val) if rankIdx == 1 else NumberToDecimalString(val)
			valueText = CreateWindow(ui.TextLine(), self, (268, 3), valueComparedTest, "horizontal:center")
			self.__children["valueText"] = valueText

			if name == player.GetName():
				indexText.SetPackedFontColor(0xFFffcc00)
				nameText.SetPackedFontColor(0xFFffcc00)
				levelText.SetPackedFontColor(0xFFffcc00)
				valueText.SetPackedFontColor(0xFFffcc00)

	def Destroy(self):
		listBox = self.__children["listBox"] if "listBox" in self.__children else None
		if listBox:
			listBox.RemoveAllItems()
		self.__children = {}
	def __init__(self):
		ui.BoardWithTitleBar.__init__(self)
		self.Destroy()
		self.__LoadWindow()

	def __LoadWindow(self):
		self.SetSize(362,200)
		self.SetCenterPosition()
		self.AddFlag("float")
		self.AddFlag("movable")
		self.AddFlag("attach")
		self.AddFlag("animate")

		logTitle = CreateWindow(ui.ImageBox(), self, (19, 39), IMG_DIR+"log_title.tga")
		self.__children["logTitle"] = logTitle

		self.__children["rankText"] = CreateWindow(ui.TextLine(), logTitle, (20, 3), localeInfo.DUNGEON_TRACK_RANK_INDEX, "horizontal:center")
		self.__children["nameText"] = CreateWindow(ui.TextLine(), logTitle, (110, 3), localeInfo.DUNGEON_TRACK_RANK_NAME, "horizontal:center")
		self.__children["levelText"] = CreateWindow(ui.TextLine(), logTitle, (203, 3), localeInfo.DUNGEON_TRACK_RANK_LEVEL, "horizontal:center")
		self.__children["valueText"] = CreateWindow(ui.TextLine(), logTitle, (268, 3), "", "horizontal:center")

		listBox = CreateWindow(ui.ListBoxEx(), self, (19,39+logTitle.GetHeight()+5), "", "", (308, 23*5))
		listBox.AddFlag("attach")
		listBox.SetItemSize(308, 21)
		listBox.SetItemStep(23)
		listBox.SetViewItemCount(5)
		self.__children["listBox"] = listBox

		self.__children["loadingImage"] = CreateWindow(ui.ExpandedImageBox(), listBox, ((listBox.GetWidth()/2)-16, (listBox.GetHeight()/2)-16), IMG_DIR+"load_.tga")
		self.__children["loadingImage"].Hide()
		self.__children["loadingImageRotation"] = 0

		scrollBar = CreateWindow(ui.ScrollBar(), self, (19+logTitle.GetWidth()+5,39+logTitle.GetHeight()))
		#scrollBar.SetScrollBarSize(21 * 5 + 15)
		listBox.SetScrollBar(scrollBar)
		self.__children["scrollBar"] = scrollBar
	
		self.__children["rankData"] = {}

	def LoadServerData(self, mobIdx, rankIdx, cmd):
		rankData = self.__children["rankData"][mobIdx] if mobIdx in self.__children["rankData"] else {}
		data = rankData[rankIdx] if rankIdx in rankData else {}
		rankList = []
		if cmd != "-":
			cmdSplit = cmd.split("#")
			for cmdInfo in cmdSplit:
				cmdInfoSplit = cmdInfo.split("|")
				if len(cmdInfoSplit) != 3:
					continue
				rankList.append({"name":cmdInfoSplit[0],"val":int(cmdInfoSplit[1]),"level":int(cmdInfoSplit[2])})

		data["leftTime"] = app.GetGlobalTimeStamp() + LOG_UPDATE_TIME
		data["data"] = rankList

		rankData[rankIdx] = data
		self.__children["rankData"][mobIdx] = rankData
		self.__LoadData(mobIdx, rankIdx)
		
	def __LoadData(self, mobIdx, rankIdx):
		self.__children["listBox"].RemoveAllItems()
		global dungeonData
		if not mobIdx in dungeonData:
			return
		__titleNames = [localeInfo.DUNGEON_TRACK_RANK_COMPLETED_TITLE, localeInfo.DUNGEON_TRACK_RANK_FASTEST_TITLE, localeInfo.DUNGEON_TRACK_RANK_DMG_TITLE]
		self.__children["valueText"].SetText(__titleNames[rankIdx])
		self.SetTitleName(dungeonData[mobIdx]["name"] + " - " + __titleNames[rankIdx])

		(self.__children["mobIdx"], self.__children["rankIdx"]) = (mobIdx, rankIdx)

		if self.__CheckRankNeedUpdate(mobIdx, rankIdx):
			self.__children["loadingImage"].Show()
			import dungeonInfo
			for key in range(dungeonInfo.GetCount()):
				if dungeonInfo.GetMapIndex(key) == mobIdx:
					dungeonInfo.Ranking(key, rankIdx + 1)
					break
		else:
			self.__children["loadingImage"].Hide()

			rankData = self.__GetData(mobIdx, rankIdx)
			if rankData != None:
				rankList = rankData["data"]
				for j in range(len(rankList)):
					self.__children["listBox"].AppendItem(self.LogItem(j, rankList[j]["name"], rankList[j]["val"], rankList[j]["level"], rankIdx))
		self.Show()
		self.SetTop()

	def __GetData(self, mobIdx, rankIdx):
		rankData = self.__children["rankData"]
		if mobIdx in rankData:
			if rankIdx in rankData[mobIdx]:
				return rankData[mobIdx][rankIdx]
		return None
	def __GetLeftTime(self, mobIdx, rankIdx):
		rankData = self.__children["rankData"]
		if mobIdx in rankData:
			if rankIdx in rankData[mobIdx]:
				return rankData[mobIdx][rankIdx]["leftTime"]
		return -1
	def __CheckRankNeedUpdate(self, mobIdx, rankIdx):
		return False if self.__GetLeftTime(mobIdx, rankIdx) > app.GetGlobalTimeStamp() else True
	def OnUpdate(self):
		loadingImage = self.__children["loadingImage"] if "loadingImage" in self.__children else None
		if loadingImage:
			if loadingImage.IsShow():
				newRotation = self.__children["loadingImageRotation"] = self.__children["loadingImageRotation"] + 10
				self.__children["loadingImage"].SetRotation(newRotation)
	def OnServerRankingData(self):
		if "mobIdx" not in self.__children or "rankIdx" not in self.__children:
			return
		import dungeonInfo
		rankCount = dungeonInfo.GetRankingCount()
		mobIdx = self.__children["mobIdx"]
		rankIdx = self.__children["rankIdx"]
		rankList = []
		for i in range(rankCount):
			name, level, points = dungeonInfo.GetRankingByLine(i)
			rankList.append({"name": name, "val": points, "level": level})
		dungeonInfo.ClearRanking()
		data = {}
		data["leftTime"] = app.GetGlobalTimeStamp() + LOG_UPDATE_TIME
		data["data"] = rankList
		rankData = self.__children.get("rankData", {})
		if mobIdx not in rankData:
			rankData[mobIdx] = {}
		rankData[mobIdx][rankIdx] = data
		self.__children["rankData"] = rankData
		self.__children["loadingImage"].Hide()
		self.__children["listBox"].RemoveAllItems()
		for j in range(len(rankList)):
			self.__children["listBox"].AppendItem(self.LogItem(j, rankList[j]["name"], rankList[j]["val"], rankList[j]["level"], rankIdx))
	def Open(self, mobIdx, rankIdx):
		SetActiveLogWindow(self)
		self.__LoadData(mobIdx, rankIdx)
	def Close(self):
		SetActiveLogWindow(None)
		self.Hide()
	def OnPressEscapeKey(self):
		self.Close()
		return True
