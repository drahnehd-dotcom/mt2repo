# -*- coding: utf-8 -*-
"""
Locale Info Module
Rewritten for Python 3
"""

import app
import constInfo
import os

__all__ = [
    "LoadLocaleData",
    "LoadLocaleFile",
    "NumberToString",
    "NumberToMoneyString",
    "MoneyFormat",
    "SecondToDHM",
    "SecondToDHMS",
    "SecondToHM",
    "SecondToMS",
    "SecondToHMS",
    "sec2time",
    "GetFormattedNumberString",
    "FormatMoney",
    "GetAlignmentTitleName",
    "GetMiniMapZoneNameByIdx",
    "GetMiniMapZoneNameByIdx2",
    "GetLocaleString",
]

APP_TITLE = "KowalMT2"

GUILD_MEMBER_COUNT_INFINITY = "INFINITY"
GUILD_MARK_MIN_LEVEL = "3"
ERROR_MARK_UPLOAD_NEED_RECONNECT = "UploadMark: Reconnect to game"

# Font configuration file handling
if not os.path.exists("_cfg"):
    os.makedirs("_cfg")

if not os.path.exists("_cfg/font.cfg"):
    f = open("_cfg/font.cfg", "w")
    f.write("0")
    f.close()

f = open("_cfg/font.cfg", "r+")
hehe = f.read()
if hehe == "1":
    UI_DEF_FONT = "Tahoma:14"
    UI_DEF_FONT_LARGE = "Tahoma:16"
    UI_DEF_FONT_SMALL = "Tahoma:11"
    UI_BOLD_FONT = "Tahoma:14b"
elif hehe == "0":
    UI_DEF_FONT = "Tahoma:12"
    UI_DEF_FONT_LARGE = "Tahoma:14"
    UI_DEF_FONT_SMALL = "Tahoma:9"
    UI_BOLD_FONT = "Tahoma:12b"
else:
    UI_DEF_FONT = "Tahoma:12"
    UI_DEF_FONT_LARGE = "Tahoma:14"
    UI_DEF_FONT_SMALL = "Tahoma:9"
    UI_BOLD_FONT = "Tahoma:12b"
    fw = open("_cfg/font.cfg", "w")
    fw.write("0")
    fw.close()
f.close()



def NumberToString(n):
    """Convert number to string with thousand separators."""
    if n <= 0:
        return "0"

    return "{:,}".format(int(n)).replace(",", ".")

# Cheque system functions
if app.ENABLE_CHEQUE_SYSTEM:
    def NumberToGoldNotText(n):
        """Format gold number without unit text."""
        if n <= 0:
            return "0 "

        return "{:,}".format(int(n)).replace(",", ".")

    def NumberToCheque(n):
        """Format cheque number with unit."""
        if n <= 0:
            return "0 {}".format(CHEQUE_SYSTEM_UNIT_CHEQUE)

        return "{} {}".format(
            "{:,}".format(int(n)).replace(",", "."),
            CHEQUE_SYSTEM_UNIT_CHEQUE
        )

    def DO_YOU_BUY_ITEM_YANG_CHEQUE(buyItemName, buyItemCount, buyItemPrice, buyItemCheque):
        """Generate buy confirmation message with yang and cheque."""
        if buyItemCount > 1:
            return DO_YOU_BUY_ITEM4 % (buyItemName, buyItemCount, buyItemCheque, buyItemPrice)
        else:
            return DO_YOU_BUY_ITEM3 % (buyItemName, buyItemCheque, buyItemPrice)

    def DO_YOU_BUY_ITEM_CHEQUE_SIN_YANG(buyItemName, buyItemCount, buyItemCheque):
        """Generate buy confirmation message with cheque only."""
        if buyItemCount > 1:
            return DO_YOU_BUY_ITEM4 % (buyItemName, buyItemCount, buyItemCheque)
        else:
            return DO_YOU_BUY_ITEM3 % (buyItemName, buyItemCheque)


def LoadLocaleData():
    """Load locale data from path."""
    app.LoadLocaleData(app.GetLocalePath())


def mapping(**kwargs):
    """Create a dictionary from keyword arguments."""
    return kwargs


def SNA(text):
    """String No Argument - return text as-is."""
    def f(x):
        return text
    return f


def SA(text):
    """String Argument - format text with one argument."""
    def f(x):
        return text % x
    return f


