# -*- coding: utf-8 -*-
"""
Companion Window — combined Pet + Mount UI with tab switching.
Pet tab: reads all data from `pet` C++ module (server-authoritative).
Mount tab: receives data via BINARY_SetMountInfo callback.
"""

import pet

import app
import chat
import chrmgr
import nonplayer
import constInfo
import dbg
import item
import localeInfo
import mouseModule
import net
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

SKILL_COUNT = pet.SKILL_COUNT
SKILL_VNUM_BASE = pet.SKILL_VNUM_BASE
MAX_SKILL_LEVEL = pet.MAX_SKILL_LEVEL
SKILL_LV_BY_POINT = pet.SKILL_LV_BY_POINT

GRADE_NORMAL_MAX = pet.GRADE_NORMAL_MAX
GRADE_APPRENTICE_MAX = pet.GRADE_APPRENTICE_MAX
GRADE_ADEPT_MAX = pet.GRADE_ADEPT_MAX

SKILL_GRADE_NORMAL = 0
SKILL_GRADE_APPRENTICE = 1
SKILL_GRADE_ADEPT = 2
SKILL_GRADE_MASTER = 3

SKILL_ACTIVATE_MIN_LV = GRADE_NORMAL_MAX + 1
SKILL_ACTIVATE_MAX_LV = MAX_SKILL_LEVEL

COLOR_AFFECT = 0xFF89B88D

# Komplet umiejetnosci na "P" NIE daje zadnej premii - serwer (PetSystem.cpp CalcBonus)
# wysyla goly bonus z tabeli umiejetnosci. Bylo tu odtwarzanie +30% z wartosci koncowej.

EXP_GAUGE_COUNT = 4

# Mount bonus information
# Lustro s_vecMountBonus z Server/game/src/char.cpp - klient tylko odwzorowuje to, co
# serwer nalicza w ComputePoints. Indeks = surowy poziom wierzchowca (0 = swiezy, bez
# bonusow), dlugosc MOUNT_MAX_LEVEL+1. Progi co 5 poziomow, wartosci docelowe od 21.
# Przebudowa 2026-08-06: bylo 150 poziomow i bonusy na metiny/bossy zamiast bloku
# i odpornosci; predkosc byla fikcja - serwer jej wtedy w ogole nie naliczal.
MOUNT_MAX_LEVEL = 25
MOUNT_BONUS_INFO = (
	(localeInfo.MOUNT_TOOLTIP_APPLY_ATTBONUS_MONSTER, (0, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5)),
	(localeInfo.MOUNT_TOOLTIP_BLOCK, (0, 2, 2, 2, 2, 2, 4, 4, 4, 4, 4, 6, 6, 6, 6, 6, 8, 8, 8, 8, 8, 10, 10, 10, 10, 10)),
	(localeInfo.MOUNT_TOOLTIP_RESIST_MONSTER, (0, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5)),
	(localeInfo.MOUNT_TOOLTIP_MOUNT_SPEED, (0, 2, 2, 4, 4, 6, 6, 8, 8, 10, 10, 12, 12, 14, 14, 16, 16, 18, 18, 20, 20, 22, 22, 24, 24, 26)),
)


# ----------------------------------------------
#  Helpers
# ----------------------------------------------
def GetPetSkillName(index):
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


def _skill_grade(level):
	if level > GRADE_ADEPT_MAX:
		return level - GRADE_ADEPT_MAX, SKILL_GRADE_MASTER
	if level > GRADE_APPRENTICE_MAX:
		return level - GRADE_APPRENTICE_MAX, SKILL_GRADE_ADEPT
	if level > GRADE_NORMAL_MAX:
		return level - GRADE_NORMAL_MAX, SKILL_GRADE_APPRENTICE
	return level, SKILL_GRADE_NORMAL


# ----------------------------------------------
#  TextToolTip (tiny floating label)
# ----------------------------------------------
class TextToolTip(ui.Window):
	def __init__(self, y_offset=0):
		super().__init__("TOP_MOST")
		self._y_offset = y_offset
		self._line = ui.TextLine()
		self._line.SetParent(self)
		self._line.SetHorizontalAlignLeft()
		self._line.SetOutline()
		self._line.Hide()

	def __del__(self):
		super().__del__()

	def SetText(self, text):
		self._line.SetText(text)

	def OnRender(self):
		mx, my = wndMgr.GetMousePosition()
		self._line.SetPosition(mx - 30, my - 30 + self._y_offset)
		self._line.Show()


