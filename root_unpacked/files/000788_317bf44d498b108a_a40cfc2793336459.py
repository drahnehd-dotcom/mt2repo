# -*- coding: utf-8 -*-
"""Collection mission system window."""

import ui
import uiToolTip
import time
import event
import constInfo
import app
import renderTarget
import chat
import player
import nonplayer
import net
import item
import localeInfo

# Boostery okna misji.
# Przycisk "szansa" bierze eliksir wlasciwy dla kategorii (serwer rozroznia je po value1 itemu).
# Przycisk "czas" bierze dowolna Spirale Czasu - obie dzialaja i u biologa, i u kolekcjonera,
# wiec probujemy najpierw slabsza (50%), zeby nie marnowac mocniejszej (100%).
CHANCE_ITEM_BY_CAT = {
    0: (71036,),
    1: (71037,),
}
TIME_ITEM_ORDER = (72348, 72349)

BLOCKED_CAT_LIST = [2, 3, 4]
RENDER_INDEX = 10

QUEST_COUNTER = {
    0: 7,
    1: 9,
    2: 9,
    3: 10,
    4: 10,
}

CATEGORY_KEYS = [
    "COLLECT_CATEGORY_BIOLOGICAL",
    "COLLECT_CATEGORY_COLLECTOR",
    "COLLECT_CATEGORY_HUNTING",
    "COLLECT_CATEGORY_BOSS",
    "COLLECT_CATEGORY_STONE",
]

