import uiScriptLocale
import localeInfo

BOARD_WIDTH = 292
BOARD_HEIGHT = 300

window = {
	"name" : "OfflineShopAdminPanelWindow",
	"style" : ("movable", "float",),
	"x" : 0,"y" : 0,
	"width" : BOARD_WIDTH,"height" : BOARD_HEIGHT+60,
	"children":
	(
		{
			"name" : "board_logs",
			"type" : "board",
			"x": 0, "y": 275,
			"horizontal_align":"center",
			"width": 150,"height": 30,
			"children" :
			(
				{
					"name" : "LogsButton",
					"type" : "button",

					"x" : 0,
					"y" : 30,
                    "horizontal_align":"center",

					"default_image" : "d:/ymir work/ui/weekly_rank/button-example-020.png",
					"over_image" : "d:/ymir work/ui/weekly_rank/button-example-021.png",
					"down_image" : "d:/ymir work/ui/weekly_rank/button-example-022.png",
                    "children":
                    (
						{
                            "name":"buybutton_text",
                            "type":"text",
                            "x":0,"y":0,
                            "all_align":"center",
                            "text" : uiScriptLocale.OFFLINE_SHOP_HISTORY,
                   			"outline":1,
                    		"fontname":"Tahoma:14b",
						},
					),
				},
			),
		},
		{
			"name" : "Board",
			"type" : "board_with_titlebar",
			"style" : ("attach", ),
			"x" : 0,"y" : 0,
			"width" : BOARD_WIDTH,"height" : BOARD_HEIGHT,
			"title" : uiScriptLocale.PRIVATE_SHOP_TITLE,
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
							"name" : "HeaderText",
							"type" : "text",
							"x": 5,"y": 0,
							"text" : uiScriptLocale.OFFLINE_SHOP_INFORMATIONS,
							"outline" : "1",
						},
					),
				},
                {
                  	"name" : "separator",
					"type" : "image",
					# "x": 35, "y": 80,
					"x": 35, "y": 90,
					"image" : "d:/ymir work/ui/offline_shop/separator.tga",  
				},
                {
                  	"name" : "separator2",
					"type" : "image",
					# "x": 35, "y": 80,
					"x": 35, "y": 187,
					"image" : "d:/ymir work/ui/offline_shop/separator.tga",  
				},
                {
                    "name" : "ThinBoard2",
                    "type" : "thinboard_new",
                    "x": 8, "y": 58,
                    "width":274,"height":50,
                    "children" :
                    (
						{
							"name" : "ShopInfo",
							"type" : "image",
							"x" : 10,"y" : 15,
							"image" : "d:/ymir work/ui/offline_shop/button-example-experiment.png",
                            "children" :
                            (
                              	{
									"name" : "ShopInfoIcon",
									"type" : "image",
									"x" : 7,"y" : 3,
									"image" : "d:/ymir work/ui/offline_shop/test_image_012.png",
								},  
								{
									"name" : "ShopInfoText",
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
					"x": 14, "y": 120,
					"image" : "d:/ymir work/ui/offline_shop/test_image_020.tga",
					"children" :
					(
						{
							"name" : "HeaderText",
							"type" : "text",
							"x": 5,"y": 0,
							"text" : uiScriptLocale.OFFLINE_SHOP_POSSIBLE_SETTINGS,
							"outline" : "1",
						},
					),
				},
                {
                    "name" : "ThinBoard3",
                    "type" : "thinboard_new",
                    "x": 8, "y": 144,
                    "width":274,"height":60,
                    "children" :
                    (
						{
							"name" : "StartShopButton",
							"type" : "button",
							"x" : 4,"y" : 10,
							"tooltip_text_new" : uiScriptLocale.OFFLINE_SHOP_OPEN_SHOP,
							"tooltip_text_color" : 0xfff1e6c0,
							"tooltip_x" : 0,
							"tooltip_y" : -35,
							"default_image" : "d:/ymir work/ui/offline_shop/button_example_160.png",
							"over_image" : "d:/ymir work/ui/offline_shop/button_example_161.png",
							"down_image" : "d:/ymir work/ui/offline_shop/button_example_162.png",
						},
						{
							"name" : "CloseShopButton",
							"type" : "button",
							"x" : 4,"y" : 32,
							"tooltip_text_new" : uiScriptLocale.OFFLINE_SHOP_CLOSE_SHOP,
							"tooltip_text_color" : 0xfff1e6c0,
							"tooltip_x" : 0,
							"tooltip_y" : -57,
							"default_image" : "d:/ymir work/ui/offline_shop/button_example_210.png",
							"over_image" : "d:/ymir work/ui/offline_shop/button_example_211.png",
							"down_image" : "d:/ymir work/ui/offline_shop/button_example_212.png",
						},
						{
							"name" : "FindShopButton",
							"type" : "button",
							"x" : 93,"y" : 10,
							"tooltip_text_new" : uiScriptLocale.OFFLINE_SHOP_SEARCH_ITEM,
							"tooltip_text_color" : 0xfff1e6c0,
							"tooltip_x" : 0,
							"tooltip_y" : -35,
							"default_image" : "d:/ymir work/ui/offline_shop/button_example_030.png",
							"over_image" : "d:/ymir work/ui/offline_shop/button_example_031.png",
							"down_image" : "d:/ymir work/ui/offline_shop/button_example_032.png",
						},
						{
							"name" : "ReceiveMoneyShopButton",
							"type" : "button",
							"x" : 93,"y" : 32,
							"tooltip_text_new" : uiScriptLocale.OFFLINE_SHOP_TAKE_YANG_WON,
							"tooltip_text_color" : 0xfff1e6c0,
							"tooltip_x" : 0,
							"tooltip_y" : -57,
							"default_image" : "d:/ymir work/ui/offline_shop/button_example_250.png",
							"over_image" : "d:/ymir work/ui/offline_shop/button_example_251.png",
							"down_image" : "d:/ymir work/ui/offline_shop/button_example_252.png",
						},
						{
							"name" : "SendItemShopButton",
							"type" : "button",
							"x" : 183,"y" : 10,
							"tooltip_text_new" : uiScriptLocale.OFFLINE_SHOP_ADD_ITEM,
							"tooltip_text_color" : 0xfff1e6c0,
							"tooltip_x" : 0,
							"tooltip_y" : -35,
							"default_image" : "d:/ymir work/ui/offline_shop/button_example_220.png",
							"over_image" : "d:/ymir work/ui/offline_shop/button_example_221.png",
							"down_image" : "d:/ymir work/ui/offline_shop/button_example_222.png",
						},
						{
							"name" : "RemoveItemShopButton",
							"type" : "button",
							"x" : 183,"y" : 32,
							"tooltip_text_new" : uiScriptLocale.OFFLINE_SHOP_DELETE_ITEM,
							"tooltip_text_color" : 0xfff1e6c0,
							"tooltip_x" : 0,
							"tooltip_y" : -57,
							"default_image" : "d:/ymir work/ui/offline_shop/button_example_230.png",
							"over_image" : "d:/ymir work/ui/offline_shop/button_example_231.png",
							"down_image" : "d:/ymir work/ui/offline_shop/button_example_232.png",
						},
					),
				},
				{
					"name" : "Header",
					"type" : "image",
					"x": 17, "y": 216,
					"image" : "d:/ymir work/ui/offline_shop/test_image_020.tga",
					"children" :
					(
						{
							"name" : "HeaderText",
							"type" : "text",
							"x": 5,"y": 0,
							"text" : uiScriptLocale.OFFLINE_SHOP_CTIME,
							"outline" : "1",
						},
					),
				},
                {
                    "name" : "ThinBoard4",
                    "type" : "thinboard_new",
                    "x": 8, "y": 240,
                    "width":274,"height":50,
                    "children" :
                    (
						{
							"name" : "ShopInfo",
							"type" : "image",
							"x" : 10,"y" : 15,
							"image" : "d:/ymir work/ui/offline_shop/button-example-experiment.png",
                            "children" :
                            (
								{
									"name" : "ShopTimer",
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
			),
		},
	),
}