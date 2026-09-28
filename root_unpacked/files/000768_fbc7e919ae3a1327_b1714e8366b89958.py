import ui
import localeInfo
import chr
import app
import skill
import player
import uiToolTip
import math
import uiCommon
import net
import chat
import emoji
import item

# Grzaniec (item 50840, ITEM_NOG_POCKET) - AFFECT_NOG_ABILITY z Shared/AffectConstants.hpp:52.
# Serwer wysyla DWA afekty pod tym samym typem 302, rozniace sie tylko pointIdx (POINT_*),
# wiec opis dobieramy po pointIdx - inaczej kolejnosc pakietow decydowalaby o tresci tooltipa.
AFFECT_NOG_ABILITY = 302

# Dostep do CH5 (itemy 10165 / 10166). Serwer wysyla go jako zwykly afekt premium:
# AFFECT_PREMIUM_START (500) + PREMIUM_CHANNEL (indeks 9 w EPremiumTypes) = 509.
# Klient nie ma na to stalej w InstanceBase.h - enum konczy sie na 508 - wiec numer
# jawnie, tak jak inne "gole" wpisy w AFFECT_DATA_DICT (551, 746, 1295...).
AFFECT_CHANNEL_PREMIUM = 509
NOG_BONUS_DESC_DICT = {
	122 : localeInfo.TOOLTIP_NORMAL_HIT_DAMAGE_BONUS,	# POINT_NORMAL_HIT_DAMAGE_BONUS
	159 : localeInfo.TOOLTIP_ATTBONUS_DUNGEON,			# POINT_ATTBONUS_DUNGEON
}

class ItemAffectImage(ui.ExpandedImageBox):
	def __init__(self):
		ui.ExpandedImageBox.__init__(self)

		self.toolTip = uiToolTip.ItemToolTip(100)
		self.toolTip.HideToolTip()

	def OnMouseOverIn(self):
		self.toolTip.ShowToolTip()

	def OnMouseOverOut(self):
		self.toolTip.HideToolTip()

class LovePointImage(ui.ExpandedImageBox):

	FILE_PATH = "d:/ymir work/ui/pattern/LovePoint/"
	FILE_DICT = {
		0 : FILE_PATH + "01.dds",
		1 : FILE_PATH + "02.dds",
		2 : FILE_PATH + "02.dds",
		3 : FILE_PATH + "03.dds",
		4 : FILE_PATH + "04.dds",
		5 : FILE_PATH + "05.dds",
	}

	def __init__(self):
		ui.ExpandedImageBox.__init__(self)

		self.loverName = ""
		self.lovePoint = 0

		self.toolTip = uiToolTip.ToolTip(100)
		self.toolTip.HideToolTip()

	def __del__(self):
		ui.ExpandedImageBox.__del__(self)

	def SetLoverInfo(self, name, lovePoint):
		self.loverName = name
		self.lovePoint = lovePoint
		self.__Refresh()

	def OnUpdateLovePoint(self, lovePoint):
		self.lovePoint = lovePoint
		self.__Refresh()

	def __Refresh(self):
		self.lovePoint = max(0, self.lovePoint)
		self.lovePoint = min(100, self.lovePoint)

		if 0 == self.lovePoint:
			loveGrade = 0
		else:
			loveGrade = self.lovePoint // 25 + 1
		fileName = self.FILE_DICT.get(loveGrade, self.FILE_PATH+"00.dds")

		try:
			self.LoadImage(fileName)
		except:
			import dbg
			dbg.TraceError("LovePointImage.SetLoverInfo(lovePoint=%d) - LoadError %s" % (self.lovePoint, fileName))

		self.SetScale(0.7, 0.7)

		self.toolTip.ClearToolTip()
		self.toolTip.SetTitle(self.loverName)
		self.toolTip.AppendTextLine(localeInfo.AFF_LOVE_POINT % (self.lovePoint))
		self.toolTip.ResizeToolTip()

	def OnMouseOverIn(self):
		self.toolTip.ShowToolTip()

	def OnMouseOverOut(self):
		self.toolTip.HideToolTip()


class HorseImage(ui.ExpandedImageBox):

	FILE_PATH = "d:/ymir work/ui/pattern/HorseState/"

	FILE_DICT = {
		00 : FILE_PATH+"00.dds",
		1 : FILE_PATH+"00.dds",
		2 : FILE_PATH+"00.dds",
		3 : FILE_PATH+"00.dds",
		10 : FILE_PATH+"10.dds",
		11 : FILE_PATH+"11.dds",
		12 : FILE_PATH+"12.dds",
		13 : FILE_PATH+"13.dds",
		20 : FILE_PATH+"20.dds",
		21 : FILE_PATH+"21.dds",
		22 : FILE_PATH+"22.dds",
		23 : FILE_PATH+"23.dds",
		30 : FILE_PATH+"30.dds",
		31 : FILE_PATH+"31.dds",
		32 : FILE_PATH+"32.dds",
		33 : FILE_PATH+"33.dds",
	}

	def __init__(self):
		ui.ExpandedImageBox.__init__(self)

		self.toolTip = uiToolTip.ToolTip(100)
		self.toolTip.HideToolTip()

	def __GetHorseGrade(self, level):
		if 0 == level:
			return 0

		return (level-1)//10 + 1

	def SetState(self, level, health, battery):
		self.toolTip.ClearToolTip()

		if level>0:

			try:
				grade = self.__GetHorseGrade(level)
				self.__AppendText(localeInfo.LEVEL_LIST[grade])
			except IndexError:
				print(("HorseImage.SetState(level=%d, health=%d, battery=%d) - Unknown Index" % (level, health, battery)))
				return

			try:
				healthName=localeInfo.HEALTH_LIST[health]
				if len(healthName)>0:
					self.__AppendText(healthName)
			except IndexError:
				print(("HorseImage.SetState(level=%d, health=%d, battery=%d) - Unknown Index" % (level, health, battery)))
				return

			if health>0:
				if battery==0:
					self.__AppendText(localeInfo.NEEFD_REST)

			try:
				fileName=self.FILE_DICT[health*10+battery]
			except KeyError:
				print(("HorseImage.SetState(level=%d, health=%d, battery=%d) - KeyError" % (level, health, battery)))

			try:
				self.LoadImage(fileName)
			except:
				print(("HorseImage.SetState(level=%d, health=%d, battery=%d) - LoadError %s" % (level, health, battery, fileName)))

		self.SetScale(0.7, 0.7)

	def __AppendText(self, text):

		self.toolTip.AppendTextLine(text)


	def OnMouseOverIn(self):

		self.toolTip.ShowToolTip()

	def OnMouseOverOut(self):

		self.toolTip.HideToolTip()

class ItemImage(ItemAffectImage):
	def __init__(self, cell):
		ItemAffectImage.__init__(self)

		self.cell = cell

	def SetImage(self, filename):
		self.LoadImage(filename)

		self.SetScale(0.7, 0.7)

	def Update(self):
		if not self.toolTip.IsShow():
			return

		self.toolTip.ClearToolTip()
		self.toolTip.SetInventoryItem(self.cell)

	def OnMouseOverIn(self):
		ItemAffectImage.OnMouseOverIn(self)
		self.Update()


