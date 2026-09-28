import uiScriptLocale

BOARD_WIDTH = 400
BOARD_HEIGHT = 344
BACK_IMG_PATH = "d:/ymir work/ui/public/public_board_back/"
ROOT_PATH = "d:/ymir work/ui/game/guild/dragonlairranking/"

window = {
	"name" : "DungeonRankingWindow",
	"style" : ("movable", "float",),

	"x" : 0,
	"y" : 0,

	"width" : BOARD_WIDTH,
	"height" : BOARD_HEIGHT,

	"children" :
	(
		{
			"name" : "Board",
			"type" : "board",
			"style" : ("attach",),

			"x" : 0,
			"y" : 0,

			"width" : BOARD_WIDTH,
			"height" : BOARD_HEIGHT,

			"children" :
			(
				{
					"name" : "TitleBar",
					"type" : "titlebar",
					"style" : ("attach",),

					"x" : 6,
					"y" : 6,

					"width" : BOARD_WIDTH - 13,

					"children" :
					(
						{
							"name" : "TitleBarName",
							"type" : "text",

							"x" : 0,
							"y" : -3,

							"text" : uiScriptLocale.DUNGEON_RANKING,
                            "outline":"1",
							"all_align" : "center"
						},
					),
				},
				{
					"name" : "border_a",
					"type" : "border_a",
					"width": 375,
					"height" : 268,
					"x":0,"y":30,
					"horizontal_align":"center",
					"children":
					(
						{
							"name" : "RankingTiTleImg",
							"type" : "image",
							"x" : 1,
							"y" : 3,
							"horizontal_align":"center",
							"image" : "d:/ymir work/ui/ranking_header.png",
						},
					)
				},
				{
					"name" : "border_a1",
					"type" : "border_a",
					"width": 375,
					"height" : 20,
					"x":0,"y":300, 
					"horizontal_align":"center",
				},
				{
					"name" : "WaitAniImg",
					"type" : "ani_image",

					"x" : 0,
					"y" : 40,
					"width" : 32,
					"height" : 128,
					"horizontal_align" : "center",
					"vertical_align" : "center",

					"delay" : 6,

					"images" :
					(
						"d:/ymir work/ui/game/" + "TaskBar/Rampage_01/00.sub",
						"d:/ymir work/ui/game/" + "TaskBar/Rampage_01/01.sub",
						"d:/ymir work/ui/game/" + "TaskBar/Rampage_01/02.sub",
						"d:/ymir work/ui/game/" + "TaskBar/Rampage_01/03.sub",
						"d:/ymir work/ui/game/" + "TaskBar/Rampage_01/04.sub",
						"d:/ymir work/ui/game/" + "TaskBar/Rampage_01/05.sub",
						"d:/ymir work/ui/game/" + "TaskBar/Rampage_01/06.sub",
						"d:/ymir work/ui/game/" + "TaskBar/Rampage_01/07.sub",
						"d:/ymir work/ui/game/" + "TaskBar/Rampage_01/08.sub",
						"d:/ymir work/ui/game/" + "TaskBar/Rampage_01/09.sub",
						"d:/ymir work/ui/game/" + "TaskBar/Rampage_01/11.sub",
						"d:/ymir work/ui/game/" + "TaskBar/Rampage_01/12.sub",
						"d:/ymir work/ui/game/" + "TaskBar/Rampage_01/13.sub",
						"d:/ymir work/ui/game/" + "TaskBar/Rampage_01/14.sub",
						"d:/ymir work/ui/game/" + "TaskBar/Rampage_01/15.sub",
						"d:/ymir work/ui/game/" + "TaskBar/Rampage_01/16.sub",
					),

					"children" :
					(
						{
							"name" : "WaitTextLine",
							"type" : "text",

							"x" : 2,
							"y" : -15,

							"text" : "...",
							"all_align" : "center"
						},
					)
				},
			),
		},
	),
}
