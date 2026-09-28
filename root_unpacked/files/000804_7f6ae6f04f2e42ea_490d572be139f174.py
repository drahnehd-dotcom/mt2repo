import ui
import chat
import item
import localeInfo
import net
import app
import wndMgr

# ---------------------------------------------------------------------------
# FishConfigManager - receives and stores fish config from server
# ---------------------------------------------------------------------------

class FishConfigManager:
	def __init__(self):
		self.fish_entries = []
		self.fish_index = {}
		self.categories = []
		self.categories_per_row = 3
		self.is_loaded = False
		self._pending_entries = []

	def on_config_start(self, fish_count, categories_per_row):
		self._pending_entries = []
		self.categories_per_row = max(1, categories_per_row)

	def on_config_fish(self, vnum, needed_count, needed_length, success_chance, reward_type, reward_value):
		self._pending_entries.append({
			"vnum": vnum,
			"needed_count": needed_count,
			"needed_length": needed_length,
			"success_chance": success_chance,
			"reward_type": reward_type,
			"reward_value": reward_value,
		})

	def on_config_end(self):
		self.fish_entries = self._pending_entries
		self._pending_entries = []

		self.fish_index = {}
		for i, entry in enumerate(self.fish_entries):
			self.fish_index[entry["vnum"]] = i

		self.categories = []
		row = self.categories_per_row
		for i in range(0, len(self.fish_entries), row):
			cat = [e["vnum"] for e in self.fish_entries[i:i + row]]
			while len(cat) < row:
				cat.append(0)
			self.categories.append(cat)

		self.is_loaded = True

	def get_mission_data(self, vnum):
		idx = self.fish_index.get(vnum)
		if idx is None:
			return None
		e = self.fish_entries[idx]
		return [e["needed_count"], e["needed_length"], e["success_chance"], e["reward_type"], e["reward_value"]]

	def get_fish_count(self):
		return len(self.fish_entries)

	def get_categories(self):
		return self.categories

	def get_all_vnums(self):
		return [e["vnum"] for e in self.fish_entries]


_config_manager = FishConfigManager()


def GetFishMissionData(fishVnum):
	return _config_manager.get_mission_data(fishVnum)


# ---------------------------------------------------------------------------
# ScrollBar
# ---------------------------------------------------------------------------

class ScrollBar(ui.Window):
	MIDDLE_BAR_POS = 0
	MIDDLE_BAR_UPPER_PLACE = 6
	MIDDLE_BAR_DOWNER_PLACE = 5
	TEMP_SPACE = MIDDLE_BAR_UPPER_PLACE + MIDDLE_BAR_DOWNER_PLACE

	class MiddleBar(ui.DragButton):
		def __init__(self):
			ui.DragButton.__init__(self)
			self.AddFlag("movable")
			ui.DragButton.SetSize(self, 20, 22)

		def MakeImage(self):
			middle = ui.ExpandedImageBox()
			middle.SetParent(self)
			middle.LoadImage("kowal/fish_wiki/scroll_middle.png")
			middle.SetPosition(-3, 0)
			middle.AddFlag("not_pick")
			middle.Show()
			self.middle = middle

		def SetSize(self, height):
			ui.DragButton.SetSize(self, 20, 22)

	def __init__(self):
		ui.Window.__init__(self)
		self.pageSize = 1
		self.curPos = 0.0
		self.eventScroll = lambda *arg: None
		self.lockFlag = False
		self.scrollStep = 0.20
		self._CreateScrollBar()
		self._SetScrollBarSize(266)

	def __del__(self):
		ui.Window.__del__(self)

	def _CreateScrollBar(self):
		barSlot = ui.ExpandedImageBox()
		barSlot.SetParent(self)
		barSlot.LoadImage("kowal/fish_wiki/scroll_base.png")
		barSlot.SetPosition(0, 0)
		barSlot.AddFlag("not_pick")
		barSlot.Show()

		middleBar = self.MiddleBar()
		middleBar.SetParent(self)
		middleBar.SetMoveEvent(ui.__mem_func__(self.OnMove))
		middleBar.Show()
		middleBar.MakeImage()

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
		realHeight = self.GetHeight()
		self.SCROLLBAR_MIDDLE_HEIGHT = int(pageScale * float(realHeight))
		self.middleBar.SetSize(self.SCROLLBAR_MIDDLE_HEIGHT)
		self.pageSize = self.GetHeight() - self.SCROLLBAR_MIDDLE_HEIGHT - self.TEMP_SPACE

	def _SetScrollBarSize(self, height):
		self.pageSize = height - self.SCROLLBAR_MIDDLE_HEIGHT - self.TEMP_SPACE
		self.SetSize(self.SCROLLBAR_WIDTH, height)
		self.middleBar.SetRestrictMovementArea(
			self.MIDDLE_BAR_POS, self.MIDDLE_BAR_UPPER_PLACE,
			self.MIDDLE_BAR_POS + 2, height - self.TEMP_SPACE)
		self.middleBar.SetPosition(self.MIDDLE_BAR_POS, 0)
		self._UpdateBarSlot()

	def SetScrollBarSize(self, height):
		self._SetScrollBarSize(266)

	def _UpdateBarSlot(self):
		self.barSlot.SetPosition(0, 0)
		self.barSlot.SetSize(self.GetWidth() - 2, self.GetHeight() - 2)

	def GetPos(self):
		return self.curPos

	def SetPos(self, pos):
		pos = max(0.0, min(1.0, pos))
		newPos = float(self.pageSize) * pos
		self.middleBar.SetPosition(self.MIDDLE_BAR_POS, int(newPos) + self.MIDDLE_BAR_UPPER_PLACE)
		self.OnMove()

	def SetScrollStep(self, step):
		self.scrollStep = step

	def GetScrollStep(self):
		return self.scrollStep

	def OnUp(self):
		self.SetPos(self.curPos - self.scrollStep)

	def OnDown(self):
		self.SetPos(self.curPos + self.scrollStep)

	def OnMove(self):
		if self.lockFlag:
			return
		if self.pageSize == 0:
			return
		(xLocal, yLocal) = self.middleBar.GetLocalPosition()
		self.curPos = float(yLocal - self.MIDDLE_BAR_UPPER_PLACE) / float(self.pageSize)
		self.eventScroll()

	def OnMouseLeftButtonDown(self):
		(xMouseLocalPosition, yMouseLocalPosition) = self.GetMouseLocalPosition()
		pickedPos = yMouseLocalPosition - self.SCROLLBAR_MIDDLE_HEIGHT // 2
		newPos = float(pickedPos) / float(self.pageSize)
		self.SetPos(newPos)

	def LockScroll(self):
		self.lockFlag = True

	def UnlockScroll(self):
		self.lockFlag = False


