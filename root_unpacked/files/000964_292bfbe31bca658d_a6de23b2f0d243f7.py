import uiScriptLocale
import localeInfo

BOARD_WIDTH = 220
BOARD_HEIGHT = 160

window = {
	"name" : "PrivateShopSearchFilterSlot",

	"x" : 0,
	"y" : 0,

	"width" : BOARD_WIDTH,
	"height" : BOARD_HEIGHT,

	"children" :
	(
		{
			"name" : "Background",
			"type" : "imagebox",

			"x" : 0,
			"y" : 0,

			"width" : BOARD_WIDTH,
			"height" : BOARD_HEIGHT,
			
			"title" : uiScriptLocale.PRIVATESHOPSEARCH_FILTER_SELECT_TITLE,
		
			"children" :
			(
				{
							"name" : "FilterScrollBar",
							"type" : "scrollbar",

							"x" : BOARD_WIDTH - 30,
							"y" : 30,

							"size" : 123,
				},
			),
		},
	),
}
