# -*- coding: iso-8859-1 -*-
import uiScriptLocale
import emoji

window = {
	"name" : "DragonSoulRefineWindow",

	"x" : SCREEN_WIDTH/2.6,
	"y" : SCREEN_HEIGHT/2-250,

	"style" : ("movable", "float",),

	"width" : 287,
	"height" : 232,

	"children" :
	(
		{
			"name" : "board",
			"type" : "board",
			"style" : ("attach",),

			"x" : 0,
			"y" : 0,

			"width" : 287,
			"height" : 232,

			"children" :
			(
				{
					"name" : "DragonSoulRefineWindowBaseImage",
					"type" : "expanded_image",
					"x" : 0,
					"y" : 0,

					"image" : "d:/ymir work/ui/dragonsoul/dragon_soul_refine_bg.tga",
				},

				{
					"name" : "TitleBar",
					"type" : "titlebar",
					"style" : ("attach",),

					"x" : 5,
					"y" : 7,

					"width" : 275,
					"color" : "yellow",

					"children" :
					(
						{ 
							"name":"TitleName", 
							"type":"text", 
							"x":140, 
							"y":5, 
							"text":uiScriptLocale.DRAGONSOUL_REFINE_WINDOW_TITLE, 
                            "outline":"1",
							"text_horizontal_align":"center" 
						},
					),
				},
				
				{
					"name" : "DoRefineWithEnter",
					"type" : "toggle_button",
					"x" : 13,
					"y" : 11,
					"default_image" : "d:/ymir work/ui/game/buttons/hehe.png",
					"over_image" : "d:/ymir work/ui/game/buttons/hehe1.png",
					"down_image" : "d:/ymir work/ui/game/buttons/hehe2.png",

					"tooltip_text_new" : uiScriptLocale.DRAGON_SOUL_REFINE_WITH_BUTTON.format(emoji.AppendEmoji("icon/emoji/key_enter.png")),

					"tooltip_text_color" : 0xfff1e6c0,
					"tooltip_x" : 0,
					"tooltip_y" : -30,
				},

				{
					"name" : "RefineSlot",
					"type" : "grid_table",

					"image" : "d:/ymir work/ui/dragonsoul/cap.tga", 

					"x" : 15,
					"y" : 39,

					"start_index" : 0,
					"x_count" : 5,
					"y_count" : 3,
					"x_step" : 32,
					"y_step" : 32,
				},

				{
					"name" : "ResultSlot",
					"type" : "grid_table",

					"x" : 207,
					"y" : 39,

					"start_index" : 0,
					"x_count" : 2,
					"y_count" : 3,
					"x_step" : 32,
					"y_step" : 32,
				},
				
				{
					"name" : "GradeButton",
					"type" : "toggle_button",

					"x" : 36,
					"y" : 148,

					"default_image" : "d:/ymir work/ui/dragonsoul/button_01.tga",
					"over_image" : "d:/ymir work/ui/dragonsoul/button_02.tga",
					"down_image" : "d:/ymir work/ui/dragonsoul/button_03.tga",

					"children" :
					(
						{
							"name" : "GradeSlotTitle",
							"type" : "text",
							"x" : 0,
							"y" : 0,
							"all_align" : "center",
							"text" : uiScriptLocale.GRADE_SELECT,
							"color" : 0xFFF1E6C0,
						},
					),
				},

				{
					"name" : "StepButton",
					"type" : "toggle_button",

					"x" : 118,
					"y" : 148,

					"default_image" : "d:/ymir work/ui/dragonsoul/button_01.tga",
					"over_image" : "d:/ymir work/ui/dragonsoul/button_02.tga",
					"down_image" : "d:/ymir work/ui/dragonsoul/button_03.tga",

					"children" :
					(
						{
							"name" : "StepSlotTitle",
							"type" : "text",
							"x" : 0,
							"y" : 0,
							"all_align" : "center",
							"text" : uiScriptLocale.STEP_SELECT,
							"color" : 0xFFF1E6C0,
						},
					),
				},

				{
					"name" : "StrengthButton",
					"type" : "toggle_button",

					"x" : 198,
					"y" : 148,

					"default_image" : "d:/ymir work/ui/dragonsoul/button_01.tga",
					"over_image" : "d:/ymir work/ui/dragonsoul/button_02.tga",
					"down_image" : "d:/ymir work/ui/dragonsoul/button_03.tga",

					"children" :
					(
						{
							"name" : "RefineSlotTitle",
							"type" : "text",
							"x" : 0,
							"y" : 0,
							"all_align" : "center",
							"text" : uiScriptLocale.STRENGTH_SELECT,
							"color" : 0xFFF1E6C0,
						},
					),
				},

				{
					"name":"Money_Slot",
					"type" : "text",

					"x":18,
					"y":178,

					"horizontal_align" : "right",
					"text_horizontal_align" : "right",

					"text" : "123456789",
				},
				{
					"name" : "DoFastRefineButton",
					"type" : "button",

					"x" : 188-90,
					"y" : 200,

					"default_image" : "d:/ymir work/ui/dragonsoul/l_button01.tga",
					"over_image" : "d:/ymir work/ui/dragonsoul/l_button02.tga",
					"down_image" : "d:/ymir work/ui/dragonsoul/l_button03.tga",

					"children" :
					(
						{
							"name" : "DoFastRefineButtonTitle", 
							"type" : "text", 
							"x" : 0, 
							"y" : 0, 
							"text" : uiScriptLocale.DO_ALL_REFINE, 
							"all_align" : "center",
						},
					),
				},

                { 
                    "name" : "Percent_Text", 
                    "type" : "text", 
                    "x" : 13, 
                    "y" : 202, 
                    "text" : "", 
                    "outline":1,
                },

				{
					"name" : "DoRefineButton",
					"type" : "button",

					"x" : 188,
					"y" : 200,

					"default_image" : "d:/ymir work/ui/dragonsoul/l_button01.tga",
					"over_image" : "d:/ymir work/ui/dragonsoul/l_button02.tga",
					"down_image" : "d:/ymir work/ui/dragonsoul/l_button03.tga",

					"children" :
					(
						{ 
							"name" : "DoRefineButtonTitle", 
							"type" : "text", 
							"x" : 0, 
							"y" : 0, 
							"text" : uiScriptLocale.DO_REFINE, 
							"all_align" : "center",
						},
					),
				},
			),
		},
	),
}