# ---------------------------------------------------------------------------
# FishSlotWidget - a row of fish icon buttons (dynamic)
# ---------------------------------------------------------------------------

class FishSlotWidget(ui.Window):
	def __init__(self, category_idx, fish_vnums, click_event):
		ui.Window.__init__(self)
		self.category_idx = category_idx
		self.fish_vnums = fish_vnums
		self.click_event = click_event
		self.is_unlocked = [False] * len(fish_vnums)
		self.fishBtns = {}
		self.fishImgs = {}
		self.fishLockedImgs = {}
		self._BuildSlots()

	def __del__(self):
		ui.Window.__del__(self)

	def _BuildSlots(self):
		active_count = 0
		for i, vnum in enumerate(self.fish_vnums):
			if vnum == 0:
				break

			btn = ui.Button()
			btn.SetParent(self)
			btn.SetUpVisual("kowal/fish_wiki/slot_norm.png")
			btn.SetOverVisual("kowal/fish_wiki/slot_hover.png")
			btn.SetDownVisual("kowal/fish_wiki/slot_down.png")
			btn.SetDisableVisual("kowal/fish_wiki/slot_disabled.png")
			btn.SAFE_SetEvent(self._OnClick, i)
			btn.SetPosition(43 * i, 0)
			btn.Show()
			self.fishBtns[i] = btn

			item.SelectItem(vnum)
			img = ui.ImageBox()
			img.SetParent(btn)
			img.LoadImage(item.GetIconImageFileName())
			img.SetPosition(0, 0)
			img.AddFlag("not_pick")
			img.SetWindowHorizontalAlignCenter()
			img.SetWindowVerticalAlignCenter()
			img.SetAlpha(0.4)
			img.Show()
			self.fishImgs[i] = img

			locked_img = ui.ImageBox()
			locked_img.SetParent(img)
			locked_img.LoadImage("kowal/fish_wiki/not_unlocked.png")
			locked_img.SetPosition(0, 0)
			locked_img.AddFlag("not_pick")
			locked_img.SetWindowHorizontalAlignCenter()
			locked_img.SetWindowVerticalAlignCenter()
			locked_img.Show()
			self.fishLockedImgs[i] = locked_img

			active_count += 1

		start_x = 43
		if active_count == 2:
			start_x -= 43 // 2
		elif active_count >= 3:
			start_x = 0

		for i in range(active_count):
			self.fishBtns[i].SetPosition(start_x + 43 * i, 0)

		self.SetSize(43 * 3, 47)

	def SetIsUnlocked(self, fish_idx, unlocked):
		if fish_idx not in self.fishImgs:
			return
		if self.is_unlocked[fish_idx] == unlocked:
			return

		self.is_unlocked[fish_idx] = unlocked
		if unlocked:
			self.fishLockedImgs[fish_idx].Hide()
			self.fishImgs[fish_idx].SetAlpha(1.0)
		else:
			self.fishLockedImgs[fish_idx].Show()
			self.fishImgs[fish_idx].SetAlpha(0.4)

	def _OnClick(self, idx):
		self.click_event(self.category_idx, idx)


