import app
import re

SERVER_NAME = "Kowal" ''' app.GetExecutableName().replace('.exe', '').lower()'''

SAFEBOX_OPENED = False
# Kosz (RemoveItemDialog) otwarty - tooltip pokazuje wtedy skrot shift+PPM
REMOVE_ITEM_OPENED = False

SERVER_PATH = "{}".format(SERVER_NAME)

ASSETS_PATH = "assets/{}/".format(SERVER_NAME)

def GetServerScriptPath(script_path):
    """
    Get server-specific script path
    Args:
        script_path: relative script path (e.g., "ui/createcharacterwindow.py")
    Returns:
        server-specific path (e.g., "servername/ui/createcharacterwindow.py")
    """
    return "{}/{}".format(SERVER_PATH, script_path)
    

ENABLE_UI_DEBUG_WINDOW = False
itemRemoveGrid = []
listRemoveItem = []

CLIENT_VERSION = 45
if app.ENABLE_SKILL_SELECT_FEATURE:
	ARE_ENABLED_6TH_SKILLS = 0
	
MOUNT_LEVEL = 0

BOTCONTROL_TIME = 450

MY_ORE_COUNT = 0
MY_FISH_COUNT = 0

if app.ENABLE_EXTRABONUS_SYSTEM:
	RUNE_EXTRABONUS_VALUE = 20  # zachowane (martwe) - uitooltip go uzywa; system Run usuniety
	if app.ENABLE_EXTRABONUS_SYSTEM:
		PET_EXTRABONUS_VALUE = 20

if app.TAKE_LEGEND_DAMAGE_BOARD_SYSTEM:
	LEGEND_DAMAGE_DATA = {
		"NAME": [None] * 15,
		"LEVEL": [None] * 15,
		"RACE": [None] * 15,
		"EMPIRE": [None] * 15,
		"DAMAGE": [None] * 15
	}

LAST_CHESTINFO_VNUM = 0
EXTENDED_INVENTORY_IS_OPEN = 0
# Note: EXTENDED_INVENTORY_AUTO_USE now stored in registry via settings.py
CHESTDROP_INFO_IS_OPEN = 0

# Note: REMEMBER_* settings now stored in registry via settings.py
LASTPAGE = 0

ANTY_EXP_STATUS = 2

# Note: Tooltip settings now stored in registry via settings.py

if app.ENABLE_AUTO_SHOUT:
	AUTO_SHOUT_ACTIVATED = 0
	SHOUT_PER_SECOND = 15
	LAST_SHOUT_MESSAGE = ""

DragonSoulPageIndex = 0
DragonSoulInvIndex = 0
IS_DRAGON_SOUL_OPEN = False

iconsExpanded = 1
MoneyTaskBarExpander = 1
ENABLE_EXPANDED_MONEY_TASKBAR = 1

OFFLINESHOP_DIALOG = 0
itemRemoveGrid = []
listRemoveItem = []
GIFT_CODE_SYSTEM = 1
IS_ACCE_WINDOW = False
buy_without_dialog = 0
price_color1 = "|cFFb0a996"

windowStatusOpened = "opened"
windowStatusClosed = "closed"
windowStatus = {
	"switchbot" : {
		"status": windowStatusClosed,
		"pos": [None, None],
		"slot": None,
		"switchType": None,
		"switchTypeVnum": None,
	},
}

def windowIsOpened(window):
	return window in windowStatus and windowStatus[window]["status"] == windowStatusOpened

def getWindowValue(window, key):
	if window in windowStatus and key in windowStatus[window]:
		return windowStatus[window][key]

	return None

def setWindowValue(window, key, value):
	if window in windowStatus:
		windowStatus[window][key] = value

if app.ENABLE_EVENT_MANAGER:
	_interface_instance = None
	def GetInterfaceInstance():
		global _interface_instance
		return _interface_instance
	def SetInterfaceInstance(instance):
		global _interface_instance
		if _interface_instance:
			del _interface_instance
		_interface_instance = instance

if app.ENABLE_COLLECT_WINDOW:
	CollectWindowQID = [0 for i in range(5)]

