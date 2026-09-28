import uiScriptLocale
import localeInfo

BOARD_WIDTH = 697
BOARD_HEIGHT = 287

window = {
	"name" : "OfflineShopLogsWindow",
	"style" : ("movable", "float", ),
	"x" : 0,"y" : 0,
	"width" : BOARD_WIDTH,"height" : BOARD_HEIGHT+50,
	"children" :
	(
		{
			"name" : "board_logs",
			"type" : "board",
			"x": 0, "y": 260,
			"horizontal_align":"center",
			"width": 130,"height": 30,
			"children" :
			(
				{
					"name":"PageSlotbar", "type":"image",
					"x": 0, "y": 28,
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
							"text":"I",
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
			"name" : "Board",
			"type" : "board_with_titlebar",
			"style" : ("attach", ),
			"x" : 0,"y" : 0,
			"width" : BOARD_WIDTH,"height" : BOARD_HEIGHT,
			"title" : uiScriptLocale.OFFLINE_SHOP_HISTORY,
			"children" :
			(
                {
					"name" : "thinboard",
                    "type" : "thinboard_circle",
                    "x":0,"y":35,
                    "horizontal_align":"center",
                    # "vertical_align":"center",
                    "width":BOARD_WIDTH-25,"height":BOARD_HEIGHT-55,
                    "children":
                    (
						{
							"name" : "box",
							"type" : "image",
							"x" : 0, "y" : 22,
							"image" : "d:/ymir work/ui/offline_shop/box.png",
						},
                        {
							"name" : "page0_window",
                            "type" : "window",
                            "x" : 0, "y" : 0,
                            "width": 671, "height":242,
                            "children":
                            (
                                {
									"name" : "table0_window",
									"type" : "window",
									"x" : 0, "y":22,
									"width" : 671, "height": 22,
								},
                                {
									"name" : "table1_window",
									"type" : "window",
									"x" : 0, "y":44,
									"width" : 671, "height": 22,
								},
                                {
									"name" : "table2_window",
									"type" : "window",
									"x" : 0, "y":66,
									"width" : 671, "height": 22,
								},
                                {
									"name" : "table3_window",
									"type" : "window",
									"x" : 0, "y":88,
									"width" : 671, "height": 22,
								},
                                {
									"name" : "table4_window",
									"type" : "window",
									"x" : 0, "y":110,
									"width" : 671, "height": 22,
								},
                                {
									"name" : "table5_window",
									"type" : "window",
									"x" : 0, "y":132,
									"width" : 671, "height": 22,
								},
                                {
									"name" : "table6_window",
									"type" : "window",
									"x" : 0, "y":154,
									"width" : 671, "height": 22,
								},
                                {
									"name" : "table7_window",
									"type" : "window",
									"x" : 0, "y":176,
									"width" : 671, "height": 22,
								},
                                {
									"name" : "table8_window",
									"type" : "window",
									"x" : 0, "y":198,
									"width" : 671, "height": 22,
								},
                                {
									"name" : "table9_window",
									"type" : "window",
									"x" : 0, "y":220,
									"width" : 671, "height": 22,
								},
							),
						},
                        {
							"name" : "page1_window",
                            "type" : "window",
                            "x" : 0, "y" : 0,
                            "width": 671, "height":242,
                            "children":
                            (
                                {
									"name" : "table10_window",
									"type" : "window",
									"x" : 0, "y":22,
									"width" : 671, "height": 22,
								},
                                {
									"name" : "table11_window",
									"type" : "window",
									"x" : 0, "y":44,
									"width" : 671, "height": 22,
								},
                                {
									"name" : "table12_window",
									"type" : "window",
									"x" : 0, "y":66,
									"width" : 671, "height": 22,
								},
                                {
									"name" : "table13_window",
									"type" : "window",
									"x" : 0, "y":88,
									"width" : 671, "height": 22,
								},
                                {
									"name" : "table14_window",
									"type" : "window",
									"x" : 0, "y":110,
									"width" : 671, "height": 22,
								},
                                {
									"name" : "table15_window",
									"type" : "window",
									"x" : 0, "y":132,
									"width" : 671, "height": 22,
								},
                                {
									"name" : "table16_window",
									"type" : "window",
									"x" : 0, "y":154,
									"width" : 671, "height": 22,
								},
                                {
									"name" : "table17_window",
									"type" : "window",
									"x" : 0, "y":176,
									"width" : 671, "height": 22,
								},
                                {
									"name" : "table18_window",
									"type" : "window",
									"x" : 0, "y":198,
									"width" : 671, "height": 22,
								},
                                {
									"name" : "table19_window",
									"type" : "window",
									"x" : 0, "y":220,
									"width" : 671, "height": 22,
								},
							),
						},
						{
                        	"name" : "header",
                            "type" : "image",
                            "x":0,"y":0,
                            "image":"d:/ymir work/ui/biolog_gui/header_big.png",
                            "children":
                            (
								{
									"name":"header_text",
                                    "type":"text",
                                    "x":0,"y":0,
                                    "all_align":"center",
                                    "text": uiScriptLocale.OFFLINE_SHOP_LOG_ITEM_NAME,
                                    "outline":"1",
								},
							),
						},
						{
                        	"name" : "header",
                            "type" : "image",
                            "x":173,"y":0,
                            "image":"d:/ymir work/ui/biolog_gui/header_smaller.png",
                            "children":
                            (
								{
									"name":"header_text",
                                    "type":"text",
                                    "x":0,"y":0,
                                    "all_align":"center",
                                    "text": uiScriptLocale.OFFLINE_SHOP_LOG_ITEM_COUNT,
                                    "outline":"1",
								},
							),
						},
						{
                        	"name" : "header",
                            "type" : "image",
                            "x":238,"y":0,
                            "image":"d:/ymir work/ui/biolog_gui/header_big.png",
                            "children":
                            (
								{
									"name":"header_text",
                                    "type":"text",
                                    "x":0,"y":0,
                                    "all_align":"center",
                                    "text":"Cena",
                                    "outline":"1",
								},
							),
						},
						{
                        	"name" : "header",
                            "type" : "image",
                            "x":410,"y":0,
                            "image":"d:/ymir work/ui/biolog_gui/header_small.png",
                            "children":
                            (
								{
									"name":"header_text",
                                    "type":"text",
                                    "x":0,"y":0,
                                    "all_align":"center",
                                    "text":"Data",
                                    "outline":"1",
								},
							),
						},
						{
                        	"name" : "header",
                            "type" : "image",
                            "x":541,"y":0,
                            "image":"d:/ymir work/ui/biolog_gui/header_small.png",
                            "children":
                            (
								{
									"name":"header_text",
                                    "type":"text",
                                    "x":0,"y":0,
                                    "all_align":"center",
                                    "text": uiScriptLocale.OFFLINE_SHOP_LOG_CATEGORY,
                                    "outline":"1",
								},
							),
						},
					),
				},
			),
		},
	),
}