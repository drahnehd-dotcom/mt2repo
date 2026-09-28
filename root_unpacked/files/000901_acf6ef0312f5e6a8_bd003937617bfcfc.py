#-*- coding: iso-8859-1 -*-
import uiScriptLocale
import app
import emoji
import localeInfo

ROOT_PATH = "d:/ymir work/ui/public/"
PATH = "d:/ymir work/ui/new_weekly_rank/"
NEW_PATH = "d:/ymir work/ui/settings/"
ETC_PATH = "d:/ymir work/ui/"

TEMPORARY_X = +13
BUTTON_TEMPORARY_X = 5
PVP_X = -10

LINE_LABEL_X 	= 20
LINE_LABEL_Y	= 10

LINE_DATA_X 	= 120
LINE_BEGIN	= 40
LINE_STEP	= 25

# KowalMT2: wiersz "Rozciaganie okna" istnieje tylko przy kliencie zbudowanym z
# ENABLE_RESIZABLE_WINDOW. Bez niego okno opcji ma wymiary takie jak przed ta zmiana.
RESIZE_WINDOW_ENABLED = getattr(app, "ENABLE_RESIZABLE_WINDOW", 0)
RESIZE_ROW_HEIGHT = 30 if RESIZE_WINDOW_ENABLED else 0

THINBOARD_WIDTH	= 410
THINBOARD_HEIGHT = 335 + RESIZE_ROW_HEIGHT

MNOZENIE = 1

SMALL_BUTTON_WIDTH 	= 45
MIDDLE_BUTTON_WIDTH 	= 65

BOARD_WIDTH = 590
BOARD_HEIGHT = 375 + RESIZE_ROW_HEIGHT
BG_HEIGHT = 333 + RESIZE_ROW_HEIGHT


# KowalMT2: przelacznik rozciagania okna - doklejany do sekcji systemowej tylko wtedy,
# gdy klient go obsluguje. Wspolrzedne dobrane pod wiersz ponizej limitu FPS.
RESIZE_WINDOW_ITEMS = []
if RESIZE_WINDOW_ENABLED:
	RESIZE_WINDOW_ITEMS = [
		{
			"name" : "resize_window_separator",
			"type" : "image",
			"x" : LINE_LABEL_X-20,
			"y" : LINE_LABEL_Y+318,
			"style":("not_pick",),
			"image" : NEW_PATH+"rectangle.png",
		},
		{
			"name" : "resize_window_name",
			"type" : "text",
			"x" : LINE_LABEL_X,
			"y" : LINE_LABEL_Y+330,
			"text" : uiScriptLocale.OPTION_RESIZE_WINDOW,
		},
		{
			"name" : "resize_window_on",
			"type" : "radio_button",
			"x" : 290,
			"y" : LINE_LABEL_Y+328,
			"default_image" : ROOT_PATH + "small_Button_01.sub",
			"over_image" : ROOT_PATH + "small_Button_02.sub",
			"down_image" : ROOT_PATH + "small_Button_03.sub",
			"children":
			(
				{
					"name" : "resize_window_on_text",
					"type" : "text",
					"x": 0, "y": 0,
					"all_align":"center",
					"text" : uiScriptLocale.OPTION_RESIZE_WINDOW_ON,
					"outline":1,
					"fontname":"Tahoma:12",
				},
			),
		},
		{
			"name" : "resize_window_off",
			"type" : "radio_button",
			"x" : 345,
			"y" : LINE_LABEL_Y+328,
			"default_image" : ROOT_PATH + "small_Button_01.sub",
			"over_image" : ROOT_PATH + "small_Button_02.sub",
			"down_image" : ROOT_PATH + "small_Button_03.sub",
			"children":
			(
				{
					"name" : "resize_window_off_text",
					"type" : "text",
					"x": 0, "y": 0,
					"all_align":"center",
					"text" : uiScriptLocale.OPTION_RESIZE_WINDOW_OFF,
					"outline":1,
					"fontname":"Tahoma:12",
				},
			),
		},
	]