ENABLE_NEW_LEVELSKILL_SYSTEM = 0
ENABLE_RANDOM_CHANNEL_SEL = 0
ENABLE_CLEAN_DATA_IF_FAIL_LOGIN = 0
ENABLE_PASTE_FEATURE = 1
ENABLE_FULLSTONE_DETAILS = 1
ENABLE_REFINE_PCT = 1
IS_BONUS_CHANGER = False
EXTRA_UI_FEATURE = 1

if app.ENABLE_HIDE_COSTUME_SYSTEM:
	HIDDEN_BODY_COSTUME = 0
	HIDDEN_HAIR_COSTUME = 0
	HIDDEN_ACCE_COSTUME = 0
	HIDDEN_WEAPON_COSTUME = 0
	HIDDEN_AURA_COSTUME = 0
	HIDDEN_STOLE_COSTUME = 0

NEW_678TH_SKILL_ENABLE = 1
SELECT_CHAR_NO_DELAY = 0.3
ENABLE_LOAD_EX_DATA = False
ENABLE_POTIONS_AFFECTSHOWER = 0
ENABLE_SAVE_ACCOUNT = True
CONFIG_YOL = "locale/shared/ui/config/"
DISABLE_MODEL_PREVIEW = 0
SYSTEMS_WINDOW_CLOSE = 0
SYSTEMS_WINDOW_OPEN = 0
AFFECT_SHOWER_TOOLTIP_RENEWAL = 1

PO = 0
DRAGON_SOULD_REFINE_OPEN = 0
DRAGON_SOULD_STEP_OPEN = 0

def NumberToStrRomanNumerals(number):
	ROMAN = [
		(1000, "M"),
		( 900, "CM"),
		( 500, "D"),
		( 400, "CD"),
		( 100, "C"),
		(  90, "XC"),
		(  50, "L"),
		(  40, "XL"),
		(  10, "X"),
		(   9, "IX"),
		(   5, "V"),
		(   4, "IV"),
		(   1, "I"),
	]
	
	result = ""
	for (arabic, roman) in ROMAN:
		(factor, number) = divmod(number, arabic)
		result += roman * factor
	return result

import grp
def GetPriceColor(price):
	if price < 500000000:
		return grp.GenerateColor(1.0, 0.7843, 0.0, 1.0)
	elif price < 1000000000:
		return grp.GenerateColor((255.0/255.0), (153.0/255.0), (51.0/255.0), 1.0)
	elif price < 10000000000:
		return grp.GenerateColor((153.0/255.0), (76.0/255.0), (0.0/255.0), 1.0)
	else:
		return grp.GenerateColor((255.0/255.0), (51.0/255.0), (51.0/255.0), 1.0)
			
def ConvertMoneyText(text, powers = dict(k = 10**3, m = 10**6, b = 10**9)):
	"""
	Format string value in thousands, millions or billions.

	'1k' = 1.000
	'100kk' = 100.000.000
	'100m' = 100.000.000
	'1b' = 1.000.000.000
	'1kmb' = 1.000 (can't use multiple suffixes types)
	"""

	match = re.search(r'(\d+)({:s}+)?'.format('+|'.join(powers.keys())), text, re.I)
	if match:
		moneyValue, suffixName = match.groups()
		moneyValue = int(moneyValue)
		if not suffixName:
			return moneyValue

		return moneyValue * (powers[suffixName[0]] ** len(suffixName))

	return 0

def ConvertChequeText(text, powers = dict(k = 10**3, m = 10**6, b = 10**9)):
	"""
	Format string value in thousands, millions or billions.

	'1k' = 1.000
	'100kk' = 100.000.000
	'100m' = 100.000.000
	'1b' = 1.000.000.000
	'1kmb' = 1.000 (can't use multiple suffixes types)
	"""

	match = re.search(r'(\d+)({:s}+)?'.format('+|'.join(powers.keys())), text, re.I)
	if match:
		chequeValue, suffixName = match.groups()
		chequeValue = int(chequeValue)
		if not suffixName:
			return chequeValue

		return chequeValue * (powers[suffixName[0]] ** len(suffixName))

	return 0

# Note: INVENTORY_AUTO_OPEN and ENABLE_FAST_OPEN now stored in registry via settings.py

lastSentenceStack = []
lastSentencePos = 0

INPUT_IGNORE = 0

