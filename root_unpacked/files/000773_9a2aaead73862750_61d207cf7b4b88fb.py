# -*- coding: utf-8 -*-
# author: dracaryS (adaptacja py3 / Kowal)

# static
import ui, dbg, mouseModule, constInfo, localeInfo

# dynamic
import item, player, miniMap, chat, net, nonplayer, skill

# === LOCAL AUTO HUNT CORE (embedded; no standalone localAutoHunt import) ===
import re
import math
import app
import chr
import chrmgr

# ---------- user-tunable configuration ----------

ENABLED = True

# Farm Mobow = normalne podejscie, bez teleportowania.
LOCAL_TELEPORT = False

# Existing UI range is expressed in the Auto Hunt UI as metres-like units.
# Client world coordinates use a larger unit scale, so keep this conversion
# configurable.
RANGE_TO_WORLD = 100.0

DEFAULT_RANGE_UI = 60.0
MIN_RANGE_WORLD = 0.0
MAX_RANGE_WORLD = 8000.0

# Nie teleportuj do moba, gdy jest juz w zasiegu normalnego ataku.
ATTACK_DISTANCE_WORLD = 250.0

# Wszystkie teleporty Auto Hunt, zarowno do punktu F8, jak i do Metina,
# sa ograniczone do maksymalnie 1 teleportu / 2 sekundy.
TELEPORT_COOLDOWN = 2.0

# Po teleportacji do punktu F8 daj klientowi chwile na zaktualizowanie
# widocznych obiektow przed skanem Metinow.
METIN_SCAN_DELAY = 0.35

# Scan existing character VIDs incrementally instead of blocking one frame.
VID_SCAN_MIN = 1
VID_SCAN_MAX = 200000
VID_SCAN_CHUNK = 15000
VID_SCAN_INTERVAL = 0.01

# Re-score targets frequently, but not every render tick.
TARGET_REFRESH_INTERVAL = 0.035

# Normalny ruch do moba: ponawiaj komendę ruchu, ale nie atakuj dopóki cel
# nie znajdzie się w zasięgu ataku.
MOVE_RETRY_INTERVAL = 0.25

# Pickup once a target disappears/dies.
AUTO_PICKUP_AFTER_KILL = True
PICKUP_COOLDOWN = 0.10
AUTO_ITEM_USE_COOLDOWN = 5.0

# If the server creates a target outside our current scan window, a currently
# selected/picked enemy is accepted immediately as a seed.
USE_PICKED_TARGET_FALLBACK = True

# ---------- state ----------

_running = False
_target_vid = 0
_range_ui = DEFAULT_RANGE_UI

_last_scan_time = 0.0
_scan_vid = VID_SCAN_MIN

_last_target_refresh = 0.0
_last_move_time = -9999.0
_last_teleport_time = -9999.0
_last_pickup_time = 0.0
_last_auto_item_use_time = -9999.0
_selected_auto_item_slot = -1
_selected_auto_item_vnum = 0
_movement_key_down = False
_last_move_target_vid = 0
_last_move_position = None

_known_vids = set()
_target_snapshot = []
_last_snapshot_time = -9999.0
_MOB_VNUM_CACHE = {}


# ---------------------------------------------------------------------------
# AUTO SKILLS
# ---------------------------------------------------------------------------
_AUTO_SKILLS_ENABLED = False
_AUTO_SKILL_SLOTS = [None] * 6
_AUTO_SKILL_ACTIVE = [False] * 6
_AUTO_SKILL_LAST_USE = [0.0] * 6
_AUTO_SKILL_REMOUNT_AT = 0.0
_AUTO_SKILL_REMOUNT_PENDING = False
_AUTO_SKILL_WAS_MOUNTED = False
_AUTO_SKILL_RETRY = 0.15
_AUTO_SKILL_MOUNT_WAIT = 0.45
_AUTO_SKILL_MOUNT_ATTACK_ALLOWED = False
_TARGET_HP_CACHE = {}

try:
    _saved_auto_skill_cfg = getattr(constInfo, 'AUTO_HUNT_SKILL_CONFIG', None)
    if isinstance(_saved_auto_skill_cfg, dict):
        _AUTO_SKILL_SLOTS[:] = list(_saved_auto_skill_cfg.get('slots', [None] * 6))[:6]
        _AUTO_SKILL_SLOTS.extend([None] * (6 - len(_AUTO_SKILL_SLOTS)))
        _AUTO_SKILL_ACTIVE[:] = list(_saved_auto_skill_cfg.get('active', [False] * 6))[:6]
        _AUTO_SKILL_ACTIVE.extend([False] * (6 - len(_AUTO_SKILL_ACTIVE)))
        _AUTO_SKILLS_ENABLED = bool(_saved_auto_skill_cfg.get('enabled', False))
except Exception:
    pass


def _save_auto_skill_config():
    try:
        constInfo.AUTO_HUNT_SKILL_CONFIG = {
            'slots': list(_AUTO_SKILL_SLOTS),
            'active': list(_AUTO_SKILL_ACTIVE),
            'enabled': bool(_AUTO_SKILLS_ENABLED),
        }
    except Exception:
        pass


def SetAutoSkillsEnabled(enabled):
    global _AUTO_SKILLS_ENABLED
    _AUTO_SKILLS_ENABLED = bool(enabled)
    _save_auto_skill_config()
    _say('Auto Skile: %s' % ('ON' if _AUTO_SKILLS_ENABLED else 'OFF'))


def IsAutoSkillsEnabled():
    return bool(_AUTO_SKILLS_ENABLED)


def SetAutoSkillSlot(index, skill_slot, active=True):
    try:
        index = int(index)
        skill_slot = int(skill_slot)
    except Exception:
        return
    if index < 0 or index >= 6 or skill_slot < 0:
        return
    # Avoid duplicate assignment. One skill can occupy one Auto Skill slot only.
    for i in range(6):
        if i != index and _AUTO_SKILL_SLOTS[i] == skill_slot:
            _AUTO_SKILL_SLOTS[i] = None
    _AUTO_SKILL_SLOTS[index] = skill_slot
    _AUTO_SKILL_ACTIVE[index] = bool(active)
    _save_auto_skill_config()


def ClearAutoSkillSlot(index):
    try:
        index = int(index)
    except Exception:
        return
    if 0 <= index < 6:
        _AUTO_SKILL_SLOTS[index] = None
        _AUTO_SKILL_ACTIVE[index] = False
        _save_auto_skill_config()


def SetAutoSkillActive(index, active):
    try:
        index = int(index)
    except Exception:
        return
    if 0 <= index < 6 and _AUTO_SKILL_SLOTS[index] is not None:
        _AUTO_SKILL_ACTIVE[index] = bool(active)
        _save_auto_skill_config()


def SetAutoSkillSourceSlot(source_slot, active=True):
    """Select/unselect a native character skill source slot for Auto Skills.

    The V/Umiejetnosci window supplies the authoritative source slot number, so
    the farm/AutoHunt code can use exactly the same cooldown and active state as
    the native skill UI.
    """
    try:
        source_slot = int(source_slot)
    except Exception:
        return False

    existing = None
    for i in range(6):
        if _AUTO_SKILL_SLOTS[i] == source_slot:
            existing = i
            break

    if not active:
        if existing is not None:
            _AUTO_SKILL_SLOTS[existing] = None
            _AUTO_SKILL_ACTIVE[existing] = False
            _AUTO_SKILL_LAST_USE[existing] = 0.0
            _save_auto_skill_config()
        return True

    if existing is not None:
        _AUTO_SKILL_ACTIVE[existing] = True
        _save_auto_skill_config()
        return True

    free = None
    for i in range(6):
        if _AUTO_SKILL_SLOTS[i] is None:
            free = i
            break
    if free is None:
        # Prefer an inactive slot over replacing a running skill.
        for i in range(6):
            if not _AUTO_SKILL_ACTIVE[i]:
                free = i
                break
    if free is None:
        _say('Auto Skile: wszystkie 6 miejsc jest zajete.')
        return False

    _AUTO_SKILL_SLOTS[free] = source_slot
    _AUTO_SKILL_ACTIVE[free] = True
    _AUTO_SKILL_LAST_USE[free] = 0.0
    _save_auto_skill_config()
    return True


def IsAutoSkillSourceSelected(source_slot):
    try:
        source_slot = int(source_slot)
    except Exception:
        return False
    for i in range(6):
        if _AUTO_SKILL_SLOTS[i] == source_slot and _AUTO_SKILL_ACTIVE[i]:
            return True
    return False


def SetAutoSkillMaster(enabled):
    SetAutoSkillsEnabled(bool(enabled))


