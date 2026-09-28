import uiScriptLocale

ROOT = "d:/ymir work/ui/public/"

window = {
	"name" : "WhisperDialog",
	"style" : ("movable", "float",),

	"x" : 0,
	"y" : 0,

	"width" : 280,
	"height" : 200,

	"children" :
	(
		{
			"name" : "board",
			"type" : "thinboard",
			"style" : ("attach",),

			"x" : 0,
			"y" : 0,

			"width" : 280,
			"height" : 200,

			"children" :
			(
				{
					"name" : "name_slot",
					"type" : "image",
					"style" : ("attach",),

					"x" : 10,
					"y" : 10,

					"image":"d:/ymir work/ui/public/Parameter_Slot_05.sub",

					"children" :
					(
						{
							"name" : "titlename",
							"type" : "text",

							"x" : 3,
							"y" : 3,

							"text" : uiScriptLocale.WHISPER_NAME,
						},
						{
							"name" : "titlename_edit",
							"type" : "editline",

							"x" : 3,
							"y" : 3,

							"width" : 120,
							"height" : 17,

							"input_limit" : 16,

							"text" : uiScriptLocale.WHISPER_NAME,
						},
					),
				},

				{
					"name" : "gamemastermark",
					"type" : "expanded_image",
					"style" : ("attach",),

					"x" : 206,
					"y" : 6,

					"x_scale" : 0.2,
					"y_scale" : 0.2,

					"image" : "locale/shared/effect/ymirred.tga",
				},

				{
					"name" : "ignorebutton",
					"type" : "toggle_button",

					"x" : 145,
					"y" : 10,

					"text" : uiScriptLocale.WHISPER_BAN,

					"default_image" : "d:/ymir work/ui/public/small_thin_button_01.sub",
					"over_image" : "d:/ymir work/ui/public/small_thin_button_02.sub",
					"down_image" : "d:/ymir work/ui/public/small_thin_button_03.sub",
				},
				{
					"name" : "reportviolentwhisperbutton",
					"type" : "button",

					"x" : 145,
					"y" : 10,

					"text" : "",

					"default_image" : "d:/ymir work/ui/public/large_button_01.sub",
					"over_image" : "d:/ymir work/ui/public/large_button_02.sub",
					"down_image" : "d:/ymir work/ui/public/large_button_03.sub",
				},
				{
					"name" : "acceptbutton",
					"type" : "button",

					"x" : 145,
					"y" : 10,

					"text" : uiScriptLocale.OK,

					"default_image" : "d:/ymir work/ui/public/small_thin_button_01.sub",
					"over_image" : "d:/ymir work/ui/public/small_thin_button_02.sub",
					"down_image" : "d:/ymir work/ui/public/small_thin_button_03.sub",
                },
                {
                    "name" : "searchplayershopbutton",
                    "type" : "button",

                    "x" : 280 - 65,
                    "y" : 10,

                    "tooltip_text" : uiScriptLocale.WHISPER_SEARCH_PLAYER_SHOP,

                    "default_image" : "kowal/whisper/shopsearch1.png",
                    "over_image" : "kowal/whisper/shopsearch2.png",
                    "down_image" : "kowal/whisper/shopsearch3.png",
                    "disable_image" : "kowal/whisper/shopsearch1.png",
                },
                {
                    "name" : "AddFriendButton",
                    "type" : "button",

                    "x" : 280 - 53,
                    "y" : 10,

                    "tooltip_text" : uiScriptLocale.MESSENGER_ADD_FRIEND,

                    "default_image" : "d:/ymir work/ui/game/windows/messenger_add_friend_01.sub",
                    "over_image" : "d:/ymir work/ui/game/windows/messenger_add_friend_02.sub",
                    "down_image" : "d:/ymir work/ui/game/windows/messenger_add_friend_03.sub",
                    "disable_image" : "d:/ymir work/ui/game/windows/messenger_add_friend_04.sub",
                },
				{
					"name" : "minimizebutton",
					"type" : "button",

					"x" : 280 - 41,
					"y" : 12,

					"tooltip_text" : uiScriptLocale.MINIMIZE,

					"default_image" : "d:/ymir work/ui/public/minimize_button_01.sub",
					"over_image" : "d:/ymir work/ui/public/minimize_button_02.sub",
					"down_image" : "d:/ymir work/ui/public/minimize_button_03.sub",
				},
				{
					"name" : "closebutton",
					"type" : "button",

					"x" : 280 - 24,
					"y" : 12,

					"tooltip_text" : uiScriptLocale.CLOSE,

					"default_image" : "d:/ymir work/ui/public/close_button_0111.sub",
					"over_image" : "d:/ymir work/ui/public/close_button_0222.sub",
					"down_image" : "d:/ymir work/ui/public/close_button_0333.sub",
				},
				{
					"name" : "scrollbar",
					"type" : "thin_scrollbar",

					"x" : 280 - 25,
					"y" : 35,

					"size" : 280 - 160,
				},

				{
					"name" : "editbar",
					"type" : "bar",

					"x" : 10,
					"y" : 200 - 60,

					"width" : 280 - 18,
					"height" : 50,

					"color" : 0x77000000,

					"children" :
					(
						{
							"name" : "chatline",
							"type" : "editline",

							"x" : 5,
							"y" : 5,

							"width" : 280 - 70,
							"height" : 40,

							"with_codepage" : 1,
							"input_limit" : 40,
							"limit_width" : 280 - 90,
							"multi_line" : 1,
						},
						{
							"name" : "sendbutton",
							"type" : "button",

							"x" : 280 - 80,
							"y" : 10,

							"text" : uiScriptLocale.WHISPER_SEND,

							"default_image" : "d:/ymir work/ui/public/xlarge_thin_button_01.sub",
							"over_image" : "d:/ymir work/ui/public/xlarge_thin_button_02.sub",
							"down_image" : "d:/ymir work/ui/public/xlarge_thin_button_03.sub",
						},

					),
				},
			),
		},
	),
}
