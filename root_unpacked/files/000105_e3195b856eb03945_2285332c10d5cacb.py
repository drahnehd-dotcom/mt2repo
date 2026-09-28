# -*- coding: utf-8 -*-
"""
Costume set preview data synchronized with the `packages` quest.

Only deterministic package previews live here. Multi-branch packages such as
50160-50168 are intentionally omitted until the tooltip supports branch-aware
previews instead of a single static render. When the quest mapping drifts from
the live client assets, the preview uses the verified client-side set.
"""


def _build_weapon_map(weapon_choices):
    result = {
        "sword": 0,
        "twohand": 0,
        "dagger": 0,
        "bow": 0,
        "sura_sword": 0,
        "bell": 0,
        "fan": 0,
    }

    # Quest order:
    # sword, dagger, bow, twohand, bell, fan, sura_sword(optional)
    order = ("sword", "dagger", "bow", "twohand", "bell", "fan", "sura_sword")
    for index, weapon_vnum in enumerate(weapon_choices):
        if index >= len(order):
            break
        result[order[index]] = weapon_vnum

    # Some older packages do not provide a dedicated sura weapon.
    if not result["sura_sword"]:
        result["sura_sword"] = result["sword"]

    return result


def _build_set(hair_vnum, body_vnum, acce_vnum, weapon_choices=()):
    return {
        "hair_vnum": hair_vnum,
        "body_vnum": body_vnum,
        "acce_vnum": acce_vnum,
        "weapons": _build_weapon_map(weapon_choices),
    }


class CostumeSet:
    """Represents a costume set for one gender."""

    def __init__(self, hair_vnum, body_vnum, acce_vnum, weapons):
        self.hair_vnum = hair_vnum
        self.body_vnum = body_vnum
        self.acce_vnum = acce_vnum
        self.weapons = weapons

    def get_weapon(self, weapon_type):
        return self.weapons.get(weapon_type, 0)


class CostumeSetEntry:
    """Represents a costume set entry with male and female variants."""

    def __init__(self, item_vnum, male_data, female_data):
        self.item_vnum = item_vnum
        self.male = CostumeSet(**male_data)
        self.female = CostumeSet(**female_data)

    def get_for_gender(self, is_male):
        return self.male if is_male else self.female