# ---------------------------------------------------------------------------
# FishLockedPanel - shown when a locked fish is selected
# ---------------------------------------------------------------------------

class FishLockedPanel(ui.Window):
	def __init__(self, parent_board):
		ui.Window.__init__(self)
		self.SetParent(parent_board)
		self.SetSize(348, 320)
		self.SetPosition(190, 0)

		bg = ui.ImageBox()
		bg.SetParent(self)
		bg.SetPosition(12, 10)
		bg.LoadImage("kowal/fish_wiki/unknown_fish_board.png")
		bg.Show()
		self.bg = bg

		# Oba napisy byly wczesniej wpalone w unknown_fish_board.png po czesku.
		# Pozycje odpowiadaja miejscu, gdzie siedzialy na grafice (srodek plyty = x 161).
		self.title_txt = ui.TextLine("Tahoma:12")
		self.title_txt.SetParent(bg)
		self.title_txt.SetPackedFontColor(0xFFD0D0D0)
		self.title_txt.SetPosition(161, 127)
		self.title_txt.SetOutline()
		self.title_txt.SetHorizontalAlignCenter()
		self.title_txt.SetText(localeInfo.FISHWIKI_UNKNOWN_TITLE)
		self.title_txt.Show()

		self.rod_txt = ui.TextLine("Tahoma:12")
		self.rod_txt.SetParent(bg)
		self.rod_txt.SetPackedFontColor(0xFFD0D0D0)
		self.rod_txt.SetPosition(161, 154)
		self.rod_txt.SetOutline()
		self.rod_txt.SetHorizontalAlignCenter()
		self.rod_txt.SetText(localeInfo.FISHWIKI_UNKNOWN_ROD)
		self.rod_txt.Show()

		hide_btn = ui.Button()
		hide_btn.SetParent(self)
		hide_btn.SetPosition(116, 284)
		hide_btn.SetUpVisual("kowal/fish_wiki/btn_normal.png")
		hide_btn.SetOverVisual("kowal/fish_wiki/btn_hover.png")
		hide_btn.SetDownVisual("kowal/fish_wiki/btn_down.png")
		hide_btn.Show()
		self.hide_btn = hide_btn

		self.Hide()

	def SetCloseEvent(self, event):
		self.hide_btn.SAFE_SetEvent(event)

	def SetText(self, text):
		pass


# ---------------------------------------------------------------------------
# FishDetailPanel - shows fish stats + mission info
# ---------------------------------------------------------------------------

