import uiScriptLocale

WIDTH = 312
HEIGHT = 175
THINBOARD_WIDTH = 290
THINBOARD_HEIGHT = 44
GREEN_COLOR = 0xffc3d4c4
ROOT_PATH = "d:/ymir work/ui/public/"

window = {
    "name": "GMPanelWindow",

    "x" : SCREEN_WIDTH / 2 - WIDTH / 2,
    "y" : SCREEN_HEIGHT / 2 - HEIGHT / 2,

    "style": ("movable", "float",),

    "width": WIDTH,
    "height": HEIGHT,

    "children":
    (
        {
            "name": "board",
            "type": "board",
            "style": ("attach",),

            "x": 0,
            "y": 0,

            "width": WIDTH,
            "height": HEIGHT,

            "children":
            (
                {
                    "name": "TitleBar",
                    "type": "titlebar",
                    "style": ("attach",),

                    "x": 8,
                    "y": 6,

                    "width": WIDTH - 13,
                    "color": "yellow",

                    "children":
                    (
                        {"name": "TitleName", "type": "text", "x": 0, "y": -4, "text": uiScriptLocale.STONE_DETACH_TITLE, "outline":"1", "all_align": "center"},
                    ),
                },
                {
                    "name": "StoneWindow1",
                    "type": "window",

                    "x": 10,
                    "y": 32,
                    "width": WIDTH - 20,
                    "height": THINBOARD_HEIGHT,
                    "children":
                    (
                        {
                            "name": "Metin1Thinboard",
                            "type": "thinboard_circle",
                            "x": 0,
                            "y": 0,
                            "width": THINBOARD_WIDTH,
                            "height": THINBOARD_HEIGHT,
                            "children":
                            (
                                {
                                    "name": "MetinImage1",
                                    "type": "image",
                                    "x": 42,
                                    "y": 1,
                                    "image": "d:/ymir work/ui/detach_slot.png",
                                    "children":
                                        (
                                            {"name":"window","type":"window","x":0,"y":0,"width":202,"height":20,"children":
                                             (
                                                {"name": "MetinName1", "type": "text", "x": 0, "all_align":"center", "y": 0, "outline":"1", "text": ""},
                                                {"name": "MetinBonus1", "type": "text", "x": 0, "all_align":"center", "y": 19, "outline":"1",
                                                "text": "", "color": GREEN_COLOR},
                                             ),
                                            },
                                        ),
                                },
                                {
                                    "name": "MetinImage1",
                                    "type": "image",
                                    "x": 1,
                                    "y": 1,
                                    "image": "d:/ymir work/ui/detach_slot2.png",
                                },
                            ),
                        },
                        {
                            "name": "MetinButton1",
                            "type": "button",

                            "x": THINBOARD_WIDTH - 45,
                            "y": 0,
                            "vertical_align": "center",

                            "default_image": "d:/ymir work/ui/accept0.tga",
                            "over_image": "d:/ymir work/ui/accept1.tga",
                            "down_image": "d:/ymir work/ui/accept2.tga",
                        },
                    ),
                },
                {
                    "name": "StoneWindow2",
                    "type": "window",

                    "x": 10,
                    "y": 75,
                    "width": WIDTH - 20,
                    "height": THINBOARD_HEIGHT,
                    "children":
                    (
                        {
                            "name": "Metin2Thinboard",
                            "type": "thinboard_circle",
                            "x": 0,
                            "y": 0,
                            "width": THINBOARD_WIDTH,
                            "height": THINBOARD_HEIGHT,
                            "children":
                            (
                                {
                                    "name": "MetinImage2",
                                    "type": "image",
                                    "x": 42,
                                    "y": 1,
                                    "image": "d:/ymir work/ui/detach_slot.png",
                                    "children":
                                        (
                                            {"name":"window","type":"window","x":0,"y":0,"width":202,"height":20,"children":
                                             (
                                                {"name": "MetinName2", "type": "text", "x": 0, "all_align":"center", "y": 0, "outline":"1", "text": ""},
                                                {"name": "MetinBonus2", "type": "text", "x": 0, "all_align":"center", "y": 19, "outline":"1",
                                                "text": "", "color": GREEN_COLOR},
                                             ),
                                            },
                                        ),
                                },
                                {
                                    "name": "MetinImage2",
                                    "type": "image",
                                    "x": 1,
                                    "y": 1,
                                    "image": "d:/ymir work/ui/detach_slot2.png",
                                },
                            ),
                        },
                        {
                            "name": "MetinButton2",
                            "type": "button",

                            "x": THINBOARD_WIDTH - 45,
                            "y": 0,
                            "vertical_align": "center",

                            "default_image": "d:/ymir work/ui/accept0.tga",
                            "over_image": "d:/ymir work/ui/accept1.tga",
                            "down_image": "d:/ymir work/ui/accept2.tga",
                        },
                    ),
                },
                {
                    "name": "StoneWindow3",
                    "type": "window",

                    "x": 10,
                    "y": 118,
                    "width": WIDTH - 20,
                    "height": THINBOARD_HEIGHT,
                    "children":
                    (
                        {
                            "name": "Metin3Thinboard",
                            "type": "thinboard_circle",
                            "x": 0,
                            "y": 0,
                            "width": THINBOARD_WIDTH,
                            "height": THINBOARD_HEIGHT,
                            "children":
                            (
                                {
                                    "name": "MetinImage3",
                                    "type": "image",
                                    "x": 42,
                                    "y": 1,
                                    "image": "d:/ymir work/ui/detach_slot.png",
                                    "children":
                                        (
                                            {"name":"window","type":"window","x":0,"y":0,"width":202,"height":20,"children":
                                             (
                                                {"name": "MetinName3", "type": "text", "x": 0, "all_align":"center", "y": 0, "outline":"1", "text": ""},
                                                {"name": "MetinBonus3", "type": "text", "x": 0, "all_align":"center", "y": 19, "outline":"1",
                                                "text": "", "color": GREEN_COLOR},
                                             ),
                                            },
                                        ),
                                },
                                {
                                    "name": "MetinImage3",
                                    "type": "image",
                                    "x": 1,
                                    "y": 1,
                                    "image": "d:/ymir work/ui/detach_slot2.png",
                                },
                            ),
                        },
                        {
                            "name": "MetinButton3",
                            "type": "button",

                            "x": THINBOARD_WIDTH - 45,
                            "y": 0,
                            "vertical_align": "center",

                            "default_image": "d:/ymir work/ui/accept0.tga",
                            "over_image": "d:/ymir work/ui/accept1.tga",
                            "down_image": "d:/ymir work/ui/accept2.tga",
                        },
                    ),
                },
            ),
        },
    ),
}