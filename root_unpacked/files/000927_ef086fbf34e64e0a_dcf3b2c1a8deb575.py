import uiScriptLocale

ROOT_PATH = "d:/ymir work/ui/game/itemshop/select_attr/"

window = {
	"name" : "ItemShopSelectItemDialog",
	"style" : ("movable", "float",),

	"x" : (SCREEN_WIDTH - 620) / 2,
	"y" : (SCREEN_HEIGHT - 355) / 2,

	"width": 620,
	"height": 355,

	"children" : (
		{
			"name" : "board",
			"type" : "image",

			"x" : -34,
			"y" : -34,

			"image" : ROOT_PATH + "board.tga",
		},
		{
			"name" : "main_board",
			"type" : "window",
			"style" : ("attach",),

			"x": 0,
			"y": 0,

			"width": 620,
			"height": 355,

			"children" :
			(
				{
					"name" : "pvp_wnd",
					"type" : "window",

					"x" : 36,
					"y" : 15,

					"width" : 261,
					"height" : 152,

					"children" : (
						{
							"name" : "pvp_image",
							"type" : "image",
							"style" : ("attach",),

							"x" : 0,
							"y" : 0,

							"image" : ROOT_PATH + "pvp_image.tga",
						},
						{
							"name" : "pvp_button",
							"type" : "radio_button",

							"x" : 0,
							"y" : 116,

							"horizontal_align" : "center",

							"default_image": ROOT_PATH + "bonus_button_01.tga",
							"over_image": ROOT_PATH + "bonus_button_02.tga",
							"down_image": ROOT_PATH + "bonus_button_03.tga",

							"children": (
								{
									"name": "pvp_button_text",
									"type": "text",

									"x": 0,
									"y": 0,

									"all_align": "center",

									"fontname": "Tahoma:14b",
									"outline": True,

									"text": uiScriptLocale.ITEMSHOP_ATTRIBUTE_PVP,
								},
							),
						},
					),
				},
				{
					"name" : "exp_wnd",
					"type" : "window",

					"x" : 323,
					"y" : 15,

					"width" : 261,
					"height" : 152,

					"children" : (
						{
							"name" : "exp_image",
							"type" : "image",
							"style" : ("attach",),

							"x" : 0,
							"y" : 0,

							"image" : ROOT_PATH + "exp_image.tga",
						},
						{
							"name" : "exp_button",
							"type" : "radio_button",

							"x" : 0,
							"y" : 116,

							"horizontal_align" : "center",

							"default_image": ROOT_PATH + "bonus_button_01.tga",
							"over_image": ROOT_PATH + "bonus_button_02.tga",
							"down_image": ROOT_PATH + "bonus_button_03.tga",

							"children": (
								{
									"name": "exp_button_text",
									"type": "text",

									"x": 0,
									"y": 0,

									"all_align": "center",

									"fontname": "Tahoma:14b",
									"outline": True,

									"text": uiScriptLocale.ITEMSHOP_ATTRIBUTE_EXP,
								},
							),
						},
					),
				},
				{
					"name" : "attribute_board",
					"type" : "image",
					"style" : ("attach",),

					"x" : 0,
					"y" : 179,

					"horizontal_align" : "center",

					"image" : ROOT_PATH + "attribute_board.tga",
				},
				{
					"name" : "buy_button",
					"type" : "button",

					"x" : 0,
					"y" : 296,

					"horizontal_align" : "center",

					"default_image": ROOT_PATH + "buy_button_01.tga",
					"over_image": ROOT_PATH + "buy_button_02.tga",
					"down_image": ROOT_PATH + "buy_button_03.tga",

					"children": (
						{
							"name": "buy_button_text",
							"type": "text",

							"x": 0,
							"y": 0,

							"all_align": "center",

							"fontname": "Tahoma:14b",
							"outline": True,

							"text": uiScriptLocale.ITEMSHOP_ATTRIBUTE_BUY,
						},
					),
				},
			),
		},
	),
}