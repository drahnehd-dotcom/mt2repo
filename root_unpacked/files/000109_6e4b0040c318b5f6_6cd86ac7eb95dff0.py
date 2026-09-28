# -*- coding: utf-8 -*-
"""
Emotion System Module

This module handles character emotion animations, icons, and commands for the game.
Uses emotion version 2 with full feature set.
"""

import localeInfo
import player
import chrmgr
import chr
import app


class EmotionType(object):
    """Emotion type constants"""
    CLAP = 1
    CONGRATULATION = 2
    FORGIVE = 3
    ANGRY = 4
    ATTRACTIVE = 5
    SAD = 6
    SHY = 7
    CHEERUP = 8
    BANTER = 9
    JOY = 10
    CHEERS_1 = 11
    CHEERS_2 = 12
    DANCE_1 = 13
    DANCE_2 = 14
    DANCE_3 = 15
    DANCE_4 = 16
    DANCE_5 = 17
    DANCE_6 = 18
    
    # Interactive emotions
    KISS = 51
    FRENCH_KISS = 52
    SLAP = 53


# Emotion configuration
EMOTION_DICT = {
    EmotionType.CLAP: {
        "name": localeInfo.EMOTION_CLAP,
        "command": "/clap"
    },
    EmotionType.DANCE_1: {
        "name": localeInfo.EMOTION_DANCE_1,
        "command": "/dance1"
    },
    EmotionType.DANCE_2: {
        "name": localeInfo.EMOTION_DANCE_2,
        "command": "/dance2"
    },
    EmotionType.DANCE_3: {
        "name": localeInfo.EMOTION_DANCE_3,
        "command": "/dance3"
    },
    EmotionType.DANCE_4: {
        "name": localeInfo.EMOTION_DANCE_4,
        "command": "/dance4"
    },
    EmotionType.DANCE_5: {
        "name": localeInfo.EMOTION_DANCE_5,
        "command": "/dance5"
    },
    EmotionType.DANCE_6: {
        "name": localeInfo.EMOTION_DANCE_6,
        "command": "/dance6"
    },
    EmotionType.CONGRATULATION: {
        "name": localeInfo.EMOTION_CONGRATULATION,
        "command": "/congratulation"
    },
    EmotionType.FORGIVE: {
        "name": localeInfo.EMOTION_FORGIVE,
        "command": "/forgive"
    },
    EmotionType.ANGRY: {
        "name": localeInfo.EMOTION_ANGRY,
        "command": "/angry"
    },
    EmotionType.ATTRACTIVE: {
        "name": localeInfo.EMOTION_ATTRACTIVE,
        "command": "/attractive"
    },
    EmotionType.SAD: {
        "name": localeInfo.EMOTION_SAD,
        "command": "/sad"
    },
    EmotionType.SHY: {
        "name": localeInfo.EMOTION_SHY,
        "command": "/shy"
    },
    EmotionType.CHEERUP: {
        "name": localeInfo.EMOTION_CHEERUP,
        "command": "/cheerup"
    },
    EmotionType.BANTER: {
        "name": localeInfo.EMOTION_BANTER,
        "command": "/banter"
    },
    EmotionType.JOY: {
        "name": localeInfo.EMOTION_JOY,
        "command": "/joy"
    },
    EmotionType.CHEERS_1: {
        "name": localeInfo.EMOTION_CHEERS_1,
        "command": "/cheer1"
    },
    EmotionType.CHEERS_2: {
        "name": localeInfo.EMOTION_CHEERS_2,
        "command": "/cheer2"
    },
    EmotionType.KISS: {
        "name": localeInfo.EMOTION_CLAP_KISS,
        "command": "/kiss"
    },
    EmotionType.FRENCH_KISS: {
        "name": localeInfo.EMOTION_FRENCH_KISS,
        "command": "/french_kiss"
    },
    EmotionType.SLAP: {
        "name": localeInfo.EMOTION_SLAP,
        "command": "/slap"
    },
}

