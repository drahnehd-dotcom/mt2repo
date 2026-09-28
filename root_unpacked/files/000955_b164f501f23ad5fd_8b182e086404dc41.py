import uiScriptLocale

window = {
	"name" : "PickMoneyDialog",

	"x" : 150,
	"y" : 150,

	"style" : ("movable", "float",),

	"width" : 170,
	"height" : 112,

	"children" :
	(
		{
			"name" : "board",
			"type" : "board_with_titlebar",

			"x" : 0,
			"y" : 0,

			"width" : 170,
			"height" : 112,
			"title" : uiScriptLocale.PICK_MONEY_TITLE,
			"outline" : "1",

			"children" :
			(
				{
					"name" : "cheque_slot",
					"type" : "image",

					"x" : 15,
					"y" : 55,

					"image" : "d:/ymir work/ui/public/Parameter_Slot_04.sub",

					"children" :
					(

						{
							"name":"Cheque_Icon",
							"type":"image",

							"x":122,
							"y":2,

							"image":"d:/ymir work/ui/game/windows/cheque_icon.sub",
						},
						{
							"name" : "cheque_value",
							"type" : "editline",

							"x" : 3,
							"y" : 2,

							"width" : 60,
							"height" : 18,

							"input_limit" : 6,
							"only_number" : 0,
                            
							"text" : "0",
						},
					),
				},

				{
					"name" : "money_slot",
					"type" : "image",

					"x" : 15,
					"y" : 34,

					"image" : "d:/ymir work/ui/public/parameter_slot_04.sub",

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
							"only_number" : 0,

							"text" : "1",
						},
						{
							"name" : "money_image",
							"type" : "image",

							"x" : 122,
							"y" : 2,

							"image":"d:/ymir work/ui/game/windows/money_icon.sub",
						},
					),
				},

				{
					"name" : "accept_button",
					"type" : "button",

					"x" : 190/2 - 61 - 5,
					"y" : 82,

					"default_image" : "d:/ymir work/ui/accept0.tga",
					"over_image" : "d:/ymir work/ui/accept1.tga",
					"down_image" : "d:/ymir work/ui/accept2.tga",
				},
				{
					"name" : "cancel_button",
					"type" : "button",

					"x" : 150/2 + 20,
					"y" : 82,

					"default_image" : "d:/ymir work/ui/cancel0.tga",
					"over_image" : "d:/ymir work/ui/cancel1.tga",
					"down_image" : "d:/ymir work/ui/cancel2.tga",
				},
			),
		},
	),
}