def _collect_character_skills(max_slots=256):
    """Return character skill source slots available to Auto Skills.

    Do not use CanUseSkill() as a hard filter here: offensive skills often report
    False until a target is selected or the character is positioned correctly.
    Skill type + positive level are sufficient to populate the configuration.
    """
    result = []
    seen = set()
    excluded_indexes = set()
    for name in (
        "SKILL_INDEX_RIDING", "SKILL_INDEX_FISHING", "SKILL_INDEX_MINING",
        "SKILL_INDEX_TONGSOL", "SKILL_INDEX_LANGUAGE",
    ):
        try:
            value = int(getattr(player, name))
            if value > 0:
                excluded_indexes.add(value)
        except Exception:
            pass

    active_type = getattr(skill, "SKILL_TYPE_ACTIVE", None)
    support_type = getattr(skill, "SKILL_TYPE_SUPPORT", None)

    for slot_index in range(int(max_slots)):
        try:
            skill_index = int(player.GetSkillIndex(slot_index))
            skill_level = abs(int(player.GetSkillLevel(slot_index)))
            if skill_index <= 0 or skill_level <= 0:
                continue
            if skill_index in excluded_indexes or skill_index in seen:
                continue

            skill_type = None
            try:
                skill_type = skill.GetSkillType(skill_index)
            except Exception:
                pass

            # Only reject an explicit passive/non-combat type. Unknown types are
            # kept because custom server skills frequently do not export their
            # type constants to Python.
            if skill_type is not None and active_type is not None and support_type is not None:
                if skill_type not in (active_type, support_type):
                    continue

            try:
                name = skill.GetSkillName(skill_index)
            except Exception:
                name = str(skill_index)

            kind = _auto_skill_kind(slot_index, skill_index)
            result.append((slot_index, skill_index, skill_level, str(name), kind))
            seen.add(skill_index)
        except Exception:
            continue

    # Offensive skills first, then toggle/support skills. This gives a useful
    # default setup while still allowing manual re-ordering.
    result.sort(key=lambda item: (0 if item[4] == 'attack' else 1, item[0]))
    return result

def LoadCharacterAutoSkills(force=True, max_slots=6):
    """Load the character's combat/toggle skills into the six Auto Skill slots."""
    try:
        candidates = _collect_character_skills(max_slots=256)
        if not candidates:
            _say('Nie znaleziono skili bojowych/bufow postaci.')
            return []

        chosen = candidates[:int(max_slots)]
        for i in range(6):
            if i < len(chosen):
                source_slot, skill_index, skill_level, skill_name, kind = chosen[i]
                _AUTO_SKILL_SLOTS[i] = int(source_slot)
                _AUTO_SKILL_ACTIVE[i] = True
            else:
                _AUTO_SKILL_SLOTS[i] = None
                _AUTO_SKILL_ACTIVE[i] = False
            _AUTO_SKILL_LAST_USE[i] = 0.0

        _save_auto_skill_config()
        _say('Wczytano skile postaci: %s' % ', '.join(x[3] for x in chosen))
        return chosen
    except Exception as exc:
        _say('Nie mozna wczytac skili postaci: %s' % (exc,))
        return []

def GetAutoSkillConfig():
    return list(_AUTO_SKILL_SLOTS), list(_AUTO_SKILL_ACTIVE)

def SetAutoSkillAttackOnMount(enabled):
    """Tell Auto Skills whether attack skills may be cast while mounted.

    Farm mode sets this per current target. Toggle/support skills still require
    dismounting even when attack skills are allowed from horseback.
    """
    global _AUTO_SKILL_MOUNT_ATTACK_ALLOWED
    _AUTO_SKILL_MOUNT_ATTACK_ALLOWED = bool(enabled)


def IsAutoSkillAttackOnMountAllowed():
    return bool(_AUTO_SKILL_MOUNT_ATTACK_ALLOWED)


def _auto_skill_kind(slot_index, skill_index=None):
    try:
        if skill_index is None:
            skill_index = int(player.GetSkillIndex(int(slot_index)))
        if skill.IsToggleSkill(int(skill_index)):
            return "buff"
    except Exception:
        pass
    try:
        skill_type = skill.GetSkillType(int(skill_index))
        if skill_type == getattr(skill, 'SKILL_TYPE_ACTIVE', object()):
            return "attack"
    except Exception:
        pass
    return "buff"


def _auto_skill_has_target():
    for getter in (getattr(player, 'GetTargetVID', None), getattr(chrmgr, 'GetPickedVID', None)):
        if getter:
            try:
                vid = int(getter())
                if vid > 0 and chr.HasInstance(vid):
                    if hasattr(player, 'CanAttackInstance'):
                        return bool(player.CanAttackInstance(vid))
                    return True
            except Exception:
                pass
    return False


def OnTargetHPUpdate(vid, min_hp, max_hp):
    try:
        _TARGET_HP_CACHE[int(vid)] = (int(min_hp), int(max_hp), _now())
    except Exception:
        pass


def GetTargetHP(vid):
    try:
        return _TARGET_HP_CACHE.get(int(vid))
    except Exception:
        return None


def _auto_skill_can_cast(slot_index):
    try:
        skill_index = int(player.GetSkillIndex(int(slot_index)))
        if skill_index <= 0 or int(player.GetSkillLevel(int(slot_index))) <= 0:
            return False, skill_index
    except Exception:
        return False, 0

    try:
        if player.IsSkillCoolTime(int(slot_index)):
            return False, skill_index
    except Exception:
        pass

    try:
        if not skill.CanUseSkill(skill_index):
            return False, skill_index
    except Exception:
        pass

    return True, skill_index


def _auto_skill_update(now):
    global _AUTO_SKILL_REMOUNT_AT, _AUTO_SKILL_REMOUNT_PENDING, _AUTO_SKILL_WAS_MOUNTED

    if not _AUTO_SKILLS_ENABLED:
        return

    # Remount only after a temporary dismount caused by a buff/attack skill and
    # only if the current farm context still permits horseback combat.
    if _AUTO_SKILL_REMOUNT_PENDING and now >= _AUTO_SKILL_REMOUNT_AT:
        try:
            if _AUTO_SKILL_MOUNT_ATTACK_ALLOWED and not player.IsMountingHorse():
                net.SendChatPacket('/user_horse_ride')
        except Exception:
            pass
        _AUTO_SKILL_REMOUNT_PENDING = False
        _AUTO_SKILL_WAS_MOUNTED = False

    for i in range(6):
        if not _AUTO_SKILL_ACTIVE[i]:
            continue
        slot_index = _AUTO_SKILL_SLOTS[i]
        if slot_index is None:
            continue
        if now - _AUTO_SKILL_LAST_USE[i] < _AUTO_SKILL_RETRY:
            continue

        can_cast, skill_index = _auto_skill_can_cast(slot_index)
        if not can_cast:
            continue

        kind = _auto_skill_kind(slot_index, skill_index)
        if kind == 'attack' and not _auto_skill_has_target():
            continue

        # Toggle buffs such as Aura / Enchanted Blade / Dragon Assistance should
        # not be recast while already active.
        if kind == 'buff':
            try:
                if player.IsSkillActive(int(slot_index)):
                    continue
            except Exception:
                pass

        try:
            was_mounted = bool(player.IsMountingHorse())
        except Exception:
            was_mounted = False

        if was_mounted and (kind == 'buff' or not _AUTO_SKILL_MOUNT_ATTACK_ALLOWED):
            try:
                net.SendChatPacket('/unmount')
            except Exception:
                continue
            _AUTO_SKILL_WAS_MOUNTED = True
            _AUTO_SKILL_REMOUNT_PENDING = True
            _AUTO_SKILL_REMOUNT_AT = now + _AUTO_SKILL_MOUNT_WAIT
            _AUTO_SKILL_LAST_USE[i] = now
            continue

        try:
            player.ClickSkillSlot(int(slot_index))
            _AUTO_SKILL_LAST_USE[i] = now
            _say('Auto Skill: slot=%d skill=%d %s' % (int(slot_index), int(skill_index), kind))
            if _AUTO_SKILL_WAS_MOUNTED:
                _AUTO_SKILL_REMOUNT_PENDING = True
                _AUTO_SKILL_REMOUNT_AT = now + _AUTO_SKILL_MOUNT_WAIT
            return
        except Exception:
            continue

def AutoSkillTick():
    _auto_skill_update(_now())


_position_re = re.compile(r"pos=\((-?\d+),\s*(-?\d+)\)")
_alive_re = re.compile(r"isAlive=(\d+)")
_dead_re = re.compile(r"isDead=(\d+)")

_orig_create = None
_orig_delete = None
_hooks_installed = False


def _now():
    try:
        return float(app.GetTime())
    except Exception:
        return 0.0


def _set_const_status(value):
    try:
        import constInfo
        constInfo.AUTO_HUNT_ACTIVE = 1 if value else 0
    except Exception:
        pass


def _say(msg):
    try:
        chat.AppendChat(chat.CHAT_TYPE_INFO, "[Local AutoHunt] " + str(msg))
    except Exception:
        pass


