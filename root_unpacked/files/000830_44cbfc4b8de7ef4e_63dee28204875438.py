# -*- coding: utf-8 -*-
"""
Pet System UI — server-authoritative, reads all data from the `pet` C++ module.
No pet data is stored in Python (constInfo) — everything comes from the server
via GC_PET_INFO packets, parsed by CPythonPet and exposed through `pet`.
"""

import pet  # pybind11 module — CPythonPet data store + action senders

import app
import chat
import dbg
import item
import localeInfo
import player
import skill
import ui
import uiScriptLocale
import uiToolTip
import wndMgr
from uiToolTip import ItemToolTip

# ----------------------------------------------
#  Constants
# ----------------------------------------------
AFFECT_DICT = ItemToolTip.AFFECT_DICT

SKILL_COUNT = pet.SKILL_COUNT          # 11
SKILL_VNUM_BASE = pet.SKILL_VNUM_BASE  # 301
MAX_SKILL_LEVEL = pet.MAX_SKILL_LEVEL  # 40
SKILL_LV_BY_POINT = pet.SKILL_LV_BY_POINT  # 10

GRADE_NORMAL_MAX = pet.GRADE_NORMAL_MAX          # 9
GRADE_APPRENTICE_MAX = pet.GRADE_APPRENTICE_MAX  # 19
GRADE_ADEPT_MAX = pet.GRADE_ADEPT_MAX            # 29

SKILL_GRADE_NORMAL = 0
SKILL_GRADE_APPRENTICE = 1
SKILL_GRADE_ADEPT = 2
SKILL_GRADE_MASTER = 3

# Skill activation range: apprentice grade (levels 10-19)
SKILL_ACTIVATE_MIN_LV = GRADE_NORMAL_MAX + 1  # 10
SKILL_ACTIVATE_MAX_LV = MAX_SKILL_LEVEL  # 30

COLOR_AFFECT = 0xFF89B88D

EXP_GAUGE_COUNT = 4
EXP_GAUGE_NAMES = ("exp_gauge_01", "exp_gauge_02", "exp_gauge_03", "exp_gauge_04")
UI_SCRIPT_PATH = "uiscript/petsystemwindow.py"


# ----------------------------------------------
#  Helpers
# ----------------------------------------------
def GetPetSkillName(index: int) -> str:
	"""Return localised skill name or fallback."""
	key = "PET_SKILL_%d" % (index + 1)
	name = getattr(localeInfo, key, "")
	if name and name.strip():
		return name
	try:
		name = skill.GetSkillName(index + SKILL_VNUM_BASE)
		if name and name.strip():
			return name
	except Exception:
		pass
	return "noname"


def _skill_grade(level: int):
	"""Return (display_level, grade) from raw skill level."""
	if level > GRADE_ADEPT_MAX:
		return level - GRADE_ADEPT_MAX, SKILL_GRADE_MASTER
	if level > GRADE_APPRENTICE_MAX:
		return level - GRADE_APPRENTICE_MAX, SKILL_GRADE_ADEPT
	if level > GRADE_NORMAL_MAX:
		return level - GRADE_NORMAL_MAX, SKILL_GRADE_APPRENTICE
	return level, SKILL_GRADE_NORMAL


# ----------------------------------------------
#  TextToolTip  (tiny floating label)
# ----------------------------------------------
class TextToolTip(ui.Window):
	"""Single-line tooltip that follows the mouse cursor."""

	def __init__(self, y_offset: int = 0):
		super().__init__("TOP_MOST")
		self._y_offset = y_offset
		self._line = ui.TextLine()
		self._line.SetParent(self)
		self._line.SetHorizontalAlignLeft()
		self._line.SetOutline()
		self._line.Hide()

	def __del__(self):
		super().__del__()

	def SetText(self, text: str):
		self._line.SetText(text)

	def OnRender(self):
		mx, my = wndMgr.GetMousePosition()
		self._line.SetPosition(mx - 30, my - 30 + self._y_offset)
		self._line.Show()


