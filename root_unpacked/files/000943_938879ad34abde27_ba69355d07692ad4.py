#-*- coding: iso-8859-1 -*-
import uiScriptLocale

ROOT = "d:/ymir work/ui/dungeon_minimap/"
GOLD_COLOR	= 0xFFFEE3AE
TEXT_POS_X = 64

window = {
	"name" : "DungeoninfoMiniMap",
	"x" : SCREEN_WIDTH - 140, "y" : -1, "width" : 144, "height" : 144,
	"children" :
	(
		{
			"name" : "ServerInfo",
			"type" : "text",
			"text_horizontal_align" : "center",
			"outline" : 1,
			"x" : TEXT_POS_X,
			"y" : 140+35,
			"text" : "",
		},
		{
			"name": "dayInfo",
			"type": "text",
			"text_horizontal_align": "center",
			"outline": 1,
			"x": TEXT_POS_X,
			"y": 190,
			"text": "",
			"outline": True,
		},
		{
			"name" : "krecha",
			"type" : "text",
			"text_horizontal_align" : "center",
			"outline" : 1,
			"x" : TEXT_POS_X,
			"y" : 198,
			"text" : "______________",
			"color":0xff999999,
		},
		{
			"name" : "PositionInfo",
			"type" : "text",
			"text_horizontal_align" : "center",
			"outline" : 1,
			"x" : TEXT_POS_X,
			"y" : 216,
			"text" : "",
		},
		{
			"name": "fpsInfo",
			"type": "text",
			"text_horizontal_align": "center",
			"outline": 1,
			"x": TEXT_POS_X,
			"y": 232,
			"text": "",
			"outline": True,
		},
		{
			"name" : "krecha",
			"type" : "text",
			"text_horizontal_align" : "center",
			"outline" : 1,
			"x" : TEXT_POS_X,
			"y" : 237,
			"text" : "______________",
			"color":0xff999999,
		},
		{
			"name": "Timer",
			"type": "text",
			"text_horizontal_align": "center",
			"outline": 1,
			"x": TEXT_POS_X,
			"y": 255,
			"text": uiScriptLocale.MINIMAP_DUNGEON_INFO_TIMER,
			"outline": True,
		},
		{
			"name": "Timer_text",
			"type": "text",
			"text_horizontal_align": "center",
			"outline": 1,
			"x": TEXT_POS_X,
			"y": 272,
			"text": "",
			"color":0xfff0e2ec,
			"outline": True,
		},
		{
			"name" : "OpenWindow", "type" : "window", "x" : 0, "y" : 0, "width" : 144, "height" : 144,
			"children" :
			(
				{ "name" : "RotateGaugeBackground", "type" : "image", "x" : 5, "y" : 30, "image" : ROOT + "stage_gauge_background.tga" },
				{ "name" : "RotateGauge", "type" : "expanded_image", "x" : -8, "y" : 10, "horizontal_align" : "center",  "vertical_align" : "center",  "image" : ROOT + "stage_gauge_green.tga" },
				{ "name" : "BaseBoard", "type" : "image", "x" : -11, "y" : 2, "image" : ROOT + "base_board.png", },
				
				{ "name" : "StageText", "type" : "text", "x" : -6, "y" : 60, "horizontal_align" : "center", "text":"1", "text_horizontal_align" : "center", "fontsize":"LARGE",  "color" : GOLD_COLOR },
									
				{ "name" : "SlideTextWindow", "type" : "window", "x" : 18, "y" : 82, "width" : 95, "height" : 18, },
				{ "name" : "SlideTextShadow", "type" : "image", "x" : 16, "y" : 82, "image" : ROOT + "infotext_shadow.tga" },
				
				{ "name" : "CountGauge", "type" : "expanded_image", "x" : 19, "y" : 105, "image" : ROOT + "gauge_normal.tga" },
				{ "name" : "CountText", "type" : "text", "x" : -6, "y" : 104, "horizontal_align" : "center", "text_horizontal_align" : "center", "outline" : 1, "color" : GOLD_COLOR },
				
				{
                    "name" : "PowtorzBackground",
                    "type" : "image",
                    "x" : -11, "y" : 2,
                    "image": ROOT + "base_board_end.png",
                    "children":
                    (
						{ 
							"name" : "PowtorzButton",
							"type" : "button",
							"x" : 0, "y" : 75,
							"horizontal_align":"center",
							"default_image": ROOT + "powtorz_btn0.png",
							"over_image": ROOT + "powtorz_btn1.png",
							"down_image": ROOT + "powtorz_btn2.png",
                            "children":
                            (
                                {
                                    "name":"PowtorzText",
                                    "type":"text",
                                    "x":0,"y":-1,
                                    "text":uiScriptLocale.MINIMAP_DUNGEON_INFO_REPEAT,
                                    "all_align":"center",
                                    "fontname":"Tahoma:12",
                                    "outline":1,
                                    "color":0xffd6cc8a,
                                },
                            ),
						},
					),
				},
			),
		},
	),
}
