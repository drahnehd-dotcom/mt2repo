#-*- coding: iso-8859-1 -*-
import dbg
import player
import item
import grp
import wndMgr
import skill
import shop
import exchange
import grpText
import safebox
import localeInfo
import app
import background
import switchbot
import nonplayer
import chr
import ui
import mouseModule
import chat
import constInfo
import settings
import uiScriptLocale
if app.ENABLE_AURA_SYSTEM:
	import aura
import renderTarget
import new_uiWeeklyRank
if app.ENABLE_ACCE_COSTUME_SYSTEM:
	import acce
import emoji

# Vnum umiejetnosci Jezdziectwo - tooltip pokazuje jej progi bonusow.
SKILL_HORSE_RIDING = 130
if app.ENABLE_PREMIUM_PRIVATE_SHOP_OFFICIAL:
	import privateShop

item_ids = [50187, 50188, 90051, 90041, 90071]

POLY_DMG_VAL = {
	0 : [ 1,1,2,2,3,3,4,4,5,5,6,6,7,7,8,8,9,9,10,10 ],
	1 : [ 11,11,11,12,12,13,13,14,14,15,15 ],
	2 : [ 16,16,16,17,18,19,20,21,22,23,24 ],
	3 : [ 25,25 ]
}

if app.ENABLE_EXTRABONUS_SYSTEM:
	GLOVE_BONUS_TABLE = {
		118 : 20,
		72 : 30,
		113 : 30,
		17 : 50,
		71 : 25,
		23 : 15,
		1 : 2000,
		15 : 20,
		7 : 8,
		8 : 8,
		14 : 8,
		12 : 5,
		105 : 20,
	}


from costume_set_data import get_costume_manager

WARP_SCROLLS = [22011, 22000, 22010]

DESC_DEFAULT_MAX_COLS = 26
DESC_WESTERN_MAX_COLS = 35
DESC_WESTERN_MAX_WIDTH = 220

def chop(n):
	return round(n - 0.5, 1)

def SplitDescription(desc, limit):
	total_tokens = desc.split()
	line_tokens = []
	line_len = 0
	lines = []

	for token in total_tokens:
		if "|" in token:
			sep_pos = token.find("|")
			line_tokens.append(token[:sep_pos])
			lines.append(" ".join(line_tokens))
			line_len = len(token) - (sep_pos + 1)
			line_tokens = [token[sep_pos+1:]]
		elif app.WJ_MULTI_TEXTLINE and "\\n" in token:
			sep_pos = token.find("\\n")
			line_tokens.append(token[:sep_pos])

			lines.append(" ".join(line_tokens))
			line_len = len(token) - (sep_pos + 2)
			line_tokens = [token[sep_pos+2:]]
		else:
			line_len += len(token)
			if len(line_tokens) + line_len > limit:
				lines.append(" ".join(line_tokens))
				line_len = len(token)
				line_tokens = [token]
			else:
				line_tokens.append(token)

	if line_tokens:
		lines.append(" ".join(line_tokens))

	return lines

