import uiScriptLocale

PATH = "d:/ymir work/ui/bonus_window/"

WIDTH = 310
HEIGHT = 420

window = {
	"name" : "BonusWindow",
	"style" : ("movable", "float",),
	"x" : 24,"y" : (SCREEN_HEIGHT - 37 - 420) / 2,
	"width" : WIDTH,
	"height" : HEIGHT+50,
	"children" :
	(
		{
			"name" : "Board",
			"type" : "board",
			"x" : 0, "y" : 0,
			"width" : WIDTH,
			"height" : HEIGHT,
			"children" :
			(
				{
					"name" : "Bonus_Page",
					"type" : "window",
					"style" : ("attach",),
					"x" : 0,"y" : 0,
					"width" : WIDTH,
					"height" : HEIGHT,
					"children" :
					(
						{
							"name" : "BonusPvP_Page",
							"type" : "window",
							"style" : ("attach",),
							"x" : 0, "y" : 0,
							"width" : WIDTH,
							"height" : HEIGHT,
							"children" :
							(
								{
									"name" : "TitleBar", "type" : "titlebar", "style" : ("attach",), "x" : 8, "y" : 7, "width" : WIDTH-15, "color" : "red",
									"children" :
									(
										{ "name" : "TitleName", "type":"text", "x":0, "y":-3, "text":uiScriptLocale.BONUS_TITLE, "all_align":"center","outline":"1" },
									),
								},
								{
									"name" : "border",
									"type" : "border_a",
									"x" : 12, "y" : 32,
									"width" : WIDTH-42, "height" : HEIGHT-80,
								},
							),
						},
					),
				},
			),
		},
		{
			"name" : "border2",
			"type" : "border_a",
			"x" : 12, "y" : HEIGHT-45,
			"width" : WIDTH-42, "height" : 30,
			"children":
			(
				{
					"name" : "search_icon",
					"type" : "image",
					"x" : 6, "y" : 8,
					"image" : PATH+"search_icon.png",
				},
				{
					"name" : "InputSlot",
					"type" : "slotbar",
					"x" : 8, "y" : 0,
					"width" : 230, "height" : 18,
					"horizontal_align" : "center",
					"vertical_align" : "center",
					"children" :
					(
						{
							"name" : "InputValue",
							"type" : "editline",
							"x" : 3, "y" : 3,
							"width" : 230, "height" : 18,
							"input_limit" : 12,
						},
					),
				},
			),
		},
	),
}