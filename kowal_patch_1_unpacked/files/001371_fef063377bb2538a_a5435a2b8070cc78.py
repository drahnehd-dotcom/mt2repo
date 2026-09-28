import uiScriptLocale
import localeInfo

BOARD_WIDTH = 292
BOARD_HEIGHT = 453

window = {
	"name" : "OfflineShopBankWindow",
	"style" : ("movable", "float", ),
	"x" : 0,"y" : 0,
	"width" : BOARD_WIDTH,"height" : BOARD_HEIGHT,
	"children" :
	(
		{
			"name" : "Board",
			"type" : "board_with_titlebar",
			"style" : ("attach", ),
			"x" : 0,"y" : 0,
			"width" : BOARD_WIDTH,"height" : BOARD_HEIGHT,
			"title" : localeInfo.OFFLINE_SHOP_BANK_TITLE,
			"children" :
			(
				{
					"name" : "Header",
					"type" : "image",
					"x": 17, "y": 35,
					"image" : "d:/ymir work/ui/offline_shop/test_image_020.tga",
					"children" :
					(
						{
							"name" : "MoneyLine",
							"type" : "text",
							"x": 5,"y": 0,
							"text" : uiScriptLocale.OFFLINE_SHOP_EXPECTED_EARNINGS,
							"outline" : "1",
						},
					),
				},
                {
                  	"name" : "separator",
					"type" : "image",
					# "x": 35, "y": 80,
					"x": 35, "y": 343,
					"image" : "d:/ymir work/ui/offline_shop/separator.tga",  
				},
                {
                  	"name" : "separator2",
					"type" : "image",
					# "x": 35, "y": 80,
					"x": 35, "y": 218,
					"image" : "d:/ymir work/ui/offline_shop/separator.tga",  
				},
                {
                  	"name" : "separator2",
					"type" : "image",
					# "x": 35, "y": 80,
					"x": 35, "y": 82,
					"image" : "d:/ymir work/ui/offline_shop/separator.tga",  
				},
                {
                    "name" : "ThinBoard",
                    "type" : "thinboard_new",
                    "x": 8, "y": 60,
                    "width":274,"height":96,
                    "children" :
                    (
						{
							"name" : "zarobekyang",
							"type" : "image",
							"x" : 10,"y" : 15,
							"image" : "d:/ymir work/ui/offline_shop/button-example-experiment.png",
                            "children" :
                            (
								{
									"name" : "CurrentMoneyZarobek",
									"type" : "text",
									"x": 0,"y": 0,
									"text" : "",
									"outline" : "1",
                                    "all_align" : "center",
								},
							),
						},
						{
							"name" : "zarobekwon",
							"type" : "image",
							"x" : 10,"y" : 60,
							"image" : "d:/ymir work/ui/offline_shop/button-example-experiment.png",
							"children" :
							(
								{
									"name" : "CurrentChequeZarobek",
									"type" : "text",
									"x": 0,"y": 0,
									"text" : "",
									"outline" : "1",
									"all_align" : "center",
								},
							),
						},
					),
				},
                ###############
				{
					"name" : "Header",
					"type" : "image",
					"x": 17, "y": 168,
					"image" : "d:/ymir work/ui/offline_shop/test_image_020.tga",
					"children" :
					(
						{
							"name" : "MoneyLine",
							"type" : "text",
							"x": 5,"y": 0,
							"text" : uiScriptLocale.OFFLINE_SHOP_EARNINGS,
							"outline" : "1",
						},
					),
				},
                {
                    "name" : "ThinBoard",
                    "type" : "thinboard_new",
                    "x": 8, "y": 195,
                    "width":274,"height":96,
                    "children" :
                    (
						{
							"name" : "MoneyInfo",
							"type" : "image",
							"x" : 10,"y" : 15,
							"image" : "d:/ymir work/ui/offline_shop/button-example-experiment.png",
                            "children" :
                            (
								{
									"name" : "CurrentMoneyLine",
									"type" : "text",
									"x": 0,"y": 0,
									"text" : "",
									"outline" : "1",
                                    "all_align" : "center",
								},
							),
						},
						{
							"name" : "ChequeInfo",
							"type" : "image",
							"x" : 10,"y" : 60,
							"image" : "d:/ymir work/ui/offline_shop/button-example-experiment.png",
							"children" :
							(
								{
									"name" : "CurrentChequeLine",
									"type" : "text",
									"x": 0,"y": 0,
									"text" : "",
									"outline" : "1",
									"all_align" : "center",
								},
							),
						},
					),
				},
				{
					"name" : "Header",
					"type" : "image",
					"x": 17, "y": 300,
					"image" : "d:/ymir work/ui/offline_shop/test_image_020.tga",
					"children" :
					(
						{
							"name" : "MoneyLine",
							"type" : "text",
							"x": 5,"y": 0,
							"text" : uiScriptLocale.OFFLINE_SHOP_TAKE_YANG_VALUE,
							"outline" : "1",
						},
					),
				},
                {
                    "name" : "ThinBoard2",
                    "type" : "thinboard_new",
                    "x": 8, "y": 325,
                    "width":274,"height":85,
                    "children" :
                    (
						{
							"name" : "RequiredMoneySlot",
							"type" : "slotbar",
							"x" : 0,"y" : 15,
							"width" : 210,
							"height" : 15,
							"horizontal_align" : "center",	
							"children" :
							(
								{
									"name" : "RequiredMoneyLine",
									"type" : "editline",
									"x" : 3,"y" : 1,
									"width" : 210,"height" : 15,
									"input_limit" : 15,
									"text" : "",
								},
							),
						},
						{
							"name" : "RequiredChequeSlot",
							"type" : "slotbar",
							"x" : 0,"y" : 53,
							"width" : 210,
							"height" : 15,
							"horizontal_align" : "center",	
							"children" :
							(
								{
									"name" : "RequiredChequeLine",
									"type" : "editline",
									"x" : 3,"y" : 1,
									"width" : 210,"height" : 15,
									"input_limit" : 15,
									"text" : "",
								},
							),
						},
					),
				},
				{
					"name" : "withdraw_button",
					"type" : "button",
					"x" : -100,"y" : 205,
					"horizontal_align" : "center",
					"vertical_align" : "center",
					"default_image" : uiScriptLocale.LOCALE_OFFLINESHOP_PATH + "/accept_01.tga",
					"over_image" : uiScriptLocale.LOCALE_OFFLINESHOP_PATH + "/accept_02.tga",
					"down_image" : uiScriptLocale.LOCALE_OFFLINESHOP_PATH + "/accept_03.tga",
				},
				{
					"name" : "withdrawall_button",
					"type" : "button",
					"x" : 0,"y" : 203,
					"horizontal_align" : "center",
					"vertical_align" : "center",
                    "text": uiScriptLocale.OFFLINE_SHOP_TAKE_ALL,
					"default_image" : "d:/ymir work/ui/location_window/button_example_001.png",
					"over_image" : "d:/ymir work/ui/location_window/button_example_002.png",
					"down_image" : "d:/ymir work/ui/location_window/button_example_003.png",
				},
				{
					"name" : "cancel_button",
					"type" : "button",
					"x" : 100,"y" : 205,
					"horizontal_align" : "center",
					"vertical_align" : "center",
					"default_image" : uiScriptLocale.LOCALE_OFFLINESHOP_PATH + "/no_01.tga",
					"over_image" : uiScriptLocale.LOCALE_OFFLINESHOP_PATH + "/no_02.tga",
					"down_image" : uiScriptLocale.LOCALE_OFFLINESHOP_PATH + "/no_03.tga",
				},	
			),
		},
	),
}