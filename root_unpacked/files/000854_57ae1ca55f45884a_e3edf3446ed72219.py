import uiScriptLocale
import localeInfo

window = {
	"name" : "Aura_AbsorbtionWindow",
	"x" : SCREEN_WIDTH - 176 - 287 - 10,
	"y" : SCREEN_HEIGHT - 37 - 525,
	"style" : ("movable", "float",),
	"width" : 205,
	"height" : 270,
	"children" :
	(
		{
			"name" : "board",
			"type" : "board",
			"style" : ("attach",),
			"x" : 0,
			"y" : 0,
			"width" : 205,
			"height" : 270,
			"children" :
			(
				{
					"name" : "TitleBar",
					"type" : "titlebar",
					"style" : ("attach",),
					"x" : 6,
					"y" : 6,
					"width" : 190,
					"color" : "yellow",
					"children" :
					(
						{
							"name":"TitleName",
							"type":"text",
							"x":95,
							"y":0,
							"text":localeInfo.AURA_TITLE_ABSORB,
                            "outline":1,
							"text_horizontal_align":"center"
						},
					),
				},
				{
					"name" : "Aura_Combine",
					"type" : "image",
					"x" : 9,
					"y" : 35,
					"image" : uiScriptLocale.LOCALE_UISCRIPT_PATH + "Acce/Acce_absorb.tga",
					"children" :
					(
						{
							"name" : "AuraSlot",
							"type" : "slot",
							"x" : 3,
							"y" : 3,
							"width" : 190,
							"height" : 200,
							"slot" : (
										{
											"index" : 0,
											"x" : 26,
											"y" : 41,
											"width" : 31,
											"height" : 31
										},
										{
											"index" : 1,
											"x" : 125,
											"y" : 8,
											"width" : 31,
											"height" : 96
										},
										{
											"index" : 2,
											"x" : 75,
											"y" : 126,
											"width" : 31,
											"height" : 31
										},
							),
						},
					),
				},
				{
					"name" : "AcceptButton",
					"type" : "button",

					"x" : 28,
					"y" : 235,

					"default_image" : "d:/ymir work/ui/button_example_040.png",
					"over_image" : "d:/ymir work/ui/button_example_041.png",
					"down_image" : "d:/ymir work/ui/button_example_042.png",
				},
				{
					"name" : "CancelButton",
					"type" : "button",

					"x" : 114,
					"y" : 235,

					"default_image" : "d:/ymir work/ui/button_example_050.png",
					"over_image" : "d:/ymir work/ui/button_example_051.png",
					"down_image" : "d:/ymir work/ui/button_example_052.png",
				},		
			),
		},
	),
}