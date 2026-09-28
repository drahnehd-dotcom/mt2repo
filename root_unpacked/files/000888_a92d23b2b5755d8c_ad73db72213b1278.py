import uiScriptLocale

WINDOW_WIDTH	= 366
WINDOW_HEIGHT	= 285

window = {
	"name" : "DungeonInfo_Ranking",
	"style" : ("movable", "float",),
	
	"x" : 0,
	"y" : 0,
	
	"width" : WINDOW_WIDTH,
	"height" : WINDOW_HEIGHT,
	
	"children" :
	(
		{
			"name" : "board",
			"type" : "board_with_titlebar",
			"style" : ("attach",),

			"x" : 0,
			"y" : 0,

			"width" : WINDOW_WIDTH,
			"height" : WINDOW_HEIGHT,

			"title" : uiScriptLocale.DUNGEON_INFO_RANKING_TITLE,

			"children" :
			(
				{
					"name" : "ListBoard",
					"type" : "border_a",
					
					"style" : ("attach",),

					"x" : 18,
					"y" : 38,
					
					"width" : 317,
					"height" : 230,
					
					"children" :
					(
						{
							"name" : "Ranking_Header",
							"type" : "image",
							
							"x" : 3, "y" : 3,
							"image" : "d:/ymir work/ui/game/guild/dragonlairranking/ranking_list_menu.sub",
							
							"children" :
							(
								{ "name" : "Header_Rank", "type" : "text", "x" : 25, "y" : 4, "text" : uiScriptLocale.DUNGEON_INFO_RANKING_HEADER_RANK, "text_horizontal_align" : "center", },
								{ "name" : "Header_Name", "type" : "text", "x" : 114, "y" : 4, "text" : uiScriptLocale.DUNGEON_INFO_RANKING_HEADER_NAME, "text_horizontal_align" : "center", },
								{ "name" : "Header_Level", "type" : "text", "x" : 205, "y" : 4, "text" : uiScriptLocale.DUNGEON_INFO_RANKING_HEADER_LEVEL, "text_horizontal_align" : "center", },
								{ "name" : "Header_Score", "type" : "text", "x" : 271, "y" : 4, "text" : uiScriptLocale.DUNGEON_INFO_RANKING_HEADER_SCORE, "text_horizontal_align" : "center", },
							),
						},
						
						{
							"name" : "ListClipper",
							"type" : "listboxex",
							
							"x" : 0,
							"y" : 26,
							
							"width" : 317,
							"height" : 202,
						},
					),
				},
				
				{
					"name" : "ListScrollBar",
					"type" : "scrollbar",

					"x" : 27,
					"y" : 38,
					"size" : 235,
					
					"horizontal_align" : "right",
				},
			),
		},
	),	
}