def IsRunning():
    return bool(_running)


def GetTargetVID():
    return int(_target_vid or 0)


def ConfigureRange(ui_range):
    global _range_ui
    try:
        value = float(ui_range)
    except Exception:
        value = DEFAULT_RANGE_UI

    if value <= 0:
        value = DEFAULT_RANGE_UI

    _range_ui = value


def _range_world():
    # Auto Hunt range is the single source of truth for target selection and
    # teleport authorization. Do not silently expand a zero/small UI range.
    value = _range_ui * RANGE_TO_WORLD
    if value < MIN_RANGE_WORLD:
        value = MIN_RANGE_WORLD
    if value > MAX_RANGE_WORLD:
        value = MAX_RANGE_WORLD
    return value


def _install_instance_hooks():
    """
    Cache VIDs passed through the public chr.CreateInstance/DeleteInstance API.
    Network-side character creation may happen natively, so the incremental
    scanner remains the authoritative fallback.
    """
    global _orig_create, _orig_delete, _hooks_installed

    if _hooks_installed:
        return

    try:
        if hasattr(chr, "CreateInstance") and hasattr(chr, "DeleteInstance"):
            _orig_create = chr.CreateInstance
            _orig_delete = chr.DeleteInstance

            def _create_hook(vid, *args):
                try:
                    _known_vids.add(int(vid))
                except Exception:
                    pass
                return _orig_create(vid, *args)

            def _delete_hook(vid, *args):
                try:
                    _known_vids.discard(int(vid))
                except Exception:
                    pass
                return _orig_delete(vid, *args)

            chr.CreateInstance = _create_hook
            chr.DeleteInstance = _delete_hook
            _hooks_installed = True
    except Exception:
        _hooks_installed = False


# Install instance hooks during module import so mobs created before START are cached too.
# The fallback VID scanner remains active for builds where character creation happens natively.
try:
    _install_instance_hooks()
except Exception:
    pass


def _main_vid():
    try:
        return int(player.GetMainCharacterIndex())
    except Exception:
        return 0


def _is_instance(vid):
    try:
        return bool(chr.HasInstance(int(vid)))
    except Exception:
        return False


def _is_enemy(vid):
    try:
        return bool(chr.IsEnemy(int(vid)))
    except Exception:
        return False


def _is_attackable(vid):
    try:
        return bool(player.CanAttackInstance(int(vid)))
    except Exception:
        return _is_enemy(vid)


def _distance(vid):
    try:
        return float(player.GetCharacterDistance(int(vid)))
    except Exception:
        return 10 ** 9


def _vid_info(vid):
    try:
        return str(chrmgr.GetVIDInfo(int(vid)))
    except Exception:
        return ""


def _get_vid_state(vid):
    info = _vid_info(vid)

    alive = None
    dead = None
    pos = None

    match = _alive_re.search(info)
    if match:
        alive = int(match.group(1)) != 0

    match = _dead_re.search(info)
    if match:
        dead = int(match.group(1)) != 0

    match = _position_re.search(info)
    if match:
        pos = (int(match.group(1)), int(match.group(2)))

    return alive, dead, pos, info


def _is_alive(vid):
    alive, dead, _, info = _get_vid_state(vid)

    if dead is True:
        return False

    if alive is False:
        return False

    # If the build doesn't expose these flags, fall back to native attackability.
    if alive is None and dead is None:
        return _is_attackable(vid)

    return _is_attackable(vid)


def _get_world_position(vid):
    # Use the native chr.GetPixelPosition(VID) API. In this client it returns
    # the actor's actual pixel/world coordinates directly. The old GetVIDInfo
    # text parser is only kept as a compatibility fallback.
    try:
        result = chr.GetPixelPosition(int(vid))
        if result is not None and len(result) >= 3:
            x = float(result[0])
            y = float(result[1])
            z = float(result[2])
            return (x, y, z)
    except Exception:
        pass

    _, _, pos, _ = _get_vid_state(vid)
    if pos:
        return (float(pos[0]), float(pos[1]), 0.0)
    return None


def _seed_known_targets():
    """
    Add targets already known through native current/picked selection.
    """
    try:
        current = int(player.GetTargetVID())
        if current > 0:
            _known_vids.add(current)
    except Exception:
        pass

    if USE_PICKED_TARGET_FALLBACK:
        try:
            picked = int(chrmgr.GetPickedVID())
            if picked > 0:
                _known_vids.add(picked)
        except Exception:
            pass


def _scan_vids(now):
    global _last_scan_time, _scan_vid

    if now - _last_scan_time < VID_SCAN_INTERVAL:
        return

    _last_scan_time = now

    # First walk through the known VIDs because this is effectively free.
    for vid in tuple(_known_vids):
        if vid <= 0:
            continue
        if not _is_instance(vid):
            _known_vids.discard(vid)

    # Then do a small incremental sweep through the native instance table.
    end = min(_scan_vid + VID_SCAN_CHUNK, VID_SCAN_MAX + 1)

    for vid in range(_scan_vid, end):
        if vid <= 0:
            continue
        try:
            if chr.HasInstance(vid):
                _known_vids.add(vid)
        except Exception:
            pass

    if end > VID_SCAN_MAX:
        _scan_vid = VID_SCAN_MIN
    else:
        _scan_vid = end

    _refresh_target_snapshot(now)


def _refresh_target_snapshot(now, force=False):
    """Maintain a sorted live list of eligible mobs by current distance."""
    global _target_snapshot, _last_snapshot_time
    if not force and now - _last_snapshot_time < 0.07:
        return
    _last_snapshot_time = now
    main_vid = _main_vid()
    max_distance = _range_world()
    candidates = []
    for vid in tuple(_known_vids):
        if vid <= 0 or vid == main_vid:
            continue
        try:
            if not _is_instance(vid):
                _known_vids.discard(vid)
                _MOB_VNUM_CACHE.pop(vid, None)
                continue
            try:
                instance_type = chr.GetInstanceType(int(vid))
                excluded_types = set()
                for _name in ("INSTANCE_TYPE_PLAYER", "INSTANCE_TYPE_NPC", "INSTANCE_TYPE_BUILDING", "INSTANCE_TYPE_OBJECT", "INSTANCE_TYPE_STONE"):
                    if hasattr(chr, _name):
                        excluded_types.add(getattr(chr, _name))
                if instance_type in excluded_types:
                    continue
            except Exception:
                pass
            mob_vnum = _MOB_VNUM_CACHE.get(int(vid), 0)
            if mob_vnum <= 0:
                mob_vnum = int(chr.GetVirtualNumber(int(vid)))
                if mob_vnum > 0:
                    _MOB_VNUM_CACHE[int(vid)] = mob_vnum
            if mob_vnum <= 0:
                continue
            if not _is_enemy(vid) or not _is_alive(vid) or not _is_attackable(vid):
                continue
            dist = _distance(vid)
            if dist < 0.0 or dist > max_distance:
                continue
            candidates.append((float(dist), int(vid), int(mob_vnum)))
        except Exception:
            continue
    candidates.sort(key=lambda row: (row[0], row[1]))
    _target_snapshot = candidates


def _candidate_target():
    if _target_snapshot:
        for dist, vid, vnum in _target_snapshot:
            try:
                if _is_instance(vid) and _is_enemy(vid) and _is_alive(vid) and _is_attackable(vid):
                    if _distance(vid) <= _range_world():
                        return int(vid)
            except Exception:
                continue
    return 0


def _release_manual_walk():
    global _movement_key_down
    if not _movement_key_down:
        return
    try:
        player.SetSingleDIKKeyState(app.DIK_UP, False)
    except Exception:
        pass
    _movement_key_down = False


def _stop_attack_only():
    try:
        player.SetAttackKeyState(False)
    except Exception:
        pass


def _stop_attack():
    _release_manual_walk()
    try:
        player.SetAttackKeyState(False)
    except Exception:
        pass


def _start_attack(vid):
    _release_manual_walk()
    try:
        player.SetTarget(int(vid))
    except Exception:
        return

    try:
        player.SetAttackKeyState(True)
    except Exception:
        pass


