import ui
import mouseModule
import net
import uiCommon
import localeInfo
import player
import item
import dbg
import snd
import app
import uiScriptLocale
import sndLevelMgr
import grp
from _weakref import proxy

import uiToolTip
AFFECT_DICT = uiToolTip.ItemToolTip.AFFECT_DICT_POLY


LEVEL_NAMES = {
	0 : localeInfo.SECONDARY_LEVEL_0,
	1 : localeInfo.SECONDARY_LEVEL_1,
	2 : localeInfo.SECONDARY_LEVEL_2,
	3 : localeInfo.SECONDARY_LEVEL_3,
	4 : localeInfo.SECONDARY_LEVEL_4,
	5 : localeInfo.SECONDARY_LEVEL_5,
	6 : localeInfo.SECONDARY_LEVEL_6,
	7 : localeInfo.SECONDARY_LEVEL_7,
	8 : localeInfo.SECONDARY_LEVEL_8,
	9 : localeInfo.SECONDARY_LEVEL_9,
	10 : localeInfo.SECONDARY_LEVEL_10,
	11 : localeInfo.SECONDARY_LEVEL_11,
	12 : localeInfo.SECONDARY_LEVEL_12,
	13 : localeInfo.SECONDARY_LEVEL_13,
	14 : localeInfo.SECONDARY_LEVEL_14,
	15 : localeInfo.SECONDARY_LEVEL_15,
}

def GetAffectString(affectType, affectValue):
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
		
def GetSplittedBonus(text, offset = 0):
	index = text.rindex(' ')+1 - offset
	apply = text[:index]
	value = text[index:]
	return (apply, value)

