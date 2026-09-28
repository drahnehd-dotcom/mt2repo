import uiScriptLocale

window = {
	"name" : "OfflineShopBuilder",

	"x" : 0,
	"y" : 0,

	"style" : ("movable", "float",),

	"width" : 406,
	"height" : 420,

	"children" :
	(
		{
			"name" : "Board",
			"type" : "board_with_titlebar",
			"style" : ("attach",),

			"x" : 0,
			"y" : 0,

			"width" : 406,
			"height" : 420,
			
			"title" : uiScriptLocale.PRIVATE_SHOP_TITLE,

			"children" :
			(
				{
					"name" : "NameSlot",
					"type" : "image",
					
					"x" : 0,
					"y" : 33,

					"horizontal_align" : "center",
					
					"image" : "d:/ymir work/ui/offline_shop/button-example-experiment.png",

					"children" :
					(
						{
							"name" : "NameLine",
							"type" : "text",
							
							"x" : 0,
							"y" : -1,
							
							"horizontal_align" : "center",
							"vertical_align" : "center",

							"input_limit" : 25,

							"text" : "",
							"fontsize":"LARGE",
							"all_align" : "center",
						},
					),
				},
				{
					"name" : "ItemSlot",
					"type" : "grid_table",

					"x" : 12,
					"y" : 34 + 26,

					"start_index" : 0,
					"x_count" : 12,
					"y_count" : 10,
					"x_step" : 32,
					"y_step" : 32,

					"image" : "d:/ymir work/ui/public/Slot_Base.sub",
				},
				{
					"name" : "OkButton",
					"type" : "button",
					
					"x" : -50,
					"y" : 356 + 33,

					"horizontal_align" : "center",
					
					"default_image" : uiScriptLocale.LOCALE_OFFLINESHOP_PATH + "/accept_01.tga",
					"over_image" : uiScriptLocale.LOCALE_OFFLINESHOP_PATH + "/accept_02.tga",
					"down_image" : uiScriptLocale.LOCALE_OFFLINESHOP_PATH + "/accept_03.tga",
				},
				{
					"name" : "CloseButton",
					"type" : "button",
					
					"x" : 50,
					"y" : 356 + 33,

					"horizontal_align" : "center",
					
					"default_image" : uiScriptLocale.LOCALE_OFFLINESHOP_PATH + "/no_01.tga",
					"over_image" : uiScriptLocale.LOCALE_OFFLINESHOP_PATH + "/no_02.tga",
					"down_image" : uiScriptLocale.LOCALE_OFFLINESHOP_PATH + "/no_03.tga",
				},
			),
		},
	),
}