class FishDetailPanel(ui.Window):
	def __init__(self, parent_board):
		ui.Window.__init__(self)
		self.SetParent(parent_board)
		self.SetSize(348, 320)
		self.SetPosition(190, 0)

		bg = ui.ImageBox()
		bg.SetParent(self)
		bg.SetPosition(6, 6)
		bg.LoadImage("kowal/fish_wiki/mission_board.png")
		bg.Show()
		self.bg = bg

		# Naglowek paska misji — byl wpalony w mission_board.png jako czeskie "Ke splneni".
		self.mission_header_txt = self._MakeText(bg, "Tahoma:12", 0xFFD0D0D0, 14, 136)
		self.mission_header_txt.SetText(localeInfo.FISHWIKI_MISSION_HEADER)

		self.fish_name_txt = self._MakeText(bg, "Tahoma:14", 0xFFD0D0D0, 16, 3)
		self.caught_count_txt = self._MakeText(bg, "Tahoma:14", 0xFFD0D0D0, 16, 40)
		self.best_length_txt = self._MakeText(bg, "Tahoma:14", 0xFFD0D0D0, 16, 60)
		self.best_price_txt = self._MakeText(bg, "Tahoma:14", 0xFFD0D0D0, 16, 80)
		self.mission_info_txt = self._MakeText(bg, "Tahoma:12", 0xFFD0D0D0, 16, 172)
		self.mission_chance_txt = self._MakeText(bg, "Tahoma:12", 0xFFD0D0D0, 16, 190)
		self.mission_reward_txt = self._MakeText(bg, "Tahoma:12", 0xFFD0D0D0, 16, 208)

		self.mission_progress_txt = ui.TextLine("Tahoma:12")
		self.mission_progress_txt.SetParent(bg)
		self.mission_progress_txt.SetPackedFontColor(0xFFD0D0D0)
		self.mission_progress_txt.SetPosition(311, 227)
		self.mission_progress_txt.SetOutline()
		self.mission_progress_txt.SetHorizontalAlignCenter()
		self.mission_progress_txt.SetText(localeInfo.FISH_PROGRESS_INFO)
		self.mission_progress_txt.Show()

		ranking_btn = ui.Button()
		ranking_btn.SetParent(self)
		ranking_btn.SetPosition(284, 56)
		ranking_btn.SetUpVisual("kowal/fish_wiki/rank_btn_norm.png")
		ranking_btn.SetOverVisual("kowal/fish_wiki/rank_btn_hover.png")
		ranking_btn.SetDownVisual("kowal/fish_wiki/rank_btn_down.png")
		ranking_btn.SetText("")
		ranking_btn.SetToolTipText(localeInfo.FISHWIKI_SHOW_RANKING, 0, -10)
		ranking_btn.Show()
		self.ranking_btn = ranking_btn

		give_btn = ui.Button()
		give_btn.SetParent(self)
		give_btn.SetPosition(114, 284)
		give_btn.SetUpVisual("kowal/fish_wiki/btn_normal.png")
		give_btn.SetOverVisual("kowal/fish_wiki/btn_hover.png")
		give_btn.SetDownVisual("kowal/fish_wiki/btn_down.png")
		give_btn.SetDisableVisual("kowal/fish_wiki/btn_disable.png")
		give_btn.SetText(localeInfo.FISH_GIVE_MISSION_BTN)
		give_btn.Show()
		self.give_btn = give_btn

		self.caught_count_txt.SetText(localeInfo.FISHWIKI_CATCHED_FISHES)
		self.best_length_txt.SetText(localeInfo.FISHWIKI_LONGEST_FISH)
		self.best_price_txt.SetText(localeInfo.FISHWIKI_MOST_EXPENSIVE_FISH)
		self.mission_info_txt.SetText(localeInfo.FISHWIKI_GIVE_10_FISHES)
		self.mission_chance_txt.SetText(localeInfo.FISHWIKI_GIVE_CHANCE)
		self.mission_reward_txt.SetText(localeInfo.FISHWIKI_REWARD_FOR_MISSION)

		self.Hide()

	def _MakeText(self, parent, font, color, x, y):
		txt = ui.TextLine(font)
		txt.SetParent(parent)
		txt.SetPackedFontColor(color)
		txt.SetPosition(x, y)
		txt.SetOutline()
		txt.SetText("")
		txt.Show()
		return txt

	def SetRankingEvent(self, event):
		self.ranking_btn.SAFE_SetEvent(event)

	def SetGiveEvent(self, event):
		self.give_btn.SAFE_SetEvent(event)

	def Refresh(self, fish_vnum, fish_data, mission_data):
		item.SelectItem(fish_vnum)
		self.fish_name_txt.SetText(item.GetItemName())

		count = fish_data.get("count", 0)
		best_length = fish_data.get("best_length", 0)
		best_price = fish_data.get("best_price", 0)
		mission_progress = fish_data.get("mission_progress", 0)

		self.caught_count_txt.SetText(localeInfo.FISHWIKI_CATCHED_FISHES_COUNT % count)
		self.best_length_txt.SetText(localeInfo.FISHWIKI_LONGEST_FISH_CM % (float(best_length) / 100.0))
		self.best_price_txt.SetText(localeInfo.FISHWIKI_MOST_EXPENSIVE_FISH_YANG % localeInfo.NumberToString(best_price))

		if mission_data:
			needed_count = mission_data[0]
			needed_length = mission_data[1]
			success_chance = mission_data[2]

			self.mission_info_txt.SetText(localeInfo.FISHWIKI_GIVE_FISHES % (needed_count, item.GetItemName(), needed_length))
			self.mission_chance_txt.SetText(localeInfo.FISHWIKI_GIVE_CHANCE_SUCCESS % success_chance)

			reward_desc = self._GetRewardDescription(fish_vnum)
			self.mission_reward_txt.SetText(localeInfo.FISHWIKI_REWARD_FOR_MISSION_FISH % reward_desc)
			self.mission_progress_txt.SetText(localeInfo.FISHWIKI_PROGRESS_STATE % (mission_progress, needed_count))

			if mission_progress < needed_count:
				self.give_btn.Enable()
			else:
				self.give_btn.Disable()

	def _GetRewardDescription(self, fish_vnum):
		mission_data = _config_manager.get_mission_data(fish_vnum)
		if not mission_data:
			return ""
		return "%d/%d" % (mission_data[3], mission_data[4])


# ---------------------------------------------------------------------------
# FishRankingPanel - shows top-10 length ranking
# ---------------------------------------------------------------------------