class AutoPotionImage(ItemImage):
	FILE_PATH_HP = "d:/ymir work/ui/pattern/auto_hpgauge/"
	FILE_PATH_SP = "d:/ymir work/ui/pattern/auto_spgauge/"

	def __init__(self, subType, cell):
		ItemImage.__init__(self, cell)

		self.subType = subType
		self.oldGrade = -1

	def Update(self):
		itemVnum = player.GetItemIndex(player.INVENTORY, self.cell)
		if itemVnum == 0:
			return

		item.SelectItem(itemVnum)
		metinSocket = [player.GetItemMetinSocket(self.cell, j) for j in range(player.METIN_SOCKET_MAX_NUM)]	

		totalAmount = metinSocket[2]
		usedAmount = metinSocket[1]
		currentAmount = totalAmount - usedAmount

		if 0 == totalAmount:
			totalAmount = 100
			usedAmount = 0
			currentAmount = 100

		amountPercent = 100 * currentAmount // totalAmount

		if self.subType == item.TOGGLE_AUTO_RECOVERY_HP:
			path = self.FILE_PATH_HP
		else:
			path = self.FILE_PATH_SP

		grade = self.__GetGradeFromPercent(amountPercent)
		if self.oldGrade != grade:
			fileName = "%s%.2d.dds" % (path, grade)

			print(("AutoPotion: %d %d %s", self.subType, amountPercent, fileName))

			try:
				self.SetImage(fileName)
			except RuntimeError:
				import dbg
				dbg.TraceError("Failed to load auto-potion image %s" % fileName)

			self.oldGrade = grade

		ItemImage.Update(self)

	def __GetGradeFromPercent(self, percent):
		if percent > 80:
			return 5
		if percent > 60:
			return 4
		if percent > 40:
			return 3
		if percent > 20:
			return 2

		return 1

class ToggleItemImage(ItemImage):
	def __init__(self, cell):
		ItemImage.__init__(self, cell)

	def Update(self):
		itemVnum = player.GetItemIndex(player.INVENTORY, self.cell)
		if itemVnum == 0:
			return

		item.SelectItem(itemVnum)
		self.SetImage(item.GetIconImageFileName())
		
		ItemImage.Update(self)

class AffectImage(ui.ExpandedImageBox):

	def __init__(self):
		ui.ExpandedImageBox.__init__(self)

		self.toolTip = uiToolTip.ToolTip()
		self.toolTip.HideToolTip()

		self.isSkillAffect = True
		self.description = None
		# kolor glownej linii opisu; None = domyslny FONT_COLOR tooltipa
		self.descriptionColor = None
		# (pointIdx, value) afektow Grzanca - patrz AddNogBonus
		self.nogBonuses = []
		self.endTime = 0
		self.affect = None
		self.isClocked = True
		# referencja do linii tooltipa z pozostalym czasem - NIE zakladamy, ze jest
		# ostatnia w childrenList (SetExtraDescriptions dopisuje linie po niej)
		self.timeLine = None
		self.lastClockUpdate = 0
		self.polymorphQuestionDialog = None
		self.skillAffectQuestionDialog = None
		self.buffQuestionDialog = None
		self.extraQuestionDialog = None
		self.skillIndex = None

	def SetAffect(self, affect):
		self.affect = affect

	def GetAffect(self):
		return self.affect

	def FormatTime(self, time):
		text = ""

		d = time // (24 * 3600)
		time = time % (24 * 3600)
		h = time // 3600
		time %= 3600
		m = time // 60
		time %= 60
		s = time

		if d:
			text += "%dd " % d
		if text or h:
			text += "%dg " % h
		if text or m:
			text += "%dm " % m
		if text or s:
			text += "%ds " % s

		return text[:-1]

	def SetToolTipText(self, text, x = 0, y = -19, color = None):
		self.toolTip.ClearToolTip()
		# ClearToolTip zeruje childrenList, wiec stara linia czasu juz nie istnieje
		self.timeLine = None
		self.toolTip.AppendSpace(-5)
		if color is None:
			self.toolTip.AppendDescription(text, 26)
		else:
			self.toolTip.AppendDescription(text, 26, color)

	def SetDescription(self, description, color = None):
		self.description = description
		self.descriptionColor = color
		self.__UpdateDescription2()

	def SetDuration(self, duration):
		self.endTime = 0
		if duration > 0:
			self.endTime = app.GetGlobalTimeStamp() + duration
			leftTime = self.FormatTime(self.endTime - app.GetGlobalTimeStamp())
			self.toolTip.AppendHorizontalLine()
			self.toolTip.AppendTextLine(localeInfo.LEFTOVER_TIME)
			self.toolTip.AppendTextLine(emoji.AppendEmoji("icon/emoji/image-example-007.png")+" "+leftTime)
			# zapamietujemy sama linie - UpdateDescription nadpisuje wlasnie ja,
			# niezaleznie od tego co dojdzie do tooltipa pozniej
			if self.toolTip.childrenList:
				self.timeLine = self.toolTip.childrenList[-1]
	
	def AddNogBonus(self, pointIdx, value):
		if pointIdx not in NOG_BONUS_DESC_DICT:
			return

		self.nogBonuses = [b for b in self.nogBonuses if b[0] != pointIdx]
		self.nogBonuses.append((pointIdx, value))
		self.__RebuildNogToolTip()

	def __RebuildNogToolTip(self):
		# Tooltip budujemy od zera, bo AppendTextLine dopisuje wylacznie na koniec.
		# Bez tego drugi bonus ladowal POD blokiem "Pozostaly czas" - oba maja stac razem
		# nad nim. Kolejnosc jak w tooltipie samego itemu (uitooltip.py, itemVnum == 50840).
		order = list(NOG_BONUS_DESC_DICT.keys())
		lines = [NOG_BONUS_DESC_DICT[p](float(v))
			for p, v in sorted(self.nogBonuses, key = lambda b: order.index(b[0]))]
		if not lines:
			return

		remainTime = 0
		if self.endTime > 0:
			remainTime = max(0, self.endTime - app.GetGlobalTimeStamp())

		# Wszystkie linie na zielono - to lista bonusow, dokladnie jak w tooltipie itemu.
		# Pierwsza szla przez AppendDescription (domyslny szary), reszta przez AppendTextLine,
		# przez co jedna linia byla szara a druga zielona.
		self.SetDescription(lines[0], self.toolTip.POSITIVE_COLOR)
		for line in lines[1:]:
			self.toolTip.AppendTextLine(line, self.toolTip.POSITIVE_COLOR)

		if remainTime > 0:
			self.SetDuration(remainTime)
		else:
			# bez tego UpdateDescription nadpisalby ostatnia linie bonusu tekstem zegara
			self.endTime = 0

		self.UpdateDescription()

	def SetExtraDescriptions(self, affect):
		if affect == chr.AFFECT_RUNE_DECK5:
			self.toolTip.AppendHorizontalLine()
			self.toolTip.AppendTextLine(localeInfo.RUNE_SET_BONUS_1, self.toolTip.POSITIVE_COLOR)
			self.toolTip.AppendTextLine(localeInfo.RUNE_SET_BONUS_2, self.toolTip.POSITIVE_COLOR)
			self.toolTip.AppendTextLine(localeInfo.RUNE_SET_BONUS_3, self.toolTip.POSITIVE_COLOR)
		elif affect == chr.AFFECT_RUNE_DECK9:
			self.toolTip.AppendHorizontalLine()
			self.toolTip.AppendTextLine(localeInfo.RUNE_SET_BONUS_4, self.toolTip.POSITIVE_COLOR)
			self.toolTip.AppendTextLine(localeInfo.RUNE_SET_BONUS_5, self.toolTip.POSITIVE_COLOR)
			self.toolTip.AppendTextLine(localeInfo.RUNE_SET_BONUS_6, self.toolTip.POSITIVE_COLOR)

	def UpdateAutoPotionDescription(self):
		# bez tych dwoch guardow kazdy tick rzucal wyjatek (IndexError na pustym
		# tooltipie / TypeError gdy opis nie ma placeholdera) i - przy wspolnym
		# try w AffectShower.OnUpdate - zatrzymywal zegar wszystkich afektow
		if not self.toolTip.childrenList or not self.description:
			return

		potionType = player.AUTO_POTION_TYPE_HP if self.affect == chr.NEW_AFFECT_AUTO_HP_RECOVERY\
			else player.AUTO_POTION_TYPE_SP
		isActivated, currentAmount, totalAmount, slotIndex = player.GetAutoPotionInfo(potionType)

		try:
			amountPercent = (float(currentAmount) / totalAmount) * 100.0
		except:
			amountPercent = 100.0

		try:
			text = self.description % amountPercent
		except TypeError:
			text = self.description

		self.toolTip.childrenList[-1].SetText(text)

	def SetClock(self, isClocked):
		self.isClocked = isClocked
		self.SetDescription(self.description)
		
	def UpdateDescription(self):
		if not self.isClocked:
			return

		if not self.description:
			return

		if self.endTime > 0:
			timeLine = self.timeLine
			if not timeLine:
				if not self.toolTip.childrenList:
					return
				timeLine = self.toolTip.childrenList[-1]

			leftTime = max(0, self.endTime - app.GetGlobalTimeStamp())

			timeLine.SetText(emoji.AppendEmoji("icon/emoji/image-example-007.png")+" "+self.FormatTime(leftTime))

	def OnUpdate(self):
		# Odliczanie trzymamy na samym obrazku, a nie tylko w AffectShower.OnUpdate:
		# ikona jest widocznym oknem, wiec jej OnUpdate leci na pewno, a jeden wyjatek
		# w petli rodzica nie zatrzyma zegara wszystkich pozostalych afektow.
		if self.isSkillAffect:
			return

		if self.endTime <= 0:
			return

		now = app.GetGlobalTime()
		if now - self.lastClockUpdate < 500:
			return

		self.lastClockUpdate = now

		try:
			self.UpdateDescription()
		except Exception as e:
			import dbg
			dbg.TraceError("AffectImage.OnUpdate: %s" % e)

	def __UpdateDescription2(self):
		if not self.description:
			return

		toolTip = self.description
		self.SetToolTipText(toolTip, 0, 40, self.descriptionColor)

	def SetSkillAffectFlag(self, flag):
		self.isSkillAffect = flag
	def SetSkillIndex(self, skillIndex):
		self.skillIndex = skillIndex

	def IsSkillAffect(self):
		return self.isSkillAffect
		
	def OnPolymorphQuestionDialog(self):
		import uiCommon
		self.polymorphQuestionDialog = uiCommon.QuestionDialog()
		self.polymorphQuestionDialog.SetText(localeInfo.POLYMORPH_AFFECT_REMOVE_QUESTION)
		self.polymorphQuestionDialog.SetWidth(350)
		self.polymorphQuestionDialog.SetAcceptEvent(lambda arg = TRUE: self.OnClosePolymorphQuestionDialog(arg))
		self.polymorphQuestionDialog.SetCancelEvent(lambda arg = FALSE: self.OnClosePolymorphQuestionDialog(arg))
		self.polymorphQuestionDialog.Open()
		
	def OnClosePolymorphQuestionDialog(self, answer):

		if not self.polymorphQuestionDialog:
			return

		self.polymorphQuestionDialog.Close()
		self.polymorphQuestionDialog = None
				
		if not answer:
			return

		net.SendChatPacket("/remove_polymorph")
		return TRUE
		
	def OnBuffQuestionDialog(self):
		skillIndex = self.skillIndex
		if not skillIndex or skillIndex == 66:
			return
		self.buffQuestionDialog = uiCommon.QuestionDialog()
		self.buffQuestionDialog.SetWidth(350)
		self.buffQuestionDialog.SetText(localeInfo.BUFF_AFFECT_REMOVE_QUESTION % (skill.GetSkillName(skillIndex)))
		self.buffQuestionDialog.SetAcceptEvent(lambda arg = skillIndex: self.OnCloseBuffQuestionDialog(arg))
		self.buffQuestionDialog.SetCancelEvent(lambda arg = 0: self.OnCloseBuffQuestionDialog(arg))
		self.buffQuestionDialog.Open()
		
	def OnCloseBuffQuestionDialog(self, answer):
		if not self.buffQuestionDialog:
			return

		self.buffQuestionDialog.Close()
		self.buffQuestionDialog = None

		if not answer:
			return

		net.SendChatPacket("/remove_skill_affect %d" % answer)
		return TRUE

	def OnExtraQuestionDialog(self):
		affect = self.affect
		if not affect:
			return
		self.extraQuestionDialog = uiCommon.QuestionDialog()
		self.extraQuestionDialog.SetWidth(350)
		self.extraQuestionDialog.SetText(localeInfo.AFFECT_SHOWER_DELETE_BONUS)
		self.extraQuestionDialog.SetAcceptEvent(lambda arg = affect: self.OnCloseExtraQuestionDialog(arg))
		self.extraQuestionDialog.SetCancelEvent(lambda arg = 0: self.OnCloseExtraQuestionDialog(arg))
		self.extraQuestionDialog.Open()
		
	def OnCloseExtraQuestionDialog(self, answer):
		if not self.extraQuestionDialog:
			return

		self.extraQuestionDialog.Close()
		self.extraQuestionDialog = None

		if not answer:
			return

		affect_map = {
			1116: {510},
		}

		if answer not in affect_map:
			return

		net.SendChatPacket("/remove_skill_affect %d" % next(iter(affect_map[answer])))
		return True

	def OnMouseOverIn(self):
		self.toolTip.ShowToolTip()

	def OnMouseOverOut(self):
		self.toolTip.HideToolTip()
	
	def OnMouseLeftButtonUp(self):
		if self.affect == chr.NEW_AFFECT_POLYMORPH:
			self.OnPolymorphQuestionDialog()

		if self.affect == 1116:
			self.OnExtraQuestionDialog()

		skillIndex = self.skillIndex
		if skillIndex == 3 or skillIndex == 4:
			self.OnBuffQuestionDialog()

