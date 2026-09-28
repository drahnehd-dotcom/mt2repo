import uiScriptLocale


SIZE_X = 266
SIZE_Y = 123

WIDTH = (SCREEN_WIDTH/2) - (SIZE_X/2)
HEIGHT = (SCREEN_HEIGHT/2) - (SIZE_Y/2)

window = {
	"name" : "UiGiftCodeWindow",
	"style" : ("movable", "float",),
	
	"x" : WIDTH,
	"y" : HEIGHT,	

	"width" : SIZE_X,
	"height" : SIZE_Y,
	
	"children" :
	(

		{
			"name" : "Board",
			"type" : "board",
			"style" : ("attach",),

			"x" : 0,"y" : 0,
			"width" : SIZE_X,"height" : SIZE_Y,
			
			"children" :
			(
				{
					"name" : "TitleBar",
					"type" : "titlebar",
					"style" : ("attach",),

					"x" : 6, "y" : 7, "width" : SIZE_X - 13,
					
					"children" :
					(
						{ "name" : "TitleName", "type" : "text", "x" : 0, "y" : -4, "text": uiScriptLocale.GIFT_SYSTEM_1, "all_align":"center", "outline":"1", },
					),
				},
			),
		},
		
		{
			"name" : "ExchangeTitleFrame",
			"type" : "image",
				
			"x" : 6,
			"y" : 35,
				
			"image" : "d:/ymir work/gift_code_window/gift_frame.tga",
				
			"children" :
			(
				{
					"name" : "ExchangeTitleFrameText",
					"type" : "text",
					
					"text" : uiScriptLocale.GIFT_SYSTEM_6,
					
					"x" : 0,
					"y" : -1,
					"r" : 1.0,
					"g" : 1.0,
					"b" : 1.0,
					"a" : 1.0,
					"all_align" : "center",
                    "fontname":"Tahoma:14b",
                    "outline":"1",
				},
			),
		},
		{
			"name" : "YourCode",
			"type" : "text",
			
			"x" : 13,
			"y" : 60+5,
			
			"text" : uiScriptLocale.GIFT_SYSTEM_7,
		},
		
		{
			"name" : "CodeFrameSlot",
			"type" : "image",
			
			"x" : 90,
			"y" : 58+5,
			
			"image" : "d:/ymir work/ui/public/Parameter_Slot_04.sub",
			
			"children" :
			(
				{
					"name" : "CodeFrameSlotText",
					"type" : "editline",

					"x" : 4,
					"y" : 2,

					"width" : 100,
					"height" : 17,

					"input_limit" : 10,

					"secret_flag" : 0,
							
					"text" : "",
				},
			),
		},
		
		{
			"name" : "AcceptButton",
			"type" : "button",

			"x" : 70-3,
			"y" : 90,

			"tooltip_text" : uiScriptLocale.GIFT_SYSTEM_2,

			"default_image" : "d:/ymir work/gift_code_window/acceptbutton00.sub",
			"over_image" : "d:/ymir work/gift_code_window/acceptbutton01.sub",
			"down_image" : "d:/ymir work/gift_code_window/acceptbutton02.sub",
		},
		
		{
			"name" : "CancelButton",
			"type" : "button",

			"x" : 70+65-3,
			"y" : 90,

			"tooltip_text" : uiScriptLocale.GIFT_SYSTEM_3,

			"default_image" : "d:/ymir work/gift_code_window/canclebutton00.sub",
			"over_image" : "d:/ymir work/gift_code_window/canclebutton01.sub",
			"down_image" : "d:/ymir work/gift_code_window/canclebutton02.sub",
		},
	),
}