class FishRankingPanel(ui.Window):
	RANK_SLOTS = 10

	def __init__(self, parent_board):
		ui.Window.__init__(self)
		self.SetParent(parent_board)
		self.SetSize(348, 320)
		self.SetPosition(190, 0)

		bg = ui.ImageBox()
		bg.SetParent(self)
		bg.SetPosition(22, 6)
		bg.LoadImage("kowal/fish_wiki/rank_board.png")
		bg.Show()
		self.bg = bg

		self.title_txt = ui.TextLine("Tahoma:12")
		self.title_txt.SetParent(bg)
		self.title_txt.SetPackedFontColor(0xFFD0D0D0)
		self.title_txt.SetPosition(12, 6)
		self.title_txt.SetOutline()
		self.title_txt.SetText(localeInfo.FISHWIKI_LENGTH_RANKING)
		self.title_txt.Show()

		# Naglowki kolumn — byly wpalone w rank_board.png po czesku. Kolumny rozdzielaja
		# separatory na x = 34, 125 i 214, wiec teksty trzymaja sie tych samych wciec
		# co dane w wierszach ponizej (18 / 41 / 133 / 222).
		self.header_txts = []
		for x, align, key in [(18, True,  localeInfo.FISHWIKI_RANK_COL_POS),
		                      (41, False, localeInfo.FISHWIKI_RANK_COL_NAME),
		                      (133, False, localeInfo.FISHWIKI_RANK_COL_LENGTH),
		                      (217, False, localeInfo.FISHWIKI_RANK_COL_ROD)]:
			txt = ui.TextLine("Tahoma:12")
			txt.SetParent(bg)
			txt.SetPackedFontColor(0xFFD0D0D0)
			txt.SetPosition(x, 32)
			txt.SetOutline()
			if align:
				txt.SetHorizontalAlignCenter()
			txt.SetText(key)
			txt.Show()
			self.header_txts.append(txt)

		self.rank_rows = []
		for i in range(self.RANK_SLOTS):
			row = self._CreateRankRow(bg, i)
			self.rank_rows.append(row)

		back_btn = ui.Button()
		back_btn.SetParent(self)
		back_btn.SetPosition(115, 284)
		back_btn.SetUpVisual("kowal/fish_wiki/btn_normal.png")
		back_btn.SetOverVisual("kowal/fish_wiki/btn_hover.png")
		back_btn.SetDownVisual("kowal/fish_wiki/btn_down.png")
		back_btn.Show()
		self.back_btn = back_btn

		self.Hide()

	def _CreateRankRow(self, parent, index):
		y = 51 + index * 21

		idx_txt = ui.TextLine("Tahoma:12")
		idx_txt.SetParent(parent)
		idx_txt.SetPackedFontColor(0xFFD0D0D0)
		idx_txt.SetPosition(18, y)
		idx_txt.SetOutline()
		idx_txt.SetText("%d." % (index + 1))
		idx_txt.SetHorizontalAlignCenter()
		idx_txt.Show()

		name_txt = ui.TextLine("Tahoma:12")
		name_txt.SetParent(parent)
		name_txt.SetPackedFontColor(0xFFD0D0D0)
		name_txt.SetPosition(41, y)
		name_txt.SetOutline()
		name_txt.SetText("---")
		name_txt.Show()

		length_txt = ui.TextLine("Tahoma:12")
		length_txt.SetParent(parent)
		length_txt.SetPackedFontColor(0xFFD0D0D0)
		length_txt.SetPosition(133, y)
		length_txt.SetOutline()
		length_txt.SetText(localeInfo.FISH_LENGTH_DEFAULT)
		length_txt.Show()

		rod_txt = ui.TextLine("Tahoma:12")
		rod_txt.SetParent(parent)
		rod_txt.SetPackedFontColor(0xFFD0D0D0)
		rod_txt.SetPosition(222, y)
		rod_txt.SetOutline()
		rod_txt.SetText(localeInfo.FISHWIKI_ROD_LEVEL_0)
		rod_txt.Show()

		return [idx_txt, name_txt, length_txt, rod_txt]

	def SetBackEvent(self, event):
		self.back_btn.SAFE_SetEvent(event)

	def SetTitle(self, fish_name):
		self.title_txt.SetText(localeInfo.FISHWIKI_LENGTH_RANKING_BEST % fish_name)

	def Refresh(self, ranking_data):
		for i in range(self.RANK_SLOTS):
			entry = ranking_data.get(i)
			if entry and entry[1] != 0:
				self.rank_rows[i][1].SetText(entry[0])
				self.rank_rows[i][2].SetText("%.2f cm." % (float(entry[1]) / 100.0))
				self.rank_rows[i][3].SetText(localeInfo.FISHWIKI_ROD_LEVEL % entry[2])
			else:
				self.rank_rows[i][1].SetText("-----")
				self.rank_rows[i][2].SetText(localeInfo.FISH_LENGTH_DEFAULT)
				self.rank_rows[i][3].SetText("")

	def ClearRanking(self):
		for i in range(self.RANK_SLOTS):
			self.rank_rows[i][1].SetText("-----")
			self.rank_rows[i][2].SetText(localeInfo.FISH_LENGTH_DEFAULT)
			self.rank_rows[i][3].SetText("")


# ---------------------------------------------------------------------------
# FishingWikipediaWindow - main window
# ---------------------------------------------------------------------------