class SecondaryLevelWindow(ui.ScriptWindow):
	# odswiezanie co 333 ms i blokada przyciskow na 3.3 s - tyle wynosily stare liczniki
	# klatkowe (20 i 200 klatek) przy 60 FPS. Teraz nie zaleza od FPS.
	REFRESH_INTERVAL_MS = 333
	LOCK_BUTTON_MS      = 3333

	# Prawa kolumna okna to CALA sekcja awansu - nastepna ranga, jej bonusy, szanse,
	# koszty i oba przyciski. Na maksymalnym poziomie nie ma nastepnego poziomu, wiec
	# musi zniknac; inaczej "nastepny poziom" pokazywal ten sam poziom co obecny
	# (nextLevel = min(currentLevel + 1, max(LEVEL_NAMES))).
	# ItemSlot / required_items NIE nalezy tu ruszac - siedzi w LEWEJ kolumnie.
	NEXT_SECTION_CONTAINER = "next_level_section"

	def __init__(self):
		self.tooltipItem = None
		self.__questionDialog = None
		self.__loaded = False
		self.__lastRefreshTime = 0
		self.__lockBtnEndTime = 0
		
		self.actualBonusListImages = []
		self.actualBonusListTypeTexts = []
		self.actualBonusListValueTexts = []
		
		self.nextBonusListImages = []
		self.nextBonusListTypeTexts = []
		self.nextBonusListValueTexts = []
			
		ui.ScriptWindow.__init__(self)
		self.__LoadWindow()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def SetItemToolTip(self, itemToolTip):
		self.tooltipItem = proxy(itemToolTip)

	def __LoadWindow(self):
		try:
			pythonScriptLoader = ui.PythonScriptLoader()
			pythonScriptLoader.LoadScriptFile(self, "uiscript/secondarylevelwindow.py")
			
			self.requiredItems = self.GetChild("ItemSlot")
			self.actualRank = self.GetChild("actual_rank")
			self.acutalTextRank = self.GetChild("actual_rank_text")
			self.nextRank = self.GetChild("next_rank")
			self.nextTextRank = self.GetChild("next_rank_text")
			
			self.opt1Chance = self.GetChild("option1_chance")
			self.opt1Cost = self.GetChild("option1_cost")
			self.opt1Button = self.GetChild("option1_button")
			
			self.opt2Chance = self.GetChild("option2_chance")
			self.opt2Cost = self.GetChild("option2_cost")
			self.opt2Button = self.GetChild("option2_button")
		except:
			import exception
			exception.Abort("RemoveItemDialog.__LoadWindow.LoadObject")
			
		self.GetChild("board").SetCloseEvent(ui.__mem_func__(self.Close))
		self.requiredItems.SetOverInItemEvent(ui.__mem_func__(self.OverInItem))
		self.requiredItems.SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))
		
		self.opt1Button.SetEvent(ui.__mem_func__(self.SelectOption1))
		self.opt2Button.SetEvent(ui.__mem_func__(self.SelectOption2))
			
		y = 47
		for i in range(5):
			img = ui.ImageBox()
			img.SetParent(self.GetChild("actual_bonus_list"))
			img.SetPosition(6, y)
			img.Show()
			
			txt = ui.TextLine()
			txt.SetParent(img)
			txt.SetPosition(20, 4)
			txt.SetPackedFontColor(grp.GenerateColor(0.6705, 0.6705, 0.6705, 1.0))
			txt.Show()
			
			txt2 = ui.TextLine()
			txt2.SetParent(img)
			txt2.SetPosition(215, 4)
			txt2.SetHorizontalAlignCenter()
			txt2.SetPackedFontColor(grp.GenerateColor(0.4078, 1.0, 0.4666, 1.0))
			txt2.Show()
			
			self.actualBonusListImages.append(img)
			self.actualBonusListTypeTexts.append(txt)
			self.actualBonusListValueTexts.append(txt2)
			y += 22
			
		y = 47
		for i in range(5):
			img = ui.ImageBox()
			img.SetParent(self.GetChild("next_bonus_list"))
			img.SetPosition(6, y)
			img.Show()
			
			txt = ui.TextLine()
			txt.SetParent(img)
			txt.SetPosition(20, 4)
			txt.SetPackedFontColor(grp.GenerateColor(0.6705, 0.6705, 0.6705, 1.0))
			txt.Show()
			
			txt2 = ui.TextLine()
			txt2.SetParent(img)
			txt2.SetPosition(215, 4)
			txt2.SetHorizontalAlignCenter()
			txt2.SetPackedFontColor(grp.GenerateColor(0.4078, 1.0, 0.4666, 1.0))
			txt2.Show()
			
			self.nextBonusListImages.append(img)
			self.nextBonusListTypeTexts.append(txt)
			self.nextBonusListValueTexts.append(txt2)
			y += 22

		self.__loaded = True
		self.Refresh()
		self.Hide()
		
	def SelectOption1(self):
		sndLevelMgr.SendPacket(0, 0)
		self.LockButtons()
		
	def SelectOption2(self):
		sndLevelMgr.SendPacket(0, 1)
		self.LockButtons()
		
	def LockButtons(self):
		self.opt1Button.Disable()
		self.opt1Button.Down()
		self.opt2Button.Disable()
		self.opt2Button.Down()
		self.__lockBtnEndTime = app.GetGlobalTime() + self.LOCK_BUTTON_MS
		
	def __SetNextSectionVisible(self, visible):
		section = self.GetChild2(self.NEXT_SECTION_CONTAINER)
		if section:
			if visible:
				section.Show()
			else:
				section.Hide()

		# Widzety listy bonusow powstaja w kodzie, a nie w uiscript. Maja rodzica
		# wewnatrz sekcji, ale chowamy je jawnie, zeby nie zalezec od tego, czy
		# Hide() rodzica propaguje sie na dzieci dodane recznie.
		for group in (self.nextBonusListImages, self.nextBonusListTypeTexts,
		              self.nextBonusListValueTexts):
			for widget in group:
				if visible:
					widget.Show()
				else:
					widget.Hide()

	def Refresh(self):
		isMaxLevel = False

		try:
			currentLevel = player.GetStatus(244)
			if currentLevel < 0 or currentLevel not in LEVEL_NAMES:
				currentLevel = 0
			nextLevel = min(currentLevel + 1, max(LEVEL_NAMES))
			isMaxLevel = currentLevel >= max(LEVEL_NAMES)

			self.actualRank.LoadImage("kowal/secondary_level/level_icons/{}.tga".format(currentLevel))
			self.acutalTextRank.SetText(LEVEL_NAMES.get(currentLevel, LEVEL_NAMES[0]))

			if not isMaxLevel:
				self.nextRank.LoadImage("kowal/secondary_level/level_icons/{}.tga".format(nextLevel))
				self.nextTextRank.SetText(LEVEL_NAMES.get(nextLevel, LEVEL_NAMES[max(LEVEL_NAMES)]))
		except:
			pass

		self.__SetNextSectionVisible(not isMaxLevel)

		# Bonusy AKTUALNEGO poziomu wypelniamy zawsze - to lewa kolumna, ktora
		# zostaje widoczna takze na maksie.
		for i in range(5):
			(apply, value) = sndLevelMgr.GetApply(i)
			if apply > 0:
				self.actualBonusListImages[i].LoadImage("kowal/secondary_level/bonus_layer.png")
				affString = GetAffectString(apply, value)
				(spltApply, spltValue) = GetSplittedBonus(affString)
				self.actualBonusListTypeTexts[i].SetText(spltApply)
				self.actualBonusListValueTexts[i].SetText(spltValue)
			else:
				self.actualBonusListImages[i].LoadImage("kowal/secondary_level/bonus_none.png")
				self.actualBonusListTypeTexts[i].SetText(localeInfo.SECONDARY_LEVEL_BONUS_NONE)
				self.actualBonusListValueTexts[i].SetText("")

		if isMaxLevel:
			# Dalej jest juz wylacznie sekcja awansu, a ta jest schowana.
			return

		for i in range(5):
			(apply, value) = sndLevelMgr.GetNextApply(i)
			if apply > 0:
				self.nextBonusListImages[i].LoadImage("kowal/secondary_level/bonus_layer.png")
				affString = GetAffectString(apply, value)
				(spltApply, spltValue) = GetSplittedBonus(affString)
				self.nextBonusListTypeTexts[i].SetText(spltApply)
				self.nextBonusListValueTexts[i].SetText(spltValue)
			else:
				self.nextBonusListImages[i].LoadImage("kowal/secondary_level/bonus_none.png")
				self.nextBonusListTypeTexts[i].SetText(localeInfo.SECONDARY_LEVEL_BONUS_NONE)
				self.nextBonusListValueTexts[i].SetText("")
				
		freeSlot = 0
		for i in range(1):
			(vnum, count) = sndLevelMgr.GetRequiredItem(i)
			if vnum > 0:
				self.requiredItems.SetItemSlot(freeSlot, vnum, count)
				freeSlot += 1
				
				
		(chance1) = sndLevelMgr.GetChance(0)
		(cost1) = sndLevelMgr.GetRequiredGold(0)
		self.opt1Chance.SetText("{}%".format(chance1))
		self.opt1Cost.SetText("{}".format(localeInfo.NumberToString(cost1)))
		
		self.opt2Chance.SetText("{}%".format(sndLevelMgr.GetChance(1)))
		self.opt2Cost.SetText("{}".format(localeInfo.NumberToString(sndLevelMgr.GetRequiredGold(1))))
				
	def OverInItem(self, slotIndex):
		if self.tooltipItem:
			self.tooltipItem.SetItemToolTip(self.requiredItems.GetItemSlot(slotIndex))

	def OverOutItem(self):
		if self.tooltipItem:
			self.tooltipItem.HideToolTip()

	def Open(self):
		self.Refresh()
		self.Show()
		
	def Close(self):
		self.Hide()
		
	def OnUpdate(self):
		# Liczniki byly w KLATKACH (20 klatek = 333 ms, blokada 200 klatek = 3.3 s przy 60 FPS).
		# Po odblokowaniu limitu FPS przy 144 Hz odswiezaloby sie 2.4x czesciej, a blokada
		# przyciskow schodzilaby po 1.4 s zamiast 3.3 s. Liczymy czasem rzeczywistym.
		curTime = app.GetGlobalTime()

		if curTime - self.__lastRefreshTime >= self.REFRESH_INTERVAL_MS:
			self.__lastRefreshTime = curTime
			self.Refresh()

		if self.__lockBtnEndTime and curTime >= self.__lockBtnEndTime:
			self.__lockBtnEndTime = 0
			self.opt1Button.Enable()
			self.opt1Button.SetUp()
			self.opt2Button.Enable()
			self.opt2Button.SetUp()
				
	def OnPressEscapeKey(self):
		self.Close()
		return True