_LOCATION_KEY_BY_MOBID = {
    101: "COLLECT_LOCATION_FIRST_CITIES",
    302: "COLLECT_LOCATION_FIRST_CITIES",        # Zaprzys. Lucznik (potworologia prog 1)
    502: "COLLECT_LOCATION_SECOND_CITIES",
    554: "COLLECT_LOCATION_SECOND_CITIES",       # Silny Dziki General (potworologia prog 2)
    591: "COLLECT_LOCATION_SECOND_CITIES",
    636: "COLLECT_LOCATION_ORC_VALLEY",
    731: "COLLECT_LOCATION_SECOND_CITIES",       # Elit. Ezot. Fanatyk (potworologia prog 4)
    1107: "COLLECT_LOCATION_FROZEN_LAND",        # Lodowy Golem (potworologia prog 5)
    2205: "COLLECT_LOCATION_FIRE_LAND",          # Ognisty Wojownik (potworologia prog 6)
    2314: "COLLECT_LOCATION_ENCHANTED_FOREST",   # Czerw. Duch Wierzby (potworologia prog 7)
    2401: "COLLECT_LOCATION_PHARAOH_DESERT",     # Wojownik Setaou (potworologia prog 8)
    8013: "COLLECT_LOCATION_FROZEN_LAND",        # Metin Smierci (metinologia prog 3)
    8025: "COLLECT_LOCATION_ENCHANTED_FOREST",   # Metin Ma-An (metinologia prog 4)
    8027: "COLLECT_LOCATION_ENCHANTED_FOREST",   # Metin Jeon-Un (metinologia prog 5)
    8028: "COLLECT_LOCATION_PHARAOH_DESERT",     # Metin Upadlych (metinologia prog 6)
    8207: "COLLECT_LOCATION_PHARAOH_DESERT",     # Starozytny Kamien (metinologia prog 8)
    691: "COLLECT_LOCATION_ORC_VALLEY",
    693: "COLLECT_LOCATION_ORC_VALLEY",           # Odrodzony Wodz Orkow (kolekcjoner prog 1)
    1901: "COLLECT_LOCATION_SECOND_CITIES",       # Dziewiec Ogonow - Sohan (kolekcjoner prog 3)
    2034: "COLLECT_LOCATION_SPIDER_CAVE",
    2092: "COLLECT_LOCATION_SPIDER_CAVE",         # Baronowna Pajakow (kolekcjoner prog 5)
    2206: "COLLECT_LOCATION_FIRE_LAND",           # Ognisty Krol (kolekcjoner prog 4 / bossologia prog 3)
    2771: "COLLECT_LOCATION_PHARAOH_DESERT",      # Straznik Yin (bossologia prog 6)
    2074: "COLLECT_LOCATION_SPIDER_CAVE",
    2075: "COLLECT_LOCATION_SPIDER_CAVE",
    2091: "COLLECT_LOCATION_SPIDER_CAVE",
    2095: "COLLECT_LOCATION_SPIDER_CAVE",
    3102: "COLLECT_LOCATION_CYCLOPS_VALLEY",
    3103: "COLLECT_LOCATION_CYCLOPS_VALLEY",
    3104: "COLLECT_LOCATION_CYCLOPS_VALLEY",
    3190: "COLLECT_LOCATION_CYCLOPS_VALLEY",
    3191: "COLLECT_LOCATION_CYCLOPS_VALLEY",
    3302: "COLLECT_LOCATION_ENCHANTED_FOREST",
    3304: "COLLECT_LOCATION_ENCHANTED_FOREST",
    3391: "COLLECT_LOCATION_ENCHANTED_FOREST",
    6002: "COLLECT_LOCATION_FIRE_LAND",
    6006: "COLLECT_LOCATION_FIRE_LAND",
    6775: "COLLECT_LOCATION_FROZEN_LAND",
    6779: "COLLECT_LOCATION_FROZEN_LAND",
    6781: "COLLECT_LOCATION_FROZEN_LAND",
    6789: "COLLECT_LOCATION_FROZEN_LAND",
    6798: "COLLECT_LOCATION_FROZEN_LAND",
    6801: "COLLECT_LOCATION_FIRE_LAND",
    6803: "COLLECT_LOCATION_ENCHANTED_FOREST",
    8006: "COLLECT_LOCATION_SECOND_CITIES",
    8008: "COLLECT_LOCATION_ORC_VALLEY",
    8052: "COLLECT_LOCATION_CYCLOPS_VALLEY",
    8210: "COLLECT_LOCATION_PHARAOH_DESERT",
    8213: "COLLECT_LOCATION_PHARAOH_DESERT",
    8214: "COLLECT_LOCATION_PHARAOH_DESERT",
    9671: "COLLECT_LOCATION_PHARAOH_DESERT",
    9673: "COLLECT_LOCATION_PHARAOH_DESERT",
    34600: "COLLECT_LOCATION_FIRE_LAND",
    34601: "COLLECT_LOCATION_FIRE_LAND",
    201001: "COLLECT_LOCATION_SWAMP",
    201003: "COLLECT_LOCATION_SWAMP",
    201004: "COLLECT_LOCATION_SWAMP",
    201005: "COLLECT_LOCATION_SWAMP",
    201008: "COLLECT_LOCATION_SWAMP",
    201009: "COLLECT_LOCATION_SWAMP",
    # === Biolog (Badania Biologa) - moby dropu (port MT2 Nostalgia) -> lokacje ===
    601: "COLLECT_LOCATION_ORC_VALLEY",          # Ork (lv30)
    631: "COLLECT_LOCATION_ORC_VALLEY",          # Elit. Ork (lv30 key)
    701: "COLLECT_LOCATION_SECOND_CITIES",       # Ezot. Fanatyk (lv40)
    731: "COLLECT_LOCATION_SECOND_CITIES",       # Elit. Ezot. Fanatyk (lv40 key)
    1001: "COLLECT_LOCATION_CYCLOPS_VALLEY",     # Demon Zolnierz (lv50)
    1093: "COLLECT_LOCATION_CYCLOPS_VALLEY",     # Umarly Rozpruwacz (lv90 key)
    1101: "COLLECT_LOCATION_FROZEN_LAND",        # Zaczarowany Lod (lv60)
    1135: "COLLECT_LOCATION_FROZEN_LAND",        # Podziemny Lod. Czlowiek (lv92)
    1137: "COLLECT_LOCATION_FROZEN_LAND",        # Podziemny Lodowy Golem (lv92)
    2301: "COLLECT_LOCATION_ENCHANTED_FOREST",   # Drzewo Duchow (lv70)
    2311: "COLLECT_LOCATION_ENCHANTED_FOREST",   # Czerwone Drzewo Duchow (lv85)
    2412: "COLLECT_LOCATION_PHARAOH_DESERT",     # Lucznik Setaou (lv94/96)
    2414: "COLLECT_LOCATION_PHARAOH_DESERT",     # Komendant Setaou (lv94/96)
    2493: "COLLECT_LOCATION_PHARAOH_DESERT",     # Beran-Setaou (lv94 key)
    2495: "COLLECT_LOCATION_PHARAOH_DESERT",     # (lv94 key alt)
}