# ----------------------------------------------
#  CompanionWindow
# ----------------------------------------------
class CompanionWindow(ui.ScriptWindow):
	MODE_PET = 0
	MODE_MOUNT = 1

	def __init__(self, wnd_inventory=None):
		super().__init__()
		self.wnd_inventory = wnd_inventory
		self.current_mode = self.MODE_PET
		self._active_skill = -1
		self.tooltipItem = None
		self._skill_tooltip = uiToolTip.ToolTip()
		self._skill_tooltip.Hide()
		self._exp_tooltip = None
		self._mount_exp_tooltip = None
		self.mountLevel = 0
		self._awaiting_pet_info = False
		self._lastPetInfoRequest = 0.0

		self.title_bar = None
		self.pet_button = None
		self.mount_button = None
		self.board_01 = None
		self.board_02 = None

		self.pet_components = {}
		self.mount_components = {}

		self._load_ui()

	def __del__(self):
		super().__del__()

	def Destroy(self):
		self.ClearDictionary()

	def _load_ui(self):
		try:
			ui.PythonScriptLoader().LoadScriptFile(self, "uiscript/companionwindow.py")
		except KeyError:
			dbg.TraceError("[Companion] Error loading UI")
			return
		self.SetCenterPosition()
		self._bind_ui_objects()

	def _bind_ui_objects(self):
		try:
			self.title_bar = self.GetChild("TitleBar")
			self.title_bar.SetCloseEvent(ui.__mem_func__(self.Close))

			self.board_01 = self.GetChild("board_01")
			self.board_02 = self.GetChild("board_02")

			self._bind_pet_components()
			self._bind_mount_components()
			self.SwitchToPetMode()
		except KeyError as e:
			dbg.TraceError("[Companion] Bind error: {}".format(str(e)))

	# ==============================
	#  PET TAB (C++ pet module)
	# ==============================
	def _bind_pet_components(self):
		try:
			self.pet_components['skill_points'] = self.GetChild("skill_points")
			self.pet_components['pet_level'] = self.GetChild("pet_level")
			self.pet_components['pet_name'] = self.GetChild("pet_name")
			self.pet_components['petFeedItem'] = self.GetChild("pet_feed_item")
			self.pet_components['exp_hover_info'] = self.GetChild("exp_hover_info")

			gauge_names = ["exp_gauge_01", "exp_gauge_02", "exp_gauge_03", "exp_gauge_04"]
			self.pet_components['exp_gauges'] = [self.GetChild(n) for n in gauge_names]
			for g in self.pet_components['exp_gauges']:
				g.SetSize(0, 0)
				g.Hide()

			self.pet_components['islot'] = self.GetChild("islot")
			slot = self.pet_components['islot']
			inv = self.wnd_inventory
			slot.SetOverInItemEvent(ui.__mem_func__(inv.OverInItem))
			slot.SetOverOutItemEvent(ui.__mem_func__(inv.OverOutItem))
			slot.SetUnselectItemSlotEvent(ui.__mem_func__(inv.UseItemSlot))
			slot.SetUseSlotEvent(ui.__mem_func__(inv.UseItemSlot))
			slot.SetSelectEmptySlotEvent(ui.__mem_func__(inv.SelectEmptySlot))
			slot.SetSelectItemSlotEvent(ui.__mem_func__(inv.SelectItemSlot))

			self.pet_components['skills'] = self.GetChild("skills")
			sk = self.pet_components['skills']
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

			self.pet_components['eqs'] = self.GetChild("eqs")
			eqs = self.pet_components['eqs']
			eqs.SetOverInItemEvent(ui.__mem_func__(inv.OverInItem))
			eqs.SetOverOutItemEvent(ui.__mem_func__(inv.OverOutItem))
			eqs.SetUnselectItemSlotEvent(ui.__mem_func__(inv.UseItemSlot))
			eqs.SetUseSlotEvent(ui.__mem_func__(inv.UseItemSlot))
			eqs.SetSelectEmptySlotEvent(ui.__mem_func__(inv.SelectEmptySlot))
			eqs.SetSelectItemSlotEvent(ui.__mem_func__(inv.SelectItemSlot))

			self.PetRefresh()
		except KeyError as e:
			dbg.TraceError("[Companion] Pet bind error: {}".format(str(e)))

	# -- BINARY callbacks (forwarded from game.py) --
	def BINARY_PetFullSync(self):
		self._awaiting_pet_info = False
		self.PetRefresh()

	def BINARY_PetExpUpdate(self):
		self._refresh_pet_level()
		self._refresh_pet_exp()
		self._refresh_pet_points()

	def BINARY_PetSkillUpdate(self, skill_index):
		self._refresh_all_pet_skills()
		self._refresh_pet_points()

	def BINARY_PetDismissed(self):
		if self._awaiting_pet_info:
			# This is a response to our SendRequestInfo() — it means no pet is equipped.
			# Do NOT close the window; just clear the flag and refresh to show empty state.
			self._awaiting_pet_info = False
			self.PetRefresh()
			return
		if self.current_mode == self.MODE_PET:
			self.Close()

	# -- Pet refresh --
	def PetRefresh(self):
		self._update_pet_item_slots()
		if not pet.HasPet():
			# Bez danych z serwera nie zostawiamy nieaktualnych ikon i poziomow w oknie -
			# inaczej sloty daja sie najechac myszka i tooltip klamie ("Poz. 0", "No bonus").
			self._clear_pet_ui()
			return
		self._refresh_pet_name()
		self._refresh_pet_level()
		self._refresh_pet_exp()
		self._refresh_pet_points()
		self._refresh_all_pet_skills()

	def _clear_pet_ui(self):
		"""Reset widocznego stanu pupila po Dismissed / braku FullSync."""
		sk = self.pet_components.get('skills')
		if sk:
			for i in range(SKILL_COUNT):
				if sk.IsActivatedSlot(i):
					sk.DeactivateSlot(i)
				# ClearSlot, NIE ClearAllSlot - to drugie wola CSlotWindow::Destroy(),
				# ktore kasuje m_SlotList i przycisk "+" (AppendSlotButton), wiec siatka
				# skilli juz nigdy by sie nie odbudowala.
				sk.ClearSlot(i)
			try:
				sk.HideAllSlotButton()
			except AttributeError:
				pass
		if self.pet_components.get('pet_name'):
			self.pet_components['pet_name'].SetText("")
		if self.pet_components.get('pet_level'):
			self.pet_components['pet_level'].SetText("")
		if self.pet_components.get('skill_points'):
			self.pet_components['skill_points'].SetText("0")
		self._set_pet_exp(0, 0)
		self._OnSkillMouseOut()

	def _request_pet_info(self):
		"""Dopytanie serwera o stan pupila, max raz na 2 s."""
		now = app.GetTime()
		if now - self._lastPetInfoRequest < 2.0:
			return
		self._lastPetInfoRequest = now
		self._awaiting_pet_info = True
		pet.SendRequestInfo()

	def _refresh_pet_name(self):
		if self.pet_components.get('pet_name'):
			try:
				rawName = pet.GetName()
				mobVnum = pet.GetMobVnum()
				if mobVnum and "MN;" in rawName or "(" in rawName:
					ownerName = rawName.split("(")[0].strip() if "(" in rawName else rawName
					mobName = nonplayer.GetMonsterName(mobVnum)
					if mobName and mobName.strip():
						self.pet_components['pet_name'].SetText("%s (%s)" % (ownerName, mobName))
					else:
						self.pet_components['pet_name'].SetText(ownerName)
				else:
					self.pet_components['pet_name'].SetText(rawName)
			except:
				pass

	def _refresh_pet_level(self):
		level = pet.GetLevel()
		if self.pet_components.get('pet_level'):
			self.pet_components['pet_level'].SetText("Lv. %d" % level)

		if self.pet_components.get('petFeedItem'):
			if level < 40:
				self.pet_components['petFeedItem'].SetText(uiScriptLocale.COMPANION_PET_EXP_WITH_CHAR)
			elif level < 70:
				self.pet_components['petFeedItem'].SetText("|Eemoji/feed_pet_1|e" + uiScriptLocale.COMPANION_PET_FEED_1)
			elif level <= 110:
				self.pet_components['petFeedItem'].SetText("|Eemoji/feed_pet_2|e" + uiScriptLocale.COMPANION_PET_FEED_2)
			else:
				self.pet_components['petFeedItem'].SetText("|Eemoji/feed_pet_3|e" + uiScriptLocale.COMPANION_PET_FEED_3)

	def _refresh_pet_exp(self):
		cur, need = pet.GetExp()
		self._set_pet_exp(cur, need)

	def _refresh_pet_points(self):
		pts = pet.GetSkillPoints()
		if self.pet_components.get('skill_points'):
			self.pet_components['skill_points'].SetText(str(pts))
			self.pet_components['skill_points'].Show()

	def _refresh_all_pet_skills(self):
		sk = self.pet_components.get('skills')
		if not sk:
			return
		try:
			sk.HideAllSlotButton()
		except AttributeError:
			pass
		pts = pet.GetSkillPoints()
		for i in range(SKILL_COUNT):
			self._refresh_pet_skill_slot(i, pts)

	def _refresh_pet_skill(self, index):
		sk = self.pet_components.get('skills')
		if not sk or index < 0 or index >= SKILL_COUNT:
			return
		self._refresh_pet_skill_slot(index, pet.GetSkillPoints())

	def _refresh_pet_skill_slot(self, index, points):
		sk = self.pet_components.get('skills')
		if not sk:
			return
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

	# -- Skill interaction --
	def _OnSkillClick(self, index):
		try:
			if not pet.HasPet() or index >= SKILL_COUNT:
				return
			lv = pet.GetSkillLevel(index)
			if not (SKILL_ACTIVATE_MIN_LV <= lv <= SKILL_ACTIVATE_MAX_LV):
				return
			sk = self.pet_components.get('skills')
			if not sk:
				return
			if sk.IsActivatedSlot(index):
				sk.DeactivateSlot(index)
				pet.SendSkillDeactivate(index)
			else:
				for j in range(SKILL_COUNT):
					if sk.IsActivatedSlot(j):
						sk.DeactivateSlot(j)
						pet.SendSkillDeactivate(j)
				sk.ActivateSlot(index)
				pet.SendSkillActivate(index)
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.PET_INFO_3.format(GetPetSkillName(index)))
		except Exception as e:
			dbg.TraceError("[Companion] Skill click error: {}".format(str(e)))

	def _OnSkillUpgrade(self, index):
		now = app.GetTime()
		if hasattr(self, '_lastSkillUpgradeTime') and now - self._lastSkillUpgradeTime < 0.5:
			return
		self._lastSkillUpgradeTime = now
		pet.SendSkillUpgrade(index)

	def _OnSkillMouseOver(self, index):
		self._active_skill = index
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

		tip.SetTitle(GetPetSkillName(index))
		tip.AppendTextLine(GRADE_LABEL % (GRADE_NAMES[grade], disp), GRADE_COLORS[grade])
		tip.AppendSpace(4)

		# Brak danych z serwera (Dismissed / brak FullSync) => bonus_type[] = 0 dla WSZYSTKICH
		# skilli. Bez tego rozroznienia tooltip pokazywal "No bonus", czyli komunikat o skillu
		# bez bonusu - mylacy, bo bonus istnieje, tylko klient go nie dostal.
		if not pet.HasPet():
			tip.AppendTextLine(getattr(localeInfo, "PET_SKILL_DATA_MISSING",
									   "Pet data not loaded - reopen the window"), 0xFFFF8888)
			self._request_pet_info()
			tip.Show()
			return

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

		tip.Show()

	def _OnSkillMouseOut(self):
		if self._skill_tooltip:
			self._skill_tooltip.Hide()

	def _deactivate_all_skills(self):
		sk = self.pet_components.get('skills')
		if sk:
			for i in range(SKILL_COUNT):
				if sk.IsActivatedSlot(i):
					sk.DeactivateSlot(i)
			pet.SendSkillDeactivate(0)

	# -- Pet EXP --
	def _set_pet_exp(self, cur, cap):
		cur, cap = max(int(cur), 0), max(int(cap), 0)
		pct = (float(cur) / cap * 100.0) if cap > 0 else 0.0
		self._render_gauges(self.pet_components.get('exp_gauges', []), cur, cap)
		txt = uiScriptLocale.ASLAN_BUFF_HOVER_EXP_INFO % (localeInfo.MoneyFormat(int(cur)), localeInfo.MoneyFormat(int(cap)), pct)
		# jw. - okno tworzone raz, potem tylko podmiana tekstu (bylo tworzone na kazdy pakiet exp)
		if not self._exp_tooltip:
			self._exp_tooltip = TextToolTip(15)
			self._exp_tooltip.Hide()

		self._exp_tooltip.SetText(txt)

	# -- Pet item slots --
	def _update_pet_item_slots(self):
		pet_slot = item.SLOT_ITEM_NEW_PET
		islot = self.pet_components.get('islot')
		if islot:
			islot.SetItemSlot(pet_slot, player.GetItemIndex(pet_slot), 0)

		eqs = self.pet_components.get('eqs')
		if eqs:
			for i in range(3):
				s = item.SLOT_ITEM_NEW_PET_EQ_START + i
				eqs.SetItemSlot(s, player.GetItemIndex(s), 0)
			eqs.RefreshSlot()

	# ==============================
	#  MOUNT TAB
	# ==============================
	def _bind_mount_components(self):
		try:
			self.mount_components['equipSlots'] = self.GetChild("equip_slot")
			self.mount_components['costumeSlot'] = self.GetChild("costume_slot")
			self.mount_components['value_name'] = self.GetChild("value_name")
			self.mount_components['valueLevel'] = self.GetChild("value_level")
			self.mount_components['mountFeedItem'] = self.GetChild("mount_feed_item")
			self.mount_components['mount_exp_hover_info'] = self.GetChild("mount_exp_hover_info")

			mount_gauge_names = ["mount_exp_gauge_01", "mount_exp_gauge_02", "mount_exp_gauge_03", "mount_exp_gauge_04"]
			self.mount_components['exp_gauges'] = [self.GetChild(n) for n in mount_gauge_names]
			for g in self.mount_components['exp_gauges']:
				g.SetSize(0, 0)
				g.Hide()

			self.mount_components['mountButton'] = self.GetChild("mount_button")
			self.mount_components['mountButtonUnsummon'] = self.GetChild("mount_button_unsummon")

			self.mount_components['bonusLabels'] = {
				'att_bonus_monster': self.GetChild("label_att_bonus_monster"),
				'block_chance': self.GetChild("label_block_chance"),
				'resist_monster': self.GetChild("label_resist_monster"),
				'mount_movement_speed': self.GetChild("label_mount_movement_speed"),
			}

			inv = self.wnd_inventory
			for slot_comp in [self.mount_components['equipSlots'], self.mount_components['costumeSlot']]:
				slot_comp.SetOverInItemEvent(ui.__mem_func__(inv.OverInItem))
				slot_comp.SetOverOutItemEvent(ui.__mem_func__(inv.OverOutItem))
				slot_comp.SetUnselectItemSlotEvent(ui.__mem_func__(inv.UseItemSlot))
				slot_comp.SetUseSlotEvent(ui.__mem_func__(inv.UseItemSlot))
				slot_comp.SetSelectEmptySlotEvent(ui.__mem_func__(inv.SelectEmptySlot))
				slot_comp.SetSelectItemSlotEvent(ui.__mem_func__(inv.SelectItemSlot))

			self.mount_components['mountButtonUnsummon'].SetEvent(ui.__mem_func__(self.__UnsummonMount))
			self.mount_components['mountButton'].SetEvent(ui.__mem_func__(self.__SummonMount))
		except KeyError as e:
			dbg.TraceError("[Companion] Mount bind error: {}".format(str(e)))

	def SetBasicInfo(self, vnum, name, level, exp, req_exp, summoned):
		# Ensure name is a valid non-empty str (C++ may send bytes or empty string)
		if isinstance(name, bytes):
			try:
				name = name.decode("utf-8", errors="replace")
			except Exception:
				name = ""
		if not isinstance(name, str):
			name = str(name)
		if not name or not name.strip() or name.startswith("[MN;"):
			# Fallback: use mob name from NonPlayer table
			try:
				name = nonplayer.GetMonsterName(int(vnum))
			except Exception:
				name = ""
			if not name or not name.strip():
				name = "Mount"
		self.mount_components['value_name'].SetOutline()
		self.mount_components['value_name'].SetText(name)
		self.mount_components['valueLevel'].SetOutline()
		self.mount_components['valueLevel'].SetText(str(level))
		self.mountLevel = level

		try:
			self.UpdateBonusLabels(level)
		except Exception as e:
			dbg.TraceError("[Companion] UpdateBonusLabels error (level=%d): %s" % (level, str(e)))

		if level <= 24:
			self.mount_components['mountFeedItem'].SetText("|Eemoji/feed_1|e" + localeInfo.MOUNT_WINDOW_FEED_ITEM_1)
		elif level <= 49:
			self.mount_components['mountFeedItem'].SetText("|Eemoji/feed_2|e" + localeInfo.MOUNT_WINDOW_FEED_ITEM_2)
		elif level <= 74:
			self.mount_components['mountFeedItem'].SetText("|Eemoji/feed_3|e" + localeInfo.MOUNT_WINDOW_FEED_ITEM_3)
		else:
			self.mount_components['mountFeedItem'].SetText("|Eemoji/feed_4|e" + localeInfo.MOUNT_WINDOW_FEED_ITEM_4)

		self._set_mount_exp(exp, req_exp)

		if summoned:
			self.mount_components['mountButton'].Hide()
			self.mount_components['mountButtonUnsummon'].Show()
		else:
			self.mount_components['mountButton'].Show()
			self.mount_components['mountButtonUnsummon'].Hide()

	def _set_mount_exp(self, cur, cap):
		cur, cap = max(int(cur), 0), max(int(cap), 0)
		pct = (float(cur) / cap * 100.0) if cap > 0 else 0.0
		self._render_gauges(self.mount_components.get('exp_gauges', []), cur, cap)
		txt = uiScriptLocale.ASLAN_BUFF_HOVER_EXP_INFO % (localeInfo.MoneyFormat(int(cur)), localeInfo.MoneyFormat(int(cap)), pct)
		# jw.
		if not self._mount_exp_tooltip:
			self._mount_exp_tooltip = TextToolTip(15)
			self._mount_exp_tooltip.Hide()

		self._mount_exp_tooltip.SetText(txt)

	def UpdateBonusLabels(self, level):
		# Indeksujemy SUROWYM poziomem, tak jak serwer (char.cpp: s_vecMountBonus
		# czytane przez GetMountLevel()). Wczesniej bylo level-1, przez co okno
		# pokazywalo wartosc o jeden prog nizsza niz gracz faktycznie dostawal.
		max_idx = len(MOUNT_BONUS_INFO[0][1]) - 1
		idx = max(0, min(level, max_idx))
		att_monster = MOUNT_BONUS_INFO[0][1][idx]
		block_chance = MOUNT_BONUS_INFO[1][1][idx]
		resist_monster = MOUNT_BONUS_INFO[2][1][idx]
		mount_speed = MOUNT_BONUS_INFO[3][1][idx]

		fmt = "|cff95876e|H|h{}|H|h: |cffc2bba5|H|h+{}%|H|h"
		self.mount_components['bonusLabels']['att_bonus_monster'].SetText(fmt.format(localeInfo.MOUNT_TOOLTIP_APPLY_ATTBONUS_MONSTER, att_monster))
		self.mount_components['bonusLabels']['block_chance'].SetText(fmt.format(localeInfo.MOUNT_TOOLTIP_BLOCK, block_chance))
		self.mount_components['bonusLabels']['resist_monster'].SetText(fmt.format(localeInfo.MOUNT_TOOLTIP_RESIST_MONSTER, resist_monster))
		self.mount_components['bonusLabels']['mount_movement_speed'].SetText(fmt.format(localeInfo.MOUNT_TOOLTIP_MOUNT_SPEED, mount_speed))

	def __UnsummonMount(self):
		net.SendChatPacket("/horse_unsummon")

	def __SummonMount(self):
		net.SendChatPacket("/horse_summon")

	def RefreshMountEquipmentSlots(self):
		getItemVNum = player.GetItemIndex
		slotStart = item.MOUNT_SLOT_START - 1
		for i in range(item.MOUNT_SLOT_COUNT):
			self.mount_components['equipSlots'].SetItemSlot(slotStart + i, getItemVNum(slotStart + i), 0)
		self.mount_components['equipSlots'].RefreshSlot()
		self.mount_components['costumeSlot'].SetItemSlot(item.COSTUME_SLOT_MOUNT, getItemVNum(item.COSTUME_SLOT_MOUNT), 0)
		self.mount_components['costumeSlot'].RefreshSlot()

	# ==============================
	#  SHARED
	# ==============================
	def _render_gauges(self, gauges, cur, cap):
		for g in gauges:
			g.Hide()
		if cap <= 0:
			return
		quarter = cap // 4
		if quarter == 0:
			return
		full = min(4, cur // quarter)
		for i in range(full):
			gauges[i].SetRenderingRect(0.0, 0.0, 0.0, 0.0)
			gauges[i].Show()
		if full < 4:
			remainder = cur % quarter
			frac = float(remainder) / quarter - 1.0
			gauges[full].SetRenderingRect(0.0, frac, 0.0, 0.0)
			gauges[full].Show()

	def SetItemToolTip(self, itemTooltip):
		self.tooltipItem = itemTooltip

	# -- Tab switching --
	def SwitchToPetMode(self):
		self.current_mode = self.MODE_PET
		self.board_01.Show()
		self.board_02.Hide()
		if self.IsShow():
			self._awaiting_pet_info = True
			pet.SendRequestInfo()
		self.PetRefresh()

	def SwitchToMountMode(self):
		self.current_mode = self.MODE_MOUNT
		self.board_01.Hide()
		self.board_02.Show()
		self.RefreshMountEquipmentSlots()

	# -- Window management --
	def Open(self):
		if self.IsShow():
			self.Close()
		else:
			self.SetCenterPosition()
			self.Show()
			if self.current_mode == self.MODE_PET:
				self._awaiting_pet_info = True
				pet.SendRequestInfo()
				self.PetRefresh()
			else:
				self.RefreshMountEquipmentSlots()

	def Close(self):
		self._awaiting_pet_info = False
		self._deactivate_all_skills()
		if self._exp_tooltip:
			self._exp_tooltip.Hide()
		if self._mount_exp_tooltip:
			self._mount_exp_tooltip.Hide()
		if self.tooltipItem:
			self.tooltipItem.HideToolTip()
		self.Hide()
		self._OnSkillMouseOut()

	def OnPressEscapeKey(self):
		self.Close()
		return True

	# -- Per-frame update --
	def OnUpdate(self):
		if self.current_mode == self.MODE_PET:
			# Skill tooltip refresh
			if self._skill_tooltip and self._skill_tooltip.IsShow():
				sk = self.pet_components.get('skills')
				if sk:
					wndMgr.RefreshSlot(sk.GetWindowHandle())

			# EXP tooltip
			eh = self.pet_components.get('exp_hover_info')
			if eh and eh.IsIn():
				if self._exp_tooltip:
					self._exp_tooltip.Show()
			else:
				if self._exp_tooltip:
					self._exp_tooltip.Hide()

			# Item slots
			self._update_pet_item_slots()

			# Auto-deactivate maxed skills
			sk = self.pet_components.get('skills')
			if sk and pet.HasPet():
				for i in range(SKILL_COUNT):
					if pet.GetSkillLevel(i) > GRADE_ADEPT_MAX and sk.IsActivatedSlot(i):
						sk.DeactivateSlot(i)
						pet.SendSkillDeactivate(i)

		elif self.current_mode == self.MODE_MOUNT:
			self.RefreshMountEquipmentSlots()
			meh = self.mount_components.get('mount_exp_hover_info')
			if meh and meh.IsIn():
				if self._mount_exp_tooltip:
					self._mount_exp_tooltip.Show()
			else:
				if self._mount_exp_tooltip:
					self._mount_exp_tooltip.Hide()
