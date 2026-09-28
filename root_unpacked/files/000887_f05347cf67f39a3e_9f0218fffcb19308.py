import uiScriptLocale

BATTLE_PASS_UI_PATH = "d:/ymir work/ui/game/battle_pass/"
DUNGEON_INFO_UI_PATH = "d:/ymir work/ui/game/dungeon_info/"

BAR_COLOUR = 0x2f000000
BAR_BREADTH = 14

window = {
	"name" : "DungeonInfo",

	"x" : 0,
	"y" : 0,
	
	"style" : ("movable", "float",),

	"width" : 890,
	"height" : 320,

	"children" :
	(
		{
			"name" : "A_DungeonDropSlideBar",
			"type" : "board",

			"x" : 550 + 78,
			"y" : 290,

			"width" : 155,
			"height" : 64,

			"children" :
			(
				{
					"name" : "DungeonInfo_SlidebarText",
					"type" : "text",

					"x" : 0,
					"y" : 35,

					"horizontal_align" : "center",
					"text_horizontal_align" : "center",

					"text" : uiScriptLocale.DUNGEON_BOSS_DROP,
				},
			),
		},
		{
			"name" : "board",
			"type" : "board_with_titlebar",
			"style" : ("attach",),

			"x" : 0,
			"y" : 0,

			"width" : 890,
			"height" : 320,
			
			"title" : uiScriptLocale.DUNGEON_INFO_MAIN_TITLE,

			"children" :
			(
				{
					"name" : "DungeonList_Board",
					"type" : "border_a",

					"x" : 10,
					"y" : 50,

					"width" : 307,
					"height" : 260,

					"children" :
					(
						{
							"name" : "DungeonList_Window",
							"type" : "listboxex",

							"x" : 3,
							"y" : 3,

							"width" : 307-6,
							"height" : 250-6,
						},
						{
							"name" : "DungeonListScroll_Window",
							"type" : "scrollbar",

							"x" : 301-6,
							"y" : 0,

							"vertical_align" : "center",

							"size" : 250-6,
						},
					),
				},
				{
					"name" : "BasicInfo_Window",
					"type" : "thinboard",

					"x" : 307 + 10 + 10,
					"y" : 30,

					"width" : 207,
					"height" : 280,

					"children" :
					(
						{
							"name" : "BackGround",
							"type" : "image",

							"x" : 0,
							"y" : 0,

							"image" : DUNGEON_INFO_UI_PATH + "background_ani/0.tga",
						},
						
						{
							"name" : "DungeonDetails_InformationLabel",
							"type" : "expanded_image",

							"x" : 0,
							"y" : 0,

							"horizontal_align" : "center",

							"image" : BATTLE_PASS_UI_PATH + "title_bar_special.tga",
							"children" :
							(
								{
									"name" : "DungeonDetails_InformationText",
									"type" : "text",

									"x" : 0,
									"y" : 0,

									"all_align" : "center",
									"text" : uiScriptLocale.DUNGEON_INFO_MAIN_DETAILS,
								},
							),
						},
						{
							"name" : "DungeonDetails_TypeBar",
							"type" : "bar",

							"x" : 10,
							"y" : 30,

							"width" : 207-30,
							"height" : BAR_BREADTH,

							"color" : BAR_COLOUR,

							"children" :
							(
								{
									"name" : "DungeonDetails_TypeText",
									"type" : "text",

									"x" : 2,
									"y" : 0,

									"text" : uiScriptLocale.DUNGEON_INFO_MAIN_TYPE,
								},
							),
						},
						{
							"name" : "DungeonDetails_ApplyBar",
							"type" : "bar",

							"x" : 10,
							"y" : 30 + (BAR_BREADTH + 10),

							"width" : 207-30,
							"height" : BAR_BREADTH,

							"color" : BAR_COLOUR,

							"children" :
							(
								{
									"name" : "DungeonDetails_ApplyText",
									"type" : "text",

									"x" : 2,
									"y" : 0,

									"text" : uiScriptLocale.DUNGEON_INFO_MAIN_APPLY_TEXT,
								},
							),
						},
						{
							"name" : "DungeonDetails_LevelLimitBar",
							"type" : "bar",

							"x" : 10,
							"y" : 30 + (BAR_BREADTH + 10)*2,

							"width" : 207-30,
							"height" : BAR_BREADTH,

							"color" : BAR_COLOUR,

							"children" :
							(
								{
									"name" : "DungeonDetails_LevelLimitText",
									"type" : "text",

									"x" : 2,
									"y" : 0,

									"text" : uiScriptLocale.DUNGEON_INFO_MAIN_LEVEL_LIMIT,
								},
							),
						},
						{
							"name" : "DungeonDetails_CooldownBar",
							"type" : "bar",

							"x" : 10,
							"y" : 30 + (BAR_BREADTH + 10)*3,

							"width" : 207-30,
							"height" : BAR_BREADTH,

							"color" : BAR_COLOUR,

							"children" :
							(
								{
									"name" : "DungeonDetails_CooldownText",
									"type" : "text",

									"x" : 2,
									"y" : 0,

									"text" : uiScriptLocale.DUNGEON_INFO_MAIN_COOLDOWN,
								},
							),
						},
						{
							"name" : "DungeonDetails_PassItemBar",
							"type" : "bar",

							"x" : 10,
							"y" : 30 + (BAR_BREADTH + 10)*4,

							"width" : 207-30,
							"height" : BAR_BREADTH,

							"color" : BAR_COLOUR,

							"children" :
							(
								{
									"name" : "DungeonDetails_PassItemText",
									"style" : ("not_pick", ),
									"type" : "text",

									"x" : 2,
									"y" : 0,

									"text" : uiScriptLocale.DUNGEON_INFO_MAIN_PASS_ITEM,
								},
							),
						},
						{
							"name" : "DungeonDetails_CompletionCountBar",
							"type" : "bar",

							"x" : 10,
							"y" : 30 + (BAR_BREADTH + 10)*5,

							"width" : 207-30,
							"height" : BAR_BREADTH,

							"color" : BAR_COLOUR,

							"children" :
							(
								{
									"name" : "DungeonDetails_CompletionCountText",
									"type" : "text",

									"x" : 2,
									"y" : 0,

									"text" : uiScriptLocale.DUNGEON_INFO_MAIN_COMPLETION_COUNT,
								},
							),
						},
						{
							"name" : "DungeonDetails_FastestCompletionBar",
							"type" : "bar",

							"x" : 10,
							"y" : 30 + (BAR_BREADTH + 10)*6,

							"width" : 207-30,
							"height" : BAR_BREADTH,

							"color" : BAR_COLOUR,

							"children" :
							(
								{
									"name" : "DungeonDetails_FastestCompletionText",
									"type" : "text",

									"x" : 2,
									"y" : 0,

									"text" : uiScriptLocale.DUNGEON_INFO_MAIN_FASTEST_COMPLETION,
								},
							),
						},
						{
							"name" : "DungeonDetails_GreatestDamageBar",
							"type" : "bar",

							"x" : 10,
							"y" : 30 + (BAR_BREADTH + 10)*7,

							"width" : 207-30,
							"height" : BAR_BREADTH,

							"color" : BAR_COLOUR,

							"children" :
							(
								{
									"name" : "DungeonDetails_GreatestDamageText",
									"type" : "text",

									"x" : 2,
									"y" : 0,

									"text" : uiScriptLocale.DUNGEON_INFO_MAIN_GREATEST_DAMAGE,
								},
							),
						},
						{
							"name" : "DungeonDetails_HorizontalBar",
							"type" : "bar",

							"x" : 10,
							"y" : 30 + (BAR_BREADTH + 10)*8,

							"width" : 207-30,
							"height" : 1,

							"color" : 0x5fFFFFFF,
						},
						{
							"name" : "DungeonDetails_CompletionCountButton",
							"type" : "button",

							"x" : 6,
							"y" : 40 + (BAR_BREADTH + 10)*8,

							"default_image" : "d:/ymir work/ui/game/guild/extra/king_button00.sub",
							"over_image" : "d:/ymir work/ui/game/guild/extra/king_button01.sub",
							"down_image" : "d:/ymir work/ui/game/guild/extra/king_button02.sub",

							"tooltip_text" : uiScriptLocale.DUNGEON_INFO_MAIN_COMPLETION_COUNT_BUTTON,
						},
						{
							"name" : "DungeonDetails_FastestCompletionButton",
							"type" : "button",

							"x" : 73,
							"y" : 40 + (BAR_BREADTH + 10)*8,

							"default_image" : "d:/ymir work/ui/game/guild/extra/time_button00.sub",
							"over_image" : "d:/ymir work/ui/game/guild/extra/time_button01.sub",
							"down_image" : "d:/ymir work/ui/game/guild/extra/time_button02.sub",

							"tooltip_text" : uiScriptLocale.DUNGEON_INFO_MAIN_FASTEST_COMPLETION_BUTTON,
						},
						{
							"name" : "DungeonDetails_GreatestDamageButton",
							"type" : "button",

							"x" : 140,
							"y" : 40 + (BAR_BREADTH + 10)*8,

							"default_image" : "d:/ymir work/ui/game/guild/extra/tiger_button00.sub",
							"over_image" : "d:/ymir work/ui/game/guild/extra/tiger_button01.sub",
							"down_image" : "d:/ymir work/ui/game/guild/extra/tiger_button02.sub",

							"tooltip_text" : uiScriptLocale.DUNGEON_INFO_MAIN_GREATEST_DAMAGE_BUTTON,
						},
						{
							"name" : "DungeonDetails_JoinButton",
							"type" : "button",

							"x" : -50,
							"y" : 40 + (BAR_BREADTH + 10)*8 + 23,

							"horizontal_align" : "center",

							"default_image" : "d:/ymir work/ui/public/Large_Button_01.sub",
							"over_image" : "d:/ymir work/ui/public/Large_Button_02.sub",
							"down_image" : "d:/ymir work/ui/public/Large_Button_03.sub",

							"text" : uiScriptLocale.DUNGEON_INFO_MAIN_JOIN_BUTTON,
						},
						{
							"name" : "DungeonDetails_ReJoinButton",
							"type" : "button",

							"x" : 50,
							"y" : 40 + (BAR_BREADTH + 10)*8 + 23,

							"horizontal_align" : "center",

							"default_image" : "d:/ymir work/ui/public/Large_Button_01.sub",
							"over_image" : "d:/ymir work/ui/public/Large_Button_02.sub",
							"down_image" : "d:/ymir work/ui/public/Large_Button_03.sub",

							"text" : uiScriptLocale.DUNGEON_INFO_MAIN_REJOIN_BUTTON,
						},
					),
				},
				{
					"name" : "DungeonDropDialog",
					"type" : "window",

					"x" : 550,
					"y" : 30,

					"width" : 310,
					"height" : 280,
				},
			),
		},
	),
}