# Bonus data: (category, tier, index) -> (item.APPLY_*, value)
# Uses the tooltip affect system for translations (AFFECT_DICT)
# Entries not present here resolve to COLLECT_BONUS_NONE ("-")
_BONUS_DATA = {
    # Category 0 - Biolog (zsynchronizowane z quest collectors/biologist.lua fixedreward/choicereward)
    # index = quest state: 0=lv30 1=lv40 2=lv50 3=lv60 4=lv70 5=lv80 6=lv85 7=lv90 8=lv92 9=lv94 10=lv96
    (0, 0, 0): (item.APPLY_ATTBONUS_MONSTER, 5),   # lv30: silny p.potworom +5
    (0, 1, 0): (item.APPLY_MOV_SPEED, 10),         # lv30: ruch +10
    (0, 0, 1): (item.APPLY_MOV_SPEED, 5),          # lv40: ruch +5
    (0, 0, 2): (item.APPLY_DEF_GRADE_BONUS, 60),   # lv50: obrona +60
    (0, 0, 3): (item.APPLY_ATT_GRADE_BONUS, 50),   # lv60: atak +50
    (0, 0, 4): (item.APPLY_MOV_SPEED, 11),         # lv70: ruch +11
    (0, 1, 4): (item.APPLY_DEF_GRADE_BONUS, 10),   # lv70: obrona +10
    (0, 0, 5): (item.APPLY_ATT_SPEED, 6),          # lv80: pr.ataku +6
    (0, 1, 5): (item.APPLY_ATT_GRADE_BONUS, 10),   # lv80: atak +10
    (0, 0, 6): (item.APPLY_RESIST_WARRIOR, 10),    # lv85: odpornosc na klasy graczy +10
    (0, 1, 6): (item.APPLY_RESIST_ASSASSIN, 10),
    (0, 2, 6): (item.APPLY_RESIST_SURA, 10),
    (0, 3, 6): (item.APPLY_RESIST_SHAMAN, 10),
    (0, 0, 7): (item.APPLY_ATTBONUS_WARRIOR, 8),   # lv90: silny p.klasom graczy +8
    (0, 1, 7): (item.APPLY_ATTBONUS_ASSASSIN, 8),
    (0, 2, 7): (item.APPLY_ATTBONUS_SURA, 8),
    (0, 3, 7): (item.APPLY_ATTBONUS_SHAMAN, 8),
    (0, 0, 8): (item.APPLY_MAX_HP, 1000),          # lv92 (wybor): HP / obrona / atak
    (0, 1, 8): (item.APPLY_DEF_GRADE_BONUS, 120),
    (0, 2, 8): (item.APPLY_ATT_GRADE_BONUS, 51),
    (0, 0, 9): (item.APPLY_MAX_HP, 1100),          # lv94 (wybor)
    (0, 1, 9): (item.APPLY_DEF_GRADE_BONUS, 140),
    (0, 2, 9): (item.APPLY_ATT_GRADE_BONUS, 60),
    (0, 0, 10): (item.APPLY_MAX_HP, 2000),         # lv96 (wybor)
    (0, 1, 10): (item.APPLY_DEF_GRADE_BONUS, 700),
    (0, 2, 10): (item.APPLY_ATT_GRADE_BONUS, 300),
    # Category 1 - Collector (zsynchronizowane z quest collectors/collector.lua -> reward)
    # index = prog 0..8; drugi indeks = kolejny bonus w ramach tego samego progu
    (1, 0, 0): (item.APPLY_ATTBONUS_DUNGEON, 5),        # prog 1: silny w lochach
    (1, 0, 1): (item.APPLY_ATTBONUS_BOSS, 5),           # prog 2: silny p. bossom
    (1, 0, 2): (item.APPLY_ATTBONUS_HUMAN, 5),          # prog 3: silny p. ludziom
    (1, 0, 3): (item.APPLY_ATTBONUS_MONSTER, 5),        # prog 4: silny p. potworom
    (1, 0, 4): (item.APPLY_NORMAL_HIT_DAMAGE_BONUS, 10),# prog 5: obr. zwyklego ataku
    (1, 0, 5): (item.APPLY_ATTBONUS_STONE, 5),          # prog 6: silny p. metinom
    (1, 0, 6): (item.APPLY_SKILL_DAMAGE_BONUS, 10),     # prog 7: obr. umiejetnosci
    (1, 0, 7): (item.APPLY_ATTBONUS_BOSS, 5),           # prog 8: silny p. bossom
    (1, 1, 7): (item.APPLY_FINAL_DMG_BONUS, 5),         # prog 8: finalne obrazenia
    (1, 0, 8): (item.APPLY_RESIST_KLASY, 10),           # prog 9: odpornosc na wszystkie klasy
    # Category 2 - Hunting/Potworologia (10 progow, bonus laczny +1 na prog)
    # Kill-based -> add_collect z override=True, wiec wartosc ZASTEPUJE poprzednia.
    (2, 0, 0): (item.APPLY_ATTBONUS_MONSTER, 1),
    (2, 0, 1): (item.APPLY_ATTBONUS_MONSTER, 2),
    (2, 0, 2): (item.APPLY_ATTBONUS_MONSTER, 3),
    (2, 0, 3): (item.APPLY_ATTBONUS_MONSTER, 4),
    (2, 0, 4): (item.APPLY_ATTBONUS_MONSTER, 5),
    (2, 0, 5): (item.APPLY_ATTBONUS_MONSTER, 6),
    (2, 0, 6): (item.APPLY_ATTBONUS_MONSTER, 7),
    (2, 0, 7): (item.APPLY_ATTBONUS_MONSTER, 8),
    (2, 0, 8): (item.APPLY_ATTBONUS_MONSTER, 9),
    (2, 0, 9): (item.APPLY_ATTBONUS_MONSTER, 10),
    # Category 3 - Bossology (6 progow, przyrost +1,+1,+1,+1,+2,+4)
    # Kill-based -> add_collect z override=True, wiec wartosc ZASTEPUJE poprzednia.
    (3, 0, 0): (item.APPLY_ATTBONUS_BOSS, 1),
    (3, 0, 1): (item.APPLY_ATTBONUS_BOSS, 2),
    (3, 0, 2): (item.APPLY_ATTBONUS_BOSS, 3),
    (3, 0, 3): (item.APPLY_ATTBONUS_BOSS, 4),
    (3, 0, 4): (item.APPLY_ATTBONUS_BOSS, 6),
    (3, 0, 5): (item.APPLY_ATTBONUS_BOSS, 10),
    # Category 4 - Metinology (8 progow, +1 na prog, na dwoch ostatnich +2)
    # Kill-based -> add_collect z override=True, wiec wartosc ZASTEPUJE poprzednia.
    (4, 0, 0): (item.APPLY_ATTBONUS_STONE, 1),
    (4, 0, 1): (item.APPLY_ATTBONUS_STONE, 2),
    (4, 0, 2): (item.APPLY_ATTBONUS_STONE, 3),
    (4, 0, 3): (item.APPLY_ATTBONUS_STONE, 4),
    (4, 0, 4): (item.APPLY_ATTBONUS_STONE, 5),
    (4, 0, 5): (item.APPLY_ATTBONUS_STONE, 6),
    (4, 0, 6): (item.APPLY_ATTBONUS_STONE, 8),
    (4, 0, 7): (item.APPLY_ATTBONUS_STONE, 10),
}


