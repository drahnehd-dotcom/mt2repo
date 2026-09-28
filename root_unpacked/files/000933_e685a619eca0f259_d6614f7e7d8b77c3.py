# -*- coding: utf-8 -*-
# MaintenanceWindow — countdown widget pokazany każdemu graczowi.
# Tytuł ustawiany dynamicznie z localeInfo w MaintenanceWindow.LoadWindow().

import uiScriptLocale

window = {
	"name" : "MaintenanceWindow",
	"style" : ("movable", "float",),

	"x" : SCREEN_WIDTH / 2 - 320 / 2,
	"y" : 60,

	"width" : 320,
	"height" : 100,

	"children" :
	(
		{
			"name" : "Thinboard",
			"type" : "thinboard",

			"x" : 0,
			"y" : 0,
			"width" : 320,
			"height" : 100,

			"children" :
			(
				{
					"name" : "maintitle",
					"type" : "text",

					"x" : 0,
					"y" : 14,

					"color" : 0xfff8d090,

					"text" : uiScriptLocale.MAINTENANCE_TITLE,

					"horizontal_align" : "center",
					"text_horizontal_align" : "center",
					"text_vertical_align" : "center",
				},
				{
					"name" : "message1",
					"type" : "text",

					"x" : 0,
					"y" : 40,

					"text" : "",

					"horizontal_align" : "center",
					"text_horizontal_align" : "center",
					"text_vertical_align" : "center",
				},
				{
					"name" : "message2",
					"type" : "text",

					"x" : 0,
					"y" : 65,

					"text" : "",

					"horizontal_align" : "center",
					"text_horizontal_align" : "center",
					"text_vertical_align" : "center",
				},
			),
		},
	),
}
