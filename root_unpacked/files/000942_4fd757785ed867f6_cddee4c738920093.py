#-*- coding: iso-8859-1 -*-
import emoji
import app

ROOT = "d:/ymir work/ui/minimap/"
NEW_PATH = "d:/ymir work/ui/game/NEW_PATH/"
NEW_PATH = "d:/ymir work/ui/minimap/"

TEXT_POS_X = 60

window = {
	"name" : "MiniMap",

	"x" : SCREEN_WIDTH - 136,
	"y" : 0,

	"width" : 136,
	"height" : 150,

	"children" :
	(
		{
			"name" : "OpenWindow",
			"type" : "window",

			"x" : 0,
			"y" : 0,

			"width" : 136,
			"height" : 150,

			"children" :
			(
				{
					"name" : "OpenWindowBGI",
					"type" : "image",
					"x" : 0,
					"y" : 0,
					"image" : ROOT + "minimap.sub",
				},
				{
					"name" : "MiniMapWindow",
					"type" : "window",

					"x" : 4,
					"y" : 5,

					"width" : 128,
					"height" : 128,
				},
				{
					"name" : "ScaleUpButton",
					"type" : "button",

					"x" : 101,
					"y" : 116,

					"default_image" : ROOT + "minimap_scaleup_default.sub",
					"over_image" : ROOT + "minimap_scaleup_over.sub",
					"down_image" : ROOT + "minimap_scaleup_down.sub",
				},
				{
					"name" : "ScaleDownButton",
					"type" : "button",

					"x" : 115,
					"y" : 103,

					"default_image" : ROOT + "minimap_scaledown_default.sub",
					"over_image" : ROOT + "minimap_scaledown_over.sub",
					"down_image" : ROOT + "minimap_scaledown_down.sub",
				},
				{
					"name" : "MiniMapHideButton",
					"type" : "button",

					"x" : 111,
					"y" : 6,

					"default_image" : ROOT + "minimap_close_default.sub",
					"over_image" : ROOT + "minimap_close_over.sub",
					"down_image" : ROOT + "minimap_close_down.sub",
				},
				{
					"name" : "AtlasShowButton",
					"type" : "button",

					"x" : 12,
					"y" : 12,

					"default_image" : ROOT + "atlas_open_default.sub",
					"over_image" : ROOT + "atlas_open_over.sub",
					"down_image" : ROOT + "atlas_open_down.sub",
				},
				{
					"name" : "Channel1",
					"type" : "radio_button",
					"x" : 1,
					"y" : 31,
					"default_image" : NEW_PATH + "ch1_0.png",
					"over_image" : NEW_PATH + "ch1_1.png",
					"down_image" : NEW_PATH + "ch1_2.png",

					"tooltip_text_new" : emoji.AppendEmoji("icon/emoji/key_alt.png")+"+"+emoji.AppendEmoji("icon/emoji/key_f1.png"),
					"tooltip_text_color" : 0xfff1e6c0,
					"tooltip_x" : 0,
					"tooltip_y" : -40,
				},
				{
					"name" : "Channel2",
					"type" : "radio_button",
					"x" : -3,
					"y" : 50,
					"default_image" : NEW_PATH + "ch2_0.png",
					"over_image" : NEW_PATH + "ch2_1.png",
					"down_image" : NEW_PATH + "ch2_2.png",

					"tooltip_text_new" : emoji.AppendEmoji("icon/emoji/key_alt.png")+"+"+emoji.AppendEmoji("icon/emoji/key_f2.png"),
					"tooltip_text_color" : 0xfff1e6c0,
					"tooltip_x" : 0,
					"tooltip_y" : -40,
				},
				{
					"name" : "Channel3",
					"type" : "radio_button",
					"x" : -1,
					"y" : 69,
					"default_image" : NEW_PATH + "ch3_0.png",
					"over_image" : NEW_PATH + "ch3_1.png",
					"down_image" : NEW_PATH + "ch3_2.png",

					"tooltip_text_new" : emoji.AppendEmoji("icon/emoji/key_alt.png")+"+"+emoji.AppendEmoji("icon/emoji/key_f3.png"),
					"tooltip_text_color" : 0xfff1e6c0,
					"tooltip_x" : 0,
					"tooltip_y" : -40,
				},
				{
					"name" : "Channel4",
					"type" : "radio_button",
					"x" : 4,
					"y" : 88,
					"default_image" : NEW_PATH + "ch4_0.png",
					"over_image" : NEW_PATH + "ch4_1.png",
					"down_image" : NEW_PATH + "ch4_2.png",

					"tooltip_text_new" : emoji.AppendEmoji("icon/emoji/key_alt.png")+"+"+emoji.AppendEmoji("icon/emoji/key_f4.png"),
					"tooltip_text_color" : 0xfff1e6c0,
					"tooltip_x" : 0,
					"tooltip_y" : -40,
				},
				{
					"name" : "Channel5",
					"type" : "radio_button",
					"x" : 16,
					"y" : 104,
					"default_image" : NEW_PATH + "ch5_0.png",
					"over_image" : NEW_PATH + "ch5_1.png",
					"down_image" : NEW_PATH + "ch5_2.png",

					"tooltip_text_new" : emoji.AppendEmoji("icon/emoji/key_alt.png")+"+"+emoji.AppendEmoji("icon/emoji/key_f5.png"),
					"tooltip_text_color" : 0xfff1e6c0,
					"tooltip_x" : 0,
					"tooltip_y" : -40,
				},
				{
					"name" : "bgDown",
					"type" : "window",
					"x" : 3,
					"y" : 155,
					"width" : 130,
					"height" : 45,
					"children" :
					(
						{
							"name" : "ServerInfo",
							"type" : "text",
							"text_horizontal_align" : "center",
							"outline" : 1,
							"x" : 65,
							"y" : 4,
							"text" : "",
						},
						{
							"name" : "dayInfo",
							"type" : "text",
							"text_horizontal_align" : "center",
							"outline" : 1,
							"x" : 65,
							"y" : 17,
							"text" : "",
						},
						{
							"name" : "PositionInfo",
							"type" : "text",
							"text_horizontal_align" : "center",
							"outline" : 1,
							"x" : 65,
							"y" : 30,
							"text" : "",
						},
					),
				},
				{
					"name": "fpsInfo",
					"type": "text",
					"text_horizontal_align": "center",
					"outline": 1,
					"x": TEXT_POS_X,
					"y": 200,
					"text": "",
					"outline": True,
				},



				{
					"name" : "ObserverCount",
					"type" : "text",

					"text_horizontal_align" : "center",

					"outline" : 1,

					"x" : 70,
					"y" : 180,

					"text" : "",
				},
			),
		},
		{
			"name" : "CloseWindow",
			"type" : "window",

			"x" : 0,
			"y" : 0,

			"width" : 132,
			"height" : 48,

			"children" :
			(
				{
					"name" : "MiniMapShowButton",
					"type" : "button",

					"x" : 100,
					"y" : 4,

					"default_image" : ROOT + "minimap_open_default.sub",
					"over_image" : ROOT + "minimap_open_default.sub",
					"down_image" : ROOT + "minimap_open_default.sub",
				},
			),
		},
	),
}