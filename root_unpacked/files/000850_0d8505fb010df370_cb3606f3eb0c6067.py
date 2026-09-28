#-*- coding: iso-8859-1 -*-
import uiScriptLocale
import emoji
import item

COSTUME_START_INDEX = item.COSTUME_SLOT_START
WINDOW_HEIGHT = 365

window = {
	"name" : "Acce_CombineWindow",
	"x" : 0,
	"y" : 0,
	"style" : ("movable", "float",),
	"width" : 215,
	"height" : WINDOW_HEIGHT,
	"children" :
	(
		{
			"name" : "board",
			"type" : "board",
			"style" : ("attach",),

			"x" : 0,
			"y" : 0,

			"width" : 215,
			"height" : WINDOW_HEIGHT,

			"children" :
			(
				{
					"name" : "TitleBar",
					"type" : "titlebar",
					"style" : ("attach",),

					"x" : 6,
					"y" : 6,

					"width" : 200,
					"color" : "yellow",

					"children" :
					(
						{ "name":"TitleName", "type":"text", "x":99, "y":0, "text":uiScriptLocale.ACCE_COMBINE, "outline":1, "text_horizontal_align":"center" },
					),
				},

				{
					"name" : "Acce_Combine",
					"type" : "image",

					"x" : 9,
					"y" : 35,

					"image" : uiScriptLocale.LOCALE_UISCRIPT_PATH + "acce/acce_combine.tga",

					"children" :
					(
						{
							"name" : "AcceSlot",
							"type" : "slot",

							"x" : 3,
							"y" : 3,

							"width" : 200,
							"height" : 150,

							"slot" : (
								{"index":0, "x":78, "y":7, "width":32, "height":32},
								{"index":1, "x":78, "y":60, "width":32, "height":32},
								{"index":2, "x":78, "y":115, "width":32, "height":32},
							),
						},
						{
							"name" : "Main", "type" : "text", "text" : uiScriptLocale.ACCE_MAIN, 
							"text_horizontal_align":"center", 
							"fontname":"Tahoma:12", 
							"outline":1,
							"x" : 85+12, "y" : 7+36,
						},
						{
							"name" : "serve", "type" : "text", "text" : uiScriptLocale.ACCE_SERVE, 
							"text_horizontal_align":"center", 
							"fontname":"Tahoma:12", 
							"outline":1,
							"x" : 85+12, "y" : 60+38,
						},
						{
							"name" : "Result", "type" : "text", "text" : uiScriptLocale.ACCE_RESULT, 
							"text_horizontal_align":"center", 
							"fontname":"Tahoma:12", 
							"outline":1,
							"x" : 85+12, "y" : 115+40
						},

					),
				},
				{
					"name" : "item_board",
					"type" : "thinboard_circle",
					"x": 9, "y": 216,
					"width" : 195, "height" : 72,
					"children":
					(
						{
							"name" : "AcceBg",
							"type" : "image",
							"x": 0, "y":20,
							"image" : "d:/ymir work/ui/acce_bg.png",
						},
						{
							"name" : "ItemHeader",
							"type" : "image",
							"x": 0, "y": 0,
							"image" : "d:/ymir work/ui/acce_header.png",
							"children":
							(
								{
									"name" : "item_text_window",
									"type" : "window",
									"x": 0, "y": 0,
									"width" : 195, "height" : 18,
									"children":
									(
										{
											"name" : "Item_text",
											"type" : "text",
											"text" : uiScriptLocale.ACCE_COMBINE_NEEDED_ITEMS,
											"outline" : 1,
											"fontname" : "Tahoma:14",
											"x" : 0, "y" : 0,
											"all_align" : "center",
										},
									),
								},
							),
						},
						{
							"name" : "RequiredItems",
							"type" : "slot",

							"x" : 0,
							"y" : 0,

							"width" : 200,
							"height" : 150,

							"slot" : (
								{"index":0, "x":50, "y":30, "width":32, "height":32},
								{"index":1, "x":110, "y":30, "width":32, "height":32},
							),
						},
					),
				},
				{
					"name" : "Chance",
					"type" : "text",
					"text" : "",
					"text_horizontal_align" : "center",
					"x" : 105,
					"y" : WINDOW_HEIGHT-72,
				},
				{
					"name" : "NeedMoney",
					"type" : "text",
					"text" : "",
					"text_horizontal_align" : "center",
					"x" : 105,
					"y" : WINDOW_HEIGHT-53,
				},
				{
					"name" : "AcceptButton",
					"type" : "button",

					"x" : 32,
					"y" : WINDOW_HEIGHT-30,

					"default_image" : "d:/ymir work/ui/button_example_040.png",
					"over_image" : "d:/ymir work/ui/button_example_041.png",
					"down_image" : "d:/ymir work/ui/button_example_042.png",
				},
				{
					"name" : "CancelButton",
					"type" : "button",

					"x" : 116,
					"y" : WINDOW_HEIGHT-30,

					"default_image" : "d:/ymir work/ui/button_example_050.png",
					"over_image" : "d:/ymir work/ui/button_example_051.png",
					"down_image" : "d:/ymir work/ui/button_example_052.png",
				},
				{
					"name" : "DoRefineWithEnter",
					"type" : "toggle_button",
					"x" : 13,
					"y" : 9,
					"default_image" : "d:/ymir work/ui/game/buttons/hehe.png",
					"over_image" : "d:/ymir work/ui/game/buttons/hehe1.png",
					"down_image" : "d:/ymir work/ui/game/buttons/hehe2.png",

					"tooltip_text_new" :  uiScriptLocale.SASH_COMBINATION_SHORTCUT + emoji.AppendEmoji("icon/emoji/key_enter.png"),
					"tooltip_text_color" : 0xfff1e6c0,
					"tooltip_x" : 0,
					"tooltip_y" : -30,
				},
			),
		},
	),
}