if app.ENABLE_REFINE_RENEWAL:
	IS_AUTO_REFINE = False
	AUTO_REFINE_TYPE = 0
	AUTO_REFINE_DATA = {
		"ITEM" : [-1, -1],
		"NPC" : [0, -1, -1, 0]
	}


IN_GAME_SHOP_ENABLE = 0
CONSOLE_ENABLE = 0

PVPMODE_ENABLE = 1
PVPMODE_TEST_ENABLE = 0
PVPMODE_ACCELKEY_ENABLE = 1
PVPMODE_ACCELKEY_DELAY = 0.5
PVPMODE_PROTECTED_LEVEL = 15

FOG_LEVEL0 = 4800.0
FOG_LEVEL1 = 9600.0
FOG_LEVEL2 = 12800.0
FOG_LEVEL = FOG_LEVEL0
FOG_LEVEL_LIST=[FOG_LEVEL0, FOG_LEVEL1, FOG_LEVEL2]

CAMERA_MAX_DISTANCE_SHORT = 2500.0
CAMERA_MAX_DISTANCE_LONG = 3500.0
CAMERA_MAX_DISTANCE_LIST=[CAMERA_MAX_DISTANCE_SHORT, CAMERA_MAX_DISTANCE_LONG]
CAMERA_MAX_DISTANCE = CAMERA_MAX_DISTANCE_SHORT

CHRNAME_COLOR_INDEX = 0

ENVIRONMENT_NIGHT="d:/ymir work/environment/moonlight04.msenv"

HIGH_PRICE = 500000
MIDDLE_PRICE = 50000
ERROR_METIN_STONE = 28960
SUB2_LOADING_ENABLE = 1
EXPANDED_COMBO_ENABLE = 1
CONVERT_EMPIRE_LANGUAGE_ENABLE = 0
USE_ITEM_WEAPON_TABLE_ATTACK_BONUS = 0
ADD_DEF_BONUS_ENABLE = 0
LOGIN_COUNT_LIMIT_ENABLE = 0

USE_SKILL_EFFECT_UPGRADE_ENABLE = 1

VIEW_OTHER_EMPIRE_PLAYER_TARGET_BOARD = 1
GUILD_MONEY_PER_GSP = 100
GUILD_WAR_TYPE_SELECT_ENABLE = 1
TWO_HANDED_WEAPON_ATT_SPEED_DECREASE_VALUE = 10

HAIR_COLOR_ENABLE = 1
ARMOR_SPECULAR_ENABLE = 1
WEAPON_SPECULAR_ENABLE = 1
SEQUENCE_PACKET_ENABLE = 1
KEEP_ACCOUNT_CONNETION_ENABLE = 1
MINIMAP_POSITIONINFO_ENABLE = 1

isItemQuestionDialog = 0

def GET_ITEM_QUESTION_DIALOG_STATUS():
	global isItemQuestionDialog
	return isItemQuestionDialog

def SET_ITEM_QUESTION_DIALOG_STATUS(flag):
	global isItemQuestionDialog
	isItemQuestionDialog = flag

import app
import net

	
def SET_DEFAULT_FOG_LEVEL():
	global FOG_LEVEL
	app.SetMinFog(FOG_LEVEL)

def SET_FOG_LEVEL_INDEX(index):
	global FOG_LEVEL
	global FOG_LEVEL_LIST
	try:
		FOG_LEVEL=FOG_LEVEL_LIST[index]
	except IndexError:
		FOG_LEVEL=FOG_LEVEL_LIST[0]
	app.SetMinFog(FOG_LEVEL)

def GET_FOG_LEVEL_INDEX():
	global FOG_LEVEL
	global FOG_LEVEL_LIST
	return FOG_LEVEL_LIST.index(FOG_LEVEL)


def SET_DEFAULT_CAMERA_MAX_DISTANCE():
	global CAMERA_MAX_DISTANCE
	app.SetCameraMaxDistance(CAMERA_MAX_DISTANCE)

def SET_CAMERA_MAX_DISTANCE_INDEX(index):
	global CAMERA_MAX_DISTANCE
	global CAMERA_MAX_DISTANCE_LIST
	try:
		CAMERA_MAX_DISTANCE=CAMERA_MAX_DISTANCE_LIST[index]
	except:
		CAMERA_MAX_DISTANCE=CAMERA_MAX_DISTANCE_LIST[0]

	app.SetCameraMaxDistance(CAMERA_MAX_DISTANCE)

