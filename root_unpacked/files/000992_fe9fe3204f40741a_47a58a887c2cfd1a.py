import localeInfo

WIDTH = 400
HEIGHT = 550

window = {
	"name" : "SwitchbotWindow",
	"x" : 0,
	"y" : 0,
	"style" : ("movable", "float",),

	"x" : (SCREEN_WIDTH/2) - (WIDTH/2),
	"y" : (SCREEN_HEIGHT/2) - (HEIGHT/2),

	"width" : WIDTH,
	"height" : HEIGHT,
	"children" :
	(
		{
			"name" : "board",
			"type" : "board_with_titlebar",
			"style" : ("attach",),
			"x" : 0,
			"y" : 0,
			"width" : WIDTH,
			"height" : HEIGHT,
			"title" : localeInfo.SWITCHBOT_TITLE,
		},
	),
}
