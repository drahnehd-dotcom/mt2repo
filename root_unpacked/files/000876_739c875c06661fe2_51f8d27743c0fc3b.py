import uiScriptLocale
import item
import app

COSTUME_START_INDEX = item.COSTUME_SLOT_START

window = {
	"name" : "CostumeWindow",

	"x" : SCREEN_WIDTH - 175 - 140,
	"y" : SCREEN_HEIGHT - 37 - 565,

	"style" : ("movable", "float",),

	"width" : 140,
	"height" : (210 + 47),

	"children" :
	(
		{
			"name" : "board",
			"type" : "board",
			"style" : ("attach",),

			"x" : 0,
			"y" : 0,

			"width" : 140,
			"height" : (210 + 47),

			"children" :
			(
				{
					"name" : "TitleBar",
					"type" : "titlebar",
					"style" : ("attach",),

					"x" : 6,
					"y" : 6,

					"width" : 130,
					"color" : "yellow",

					"children" :
					(
						{ "name":"TitleName", "type":"text", "x":60, "y":0, "text":uiScriptLocale.COSTUME_WINDOW_TITLE, "outline":"1","text_horizontal_align":"center" },
					),
				},

				{
					"name" : "Costume_Base",
					"type" : "image",

					"x" : 13,
					"y" : 38,

					"image" : uiScriptLocale.LOCALE_UISCRIPT_PATH + "costume/new_costume_bg.jpg",

					"children" :
					(

						{
							"name" : "CostumeSlot",
							"type" : "slot",

							"x" : 3,
							"y" : 3,

							"width" : 127,
							"height" : 200,

							"slot" : (
										{"index":COSTUME_START_INDEX+0, "x":62, "y":45, "width":32, "height":64},
										{"index":COSTUME_START_INDEX+1, "x":62, "y": 9, "width":32, "height":32},
										{"index":COSTUME_START_INDEX+3, "x":71, "y":126, "width":32, "height":32},
										{"index":COSTUME_START_INDEX+4, "x":40, "y":126, "width":32, "height":32},
										{"index":COSTUME_START_INDEX+5, "x":13, "y":13, "width":32, "height":96},
										{"index":COSTUME_START_INDEX+6, "x":38, "y":158, "width":32, "height":32},
										{"index":COSTUME_START_INDEX+7, "x":5, "y":126, "width":32, "height":32},
									),
						},
						{
							"name" : "BodyToolTipButton",
							"type" : "toggle_button",

							"x" : 62 + 32 - 10,
							"y" : 45 - 5,


							"default_image" : "d:/ymir work/ui/pattern/visible_mark_01.tga",
							"over_image" : "d:/ymir work/ui/pattern/visible_mark_02.tga",
							"down_image" : "d:/ymir work/ui/pattern/visible_mark_03.tga",
						},
						{
							"name" : "HairToolTipButton",
							"type" : "toggle_button",

							"x" : 62 + 32 -6,
							"y" : 9 - 3,


							"default_image" : "d:/ymir work/ui/pattern/visible_mark_01.tga",
							"over_image" : "d:/ymir work/ui/pattern/visible_mark_02.tga",
							"down_image" : "d:/ymir work/ui/pattern/visible_mark_03.tga",
						},
						{
							"name" : "AcceToolTipButton",
							"type" : "toggle_button",

							"x" : 62 + 32,
							"y" : 126,


							"default_image" : "d:/ymir work/ui/pattern/visible_mark_01.tga",
							"over_image" : "d:/ymir work/ui/pattern/visible_mark_02.tga",
							"down_image" : "d:/ymir work/ui/pattern/visible_mark_03.tga",
						},
						{
							"name" : "WeaponToolTipButton",
							"type" : "toggle_button",

							"x" : 13 + 32 - 6,
							"y" : 13,


							"default_image" : "d:/ymir work/ui/pattern/visible_mark_01.tga",
							"over_image" : "d:/ymir work/ui/pattern/visible_mark_02.tga",
							"down_image" : "d:/ymir work/ui/pattern/visible_mark_03.tga",
						},
						{
							"name" : "AuraToolTipButton",
							"type" : "toggle_button",

							"x" : 62,
							"y" : 160,


							"default_image" : "d:/ymir work/ui/pattern/visible_mark_01.tga",
							"over_image" : "d:/ymir work/ui/pattern/visible_mark_02.tga",
							"down_image" : "d:/ymir work/ui/pattern/visible_mark_03.tga",
						},
						{
							"name" : "StoleToolTipButton",
							"type" : "toggle_button",

							"x" : 62,
							"y" : 126,


							"default_image" : "d:/ymir work/ui/pattern/visible_mark_01.tga",
							"over_image" : "d:/ymir work/ui/pattern/visible_mark_02.tga",
							"down_image" : "d:/ymir work/ui/pattern/visible_mark_03.tga",
						},
					),
				},
			),
		},
	),
}