class FishingWikipediaWindow(ui.Window):
	SIMPLE_WIDTH = 228
	EXPANDED_WIDTH = 576
	WINDOW_HEIGHT = 386

	PANEL_LOCKED = 0
	PANEL_DETAIL = 1
	PANEL_RANKING = 2

	def __init__(self):
		ui.Window.__init__(self)

		self.config_manager = _config_manager
		self.player_fish_data = {}
		self.ranking_data = {}
		self.ranking_load_times = {}

		self.selected_cat_idx = -1
		self.selected_fish_idx = -1

		self.need_close_blackboard = False
		self.blackboard_close_time = 0

		self.new_fish_window = None
		self.fish_list_items = {}

		self._BuildWindow()

	def __del__(self):
		ui.Window.__del__(self)

	def _BuildWindow(self):
		self.AddFlag("float")

		self.board = ui.BoardWithTitleBar()
		self.board.SetParent(self)
		self.board.SetSize(self.SIMPLE_WIDTH, self.WINDOW_HEIGHT)
		self.board.SetPosition(0, 0)
		self.board.SetTitleName(localeInfo.FISHWIKI_MAIN_WINDOW)
		self.board.SetCloseEvent(ui.__mem_func__(self._CloseByPlayer))
		self.board.Show()

		self.bg = ui.ImageBox()
		self.bg.SetParent(self.board)
		self.bg.SetPosition(20, 50)
		self.bg.LoadImage("kowal/fish_wiki/bg_simple.png")
		self.bg.Show()

		self.scroll_bar = ScrollBar()
		self.scroll_bar.SetParent(self.bg)
		self.scroll_bar.SetScrollBarSize(256)
		self.scroll_bar.SetPosition(160, 24)
		self.scroll_bar.Show()

		self.fish_list_box = ui.ListBoxEx()
		self.fish_list_box.SetParent(self.bg)
		self.fish_list_box.SetPosition(16, 20)
		self.fish_list_box.SetSize(129, 45 * 6)
		self.fish_list_box.SetItemSize(129, 45)
		self.fish_list_box.SetItemStep(46)
		self.fish_list_box.SetViewItemCount(6)
		self.fish_list_box.SetScrollBar(self.scroll_bar)
		self.fish_list_box.Show()

		self.locked_panel = FishLockedPanel(self.bg)
		self.locked_panel.SetCloseEvent(ui.__mem_func__(self._SetSimpleBoard))

		self.detail_panel = FishDetailPanel(self.bg)
		self.detail_panel.SetRankingEvent(ui.__mem_func__(self._OnClickRanking))
		self.detail_panel.SetGiveEvent(ui.__mem_func__(self._OnClickGiveFish))

		self.ranking_panel = FishRankingPanel(self.bg)
		self.ranking_panel.SetBackEvent(ui.__mem_func__(self._OnClickReturnToStats))

		self.blackboard_loading = ui.ImageBox()
		self.blackboard_loading.SetParent(self.bg)
		self.blackboard_loading.SetPosition(0, 0)
		self.blackboard_loading.LoadImage("kowal/fish_wiki/blackboard_bg.png")
		self.blackboard_loading.Hide()

		# Napis ladowania — byl wpalony w blackboard_bg.png po czesku. Jako dziecko
		# zaslony chowa sie i pokazuje razem z nia.
		self.blackboard_text = ui.TextLine("Tahoma:12")
		self.blackboard_text.SetParent(self.blackboard_loading)
		self.blackboard_text.SetPackedFontColor(0xFFF0F0F0)
		self.blackboard_text.SetPosition(268, 122)
		self.blackboard_text.SetOutline()
		self.blackboard_text.SetHorizontalAlignCenter()
		self.blackboard_text.SetText(localeInfo.FISHWIKI_LOADING)
		self.blackboard_text.Show()

		self.SetSize(self.SIMPLE_WIDTH, self.WINDOW_HEIGHT)
		self.SetCenterPosition()
		self.Hide()

	def _BuildFishList(self):
		self.fish_list_box.RemoveAllItems()
		self.fish_list_items = {}

		categories = self.config_manager.get_categories()
		for i, cat in enumerate(categories):
			slot_widget = FishSlotWidget(i, cat, ui.__mem_func__(self._OnClickFish))
			slot_widget.SetParent(self.fish_list_box)
			self.fish_list_box.AppendItem(slot_widget)
			self.fish_list_items[i] = slot_widget

	# --- Server config callbacks ---

	def on_config_start(self, fish_count, categories_per_row):
		self.config_manager.on_config_start(fish_count, categories_per_row)

	def on_config_fish(self, vnum, needed_count, needed_length, success_chance, reward_type, reward_value):
		self.config_manager.on_config_fish(vnum, needed_count, needed_length, success_chance, reward_type, reward_value)

	def on_config_end(self):
		self.config_manager.on_config_end()

		self.player_fish_data = {}
		for entry in self.config_manager.fish_entries:
			vnum = entry["vnum"]
			self.player_fish_data[vnum] = {
				"count": 0, "best_length": 0, "best_price": 0,
				"mission_progress": 0, "loaded": False,
			}

		self._BuildFishList()

	# --- Server data callbacks ---

	def OnUnlockNewFish(self, fish_vnum):
		if self.new_fish_window is None:
			self.new_fish_window = NewFishFoundWindow()
		self.new_fish_window.OnCatchNewFish(fish_vnum)

	def OnLoadUnlockStatus(self, unlock_data1, unlock_data2):
		unlock_data = [int(unlock_data1), int(unlock_data2)]
		categories = self.config_manager.get_categories()
		per_row = self.config_manager.categories_per_row

		cat_idx = 0
		in_cat_idx = 0
		unlock_idx = 0
		data_idx = 0

		total_fish = self.config_manager.get_fish_count()
		for i in range(total_fish):
			if cat_idx >= len(categories):
				break

			vnum = categories[cat_idx][in_cat_idx]
			if vnum != 0 and cat_idx in self.fish_list_items:
				unlocked = bool(unlock_data[unlock_idx] & (1 << data_idx))
				self.fish_list_items[cat_idx].SetIsUnlocked(in_cat_idx, unlocked)

			in_cat_idx += 1
			if in_cat_idx >= per_row:
				in_cat_idx = 0
				cat_idx += 1

			if data_idx >= 30:
				data_idx = 0
				unlock_idx += 1
			else:
				data_idx += 1

		if not self.IsShow():
			self.Show()

	def OnLoadMyFishData(self, fish_vnum, count, best_length, best_price, mission_progress):
		if fish_vnum in self.player_fish_data:
			self.player_fish_data[fish_vnum] = {
				"count": count, "best_length": best_length,
				"best_price": best_price, "mission_progress": mission_progress,
				"loaded": True,
			}

		selected_vnum = self._GetSelectedFishVnum()
		if selected_vnum == fish_vnum:
			item.SelectItem(fish_vnum)
			mission_data = self.config_manager.get_mission_data(fish_vnum)
			self.detail_panel.Refresh(fish_vnum, self.player_fish_data[fish_vnum], mission_data)

		self.need_close_blackboard = True

	def OnLoadRankingStart(self):
		selected_vnum = self._GetSelectedFishVnum()
		if selected_vnum:
			self.ranking_load_times[selected_vnum] = app.GetGlobalTimeStamp()
			self.ranking_data[selected_vnum] = {}
			for i in range(10):
				self.ranking_data[selected_vnum][i] = ["-----", 0, 0]

	def OnLoadRanking(self, pos, name, length, rod_level):
		selected_vnum = self._GetSelectedFishVnum()
		if selected_vnum and selected_vnum in self.ranking_data:
			self.ranking_data[selected_vnum][pos] = [name, length, rod_level]

	def OnLoadRankingEnd(self):
		selected_vnum = self._GetSelectedFishVnum()
		if selected_vnum and selected_vnum in self.ranking_data:
			self.ranking_panel.Refresh(self.ranking_data[selected_vnum])
		self.need_close_blackboard = True

	def OnLoadError(self, status=""):
		self.need_close_blackboard = True

	# --- UI interaction ---

	def _OnClickFish(self, cat_idx, fish_idx):
		if self.selected_cat_idx != -1 and self.selected_cat_idx in self.fish_list_items:
			self.fish_list_items[self.selected_cat_idx].fishBtns[self.selected_fish_idx].Enable()

		if cat_idx in self.fish_list_items and fish_idx in self.fish_list_items[cat_idx].fishBtns:
			self.fish_list_items[cat_idx].fishBtns[fish_idx].Disable()

		self.selected_cat_idx = cat_idx
		self.selected_fish_idx = fish_idx

		fish_vnum = self._GetSelectedFishVnum()
		if not fish_vnum:
			return

		if self.fish_list_items[cat_idx].is_unlocked[fish_idx]:
			item.SelectItem(fish_vnum)

			mission_data = self.config_manager.get_mission_data(fish_vnum)
			self.detail_panel.Refresh(fish_vnum, self.player_fish_data.get(fish_vnum, {}), mission_data)

			if fish_vnum in self.player_fish_data and not self.player_fish_data[fish_vnum]["loaded"]:
				self.blackboard_loading.Show()
				self.need_close_blackboard = False
				self.blackboard_close_time = app.GetGlobalTime() + 400
				net.SendChatPacket("/fish_wiki 2 %d" % fish_vnum)

			self._SetExpandedPanel(self.PANEL_DETAIL)
		else:
			self._SetExpandedPanel(self.PANEL_LOCKED)

	def _OnClickRanking(self):
		fish_vnum = self._GetSelectedFishVnum()
		if not fish_vnum:
			return

		item.SelectItem(fish_vnum)
		self.ranking_panel.SetTitle(item.GetItemName())
		self._SetExpandedPanel(self.PANEL_RANKING)

		needs_load = (
			fish_vnum not in self.ranking_load_times or
			app.GetGlobalTimeStamp() >= self.ranking_load_times[fish_vnum] + 15 * 60
		)

		if needs_load:
			self.blackboard_loading.Show()
			self.need_close_blackboard = False
			self.blackboard_close_time = app.GetGlobalTime() + 400
			net.SendChatPacket("/fish_wiki 4 %d" % fish_vnum)
		else:
			self.OnLoadRankingEnd()

	def _OnClickGiveFish(self):
		fish_vnum = self._GetSelectedFishVnum()
		if fish_vnum:
			net.SendChatPacket("/fish_wiki 3 %d" % fish_vnum)

	def _OnClickReturnToStats(self):
		self._OnClickFish(self.selected_cat_idx, self.selected_fish_idx)

	# --- Panel management ---

	def _SetExpandedPanel(self, panel_type):
		self.bg.LoadImage("kowal/fish_wiki/bg.png")
		self.board.SetSize(self.EXPANDED_WIDTH, self.WINDOW_HEIGHT)
		self.SetSize(self.EXPANDED_WIDTH, self.WINDOW_HEIGHT)
		self.SetCenterPosition()

		self.locked_panel.Hide()
		self.detail_panel.Hide()
		self.ranking_panel.Hide()

		if panel_type == self.PANEL_LOCKED:
			self.locked_panel.Show()
		elif panel_type == self.PANEL_DETAIL:
			self.detail_panel.Show()
		elif panel_type == self.PANEL_RANKING:
			self.ranking_panel.Show()

	def _SetSimpleBoard(self):
		if self.selected_cat_idx != -1 and self.selected_cat_idx in self.fish_list_items:
			if self.selected_fish_idx in self.fish_list_items[self.selected_cat_idx].fishBtns:
				self.fish_list_items[self.selected_cat_idx].fishBtns[self.selected_fish_idx].Enable()

		self.selected_cat_idx = -1
		self.selected_fish_idx = -1

		self.bg.LoadImage("kowal/fish_wiki/bg_simple.png")
		self.board.SetSize(self.SIMPLE_WIDTH, self.WINDOW_HEIGHT)
		self.SetSize(self.SIMPLE_WIDTH, self.WINDOW_HEIGHT)
		self.SetCenterPosition()

		self.locked_panel.Hide()
		self.detail_panel.Hide()
		self.ranking_panel.Hide()

	# --- Helpers ---

	def _GetSelectedFishVnum(self):
		if self.selected_cat_idx < 0 or self.selected_fish_idx < 0:
			return None

		categories = self.config_manager.get_categories()
		if self.selected_cat_idx >= len(categories):
			return None

		cat = categories[self.selected_cat_idx]
		if self.selected_fish_idx >= len(cat):
			return None

		vnum = cat[self.selected_fish_idx]
		return vnum if vnum != 0 else None

	def _CloseByPlayer(self):
		net.SendChatPacket("/fish_wiki 1")
		self.Close()

	def Close(self):
		self.Hide()
		self._SetSimpleBoard()

	def OnUpdate(self):
		if self.need_close_blackboard:
			if app.GetGlobalTime() >= self.blackboard_close_time:
				self.need_close_blackboard = False
				self.blackboard_loading.Hide()

	def OnPressEscapeKey(self):
		if self.IsShow():
			self._CloseByPlayer()
			return TRUE
		return FALSE