def SAN(text):
    """String Argument Number - format text with one argument."""
    def f(x):
        return text % x
    return f


def SAA(text):
    """String Argument Argument - format text with one argument."""
    def f(x):
        return text % x
    return f


def SAAAA(text):
    """String Argument (4x) - format text with one argument."""
    def f(x):
        return text % x
    return f


def LoadLocaleFile(srcFileName, localeDict):
    """Load locale strings from a file into the given dictionary."""
    funcDict = {"SA": SA, "SNA": SNA, "SAA": SAA, "SAN": SAN, "SAAAA": SAAAA}

    lineIndex = 1

    try:
        f = open(srcFileName, "r")
        lines = f.readlines()
        f.close()
    except IOError:
        import dbg
        dbg.LogBox("LoadLocaleError({})".format(srcFileName))
        return

    for line in lines:
        try:
            if not line.strip():
                lineIndex += 1
                continue

            tokens = line.rstrip("\n").split("\t")
            if len(tokens) == 2:
                localeDict[tokens[0]] = tokens[1]
            elif len(tokens) >= 3:
                type_str = tokens[2].strip()
                if type_str:
                    localeDict[tokens[0]] = funcDict[type_str](tokens[1])
                else:
                    localeDict[tokens[0]] = tokens[1]
            elif len(tokens) == 1:
                localeDict[tokens[0]] = ""
            elif len(tokens) == 0:
                localeDict[line.rstrip()] = ""
            else:
                raise RuntimeError("Unknown TokenSize")

            lineIndex += 1
        except Exception as e:
            import dbg
            dbg.LogBox("{}: line({}): {}".format(srcFileName, lineIndex, line), "Error")
            raise


# Module exports
all_exports = ["locale", "error"]

FN_GM_MARK = "locale/shared/effect/gm.mse"
LOCALE_FILE_NAME = "{}/locale_game.txt".format(app.GetLocalePath())
LOCALE_GAME2 = "{}/locale_game_new.txt".format(app.GetLocalePath())

LoadLocaleFile(LOCALE_FILE_NAME, locals())
LoadLocaleFile(LOCALE_GAME2, locals())
if constInfo.ENABLE_LOAD_EX_DATA:
    LoadLocaleFile("locale/ex/locale_game_ex.txt", locals())


def CutMoneyString(sourceText, startIndex, endIndex, insertingText, backText):
    """Cut and format money string."""
    sourceLength = len(sourceText)

    if sourceLength < startIndex:
        return backText

    text = sourceText[max(0, sourceLength - endIndex):sourceLength - startIndex]

    if not text:
        return backText

    if int(text) <= 0:
        return backText

    text = str(int(text))

    if backText:
        backText = " " + backText

    return text + insertingText + backText


