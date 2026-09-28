#-*- coding: iso-8859-1 -*-
import uiScriptLocale

WINDOW_X = 223
WINDOW_Y = 329

window = {
	"name" : "ChangerWindow",

	"x" : 0,
	"y" : 0,

	"style" : ("movable", "float"),

	"width" : WINDOW_X,
	"height" : WINDOW_Y,

	"children" :
	(
		{
			"name" : "board",
			"type" : "board",
			"style" : ("attach",),

			"x" : 0,
			"y" : 0,

			"width" :WINDOW_X,
			"height" : WINDOW_Y,

			"children" :
			(
				{
					"name" : "TitleBar",
					"type" : "titlebar",
					"style" : ("attach",),

					"x" : 8,
					"y" : 7,

					"width" : WINDOW_X-15,
					"color" : "yellow",

					"children" :
					(
						{ "name":"TitleName", "type":"text", "x":0, "y":0, "text": uiScriptLocale.BONUS_CHANGER, "text_horizontal_align":"center", "horizontal_align" : "center", "outline":"1", },
					),
				},
				
				{
					"name" : "image",
					"type" : "image",
					"x" : 40,
					"y" : 299,
					"image":"icon\\emoji\\key_enter.png",
				},
                {
                    "name":"vasto",
                    "type":"text",
                    "x":90,
                    "y":299,
                    "text": uiScriptLocale.BONUS_CHANGER_CHANGE,
					"fontname" : "Tahoma:14",
					"outline" : 1,
				},

				{
					"name": "background",
					"type": "image",
					"x":6,
					"y":28,
					
					"image": "d:/ymir work/changer/changer_background.tga",
					
					"children":
					(
						{
							"name": "ItemsTitleBar",
							"type": "window",
							"x": 0,
							"y": 0,
							"width": 217,
							"height": 22,
						},
						
						{
							"name": "BonusTitleBar",
							"type": "window",
							"x": 0,
							"y": 120,
							"width": 217,
							"height": 22,
						},
						
						{
							"name": "BonusInformation1",
							"type": "window",
							"x": 4,
							"y": 166,
							"width": 205,
							"height": 9,
							
							"children":
							(
								{
									"name": "BonusName1",
									"type": "text",
									"x": 0,
									"y": 0,
                                    "all_align":"center",
									
									"text": "",
                                    "outline":"1",
                                    "color":0xff89b88d,
                                    "fontname":"Tahoma:12",
								},
								
							),
						},
						
						{
							"name": "BonusInformation2",
							"type": "window",
							"x": 4,
							"y": 185,
							"width": 205,
							"height": 9,
							
							"children":
							(
								{
									"name": "BonusName2",
									"type": "text",
									"x": 0,
									"y": 0,
                                    "all_align":"center",
									
									"text": "",
                                    "outline":"1",
                                    "color":0xff89b88d,
                                    "fontname":"Tahoma:12",
								},
							
							),
						},
						
						{
							"name": "BonusInformation3",
							"type": "window",
							"x": 4,
							"y": 205,
							"width": 205,
							"height": 9,
							
							"children":
							(
								{
									"name": "BonusName3",
									"type": "text",
									"x": 0,
									"y": 0,
                                    "all_align":"center",
									
									"text": "",
                                    "outline":"1",
                                    "color":0xff89b88d,
                                    "fontname":"Tahoma:12",
								},
								
							),
						},
						
						{
							"name": "BonusInformation4",
							"type": "window",
							"x": 4,
							"y": 225,
							"width": 205,
							"height": 9,
							
							"children":
							(
								{
									"name": "BonusName4",
									"type": "text",
									"x": 0,
									"y": 0,
                                    "all_align":"center",
									
									"text": "",
                                    "outline":"1",
                                    "color":0xff89b88d,
                                    "fontname":"Tahoma:12",
								},
							
							),
						},
						
						{
							"name": "BonusInformation5",
							"type": "window",
							"x": 4,
							"y": 244,
							"width": 205,
							"height": 9,
							
							"children":
							(
								{
									"name": "BonusName5",
									"type": "text",
									"x": 0,
									"y": 0,
                                    "all_align":"center",
									
									"text": "",
                                    "outline":"1",
                                    "color":0xff89b88d,
                                    "fontname":"Tahoma:12",
								},
							),
						},
						
						{
							"name" : "ItemsSlots",
							"type" : "slot",

							"x" : 0,
							"y" : 0,

							"width" : 190,
							"height" : 180,

							"slot" : (
										{"index":0, "x":39, "y":21, "width":32, "height":96},
										{"index":1, "x":128, "y":42, "width":32, "height":32},
									),
						},
						
						{
							"name": "ChangeButton",
							"type": "button",
							
							"x": 98,
							"y": 90,
							
							"default_image" : "d:/ymir work/ui/marmur_window/buy_btn.png",
							"over_image" : "d:/ymir work/ui/marmur_window/buy_btn1.png",
							"down_image" : "d:/ymir work/ui/marmur_window/buy_btn2.png",
						},
					),
				},
			),
		},
	),
}