def _local_teleport(vid):
    global _last_teleport_time

    now = _now()
    if now - _last_teleport_time < TELEPORT_COOLDOWN:
        return False

    # Never teleport using an untrusted/stale coordinate. Read the target
    # position directly from the native character manager first.
    target_pos = _get_world_position(vid)
    if not target_pos:
        return False

    try:
        tx, ty, tz = target_pos
        tx = float(tx)
        ty = float(ty)
        tz = float(tz)
    except Exception:
        return False

    # Hard authorization boundary: target must be inside the currently
    # configured Auto Hunt radius. This check is deliberately independent of
    # the attack distance.
    max_distance = _range_world()
    if max_distance <= 0.0:
        return False

    try:
        mx, my, mz = player.GetMainCharacterPosition()
        dx = tx - float(mx)
        dy = ty - float(my)
        coordinate_distance = (dx * dx + dy * dy) ** 0.5
    except Exception:
        return False

    if coordinate_distance > max_distance:
        return False

    # Cross-check against the client's native distance calculation so that a
    # bad/stale coordinate can never produce a huge teleport. A large
    # disagreement means: do not teleport, let normal movement handle it.
    try:
        native_distance = _distance(vid)
        if native_distance < 0 or native_distance > max_distance:
            return False
        if abs(native_distance - coordinate_distance) > 500.0:
            return False
    except Exception:
        return False

    main_vid = _main_vid()
    if main_vid <= 0 or not _is_instance(main_vid):
        return False

    try:
        chr.SelectInstance(main_vid)
        # Pass X/Y/Z exactly as returned for the selected target.
        chr.SetPixelPosition(int(round(tx)), int(round(ty)), int(round(tz)))
        _last_teleport_time = now
        return True
    except Exception:
        return False


def _face_target(vid):
    """Continuously rotate the main character toward the target's current position."""
    main_vid = _main_vid()
    if main_vid <= 0:
        return False
    try:
        target_pos = _get_world_position(vid)
        if not target_pos:
            return False
        mx, my, _ = player.GetMainCharacterPosition()
        dx = float(target_pos[0]) - float(mx)
        dy = float(target_pos[1]) - float(my)
        if abs(dx) < 0.01 and abs(dy) < 0.01:
            return True
        angle = math.degrees(math.atan2(dy, dx))
        if angle < 0.0:
            angle += 360.0
        chr.SelectInstance(int(main_vid))
        chr.SetDirection(float(angle))
        return True
    except Exception:
        return False


def _walk_to(vid):
    """Use the client's native movement core, without synthetic key jitter."""
    global _last_move_target_vid, _last_move_position, _movement_key_down

    pos = _get_world_position(vid)
    if not pos:
        return False
    x, y, _ = pos
    main_vid = _main_vid()
    if main_vid <= 0:
        return False

    try:
        mx, my, _ = player.GetMainCharacterPosition()
        current_pos = (float(mx), float(my))
    except Exception:
        current_pos = None

    # MoveToDestPosition() owns the movement state. Repeated DIK_UP press/release
    # was the source of the visible vibration, so do not synthesize keyboard input.
    if _last_move_target_vid == int(vid) and _last_move_position is not None and current_pos is not None:
        moved = ((current_pos[0] - _last_move_position[0]) ** 2 +
                 (current_pos[1] - _last_move_position[1]) ** 2) ** 0.5
        if moved >= 3.0:
            _last_move_position = current_pos
            return True

    try:
        chr.MoveToDestPosition(int(main_vid), int(round(x)), int(round(y)))
        _last_move_target_vid = int(vid)
        _last_move_position = current_pos
        _movement_key_down = False
        return True
    except Exception as exc:
        _say("Natywny ruch do celu nieudany: %s" % (exc,))
        return False


def _acquire_or_keep_target(now):
    global _target_vid, _last_target_refresh, _last_move_target_vid, _last_move_position

    if _target_vid > 0:
        if not _is_instance(_target_vid):
            _target_vid = 0
        elif not _is_enemy(_target_vid):
            _target_vid = 0
        elif not _is_alive(_target_vid):
            _target_vid = 0

    if _target_vid <= 0 and now - _last_target_refresh >= TARGET_REFRESH_INTERVAL:
        _last_target_refresh = now
        _target_vid = _candidate_target()
        if _target_vid > 0:
            _last_move_target_vid = 0
            _last_move_position = None
            try:
                player.SetTarget(int(_target_vid))
            except Exception:
                pass
            try:
                _say("Target mob VID=%d VNUM=%d dist=%.0f" % (
                    int(_target_vid), int(chr.GetVirtualNumber(int(_target_vid))), float(_distance(_target_vid))))
            except Exception:
                pass

    return _target_vid


def _handle_current_target(now):
    global _target_vid, _last_pickup_time, _last_move_time

    vid = _target_vid
    if vid <= 0:
        return

    if not _is_instance(vid) or not _is_alive(vid):
        _stop_attack()

        if AUTO_PICKUP_AFTER_KILL and now - _last_pickup_time >= PICKUP_COOLDOWN:
            try:
                player.PickCloseItem()
            except Exception:
                pass
            _last_pickup_time = now

        _target_vid = 0
        return

    try:
        if not _is_attackable(vid):
            _stop_attack()
            _target_vid = 0
            return
    except Exception:
        pass

    distance = _distance(vid)

    # Najpierw podejście. Kluczowe: nie włączaj ataku, dopóki nie jesteśmy
    # w realnym zasięgu ataku. Wcześniej SetAttackKeyState(True) było
    # wysyłane natychmiast i zatrzymywało/zakłócało MoveToDestPosition().
    if distance > ATTACK_DISTANCE_WORLD:
        _stop_attack_only()
        # Keep the movement destination synchronized with the target. The native
        # movement core performs the actual shortest reachable movement.
        _face_target(vid)
        if now - _last_move_time >= MOVE_RETRY_INTERVAL:
            _last_move_time = now
            if not _walk_to(vid):
                _target_vid = 0
        return

    # Keep facing the target every update because mobs can move between swings.
    _face_target(vid)
    _start_attack(vid)


def SetAutoHuntItemSlot(slot, vnum):
    global _selected_auto_item_slot, _selected_auto_item_vnum, _last_auto_item_use_time
    try:
        slot = int(slot); vnum = int(vnum)
    except Exception:
        slot, vnum = -1, 0
    _selected_auto_item_slot = slot if slot >= 0 else -1
    _selected_auto_item_vnum = vnum if slot >= 0 else 0
    _last_auto_item_use_time = -9999.0


def ClearAutoHuntItemSlot():
    global _selected_auto_item_slot, _selected_auto_item_vnum, _last_auto_item_use_time
    _selected_auto_item_slot = -1
    _selected_auto_item_vnum = 0
    _last_auto_item_use_time = -9999.0


def _use_auto_hunt_item_if_needed(now):
    """Use exactly the item placed in the Auto Hunt consumable slot."""
    global _last_auto_item_use_time
    if now - _last_auto_item_use_time < AUTO_ITEM_USE_COOLDOWN:
        return False

    slot = _selected_auto_item_slot
    vnum = _selected_auto_item_vnum
    if slot < 0 or vnum <= 0:
        return False

    try:
        current_vnum = int(player.GetItemIndex(slot))
    except Exception:
        return False
    if current_vnum != vnum:
        return False

    try:
        if int(player.GetItemCount(slot)) <= 0:
            return False
    except Exception:
        pass

    try:
        net.SendItemUsePacket(slot)
        _last_auto_item_use_time = now
        _say("Uzyto itemu z wybranego slotu: VNUM=%d slot=%d" % (vnum, slot))
        return True
    except Exception as exc:
        _say("Nie mozna uzyc wybranego itemu VNUM=%d slot=%d: %s" % (vnum, slot, exc))
        return False

def Start(mob_range=None, use_teleport=False, farm_mobs=True):
    global _running, _target_vid, _scan_vid
    global _last_scan_time, _last_target_refresh, _last_move_time
    global _last_move_target_vid, _last_move_position, _target_snapshot, _last_snapshot_time

    if mob_range is not None:
        ConfigureRange(mob_range)

    # Auto Hunt is now a pure Mob Farm. Metin Farm lives entirely in F8.
    if not farm_mobs:
        _say("Auto Hunt obsluguje tylko Farm Mobow. Farma Metinow jest w panelu F8.")
        return

    _install_instance_hooks()
    _seed_known_targets()

    _running = True
    _target_vid = 0
    _scan_vid = VID_SCAN_MIN
    _last_scan_time = 0.0
    _last_target_refresh = 0.0
    _last_move_time = -9999.0
    _last_move_target_vid = 0
    _last_move_position = None
    _target_snapshot = []
    _last_snapshot_time = -9999.0

    _set_const_status(True)
    _say("START: lokalny Farm Mobow.")


def Stop():
    global _running, _target_vid, _last_move_target_vid, _last_move_position, _target_snapshot

    _running = False
    _target_vid = 0
    _last_move_target_vid = 0
    _last_move_position = None
    _target_snapshot = []

    _stop_attack()
    _set_const_status(False)

    try:
        player.ClearTarget()
    except Exception:
        pass

    _say("STOP.")


def Toggle():
    if _running:
        Stop()
    else:
        Start()