def SecondToDHM(time):
    """Convert seconds to Days, Hours, Minutes format."""
    if time < 60:
        return "0" + MINUTE

    second = int(time % 60)
    minute = int((time // 60) % 60)
    hour = int((time // 60) // 60) % 24
    day = int(int((time // 60) // 60) // 24)

    text = ""

    if day > 0:
        text += str(day) + DAY
        text += " "

    if hour > 0:
        text += str(hour) + HOUR
        text += " "

    if minute > 0:
        text += str(minute) + MINUTE

    return text


def SecondToDHMS(time):
    """Convert seconds to Days, Hours, Minutes format (alternate)."""
    if time < 60:
        return str(time) + "sek."

    second = int(time % 60)
    minute = int((time // 60) % 60)
    hour = int((time // 60) // 60) % 24
    day = int(int((time // 60) // 60) // 24)

    text = ""

    if day > 0:
        text += str(day) + DAY
        text += " "

    if hour > 0:
        text += str(hour) + HOUR
        text += " "

    if minute > 0:
        text += str(minute) + MINUTE

    return text


def SecondToHM(time):
    """Convert seconds to Hours, Minutes format."""
    if time < 60:
        return "0" + MINUTE

    second = int(time % 60)
    minute = int((time // 60) % 60)
    hour = int((time // 60) // 60)

    text = ""

    if hour > 0:
        text += str(hour) + HOUR
        if hour > 0:
            text += " "

    if minute > 0:
        text += str(minute) + MINUTE

    return text


def MinuteToHM(minute):
    """Convert minutes to Hours, Minutes format (playtime on the character select)."""
    minute = int(minute)

    if minute < 60:
        return str(minute) + MINUTE

    text = str(minute // 60) + HOUR

    if minute % 60 > 0:
        text += " " + str(minute % 60) + MINUTE

    return text


def GetAlignmentTitleName(alignment):
    """Get title name based on alignment value."""
    if alignment >= 700000:
        return TITLE_NAME_LIST[0]
    elif alignment >= 600000:
        return TITLE_NAME_LIST[1]
    elif alignment >= 500000:
        return TITLE_NAME_LIST[2]
    elif alignment >= 450000:
        return TITLE_NAME_LIST[3]
    elif alignment >= 350000:
        return TITLE_NAME_LIST[4]
    elif alignment >= 250000:
        return TITLE_NAME_LIST[5]
    elif alignment >= 150000:
        return TITLE_NAME_LIST[6]
    elif alignment >= 50000:
        return TITLE_NAME_LIST[7]
    elif alignment >= 25000:
        return TITLE_NAME_LIST[8]
    elif alignment >= 0:
        return TITLE_NAME_LIST[9]
    elif alignment > -25000:
        return TITLE_NAME_LIST[10]
    elif alignment > -50000:
        return TITLE_NAME_LIST[11]
    elif alignment > -100000:
        return TITLE_NAME_LIST[12]
    return TITLE_NAME_LIST[13]


OPTION_PVPMODE_MESSAGE_DICT = {
    0: PVP_MODE_NORMAL,
    1: PVP_MODE_REVENGE,
    2: PVP_MODE_KILL,
    3: PVP_MODE_PROTECT,
    4: PVP_MODE_GUILD,
}

error = mapping(
    CREATE_WINDOW=GAME_INIT_ERROR_MAIN_WINDOW,
    CREATE_CURSOR=GAME_INIT_ERROR_CURSOR,
    CREATE_NETWORK=GAME_INIT_ERROR_NETWORK,
    CREATE_ITEM_PROTO=GAME_INIT_ERROR_ITEM_PROTO,
    CREATE_MOB_PROTO=GAME_INIT_ERROR_MOB_PROTO,
    CREATE_NO_DIRECTX=GAME_INIT_ERROR_DIRECTX,
    CREATE_DEVICE=GAME_INIT_ERROR_GRAPHICS_NOT_EXIST,
    CREATE_NO_APPROPRIATE_DEVICE=GAME_INIT_ERROR_GRAPHICS_BAD_PERFORMANCE,
    CREATE_FORMAT=GAME_INIT_ERROR_GRAPHICS_NOT_SUPPORT_32BIT,
    NO_ERROR=""
)

GUILDWAR_NORMAL_DESCLIST = [GUILD_WAR_USE_NORMAL_MAP, GUILD_WAR_LIMIT_30MIN, GUILD_WAR_WIN_CHECK_SCORE]
GUILDWAR_WARP_DESCLIST = [GUILD_WAR_USE_BATTLE_MAP, GUILD_WAR_WIN_WIPE_OUT_GUILD, GUILD_WAR_REWARD_POTION]
GUILDWAR_CTF_DESCLIST = [GUILD_WAR_USE_BATTLE_MAP, GUILD_WAR_WIN_TAKE_AWAY_FLAG1, 
                         GUILD_WAR_WIN_TAKE_AWAY_FLAG2, GUILD_WAR_REWARD_POTION]


def GetMiniMapZoneNameByIdx(idx):
    """Get mini map zone name by index."""
    if idx in MINIMAP_ZONE_NAME_DICT_BY_IDX and idx != 0:
        return MINIMAP_ZONE_NAME_DICT_BY_IDX[idx]
    return MAP_NONE


MINIMAP_ZONE_NAME_DICT_BY_IDX = {
    0: "",
    1: MAP_A1,
    2: MAP_C1,
    6: DALSZE_ZAKATKI,
    17: SPIDER_DUNGEON,
    300: WUKONG_DUNGEON,
    21: DEMON_TOWER,
    14: SCORPION_DUNGEON,
    16: ARCTIC_DUNGEON,
    18: HELL_DUNGEON,
    12: JUNGLE_DUNGEON,
    15: SHIP_DUNGEON_1,
    24: SHIP_DUNGEON_2,
    101: AVERAGE_DAMAGE_DUNGEON_2,
    39: SUMMER_DUNGEON,
}


def GetMiniMapZoneNameByIdx2(idx2):
    """Get mini map zone name by index 2."""
    if idx2 in MINIMAP_ZONE_NAME_DICT_BY_IDX2 and idx2 != 0:
        return MINIMAP_ZONE_NAME_DICT_BY_IDX2[idx2]
    return MAP_NONE


MINIMAP_ZONE_NAME_DICT_BY_IDX2 = {
    0: "",
    1: "metin2_map_a1",
    2: "metin2_map_c1",
    3: "metin2_map_a3",
    4: "metin2_map_c3",
    6: "metin2_map_threeway",
    7: "metin2_map_anglar_dungeon_01",
    8: "metin2_map_exp",
    9: "metin2_map_pustynia",
    10: "metin2_map_snow",
    11: "natural_map",
    20: "plechito_lava_map_01",
    22: "metin2_map_sohan",
    23: "metin2_map_las",
    30: "metin2_map_las",
}

MINIMAP_ZONE_NAME_DICT = {
    "metin2_map_a1": MAP_A1,
    "metin2_map_a3": MAP_A3,
    "metin2_map_c1": MAP_C1,
    "metin2_map_c3": MAP_C3,
    "metin2_map_threeway": MAP_THREEWAY,
    "metin2_map_anglar_dungeon_01": MAP_PAJAKI,
    "metin2_map_exp": MAP_75,
    "metin2_map_pustynia": MAP_PUSTYNIA,
    "metin2_map_snow": MAP_SNOW,
    "natural_map": MAP_ZACZAROWANY,
    "plechito_lava_map_01": MAP_OGNISTA,
    "metin2_map_sohan": MAP_SOHAN,
    "metin2_map_las": MAP_LAS,
    "metin2_zakatki": DALSZE_ZAKATKI,
    "zaris_easter_map_2025": EASTER_MAP_2025,
}

JOBINFO_TITLE = [
    [JOB_WARRIOR0, JOB_WARRIOR1, JOB_WARRIOR2],
    [JOB_ASSASSIN0, JOB_ASSASSIN1, JOB_ASSASSIN2],
    [JOB_SURA0, JOB_SURA1, JOB_SURA2],
    [JOB_SHAMAN0, JOB_SHAMAN1, JOB_SHAMAN2],
]
if app.ENABLE_WOLFMAN_CHARACTER:
    JOBINFO_TITLE.append([JOB_WOLFMAN0, JOB_WOLFMAN1, JOB_WOLFMAN2])

WHISPER_ERROR = {
    1: CANNOT_WHISPER_NOT_LOGON,
    2: CANNOT_WHISPER_DEST_REFUSE,
    3: CANNOT_WHISPER_SELF_REFUSE,
}

NOTIFY_MESSAGE = {
    "CANNOT_EQUIP_SHOP": CANNOT_EQUIP_IN_SHOP,
    "CANNOT_EQUIP_EXCHANGE": CANNOT_EQUIP_IN_EXCHANGE,
}

ATTACK_ERROR_TAIL_DICT = {
    "IN_SAFE": CANNOT_ATTACK_SELF_IN_SAFE,
    "DEST_IN_SAFE": CANNOT_ATTACK_DEST_IN_SAFE,
}

SHOT_ERROR_TAIL_DICT = {
    "EMPTY_ARROW": CANNOT_SHOOT_EMPTY_ARROW,
    "IN_SAFE": CANNOT_SHOOT_SELF_IN_SAFE,
    "DEST_IN_SAFE": CANNOT_SHOOT_DEST_IN_SAFE,
}

USE_SKILL_ERROR_TAIL_DICT = {
    "IN_SAFE": CANNOT_SKILL_SELF_IN_SAFE,
    "NEED_TARGET": CANNOT_SKILL_NEED_TARGET,
    "NEED_EMPTY_BOTTLE": CANNOT_SKILL_NEED_EMPTY_BOTTLE,
    "NEED_POISON_BOTTLE": CANNOT_SKILL_NEED_POISON_BOTTLE,
    "REMOVE_FISHING_ROD": CANNOT_SKILL_REMOVE_FISHING_ROD,
    "NOT_YET_LEARN": CANNOT_SKILL_NOT_YET_LEARN,
    "NOT_MATCHABLE_WEAPON": CANNOT_SKILL_NOT_MATCHABLE_WEAPON,
    "WAIT_COOLTIME": CANNOT_SKILL_WAIT_COOLTIME,
    "NOT_ENOUGH_HP": CANNOT_SKILL_NOT_ENOUGH_HP,
    "NOT_ENOUGH_SP": CANNOT_SKILL_NOT_ENOUGH_SP,
    "CANNOT_USE_SELF": CANNOT_SKILL_USE_SELF,
    "ONLY_FOR_ALLIANCE": CANNOT_SKILL_ONLY_FOR_ALLIANCE,
    "CANNOT_ATTACK_ENEMY_IN_SAFE_AREA": CANNOT_SKILL_DEST_IN_SAFE,
    "CANNOT_APPROACH": CANNOT_SKILL_APPROACH,
    "CANNOT_ATTACK": CANNOT_SKILL_ATTACK,
    "ONLY_FOR_CORPSE": CANNOT_SKILL_ONLY_FOR_CORPSE,
    "EQUIP_FISHING_ROD": CANNOT_SKILL_EQUIP_FISHING_ROD,
    "NOT_HORSE_SKILL": CANNOT_SKILL_NOT_HORSE_SKILL,
    "HAVE_TO_RIDE": CANNOT_SKILL_HAVE_TO_RIDE,
}

LEVEL_LIST = ["", HORSE_LEVEL1, HORSE_LEVEL2, HORSE_LEVEL3]

HEALTH_LIST = [
    HORSE_HEALTH0,
    HORSE_HEALTH1,
    HORSE_HEALTH2,
    HORSE_HEALTH3,
]

USE_SKILL_ERROR_CHAT_DICT = {
    "NEED_EMPTY_BOTTLE": SKILL_NEED_EMPTY_BOTTLE,
    "NEED_POISON_BOTTLE": SKILL_NEED_POISON_BOTTLE,
    "ONLY_FOR_GUILD_WAR": SKILL_ONLY_FOR_GUILD_WAR,
}

SHOP_ERROR_DICT = {
    "NOT_ENOUGH_MONEY": SHOP_NOT_ENOUGH_MONEY,
    "SOLDOUT": SHOP_SOLDOUT,
    "INVENTORY_FULL": SHOP_INVENTORY_FULL,
    "INVALID_POS": SHOP_INVALID_POS,
    "NOT_ENOUGH_MONEY_EX": SHOP_NOT_ENOUGH_MONEY_EX,
    "NOT_ENOUGH_PKT_OSIAG": SHOP_NOT_ENOUGH_PKT_OSIAG,
}

if app.ENABLE_CHEQUE_SYSTEM:
    SHOP_ERROR_DICT["NOT_ENOUGH_CHEQUE"] = SHOP_NOT_ENOUGH_CHEQUE
    SHOP_ERROR_DICT["NOT_ENOUGH_MONEY_CHEQUE"] = SHOP_NOT_ENOUGH_MONEY_CHEQUE

STAT_MINUS_DESCRIPTION = {
    "HTH-": STAT_MINUS_CON,
    "INT-": STAT_MINUS_INT,
    "STR-": STAT_MINUS_STR,
    "DEX-": STAT_MINUS_DEX,
}

import itemshop

ITEMSHOP_ERROR_DICT = {
    itemshop.ERROR_NOT_ENOUGH_COINS: ITEMSHOP_NOT_ENOUGH_COINS,
    itemshop.ERROR_INVENTORY_FULL: ITEMSHOP_INVENTORY_FULL,
    itemshop.ERROR_WARP: ITEMSHOP_WARP,
    itemshop.ERROR_NON_EDITOR: ITEMSHOP_NON_EDITOR,
    itemshop.ERROR_COUNT: ITEMSHOP_COUNT,
    itemshop.ERROR_UNKNOWN_ERROR: ITEMSHOP_UNKNOWN_ERROR,
}


def SecondToMS(time):
    """Convert seconds to Minutes, Seconds format."""
    if time < 60:
        return "{}{}".format(time, SECOND)

    second = int(time % 60)
    minute = int((time // 60) % 60)

    text = ""

    if minute > 0:
        text += str(minute) + MINUTE
        if minute > 0:
            text += " "

    if second > 0:
        text += str(second) + SECOND

    return text


MODE_NAME_LIST = (PVP_OPTION_NORMAL, PVP_OPTION_REVENGE, PVP_OPTION_KILL, PVP_OPTION_PROTECT)

if app.ENABLE_ALIGN_RENEWAL:
    TITLE_NAME_LIST = (
        PVP_LEVEL0, PVP_LEVEL1, PVP_LEVEL2, PVP_LEVEL3, PVP_LEVEL4, PVP_LEVEL5, 
        PVP_LEVEL6, PVP_LEVEL7, PVP_LEVEL8, PVP_LEVEL9, PVP_LEVEL10, PVP_LEVEL11, 
        PVP_LEVEL12, PVP_LEVEL13
    )
else:
    TITLE_NAME_LIST = (
        PVP_LEVEL0, PVP_LEVEL1, PVP_LEVEL2, PVP_LEVEL3, PVP_LEVEL4, 
        PVP_LEVEL5, PVP_LEVEL6, PVP_LEVEL7, PVP_LEVEL8
    )


def GetLetterImageName():
    """Get letter image name."""
    return "season1/icon/scroll_close.tga"


def GetLetterOpenImageName():
    """Get letter open image name."""
    return "season1/icon/scroll_open.tga"


def GetLetterCloseImageName():
    """Get letter close image name."""
    return "season1/icon/scroll_close.tga"


def ITEMSHOP_DO_YOU_BUY_ITEM(buyItemName, buyItemCount, buyItemPrice):
    """Generate item shop buy confirmation message."""
    if buyItemCount > 1:
        return ITEMSHOP_DO_YOU_BUY_ITEM2 % (buyItemName, buyItemCount, buyItemPrice)
    else:
        return ITEMSHOP_DO_YOU_BUY_ITEM1 % (buyItemName, buyItemPrice)


def DO_YOU_SELL_ITEM(sellItemName, sellItemCount, sellItemPrice):
    """Generate sell confirmation message."""
    if sellItemCount > 1:
        return DO_YOU_SELL_ITEM2 % (sellItemName, sellItemCount, NumberToMoneyString(sellItemPrice))
    else:
        return DO_YOU_SELL_ITEM1 % (sellItemName, NumberToMoneyString(sellItemPrice))


if app.ENABLE_CHEQUE_SYSTEM:
    def DO_YOU_BUY_ITEM(buyItemName, buyItemCount, buyItemPrice, sellItemCheque = 0):
        """Generate buy confirmation message."""
        if sellItemCheque > 0:
            if buyItemCount > 1:
                return DO_YOU_BUY_ITEM4 % (buyItemName, buyItemCount, sellItemCheque, buyItemPrice)
            else:
                return DO_YOU_BUY_ITEM3 % (buyItemName, sellItemCheque, buyItemPrice)			
        else:
            if buyItemCount > 1:
                return DO_YOU_BUY_ITEM2 % (buyItemName, buyItemCount, buyItemPrice)
            else:
                return DO_YOU_BUY_ITEM1 % (buyItemName, buyItemPrice)
else:
    def DO_YOU_BUY_ITEM(buyItemName, buyItemCount, buyItemPrice):
        """Generate buy confirmation message."""
        if buyItemCount > 1:
            return DO_YOU_BUY_ITEM2 % (buyItemName, buyItemCount, buyItemPrice)
        else:
            return DO_YOU_BUY_ITEM1 % (buyItemName, buyItemPrice)


def REFINE_FAILURE_CAN_NOT_ATTACH(attachedItemName):
    """Generate refine failure message."""
    return REFINE_FAILURE_CAN_NOT_ATTACH % (attachedItemName)


def REFINE_FAILURE_NO_SOCKET(attachedItemName):
    """Generate refine failure no socket message."""
    return REFINE_FAILURE_NO_SOCKET0 % (attachedItemName)


def REFINE_FAILURE_NO_GOLD_SOCKET(attachedItemName):
    """Generate refine failure no gold socket message."""
    return REFINE_FAILURE_NO_GOLD_SOCKET0 % (attachedItemName)


def HOW_MANY_ITEM_DO_YOU_DROP(dropItemName, dropItemCount):
    """Generate drop confirmation message."""
    if dropItemCount > 1:
        return HOW_MANY_ITEM_DO_YOU_DROP2 % (dropItemName, dropItemCount)
    else:
        return HOW_MANY_ITEM_DO_YOU_DROP1 % (dropItemName)


def FISHING_NOTIFY(isFish, fishName):
    """Generate fishing notification message."""
    if isFish:
        return FISHING_NOTIFY1 % (fishName)
    else:
        return FISHING_NOTIFY2 % (fishName)


def FISHING_SUCCESS(isFish, fishName):
    """Generate fishing success message."""
    if isFish:
        return FISHING_SUCCESS1 % (fishName)
    else:
        return FISHING_SUCCESS2 % (fishName)


def NumberToMoneyString(n, unit = MONETARY_UNIT0):
    """Format number as money string with thousand separators."""
    if n <= 0:
        return "0 {}".format(unit)
    
    # Format with thousand separator (dot for PL/CZ locale)
    formatted = "{:,}".format(int(n)).replace(",", ".")
    return "{} {}".format(formatted, unit)


def MoneyFormat(n):
    """Format money number with thousand separators."""
    if n <= 0:
        return "0"

    # Format with thousand separator (dot for PL/CZ locale)
    return "{:,}".format(int(n)).replace(",", ".")

NumberToDecimal = MoneyFormat


def SecondToHMS(time):
    """Convert seconds to Hours, Minutes, Seconds format."""
    try:
        time = int(time)
    except ValueError:
        return "0 " + SECOND

    if int(time) <= 0:
        return "0 " + SECOND

    second = int(time % 60)
    minute = int((time // 60) % 60)
    hour = int((time // 60) // 60)

    text = ""

    if hour > 0:
        text += str(hour) + HOUR
        if minute > 0:
            text += " "

    if minute > 0:
        text += str(minute) + MINUTE
        if second > 0:
            text += " "

    if second > 0:
        text += str(second) + " " + SECOND

    return text


def GetLocaleString(string):
    """Get locale string by key."""
    return globals().get(string, string)


if app.ENABLE_PUNKTY_OSIAGNIEC:
    def NumberToPktOsiagString(n):
        """Format points of achievement number."""
        if n <= 0:
            return "0 {}".format(PKT_OSIAG_LOCALE_GAME)
        return "{} {}".format(
            "{:,}".format(int(n)).replace(",", "."),
            PKT_OSIAG_LOCALE_GAME
        )

    def NumberToSecondaryCoinString(n):
        """Format secondary coin number."""
        if n <= 0:
            return "0 {}".format(PKT_OSIAG_LOCALE_GAME)
        return "{} {}".format(
            "{:,}".format(int(n)).replace(",", "."),
            PKT_OSIAG_LOCALE_GAME
        )


if app.TAKE_LEGEND_DAMAGE_BOARD_SYSTEM:
    def NumberWithDots(n):
        """Format number with dot separators."""
        if n <= 0:
            return "0"
        
        return "{:,}".format(int(n)).replace(",", ".")


def sec2time(timeSeconds, timeTypes, timeShowAll = False):
    """
    Convert seconds to specific format time readable.
    :param timeSeconds: int
    :param timeTypes: str (DMS, DHS, HMS, HM, HS, MS, M, S)
    :param timeShowAll: bool (showing the time name even if the value is 0, otherwise check the value if is > 0)
    :return: string
    """
    (d, remainder) = divmod(timeSeconds, 86400)
    (h, remainder) = divmod(remainder, 3600)
    (m, s) = divmod(remainder, 60)

    TIME_INFO_DICT = dict(
        d = (d, DAY),
        h = (h, HOUR),
        m = (m, MINUTE),
        s = (s, SECOND)
    )

    timeOutput = str()
    for timeType in timeTypes:
        timeType = timeType.lower()

        if timeType in TIME_INFO_DICT:
            (timeValue, timeLocaleName) = TIME_INFO_DICT[timeType]
            if timeValue > 0 or timeShowAll:
                timeOutput += '{:0.0f} {} '.format(timeValue, timeLocaleName)

    if not timeOutput:
        return "Less than a minute"
    return timeOutput[:-1]


def GetFormattedNumberString(number):
    """Get formatted number string with dot separators."""
    return "{:,}".format(number).replace(",", ".")


def FormatMoney(money, suffix = "Yang"):
    """Format money with suffix."""
    return "{} {}".format(GetFormattedNumberString(money), suffix)
