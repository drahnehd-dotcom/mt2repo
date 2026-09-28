# -*- coding: iso-8859-1 -*-
import item
import app
import uiScriptLocale

BOARD_WIDTH = 300
BOARD_HEIGHT = 270
IMG_PATH = "d:/ymir work/ui/mount_window/"

window = {
        "name": "Mount_Window",
        "style": ("movable", "float",),
        "x": 0, "y": 0,
        "width": BOARD_WIDTH, "height": BOARD_HEIGHT,
        "children": [
            {
                "name": "board",
                "type": "board",
                "x": 0, "y": 0,
                "width": BOARD_WIDTH, "height": BOARD_HEIGHT,
                "children": [
                    {
                        "name": "TitleBar",
                        "type": "titlebar",
                        "style": ("attach",),
                        "x": 8, "y": 7,
                        "width": BOARD_WIDTH - 15,
                        "color": "yellow",
                        "children": [
                            { 
                                "name": "TitleName",
                                "type": "text",
                                "x": 0, "y": -4,
                                "text": uiScriptLocale.MOUNT_RIDE_TITLE,
                                "outline": "1",
                                "all_align": "center",
                            },
                        ],
                    },
                    { 
                        "name": "info_board", 
                        "type": "image", 
                        "x": 57, 
                        "y": 35, 
                        "image": IMG_PATH + "base-image.png",
                        "children": [
                            {
                                "name": "window",
                                "type": "window",
                                "x": 58, 
                                "y": 3,
                                "width": 172, "height": 12,
                                "children": [
                                    { "name": "mount_level", "type": "text", "x": 0, "y": 0, "all_align": "center" },
                                ],
                            },
                            { "name": "exp_hover_info", "type": "window", "x": 109, "y": 24, "width": 75, "height": 18},
                            { "name": "exp_gauge_01", "type": "expanded_image", "x": 109 + 0, "y": 24, "image": IMG_PATH + "exp_full.png" },
                            { "name": "exp_gauge_02", "type": "expanded_image", "x": 109 + 18, "y": 24, "image": IMG_PATH + "exp_full.png" },
                            { "name": "exp_gauge_03", "type": "expanded_image", "x": 109 + 36, "y": 24, "image": IMG_PATH + "exp_full.png" },
                            { "name": "exp_gauge_04", "type": "expanded_image", "x": 109 + 54, "y": 24, "image": IMG_PATH + "exp_full.png" },
                        ],
                    },
                    {
                        "name": "header",
                        "type": "image",
                        "x": 20,
                        "y": 85,
                        "image": "d:/ymir work/ui/game/buttons/test_image_020.tga",
                        "children": [
                            {
                                "name": "header_text",
                                "type": "text",
                                "x": 0, "y": -1,
                                "all_align": "center",
                                "outline": "1",
                                "text": uiScriptLocale.MOUNT_PASSIVE_ABILITIES,
                            },
                            {
                                "name": "um",
                                "type": "image",
                                "x": 7,
                                "y": 3,
                                "image": IMG_PATH + "um.png",
                                "children": [
                                    {
                                        "name": "skill_points",
                                        "type": "text",
                                        "x": 0, "y": -1,
                                        "all_align": "center",
                                        "outline": "1",
                                        "text": "0",
                                    },
                                ],
                            },
                        ],
                    },
                    {
                        "name": "skill_window",
                        "type": "thinboard_circle",
                        "x": 12, "y": 108,
                        "width": 272, "height": 60,
                        "children": [
                            {
                                "name": "skill_board",
                                "type": "image",
                                "x": 9, "y": 10,
                                "image": IMG_PATH + "item-image.png",
                            },
                        ],
                    },
                    {
                        "name": "header",
                        "type": "image",
                        "x": 20,
                        "y": 174,
                        "image": "d:/ymir work/ui/game/buttons/test_image_020.tga",
                        "children": [
                            {
                                "name": "header_text",
                                "type": "text",
                                "x": 0, "y": -1,
                                "all_align": "center",
                                "outline": "1",
                                "text": uiScriptLocale.MOUNT_EQUIPMENT,
                            },
                        ],
                    },
                    {
                        "name": "horseshoe_window",
                        "type": "thinboard_circle",
                        "x": 12, "y": 197,
                        "width": 272, "height": 60,
                        "children": [
                            {
                                "name": "horseshoe_board",
                                "type": "image",
                                "x": 9, "y": 10,
                                "image": IMG_PATH + "item-image-1.png",
                                "children": [
                                    {
                                        "name": "HorseShoeName",
                                        "type": "text",
                                        "x": 10, "y": 2,
                                        "text": uiScriptLocale.MOUNT_HORSESHOE,
                                        "outline": "1",
                                        "fontname": "Tahoma:14i",
                                    },
                                    {
                                        "name": "block",
                                        "type": "image",
                                        "x": 218,
                                        "y": 8,
                                        "image": "d:/ymir work/ui/slot_off.png",
                                    },
                                ],
                            },
                        ],
                    },
                    {
                        "name": "offsystem",
                        "type": "image",
                        "x": 12,
                        "y": 35,
                        "image": "d:/ymir work/ui/off_system.png",
                        "children": [
                            {
                                "name": "offsystem_text",
                                "type": "text",
                                "x": 70, "y": 90,
                                "text": uiScriptLocale.MOUNT_IN_PREPARATION,
                                "fontname": "Tahoma:20",
                                "outline": 1,
                            },
                        ],
                    },
                ],
            },
            {
                "name": "MountSlotImage",
                "type": "image",
                "x": 12,
                "y": 36,
                "image": "d:/ymir work/ui/detach_slot2.png",
                "children": [
                    {
                        "name": "MountSlot",
                        "type": "slot",
                        "x": 4,
                        "y": 4,
                        "width": 32,
                        "height": 32,
                        "slot": [
                            {"index": item.COSTUME_SLOT_MOUNT, "x": 0, "y": 0, "width": 32, "height": 32},
                        ],
                    },
                ],
            },
        ],
    }