# ---------------------------------------------------------------------------
# NewFishFoundWindow - notification popup
# ---------------------------------------------------------------------------

class NewFishFoundWindow(ui.Window):
	DISPLAY_DURATION = 5
	WINDOW_WIDTH = 264
	WINDOW_HEIGHT = 113

	def __init__(self):
		ui.Window.__init__(self, "TOP_MOST")
		self.close_time = 0
		self._BuildWindow()

	def __del__(self):
		ui.Window.__del__(self)

	def _BuildWindow(self):
		self.AddFlag("float")

		board_bg = ui.ImageBox()
		board_bg.SetParent(self)
		board_bg.SetPosition(0, 0)
		board_bg.LoadImage("kowal/notification/background_item.png")
		board_bg.Show()
		self.board_bg = board_bg

		fish_img = ui.ImageBox()
		fish_img.SetParent(self)
		fish_img.SetPosition(115, 16)
		fish_img.Show()
		self.fish_img = fish_img

		self.SetSize(self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
		self.SetPosition(wndMgr.GetScreenWidth() // 2 - self.WINDOW_WIDTH // 2, 30)
		self.Hide()

	def OnUpdate(self):
		if app.GetGlobalTimeStamp() >= self.close_time:
			self.Hide()

	def OnCatchNewFish(self, fish_vnum):
		self.close_time = app.GetGlobalTimeStamp() + self.DISPLAY_DURATION
		item.SelectItem(fish_vnum)
		self.fish_img.LoadImage(item.GetIconImageFileName())
		self.Show()
