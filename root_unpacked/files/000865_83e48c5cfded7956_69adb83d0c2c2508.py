import uiScriptLocale

window = {
	"name" : "CardsLottery",

	"x" : SCREEN_WIDTH/2 - 290,
	"y" : SCREEN_HEIGHT/2 - 250,

	"style" : ("float",),

	"width" : 600,
	"height" : 450,

	"children" :
	(

		{
			"name" : "board",
			"type" : "expanded_image",
			"style" : ("attach",),

			"x" : 120,
			"y" : 0,

			"image" : "kowal/dungeon_cards/cards_background.png",
		},
		{
			"name" : "CloseButton",
			"type" : "button",
        
			"x" : 500,
			"y" : 10,
        
			"text" : "",
        
			"default_image" : "kowal/dungeon_cards/close_1.tga",
			"over_image" : "kowal/dungeon_cards/close_2.tga",
			"down_image" : "kowal/dungeon_cards/close_3.tga",
		},
	),
}