def GET_CAMERA_MAX_DISTANCE_INDEX():
	global CAMERA_MAX_DISTANCE
	global CAMERA_MAX_DISTANCE_LIST
	return CAMERA_MAX_DISTANCE_LIST.index(CAMERA_MAX_DISTANCE)


import chrmgr
try:
	import player
except Exception as e:
	import dbg
	import traceback
	dbg.TraceError("PLAYER IMPORT FAILED: " + traceback.format_exc())
	raise
import app

def SET_DEFAULT_CHRNAME_COLOR():
	global CHRNAME_COLOR_INDEX
	chrmgr.SetEmpireNameMode(CHRNAME_COLOR_INDEX)

def SET_CHRNAME_COLOR_INDEX(index):
	global CHRNAME_COLOR_INDEX
	CHRNAME_COLOR_INDEX=index
	chrmgr.SetEmpireNameMode(index)

def GET_CHRNAME_COLOR_INDEX():
	global CHRNAME_COLOR_INDEX
	return CHRNAME_COLOR_INDEX

def SET_VIEW_OTHER_EMPIRE_PLAYER_TARGET_BOARD(index):
	global VIEW_OTHER_EMPIRE_PLAYER_TARGET_BOARD
	VIEW_OTHER_EMPIRE_PLAYER_TARGET_BOARD = index

def GET_VIEW_OTHER_EMPIRE_PLAYER_TARGET_BOARD():
	global VIEW_OTHER_EMPIRE_PLAYER_TARGET_BOARD
	return VIEW_OTHER_EMPIRE_PLAYER_TARGET_BOARD

def SET_DEFAULT_CONVERT_EMPIRE_LANGUAGE_ENABLE():
	global CONVERT_EMPIRE_LANGUAGE_ENABLE
	net.SetEmpireLanguageMode(CONVERT_EMPIRE_LANGUAGE_ENABLE)

def SET_DEFAULT_USE_ITEM_WEAPON_TABLE_ATTACK_BONUS():
	global USE_ITEM_WEAPON_TABLE_ATTACK_BONUS
	player.SetWeaponAttackBonusFlag(USE_ITEM_WEAPON_TABLE_ATTACK_BONUS)

def SET_DEFAULT_USE_SKILL_EFFECT_ENABLE():
	global USE_SKILL_EFFECT_UPGRADE_ENABLE
	app.SetSkillEffectUpgradeEnable(USE_SKILL_EFFECT_UPGRADE_ENABLE)

def SET_TWO_HANDED_WEAPON_ATT_SPEED_DECREASE_VALUE():
	global TWO_HANDED_WEAPON_ATT_SPEED_DECREASE_VALUE
	app.SetTwoHandedWeaponAttSpeedDecreaseValue(TWO_HANDED_WEAPON_ATT_SPEED_DECREASE_VALUE)

import item

ACCESSORY_MATERIAL_LIST = [50623, 50624, 50625, 50626, 50627, 50628, 50629, 50630, 50631, 50632, 50633, 50634, 50635, 50636, 50637, 50638, 50639, 50640, 50641, 50642, 50643, 50644, 50647]
JewelAccessoryInfos = [
		[ 50639,	89110,	89120,	89130 ],
		[ 50640,	32180,	32280,	32380 ],
		[ 50641,	32120,	32220,	32320 ],
		[ 50642,	32150,	32250,	32350 ],
		[ 50643,	32130,	32230,	32330 ],
		[ 50644,	32160,	32260,	32360 ],
		[ 50639,	17200,	14200,	16200 ],
		[ 50640,	32170,	32270,	32370 ],
		[ 50641,	32140,	32240,	32340 ],
		[ 50642,	32100,	32200,	32300 ],
		[ 50643,	32190,	32290,	32390 ],
		[ 50644,	32110,	32210,	32310 ],
		[ 50647,	32670,	32680,	32690 ],
	]