def Update():
    if not ENABLED:
        return

    now = _now()
    try:
        _auto_skill_update(now)
    except Exception:
        pass

    if not _running:
        return

    try:
        _seed_known_targets()
        _scan_vids(now)

        _use_auto_hunt_item_if_needed(now)

        # Build/refresh the live target snapshot before handling the current mob.
        if _target_vid > 0:
            _handle_current_target(now)

        if _target_vid <= 0:
            _refresh_target_snapshot(now, force=True)
            _acquire_or_keep_target(now)

        if _target_vid > 0:
            _handle_current_target(now)
        else:
            _stop_attack()
    except Exception:
        try:
            _stop_attack()
        except Exception:
            pass


def DebugState():
    return {
        "running": bool(_running),
        "target": int(_target_vid or 0),
        "range_ui": float(_range_ui),
        "range_world": float(_range_world()),
        "known_vids": len(_known_vids),
        "teleport": False,
    }

RANGE_CIRCLE = 60.0

IMG_DIR = "auto_hunt/"

# === KONFIGURACJA: vnumy 3 itemow auto-uzywanych przez bota ===
# PODSTAW TU SWOJE VNUMY. Te same vnumy MUSZA byc w PythonPlayer.cpp (__GetAutoHuntItemData).
# Slot 0/1/2 odpowiada kolejnym ikonom w oknie.
AUTO_HUNT_ITEM_VNUMS = {}

class AutoSkillSettings(ui.BoardWithTitleBar):
    """Six-slot Auto Skill configuration with automatic character-skill loading."""

    def __init__(self):
        ui.BoardWithTitleBar.__init__(self)
        self.AddFlag('float')
        self.AddFlag('movable')
        self.SetTitleName('Auto Skile - ustawienia')
        self.SetCloseEvent(ui.__mem_func__(self.Close))
        self.SetSize(250, 145)

        self.__slots = ui.SlotWindow()
        self.__slots.SetParent(self)
        self.__slots.SetPosition(15, 38)
        self.__slots.SetSize(220, 32)
        self.__slots.SetSelectEmptySlotEvent(ui.__mem_func__(self._select_empty))
        self.__slots.SetSelectItemSlotEvent(ui.__mem_func__(self._click_slot))
        self.__slots.SetUnselectItemSlotEvent(ui.__mem_func__(self._click_slot))
        self.__slots.SetUseSlotEvent(ui.__mem_func__(self._click_slot))
        self.__slots.SetOverInItemEvent(ui.__mem_func__(self._over_in))
        self.__slots.SetOverOutItemEvent(ui.__mem_func__(self._over_out))
        for i in range(6):
            self.__slots.AppendSlot(i, i * 35, 0, 32, 32)

        self.__checks = []
        for i in range(6):
            cb = ui.Button()
            cb.SetParent(self)
            cb.SetPosition(16 + i * 35, 70)
            cb.SetSize(32, 20)
            cb.SetUpVisual('d:/ymir work/ui/public/small_button_01.sub')
            cb.SetOverVisual('d:/ymir work/ui/public/small_button_02.sub')
            cb.SetDownVisual('d:/ymir work/ui/public/small_button_03.sub')
            cb.SetText('OFF')
            cb.SetEvent(ui.__mem_func__(self._toggle), i)
            cb.Show()
            self.__checks.append(cb)

        self.__loadBtn = ui.Button()
        self.__loadBtn.SetParent(self)
        self.__loadBtn.SetPosition(15, 98)
        self.__loadBtn.SetUpVisual('d:/ymir work/ui/public/middle_button_01.sub')
        self.__loadBtn.SetOverVisual('d:/ymir work/ui/public/middle_button_02.sub')
        self.__loadBtn.SetDownVisual('d:/ymir work/ui/public/middle_button_03.sub')
        self.__loadBtn.SetText('WCZYTAJ SKILE')
        self.__loadBtn.SetEvent(ui.__mem_func__(self.LoadCharacterSkills))
        self.__loadBtn.Show()

        self.__clearBtn = ui.Button()
        self.__clearBtn.SetParent(self)
        self.__clearBtn.SetPosition(135, 98)
        self.__clearBtn.SetUpVisual('d:/ymir work/ui/public/middle_button_01.sub')
        self.__clearBtn.SetOverVisual('d:/ymir work/ui/public/middle_button_02.sub')
        self.__clearBtn.SetDownVisual('d:/ymir work/ui/public/middle_button_03.sub')
        self.__clearBtn.SetText('WYCZYSC')
        self.__clearBtn.SetEvent(ui.__mem_func__(self.ClearAllSkills))
        self.__clearBtn.Show()

        self.__hint = ui.TextLine()
        self.__hint.SetParent(self)
        self.__hint.SetPosition(125, 126)
        self.__hint.SetHorizontalAlignCenter()
        self.__hint.SetText('Przeciagnij skill do slotu lub uzyj WCZYTAJ SKILE')
        self.__hint.Show()

        self.Refresh()

    def LoadCharacterSkills(self):
        chosen = LoadCharacterAutoSkills(force=True, max_slots=6)
        self.Refresh()
        return chosen

    def ClearAllSkills(self):
        for i in range(6):
            ClearAutoSkillSlot(i)
        self.Refresh()
        _say('Lista auto skili wyczyszczona.')

    def _refresh_slot(self, i):
        slots, active = GetAutoSkillConfig()
        self.__slots.ClearSlot(i)
        slot_no = slots[i]
        if slot_no is not None:
            try:
                idx = player.GetSkillIndex(int(slot_no))
                grade = player.GetSkillGrade(int(slot_no))
                level = player.GetSkillLevel(int(slot_no))
                self.__slots.SetSkillSlotNew(i, idx, grade, level)
                self.__slots.SetSlotCountNew(i, grade, level)
            except Exception:
                pass
        self.__checks[i].SetText('ON' if active[i] and slot_no is not None else 'OFF')

    def Refresh(self):
        for i in range(6):
            self._refresh_slot(i)
        self.__slots.RefreshSlot()

    def _select_empty(self, slot_index):
        try:
            if not mouseModule.mouseController.isAttached():
                return
            attached_type = mouseModule.mouseController.GetAttachedType()
            if attached_type != player.SLOT_TYPE_SKILL:
                return
            skill_slot = int(mouseModule.mouseController.GetAttachedSlotNumber())
            SetAutoSkillSlot(int(slot_index), skill_slot, True)
            mouseModule.mouseController.DeattachObject()
            self.Refresh()
        except Exception:
            try:
                mouseModule.mouseController.DeattachObject()
            except Exception:
                pass

    def _click_slot(self, slot_index):
        try:
            slot_index = int(slot_index)
            if mouseModule.mouseController.isAttached():
                attached_type = mouseModule.mouseController.GetAttachedType()
                if attached_type == player.SLOT_TYPE_SKILL:
                    skill_slot = int(mouseModule.mouseController.GetAttachedSlotNumber())
                    SetAutoSkillSlot(slot_index, skill_slot, True)
                    mouseModule.mouseController.DeattachObject()
                    self.Refresh()
                    return
                return
            slots, _ = GetAutoSkillConfig()
            if 0 <= slot_index < 6 and slots[slot_index] is not None:
                ClearAutoSkillSlot(slot_index)
                self.Refresh()
        except Exception:
            try:
                mouseModule.mouseController.DeattachObject()
            except Exception:
                pass

    def _toggle(self, *args):
        try:
            index = int(args[-1]) if args else 0
            slots, active = GetAutoSkillConfig()
            if slots[index] is not None:
                SetAutoSkillActive(index, not bool(active[index]))
                self.Refresh()
        except Exception:
            pass

    def _over_in(self, index):
        try:
            slots, _ = GetAutoSkillConfig()
            slot_no = slots[int(index)]
            if slot_no is None:
                return
            interface = constInfo.GetInterfaceInstance()
            if interface and interface.tooltipSkill:
                interface.tooltipSkill.SetSkillNew(int(slot_no), player.GetSkillIndex(int(slot_no)), player.GetSkillGrade(int(slot_no)), player.GetSkillLevel(int(slot_no)))
        except Exception:
            pass

    def _over_out(self, *args):
        try:
            interface = constInfo.GetInterfaceInstance()
            if interface and interface.tooltipSkill:
                interface.tooltipSkill.HideToolTip()
        except Exception:
            pass

    def Open(self):
        # Auto-populate on first open when no skills are configured yet.
        slots, _ = GetAutoSkillConfig()
        if not any(slot is not None for slot in slots):
            LoadCharacterAutoSkills(force=False, max_slots=6)
        self.Refresh()
        self.Show()
        self.SetTop()

    def Close(self):
        self.Hide()


