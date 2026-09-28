import uiScriptLocale
import app

WIDTH = 1125
HEIGHT = 505
POS_X = 28

X_ADD = 203
X_ADD2 = 418
X_ADD3 = 608
X_ADD4 = 830

window = {
	"name" : "KeyChange_Window",
	"style" : ("movable", "float",),

	"x" : 0,
	"y" : 0,

	"width" : WIDTH,
	"height" : HEIGHT,

	"children" :
	[
		{
			"name" : "board",
			"type" : "board",
			"style" : ("attach",),

			"x" : 0,
			"y" : 0,

			"width" : WIDTH,
			"height" : HEIGHT,

			"children" :
			[
				{
					"name" : "TitleBar",
					"type" : "titlebar",
					"style" : ("attach",),

					"x" : 6,
					"y" : 6,

					"width" : WIDTH-12,

					"color" : "yellow",

					"children" :
					(
						{ "name" : "TitleName", "type" : "text", "x" : 0, "y" : -3, "text" : uiScriptLocale.KEYCHANGE_KEY_SETTING, "all_align" : "center", "outline":1, },
					),
				},
				{
					"name" : "HorizontalBar1",
					"type" : "horizontalbar",

					"x" : 20,
					"y" : 45,

					"width" : 410,

					"children":
					(
						{
							"name" : "BaseInfo", "type" : "text", "x" : 8, "y" : 2, "text" : uiScriptLocale.KEYCHANGE_BASEACTION,
						},
					),
				},
				{
					"name" : "HorizontalBar1",
					"type" : "horizontalbar",

					"x" : 28 + 360 + 50,
					"y" : 45,

					"width" : 180,

					"children":
					(
						{
							"name" : "BaseInfo", "type" : "text", "x" : 8, "y" : 2, "text" : uiScriptLocale.KEYCHANGE_SLOT_KET,
						},
					),
				},
				{
					"name" : "HorizontalBar1",
					"type" : "horizontalbar",

					"x" : 28 + 540 + 58,
					"y" : 45,

					"width" : 480,

					"children":
					(
						{
							"name" : "BaseInfo", "type" : "text", "x" : 8, "y" : 2, "text" : uiScriptLocale.KEYCHANGE_INTERFACE,
						},
					),
				},
				{
					"name" : "ClearButton",
					"type" : "button",
					"x" : 0,
					"y" : HEIGHT-35,
					"horizontal_align":"center",
					"default_image" : "d:/ymir work/ui/button_exmaple_060.png",
					"over_image" : "d:/ymir work/ui/button_example_061.png",
					"down_image" : "d:/ymir work/ui/button_example_062.png",

					"tooltip_text_new" : "Resetuj Ustawienia",
					"tooltip_text_color" : 0xfff1e6c0,
					"tooltip_x" : 0,
					"tooltip_y" : -35,
				},
				{
					"name" : "SaveButton",
					"type" : "button",
					"x" : -70,
					"y" : HEIGHT-35,
					"horizontal_align":"center",
					"default_image" : "d:/ymir work/ui/button_example_040.png",
					"over_image" : "d:/ymir work/ui/button_example_041.png",
					"down_image" : "d:/ymir work/ui/button_example_042.png",

					"tooltip_text_new" : "Zapisz",
					"tooltip_text_color" : 0xfff1e6c0,
					"tooltip_x" : 0,
					"tooltip_y" : -35,
				},
				{
					"name" : "CancleButton",
					"type" : "button",
					"x" : 70,
					"y" : HEIGHT-35,
					"horizontal_align":"center",
					"default_image" : "d:/ymir work/ui/button_example_050.png",
					"over_image" : "d:/ymir work/ui/button_example_051.png",
					"down_image" : "d:/ymir work/ui/button_example_052.png",

					"tooltip_text_new" : "Anuluj",
					"tooltip_text_color" : 0xfff1e6c0,
					"tooltip_x" : 0,
					"tooltip_y" : -35,
				},

				{ "name" : "Main", "type" : "text", "text" : uiScriptLocale.KEYCHANGE_UP1, "text_horizontal_align" : "left", "x" : POS_X, "y" : 75, },
				{ "name" : "Main", "type" : "text", "text" : uiScriptLocale.KEYCHANGE_DOWN1, "text_horizontal_align" : "left", "x" : POS_X, "y" : 75 + 20, },
				{ "name" : "Main", "type" : "text", "text" : uiScriptLocale.KEYCHANGE_LEFT1, "text_horizontal_align" : "left", "x" : POS_X, "y" : 75 + 40, },
				{ "name" : "Main", "type" : "text", "text" : uiScriptLocale.KEYCHANGE_RIGHT1, "text_horizontal_align" : "left", "x" : POS_X, "y" : 75 + 60, },
				{ "name" : "Main", "type" : "text", "text" : uiScriptLocale.KEYCHANGE_CAM_RIGHT1, "text_horizontal_align" : "left", "x" : POS_X, "y" : 75 + 80, },
				{ "name" : "Main", "type" : "text", "text" : uiScriptLocale.KEYCHANGE_CAM_LEFT1, "text_horizontal_align" : "left", "x" : POS_X, "y" : 75 + 100, },
				{ "name" : "Main", "type" : "text", "text" : uiScriptLocale.KEYCHANGE_CAM_ZOOM_IN1, "text_horizontal_align" : "left", "x" : POS_X, "y" : 75 + 120, },
				{ "name" : "Main", "type" : "text", "text" : uiScriptLocale.KEYCHANGE_CAM_ZOOM_OUT1, "text_horizontal_align" : "left", "x" : POS_X, "y" : 75 + 140, },
				{ "name" : "Main", "type" : "text", "text" : uiScriptLocale.KEYCHANGE_CAM_DOWN1, "text_horizontal_align" : "left", "x" : POS_X, "y" : 75 + 160, },
				{ "name" : "Main", "type" : "text", "text" : uiScriptLocale.KEYCHANGE_CAM_UP1, "text_horizontal_align" : "left", "x" : POS_X, "y" : 75 + 180, },
				{ "name" : "Main", "type" : "text", "text" : uiScriptLocale.KEYCHANGE_ROOT1, "text_horizontal_align" : "left", "x" : POS_X, "y" : 75 + 200, },
				{ "name" : "Main", "type" : "text", "text" : uiScriptLocale.KEYCHANGE_ATTACK, "text_horizontal_align" : "left", "x" : POS_X, "y" : 75 + 220, },
				{ "name" : "Main", "type" : "text", "text" : uiScriptLocale.KEYCHANGE_RIDE_HORSE, "text_horizontal_align" : "left", "x" : POS_X, "y" : 75 + 240, },
				{ "name" : "Main", "type" : "text", "text" : uiScriptLocale.KEYCHANGE_RIDE_PEED, "text_horizontal_align" : "left", "x" : POS_X, "y" : 75 + 260, },
				{ "name" : "Main", "type" : "text", "text" : uiScriptLocale.KEYCHANGE_EMOTION1, "text_horizontal_align" : "left", "x" : POS_X, "y" : 75 + 280, },
				{ "name" : "Main", "type" : "text", "text" : uiScriptLocale.KEYCHANGE_EMOTION2, "text_horizontal_align" : "left", "x" : POS_X, "y" : 75 + 300, },
				{ "name" : "Main", "type" : "text", "text" : uiScriptLocale.KEYCHANGE_EMOTION3, "text_horizontal_align" : "left", "x" : POS_X, "y" : 75 + 320, },
				{ "name" : "Main", "type" : "text", "text" : uiScriptLocale.KEYCHANGE_EMOTION4, "text_horizontal_align" : "left", "x" : POS_X, "y" : 75 + 340, },
				{ "name" : "Main", "type" : "text", "text" : uiScriptLocale.KEYCHANGE_AUTORUN, "text_horizontal_align" : "left", "x" : POS_X, "y" : 75 + 360, },

				{ "name" : "Main", "type" : "text", "text" : uiScriptLocale.KEYCHANGE_UP2, "text_horizontal_align" : "left", "x" : POS_X+X_ADD, "y" : 75, },
				{ "name" : "Main", "type" : "text", "text" : uiScriptLocale.KEYCHANGE_DOWN2, "text_horizontal_align" : "left", "x" : POS_X+X_ADD, "y" : 75 + 20, },
				{ "name" : "Main", "type" : "text", "text" : uiScriptLocale.KEYCHANGE_LEFT2, "text_horizontal_align" : "left", "x" : POS_X+X_ADD, "y" : 75 + 40, },
				{ "name" : "Main", "type" : "text", "text" : uiScriptLocale.KEYCHANGE_RIGHT2, "text_horizontal_align" : "left", "x" : POS_X+X_ADD, "y" : 75 + 60, },
				{ "name" : "Main", "type" : "text", "text" : uiScriptLocale.KEYCHANGE_CAM_RIGHT2, "text_horizontal_align" : "left", "x" : POS_X+X_ADD, "y" : 75 + 80, },
				{ "name" : "Main", "type" : "text", "text" : uiScriptLocale.KEYCHANGE_CAM_LEFT2, "text_horizontal_align" : "left", "x" : POS_X+X_ADD, "y" : 75 + 100, },
				{ "name" : "Main", "type" : "text", "text" : uiScriptLocale.KEYCHANGE_CAM_ZOOM_IN2, "text_horizontal_align" : "left", "x" : POS_X+X_ADD, "y" : 75 + 120, },
				{ "name" : "Main", "type" : "text", "text" : uiScriptLocale.KEYCHANGE_CAM_ZOOM_OUT2, "text_horizontal_align" : "left", "x" : POS_X+X_ADD, "y" : 75 + 140, },
				{ "name" : "Main", "type" : "text", "text" : uiScriptLocale.KEYCHANGE_CAM_DOWN2, "text_horizontal_align" : "left", "x" : POS_X+X_ADD, "y" : 75 + 160, },
				{ "name" : "Main", "type" : "text", "text" : uiScriptLocale.KEYCHANGE_CAM_UP2, "text_horizontal_align" : "left", "x" : POS_X+X_ADD, "y" : 75 + 180, },
				{ "name" : "Main", "type" : "text", "text" : uiScriptLocale.KEYCHANGE_ROOT2, "text_horizontal_align" : "left", "x" : POS_X+X_ADD, "y" : 75 + 200, },
				{ "name" : "Main", "type" : "text", "text" : uiScriptLocale.KEYCHANGE_RIDE, "text_horizontal_align" : "left", "x" : POS_X+X_ADD, "y" : 75 + 220, },
				{ "name" : "Main", "type" : "text", "text" : uiScriptLocale.KEYCHANGE_RIDE_BYE, "text_horizontal_align" : "left", "x" : POS_X+X_ADD, "y" : 75 + 240, },
				{ "name" : "Main", "type" : "text", "text" : uiScriptLocale.KEYCHANGE_EMOTION5, "text_horizontal_align" : "left", "x" : POS_X+X_ADD, "y" : 75 + 260, },
				{ "name" : "Main", "type" : "text", "text" : uiScriptLocale.KEYCHANGE_EMOTION6, "text_horizontal_align" : "left", "x" : POS_X+X_ADD, "y" : 75 + 280, },
				{ "name" : "Main", "type" : "text", "text" : uiScriptLocale.KEYCHANGE_EMOTION7, "text_horizontal_align" : "left", "x" : POS_X+X_ADD, "y" : 75 + 300, },
				{ "name" : "Main", "type" : "text", "text" : uiScriptLocale.KEYCHANGE_EMOTION8, "text_horizontal_align" : "left", "x" : POS_X+X_ADD, "y" : 75 + 320, },
				{ "name" : "Main", "type" : "text", "text" : uiScriptLocale.KEYCHANGE_EMOTION9, "text_horizontal_align" : "left", "x" : POS_X+X_ADD, "y" : 75 + 340, },
				{ "name" : "Main", "type" : "text", "text" : uiScriptLocale.KEYCHANGE_TELEPORTACJA, "text_horizontal_align" : "left", "x" : POS_X+X_ADD, "y" : 75 + 360, },
				{ "name" : "Main", "type" : "text", "text" : uiScriptLocale.KEYCHANGE_SLOT1, "text_horizontal_align" : "left", "x" : POS_X+X_ADD2, "y" : 75, },
				{ "name" : "Main", "type" : "text", "text" : uiScriptLocale.KEYCHANGE_SLOT2, "text_horizontal_align" : "left", "x" : POS_X+X_ADD2, "y" : 75 + 20, },
				{ "name" : "Main", "type" : "text", "text" : uiScriptLocale.KEYCHANGE_SLOT3, "text_horizontal_align" : "left", "x" : POS_X+X_ADD2, "y" : 75 + 40, },
				{ "name" : "Main", "type" : "text", "text" : uiScriptLocale.KEYCHANGE_SLOT4, "text_horizontal_align" : "left", "x" : POS_X+X_ADD2, "y" : 75 + 60, },
				{ "name" : "Main", "type" : "text", "text" : uiScriptLocale.KEYCHANGE_SLOT5, "text_horizontal_align" : "left", "x" : POS_X+X_ADD2, "y" : 75 + 80, },
				{ "name" : "Main", "type" : "text", "text" : uiScriptLocale.KEYCHANGE_SLOT6, "text_horizontal_align" : "left", "x" : POS_X+X_ADD2, "y" : 75 + 100, },
				{ "name" : "Main", "type" : "text", "text" : uiScriptLocale.KEYCHANGE_SLOT7, "text_horizontal_align" : "left", "x" : POS_X+X_ADD2, "y" : 75 + 120, },
				{ "name" : "Main", "type" : "text", "text" : uiScriptLocale.KEYCHANGE_SLOT8, "text_horizontal_align" : "left", "x" : POS_X+X_ADD2, "y" : 75 + 140, },
				{ "name" : "Main", "type" : "text", "text" : uiScriptLocale.KEYCHANGE_QUICKSLOT1, "text_horizontal_align" : "left", "x" : POS_X+X_ADD2, "y" : 75 + 160, },
				{ "name" : "Main", "type" : "text", "text" : uiScriptLocale.KEYCHANGE_QUICKSLOT2, "text_horizontal_align" : "left", "x" : POS_X+X_ADD2, "y" : 75 + 180, },
				{ "name" : "Main", "type" : "text", "text" : uiScriptLocale.KEYCHANGE_QUICKSLOT3, "text_horizontal_align" : "left", "x" : POS_X+X_ADD2, "y" : 75 + 200, },
				{ "name" : "Main", "type" : "text", "text" : uiScriptLocale.KEYCHANGE_QUICKSLOT4, "text_horizontal_align" : "left", "x" : POS_X+X_ADD2, "y" : 75 + 220, },
				{ "name" : "Main", "type" : "text", "text" : uiScriptLocale.KEYCHANGE_STATUS_WINDOW, "text_horizontal_align" : "left", "x" : POS_X+X_ADD3, "y" : 75, },
				{ "name" : "Main", "type" : "text", "text" : uiScriptLocale.KEYCHANGE_SKILL_WINDOW, "text_horizontal_align" : "left", "x" : POS_X+X_ADD3, "y" : 75 + 20, },
				{ "name" : "Main", "type" : "text", "text" : uiScriptLocale.KEYCHANGE_QUEST_WINDOW, "text_horizontal_align" : "left", "x" : POS_X+X_ADD3, "y" : 75 + 40, },
				{ "name" : "Main", "type" : "text", "text" : uiScriptLocale.KEYCHANGE_INVENTORY_WINDOW, "text_horizontal_align" : "left", "x" : POS_X+X_ADD3, "y" : 75 + 60, },
				{ "name" : "Main", "type" : "text", "text" : uiScriptLocale.KEYCHANGE_DDS_WINDOW, "text_horizontal_align" : "left", "x" : POS_X+X_ADD3, "y" : 75 + 80, },
				{ "name" : "Main", "type" : "text", "text" : uiScriptLocale.KEYCHANGE_MINIMAP_WINDOW, "text_horizontal_align" : "left", "x" : POS_X+X_ADD3, "y" : 75 + 100, },
				{ "name" : "Main", "type" : "text", "text" : uiScriptLocale.KEYCHANGE_CHAT_WINDOW, "text_horizontal_align" : "left", "x" : POS_X+X_ADD3, "y" : 75 + 120, },
				{ "name" : "Main", "type" : "text", "text" : uiScriptLocale.KEYCHANGE_QUEST_SCROLL_ONOFF, "text_horizontal_align" : "left", "x" : POS_X+X_ADD3, "y" : 75 + 140, },
				{ "name" : "Main", "type" : "text", "text" : uiScriptLocale.KEYCHANGE_GUILD_WINDOW, "text_horizontal_align" : "left", "x" : POS_X+X_ADD3, "y" : 75 + 160, },
				{ "name" : "Main", "type" : "text", "text" : uiScriptLocale.KEYCHANGE_MESSENGER_WINDOW, "text_horizontal_align" : "left", "x" : POS_X+X_ADD3, "y" : 75 + 180, },
				{ "name" : "Main", "type" : "text", "text" : uiScriptLocale.KEYCHANGE_HELP_WINDOW, "text_horizontal_align" : "left", "x" : POS_X+X_ADD3, "y" : 75 + 200, },
				{ "name" : "Main", "type" : "text", "text" : uiScriptLocale.KEYCHANGE_ACTION_WINDOW, "text_horizontal_align" : "left", "x" : POS_X+X_ADD3, "y" : 75 + 220, },
				{ "name" : "Main", "type" : "text", "text" : uiScriptLocale.KEYCHANGE_MINIMAP_PLUS, "text_horizontal_align" : "left", "x" : POS_X+X_ADD3, "y" : 75 + 240, },
				{ "name" : "Main", "type" : "text", "text" : uiScriptLocale.KEYCHANGE_MINIMAP_MINER, "text_horizontal_align" : "left", "x" : POS_X+X_ADD3, "y" : 75 + 260, },
				{ "name" : "Main", "type" : "text", "text" : uiScriptLocale.KEYCHANGE_SCREENSHOT, "text_horizontal_align" : "left", "x" : POS_X+X_ADD3, "y" : 75 + 280, },
				{ "name" : "Main", "type" : "text", "text" : uiScriptLocale.KEYCHANGE_SHOW_NAME, "text_horizontal_align" : "left", "x" : POS_X+X_ADD3, "y" : 75 + 300, },
				{ "name" : "Main", "type" : "text", "text" : uiScriptLocale.KEYCHANGE_DODATKOWE, "text_horizontal_align" : "left", "x" : POS_X+X_ADD4, "y" : 75, },
				{ "name" : "Main", "type" : "text", "text" : uiScriptLocale.KEYCHANGE_PET, "text_horizontal_align" : "left", "x" :POS_X+X_ADD4, "y" : 75 + 20, },
				{ "name" : "Main", "type" : "text", "text" : uiScriptLocale.KEYCHANGE_DOPALACZE, "text_horizontal_align" : "left", "x" :POS_X+X_ADD4, "y" : 75 + 20 * 2, },
				{ "name" : "Main", "type" : "text", "text" : uiScriptLocale.KEYCHANGE_MARMURY, "text_horizontal_align" : "left", "x" :POS_X+X_ADD4, "y" : 75 + 20 * 3, },
				{ "name" : "Main", "type" : "text", "text" : uiScriptLocale.KEYCHANGE_ZAPIS, "text_horizontal_align" : "left", "x" :POS_X+X_ADD4, "y" : 75 + 20 * 4, },
				{ "name" : "Main", "type" : "text", "text" : uiScriptLocale.KEYCHANGE_TPBOSS, "text_horizontal_align" : "left", "x" :POS_X+X_ADD4, "y" : 75 + 20 * 5, },
				{ "name" : "Main", "type" : "text", "text" : uiScriptLocale.KEYCHANGE_POMOCNIK, "text_horizontal_align" : "left", "x" :POS_X+X_ADD4, "y" : 75 + 20 * 6, },
				{ "name" : "Main", "type" : "text", "text" : uiScriptLocale.KEYCHANGE_PMISJE, "text_horizontal_align" : "left", "x" :POS_X+X_ADD4, "y" : 75 + 20 * 7, },
				{ "name" : "Main", "type" : "text", "text" : uiScriptLocale.KEYCHANGE_ENTER, "text_horizontal_align" : "left", "x" :POS_X+X_ADD4, "y" : 75 + 20 * 8, },
				{ "name" : "Main", "type" : "text", "text" : uiScriptLocale.KEYCHANGE_DUNGEONY, "text_horizontal_align" : "left", "x" :POS_X+X_ADD4, "y" : 75 + 20 * 9, },
				{ "name" : "Main", "type" : "text", "text" : uiScriptLocale.KEYCHANGE_CH1, "text_horizontal_align" : "left", "x" :POS_X+X_ADD4, "y" : 75 + 20 * 10, },
				{ "name" : "Main", "type" : "text", "text" : uiScriptLocale.KEYCHANGE_CH2, "text_horizontal_align" : "left", "x" :POS_X+X_ADD4, "y" : 75 + 20 * 11, },
				{ "name" : "Main", "type" : "text", "text" : uiScriptLocale.KEYCHANGE_CH3, "text_horizontal_align" : "left", "x" :POS_X+X_ADD4, "y" : 75 + 20 * 12, },
				{ "name" : "Main", "type" : "text", "text" : uiScriptLocale.KEYCHANGE_CH4, "text_horizontal_align" : "left", "x" :POS_X+X_ADD4, "y" : 75 + 20 * 13, },
				{ "name" : "Main", "type" : "text", "text" : uiScriptLocale.KEYCHANGE_CH5, "text_horizontal_align" : "left", "x" :POS_X+X_ADD4, "y" : 75 + 20 * 14, },
				{ "name" : "Main", "type" : "text", "text" : uiScriptLocale.KEYCHANGE_CH6, "text_horizontal_align" : "left", "x" :POS_X+X_ADD4, "y" : 75 + 20 * 15, },
			],
		},
	],
}