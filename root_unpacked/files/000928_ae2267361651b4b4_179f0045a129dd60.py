import uiScriptLocale
window = {
	"name" : "MusicListWindow",

	"x" : (SCREEN_WIDTH - 360) / 2,
	"y" : (SCREEN_HEIGHT - 410) / 2,

	"style" : ("movable", "float",),

	"width" : 360,
	"height" : 410,

	"children" :
	(

		{
			"name" : "board",
			"type" : "board_with_titlebar",

			"x" : 0,
			"y" : 0,

			"width" : 360,
			"height" : 410,
			"title" : uiScriptLocale.MUSICLIST_TITLE,

			"children" : (
				{
					"name" : "bar",
					"type" : "bar",

					"x" : 20,
					"y" : 35,

					"width" : 300,
					"height" : 360,

					"color" : 0x70000000,
				},
				{
					"name" : "scroll_bar",
					"type" : "scrollbar",

					"x" : 325,
					"y" : 40,
					"size" : 360,
				},
				{
					"name" : "list_box_ex",
					"type" : "listboxex",

					"x" : 20,
					"y" : 35,

					"width" : 280,
					"height" : 360,

					"viewcount" : 18,
				},
				{
					"name": "item_name_slot",
					"type": "thinboard_circle",

					"x": 20,
					"y" : 35 + 360 - 16,

					"width" : 300,
					"height" : 16,

					"children" : (
						{
							"name": "item_name_value",
							"type": "editline",

							"x": 5,
							"y": 0,

							"width": 64,
							"height": 16,

							"input_limit": 24,

							"text": ""
						},

					),
				},
			),
		},
	)
}
