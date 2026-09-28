import uiScriptLocale

window = {
	"name" : "WarpShowerWindow",
	"sytle" : ("float", "ltr",),

	"x" : 0,
	"y" : 0,

	"width" : SCREEN_WIDTH,
	"height" : SCREEN_HEIGHT,

	"children" :
	[
		{
			"name" : "BackgroundBar",
			"type" : "bar",

			"x" : 0,
			"y" : 0,

			"width" : SCREEN_WIDTH,
			"height" : SCREEN_HEIGHT,

			"color" : 0x66000000,

			"children" :
			[
				{
					"name" : "LoadingWindow",
					"type" : "window",

					"x" : 0,
					"y" : 0,

					"width" : 380,
					"height": 380,

					"horizontal_align" : "center",
					"vertical_align" : "center",

					"children" :
					[
						{
							"name" : "LoadingAniImage",
							"type" : "ani_image",

							"x" : 0,
							"y" : 0,

							"delay" : 1,

							"images" :
							(
								"d:/ymir work/kowal/loginwindow/logo.png",
							)
						},
					],
				},
			],
		}
	],
}
