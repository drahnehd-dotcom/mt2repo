import uiScriptLocale
import player

PAGE_NUM = player.SAVE_MAP_PAGE_MAX_NUM
ROOT_PATH = "d:/ymir work/ui/game/save/"
BOARD_WIDTH = 367
BOARD_HEIGHT = 295
PATH = "d:/ymir work/ui/location_window/"

window = {
	"name": "SaveMapDialog",
	"x": 0,
	"y": 0,
	"style": (
		"movable",
		"float",
	),
	"width": BOARD_WIDTH,
	"height": BOARD_HEIGHT+30,
	"children": (
		{
			"name" : "page_board",
			"type" : "board",
			"x" : 0, "y" : BOARD_HEIGHT-30,
			"width" : 110, "height" : 20,
			"horizontal_align" : "center",
			"children" :
			(
				{
					"name":"PageSlotbar", "type":"image",
					"x": 0, "y": 30,
					"horizontal_align":"center",
					"image":"d:/ymir work/ui/location_window/slotbar-84x23.png",
					"children": 
					(
						{
							"name":"PrevPageBtn", "type":"button",
							"x": 10, "y": 5,
							"default_image":"d:/ymir work/ui/location_window/btn-left-0.png",
							"over_image":"d:/ymir work/ui/location_window/btn-left-1.png",
							"down_image":"d:/ymir work/ui/location_window/btn-left-2.png",
						},
						{
							"name":"PageText","type":"text",
							"x":0,"y":0,
							"all_align":"center",
							"text":"-1",
							"fontname":"Tahoma:14b",
							"outline":"1",
						},
						{
							"name":"NextPageBtn", "type":"button",
							"x": 60, "y": 5,
							"default_image":"d:/ymir work/ui/location_window/btn-right-0.png",
							"over_image":"d:/ymir work/ui/location_window/btn-right-1.png",
							"down_image":"d:/ymir work/ui/location_window/btn-right-2.png",
						},  
					),
				},
			),
		},
		{
			"name" : "board",
			"type" : "board",
			"x" : 0, "y" : 0,
			"width" : BOARD_WIDTH, "height" : BOARD_HEIGHT,
			"children" :
			(
				{
					"name" : "TitleBar",
					"type" : "titlebar",
					"style" : ("attach",),
					"x" : 8, "y" : 7,
					"width" : BOARD_WIDTH - 15,
					"children" :
					(
						{ "name":"titlename", "type":"text", "x":0, "y":-3,
						"text" : uiScriptLocale.SAVE_MAPS_TITLE,
						"all_align":"center","outline":"1" },
					),
				},
                {
                    "name" : "border",
                    "type" : "border_a",
                    "x" : 0, "y" : 28,
                    "width" : BOARD_WIDTH - 20,
                    "height" : BOARD_HEIGHT - 38,
                    "horizontal_align" : "center",
                    "children":
                    (

                    ),
                },
			),
		},
	),
}

for i in range(5):
	window["children"] += (
		{
			"name" : "slot_window_%02d" % (i + 1),
			"type" : "border_a",
			"x" : 0, "y" : 32 + 50 * i,
			"width" : 339, "height" : 49,
            "horizontal_align" : "center",
            "children" : (
                {
                    "name " : "background",
                    "type" : "image",
                    "x" : 0, "y" : 0,
                    "horizontal_align" : "center",
                    "vertical_align" : "center",
                    "image" : PATH+"background-%d.png" % i,
                    "children":
                    (
                        {
                            "name" : "tooltip",
                            "type" : "thinboard",
                            "x" : -1, "y" : -1,
                            "width" : 335, "height" : 45,
                        },
                    ),
                },
                {
                    "name" : "save_button_%02d" % (i + 1),
                    "type" : "button",
                    "x" : 123, "y" : 3,
                    "horizontal_align" : "right",
                    "default_image" : "d:/ymir work/ui/location_window/button_example_001.png",
                    "over_image" : "d:/ymir work/ui/location_window/button_example_002.png",
                    "down_image" : "d:/ymir work/ui/location_window/button_example_003.png",
                    "children":
                    (
                        {
                            "name" : "location_button_text",
                            "type" : "text",
                            "x" : 0, "y" : 0,
                            "text" : uiScriptLocale.SAVEMAP_SAVE,
                            "all_align" : "center",
                            "outline" : 1,
                            "fontname" : "Tahoma:14b",
                        },
                    ),
                },
                {
                    "name": "teleport_button_%02d" % (i + 1),
                    "type" : "button",
                    "x" : 123, "y" : 26,
                    "horizontal_align" : "right",
                    "default_image" : "d:/ymir work/ui/location_window/button_example_001.png",
                    "over_image" : "d:/ymir work/ui/location_window/button_example_002.png",
                    "down_image" : "d:/ymir work/ui/location_window/button_example_003.png",
                    "children":
                    (
                        {
                            "name" : "location_button_text",
                            "type" : "text",
                            "x" : 0, "y" : 0,
                            "text" : uiScriptLocale.SAVEMAP_LOAD,
                            "all_align" : "center",
                            "outline" : 1,
                            "fontname" : "Tahoma:14b",
                        },
                    ),
                },
                {
                    "name": "qmark_%02d" % (i + 1),
                    "type" : "image",
                    "x" : 10, "y" : 15,
                    "image" : "d:/ymir work/ui/pattern/q_mark_01.tga",
                },
                {
                    "name": "input_name_%02d" % (i + 1),
                    "type": "text",
                    "x": -60,
                    "y": -12,
                    "all_align": "center",
                    "text": uiScriptLocale.SAVEMAP_TEST,
                    "outline" : 1,
                    "fontname" : "Tahoma:14",
                },
                {
                    "name": "input_cord_%02d" % (i + 1),
                    "type": "text",
                    "x": -60,
                    "y": 10,
                    "all_align": "center",
                    "text": "(0, 0)",
                    "outline" : 1,
                },
            ),
		},
	)