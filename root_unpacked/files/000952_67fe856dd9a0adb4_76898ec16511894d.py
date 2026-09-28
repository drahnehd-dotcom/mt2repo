# -*- coding: utf-8 -*-
import item
import uiScriptLocale

BOARD_WIDTH = 300
BOARD_HEIGHT = 325
IMG_PATH = "d:/ymir work/ui/mount_window/"

# Pet equip: 3 equipment slots
PET_EQ_COUNT = 3
# Center the 3 slots (each 32px wide + 13px gap = 45 step)
# Total width of 3 slots: 32 + 45 + 45 = 122. Board inner ~254, center offset ~66
EQ_SLOT_X = 66
EQ_SLOT_Y = 6

window = {
    "name": "Pet_Window",
    "style": ("movable", "float"),
    "x": 0, "y": 0,
    "width": BOARD_WIDTH, "height": BOARD_HEIGHT,
    "children": (
        {
            "name": "board",
            "type": "board",
            "x": 0, "y": 0,
            "width": BOARD_WIDTH, "height": BOARD_HEIGHT,
            "children": (
                # ── Title Bar ──
                {
                    "name": "TitleBar",
                    "type": "titlebar",
                    "style": ("attach",),
                    "x": 8, "y": 7,
                    "width": BOARD_WIDTH - 15,
                    "color": "yellow",
                    "children": (
                        {
                            "name": "TitleName",
                            "type": "text",
                            "x": 0, "y": -3,
                            "text": uiScriptLocale.PET_TEXT,
                            "outline": "1",
                            "all_align": "center",
                        },
                    ),
                },
                # ── Pet info area (level + exp) ──
                {
                    "name": "info_board",
                    "type": "image",
                    "x": 57, "y": 35,
                    "image": IMG_PATH + "base-image.png",
                    "children": (
                        {
                            "name": "window",
                            "type": "window",
                            "x": 58, "y": 3,
                            "width": 172, "height": 12,
                            "children": (
                                {"name": "mount_level", "type": "text", "x": 0, "y": 0, "all_align": "center"},
                            ),
                        },
                        {"name": "exp_hover_info", "type": "window", "x": 109, "y": 24, "width": 75, "height": 18},
                        {"name": "exp_gauge_01", "type": "expanded_image", "x": 109, "y": 24, "image": IMG_PATH + "exp_full.png"},
                        {"name": "exp_gauge_02", "type": "expanded_image", "x": 127, "y": 24, "image": IMG_PATH + "exp_full.png"},
                        {"name": "exp_gauge_03", "type": "expanded_image", "x": 145, "y": 24, "image": IMG_PATH + "exp_full.png"},
                        {"name": "exp_gauge_04", "type": "expanded_image", "x": 163, "y": 24, "image": IMG_PATH + "exp_full.png"},
                    ),
                },
                # ── Pet item slot ──
                {
                    "name": "MountSlotImage",
                    "type": "image",
                    "x": 12, "y": 36,
                    "image": "d:/ymir work/ui/detach_slot2.png",
                    "children": (
                        {
                            "name": "islot",
                            "type": "slot",
                            "x": 5, "y": 4,
                            "width": 32, "height": 32,
                            "slot": (
                                {"index": item.SLOT_ITEM_NEW_PET, "x": 0, "y": 0, "width": 32, "height": 32},
                            ),
                        },
                    ),
                },
                # ── Skills header ──
                {
                    "name": "skills_header",
                    "type": "image",
                    "x": 20, "y": 85,
                    "image": "d:/ymir work/ui/game/buttons/test_image_020.tga",
                    "children": (
                        {
                            "name": "skills_header_text",
                            "type": "text",
                            "x": 0, "y": -1,
                            "all_align": "center",
                            "outline": "1",
                            "text": uiScriptLocale.PET_SKILS,
                        },
                        {
                            "name": "um",
                            "type": "image",
                            "x": 7, "y": 3,
                            "image": IMG_PATH + "um.png",
                            "children": (
                                {
                                    "name": "skill_points",
                                    "type": "text",
                                    "x": 0, "y": -1,
                                    "all_align": "center",
                                    "outline": "1",
                                    "text": "0",
                                },
                            ),
                        },
                    ),
                },
                # ── Skills grid ──
                {
                    "name": "skill_window",
                    "type": "thinboard_circle",
                    "x": 12, "y": 108,
                    "width": 272, "height": 109,
                    "children": (
                        {
                            "name": "skill_board",
                            "type": "image",
                            "x": 9, "y": 18,
                            "image": IMG_PATH + "item-image0.png",
                        },
                        {
                            "name": "skills",
                            "type": "grid_table",
                            "x": 40, "y": 22,
                            "start_index": 0,
                            "x_count": 6,
                            "y_count": 2,
                            "x_step": 32,
                            "y_step": 32,
                            "image": "d:/ymir work/ui/public/Slot_Base.sub",
                        },
                    ),
                },
                # ── Equipment header ──
                {
                    "name": "equip_header",
                    "type": "image",
                    "x": 20, "y": 223,
                    "image": "d:/ymir work/ui/game/buttons/test_image_020.tga",
                    "children": (
                        {
                            "name": "equip_header_text",
                            "type": "text",
                            "x": 0, "y": -1,
                            "all_align": "center",
                            "outline": "1",
                            "text": uiScriptLocale.PET_EQUIPMENT,
                        },
                    ),
                },
                # ── Equipment slots ──
                {
                    "name": "horseshoe_window",
                    "type": "thinboard_circle",
                    "x": 12, "y": 245,
                    "width": 272, "height": 65,
                    "children": (
                        {
                            "name": "horseshoe_board",
                            "type": "image",
                            "x": 9, "y": 10,
                            "image": IMG_PATH + "item-image-base.png",
                            "children": (
                                {
                                    "name": "eqs",
                                    "type": "slot",
                                    "x": 0, "y": 0,
                                    "width": 254, "height": 40,
                                    "slot": (
                                        {"index": item.SLOT_ITEM_NEW_PET_EQ_START,     "x": 51,  "y": 4, "width": 32, "height": 32},
                                        {"index": item.SLOT_ITEM_NEW_PET_EQ_START + 1, "x": 101, "y": 4, "width": 32, "height": 32},
                                        {"index": item.SLOT_ITEM_NEW_PET_EQ_START + 2, "x": 151, "y": 4, "width": 32, "height": 32},
                                    ),
                                },
                            ),
                        },
                    ),
                },
            ),
        },
    ),
}
