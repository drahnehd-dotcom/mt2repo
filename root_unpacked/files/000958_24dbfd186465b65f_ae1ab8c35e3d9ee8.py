import uiScriptLocale

window = {
	"name" : "PrivateShopBuilder",

	"x" : 0,
	"y" : 0,

	"style" : ("movable", "float",),

	"width" : 184,
	"height" : 360 + 26,

	"children" :
	(
		{
			"name" : "board",
			"type" : "board",
			"style" : ("attach",),

			"x" : 0,
			"y" : 0,

			"width" : 184,
			"height" : 360 + 26,

			"children" :
			(
				{
					"name" : "TitleBar",
					"type" : "titlebar",
					"style" : ("attach",),

					"x" : 8,
					"y" : 8,

					"width" : 169,
					"color" : "gray",

					"children" :
					(
						{ "name":"TitleName", "type":"text", "x":84, "y":0, "text":uiScriptLocale.PRIVATE_SHOP_TITLE, "text_horizontal_align":"center" },
					),
				},

				{
					"name" : "NameSlot",
					"type" : "slotbar",
					"x" : 13,
					"y" : 35,
					"width" : 90 + 67,
					"height" : 18,

					"children" :
					(
						{
							"name" : "NameLine",
							"type" : "text",
							"x" : 3,
							"y" : 3,
							"width" : 157,
							"height" : 15,
							"input_limit" : 25,
							"text" : "1234567890123456789012345",
						},
					),
				},

				{
					"name" : "ItemSlot",
					"type" : "grid_table",

					"x" : 12,
					"y" : 34 + 26,

					# 5 x 9 = 45 slots, kept in sync with SHOP_HOST_ITEM_MAX_NUM
					# (kowalcore/Shared/ShopConstants.hpp) - uiprivateshopbuilder.py
					# iterates range(shop.SHOP_SLOT_COUNT) over these slots.
					"start_index" : 0,
					"x_count" : 5,
					"y_count" : 9,
					"x_step" : 32,
					"y_step" : 32,

					"image" : "d:/ymir work/ui/public/Slot_Base.sub",
				},

				{
					"name" : "OkButton",
					"type" : "button",

					"x" : 21,
					"y" : 327 + 26,

					"width" : 61,
					"height" : 21,

					"text" : uiScriptLocale.OK,

					"default_image" : "d:/ymir work/ui/public/middle_button_01.sub",
					"over_image" : "d:/ymir work/ui/public/middle_button_02.sub",
					"down_image" : "d:/ymir work/ui/public/middle_button_03.sub",
				},

				{
					"name" : "CloseButton",
					"type" : "button",

					"x" : 104,
					"y" : 327 + 26,

					"width" : 61,
					"height" : 21,

					"text" : uiScriptLocale.CLOSE,

					"default_image" : "d:/ymir work/ui/public/middle_button_01.sub",
					"over_image" : "d:/ymir work/ui/public/middle_button_02.sub",
					"down_image" : "d:/ymir work/ui/public/middle_button_03.sub",
				},
			),
		},
	),
}