window = {
	"name" : "GameOptionDialog",
	"style" : ["movable", "float",],

	"x" : 0,
	"y" : 0,

	"width" : BOARD_WIDTH,
	"height" : BOARD_HEIGHT,

	"children" :
	[
		{
			"name" : "board",
			"type" : "board",

			"x" : 0,
			"y" : 0,

			"width" : BOARD_WIDTH,
			"height" : BOARD_HEIGHT,

			"children" :
			[
				{
					"name" : "titlebar",
					"type" : "titlebar",
					"style" : ["attach",],

					"x" : 8,
					"y" : 8,

					"width" : BOARD_WIDTH-16,
					"color" : "gray",

					"children" :
					[
						{ "name":"titlename", "type":"text", "x":0, "y":0,
						"text" : uiScriptLocale.GAMEOPTION_TITLE,"outline":1,
						"horizontal_align":"center", "text_horizontal_align":"center" },
					],
				},
				{
					"name":"global_window",
					"type":"window",
					"x":169,"y":30,
					"width":400,
					"height":300,
					"children":
					(
						{
							"name":"thinboard0",
							"type":"thinboard_circle",
							"x":0,"y":0,
							"width" : THINBOARD_WIDTH,
							"height" : THINBOARD_HEIGHT,
							"children":
							(
								{
									"name":"bg",
									"type" : "thinboard",
									"x":1,"y":1,
									"width" : 408, "height" : BG_HEIGHT,
								},
								{
									"name" : "name_color",
									"type" : "text",

									"x" : LINE_LABEL_X,
									"y" : LINE_LABEL_Y+2,

									"text" : uiScriptLocale.OPTION_NAME_COLOR,
								},
								{
									"name" : "name_color_normal",
									"type" : "radio_button",
									"x" : LINE_DATA_X+MIDDLE_BUTTON_WIDTH*0,
									"y" : LINE_LABEL_Y,
									"default_image" : "d:/ymir work/ui/public/middle_button_01.sub",
									"over_image" : "d:/ymir work/ui/public/middle_button_02.sub",
									"down_image" : "d:/ymir work/ui/public/middle_button_03.sub",
									"children":
									(
										{
											"name" : "btn_text",
											"type" : "text",
											"x": 0, "y": 0,
											"all_align":"center",
											"text":uiScriptLocale.OPTION_NAME_COLOR_NORMAL,
											"outline":1,
											"fontname":"Tahoma:12",
										},
									),
								},
								{
									"name" : "name_color_empire",
									"type" : "radio_button",
									"x" : LINE_DATA_X+MIDDLE_BUTTON_WIDTH*MNOZENIE,
									"y" : LINE_LABEL_Y,
									"default_image" : "d:/ymir work/ui/public/middle_button_01.sub",
									"over_image" : "d:/ymir work/ui/public/middle_button_02.sub",
									"down_image" : "d:/ymir work/ui/public/middle_button_03.sub",
									"children":
									(
										{
											"name" : "btn_text",
											"type" : "text",
											"x": 0, "y": 0,
											"all_align":"center",
											"text" : uiScriptLocale.OPTION_NAME_COLOR_EMPIRE,
											"outline":1,
											"fontname":"Tahoma:12",
										},
									),
								},

								{
									"name" : "rectangle",
									"type" : "image",
									"x" : LINE_LABEL_X-20,
									"y" : LINE_LABEL_Y+22,
									"style":("not_pick",),
									"image" : NEW_PATH+"rectangle.png",
								},

								{
									"name" : "target_board",
									"type" : "text",

									"x" : LINE_LABEL_X,
									"y" : LINE_LABEL_Y+27,

									"text" : uiScriptLocale.OPTION_TARGET_BOARD,
								},
								{
									"name" : "target_board_no_view",
									"type" : "radio_button",

									"x" : LINE_DATA_X+MIDDLE_BUTTON_WIDTH*0,
									"y" : LINE_LABEL_Y+25,

									"default_image" : "d:/ymir work/ui/public/middle_button_01.sub",
									"over_image" : "d:/ymir work/ui/public/middle_button_02.sub",
									"down_image" : "d:/ymir work/ui/public/middle_button_03.sub",
									"children":
									(
										{
											"name" : "btn_text",
											"type" : "text",
											"x": 0, "y": 0,
											"all_align":"center",
											"text" : uiScriptLocale.OPTION_TARGET_BOARD_NO_VIEW,
											"outline":1,
											"fontname":"Tahoma:12",
										},
									),
								},
								{
									"name" : "target_board_view",
									"type" : "radio_button",

									"x" : LINE_DATA_X+MIDDLE_BUTTON_WIDTH*MNOZENIE,
									"y" : LINE_LABEL_Y+25,

									"default_image" : "d:/ymir work/ui/public/middle_button_01.sub",
									"over_image" : "d:/ymir work/ui/public/middle_button_02.sub",
									"down_image" : "d:/ymir work/ui/public/middle_button_03.sub",
									"children":
									(
										{
											"name" : "btn_text",
											"type" : "text",
											"x": 0, "y": 0,
											"all_align":"center",
											"text" : uiScriptLocale.OPTION_TARGET_BOARD_VIEW,
											"outline":1,
											"fontname":"Tahoma:12",
										},
									),
								},

								{
									"name" : "rectangle",
									"type" : "image",
									"x" : LINE_LABEL_X-20,
									"y" : LINE_LABEL_Y+47,
									"style":("not_pick",),
									"image" : NEW_PATH+"rectangle.png",
								},


								{
									"name" : "pvp_mode",
									"type" : "text",

									"x" : LINE_LABEL_X,
									"y" : LINE_LABEL_Y+52,

									"text" : uiScriptLocale.OPTION_PVPMODE,
								},
								{
									"name" : "pvp_peace",
									"type" : "radio_button",

									"x" : LINE_DATA_X+SMALL_BUTTON_WIDTH*0,
									"y" : LINE_LABEL_Y+50,

									"tooltip_text_new" : uiScriptLocale.OPTION_PVPMODE_PEACE_TOOLTIP,
									"tooltip_text_color" : 0xfff1e6c0,
									"tooltip_x" : 40,
									"tooltip_y" : -30,
									"outline":1,

									"default_image" : "d:/ymir work/ui/public/middle_button_01.sub",
									"over_image" : "d:/ymir work/ui/public/middle_button_02.sub",
									"down_image" : "d:/ymir work/ui/public/middle_button_03.sub",
									"children":
									(
										{
											"name" : "btn_text",
											"type" : "text",
											"x": 0, "y": 0,
											"all_align":"center",
											"text" : uiScriptLocale.OPTION_PVPMODE_PEACE,
											"outline":1,
											"fontname":"Tahoma:12",
										},
									),
								},
								{
									"name" : "pvp_revenge",
									"type" : "radio_button",

									"x" : LINE_DATA_X+MIDDLE_BUTTON_WIDTH*MNOZENIE,
									"y" : LINE_LABEL_Y+50,

									"tooltip_text_new" : uiScriptLocale.OPTION_PVPMODE_REVENGE_TOOLTIP,
									"tooltip_text_color" : 0xfff1e6c0,
									"tooltip_x" : 10,
									"tooltip_y" : -30,

									"default_image" : "d:/ymir work/ui/public/middle_button_01.sub",
									"over_image" : "d:/ymir work/ui/public/middle_button_02.sub",
									"down_image" : "d:/ymir work/ui/public/middle_button_03.sub",
									"children":
									(
										{
											"name" : "btn_text",
											"type" : "text",
											"x": 0, "y": 0,
											"all_align":"center",
											"text" : uiScriptLocale.OPTION_PVPMODE_REVENGE,
											"outline":1,
											"fontname":"Tahoma:12",
										},
									),
								},
								{
									"name" : "pvp_guild",
									"type" : "radio_button",

									"x" : LINE_DATA_X+MIDDLE_BUTTON_WIDTH*MNOZENIE*1.98,
									"y" : LINE_LABEL_Y+50,

									"tooltip_text_new" : uiScriptLocale.OPTION_PVPMODE_GUILD_TOOLTIP,
									"tooltip_text_color" : 0xfff1e6c0,
									"tooltip_x" : 10,
									"tooltip_y" : -30,

									"default_image" : "d:/ymir work/ui/public/middle_button_01.sub",
									"over_image" : "d:/ymir work/ui/public/middle_button_02.sub",
									"down_image" : "d:/ymir work/ui/public/middle_button_03.sub",
									"children":
									(
										{
											"name" : "btn_text",
											"type" : "text",
											"x": 0, "y": 0,
											"all_align":"center",
											"text" : uiScriptLocale.OPTION_PVPMODE_GUILD,
											"outline":1,
											"fontname":"Tahoma:12",
										},
									),
								},
								{
									"name" : "pvp_free",
									"type" : "radio_button",

									"x" : LINE_DATA_X+MIDDLE_BUTTON_WIDTH*MNOZENIE*2.96,
									"y" : LINE_LABEL_Y+50,

									"tooltip_text_new" : uiScriptLocale.OPTION_PVPMODE_FREE_TOOLTIP,
									"tooltip_text_color" : 0xfff1e6c0,
									"tooltip_x" : 10,
									"tooltip_y" : -30,

									"default_image" : "d:/ymir work/ui/public/middle_button_01.sub",
									"over_image" : "d:/ymir work/ui/public/middle_button_02.sub",
									"down_image" : "d:/ymir work/ui/public/middle_button_03.sub",
									"children":
									(
										{
											"name" : "btn_text",
											"type" : "text",
											"x": 0, "y": 0,
											"all_align":"center",
											"text" : uiScriptLocale.OPTION_PVPMODE_FREE,
											"outline":1,
											"fontname":"Tahoma:12",
										},
									),
								},

								{
									"name" : "rectangle",
									"type" : "image",
									"x" : LINE_LABEL_X-20,
									"y" : LINE_LABEL_Y+72,
									"style":("not_pick",),
									"image" : NEW_PATH+"rectangle.png",
								},

								{
									"name" : "block",
									"type" : "text",

									"x" : LINE_LABEL_X,
									"y" : LINE_LABEL_Y+77,

									"text" : uiScriptLocale.OPTION_BLOCK,
								},
								{
									"name" : "block_exchange_button",
									"type" : "toggle_button",

									"x" : LINE_DATA_X+MIDDLE_BUTTON_WIDTH*0,
									"y" : LINE_LABEL_Y+75,

									"default_image" : "d:/ymir work/ui/public/middle_button_01.sub",
									"over_image" : "d:/ymir work/ui/public/middle_button_02.sub",
									"down_image" : "d:/ymir work/ui/public/middle_button_03.sub",
									"children":
									(
										{
											"name" : "btn_text",
											"type" : "text",
											"x": 0, "y": 0,
											"all_align":"center",
											"text" : uiScriptLocale.OPTION_BLOCK_EXCHANGE,
											"outline":1,
											"fontname":"Tahoma:12",
										},
									),
								},
								{
									"name" : "block_party_button",
									"type" : "toggle_button",

									"x" : LINE_DATA_X+MIDDLE_BUTTON_WIDTH*MNOZENIE,
									"y" : LINE_LABEL_Y+75,

									"default_image" : "d:/ymir work/ui/public/middle_button_01.sub",
									"over_image" : "d:/ymir work/ui/public/middle_button_02.sub",
									"down_image" : "d:/ymir work/ui/public/middle_button_03.sub",
									"children":
									(
										{
											"name" : "btn_text",
											"type" : "text",
											"x": 0, "y": 0,
											"all_align":"center",
											"text" : uiScriptLocale.OPTION_BLOCK_PARTY,
											"outline":1,
											"fontname":"Tahoma:12",
										},
									),
								},
								{
									"name" : "block_guild_button",
									"type" : "toggle_button",

									"x" : LINE_DATA_X+MIDDLE_BUTTON_WIDTH*MNOZENIE*1.98,
									"y" : LINE_LABEL_Y+75,

									"default_image" : "d:/ymir work/ui/public/middle_button_01.sub",
									"over_image" : "d:/ymir work/ui/public/middle_button_02.sub",
									"down_image" : "d:/ymir work/ui/public/middle_button_03.sub",
									"children":
									(
										{
											"name" : "btn_text",
											"type" : "text",
											"x": 0, "y": 0,
											"all_align":"center",
											"text" : uiScriptLocale.OPTION_BLOCK_GUILD,
											"outline":1,
											"fontname":"Tahoma:12",
										},
									),
								},
								{
									"name" : "block_whisper_button",
									"type" : "toggle_button",

									"x" : LINE_DATA_X+MIDDLE_BUTTON_WIDTH*0,
									"y" : LINE_LABEL_Y+100,

									"default_image" : "d:/ymir work/ui/public/middle_button_01.sub",
									"over_image" : "d:/ymir work/ui/public/middle_button_02.sub",
									"down_image" : "d:/ymir work/ui/public/middle_button_03.sub",
									"children":
									(
										{
											"name" : "btn_text",
											"type" : "text",
											"x": 0, "y": 0,
											"all_align":"center",
											"text" : uiScriptLocale.OPTION_BLOCK_WHISPER,
											"outline":1,
											"fontname":"Tahoma:12",
										},
									),
								},
								{
									"name" : "block_friend_button",
									"type" : "toggle_button",

									"x" : LINE_DATA_X+MIDDLE_BUTTON_WIDTH*MNOZENIE,
									"y" : LINE_LABEL_Y+100,

									"default_image" : "d:/ymir work/ui/public/middle_button_01.sub",
									"over_image" : "d:/ymir work/ui/public/middle_button_02.sub",
									"down_image" : "d:/ymir work/ui/public/middle_button_03.sub",
									"children":
									(
										{
											"name" : "btn_text",
											"type" : "text",
											"x": 0, "y": 0,
											"all_align":"center",
											"text" : uiScriptLocale.OPTION_BLOCK_FRIEND,
											"outline":1,
											"fontname":"Tahoma:12",
										},
									),
								},
								{
									"name" : "block_party_request_button",
									"type" : "toggle_button",

									"x" : LINE_DATA_X+MIDDLE_BUTTON_WIDTH*MNOZENIE*1.98,
									"y" : LINE_LABEL_Y+100,

									"default_image" : "d:/ymir work/ui/public/middle_button_01.sub",
									"over_image" : "d:/ymir work/ui/public/middle_button_02.sub",
									"down_image" : "d:/ymir work/ui/public/middle_button_03.sub",
									"children":
									(
										{
											"name" : "btn_text",
											"type" : "text",
											"x": 0, "y": 0,
											"all_align":"center",
											"text" : uiScriptLocale.OPTION_BLOCK_PARTY_REQUEST,
											"outline":1,
											"fontname":"Tahoma:12",
										},
									),
								},

								{
									"name" : "rectangle",
									"type" : "image",
									"x" : LINE_LABEL_X-20,
									"y" : LINE_LABEL_Y+122,
									"style":("not_pick",),
									"image" : NEW_PATH+"rectangle.png",
								},

								{
									"name" : "chat",
									"type" : "text",

									"x" : LINE_LABEL_X,
									"y" : LINE_LABEL_Y+127,

									"text" : uiScriptLocale.OPTION_VIEW_CHAT,
								},
								{
									"name" : "view_chat_on_button",
									"type" : "radio_button",

									"x" : LINE_DATA_X,
									"y" : LINE_LABEL_Y+125,

									"default_image" : "d:/ymir work/ui/public/middle_button_01.sub",
									"over_image" : "d:/ymir work/ui/public/middle_button_02.sub",
									"down_image" : "d:/ymir work/ui/public/middle_button_03.sub",
									"children":
									(
										{
											"name" : "btn_text",
											"type" : "text",
											"x": 0, "y": 0,
											"all_align":"center",
											"text" : uiScriptLocale.OPTION_VIEW_CHAT_ON,
											"outline":1,
											"fontname":"Tahoma:12",
										},
									),
								},
								{
									"name" : "view_chat_off_button",
									"type" : "radio_button",

									"x" : LINE_DATA_X+MIDDLE_BUTTON_WIDTH*MNOZENIE,
									"y" : LINE_LABEL_Y+125,

									"default_image" : "d:/ymir work/ui/public/middle_button_01.sub",
									"over_image" : "d:/ymir work/ui/public/middle_button_02.sub",
									"down_image" : "d:/ymir work/ui/public/middle_button_03.sub",
									"children":
									(
										{
											"name" : "btn_text",
											"type" : "text",
											"x": 0, "y": 0,
											"all_align":"center",
											"text" : uiScriptLocale.OPTION_VIEW_CHAT_OFF,
											"outline":1,
											"fontname":"Tahoma:12",
										},
									),
								},

								{
									"name" : "rectangle",
									"type" : "image",
									"x" : LINE_LABEL_X-20,
									"y" : LINE_LABEL_Y+147,
									"style":("not_pick",),
									"image" : NEW_PATH+"rectangle.png",
								},

								{
									"name" : "always_show_name",
									"type" : "text",

									"x" : LINE_LABEL_X,
									"y" : LINE_LABEL_Y+152,

									"text" : uiScriptLocale.OPTION_ALWAYS_SHOW_NAME,
								},
								{
									"name" : "always_show_name_on_button",
									"type" : "radio_button",

									"x" : LINE_DATA_X,
									"y" : LINE_LABEL_Y+150,

									"default_image" : "d:/ymir work/ui/public/middle_button_01.sub",
									"over_image" : "d:/ymir work/ui/public/middle_button_02.sub",
									"down_image" : "d:/ymir work/ui/public/middle_button_03.sub",
									"children":
									(
										{
											"name" : "btn_text",
											"type" : "text",
											"x": 0, "y": 0,
											"all_align":"center",
											"text" : uiScriptLocale.OPTION_ALWAYS_SHOW_NAME_ON,
											"outline":1,
											"fontname":"Tahoma:12",
										},
									),
								},
								{
									"name" : "always_show_name_off_button",
									"type" : "radio_button",

									"x" : LINE_DATA_X+MIDDLE_BUTTON_WIDTH*MNOZENIE,
									"y" : LINE_LABEL_Y+150,

									"default_image" : "d:/ymir work/ui/public/middle_button_01.sub",
									"over_image" : "d:/ymir work/ui/public/middle_button_02.sub",
									"down_image" : "d:/ymir work/ui/public/middle_button_03.sub",
									"children":
									(
										{
											"name" : "btn_text",
											"type" : "text",
											"x": 0, "y": 0,
											"all_align":"center",
											"text" : uiScriptLocale.OPTION_ALWAYS_SHOW_NAME_OFF,
											"outline":1,
											"fontname":"Tahoma:12",
										},
									),
								},

								{
									"name" : "rectangle",
									"type" : "image",
									"x" : LINE_LABEL_X-20,
									"y" : LINE_LABEL_Y+172,
									"style":("not_pick",),
									"image" : NEW_PATH+"rectangle.png",
								},

								{
									"name" : "effect_on_off",
									"type" : "text",

									"x" : LINE_LABEL_X,
									"y" : LINE_LABEL_Y+177,

									"text" : uiScriptLocale.OPTION_EFFECT,
								},
								{
									"name" : "show_damage_on_button",
									"type" : "radio_button",

									"x" : LINE_DATA_X,
									"y" : LINE_LABEL_Y+175,

									"default_image" : "d:/ymir work/ui/public/middle_button_01.sub",
									"over_image" : "d:/ymir work/ui/public/middle_button_02.sub",
									"down_image" : "d:/ymir work/ui/public/middle_button_03.sub",
									"children":
									(
										{
											"name" : "btn_text",
											"type" : "text",
											"x": 0, "y": 0,
											"all_align":"center",
											"text" : uiScriptLocale.OPTION_VIEW_CHAT_ON,
											"outline":1,
											"fontname":"Tahoma:12",
										},
									),
								},
								{
									"name" : "show_damage_off_button",
									"type" : "radio_button",

									"x" : LINE_DATA_X+MIDDLE_BUTTON_WIDTH*MNOZENIE,
									"y" : LINE_LABEL_Y+175,

									"default_image" : "d:/ymir work/ui/public/middle_button_01.sub",
									"over_image" : "d:/ymir work/ui/public/middle_button_02.sub",
									"down_image" : "d:/ymir work/ui/public/middle_button_03.sub",
									"children":
									(
										{
											"name" : "btn_text",
											"type" : "text",
											"x": 0, "y": 0,
											"all_align":"center",
											"text" : uiScriptLocale.OPTION_VIEW_CHAT_OFF,
											"outline":1,
											"fontname":"Tahoma:12",
										},
									),
								},

								{
									"name" : "rectangle",
									"type" : "image",
									"x" : LINE_LABEL_X-20,
									"y" : LINE_LABEL_Y+197,
									"style":("not_pick",),
									"image" : NEW_PATH+"rectangle.png",
								},

								{
									"name" : "salestext_on_off",
									"type" : "text",

									"x" : LINE_LABEL_X,
									"y" : LINE_LABEL_Y+202,

									"text" : uiScriptLocale.OPTION_SALESTEXT,
								},
								{
									"name" : "salestext_on_button",
									"type" : "radio_button",

									"x" : LINE_DATA_X,
									"y" : LINE_LABEL_Y+200,

									"default_image" : "d:/ymir work/ui/public/middle_button_01.sub",
									"over_image" : "d:/ymir work/ui/public/middle_button_02.sub",
									"down_image" : "d:/ymir work/ui/public/middle_button_03.sub",
									"children":
									(
										{
											"name" : "btn_text",
											"type" : "text",
											"x": 0, "y": 0,
											"all_align":"center",
											"text" : uiScriptLocale.OPTION_SALESTEXT_VIEW_ON,
											"outline":1,
											"fontname":"Tahoma:12",
										},
									),
								},
								{
									"name" : "salestext_off_button",
									"type" : "radio_button",

									"x" : LINE_DATA_X+MIDDLE_BUTTON_WIDTH*MNOZENIE,
									"y" : LINE_LABEL_Y+200,

									"default_image" : "d:/ymir work/ui/public/middle_button_01.sub",
									"over_image" : "d:/ymir work/ui/public/middle_button_02.sub",
									"down_image" : "d:/ymir work/ui/public/middle_button_03.sub",
									"children":
									(
										{
											"name" : "btn_text",
											"type" : "text",
											"x": 0, "y": 0,
											"all_align":"center",
											"text" : uiScriptLocale.OPTION_SALESTEXT_VIEW_OFF,
											"outline":1,
											"fontname":"Tahoma:12",
										},
									),
								},

								{
									"name" : "rectangle",
									"type" : "image",
									"x" : LINE_LABEL_X-20,
									"y" : LINE_LABEL_Y+222,
									"style":("not_pick",),
									"image" : NEW_PATH+"rectangle.png",
								},

								{
									"name" : "font_text",
									"type" : "text",

									"x" : LINE_LABEL_X,
									"y" : LINE_LABEL_Y+227,

									"text" : uiScriptLocale.GAME_OPTION_FONT,
								},
								{
									"name" : "font_type",
									"type" : "radio_button",

									"x" : LINE_DATA_X,
									"y" : LINE_LABEL_Y+225,

									"default_image" : "d:/ymir work/ui/public/middle_button_01.sub",
									"over_image" : "d:/ymir work/ui/public/middle_button_02.sub",
									"down_image" : "d:/ymir work/ui/public/middle_button_03.sub",
									"children":
									(
										{
											"name" : "btn_text",
											"type" : "text",
											"x": 0, "y": 0,
											"all_align":"center",
											"text" : uiScriptLocale.GAME_OPTION_FONT_SMALL,
											"outline":1,
											"fontname":"Tahoma:12",
										},
									),
								},
								{
									"name" : "font_type2",
									"type" : "radio_button",

									"x" : LINE_DATA_X+MIDDLE_BUTTON_WIDTH*MNOZENIE,
									"y" : LINE_LABEL_Y+225,

									"default_image" : "d:/ymir work/ui/public/middle_button_01.sub",
									"over_image" : "d:/ymir work/ui/public/middle_button_02.sub",
									"down_image" : "d:/ymir work/ui/public/middle_button_03.sub",
									"children":
									(
										{
											"name" : "btn_text",
											"type" : "text",
											"x": 0, "y": 0,
											"all_align":"center",
											"text" : uiScriptLocale.GAME_OPTION_FONT_BIG,
											"outline":1,
											"fontname":"Tahoma:12",
										},
									),
								},
								{
									"name" : "rectangle",
									"type" : "image",
									"x" : LINE_LABEL_X-20,
									"y" : LINE_LABEL_Y+247,
									"style":("not_pick",),
									"image" : NEW_PATH+"rectangle.png",
								},
								{
									"name" : "show_mob_info",
									"type" : "text",

									"multi_line" : 1,

									"x" : LINE_LABEL_X,
									"y" : LINE_LABEL_Y+252,

									"text" : uiScriptLocale.OPTION_MOB_INFO,
								},
								{
									"name" : "show_mob_level_button",
									"type" : "toggle_button",

									"x" : LINE_DATA_X,
									"y" : LINE_LABEL_Y+250,

									"default_image" : "d:/ymir work/ui/public/middle_button_01.sub",
									"over_image" : "d:/ymir work/ui/public/middle_button_02.sub",
									"down_image" : "d:/ymir work/ui/public/middle_button_03.sub",
									"children":
									(
										{
											"name" : "btn_text",
											"type" : "text",
											"x": 0, "y": 0,
											"all_align":"center",
											"text" : uiScriptLocale.OPTION_MOB_INFO_LEVEL,
											"outline":1,
											"fontname":"Tahoma:12",
										},
									),
								},
								{
									"name" : "show_mob_AI_flag_button",
									"type" : "toggle_button",

									"x" : LINE_DATA_X+MIDDLE_BUTTON_WIDTH*MNOZENIE,
									"y" : LINE_LABEL_Y+250,

									"default_image" : "d:/ymir work/ui/public/middle_button_01.sub",
									"over_image" : "d:/ymir work/ui/public/middle_button_02.sub",
									"down_image" : "d:/ymir work/ui/public/middle_button_03.sub",
									"children":
									(
										{
											"name" : "btn_text",
											"type" : "text",
											"x": 0, "y": 0,
											"all_align":"center",
											"text" : uiScriptLocale.OPTION_MOB_INFO_AGGR,
											"outline":1,
											"fontname":"Tahoma:12",
										},
									),
								},
								{
									"name" : "rectangle",
									"type" : "image",
									"x" : LINE_LABEL_X-20,
									"y" : LINE_LABEL_Y+272,
									"style":("not_pick",),
									"image" : NEW_PATH+"rectangle.png",
								},
								{
									"name" : "dogmode_on_off",
									"type" : "text",

									"multi_line" : 1,

									"x" : LINE_LABEL_X,
									"y" : LINE_LABEL_Y+277,

									"text" : uiScriptLocale.GAME_OPTION_MONSTERS,
								},
								{
									"name" : "dog_mode_open",
									"type" : "radio_button",

									"x" : LINE_DATA_X,
									"y" : LINE_LABEL_Y+275,

									"default_image" : "d:/ymir work/ui/public/middle_button_01.sub",
									"over_image" : "d:/ymir work/ui/public/middle_button_02.sub",
									"down_image" : "d:/ymir work/ui/public/middle_button_03.sub",
									"children":
									(
										{
											"name" : "btn_text",
											"type" : "text",
											"x": 0, "y": 0,
											"all_align":"center",
											"text" : uiScriptLocale.GAME_OPTION_MONSTERS_DOGS,
											"outline":1,
											"fontname":"Tahoma:12",
										},
									),
								},
								{
									"name" : "dog_mode_close",
									"type" : "radio_button",

									"x" : LINE_DATA_X+MIDDLE_BUTTON_WIDTH*MNOZENIE,
									"y" : LINE_LABEL_Y+275,

									"default_image" : "d:/ymir work/ui/public/middle_button_01.sub",
									"over_image" : "d:/ymir work/ui/public/middle_button_02.sub",
									"down_image" : "d:/ymir work/ui/public/middle_button_03.sub",
									"children":
									(
										{
											"name" : "btn_text",
											"type" : "text",
											"x": 0, "y": 0,
											"all_align":"center",
											"text" : uiScriptLocale.GAME_OPTION_MONSTERS_NORMAL,
											"outline":1,
											"fontname":"Tahoma:12",
										},
									),
								},
							),
						},
					),
				},
				{
					"name":"system_window",
					"type":"window",
					"x":169,"y":30,
					"width":400,
					"height":360,
					"children":
					(
						{
							"name":"thinboard0",
							"type":"thinboard_circle",
							"x":0,"y":0,
							"width" : THINBOARD_WIDTH,
							"height" : THINBOARD_HEIGHT,
							"children":
							(
								{
									"name":"bg",
									"type" : "thinboard",
									"x":1,"y":1,
									"width" : 408, "height" : BG_HEIGHT,
								},
                                {
                                    "name" : "music_name",
                                    "type" : "text",
                                    "x" : LINE_LABEL_X,
                                    "y" : LINE_LABEL_Y+34,
                                    "text" : uiScriptLocale.OPTION_MUSIC,
                                },
                                {
                                    "name" : "music_volume_controller",
                                    "type" : "sliderbarNew",
                                    "x" : LINE_LABEL_X+MIDDLE_BUTTON_WIDTH*1.2,
                                    "y" : LINE_LABEL_Y+37,
                                },
                                {
									"name" : "rectangle",
									"type" : "image",
									"x" : LINE_LABEL_X-20,
									"y" : LINE_LABEL_Y+25,
									"style":("not_pick",),
									"image" : NEW_PATH+"rectangle.png",
								},
                                {
                                    "name" : "sound_name",
                                    "type" : "text",
                                    "x" : LINE_LABEL_X,
                                    "y" : LINE_LABEL_Y,
                                    "text" : uiScriptLocale.OPTION_SOUND,
                                },
                                {
                                    "name" : "sound_volume_controller",
                                    "type" : "sliderbarNew",

                                    "x" : LINE_LABEL_X+MIDDLE_BUTTON_WIDTH*1.2,
                                    "y" : LINE_LABEL_Y+3,
                                },
                                {
                                    "name" : "bgm_button",
                                    "type" : "button",
                                    "x" : LINE_LABEL_X-2,
                                    "y" : LINE_LABEL_Y+60,
                                    "default_image" : ROOT_PATH + "Middle_Button_01.sub",
                                    "over_image" : ROOT_PATH + "Middle_Button_02.sub",
                                    "down_image" : ROOT_PATH + "Middle_Button_03.sub",
                                    "children":
									(
										{
											"name" : "bgm_text",
											"type" : "text",
											"x": 0, "y": 0,
											"all_align":"center",
                                            "text" : uiScriptLocale.OPTION_MUSIC_CHANGE,
											"outline":1,
											"fontname":"Tahoma:12",
										},
									),
								},
                                {
                                    "name" : "bgm_file",
                                    "type" : "text",
                                    "x" : LINE_LABEL_X+MIDDLE_BUTTON_WIDTH*1.75,
                                    "y" : LINE_LABEL_Y+62,
                                    "text" : uiScriptLocale.OPTION_MUSIC_DEFAULT_THEMA,
                                    "outline":1,
                                },
                                {
									"name" : "rectangle",
									"type" : "image",
									"x" : LINE_LABEL_X-20,
									"y" : LINE_LABEL_Y+90,
									"style":("not_pick",),
									"image" : NEW_PATH+"rectangle.png",
								},
                                {
                                    "name" : "camera_mode",
                                    "type" : "text",
                                    "x" : LINE_LABEL_X,
                                    "y" : LINE_LABEL_Y+100,
                                    "text" : uiScriptLocale.OPTION_CAMERA_DISTANCE,
                                },
                                {
                                    "name" : "camera_short",
                                    "type" : "radio_button",
                                    "x" : LINE_LABEL_X+MIDDLE_BUTTON_WIDTH*1.9,
                                    "y" : LINE_LABEL_Y+99,
                                    "default_image" : ROOT_PATH + "Middle_Button_01.sub",
                                    "over_image" : ROOT_PATH + "Middle_Button_02.sub",
                                    "down_image" : ROOT_PATH + "Middle_Button_03.sub",
                                    "children":
									(
										{
											"name" : "camera_short_text",
											"type" : "text",
											"x": 0, "y": 0,
											"all_align":"center",
                                            "text" : uiScriptLocale.OPTION_CAMERA_DISTANCE_SHORT,
											"outline":1,
											"fontname":"Tahoma:12",
										},
									),
								},
                                {
                                    "name" : "camera_long",
                                    "type" : "radio_button",
                                    "x" : LINE_LABEL_X+MIDDLE_BUTTON_WIDTH*3,
                                    "y" : LINE_LABEL_Y+99,
                                    "default_image" : ROOT_PATH + "Middle_Button_01.sub",
                                    "over_image" : ROOT_PATH + "Middle_Button_02.sub",
                                    "down_image" : ROOT_PATH + "Middle_Button_03.sub",
                                    "children":
									(
										{
											"name" : "camera_long_text",
											"type" : "text",
											"x": 0, "y": 0,
											"all_align":"center",
                                            "text" : uiScriptLocale.OPTION_CAMERA_DISTANCE_LONG,
											"outline":1,
											"fontname":"Tahoma:12",
										},
									),
								},
                                {
									"name" : "rectangle",
									"type" : "image",
									"x" : LINE_LABEL_X-20,
									"y" : LINE_LABEL_Y+127,
									"style":("not_pick",),
									"image" : NEW_PATH+"rectangle.png",
								},

                                {
                                    "name" : "fog_mode",
                                    "type" : "text",
                                    "x" : LINE_LABEL_X,
									"y" : LINE_LABEL_Y+136,
                                    "text" : uiScriptLocale.OPTION_FOG,
                                },
                                {
                                    "name" : "fog_level0",
                                    "type" : "radio_button",
                                    "x" : LINE_LABEL_X+MIDDLE_BUTTON_WIDTH*1.8,
                                    "y" : LINE_LABEL_Y+136,
                                    "default_image" : ROOT_PATH + "small_Button_01.sub",
                                    "over_image" : ROOT_PATH + "small_Button_02.sub",
                                    "down_image" : ROOT_PATH + "small_Button_03.sub",
                                    "children":
									(
										{
											"name" : "fog_level0_text",
											"type" : "text",
											"x": 0, "y": 0,
											"all_align":"center",
                                            "text" : uiScriptLocale.OPTION_FOG_DENSE,
											"outline":1,
											"fontname":"Tahoma:12",
										},
									),
								},
                                {
                                    "name" : "fog_level1",
                                    "type" : "radio_button",
                                    "x" : LINE_LABEL_X+MIDDLE_BUTTON_WIDTH*2.6,
                                    "y" : LINE_LABEL_Y+136,
                                    "default_image" : ROOT_PATH + "small_Button_01.sub",
                                    "over_image" : ROOT_PATH + "small_Button_02.sub",
                                    "down_image" : ROOT_PATH + "small_Button_03.sub",
                                    "children":
									(
										{
											"name" : "fog_level1_text",
											"type" : "text",
											"x": 0, "y": 0,
											"all_align":"center",
                                            "text" : uiScriptLocale.OPTION_FOG_MIDDLE,
											"outline":1,
											"fontname":"Tahoma:12",
										},
									),
								},
                                {
                                    "name" : "fog_level2",
                                    "type" : "radio_button",
                                    "x" : LINE_LABEL_X+MIDDLE_BUTTON_WIDTH*3.4,
                                    "y" : LINE_LABEL_Y+136,
                                    "default_image" : ROOT_PATH + "small_Button_01.sub",
                                    "over_image" : ROOT_PATH + "small_Button_02.sub",
                                    "down_image" : ROOT_PATH + "small_Button_03.sub",
                                    "children":
									(
										{
											"name" : "fog_level2_text",
											"type" : "text",
											"x": 0, "y": 0,
											"all_align":"center",
                                            "text" : uiScriptLocale.OPTION_FOG_LIGHT,
											"outline":1,
											"fontname":"Tahoma:12",
										},
									),
								},
                                {
									"name" : "rectangle",
									"type" : "image",
									"x" : LINE_LABEL_X-20,
									"y" : LINE_LABEL_Y+163,
									"style":("not_pick",),
									"image" : NEW_PATH+"rectangle.png",
								},
                                {
                                    "name" : "tiling_mode",
                                    "type" : "text",
                                    "x" : LINE_LABEL_X,
									"y" : LINE_LABEL_Y+173,
                                    "text" : uiScriptLocale.OPTION_TILING,
                                },
                                {
                                    "name" : "tiling_cpu",
                                    "type" : "radio_button",
                                    "x" : LINE_LABEL_X+MIDDLE_BUTTON_WIDTH*1.8,
                                    "y" : LINE_LABEL_Y+173,
                                    "default_image" : ROOT_PATH + "small_Button_01.sub",
                                    "over_image" : ROOT_PATH + "small_Button_02.sub",
                                    "down_image" : ROOT_PATH + "small_Button_03.sub",
                                    "children":
									(
										{
											"name" : "tilling_cpu_text",
											"type" : "text",
											"x": 0, "y": 0,
											"all_align":"center",
                                            "text" : uiScriptLocale.OPTION_TILING_CPU,
											"outline":1,
											"fontname":"Tahoma:12",
										},
									),
								},
                                {
                                    "name" : "tiling_gpu",
                                    "type" : "radio_button",
                                    "x" : LINE_LABEL_X+MIDDLE_BUTTON_WIDTH*2.6,
                                    "y" : LINE_LABEL_Y+173,
                                    "default_image" : ROOT_PATH + "small_Button_01.sub",
                                    "over_image" : ROOT_PATH + "small_Button_02.sub",
                                    "down_image" : ROOT_PATH + "small_Button_03.sub",
                                    "children":
									(
										{
											"name" : "tiling_gpu_text",
											"type" : "text",
											"x": 0, "y": 0,
											"all_align":"center",
                                            "text" : uiScriptLocale.OPTION_TILING_GPU,
											"outline":1,
											"fontname":"Tahoma:12",
										},
									),
								},
                                {
                                    "name" : "tiling_apply",
                                    "type" : "button",
                                    "x" : LINE_LABEL_X+MIDDLE_BUTTON_WIDTH*3.4,
                                    "y" : LINE_LABEL_Y+173,
                                    "default_image" : ROOT_PATH + "middle_Button_01.sub",
                                    "over_image" : ROOT_PATH + "middle_Button_02.sub",
                                    "down_image" : ROOT_PATH + "middle_Button_03.sub",
                                    "children":
									(
										{
											"name" : "tiling_gpu_text",
											"type" : "text",
											"x": 0, "y": 0,
											"all_align":"center",
                                            "text" : uiScriptLocale.OPTION_TILING_APPLY,
											"outline":1,
											"fontname":"Tahoma:12",
										},
									),
								},
                                {
									"name" : "rectangle",
									"type" : "image",
									"x" : LINE_LABEL_X-20,
									"y" : LINE_LABEL_Y+201,
									"style":("not_pick",),
									"image" : NEW_PATH+"rectangle.png",
								},

                                {
                                    "name" : "fov_option",
                                    "type" : "text",
                                    "x" : LINE_LABEL_X,
									"y" : LINE_LABEL_Y+210,
                                    "text" : uiScriptLocale.FOV_OPTION,
                                },
                                {
                                    "name" : "fov_controller",
                                    "type" : "sliderbarNew",
                                    "x" : LINE_LABEL_X+MIDDLE_BUTTON_WIDTH*1.2,
                                    "y" : LINE_LABEL_Y+211,
                                },
                                {
                                    "name" : "fov_reset_button",
                                    "type" : "button",
                                    "x" : LINE_LABEL_X+MIDDLE_BUTTON_WIDTH*5.32,
                                    "y" : LINE_LABEL_Y+210,

                                    "tooltip_text_new" : uiScriptLocale.FOV_RESET_OPTION_TOOLTIP,
                                    "tooltip_text_color" : 0xfff1e6c0,
									"tooltip_x" : 0,
									"tooltip_y" : -30,

                                    "default_image" : "d:/ymir work/ui/game/windows/reset_badge_button_default.tga",
                                    "over_image" : "d:/ymir work/ui/game/windows/reset_badge_button_over.tga",
                                    "down_image" : "d:/ymir work/ui/game/windows/reset_badge_button_down.tga",
                                },
                                {
                                    "name" : "fov_value_text",
                                    "type" : "text",
                                    "x" : LINE_LABEL_X+MIDDLE_BUTTON_WIDTH*4.85,
                                    "y" : LINE_LABEL_Y+211,
                                    "text" : "0",
                                    "outline":1,
                                    "fontname":"Tahoma:14b",
                                },
								{
									"name" : "rectangle",
									"type" : "image",
									"x" : LINE_LABEL_X-20,
									"y" : LINE_LABEL_Y+241,
									"style":("not_pick",),
									"image" : NEW_PATH+"rectangle.png",
								},

								# Skybox selection section
								{
									"name" : "skybox_text",
									"type" : "text",
									"x" : LINE_LABEL_X,
									"y" : LINE_LABEL_Y+250,
                                    "text" : uiScriptLocale.GAME_OPTION_SKYBOX,
								},
								{
									"name" : "skybox_type_default",
									"type" : "radio_button",
									"x" : LINE_LABEL_X,
									"y" : LINE_LABEL_Y+270,
									"default_image" : ROOT_PATH + "small_Button_01.sub",
									"over_image" : ROOT_PATH + "small_Button_02.sub",
									"down_image" : ROOT_PATH + "small_Button_03.sub",
									"children":
									(
										{
											"name" : "skybox_default_text",
											"type" : "text",
											"x": 0, "y": 0,
											"all_align":"center",
											"text" : uiScriptLocale.GAME_OPTION_SKYBOX_DEFAULT,
											"outline":1,
											"fontname":"Tahoma:12",
										},
									),
								},
								{
									"name" : "skybox_type_1",
									"type" : "radio_button",
									"x" : LINE_LABEL_X+55,
									"y" : LINE_LABEL_Y+270,
									"default_image" : ROOT_PATH + "small_Button_01.sub",
									"over_image" : ROOT_PATH + "small_Button_02.sub",
									"down_image" : ROOT_PATH + "small_Button_03.sub",
									"children":
									(
										{
											"name" : "skybox_1_text",
											"type" : "text",
											"x": 0, "y": 0,
											"all_align":"center",
											"text" : "1",
											"outline":1,
											"fontname":"Tahoma:12",
										},
									),
								},
								{
									"name" : "skybox_type_2",
									"type" : "radio_button",
									"x" : LINE_LABEL_X+110,
									"y" : LINE_LABEL_Y+270,
									"default_image" : ROOT_PATH + "small_Button_01.sub",
									"over_image" : ROOT_PATH + "small_Button_02.sub",
									"down_image" : ROOT_PATH + "small_Button_03.sub",
									"children":
									(
										{
											"name" : "skybox_2_text",
											"type" : "text",
											"x": 0, "y": 0,
											"all_align":"center",
											"text" : "2",
											"outline":1,
											"fontname":"Tahoma:12",
										},
									),
								},
								{
									"name" : "skybox_type_3",
									"type" : "radio_button",
									"x" : LINE_LABEL_X+165,
									"y" : LINE_LABEL_Y+270,
									"default_image" : ROOT_PATH + "small_Button_01.sub",
									"over_image" : ROOT_PATH + "small_Button_02.sub",
									"down_image" : ROOT_PATH + "small_Button_03.sub",
									"children":
									(
										{
											"name" : "skybox_3_text",
											"type" : "text",
											"x": 0, "y": 0,
											"all_align":"center",
											"text" : "3",
											"outline":1,
											"fontname":"Tahoma:12",
										},
									),
								},
								{
									"name" : "skybox_type_4",
									"type" : "radio_button",
									"x" : LINE_LABEL_X,
									"y" : LINE_LABEL_Y+295,
									"default_image" : ROOT_PATH + "small_Button_01.sub",
									"over_image" : ROOT_PATH + "small_Button_02.sub",
									"down_image" : ROOT_PATH + "small_Button_03.sub",
									"children":
									(
										{
											"name" : "skybox_4_text",
											"type" : "text",
											"x": 0, "y": 0,
											"all_align":"center",
											"text" : "4",
											"outline":1,
											"fontname":"Tahoma:12",
										},
									),
								},
								{
									"name" : "skybox_type_5",
									"type" : "radio_button",
									"x" : LINE_LABEL_X+55,
									"y" : LINE_LABEL_Y+295,
									"default_image" : ROOT_PATH + "small_Button_01.sub",
									"over_image" : ROOT_PATH + "small_Button_02.sub",
									"down_image" : ROOT_PATH + "small_Button_03.sub",
									"children":
									(
										{
											"name" : "skybox_5_text",
											"type" : "text",
											"x": 0, "y": 0,
											"all_align":"center",
											"text" : "5",
											"outline":1,
											"fontname":"Tahoma:12",
										},
									),
								},
								{
									"name" : "skybox_type_6",
									"type" : "radio_button",
									"x" : LINE_LABEL_X+110,
									"y" : LINE_LABEL_Y+295,
									"default_image" : ROOT_PATH + "small_Button_01.sub",
									"over_image" : ROOT_PATH + "small_Button_02.sub",
									"down_image" : ROOT_PATH + "small_Button_03.sub",
									"children":
									(
										{
											"name" : "skybox_6_text",
											"type" : "text",
											"x": 0, "y": 0,
											"all_align":"center",
											"text" : "6",
											"outline":1,
											"fontname":"Tahoma:12",
										},
									),
								},
								{
									"name" : "skybox_type_7",
									"type" : "radio_button",
									"x" : LINE_LABEL_X+165,
									"y" : LINE_LABEL_Y+295,
									"default_image" : ROOT_PATH + "small_Button_01.sub",
									"over_image" : ROOT_PATH + "small_Button_02.sub",
									"down_image" : ROOT_PATH + "small_Button_03.sub",
									"children":
									(
										{
											"name" : "skybox_7_text",
											"type" : "text",
											"x": 0, "y": 0,
											"all_align":"center",
											"text" : "7",
											"outline":1,
											"fontname":"Tahoma:12",
										},
									),
								},
								{
									"name" : "vsync_mode",
									"type" : "text",
									"x" : 240,
									"y" : LINE_LABEL_Y+272,
									"text" : uiScriptLocale.OPTION_VSYNC,
								},
								{
									"name" : "vsync_on",
									"type" : "radio_button",
									"x" : 290,
									"y" : LINE_LABEL_Y+270,
									"default_image" : ROOT_PATH + "small_Button_01.sub",
									"over_image" : ROOT_PATH + "small_Button_02.sub",
									"down_image" : ROOT_PATH + "small_Button_03.sub",
									"children":
									(
										{
											"name" : "vsync_on_text",
											"type" : "text",
											"x": 0, "y": 0,
											"all_align":"center",
											"text" : uiScriptLocale.OPTION_VSYNC_ON,
											"outline":1,
											"fontname":"Tahoma:12",
										},
									),
								},
								{
									"name" : "vsync_off",
									"type" : "radio_button",
									"x" : 345,
									"y" : LINE_LABEL_Y+270,
									"default_image" : ROOT_PATH + "small_Button_01.sub",
									"over_image" : ROOT_PATH + "small_Button_02.sub",
									"down_image" : ROOT_PATH + "small_Button_03.sub",
									"children":
									(
										{
											"name" : "vsync_off_text",
											"type" : "text",
											"x": 0, "y": 0,
											"all_align":"center",
											"text" : uiScriptLocale.OPTION_VSYNC_OFF,
											"outline":1,
											"fontname":"Tahoma:12",
										},
									),
								},
								{
									"name" : "fps_limit_name",
									"type" : "text",
									"x" : 240,
									"y" : LINE_LABEL_Y+297,
									"text" : uiScriptLocale.OPTION_FPS_LIMIT,
								},
								{
									"name" : "fps_limit_button",
									"type" : "button",
									"x" : 310,
									"y" : LINE_LABEL_Y+295,
									"default_image" : ROOT_PATH + "Middle_Button_01.sub",
									"over_image" : ROOT_PATH + "Middle_Button_02.sub",
									"down_image" : ROOT_PATH + "Middle_Button_03.sub",
									"children":
									(
										{
											"name" : "fps_limit_value",
											"type" : "text",
											"x": 0, "y": 0,
											"all_align":"center",
											"text" : "60",
											"outline":1,
											"fontname":"Tahoma:12",
										},
									),
								},
							) + tuple(RESIZE_WINDOW_ITEMS),
						},
					),
				},
				{
					"name":"desc_window",
					"type":"window",
					"x":169,"y":30,
					"width":400,
					"height":300,
					"children":
					(
						{
							"name":"thinboard0",
							"type":"thinboard_circle",
							"x":0,"y":0,
							"width" : THINBOARD_WIDTH,
							"height" : THINBOARD_HEIGHT,
							"children":
							(
								{
									"name":"bg",
									"type" : "thinboard",
									"x":1,"y":1,
									"width" : 408, "height" : BG_HEIGHT,
								},
								{
									"name":"desc0",
									"type":"thinboard",
									"x":20,"y":10,
									"width":200,
									"height":55,
									"children":
									(
										{
											"name" : "desc0_emoji",
											"type" : "text",
											"x" : 0,
											"y" : -14,
											"all_align":"center",
											"text" : localeInfo.CHEST_DROP_INFO,
										},
										{
											"name" : "desc0_text",
											"type" : "text",
											"x" : 0,
											"y" : 0,
											"all_align":"center",
											"text" : uiScriptLocale.GAME_OPTIONS_FIND_CHESTS_DESC_1,
										},
										{
											"name" : "desc0_text",
											"type" : "text",
											"x" : 60,
											"y" : LINE_LABEL_Y+22,
											"text" : uiScriptLocale.GAME_OPTIONS_FIND_CHESTS_DESC_2,
										},
									),
								},
								{
									"name" : "desc0_on",
									"type" : "radio_button",
									"x" : LINE_DATA_X+MIDDLE_BUTTON_WIDTH*1.8,
									"y" : LINE_LABEL_Y+18,
									"default_image" : "d:/ymir work/ui/public/middle_button_01.sub",
									"over_image" : "d:/ymir work/ui/public/middle_button_02.sub",
									"down_image" : "d:/ymir work/ui/public/middle_button_03.sub",
									"children":
									(
										{
											"name" : "btn_text",
											"type" : "text",
											"x": 0, "y": 0,
											"all_align":"center",
											"text": uiScriptLocale.GAME_OPTIONS_ACTIVATE_BUTTON,
											"outline":1,
											"fontname":"Tahoma:12",
										},
									),
								},
								{
									"name" : "desc0_off",
									"type" : "radio_button",
									"x" : LINE_DATA_X+MIDDLE_BUTTON_WIDTH*MNOZENIE*2.8,
									"y" : LINE_LABEL_Y+18,
									"default_image" : "d:/ymir work/ui/public/middle_button_01.sub",
									"over_image" : "d:/ymir work/ui/public/middle_button_02.sub",
									"down_image" : "d:/ymir work/ui/public/middle_button_03.sub",
									"children":
									(
										{
											"name" : "btn_text",
											"type" : "text",
											"x": 0, "y": 0,
											"all_align":"center",
											"text" : uiScriptLocale.GAME_OPTIONS_DEACTIVATE_BUTTON,
											"outline":1,
											"fontname":"Tahoma:12",
										},
									),
								},

								{
									"name":"desc1",
									"type":"thinboard",
									"x":20,"y":80,
									"width":200,
									"height":30,
									"children":
									(
										{
											"name" : "desc1_emoji",
											"type" : "text",
											"x" : 0,
											"y" : -2,
											"all_align":"center",
                                            "text" : uiScriptLocale.GAME_OPTIONS_SPLIT_OPTION.format(emoji.AppendEmoji("icon/emoji/key_shift.png"),
                                                                                                     emoji.AppendEmoji("icon/emoji/key_lclick.png") 
                                                                                                     )
										},
									),
								},
								{
									"name" : "desc1_on",
									"type" : "radio_button",
									"x" : LINE_DATA_X+MIDDLE_BUTTON_WIDTH*1.8,
									"y" : LINE_LABEL_Y+76,
									"default_image" : "d:/ymir work/ui/public/middle_button_01.sub",
									"over_image" : "d:/ymir work/ui/public/middle_button_02.sub",
									"down_image" : "d:/ymir work/ui/public/middle_button_03.sub",
									"children":
									(
										{
											"name" : "btn_text",
											"type" : "text",
											"x": 0, "y": 0,
											"all_align":"center",
											"text": uiScriptLocale.GAME_OPTIONS_ACTIVATE_BUTTON,
											"outline":1,
											"fontname":"Tahoma:12",
										},
									),
								},
								{
									"name" : "desc1_off",
									"type" : "radio_button",
									"x" : LINE_DATA_X+MIDDLE_BUTTON_WIDTH*MNOZENIE*2.8,
									"y" : LINE_LABEL_Y+76,
									"default_image" : "d:/ymir work/ui/public/middle_button_01.sub",
									"over_image" : "d:/ymir work/ui/public/middle_button_02.sub",
									"down_image" : "d:/ymir work/ui/public/middle_button_03.sub",
									"children":
									(
										{
											"name" : "btn_text",
											"type" : "text",
											"x": 0, "y": 0,
											"all_align":"center",
											"text": uiScriptLocale.GAME_OPTIONS_DEACTIVATE_BUTTON,
											"outline":1,
											"fontname":"Tahoma:12",
										},
									),
								},
								{
									"name":"desc2",
									"type":"thinboard",
									"x":20,"y":130,
									"width":200,
									"height":30,
									"children":
									(
										{
											"name" : "desc2_emoji",
											"type" : "text",
											"x" : 0,
											"y" : -2,
											"all_align":"center",
                                            "text" : uiScriptLocale.GAME_OPTIONS_PULL_OUT.format(emoji.AppendEmoji("icon/emoji/key_rclick.png"))
										},
									),
								},
								{
									"name" : "desc2_on",
									"type" : "radio_button",
									"x" : LINE_DATA_X+MIDDLE_BUTTON_WIDTH*1.8,
									"y" : LINE_LABEL_Y+125,
									"default_image" : "d:/ymir work/ui/public/middle_button_01.sub",
									"over_image" : "d:/ymir work/ui/public/middle_button_02.sub",
									"down_image" : "d:/ymir work/ui/public/middle_button_03.sub",
									"children":
									(
										{
											"name" : "btn_text",
											"type" : "text",
											"x": 0, "y": 0,
											"all_align":"center",
											"text": uiScriptLocale.GAME_OPTIONS_ACTIVATE_BUTTON,
											"outline":1,
											"fontname":"Tahoma:12",
										},
									),
								},
								{
									"name" : "desc2_off",
									"type" : "radio_button",
									"x" : LINE_DATA_X+MIDDLE_BUTTON_WIDTH*MNOZENIE*2.8,
									"y" : LINE_LABEL_Y+125,
									"default_image" : "d:/ymir work/ui/public/middle_button_01.sub",
									"over_image" : "d:/ymir work/ui/public/middle_button_02.sub",
									"down_image" : "d:/ymir work/ui/public/middle_button_03.sub",
									"children":
									(
										{
											"name" : "btn_text",
											"type" : "text",
											"x": 0, "y": 0,
											"all_align":"center",
											"text": uiScriptLocale.GAME_OPTIONS_DEACTIVATE_BUTTON,
											"outline":1,
											"fontname":"Tahoma:12",
										},
									),
								},
								{
									"name":"desc3",
									"type":"thinboard",
									"x":20,"y":180,
									"width":200,
									"height":40,
									"children":
									(
										{
											"name" : "desc3_emoji",
											"type" : "text",
											"x" : 0,
											"y" : -8,
											"all_align":"center",
											"text" : emoji.AppendEmoji("icon/emoji/key_shift.png")+" + "+emoji.AppendEmoji("icon/emoji/key_rclick.png"),
										},
										{
											"name" : "desc3_text",
											"type" : "text",
											"x" : 0,
											"y" : 5,
											"all_align":"center",
											"text" : uiScriptLocale.GAME_OPTIONS_ADD_TO_SPECIAL_INVENTORY,
										},
									),
								},
								{
									"name" : "desc3_on",
									"type" : "radio_button",
									"x" : LINE_DATA_X+MIDDLE_BUTTON_WIDTH*1.8,
									"y" : LINE_LABEL_Y+180,
									"default_image" : "d:/ymir work/ui/public/middle_button_01.sub",
									"over_image" : "d:/ymir work/ui/public/middle_button_02.sub",
									"down_image" : "d:/ymir work/ui/public/middle_button_03.sub",
									"children":
									(
										{
											"name" : "btn_text",
											"type" : "text",
											"x": 0, "y": 0,
											"all_align":"center",
											"text": uiScriptLocale.GAME_OPTIONS_ACTIVATE_BUTTON,
											"outline":1,
											"fontname":"Tahoma:12",
										},
									),
								},
								{
									"name" : "desc3_off",
									"type" : "radio_button",
									"x" : LINE_DATA_X+MIDDLE_BUTTON_WIDTH*MNOZENIE*2.8,
									"y" : LINE_LABEL_Y+180,
									"default_image" : "d:/ymir work/ui/public/middle_button_01.sub",
									"over_image" : "d:/ymir work/ui/public/middle_button_02.sub",
									"down_image" : "d:/ymir work/ui/public/middle_button_03.sub",
									"children":
									(
										{
											"name" : "btn_text",
											"type" : "text",
											"x": 0, "y": 0,
											"all_align":"center",
											"text": uiScriptLocale.GAME_OPTIONS_DEACTIVATE_BUTTON,
											"outline":1,
											"fontname":"Tahoma:12",
										},
									),
								},


								{
									"name" : "rectangle",
									"type" : "image",
									"x" : LINE_LABEL_X-20,
									"y" : LINE_LABEL_Y+62,
									"style":("not_pick",),
									"image" : NEW_PATH+"rectangle.png",
								},
								{
									"name" : "rectangle",
									"type" : "image",
									"x" : LINE_LABEL_X-20,
									"y" : LINE_LABEL_Y+110,
									"style":("not_pick",),
									"image" : NEW_PATH+"rectangle.png",
								},
								{
									"name" : "rectangle",
									"type" : "image",
									"x" : LINE_LABEL_X-20,
									"y" : LINE_LABEL_Y+160,
									"style":("not_pick",),
									"image" : NEW_PATH+"rectangle.png",
								},
								{
									"name" : "rectangle",
									"type" : "image",
									"x" : LINE_LABEL_X-20,
									"y" : LINE_LABEL_Y+218,
									"style":("not_pick",),
									"image" : NEW_PATH+"rectangle.png",
								},
							),
						},
					),
				},
				{
					"name":"ukrywanie_window",
					"type":"window",
					"x":169,"y":30,
					"width":400,
					"height":300,
					"children":
					(
						{
							"name":"thinboard0",
							"type":"thinboard_circle",
							"x":0,"y":0,
							"width" : THINBOARD_WIDTH,
							"height" : THINBOARD_HEIGHT,
							"children":
							(
								{
									"name":"bg",
									"type" : "thinboard",
									"x":1,"y":1,
									"width" : 408, "height" : BG_HEIGHT,
								},
                                
                              
                                {
									"name" : "rectangle",
									"type" : "image",
									"x" : LINE_LABEL_X-20,
									"y" : LINE_LABEL_Y+25,
									"style":("not_pick",),
									"image" : NEW_PATH+"rectangle.png",
								},
                               
                                {
                                    "name" : "wierzchowce_mode",
                                    "type" : "text",
                                    "x" : LINE_LABEL_X,
                                    "y" : LINE_LABEL_Y+35,
                                    "text" : uiScriptLocale.GAME_OPTIONS_MOUNTS_VISIBILITY,
                                },
                                {
                                    "name" : "wierzchowce_on",
                                    "type" : "radio_button",
                                    "x" : LINE_LABEL_X+MIDDLE_BUTTON_WIDTH*1.9,
                                    "y" : LINE_LABEL_Y+34,
                                    "default_image" : ROOT_PATH + "Middle_Button_01.sub",
                                    "over_image" : ROOT_PATH + "Middle_Button_02.sub",
                                    "down_image" : ROOT_PATH + "Middle_Button_03.sub",
                                    "children":
									(
										{
											"name" : "wierzchowce_on_text",
											"type" : "text",
											"x": 0, "y": 0,
											"all_align":"center",
                                            "text" : uiScriptLocale.GAME_OPTIONS_MOUNTS_SHOW,
											"outline":1,
											"fontname":"Tahoma:12",
										},
									),
								},
                               {
                                    "name" : "wierzchowce_off",
                                    "type" : "radio_button",
                                    "x" : LINE_LABEL_X+MIDDLE_BUTTON_WIDTH*3,
                                    "y" : LINE_LABEL_Y+34,
                                    "default_image" : ROOT_PATH + "Middle_Button_01.sub",
                                    "over_image" : ROOT_PATH + "Middle_Button_02.sub",
                                    "down_image" : ROOT_PATH + "Middle_Button_03.sub",
                                    "children":
									(
										{
											"name" : "wierzchowce_off_text",
											"type" : "text",
											"x": 0, "y": 0,
											"all_align":"center",
                                            "text" : uiScriptLocale.GAME_OPTIONS_MOUNTS_HIDE,
											"outline":1,
											"fontname":"Tahoma:12",
										},
									),
								},
                                {
									"name" : "rectangle",
									"type" : "image",
									"x" : LINE_LABEL_X-20,
									"y" : LINE_LABEL_Y+65,
									"style":("not_pick",),
									"image" : NEW_PATH+"rectangle.png",
								},
								{
                                    "name" : "pety_mode",
                                    "type" : "text",
                                    "x" : LINE_LABEL_X,
                                    "y" : LINE_LABEL_Y+75,
                                    "text" : uiScriptLocale.GAME_OPTIONS_PETS_VISIBILITY,
                                },
                                {
                                    "name" : "pety_on",
                                    "type" : "radio_button",
                                    "x" : LINE_LABEL_X+MIDDLE_BUTTON_WIDTH*1.9,
                                    "y" : LINE_LABEL_Y+73,
                                    "default_image" : ROOT_PATH + "Middle_Button_01.sub",
                                    "over_image" : ROOT_PATH + "Middle_Button_02.sub",
                                    "down_image" : ROOT_PATH + "Middle_Button_03.sub",
                                    "children":
									(
										{
											"name" : "pety_text",
											"type" : "text",
											"x": 0, "y": 0,
											"all_align":"center",
                                            "text" : uiScriptLocale.GAME_OPTIONS_PETS_SHOW,
											"outline":1,
											"fontname":"Tahoma:12",
										},
									),
								},
                               	{
                                    "name" : "pety_off",
                                    "type" : "radio_button",
                                    "x" : LINE_LABEL_X+MIDDLE_BUTTON_WIDTH*3,
                                    "y" : LINE_LABEL_Y+73,
                                    "default_image" : ROOT_PATH + "Middle_Button_01.sub",
                                    "over_image" : ROOT_PATH + "Middle_Button_02.sub",
                                    "down_image" : ROOT_PATH + "Middle_Button_03.sub",
                                    "children":
									(
										{
											"name" : "pety_text",
											"type" : "text",
											"x": 0, "y": 0,
											"all_align":"center",
                                            "text" : uiScriptLocale.GAME_OPTIONS_PETS_HIDE,
											"outline":1,
											"fontname":"Tahoma:12",
										},
									),
								},
								{
									"name" : "rectangle",
									"type" : "image",
									"x" : LINE_LABEL_X-20,
									"y" : LINE_LABEL_Y+103,
									"style":("not_pick",),
									"image" : NEW_PATH+"rectangle.png",
								},

								{
                                    "name" : "autobuff_mude",
                                    "type" : "text",
                                    "x" : LINE_LABEL_X,
                                    "y" : LINE_LABEL_Y+115,
                                    "text" : uiScriptLocale.OPTION_AUTOBUFF,
                                },
                                {
                                    "name" : "autobuff_on",
                                    "type" : "radio_button",
                                    "x" : LINE_LABEL_X+MIDDLE_BUTTON_WIDTH*1.9,
                                    "y" : LINE_LABEL_Y+113,
                                    "default_image" : ROOT_PATH + "Middle_Button_01.sub",
                                    "over_image" : ROOT_PATH + "Middle_Button_02.sub",
                                    "down_image" : ROOT_PATH + "Middle_Button_03.sub",
                                    "children":
									(
										{
											"name" : "autobuff_text",
											"type" : "text",
											"x": 0, "y": 0,
											"all_align":"center",
                                            "text" : uiScriptLocale.GAME_OPTIONS_BUFFI_SHOW,
											"outline":1,
											"fontname":"Tahoma:12",
										},
									),
								},
                               	{
                                    "name" : "autobuff_off",
                                    "type" : "radio_button",
                                    "x" : LINE_LABEL_X+MIDDLE_BUTTON_WIDTH*3,
                                    "y" : LINE_LABEL_Y+113,
                                    "default_image" : ROOT_PATH + "Middle_Button_01.sub",
                                    "over_image" : ROOT_PATH + "Middle_Button_02.sub",
                                    "down_image" : ROOT_PATH + "Middle_Button_03.sub",
                                    "children":
									(
										{
											"name" : "autobuff_text",
											"type" : "text",
											"x": 0, "y": 0,
											"all_align":"center",
                                            "text" : uiScriptLocale.GAME_OPTIONS_BUFFI_HIDE,
											"outline":1,
											"fontname":"Tahoma:12",
										},
									),
								},
								{
									"name" : "rectangle",
									"type" : "image",
									"x" : LINE_LABEL_X-20,
									"y" : LINE_LABEL_Y+142,
									"style":("not_pick",),
									"image" : NEW_PATH+"rectangle.png",
								},
							),
						},
					),
				},
				{
					"name":"voicechat_window",
					"type":"window",
					"x":169,"y":30,
					"width":400,
					"height":340,
					"children":
					(
						{
							"name":"thinboard0",
							"type":"thinboard_circle",
							"x":0,"y":0,
							"width" : THINBOARD_WIDTH,
							"height" : 340,
							"children":
							(
								{
									"name":"bg",
									"type" : "thinboard",
									"style":("not_pick",),
									"x":1,"y":1,
									"width" : 408, "height" : BG_HEIGHT,
								},
								{
									"name":"vc_instr1",
									"type":"text",
									"style":("not_pick",),
									"x":LINE_LABEL_X,"y":LINE_LABEL_Y,
									"text":uiScriptLocale.VOICE_CHAT_INSTRUCTION1,
								},
								{
									"name":"vc_instr2",
									"type":"text",
									"style":("not_pick",),
									"x":LINE_LABEL_X,"y":LINE_LABEL_Y+LINE_STEP,
									"text":uiScriptLocale.VOICE_CHAT_INSTRUCTION2,
								},
								{
									"name":"vc_instr3",
									"type":"text",
									"style":("not_pick",),
									"x":LINE_LABEL_X,"y":LINE_LABEL_Y+LINE_STEP*2,
									"text":uiScriptLocale.VOICE_CHAT_INSTRUCTION3,
								},
								{
									"name":"vc_instr4",
									"type":"text",
									"style":("not_pick",),
									"x":LINE_LABEL_X,"y":LINE_LABEL_Y+LINE_STEP*3,
									"text":uiScriptLocale.VOICE_CHAT_INSTRUCTION4,
								},
								{
									"name":"rectangle",
									"type":"image",
									"style":("not_pick",),
									"x":LINE_LABEL_X-20,"y":LINE_LABEL_Y+LINE_STEP*4,
									"style":("not_pick",),
									"image":NEW_PATH+"rectangle.png",
								},
								{
									"name":"vc_mic_dev_label",
									"type":"text",
									"style":("not_pick",),
									"x":LINE_LABEL_X,"y":LINE_LABEL_Y+LINE_STEP*4+12,
									"text":uiScriptLocale.VOICE_CHAT_MIC_DEVICE,
								},
								{
									"name":"vc_mic_device",
									"type":"button",
									"x":LINE_LABEL_X+MIDDLE_BUTTON_WIDTH*2.4,"y":LINE_LABEL_Y+LINE_STEP*4+10,
									"default_image":ROOT_PATH + "Middle_Button_01.sub",
									"over_image":ROOT_PATH + "Middle_Button_02.sub",
									"down_image":ROOT_PATH + "Middle_Button_03.sub",
									"children":
									(
										{
										"name":"vc_mic_device_text",
										"type":"text",
										"x":0,"y":0,
										"all_align":"center",
										"text":"-",
										"outline":1,
										"fontname":"Tahoma:12",
										},
									),
								},
								{
									"name":"vc_spk_dev_label",
									"type":"text",
									"style":("not_pick",),
									"x":LINE_LABEL_X,"y":LINE_LABEL_Y+LINE_STEP*5+12,
									"text":uiScriptLocale.VOICE_CHAT_SPK_DEVICE,
								},
								{
									"name":"vc_spk_device",
									"type":"button",
									"x":LINE_LABEL_X+MIDDLE_BUTTON_WIDTH*2.4,"y":LINE_LABEL_Y+LINE_STEP*5+10,
									"default_image":ROOT_PATH + "Middle_Button_01.sub",
									"over_image":ROOT_PATH + "Middle_Button_02.sub",
									"down_image":ROOT_PATH + "Middle_Button_03.sub",
									"children":
									(
										{
										"name":"vc_spk_device_text",
										"type":"text",
										"x":0,"y":0,
										"all_align":"center",
										"text":"-",
										"outline":1,
										"fontname":"Tahoma:12",
										},
									),
								},
								{
									"name":"rectangle",
									"type":"image",
									"style":("not_pick",),
									"x":LINE_LABEL_X-20,"y":LINE_LABEL_Y+LINE_STEP*6+8,
									"style":("not_pick",),
									"image":NEW_PATH+"rectangle.png",
								},
								{
									"name":"vc_mic_vol_label",
									"type":"text",
									"style":("not_pick",),
									"x":LINE_LABEL_X,"y":LINE_LABEL_Y+LINE_STEP*6+18,
									"text":uiScriptLocale.VOICE_CHAT_MIC_VOLUME,
								},
								{
									"name":"vc_mic_volume",
									"type":"sliderbarNew",
									"x":LINE_LABEL_X+MIDDLE_BUTTON_WIDTH*2.4,"y":LINE_LABEL_Y+LINE_STEP*6+21,
								},
								{
									"name":"vc_hear_vol_label",
									"type":"text",
									"style":("not_pick",),
									"x":LINE_LABEL_X,"y":LINE_LABEL_Y+LINE_STEP*7+18,
									"text":uiScriptLocale.VOICE_CHAT_HEAR_VOLUME,
								},
								{
									"name":"vc_hear_volume",
									"type":"sliderbarNew",
									"x":LINE_LABEL_X+MIDDLE_BUTTON_WIDTH*2.4,"y":LINE_LABEL_Y+LINE_STEP*7+21,
								},
								{
									"name":"rectangle",
									"type":"image",
									"style":("not_pick",),
									"x":LINE_LABEL_X-20,"y":LINE_LABEL_Y+LINE_STEP*8+16,
									"style":("not_pick",),
									"image":NEW_PATH+"rectangle.png",
								},
								{
									"name":"vc_enable_label",
									"type":"text",
									"style":("not_pick",),
									"x":LINE_LABEL_X,"y":LINE_LABEL_Y+LINE_STEP*8+26,
									"text":uiScriptLocale.VOICE_CHAT_ENABLE,
								},
								{
									"name":"vc_enable_on",
									"type":"radio_button",
									"x":LINE_LABEL_X+MIDDLE_BUTTON_WIDTH*1.9,"y":LINE_LABEL_Y+LINE_STEP*8+24,
									"default_image":ROOT_PATH + "Middle_Button_01.sub",
									"over_image":ROOT_PATH + "Middle_Button_02.sub",
									"down_image":ROOT_PATH + "Middle_Button_03.sub",
									"children":
									(
										{
										"name":"vc_enable_on_text",
										"type":"text",
										"x":0,"y":0,
										"all_align":"center",
										"text":uiScriptLocale.VOICE_CHAT_ON,
										"outline":1,
										"fontname":"Tahoma:12",
										},
									),
								},
								{
									"name":"vc_enable_off",
									"type":"radio_button",
									"x":LINE_LABEL_X+MIDDLE_BUTTON_WIDTH*3,"y":LINE_LABEL_Y+LINE_STEP*8+24,
									"default_image":ROOT_PATH + "Middle_Button_01.sub",
									"over_image":ROOT_PATH + "Middle_Button_02.sub",
									"down_image":ROOT_PATH + "Middle_Button_03.sub",
									"children":
									(
										{
										"name":"vc_enable_off_text",
										"type":"text",
										"x":0,"y":0,
										"all_align":"center",
										"text":uiScriptLocale.VOICE_CHAT_OFF,
										"outline":1,
										"fontname":"Tahoma:12",
										},
									),
								},
								{
									"name":"rectangle",
									"type":"image",
									"style":("not_pick",),
									"x":LINE_LABEL_X-20,"y":LINE_LABEL_Y+LINE_STEP*9+22,
									"style":("not_pick",),
									"image":NEW_PATH+"rectangle.png",
								},
								{
									"name":"vc_ptt_key_label",
									"type":"text",
									"style":("not_pick",),
									"x":LINE_LABEL_X,"y":LINE_LABEL_Y+LINE_STEP*9+32,
									"text":uiScriptLocale.VOICE_CHAT_PTT_KEY_LABEL,
								},
								{
									"name":"vc_ptt_key",
									"type":"button",
									"x":LINE_LABEL_X+MIDDLE_BUTTON_WIDTH*2.4,"y":LINE_LABEL_Y+LINE_STEP*9+30,
									"default_image":ROOT_PATH + "Middle_Button_01.sub",
									"over_image":ROOT_PATH + "Middle_Button_02.sub",
									"down_image":ROOT_PATH + "Middle_Button_03.sub",
									"children":
									(
										{
										"name":"vc_ptt_key_text",
										"type":"text",
										"x":0,"y":0,
										"all_align":"center",
										"text":"Y",
										"outline":1,
										"fontname":"Tahoma:12",
										},
									),
								},
								{
									"name":"rectangle",
									"type":"image",
									"style":("not_pick",),
									"x":LINE_LABEL_X-20,"y":LINE_LABEL_Y+LINE_STEP*10+28,
									"style":("not_pick",),
									"image":NEW_PATH+"rectangle.png",
								},
								{
									"name":"vc_chat_type_label",
									"type":"text",
									"style":("not_pick",),
									"x":LINE_LABEL_X,"y":LINE_LABEL_Y+LINE_STEP*10+38,
									"text":uiScriptLocale.VOICE_CHAT_CHANNEL,
								},
								{
									"name":"vc_type_local",
									"type":"radio_button",
									"x":LINE_LABEL_X+MIDDLE_BUTTON_WIDTH*1.4,"y":LINE_LABEL_Y+LINE_STEP*10+36,
									"default_image":ROOT_PATH + "Middle_Button_01.sub",
									"over_image":ROOT_PATH + "Middle_Button_02.sub",
									"down_image":ROOT_PATH + "Middle_Button_03.sub",
									"children":
									(
										{
										"name":"vc_type_local_text",
										"type":"text",
										"x":0,"y":0,
										"all_align":"center",
										"text":uiScriptLocale.VOICE_CHAT_LOCAL,
										"outline":1,
										"fontname":"Tahoma:12",
										},
									),
								},
								{
									"name":"vc_type_party",
									"type":"radio_button",
									"x":LINE_LABEL_X+MIDDLE_BUTTON_WIDTH*2.4,"y":LINE_LABEL_Y+LINE_STEP*10+36,
									"default_image":ROOT_PATH + "Middle_Button_01.sub",
									"over_image":ROOT_PATH + "Middle_Button_02.sub",
									"down_image":ROOT_PATH + "Middle_Button_03.sub",
									"children":
									(
										{
										"name":"vc_type_party_text",
										"type":"text",
										"x":0,"y":0,
										"all_align":"center",
										"text":uiScriptLocale.VOICE_CHAT_PARTY,
										"outline":1,
										"fontname":"Tahoma:12",
										},
									),
								},
								{
									"name":"vc_type_guild",
									"type":"radio_button",
									"x":LINE_LABEL_X+MIDDLE_BUTTON_WIDTH*3.4,"y":LINE_LABEL_Y+LINE_STEP*10+36,
									"default_image":ROOT_PATH + "Middle_Button_01.sub",
									"over_image":ROOT_PATH + "Middle_Button_02.sub",
									"down_image":ROOT_PATH + "Middle_Button_03.sub",
									"children":
									(
										{
										"name":"vc_type_guild_text",
										"type":"text",
										"x":0,"y":0,
										"all_align":"center",
										"text":uiScriptLocale.VOICE_CHAT_GUILD,
										"outline":1,
										"fontname":"Tahoma:12",
										},
									),
								},
							)
						},
					)
				},
			],
		},
		{
			"name" : "Window_Board",
			"type" : "window",
			"x": 10, "y": 25,
			"width":160,"height":THINBOARD_HEIGHT,
			"children" :
			(
				{
					"name":"thinboard0",
					"type":"thinboard_circle",
					"x":0,"y":5,
					"width" : 160,
					"height" : THINBOARD_HEIGHT,
					"children":
					(
						{
							"name":"bg",
							"type" : "thinboard",
							"x":1,"y":1,
							"width" : 158, "height" : BG_HEIGHT,
							"children":
							(
								{
									"name":"category_btn1",
									"type":"radio_button",
									"x":-1,"y":15,
									"horizontal_align":"center",
									"default_image":"d:/ymir work/ui/weekly_rank/button-example-020.png",
									"over_image":"d:/ymir work/ui/weekly_rank/button-example-021.png",
									"down_image":"d:/ymir work/ui/weekly_rank/button-example-022.png",
									"children":
									(
										{
											"name":"category_txt",
											"type":"text",
											"x":0,"y":0,
											"all_align":"center",
											"text": uiScriptLocale.GAME_OPTIONS_MAIN_CATEGORY,
											"outline":1,
											"fontname":"Tahoma:14",
										},
									),
								},
                                {
									"name":"category_btn2",
									"type":"radio_button",
									"x":-1,"y":40,
									"horizontal_align":"center",
									"default_image":"d:/ymir work/ui/weekly_rank/button-example-020.png",
									"over_image":"d:/ymir work/ui/weekly_rank/button-example-021.png",
									"down_image":"d:/ymir work/ui/weekly_rank/button-example-022.png",
									"children":
									(
										{
											"name":"category_txt",
											"type":"text",
											"x":0,"y":0,
											"all_align":"center",
											"text": uiScriptLocale.GAME_OPTIONS_SYSTEM_CATEGORY,
											"outline":1,
											"fontname":"Tahoma:14",
										},
									),
								},
								{
									"name":"category_btn3",
									"type":"radio_button",
									"x":-1,"y":65,
									"horizontal_align":"center",
									"default_image":"d:/ymir work/ui/weekly_rank/button-example-020.png",
									"over_image":"d:/ymir work/ui/weekly_rank/button-example-021.png",
									"down_image":"d:/ymir work/ui/weekly_rank/button-example-022.png",
									"children":
									(
										{
											"name":"category_txt",
											"type":"text",
											"x":0,"y":0,
											"all_align":"center",
											"text": uiScriptLocale.GAME_OPTIONS_DESCRIPTIONS_CATEGORY,
											"outline":1,
											"fontname":"Tahoma:14",
										},
									),
								},
								{
									"name":"category_btn4",
									"type":"radio_button",
									"x":-1,"y":90,
									"horizontal_align":"center",
									"default_image":"d:/ymir work/ui/weekly_rank/button-example-020.png",
									"over_image":"d:/ymir work/ui/weekly_rank/button-example-021.png",
									"down_image":"d:/ymir work/ui/weekly_rank/button-example-022.png",
									"children":
									(
										{
											"name":"category_txt",
											"type":"text",
											"x":0,"y":0,
											"all_align":"center",
											"text": uiScriptLocale.GAME_OPTIONS_HIDING_CATEGORY,
											"outline":1,
											"fontname":"Tahoma:14",
										},
									),
								},
								{
									"name":"category_btn5",
									"type":"radio_button",
									"x":-1,"y":115,
									"horizontal_align":"center",
									"default_image":"d:/ymir work/ui/weekly_rank/button-example-020.png",
									"over_image":"d:/ymir work/ui/weekly_rank/button-example-021.png",
									"down_image":"d:/ymir work/ui/weekly_rank/button-example-022.png",
									"children":
									(
										{
										"name":"category_txt",
										"type":"text",
										"x":0,"y":0,
										"all_align":"center",
										"text": uiScriptLocale.GAME_OPTIONS_VOICE_CHAT_CATEGORY,
										"outline":1,
										"fontname":"Tahoma:14",
										},
									),
								},
							),
						},
					),
				},
			),
		},
	],
}
