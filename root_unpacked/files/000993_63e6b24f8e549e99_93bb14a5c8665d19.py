import uiScriptLocale

ROOT = "d:/ymir work/ui/public/"
VERSION_ADD_Y = 10

window = {
	"name" : "SystemDialog",
	"style" : ("float",),

	"x" : (SCREEN_WIDTH  - 200) /2,
	"y" : (SCREEN_HEIGHT - (318 - 30)) /2,

	"width" : 200,
	"height" : 318 + VERSION_ADD_Y + 10,

	"children" :
	(
		{
			"name" : "board",
			"type" : "thinboard",

			"x" : 0,
			"y" : 0,

			"width" : 200,
			"height" : 318 - 30 + VERSION_ADD_Y+10,

			"children" :
			(
				{
					"name" : "klawisze_button",
					"type" : "button",

					"x" : 10,
					"y" : 17,

					"text" : uiScriptLocale.KEYCHANGE_KEY_SETTING,
                    "outline":1,

					"default_image" : ROOT + "XLarge_Button_01.sub",
					"over_image" : ROOT + "XLarge_Button_02.sub",
					"down_image" : ROOT + "XLarge_Button_03.sub",
				},
				{
					"name" : "mall_button",
					"type" : "button",

					"x" : 10,
					"y" : 57 + VERSION_ADD_Y,

					"text" : uiScriptLocale.SYSTEM_MALL,
					"text_color" : 0xffF8BF24,
                    "outline":1,

					"default_image" : ROOT + "XLarge_Button_02.sub",
					"over_image" : ROOT + "XLarge_Button_02.sub",
					"down_image" : ROOT + "XLarge_Button_02.sub",
				},

				{
					"name" : "option_button",
					"type" : "button",

					"x" : 10,
					"y" : 87 + VERSION_ADD_Y,

					"text" : uiScriptLocale.GAMEOPTION_TITLE,
                    "outline":1,

					"default_image" : ROOT + "XLarge_Button_01.sub",
					"over_image" : ROOT + "XLarge_Button_02.sub",
					"down_image" : ROOT + "XLarge_Button_03.sub",
				},
				{
					"name" : "movechannel_button",
					"type" : "button",

					"x" : 10,
					"y" : 117 + VERSION_ADD_Y,

					"text" : uiScriptLocale.SYSTEM_MOVE_CHANNEL,
                    "outline":1,

					"default_image" : ROOT + "XLarge_Button_01.sub",
					"over_image" : ROOT + "XLarge_Button_02.sub",
					"down_image" : ROOT + "XLarge_Button_03.sub",
				},
				{
					"name" : "change_button",
					"type" : "button",

					"x" : 10,
					"y" : 147 + VERSION_ADD_Y,

					"text" : uiScriptLocale.SYSTEM_CHANGE,
                    "outline":1,

					"default_image" : ROOT + "XLarge_Button_01.sub",
					"over_image" : ROOT + "XLarge_Button_02.sub",
					"down_image" : ROOT + "XLarge_Button_03.sub",
				},
				{
					"name" : "logout_button",
					"type" : "button",

					"x" : 10,
					"y" : 177 + VERSION_ADD_Y,

					"text" : uiScriptLocale.SYSTEM_LOGOUT,
                    "outline":1,

					"default_image" : ROOT + "XLarge_Button_01.sub",
					"over_image" : ROOT + "XLarge_Button_02.sub",
					"down_image" : ROOT + "XLarge_Button_03.sub",
				},
				{
					"name" : "exit_button",
					"type" : "button",

					"x" : 10,
					"y" : 207 + VERSION_ADD_Y,

					"text" : uiScriptLocale.SYSTEM_EXIT,
                    "outline":1,

					"default_image" : ROOT + "XLarge_Button_01.sub",
					"over_image" : ROOT + "XLarge_Button_02.sub",
					"down_image" : ROOT + "XLarge_Button_03.sub",
				},
				{
					"name" : "cancel_button",
					"type" : "button",

					"x" : 10,
					"y" : 255 + VERSION_ADD_Y,

					"text" : uiScriptLocale.CANCEL,
                    "outline":1,

					"default_image" : ROOT + "XLarge_Button_01.sub",
					"over_image" : ROOT + "XLarge_Button_02.sub",
					"down_image" : ROOT + "XLarge_Button_03.sub",
				},
			),
		},
	),
}