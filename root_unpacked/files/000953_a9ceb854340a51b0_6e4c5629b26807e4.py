import uiScriptLocale

window = {
	"name" : "PickETCDialog",

	"x" : 100,
	"y" : 100,

	"style" : ("movable", "float",),

	"width" : 200,
	"height" : 90+20+12,

	"children" :
	(
		{
			"name" : "board",
			"type" : "board_with_titlebar",

			"x" : 0,
			"y" : 0,

			"width" : 200,
			"height" : 90+20+12,
			"title" : uiScriptLocale.PICK_MONEY_TITLE,

			"children" :
			(
				{
                    "name":"text",
                    "type":"text",
                    "text": uiScriptLocale.PIECES_OF_ITEM,
                    "x":20,"y":35,
                    "outline":"1",
				},
				{
					"name" : "money_slot",
					"type" : "image",

					"x" : 66,
					"y" : 34,

					"image" : "d:/ymir work/ui/public/Parameter_Slot_02.sub",

					"children" :
					(
						{
							"name" : "money_value",
							"type" : "editline",

							"x" : 3,
							"y" : 2,

							"width" : 60,
							"height" : 18,

							"input_limit" : 6,
							"only_number" : 1,

							"text" : "1",
						},
						{
							"name" : "max_value",
							"type" : "text",

							"x" : 63,
							"y" : 3,

							"text" : "/ 999999",
						},
					),
				},









				{
					"name" : "accept_button",
					"type" : "button",

					"x" : 170/2 - 61 - 5+10,
					"y" : 58+20+8,

					"default_image" : "d:/ymir work/ui/button_example_040.png",
					"over_image" : "d:/ymir work/ui/button_example_041.png",
					"down_image" : "d:/ymir work/ui/button_example_042.png",
				},
				{
					"name" : "cancel_button",
					"type" : "button",

					"x" : 170/2 + 5+22,
					"y" : 58+20+8,

					"default_image" : "d:/ymir work/ui/button_example_050.png",
					"over_image" : "d:/ymir work/ui/button_example_051.png",
					"down_image" : "d:/ymir work/ui/button_example_052.png",
				},
			),
		},
	),
}