class Window(ui.BoardWithTitleBar):
	def __init__(self):
		ui.BoardWithTitleBar.__init__(self)
		self.__children = {}
		self.__autoSkillSettings = AutoSkillSettings()
		self.__LoadWindow()
	def Destroy(self):
		try:
			self.__autoSkillSettings.Close()
		except Exception:
			pass
		if len(self.__children) != 0:
			if self.IsActive():
				if self.__children["newOptions"]["auto_login"] == 1:
					constInfo.autoHuntAutoLoginDict["status"] = 1
					constInfo.autoHuntAutoLoginDict["leftTime"] = 0
					constInfo.autoHuntAutoLoginDict["skillDict"] = self.__children["skillDict"] if "skillDict" in self.__children else {}
					constInfo.autoHuntAutoLoginDict["newOptions"] = self.__children["newOptions"]
					slotItemDict = self.__children["slotItemDict"] if "slotItemDict" in self.__children else {}
					for key, itemIdx in slotItemDict.items():
						constInfo.autoHuntAutoLoginDict["slotStatus"][key] = self.__children["slotStatus" + str(key)] if ("slotStatus" + str(key)) in self.__children else False

		self.__children = {}
	def __LoadWindow(self):
		self.Destroy()
		self.AddFlag("float")
		self.AddFlag("movable")
		self.SetTitleName(localeInfo.AUTO_HUNT_TITLE)
		self.SetCloseEvent(ui.__mem_func__(self.Close))

		bg = CreateWindow(ui.ImageBox(), self, (8, 29), IMG_DIR+"bg.tga")
		bg.AddFlag("attach")
		self.__children["bg"] = bg

		slotItemDict = dict(AUTO_HUNT_ITEM_VNUMS)

		for key, itemIdx in slotItemDict.items():
			item.SelectItem(itemIdx)
			itemImg = CreateWindow(ui.ImageBox(), bg, (20 + (key * 50), 99), item.GetIconImageFileName())
			itemImg.SetEvent(ui.__mem_func__(self.__OverInItem), "mouse_over_in", itemIdx)
			itemImg.SAFE_SetStringEvent("MOUSE_OVER_OUT", self.__OverOut)
			itemImg.SetEvent(ui.__mem_func__(self.__ClickStatus), "mouse_click", key)
			self.__children["itemImg"+str(key)] = itemImg

			status = CreateWindow(ui.ImageBox(), itemImg, (itemImg.GetWidth() - 12, itemImg.GetHeight() - 11), IMG_DIR+"check_0.tga")
			status.SetEvent(ui.__mem_func__(self.__ClickStatus), "mouse_click", key)
			self.__children["status"+str(key)] = status
		self.__children["slotItemDict"] = slotItemDict

		slot = CreateWindow(ui.SlotWindow(), bg, (10, 31), "", "", (205, 32))
		slot.SetSelectEmptySlotEvent(ui.__mem_func__(self.SelectSlot))
		slot.SetSelectItemSlotEvent(ui.__mem_func__(self.__ClickSkillSlot))
		slot.SetUnselectItemSlotEvent(ui.__mem_func__(self.__ClickSkillSlot))
		slot.SetUseSlotEvent(ui.__mem_func__(self.__ClickSkillSlot))
		for j in range(6):
			slot.AppendSlot(j, (j * 35), 0, 32, 32)
		slot.SetOverInItemEvent(ui.__mem_func__(self.__OverInSkill))
		slot.SetOverOutItemEvent(ui.__mem_func__(self.__OverOut))
		self.__children["slot"] = slot

		# Manual Auto Hunt consumable slot. Drag an item from normal inventory here.
		cloakLabel = CreateWindow(ui.TextLine(), bg, (150, 78), "Pelerynka", "horizontal:center")
		self.__children["cloakLabel"] = cloakLabel
		cloakSlot = CreateWindow(ui.SlotWindow(), bg, (164, 96), "", "", (32, 32))
		cloakSlot.AppendSlot(0, 0, 0, 32, 32)
		cloakSlot.SetSelectEmptySlotEvent(ui.__mem_func__(self.__SelectCloakSlot))
		if hasattr(cloakSlot, "SetUnselectEmptySlotEvent"):
			cloakSlot.SetUnselectEmptySlotEvent(ui.__mem_func__(self.__SelectCloakSlot))
		cloakSlot.SetSelectItemSlotEvent(ui.__mem_func__(self.__ClickCloakSlot))
		cloakSlot.SetUseSlotEvent(ui.__mem_func__(self.__ClickCloakSlot))
		cloakSlot.SetOverInItemEvent(ui.__mem_func__(self.__OverInCloakItem))
		cloakSlot.SetOverOutItemEvent(ui.__mem_func__(self.__OverOutCloakItem))
		self.__children["cloakSlot"] = cloakSlot
		self.__children["cloakSlotIndex"] = -1
		self.__children["cloakVnum"] = 0

		self.__children["text0"] = CreateWindow(ui.TextLine(), bg, (bg.GetWidth() // 2, 9), localeInfo.AUTO_HUNT_SKILLS, "horizontal:center")

		resetBtn = CreateWindow(ui.Button(), bg, (205, 6))
		resetBtn.SetUpVisual(IMG_DIR+"reset_0.tga")
		resetBtn.SetOverVisual(IMG_DIR+"reset_1.tga")
		resetBtn.SetDownVisual(IMG_DIR+"reset_2.tga")
		resetBtn.SetEvent(ui.__mem_func__(self.__ResetBtn))
		resetBtn.SetToolTipText(localeInfo.AUTO_HUNT_RESET)
		self.__children["resetBtn"] = resetBtn

		optionBtn = CreateWindow(ui.ToggleButton(), bg, (0, 151), "", "horizontal:center")
		optionBtn.SetUpVisual("d:/ymir work/ui/public/large_button_01.sub")
		optionBtn.SetOverVisual("d:/ymir work/ui/public/large_button_02.sub")
		optionBtn.SetDownVisual("d:/ymir work/ui/public/large_button_03.sub")
		optionBtn.SetToggleUpEvent(ui.__mem_func__(self.__OptionBtn))
		optionBtn.SetToggleDownEvent(ui.__mem_func__(self.__OptionBtn))
		optionBtn.SetText(localeInfo.AUTO_HUNT_OPTION)
		self.__children["optionBtn"] = optionBtn

		startBtn = CreateWindow(ui.RadioButton(), bg, (-55, 178), "", "horizontal:center")
		startBtn.SetUpVisual("d:/ymir work/ui/public/large_button_01.sub")
		startBtn.SetOverVisual("d:/ymir work/ui/public/large_button_02.sub")
		startBtn.SetDownVisual("d:/ymir work/ui/public/large_button_03.sub")
		startBtn.SetEvent(ui.__mem_func__(self.__StartBtn))
		startBtn.SetText(localeInfo.AUTO_HUNT_START)
		self.__children["startBtn"] = startBtn

		stopBtn = CreateWindow(ui.RadioButton(), bg, (55, 178), "", "horizontal:center")
		stopBtn.SetUpVisual("d:/ymir work/ui/public/large_button_01.sub")
		stopBtn.SetOverVisual("d:/ymir work/ui/public/large_button_02.sub")
		stopBtn.SetDownVisual("d:/ymir work/ui/public/large_button_03.sub")
		stopBtn.SetEvent(ui.__mem_func__(self.__StopBtn))
		stopBtn.SetText(localeInfo.AUTO_HUNT_STOP)
		self.__children["stopBtn"] = stopBtn

		self.SetSize(8 + bg.GetWidth() + 8, 29 + bg.GetHeight() + 9)

		self.__children["rangeText"] = CreateWindow(ui.TextLine(), self, (100, self.GetHeight()-7), localeInfo.AUTO_HUNT_RANGE)

		sliderBar = CreateWindow(ui.SliderBar(), self, (30, self.GetHeight() + 15))
		sliderBar.SetEvent(ui.__mem_func__(self.__OnChangeRange))
		sliderBar.Hide()
		self.__children["sliderBar"] = sliderBar

		self.__children["mobFarmCheckBox"] = CreateWindow(ui.ImageBox(), self, (30, self.GetHeight() + 15 + 18), IMG_DIR+"unselected.tga")
		self.__children["mobFarmCheckBox"].SetEvent(ui.__mem_func__(self.__ClickOption), "mouse_click", "mob")
		self.__children["mobFarmText"] = CreateWindow(ui.TextLine(), self, (30 + 15, self.GetHeight() + 15 + 20), localeInfo.AUTO_HUNT_MOB_FARM)

		self.__children["autoLoginCheckBox"] = CreateWindow(ui.ImageBox(), self, (30, self.GetHeight() + 15 + 18 + 22), IMG_DIR+"unselected.tga")
		self.__children["autoLoginCheckBox"].SetEvent(ui.__mem_func__(self.__ClickOption), "mouse_click", "auto_login")
		self.__children["autoLoginText"] = CreateWindow(ui.TextLine(), self, (30 + 15, self.GetHeight() + 15 + 20 + 22), localeInfo.AUTO_HUNT_AUTO_LOGIN)

		self.__children["mountCheckBox"] = CreateWindow(ui.ImageBox(), self, (30 + 100, self.GetHeight() + 15 + 18 + 22), IMG_DIR+"unselected.tga")
		self.__children["mountCheckBox"].SetEvent(ui.__mem_func__(self.__ClickOption), "mouse_click", "mount")
		self.__children["mountText"] = CreateWindow(ui.TextLine(), self, (30 + 100 + 15, self.GetHeight() + 15 + 20 + 22), localeInfo.AUTO_HUNT_MOUNT)

		self.__children["mobRange"] = RANGE_CIRCLE

		self.__children["newOptions"] = {
			"auto_login" : 1,
			"mob" : 1,
			"mount" : 1,
		}

		self.SetCenterPosition()

	def __ToggleAutoSkills(self):
		SetAutoSkillsEnabled(not IsAutoSkillsEnabled())
		self.Refresh()

	def __OpenAutoSkillSettings(self):
		try:
			self.__autoSkillSettings.Open()
		except Exception as exc:
			chat.AppendChat(chat.CHAT_TYPE_INFO, "[Local AutoHunt] Nie mozna otworzyc ustawien skili: %s" % (exc,))

	def __ClickOption(self, emptyArg, option):
		if self.IsActive():
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.AUTO_HUNT_CANT_CHANGE_ACTIVE)
			return
		value = 1 if not self.__children["newOptions"][option] else 0
		self.__children["newOptions"][option] = value
		# Auto Hunt has only one local mode: Farm Mobow.
		if option == "mob" and value:
			self.__children["newOptions"]["mob"] = 1
		self.Refresh()

	def Refresh(self):
		slotItemDict = self.__children["slotItemDict"] if "slotItemDict" in self.__children else {}
		for key, itemIdx in slotItemDict.items():
			slotStatus = self.__children["slotStatus" + str(key)] if ("slotStatus" + str(key)) in self.__children else False
			self.__children["status"+str(key)].LoadImage(IMG_DIR+"check_1.tga" if slotStatus else IMG_DIR+"check_0.tga")

		bg = self.__children["bg"]
		if "autoSkillBtn" in self.__children:
			self.__children["autoSkillBtn"].SetText("Auto Skile: ON" if IsAutoSkillsEnabled() else "Auto Skile: OFF")

		if (self.__children["rangeStatus"] if "rangeStatus" in self.__children else False):
			miniMap.SetAutoHuntRangeStatus(True)
			self.__children["optionBtn"].Down()
			self.__children["rangeText"].Show()
			self.__children["sliderBar"].Show()
			self.__children["autoLoginCheckBox"].LoadImage(IMG_DIR + "selected.tga" if self.__children["newOptions"]["auto_login"] else IMG_DIR + "unselected.tga")
			self.__children["autoLoginCheckBox"].Show()
			self.__children["mobFarmCheckBox"].Show()
			self.__children["mobFarmCheckBox"].LoadImage(IMG_DIR + "selected.tga" if self.__children["newOptions"]["mob"] else IMG_DIR + "unselected.tga")
			self.__children["mobFarmText"].Show()
			self.__children["autoLoginText"].Show()
			self.__children["mountCheckBox"].Show()
			self.__children["mountCheckBox"].LoadImage(IMG_DIR + "selected.tga" if self.__children["newOptions"]["mount"] else IMG_DIR + "unselected.tga")
			self.__children["mountText"].Show()
			self.SetSize(8 + bg.GetWidth() + 8, 29 + bg.GetHeight() + 9 + 25 + 62)

			mobRange = self.__children["mobRange"] if "mobRange" in self.__children else 0.0
			self.__children["sliderBar"].SetSliderPos((1.0/RANGE_CIRCLE) * mobRange if mobRange > 0 else 0.0)

		else:
			self.SetSize(8 + bg.GetWidth() + 8, 29 + bg.GetHeight() + 9)
			self.__children["rangeText"].Hide()
			self.__children["sliderBar"].Hide()
			self.__children["autoLoginText"].Hide()
			self.__children["autoLoginCheckBox"].Hide()
			self.__children["mobFarmCheckBox"].Hide()
			self.__children["mobFarmText"].Hide()
			self.__children["mountCheckBox"].Hide()
			self.__children["mountText"].Hide()
			self.__children["optionBtn"].SetUp()
			miniMap.SetAutoHuntRangeStatus(False)

		slot = self.__children["slot"]
		skillDict = self.__children["skillDict"] if "skillDict" in self.__children else {}
		for j in range(6):
			slot.ClearSlot(j)
			if j not in skillDict:
				continue
			slotNumber = skillDict[j]
			(skillIndex, skillGrade, skillLevel) = (player.GetSkillIndex(slotNumber), player.GetSkillGrade(slotNumber), player.GetSkillLevel(slotNumber))
			slot.SetSkillSlotNew(j, skillIndex, skillGrade, skillLevel)
			slot.SetSlotCountNew(j, skillGrade, skillLevel)
		slot.RefreshSlot()

		cloakSlot = self.__children.get("cloakSlot")
		cloakSlotIndex = self.__children.get("cloakSlotIndex", -1)
		cloakVnum = self.__children.get("cloakVnum", 0)
		if cloakSlot is not None:
			cloakSlot.ClearSlot(0)
			if cloakSlotIndex is not None and int(cloakSlotIndex) >= 0:
				try:
					if int(player.GetItemIndex(int(cloakSlotIndex))) == int(cloakVnum) and int(cloakVnum) > 0:
						cloakSlot.SetItemSlot(0, int(cloakVnum), 0)
						SetAutoHuntItemSlot(int(cloakSlotIndex), int(cloakVnum))
					else:
						self.__children["cloakSlotIndex"] = -1
						self.__children["cloakVnum"] = 0
						ClearAutoHuntItemSlot()
				except Exception:
					pass
			else:
				ClearAutoHuntItemSlot()
			cloakSlot.RefreshSlot()

		activeStatus = self.IsActive()
		self.__children["startBtn" if activeStatus else "stopBtn"].Down()
		self.__children["startBtn" if not activeStatus else "stopBtn"].SetUp()

	def CheckAutoLogin(self):
		autoHuntAutoLoginDict = constInfo.autoHuntAutoLoginDict
		if autoHuntAutoLoginDict["status"] == 1:
			constInfo.autoHuntAutoLoginDict["status"] = 0
			self.__children["skillDict"] = autoHuntAutoLoginDict["skillDict"]
			self.__children["slotStatus"] = autoHuntAutoLoginDict["slotStatus"]
			self.__children["newOptions"] = autoHuntAutoLoginDict["newOptions"]

			slotItemDict = self.__children["slotItemDict"] if "slotItemDict" in self.__children else {}
			for key, itemIdx in slotItemDict.items():
				self.__children["slotStatus" + str(key)] = autoHuntAutoLoginDict["slotStatus"][key]

			self.Refresh()
			self.__StartBtn()

	def __OnChangeRange(self):
		# Guard re-entrancy: SetSliderPos -> cursor.SetPosition -> (C++ OnMove) -> __OnMove ->
		# eventChange(__OnChangeRange) tworzy nieskonczona rekurencje (stack overflow). Przerwij ja.
		if self.__children.get("__inRange", False):
			return
		self.__children["__inRange"] = True
		try:
			if self.IsActive():
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.AUTO_HUNT_NEED_DEACTIVE)
				self.Refresh()
				return
			sliderBar = self.__children["sliderBar"]
			mobRange = ((1.0/RANGE_CIRCLE) * (sliderBar.GetSliderPos()*RANGE_CIRCLE)) * RANGE_CIRCLE
			self.__children["mobRange"] = mobRange
			miniMap.SetAutoHuntRange(mobRange)
		finally:
			self.__children["__inRange"] = False

	def __OptionBtn(self):
		rangeStatus = self.__children["rangeStatus"] if "rangeStatus" in self.__children else False
		self.__children["rangeStatus"] = not rangeStatus
		miniMap.SetAutoHuntRange(self.__children["mobRange"] if "mobRange" in self.__children else 0.0)
		self.Refresh()

	def IsActive(self):
		try:
			return IsRunning()
		except:
			return self.__children["activeStatus"] if "activeStatus" in self.__children else False

	def __ResetBtn(self):
		if self.IsActive():
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.AUTO_HUNT_NEED_DEACTIVE)
			return
		self.__children["skillDict"] = {}
		slotItemDict = self.__children["slotItemDict"] if "slotItemDict" in self.__children else {}
		for key, itemIdx in slotItemDict.items():
			self.__children["slotStatus" + str(key)] = False
		self.__children["cloakSlotIndex"] = -1
		self.__children["cloakVnum"] = 0
		ClearAutoHuntItemSlot()
		self.Refresh()

	def SetStatus(self, status):
		self.__children["activeStatus"] = bool(status)
		# Local Auto Hunt is the source of truth; server status is optional.
		self.Refresh()

	def __StartBtn(self):
		if self.IsActive():
			self.Refresh()
			return
		selectedItemText = ""
		selectedSkillText = ""
		slotItemDict = self.__children["slotItemDict"] if "slotItemDict" in self.__children else {}
		for key, itemIdx in slotItemDict.items():
			if selectedItemText != "":
				selectedItemText += "?"
			selectedItemText += "1" if (self.__children["slotStatus" + str(key)] if ("slotStatus" + str(key)) in self.__children else False) else "0"
		if selectedItemText == "":
			selectedItemText = "empty"

		skillDict = self.__children["skillDict"] if "skillDict" in self.__children else {}
		for key, skillSlotNumber in skillDict.items():
			if skillSlotNumber != -1:
				if selectedSkillText != "":
					selectedSkillText += "?"
				selectedSkillText += str(skillSlotNumber)
		if selectedSkillText == "":
			selectedSkillText = "empty"
		# Zsynchronizuj zasieg z C++ przed startem (inaczej, gdy gracz nie otworzyl Option/nie ruszyl
		# suwaka, bot uzylby domyslnej wartosci z Create zamiast mobRange = brak realnego zasiegu).
		mobRange = self.__children["mobRange"] if "mobRange" in self.__children else RANGE_CIRCLE
		miniMap.SetAutoHuntRange(mobRange)

		# Local Auto Hunt: no /auto_hunt packet is sent to the server.
		# Auto Hunt is only the normal Mob Farm; Metin Farm is controlled from F8.
		farm_mobs = bool(self.__children["newOptions"].get("mob"))
		if not farm_mobs:
			chat.AppendChat(chat.CHAT_TYPE_INFO, "[Local AutoHunt] Zaznacz Farm Mobow. Farma Metinow jest w panelu F8.")
			return
		ConfigureRange(mobRange)
		Start(mob_range=mobRange, use_teleport=False, farm_mobs=True)
		self.__children["activeStatus"] = True
		self.Refresh()

	def __StopBtn(self):
		if not self.IsActive():
			self.Refresh()
			return
		Stop()
		self.__children["activeStatus"] = False
		self.Refresh()

	def __ClickStatus(self, emptyArg, slotIdx):
		if self.IsActive():
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.AUTO_HUNT_NEED_DEACTIVE)
			self.Refresh()
			return
		slotStatus = self.__children["slotStatus" + str(slotIdx)] if ("slotStatus" + str(slotIdx)) in self.__children else False
		self.__children["slotStatus" + str(slotIdx)] = not slotStatus
		self.Refresh()

	def __SelectCloakSlot(self, slotIndex):
		"""Accept an inventory item dropped onto the dedicated cloak slot."""
		mouse_controller = mouseModule.mouseController
		try:
			if mouse_controller.isAttached():
				attached_type = mouse_controller.GetAttachedType()
				attached_slot = mouse_controller.GetAttachedSlotNumber()
				if attached_type != player.SLOT_TYPE_INVENTORY:
					mouse_controller.DeattachObject()
					return
				vnum = int(player.GetItemIndex(attached_slot))
				count = int(player.GetItemCount(attached_slot))
				if vnum <= 0 or count <= 0:
					mouse_controller.DeattachObject()
					return
				self.__children["cloakSlotIndex"] = int(attached_slot)
				self.__children["cloakVnum"] = vnum
				self.__children["cloakSlot"].SetItemSlot(0, vnum, count)
				self.__children["cloakSlot"].RefreshSlot()
				SetAutoHuntItemSlot(int(attached_slot), vnum)
				chat.AppendChat(chat.CHAT_TYPE_INFO, "[Local AutoHunt] Pelerynka ustawiona: EQ=%d VNUM=%d." % (int(attached_slot), vnum))
				mouse_controller.DeattachObject()
				return
			# Clicking an empty selector without an attached item has nothing to accept.
		except Exception as exc:
			chat.AppendChat(chat.CHAT_TYPE_INFO, "[Local AutoHunt] Nie mozna ustawic pelerynki: %s" % (exc,))
		try:
			mouse_controller.DeattachObject()
		except Exception:
			pass

	def __ClickCloakSlot(self, slotIndex):
		if self.IsActive():
			self.Refresh()
			return
		self.__children["cloakSlotIndex"] = -1
		self.__children["cloakVnum"] = 0
		ClearAutoHuntItemSlot()
		self.Refresh()

	def __OverInCloakItem(self, slotIndex):
		vnum = int(self.__children.get("cloakVnum", 0))
		if vnum <= 0:
			return
		interface = constInfo.GetInterfaceInstance()
		if interface and getattr(interface, "tooltipItem", None):
			interface.tooltipItem.SetItemToolTip(vnum)

	def __OverOutCloakItem(self, *args):
		self.__OverOut(*args)


	def __ClickSkillSlot(self, slotIndex):
		if self.IsActive():
			self.Refresh()
			return
		skillDict = self.__children["skillDict"] if "skillDict" in self.__children else {}
		if slotIndex not in skillDict:
			return
		self.__children["skillDict"][slotIndex] = -1
		self.Refresh()

	def SelectSlot(self, slotIndex):
		if self.IsActive():
			self.Refresh()
			return
		if True != mouseModule.mouseController.isAttached():
			return
		attachedSlotType = mouseModule.mouseController.GetAttachedType()
		if attachedSlotType == player.SLOT_TYPE_SKILL:
			attachedSlotNumber = mouseModule.mouseController.GetAttachedSlotNumber()
			skillDict = self.__children["skillDict"] if "skillDict" in self.__children else {}
			for key, skillSlotNumber in skillDict.items():
				if skillSlotNumber == attachedSlotNumber:
					skillDict[key] = -1
					break
			skillDict[slotIndex] = attachedSlotNumber
			self.__children["skillDict"] = skillDict
			self.Refresh()
		mouseModule.mouseController.DeattachObject()

	def __OverInSkill(self, index):
		skillDict = self.__children["skillDict"] if "skillDict" in self.__children else {}
		if index not in skillDict:
			return
		skillNumber = skillDict[index]
		interface = constInfo.GetInterfaceInstance()
		if interface:
			if interface.tooltipSkill:
				interface.tooltipSkill.SetSkillNew(skillNumber, player.GetSkillIndex(skillNumber), player.GetSkillGrade(skillNumber), player.GetSkillLevel(skillNumber))

	def __OverInItem(self, emptyArg, itemIdx):
		interface = constInfo.GetInterfaceInstance()
		if interface:
			if interface.tooltipItem:
				interface.tooltipItem.SetItemToolTip(itemIdx)

	def __OverOut(self, *args):
		interface = constInfo.GetInterfaceInstance()
		if interface:
			if interface.tooltipItem:
				interface.tooltipItem.HideToolTip()
			if interface.tooltipSkill:
				interface.tooltipSkill.HideToolTip()

	def Open(self):
		self.Refresh()
		self.Show()
		self.SetTop()

	def Close(self):
		miniMap.SetAutoHuntRangeStatus(False)
		self.Hide()

	def OnPressEscapeKey(self):
		self.Close()
		return True