def GET_ACCESSORY_MATERIAL_VNUM(vnum, subType):
	ret = vnum
	item_base = (vnum // 10) * 10
	for info in JewelAccessoryInfos:
		if item.ARMOR_WRIST == subType:
			if info[1] == item_base:
				return info[0]
		elif item.ARMOR_NECK == subType:
			if info[2] == item_base:
				return info[0]
		elif item.ARMOR_EAR == subType:
			if info[3] == item_base:
				return info[0]

	if vnum >= 16210 and vnum <= 16219:
		return 50625

	if item.ARMOR_WRIST == subType:
		WRIST_ITEM_VNUM_BASE = 14000
		ret -= WRIST_ITEM_VNUM_BASE
	elif item.ARMOR_NECK == subType:
		NECK_ITEM_VNUM_BASE = 16000
		ret -= NECK_ITEM_VNUM_BASE
	elif item.ARMOR_EAR == subType:
		EAR_ITEM_VNUM_BASE = 17000
		ret -= EAR_ITEM_VNUM_BASE

	type = ret//20

	if type<0 or type>=len(ACCESSORY_MATERIAL_LIST):
		type = (ret-170) // 20
		if type<0 or type>=len(ACCESSORY_MATERIAL_LIST):
			return 0

	return ACCESSORY_MATERIAL_LIST[type]


def GET_BELT_MATERIAL_VNUM(vnum, subType = 0):
	return 18900


def IS_AUTO_POTION(itemVnum):
	return IS_AUTO_POTION_HP(itemVnum) or IS_AUTO_POTION_SP(itemVnum)

def IS_AUTO_POTION_HP(itemVnum):
	if 72723 <= itemVnum and 72726 >= itemVnum:
		return 1
	elif itemVnum >= 76021 and itemVnum <= 76022:
		return 1

	return 0

def IS_AUTO_POTION_SP(itemVnum):
	if 72727 <= itemVnum and 72730 >= itemVnum:
		return 1
	elif itemVnum >= 76004 and itemVnum <= 76005:
		return 1

	return 0

if app.ENABLE_EXTENDED_BLEND:
	def IS_BLEND_ITEM(itemVnum):
		try:
			item.SelectItem(itemVnum)
			itemType = item.GetItemType()
			if itemType == item.BLEND:
				return 1
		except:
			pass
		return 0

	def IS_PERMANANET_BLEND_ITEM(itemVnum):
		if 51821 <= itemVnum and 51826 >= itemVnum:
			return 1

		if 51813 <= itemVnum and 51820 >= itemVnum:
			return 1

		if 40017 <= itemVnum and 40025 >= itemVnum:
			return 1

		return 0



# Pet system data is now stored in the C++ CPythonPet singleton,
# accessible via the `pet` pybind11 module. No Python-side storage needed.
if app.ENABLE_NEW_PET_SYSTEM:
	gui_mount = {
		"LEVEL" : 0,
		"EXP" : 0,
		"EXP_NEED" : 0,
		"SKILLS" : [],
	}
if app.ENABLE_DROP_INFO:
	dropInfoDict = {}
	
if app.ENABLE_PERFORMANCE_IMPROVEMENTS_NEW:
	isGameLoaded = False



_game_instance = None
def GetGameInstance():
	global _game_instance
	return _game_instance
def SetGameInstance(instance):
	global _game_instance
	if _game_instance:
		del _game_instance
	_game_instance = instance
	
_interface_instance = None
def GetInterfaceInstance():
	global _interface_instance
	return _interface_instance
def SetInterfaceInstance(instance):
	global _interface_instance
	if _interface_instance:
		del _interface_instance
	_interface_instance = instance

# ============================================================================
# Voice Chat (Opus) — voice-chat/CHANGES_ZARIS.md (Etap 5)
# ============================================================================
if app.ENABLE_VOICE_CHAT:
	VOICE_CHAT_CONFIG = {}
	VOICE_CHAT_CONFIG_LOADED = False
	# #7 per-player mute: zbior nazw wyciszonych mowcow. Trzymany ODDZIELNIE od
	# VOICE_CHAT_CONFIG (ktore SendVoiceChatVolumes iteruje jako glosnosci) — w
	# pliku jako linie "__MUTE__\t<nazwa>".
	VOICE_MUTED_SPEAKERS = set()
	VOICE_MUTE_MARKER = "__MUTE__"
	def LoadVoiceChatConfig():
		global VOICE_CHAT_CONFIG_LOADED
		if VOICE_CHAT_CONFIG_LOADED:
			return

		# ZARIS FORK (P1-8): poprzednio tryb "a+" - wskaznik pliku stoi na EOF,
		# wiec readlines() zawsze zwracalo [] i zapisane glosnosci nigdy sie nie
		# wczytywaly. Tryb "r"; brak pliku = pusta konfiguracja.
		# UWAGA: open() klienta zwraca pack_file (brak context-managera) - explicit
		# open/close jak localeInfo, NIE `with`. Szeroki except (pack_file rzuca
		# nie-OSError przy braku pliku).
		lines = []
		try:
			f = open("voicechat.cfg", "r")
			lines = f.readlines()
			f.close()
		except Exception:
			lines = []

		for line in lines:
			data = line.replace("\n", "").split("\t")
			if len(data) < 2:
				continue

			# #7: wpis mute (nazwa NIE jest glosnoscia) -> osobny zbior.
			if data[0] == VOICE_MUTE_MARKER:
				if data[1]:
					VOICE_MUTED_SPEAKERS.add(data[1])
				continue

			try:
				VOICE_CHAT_CONFIG[data[0]] = float(data[1])
			except:
				pass

		VOICE_CHAT_CONFIG_LOADED = True

	def SendVoiceChatVolumes():
		for playerName, vol in VOICE_CHAT_CONFIG.items():
			try:
				volume = float(vol) # In case we have anything that isn't a number
				app.VoiceChatSetVolumeForSpeaker(playerName, volume)
			except Exception:
				pass

	def GetVoiceChatVolume(playerName):
		global VOICE_CHAT_CONFIG_LOADED
		if not VOICE_CHAT_CONFIG_LOADED:
			LoadVoiceChatConfig()

		if playerName in VOICE_CHAT_CONFIG:
			return VOICE_CHAT_CONFIG[playerName]

		return 1.0 # Default to 100

	def GetVoiceChatConfig(option):
		global VOICE_CHAT_CONFIG_LOADED
		if not VOICE_CHAT_CONFIG_LOADED:
			LoadVoiceChatConfig()

		if option in VOICE_CHAT_CONFIG:
			return int(VOICE_CHAT_CONFIG[option])

		return 0

	def SetVoiceChatConfig(option, value):
		VOICE_CHAT_CONFIG[option] = value

	def ApplyVoiceChatDevices():
		# Aplikuj ZAPISANE urzadzenia nagrywajace/odtwarzajace przy wejsciu do gry.
		# Domyslny (nullptr) capture device miniaudio bywa CICHY na WASAPI (oddaje
		# cyfrowa cisze, SPL=0) - dopiero jawny endpoint otwiera realny mikrofon.
		# Dlatego ZAWSZE aplikujemy konkretny index (0 = pierwsze urzadzenie gdy brak
		# zapisu), zamiast polegac na domysle. Clamp do liczby urzadzen (lista mogla
		# sie zmienic miedzy sesjami).
		try:
			micCount = app.VoiceChatGetCaptureDeviceCount()
			if micCount > 0:
				micIdx = GetVoiceChatConfig("VOICE_CHAT_MIC_DEVICE")
				if micIdx < 0 or micIdx >= micCount:
					micIdx = 0
				app.VoiceChatSetCaptureDevice(micIdx)
			spkCount = app.VoiceChatGetPlaybackDeviceCount()
			if spkCount > 0:
				spkIdx = GetVoiceChatConfig("VOICE_CHAT_SPK_DEVICE")
				if spkIdx < 0 or spkIdx >= spkCount:
					spkIdx = 0
				app.VoiceChatSetPlaybackDevice(spkIdx)
		except Exception:
			pass

	def ApplyVoiceChatMutes():
		# #7: re-aplikuj zapisana liste mute do C++ przy wejsciu do gry (C++ czysci
		# m_MutedSpeakers przy Destroy / LeaveGamePhase).
		global VOICE_CHAT_CONFIG_LOADED
		if not VOICE_CHAT_CONFIG_LOADED:
			LoadVoiceChatConfig()
		for name in VOICE_MUTED_SPEAKERS:
			try:
				app.VoiceChatMuteSpeaker(name, 1)
			except Exception:
				pass

	def IsVoiceSpeakerMuted(name):
		global VOICE_CHAT_CONFIG_LOADED
		if not VOICE_CHAT_CONFIG_LOADED:
			LoadVoiceChatConfig()
		return name in VOICE_MUTED_SPEAKERS

	def SetVoiceSpeakerMuted(name, mute):
		# #7: ustaw/zdejmij mute dla mowcy, zsynchronizuj C++ i zapisz config.
		global VOICE_CHAT_CONFIG_LOADED
		if not VOICE_CHAT_CONFIG_LOADED:
			LoadVoiceChatConfig()
		if not name:
			return
		if mute:
			VOICE_MUTED_SPEAKERS.add(name)
		else:
			VOICE_MUTED_SPEAKERS.discard(name)
		try:
			app.VoiceChatMuteSpeaker(name, 1 if mute else 0)
		except Exception:
			pass
		SaveVoiceChatConfig()

	def ToggleVoiceSpeakerMuted(name):
		# Zwraca nowy stan (True = teraz wyciszony).
		newState = not IsVoiceSpeakerMuted(name)
		SetVoiceSpeakerMuted(name, newState)
		return newState

	def SetVoiceChatVolume(playerName, vol):
		VOICE_CHAT_CONFIG[playerName] = vol

	def SaveVoiceChatConfig():
		lines = []
		for playerName, vol in VOICE_CHAT_CONFIG.items():
			lines.append("{}\t{}\n".format(playerName, vol))

		# #7: dopisz wyciszonych mowcow jako "__MUTE__\t<nazwa>".
		for name in VOICE_MUTED_SPEAKERS:
			lines.append("{}\t{}\n".format(VOICE_MUTE_MARKER, name))

		# explicit open/close (pack_file - brak `with`)
		try:
			f = open("voicechat.cfg", "w+")
			f.writelines(lines)
			f.close()
		except Exception:
			pass

	# Push-to-talk key (configurable). Stored as DIK code in VOICE_CHAT_CONFIG
	# under VOICE_CHAT_PTT_KEY. 0 / missing == default app.DIK_Y.
	def GetVoiceChatPTTKey():
		key = GetVoiceChatConfig("VOICE_CHAT_PTT_KEY")
		if key <= 0:
			return app.DIK_Y
		return key

	# Capture-mode flag: set while the option dialog waits for the next key press
	# to rebind PTT. game.py reads this to swallow the key instead of broadcasting.
	VOICE_PTT_CAPTURE_MODE = False
	# Instancja okna opcji ktora aktualnie czeka na klawisz (jest kilka instancji
	# OptionDialog - interfacemodule/uisystem/uioption). game.py musi zwrocic klawisz
	# DO TEJ WIDOCZNEJ, ktora user kliknal, nie do hardcoded self.interface.wndgameOption.
	VOICE_PTT_CAPTURE_DIALOG = None

	def SetVoicePTTCaptureMode(state, dialog=None):
		global VOICE_PTT_CAPTURE_MODE, VOICE_PTT_CAPTURE_DIALOG
		VOICE_PTT_CAPTURE_MODE = bool(state)
		VOICE_PTT_CAPTURE_DIALOG = dialog if state else None

	def IsVoicePTTCaptureMode():
		return VOICE_PTT_CAPTURE_MODE

	def GetVoicePTTCaptureDialog():
		return VOICE_PTT_CAPTURE_DIALOG

if app.__AUTO_HUNT__:
	# Auto Hunt - aktywny status (do wyciszenia captchy / bot control gdy bot wlaczony)
	AUTO_HUNT_ACTIVE = 0
	# Auto Hunt - czy gracz POSIADA affect-uprawnienie (item 38014). Ustawiane w BINARY_NEW_AddAffect/
	# RemoveAffect. Gate na otwarcie panelu F6 (serwer i tak blokuje start bez affectu, ale panel ma byc ukryty).
	AUTO_HUNT_HAS_AFFECT = 0
	# Auto Hunt - auto-login: stan + zapamietane dane polaczenia/logowania
	autoHuntAutoLoginDict = {
		"status" : 0,
		"leftTime" : 0,
		"id" : "",
		"pwd" : "",
		"pin" : "",
		"addr" : "",
		"port" : 0,
		"account_addr" : "",
		"account_port" : 0,
		"slot" : -1,
		"newOptions" : None,
		"slotStatus" : {},
		"skillDict" : None,
	}
