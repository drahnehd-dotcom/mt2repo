import uiScriptLocale
import player
import emoji

ROOT_PATH = "d:/ymir work/ui/game/shopui/"
PATTERN_PATH = "d:/ymir work/ui/pattern/"
MARGIN_X = 12
MARGIN_Y = 30
SLOT_MARGIN_X = 10
SLOT_MARGIN_Y = 10
SLOT_WINDOW_WIDTH = 32 * 8.32 + 10

Y_COUNT = 3

SLOT_WINDOW_HEIGHT = 32 * Y_COUNT + 20
WINDOW_WIDTH = SLOT_WINDOW_WIDTH + MARGIN_X + 13
WINDOW_HEIGHT = SLOT_WINDOW_HEIGHT + MARGIN_Y + 45

USE_BUTTON_HEIGHT = WINDOW_HEIGHT-40

window = {
	"name" : "DopalaczeDialog",
	"style": ("movable", "float",),
	"x" : SCREEN_WIDTH/2,
	"y" : SCREEN_HEIGHT/2,
	"width" : WINDOW_WIDTH,
	"height" : WINDOW_HEIGHT,

	"children" :
	(
		{
			"name" : "board",
			"type" : "board",
			"x" : 0,
			"y" : 0,
			"width" : WINDOW_WIDTH,
			"height" : WINDOW_HEIGHT,
			"children" :
			(
				{
					"name" : "TitleBar",
					"type" : "titlebar",
					"style" : ("attach",),
					"x" : 8,"y" : 7,
					"width" : WINDOW_WIDTH-15,
					"color" : "yellow",
					"children" :
					(
						{ 
							"name": "TitleName",
							"type":"text",
							"x":WINDOW_WIDTH/2,"y":0,
							"text": uiScriptLocale.BOOSTER_WINDOW_TITLE,
                            "outline":"1",
							"text_horizontal_align":"center",
						},
						{
							"name" : "clear_button",
							"type" : "button",
							"x" : 10,
							"y" : -2,
							"default_image" : "d:/ymir work/ui/close_btn_dop0.png",
							"over_image" : "d:/ymir work/ui/close_btn_dop1.png",
							"down_image" : "d:/ymir work/ui/close_btn_dop2.png",

							"tooltip_text_new" : uiScriptLocale.BOOSTER_WINDOW_CLOSE,
							"tooltip_text_color" : 0xfff1e6c0,
							"tooltip_x" : 0,
							"tooltip_y" : -35,
						},
					),
				},
				{
					"name": "main_bg_window",
					"type": "border_a",
					"style": ("attach", "ltr",),
					"x": MARGIN_X,
					"y": MARGIN_Y,
					"width": SLOT_WINDOW_WIDTH,
					"height": SLOT_WINDOW_HEIGHT,

					"children":
						(
							{
								"name": "item_slot",
								"type": "grid_table",

								"start_index": 0,

								"x": SLOT_MARGIN_X,
								"y": SLOT_MARGIN_Y,

								"x_count": 8,
								"y_count": Y_COUNT,
								"x_step": 32,
								"y_step": 32,
								"x_blank": 0,
								"y_blank": 0,

								"image": "d:/ymir work/ui/public/slot_base.sub",
							},
						),
				},
				{
					"name" : "use_button",
					"type" : "button",
					"x" : 0,
					"y" : USE_BUTTON_HEIGHT,
					"horizontal_align" : "center",
					"default_image" : "d:/ymir work/ui/button-accept-0.png",
					"over_image" : "d:/ymir work/ui/button-accept-1.png",
					"down_image" : "d:/ymir work/ui/button-accept-2.png",
				},
			),
		},
	),
}