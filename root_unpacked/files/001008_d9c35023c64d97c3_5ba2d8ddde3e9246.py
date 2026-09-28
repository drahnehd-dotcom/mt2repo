import app
import constInfo

AUTOBAN_QUIZ_ANSWER = "ANSWER"
AUTOBAN_QUIZ_REFRESH = "REFRESH"
AUTOBAN_QUIZ_REST_TIME = "REST_TIME"

OPTION_SHADOW = "SHADOW"

CODEPAGE = str(app.GetDefaultCodePage())
name = app.GetLocalePath()

def LoadLocaleFile(srcFileName, localeDict):
	localeDict["CUBE_INFO_TITLE"] = "Recipe"
	localeDict["CUBE_REQUIRE_MATERIAL"] = "Requirements"
	localeDict["CUBE_REQUIRE_MATERIAL_OR"] = "or"

	try:
		lines = open(srcFileName, "r").readlines()
	except IOError:
		import dbg
		dbg.LogBox("LoadUIScriptLocaleError(%(srcFileName)s)" % locals())
		pass

	for line in lines:
		tokens = line[:-1].split("\t")

		if len(tokens) >= 2:
			localeDict[tokens[0]] = tokens[1]

		else:
			print(len(tokens), lines.index(line), line
)

import re
from decimal import Decimal
def ConvertKKK(number, divisor, KKKType):
	convertedNum = Decimal(number) / Decimal(divisor)
	convertedNum = format(convertedNum.quantize(Decimal("0.001")).normalize(), "f")
	return "%s%s" % (str(convertedNum), KKKType)
	
def NumberToKKK(number):
	number = int(number)
	trilion = int(10**15)
	biolion = int(10**12)
	mld = int(10**9)
	mio = int(10**6)
	ths = int(10**3)

	if number >= trilion:
		return ConvertKKK(number, trilion, "T")

	elif number >= biolion:
		return ConvertKKK(number, biolion, "B")

	elif number >= mld:
		return ConvertKKK(number, mld, "kkk")

	elif number >= mio:
		return ConvertKKK(number, mio, "kk")

	elif number >= ths:
		return ConvertKKK(number, ths, "k")

	return ConvertKKK(number, 1, "")

ITEM_NAMES = "%s/item_names.txt" % (name)
itemNamesDict = {}
for line in open(ITEM_NAMES, 'r'):
	split = line.split('\t')
	if len(split) == 2:
		itemNamesDict[int(split[0])] = split[1].replace("\r", "").replace("\n", "")
		
def FindItemName(vnum):
	if vnum in itemNamesDict:
		return itemNamesDict[vnum]
	else:
		return "Noname"

def RemoveDiacritic(text):
	text = str(text)
	charList = {
		"ě" : "e",
		"Ě" : "e",
		"š" : "s",
		"Š" : "s",
		"č" : "c",
		"Č" : "c",
		"ř" : "r",
		"Ř" : "r",
		"ž" : "z",
		"Ž" : "z",
		"ý" : "y",
		"Ý" : "y",
		"á" : "a",
		"Á" : "a",
		"í" : "i",
		"Í" : "i",
		"é" : "e",
		"É" : "e",
		"ď" : "d",
		"Ď" : "d",
		"ť" : "t",
		"Ť" : "t",
		"ú" : "u",
		"Ú" : "u",
		"ů" : "u",
		"Ů" : "u",
		"Ó" : "o",
		"ó" : "o",
		"Ň" : "n",
		"ň" : "n",
	}

	for key, value in charList.items():
		text = text.replace(key, value)

	return text


LOCALE_UISCRIPT_PATH = "locale/shared/ui/"
LOGIN_PATH = "%s/ui/login/" % (name)
EMPIRE_PATH = "locale/shared/ui/empire/"
GUILD_PATH = "locale/shared/ui/guild/"
SELECT_PATH = "%s/ui/select/" % (name)
WINDOWS_PATH = "locale/shared/ui/windows/"
MAPNAME_PATH = "%s/ui/mapname/" % (name)

LOCALE_INTERFACE_FILE_NAME = "kowal/locale_interface.txt"
CARDS_DESC = "kowal/mini_game_okey_desc.txt"

LOCALE_INTERFACE_FILE_NAME = "%s/locale_interface.txt" % (name)
LOCALE_INTERFACE2 = "%s/locale_interface_new.txt" % (name)
LoadLocaleFile(LOCALE_INTERFACE_FILE_NAME, locals())
LoadLocaleFile(LOCALE_INTERFACE2, locals())
if constInfo.ENABLE_LOAD_EX_DATA:
	LoadLocaleFile("locale/ex/locale_interface_ex.txt", locals())