class ToolTip(ui.ThinBoard):

	swordEmoji = "  |Eemoji/sword|e  "
	klepsydraEmoji = "  |Eemoji/klepsydra|e  "

	TOOL_TIP_WIDTH = 220
	
	TOOL_TIP_HEIGHT = 10

	TEXT_LINE_HEIGHT = 17

	TITLE_COLOR = grp.GenerateColor(0.9490, 0.9058, 0.7568, 1.0)
	SPECIAL_TITLE_COLOR = grp.GenerateColor(1.0, 0.7843, 0.0, 1.0)
	SPECIAL_TITLE_COLOR2 = grp.GenerateColor(1.0, 0.8745, 0.4196, 1.0)

	NORMAL_COLOR = grp.GenerateColor(0.7607, 0.7607, 0.7607, 1.0)
	FONT_COLOR = grp.GenerateColor(0.7607, 0.7607, 0.7607, 1.0)
	PRICE_COLOR = 0xffFFB96D

	HIGH_PRICE_COLOR = SPECIAL_TITLE_COLOR
	MIDDLE_PRICE_COLOR = SPECIAL_TITLE_COLOR
	LOW_PRICE_COLOR = SPECIAL_TITLE_COLOR

	ENABLE_COLOR = grp.GenerateColor(0.7607, 0.7607, 0.7607, 1.0)
	DISABLE_COLOR = grp.GenerateColor(0.9, 0.4745, 0.4627, 1.0)

	NEGATIVE_COLOR = grp.GenerateColor(0.9, 0.4745, 0.4627, 1.0)
	POSITIVE_COLOR = grp.GenerateColor(0.5411, 0.7254, 0.5568, 1.0)
	SPECIAL_POSITIVE_COLOR2 = grp.GenerateColor((50.00 / 255), (250.00 / 255), (207.00 / 255), 1.0)
	SPECIAL_POSITIVE_COLOR = grp.GenerateColor(0.6911, 0.8754, 0.7068, 1.0)
	#SPECIAL_POSITIVE_COLOR2 = grp.GenerateColor(0.8824, 0.9804, 0.8824, 1.0)
	#SPECIAL_POSITIVE_COLOR2 = grp.GenerateColor(1.0, 0.8, 0.8, 1.0)
	SPECIAL_POSITIVE_COLOR5 = grp.GenerateColor(0.7824, 0.9004, 0.8024, 1.0)

	GLOVE_COLOR = grp.GenerateColor((122.00 / 255), (246.00 / 255), (212.00 / 255), 1.0)
	GLOVE_COLOR1 = grp.GenerateColor((137.00 / 255), (184.00 / 255), (141.00 / 255), 1.0)

	CONDITION_COLOR = 0xffBEB47D
	CAN_LEVEL_UP_COLOR = 0xff8EC292
	CANNOT_LEVEL_UP_COLOR = DISABLE_COLOR
	TEXTLINE_2ND_COLOR_DEFAULT = grp.GenerateColor(1.0, 1.0, 0.6078, 1.0)
	ITEMSHOP_UNIQUE_ITEM_COLOR = 0xFF008784
	NEED_SKILL_POINT_COLOR = 0xff9A9CDB
	renderOnKey = False

	def __init__(self, width = TOOL_TIP_WIDTH, isPickable=False):
		ui.ThinBoard.__init__(self, "TOP_MOST")

		if isPickable:
			pass
		else:
			self.AddFlag("not_pick")

		self.AddFlag("float")

		self.followFlag = True
		self.toolTipWidth = width

		self.xPos = -1
		self.yPos = -1

		self.defFontName = localeInfo.UI_DEF_FONT
		self.ClearToolTip()

	def __del__(self):
		ui.ThinBoard.__del__(self)

	def ClearToolTip(self):
		self.toolTipHeight = 12
		self.childrenList = []

	def SetFollow(self, flag):
		self.followFlag = flag

	def SetDefaultFontName(self, fontName):
		self.defFontName = fontName

	def AppendSpace(self, size):
		self.toolTipHeight += size
		self.ResizeToolTip()

	def AppendHorizontalLine(self):

		for i in range(2):
			horizontalLine = ui.Line()
			horizontalLine.SetParent(self)
			horizontalLine.SetPosition(0, self.toolTipHeight + 3 + i)
			horizontalLine.SetWindowHorizontalAlignCenter()
			horizontalLine.SetSize(150, 0)
			horizontalLine.Show()

			if 0 == i:
				horizontalLine.SetColor(0xff555555)
			else:
				horizontalLine.SetColor(0xff000000)

			self.childrenList.append(horizontalLine)

		self.toolTipHeight += 11
		self.ResizeToolTip()

	def AlignHorizonalCenter(self):
		for child in self.childrenList:
			(x, y)=child.GetLocalPosition()
			child.SetPosition(self.toolTipWidth/2, y)

		self.ResizeToolTip()

	def SetThinBoardSize(self, width, height = 12):
		self.toolTipWidth = width
		self.toolTipHeight = height

	if app.ENABLE_DUNGEON_INFO_SYSTEM:
		def TextAlignHorizonalCenter(self):
			for child in self.childrenList:
				(x, y) = child.GetLocalPosition()
				try:
					if child.GetText() != "":
						child.SetPosition(self.toolTipWidth / 2, y)
				except:
					pass

			self.ResizeToolTip()

	def AutoAppendTextLine(self, text, color = FONT_COLOR, centerAlign = True):
		textLine = ui.TextLine()
		textLine.SetParent(self)
		textLine.SetFontName(self.defFontName)
		textLine.SetPackedFontColor(color)
		textLine.SetText(text)
		textLine.SetOutline()
		textLine.SetFeather(False)
		textLine.Show()

		if centerAlign:
			textLine.SetPosition(self.toolTipWidth/2, self.toolTipHeight)
			textLine.SetHorizontalAlignCenter()

		else:
			textLine.SetPosition(10, self.toolTipHeight)

		self.childrenList.append(textLine)

		(textWidth, textHeight)=textLine.GetTextSize()

		textWidth += 40
		textHeight += 5

		if self.toolTipWidth < textWidth:
			self.toolTipWidth = textWidth

		self.toolTipHeight += textHeight

		return textLine


	def ResizeToolTipText(self, x, y):
		self.SetSize(x, y)
		
	def AppendTwoColorTextLine(self, text, color, text2, color2 = TEXTLINE_2ND_COLOR_DEFAULT, centerAlign = True):
		textLine = ui.TextLine()
		textLine.SetParent(self)
		textLine.SetFontName(self.defFontName)
		textLine.SetPackedFontColor(color)
		textLine.SetText(text)
		textLine.SetOutline()
		textLine.SetFeather(False)
		w, h = textLine.GetTextSize()
		
		textLine2 = ui.TextLine()
		textLine2.SetParent(textLine)
		textLine2.SetFontName(self.defFontName)
		textLine2.SetPackedFontColor(color2)
		textLine2.SetText(text2)
		textLine2.SetOutline()
		textLine2.SetFeather(False)
		textLine2.Show()
		
		w2, h2 = textLine2.GetTextSize()
		
		textLine.Show()
		if centerAlign:
			textLine.SetPosition(self.toolTipWidth/2-w2/2, self.toolTipHeight)
			textLine.SetHorizontalAlignCenter()
			textLine2.SetPosition(w // 2, 0)
		else:
			textLine.SetPosition(10, self.toolTipHeight)
		
		self.childrenList.append(textLine)
		self.childrenList.append(textLine2)
		
		self.toolTipHeight += self.TEXT_LINE_HEIGHT
		
		self.ResizeToolTip()
		return textLine
		
	def AutoAppendNewTextLine(self, text, color = FONT_COLOR, centerAlign = True):
		textLine = ui.TextLine()
		textLine.SetParent(self)
		textLine.SetFontName(self.defFontName)
		textLine.SetPackedFontColor(color)
		textLine.SetText(text)
		textLine.SetOutline()
		textLine.SetFeather(FALSE)
		textLine.Show()
		textLine.SetPosition(15, self.toolTipHeight)
		
		self.childrenList.append(textLine)
		(textWidth, textHeight) = textLine.GetTextSize()
		textWidth += 30
		textHeight += 10
		if self.toolTipWidth < textWidth:
			self.toolTipWidth = textWidth
		
		self.toolTipHeight += textHeight
		self.ResizeToolTipText(textWidth, self.toolTipHeight)
		return textLine

	def AppendTextLine(self, text, color = FONT_COLOR, centerAlign = True):
		textLine = ui.TextLine()
		textLine.SetParent(self)
		textLine.SetFontName(self.defFontName)
		textLine.SetPackedFontColor(color)
		textLine.SetText(text)
		textLine.SetOutline()
		textLine.SetFeather(False)
		if app.WJ_MULTI_TEXTLINE:
			textLine.SetLineHeight(self.TEXT_LINE_HEIGHT)

		if centerAlign:
			textLine.SetPosition(self.toolTipWidth / 2, self.toolTipHeight)
			textLine.SetHorizontalAlignCenter()
		else:
			textLine.SetPosition(10, self.toolTipHeight)

		textLine.Show()

		self.childrenList.append(textLine)

		if app.WJ_MULTI_TEXTLINE:
			lineCount = textLine.GetTextLineCount()
			self.toolTipHeight += self.TEXT_LINE_HEIGHT * lineCount
		else:
			self.toolTipHeight += self.TEXT_LINE_HEIGHT

		self.ResizeToolTip()

		return textLine

	def AppendDescription(self, desc, limit, color = FONT_COLOR):
		# Western (word-wrap) - breaks on spaces, not mid-word. The client is
		# Polish/Western so the Eastern char-wrap split garbled long names
		# (e.g. an affect name wrapping as "...podnoszenie p"/"rzedmiotow.").
		self.__AppendDescription_WesternLanguage(desc, limit, color)

	def __AppendDescription_EasternLanguage(self, description, characterLimitation, color=FONT_COLOR):
		length = len(description)
		if 0 == length:
			return

		lineCount = grpText.GetSplitingTextLineCount(description, characterLimitation)
		for i in range(lineCount):
			if 0 == i:
				self.AppendSpace(5)
			self.AppendTextLine(grpText.GetSplitingTextLine(description, characterLimitation, i), color)

	def __AppendDescription_WesternLanguage(self, desc, limit=DESC_WESTERN_MAX_COLS, color=FONT_COLOR):
		lines = SplitDescription(desc, limit)
		if not lines:
			return

		self.AppendSpace(5)
		for line in lines:
			self.AppendTextLine(line, color)


	def ResizeToolTip(self):
		self.SetSize(self.toolTipWidth, self.TOOL_TIP_HEIGHT + self.toolTipHeight)

	def SetTitle(self, name):
		self.AppendTextLine(name, self.TITLE_COLOR)

	def GetLimitTextLineColor(self, curValue, limitValue):
		if curValue < limitValue:
			return self.DISABLE_COLOR

		return self.ENABLE_COLOR

	def GetChangeTextLineColor(self, value, isSpecial=False):
		if value > 0:
			if isSpecial:
				return self.SPECIAL_POSITIVE_COLOR
			else:
				return self.POSITIVE_COLOR

		if 0 == value:
			return self.NORMAL_COLOR

		return self.NEGATIVE_COLOR

	def SetToolTipPosition(self, x = -1, y = -1):
		self.xPos = x
		self.yPos = y

	def ShowToolTip(self):
		self.SetTop()
		self.Show()

		self.OnUpdate()

	def HideToolTip(self):
		self.Hide()

	def OnUpdate(self):

		if not self.followFlag:
			return

		x = 0
		y = 0
		width = self.GetWidth()
		height = self.toolTipHeight

		if -1 == self.xPos and -1 == self.yPos:

			(mouseX, mouseY) = wndMgr.GetMousePosition()

			if mouseY < wndMgr.GetScreenHeight() - 300:
				y = mouseY + 40
			else:
				y = mouseY - height - 30

			x = mouseX - width // 2

		else:

			x = self.xPos - width // 2
			y = self.yPos - height

		x = max(x, 0)
		y = max(y, 0)
		x = min(x + width // 2, wndMgr.GetScreenWidth() - width // 2) - width // 2
		y = min(y + self.GetHeight(), wndMgr.GetScreenHeight()) - self.GetHeight()

		parentWindow = self.GetParentProxy()
		if parentWindow:
			(gx, gy) = parentWindow.GetGlobalPosition()
			x -= gx
			y -= gy

		self.SetPosition(x, y)

class ItemToolTip(ToolTip):
	CHARACTER_NAMES = (
		localeInfo.TOOLTIP_WARRIOR,
		localeInfo.TOOLTIP_ASSASSIN,
		localeInfo.TOOLTIP_SURA,
		localeInfo.TOOLTIP_SHAMAN
	)

	if app.ENABLE_WOLFMAN_CHARACTER:
		CHARACTER_NAMES += (
			localeInfo.TOOLTIP_WOLFMAN,
		)

	POSITIVE_COLOR = grp.GenerateColor(0.5411, 0.7254, 0.5568, 1.0)

	CHARACTER_COUNT = len(CHARACTER_NAMES)
	WEAR_NAMES = (
		localeInfo.TOOLTIP_ARMOR,
		localeInfo.TOOLTIP_HELMET,
		localeInfo.TOOLTIP_SHOES,
		localeInfo.TOOLTIP_WRISTLET,
		localeInfo.TOOLTIP_WEAPON,
		localeInfo.TOOLTIP_NECK,
		localeInfo.TOOLTIP_EAR,
		localeInfo.TOOLTIP_UNIQUE,
		localeInfo.TOOLTIP_SHIELD,
		localeInfo.TOOLTIP_ARROW,
	)
	WEAR_COUNT = len(WEAR_NAMES)

	AFFECT_DICT = {
		item.APPLY_MAX_HP : localeInfo.TOOLTIP_MAX_HP,
		item.APPLY_MAX_SP : localeInfo.TOOLTIP_MAX_SP,
		item.APPLY_CON : localeInfo.TOOLTIP_CON,
		item.APPLY_INT : localeInfo.TOOLTIP_INT,
		item.APPLY_STR : localeInfo.TOOLTIP_STR,
		item.APPLY_DEX : localeInfo.TOOLTIP_DEX,
		item.APPLY_ATT_SPEED : localeInfo.TOOLTIP_ATT_SPEED,
		item.APPLY_MOV_SPEED : localeInfo.TOOLTIP_MOV_SPEED,
		item.APPLY_CAST_SPEED : localeInfo.TOOLTIP_CAST_SPEED,
		item.APPLY_HP_REGEN : localeInfo.TOOLTIP_HP_REGEN,
		item.APPLY_SP_REGEN : localeInfo.TOOLTIP_SP_REGEN,
		item.APPLY_POISON_PCT : localeInfo.TOOLTIP_APPLY_POISON_PCT,
		item.APPLY_STUN_PCT : localeInfo.TOOLTIP_APPLY_STUN_PCT,
		item.APPLY_SLOW_PCT : localeInfo.TOOLTIP_APPLY_SLOW_PCT,
		item.APPLY_CRITICAL_PCT : localeInfo.TOOLTIP_APPLY_CRITICAL_PCT,
		item.APPLY_PENETRATE_PCT : localeInfo.TOOLTIP_APPLY_PENETRATE_PCT,
		item.APPLY_ATTBONUS_WARRIOR : localeInfo.TOOLTIP_APPLY_ATTBONUS_WARRIOR,
		item.APPLY_ATTBONUS_ASSASSIN : localeInfo.TOOLTIP_APPLY_ATTBONUS_ASSASSIN,
		item.APPLY_ATTBONUS_SURA : localeInfo.TOOLTIP_APPLY_ATTBONUS_SURA,
		item.APPLY_ATTBONUS_SHAMAN : localeInfo.TOOLTIP_APPLY_ATTBONUS_SHAMAN,
		item.APPLY_ATTBONUS_MONSTER : localeInfo.TOOLTIP_APPLY_ATTBONUS_MONSTER,
		item.APPLY_ATTBONUS_HUMAN : localeInfo.TOOLTIP_APPLY_ATTBONUS_HUMAN,
		item.APPLY_ATTBONUS_ANIMAL : localeInfo.TOOLTIP_APPLY_ATTBONUS_ANIMAL,
		item.APPLY_ATTBONUS_ORC : localeInfo.TOOLTIP_APPLY_ATTBONUS_ORC,
		item.APPLY_ATTBONUS_MILGYO : localeInfo.TOOLTIP_APPLY_ATTBONUS_MILGYO,
		item.APPLY_ATTBONUS_UNDEAD : localeInfo.TOOLTIP_APPLY_ATTBONUS_UNDEAD,
		item.APPLY_ATTBONUS_DEVIL : localeInfo.TOOLTIP_APPLY_ATTBONUS_DEVIL,
		item.APPLY_STEAL_HP : localeInfo.TOOLTIP_APPLY_STEAL_HP,
		item.APPLY_STEAL_SP : localeInfo.TOOLTIP_APPLY_STEAL_SP,
		item.APPLY_MANA_BURN_PCT : localeInfo.TOOLTIP_APPLY_MANA_BURN_PCT,
		item.APPLY_DAMAGE_SP_RECOVER : localeInfo.TOOLTIP_APPLY_DAMAGE_SP_RECOVER,
		item.APPLY_BLOCK : localeInfo.TOOLTIP_APPLY_BLOCK,
		item.APPLY_DODGE : localeInfo.TOOLTIP_APPLY_DODGE,
		item.APPLY_RESIST_SWORD : localeInfo.TOOLTIP_APPLY_RESIST_SWORD,
		item.APPLY_RESIST_TWOHAND : localeInfo.TOOLTIP_APPLY_RESIST_TWOHAND,
		item.APPLY_RESIST_DAGGER : localeInfo.TOOLTIP_APPLY_RESIST_DAGGER,
		item.APPLY_RESIST_BELL : localeInfo.TOOLTIP_APPLY_RESIST_BELL,
		item.APPLY_RESIST_FAN : localeInfo.TOOLTIP_APPLY_RESIST_FAN,
		item.APPLY_RESIST_BOW : localeInfo.TOOLTIP_RESIST_BOW,
		item.APPLY_RESIST_FIRE : localeInfo.TOOLTIP_RESIST_FIRE,
		item.APPLY_RESIST_ELEC : localeInfo.TOOLTIP_RESIST_ELEC,
		item.APPLY_RESIST_MAGIC : localeInfo.TOOLTIP_RESIST_MAGIC,
		item.APPLY_RESIST_WIND : localeInfo.TOOLTIP_APPLY_RESIST_WIND,
		item.APPLY_REFLECT_MELEE : localeInfo.TOOLTIP_APPLY_REFLECT_MELEE,
		item.APPLY_REFLECT_CURSE : localeInfo.TOOLTIP_APPLY_REFLECT_CURSE,
		item.APPLY_POISON_REDUCE : localeInfo.TOOLTIP_APPLY_POISON_REDUCE,
		item.APPLY_KILL_SP_RECOVER : localeInfo.TOOLTIP_APPLY_KILL_SP_RECOVER,
		item.APPLY_EXP_DOUBLE_BONUS : localeInfo.TOOLTIP_APPLY_EXP_DOUBLE_BONUS,
		item.APPLY_GOLD_DOUBLE_BONUS : localeInfo.TOOLTIP_APPLY_GOLD_DOUBLE_BONUS,
		item.APPLY_ITEM_DROP_BONUS : localeInfo.TOOLTIP_APPLY_ITEM_DROP_BONUS,
		item.APPLY_POTION_BONUS : localeInfo.TOOLTIP_APPLY_POTION_BONUS,
		item.APPLY_KILL_HP_RECOVER : localeInfo.TOOLTIP_APPLY_KILL_HP_RECOVER,
		item.APPLY_IMMUNE_STUN : localeInfo.TOOLTIP_APPLY_IMMUNE_STUN,
		item.APPLY_IMMUNE_SLOW : localeInfo.TOOLTIP_APPLY_IMMUNE_SLOW,
		item.APPLY_IMMUNE_FALL : localeInfo.TOOLTIP_APPLY_IMMUNE_FALL,
		item.APPLY_BOW_DISTANCE : localeInfo.TOOLTIP_BOW_DISTANCE,
		item.APPLY_DEF_GRADE_BONUS : localeInfo.TOOLTIP_DEF_GRADE,
		item.APPLY_ATT_GRADE_BONUS : localeInfo.TOOLTIP_ATT_GRADE,
		item.APPLY_MAGIC_ATT_GRADE : localeInfo.TOOLTIP_MAGIC_ATT_GRADE,
		item.APPLY_MAGIC_DEF_GRADE : localeInfo.TOOLTIP_MAGIC_DEF_GRADE,
		item.APPLY_MAX_STAMINA : localeInfo.TOOLTIP_MAX_STAMINA,
		item.APPLY_MALL_ATTBONUS : localeInfo.TOOLTIP_MALL_ATTBONUS,
		item.APPLY_MALL_DEFBONUS : localeInfo.TOOLTIP_MALL_DEFBONUS,
		item.APPLY_MALL_EXPBONUS : localeInfo.TOOLTIP_MALL_EXPBONUS,
		item.APPLY_MALL_ITEMBONUS : localeInfo.TOOLTIP_MALL_ITEMBONUS,
		item.APPLY_MALL_GOLDBONUS : localeInfo.TOOLTIP_MALL_GOLDBONUS,
		item.APPLY_SKILL_DAMAGE_BONUS : localeInfo.TOOLTIP_SKILL_DAMAGE_BONUS,
		item.APPLY_NORMAL_HIT_DAMAGE_BONUS : localeInfo.TOOLTIP_NORMAL_HIT_DAMAGE_BONUS,
		item.APPLY_SKILL_DEFEND_BONUS : localeInfo.TOOLTIP_SKILL_DEFEND_BONUS,
		item.APPLY_NORMAL_HIT_DEFEND_BONUS : localeInfo.TOOLTIP_NORMAL_HIT_DEFEND_BONUS,
		item.APPLY_PC_BANG_EXP_BONUS : localeInfo.TOOLTIP_MALL_EXPBONUS_P_STATIC,
		item.APPLY_PC_BANG_DROP_BONUS : localeInfo.TOOLTIP_MALL_ITEMBONUS_P_STATIC,
		item.APPLY_RESIST_WARRIOR : localeInfo.TOOLTIP_APPLY_RESIST_WARRIOR,
		item.APPLY_RESIST_ASSASSIN : localeInfo.TOOLTIP_APPLY_RESIST_ASSASSIN,
		item.APPLY_RESIST_SURA : localeInfo.TOOLTIP_APPLY_RESIST_SURA,
		item.APPLY_RESIST_SHAMAN : localeInfo.TOOLTIP_APPLY_RESIST_SHAMAN,
		item.APPLY_MAX_HP_PCT : localeInfo.TOOLTIP_APPLY_MAX_HP_PCT,
		item.APPLY_MAX_SP_PCT : localeInfo.TOOLTIP_APPLY_MAX_SP_PCT,
		item.APPLY_ENERGY : localeInfo.TOOLTIP_ENERGY,
		item.APPLY_COSTUME_ATTR_BONUS : localeInfo.TOOLTIP_COSTUME_ATTR_BONUS,
		item.APPLY_MAGIC_ATTBONUS_PER : localeInfo.TOOLTIP_MAGIC_ATTBONUS_PER,
		item.APPLY_MELEE_MAGIC_ATTBONUS_PER : localeInfo.TOOLTIP_MELEE_MAGIC_ATTBONUS_PER,
		item.APPLY_RESIST_ICE : localeInfo.TOOLTIP_RESIST_ICE,
		item.APPLY_RESIST_EARTH : localeInfo.TOOLTIP_RESIST_EARTH,
		item.APPLY_RESIST_DARK : localeInfo.TOOLTIP_RESIST_DARK,
		item.APPLY_ANTI_CRITICAL_PCT : localeInfo.TOOLTIP_ANTI_CRITICAL_PCT,
		item.APPLY_ANTI_PENETRATE_PCT : localeInfo.TOOLTIP_ANTI_PENETRATE_PCT,
		item.APPLY_RESIST_HUMAN : localeInfo.TOOLTIP_APPLY_RESIST_HUMAN,
		item.APPLY_ATTBONUS_BOSS : localeInfo.TOOLTIP_APPLY_ATTBONUS_BOSS,
		item.APPLY_ATTBONUS_WLADCA : localeInfo.TOOLTIP_APPLY_ATTBONUS_WLADCA,
		item.APPLY_ATTBONUS_STONE : localeInfo.TOOLTIP_APPLY_ATTBONUS_STONE,
		item.APPLY_RESIST_BOSS : localeInfo.TOOLTIP_RESIST_BOSS,
		item.APPLY_RESIST_WLADCA : localeInfo.TOOLTIP_RESIST_WLADCA,
		item.APPLY_RESIST_MONSTER : localeInfo.TOOLTIP_RESIST_MONSTER,
		item.APPLY_STAT_BONUS: localeInfo.TOOLTIP_STAT_BONUS,
		item.APPLY_ATTBONUS_DUNGEON : localeInfo.TOOLTIP_ATTBONUS_DUNGEON,
		item.APPLY_ATTBONUS_KLASY : localeInfo.TOOLTIP_APPLY_ATTBONUS_KLASY,
		item.APPLY_RESIST_KLASY : localeInfo.TOOLTIP_APPLY_RESIST_KLASY,
        item.APPLY_ATTBONUS_LEGENDA : localeInfo.TOOLTIP_APPLY_ATTBONUS_LEGENDA,
		item.APPLY_DMG_BONUS : localeInfo.TOOLTIP_APPLY_DMG_BONUS,
		item.APPLY_FINAL_DMG_BONUS : localeInfo.TOOLTIP_APPLY_FINAL_DMG_BONUS,
		item.APPLY_MINING_SUCCESS_CHANCE : localeInfo.TOOLTIP_MINING_SUCCESS_CHANCE,
		item.APPLY_MINING_MORE_ORES_CHANCE : localeInfo.TOOLTIP_MINING_MORE_ORES_CHANCE,
		item.APPLY_MINING_LESS_MINE_TIME : localeInfo.TOOLTIP_MINING_LESS_MINE_TIME,
		item.APPLY_MINING_MORE_POINTS : localeInfo.TOOLTIP_MINING_MORE_POINTS,

		item.APPLY_FISHING_INSTANT_CATCH_CHANCE : localeInfo.TOOLTIP_FISHING_INSTANT_CATCH_CHANCE,
		item.APPLY_FISHING_BIGGER_FISH_CHANCE : localeInfo.TOOLTIP_FISHING_BIGGER_FISH_CHANCE,
		item.APPLY_FISHING_NEXT_SECTION_CHANCE : localeInfo.TOOLTIP_FISHING_NEXT_SECTION_CHANCE,
		item.APPLY_FISHING_MORE_YANG_MULTIPLIER : localeInfo.TOOLTIP_FISHING_MORE_YANG_MULTIPLIER,
		item.APPLY_FISHING_MORE_POINTS_CHANCE : localeInfo.TOOLTIP_FISHING_MORE_POINTS_CHANCE,
		item.APPLY_FISHING_SUCCESS_CHANCE : localeInfo.TOOLTIP_FISHING_SUCCESS_CHANCE,
		item.APPLY_ATTBONUS_PVM_SKILL : localeInfo.TOOLTIP_ATTBONUS_PVM_SKILL,
		item.APPLY_ATTBONUS_ELEMENT : localeInfo.TOOLTIP_ATTBONUS_ELEMENT,
		item.APPLY_DEFBONUS_ELEMENT : localeInfo.TOOLTIP_DEFBONUS_ELEMENT,
		item.APPLY_ENCHANT_ELECT : localeInfo.TOOLTIP_ENCHANT_ELEC,
		item.APPLY_ENCHANT_FIRE : localeInfo.TOOLTIP_ENCHANT_FIRE,
		item.APPLY_ENCHANT_ICE : localeInfo.TOOLTIP_ENCHANT_ICE,
		item.APPLY_ENCHANT_WIND : localeInfo.TOOLTIP_ENCHANT_WIND,
		item.APPLY_ENCHANT_EARTH : localeInfo.TOOLTIP_ENCHANT_EARTH,
		item.APPLY_ENCHANT_DARK : localeInfo.TOOLTIP_ENCHANT_DARK,
		item.APPLY_DOUBLE_LOOT_SUMMER : localeInfo.TOOLTIP_DOUBLE_LOOT_SUMMER,
		item.APPLY_DOUBLE_LOOT_DROP : localeInfo.TOOLTIP_DOUBLE_LOOT_DROP,
	}
	AFFECT_DICT_POLY = {
		item.APPLY_ATTBONUS_HUMAN : localeInfo.TOOLTIP_APPLY_ATTBONUS_HUMAN_POLY,
		item.APPLY_ATTBONUS_MONSTER : localeInfo.TOOLTIP_APPLY_ATTBONUS_MONSTER_POLY,
		item.APPLY_ATTBONUS_BOSS : localeInfo.TOOLTIP_APPLY_ATTBONUS_BOSS_POLY,
		item.APPLY_ATTBONUS_STONE : localeInfo.TOOLTIP_APPLY_ATTBONUS_STONE_POLY,
		item.APPLY_MAX_HP : localeInfo.TOOLTIP_APPLY_ATTBONUS_MAX_HP_POLY,
		item.APPLY_ENCHANT_DARK : localeInfo.TOOLTIP_APPLY_ATTBONUS_ENCHANT_DARK_POLY,
		item.APPLY_ATTBONUS_WLADCA : localeInfo.TOOLTIP_APPLY_ATTBONUS_WLADCA_POLY,
		item.APPLY_ATTBONUS_ELEMENT : localeInfo.TOOLTIP_ATTBONUS_ELEMENT_POLY,
	}

	MAX_AFFECT_VALUE = {
		0: -1,
		item.APPLY_MAX_HP: 2500,
		item.APPLY_MAX_SP: 200,
		item.APPLY_CON: 12,
		item.APPLY_INT: 12,
		item.APPLY_STR: 12,
		item.APPLY_DEX: 12,
		item.APPLY_ATT_SPEED: 8,
		item.APPLY_MOV_SPEED: 20,
		item.APPLY_CAST_SPEED: 20,
		item.APPLY_HP_REGEN: 30,
		item.APPLY_SP_REGEN: 20,
		item.APPLY_POISON_PCT: 8,
		item.APPLY_STUN_PCT: 8,
		item.APPLY_SLOW_PCT: 8,
		item.APPLY_CRITICAL_PCT: 10,
		item.APPLY_PENETRATE_PCT: 20,
		item.APPLY_ATTBONUS_WARRIOR: 10,
		item.APPLY_ATTBONUS_ASSASSIN: 10,
		item.APPLY_ATTBONUS_SURA: 10,
		item.APPLY_ATTBONUS_SHAMAN: 10,
		item.APPLY_ATTBONUS_MONSTER: 10,
		item.APPLY_ATTBONUS_HUMAN: 10,
		item.APPLY_ATTBONUS_ANIMAL: 20,
		item.APPLY_ATTBONUS_ORC: 20,
		item.APPLY_ATTBONUS_MILGYO: 20,
		item.APPLY_ATTBONUS_UNDEAD: 20,
		item.APPLY_ATTBONUS_DEVIL: 20,
		item.APPLY_STEAL_HP: 10,
		item.APPLY_STEAL_SP: 10,
		item.APPLY_MANA_BURN_PCT: 10,
		item.APPLY_DAMAGE_SP_RECOVER: 0,
		item.APPLY_BLOCK: 15,
		item.APPLY_DODGE: 15,
		item.APPLY_RESIST_SWORD: 15,
		item.APPLY_RESIST_TWOHAND: 15,
		item.APPLY_RESIST_DAGGER: 15,
		item.APPLY_RESIST_BELL: 15,
		item.APPLY_RESIST_FAN: 15,
		item.APPLY_RESIST_BOW: 15,
		item.APPLY_RESIST_FIRE: 15,
		item.APPLY_RESIST_ELEC: 15,
		item.APPLY_RESIST_MAGIC: 15,
		item.APPLY_RESIST_WIND: 15,
		item.APPLY_REFLECT_MELEE: 10,
		item.APPLY_REFLECT_CURSE: 0,
		item.APPLY_POISON_REDUCE: 8,
		item.APPLY_KILL_SP_RECOVER: 0,
		item.APPLY_EXP_DOUBLE_BONUS: 20,
		item.APPLY_GOLD_DOUBLE_BONUS: 20,
		item.APPLY_ITEM_DROP_BONUS: 20,
		item.APPLY_POTION_BONUS: 0,
		item.APPLY_KILL_HP_RECOVER: 0,
		item.APPLY_IMMUNE_STUN: 1,
		item.APPLY_IMMUNE_SLOW: 1,
		item.APPLY_IMMUNE_FALL: 0,
		item.APPLY_BOW_DISTANCE: 0,
		item.APPLY_DEF_GRADE_BONUS: 0,
		item.APPLY_ATT_GRADE_BONUS: 50,
		item.APPLY_MAGIC_ATT_GRADE: 0,
		item.APPLY_MAGIC_DEF_GRADE: 0,
		item.APPLY_MAX_STAMINA: 0,
		item.APPLY_MALL_ATTBONUS: 0,
		item.APPLY_MALL_DEFBONUS: 0,
		item.APPLY_MALL_EXPBONUS: 0,
		item.APPLY_MALL_ITEMBONUS: 0,
		item.APPLY_MALL_GOLDBONUS: 0,
		item.APPLY_SKILL_DAMAGE_BONUS: 0,
		item.APPLY_NORMAL_HIT_DAMAGE_BONUS: 0,
		item.APPLY_SKILL_DEFEND_BONUS: 0,
		item.APPLY_NORMAL_HIT_DEFEND_BONUS: 0,
		item.APPLY_PC_BANG_EXP_BONUS: 0,
		item.APPLY_PC_BANG_DROP_BONUS: 0,
		item.APPLY_RESIST_WARRIOR: 5,
		item.APPLY_RESIST_ASSASSIN: 5,
		item.APPLY_RESIST_SURA: 5,
		item.APPLY_RESIST_SHAMAN: 5,
		item.APPLY_MAX_HP_PCT: 0,
		item.APPLY_MAX_SP_PCT: 0,
		item.APPLY_ENERGY: 0,
		item.APPLY_COSTUME_ATTR_BONUS: 0,
		item.APPLY_MAGIC_ATTBONUS_PER: 0,
		item.APPLY_MELEE_MAGIC_ATTBONUS_PER: 0,
		item.APPLY_RESIST_ICE: 0,
		item.APPLY_RESIST_EARTH: 0,
		item.APPLY_RESIST_DARK: 0,
		item.APPLY_ANTI_CRITICAL_PCT: 0,
		item.APPLY_ANTI_PENETRATE_PCT: 0,
		item.APPLY_STAT_BONUS : 0,
		item.APPLY_RESIST_MONSTER : 0,
		item.APPLY_ATTBONUS_DUNGEON : 0,
		item.APPLY_ATTBONUS_LEGENDA : 0,
		item.APPLY_ATTBONUS_KLASY : 0,
		item.APPLY_DMG_BONUS : 0,
		item.APPLY_FINAL_DMG_BONUS : 0,
		item.APPLY_RESIST_MONSTER : 0,
		item.APPLY_RESIST_BOSS : 0,
		item.APPLY_RESIST_WLADCA : 0,
		item.APPLY_RESIST_HUMAN : 0,
		item.APPLY_ATTBONUS_BOSS : 0,
		item.APPLY_ATTBONUS_STONE : 0,
		item.APPLY_RESIST_KLASY : 0,
	}

	MAX_AFFECT_VALUE_BELT = {
		0 : -1,
		item.APPLY_ATTBONUS_ANIMAL : 10,
		item.APPLY_RESIST_BELL : 10,
		item.APPLY_INT : 10,
		item.APPLY_STR : 10,
		item.APPLY_DEX : 10,
		item.APPLY_ATTBONUS_ORC : 10,
		item.APPLY_ATTBONUS_DEVIL : 10,
		item.APPLY_ATTBONUS_UNDEAD : 10,
		item.APPLY_RESIST_FAN : 10,
		item.APPLY_MAGIC_ATT_GRADE : 75,
		item.APPLY_ATT_GRADE_BONUS : 100,
		item.APPLY_RESIST_SWORD : 10,
		item.APPLY_RESIST_TWOHAND : 10,
		item.APPLY_RESIST_BOW : 10,
		item.APPLY_RESIST_DAGGER : 10,
	}
	MAX_AFFECT_VALUE_GLOVE = {
		0 : -1,
		item.APPLY_ATTBONUS_HUMAN : 7,
		item.APPLY_ATTBONUS_MILGYO : 7,
		item.APPLY_ATTBONUS_ORC : 7,
		item.APPLY_ATTBONUS_UNDEAD : 7,
		item.APPLY_MAX_SP : 1000,
		item.APPLY_ATTBONUS_STONE : 7,
		item.APPLY_ATTBONUS_DEVIL : 7,
		item.APPLY_STAT_BONUS : 7,
		item.APPLY_ATT_GRADE_BONUS : 75,
		item.APPLY_FINAL_DMG_BONUS : 0,
		item.APPLY_NORMAL_HIT_DAMAGE_BONUS : 0,
		item.APPLY_ATTBONUS_DUNGEON : 0,
		item.APPLY_SKILL_DAMAGE_BONUS : 0,
		item.APPLY_STEAL_HP : 0,
		item.APPLY_MAX_HP : 0,
		item.APPLY_CRITICAL_PCT : 0,
		item.APPLY_ATT_SPEED : 0,
		item.APPLY_MOV_SPEED : 0,
		item.APPLY_SLOW_PCT : 0,
		item.APPLY_POISON_PCT : 0,
		item.APPLY_RESIST_HUMAN : 0,
	}

	ATTRIBUTE_NEED_WIDTH = {
		23 : 230,
		24 : 230,
		25 : 230,
		26 : 220,
		27 : 210,

		35 : 210,
		36 : 210,
		37 : 210,
		38 : 210,
		39 : 210,
		40 : 210,
		41 : 210,

		42 : 220,
		43 : 230,
		45 : 230,
	}

	ANTI_FLAG_DICT = {
		0 : item.ITEM_ANTIFLAG_WARRIOR,
		1 : item.ITEM_ANTIFLAG_ASSASSIN,
		2 : item.ITEM_ANTIFLAG_SURA,
		3 : item.ITEM_ANTIFLAG_SHAMAN,
	}
	if app.ENABLE_WOLFMAN_CHARACTER:
		ANTI_FLAG_DICT.update({
			4 : item.ITEM_ANTIFLAG_WOLFMAN,
		})

	FONT_COLOR = grp.GenerateColor(0.7607, 0.7607, 0.7607, 1.0)

	def __init__(self, *args, **kwargs):
		ToolTip.__init__(self, *args, **kwargs)
		self.itemVnum = 0
		self.metinSlot = []
		self.isShopItem = False
		if app.ENABLE_OFFLINE_SHOP_SYSTEM:
			self.isOfflineShopItem = False

		self.bCannotUseItemForceSetDisableColor = True

		self.modelShow = True
		self.modelPreviewBoard = None
		self.modelPreviewRender = None
		self.modelPreviewSeparator = None
		self.modelPreviewTextLine = None
		self.modelPreviewKey = None
		self.modelPreviewRequested = False

		if app.ENABLE_PREMIUM_PRIVATE_SHOP_OFFICIAL:
			self.isPrivateSearchItem = False
			self.isPrivateShopSaleItem = False

	def __del__(self):
		ToolTip.__del__(self)
		self.metinSlot = None

	def SetCannotUseItemForceSetDisableColor(self, enable):
		self.bCannotUseItemForceSetDisableColor = enable

	def __AppendRealTimeToolTip(self, itemVnum, endTime):
		item.SelectItem(itemVnum)
		for i in range(item.LIMIT_MAX_NUM):
			(limitType, limitValue) = item.GetLimit(i)
			if item.LIMIT_REAL_TIME == limitType and limitValue > 0:
				self.AppendSpace(5)
				leftSec = max(0, endTime - app.GetGlobalTimeStamp())
				if leftSec > 0:
					self.AppendTextLine(localeInfo.LEFT_TIME + " : " + localeInfo.SecondToDHM(leftSec), self.NORMAL_COLOR)
				return
			else:
				continue

	def CanEquip(self):
		if app.ENABLE_PREMIUM_PRIVATE_SHOP_OFFICIAL:
			if self.isPrivateSearchItem or self.isPrivateShopSaleItem:
				return True

		if not item.IsEquipmentVID(self.itemVnum):
			return True

		race = player.GetOriginalRace()
		job = chr.RaceToJob(race)
		if job not in self.ANTI_FLAG_DICT:
			return False

		if item.IsAntiFlag(self.ANTI_FLAG_DICT[job]):
			return False

		sex = chr.RaceToSex(race)

		MALE = 1
		FEMALE = 0

		if item.IsAntiFlag(item.ITEM_ANTIFLAG_MALE) and sex == MALE:
			return False

		if item.IsAntiFlag(item.ITEM_ANTIFLAG_FEMALE) and sex == FEMALE:
			return False

		for i in range(item.LIMIT_MAX_NUM):
			(limitType, limitValue) = item.GetLimit(i)

			if item.LIMIT_LEVEL == limitType:
				if player.GetStatus(player.LEVEL) < limitValue:
					return False
			"""
			elif item.LIMIT_STR == limitType:
				if player.GetStatus(player.ST) < limitValue:
					return False
			elif item.LIMIT_DEX == limitType:
				if player.GetStatus(player.DX) < limitValue:
					return False
			elif item.LIMIT_INT == limitType:
				if player.GetStatus(player.IQ) < limitValue:
					return False
			elif item.LIMIT_CON == limitType:
				if player.GetStatus(player.HT) < limitValue:
					return False
			"""

		return True
		
	def AppendTextLine(self, text, color = FONT_COLOR, centerAlign = True):
		if not self.CanEquip() and self.bCannotUseItemForceSetDisableColor:
			color = self.DISABLE_COLOR

		return ToolTip.AppendTextLine(self, text, color, centerAlign)

	def GetAffectStrings(self, affectType, affectValue):
		if 0 == affectType:
			return None

		if 0 == affectValue:
			return None

		try:
			return self.AFFECT_DICT[affectType](affectValue)
		except TypeError:
			return "UNKNOWN_VALUE[%s] %s" % (affectType, affectValue)
		except KeyError:
			return "UNKNOWN_TYPE[%s] %s" % (affectType, affectValue)

	def ClearToolTip(self):
		self.isShopItem = False
		self.toolTipWidth = self.TOOL_TIP_WIDTH
		if app.ENABLE_PREMIUM_PRIVATE_SHOP_OFFICIAL:
			self.isPrivateSearchItem = False
			self.isPrivateShopSaleItem = False
		ToolTip.ClearToolTip(self)

	if app.ENABLE_PREMIUM_PRIVATE_SHOP_OFFICIAL:
		def SetPrivateShopItem(self, slotIndex):
			itemVnum = privateShop.GetItemVnum(slotIndex)
			if 0 == itemVnum:
				return

			self.ClearToolTip()

			metinSlot = []
			for i in range(player.METIN_SOCKET_MAX_NUM):
				metinSlot.append(privateShop.GetItemMetinSocket(slotIndex, i))
			attrSlot = []
			for i in range(player.ATTRIBUTE_SLOT_MAX_NUM):
				attrSlot.append(privateShop.GetItemAttribute(slotIndex, i))

			args = {}
			if app.ENABLE_PRIVATE_SHOP_REFINE_ELEMENT:
				args["refineElement"] = privateShop.GetItemRefineElement(slotIndex)

			apply_random_list = []
			if app.ENABLE_PRIVATE_SHOP_APPLY_RANDOM:
				for i in range(player.APPLY_RANDOM_SLOT_MAX_NUM):
					apply_random_list.append(privateShop.GetItemApplyRandom(slotIndex, i))
				args["apply_random_list"] = apply_random_list

			self.AddItemData(itemVnum, metinSlot, attrSlot, **args)

			if app.ENABLE_PRIVATE_SHOP_CHANGE_LOOK:
				changelookvnum = privateShop.GetItemChangeLookVnum(slotIndex)
				self.AppendChangeLookInfoItemVnum(changelookvnum)

			if app.ENABLE_CHEQUE_SYSTEM:
				goldPrice = privateShop.GetItemPrice(slotIndex)
				chequePrice = privateShop.GetChequeItemPrice(slotIndex)
				self.AppendSellingPrice(goldPrice, chequePrice, True)
			else:
				self.AppendSellingPrice(privateShop.GetItemPrice(slotIndex))


		def SetPrivateShopSearchItem(self, slotIndex):
			itemVnum = privateShop.GetSearchItemVnum(slotIndex)
			if 0 == itemVnum:
				return

			self.ClearToolTip()
			self.isPrivateSearchItem = True

			metinSlot = []
			for i in range(player.METIN_SOCKET_MAX_NUM):
				metinSlot.append(privateShop.GetSearchItemMetinSocket(slotIndex, i))
			attrSlot = []
			for i in range(player.ATTRIBUTE_SLOT_MAX_NUM):
				attrSlot.append(privateShop.GetSearchItemAttribute(slotIndex, i))

			args = {}
			if app.ENABLE_PRIVATE_SHOP_REFINE_ELEMENT:
				args["refineElement"] = privateShop.GetSearchItemRefineElement(slotIndex)

			apply_random_list = []
			if app.ENABLE_PRIVATE_SHOP_APPLY_RANDOM:
				for i in range(player.APPLY_RANDOM_SLOT_MAX_NUM):
					apply_random_list.append(privateShop.GetSearchItemApplyRandom(slotIndex, i))
				args["apply_random_list"] = apply_random_list

			self.AddItemData(itemVnum, metinSlot, attrSlot, **args)

			if app.ENABLE_PRIVATE_SHOP_CHANGE_LOOK:
				changelookvnum = privateShop.GetSearchItemChangeLookVnum(slotIndex)
				self.AppendChangeLookInfoItemVnum(changelookvnum)

		def SetPrivateShopSaleItem(self, slotIndex):
			itemVnum = privateShop.GetSaleItemVnum(slotIndex)
			if 0 == itemVnum:
				return

			self.ClearToolTip()
			self.isPrivateShopSaleItem = True

			self.itemVnum = itemVnum

			metinSlot = []
			for i in range(player.METIN_SOCKET_MAX_NUM):
				metinSlot.append(privateShop.GetSaleItemMetinSocket(slotIndex, i))
			attrSlot = []
			for i in range(player.ATTRIBUTE_SLOT_MAX_NUM):
				attrSlot.append(privateShop.GetSaleItemAttribute(slotIndex, i))

			args = {}
			if app.ENABLE_PRIVATE_SHOP_REFINE_ELEMENT:
				args["refineElement"] = privateShop.GetSaleItemRefineElement(slotIndex)

			apply_random_list = []
			if app.ENABLE_PRIVATE_SHOP_APPLY_RANDOM:
				for i in range(player.APPLY_RANDOM_SLOT_MAX_NUM):
					apply_random_list.append(privateShop.GetSaleItemApplyRandom(slotIndex, i))
				args["apply_random_list"] = apply_random_list

			self.AddItemData(itemVnum, metinSlot, attrSlot, **args)

			if app.ENABLE_PRIVATE_SHOP_CHANGE_LOOK:
				changelookvnum = privateShop.GetSaleItemChangeLookVnum(slotIndex)
				self.AppendChangeLookInfoItemVnum(changelookvnum)

			self.AppendHorizontalLine()

			self.AppendTextLine(localeInfo.PREMIUM_PRIVATE_SALE_CUSTOMER % privateShop.GetSaleCustomerName(slotIndex), self.TITLE_COLOR)

			timestamp = privateShop.GetSaleTime(slotIndex)

			self.AppendTextLine(localeInfo.PREMIUM_PRIVATE_SALE_TIME % localeInfo.GetFullDateFormat(timestamp), self.TITLE_COLOR)
			self.AppendSpace(2)

			if app.ENABLE_CHEQUE_SYSTEM:
				goldPrice = privateShop.GetSaleItemPrice(slotIndex)
				chequePrice = privateShop.GetSaleChequeItemPrice(slotIndex)
				self.AppendSellingPrice(goldPrice, chequePrice, True)
			else:
				self.AppendSellingPrice(privateShop.GetSaleItemPrice(slotIndex))

	if app.ENABLE_OFFLINE_SHOP_SYSTEM:
		def SetOfflineShopBuilderItem(self, invenType, invenPos, offlineShopIndex):
			itemVnum = player.GetItemIndex(invenType, invenPos)
			if (itemVnum == 0):
				return

			item.SelectItem(itemVnum)
			self.ClearToolTip()

			metinSlot = []
			for i in range(player.METIN_SOCKET_MAX_NUM):
				metinSlot.append(player.GetItemMetinSocket(invenType, invenPos, i))
			attrSlot = []
			for i in range(player.ATTRIBUTE_SLOT_MAX_NUM):
				attrSlot.append(player.GetItemAttribute(invenType, invenPos, i))

			self.AddItemData(itemVnum, metinSlot, attrSlot)

			self.AppendTextLine(localeInfo.TOOLTIP_BUYPRICE_TEXT)
			self.AppendHorizontalLine()
			self.AppendOfflineShopSellingPrice(shop.GetOfflineShopItemPriceDisplayGold(invenType, invenPos), shop.GetOfflineShopItemPriceDisplayCheque(invenType, invenPos))

		def SetOfflineShopItem(self, slotIndex):
			itemVnum = shop.GetOfflineShopItemID(slotIndex)
			if (itemVnum == 0):
				return

			price_gold = shop.GetOfflineShopItemPriceGold(slotIndex)
			price_cheque = shop.GetOfflineShopItemPriceCheque(slotIndex)

			self.ClearToolTip()
			self.isOfflineShopItem = True

			metinSlot = []
			for i in range(player.METIN_SOCKET_MAX_NUM):
				metinSlot.append(shop.GetOfflineShopItemMetinSocket(slotIndex, i))
			attrSlot = []
			for i in range(player.ATTRIBUTE_SLOT_MAX_NUM):
				attrSlot.append(shop.GetOfflineShopItemAttribute(slotIndex, i))

			self.AddItemData(itemVnum, metinSlot, attrSlot)

			self.AppendTextLine(localeInfo.SELL_PRICE)
			if price_gold > 0:
				self.AppendPrice(price_gold)
			if price_cheque > 0:
				self.AppendCheque(price_cheque)

			count = shop.GetOfflineShopItemCount(slotIndex)
			wyliczenie = (price_gold/count)
			wyliczenie2 = (price_cheque/count)

			if wyliczenie != 0 or wyliczenie2 != 0:
				if count > 1:
					self.AppendSpace(15)
					self.AppendTextLine(constInfo.price_color1+"P\xf8edpokl\xe1dan\xe1 cena za 1ks.")

				if not price_gold <= 0:
					if wyliczenie != 0:
						if count > 1:
							self.AppendSpace(5)
							self.AppendTextLine(localeInfo.NumberToGoldNotText(wyliczenie)+" {}".format(emoji.AppendEmoji("icon/emoji/money_icon.png")), self.GetPriceColor(wyliczenie))
							self.AppendSpace(2)

				if not price_cheque <= 0:
					if wyliczenie2 != 0:
						if count > 1:
							self.AppendSpace(5)
							self.AppendTextLine(localeInfo.NumberToGoldNotText(wyliczenie2)+" {}".format(emoji.AppendEmoji("icon/emoji/cheque_icon.png")), grp.GenerateColor(184./255, 184./255, 184./255, 1))
							self.AppendSpace(2)

	def SetInventoryItem(self, slotIndex, window_type = player.INVENTORY):
		itemVnum = player.GetItemIndex(window_type, slotIndex)
		if 0 == itemVnum:
			return

		self.ClearToolTip()
		if shop.IsOpen():
			if not shop.IsPrivateShop():
				item.SelectItem(itemVnum)
				self.AppendSellingPrice(player.GetISellItemPrice(window_type, slotIndex))

		metinSlot = [player.GetItemMetinSocket(window_type, slotIndex, i) for i in range(player.METIN_SOCKET_MAX_NUM)]
		attrSlot = [player.GetItemAttribute(window_type, slotIndex, i) for i in range(player.ATTRIBUTE_SLOT_MAX_NUM)]

		self.AddItemData(itemVnum, metinSlot, attrSlot, 0, 0, window_type, slotIndex)

		if getattr(constInfo, "SAFEBOX_OPENED", False) and window_type == player.INVENTORY:
			item.SelectItem(itemVnum)
			if not item.IsAntiFlag(item.ANTIFLAG_SAFEBOX):
				self.AppendSpace(5)
				self.AppendTextLine(localeInfo.TOOLTIP_SAFEBOX_DEPOSIT, self.POSITIVE_COLOR)

	def FormatMultiplePurchaseText(self):
		return localeInfo.MULTIPLE_PURCHASE.format(
			key_shift=emoji.AppendEmoji("icon/emoji/key_shift.png"),
			key_rclick=emoji.AppendEmoji("icon/emoji/key_rclick.png")
		)

	def SetShopItem(self, slotIndex):
		itemVnum = shop.GetItemID(slotIndex)
		if 0 == itemVnum:
			return

		price = shop.GetItemPrice(slotIndex)
		self.ClearToolTip()
		self.isShopItem = True

		metinSlot = []
		for i in range(player.METIN_SOCKET_MAX_NUM):
			metinSlot.append(shop.GetItemMetinSocket(slotIndex, i))
		attrSlot = []
		for i in range(player.ATTRIBUTE_SLOT_MAX_NUM):
			attrSlot.append(shop.GetItemAttribute(slotIndex, i))

		self.AddItemData(itemVnum, metinSlot, attrSlot)
		self.AppendPrice(price)

		self.AppendSpace(5)
		self.AppendTextLine(self.FormatMultiplePurchaseText(), self.NORMAL_COLOR)

	def AppendGreenTextLine(self, text, color = POSITIVE_COLOR, centerAlign = True):
		textLine = ui.TextLine()
		textLine.SetParent(self)
		textLine.SetFontName(self.defFontName)
		textLine.SetPackedFontColor(color)
		textLine.SetText(text)
		textLine.SetOutline()
		textLine.SetFeather(False)
		textLine.Show()

		if centerAlign:
			textLine.SetPosition(self.toolTipWidth/2, self.toolTipHeight)
			textLine.SetHorizontalAlignCenter()

		else:
			textLine.SetPosition(10, self.toolTipHeight)

		self.childrenList.append(textLine)

		self.toolTipHeight += self.TEXT_LINE_HEIGHT
		self.ResizeToolTip()

		return textLine

	def SetShopItemBySecondaryCoin(self, slotIndex):
		itemVnum = shop.GetItemID(slotIndex)
		if 0 == itemVnum:
			return

		price = shop.GetItemPrice(slotIndex)
		self.ClearToolTip()
		self.isShopItem = True

		metinSlot = []
		for i in range(player.METIN_SOCKET_MAX_NUM):
			metinSlot.append(shop.GetItemMetinSocket(slotIndex, i))
		attrSlot = []
		for i in range(player.ATTRIBUTE_SLOT_MAX_NUM):
			attrSlot.append(shop.GetItemAttribute(slotIndex, i))

		self.AddItemData(itemVnum, metinSlot, attrSlot)
		self.AppendPriceBySecondaryCoin(price)

	def SetExchangeOwnerItem(self, slotIndex):
		itemVnum = exchange.GetItemVnumFromSelf(slotIndex)
		if 0 == itemVnum:
			return

		self.ClearToolTip()

		metinSlot = []
		for i in range(player.METIN_SOCKET_MAX_NUM):
			metinSlot.append(exchange.GetItemMetinSocketFromSelf(slotIndex, i))
		attrSlot = []
		for i in range(player.ATTRIBUTE_SLOT_MAX_NUM):
			attrSlot.append(exchange.GetItemAttributeFromSelf(slotIndex, i))
		self.AddItemData(itemVnum, metinSlot, attrSlot)

	def SetExchangeTargetItem(self, slotIndex):
		itemVnum = exchange.GetItemVnumFromTarget(slotIndex)
		if 0 == itemVnum:
			return

		self.ClearToolTip()

		metinSlot = []
		for i in range(player.METIN_SOCKET_MAX_NUM):
			metinSlot.append(exchange.GetItemMetinSocketFromTarget(slotIndex, i))
		attrSlot = []
		for i in range(player.ATTRIBUTE_SLOT_MAX_NUM):
			attrSlot.append(exchange.GetItemAttributeFromTarget(slotIndex, i))
		self.AddItemData(itemVnum, metinSlot, attrSlot)

	def SetPrivateShopBuilderItem(self, invenType, invenPos, privateShopSlotIndex):
		itemVnum = player.GetItemIndex(invenType, invenPos)
		if 0 == itemVnum:
			return

		item.SelectItem(itemVnum)
		self.ClearToolTip()
		if app.ENABLE_PREMIUM_PRIVATE_SHOP_OFFICIAL:
			if app.ENABLE_CHEQUE_SYSTEM:
				goldPrice = privateShop.GetStockItemPrice(invenType, invenPos)
				chequePrice = privateShop.GetStockChequeItemPrice(invenType, invenPos)

				self.AppendSellingPrice(goldPrice, chequePrice, True)
			else:
				self.AppendSellingPrice(privateShop.GetStockItemPrice(invenType, invenPos))
		else:
			# isPrivateShopBuilder=True: w edytorze wlasnego sklepu cena MUSI byc widoczna
			# takze dla przedmiotow z ITEM_ANTIFLAG_SELL (nie da sie ich sprzedac NPC, ale
			# wystawic w sklepie owszem). Bez tego AppendSellingPrice pokazuje "nie mozna
			# sprzedac" zamiast ceny. ENABLE_PREMIUM_PRIVATE_SHOP_OFFICIAL jest u nas
			# wylaczone, wiec to jest ta aktywna galaz. Patrz metin2.dev/topic/18677.
			self.AppendSellingPrice(shop.GetPrivateShopItemPrice(invenType, invenPos), 0, True)

		args = {}

		apply_random_list = []
		metinSlot = []
		for i in range(player.METIN_SOCKET_MAX_NUM):
			metinSlot.append(player.GetItemMetinSocket(invenPos, i))
		attrSlot = []
		for i in range(player.ATTRIBUTE_SLOT_MAX_NUM):
			attrSlot.append(player.GetItemAttribute(invenPos, i))

		self.AddItemData(itemVnum, metinSlot, attrSlot, **args)

	def SetSafeBoxItem(self, slotIndex):
		itemVnum = safebox.GetItemID(slotIndex)
		if 0 == itemVnum:
			return

		self.ClearToolTip()
		metinSlot = []
		for i in range(player.METIN_SOCKET_MAX_NUM):
			metinSlot.append(safebox.GetItemMetinSocket(slotIndex, i))
		attrSlot = []
		for i in range(player.ATTRIBUTE_SLOT_MAX_NUM):
			attrSlot.append(safebox.GetItemAttribute(slotIndex, i))

		self.AddItemData(itemVnum, metinSlot, attrSlot, safebox.GetItemFlags(slotIndex))

		self.AppendSpace(5)
		self.AppendTextLine(localeInfo.TOOLTIP_SAFEBOX_WITHDRAW, self.POSITIVE_COLOR)

	def SetMallItem(self, slotIndex):
		itemVnum = safebox.GetMallItemID(slotIndex)
		if 0 == itemVnum:
			return

		self.ClearToolTip()
		metinSlot = []
		for i in range(player.METIN_SOCKET_MAX_NUM):
			metinSlot.append(safebox.GetMallItemMetinSocket(slotIndex, i))
		attrSlot = []
		for i in range(player.ATTRIBUTE_SLOT_MAX_NUM):
			attrSlot.append(safebox.GetMallItemAttribute(slotIndex, i))

		self.AddItemData(itemVnum, metinSlot, attrSlot)

	def SetItemToolTip(self, itemVnum, showIcon=0):
		self.ClearToolTip()
		
		metinSlot = []
		for i in range(player.METIN_SOCKET_MAX_NUM):
			metinSlot.append(0)
		attrSlot = []
		for i in range(player.ATTRIBUTE_SLOT_MAX_NUM):
			attrSlot.append((0, 0))

		self.AddItemData(itemVnum, metinSlot, attrSlot, showIcon=showIcon)

	if app.ENABLE_ASLAN_BUFF_NPC_SYSTEM:
		def GetBuffSkillLevelGrade(self, skillLevel):
			skillLevel = int(skillLevel)
			if skillLevel >= 0 and skillLevel < 20:
				return ("%d" % int(skillLevel))
			if skillLevel >= 20 and skillLevel < 30:
				return ("M%d" % int(skillLevel-19))
			if skillLevel >= 30 and skillLevel < 40: 
				return ("G%d" % int(skillLevel-29))
			if skillLevel == 40: 
				return "P"

		def AppendEXPGauge(self, exp_perc):
			IMG_PATH = "d:/ymir work/ui/aslan/buffnpc/"
			gauge_empty_list = []
			gauge_full_list = []
			x_pos = [35, 17, 1, 19]
			for i in range(4):
				gauge_empty = ui.ExpandedImageBox()
				gauge_empty.SetParent(self)
				gauge_empty.LoadImage(IMG_PATH + "exp_empty.sub")
				if i <= 1:
					gauge_empty.SetPosition(self.toolTipWidth/2 - x_pos[i], self.toolTipHeight)
				else:
					gauge_empty.SetPosition(self.toolTipWidth/2 + x_pos[i], self.toolTipHeight)
				gauge_empty.Show()

				gauge_full = ui.ExpandedImageBox()
				gauge_full.SetParent(self)
				gauge_full.LoadImage(IMG_PATH + "exp_full.sub")
				if i <= 1:
					gauge_full.SetPosition(self.toolTipWidth/2 - x_pos[i], self.toolTipHeight)
				else:
					gauge_full.SetPosition(self.toolTipWidth/2 + x_pos[i], self.toolTipHeight)
					
				gauge_empty_list.append(gauge_empty)
				gauge_full_list.append(gauge_full)
		
			exp_perc = float(exp_perc / 100.0)
			exp_bubble_perc = 25.0

			for i in range(4):
				if exp_perc > exp_bubble_perc:
					exp_bubble_perc += 25.0
					gauge_full_list[i].SetRenderingRect(0.0, 0.0, 0.0, 0.0)
					gauge_full_list[i].Show()
				else:
					exp_perc = float((exp_perc - exp_bubble_perc) * 4 / 100) 
					gauge_full_list[i].SetRenderingRect(0.0, exp_perc, 0.0, 0.0)
					gauge_full_list[i].Show()
					break

			self.childrenList.append(gauge_empty_list)
			self.childrenList.append(gauge_full_list)
			
			self.toolTipHeight += 18
			self.ResizeToolTip()

	def __AppendAttackSpeedInfo(self, item):
		atkSpd = item.GetValue(0)

		if atkSpd < 80:
			stSpd = localeInfo.TOOLTIP_ITEM_VERY_FAST
		elif atkSpd <= 95:
			stSpd = localeInfo.TOOLTIP_ITEM_FAST
		elif atkSpd <= 105:
			stSpd = localeInfo.TOOLTIP_ITEM_NORMAL
		elif atkSpd <= 120:
			stSpd = localeInfo.TOOLTIP_ITEM_SLOW
		else:
			stSpd = localeInfo.TOOLTIP_ITEM_VERY_SLOW

		self.AppendTextLine(localeInfo.TOOLTIP_ITEM_ATT_SPEED % stSpd, self.NORMAL_COLOR)

	def __AppendAttackGradeInfo(self):
		atkGrade = item.GetValue(1)
		self.AppendTextLine(localeInfo.TOOLTIP_ITEM_ATT_GRADE % atkGrade, self.GetChangeTextLineColor(atkGrade))

	if app.ENABLE_ACCE_COSTUME_SYSTEM:
		def CalcAcceValue(self, value, abs):
			if not value:
				return 0

			valueCalc 	= round(value * abs) / 100
			valueCalc 	-= 0.5
			valueCalc 	= int(valueCalc) +1 if valueCalc > 0 else int(valueCalc)
			value 		= 1 if (valueCalc <= 0 and value > 0) else valueCalc
			return value

	def __AppendAttackPowerInfo(self, itemAbsChance = 0):
		minPower = item.GetValue(3)
		maxPower = item.GetValue(4)
		addPower = item.GetValue(5)
		if app.ENABLE_ACCE_COSTUME_SYSTEM:
			if itemAbsChance != 0:
				minPower = self.CalcAcceValue(minPower, itemAbsChance)
				maxPower = self.CalcAcceValue(maxPower, itemAbsChance)
				addPower = self.CalcAcceValue(addPower, itemAbsChance)

		if maxPower > minPower:
			self.AppendTextLine(localeInfo.TOOLTIP_ITEM_ATT_POWER % (minPower+addPower, maxPower+addPower), self.POSITIVE_COLOR)
		else:
			self.AppendTextLine(localeInfo.TOOLTIP_ITEM_ATT_POWER_ONE_ARG % (minPower+addPower), self.POSITIVE_COLOR)

	def __AppendMagicAttackInfo(self, itemAbsChance = 0):
		minMagicAttackPower = item.GetValue(1)
		maxMagicAttackPower = item.GetValue(2)
		addPower 			= item.GetValue(5)
		if app.ENABLE_ACCE_COSTUME_SYSTEM:
			if itemAbsChance != 0:
				minMagicAttackPower = self.CalcAcceValue(minMagicAttackPower, itemAbsChance)
				maxMagicAttackPower = self.CalcAcceValue(maxMagicAttackPower, itemAbsChance)
				addPower 			= self.CalcAcceValue(addPower, itemAbsChance)

		if minMagicAttackPower > 0 or maxMagicAttackPower > 0:
			if maxMagicAttackPower > minMagicAttackPower:
				self.AppendTextLine(localeInfo.TOOLTIP_ITEM_MAGIC_ATT_POWER % (minMagicAttackPower+addPower, maxMagicAttackPower+addPower), self.POSITIVE_COLOR)
			else:
				self.AppendTextLine(localeInfo.TOOLTIP_ITEM_MAGIC_ATT_POWER_ONE_ARG % (minMagicAttackPower+addPower), self.POSITIVE_COLOR)

	def __AppendMagicDefenceInfo(self, itemAbsChance = 0):
		magicDefencePower = item.GetValue(0)
		if app.ENABLE_ACCE_COSTUME_SYSTEM:
			if itemAbsChance != 0:
				magicDefencePower = self.CalcAcceValue(magicDefencePower, itemAbsChance)

		if magicDefencePower > 0:
			self.AppendTextLine(localeInfo.TOOLTIP_ITEM_MAGIC_DEF_POWER % magicDefencePower, self.GetChangeTextLineColor(magicDefencePower))

	def __AppendAttributeInformation(self, attrSlot, itemAbsChance = 0):
		if 0 != attrSlot:
			for i in range(player.ATTRIBUTE_SLOT_MAX_NUM):
				type = attrSlot[i][0]
				value = attrSlot[i][1]

				if 0 == value:
					continue

				affectString = self.__GetAffectString(type, value)
				if app.ENABLE_ACCE_COSTUME_SYSTEM:
					if item.GetItemType() == item.COSTUME:
						if item.GetItemSubType() == item.COSTUME_TYPE_ACCE:
							if itemAbsChance != 0:
								value = self.CalcAcceValue(value, itemAbsChance)
								affectString = self.__GetAffectString(type, value)

				if app.ENABLE_AURA_SYSTEM:
					if item.GetItemType() == item.COSTUME and item.GetItemSubType() == item.COSTUME_TYPE_AURA and itemAbsChance:
						value = self.CalcSashValue(value, itemAbsChance)
						affectString = self.__GetAffectString(type, value)

				if affectString:
					affectColor = self.__GetAttributeColor(i, value, type)
					if item.GetItemType() == item.ARMOR and item.GetItemSubType() == item.ARMOR_GLOVE:
						if i > 2:
							self.AppendTextLine(affectString, affectColor)
						else:
							self.AppendTextLine(affectString, self.GetChangeTextLineColor(value))
					else:
						self.AppendTextLine(affectString, affectColor)

	def __GetAttributeColor(self, index, value, type=0):
		if item.GetItemType() == item.DS:
			return self.SPECIAL_POSITIVE_COLOR
		if value > 0:
			# Check for 6th and 7th bonus FIRST, before max value check
			if index >= player.ATTRIBUTE_SLOT_RARE_START and index <= player.ATTRIBUTE_SLOT_RARE_END:
				return self.SPECIAL_POSITIVE_COLOR2  # or whatever color you want
				
			# .get() zamiast [] - "type" to numer bonusu z danych przedmiotu i nie musi byc
			# kluczem w tablicy; KeyError zabijal caly tooltip zamiast jednej kolorystyki.
			if item.GetItemType() == item.ARMOR and item.GetItemSubType() == item.ARMOR_GLOVE:
				if index < 3:
					return self.POSITIVE_COLOR
				if value == self.MAX_AFFECT_VALUE_GLOVE.get(type):
					return self.SPECIAL_TITLE_COLOR2
			elif item.GetItemType() == item.BELT:
				if value == self.MAX_AFFECT_VALUE_BELT.get(type):
					return self.SPECIAL_TITLE_COLOR2
			else:
				if value == self.MAX_AFFECT_VALUE.get(type):
					return self.SPECIAL_TITLE_COLOR2
	
			if index == player.ATTRIBUTE_SLOT_NORM_END:
				return self.SPECIAL_POSITIVE_COLOR5
			else:
				return self.SPECIAL_POSITIVE_COLOR
		elif value == 0:
			return self.NORMAL_COLOR
		else:
			return self.NEGATIVE_COLOR

	def GetAttributeColor(self, index, value, type=0):
		# Publiczny dostep do kolorystyki bonusow (max bonus = zloto).
		# Uzywane poza tooltipem, m.in. przez uibonuschanger, zeby lista bonusow
		# w oknie zmiennika miala te sama kolorystyke co tooltip przedmiotu.
		# UWAGA: wynik zalezy od aktualnie wybranego itemu (item.SelectItem),
		# bo rozne typy maja rozne tablice MAX_AFFECT_VALUE.
		return self.__GetAttributeColor(index, value, type)

	def __IsPolymorphItem(self, itemVnum):
		if itemVnum >= 70103 and itemVnum <= 70107:
			return 1
		return 0

	def __SetPolymorphItemTitle(self, monsterVnum):
		itemName =nonplayer.GetMonsterName(monsterVnum)
		itemName+=" "
		itemName+=item.GetItemName()
		self.SetTitle(itemName)

	def __SetNormalItemTitle(self):
		self.SetTitle(item.GetItemName())

	def __SetSpecialItemTitle(self):
		self.AppendTextLine(item.GetItemName(), self.SPECIAL_TITLE_COLOR)

	def __SetItemTitle(self, itemVnum, metinSlot, attrSlot):
		if self.__IsPolymorphItem(itemVnum):
			self.__SetPolymorphItemTitle(metinSlot[0])
		else:
			if self.__IsAttr(attrSlot):
				self.__SetSpecialItemTitle()
				return

			self.__SetNormalItemTitle()

	def __IsAttr(self, attrSlot):
		if not attrSlot:
			return False

		for i in range(player.ATTRIBUTE_SLOT_MAX_NUM):
			type = attrSlot[i][0]
			if 0 != type:
				return True

		return False

	def AddRefineItemData(self, itemVnum, metinSlot, attrSlot = 0):
		for i in range(player.METIN_SOCKET_MAX_NUM):
			metinSlotData=metinSlot[i]
			if self.GetMetinItemIndex(metinSlotData) == constInfo.ERROR_METIN_STONE:
				metinSlot[i]=player.METIN_SOCKET_TYPE_SILVER

		if app.ENABLE_GLOVE_SYSTEM:
			if itemVnum >= 23000 and itemVnum <= 23009:
				self.AddGloveItemData(itemVnum, metinSlot, attrSlot)
			else:
				self.AddItemData(itemVnum, metinSlot, attrSlot)
		else:
			self.AddItemData(itemVnum, metinSlot, attrSlot)


	if app.ENABLE_OFFLINE_SHOP:
		def AddRightClickForSale(self):
			self.AppendSpace(3)
			self.AppendTextLine(localeInfo.OFFLINESHOP_TOOLTIP_RIGHT_CLICK_FOR_SALE, centerAlign = False)
			self.AppendSpace(3)
			self.AppendTextLine(localeInfo.OFFLINESHOP_TOOLTIP_RIGHT_CLICK_FOR_SALE2, centerAlign = False)

	def AddItemData_Offline(self, itemVnum, itemDesc, itemSummary, metinSlot, attrSlot):
		self.__AdjustMaxWidth(attrSlot, itemDesc)
		self.__SetItemTitle(itemVnum, metinSlot, attrSlot)

		if self.__IsHair(itemVnum):
			self.__AppendHairIcon(itemVnum)

		if app.ENABLE_PREMIUM_PRIVATE_SHOP_OFFICIAL:
			if self.isPrivateSearchItem or self.isPrivateShopSaleItem:
				if not self.__IsHair(itemVnum):
					self.__AppendPrivateItemIcon(itemVnum)

		self.AppendDescription(itemDesc, 26)
		self.AppendDescription(itemSummary, 26, self.CONDITION_COLOR)

	def __ItemGetRace(self):
		race = 0

		if item.IsAntiFlag(item.ITEM_ANTIFLAG_ASSASSIN) and item.IsAntiFlag(item.ITEM_ANTIFLAG_SURA) and item.IsAntiFlag(item.ITEM_ANTIFLAG_SHAMAN):
			race = 9
		elif item.IsAntiFlag(item.ITEM_ANTIFLAG_WARRIOR) and item.IsAntiFlag(item.ITEM_ANTIFLAG_SURA) and item.IsAntiFlag(item.ITEM_ANTIFLAG_SHAMAN):
			race = 1
		elif item.IsAntiFlag(item.ITEM_ANTIFLAG_WARRIOR) and item.IsAntiFlag(item.ITEM_ANTIFLAG_ASSASSIN) and item.IsAntiFlag(item.ITEM_ANTIFLAG_SHAMAN):
			race = 2
		elif item.IsAntiFlag(item.ITEM_ANTIFLAG_WARRIOR) and item.IsAntiFlag(item.ITEM_ANTIFLAG_ASSASSIN) and item.IsAntiFlag(item.ITEM_ANTIFLAG_SURA):
			race = 3

		sex = chr.RaceToSex(player.GetOriginalRace())
		MALE = 1
		FEMALE = 0

		if item.IsAntiFlag(item.ITEM_ANTIFLAG_MALE) and sex == MALE:
			race = player.GetOriginalRace() + 4

		if item.IsAntiFlag(item.ITEM_ANTIFLAG_FEMALE) and sex == FEMALE:
			race = player.GetOriginalRace()

		if race == 0:
			race = player.GetOriginalRace()

		if race == 9:
			race = 0

		return race

	def __ItemGetRaceShaman(self):
		if item.IsAntiFlag(item.ITEM_ANTIFLAG_SHAMAN):
			return 3

		sex = chr.RaceToSex(player.GetOriginalRace())
		MALE = 1
		FEMALE = 0

		if item.IsAntiFlag(item.ITEM_ANTIFLAG_MALE) and sex == MALE:
			race = player.GetOriginalRace() + 4

		if item.IsAntiFlag(item.ITEM_ANTIFLAG_FEMALE) and sex == FEMALE:
			race = player.GetOriginalRace()
    
		return 3

	def AddItemData(self, itemVnum, metinSlot, attrSlot=0, flags=0, unbindTime=0,
					window_type=player.INVENTORY, slotIndex=-1, showIcon=0):
		"""Main entry point for building item tooltip content."""
		self.itemVnum = itemVnum
		self.metinSlot = metinSlot
		self.modelPreviewRequested = False
		item.SelectItem(itemVnum)
		
		itemType = item.GetItemType()
		itemSubType = item.GetItemSubType()
		
		# Handle special items with early returns
		if self.__TryHandleSpecialItem(itemVnum, metinSlot, window_type, slotIndex):
			if not self.modelPreviewRequested:
				self.__ModelPreviewClose()
			return
		
		# Setup common header
		self.__SetupTooltipHeader(itemVnum, metinSlot, attrSlot, showIcon)
		
		# Route to type-specific handler
		self.__RouteItemType(
			itemVnum, itemType, itemSubType, metinSlot, attrSlot
		)
		
		# Handle costume set items (special models)
		self.__TryHandleCostumeSet(itemVnum)
		
		# Footer elements
		self.__AppendItemLimitsAndTips(window_type, slotIndex)

		if not self.modelPreviewRequested:
			self.__ModelPreviewClose()
	
	def __TryHandleSpecialItem(self, itemVnum, metinSlot, window_type, slotIndex):
		"""Handle items that need special early-return processing."""
		handlers = {
			50026: self.__HandleGoldBar,
			50300: self.__HandleSkillBook,
			70037: self.__HandleSkillForgetBook,
			70055: self.__HandleSkillForgetBook,
		}
		
		handler = handlers.get(itemVnum)
		if handler:
			handler(itemVnum, metinSlot, window_type, slotIndex)
			return True
		return False
	
	def __HandleGoldBar(self, itemVnum, metinSlot, window_type, slotIndex):
		"""Display gold bar with amount."""
		name = item.GetItemName()
		if metinSlot and metinSlot[0] > 0:
			name += " " + localeInfo.NumberToMoneyString(metinSlot[0])
		self.SetTitle(name)
		self.__AppendSealInformation(window_type, slotIndex)
		self.AdditionalTips(window_type, itemVnum, metinSlot, slotIndex)
		self.ShowToolTip()
	
	def __HandleSkillBook(self, itemVnum, metinSlot, window_type, slotIndex):
		"""Display skill book tooltip."""
		if metinSlot:
			self.__SetSkillBookToolTip(metinSlot[0], localeInfo.TOOLTIP_SKILLBOOK_NAME, 1)
		self.__AppendSealInformation(window_type, slotIndex)
		self.AdditionalTips(window_type, itemVnum, metinSlot, slotIndex)
		self.ShowToolTip()
	
	def __HandleSkillForgetBook(self, itemVnum, metinSlot, window_type, slotIndex):
		"""Display skill forget book tooltip."""
		if metinSlot:
			self.__SetSkillBookToolTip(metinSlot[0], localeInfo.TOOLTIP_SKILL_FORGET_BOOK_NAME, 0)
		self.AppendDescription(item.GetItemDescription(), 26)
		self.AppendDescription(item.GetItemSummary(), 26, self.CONDITION_COLOR)
		self.__AppendSealInformation(window_type, slotIndex)
		self.AdditionalTips(window_type, itemVnum, metinSlot, slotIndex)
		self.ShowToolTip()
	
	def __SetupTooltipHeader(self, itemVnum, metinSlot, attrSlot, showIcon):
		"""Setup title, description and icon."""
		if not item.GetItemDescription():
			self.__CalculateToolTipWidth()
		
		self.__AdjustMaxWidth(attrSlot, item.GetItemDescription())
		self.__SetItemTitle(itemVnum, metinSlot, attrSlot)
		
		if showIcon:
			self.AppendSpace(3)
			self.AppendItemIcon(itemVnum)
			self.AppendSpace(3)
		
		self.AppendDescription(item.GetItemDescription(), 26)
		self.AppendDescription(item.GetItemSummary(), 26, self.CONDITION_COLOR)
	
	def __RouteItemType(self, itemVnum, itemType, itemSubType, metinSlot, attrSlot):
		"""Route to appropriate item type handler."""
		handlers = {
			item.WEAPON: lambda: self.__HandleWeapon(itemSubType, metinSlot, attrSlot),
			item.ARMOR: lambda: self.__HandleArmor(itemVnum, itemSubType, metinSlot, attrSlot),
			item.COSTUME: lambda: self.__HandleCostume(itemVnum, itemSubType, metinSlot, attrSlot),
			item.TITLE: self.__HandleTitle,
			item.MOUNT: lambda: self.__HandleMount(metinSlot, attrSlot),
			item.METIN: self.__HandleMetin,
			item.FISH: lambda: self.__HandleFish(metinSlot),
			item.ROD: lambda: self.__HandleRod(metinSlot, attrSlot),
			item.PICK: lambda: self.__HandlePick(metinSlot),
			item.LOTTERY: lambda: self.__HandleLottery(metinSlot),
			item.RING: lambda: self.__HandleRing(metinSlot, attrSlot),
			item.BELT: lambda: self.__HandleBelt(itemVnum, metinSlot, attrSlot),
			item.TOGGLE: lambda: self.__HandleToggle(itemSubType, metinSlot, attrSlot),
			item.UNIQUE: lambda: self.__HandleUnique(metinSlot, attrSlot),
			item.USE: lambda: self.__HandleUse(itemVnum, itemSubType, metinSlot),
			item.QUEST: lambda: self.__HandleQuest(metinSlot),
			item.DS: lambda: self.__HandleDragonSoul(itemVnum, metinSlot, attrSlot),
			item.ARTEFAKT: lambda: self.__HandleArtefact(itemVnum, metinSlot, attrSlot),
			item.RUNE: lambda: self.__HandleRune(metinSlot, attrSlot),
			item.RUNE_RED: lambda: self.__HandleRune(metinSlot, attrSlot),
			item.RUNE_BLUE: lambda: self.__HandleRune(metinSlot, attrSlot),
			item.RUNE_BLACK: lambda: self.__HandleRune(metinSlot, attrSlot),
			item.RUNE_YELLOW: lambda: self.__HandleRune(metinSlot, attrSlot),
			item.RUNE_GREEN: lambda: self.__HandleRune(metinSlot, attrSlot),
		}
		
		if app.ENABLE_NEW_PET_SYSTEM:
			handlers.update({
				item.NEW_PET: lambda: self.__HandleNewPet(itemVnum, metinSlot, attrSlot),
				item.NEW_PET_EQ: lambda: self.__HandleNewPet(itemVnum, metinSlot, attrSlot),
			})
		
		if app.ENABLE_PET_SYSTEM_EX:
			handlers[item.PET] = lambda: self.__HandlePet(metinSlot, attrSlot)
		
		if app.ENABLE_EXTENDED_BLEND:
			handlers[item.BLEND] = lambda: self.__HandleBlend(metinSlot)
		
		handler = handlers.get(itemType)
		if handler:
			handler()
		elif 91201 <= itemVnum <= 91210:
			self.__HandleAttrScroll(metinSlot)
		elif 80050 <= itemVnum <= 80055 or itemVnum in (203027, 203028):
			self.__HandleFruitOfLife(itemVnum)
		elif itemVnum in (90041, 90051, 90071, 90073, 90074, 90075, 99901, 99902, 99903):
			self.__HandleSpecialCostume(itemVnum)
	
	def __HandleWeapon(self, itemSubType, metinSlot, attrSlot):
		"""Display weapon stats."""
		self.__AppendLimitInformation()
		self.AppendSpace(5)
		
		if itemSubType == item.WEAPON_FAN:
			self.__AppendMagicAttackInfo()
			self.__AppendAttackPowerInfo()
		else:
			self.__AppendAttackPowerInfo()
			self.__AppendMagicAttackInfo()
		
		self.__AppendAffectInformation()
		self.__AppendAttributeInformation(attrSlot)
		self.AppendWearableInformation()
		
		if app.ENABLE_QUIVER_SYSTEM and itemSubType == item.WEAPON_QUIVER:
			self.__AppendQuiverTime(metinSlot)
		else:
			self.__AppendMetinSlotInfo(metinSlot)
	
	def __HandleArmor(self, itemVnum, itemSubType, metinSlot, attrSlot):
		"""Display armor stats."""
		self.__AppendLimitInformation()
		
		defGrade = item.GetValue(1)
		defBonus = item.GetValue(5) * 2
		if defGrade > 0:
			self.AppendSpace(5)
			self.AppendTextLine(
				localeInfo.TOOLTIP_ITEM_DEF_GRADE % (defGrade + defBonus),
				self.GetChangeTextLineColor(defGrade)
			)
		
		self.__AppendMagicDefenceInfo()
		self.__AppendAffectInformation()
		self.__AppendAttributeInformation(attrSlot)
		
		if itemSubType == item.ARMOR_GLOVE:
			self.__AppendEnchantStatus(metinSlot)
		
		self.AppendWearableInformation()
		
		if itemSubType in (item.ARMOR_WRIST, item.ARMOR_NECK, item.ARMOR_EAR):
			self.__AppendAccessoryMetinSlotInfo(
				metinSlot, constInfo.GET_ACCESSORY_MATERIAL_VNUM(itemVnum, itemSubType)
			)
		else:
			self.__AppendMetinSlotInfo(metinSlot)
	
	def __HandleCostume(self, itemVnum, itemSubType, metinSlot, attrSlot):
		"""Display costume item info."""
		# Mount costumes
		if itemSubType == item.COSTUME_TYPE_MOUNT:
			self.__AppendLimitInformation()
			if item.GetValue(1) != 0:
				self.__ModelPreviewOpen(itemVnum, item.GetValue(1), "monster")
			return
		
		# Regular costumes
		self.__AppendLimitInformation()
		self.__AppendAffectInformation()
		
		bonusLeftTime = metinSlot[1] - app.GetGlobalTimeStamp() if metinSlot else 0
		if bonusLeftTime > 0:
			self.__AppendCostumeBonusAffects(itemVnum, metinSlot, bonusLeftTime)
		
		isWeapon = app.ENABLE_WEAPON_COSTUME_SYSTEM and itemSubType == item.COSTUME_TYPE_WEAPON
		isHair = itemSubType == item.COSTUME_TYPE_HAIR
		isBody = itemSubType == item.COSTUME_TYPE_BODY
		isStole = itemSubType == item.COSTUME_TYPE_STOLE
		isAcce = app.ENABLE_ACCE_COSTUME_SYSTEM and itemSubType == item.COSTUME_TYPE_ACCE
		
		if isAcce:
			self.__HandleAcceCostume(itemVnum, metinSlot, attrSlot)
		else:
			self.__AppendAttributeInformation(attrSlot)
		
		self.AppendWearableInformation()
		self.AppendLastTimeInformation(metinSlot)
		
		# Model previews
		if isWeapon:
			self.__ModelPreviewOpen(itemVnum, self.__ItemGetRace(), "weapon")
		if isHair:
			self.__ModelPreviewOpen(item.GetValue(3), self.__ItemGetRace(), "hair")
		if isStole:
			self.__ModelPreviewOpen(itemVnum, self.__ItemGetRace(), "acce")
		if isBody:
			self.__ModelPreviewOpen(itemVnum, self.__ItemGetRace(), "body")
	
	def __HandleAcceCostume(self, itemVnum, metinSlot, attrSlot):
		"""Handle ACCE (sash) costume with absorption."""
		absChance = int(metinSlot[acce.ABSORPTION_SOCKET]) if metinSlot else 0
		reinforcement = int(metinSlot[2]) if metinSlot else 0
		
		if reinforcement > 0:
			self.__AppendEnchantIndicator()
		
		self.AppendSpace(5)
		self.AppendTextLine(localeInfo.ACCE_ABSORB_CHANCE % absChance, self.CONDITION_COLOR)
		self.AppendSpace(5)
		
		self.__ModelPreviewOpen(itemVnum, self.__ItemGetRace(), "acce")
		
		itemAbsorbedVnum = int(metinSlot[acce.ABSORBED_SOCKET]) if metinSlot else 0
		if itemAbsorbedVnum:
			self.__AppendAbsorbedItemInfo(itemAbsorbedVnum, metinSlot, attrSlot)
		else:
			self.__AppendAttributeInformation(attrSlot)
	
	def __AppendAbsorbedItemInfo(self, absorbedVnum, metinSlot, attrSlot):
		"""Display absorbed item stats in ACCE."""
		self.AppendHorizontalLine()
		item.SelectItem(absorbedVnum)
		
		absSocket = acce.ABSORPTION_SOCKET
		
		if item.GetItemType() == item.WEAPON:
			if item.GetItemSubType() == item.WEAPON_FAN:
				self.__AppendMagicAttackInfo(metinSlot[absSocket])
				item.SelectItem(absorbedVnum)
				self.__AppendAttackPowerInfo(metinSlot[absSocket])
			else:
				self.__AppendAttackPowerInfo(metinSlot[absSocket])
				item.SelectItem(absorbedVnum)
				self.__AppendMagicAttackInfo(metinSlot[absSocket])
		elif item.GetItemType() == item.ARMOR:
			defGrade = item.GetValue(1)
			defBonus = item.GetValue(5) * 2
			defGrade = self.CalcAcceValue(defGrade, metinSlot[absSocket])
			defBonus = self.CalcAcceValue(defBonus, metinSlot[absSocket])
			
			if defGrade > 0:
				self.AppendSpace(5)
				self.AppendTextLine(
					localeInfo.TOOLTIP_ITEM_DEF_GRADE % (defGrade + defBonus),
					self.GetChangeTextLineColor(defGrade)
				)
			item.SelectItem(absorbedVnum)
			self.__AppendMagicDefenceInfo(metinSlot[absSocket])
		
		item.SelectItem(absorbedVnum)
		for i in range(item.ITEM_APPLY_MAX_NUM):
			affectType, affectValue = item.GetAffect(i)
			affectValue = self.CalcAcceValue(affectValue, metinSlot[absSocket])
			affectString = self.__GetAffectString(affectType, affectValue)
			
			valid = affectString and affectValue != 0
			if app.USE_ACCE_ABSORB_WITH_NO_NEGATIVE_BONUS:
				valid = affectString and affectValue > 0
			
			if valid:
				self.AppendTextLine(affectString, self.GetChangeTextLineColor(affectValue))
			item.SelectItem(absorbedVnum)
		
		item.SelectItem(self.itemVnum)
		self.__AppendAttributeInformation(attrSlot, metinSlot[absSocket])
		
		self.AppendSpace(5)
		self.AppendHorizontalLine()
		self.AppendSpace(5)
		self.AppendTextLine(localeInfo.SASH_ABSORBED_ITEM, self.CONDITION_COLOR)
		item.SelectItem(absorbedVnum)
		self.AppendTextLine(item.GetItemName(), self.CONDITION_COLOR)
	
	def __HandleTitle(self):
		"""Display title item."""
		self.AppendSpace(5)
	
	def __HandleMount(self, metinSlot, attrSlot):
		"""Display mount stats."""
		self.AppendSpace(4)
		self.__AppendAffectInformation()
		self.AppendSpace(1)
		self.__AppendAttributeInformation(attrSlot)
		self.AppendSpace(2)
		self.__AppendLimitInformation()
	
	def __HandleNewPet(self, itemVnum, metinSlot, attrSlot):
		"""Display new pet system item."""
		petVnum = item.GetValue(0)
		if petVnum != 0 and itemVnum not in (80109, 80119, 80129):
			self.__ModelPreviewOpen(itemVnum, petVnum, "monster")
		
		self.AppendSpace(5)
		self.__AppendLimitInformation()
		self.__AppendAttributeInformation(attrSlot)
		
		bonusLeftTime = metinSlot[1] - app.GetGlobalTimeStamp() if metinSlot else 0
		if bonusLeftTime > 0:
			self.__AppendPetBonusAffects(itemVnum, metinSlot, bonusLeftTime)
		
		if app.ENABLE_EXTRABONUS_SYSTEM:
			self.__AppendNewPetExtraBonus(itemVnum, metinSlot)
		else:
			self.__AppendAffectInformation()
	
	def __HandlePet(self, metinSlot, attrSlot):
		"""Display pet system item."""
		self.__AppendLimitInformation()
		self.__AppendAffectInformation()
		self.__AppendAttributeInformation(attrSlot)
		self.AppendWearableInformation()
		self.AppendLastTimeInformation(metinSlot)
	
	def __HandleMetin(self):
		"""Display metin stone info."""
		self.AppendMetinInformation()
		self.AppendMetinWearInformation()
	
	def __HandleFish(self, metinSlot):
		"""Display fish info."""
		if metinSlot:
			self.__AppendFishInfo(metinSlot[0], metinSlot[1])
	
	def __HandleRod(self, metinSlot, attrSlot):
		"""Display fishing rod info."""
		if not metinSlot:
			return
		
		curLevel = item.GetValue(0) // 10
		curEXP = metinSlot[0]
		maxEXP = item.GetValue(2)
		
		self.__AppendLimitInformation()
		self.__AppendRodInformation(curLevel, curEXP, maxEXP)
		self.AppendHorizontalLine()
		self.__AppendAffectInformation()
		self.__AppendRodAttributes(attrSlot)
	
	def __HandlePick(self, metinSlot):
		"""Display pickaxe info."""
		if not metinSlot:
			return
		
		curLevel = item.GetValue(0) // 10
		curEXP = metinSlot[0]
		maxEXP = item.GetValue(2)
		
		self.__AppendLimitInformation()
		self.__AppendPickInformation(curLevel, curEXP, maxEXP)
		self.AppendHorizontalLine()
		self.__AppendAffectInformation()
	
	def __HandleLottery(self, metinSlot):
		"""Display lottery ticket info."""
		if not metinSlot:
			return
		
		ticketNumber = int(metinSlot[0])
		stepNumber = int(metinSlot[1])
		
		self.AppendSpace(5)
		self.AppendTextLine(
			localeInfo.TOOLTIP_LOTTERY_STEP_NUMBER % stepNumber,
			self.NORMAL_COLOR
		)
		self.AppendTextLine(
			localeInfo.TOOLTIP_LOTTO_NUMBER % ticketNumber,
			self.NORMAL_COLOR
		)
	
	def __HandleRing(self, metinSlot, attrSlot):
		"""Display ring stats with duration."""
		time = metinSlot[0] if metinSlot else 0
		self.__AppendLimitInformation()
		self.__AppendAffectInformation()
		self.__AppendAttributeInformation(attrSlot)
		self.AppendMallItemLastTime(time)
	
	def __HandleBelt(self, itemVnum, metinSlot, attrSlot):
		"""Display belt stats."""
		self.__AppendLimitInformation()
		self.__AppendAffectInformation()
		self.__AppendAttributeInformation(attrSlot)
		self.__AppendAccessoryMetinSlotInfo(
			metinSlot, constInfo.GET_BELT_MATERIAL_VNUM(itemVnum)
		)
	
	def __HandleArtefact(self, itemVnum, metinSlot, attrSlot):
		"""Display artefact stats."""
		self.__AppendLimitInformation()
		self.__AppendAffectInformation()
		self.__AppendAttributeInformation(attrSlot)
		self.__AppendAccessoryMetinSlotInfo(
			metinSlot, constInfo.GET_BELT_MATERIAL_VNUM(itemVnum)
		)
	
	def __HandleRune(self, metinSlot, attrSlot):
		"""Display rune stats."""
		self.__AppendLimitInformation()
		
		if app.ENABLE_EXTRABONUS_SYSTEM:
			reinforcement = int(metinSlot[0]) if metinSlot else 0
			if reinforcement > 0:
				self.__AppendExtraAffectInformation(1)
			else:
				self.__AppendAffectInformation()
		else:
			self.__AppendAffectInformation()
		
		self.__AppendAttributeInformation(attrSlot)
		
		if app.ENABLE_EXTRABONUS_SYSTEM and reinforcement > 0:
			self.__AppendEnchantIndicator()
	
	def __HandleToggle(self, itemSubType, metinSlot, attrSlot):
		"""Display toggle item stats."""
		time = metinSlot[0] if metinSlot else 0
		isActivated = int(metinSlot[3]) if metinSlot else 0
		
		self.__AppendLimitInformation()
		self.__AppendAffectInformation()
		self.__AppendAttributeInformation(attrSlot)
		
		if isActivated:
			self.AppendTextLine(
				"(%s)" % localeInfo.TOOLTIP_TOGGLE_ACTIVE,
				self.SPECIAL_POSITIVE_COLOR
			)
		
		if itemSubType in (item.TOGGLE_AUTO_RECOVERY_HP, item.TOGGLE_AUTO_RECOVERY_SP):
			if metinSlot:
				usedAmount = float(metinSlot[1])
				totalAmount = float(metinSlot[2]) or 1.0
				rest = 100.0 - ((usedAmount / totalAmount) * 100.0)
				self.AppendTextLine(localeInfo.TOOLTIP_REMAINING % rest, self.POSITIVE_COLOR)
		
		self.AppendMallItemLastTime(time)
	
	def __HandleUnique(self, metinSlot, attrSlot):
		"""Display unique item stats with duration."""
		time = metinSlot[0] if metinSlot else 0
		self.__AppendLimitInformation()
		self.__AppendAffectInformation()
		self.__AppendAttributeInformation(attrSlot)
		self.AppendMallItemLastTime(time)
	
	def __HandleUse(self, itemVnum, itemSubType, metinSlot):
		"""Display usable item info."""
		self.__AppendLimitInformation()
		
		if itemSubType in (item.USE_POTION, item.USE_POTION_NODELAY):
			self.__AppendPotionInformation()
		elif itemSubType == item.USE_ADD_IS_BONUS:
			self.__AppendAffectInformation()
		elif itemSubType == item.USE_ABILITY_UP:
			self.__AppendAbilityPotionInformation()
		
		self.__HandleUseItemDetails(itemVnum, itemSubType, metinSlot)
	
	def __HandleQuest(self, metinSlot):
		"""Display quest item time limits."""
		for i in range(item.LIMIT_MAX_NUM):
			limitType, limitValue = item.GetLimit(i)
			if limitType == item.LIMIT_REAL_TIME:
				self.AppendMallItemLastTime(metinSlot[0] if metinSlot else 0)
	
	def __HandleDragonSoul(self, itemVnum, metinSlot, attrSlot):
		"""Display dragon soul info — tier/strength, attributes, activation state, remaining time.

		UWAGA: metinSlot przyjmujemy JAWNIE jako parametr, bo self.metinSlot jest
		nullowane w __CalculateToolTipWidth (linia 2781) zanim ten handler się wykona.
		"""
		self.AppendTextLine(self.__DragonSoulInfoString(itemVnum))
		self.__AppendAttributeInformation(attrSlot)

		# Metin socket layout dla DS items (z serwera):
		#   [0] = ITEM_SOCKET_REMAIN_SEC              — sekundy do wygaśnięcia
		#   [2] = ITEM_SOCKET_DRAGON_SOUL_ACTIVE_IDX  — 1 = aktywny, 0 = nieaktywny
		remainSec = 0
		isActive = 0
		if metinSlot:
			try:
				remainSec = int(metinSlot[0])
			except (IndexError, TypeError, ValueError):
				remainSec = 0
			try:
				isActive = int(metinSlot[2]) if len(metinSlot) > 2 else 0
			except (TypeError, ValueError):
				isActive = 0

		# Pokaż status aktywacji zawsze.
		self.AppendSpace(5)
		if isActive:
			self.AppendTextLine(localeInfo.DRAGON_SOUL_ACTIVE, self.POSITIVE_COLOR)
		else:
			self.AppendTextLine(localeInfo.DRAGON_SOUL_INACTIVE, self.DISABLE_COLOR)

		# Timer — tylko gdy DS ma limitowany czas działania.
		if remainSec > 0:
			endTime = app.GetGlobalTimeStamp() + remainSec
			self.AppendMallItemLastTime(endTime)
	
	def __HandleBlend(self, metinSlot):
		"""Display blend item info."""
		self.__AppendLimitInformation()
		self.AppendSpace(5)
		
		if metinSlot and metinSlot[0] != 0:
			affectType = item.GetValue(0)
			affectValue = metinSlot[0]
			time = metinSlot[2]
		else:
			affectType = item.GetValue(0)
			affectValue = item.GetValue(2)
			time = item.GetValue(1)
		
		affectText = self.__GetAffectString(affectType, affectValue)
		self.AutoAppendTextLine(affectText, self.POSITIVE_COLOR)
		self.AppendSpace(5)
		
		if time > 0:
			self.AutoAppendTextLine(localeInfo.DURATION, self.CONDITION_COLOR)
			self.AutoAppendTextLine(
				emoji.AppendEmoji("icon/emoji/image-example-007.png") + " " +
				localeInfo.SecondToDHM(time),
				self.NORMAL_COLOR
			)
		else:
			self.AppendSpace(5)
	
	def __HandleAttrScroll(self, metinSlot):
		"""Display attribute scroll info."""
		if not metinSlot:
			return
		
		attrType = item.GetValue(0)
		attrValue = item.GetValue(1)
		
		self.__AppendLimitInformation()
		self.AppendHorizontalLine()
		
		affectString = self.__GetAffectString(attrType, attrValue)
		if affectString:
			affectColor = self.__GetAttributeColor(0, attrValue)
			self.AppendTextLine(affectString, affectColor)
			self.AppendTextLine(
				localeInfo.TOOLTIP_BONUS_CAN_BE_USE_X_TIMES % metinSlot[0],
				affectColor
			)
	
	def __HandleFruitOfLife(self, itemVnum):
		"""Display fruit of life descriptions."""
		self.AppendSpace(5)
		self.AutoAppendTextLine(localeInfo.FRUIT_OF_LIFE_DESC_1.format(200))
		
		formats = {
			80050: (50000,),
			80051: (50000, 100000),
			80052: (100000, 200000),
			80053: (200000, 300000),
			80054: (300000, 400000),
			80055: (400000, 500000),
			203028: (500000, 600000),
			203027: (600000, 700000),
		}
		
		if itemVnum in formats:
			if len(formats[itemVnum]) == 1:
				self.AutoAppendTextLine(localeInfo.FRUIT_OF_LIFE_DESC_2.format(*formats[itemVnum]))
			else:
				self.AutoAppendTextLine(localeInfo.FRUIT_OF_LIFE_DESC_2_1.format(*formats[itemVnum]))
	
	def __HandleSpecialCostume(self, itemVnum):
		"""Handle special costume box items with hardcoded models."""
		models = {
			90051: (99903, 99902, 99901, 99908),
			90041: (99906, 99905, 99904, 99907),
			90071: (99909, 99908, 99907, 99907),
			90073: (99912, 99911, 99910, 99910),
			90074: (99915, 99914, 99913, 99913),
			90075: (99924, 99923, 99922, 99924),
			99901: (0, 0, 99901, 0),
			99902: (0, 99902, 0, 0),
			99903: (99903, 0, 0, 0),
		}
		
		labels = {
			99901: [localeInfo.COSTUME_WEAPON_FOR_BUFF],
			99902: [localeInfo.COSTUME_BODY_FOR_BUFF],
			99903: [localeInfo.COSTUME_HAIR_FOR_BUFF],
		}
		
		hair, body, weapon, acce = models.get(itemVnum, (0, 0, 0, 0))
		self.__IsBoxShowModel2(
			hairVnum=hair,
			bodyVnum=body,
			weaponVnum=weapon,
			acceVnum=acce,
			model=self.__ItemGetRaceShaman()
		)
		
		for label in labels.get(itemVnum, [localeInfo.COSTUME_HAIR, localeInfo.COSTUME_BODY, localeInfo.COSTUME_WEAPON]):
			self.AutoAppendTextLine(label)
	
	def __TryHandleCostumeSet(self, itemVnum):
		"""Handle costume set box items."""
		costume_mgr = get_costume_manager()
		if not costume_mgr.has_set(itemVnum):
			return
		
		race = player.GetOriginalRace()
		sex = chr.RaceToSex(race)
		data = costume_mgr.get_for_gender(itemVnum, sex == 1)
		
		if not data:
			return
		
		weaponVnum = self.__GetWeaponFromData(data)
		
		self.__IsBoxShowModel2(
			hairVnum=data.hair_vnum,
			bodyVnum=data.body_vnum,
			weaponVnum=weaponVnum,
			acceVnum=data.acce_vnum,
			model=self.__ItemGetRace()
		)
		
		if itemVnum != 50166:
			self.AutoAppendTextLine(localeInfo.COSTUME_HAIR)
			self.AutoAppendTextLine(localeInfo.COSTUME_BODY)
			self.AutoAppendTextLine(localeInfo.COSTUME_SASH)
			self.AutoAppendTextLine(localeInfo.COSTUME_WEAPON)
			self.AutoAppendTextLine(localeInfo.COSTUME_PICK_POSSIBILITY)
	
	def __AppendItemLimitsAndTips(self, window_type, slotIndex):
		"""Append time limits and additional tips."""
		for i in range(item.LIMIT_MAX_NUM):
			limitType, limitValue = item.GetLimit(i)
			
			if limitType == item.LIMIT_REAL_TIME_START_FIRST_USE:
				self.AppendRealTimeStartFirstUseLastTime(item, self.metinSlot, i)
			elif limitType == item.LIMIT_TIMER_BASED_ON_WEAR:
				self.AppendTimerBasedOnWearLastTime(self.metinSlot)
		
		self.__AppendSealInformation(window_type, slotIndex)
		self.AdditionalTips(window_type, self.itemVnum, self.metinSlot, slotIndex)
		self.AlignTextLineHorizonalCenter()
		self.ShowToolTip()
	
	def __AppendEnchantStatus(self, metinSlot):
		"""Display enchanted status indicator."""
		reinforcement = int(metinSlot[0]) if metinSlot else 0
		if reinforcement > 0:
			self.AppendSpace(15)
			self.AutoAppendTextLine(emoji.AppendEmoji("icon/emoji/34000.png"))
			self.AppendSpace(4)
			self.AutoAppendTextLine(localeInfo.TOOLTIP_ENCHANTED)
			self.AppendSpace(3)
	
	def __AppendEnchantIndicator(self):
		"""Display enchanted indicator without checking."""
		self.AppendSpace(15)
		self.AutoAppendTextLine(emoji.AppendEmoji("icon/emoji/34000.png"))
		self.AppendSpace(4)
		self.AutoAppendTextLine(localeInfo.TOOLTIP_ENCHANTED)
		self.AppendSpace(3)
	
	def __AppendQuiverTime(self, metinSlot):
		"""Display quiver real-time duration."""
		defaultValue = 0
		for i in range(item.LIMIT_MAX_NUM):
			limitType, defaultValue = item.GetLimit(i)
			if limitType == item.LIMIT_REAL_TIME:
				time = defaultValue if self.isShopItem else metinSlot[0]
				self.AppendMallItemLastTime(time)
				return
	
	def __AppendCostumeBonusAffects(self, itemVnum, metinSlot, bonusLeftTime):
		"""Display temporary costume bonus affects."""
		self.itemVnum = metinSlot[2]
		item.SelectItem(metinSlot[2])
		self.__AppendAffectInformation()
		self.itemVnum = itemVnum
		item.SelectItem(itemVnum)
		self.AppendCostumeBonuses(bonusLeftTime)
	
	def __AppendPetBonusAffects(self, itemVnum, metinSlot, bonusLeftTime):
		"""Display temporary pet bonus affects."""
		self.itemVnum = metinSlot[2]
		item.SelectItem(metinSlot[2])
		self.__AppendAffectInformation()
		self.itemVnum = itemVnum
		item.SelectItem(itemVnum)
		self.AppendCostumeBonuses(bonusLeftTime)
	
	def __AppendNewPetExtraBonus(self, itemVnum, metinSlot):
		"""Handle extra bonus system for new pets."""
		reinforcement = int(metinSlot[0]) if metinSlot else 0
		isSpecialPet = itemVnum in (80109, 80119, 80129)
		
		if reinforcement > 0:
			if isSpecialPet:
				self.__AppendExtraAffectInformation(1)
		else:
			# Base proto applies must show for special/max-level pets too (e.g. 80109 +9).
			# Previously guarded by "if not isSpecialPet", so a freshly refined +9 with
			# reinforcement == 0 displayed no bonuses at all.
			self.__AppendAffectInformation()

		if isSpecialPet and reinforcement > 0:
			self.__AppendEnchantIndicator()
	
	def __AppendRodAttributes(self, attrSlot):
		"""Display fishing rod attributes."""
		if not attrSlot:
			return
		
		for i in range(3):
			attrType = attrSlot[i][0]
			attrValue = attrSlot[i][1]
			
			if attrValue == 0:
				continue
			
			affectString = self.__GetAffectString(attrType, attrValue)
			if affectString:
				affectColor = self.__GetAttributeColor(i, attrValue)
				self.AppendTextLine(affectString, affectColor)
				self.toolTipHeight -= 7
				self.AppendTextLine(
					localeInfo.TOOLTIP_FISHINGROD_CAN_USE % attrSlot[3 + i][1],
					affectColor
				)
	
	def __HandleUseItemDetails(self, itemVnum, itemSubType, metinSlot):
		"""Handle specific use item types."""
		# Gold/stone usage count items
		if itemVnum in (27989, 76006):
			if metinSlot:
				useCount = int(metinSlot[0])
				self.AppendSpace(5)
				self.AppendTextLine(
					localeInfo.TOOLTIP_REST_USABLE_COUNT % (6 - useCount),
					self.NORMAL_COLOR
				)
		
		elif itemVnum == 50004:
			if metinSlot:
				useCount = int(metinSlot[0])
				self.AppendSpace(5)
				self.AppendTextLine(
					localeInfo.TOOLTIP_REST_USABLE_COUNT % (10 - useCount),
					self.NORMAL_COLOR
				)
		
		elif itemVnum == 50840:
			self.AppendSpace(5)
			affect1 = self.GetAffectStrings(72, 5)
			affect2 = self.GetAffectStrings(113, 5)
			self.AppendTextLine(affect1, self.POSITIVE_COLOR)
			self.AppendTextLine(affect2, self.POSITIVE_COLOR)
			self.AutoAppendTextLine(localeInfo.DURATION, self.CONDITION_COLOR)
			self.AutoAppendTextLine(
				emoji.AppendEmoji("icon/emoji/image-example-007.png") + " 15m",
				self.NORMAL_COLOR
			)
		
		elif constInfo.IS_AUTO_POTION(itemVnum):
			if metinSlot:
				isActivated = int(metinSlot[0])
				usedAmount = float(metinSlot[1])
				totalAmount = float(metinSlot[2]) or 1.0
				
				self.AppendSpace(5)
				if isActivated:
					self.AppendTextLine(
						"(%s)" % localeInfo.TOOLTIP_AUTO_POTION_USING,
						self.SPECIAL_POSITIVE_COLOR
					)
					self.AppendSpace(5)
		
		elif itemVnum in WARP_SCROLLS:
			if metinSlot:
				xPos = int(metinSlot[0])
				yPos = int(metinSlot[1])
				
				if xPos != 0 and yPos != 0:
					mapName, xBase, yBase = background.GlobalPositionToMapInfo(xPos, yPos)
					localeMapName = localeInfo.MINIMAP_ZONE_NAME_DICT.get(mapName, "")
					
					self.AppendSpace(5)
					if localeMapName:
						self.AppendTextLine(
							localeInfo.TOOLTIP_MEMORIZED_POSITION % (
								localeMapName,
								int(xPos - xBase) // 100,
								int(yPos - yBase) // 100
							),
							self.NORMAL_COLOR
						)
					else:
						self.AppendTextLine(
							localeInfo.TOOLTIP_MEMORIZED_POSITION_ERROR % (
								int(xPos) // 100,
								int(yPos) // 100
							),
							self.NORMAL_COLOR
						)
						dbg.TraceError("NOT_EXIST_IN_MINIMAP_ZONE_NAME_DICT: %s" % mapName)
		
		# Special use subtypes
		if itemSubType == item.USE_SPECIAL:
			if not self.AppendLastTimeInformation(metinSlot):
				if metinSlot and item.GetValue(2) == 1:
					self.AppendMallItemLastTime(metinSlot[player.METIN_SOCKET_MAX_NUM - 1])
		
		elif itemSubType == item.USE_TIME_CHARGE_PER:
			value = metinSlot[2] if metinSlot else 0
			self.AppendTextLine(
				localeInfo.TOOLTIP_TIME_CHARGER_PER(value or item.GetValue(0))
			)
			self.AppendLastTimeInformation(metinSlot)
		
		elif itemSubType == item.USE_TIME_CHARGE_FIX:
			value = metinSlot[2] if metinSlot else 0
			self.AppendTextLine(
				localeInfo.TOOLTIP_TIME_CHARGER_FIX(value or item.GetValue(0))
			)
			self.AppendLastTimeInformation(metinSlot)

	def AlignTextLineHorizonalCenter(self):
		for child in self.childrenList:
			if type(child).__name__ == "TextLine":
				(x, y) = child.GetLocalPosition()
				child.SetPosition(self.toolTipWidth / 2, y)

		self.ResizeToolTip()

	def AdditionalTips(self, window_type, itemVnum, metinSlot, slotIndex):
		"""Add contextual shortcut tips to item tooltips."""
		item.SelectItem(itemVnum)
		itemType = item.GetItemType()
		itemSubType = item.GetItemSubType()
		
		self.__AppendChestDropTip(itemVnum, slotIndex, window_type)
		self.__AppendInventoryShortcutTips(itemVnum, slotIndex, window_type)
		self.__AppendItemSpecificTips(itemVnum, window_type, slotIndex, metinSlot)
		self.__AppendGMDebugInfo(itemVnum, itemType, itemSubType, metinSlot, window_type, slotIndex)
	
	def __AppendChestDropTip(self, itemVnum, slotIndex, window_type):
		"""Add chest drop info tip if enabled."""
		if not settings.find_chest_tooltip:
			return
		if not app.__BL_CHEST_DROP_INFO__:
			return
		if slotIndex == -1 or window_type == 5:
			return
		
		self.AppendChestDropInfo(itemVnum)
	
	def __AppendInventoryShortcutTips(self, itemVnum, slotIndex, window_type):
		"""Add inventory movement and action shortcut tips."""
		item.SelectItem(itemVnum)
		
		# Special inventory slot range (277-1087)
		if 277 < slotIndex < 1087:
			if window_type != 5 and not item.CanUseInSpecialInv():
				if settings.extract_tooltip:
					self.__AddShortcutTip(localeInfo.INVENTORY_PULL_OUT_ITEM, "key_rclick")
		
		# Regular inventory slots with special inventory type
		elif -1 < slotIndex < 180:
			if item.GetSpecialInvType() != 0 and settings.add_additional_tooltip:
				self.__AddShortcutTip(localeInfo.INVENTORY_MOVE_TO_SPECIAL_INVENTORY, "key_shift", "key_rclick")
		
		# Stackable item separation tip
		if settings.split_tooltip and app.ENABLE_EMOJI_SYSTEM:
			if item.IsFlag(item.ITEM_FLAG_STACKABLE) and window_type == player.INVENTORY:
				if player.GetItemCount(window_type, slotIndex) > 1:
					self.AutoAppendTextLine("{} + {} - {}".format(
						emoji.AppendEmoji("icon/emoji/key_shift.png"),
						emoji.AppendEmoji("icon/emoji/key_lclick.png"),
						localeInfo.INVENTORY_SEPARATE_ITEMS
					))
	
	def __AppendItemSpecificTips(self, itemVnum, window_type, slotIndex, metinSlot):
		"""Add tips specific to certain item types or vnums."""
		# Time coupons (stack usage)
		TIME_COUPONS = {80008, 80009, 80007, 80006, 80005}
		if itemVnum in TIME_COUPONS:
			if player.GetItemCount(window_type, slotIndex) > 1:
				self.__AddShortcutTip(localeInfo.INVENTORY_USE_SOME_ITEMS.format(500), "key_alt", "key_rclick")
		
		# Gift boxes
		if app.ENABLE_EMOJI_SYSTEM:
			item.SelectItem(itemVnum)
			if item.GetItemType() == item.GIFTBOX and itemVnum not in item_ids:
				self.__AddShortcutTip(localeInfo.INVENTORY_SHOW_CHEST_DROP, "key_ctrl", "key_rclick")
				if slotIndex != -1:
					self.__AddShortcutTip(localeInfo.INVENTORY_USE_SOME_ITEMS.format(1000), "key_alt", "key_rclick")
		
		# Search in shops shortcut
		if itemVnum not in item_ids:
			self.__AddShortcutTip(localeInfo.SEARCH_IN_SHOPS_SHORTCUT, "key_ctrl", "key_x", "key_rclick")
		
		# Polymarble items
		POLYMARBLE_DATA = {
			70104: (1, [(1, 2000), (1, 15), (53, 50)]),
			53916: (None, [(1, 2000), (1, 15), (53, 50)]),
			70105: (2, [(63, 10), (106, 10)]),
			70106: (3, [(63, 20), (106, 15)]),
		}
		
		if itemVnum in POLYMARBLE_DATA:
			stage, affects = POLYMARBLE_DATA[itemVnum]
			if stage:
				self.AppendSpace(5)
				self.AutoAppendTextLine(localeInfo.POLYMARBLE_STAGE.format(stage))
			if affects:
				self.AppendSpace(5)
				for affect_type, affect_value in affects:
					affect_str = self.GetAffectStrings(affect_type, affect_value)
					self.AutoAppendTextLine(affect_str, self.POSITIVE_COLOR)
	
	def __AddShortcutTip(self, message, *key_icons):
		"""Helper to format shortcut tip with key icons."""
		keys = " + ".join(emoji.AppendEmoji("icon/emoji/" + k + ".png") for k in key_icons)
		self.AutoAppendTextLine("{} - {}".format(keys, message))
	
	def __AppendGMDebugInfo(self, itemVnum, itemType, itemSubType, metinSlot, window_type, slotIndex):
		"""Add debug information for Game Masters."""
		if not chr.IsGameMaster(0):
			return
		
		self.AppendSpace(5)
		self.AutoAppendTextLine("VNUM: {}, TYPE: {}, SUBTYPE: {}".format(itemVnum, itemType, itemSubType))
		
		if metinSlot:
			sockets = ", ".join(str(i) for i in metinSlot)
			self.AutoAppendTextLine("SOCKETS: [{}]".format(sockets))
			self.AutoAppendTextLine("WINDOW_TYPE: {}, SLOT_INDEX: {}".format(window_type, slotIndex))
			self.AutoAppendTextLine("SPECIAL_INV: TYPE: {}, CAN_USE_INSIDE: {}".format(
				item.GetSpecialInvType(), item.CanUseInSpecialInv()
			))
		
		self.ResizeToolTip()
		
	def __DragonSoulInfoString (self, dwVnum):
		step = int((dwVnum / 100) % 10)
		refine = int((dwVnum / 10) % 10)
		strengthStr = localeInfo.DRAGON_SOUL_STRENGTH(refine)
		if 0 == step:
			return localeInfo.DRAGON_SOUL_STEP_LEVEL1 + " " + strengthStr
		elif 1 == step:
			return localeInfo.DRAGON_SOUL_STEP_LEVEL2 + " " + strengthStr
		elif 2 == step:
			return localeInfo.DRAGON_SOUL_STEP_LEVEL3 + " " + strengthStr
		elif 3 == step:
			return localeInfo.DRAGON_SOUL_STEP_LEVEL4 + " " + strengthStr
		elif 4 == step:
			return localeInfo.DRAGON_SOUL_STEP_LEVEL5 + " " + strengthStr
		else:
			return ""

	def __AppendCostumeRealTimeItem(self, time):
			self.AppendSpace(5)
			self.AppendTextLine(localeInfo.AVAILABLE.format(localeInfo.TimeToDHMS(time)), self.NORMAL_COLOR)
			
	def __AppendCostumeRealTime(self, metinSlot):
		if metinSlot[3] > 0:
			self.AppendSpace(5)
			self.AppendTextLine(localeInfo.LEFT_BONUS_TIME + ": " + localeInfo.TimeToDHMS(metinSlot[3] - app.GetGlobalTimeStamp()), self.NORMAL_COLOR)
		
	def __IsHair(self, itemVnum):
		return (self.__IsOldHair(itemVnum) or
			self.__IsNewHair(itemVnum) or
			self.__IsNewHair2(itemVnum) or
			self.__IsNewHair3(itemVnum)
		)

	if app.__BL_CHEST_DROP_INFO__:
		def AppendChestDropInfo(self, itemVnum):
			hasinfo = item.HasDropInfo(itemVnum, False)
			if hasinfo:
				self.AppendSpace(5)
				self.AutoAppendTextLine(localeInfo.CHEST_DROP_INFO, self.NORMAL_COLOR)
				self.AutoAppendTextLine(localeInfo.CHEST_FIND_ITEMS_DESC_1)
				self.AutoAppendTextLine(localeInfo.CHEST_FIND_ITEMS_DESC_2)
				self.AppendSpace(5)

	def __IsOldHair(self, itemVnum):
		return itemVnum > 73000 and itemVnum < 74000

	def __IsNewHair(self, itemVnum):
		return itemVnum > 74000 and itemVnum < 75000

	def __IsNewHair2(self, itemVnum):
		return itemVnum > 75000 and itemVnum < 76000

	def __IsNewHair3(self, itemVnum):
		return ((74012 < itemVnum and itemVnum < 74022) or
			(74262 < itemVnum and itemVnum < 74272) or
			(74512 < itemVnum and itemVnum < 74599) or
			(74762 < itemVnum and itemVnum < 74799) or
			(99901 < itemVnum and itemVnum < 99903) or
			(45000 < itemVnum and itemVnum < 47000))

	if app.ENABLE_PREMIUM_PRIVATE_SHOP_OFFICIAL:
		def __AppendPrivateItemIcon(self, itemVnum):
			itemImage = ui.ImageBox()
			itemImage.SetParent(self)
			itemImage.Show()
			item.SelectItem(itemVnum)
			itemImage.LoadImage(item.GetIconImageFileName())
			itemImage.SetPosition((self.toolTipWidth/2)-16, self.toolTipHeight)
			self.toolTipHeight += itemImage.GetHeight()
			self.childrenList.append(itemImage)
			self.ResizeToolTip()

	if app.__BL_HYPERLINK_ITEM_ICON__:
		def AppendItemIcon(self, itemVnum):
			itemImage = ui.ImageBox()
			itemImage.SetParent(self)
			itemImage.Show()			
			item.SelectItem(itemVnum)
			try:
				itemImage.LoadImage(item.GetIconImageFileName())
			except:
				dbg.TraceError("ItemToolTip.AppendItemIcon() - Failed to find image file %d:%s" % 
					(itemVnum, item.GetIconImageFileName())
				)
			itemImage.SetPosition(self.toolTipWidth / 2 - itemImage.GetWidth() // 2, self.toolTipHeight)
			self.toolTipHeight += itemImage.GetHeight()
			self.childrenList.append(itemImage)
			self.ResizeToolTip()

	def __AppendHairIcon(self, itemVnum):
		itemImage = ui.ImageBox()
		itemImage.SetParent(self)
		itemImage.Show()

		if self.__IsOldHair(itemVnum):
			itemImage.LoadImage("d:/ymir work/item/quest/"+str(itemVnum)+".tga")
		elif self.__IsNewHair3(itemVnum):
			itemImage.LoadImage("icon/hair/%d.sub" % (itemVnum))
		elif self.__IsNewHair(itemVnum):
			itemImage.LoadImage("d:/ymir work/item/quest/"+str(itemVnum-1000)+".tga")
		elif self.__IsNewHair2(itemVnum):
			itemImage.LoadImage("icon/hair/%d.sub" % (itemVnum))

		if app.ENABLE_PREMIUM_PRIVATE_SHOP_OFFICIAL:
			if self.isPrivateSearchItem:
				itemImage.SetPosition((self.toolTipWidth/2)-48, self.toolTipHeight)
			else:
				itemImage.SetPosition((self.toolTipWidth/2)-48, self.toolTipHeight)
		else:
			itemImage.SetPosition(itemImage.GetWidth() // 2, self.toolTipHeight)

		self.toolTipHeight += itemImage.GetHeight()
		self.childrenList.append(itemImage)
		self.ResizeToolTip()

	def __AdjustMaxWidth(self, attrSlot, desc):
		newToolTipWidth = self.toolTipWidth
		newToolTipWidth = max(self.__AdjustAttrMaxWidth(attrSlot), newToolTipWidth)
		newToolTipWidth = max(self.__AdjustDescMaxWidth(desc), newToolTipWidth)
		if newToolTipWidth > self.toolTipWidth:
			self.toolTipWidth = newToolTipWidth
			self.ResizeToolTip()

	def __AdjustAttrMaxWidth(self, attrSlot):
		if 0 == attrSlot:
			return self.toolTipWidth

		maxWidth = self.toolTipWidth
		for i in range(player.ATTRIBUTE_SLOT_MAX_NUM):
			type = attrSlot[i][0]
			value = attrSlot[i][1]

			attrText = self.AppendTextLine(self.__GetAffectString(type, value))
			(tW, _) = attrText.GetTextSize()
			self.childrenList.remove(attrText)
			self.toolTipHeight -= self.TEXT_LINE_HEIGHT

			maxWidth = max(tW + 12, maxWidth)

		return maxWidth

	def __AdjustDescMaxWidth(self, desc):
		if len(desc) < DESC_DEFAULT_MAX_COLS:
			return self.toolTipWidth

		return DESC_WESTERN_MAX_WIDTH

	def ResizeToolTipWidth(self, width):
		self.toolTipWidth = width
		self.ResizeToolTip()

	def __CalculateToolTipWidth(self):
		affectTextLineLenList = []

		metinSocket = self.metinSlot
		if metinSocket:
			for socketIndex in metinSocket:
				if socketIndex:

					affectType, affectValue = item.GetAffect(0)
					affectString = self.__GetAffectString(affectType, affectValue)
					if affectString:
						affectTextLineLenList.append(len(affectString))

			if self.itemVnum:
				item.SelectItem(self.itemVnum)
			self.metinSlot = None

		if self.toolTipWidth == self.TOOL_TIP_WIDTH:
			if affectTextLineLenList:
				self.toolTipWidth += max(affectTextLineLenList) + 10

		self.AlignTextLineHorizonalCenter()

	def __SetSkillBookToolTip(self, skillIndex, bookName, skillGrade):
		skillName = skill.GetSkillName(skillIndex)

		if not skillName:
			return

		itemName = skillName + " " + bookName
		self.SetTitle(itemName)

	def __AppendPickInformation(self, curLevel, curEXP, maxEXP):
		self.AppendSpace(5)
		self.AppendTextLine(localeInfo.TOOLTIP_PICK_LEVEL % (curLevel), self.NORMAL_COLOR)
		self.AppendTextLine(localeInfo.TOOLTIP_PICK_EXP % (curEXP, maxEXP), self.NORMAL_COLOR)

		if curEXP == maxEXP:
			self.AppendSpace(5)
			self.AppendTextLine(localeInfo.TOOLTIP_PICK_UPGRADE1, self.NORMAL_COLOR)
			self.AppendTextLine(localeInfo.TOOLTIP_PICK_UPGRADE2, self.NORMAL_COLOR)
			self.AppendTextLine(localeInfo.TOOLTIP_PICK_UPGRADE3, self.NORMAL_COLOR)


	def __AppendRodInformation(self, curLevel, curEXP, maxEXP):
		self.AppendSpace(5)
		self.AppendTextLine(localeInfo.TOOLTIP_FISHINGROD_LEVEL % (curLevel), self.NORMAL_COLOR)
		self.AppendTextLine(localeInfo.TOOLTIP_FISHINGROD_EXP % (curEXP, maxEXP), self.NORMAL_COLOR)

		if curEXP == maxEXP:
			self.AppendSpace(5)
			self.AppendTextLine(localeInfo.TOOLTIP_FISHINGROD_UPGRADE1, self.NORMAL_COLOR)

	def __AppendLimitInformation(self):

		appendSpace = False

		for i in range(item.LIMIT_MAX_NUM):

			(limitType, limitValue) = item.GetLimit(i)

			if limitValue > 0:
				if False == appendSpace:
					self.AppendSpace(5)
					appendSpace = True

			else:
				continue

			if item.LIMIT_LEVEL == limitType:
				color = self.GetLimitTextLineColor(player.GetStatus(player.LEVEL), limitValue)
				self.AppendTextLine(self.swordEmoji + localeInfo.TOOLTIP_ITEM_LIMIT_LEVEL % (limitValue) + self.swordEmoji, color)
			elif item.LIMIT_MOUNT_LEVEL == limitType:
				color = self.GetLimitTextLineColor(constInfo.MOUNT_LEVEL, limitValue)
				self.AppendTextLine(localeInfo.TOOLTIP_ITEM_MOUNT_LIMIT_LEVEL % (limitValue), color)
			"""
			elif item.LIMIT_STR == limitType:
				color = self.GetLimitTextLineColor(player.GetStatus(player.ST), limitValue)
				self.AppendTextLine(localeInfo.TOOLTIP_ITEM_LIMIT_STR % (limitValue), color)
			elif item.LIMIT_DEX == limitType:
				color = self.GetLimitTextLineColor(player.GetStatus(player.DX), limitValue)
				self.AppendTextLine(localeInfo.TOOLTIP_ITEM_LIMIT_DEX % (limitValue), color)
			elif item.LIMIT_INT == limitType:
				color = self.GetLimitTextLineColor(player.GetStatus(player.IQ), limitValue)
				self.AppendTextLine(localeInfo.TOOLTIP_ITEM_LIMIT_INT % (limitValue), color)
			elif item.LIMIT_CON == limitType:
				color = self.GetLimitTextLineColor(player.GetStatus(player.HT), limitValue)
				self.AppendTextLine(localeInfo.TOOLTIP_ITEM_LIMIT_CON % (limitValue), color)
			"""

	def __AppendSealInformation(self, window_type, slotIndex):
		if not app.ENABLE_SOULBIND_SYSTEM:
			return

		itemSealDate = player.GetItemSealDate(window_type, slotIndex)
		if itemSealDate == item.GetDefaultSealDate():
			return

		if itemSealDate == item.GetUnlimitedSealDate():
			self.AppendSpace(5)
			self.AppendTextLine(localeInfo.TOOLTIP_SEALED, self.NEGATIVE_COLOR)

		elif itemSealDate > 0:
			self.AppendSpace(5)
			hours, minutes = player.GetItemUnSealLeftTime(window_type, slotIndex)
			self.AppendTextLine(localeInfo.TOOLTIP_UNSEAL_LEFT_TIME % (hours, minutes), self.NEGATIVE_COLOR)

	def __GetAffectString(self, affectType, affectValue):
		if 0 == affectType:
			return None

		if 0 == affectValue:
			return None

		try:
			return self.AFFECT_DICT[affectType](affectValue)
		except TypeError:
			return "UNKNOWN_VALUE[%s] %s" % (affectType, affectValue)
		except KeyError:
			return "UNKNOWN_TYPE[%s] %s" % (affectType, affectValue)

	def __AppendAffectInformation(self):
		for i in range(item.ITEM_APPLY_MAX_NUM):
			(affectType, affectValue) = item.GetAffect(i)
			if app.ENABLE_ACCE_COSTUME_SYSTEM and affectType==item.APPLY_ACCEDRAIN_RATE:
				continue
			affectString = self.__GetAffectString(affectType, affectValue)
			if affectString:
				self.AppendTextLine(affectString, self.GetChangeTextLineColor(affectValue))
	
	if app.ENABLE_EXTRABONUS_SYSTEM:
		def __AppendExtraAffectInformation(self, value):
			for i in range(item.ITEM_APPLY_MAX_NUM):
				(affectType, affectValue) = item.GetAffect(i)
				affectString = self.__GetAffectString(affectType, affectValue)
				if affectString:
					if value == 0:
						self.AppendTextLine("|cFF89b88d"+str(affectString)+" |cFFc8ff9c+"+str(affectValue*constInfo.RUNE_EXTRABONUS_VALUE//100)+"", self.GetChangeTextLineColor(affectValue))
					elif value == 1:
						self.AppendTextLine("|cFF89b88d"+str(affectString)+" |cFFc8ff9c+"+str(affectValue*constInfo.PET_EXTRABONUS_VALUE//100)+"", self.GetChangeTextLineColor(affectValue))

	if app.ENABLE_EXTRABONUS_SYSTEM:
		if app.ENABLE_GLOVE_SYSTEM:
			def __AppendGloveAttributeInformation(self, attrSlot, itemAbsChance = 0):
				if 0 != attrSlot:
					for i in range(player.ATTRIBUTE_SLOT_MAX_NUM):
						type = attrSlot[i][0]
						value = attrSlot[i][1]
						if 0 == value:
							continue
						affectString = self.__GetAffectString(type, value)
						if affectString:
							if i < 3:
								self.AppendTextLine("|cFF89b88d" + str(affectString) + " |cFFc8ff9c+" + str(GLOVE_BONUS_TABLE[type] // 9),self.GetChangeTextLineColor(value))
							else:
								self.AppendTextLine(affectString, self.SPECIAL_POSITIVE_COLOR)

			def AddGloveItemData(self, itemVnum, metinSlot, attrSlot = 0, flags = 0, unbindTime = 0, window_type = player.INVENTORY, slotIndex = -1):
				self.itemVnum = itemVnum
				item.SelectItem(itemVnum)
				itemType = item.GetItemType()
				itemSubType = item.GetItemSubType()
				self.__ModelPreviewClose()

				itemDesc = item.GetItemDescription()
				itemSummary = item.GetItemSummary()
				self.__AdjustMaxWidth(attrSlot, itemDesc)
				self.__SetItemTitle(itemVnum, metinSlot, attrSlot)
				self.AppendDescription(itemDesc, 26)
				self.AppendDescription(itemSummary, 26, self.CONDITION_COLOR)

				self.__AppendLimitInformation()
				self.__AppendMagicDefenceInfo()
				self.__AppendAffectInformation()	
				self.__AppendGloveAttributeInformation(attrSlot)
				self.AppendWearableInformation()
				self.__AppendMetinSlotInfo(metinSlot)

				self.__AppendSealInformation(window_type, slotIndex)
				self.AdditionalTips(window_type, itemVnum, metinSlot, slotIndex)
				self.AlignTextLineHorizonalCenter()
				self.ShowToolTip()

	def AppendLastTimeInformation(self, metinSlot):
		bHasRealtimeFlag = False
		for i in range(item.LIMIT_MAX_NUM):
			(limitType, limitValue) = item.GetLimit(i)
			if item.LIMIT_REAL_TIME == limitType:
				bHasRealtimeFlag = True

		if bHasRealtimeFlag:
			self.AppendMallItemLastTime(metinSlot[0])

		return bHasRealtimeFlag

	def AppendWearableInformation(self):

		self.AppendSpace(5)
		self.AppendTextLine(localeInfo.TOOLTIP_ITEM_WEARABLE_JOB, self.NORMAL_COLOR)

		flagList = (
			not item.IsAntiFlag(item.ITEM_ANTIFLAG_WARRIOR),
			not item.IsAntiFlag(item.ITEM_ANTIFLAG_ASSASSIN),
			not item.IsAntiFlag(item.ITEM_ANTIFLAG_SURA),
			not item.IsAntiFlag(item.ITEM_ANTIFLAG_SHAMAN))
		if app.ENABLE_WOLFMAN_CHARACTER:
			flagList += (not item.IsAntiFlag(item.ITEM_ANTIFLAG_WOLFMAN),)
		characterNames = ""
		for i in range(self.CHARACTER_COUNT):

			name = self.CHARACTER_NAMES[i]
			flag = flagList[i]

			if flag:
				characterNames += " "
				characterNames += name

		textLine = self.AppendTextLine(characterNames, self.NORMAL_COLOR, True)
		textLine.SetFeather()

		if item.IsAntiFlag(item.ITEM_ANTIFLAG_MALE):
			textLine = self.AppendTextLine(localeInfo.FOR_FEMALE, self.NORMAL_COLOR, True)
			textLine.SetFeather()

		if item.IsAntiFlag(item.ITEM_ANTIFLAG_FEMALE):
			textLine = self.AppendTextLine(localeInfo.FOR_MALE, self.NORMAL_COLOR, True)
			textLine.SetFeather()

	def __AppendPotionInformation(self):
		self.AppendSpace(5)

		healHP = item.GetValue(0)
		healSP = item.GetValue(1)
		healStatus = item.GetValue(2)
		healPercentageHP = item.GetValue(3)
		healPercentageSP = item.GetValue(4)

		if healHP > 0:
			self.AppendTextLine(localeInfo.TOOLTIP_POTION_PLUS_HP_POINT % healHP, self.GetChangeTextLineColor(healHP))
		if healSP > 0:
			self.AppendTextLine(localeInfo.TOOLTIP_POTION_PLUS_SP_POINT % healSP, self.GetChangeTextLineColor(healSP))
		if healStatus != 0:
			self.AppendTextLine(localeInfo.TOOLTIP_POTION_CURE)
		if healPercentageHP > 0:
			self.AppendTextLine(localeInfo.TOOLTIP_POTION_PLUS_HP_PERCENT % healPercentageHP, self.GetChangeTextLineColor(healPercentageHP))
		if healPercentageSP > 0:
			self.AppendTextLine(localeInfo.TOOLTIP_POTION_PLUS_SP_PERCENT % healPercentageSP, self.GetChangeTextLineColor(healPercentageSP))

	def __AppendAbilityPotionInformation(self):

		self.AppendSpace(5)

		abilityType = item.GetValue(0)
		time = item.GetValue(1)
		point = item.GetValue(2)


		affectText = self.__GetAffectString(abilityType, point)
		self.AutoAppendTextLine(affectText, self.POSITIVE_COLOR)
		self.AppendSpace(5)

		if time > 0:

			self.AutoAppendTextLine(localeInfo.DURATION, self.CONDITION_COLOR)
			self.AutoAppendTextLine(emoji.AppendEmoji("icon/emoji/image-example-007.png")+" "+localeInfo.SecondToDHM(time), self.NORMAL_COLOR)

	def GetPriceColor(self, price):
		if price>=constInfo.HIGH_PRICE:
			return self.HIGH_PRICE_COLOR
		if price>=constInfo.MIDDLE_PRICE:
			return self.MIDDLE_PRICE_COLOR
		else:
			return self.LOW_PRICE_COLOR

	def AppendPrice(self, price):
		if price <=0:
			return
		self.AppendSpace(5)
		self.AppendTextLine(localeInfo.NumberToGoldNotText(price)+" {}".format(emoji.AppendEmoji("icon/emoji/money_icon.png")), self.GetPriceColor(price))

	def AppendPriceBySecondaryCoin(self, price):
		self.AppendSpace(5)
		self.AppendTextLine("|cFF85d455"+localeInfo.TOOLTIP_BUYPRICE % (localeInfo.NumberToGoldNotText(price))+" {}".format(emoji.AppendEmoji("d:/ymir work/ui/stone_point/stone_point.tga")), self.GetPriceColor(price))

	if app.ENABLE_CHEQUE_SYSTEM:
		def AppendSellingPrice(self, price, cheque = 0, isPrivateShopBuilder = False):
			if item.IsAntiFlag(item.ITEM_ANTIFLAG_SELL) and \
				not isPrivateShopBuilder:		
				self.AppendTextLine(localeInfo.TOOLTIP_ANTI_SELL, self.DISABLE_COLOR)
				self.AppendSpace(5)
			else:
				
				if cheque > 0:
					self.AppendTextLine(localeInfo.CHEQUE_SYSTEM_WON % (str(cheque)), grp.GenerateColor(0.0, 0.8470, 1.0, 1.0))
				
				if price >= 0:
					self.AppendTextLine(localeInfo.CHEQUE_SYSTEM_YANG % (localeInfo.NumberToMoneyString(price)), self.GetPriceColor(price))
				
				self.AppendSpace(5)
	else:
		def AppendSellingPrice(self, price):
			if item.IsAntiFlag(item.ITEM_ANTIFLAG_SELL):			
				self.AppendTextLine(localeInfo.TOOLTIP_ANTI_SELL, self.DISABLE_COLOR)
				self.AppendSpace(5)
			else:
				self.AppendTextLine(localeInfo.TOOLTIP_SELLPRICE % (localeInfo.NumberToMoneyString(price)), self.GetPriceColor(price))
				self.AppendSpace(5)


	if app.ENABLE_CHEQUE_SYSTEM:
		def AppendCheque(self, price):
			if price <=0:
				return
			self.AppendSpace(5)
			self.AppendTextLine(localeInfo.NumberToGoldNotText(price)+" {}".format(emoji.AppendEmoji("icon/emoji/cheque_icon.png")), grp.GenerateColor(184./255, 184./255, 184./255, 1))

	def AppendOfflineShopSellingPrice(self, price, price2):
		self.AppendTextLine(localeInfo.NumberToMoneyString(price), self.GetPriceColor(price))
		self.AppendTextLine(localeInfo.NumberToCheque(price2), grp.GenerateColor(184./255, 184./255, 184./255, 1))

	def AppendMetinInformation(self):
		if constInfo.ENABLE_FULLSTONE_DETAILS:
			for i in range(item.ITEM_APPLY_MAX_NUM):
				(affectType, affectValue) = item.GetAffect(i)
				affectString = self.__GetAffectString(affectType, affectValue)
				if affectString:
					self.AppendSpace(5)
					self.AppendTextLine(affectString, self.GetChangeTextLineColor(affectValue))

	def AppendMetinWearInformation(self):

		self.AppendSpace(5)
		self.AppendTextLine(localeInfo.TOOLTIP_SOCKET_REFINABLE_ITEM, self.NORMAL_COLOR)

		flagList = (item.IsWearableFlag(item.WEARABLE_BODY),
					item.IsWearableFlag(item.WEARABLE_HEAD),
					item.IsWearableFlag(item.WEARABLE_FOOTS),
					item.IsWearableFlag(item.WEARABLE_WRIST),
					item.IsWearableFlag(item.WEARABLE_WEAPON),
					item.IsWearableFlag(item.WEARABLE_NECK),
					item.IsWearableFlag(item.WEARABLE_EAR),
					item.IsWearableFlag(item.WEARABLE_UNIQUE),
					item.IsWearableFlag(item.WEARABLE_SHIELD),
					item.IsWearableFlag(item.WEARABLE_ARROW))

		wearNames = ""
		for i in range(self.WEAR_COUNT):

			name = self.WEAR_NAMES[i]
			flag = flagList[i]

			if flag:
				wearNames += "  "
				wearNames += name

		textLine = ui.TextLine()
		textLine.SetParent(self)
		textLine.SetFontName(self.defFontName)
		textLine.SetPosition(self.toolTipWidth/2, self.toolTipHeight)
		textLine.SetHorizontalAlignCenter()
		textLine.SetPackedFontColor(self.NORMAL_COLOR)
		textLine.SetText(wearNames)
		textLine.Show()
		self.childrenList.append(textLine)

		self.toolTipHeight += self.TEXT_LINE_HEIGHT
		self.ResizeToolTip()

	def GetMetinSocketType(self, number):
		if player.METIN_SOCKET_TYPE_NONE == number:
			return player.METIN_SOCKET_TYPE_NONE
		elif player.METIN_SOCKET_TYPE_SILVER == number:
			return player.METIN_SOCKET_TYPE_SILVER
		elif player.METIN_SOCKET_TYPE_GOLD == number:
			return player.METIN_SOCKET_TYPE_GOLD
		else:
			item.SelectItem(number)
			if item.METIN_NORMAL == item.GetItemSubType():
				return player.METIN_SOCKET_TYPE_SILVER
			elif item.METIN_GOLD == item.GetItemSubType():
				return player.METIN_SOCKET_TYPE_GOLD
			elif "USE_PUT_INTO_ACCESSORY_SOCKET" == item.GetUseType(number):
				return player.METIN_SOCKET_TYPE_SILVER
			elif "USE_PUT_INTO_RING_SOCKET" == item.GetUseType(number):
				return player.METIN_SOCKET_TYPE_SILVER
			elif "USE_PUT_INTO_BELT_SOCKET" == item.GetUseType(number):
				return player.METIN_SOCKET_TYPE_SILVER

		return player.METIN_SOCKET_TYPE_NONE

	def GetMetinItemIndex(self, number):
		if player.METIN_SOCKET_TYPE_SILVER == number:
			return 0
		if player.METIN_SOCKET_TYPE_GOLD == number:
			return 0

		return number

	def __AppendAccessoryMetinSlotInfo(self, metinSlot, mtrlVnum):
		ACCESSORY_SOCKET_MAX_SIZE = 3

		cur=min(metinSlot[0], ACCESSORY_SOCKET_MAX_SIZE)
		end=min(metinSlot[1], ACCESSORY_SOCKET_MAX_SIZE)

		affectType1, affectValue1 = item.GetAffect(0)
		affectList1=[0, max(1, affectValue1*10/100), max(2, affectValue1*20/100), max(3, affectValue1*40/100)]

		affectType2, affectValue2 = item.GetAffect(1)
		affectList2=[0, max(1, affectValue2*10/100), max(2, affectValue2*20/100), max(3, affectValue2*40/100)]

		affectType3, affectValue3 = item.GetAffect(2)
		affectList3=[0, max(1, affectValue3*10/100), max(2, affectValue3*20/100), max(3, affectValue3*40/100)]

		mtrlPos=0
		mtrlList=[mtrlVnum]*cur+[player.METIN_SOCKET_TYPE_SILVER]*(end-cur)
		for mtrl in mtrlList:
			affectString1 = self.__GetAffectString(affectType1, affectList1[mtrlPos+1]-affectList1[mtrlPos])
			affectString2 = self.__GetAffectString(affectType2, affectList2[mtrlPos+1]-affectList2[mtrlPos])
			affectString3 = self.__GetAffectString(affectType3, affectList3[mtrlPos+1]-affectList3[mtrlPos])

			leftTime = 0
			if cur == mtrlPos+1:
				leftTime=metinSlot[2]

			self.__AppendMetinSlotInfo_AppendMetinSocketData(mtrlPos, mtrl, affectString1, affectString2, affectString3, leftTime)
			mtrlPos+=1

	def __AppendMetinSlotInfo(self, metinSlot):
		if self.__AppendMetinSlotInfo_IsEmptySlotList(metinSlot):
			return
		
		if app.ENABLE_EXTENDED_SOCKETS:
			for i in range(player.ITEM_STONES_MAX_NUM):
				self.__AppendMetinSlotInfo_AppendMetinSocketData(i, metinSlot[i])
		else:
			for i in range(player.METIN_SOCKET_MAX_NUM):
				self.__AppendMetinSlotInfo_AppendMetinSocketData(i, metinSlot[i])			

	def __AppendMetinSlotInfo_IsEmptySlotList(self, metinSlot):
		if 0 == metinSlot:
			return 1
			
		if app.ENABLE_EXTENDED_SOCKETS:
			for i in range(player.ITEM_STONES_MAX_NUM):
				metinSlotData=metinSlot[i]
				if 0 != self.GetMetinSocketType(metinSlotData):
					if 0 != self.GetMetinItemIndex(metinSlotData):
						return 0
		else:
			for i in range(player.METIN_SOCKET_MAX_NUM):
				metinSlotData=metinSlot[i]
				if 0 != self.GetMetinSocketType(metinSlotData):
					if 0 != self.GetMetinItemIndex(metinSlotData):
						return 0

		return 1

	def __AppendMetinSlotInfo_AppendMetinSocketData(self, index, metinSlotData, custumAffectString="", custumAffectString2="", custumAffectString3="", leftTime=0):

		slotType = self.GetMetinSocketType(metinSlotData)
		itemIndex = self.GetMetinItemIndex(metinSlotData)

		if 0 == slotType:
			return

		self.AppendSpace(5)

		slotImage = ui.ImageBox()
		slotImage.SetParent(self)
		slotImage.Show()

		nameTextLine = ui.TextLine()
		nameTextLine.SetParent(self)
		nameTextLine.SetFontName(self.defFontName)
		nameTextLine.SetPackedFontColor(self.NORMAL_COLOR)
		nameTextLine.SetOutline()
		nameTextLine.SetFeather()
		nameTextLine.SetHorizontalAlignCenter()
		nameTextLine.Show()

		self.childrenList.append(nameTextLine)

		if player.METIN_SOCKET_TYPE_SILVER == slotType:
			slotImage.LoadImage("d:/ymir work/ui/game/windows/metin_slot_silver.sub")
		elif player.METIN_SOCKET_TYPE_GOLD == slotType:
			slotImage.LoadImage("d:/ymir work/ui/game/windows/metin_slot_gold.sub")

		self.childrenList.append(slotImage)

		slotImage.SetPosition(4, self.toolTipHeight-1)
		nameTextLine.SetPosition(0, self.toolTipHeight + 2)

		metinImage = ui.ImageBox()
		metinImage.SetParent(self)
		metinImage.Show()
		self.childrenList.append(metinImage)

		if itemIndex:

			item.SelectItem(itemIndex)

			try:
				metinImage.LoadImage(item.GetIconImageFileName())
			except:
				dbg.TraceError("ItemToolTip.__AppendMetinSocketData() - Failed to find image file %d:%s" %
					(itemIndex, item.GetIconImageFileName())
				)

			nameTextLine.SetText(item.GetItemName())

			affectTextLine = ui.TextLine()
			affectTextLine.SetParent(self)
			affectTextLine.SetFontName(self.defFontName)
			affectTextLine.SetPackedFontColor(self.POSITIVE_COLOR)
			affectTextLine.SetOutline()
			affectTextLine.SetFeather()
			affectTextLine.SetHorizontalAlignCenter()
			affectTextLine.Show()

			metinImage.SetPosition(6, self.toolTipHeight)
			affectTextLine.SetPosition(0, self.toolTipHeight + 16 + 2)

			if custumAffectString:
				affectTextLine.SetText(custumAffectString)
			elif itemIndex!=constInfo.ERROR_METIN_STONE:
				affectType, affectValue = item.GetAffect(0)
				affectString = self.__GetAffectString(affectType, affectValue)
				if affectString:
					affectTextLine.SetText(affectString)
			else:
				affectTextLine.SetText(localeInfo.TOOLTIP_APPLY_NOAFFECT)

			self.childrenList.append(affectTextLine)

			if constInfo.ENABLE_FULLSTONE_DETAILS and (not custumAffectString2) and (itemIndex!=constInfo.ERROR_METIN_STONE):
				custumAffectString2 = self.__GetAffectString(*item.GetAffect(1))

			if custumAffectString2:
				affectTextLine = ui.TextLine()
				affectTextLine.SetParent(self)
				affectTextLine.SetFontName(self.defFontName)
				affectTextLine.SetPackedFontColor(self.POSITIVE_COLOR)
				affectTextLine.SetPosition(0, self.toolTipHeight + 16 + 2 + 16 + 2)
				affectTextLine.SetHorizontalAlignCenter()
				affectTextLine.SetOutline()
				affectTextLine.SetFeather()
				affectTextLine.Show()
				affectTextLine.SetText(custumAffectString2)
				self.childrenList.append(affectTextLine)
				self.toolTipHeight += 16 + 2

			if constInfo.ENABLE_FULLSTONE_DETAILS and (not custumAffectString3) and (itemIndex!=constInfo.ERROR_METIN_STONE):
				custumAffectString3 = self.__GetAffectString(*item.GetAffect(2))

			if custumAffectString3:
				affectTextLine = ui.TextLine()
				affectTextLine.SetParent(self)
				affectTextLine.SetFontName(self.defFontName)
				affectTextLine.SetPackedFontColor(self.POSITIVE_COLOR)
				affectTextLine.SetPosition(0, self.toolTipHeight + 16 + 2 + 16 + 2)
				affectTextLine.SetHorizontalAlignCenter()
				affectTextLine.SetOutline()
				affectTextLine.SetFeather()
				affectTextLine.Show()
				affectTextLine.SetText(custumAffectString3)
				self.childrenList.append(affectTextLine)
				self.toolTipHeight += 16 + 2

			if 0 != leftTime:
				timeText = (emoji.AppendEmoji("icon/emoji/image-example-007.png") + " "+localeInfo.LEFT_TIME + ": " + localeInfo.SecondToDHM(leftTime))


				timeTextLine = ui.TextLine()
				timeTextLine.SetParent(self)
				timeTextLine.SetFontName(self.defFontName)
				timeTextLine.SetPosition(0, self.toolTipHeight + 16 + 2 + 16 + 2)
				timeTextLine.SetHorizontalAlignCenter()
				timeTextLine.SetOutline()
				timeTextLine.SetFeather()
				timeTextLine.Show()
				timeTextLine.SetText(timeText)
				self.childrenList.append(timeTextLine)
				self.toolTipHeight += 16 + 2

		else:
			nameTextLine.SetText(localeInfo.TOOLTIP_SOCKET_EMPTY)

		self.toolTipHeight += 35
		self.toolTipWidth += 25
		self.ResizeToolTip()

	def __AppendFishInfo(self, size, price):
		self.AppendSpace(5)
		if size > 0:
			self.AppendTextLine(localeInfo.TOOLTIP_FISH_LEN % (float(size) / 100.0), self.NORMAL_COLOR)
		if price > 0:
			self.AppendTextLine(localeInfo.TOOLTIP_FISH_PRICE % localeInfo.NumberToMoneyString(price), self.HIGH_PRICE_COLOR)

	def AppendUniqueItemLastTime(self, restMin):
		if restMin > 0:
			restSecond = restMin*60
			self.AppendSpace(5)
			self.AutoAppendTextLine(localeInfo.LEFTOVER_TIME, self.CONDITION_COLOR)
			self.AutoAppendTextLine(emoji.AppendEmoji("icon/emoji/image-example-007.png")+" "+localeInfo.SecondToDHM(restSecond), self.NORMAL_COLOR)

	def AppendMallItemLastTime(self, endTime):
		if endTime > 0:
			leftSec = max(0, endTime - app.GetGlobalTimeStamp())
			self.AppendSpace(5)
			self.AutoAppendTextLine(localeInfo.LEFTOVER_TIME, self.CONDITION_COLOR)
			self.AutoAppendTextLine(emoji.AppendEmoji("icon/emoji/image-example-007.png")+" "+localeInfo.SecondToDHM(leftSec), self.NORMAL_COLOR)

	if app.ENABLE_VS_COSTUME_BONUSES:
		def AppendCostumeBonuses(self, endTime):
			if endTime > 0:
				self.AppendSpace(5)
				self.AutoAppendTextLine(localeInfo.LEFTOVER_BONUS_TIME, self.CONDITION_COLOR)
				self.AutoAppendTextLine(emoji.AppendEmoji("icon/emoji/image-example-007.png")+" "+localeInfo.SecondToDHMS(endTime), self.NORMAL_COLOR)

	def AppendTimerBasedOnWearLastTime(self, metinSlot):
		if metinSlot is None:
			return
		if 0 == metinSlot[0]:
			self.AppendSpace(5)
			self.AppendTextLine(localeInfo.CANNOT_USE, self.DISABLE_COLOR)
		else:
			endTime = app.GetGlobalTimeStamp() + metinSlot[0]
			self.AppendMallItemLastTime(endTime)

	def AppendRealTimeStartFirstUseLastTime(self, item, metinSlot, limitIndex):
		useCount = metinSlot[1]
		endTime = metinSlot[0]

		if 0 == useCount:
			if 0 == endTime:
				(limitType, limitValue) = item.GetLimit(limitIndex)
				endTime = limitValue

			endTime += app.GetGlobalTimeStamp()

		self.AppendMallItemLastTime(endTime)

	if app.ENABLE_ACCE_COSTUME_SYSTEM:
		def SetAcceResultItem(self, slotIndex, window_type = player.INVENTORY):
			(itemVnum, MinAbs, MaxAbs) = acce.GetResultItem()
			if not itemVnum:
				return

			self.ClearToolTip()

			metinSlot 	= [player.GetItemMetinSocket(window_type, slotIndex, i) 	for i in range(player.METIN_SOCKET_MAX_NUM)	]
			attrSlot 	= [player.GetItemAttribute(window_type, slotIndex, i) 		for i in range(player.ATTRIBUTE_SLOT_MAX_NUM)	]

			item.SelectItem(itemVnum)
			itemType = item.GetItemType()
			itemSubType = item.GetItemSubType()
			if itemType != item.COSTUME and itemSubType != item.COSTUME_TYPE_ACCE:
				return

			absChance = MaxAbs
			itemDesc = item.GetItemDescription()
			self.__AdjustMaxWidth(attrSlot, itemDesc)
			self.__SetItemTitle(itemVnum, metinSlot, attrSlot)
			self.AppendDescription(itemDesc, 26)
			self.AppendDescription(item.GetItemSummary(), 26, self.CONDITION_COLOR)
			self.__AppendLimitInformation()

			if MinAbs == MaxAbs:
				self.AppendTextLine(localeInfo.ACCE_ABSORB_CHANCE % (MinAbs), self.CONDITION_COLOR)
			else:
				self.AppendTextLine(localeInfo.ACCE_ABSORB_CHANCE2 % (MinAbs, MaxAbs), self.CONDITION_COLOR)

			itemAbsorbedVnum = int(metinSlot[acce.ABSORBED_SOCKET])
			if itemAbsorbedVnum:
				item.SelectItem(itemAbsorbedVnum)
				if item.GetItemType() == item.WEAPON:
					if item.GetItemSubType() == item.WEAPON_FAN:
						self.__AppendMagicAttackInfo(absChance)
						item.SelectItem(itemAbsorbedVnum)
						self.__AppendAttackPowerInfo(absChance)
					else:
						self.__AppendAttackPowerInfo(absChance)
						item.SelectItem(itemAbsorbedVnum)
						self.__AppendMagicAttackInfo(absChance)
				elif item.GetItemType() == item.ARMOR:
					defGrade = item.GetValue(1)
					defBonus = item.GetValue(5) * 2
					defGrade = self.CalcAcceValue(defGrade, absChance)
					defBonus = self.CalcAcceValue(defBonus, absChance)

					if defGrade > 0:
						self.AppendSpace(5)
						self.AppendTextLine(localeInfo.TOOLTIP_ITEM_DEF_GRADE % (defGrade + defBonus), self.GetChangeTextLineColor(defGrade))

					item.SelectItem(itemAbsorbedVnum)
					self.__AppendMagicDefenceInfo(absChance)

				item.SelectItem(itemAbsorbedVnum)
				for i in range(item.ITEM_APPLY_MAX_NUM):
					(affectType, affectValue) = item.GetAffect(i)
					affectValue = self.CalcAcceValue(affectValue, absChance)
					affectString = self.__GetAffectString(affectType, affectValue)
					if (not app.USE_ACCE_ABSORB_WITH_NO_NEGATIVE_BONUS and affectString and affectValue != 0)\
							or (app.USE_ACCE_ABSORB_WITH_NO_NEGATIVE_BONUS and affectString and affectValue > 0):
						self.AppendTextLine(affectString, self.GetChangeTextLineColor(affectValue))

					item.SelectItem(itemAbsorbedVnum)

			item.SelectItem(itemVnum)
			self.__AppendAttributeInformation(attrSlot, MaxAbs)

			if itemAbsorbedVnum:
				self.AppendSpace(5)
				self.AppendHorizontalLine()
				self.AppendSpace(5)
				self.AppendTextLine(localeInfo.SASH_ABSORBED_ITEM, self.CONDITION_COLOR)
				item.SelectItem(itemAbsorbedVnum)
				self.AppendTextLine(item.GetItemName(), self.CONDITION_COLOR)

			self.AppendWearableInformation()
			self.ShowToolTip()

		def SetAcceResultAbsItem(self, slotIndex1, slotIndex2, window_type = player.INVENTORY):
			itemVnumAcce = player.GetItemIndex(window_type, slotIndex1)
			itemVnumTarget = player.GetItemIndex(window_type, slotIndex2)
			if not itemVnumAcce or not itemVnumTarget:
				return

			self.ClearToolTip()

			item.SelectItem(itemVnumAcce)
			itemType = item.GetItemType()
			itemSubType = item.GetItemSubType()
			if itemType != item.COSTUME and itemSubType != item.COSTUME_TYPE_ACCE:
				return

			metinSlot = [player.GetItemMetinSocket(window_type, slotIndex1, i) for i in range(player.METIN_SOCKET_MAX_NUM)]
			attrSlot = [player.GetItemAttribute(window_type, slotIndex2, i) for i in range(player.ATTRIBUTE_SLOT_MAX_NUM)]

			itemDesc = item.GetItemDescription()
			self.__AdjustMaxWidth(attrSlot, itemDesc)
			self.__SetItemTitle(itemVnumAcce, metinSlot, attrSlot)
			self.AppendDescription(itemDesc, 26)
			self.AppendDescription(item.GetItemSummary(), 26, self.CONDITION_COLOR)
			item.SelectItem(itemVnumAcce)
			self.__AppendLimitInformation()

			self.AppendTextLine(localeInfo.ACCE_ABSORB_CHANCE % (metinSlot[acce.ABSORPTION_SOCKET]), self.CONDITION_COLOR)

			itemAbsorbedVnum = itemVnumTarget
			item.SelectItem(itemAbsorbedVnum)
			if item.GetItemType() == item.WEAPON:
				if item.GetItemSubType() == item.WEAPON_FAN:
					self.__AppendMagicAttackInfo(metinSlot[acce.ABSORPTION_SOCKET])
					item.SelectItem(itemAbsorbedVnum)
					self.__AppendAttackPowerInfo(metinSlot[acce.ABSORPTION_SOCKET])
				else:
					self.__AppendAttackPowerInfo(metinSlot[acce.ABSORPTION_SOCKET])
					item.SelectItem(itemAbsorbedVnum)
					self.__AppendMagicAttackInfo(metinSlot[acce.ABSORPTION_SOCKET])
			elif item.GetItemType() == item.ARMOR:
				defGrade = item.GetValue(1)
				defBonus = item.GetValue(5) * 2
				defGrade = self.CalcAcceValue(defGrade, metinSlot[acce.ABSORPTION_SOCKET])
				defBonus = self.CalcAcceValue(defBonus, metinSlot[acce.ABSORPTION_SOCKET])

				if defGrade > 0:
					self.AppendSpace(5)
					self.AppendTextLine(localeInfo.TOOLTIP_ITEM_DEF_GRADE % (defGrade + defBonus), self.GetChangeTextLineColor(defGrade))

				item.SelectItem(itemAbsorbedVnum)
				self.__AppendMagicDefenceInfo(metinSlot[acce.ABSORPTION_SOCKET])

			item.SelectItem(itemAbsorbedVnum)
			for i in range(item.ITEM_APPLY_MAX_NUM):
				(affectType, affectValue) = item.GetAffect(i)
				affectValue = self.CalcAcceValue(affectValue, metinSlot[acce.ABSORPTION_SOCKET])
				affectString = self.__GetAffectString(affectType, affectValue)
				if (not app.USE_ACCE_ABSORB_WITH_NO_NEGATIVE_BONUS and affectString and affectValue != 0)\
						or (app.USE_ACCE_ABSORB_WITH_NO_NEGATIVE_BONUS and affectString and affectValue > 0):
					self.AppendTextLine(affectString, self.GetChangeTextLineColor(affectValue))

				item.SelectItem(itemAbsorbedVnum)

			item.SelectItem(itemAbsorbedVnum)
			for i in range(player.ATTRIBUTE_SLOT_MAX_NUM):
				type = attrSlot[i][0]
				value = attrSlot[i][1]
				if not value:
					continue

				affectValue = self.CalcAcceValue(value, metinSlot[acce.ABSORPTION_SOCKET])
				affectString = self.__GetAffectString(type, affectValue)
				if (not app.USE_ACCE_ABSORB_WITH_NO_NEGATIVE_BONUS and affectString and affectValue != 0)\
						or (app.USE_ACCE_ABSORB_WITH_NO_NEGATIVE_BONUS and affectString and affectValue > 0):
					affectColor = self.__GetAttributeColor(i, affectValue)
					self.AppendTextLine(affectString, affectColor)

				item.SelectItem(itemAbsorbedVnum)

			item.SelectItem(itemVnumAcce)
			self.AppendSpace(5)
			self.AppendTextLine(localeInfo.TOOLTIP_ITEM_WEARABLE_JOB, self.NORMAL_COLOR)

			item.SelectItem(itemVnumAcce)
			flagList = (
						not item.IsAntiFlag(item.ITEM_ANTIFLAG_WARRIOR),
						not item.IsAntiFlag(item.ITEM_ANTIFLAG_ASSASSIN),
						not item.IsAntiFlag(item.ITEM_ANTIFLAG_SURA),
						not item.IsAntiFlag(item.ITEM_ANTIFLAG_SHAMAN)
			)

			if app.ENABLE_WOLFMAN_CHARACTER:
				flagList += (not item.IsAntiFlag(item.ITEM_ANTIFLAG_WOLFMAN),)

			characterNames = ""
			for i in range(self.CHARACTER_COUNT):
				name = self.CHARACTER_NAMES[i]
				flag = flagList[i]
				if flag:
					characterNames += " "
					characterNames += name

			textLine = self.AppendTextLine(characterNames, self.NORMAL_COLOR, True)
			textLine.SetFeather()

			item.SelectItem(itemVnumAcce)
			if item.IsAntiFlag(item.ITEM_ANTIFLAG_MALE):
				textLine = self.AppendTextLine(localeInfo.FOR_FEMALE, self.NORMAL_COLOR, True)
				textLine.SetFeather()

			if item.IsAntiFlag(item.ITEM_ANTIFLAG_FEMALE):
				textLine = self.AppendTextLine(localeInfo.FOR_MALE, self.NORMAL_COLOR, True)
				textLine.SetFeather()

			self.ShowToolTip()

	if app.ENABLE_AURA_SYSTEM:
		def SetAuraResultItem(self, slotIndex, window_type = player.INVENTORY):
			(itemVnum, MinAbs, MaxAbs) = aura.GetResultItem()
			if not itemVnum:
				return
			
			self.ClearToolTip()
			
			metinSlot = [player.GetItemMetinSocket(window_type, slotIndex, i) for i in range(player.METIN_SOCKET_MAX_NUM)]
			attrSlot = [player.GetItemAttribute(window_type, slotIndex, i) for i in range(player.ATTRIBUTE_SLOT_MAX_NUM)]
			
			item.SelectItem(itemVnum)
			itemType = item.GetItemType()
			itemSubType = item.GetItemSubType()
			if itemType != item.COSTUME and itemSubType != item.COSTUME_TYPE_AURA:
				return
			
			absChance = float(MinAbs) / 10.0
			itemDesc = item.GetItemDescription()
			self.__AdjustMaxWidth(attrSlot, itemDesc)
			self.__SetItemTitle(itemVnum, metinSlot, attrSlot)
			self.AppendDescription(itemDesc, 26)
			self.AppendDescription(item.GetItemSummary(), 26, self.CONDITION_COLOR)
			self.__AppendLimitInformation()
			
			self.AppendTextLine(localeInfo.AURA_LEVEL_STEP % (int(metinSlot[aura.LEVEL_SOCKET]), int(metinSlot[aura.LEVEL_SOCKET])), self.CONDITION_COLOR)
			self.AppendTextLine(localeInfo.AURA_DRAIN_PER % (absChance), self.CONDITION_COLOR)
			
			itemAbsorbedVnum = int(metinSlot[aura.ABSORBED_SOCKET])
			if itemAbsorbedVnum:
				item.SelectItem(itemAbsorbedVnum)
				if item.GetItemType() == item.WEAPON:
					if item.GetItemSubType() == item.WEAPON_FAN:
						self.__AppendMagicAttackInfo(absChance)
						item.SelectItem(itemAbsorbedVnum)
						self.__AppendAttackPowerInfo(absChance)
					else:
						self.__AppendAttackPowerInfo(absChance)
						item.SelectItem(itemAbsorbedVnum)
						self.__AppendMagicAttackInfo(absChance)
				elif item.GetItemType() == item.ARMOR:
					defGrade = item.GetValue(1)
					defBonus = item.GetValue(5) * 2
					defGrade = self.CalcSashValue(defGrade, absChance)
					defBonus = self.CalcSashValue(defBonus, absChance)
					
					if defGrade > 0:
						self.AppendSpace(5)
						self.AppendTextLine(localeInfo.TOOLTIP_ITEM_DEF_GRADE % (defGrade + defBonus), self.GetChangeTextLineColor(defGrade))
					
					item.SelectItem(itemAbsorbedVnum)
					self.__AppendMagicDefenceInfo(absChance)
				
				item.SelectItem(itemAbsorbedVnum)
				for i in range(item.ITEM_APPLY_MAX_NUM):
					(affectType, affectValue) = item.GetAffect(i)
					affectValue = self.CalcSashValue(affectValue, absChance)
					affectString = self.__GetAffectString(affectType, affectValue)
					if affectString and affectValue > 0:
						self.AppendTextLine(affectString, self.GetChangeTextLineColor(affectValue))
					
					item.SelectItem(itemAbsorbedVnum)
				
			item.SelectItem(itemVnum)
			self.__AppendAttributeInformation(attrSlot, MaxAbs)
			
			self.AppendWearableInformation()
			self.ShowToolTip()
			
		def SetAuraResultAbsItem(self, slotIndex1, slotIndex2, window_type = player.INVENTORY):
			itemVnumAura = player.GetItemIndex(window_type, slotIndex1)
			itemVnumTarget = player.GetItemIndex(window_type, slotIndex2)
			if not itemVnumAura or not itemVnumTarget:
				return
			
			self.ClearToolTip()
			
			item.SelectItem(itemVnumAura)
			itemType = item.GetItemType()
			itemSubType = item.GetItemSubType()
			if itemType != item.COSTUME and itemSubType != item.COSTUME_TYPE_AURA:
				return
			
			metinSlot = [player.GetItemMetinSocket(window_type, slotIndex1, i) for i in range(player.METIN_SOCKET_MAX_NUM)]
			attrSlot = [player.GetItemAttribute(window_type, slotIndex2, i) for i in range(player.ATTRIBUTE_SLOT_MAX_NUM)]
			
			itemDesc = item.GetItemDescription()
			self.__AdjustMaxWidth(attrSlot, itemDesc)
			self.__SetItemTitle(itemVnumAura, metinSlot, attrSlot)
			self.AppendDescription(itemDesc, 26)
			self.AppendDescription(item.GetItemSummary(), 26, self.CONDITION_COLOR)
			item.SelectItem(itemVnumAura)
			self.__AppendLimitInformation()
			
			absChance = float(metinSlot[aura.ABSORPTION_SOCKET]) / 10.0
			
			self.AppendTextLine(localeInfo.AURA_LEVEL_STEP % (int(metinSlot[aura.LEVEL_SOCKET]), int(metinSlot[aura.LEVEL_SOCKET])), self.CONDITION_COLOR)
			self.AppendTextLine(localeInfo.AURA_DRAIN_PER % (absChance), self.CONDITION_COLOR)
			
			itemAbsorbedVnum = itemVnumTarget
			item.SelectItem(itemAbsorbedVnum)
			if item.GetItemType() == item.WEAPON:
				if item.GetItemSubType() == item.WEAPON_FAN:
					self.__AppendMagicAttackInfo(absChance)
					item.SelectItem(itemAbsorbedVnum)
					self.__AppendAttackPowerInfo(absChance)
				else:
					self.__AppendAttackPowerInfo(absChance)
					item.SelectItem(itemAbsorbedVnum)
					self.__AppendMagicAttackInfo(absChance)
			elif item.GetItemType() == item.ARMOR:
				defGrade = item.GetValue(1)
				defBonus = item.GetValue(5) * 2
				defGrade = self.CalcSashValue(defGrade, absChance)
				defBonus = self.CalcSashValue(defBonus, absChance)
				
				if defGrade > 0:
					self.AppendSpace(5)
					self.AppendTextLine(localeInfo.TOOLTIP_ITEM_DEF_GRADE % (defGrade + defBonus), self.GetChangeTextLineColor(defGrade))
				
				item.SelectItem(itemAbsorbedVnum)
				self.__AppendMagicDefenceInfo(absChance)
			
			item.SelectItem(itemAbsorbedVnum)
			for i in range(item.ITEM_APPLY_MAX_NUM):
				(affectType, affectValue) = item.GetAffect(i)
				affectValue = self.CalcSashValue(affectValue, absChance)
				affectString = self.__GetAffectString(affectType, affectValue)
				if affectString and affectValue > 0:
					self.AppendTextLine(affectString, self.GetChangeTextLineColor(affectValue))
				
				item.SelectItem(itemAbsorbedVnum)
			
			item.SelectItem(itemAbsorbedVnum)
			for i in range(player.ATTRIBUTE_SLOT_MAX_NUM):
				type = attrSlot[i][0]
				value = attrSlot[i][1]
				if not value:
					continue
				
				value = self.CalcSashValue(value, absChance)
				affectString = self.__GetAffectString(type, value)
				if affectString and value > 0:
					affectColor = self.__GetAttributeColor(i, value, type)
					self.AppendTextLine(affectString, affectColor)
				
				item.SelectItem(itemAbsorbedVnum)
			
			item.SelectItem(itemVnumAura)
			self.AppendSpace(5)
			self.AppendTextLine(localeInfo.TOOLTIP_ITEM_WEARABLE_JOB, self.NORMAL_COLOR)
			
			item.SelectItem(itemVnumAura)
			flagList = (
						not item.IsAntiFlag(item.ITEM_ANTIFLAG_WARRIOR),
						not item.IsAntiFlag(item.ITEM_ANTIFLAG_ASSASSIN),
						not item.IsAntiFlag(item.ITEM_ANTIFLAG_SURA),
						not item.IsAntiFlag(item.ITEM_ANTIFLAG_SHAMAN)
			)
			flagList += (not item.IsAntiFlag(item.ITEM_ANTIFLAG_WOLFMAN),)
			
			characterNames = ""
			for i in range(self.CHARACTER_COUNT):
				name = self.CHARACTER_NAMES[i]
				flag = flagList[i]
				if flag:
					characterNames += " "
					characterNames += name
			
			textLine = self.AppendTextLine(characterNames, self.NORMAL_COLOR, True)
			textLine.SetFeather()
			
			item.SelectItem(itemVnumAura)
			if item.IsAntiFlag(item.ITEM_ANTIFLAG_MALE):
				textLine = self.AppendTextLine(localeInfo.FOR_FEMALE, self.NORMAL_COLOR, True)
				textLine.SetFeather()
			
			if item.IsAntiFlag(item.ITEM_ANTIFLAG_FEMALE):
				textLine = self.AppendTextLine(localeInfo.FOR_MALE, self.NORMAL_COLOR, True)
				textLine.SetFeather()
			
			self.ShowToolTip()

	def __ShowModelPreviewWidgets(self):
		if self.modelPreviewBoard:
			self.modelPreviewBoard.Show()
		if self.modelPreviewRender:
			self.modelPreviewRender.Show()
		if self.modelPreviewSeparator:
			self.modelPreviewSeparator.Show()
		if self.modelPreviewTextLine:
			self.modelPreviewTextLine.Show()

	def __EnsureModelPreviewWidgets(self, renderTargetIndex):
		if not self.modelPreviewBoard:
			self.modelPreviewBoard = ui.ThinBoard()
			self.modelPreviewBoard.SetParent(self)
			self.modelPreviewBoard.SetSize(190+10, 210+30)
			self.modelPreviewBoard.SetPosition(-202, 0)
		self.modelPreviewBoard.Show()

		if not self.modelPreviewRender:
			self.modelPreviewRender = ui.RenderTarget()
			self.modelPreviewRender.SetParent(self.modelPreviewBoard)
			self.modelPreviewRender.SetSize(194, 216)
			self.modelPreviewRender.SetPosition(3, 21)
			self.modelPreviewRender.SetRenderTarget(renderTargetIndex)
		if not renderTarget.HasTarget(renderTargetIndex):
			return False

		renderTarget.SetBackground(renderTargetIndex, "d:/ymir work/ui/game/myshop_deco/model_view_bg.sub")
		self.modelPreviewRender.Show()

		if not self.modelPreviewSeparator:
			self.modelPreviewSeparator = ui.ImageBox()
			self.modelPreviewSeparator.SetParent(self.modelPreviewBoard)
			self.modelPreviewSeparator.SetPosition(0,0)
			self.modelPreviewSeparator.LoadImage("d:/ymir work/ui/separator_big.tga")
		self.modelPreviewSeparator.Show()

		if not self.modelPreviewTextLine:
			self.modelPreviewTextLine = ui.TextLine()
			self.modelPreviewTextLine.SetParent(self.modelPreviewBoard)
			self.modelPreviewTextLine.SetFontName(localeInfo.UI_DEF_FONT_LARGE + "b")
			self.modelPreviewTextLine.SetOutline(True)
			self.modelPreviewTextLine.SetPosition(0, 3)
			UI_DEF_FONT = "Tahoma:14b"
			self.modelPreviewTextLine.SetFontName(UI_DEF_FONT)
			self.modelPreviewTextLine.SetText(localeInfo.RENDER_TARGET_PREVIEW_ITEM)
			self.modelPreviewTextLine.SetOutline()
			self.modelPreviewTextLine.SetWindowHorizontalAlignCenter()
			self.modelPreviewTextLine.SetHorizontalAlignCenter()
		self.modelPreviewTextLine.Show()

		renderTarget.SetVisibility(renderTargetIndex, True)
		return True

	def __BeginModelPreview(self, previewKey):
		self.modelPreviewRequested = True
		if not self.modelShow:
			self.modelPreviewRequested = False
			return True

		RENDER_TARGET_INDEX = 1
		if not self.__EnsureModelPreviewWidgets(RENDER_TARGET_INDEX):
			self.modelPreviewRequested = False
			return True

		if self.modelPreviewKey == previewKey:
			return True

		self.modelPreviewKey = previewKey
		return False

	def __ModelPreviewOpen(self, Vnum, model, Type=""):
		if self.__BeginModelPreview(("preview", Type, Vnum, model)):
			return
			
		RENDER_TARGET_INDEX = 1

		renderTarget.SetVisibility(RENDER_TARGET_INDEX, True)

		if Type == "monster":
			renderTarget.SelectModel(RENDER_TARGET_INDEX, model)
			return

		if Type == "body" or Type == "hair" or Type == "acce" or Type == "weapon":
			renderTarget.SelectModel(RENDER_TARGET_INDEX, model)
			if Type == "body":
				renderTarget.SetArmor(RENDER_TARGET_INDEX, Vnum)
			elif Type == "hair":
				renderTarget.SetHair(RENDER_TARGET_INDEX, item.GetValue(3))
			elif Type == "acce":
				renderTarget.SetAcce(RENDER_TARGET_INDEX, Vnum)
			elif Type == "weapon":
				renderTarget.SetWeapon(RENDER_TARGET_INDEX, Vnum)
		else:
			renderTarget.SelectModel(RENDER_TARGET_INDEX, Vnum)
			
	def __GetWeaponFromData(self, data):
		"""Get random appropriate weapon from data based on character class"""
		chrModel = player.GetRace()
		chrJob = chr.RaceToJob(chrModel)
		
		weapons = data.weapons
		
		# Handle weapon selection based on character class - ALWAYS RANDOM
		if chrJob == 0:  # Warrior
			# Always random selection between sword and two-handed
			warrRndTypes = ["sword", "twohand"]
			rnd = app.GetRandom(0, 1)
			return weapons.get(warrRndTypes[rnd], 0)
				
		elif chrJob == 1:  # Ninja
			# Always random selection between dagger and bow
			ninjaRndTypes = ["dagger", "bow"]
			rnd = app.GetRandom(0, 1)
			return weapons.get(ninjaRndTypes[rnd], 0)
				
		elif chrJob == 2:  # Sura
			# Always random selection between sword and sura_sword (scythe)
			suraRndTypes = ["sword", "sura_sword"]
			rnd = app.GetRandom(0, 1)
			return weapons.get(suraRndTypes[rnd], 0)
			
		elif chrJob == 3:  # Shaman
			# Always random selection between bell and fan
			shamRndTypes = ["bell", "fan"]
			rnd = app.GetRandom(0, 1)
			return weapons.get(shamRndTypes[rnd], 0)
		
		return 0  # No weapon for unknown class

	def __IsBoxShowModel(self, hairVnum, bodyVnum, acceVnum, model):
		if self.__BeginModelPreview(("box", hairVnum, bodyVnum, acceVnum, model)):
			return

		RENDER_TARGET_INDEX = 1

		renderTarget.SelectModel(RENDER_TARGET_INDEX, model)
		renderTarget.SetArmor(RENDER_TARGET_INDEX, bodyVnum)
		renderTarget.SetHair(RENDER_TARGET_INDEX, hairVnum)
		renderTarget.SetAcce(RENDER_TARGET_INDEX, acceVnum)
		self.__SetWeaponForPreview(RENDER_TARGET_INDEX, 0)

	def __IsBoxShowModel2(self, hairVnum, bodyVnum, weaponVnum, acceVnum, model):
		if self.__BeginModelPreview(("box2", hairVnum, bodyVnum, weaponVnum, acceVnum, model)):
			return

		RENDER_TARGET_INDEX = 1

		# Ustawienie modelu
		renderTarget.SelectModel(RENDER_TARGET_INDEX, model)
		# Ustawienie zbroi
		renderTarget.SetArmor(RENDER_TARGET_INDEX, bodyVnum)
		# Ustawienie fryzury
		renderTarget.SetHair(RENDER_TARGET_INDEX, hairVnum)
		# Ustawienie broni
		renderTarget.SetWeapon(RENDER_TARGET_INDEX, weaponVnum)
		# Ustawienie akcesori?w
		renderTarget.SetAcce(RENDER_TARGET_INDEX, acceVnum)

	def SetRenderOnKey(self, flag):
		self.renderOnKey = flag
		
	def __ModelPreviewClose(self):
		self.rtargetshow = 0
		self.modelPreviewKey = None
		self.modelPreviewRequested = False
		RENDER_TARGET_INDEX = 1

		if self.modelPreviewBoard:
			self.modelPreviewBoard.Hide()
		if self.modelPreviewRender:
			self.modelPreviewRender.Hide()
		if self.modelPreviewSeparator:
			self.modelPreviewSeparator.Hide()
		if self.modelPreviewTextLine:
			self.modelPreviewTextLine.Hide()

		if renderTarget.HasTarget(RENDER_TARGET_INDEX):
			renderTarget.SetVisibility(RENDER_TARGET_INDEX, False)
		# renderTarget.SelectModel(RENDER_TARGET_INDEX, -1)

	def SetModelShow(self, flag):
		self.modelShow = flag

	def HideToolTip(self):
		ToolTip.HideToolTip(self)
		
		self.__ModelPreviewClose()

	def HideToolTipWithoutModelPreview(self):
		ToolTip.HideToolTip(self)

##NEW TOOLTIP
class ToolTipNew(ui.ThinBoardNew):
	TOOL_TIP_WIDTH = 190
	TOOL_TIP_HEIGHT = 3
	TEXT_LINE_HEIGHT = 17
	TITLE_COLOR = grp.GenerateColor(0.9490, 0.9058, 0.7568, 1.0)
	SPECIAL_TITLE_COLOR = grp.GenerateColor(1.0, 0.7843, 0.0, 1.0)
	NORMAL_COLOR = grp.GenerateColor(0.7607, 0.7607, 0.7607, 1.0)
	FONT_COLOR = grp.GenerateColor(0.7607, 0.7607, 0.7607, 1.0)
	POSITIVE_COLOR = grp.GenerateColor(0.5411, 0.7254, 0.5568, 1.0)

	def __init__(self, width = TOOL_TIP_WIDTH, isPickable=False):
		ui.ThinBoardNew.__init__(self, "TOP_MOST")

		if isPickable:
			pass
		else:
			self.AddFlag("not_pick")

		self.AddFlag("float")

		self.followFlag = True
		self.toolTipWidth = width

		self.xPos = -1
		self.yPos = -1

		self.defFontName = localeInfo.UI_DEF_FONT
		self.ClearToolTip()

	def __del__(self):
		ui.ThinBoardNew.__del__(self)

	def ClearToolTip(self):
		self.toolTipHeight = 3
		self.childrenList = []

	def SetFollow(self, flag):
		self.followFlag = flag

	def SetDefaultFontName(self, fontName):
		self.defFontName = fontName

	def ResizeToolTip(self):
		self.SetSize(self.toolTipWidth, self.TOOL_TIP_HEIGHT + self.toolTipHeight)

	def AppendSpace(self, size):
		self.toolTipHeight += size
		self.ResizeToolTip()

	def AppendHorizontalLine(self):

		for i in range(2):
			horizontalLine = ui.Line()
			horizontalLine.SetParent(self)
			horizontalLine.SetPosition(0, self.toolTipHeight + 4 + i)
			horizontalLine.SetWindowHorizontalAlignCenter()
			horizontalLine.SetSize(100, 0)
			horizontalLine.Show()

			if 0 == i:
				horizontalLine.SetColor(0xff555555)
			else:
				horizontalLine.SetColor(0xff000000)

			self.childrenList.append(horizontalLine)

		self.toolTipHeight += 11
		self.ResizeToolTip()

	def AlignHorizonalCenter(self):
		for child in self.childrenList:
			(x, y)=child.GetLocalPosition()
			child.SetPosition(self.toolTipWidth/2, y)

		self.ResizeToolTip()

	def SetTitle(self, text, color = TITLE_COLOR, centerAlign = True):
		textLine = ui.TextLine()
		textLine.SetParent(self)
		TITLE_FONT = "Tahoma:14"
		textLine.SetFontName(TITLE_FONT)
		textLine.SetPackedFontColor(color)
		textLine.SetText(text)
		textLine.SetOutline()
		textLine.SetFeather(False)
		textLine.Show()

		if centerAlign:
			textLine.SetPosition(self.toolTipWidth/2, 5)
			textLine.SetHorizontalAlignCenter()

		else:
			textLine.SetPosition(10, self.toolTipHeight)

		self.childrenList.append(textLine)

		self.toolTipHeight += self.TEXT_LINE_HEIGHT
		self.ResizeToolTip()

		return textLine

	def AppendGreenTextLine(self, text, color = POSITIVE_COLOR, centerAlign = True):
		textLine = ui.TextLine()
		textLine.SetParent(self)
		textLine.SetFontName("Tahoma:12")
		textLine.SetPackedFontColor(color)
		textLine.SetText(text)
		textLine.SetOutline()
		textLine.SetFeather(False)
		textLine.Show()

		if centerAlign:
			textLine.SetPosition(self.toolTipWidth/2, self.toolTipHeight)
			textLine.SetHorizontalAlignCenter()

		else:
			textLine.SetPosition(10, self.toolTipHeight)

		self.childrenList.append(textLine)

		self.toolTipHeight += self.TEXT_LINE_HEIGHT
		self.ResizeToolTip()

		return textLine

	def AppendTextLine(self, text, color = FONT_COLOR, centerAlign = True):
		textLine = ui.TextLine()
		textLine.SetParent(self)
		#textLine.SetFontName(self.defFontName)
		textLine.SetFontName("Tahoma:12")
		textLine.SetPackedFontColor(color)
		textLine.SetText(text)
		textLine.SetOutline()
		textLine.SetFeather(False)
		if app.WJ_MULTI_TEXTLINE:
			textLine.SetLineHeight(self.TEXT_LINE_HEIGHT)

		if centerAlign:
			textLine.SetPosition(self.toolTipWidth / 2, self.toolTipHeight)
			textLine.SetHorizontalAlignCenter()
		else:
			textLine.SetPosition(10, self.toolTipHeight)

		textLine.Show()

		self.childrenList.append(textLine)

		if app.WJ_MULTI_TEXTLINE:
			lineCount = textLine.GetTextLineCount()
			self.toolTipHeight += self.TEXT_LINE_HEIGHT * lineCount
		else:
			self.toolTipHeight += self.TEXT_LINE_HEIGHT

		self.ResizeToolTip()

		return textLine
	
	def SetToolTipPosition(self, x = -1, y = -1):
		self.xPos = x
		self.yPos = y

	def ShowToolTip(self):
		self.SetTop()
		self.Show()

		self.OnUpdate()

	def HideToolTip(self):
		self.Hide()

	def OnUpdate(self):

		if not self.followFlag:
			return

		x = 0
		y = 0
		width = self.GetWidth()
		height = self.toolTipHeight

		if -1 == self.xPos and -1 == self.yPos:

			(mouseX, mouseY) = wndMgr.GetMousePosition()

			if mouseY < wndMgr.GetScreenHeight() - 300:
				y = mouseY + 40
			else:
				y = mouseY - height - 30

			x = mouseX - width // 2

		else:

			x = self.xPos - width // 2
			y = self.yPos - height

		x = max(x, 0)
		y = max(y, 0)
		x = min(x + width // 2, wndMgr.GetScreenWidth() - width // 2) - width // 2
		y = min(y + self.GetHeight(), wndMgr.GetScreenHeight()) - self.GetHeight()

		parentWindow = self.GetParentProxy()
		if parentWindow:
			(gx, gy) = parentWindow.GetGlobalPosition()
			x -= gx
			y -= gy

		self.SetPosition(x, y)
##end

class HyperlinkItemToolTip(ItemToolTip):
	def __init__(self):
		ItemToolTip.__init__(self, isPickable=True)

	def SetHyperlinkItem(self, tokens):
		minTokenCount = 3 + player.METIN_SOCKET_MAX_NUM
		maxTokenCount = minTokenCount + 2 * player.ATTRIBUTE_SLOT_MAX_NUM
		if tokens and len(tokens) >= minTokenCount and len(tokens) <= maxTokenCount:
			head, vnum, flag = tokens[:3]
			itemVnum = int(vnum, 16)
			
			import app
			if app.ENABLE_EXTENDED_SOCKETS:
				metinSlot = [int(metin, 16) for metin in tokens[3:9]]

				rests = tokens[9:]
			else:
				metinSlot = [int(metin, 16) for metin in tokens[3:6]]

				rests = tokens[6:]		
				
			if rests:
				attrSlot = []

				rests.reverse()
				while rests:
					key = int(rests.pop(), 16)
					if rests:
						val = int(rests.pop())
						attrSlot.append((key, val))

				attrSlot += [(0, 0)] * (player.ATTRIBUTE_SLOT_MAX_NUM - len(attrSlot))
			else:
				attrSlot = [(0, 0)] * player.ATTRIBUTE_SLOT_MAX_NUM

			self.ClearToolTip()
			self.AddItemData(itemVnum, metinSlot, attrSlot)

			ItemToolTip.OnUpdate(self)

	def OnUpdate(self):
		pass

	def OnMouseLeftButtonDown(self):
		self.Hide()

class SkillToolTip(ToolTip):

	POINT_NAME_DICT = {
		player.LEVEL : localeInfo.SKILL_TOOLTIP_LEVEL,
		player.IQ : localeInfo.SKILL_TOOLTIP_INT,
	}


	SKILL_TOOL_TIP_WIDTH = 200
	PARTY_SKILL_TOOL_TIP_WIDTH = 340

	PARTY_SKILL_EXPERIENCE_AFFECT_LIST = (	( 2, 2,  10,),
											( 8, 3,  20,),
											(14, 4,  30,),
											(22, 5,  45,),
											(28, 6,  60,),
											(34, 7,  80,),
											(38, 8, 100,), )

	PARTY_SKILL_PLUS_GRADE_AFFECT_LIST = (	( 4, 2, 1, 0,),
											(10, 3, 2, 0,),
											(16, 4, 2, 1,),
											(24, 5, 2, 2,), )

	PARTY_SKILL_ATTACKER_AFFECT_LIST = (	( 36, 3, ),
											( 26, 1, ),
											( 32, 2, ), )

	SKILL_GRADE_NAME = {	player.SKILL_GRADE_MASTER : localeInfo.SKILL_GRADE_NAME_MASTER,
							player.SKILL_GRADE_GRAND_MASTER : localeInfo.SKILL_GRADE_NAME_GRAND_MASTER,
							player.SKILL_GRADE_PERFECT_MASTER : localeInfo.SKILL_GRADE_NAME_PERFECT_MASTER, }

	AFFECT_NAME_DICT =	{
							"HP" : localeInfo.TOOLTIP_SKILL_AFFECT_ATT_POWER,
							"ATT_GRADE" : localeInfo.TOOLTIP_SKILL_AFFECT_ATT_GRADE,
							"DEF_GRADE" : localeInfo.TOOLTIP_SKILL_AFFECT_DEF_GRADE,
							"ATT_SPEED" : localeInfo.TOOLTIP_SKILL_AFFECT_ATT_SPEED,
							"MOV_SPEED" : localeInfo.TOOLTIP_SKILL_AFFECT_MOV_SPEED,
							"DODGE" : localeInfo.TOOLTIP_SKILL_AFFECT_DODGE,
							"RESIST_NORMAL" : localeInfo.TOOLTIP_SKILL_AFFECT_RESIST_NORMAL,
							"REFLECT_MELEE" : localeInfo.TOOLTIP_SKILL_AFFECT_REFLECT_MELEE,
						}
	AFFECT_APPEND_TEXT_DICT =	{
									"DODGE" : "%",
									"RESIST_NORMAL" : "%",
									"REFLECT_MELEE" : "%",
								}

	def __init__(self):
		ToolTip.__init__(self, self.SKILL_TOOL_TIP_WIDTH)
	def __del__(self):
		ToolTip.__del__(self)

	def SetSkill(self, skillIndex, skillLevel = -1):

		if 0 == skillIndex:
			return

		if skill.SKILL_TYPE_GUILD == skill.GetSkillType(skillIndex):

			if self.SKILL_TOOL_TIP_WIDTH != self.toolTipWidth:
				self.toolTipWidth = self.SKILL_TOOL_TIP_WIDTH
				self.ResizeToolTip()

			self.AppendDefaultData(skillIndex)
			self.AppendSkillConditionData(skillIndex)
			self.AppendGuildSkillData(skillIndex, skillLevel)

		else:

			if self.SKILL_TOOL_TIP_WIDTH != self.toolTipWidth:
				self.toolTipWidth = self.SKILL_TOOL_TIP_WIDTH
				self.ResizeToolTip()

			slotIndex = player.GetSkillSlotIndex(skillIndex)
			skillGrade = player.GetSkillGrade(slotIndex)
			skillLevel = player.GetSkillLevel(slotIndex)
			skillCurrentPercentage = player.GetSkillCurrentEfficientPercentage(slotIndex)
			skillNextPercentage = player.GetSkillNextEfficientPercentage(slotIndex)

			self.AppendDefaultData(skillIndex)
			self.AppendSkillConditionData(skillIndex)
			self.AppendSkillDataNew(slotIndex, skillIndex, skillGrade, skillLevel, skillCurrentPercentage, skillNextPercentage)
			self.AppendSkillRequirement(skillIndex, skillLevel)

		self.ShowToolTip()

	def SetSkillNew(self, slotIndex, skillIndex, skillGrade, skillLevel):

		if 0 == skillIndex:
			return

		if player.SKILL_INDEX_TONGSOL == skillIndex:

			slotIndex = player.GetSkillSlotIndex(skillIndex)
			skillLevel = player.GetSkillLevel(slotIndex)

			self.AppendDefaultData(skillIndex)
			self.AppendPartySkillData(skillGrade, skillLevel)

		elif player.SKILL_INDEX_FISHING == skillIndex:
			slotIndex = player.GetSkillSlotIndex(player.SKILL_INDEX_FISHING)
			skillValues = [0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9, 10, 10, 11, 11, 12, 12, 13, 13, 14, 14, 15, 15, 16, 16, 17, 17, 18, 18, 19, 19, 20, 20]
			skillValues2 = [0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9, 10, 10, 11, 11, 12, 12, 13, 13, 14, 14, 15, 15, 16, 16, 17, 17, 18, 18, 19, 19, 20, 20]
			skillValues3 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30]
			skillValues4 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 10, 11, 13, 15]
			skillValues5 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
			skillLevel = player.GetSkillLevel(slotIndex) + [0, 19, 29, 39][player.GetSkillGrade(slotIndex)]
			self.AppendDefaultData(skillIndex)
			self.AppendSpace(2)
			self.AppendTextLine(localeInfo.TOOLTIP_FISHING_SKILL_BONUS_NOW, self.POSITIVE_COLOR)
			self.AppendTextLine(localeInfo.TOOLTIP_FISHING_SKILL_BONUS_BIGGER_FISH % skillValues[skillLevel], self.POSITIVE_COLOR)
			self.AppendTextLine(localeInfo.TOOLTIP_FISHING_SKILL_BONUS_RARE % skillValues2[skillLevel], self.POSITIVE_COLOR)
			self.AppendTextLine(localeInfo.TOOLTIP_FISHING_SKILL_BONUS_YANG % skillValues3[skillLevel], self.POSITIVE_COLOR)
			self.AppendTextLine(localeInfo.TOOLTIP_FISHING_SKILL_BONUS_INSTANT % skillValues4[skillLevel], self.POSITIVE_COLOR)
			self.AppendTextLine(localeInfo.TOOLTIP_FISHING_SKILL_BONUS_POINTS % skillValues5[skillLevel], self.POSITIVE_COLOR)

			if skillLevel+1 <= 40:
				self.AppendSpace(5)
				self.AppendTextLine(localeInfo.TOOLTIP_FISHING_SKILL_BONUS_NEXT, self.NEGATIVE_COLOR)
				self.AppendTextLine(localeInfo.TOOLTIP_FISHING_SKILL_BONUS_BIGGER_FISH % skillValues[skillLevel+1], self.POSITIVE_COLOR)
				self.AppendTextLine(localeInfo.TOOLTIP_FISHING_SKILL_BONUS_RARE % skillValues2[skillLevel+1], self.POSITIVE_COLOR)
				self.AppendTextLine(localeInfo.TOOLTIP_FISHING_SKILL_BONUS_YANG % skillValues3[skillLevel+1], self.POSITIVE_COLOR)
				self.AppendTextLine(localeInfo.TOOLTIP_FISHING_SKILL_BONUS_INSTANT % skillValues4[skillLevel+1], self.POSITIVE_COLOR)
				self.AppendTextLine(localeInfo.TOOLTIP_FISHING_SKILL_BONUS_POINTS % skillValues5[skillLevel+1], self.POSITIVE_COLOR)
			else:
				self.AppendSpace(2)
				self.AppendTextLine(localeInfo.TOOLTIP_FISHING_SKILL_MAX, self.SPECIAL_TITLE_COLOR)

			self.AppendSpace(4)
			myFishCountString = "0"
			count = int(constInfo.MY_FISH_COUNT)
			if count > 0:
				myFishCountString = "{:,}".format(int(count)).replace(",", ".")
			self.AppendTextLine(localeInfo.TOOLTIP_FISHING_FISHED_COUNT % myFishCountString, self.POSITIVE_COLOR)
				
		elif player.SKILL_INDEX_MINING == skillIndex:
			slotIndex = player.GetSkillSlotIndex(player.SKILL_INDEX_MINING)
			skillValues = [0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9, 10, 10, 11, 11, 12, 12, 13, 13, 14, 14, 15, 15, 16, 16, 17, 17, 18, 18, 19, 19, 20, 20]
			skillValues2 = [0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9, 10, 10, 11, 11, 12, 12, 13, 13, 14, 14, 15, 15, 16, 16, 17, 17, 18, 18, 19, 19, 20]
			skillValues3 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
			skillValues4 = [0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 7]
			skillLevel = player.GetSkillLevel(slotIndex) + [0, 19, 29, 39][player.GetSkillGrade(slotIndex)]
			self.AppendDefaultData(skillIndex)
			self.AppendSpace(2)
			self.AppendTextLine(localeInfo.TOOLTIP_MINING_SKILL_BONUS_NOW, self.POSITIVE_COLOR)
			self.AppendTextLine(localeInfo.TOOLTIP_MINING_SKILL_BONUS_ORE % skillValues[skillLevel], self.POSITIVE_COLOR)
			self.AppendTextLine(localeInfo.TOOLTIP_MINING_SKILL_BONUS_MORE_ORE % skillValues2[skillLevel], self.POSITIVE_COLOR)
			self.AppendTextLine(localeInfo.TOOLTIP_MINING_SKILL_BONUS_TIME % skillValues3[skillLevel], self.POSITIVE_COLOR)
			self.AppendTextLine(localeInfo.TOOLTIP_MINING_SKILL_BONUS_RELIC % skillValues4[skillLevel], self.POSITIVE_COLOR)

			if skillLevel+1 <= 40:
				self.AppendSpace(5)
				self.AppendTextLine(localeInfo.TOOLTIP_MINING_SKILL_BONUS_NEXT, self.NEGATIVE_COLOR)
				self.AppendTextLine(localeInfo.TOOLTIP_MINING_SKILL_BONUS_ORE % skillValues[skillLevel+1], self.POSITIVE_COLOR)
				self.AppendTextLine(localeInfo.TOOLTIP_MINING_SKILL_BONUS_MORE_ORE % skillValues2[skillLevel+1], self.POSITIVE_COLOR)
				self.AppendTextLine(localeInfo.TOOLTIP_MINING_SKILL_BONUS_TIME % skillValues3[skillLevel+1], self.POSITIVE_COLOR)
				self.AppendTextLine(localeInfo.TOOLTIP_MINING_SKILL_BONUS_RELIC % skillValues4[skillLevel+1], self.POSITIVE_COLOR)
			else:
				self.AppendSpace(2)
				self.AppendTextLine(localeInfo.TOOLTIP_MINING_SKILL_MAX, self.SPECIAL_TITLE_COLOR)

			self.AppendSpace(4)
			myOreCountString = "0"
			count = int(constInfo.MY_ORE_COUNT)
			if count > 0:
				myOreCountString = "{:,}".format(int(count)).replace(",", ".")
			self.AppendTextLine(localeInfo.TOOLTIP_MINING_MINED_COUNT % myOreCountString, self.POSITIVE_COLOR)

		elif player.SKILL_INDEX_RIDING == skillIndex:

			slotIndex = player.GetSkillSlotIndex(skillIndex)
			self.AppendSupportSkillDefaultData(skillIndex, skillGrade, skillLevel, 30)

		elif player.SKILL_INDEX_SUMMON == skillIndex:

			maxLevel = 10

			self.ClearToolTip()
			self.__SetSkillTitle(skillIndex, skillGrade)

			## Description
			description = skill.GetSkillDescription(skillIndex)
			self.AppendDescription(description, 25)

			if skillLevel == 10:
				self.AppendSpace(5)
				self.AppendTextLine(localeInfo.TOOLTIP_SKILL_LEVEL_MASTER % (skillLevel), self.NORMAL_COLOR)
				self.AppendTextLine(localeInfo.SKILL_SUMMON_DESCRIPTION % (skillLevel*10), self.NORMAL_COLOR)

			else:
				self.AppendSpace(5)
				self.AppendTextLine(localeInfo.TOOLTIP_SKILL_LEVEL % (skillLevel), self.NORMAL_COLOR)
				self.__AppendSummonDescription(skillLevel, self.NORMAL_COLOR)

				self.AppendSpace(5)
				self.AppendTextLine(localeInfo.TOOLTIP_SKILL_LEVEL % (skillLevel+1), self.NEGATIVE_COLOR)
				self.__AppendSummonDescription(skillLevel+1, self.NEGATIVE_COLOR)

		elif skill.SKILL_TYPE_GUILD == skill.GetSkillType(skillIndex):

			if self.SKILL_TOOL_TIP_WIDTH != self.toolTipWidth:
				self.toolTipWidth = self.SKILL_TOOL_TIP_WIDTH
				self.ResizeToolTip()

			self.AppendDefaultData(skillIndex)
			self.AppendSkillConditionData(skillIndex)
			self.AppendGuildSkillData(skillIndex, skillLevel)

		else:

			if self.SKILL_TOOL_TIP_WIDTH != self.toolTipWidth:
				self.toolTipWidth = self.SKILL_TOOL_TIP_WIDTH
				self.ResizeToolTip()

			slotIndex = player.GetSkillSlotIndex(skillIndex)

			skillCurrentPercentage = player.GetSkillCurrentEfficientPercentage(slotIndex)
			skillNextPercentage = player.GetSkillNextEfficientPercentage(slotIndex)

			self.AppendDefaultData(skillIndex, skillGrade)
			self.AppendSkillConditionData(skillIndex)
			self.AppendSkillDataNew(slotIndex, skillIndex, skillGrade, skillLevel, skillCurrentPercentage, skillNextPercentage)
			self.AppendSkillRequirement(skillIndex, skillLevel)

		self.ShowToolTip()

	def __SetSkillTitle(self, skillIndex, skillGrade):
		if chr.IsGameMaster(player.GetMainCharacterIndex()):
			self.AppendTextLine("[ID: %d" % skillIndex + "]")
			self.AppendSpace(5)
		self.SetTitle(skill.GetSkillName(skillIndex, skillGrade))
		self.__AppendSkillGradeName(skillIndex, skillGrade)

	def __AppendSkillGradeName(self, skillIndex, skillGrade):
		if skillGrade in self.SKILL_GRADE_NAME:
			self.AppendSpace(5)
			self.AppendTextLine(self.SKILL_GRADE_NAME[skillGrade] % (skill.GetSkillName(skillIndex, 0)), self.CAN_LEVEL_UP_COLOR)

	def SetSkillOnlyName(self, slotIndex, skillIndex, skillGrade):
		if 0 == skillIndex:
			return

		slotIndex = player.GetSkillSlotIndex(skillIndex)

		self.toolTipWidth = self.SKILL_TOOL_TIP_WIDTH
		self.ResizeToolTip()

		self.ClearToolTip()
		self.__SetSkillTitle(skillIndex, skillGrade)
		self.AppendDefaultData(skillIndex, skillGrade)
		self.AppendSkillConditionData(skillIndex)
		self.ShowToolTip()

	def AppendDefaultData(self, skillIndex, skillGrade = 0):
		self.ClearToolTip()
		self.__SetSkillTitle(skillIndex, skillGrade)

		## Level Limit
		levelLimit = skill.GetSkillLevelLimit(skillIndex)
		if levelLimit > 0:

			color = self.NORMAL_COLOR
			if player.GetStatus(player.LEVEL) < levelLimit:
				color = self.NEGATIVE_COLOR

			self.AppendSpace(5)
			self.AppendTextLine(localeInfo.TOOLTIP_ITEM_LIMIT_LEVEL % (levelLimit), color)

		## Description
		description = skill.GetSkillDescription(skillIndex)
		self.AppendDescription(description, 25)

	if app.ENABLE_ASLAN_BUFF_NPC_SYSTEM:
		def AppendBuffDefaultData(self, skillIndex, skillGrade = 0):
			self.ClearToolTip()
			self.SetTitle(skill.GetSkillName(skillIndex, skillGrade))

			## Level Limit
			levelLimit = skill.GetSkillLevelLimit(skillIndex)
			if levelLimit > 0:

				color = self.NORMAL_COLOR
				if player.GetStatus(player.LEVEL) < levelLimit:
					color = self.NEGATIVE_COLOR

				self.AppendSpace(5)
				self.AppendTextLine(localeInfo.TOOLTIP_ITEM_LIMIT_LEVEL % (levelLimit), color)

			# ## Description
			# description = skill.GetSkillDescription(skillIndex)
			# self.AppendDescription(description, 25)

	def AppendSupportSkillDefaultData(self, skillIndex, skillGrade, skillLevel, maxLevel):
		self.ClearToolTip()
		self.__SetSkillTitle(skillIndex, skillGrade)

		## Description
		description = skill.GetSkillDescription(skillIndex)
		self.AppendDescription(description, 25)

		if 1 == skillGrade:
			skillLevel += 19
		elif 2 == skillGrade:
			skillLevel += 29
		elif 3 == skillGrade:
			skillLevel = 40

		# Jezdziectwo (skill 130) - progi bonusow jak na nostalgii.
		# Od 30 poziomu do bonusu obrazen dochodzi odpornosc.
		if skillIndex == SKILL_HORSE_RIDING:
			if 10 <= skillLevel <= 19:
				self.AppendTextLine(localeInfo.TOOLTIP_SKILL_LEVEL_HORSE_BONUS_FIRST, self.CONDITION_COLOR)
			elif 20 <= skillLevel <= 29:
				self.AppendTextLine(localeInfo.TOOLTIP_SKILL_LEVEL_HORSE_BONUS_SECOND, self.CONDITION_COLOR)
			elif skillLevel >= 30:
				self.AppendTextLine(localeInfo.TOOLTIP_SKILL_LEVEL_HORSE_BONUS_SECOND, self.CONDITION_COLOR)
				self.AppendTextLine(localeInfo.TOOLTIP_SKILL_LEVEL_HORSE_BONUS_RESIST, self.CONDITION_COLOR)

		self.AppendSpace(5)
		self.AppendTextLine(localeInfo.TOOLTIP_SKILL_LEVEL_WITH_MAX % (skillLevel, maxLevel), self.NORMAL_COLOR)

	def AppendSkillConditionData(self, skillIndex):
		conditionDataCount = skill.GetSkillConditionDescriptionCount(skillIndex)
		if conditionDataCount > 0:
			self.AppendSpace(5)
			for i in range(conditionDataCount):
				self.AppendTextLine(skill.GetSkillConditionDescription(skillIndex, i), self.CONDITION_COLOR)

	def AppendGuildSkillData(self, skillIndex, skillLevel):
		skillMaxLevel = 7
		skillCurrentPercentage = float(skillLevel) / float(skillMaxLevel)
		skillNextPercentage = float(skillLevel+1) / float(skillMaxLevel)
		## Current Level
		if skillLevel > 0:
			if self.HasSkillLevelDescription(skillIndex, skillLevel):
				self.AppendSpace(5)
				if skillLevel == skillMaxLevel:
					self.AppendTextLine(localeInfo.TOOLTIP_SKILL_LEVEL_MASTER % (skillLevel), self.NORMAL_COLOR)
				else:
					self.AppendTextLine(localeInfo.TOOLTIP_SKILL_LEVEL % (skillLevel), self.NORMAL_COLOR)

				#####

				for i in range(skill.GetSkillAffectDescriptionCount(skillIndex)):
					self.AppendTextLine(skill.GetSkillAffectDescription(skillIndex, i, skillCurrentPercentage), self.ENABLE_COLOR)

				## Cooltime
				coolTime = skill.GetSkillCoolTime(skillIndex, skillCurrentPercentage)
				if coolTime > 0:
					self.AppendTextLine(localeInfo.TOOLTIP_SKILL_COOL_TIME + str(coolTime), self.ENABLE_COLOR)

				## SP
				needGSP = skill.GetSkillNeedSP(skillIndex, skillCurrentPercentage)
				if needGSP > 0:
					self.AppendTextLine(localeInfo.TOOLTIP_NEED_GSP % (needGSP), self.ENABLE_COLOR)

		## Next Level
		if skillLevel < skillMaxLevel:
			if self.HasSkillLevelDescription(skillIndex, skillLevel+1):
				self.AppendSpace(5)
				self.AppendTextLine(localeInfo.TOOLTIP_NEXT_SKILL_LEVEL_1 % (skillLevel+1, skillMaxLevel), self.DISABLE_COLOR)

				#####

				for i in range(skill.GetSkillAffectDescriptionCount(skillIndex)):
					self.AppendTextLine(skill.GetSkillAffectDescription(skillIndex, i, skillNextPercentage), self.DISABLE_COLOR)

				## Cooltime
				coolTime = skill.GetSkillCoolTime(skillIndex, skillNextPercentage)
				if coolTime > 0:
					self.AppendTextLine(localeInfo.TOOLTIP_SKILL_COOL_TIME + str(coolTime), self.DISABLE_COLOR)

				## SP
				needGSP = skill.GetSkillNeedSP(skillIndex, skillNextPercentage)
				if needGSP > 0:
					self.AppendTextLine(localeInfo.TOOLTIP_NEED_GSP % (needGSP), self.DISABLE_COLOR)

	def AppendSkillDataNew(self, slotIndex, skillIndex, skillGrade, skillLevel, skillCurrentPercentage, skillNextPercentage):

		self.skillMaxLevelStartDict = { 0 : 17, 1 : 7, 2 : 10, }
		self.skillMaxLevelEndDict = { 0 : 20, 1 : 10, 2 : 10, }

		skillLevelUpPoint = 1
		realSkillGrade = player.GetSkillGrade(slotIndex)
		skillMaxLevelStart = self.skillMaxLevelStartDict.get(realSkillGrade, 15)
		skillMaxLevelEnd = self.skillMaxLevelEndDict.get(realSkillGrade, 20)

		## Current Level
		if skillLevel > 0:
			if self.HasSkillLevelDescription(skillIndex, skillLevel):
				self.AppendSpace(5)
				if skillGrade == skill.SKILL_GRADE_COUNT:
					pass
				elif skillLevel == skillMaxLevelEnd:
					self.AppendTextLine(localeInfo.TOOLTIP_SKILL_LEVEL_MASTER % (skillLevel), self.NORMAL_COLOR)
				else:
					self.AppendTextLine(localeInfo.TOOLTIP_SKILL_LEVEL % (skillLevel), self.NORMAL_COLOR)
				self.AppendSkillLevelDescriptionNew(skillIndex, skillCurrentPercentage, self.ENABLE_COLOR)

		## Next Level
		if skillGrade != skill.SKILL_GRADE_COUNT:
			if skillLevel < skillMaxLevelEnd:
				if self.HasSkillLevelDescription(skillIndex, skillLevel+skillLevelUpPoint):
					self.AppendSpace(5)
					if skillIndex == 141 or skillIndex == 142:
						self.AppendTextLine(localeInfo.TOOLTIP_NEXT_SKILL_LEVEL_3 % (skillLevel+1), self.DISABLE_COLOR)
					else:
						self.AppendTextLine(localeInfo.TOOLTIP_NEXT_SKILL_LEVEL_1 % (skillLevel+1, skillMaxLevelEnd), self.DISABLE_COLOR)
					self.AppendSkillLevelDescriptionNew(skillIndex, skillNextPercentage, self.DISABLE_COLOR)

		if skillIndex == 129:
			self.AppendSpace(5)
			if not skillGrade == 3:
				self.AppendTextLine(localeInfo.TOOLTIP_SKILL_LEVEL % (skillLevel), self.NORMAL_COLOR)

			self.AppendTextLine(localeInfo.SKILL_DATA_129_DESC_1.format(POLY_DMG_VAL[skillGrade][skillLevel]))

			if not skillGrade == 3:
				self.AppendSpace(5)
				self.AppendTextLine(localeInfo.TOOLTIP_NEXT_SKILL_LEVEL_1 % (skillLevel+1, 40), self.DISABLE_COLOR)
				if skillLevel == 19:					
					self.AppendTextLine(localeInfo.SKILL_DATA_129_DESC_1.format(POLY_DMG_VAL[1][0]))

				elif skillGrade == 1 and skillLevel == 10:
					self.AppendTextLine(localeInfo.SKILL_DATA_129_DESC_1.format(POLY_DMG_VAL[2][0]))
				elif skillGrade == 2 and skillLevel == 10:
					self.AppendTextLine(localeInfo.SKILL_DATA_129_DESC_1.format(POLY_DMG_VAL[3][0]))
				else:
					self.AppendTextLine(localeInfo.SKILL_DATA_129_DESC_1.format(POLY_DMG_VAL[skillGrade][skillLevel+1]))

			elif skillGrade == 3:
				self.AppendSpace(5)
				self.AppendTextLine(localeInfo.SKILLS_MAX_LEVEL, self.POSITIVE_COLOR)


	if app.ENABLE_ASLAN_BUFF_NPC_SYSTEM:
		def SetSkillBuffNPC(self, slotIndex, skillIndex, skillGrade, skillLevel, curSkillPower, nextSkillPower, intPoints):

			if 0 == skillIndex:
				return

			self.AppendBuffDefaultData(skillIndex, skillGrade)
			# self.AppendSkillConditionData(skillIndex)
			self.AppendSkillDataBuffNPC(slotIndex, skillIndex, skillGrade, skillLevel, curSkillPower, nextSkillPower, intPoints)
			self.AppendSkillRequirement(skillIndex, skillLevel)

			self.ShowToolTip()
			
		def AppendSkillDataBuffNPC(self, slotIndex, skillIndex, skillGrade, skillLevel, skillCurrentPercentage, skillNextPercentage, intPoints):
			self.skillMaxLevelStartDict = { 0 : 17, 1 : 7, 2 : 10, }
			self.skillMaxLevelEndDict = { 0 : 20, 1 : 10, 2 : 10, }

			skillLevelUpPoint = 1
			realSkillGrade = player.GetSkillGrade(slotIndex)
			skillMaxLevelStart = self.skillMaxLevelStartDict.get(realSkillGrade, 15)
			skillMaxLevelEnd = self.skillMaxLevelEndDict.get(realSkillGrade, 20)

			if skillGrade == skill.SKILL_GRADE_COUNT:
				self.AppendTextLine(localeInfo.SKILLS_MAX_LEVEL, self.POSITIVE_COLOR)
			## Current Level
			if skillLevel > 0:
				self.AppendTextLine("|cFF999999_______________________")
				if self.HasSkillLevelDescription(skillIndex, skillLevel):
					self.AppendSpace(5)
					if skillGrade == skill.SKILL_GRADE_COUNT:
						pass
					elif skillLevel == skillMaxLevelEnd:
						self.AppendTextLine(localeInfo.TOOLTIP_SKILL_LEVEL_MASTER % (skillLevel), self.NORMAL_COLOR)
					else:
						self.AppendTextLine(localeInfo.TOOLTIP_SKILL_LEVEL % (skillLevel), self.NORMAL_COLOR)
					self.AppendSkillLevelDescriptionBuffNPC(skillIndex, skillCurrentPercentage, self.ENABLE_COLOR, intPoints)

			## Next Level
			if skillGrade != skill.SKILL_GRADE_COUNT:
				if skillLevel < skillMaxLevelEnd:
					self.AppendTextLine("|cFF999999_______________________")
					if self.HasSkillLevelDescription(skillIndex, skillLevel+skillLevelUpPoint):
						self.AppendSpace(5)
						if skillIndex == 141 or skillIndex == 142:
							self.AppendTextLine(localeInfo.TOOLTIP_NEXT_SKILL_LEVEL_3 % (skillLevel+1), self.DISABLE_COLOR)
						else:
							self.AppendTextLine(localeInfo.TOOLTIP_NEXT_SKILL_LEVEL_1 % (skillLevel+1, skillMaxLevelEnd), self.DISABLE_COLOR)

						self.AppendSkillLevelDescriptionBuffNPC(skillIndex, skillNextPercentage, self.DISABLE_COLOR, intPoints)
					

		def AppendSkillLevelDescriptionBuffNPC(self, skillIndex, skillPercentage, color, intPoints):

			affectDataCount = skill.GetNewAffectDataCount(skillIndex)
			
			for i in range(skill.GetSkillAffectDescriptionCount(skillIndex)):
				if skillIndex == 94:
					self.AppendTextLine(localeInfo.BUFF_SKILL_LEVEL_DESC_1.format(skill.GetBuffNPCSkillAffectDescription(skillIndex, i, skillPercentage, intPoints)), color)
					self.AppendSpace(5)
				elif skillIndex == 96:
					self.AppendTextLine(localeInfo.BUFF_SKILL_CRIT_CHANCE.format(skill.GetBuffNPCSkillAffectDescription(skillIndex, i, skillPercentage, intPoints)), color)
					self.AppendSpace(5)
				else:
					self.AppendTextLine(localeInfo.BUFF_SKILL_ATTACK_VALUE.format(skill.GetBuffNPCSkillAffectDescription(skillIndex, i, skillPercentage, intPoints)), color)
					self.AppendSpace(5)

			duration = skill.GetDuration(skillIndex, skillPercentage)
			if duration > 0:
				self.AppendTextLine(localeInfo.TOOLTIP_SKILL_DURATION % (duration), color)

			# coolTime = skill.GetSkillCoolTime(skillIndex, skillPercentage)
			# if coolTime > 0:
			# 	self.AppendTextLine(localeInfo.TOOLTIP_SKILL_COOL_TIME + str(coolTime), color)

	def AppendSkillLevelDescriptionNew(self, skillIndex, skillPercentage, color):

		affectDataCount = skill.GetNewAffectDataCount(skillIndex)
		if affectDataCount > 0:
			for i in range(affectDataCount):
				type, minValue, maxValue = skill.GetNewAffectData(skillIndex, i, skillPercentage)

				if type not in self.AFFECT_NAME_DICT:
					continue

				minValue = int(minValue)
				maxValue = int(maxValue)
				affectText = self.AFFECT_NAME_DICT[type]

				if "HP" == type:
					if minValue < 0 and maxValue < 0:
						minValue *= -1
						maxValue *= -1

					else:
						affectText = localeInfo.TOOLTIP_SKILL_AFFECT_HEAL

				affectText += str(minValue)
				if minValue != maxValue:
					affectText += " - " + str(maxValue)
				affectText += self.AFFECT_APPEND_TEXT_DICT.get(type, "")

				#import debugInfo
				#if debugInfo.IsDebugMode():
				#	affectText = "!!" + affectText

				self.AppendTextLine(affectText, color)

		else:
			for i in range(skill.GetSkillAffectDescriptionCount(skillIndex)):
				self.AppendTextLine(skill.GetSkillAffectDescription(skillIndex, i, skillPercentage), color)


		## Duration
		duration = skill.GetDuration(skillIndex, skillPercentage)
		if duration > 0:
			self.AppendTextLine(localeInfo.TOOLTIP_SKILL_DURATION % (duration), color)

		## Cooltime
		coolTime = skill.GetSkillCoolTime(skillIndex, skillPercentage)
		if coolTime > 0:
			self.AppendTextLine(localeInfo.TOOLTIP_SKILL_COOL_TIME + str(coolTime), color)

		## SP
		needSP = skill.GetSkillNeedSP(skillIndex, skillPercentage)
		if needSP != 0:
			continuationSP = skill.GetSkillContinuationSP(skillIndex, skillPercentage)

			if skill.IsUseHPSkill(skillIndex):
				self.AppendNeedHP(needSP, continuationSP, color)
			else:
				self.AppendNeedSP(needSP, continuationSP, color)

	def AppendSkillRequirement(self, skillIndex, skillLevel):

		skillMaxLevel = skill.GetSkillMaxLevel(skillIndex)

		if skillLevel >= skillMaxLevel:
			return

		isAppendHorizontalLine = False

		## Requirement
		if skill.IsSkillRequirement(skillIndex):

			if not isAppendHorizontalLine:
				isAppendHorizontalLine = True
				self.AppendHorizontalLine()

			requireSkillName, requireSkillLevel = skill.GetSkillRequirementData(skillIndex)

			color = self.CANNOT_LEVEL_UP_COLOR
			if skill.CheckRequirementSueccess(skillIndex):
				color = self.CAN_LEVEL_UP_COLOR
			self.AppendTextLine(localeInfo.TOOLTIP_REQUIREMENT_SKILL_LEVEL % (requireSkillName, requireSkillLevel), color)

		## Require Stat
		requireStatCount = skill.GetSkillRequireStatCount(skillIndex)
		if requireStatCount > 0:

			for i in range(requireStatCount):
				type, level = skill.GetSkillRequireStatData(skillIndex, i)
				if type in self.POINT_NAME_DICT:

					if not isAppendHorizontalLine:
						isAppendHorizontalLine = True
						self.AppendHorizontalLine()

					name = self.POINT_NAME_DICT[type]
					color = self.CANNOT_LEVEL_UP_COLOR
					if player.GetStatus(type) >= level:
						color = self.CAN_LEVEL_UP_COLOR
					self.AppendTextLine(localeInfo.TOOLTIP_REQUIREMENT_STAT_LEVEL % (name, level), color)

	def HasSkillLevelDescription(self, skillIndex, skillLevel):
		if skill.GetSkillAffectDescriptionCount(skillIndex) > 0:
			return True
		if skill.GetSkillCoolTime(skillIndex, skillLevel) > 0:
			return True
		if skill.GetSkillNeedSP(skillIndex, skillLevel) > 0:
			return True

		return False

	def AppendMasterAffectDescription(self, index, desc, color):
		self.AppendTextLine(desc, color)

	def AppendNextAffectDescription(self, index, desc):
		self.AppendTextLine(desc, self.DISABLE_COLOR)

	def AppendNeedHP(self, needSP, continuationSP, color):

		self.AppendTextLine(localeInfo.TOOLTIP_NEED_HP % (needSP), color)

		if continuationSP > 0:
			self.AppendTextLine(localeInfo.TOOLTIP_NEED_HP_PER_SEC % (continuationSP), color)

	def AppendNeedSP(self, needSP, continuationSP, color):

		if -1 == needSP:
			self.AppendTextLine(localeInfo.TOOLTIP_NEED_ALL_SP, color)

		else:
			self.AppendTextLine(localeInfo.TOOLTIP_NEED_SP % (needSP), color)

		if continuationSP > 0:
			self.AppendTextLine(localeInfo.TOOLTIP_NEED_SP_PER_SEC % (continuationSP), color)

	def AppendPartySkillData(self, skillGrade, skillLevel):
		# @fixme008 BEGIN
		def comma_fix(vl):
			return vl.replace("%,0f", "%.0f")
		# @fixme008 END

		if 1 == skillGrade:
			skillLevel += 19
		elif 2 == skillGrade:
			skillLevel += 29
		elif 3 == skillGrade:
			skillLevel =  40

		if skillLevel <= 0:
			return

		skillIndex = player.SKILL_INDEX_TONGSOL
		slotIndex = player.GetSkillSlotIndex(skillIndex)
		skillPower = player.GetSkillCurrentEfficientPercentage(slotIndex)
		k = skillPower # @fixme008
		self.AppendSpace(5)
		self.AutoAppendTextLine(localeInfo.TOOLTIP_PARTY_SKILL_LEVEL % skillLevel, self.NORMAL_COLOR)

		# @fixme008 BEGIN
		if skillLevel>=10:
			self.AutoAppendTextLine(comma_fix(localeInfo.PARTY_SKILL_ATTACKER) % chop( 10 + 60 * k ))

		if skillLevel>=20:
			self.AutoAppendTextLine(comma_fix(localeInfo.PARTY_SKILL_BERSERKER) 	% chop(1 + 5 * k))
			self.AutoAppendTextLine(comma_fix(localeInfo.PARTY_SKILL_TANKER) 	% chop(50 + 1450 * k))

		if skillLevel>=25:
			self.AutoAppendTextLine(comma_fix(localeInfo.PARTY_SKILL_BUFFER) % chop(5 + 45 * k ))

		if skillLevel>=35:
			self.AutoAppendTextLine(comma_fix(localeInfo.PARTY_SKILL_SKILL_MASTER) % chop(25 + 600 * k ))

		if skillLevel>=40:
			self.AutoAppendTextLine(comma_fix(localeInfo.PARTY_SKILL_DEFENDER) % chop( 5 + 30 * k ))
		# @fixme008 END

		self.AlignHorizonalCenter()

	def __AppendSummonDescription(self, skillLevel, color):
		if skillLevel > 1:
			self.AppendTextLine(localeInfo.SKILL_SUMMON_DESCRIPTION % (skillLevel * 10), color)
		elif 1 == skillLevel:
			self.AppendTextLine(localeInfo.SKILL_SUMMON_DESCRIPTION % (15), color)
		elif 0 == skillLevel:
			self.AppendTextLine(localeInfo.SKILL_SUMMON_DESCRIPTION % (10), color)

_instanceItemToolTip = None

def GetItemToolTipInstance():
	global _instanceItemToolTip

	if not _instanceItemToolTip:
		SetItemToolTipInstance(ItemToolTip())

	return _instanceItemToolTip

def SetItemToolTipInstance(instance):
	global _instanceItemToolTip

	if _instanceItemToolTip:
		del _instanceItemToolTip

	_instanceItemToolTip = instance
