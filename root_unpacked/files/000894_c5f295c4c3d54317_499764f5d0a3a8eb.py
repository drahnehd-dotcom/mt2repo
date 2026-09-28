import uiScriptLocale

SIZE_X = 614
SIZE_Y = 418

WIDTH = (SCREEN_WIDTH / 2) - (SIZE_X / 2)
HEIGHT = (SCREEN_HEIGHT / 2) - (SIZE_Y / 2)-20
PATH = "d:/ymir work/ui/game/event_calendar/"
PATH1 = "d:/ymir work/ui/battle_pass/"

window = {
	"name" : "EventCalendarDialog",
	"style" : ("movable", "float",),
	"x" : WIDTH,
	"y" : HEIGHT,	
	"width" : SIZE_X,
	"height" : SIZE_Y,
	"children" :
	(
		{
			"name" : "mainWindow",
			"type" : "window",
			"style" : ("attach",),
			"x" : 0,"y" : 0,
			"width" : SIZE_X,
			"height" : SIZE_Y,
			"children" :
			(
				{
					"name" : "background",
					"type" : "image",
					"style": ("attach",),
					"x" : 5,
					"y" : 30,
					"image" : PATH + "bg.png",
					"children" :
                    (
						{
							"name":"board",
							"type":"image",
							"x":0,"y":45,
							"vertical_align":"center",
							"horizontal_align":"center",
							"image":PATH+"board.png",
						},
						{
							"name":"logo",
							"type":"image",
							"x":-20,"y":0,
							"image":PATH+"logo.png",
						},
                    ),
                },
                {
                    "name":"slot",
                    "type":"image",
                    "x":240,"y":90,
                    "horizontal_align":"right",
                    "image":PATH+"slot.png",
                    "children":
                    (
                        {
                            "name" : "final_date_text",
                            "type" : "text",
                            "x" : 0, "y" : -2,
                            "text" : "",
                            "fontname":"Tahoma:16",
                            "all_align":"center",
                            "outline":1,
                        },
                    ),
                },
				{
					"name" : "ExitButton",
					"type" : "button",
					"x" : 570, "y" : 60,
					"default_image" : PATH1+"exit0.png",
					"over_image" : PATH1+"exit1.png",
					"down_image" : PATH1+"exit2.png",
				},
			),
		},
	),
}