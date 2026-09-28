import uiScriptLocale
import item
import app
import localeInfo

LOCALE_PATH = "d:/ymir work/ui/privatesearch/"
GOLD_COLOR	= 0xFFFEE3AE
GREY_COLOR	= 0xFFA0A0A0

BOARD_WIDTH = 730

if app.ENABLE_CHEQUE_SYSTEM :
	window = {
		"name" : "PrivateShopSaleHistoryDialog",

		"x" : 0,
		"y" : 0,

		"style" : ("movable", "float",),

		"width" : BOARD_WIDTH,
		"height" : 410,

		"children" :
		(
			{
				"name" : "board",
				"type" : "board_with_titlebar",

				"x" : 0,
				"y" : 0,

				"width" : BOARD_WIDTH,
				"height" : 410,
				
				"title" : uiScriptLocale.PRIVATESHOPSEARCH_SEARCH_BAR,
			},
		),
	}
else :
	window = {
		"name" : "PrivateShopSaleHistoryDialog",

		"x" : 0,
		"y" : 0,

		"style" : ("movable", "float",),

		"width" : BOARD_WIDTH,
		"height" : 410,

		"children" :
		(
			{
				"name" : "board",
				"type" : "board_with_titlebar",

				"x" : 0,
				"y" : 0,

				"width" : BOARD_WIDTH,
				"height" : 410,
				
				"title" : uiScriptLocale.PRIVATESHOPSEARCH_SEARCH_BAR,
			},
		),
	}
