import uiScriptLocale

WINDOW_X = 582
WINDOW_Y = 340

PATH = "kowal/chest_preview/"

window = {

	"name" : "CasketWindow",

	"x" : (SCREEN_WIDTH-WINDOW_X)/2,
	"y" : (SCREEN_HEIGHT-WINDOW_Y)/2,

	"style" : ("movable", "float"),

	"width" : WINDOW_X,
	"height" : WINDOW_Y,

	"children" :
	(
		{
			"name" : "Board",
			"type" : "board",
			"style" : ("attach",),

			"x" : 0,
			"y" : 0,

			"width" : WINDOW_X,
			"height" : WINDOW_Y,

			"children" :
			(
				{
					"name" : "TitleBar",
					"type" : "titlebar",
					"style" : ("attach",),

					"x" : 8,
					"y" : 7,

					"width" : WINDOW_X-15,
					"color" : "yellow",

					"children" :
					(
						{ "name":"TitleName", "type":"text", "x":0, "y":3, "text": uiScriptLocale.CHEST_PREVIEW_TITLE, "text_horizontal_align":"center", "horizontal_align" : "center", "outline" : 1 },
					),
				},
				
				{
					"name" : "ItemSlot",
					"type" : "slot",
					"x" : 145,
					"y" : 70,
					"width" : 32,
					"height" : 32,
					
					"image" : "d:/ymir work/ui/public/slot_base.sub",
					"slot" : 
					( 
						{ "index" : 0, "x" : 0, "y" : 0, "width" : 32, "height" : 32}, 
					),
				},
				
				{
					"name" : "ItemArrow",
					"type" : "image",
					"x" : 0,
					"y" : 180,
					"horizontal_align" : "center",
					"image" : PATH+"arrow.tga",
				},
				
				
				{
					"name" : "Information",
					"type" : "text",
					"x" : 8,
					"y" : 185,
					
					"text": uiScriptLocale.CHEST_PREVIEW_CONTAINS_ITEM_TEXT,
					"outline" : 1,
				},
				
				{
					"name" : "NextButton",
					"type" : "button",

					"x" : 582-24,
					"y" : 199,

					"text" : "",

					"default_image" : PATH+"chest_button_right01.tga",
					"over_image" : PATH+"chest_button_right02.tga",
					"down_image" : PATH+"chest_button_right01.tga",
				},
				
				{
					"name" : "PrevButton",
					"type" : "button",

					"x" : 8,
					"y" : 199,

					"text" : "",

					"default_image" : PATH+"chest_button_left01.tga",
					"over_image" : PATH+"chest_button_left02.tga",
					"down_image" : PATH+"chest_button_left01.tga",
				},
			),
		},
	),
}