# ----------------------------------------------
#  PetWindow
# ----------------------------------------------
class PetWindow(ui.ScriptWindow):
	"""Main pet management window — reads all data from `pet` C++ module."""

	def __init__(self, inventory_window=None):
		super().__init__()
		self._inventory = inventory_window
		self._active_skill = -1

		# child refs (populated in _bind_ui)
		self._title_bar = None
		self._exp_hover = None
		self._exp_gauges: list = []
		self._exp_tooltip = None
		self._skill_tooltip = uiToolTip.ToolTip()
		self._skill_tooltip.Hide()

		self._slots_item = None   # main pet slot
		self._slots_equip = None  # pet equipment slots
		self._slots_skill = None  # skill grid
		self._txt_points = None
		self._txt_level = None

		self._load_ui()

	def __del__(self):
		super().__del__()

	# -- lifecycle ----------------------------
	def Destroy(self):
		self.ClearDictionary()
		self._title_bar = None
		self._exp_hover = None
		self._exp_gauges = []
		self._exp_tooltip = None
		self._skill_tooltip = None
		self._slots_item = None
		self._slots_equip = None
		self._slots_skill = None
		self._txt_points = None
		self._txt_level = None

	# -- UI loading ---------------------------
	def _load_ui(self):
		try:
			ui.PythonScriptLoader().LoadScriptFile(self, UI_SCRIPT_PATH)
		except KeyError:
			dbg.TraceError("[PetSystem] Missing script: " + UI_SCRIPT_PATH)
			return
		self.SetCenterPosition()
		self._bind_ui()

	def _bind_ui(self):
		try:
			self._bind_title_bar()
			self._bind_item_slots()
			self._bind_equip_slots()
			self._bind_exp()
			self._bind_skills()
			self.Refresh()
		except KeyError as exc:
			dbg.TraceError("[PetSystem] Bind failed: %s" % str(exc))

	def _bind_title_bar(self):
		self._title_bar = self.GetChild("TitleBar")
		self._title_bar.SetCloseEvent(ui.__mem_func__(self.Close))

	def _bind_item_slots(self):
		slot = self.GetChild("islot")
		self._slots_item = slot
		inv = self._inventory
		slot.SetOverInItemEvent(ui.__mem_func__(inv.OverInItem))
		slot.SetOverOutItemEvent(ui.__mem_func__(inv.OverOutItem))
		slot.SetUnselectItemSlotEvent(ui.__mem_func__(inv.UseItemSlot))
		slot.SetUseSlotEvent(ui.__mem_func__(inv.UseItemSlot))
		slot.SetSelectEmptySlotEvent(ui.__mem_func__(inv.SelectEmptySlot))
		slot.SetSelectItemSlotEvent(ui.__mem_func__(inv.SelectItemSlot))

	def _bind_equip_slots(self):
		slot = self.GetChild("eqs")
		self._slots_equip = slot
		inv = self._inventory
		slot.SetOverInItemEvent(ui.__mem_func__(inv.OverInItem))
		slot.SetOverOutItemEvent(ui.__mem_func__(inv.OverOutItem))
		slot.SetUnselectItemSlotEvent(ui.__mem_func__(inv.UseItemSlot))
		slot.SetUseSlotEvent(ui.__mem_func__(inv.UseItemSlot))
		slot.SetSelectEmptySlotEvent(ui.__mem_func__(inv.SelectEmptySlot))
		slot.SetSelectItemSlotEvent(ui.__mem_func__(inv.SelectItemSlot))

	def _bind_exp(self):
		self._exp_hover = self.GetChild("exp_hover_info")
		self._exp_gauges = [self.GetChild(n) for n in EXP_GAUGE_NAMES]
		for g in self._exp_gauges:
			g.SetSize(0, 0)
			g.Hide()

	def _bind_skills(self):
		sk = self.GetChild("skills")
		self._slots_skill = sk
		self._txt_points = self.GetChild("skill_points")
		self._txt_level = self.GetChild("mount_level")

		sk.SetSlotStyle(wndMgr.SLOT_STYLE_NONE)
		sk.SetOverInItemEvent(ui.__mem_func__(self._OnSkillMouseOver))
		sk.SetOverOutItemEvent(ui.__mem_func__(self._OnSkillMouseOut))
		sk.SetPressedSlotButtonEvent(ui.__mem_func__(self._OnSkillUpgrade))
		sk.SetSelectItemSlotEvent(ui.__mem_func__(self._OnSkillClick))
		sk.SetUnselectItemSlotEvent(ui.__mem_func__(self._OnSkillClick))
		sk.AppendSlotButton(
			"d:/ymir work/ui/game/windows/btn_plus_up.sub",
			"d:/ymir work/ui/game/windows/btn_plus_over.sub",
			"d:/ymir work/ui/game/windows/btn_plus_down.sub",
		)

	# -----------------------------------------
	#  BINARY callbacks (called from C++ via
	#  PyCallClassMemberFunc on game phase window,
	#  which forwards to us)
	# -----------------------------------------
	def BINARY_PetFullSync(self):
		"""Server sent a complete pet data snapshot."""
		self.Refresh()

	def BINARY_PetExpUpdate(self):
		"""Server sent an exp/level update."""
		self._refresh_level()
		self._refresh_exp()
		self._refresh_points()

	def BINARY_PetSkillUpdate(self, skill_index):
		"""Server sent a single skill update."""
		self._refresh_skill(skill_index)
		self._refresh_points()

	def BINARY_PetDismissed(self):
		"""Server dismissed the pet."""
		self.Close()

	# -----------------------------------------
	#  Refresh (reads from `pet` C++ module)
	# -----------------------------------------
	def Refresh(self):
		"""Full UI refresh from current pet data."""
		if not pet.HasPet():
			return

		self._refresh_level()
		self._refresh_exp()
		self._refresh_points()
		self._refresh_all_skills()

	def _refresh_level(self):
		if self._txt_level:
			self._txt_level.SetText("Lv. %d" % pet.GetLevel())

	def _refresh_exp(self):
		cur, need = pet.GetExp()
		self._set_exp(cur, need)

	def _refresh_points(self):
		pts = pet.GetSkillPoints()
		if self._txt_points:
			self._txt_points.SetText(str(pts))
			if pts > 0:
				self._txt_points.Show()

	def _refresh_all_skills(self):
		sk = self._slots_skill
		if not sk:
			return

		try:
			sk.HideAllSlotButton()
		except AttributeError:
			pass
		points = pet.GetSkillPoints()

		for i in range(SKILL_COUNT):
			self._refresh_skill_slot(i, points)

	def _refresh_skill(self, index):
		"""Refresh a single skill slot."""
		sk = self._slots_skill
		if not sk or index < 0 or index >= SKILL_COUNT:
			return

		self._refresh_skill_slot(index, pet.GetSkillPoints())

	def _refresh_skill_slot(self, index, points):
		"""Update a single skill slot's icon, grade, and upgrade button."""
		sk = self._slots_skill
		lv = pet.GetSkillLevel(index)
		disp, grade = _skill_grade(lv)
		sk.SetSkillSlotNew(index, index + SKILL_VNUM_BASE, grade, disp)
		sk.SetSlotCountNew(index, grade, disp)

		if lv < SKILL_LV_BY_POINT and points > 0:
			try:
				sk.ShowSlotButton(index)
			except AttributeError:
				pass
		else:
			try:
				sk.HideSlotButton(index)
			except AttributeError:
				pass

	# -- skills: click / upgrade / tooltip -----
	def _OnSkillClick(self, index: int):
		try:
			if not pet.HasPet() or index >= SKILL_COUNT:
				return

			lv = pet.GetSkillLevel(index)
			if not (SKILL_ACTIVATE_MIN_LV <= lv <= SKILL_ACTIVATE_MAX_LV):
				return

			sk = self._slots_skill
			if not sk:
				return

			if sk.IsActivatedSlot(index):
				sk.DeactivateSlot(index)
				pet.SendSkillDeactivate(index)
			else:
				# Deactivate all first
				for j in range(SKILL_COUNT):
					if sk.IsActivatedSlot(j):
						sk.DeactivateSlot(j)
						pet.SendSkillDeactivate(j)

				sk.ActivateSlot(index)
				pet.SendSkillActivate(index)
				name = GetPetSkillName(index)
				chat.AppendChat(chat.CHAT_TYPE_INFO,
								localeInfo.PET_INFO_3.format(name))
		except Exception as exc:
			dbg.TraceError("[PetSystem] Skill click error: %s" % str(exc))

	def _OnSkillUpgrade(self, index: int):
		now = app.GetTime()
		if hasattr(self, '_lastSkillUpgradeTime') and now - self._lastSkillUpgradeTime < 0.5:
			return
		self._lastSkillUpgradeTime = now
		pet.SendSkillUpgrade(index)

	def _OnSkillMouseOver(self, index: int):
		self._active_skill = index
		self._show_skill_tooltip(index)

	def _OnSkillMouseOut(self):
		if self._skill_tooltip:
			self._skill_tooltip.Hide()

	def _show_skill_tooltip(self, index: int):
		tip = self._skill_tooltip
		tip.ClearToolTip()

		lv = pet.GetSkillLevel(index)
		disp, grade = _skill_grade(lv)

		GRADE_NAMES = [
			getattr(localeInfo, "PET_SKILL_GRADE_NORMAL", "Normal"),
			getattr(localeInfo, "PET_SKILL_GRADE_APPRENTICE", "Apprentice"),
			getattr(localeInfo, "PET_SKILL_GRADE_ADEPT", "Adept"),
			getattr(localeInfo, "PET_SKILL_GRADE_MASTER", "Master"),
		]
		GRADE_COLORS = [0xFFFFFFFF, 0xFF5FD35F, 0xFF559FD3, 0xFFD3A055]
		GRADE_LABEL = getattr(localeInfo, "PET_SKILL_GRADE_LABEL", "Grade: %s  |  Lv. %d")

		grade_name = GRADE_NAMES[grade] if grade < len(GRADE_NAMES) else "?"
		grade_color = GRADE_COLORS[grade] if grade < len(GRADE_COLORS) else 0xFFFFFFFF

		tip.SetTitle(GetPetSkillName(index))
		tip.AppendTextLine(GRADE_LABEL % (grade_name, disp), grade_color)
		tip.AppendSpace(4)

		# Current bonuses — always show bonus name, even at level 0
		has_bonus = False
		for slot in range(2):
			try:
				btype = pet.GetSkillBonusType(index, slot)
				bval = pet.GetSkillBonusValue(index, slot)

				if btype == 0:
					btype = pet.GetNextSkillBonusType(index, slot)
					bval = 0

				if btype == 0:
					continue

				has_bonus = True
				color = COLOR_AFFECT if lv > 0 else 0xFF999999
				if btype in AFFECT_DICT:
					try:
						tip.AppendTextLine(str(AFFECT_DICT[btype](bval)), color)
					except:
						tip.AppendTextLine("Bonus %d: %d" % (btype, bval), color)
				else:
					tip.AppendTextLine("Bonus %d: %d" % (btype, bval), color)
			except:
				pass

		if not has_bonus:
			tip.AppendTextLine(getattr(localeInfo, "PET_SKILL_NO_BONUS", "No bonus"), 0xFF999999)

		# Next level preview
		if lv < MAX_SKILL_LEVEL:
			tip.AppendSpace(6)
			tip.AppendHorizontalLine()
			tip.AppendSpace(4)

			next_lv = lv + 1
			next_disp, next_grade = _skill_grade(next_lv)
			next_grade_name = GRADE_NAMES[next_grade] if next_grade < len(GRADE_NAMES) else "?"

			if next_grade != grade:
				tip.AppendTextLine("Next: %s Lv. %d" % (next_grade_name, next_disp), 0xFFE6C545)
			else:
				tip.AppendTextLine("Next: Lv. %d" % next_disp, 0xFFE6C545)

			try:
				for slot in range(2):
					btype = pet.GetNextSkillBonusType(index, slot)
					bval = pet.GetNextSkillBonusValue(index, slot)
					if btype == 0:
						continue
					if btype in AFFECT_DICT:
						tip.AppendTextLine(str(AFFECT_DICT[btype](bval)), 0xFFE6C545)
					else:
						tip.AppendTextLine("Bonus %d: %d" % (btype, bval), 0xFFE6C545)
			except (AttributeError, KeyError, IndexError):
				# GetNextSkillBonusType/Value might not exist yet
				pass

			# Upgrade hint
			if lv < SKILL_LV_BY_POINT:
				tip.AppendSpace(4)
				tip.AppendTextLine("Use skill points to upgrade", 0xFF888888)
			else:
				tip.AppendSpace(4)
				tip.AppendTextLine("Use skill books to upgrade", 0xFF888888)

		tip.Show()

	def _are_all_skills_maxed(self) -> bool:
		for i in range(SKILL_COUNT):
			if pet.GetSkillLevel(i) < MAX_SKILL_LEVEL:
				return False
		return True

	# -- experience ---------------------------
	def _set_exp(self, cur, cap):
		cur, cap = max(int(cur), 0), max(int(cap), 0)
		pct = (float(cur) / cap * 100.0) if cap > 0 else 0.0
		self._render_exp_gauges(cur, cap)
		self._build_exp_tooltip(cur, cap, pct)

	def _render_exp_gauges(self, cur: int, cap: int):
		for g in self._exp_gauges:
			g.Hide()
		if cap <= 0:
			return

		quarter = cap // 4
		if quarter == 0:
			return

		full = min(4, cur // quarter)
		for i in range(full):
			self._exp_gauges[i].SetRenderingRect(0.0, 0.0, 0.0, 0.0)
			self._exp_gauges[i].Show()

		if full < 4:
			remainder = cur % quarter
			frac = float(remainder) / quarter - 1.0
			self._exp_gauges[full].SetRenderingRect(0.0, frac, 0.0, 0.0)
			self._exp_gauges[full].Show()

	def _build_exp_tooltip(self, cur: int, cap: int, pct: float):
		text = uiScriptLocale.ASLAN_BUFF_HOVER_EXP_INFO % (
			localeInfo.MoneyFormat(int(cur)),
			localeInfo.MoneyFormat(int(cap)),
			pct,
		)
		# Tworzenie nowego TextToolTip na KAZDY pakiet exp oznaczalo tworzenie i niszczenie
		# okna C++ kilka razy na sekunde. Wystarczy zrobic je raz i podmieniac tekst.
		if not self._exp_tooltip:
			self._exp_tooltip = TextToolTip(15)
			self._exp_tooltip.Hide()

		self._exp_tooltip.SetText(text)

	# -- per-frame update ---------------------
	def OnUpdate(self):
		self._tick_tooltips()
		self._tick_item_slots()

	def _tick_tooltips(self):
		# bonus tooltip
		# skill tooltip refresh
		if self._skill_tooltip and self._skill_tooltip.IsShow() and self._slots_skill:
			wndMgr.RefreshSlot(self._slots_skill.GetWindowHandle())

		# exp tooltip
		if self._exp_hover and self._exp_hover.IsIn():
			if self._exp_tooltip:
				self._exp_tooltip.Show()
		else:
			if self._exp_tooltip:
				self._exp_tooltip.Hide()

	def _tick_item_slots(self):
		# main pet slot
		pet_slot = item.SLOT_ITEM_NEW_PET
		self._slots_item.SetItemSlot(pet_slot, player.GetItemIndex(pet_slot), 0)

		# equipment (3 slots)
		eq = self._slots_equip
		if eq:
			for i in range(3):
				s = item.SLOT_ITEM_NEW_PET_EQ_START + i
				eq.SetItemSlot(s, player.GetItemIndex(s), 0)
			eq.RefreshSlot()

	# -- window management --------------------
	def Show(self):
		# Clear UI before showing to avoid stale data from previous character
		self._clear_ui()
		# Request pet info from server (in case it hasn't been sent yet)
		pet.SendRequestInfo()
		super().Show()
		# Refresh data if pet exists (in case sync arrived before open)
		if pet.HasPet():
			self.Refresh()

	def _clear_ui(self):
		"""Clear all UI data (used on show and close)."""
		if self._slots_skill:
			for i in range(SKILL_COUNT):
				self._slots_skill.DeactivateSlot(i)
				self._slots_skill.ClearSlot(i)

		if self._txt_level:
			self._txt_level.SetText("")
		if self._txt_points:
			self._txt_points.SetText("")
		for g in self._exp_gauges:
			g.SetSize(0, 0)
			g.Hide()

		if self._exp_tooltip:
			self._exp_tooltip.Hide()

	def Close(self):
		self._clear_ui()
		self.Hide()
		self._OnSkillMouseOut()

	def OnPressEscapeKey(self):
		self.Close()
		return True
