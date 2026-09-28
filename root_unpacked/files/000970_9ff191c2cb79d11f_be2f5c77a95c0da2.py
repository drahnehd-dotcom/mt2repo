#-*- coding: iso-8859-1 -*-
import uiScriptLocale
import localeInfo

BUTTON_ROOT = "d:/ymir work/ui/public/"
PATH = "d:/ymir work/ui/"
PATH1 = "d:/ymir work/ui/bonus_window/"
BOARD_WIDTH = 246
BOARD_HEIGHT = 240

window = {
	"name" : "SearchWindow",
	"x" : 0,
	"y" : SCREEN_HEIGHT/1.75,
	"style" : ("movable", "float",),
	"width" : BOARD_WIDTH,
	"height" : 305,
	"children" :
	(
		{
			"name" : "border",
			"type" : "border_a",
			"x" : 0,
			"y" : 10,
			"horizontal_align":"center",
			"vertical_align":"center",
			"width" : BOARD_WIDTH-20,
			"height" : BOARD_HEIGHT-40,
			"children" :
			(
				{
					"name" : "nazwa_window",
					"type" : "window",
					"x" : 0, "y" : 16,
					"horizontal_align":"center",
					"vertical_align":"center",
					"width" : 218, "height" : 225,
					"children":
					(
						{
							"name" : "header_s",
							"type" : "image",
							"x" : 0, "y" : 0,
							"image" : PATH+"header_s.png",
							"children":
							(
								{
									"name" : "header_s_text",
									"type" : "text",
									"x" : 0, "y" : 0,
									"text" : uiScriptLocale.QUEUE_TITLE,
									"all_align":"center",
									"outline":1,
									"fontname":"Tahoma:16",
								},
							),
						},
						{
							"name" : "border2",
							"type" : "border_a",
							"x" : 0, "y" : 25,
							"width" : 218, "height" : 167,
							"children":
							(
								{
									"name" : "window",
									"type" : "window",
									"x" : 0, "y" : 0,
									"width" : 218, "height" : 167,
									"children":
									(
										
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

