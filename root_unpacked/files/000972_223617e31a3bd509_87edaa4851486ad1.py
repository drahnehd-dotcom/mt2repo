import uiScriptLocale
import player
import emoji

ROOT_PATH = "d:/ymir work/ui/game/shopui/"
PATTERN_PATH = "d:/ymir work/ui/pattern/"

MARGIN_X = 12
MARGIN_Y = 30
SLOT_MARGIN_X = 9
SLOT_MARGIN_Y = 9
SLOT_WINDOW_WIDTH = 32 * player.REMOVE_ITEM_SLOT_COUNT_X + 18
SLOT_WINDOW_HEIGHT = 32 * player.REMOVE_ITEM_SLOT_COUNT_Y + 18
WINDOW_WIDTH = SLOT_WINDOW_WIDTH + MARGIN_X * 2
WINDOW_HEIGHT = SLOT_WINDOW_HEIGHT + MARGIN_Y * 2.5

window = {
	"name" : "RemoveItemDialog",
	"style": ("movable", "float",),
	"x" : SCREEN_WIDTH/2,
	"y" : SCREEN_HEIGHT/2,
	"width" : WINDOW_WIDTH,
	"height" : WINDOW_HEIGHT,
	"children" :
	(
		{
			"name" : "board",
			"type" : "board_with_titlebar",
			"style": ("attach",),
			"x" : 0,
			"y" : 0,
			"width" : WINDOW_WIDTH,
			"height" : WINDOW_HEIGHT,
			"title" : uiScriptLocale.REMOVE_ITEM_TITLE,
			"children" :
			(
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
								"x_count": player.REMOVE_ITEM_SLOT_COUNT_X,
								"y_count": player.REMOVE_ITEM_SLOT_COUNT_Y,
								"x_step": 32,
								"y_step": 32,
								"x_blank": 0,
								"y_blank": 0,
								"image": "d:/ymir work/ui/public/slot_base.sub",
							},
						),
				},
				{
					"name" : "remove_button",
					"type" : "button",

					"x" : 21,
					"y" : 117,
					"horizontal_align" : "left",
					"vertical_align" : "center",
					"text" : uiScriptLocale.REMOVE_ITEM_REMOVE,
					"outline":1,
					"default_image" : "d:/ymir work/ui/new_btn0.png",
					"over_image" : "d:/ymir work/ui/new_btn1.png",
					"down_image" : "d:/ymir work/ui/new_btn0.png",
				},
				{
					"name" : "clear_button",
					"type" : "button",
					"x" : 136,
					"y" : 117,
					"horizontal_align" : "right",
					"vertical_align" : "center",
					"text" : uiScriptLocale.REMOVE_ITEM_CLEAR,
					"outline":1,
					"default_image" : "d:/ymir work/ui/new_btn0.png",
					"over_image" : "d:/ymir work/ui/new_btn1.png",
					"down_image" : "d:/ymir work/ui/new_btn0.png",
				},
			),
		},
		{
			"name" : "InfoBtn",
			"type" : "button",
			"x" : 18,
			"y" : 6,
			"default_image" : "d:/ymir work/ui/pattern/q_mark_01.tga",
			"over_image" : "d:/ymir work/ui/pattern/q_mark_02.tga",
			"down_image" : "d:/ymir work/ui/pattern/q_mark_01.tga",
            "tooltip_text_new": uiScriptLocale.REMOVE_ITEM_DIALOG.format(emoji.AppendEmoji("icon/emoji/key_shift.png"), 
                                                                         emoji.AppendEmoji("icon/emoji/key_rclick.png")),
			"tooltip_text_color" : 0xfff1e6c0,
			"tooltip_x" : 0,
			"tooltip_y" : -35,
		},
	),
}