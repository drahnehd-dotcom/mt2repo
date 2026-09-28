import uiScriptLocale

ROOT_PATH = "d:/ymir work/ui/game/wonexchange/"

BOARD_ADD_X = 0
BOARD_ADD_X += 50
BOARD_ADD_X += 60
BOARD_ADD_X += 26
BOARD_X = SCREEN_WIDTH - (300 + BOARD_ADD_X)

window = {
	"name" : "WonExchangeWindow", "style" : ("movable", "float", "ltr"),
	"x" : BOARD_X, "y" : SCREEN_HEIGHT - 65 - 200,
	"width" : 197, "height" : 190,
	"children" :
	(
		{
			"name" : "board", "type" : "board", "style" : ("attach",),
			"x" : 0, "y" : 0,
			"width" : 197, "height" : 190,
			"children" :
			(
				{
					"name" : "SellWon_TitleBar", "type" : "titlebar", "style" : ("attach",),
					"x" : 6, "y" : 7,
					"width" : 184, "color" : "red",
					"children" :
					(
						{ "name":"TitleName", "type":"text", "x":0, "y":-4, "text":uiScriptLocale.WONEXCHANGE_TITLE_SELL, "outline":"1","all_align":"center" },
					),
				},
				{
					"name" : "BuyWon_TitleBar", "type" : "titlebar", "style" : ("attach",),
					"x" : 6, "y" : 7,
					"width" : 184, "color" : "red",
					"children" :
					(
						{ "name":"TitleName", "type":"text", "x":0, "y":-4, "text":uiScriptLocale.WONEXCHANGE_TITLE_BUY, "outline":"1","all_align":"center" },
					),
				},
				{
					"name" : "TabControl",
					"type" : "window",

					"x" : 0, "y" : 121,
					"width" : 145, "height" : 59,
					"children" :
					(
						{
							"name" : "Tab_01", "type" : "image",
							"x" : 0, "y" : 30,
							"width" : 145, "height" : 29,
							"image" : ROOT_PATH+"tab_01.sub",
						},
						{
							"name" : "Tab_02", "type" : "image",
							"x" : 0, "y" : 30,
							"width" : 145, "height" : 29,
							"image" : ROOT_PATH+"tab_02.sub",
						},
						{
							"name" : "Tab_Button_01", "type" : "radio_button",
							"x" : 0, "y" : 35,
							"width" : 70, "height" : 22,
						},
						{
							"name" : "Tab_Button_02", "type" : "radio_button",
							"x" : 55, "y" : 35,
							"width" : 70, "height" : 22,
						},
					),
				},
				{
					"name" : "CurrencyConverter_Page", "type" : "window", "style" : ("attach",),
					"x" : 0, "y" : 24,
					"width" : 192, "height" : 115,
					"children" :
					(
						{
							"name" : "CThinBoard", "type" : "thinboard_circle", "style" : ("attach",),
							"x" : 11, "y" : 12,
							"width" : 174, "height" : 115,
							"children" :
							(
								{
								 	"name" : "separator",
								 	"type" : "image",
								 	"x": -14, "y": 26,
								 	"image" : "d:/ymir work/ui/game/buttons/separator.tga",  
								}, 
								{
									"name":"InputSlot", "type":"image",
									"x": 9, "y":20,
									"image" : "d:/ymir work/ui/exchangeinput.tga",
									"children" :
									(
										{
											"name":"WonIcon", "type":"expanded_image", "style" : ("attach",),
											"x": 5, "y": 4,
											"x_scale" : .8, "y_scale" : .8,
											"image":"d:/ymir work/ui/game/windows/cheque_icon.sub",
										},
										{
											"name" : "Input", "type" : "editline",
											"x" : 25, "y" : 3,
											"width" : 100, "height" : 18,
											"input_limit" : 6,
											"enable_codepage" : 0,
											"only_number" : 1,
											"r" : 1.0, "g" : 1.0, "b" : 1.0, "a" : 1.0,
										},
									),
								},
								{
									"name":"ResultSlot", "type":"image",
									"x": 9, "y":60,
									"image" : "d:/ymir work/ui/exchangeinput.tga",
									"children" :
									(
										{
											"name":"GoldIcon", "type":"expanded_image", "style" : ("attach",),
											"x": 5, "y": 4,
											"x_scale" : .6, "y_scale" : .6,
											"image":"icon/emoji/money_icon.png",
										},
										{
											"name" : "Result", "type" : "text",
											"x" : 25, "y" : 3,
											"horizontal_align" : "left",
											"text_horizontal_align" : "left",
											"text" : "",
										},
									),
								},
								{
									"name" : "AcceptButton", "type" : "button",
									"horizontal_align" : "center",
									"x" : 0, "y" : 85,
									"default_image"	: "d:/ymir work/ui/public/acceptbutton00.sub",
									"over_image"	: "d:/ymir work/ui/public/acceptbutton01.sub",
									"down_image"	: "d:/ymir work/ui/public/acceptbutton02.sub",
								},
							),
						},
					),
				},
			),
		},
	),
}
