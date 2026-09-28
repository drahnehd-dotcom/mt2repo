
window = {
	"name" : "InputDialog",

	"x" : 0,
	"y" : 0,

	"style" : ("movable", "float",),

	"width" : 170,
	"height" : 140,

	"children" :
	(
		{
			"name" : "board",
			"type" : "board_with_titlebar",

			"x" : 0,
			"y" : 0,

			"width" : 170,
			"height" : 140,
			"title" : "",
			"outline" : "1",
            
			"children" :
			(
				{
					"name" : "InputSlot_Cheque",
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
							"name" : "InputValue_Cheque",
							"type" : "editline",

							"x" : 3,
							"y" : 2,

							"width" : 60,
							"height" : 18,

							"input_limit" : 10,
							"only_number" : 1,
                            
							"text" : "0",
						},
					),
				},

				{
					"name" : "InputSlot",
					"type" : "image",

					"x" : 15,
					"y" : 34,

					"image" : "d:/ymir work/ui/public/parameter_slot_04.sub",

					"children" :
					(
						{
							"name" : "InputValue",
							"type" : "editline",

							"x" : 3,
							"y" : 2,

							"width" : 60,
							"height" : 18,

							"input_limit" : 15,
							"only_number" : 1,

							"text" : "1",
						},
						{
							"name" : "money_image",
							"type" : "image",

							"x" : 119,
							"y" : 2,

							"image":"icon/emoji/money_icon.png",
						},
					),
				},

				{
					"name" : "ChequeValue",
					"type" : "text",

					"x" : 0,
					"y" : 89,
					"text" : "999999999",
					"text_horizontal_align" : "center",
					"horizontal_align" : "center",
				},

				{
					"name" : "MoneyValue",
					"type" : "text",

					"x" : 0,
					"y" : 77,
					"text" : "999999999",
					"text_horizontal_align" : "center",
					"horizontal_align" : "center",
				},

				{
					"name" : "AcceptButton",
					"type" : "button",

					"x" : 190/2 - 61 - 5,
					"y" : 105,

					"default_image" : "d:/ymir work/ui/accept0.tga",
					"over_image" : "d:/ymir work/ui/accept1.tga",
					"down_image" : "d:/ymir work/ui/accept2.tga",
				},
				{
					"name" : "CancelButton",
					"type" : "button",

					"x" : 150/2 + 20,
					"y" : 105,

					"default_image" : "d:/ymir work/ui/cancel0.tga",
					"over_image" : "d:/ymir work/ui/cancel1.tga",
					"down_image" : "d:/ymir work/ui/cancel2.tga",
				},
			),
		},
	),
}