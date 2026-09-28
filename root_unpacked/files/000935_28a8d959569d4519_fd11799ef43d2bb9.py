import uiScriptLocale

window = {
	"name" : "MallPageDialog",
	"style" : ("movable", "float",),

	"x" : 0,
	"y" : 0,

	"width" : 620,
	"height" : 520,

	"children" :
	(
		{
			"name" : "board",
			"type" : "board",

			"x" : 0,
			"y" : 0,

			"width" : 620,
			"height" : 520,

			"children" :
			(
				{
					"name" : "titlebar",
					"type" : "titlebar",
					"style" : ("attach",),

					"x" : 8,
					"y" : 8,
					"width" : 604,
					"color" : "gray",

					"children" :
					(
						{
							"name" : "title_name",
							"type" : "text",
							"x" : 0,
							"y" : 3,
							"horizontal_align" : "center",
							"text_horizontal_align" : "center",
							"text" : uiScriptLocale.MALL_TITLE,
						},
					),
				},
			),
		},
	),
}