# Icon paths
ICON_DICT = {
    EmotionType.CLAP: "d:/ymir work/ui/game/windows/emotion_clap.sub",
    EmotionType.CHEERS_1: "d:/ymir work/ui/game/windows/emotion_cheers_1.sub",
    EmotionType.CHEERS_2: "d:/ymir work/ui/game/windows/emotion_cheers_2.sub",
    EmotionType.DANCE_1: "icon/action/dance1.tga",
    EmotionType.DANCE_2: "icon/action/dance2.tga",
    EmotionType.CONGRATULATION: "icon/action/congratulation.tga",
    EmotionType.FORGIVE: "icon/action/forgive.tga",
    EmotionType.ANGRY: "icon/action/angry.tga",
    EmotionType.ATTRACTIVE: "icon/action/attractive.tga",
    EmotionType.SAD: "icon/action/sad.tga",
    EmotionType.SHY: "icon/action/shy.tga",
    EmotionType.CHEERUP: "icon/action/cheerup.tga",
    EmotionType.BANTER: "icon/action/banter.tga",
    EmotionType.JOY: "icon/action/joy.tga",
    EmotionType.DANCE_3: "icon/action/dance3.tga",
    EmotionType.DANCE_4: "icon/action/dance4.tga",
    EmotionType.DANCE_5: "icon/action/dance5.tga",
    EmotionType.DANCE_6: "icon/action/dance6.tga",
    EmotionType.KISS: "d:/ymir work/ui/game/windows/emotion_kiss.sub",
    EmotionType.FRENCH_KISS: "d:/ymir work/ui/game/windows/emotion_french_kiss.sub",
    EmotionType.SLAP: "d:/ymir work/ui/game/windows/emotion_slap.sub",
}

# Animation mappings
ANI_DICT = {
    chr.MOTION_CLAP: "clap.msa",
    chr.MOTION_CHEERS_1: "cheers_1.msa",
    chr.MOTION_CHEERS_2: "cheers_2.msa",
    chr.MOTION_DANCE_1: "dance_1.msa",
    chr.MOTION_DANCE_2: "dance_2.msa",
    chr.MOTION_DANCE_3: "dance_3.msa",
    chr.MOTION_DANCE_4: "dance_4.msa",
    chr.MOTION_DANCE_5: "dance_5.msa",
    chr.MOTION_DANCE_6: "dance_6.msa",
    chr.MOTION_CONGRATULATION: "congratulation.msa",
    chr.MOTION_FORGIVE: "forgive.msa",
    chr.MOTION_ANGRY: "angry.msa",
    chr.MOTION_ATTRACTIVE: "attractive.msa",
    chr.MOTION_SAD: "sad.msa",
    chr.MOTION_SHY: "shy.msa",
    chr.MOTION_CHEERUP: "cheerup.msa",
    chr.MOTION_BANTER: "banter.msa",
    chr.MOTION_JOY: "joy.msa",
    
    # Interactive animations for all character classes
    chr.MOTION_FRENCH_KISS_WITH_WARRIOR: "french_kiss_with_warrior.msa",
    chr.MOTION_FRENCH_KISS_WITH_ASSASSIN: "french_kiss_with_assassin.msa",
    chr.MOTION_FRENCH_KISS_WITH_SURA: "french_kiss_with_sura.msa",
    chr.MOTION_FRENCH_KISS_WITH_SHAMAN: "french_kiss_with_shaman.msa",
    chr.MOTION_KISS_WITH_WARRIOR: "kiss_with_warrior.msa",
    chr.MOTION_KISS_WITH_ASSASSIN: "kiss_with_assassin.msa",
    chr.MOTION_KISS_WITH_SURA: "kiss_with_sura.msa",
    chr.MOTION_KISS_WITH_SHAMAN: "kiss_with_shaman.msa",
    chr.MOTION_SLAP_HIT_WITH_WARRIOR: "slap_hit.msa",
    chr.MOTION_SLAP_HIT_WITH_ASSASSIN: "slap_hit.msa",
    chr.MOTION_SLAP_HIT_WITH_SURA: "slap_hit.msa",
    chr.MOTION_SLAP_HIT_WITH_SHAMAN: "slap_hit.msa",
    chr.MOTION_SLAP_HURT_WITH_WARRIOR: "slap_hurt.msa",
    chr.MOTION_SLAP_HURT_WITH_ASSASSIN: "slap_hurt.msa",
    chr.MOTION_SLAP_HURT_WITH_SURA: "slap_hurt.msa",
    chr.MOTION_SLAP_HURT_WITH_SHAMAN: "slap_hurt.msa",
}