QUEST_PACKAGE_SET_DATA = {
    50180: {
        "male": _build_set(52914, 41968, 85523, (40731, 40732, 40733, 40734, 40735, 40736)),
        "female": _build_set(52914, 41969, 85523, (40731, 40732, 40733, 40734, 40735, 40736)),
    },
    50181: {
        "male": _build_set(46022, 41726, 85552, (40682, 40683, 40684, 40685, 40686, 40687)),
        "female": _build_set(46023, 41727, 85552, (40682, 40683, 40684, 40685, 40686, 40687)),
    },
    50182: {
        "male": _build_set(45992, 41996, 85537),
        "female": _build_set(45993, 41997, 85537),
    },
    50183: {
        "male": _build_set(45994, 41998, 85538, (40577, 40578, 40579, 40580, 40581, 40582, 40583)),
        "female": _build_set(45995, 41999, 85538, (40577, 40578, 40579, 40580, 40581, 40582, 40583)),
    },
    50184: {
        "male": _build_set(45996, 41700, 85539, (40584, 40585, 40586, 40587, 40588, 40589, 40590)),
        "female": _build_set(45997, 41701, 85539, (40584, 40585, 40586, 40587, 40588, 40589, 40590)),
    },
    50185: {
        "male": _build_set(45964, 41964, 85521, (40717, 40718, 40719, 40720, 40721, 40722)),
        "female": _build_set(45965, 41965, 85521, (40717, 40718, 40719, 40720, 40721, 40722)),
    },
    50186: {
        "male": _build_set(0, 41966, 85522, (40724, 40725, 40726, 40727, 40728, 40729)),
        "female": _build_set(0, 41967, 85522, (40724, 40725, 40726, 40727, 40728, 40729)),
    },
    50187: {
        "male": _build_set(45926, 41926, 85503, (40940, 40941, 40942, 40943, 40944, 40945)),
        "female": _build_set(45927, 41927, 85503, (40940, 40941, 40942, 40943, 40944, 40945)),
    },
    50188: {
        "male": _build_set(45932, 41932, 85506, (40970, 40971, 40972, 40973, 40974, 40975)),
        "female": _build_set(45933, 41933, 85506, (40970, 40971, 40972, 40973, 40974, 40975)),
    },
    50189: {
        "male": _build_set(45934, 41934, 85507, (40980, 40981, 40982, 40983, 40984, 40985)),
        "female": _build_set(45935, 41935, 85507, (40980, 40981, 40982, 40983, 40984, 40985)),
    },
    50190: {
        "male": _build_set(45936, 41936, 85508, (40990, 40991, 40992, 40993, 40994, 40995)),
        "female": _build_set(45937, 41937, 85508, (40990, 40991, 40992, 40993, 40994, 40995)),
    },
    50191: {
        "male": _build_set(45938, 41938, 85509, (40800, 40801, 40802, 40803, 40804, 40805)),
        "female": _build_set(45939, 41939, 85509, (40800, 40801, 40802, 40803, 40804, 40805)),
    },
    50192: {
        "male": _build_set(45940, 41940, 85510, (40810, 40811, 40812, 40813, 40814, 40815)),
        "female": _build_set(45941, 41941, 85510, (40810, 40811, 40812, 40813, 40814, 40815)),
    },
    50193: {
        "male": _build_set(45942, 41942, 85511, (40820, 40821, 40822, 40823, 40824, 40825)),
        "female": _build_set(45943, 41943, 85511, (40820, 40821, 40822, 40823, 40824, 40825)),
    },
    50194: {
        "male": _build_set(45944, 41944, 85512, (40830, 40831, 40832, 40833, 40834, 40835)),
        "female": _build_set(45945, 41945, 85512, (40830, 40831, 40832, 40833, 40834, 40835)),
    },
    50195: {
        "male": _build_set(45946, 41946, 85513, (40840, 40841, 40842, 40843, 40844, 40845)),
        "female": _build_set(45947, 41947, 85513, (40840, 40841, 40842, 40843, 40844, 40845)),
    },
    50196: {
        "male": _build_set(45948, 41948, 85514, (40850, 40851, 40852, 40853, 40854, 40855)),
        "female": _build_set(45949, 41949, 85514, (40850, 40851, 40852, 40853, 40854, 40855)),
    },
    50197: {
        "male": _build_set(45950, 41950, 85515, (40860, 40861, 40862, 40863, 40864, 40865)),
        "female": _build_set(45951, 41951, 85515, (40860, 40861, 40862, 40863, 40864, 40865)),
    },
    50198: {
        "male": _build_set(45952, 41952, 85516, (40870, 40871, 40872, 40873, 40874, 40875)),
        "female": _build_set(45953, 41953, 85516, (40870, 40871, 40872, 40873, 40874, 40875)),
    },
    50199: {
        "male": _build_set(45900, 41900, 85500, (40900, 40901, 40902, 40903, 40904, 40905)),
        "female": _build_set(45901, 41901, 85500, (40900, 40901, 40902, 40903, 40904, 40905)),
    },
    50210: {
        "male": _build_set(45998, 41702, 85540, (40591, 40592, 40593, 40594, 40595, 40596, 40597)),
        "female": _build_set(45999, 41703, 85540, (40591, 40592, 40593, 40594, 40595, 40596, 40597)),
    },
    50211: {
        "male": _build_set(46000, 41704, 85541, (40598, 40599, 40600, 40601, 40602, 40603, 40604)),
        "female": _build_set(46001, 41705, 85541, (40598, 40599, 40600, 40601, 40602, 40603, 40604)),
    },
    90042: {
        "male": _build_set(45972, 41976, 85527, (40500, 40501, 40502, 40503, 40504, 40505, 40506)),
        "female": _build_set(45973, 41977, 85527, (40500, 40501, 40502, 40503, 40504, 40505, 40506)),
    },
    90043: {
        "male": _build_set(45998, 41702, 85540, (40591, 40592, 40593, 40594, 40595, 40596, 40597)),
        "female": _build_set(45999, 41703, 85540, (40591, 40592, 40593, 40594, 40595, 40596, 40597)),
    },
    90044: {
        "male": _build_set(45978, 41982, 85530, (40521, 40522, 40523, 40524, 40525, 40526, 40527)),
        "female": _build_set(45979, 41983, 85530, (40521, 40522, 40523, 40524, 40525, 40526, 40527)),
    },
    90045: {
        "male": _build_set(45980, 41984, 85531, (40528, 40529, 40530, 40531, 40532, 40533, 40534)),
        "female": _build_set(45981, 41985, 85531, (40528, 40529, 40530, 40531, 40532, 40533, 40534)),
    },
    90046: {
        "male": _build_set(45982, 41986, 85532, (40535, 40536, 40537, 40538, 40539, 40540, 40541)),
        "female": _build_set(45983, 41987, 85532, (40535, 40536, 40537, 40538, 40539, 40540, 40541)),
    },
    90052: {
        "male": _build_set(45928, 41928, 85504, (40950, 40951, 40952, 40953, 40954, 40955, 40956)),
        "female": _build_set(45929, 41929, 85504, (40950, 40951, 40952, 40953, 40954, 40955, 40956)),
    },
    90053: {
        "male": _build_set(45930, 41930, 85505, (40960, 40961, 40962, 40963, 40964, 40965, 40966)),
        "female": _build_set(45931, 41931, 85505, (40960, 40961, 40962, 40963, 40964, 40965, 40966)),
    },
    90054: {
        "male": _build_set(45974, 41978, 85528),
        "female": _build_set(45975, 41979, 85528),
    },
    90055: {
        "male": _build_set(45958, 41958, 85519),
        "female": _build_set(45959, 41959, 85519),
    },
    90056: {
        "male": _build_set(45960, 41960, 85520),
        "female": _build_set(45961, 41961, 85520),
    },
    90070: {
        "male": _build_set(45984, 41988, 85533, (40542, 40543, 40544, 40545, 40546, 40547)),
        "female": _build_set(45985, 41989, 85533, (40542, 40543, 40544, 40545, 40546, 40547)),
    },
    90072: {
        "male": _build_set(45990, 41994, 85536, (40563, 40564, 40565, 40566, 40567, 40568)),
        "female": _build_set(45991, 41995, 85536, (40563, 40564, 40565, 40566, 40567, 40568)),
    },
}


class CostumeSetManager:
    """Manages all deterministic costume package previews."""

    def __init__(self):
        self._sets = {}
        self._load_data()

    def _add_set(self, vnum, male, female):
        self._sets[vnum] = CostumeSetEntry(vnum, male, female)

    def _load_data(self):
        for vnum, data in QUEST_PACKAGE_SET_DATA.items():
            self._add_set(vnum, data["male"], data["female"])

    def has_set(self, item_vnum):
        return item_vnum in self._sets

    def get_set(self, item_vnum):
        return self._sets.get(item_vnum)

    def get_for_gender(self, item_vnum, is_male):
        entry = self._sets.get(item_vnum)
        if entry:
            return entry.get_for_gender(is_male)
        return None


_costume_manager = None


def get_costume_manager():
    global _costume_manager
    if _costume_manager is None:
        _costume_manager = CostumeSetManager()
    return _costume_manager