class AffectShower(ui.Window):

	MALL_DESC_IDX_START = 1000
	DEW_DESC_IDX_START = 1200
	FISH_DESC_IDX_START = 800
	WATER_DESC_IDX_START = 1400
	DRAGON_GOD_DESC_IDX_START = 1600
	IMAGE_STEP = 25
	AFFECT_MAX_NUM = 32

	INFINITE_AFFECT_DURATION = 0x1FFFFFFF

	AFFECT_DATA_DICT =	{
			chr.AFFECT_POISON : (localeInfo.SKILL_TOXICDIE, "d:/ymir work/ui/skill/common/affect/poison.sub"),
			chr.AFFECT_SLOW : (localeInfo.SKILL_SLOW, "d:/ymir work/ui/skill/common/affect/slow.sub"),
			chr.AFFECT_STUN : (localeInfo.SKILL_STUN, "d:/ymir work/ui/skill/common/affect/stun.sub"),

			# Ikony mikstur, nie skilli. Wczesniej szly tu increase_attack_speed.sub /
			# increase_move_speed.sub, czyli wycinki z newskillcommon.dds - generyczne ikonki
			# skilli przyspieszenia, nijak nie kojarzace sie z wypita mikstura.
			# Te same pliki, ktore itemy maja w plecaku (kowal/item_list.txt): 27112 -> 27102.tga,
			# 27115 -> 27105.tga. Precedens uzycia icon/item/* w tym oknie: AFFECT_CHANNEL_PREMIUM.
			# UWAGA: serwer wysyla tylko flage AFF_ATT_SPEED_POTION / AFF_MOV_SPEED_POTION, bez
			# vnumu, wiec jedna ikona obsluguje WSZYSTKIE itemy dajace dany afekt - takze
			# Pieczonego Amura (27868), Wode Hwal (50820), Lody (50123) czy Pieczonego Karpia
			# (27866). Rozroznienie wymagaloby przeslania vnumu w pakiecie afektu.
			chr.AFFECT_ATT_SPEED_POTION : (localeInfo.SKILL_INC_ATKSPD, "icon/item/27102.tga"),
			chr.AFFECT_MOV_SPEED_POTION : (localeInfo.SKILL_INC_MOVSPD, "icon/item/27105.tga"),
			chr.AFFECT_FISH_MIND : (localeInfo.SKILL_FISHMIND, "d:/ymir work/ui/skill/common/affect/fishmind.sub"),
			chr.AFFECT_PREMIUM_MINE : (localeInfo.TOOLTIP_MALL_PREMIUM_MINE, "d:/ymir work/ui/skill/common/affect/ruda.tga"),

			chr.AFFECT_JEONGWI : (localeInfo.SKILL_JEONGWI, "d:/ymir work/ui/skill/warrior/jeongwi_03.sub",),
			chr.AFFECT_GEOMGYEONG : (localeInfo.SKILL_GEOMGYEONG, "d:/ymir work/ui/skill/warrior/geomgyeong_03.sub",),
			chr.AFFECT_CHEONGEUN : (localeInfo.SKILL_CHEONGEUN, "d:/ymir work/ui/skill/warrior/cheongeun_03.sub",),
			chr.AFFECT_GYEONGGONG : (localeInfo.SKILL_GYEONGGONG, "d:/ymir work/ui/skill/assassin/gyeonggong_03.sub",),
			chr.AFFECT_EUNHYEONG : (localeInfo.SKILL_EUNHYEONG, "d:/ymir work/ui/skill/assassin/eunhyeong_03.sub",),
			chr.AFFECT_GWIGEOM : (localeInfo.SKILL_GWIGEOM, "d:/ymir work/ui/skill/sura/gwigeom_03.sub",),
			chr.AFFECT_GONGPO : (localeInfo.SKILL_GONGPO, "d:/ymir work/ui/skill/sura/gongpo_03.sub",),
			chr.AFFECT_JUMAGAP : (localeInfo.SKILL_JUMAGAP, "d:/ymir work/ui/skill/sura/jumagap_03.sub"),
			chr.AFFECT_HOSIN : (localeInfo.SKILL_HOSIN, "d:/ymir work/ui/skill/shaman/hosin_03.sub",),
			chr.AFFECT_BOHO : (localeInfo.SKILL_BOHO, "d:/ymir work/ui/skill/shaman/boho_03.sub",),
			chr.AFFECT_KWAESOK : (localeInfo.SKILL_KWAESOK, "d:/ymir work/ui/skill/shaman/kwaesok_03.sub",),
			chr.AFFECT_HEUKSIN : (localeInfo.SKILL_HEUKSIN, "d:/ymir work/ui/skill/sura/heuksin_03.sub",),
			chr.AFFECT_MUYEONG : (localeInfo.SKILL_MUYEONG, "d:/ymir work/ui/skill/sura/muyeong_03.sub",),
			chr.AFFECT_GICHEON : (localeInfo.SKILL_GICHEON, "d:/ymir work/ui/skill/shaman/gicheon_03.sub",),
			chr.AFFECT_JEUNGRYEOK : (localeInfo.SKILL_JEUNGRYEOK, "d:/ymir work/ui/skill/shaman/jeungryeok_03.sub",),

			chr.AFFECT_PABEOP : (localeInfo.SKILL_PABEOP, "d:/ymir work/ui/skill/sura/pabeop_03.sub",),
			chr.AFFECT_FALLEN_CHEONGEUN : (localeInfo.SKILL_CHEONGEUN, "d:/ymir work/ui/skill/warrior/cheongeun_03.sub",),
			28 : (localeInfo.SKILL_FIRE, "d:/ymir work/ui/skill/sura/hwayeom_03.sub",),
			chr.AFFECT_CHINA_FIREWORK : (localeInfo.SKILL_POWERFUL_STRIKE, "d:/ymir work/ui/skill/common/affect/powerfulstrike.sub",),

			chr.NEW_AFFECT_EXP_BONUS : (localeInfo.TOOLTIP_MALL_EXPBONUS_STATIC, "d:/ymir work/ui/game/affectshower/pdvip.tga",),
			chr.NEW_AFFECT_ITEM_BONUS : (localeInfo.TOOLTIP_MALL_ITEMBONUS_STATIC_NEW, "d:/ymir work/ui/game/affectshower/itemvip.tga",),

			chr.NEW_AFFECT_SAFEBOX : (localeInfo.TOOLTIP_MALL_SAFEBOX, "d:/ymir work/ui/skill/common/affect/magazyn.tga",),
			chr.NEW_AFFECT_AUTOLOOT : (localeInfo.TOOLTIP_MALL_AUTOLOOT, "d:/ymir work/ui/skill/common/affect/trzecia_reka.tga",),
			chr.NEW_AFFECT_FISH_MIND : (localeInfo.TOOLTIP_MALL_FISH_MIND, "d:/ymir work/ui/skill/common/affect/ryba.tga",),
			chr.NEW_AFFECT_MARRIAGE_FAST : (localeInfo.TOOLTIP_MALL_MARRIAGE_FAST, "d:/ymir work/ui/skill/common/affect/marriage_fast.sub",),
			chr.NEW_AFFECT_GOLD_BONUS : (localeInfo.TOOLTIP_MALL_GOLDBONUS_STATIC, "d:/ymir work/ui/skill/common/affect/moneta.tga",),
			chr.AFFECT_PICKUP : (localeInfo.TOOLTIP_MALL_PICKUP, "d:/ymir work/ui/skill/common/affect/auto_podnoszenie.png",),
			chr.NEW_AFFECT_PREMIUM_MINE : (localeInfo.TOOLTIP_MALL_PREMIUM_MINE, "d:/ymir work/ui/skill/common/affect/ruda.tga",),

			chr.NEW_AFFECT_NO_DEATH_PENALTY : (localeInfo.TOOLTIP_APPLY_NO_DEATH_PENALTY, "d:/ymir work/ui/skill/common/affect/gold_premium.sub"),
			chr.NEW_AFFECT_SKILL_BOOK_BONUS : (localeInfo.TOOLTIP_APPLY_SKILL_BOOK_BONUS, "d:/ymir work/ui/game/affectshower/rada.tga"),
			chr.NEW_AFFECT_SKILL_BOOK_NO_DELAY : (localeInfo.TOOLTIP_APPLY_SKILL_BOOK_NO_DELAY, "d:/ymir work/ui/game/affectshower/egzo.tga"),
			
			chr.NEW_AFFECT_SKILE_PAS_BOOK_BONUS : (localeInfo.TOOLTIP_APPLY_SKILE_PAS_BOOK_BONUS, "d:/ymir work/ui/game/affectshower/rada0.tga"),
			chr.NEW_AFFECT_SKILE_PAS_NO_BOOK_DELAY : (localeInfo.TOOLTIP_APPLY_SKILE_PAS_NO_BOOK_DELAY, "d:/ymir work/ui/game/affectshower/egzo0.tga"),
			
			chr.NEW_AFFECT_SKILE_PET_BOOK_BONUS : (localeInfo.TOOLTIP_APPLY_SKILE_PET_BOOK_BONUS, "d:/ymir work/ui/game/affectshower/rada2.tga"),
			chr.NEW_AFFECT_SKILE_PET_NO_BOOK_DELAY : (localeInfo.TOOLTIP_APPLY_SKILE_PET_NO_BOOK_DELAY, "d:/ymir work/ui/game/affectshower/egzo2.tga"),
			
			chr.NEW_AFFECT_SKILE_BUFF_BOOK_BONUS : (localeInfo.TOOLTIP_APPLY_SKILE_BUFF_BOOK_BONUS, "d:/ymir work/ui/game/affectshower/rada1.tga"),
			chr.NEW_AFFECT_SKILE_BUFF_NO_BOOK_DELAY : (localeInfo.TOOLTIP_APPLY_SKILE_BUFF_NO_BOOK_DELAY, "d:/ymir work/ui/game/affectshower/egzo1.tga"),

			chr.NEW_AFFECT_AUTO_HP_RECOVERY : (localeInfo.TOOLTIP_AUTO_POTION_REST, "d:/ymir work/ui/pattern/auto_hpgauge/05.dds"),
			chr.NEW_AFFECT_AUTO_SP_RECOVERY : (localeInfo.TOOLTIP_AUTO_POTION_REST, "d:/ymir work/ui/pattern/auto_spgauge/05.dds"),

			551 : (localeInfo.TOOLTIP_PASYWKI_MASTER, "d:/ymir work/ui/game/affectshower/pasywki.tga"),


			MALL_DESC_IDX_START+player.POINT_MALL_ATTBONUS : (localeInfo.TOOLTIP_MALL_ATTBONUS_STATIC, "d:/ymir work/ui/skill/common/affect/att_bonus.sub",),
			MALL_DESC_IDX_START+player.POINT_MALL_DEFBONUS : (localeInfo.TOOLTIP_MALL_DEFBONUS_STATIC, "d:/ymir work/ui/game/affectshower/71030.tga",),
			MALL_DESC_IDX_START+player.POINT_MALL_EXPBONUS : (localeInfo.TOOLTIP_MALL_EXPBONUS, "d:/ymir work/ui/game/affectshower/exp.tga",),
			MALL_DESC_IDX_START+player.POINT_MALL_ITEMBONUS : (localeInfo.TOOLTIP_MALL_ITEMBONUS, "d:/ymir work/ui/skill/common/affect/item_bonus.sub",),
			MALL_DESC_IDX_START+player.POINT_MALL_GOLDBONUS : (localeInfo.TOOLTIP_MALL_GOLDBONUS, "d:/ymir work/ui/skill/common/affect/gold_bonus.sub",),
			# Ikony 710xx.tga: te same, ktore afekty mialy pod AFFECT_MALL_EX (548).
			# Po przejsciu itemow na USE_AFFECT afekt leci jako AFFECT_MALL (510),
			# czyli inny zakres slownika - bez tego graczom zmienilyby sie ikony
			# na generyczne gold_premium/critical/def_bonus.
			MALL_DESC_IDX_START+player.POINT_CRITICAL_PCT : (localeInfo.TOOLTIP_APPLY_CRITICAL_PCT,"d:/ymir work/ui/game/affectshower/71044.tga"),
			MALL_DESC_IDX_START+player.POINT_PENETRATE_PCT : (localeInfo.TOOLTIP_APPLY_PENETRATE_PCT, "d:/ymir work/ui/game/affectshower/71045.tga"),
			MALL_DESC_IDX_START+player.POINT_MAX_HP_PCT : (localeInfo.TOOLTIP_MAX_HP_PCT, "d:/ymir work/ui/game/affectshower/71027.tga"),
			MALL_DESC_IDX_START+player.POINT_MAX_SP_PCT : (localeInfo.TOOLTIP_MAX_SP_PCT, "d:/ymir work/ui/game/affectshower/71029.tga"),
			# POINT_MELEE_MAGIC_ATT_BONUS_PER (132) - Atak Boga Smokow (71028, 39018, 72031-33, 72312)
			MALL_DESC_IDX_START+132 : (localeInfo.TOOLTIP_MALL_ATTBONUS_STATIC, "d:/ymir work/ui/game/affectshower/71028.tga"),

			MALL_DESC_IDX_START+player.POINT_PC_BANG_EXP_BONUS : (localeInfo.TOOLTIP_MALL_EXPBONUS_P_STATIC, "d:/ymir work/ui/skill/common/affect/EXP_Bonus_p_on.sub",),
			MALL_DESC_IDX_START+player.POINT_PC_BANG_DROP_BONUS: (localeInfo.TOOLTIP_MALL_ITEMBONUS_P_STATIC, "d:/ymir work/ui/skill/common/affect/Item_Bonus_p_on.sub",),
	}
	if app.ENABLE_DRAGON_SOUL_SYSTEM:
		AFFECT_DATA_DICT[chr.NEW_AFFECT_DRAGON_SOUL_DECK1] = (localeInfo.TOOLTIP_DRAGON_SOUL_DECK1, "d:/ymir work/ui/dragonsoul/buff_ds_sky1.tga")
		AFFECT_DATA_DICT[chr.NEW_AFFECT_DRAGON_SOUL_DECK2] = (localeInfo.TOOLTIP_DRAGON_SOUL_DECK2, "d:/ymir work/ui/dragonsoul/buff_ds_land1.tga")

	if app.ENABLE_AFFECT_POLYMORPH_REMOVE:
		AFFECT_DATA_DICT[chr.NEW_AFFECT_POLYMORPH] = (localeInfo.POLYMORPH_AFFECT_TOOLTIP, "d:/ymir work/ui/polymorph_marble_icon.tga")

	if app.__AUTO_QUQUE_ATTACK__:
		AFFECT_DATA_DICT[chr.NEW_AFFECT_AUTO_METIN_FARM] =  (localeInfo.NEW_AFFECT_AUTO_METIN_FARM, "d:/ymir work/ui/game/affectshower/61400.tga")

	if app.__AUTO_HUNT__:
		AFFECT_DATA_DICT[chr.NEW_AFFECT_AUTO_HUNT] = (localeInfo.NEW_AFFECT_AUTO_HUNT, "icon/affectshower/auto_hunt.tga")

	if app.ENABLE_USE_FISH_SYSTEM:
		AFFECT_DATA_DICT[812] = (localeInfo.TOOLTIP_STR, "d:/ymir work/ui/game/affectshower/80400.tga")
		AFFECT_DATA_DICT[848] = (localeInfo.TOOLTIP_APPLY_ATTBONUS_DEVIL, "d:/ymir work/ui/game/affectshower/80401.tga")
		AFFECT_DATA_DICT[815] = (localeInfo.TOOLTIP_INT, "d:/ymir work/ui/game/affectshower/80402.tga")
		AFFECT_DATA_DICT[814] = (localeInfo.TOOLTIP_DEX, "d:/ymir work/ui/game/affectshower/80403.tga")
		AFFECT_DATA_DICT[853] = (localeInfo.TOOLTIP_APPLY_ATTBONUS_MONSTER, "d:/ymir work/ui/game/affectshower/80404.tga")
		AFFECT_DATA_DICT[922] = (localeInfo.TOOLTIP_NORMAL_HIT_DAMAGE_BONUS, "d:/ymir work/ui/game/affectshower/80405.tga")
		AFFECT_DATA_DICT[883] = (localeInfo.TOOLTIP_MALL_EXPBONUS, "d:/ymir work/ui/game/affectshower/80406.tga")
		AFFECT_DATA_DICT[895] = (localeInfo.TOOLTIP_ATT_GRADE, "d:/ymir work/ui/game/affectshower/80407.tga")
		# 80408.tga nigdy nie trafilo do packa (sasiednie 80400-80407 i 80418-80421 sa),
		# wiec klient logowal "Failed to load image" i zostawial pusty slot. 50839.tga to
		# ta sama ikona bonusu na bossy, uzywana juz nizej dla DEW_DESC_IDX_START+152.
		AFFECT_DATA_DICT[952] = (localeInfo.TOOLTIP_APPLY_ATTBONUS_BOSS, "d:/ymir work/ui/game/affectshower/50839.tga")
		AFFECT_DATA_DICT[954] = (localeInfo.TOOLTIP_APPLY_ATTBONUS_STONE, "d:/ymir work/ui/game/affectshower/80418.tga")
		AFFECT_DATA_DICT[964] = (localeInfo.TOOLTIP_APPLY_FINAL_DMG_BONUS, "d:/ymir work/ui/game/affectshower/80419.tga")
		AFFECT_DATA_DICT[956] = (localeInfo.TOOLTIP_APPLY_ATTBONUS_WLADCA, "d:/ymir work/ui/game/affectshower/80420.tga")
		AFFECT_DATA_DICT[951] = (localeInfo.TOOLTIP_APPLY_RESIST_HUMAN, "d:/ymir work/ui/game/affectshower/80421.tga")
		AFFECT_DATA_DICT[1295] = (localeInfo.TOOLTIP_ATT_GRADE, "d:/ymir work/ui/game/affectshower/50841.tga")

	# Grzaniec (50840): ta sama ikona, ktora item ma w plecaku - shared/item_list.txt mapuje
	# 50840 na 50216.tga (buklak). Plik 50840.tga istnieje, ale przedstawia pierscien.
	# Opis dobierany po pointIdx w BINARY_NEW_AddAffect, bo pod tym typem afektu
	# przychodza dwa rozne bonusy.
	AFFECT_DATA_DICT[AFFECT_NOG_ABILITY] = (localeInfo.TOOLTIP_ATTBONUS_DUNGEON, "icon/item/50216.tga")

	# Ikona ta sama, ktora item ma w plecaku (shared/item_list.txt: 10165/10166).
	AFFECT_DATA_DICT[AFFECT_CHANNEL_PREMIUM] = (localeInfo.TOOLTIP_MALL_CHANNEL_PREMIUM, "icon/item/channel_premium.png")

	AFFECT_DATA_DICT[746] = (localeInfo.RUNE_DECK5_TOOLTIP, "d:/ymir work/ui/game/affectshower/runy.tga")
	AFFECT_DATA_DICT[747] = (localeInfo.RUNE_DECK9_TOOLTIP, "d:/ymir work/ui/game/affectshower/runy.tga")

	AFFECT_DATA_DICT[WATER_DESC_IDX_START+player.POINT_PENETRATE_PCT] = (localeInfo.TOOLTIP_APPLY_PENETRATE_PCT, 	"d:/ymir work/ui/game/affectshower/50813.tga")
	AFFECT_DATA_DICT[WATER_DESC_IDX_START+player.POINT_CRITICAL_PCT] = (localeInfo.TOOLTIP_APPLY_CRITICAL_PCT, 	"d:/ymir work/ui/game/affectshower/50814.tga")
	AFFECT_DATA_DICT[WATER_DESC_IDX_START+player.ATT_BONUS] = (localeInfo.TOOLTIP_ATT_GRADE, 			"d:/ymir work/ui/game/affectshower/50817.tga")
	AFFECT_DATA_DICT[WATER_DESC_IDX_START+player.DEF_BONUS] = (localeInfo.TOOLTIP_DEF_GRADE, 			"d:/ymir work/ui/game/affectshower/50818.tga")
	AFFECT_DATA_DICT[WATER_DESC_IDX_START+player.RESIST_MAGIC] = (localeInfo.TOOLTIP_MAGIC_DEF_GRADE, 		"d:/ymir work/ui/game/affectshower/50819.tga")
	AFFECT_DATA_DICT[WATER_DESC_IDX_START+player.ATT_SPEED] = (localeInfo.TOOLTIP_ATT_SPEED, 			"d:/ymir work/ui/game/affectshower/50820.tga")
	
	AFFECT_DATA_DICT[WATER_DESC_IDX_START+player.POINT_CRITICAL_PCT] = (localeInfo.TOOLTIP_APPLY_CRITICAL_PCT, 	"d:/ymir work/ui/game/affectshower/50821.tga")
	AFFECT_DATA_DICT[WATER_DESC_IDX_START+player.POINT_PENETRATE_PCT] = (localeInfo.TOOLTIP_APPLY_PENETRATE_PCT, 	"d:/ymir work/ui/game/affectshower/50822.tga")
	AFFECT_DATA_DICT[WATER_DESC_IDX_START+player.ATT_SPEED] = (localeInfo.TOOLTIP_ATT_SPEED, 			"d:/ymir work/ui/game/affectshower/50823.tga")
	AFFECT_DATA_DICT[WATER_DESC_IDX_START+player.RESIST_MAGIC] = (localeInfo.TOOLTIP_RESIST_MAGIC, 			"d:/ymir work/ui/game/affectshower/50824.tga")
	AFFECT_DATA_DICT[WATER_DESC_IDX_START+player.ATT_BONUS] = (localeInfo.TOOLTIP_ATT_GRADE, 			"d:/ymir work/ui/game/affectshower/50825.tga")
	AFFECT_DATA_DICT[WATER_DESC_IDX_START+player.DEF_BONUS] = (localeInfo.TOOLTIP_DEF_GRADE, 			"d:/ymir work/ui/game/affectshower/50826.tga")
	
	AFFECT_DATA_DICT[DEW_DESC_IDX_START+player.ENERGY] = (localeInfo.TOOLTIP_ENERGY, 			"d:/ymir work/ui/game/affectshower/51002.tga")
	AFFECT_DATA_DICT[DRAGON_GOD_DESC_IDX_START+player.POINT_MAX_HP_PCT] = (localeInfo.TOOLTIP_MAX_HP_PCT, "d:/ymir work/ui/game/affectshower/71027.tga")
	AFFECT_DATA_DICT[DRAGON_GOD_DESC_IDX_START+player.POINT_MAX_SP_PCT] = (localeInfo.TOOLTIP_MAX_SP_PCT, "d:/ymir work/ui/game/affectshower/71029.tga")
	AFFECT_DATA_DICT[DRAGON_GOD_DESC_IDX_START+132] = (localeInfo.TOOLTIP_MALL_ATTBONUS_STATIC, "d:/ymir work/ui/game/affectshower/71028.tga")
	AFFECT_DATA_DICT[DRAGON_GOD_DESC_IDX_START+93] = (localeInfo.TOOLTIP_MALL_ATTBONUS_STATIC, "d:/ymir work/ui/game/affectshower/71028.tga")
	AFFECT_DATA_DICT[DRAGON_GOD_DESC_IDX_START+player.POINT_MALL_DEFBONUS] = (localeInfo.TOOLTIP_MALL_DEFBONUS_STATIC, "d:/ymir work/ui/game/affectshower/71030.tga")
	AFFECT_DATA_DICT[DRAGON_GOD_DESC_IDX_START+player.POINT_CRITICAL_PCT] = (localeInfo.TOOLTIP_APPLY_CRITICAL_PCT, "d:/ymir work/ui/game/affectshower/71044.tga")
	AFFECT_DATA_DICT[DRAGON_GOD_DESC_IDX_START+player.POINT_PENETRATE_PCT] = (localeInfo.TOOLTIP_APPLY_PENETRATE_PCT, "d:/ymir work/ui/game/affectshower/71045.tga")
	# Boostery "Boga Smokow+" (40017-40020) z cube Uriela. Do 2026-08-19 mialy w proto
	# value1=3, przez co szly jako AFFECT_MALL_EX (toggle, INFINITE) i wisialy na stale;
	# ikony bral wtedy zakres DRAGON_GOD_DESC_IDX_START. Po przestawieniu ich na afekt
	# czasowy klucz to DEW_DESC_IDX_START+POINT - bez tych czterech wpisow buff dzialal,
	# ale znikal z paska. Ikony te same, co u odpowiednikow bez plusa (71027-71030).
	AFFECT_DATA_DICT[DEW_DESC_IDX_START+player.POINT_MAX_HP_PCT] = (localeInfo.TOOLTIP_MAX_HP_PCT, "d:/ymir work/ui/game/affectshower/71027.tga")
	AFFECT_DATA_DICT[DEW_DESC_IDX_START+132] = (localeInfo.TOOLTIP_MALL_ATTBONUS_STATIC, "d:/ymir work/ui/game/affectshower/71028.tga")
	AFFECT_DATA_DICT[DEW_DESC_IDX_START+93] = (localeInfo.TOOLTIP_MALL_ATTBONUS_STATIC, "d:/ymir work/ui/game/affectshower/71029.tga")
	AFFECT_DATA_DICT[DEW_DESC_IDX_START+player.POINT_MALL_DEFBONUS] = (localeInfo.TOOLTIP_MALL_DEFBONUS_STATIC, "d:/ymir work/ui/game/affectshower/71030.tga")

	AFFECT_DATA_DICT[DEW_DESC_IDX_START+152] = (localeInfo.TOOLTIP_APPLY_ATTBONUS_BOSS, "d:/ymir work/ui/game/affectshower/50839.tga")
	AFFECT_DATA_DICT[DEW_DESC_IDX_START+53] = (localeInfo.TOOLTIP_APPLY_ATTBONUS_MONSTER, "d:/ymir work/ui/game/affectshower/50837.tga")
	AFFECT_DATA_DICT[DEW_DESC_IDX_START+154] = (localeInfo.TOOLTIP_APPLY_ATTBONUS_STONE, "d:/ymir work/ui/game/affectshower/50838.tga")

	AFFECT_DATA_DICT[1217] = (localeInfo.TOOLTIP_MOV_SPEED, "d:/ymir work/ui/game/affectshower/27109.tga")
	AFFECT_DATA_DICT[1219] = (localeInfo.TOOLTIP_ATT_SPEED, "d:/ymir work/ui/game/affectshower/27105.tga")

	AFFECT_DATA_DICT[750] = (localeInfo.TOOLTIP_MALL_EXPBONUS, "d:/ymir work/ui/game/affectshower/71153.tga")

	if app.ENABLE_WOLFMAN_CHARACTER:
		AFFECT_DATA_DICT[chr.AFFECT_BLEEDING] = (localeInfo.SKILL_BLEEDING, "d:/ymir work/ui/skill/common/affect/poison.sub")
		AFFECT_DATA_DICT[chr.AFFECT_RED_POSSESSION] = (localeInfo.SKILL_GWIGEOM, "d:/ymir work/ui/skill/wolfman/red_possession_03.sub")
		AFFECT_DATA_DICT[chr.AFFECT_BLUE_POSSESSION] = (localeInfo.SKILL_CHEONGEUN, "d:/ymir work/ui/skill/wolfman/blue_possession_03.sub")

	def __init__(self):
		ui.Window.__init__(self)

		self.serverPlayTime=0
		self.clientPlayTime=0

		self.lastUpdateTime=0
		self.affectImageDict={}
		self.toggleImageDict = {}
		self.horseImage=None
		self.lovePointImage=None

		self.SetPosition(10, 10)
		self.Show()
		
	def ClearAllAffects(self):
		self.horseImage=None
		self.lovePointImage=None
		self.affectImageDict={}
		self.__ArrangeImageList()

	def ClearAffects(self):
		self.living_affectImageDict={}
		for key, image in list(self.affectImageDict.items()):
			if not image.IsSkillAffect():
				self.living_affectImageDict[key] = image
		self.affectImageDict = self.living_affectImageDict
		self.__ArrangeImageList()


	def BINARY_NEW_AddAffect(self, type, pointIdx, value, duration):

		print(("BINARY_NEW_AddAffect"), type, pointIdx, value, duration)

		if type < 499 and type != chr.NEW_AFFECT_POLYMORPH and type != AFFECT_NOG_ABILITY:
			return

		if type == chr.NEW_AFFECT_MALL:
			affect = self.MALL_DESC_IDX_START + pointIdx
		elif type == chr.NEW_AFFECT_BLEND:
			affect = self.DEW_DESC_IDX_START + pointIdx
		elif (app.ENABLE_EXTENDED_BLEND and type == chr.NEW_AFFECT_BLEND_EX):
			affect = self.DEW_DESC_IDX_START + pointIdx
		elif type == chr.NEW_AFFECT_WATER:
			affect = self.WATER_DESC_IDX_START + pointIdx
		elif type == chr.NEW_AFFECT_MALL_EX:
			affect = self.DRAGON_GOD_DESC_IDX_START + pointIdx
		elif type == chr.AFFECT_BLEND_FISH:
			affect = self.FISH_DESC_IDX_START + pointIdx
		else:
			affect = type

		if chr.IsGameMaster(0):
			chat.AppendChat(chat.CHAT_TYPE_INFO, "BINARY_NEW_AddAffect - type: "+str(type)+" =):"+str(affect)+" pointIdx:"+str(pointIdx)+" value:"+str(value)+" duration:"+str(duration))
		
		if affect in self.affectImageDict:
			# Grzaniec wysyla dwa afekty pod tym samym typem - drugi nie dostaje wlasnej
			# ikony, tylko dopisuje swoj bonus do tooltipa tej juz istniejacej.
			if affect == AFFECT_NOG_ABILITY:
				self.affectImageDict[affect].AddNogBonus(pointIdx, value)
			return

		if affect not in self.AFFECT_DATA_DICT:
			return

		if affect == chr.NEW_AFFECT_NO_DEATH_PENALTY or\
		   affect == chr.NEW_AFFECT_SKILL_BOOK_BONUS or\
		   affect == chr.NEW_AFFECT_AUTO_SP_RECOVERY or\
		   affect == chr.NEW_AFFECT_AUTO_HP_RECOVERY or\
		   affect == chr.AFFECT_RUNE_DECK5 or\
		   affect == chr.AFFECT_RUNE_DECK9 or\
		   affect == chr.NEW_AFFECT_SKILL_BOOK_NO_DELAY:
			duration = 0

		affectData = self.AFFECT_DATA_DICT[affect]
		description = affectData[0]
		filename = affectData[1]


		trashValue = 123
		if trashValue == 1:
			try:
				image = None
				
				if affect == chr.NEW_AFFECT_AUTO_SP_RECOVERY:
					image.SetPotionType(player.AUTO_POTION_TYPE_SP)
					image = self.autoPotionImageSP
				else:
					image.SetPotionType(player.AUTO_POTION_TYPE_HP)
					image = self.autoPotionImageHP
				
				image.SetParent(self)
				image.Show()
				image.OnUpdateAutoPotionImage()
				
				self.affectImageDict[affect] = image
				self.__ArrangeImageList()
				
			except Exception as e:
				print(("except Aff auto potion affect "), e)
				pass				
			
		else:
			if affect == AFFECT_NOG_ABILITY:
				description = NOG_BONUS_DESC_DICT.get(pointIdx, description)

			if affect != chr.NEW_AFFECT_AUTO_SP_RECOVERY and affect != chr.NEW_AFFECT_AUTO_HP_RECOVERY and affect != 551 and affect != chr.AFFECT_RUNE_DECK5 and affect != chr.AFFECT_RUNE_DECK9 and affect != chr.NEW_AFFECT_AUTO_HUNT:
				description = description(float(value))

			try:
				print(("Add affect %s") % affect)
				image = AffectImage()
				image.SetParent(self)
				image.LoadImage(filename)
				image.SetDescription(description)
				image.SetDuration(duration)
				image.SetAffect(affect)
				if affect == AFFECT_NOG_ABILITY:
					image.nogBonuses.append((pointIdx, value))
				image.SetExtraDescriptions(affect)
				if affect == chr.NEW_AFFECT_EXP_BONUS_EURO_FREE or\
					affect == chr.NEW_AFFECT_EXP_BONUS_EURO_FREE_UNDER_15 or\
					affect == 551 or\
					self.INFINITE_AFFECT_DURATION < duration:
					image.SetClock(False)
					image.UpdateDescription()

				elif affect == chr.NEW_AFFECT_AUTO_SP_RECOVERY or affect == chr.NEW_AFFECT_AUTO_HP_RECOVERY:
					image.UpdateAutoPotionDescription()
				else:
					image.UpdateDescription()

				if affect == chr.NEW_AFFECT_DRAGON_SOUL_DECK1 or affect == chr.NEW_AFFECT_DRAGON_SOUL_DECK2:
					image.SetScale(1, 1)
				else:
					image.SetScale(0.7, 0.7)
				
				image.SetScale(0.7, 0.7)

				image.SetSkillAffectFlag(False)
				image.Show()
				self.affectImageDict[affect] = image
				self.__ArrangeImageList()
			except Exception as e:
				print(("except Aff affect "), e)
				pass

	def BINARY_NEW_RemoveAffect(self, type, pointIdx):
		if type == chr.NEW_AFFECT_MALL:
			affect = self.MALL_DESC_IDX_START + pointIdx
		elif type == chr.NEW_AFFECT_BLEND:
			affect = self.DEW_DESC_IDX_START + pointIdx
		elif (app.ENABLE_EXTENDED_BLEND and type == chr.NEW_AFFECT_BLEND_EX):
			affect = self.DEW_DESC_IDX_START + pointIdx
		elif type == chr.NEW_AFFECT_WATER:
			affect = self.WATER_DESC_IDX_START + pointIdx
		elif type == chr.NEW_AFFECT_MALL_EX:
			affect = self.DRAGON_GOD_DESC_IDX_START + pointIdx
		elif type == chr.AFFECT_BLEND_FISH:
			affect = self.FISH_DESC_IDX_START + pointIdx
		else:
			affect = type
	
		print(("Remove Affect %s %s" % ( type , pointIdx )))
		self.__RemoveAffect(affect)
		self.__ArrangeImageList()

		

				

	if app.ENABLE_AFFECT_FIX:
		def BINARY_NEW_RefreshAffect(self):
			self.__ArrangeImageList()

	def SetAffect(self, affect):
		self.__AppendAffect(affect)
		self.__ArrangeImageList()

	def ResetAffect(self, affect):
		self.__RemoveAffect(affect)
		self.__ArrangeImageList()

	# Jesli gracz jest spolimorfowany (aktywny afekt NEW_AFFECT_POLYMORPH), pokaz dialog
	# wylaczenia polimorfii (ten sam co klik w ikone afektu) i zwroc True. Inaczej False.
	def TryOpenPolymorphRemove(self):
		image = self.affectImageDict.get(chr.NEW_AFFECT_POLYMORPH, None)
		if image:
			image.OnPolymorphQuestionDialog()
			return True
		return False

	def SetLoverInfo(self, name, lovePoint):
		image = LovePointImage()
		image.SetParent(self)
		image.SetLoverInfo(name, lovePoint)
		self.lovePointImage = image
		self.__ArrangeImageList()

	def ShowLoverState(self):
		if self.lovePointImage:
			self.lovePointImage.Show()
			self.__ArrangeImageList()

	def HideLoverState(self):
		if self.lovePointImage:
			self.lovePointImage.Hide()
			self.__ArrangeImageList()

	def ClearLoverState(self):
		self.lovePointImage = None
		self.__ArrangeImageList()

	def OnUpdateLovePoint(self, lovePoint):
		if self.lovePointImage:
			self.lovePointImage.OnUpdateLovePoint(lovePoint)

	def SetHorseState(self, level, health, battery):
		if level==0:
			self.horseImage=None
		else:
			image = HorseImage()
			image.SetParent(self)
			image.SetState(level, health, battery)
			image.Show()

			self.horseImage=image
			self.__ArrangeImageList()

	def SetPlayTime(self, playTime):
		self.serverPlayTime = playTime
		self.clientPlayTime = app.GetTime()

	def __AppendAffect(self, affect):

		if affect in self.affectImageDict:
			return

		try:
			affectData = self.AFFECT_DATA_DICT[affect]
		except KeyError:
			return

		name = affectData[0]
		filename = affectData[1]

		skillIndex = player.AffectIndexToSkillIndex(affect)
		if 0 != skillIndex:
			name = skill.GetSkillName(skillIndex)

		# Wartosci locale w stylu SNA/SA sa funkcjami (druga sciezka dodawania affectu je wywoluje);
		# __AppendAffect zakladal string -> 'function has no len'. Zamien funkcje na string.
		if callable(name):
			try:
				name = name(0)
			except:
				name = ""

		image = AffectImage()
		image.SetParent(self)
		image.SetSkillAffectFlag(True)
		image.SetSkillIndex(skillIndex)

		try:
			image.LoadImage(filename)
		except:
			pass

		image.SetToolTipText(name, 0, 40)
		image.SetScale(0.7, 0.7)
		image.Show()
		self.affectImageDict[affect] = image

	def __RemoveAffect(self, affect):
		"""
		if affect == chr.NEW_AFFECT_AUTO_SP_RECOVERY:
			self.autoPotionImageSP.Hide()

		if affect == chr.NEW_AFFECT_AUTO_HP_RECOVERY:
			self.autoPotionImageHP.Hide()
		"""
			
		if affect not in self.affectImageDict:
			print(("__RemoveAffect %s ( No Affect )") % affect)
			return

		print(("__RemoveAffect %s ( Affect )") % affect)
		del self.affectImageDict[affect]
		
		self.__ArrangeImageList()

	def __ArrangeImageList(self):
		affectImages = list(self.affectImageDict.values()) + list(self.toggleImageDict.values())

		count = len(affectImages)

		if self.lovePointImage:
			count += 1

		if self.horseImage:
			count += 1

		self.SetSize(min(count, 10) * self.IMAGE_STEP, (((count - 1) // 10) + 1) * self.IMAGE_STEP)

		xc = 0
		yc = 0

		if self.lovePointImage and self.lovePointImage.IsShow():
			self.lovePointImage.SetPosition(xc * self.IMAGE_STEP, 0)
			xc += 1
		
		if self.horseImage:
			self.horseImage.SetPosition(xc * self.IMAGE_STEP, 0)
			xc += 1

		for image in affectImages:
			image.SetPosition(xc * self.IMAGE_STEP, yc * self.IMAGE_STEP)
			xc += 1
			
			if xc >= 10:
				xc = 0
				yc += 1

	ArrangeImageList = __ArrangeImageList

	def DeleteToggleImage(self, cell):
		if cell in self.toggleImageDict:
			del self.toggleImageDict[cell]

	def RefreshInventory(self):
		for cell in range(player.INVENTORY_SLOT_COUNT):
			itemVnum = player.GetItemIndex(player.INVENTORY, cell)
			if itemVnum == 0:
				self.DeleteToggleImage(cell)
				continue
			
			item.SelectItem(itemVnum)
			
			if item.GetItemType() != item.TOGGLE:
				self.DeleteToggleImage(cell)
				continue
			
			if 0 != player.GetItemMetinSocket(cell, 3):
				if cell in self.toggleImageDict:
					continue
				
				if item.GetItemSubType() == item.TOGGLE_AUTO_RECOVERY_HP or \
				   item.GetItemSubType() == item.TOGGLE_AUTO_RECOVERY_SP:
					image = AutoPotionImage(item.GetItemSubType(), cell)
				elif item.GetItemSubType() == item.TOGGLE_AFFECT:
					image = ToggleItemImage(cell)
				else:
					continue
				
				image.SetParent(self)
				image.Update()
				image.Show()
				
				self.toggleImageDict[cell] = image
			else:
				self.DeleteToggleImage(cell)

		self.__ArrangeImageList()

	def OnUpdate(self):
		try:
			if app.GetGlobalTime() - self.lastUpdateTime > 500:
			
				self.lastUpdateTime = app.GetGlobalTime()

				for image in list(self.toggleImageDict.values()):
					try:
						image.Update()
					except Exception as e:
						import dbg
						dbg.TraceError("Error during item-image update")

				for image in list(self.affectImageDict.values()):
					# per-obrazek: wyjatek na jednym afekcie (np. autopotion bez
					# placeholdera w opisie) nie moze zatrzymac zegara pozostalych
					try:
						if image.GetAffect() == chr.NEW_AFFECT_AUTO_HP_RECOVERY or image.GetAffect() == chr.NEW_AFFECT_AUTO_SP_RECOVERY:
							image.UpdateAutoPotionDescription()
							continue

						if not image.IsSkillAffect():
							image.UpdateDescription()
					except Exception as e:
						import dbg
						dbg.TraceError("AffectShower::OnUpdate affect %s : %s" % (image.GetAffect(), e))
		except Exception as e:
			print(("AffectShower::OnUpdate error : "), e)

