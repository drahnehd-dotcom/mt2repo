import uiScriptLocale

# Native Metin2 layout (see m2ui reference/native-geometry.md):
# board_with_titlebar, content from y=35, side inset 12, bottom inset 14,
# 10 rows x 25 px (21 px buttons + 4 px gap).
BOARD_WIDTH = 345
BOARD_HEIGHT = 295

LIST_X = 12
LIST_Y = 35
LIST_WIDTH = BOARD_WIDTH - LIST_X * 2
LIST_HEIGHT = 250

window = {
	"name" : "SavePositionWindow",
	"style" : ("movable", "float",),

	"x" : (SCREEN_WIDTH - BOARD_WIDTH) // 2,
	"y" : (SCREEN_HEIGHT - BOARD_HEIGHT) // 2,

	"width" : BOARD_WIDTH,
	"height" : BOARD_HEIGHT,

	"children" :
	(
		{
			"name" : "board",
			"type" : "board_with_titlebar",

			"x" : 0,
			"y" : 0,

			"width" : BOARD_WIDTH,
			"height" : BOARD_HEIGHT,

			"title" : uiScriptLocale.SAVE_LOCATION_TITLE,

			"children" :
			(
				{
					"name" : "ElementContainer",
					"type" : "listboxex",

					"x" : LIST_X,
					"y" : LIST_Y,

					"width" : LIST_WIDTH,
					"height" : LIST_HEIGHT,
				},
			),
		},
	),
}