def CreateWindow(window, parent, windowPos, windowArgument = "", windowPositionRule = "", windowSize = (-1, -1), windowFontName = -1):
	window.SetParent(parent)
	window.SetPosition(*windowPos)
	if windowSize != (-1, -1):
		window.SetSize(*windowSize)
	if windowPositionRule:
		splitList = windowPositionRule.split(":")
		if len(splitList) == 2:
			(type, mode) = (splitList[0], splitList[1])
			if type == "horizontal":
				if isinstance(window, ui.TextLine):
					if mode == "center":
						window.SetHorizontalAlignCenter()
					elif mode == "right":
						window.SetHorizontalAlignRight()
					elif mode == "left":
						window.SetHorizontalAlignLeft()
				else:
					if mode == "center":
						window.SetWindowHorizontalAlignCenter()
					elif mode == "right":
						window.SetWindowHorizontalAlignRight()
					elif mode == "left":
						window.SetWindowHorizontalAlignLeft()
			elif type == "vertical":
				if isinstance(window, ui.TextLine):
					if mode == "center":
						window.SetVerticalAlignCenter()
					elif mode == "top":
						window.SetVerticalAlignTop()
					elif mode == "bottom":
						window.SetVerticalAlignBottom()
				else:
					if mode == "top":
						window.SetWindowVerticalAlignTop()
					elif mode == "center":
						window.SetWindowVerticalAlignCenter()
					elif mode == "bottom":
						window.SetWindowVerticalAlignBottom()
	if windowArgument:
		if isinstance(window, ui.TextLine):
			if windowFontName != -1:
				window.SetFontName(windowFontName)
			window.SetText(windowArgument)
		elif isinstance(window, ui.NumberLine):
			window.SetNumber(windowArgument)
		elif isinstance(window, ui.ExpandedImageBox) or isinstance(window, ui.ImageBox):
			window.LoadImage(windowArgument if windowArgument.find("gr2") == -1 else "icon/item/27995.tga")
	window.Show()
	return window
