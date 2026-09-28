import uiScriptLocale
import player

ROOT_PATH = "kowal/secondary_level/"

MARGIN_X = 10+7
MARGIN_Y = 10

MAIN_WIDTH = 520
MAIN_HEIGHT = 440

WINDOW_WIDTH = MAIN_WIDTH + MARGIN_X * 2
WINDOW_HEIGHT = MAIN_HEIGHT + MARGIN_Y * 2 + 40

window = {
	"name" : "SecondaryLevelWindow",
	"style": ("movable", "float",),

	"x" : SCREEN_WIDTH / 2 - WINDOW_WIDTH / 2,
	"y" : SCREEN_HEIGHT / 2 - WINDOW_HEIGHT / 2,

	"width" : WINDOW_WIDTH-5,
	"height" : WINDOW_HEIGHT,

	"children" :
	(
		{
			"name" : "board",
			"type" : "board_with_titlebar",

			"style": ("attach",),

			"x" : 0,
			"y" : 0,

			"width" : WINDOW_WIDTH-5,
			"height" : WINDOW_HEIGHT,

			"title" : uiScriptLocale.SECONDARY_LEVEL_TITLE,

			"children" :
			(
				{
					"name": "main_bg_window",
					"type": "window",

					"style": ("attach",),

					"x": MARGIN_X,
					"y": 30,

					"width": MAIN_WIDTH-5,
					"height": MAIN_HEIGHT,

					"children":
					(
						{
							"type" : "window",
							"style": ("attach",),

							"x": 0,
							"y": 0,

							"width": 257,
							"height": MAIN_HEIGHT,
							
							"children" :
							(
								{
									"type" : "expanded_image",
									"x" : 1, "y" : 6,
									
									"image" : ROOT_PATH + "rank_actual.png",
									
									"children" :
									(
										{
											"name" : "actual_rank",
											"type" : "expanded_image",
											"x" : 33, "y" : 72,
											
											"image" : ROOT_PATH + "level_icons/0.tga",
										},
										{
											"name" : "actual_rank_text_placeholder",
											"type" : "text",
											"x" : 130, "y" : 19,
											"fontname": "Verdana:14b",
											"outline": 1,
											"text_horizontal_align" : "center",
											
											"text" : uiScriptLocale.SECONDARY_LEVEL_CURRENT,
										},
										{
											"name" : "actual_rank_text",
											"type" : "text",
											"x" : 85, "y" : 74,
											"fontname": "Verdana:12b",
											"outline": 1,
											
											"text" : uiScriptLocale.SECONDARY_LEVEL_NONE,
										},
									),
								},
								{
									"name" : "actual_bonus_list",
									"type" : "expanded_image",
									"x" : 3, "y" : 119,
									
									"image" : ROOT_PATH + "bonus_list.png",
								},
								{
									"name" : "current_level_bonuses",
									"type" : "text",
									"x" : 128, "y" : 136,
									"fontname": "Verdana:14b",
									"outline": 1,
									"text_horizontal_align" : "center",
									
									"text" : uiScriptLocale.SECONDARY_LEVEL_CURRENT_BONUSES,
								},
								{
									"type" : "expanded_image",
									"x" : 3, "y" : 279,
									
									"image" : ROOT_PATH + "required_items.png",
									
									"children" :
									(
										{
											"name" : "required_items",
											"type" : "text",
											"x" : 128, "y" : 17,
											"fontname": "Verdana:14b",
											"outline": 1,
											"text_horizontal_align" : "center",
											
											"text" : uiScriptLocale.SECONDARY_LEVEL_REQUIRED_ITEMS,
										},
										{
											"name" : "ItemSlot",
											"type" : "grid_table",

											"x" : 31,
											"y" : 57,

											"start_index" : 0,
											"x_count" : 6,
											"y_count" : 3,
											"x_step" : 32,
											"y_step" : 32,

											"image" : "d:/ymir work/ui/public/Slot_Base.sub"
										},
									),
								},
							),
						},
						{
							# Prawa kolumna = CALA sekcja awansu (nastepna ranga, jej bonusy,
							# szanse, koszty, przyciski). Nazwa dodana, zeby dalo sie ja ukryc
							# jednym Hide() na maksymalnym poziomie - patrz uisecondarylevel.py.
							"name" : "next_level_section",
							"type" : "window",
							"style": ("attach",),

							"x": 0+257,
							"y": 0,

							"width": 257,
							"height": MAIN_HEIGHT,
							
							"children" :
							(
								{
									"type" : "expanded_image",
									"x" : 0, "y" : 6,
									
									"image" : ROOT_PATH + "rank_next.png",
									
									"children" :
									(
										{
											"name" : "next_rank",
											"type" : "expanded_image",
											"x" : 33, "y" : 72,
											
											"image" : ROOT_PATH + "level_icons/0.tga",
										},
										{
											"name" : "next_rank_text_placeholder",
											"type" : "text",
											"x" : 130, "y" : 19,
											"fontname": "Verdana:14b",
											"outline": 1,
											"text_horizontal_align" : "center",
											
											"text" : uiScriptLocale.SECONDARY_LEVEL_NEXT,
										},
										{
											"name" : "next_rank_text",
											"type" : "text",
											"x" : 85, "y" : 74,
											"fontname": "Verdana:12b",
											"outline": 1,
											
											"text" : uiScriptLocale.SECONDARY_LEVEL_NONE,
										},
									),
								},
								{
									"name" : "next_bonus_list",
									"type" : "expanded_image",
									"x" : 3, "y" : 119,
									
									"image" : ROOT_PATH + "bonus_list.png",
								},
								{
									"name" : "next_level_bonuses",
									"type" : "text",
									"x" : 128, "y" : 136,
									"fontname": "Verdana:14b",
									"outline": 1,
									"text_horizontal_align" : "center",
									
									"text" : uiScriptLocale.SECONDARY_LEVEL_NEXT_BONUSES,
								},
								{
									"type" : "expanded_image",
									"x" : 3, "y" : 279,
									
									"image" : ROOT_PATH + "advance_method.png",
									
									"children" :
									(
										{
											"name" : "increasing_level",
											"type" : "text",
											"x" : 128, "y" : 17,
											"fontname": "Verdana:14b",
											"outline": 1,
											"text_horizontal_align" : "center",
											
											"text" : uiScriptLocale.SECONDARY_LEVEL_INCREASE_LEVEL,
										},
										{
											"name" : "increase_luck",
											"type" : "text",
											"x" : 66, "y" : 65,
											"fontname": "Verdana:12b",
											"outline": 1,
											"text_horizontal_align" : "center",
											"color":0xFFd4cfc1,
											
											"text" : uiScriptLocale.SECONDARY_LEVEL_LUCK,
										},
										{
											"name" : "increase_guaranteed",
											"type" : "text",
											"x" : 188, "y" : 65,
											"fontname": "Verdana:12b",
											"outline": 1,
											"text_horizontal_align" : "center",
											"color":0xFFd4cfc1,
											
											"text" : uiScriptLocale.SECONDARY_LEVEL_GUARANTEED,
										},
										{
											"name" : "increase_chance_1",
											"type" : "text",
											"x" : 11, "y" : 87,
											"fontname": "Verdana:12",
											"outline": 1,
											"text_horizontal_align" : "left",
											"color":0xFFd4cfc1,
											
											"text" : uiScriptLocale.SECONDARY_LEVEL_CHANCE,
										},
										{
											"name" : "increase_price_1",
											"type" : "text",
											"x" : 11, "y" : 112,
											"fontname": "Verdana:12",
											"outline": 1,
											"text_horizontal_align" : "left",
											"color":0xFFd4cfc1,
											
											"text" : uiScriptLocale.SECONDARY_LEVEL_REQUIRED_AP,
										},
										{
											"name" : "increase_chance_2",
											"type" : "text",
											"x" : 134, "y" : 87,
											"fontname": "Verdana:12",
											"outline": 1,
											"text_horizontal_align" : "left",
											"color":0xFFd4cfc1,
											
											"text" : uiScriptLocale.SECONDARY_LEVEL_CHANCE,
										},
										{
											"name" : "increase_price_2",
											"type" : "text",
											"x" : 134, "y" : 112,
											"fontname": "Verdana:12",
											"outline": 1,
											"text_horizontal_align" : "left",
											"color":0xFFd4cfc1,
											
											"text" : uiScriptLocale.SECONDARY_LEVEL_REQUIRED_AP,
										},
										{
											"name" : "option1_chance",
											"type" : "text",
											"x" : 70, "y" : 87,
											"color" : 0xff4eff95,
											"outline": 1,
											"text_horizontal_align" : "left",
											"text" : "100%",
										},
										{
											"name" : "option1_cost",
											"type" : "text",
											"x" : 50, "y" : 112,
											"color" : 0xffb6a4fc,
											"outline": 1,
											"text_horizontal_align" : "left",
											"text" : "500.000",
										},
										{
											"name" : "option2_chance",
											"type" : "text",
											"x" : 193, "y" : 87,
											"color" : 0xff4eff95,
											"outline": 1,
											"text_horizontal_align" : "left",
											"text" : "100%",
										},
										{
											"name" : "option2_cost",
											"type" : "text",
											"x" : 173, "y" : 112,
											"color" : 0xffb6a4fc,
											"outline": 1,
											"text_horizontal_align" : "left",
											"text" : "500.000",
										},
										{
											"name" : "option1_button",
											"type" : "button",

											"x" : -61,
											"y" : 135,
											
											"horizontal_align" : "center",

											"default_image" : ROOT_PATH + "btn_select_n.png",
											"over_image" : ROOT_PATH + "btn_select_h.png",
											"down_image" : ROOT_PATH + "btn_select_d.png",
											"children" :
											(
												{
													"name" : "increase_button_text",
													"type" : "text",
													"x" : 50, "y" : 3,
													"fontname": "Verdana:12b",
													"outline": 1,
													"text_horizontal_align" : "center",
													
													"text" : uiScriptLocale.SECONDARY_LEVEL_INCREASE_BUTTON,
												},
											),
										},
										{
											"name" : "option2_button",
											"type" : "button",

											"x" : 61,
											"y" : 135,
											
											"horizontal_align" : "center",

											"default_image" : ROOT_PATH + "btn_select_n.png",
											"over_image" : ROOT_PATH + "btn_select_h.png",
											"down_image" : ROOT_PATH + "btn_select_d.png",
											"children" :
											(
												{
													"name" : "increase_button_text",
													"type" : "text",
													"x" : 50, "y" : 3,
													"fontname": "Verdana:12b",
													"outline": 1,
													"text_horizontal_align" : "center",
													
													"text" : uiScriptLocale.SECONDARY_LEVEL_INCREASE_BUTTON,
												},
											),
										},
									),
								},
							),
						},
					),
				},
			),
		},
	),
}