# Add Wolfman character support if enabled
if hasattr(app, 'ENABLE_WOLFMAN_CHARACTER') and app.ENABLE_WOLFMAN_CHARACTER:
    ANI_DICT.update({
        chr.MOTION_FRENCH_KISS_WITH_WOLFMAN: "french_kiss_with_wolfman.msa",
        chr.MOTION_KISS_WITH_WOLFMAN: "kiss_with_wolfman.msa",
        chr.MOTION_SLAP_HIT_WITH_WOLFMAN: "slap_hit.msa",
        chr.MOTION_SLAP_HURT_WITH_WOLFMAN: "slap_hurt.msa",
    })


def register_shared_emotion_animations(motion_mode, path):
    """
    Register shared emotion animations for a specific motion mode.
    
    Args:
        motion_mode: Character motion mode constant
        path: Path to animation files
    """
    chrmgr.SetPathName(path)
    chrmgr.RegisterMotionMode(motion_mode)
    
    for motion_key, animation_file in ANI_DICT.items():
        chrmgr.RegisterMotionData(motion_mode, motion_key, animation_file)


def register_emotion_animations(base_path):
    """
    Register all emotion animations for different character modes.
    
    Args:
        base_path: Base path to character animation files
    """
    action_path = base_path + "action/"
    wedding_path = base_path + "wedding/"
    
    # Register animations for general and wedding dress modes
    register_shared_emotion_animations(chr.MOTION_MODE_GENERAL, action_path)
    register_shared_emotion_animations(chr.MOTION_MODE_WEDDING_DRESS, action_path)
    
    # Register wedding-specific animations
    chrmgr.SetPathName(wedding_path)
    chrmgr.RegisterMotionMode(chr.MOTION_MODE_WEDDING_DRESS)
    
    wedding_animations = [
        (chr.MOTION_WAIT, "wait.msa"),
        (chr.MOTION_WALK, "walk.msa"),
        (chr.MOTION_RUN, "walk.msa"),
    ]
    
    for motion, animation_file in wedding_animations:
        chrmgr.RegisterMotionData(chr.MOTION_MODE_WEDDING_DRESS, motion, animation_file)


def register_emotion_icons():
    """Register all emotion icons with the player system."""
    for emotion_id, icon_path in ICON_DICT.items():
        player.RegisterEmotionIcon(emotion_id, icon_path)


def get_emotion_command(emotion_id):
    """
    Get the chat command for an emotion.
    
    Args:
        emotion_id: Emotion ID constant
        
    Returns:
        str: Chat command string or None if not found
    """
    emotion_data = EMOTION_DICT.get(emotion_id)
    return emotion_data.get("command") if emotion_data else None


def get_emotion_name(emotion_id):
    """
    Get the display name for an emotion.
    
    Args:
        emotion_id: Emotion ID constant
        
    Returns:
        str: Emotion display name or None if not found
    """
    emotion_data = EMOTION_DICT.get(emotion_id)
    return emotion_data.get("name") if emotion_data else None


def is_emotion_available(emotion_id):
    """
    Check if an emotion is available.
    
    Args:
        emotion_id: Emotion ID constant
        
    Returns:
        bool: True if emotion is available, False otherwise
    """
    return emotion_id in EMOTION_DICT


RegisterEmotionAnis = register_emotion_animations
RegisterEmotionIcons = register_emotion_icons