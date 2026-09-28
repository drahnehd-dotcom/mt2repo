import uiScriptLocale

window = {
	"name" : "OfflineShopDialog",

	"x" : SCREEN_WIDTH - 400,
	"y" : 10,

	"style" : ("movable", "float",),

	"width" : 406,
	"height" : 392,

	"children" :
	(
		{
			"name" : "board",
			"type" : "board",
			"style" : ("attach",),

			"x" : 0,
			"y" : 0,

			"width" : 406,
			"height" : 392,

			"children" :
			(
				{
					"name" : "TitleBar",
					"type" : "titlebar",
					"style" : ("attach",),

					"x" : 8,
					"y" : 8,

					"width" : 391,
					"color" : "gray",

					"children" :
					(
						{ "name":"TitleName", "type":"text", "x":195, "y":0, "text":uiScriptLocale.SHOP_TITLE, "text_horizontal_align":"center", "outline":"1" },
					),
				},
				{
					"name" : "ItemSlot",
					"type" : "grid_table",

					"x" : 12,
					"y" : 34,

					"start_index" : 0,
					"x_count" : 12,
					"y_count" : 10,
					"x_step" : 32,
					"y_step" : 32,

					"image" : "d:/ymir work/ui/public/Slot_Base.sub",
				},
				{
					"name" : "BuyButton",
					"type" : "toggle_button",

					"x" : 0,
					"y" : 361,
                    "horizontal_align":"center",

					"default_image" : "d:/ymir work/ui/weekly_rank/button-example-020.png",
					"over_image" : "d:/ymir work/ui/weekly_rank/button-example-021.png",
					"down_image" : "d:/ymir work/ui/weekly_rank/button-example-022.png",
                    "children":
                    (
						{
                            "name":"buybutton_text",
                            "type":"text",
                            "x":0,"y":0,
                            "all_align":"center",
                            "text" : uiScriptLocale.SHOP_BUY,
                   			"outline":1,
                    		"fontname":"Tahoma:14b",
						},
					),
				},
				{
					"name" : "wiadomosc",
					"type" : "button",
					"x" : 354,
					"y" : 3,
					"tooltip_text_new" : uiScriptLocale.OFFLINE_SHOP_SEND_MESSAGE,
					"tooltip_text_color" : 0xfff1e6c0,
					"tooltip_x" : 0,
					"tooltip_y" : -35,
					"default_image" : "d:/ymir work/ui/offline_shop/sendpm.png",
					"over_image" : "d:/ymir work/ui/offline_shop/sendpm1.png",
					"down_image" : "d:/ymir work/ui/offline_shop/sendpm2.png",
				},
                {
					"name" : "status_off",
					"type" : "image",
					"x" : 332,
					"y" : 5,
					"image" : "d:/ymir work/ui/offline_shop/status_off.png",
				},
                {
					"name" : "status_on",
					"type" : "image",
					"x" : 332,
					"y" : 5,
					"image" : "d:/ymir work/ui/offline_shop/status_on.png",
				},
			),
		},
	),
}