def _GetLocationName(mobId):
    """Get translated location name for a mob ID."""
    key = _LOCATION_KEY_BY_MOBID.get(mobId, "COLLECT_LOCATION_UNKNOWN")
    return getattr(localeInfo, key, "-")


def _GetCategoryName(index):
    """Get translated category name by index."""
    if 0 <= index < len(CATEGORY_KEYS):
        return getattr(localeInfo, CATEGORY_KEYS[index], "-")
    return "-"


def _GetBonusText(category, tier, index):
    """Get formatted bonus text using the tooltip affect system."""
    entry = _BONUS_DATA.get((category, tier, index))
    if not entry:
        return getattr(localeInfo, "COLLECT_BONUS_NONE", "-")
    affectType, affectValue = entry
    try:
        return uiToolTip.ItemToolTip.AFFECT_DICT[affectType](affectValue)
    except (TypeError, KeyError):
        return getattr(localeInfo, "COLLECT_BONUS_NONE", "-")


class CollectWindow(ui.ScriptWindow):
    def __init__(self):
        ui.ScriptWindow.__init__(self)
        self.isLoaded = 0
        self.tooltipItem = uiToolTip.ItemToolTip()
        self.selectedWindow = 0
        self.realwindow = 0
        self.data = {
            i: {
                "ITEM_VNUM": 0, "TIME": -1, "COUNT": 0, "COUNT_TOTAL": 0,
                "TAKE_CHANCE": 0, "RENDERTARGET_VNUM": 0, "QUEST_INDEX": 0,
                "REQUIRED_LEVEL": 0,
            }
            for i in range(len(constInfo.CollectWindowQID))
        }
        self.progress = {i: {"COMPLETED": 0} for i in range(len(constInfo.CollectWindowQID))}
        self.CategoryButtonList = []
        self.bonus_text = {}

        self.__LoadWindow()

    def __del__(self):
        ui.ScriptWindow.__del__(self)

    def __LoadWindow(self):
        if self.isLoaded == 1:
            return

        self.isLoaded = 1
        try:
            pyScrLoader = ui.PythonScriptLoader()
            pyScrLoader.LoadScriptFile(self, "uiscript/collectwindow.py")
        except:
            import exception
            exception.Abort("CollectWindow.LoadWindow.LoadObject")

        try:
            self.titleBar = self.GetChild("TitleBar")
            self.titleBar.SetCloseEvent(ui.__mem_func__(self.Close))

            for i in range(4):
                self.bonus_text[i] = self.GetChild("bonustext_{}".format(i))

            for i in range(len(constInfo.CollectWindowQID)):
                self.CategoryButtonList.append(self.GetChild("CategoryButton_%d" % i))
                self.CategoryButtonList[i].SetEvent(ui.__mem_func__(self.__ChangeCategory), i)

            self.header_text_main = self.GetChild("header_text_main")
            self.time_left = self.GetChild("time_left")
            self.item_count = self.GetChild("item_count")
            self.chance_text = self.GetChild("chance_text")
            self.ItemSlot = self.GetChild("item_slot")
            self.ItemSlot.SetOverInItemEvent(ui.__mem_func__(self.__OverInItem))
            self.ItemSlot.SetOverOutItemEvent(ui.__mem_func__(self.__OverOutItem))
            self.blocked_slot = self.GetChild("blocked_slot")

            self.render = self.GetChild("RenderTarget")
            self.location_text = self.GetChild("location_text")
            self.mobname_text = self.GetChild("mobname_text")

            self.collect_button = self.GetChild("collect_button")
            self.collect_button.SetEvent(ui.__mem_func__(self.__ClickCollectButton))
            self.time_button1 = self.GetChild("time_button1")
            self.chance_button = self.GetChild("chance_button")
            self.chance_button.SetEvent(ui.__mem_func__(self.__useitem), 0)
            self.time_button1.SetEvent(ui.__mem_func__(self.__useitem), 1)

            self.PageText = self.GetChild("PageText")
            self.PrevPageBtn = self.GetChild("PrevPageBtn")
            self.NextPageBtn = self.GetChild("NextPageBtn")

            self.PrevPageBtn.SetEvent(ui.__mem_func__(self.SendCommand), 0)
            self.NextPageBtn.SetEvent(ui.__mem_func__(self.SendCommand), 1)

            self.progressbar = self.GetChild("progressbar")

            self.lowlevel_bg = self.GetChild("lowlevel_bg")
            self.lowlevel_text = self.GetChild("lowlevel_text")
        except:
            import exception
            exception.Abort("CollectWindow.LoadWindow.BindObject")

        self.__ChangeCategory(self.selectedWindow)
        self.SetCenterPosition()

    def Open(self):
        self.__LoadWindow()
        ui.ScriptWindow.Show(self)

    def Show(self):
        self.__LoadWindow()
        ui.ScriptWindow.Show(self)

    def Close(self):
        # Podglad 3D musi zgasnac razem z oknem - dopoki render target jest "widoczny",
        # silnik deformuje jego model CO KLATKE (do 53 ms/klatke wg hitch_log).
        renderTarget.SetVisibility(RENDER_INDEX, False)
        self.Hide()

    def __ChangeCategory(self, category):
        self.realwindow = category
        self.selectedWindow = category

        for obj in self.CategoryButtonList:
            obj.Enable()
            obj.SetUp()

        if player.GetLevel() < self.data[self.selectedWindow]["REQUIRED_LEVEL"]:
            self.lowlevel_bg.Show()
            self.lowlevel_text.SetText(
                localeInfo.COLLECT_REQUIRED_LEVEL.format(self.data[self.selectedWindow]["REQUIRED_LEVEL"])
            )
        else:
            self.lowlevel_bg.Hide()

        self.header_text_main.SetText(_GetCategoryName(category))
        self.ItemSlot.SetItemSlot(0, self.data[category]["ITEM_VNUM"], 0)
        self.item_count.SetText("{}/{}".format(
            self.data[category]["COUNT"], self.data[category]["COUNT_TOTAL"]
        ))

        if category not in BLOCKED_CAT_LIST:
            self.chance_text.Show()
            self.time_left.Show()
            self.blocked_slot.Hide()
            self.collect_button.Show()
            self.chance_button.Show()
            self.time_button1.Show()
        else:
            self.chance_text.Hide()
            self.blocked_slot.Show()
            self.time_left.Hide()
            self.collect_button.Hide()
            self.chance_button.Hide()
            self.time_button1.Hide()

        renderTarget.SetBackground(RENDER_INDEX, "d:/ymir work/ui/game/myshop_deco/model_view_bg.sub")
        renderTarget.SetVisibility(RENDER_INDEX, True)

        vnum = self.data[category]["RENDERTARGET_VNUM"]
        quest_index = self.data[category]["QUEST_INDEX"]

        if vnum != 0:
            renderTarget.SelectModel(RENDER_INDEX, vnum)
            self.location_text.SetText(
                "|cFFf1e6c0{} |r{}".format(localeInfo.COLLECT_LOCATION_LABEL, _GetLocationName(vnum))
            )
            self.mobname_text.SetText(
                "{} |cFFa7ff33(Lv. {})".format(
                    nonplayer.GetMonsterName(vnum), nonplayer.GetMonsterLevel(vnum)
                )
            )
            for i in range(4):
                self.bonus_text[i].SetText(_GetBonusText(category, i, quest_index))
        else:
            renderTarget.SelectModel(RENDER_INDEX, -1)
            none_text = getattr(localeInfo, "COLLECT_BONUS_NONE", "-")
            self.location_text.SetText(
                "|cFFf1e6c0{} |r{}".format(localeInfo.COLLECT_LOCATION_LABEL, none_text)
            )
            self.mobname_text.SetText(none_text)
            for i in range(4):
                self.bonus_text[i].SetText(none_text)

        self.PageText.SetText(str(quest_index))
        self.progressbar.SetPercentage(self.data[category]["COUNT"], self.data[category]["COUNT_TOTAL"])

        self.CategoryButtonList[category].Disable()
        self.CategoryButtonList[category].Down()

    def SendCommand(self, type):
        qid = constInfo.CollectWindowQID[self.selectedWindow]
        questid = self.data[self.selectedWindow]["QUEST_INDEX"]

        if self.selectedWindow == 1:
            if type == 0:
                if questid <= 0:
                    return
                net.SendChatPacket("/choose_quest {} {}".format(questid - 1, qid))
                self.__ChangeCategory(self.selectedWindow)
            elif type == 1:
                if questid < 0 or questid >= 6:
                    return
                net.SendChatPacket("/choose_quest {} {}".format(questid + 1, qid))
                self.__ChangeCategory(self.selectedWindow)

            self.PageText.SetText(str(self.data[self.selectedWindow]["QUEST_INDEX"]))
        else:
            chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.COLLECT_COLLECTOR_ONLY_MESSAGE)

    def __OverInItem(self, slot_num):
        if self.tooltipItem:
            self.tooltipItem.ClearToolTip()
            self.tooltipItem.AddItemData(self.data[self.selectedWindow]["ITEM_VNUM"], 0, 0)

    def __OverOutItem(self):
        if self.tooltipItem:
            self.tooltipItem.ClearToolTip()
            self.tooltipItem.HideToolTip()

    def AddData(self, windowType, time, count, itemVnum, countTotal, chance, rendertargetvnum, questindex, requiredLevel):
        self.data[windowType]["ITEM_VNUM"] = itemVnum
        self.data[windowType]["TIME"] = max(0, app.GetTime() + time)
        self.data[windowType]["COUNT"] = count
        self.data[windowType]["COUNT_TOTAL"] = countTotal
        # Szansa jest losowana jako take_chance >= number(1, 100), wiec powyzej 100 nic sie nie zmienia.
        # Tniemy do 100 takze tutaj, zeby stare flagi (np. 140 z czasow bez capa) nie straszyly w UI.
        self.data[windowType]["TAKE_CHANCE"] = min(int(chance), 100)
        self.data[windowType]["RENDERTARGET_VNUM"] = rendertargetvnum
        self.data[windowType]["QUEST_INDEX"] = questindex
        self.data[windowType]["REQUIRED_LEVEL"] = requiredLevel
        self.quest = questindex
        self.__ChangeCategory(self.realwindow)

    def OnUpdate(self):
        if self.selectedWindow not in BLOCKED_CAT_LIST:
            remaining = max(float(self.data[self.selectedWindow]["TIME"]) - app.GetTime(), 0)
            self.time_left.SetText(time.strftime("%H:%M:%S", time.gmtime(remaining)))
            self.chance_text.SetText("{}%".format(self.data[self.selectedWindow]["TAKE_CHANCE"]))

    def __ClickCollectButton(self):
        qid = constInfo.CollectWindowQID[self.selectedWindow]
        event.QuestButtonClick(qid, 1)

    def __useitem(self, value):
        # value: 0 = przycisk szansy, 1 = przycisk skrocenia czasu
        if value == 0:
            items_to_search = CHANCE_ITEM_BY_CAT.get(self.selectedWindow)
        elif value == 1:
            items_to_search = TIME_ITEM_ORDER
        else:
            return

        if not items_to_search:
            return

        inventory_ranges = [
            range(player.INVENTORY_PAGE_SIZE * player.INVENTORY_PAGE_COUNT),
            range(820, 954),
        ]

        for item_to_search in items_to_search:
            for inventory_range in inventory_ranges:
                for i in inventory_range:
                    if player.GetItemIndex(i) == item_to_search:
                        net.SendItemUsePacket(i)
                        return

    def SendTime(self, val, time):
        val = int(val)
        time_conv = float(time)
        if val in (0, 1):
            self.data[val]["TIME"] = max(0, app.GetTime() + time_conv)

    def SendChance(self, val, chance):
        val = int(val)
        if val in (0, 1):
            self.data[val]["TAKE_CHANCE"] = min(int(chance), 100)

    def OnPressEscapeKey(self):
        self.Close()
        return True

    def OnPressExitKey(self):
        self.Close()
        return True
