import uiScriptLocale
BOARD_WIDTH = 160
BOARD_HEIGHT = 100

window = {
    "name": "MallIS_Window",
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
                            "text": uiScriptLocale.ITEMSHOP_STORAGE_WINDOW_1,
                            "outline": "1",
                            "all_align": "center",
                        },
                    ),
                },
                {
                    "name": "thinboard",
                    "type": "thinboard_circle",
                    "x": 0, "y": 10,
                    "vertical_align": "center",
                    "horizontal_align": "center",
                    "width": 140, "height": 60,
                    "children": (
                        {
                            "name": "IsButton",
                            "type": "button",
                            "x": 0, "y": -10,
                            "vertical_align": "center",
                            "horizontal_align": "center",
                            "text": uiScriptLocale.ITEMSHOP_STORAGE_WINDOW_2,
                            "outline": 1,
                            "default_image": "d:/ymir work/ui/location_window/button_example_001.png",
                            "over_image": "d:/ymir work/ui/location_window/button_example_002.png",
                            "down_image": "d:/ymir work/ui/location_window/button_example_003.png",
                        },
                        {
                            "name": "DepoButton",
                            "type": "button",
                            "x": 0, "y": 11,
                            "vertical_align": "center",
                            "horizontal_align": "center",
                            "text": uiScriptLocale.ITEMSHOP_STORAGE_WINDOW_3,
                            "outline": 1,
                            "default_image": "d:/ymir work/ui/location_window/button_example_001.png",
                            "over_image": "d:/ymir work/ui/location_window/button_example_002.png",
                            "down_image": "d:/ymir work/ui/location_window/button_example_003.png",
                        },
                    ),
                },
            ),
        },
    ),
}
