import uiScriptLocale
import localeInfo
import app

BOARD_WIDTH = 200
BOARD_HEIGHT = 190

PRICE_INPUT_X = 12
PRICE_INPUT_Y = 32
PRICE_INPUT_WIDTH = 200 - 12 * 2
PRICE_INPUT_HEIGHT = 63

MARKET_PRICE_X = 12
MARKET_PRICE_Y = PRICE_INPUT_Y + PRICE_INPUT_HEIGHT + 1
MARKET_PRICE_WIDTH = 200 - 12 * 2
MARKET_PRICE_HEIGHT = 60

window = {
	"name" : "InputDialog",

	"x" : 0,
	"y" : 0,

	"style" : ("movable", "float",),

	"width" : BOARD_WIDTH,
	"height" : BOARD_HEIGHT,

	"children" :
	(
		{
			"name" : "board",
			"type" : "board_with_titlebar",

			"x" : 0,
			"y" : 0,

			"width" : BOARD_WIDTH,
			"height" : BOARD_HEIGHT,

			"title" : localeInfo.PRIVATE_SHOP_INPUT_PRICE_DIALOG_TITLE,

			"children" :
			(
				{
					"name" : "PriceHintButton",
					"type" : "button",

					"x" : BOARD_WIDTH - 50,
					"y" : 9,
					
					"default_image" : "d:/ymir work/ui/pattern/q_mark_01.tga",
					"over_image" : "d:/ymir work/ui/pattern/q_mark_02.tga",
					"down_image" : "d:/ymir work/ui/pattern/q_mark_02.tga",
				},

				{
					"name" : "PriceInputThinboard",
					"type" : "thinboard_circle",

					"x" : PRICE_INPUT_X,
					"y" : PRICE_INPUT_Y,

					"width" : PRICE_INPUT_WIDTH,
					"height" : PRICE_INPUT_HEIGHT,

					"children" : (
						{
							"name" : "PriceInputTitle",
							"type" : "text",

							"x" : 6,
							"y" : 4,

							"text_horizontal_align" : "center",
							"horizontal_align" : "center",

							"text" : uiScriptLocale.PRIVATE_SHOP_PRICE_TITLE,
						},

						{
							"name" : "InputSlot_Cheque",
							"type" : "slotbar",

							"x" : 35 - 12,
							"y" : 20,

							"width" : 24,
							"height" : 18,

							"children" :
							(
								{
									"name":"Cheque_Icon",
									"type":"image",

									"x":-18,
									"y":2,

									"image":"d:/ymir work/ui/game/windows/cheque_icon.sub",
								},
								{
									"name" : "InputValue_Cheque",
									"type" : "editline",

									"x" : 3,
									"y" : 3,

									"width" : 24,
									"height" : 18,

									"input_limit" : 2,
									"only_number" : 1,
									
									"text" : "0",
								},
							),
						},

						{
							"name" : "InputSlot",
							"type" : "slotbar",

							"x" : 90 - 12,
							"y" : 20,

							"width" : 90,
							"height" : 18,

							"children" :
							(
								{
									"name":"Money_Icon",
									"type":"image",

									"x":-18,
									"y":2,

									"image":"d:/ymir work/ui/game/windows/money_icon.sub",
								},
								{
									"name" : "InputValue",
									"type" : "editline",

									"x" : 3,
									"y" : 3,

									"width" : 90,
									"height" : 18,

									"input_limit" : 12,
									"only_currency" : 1,
								},
							),
						},
                        
						{
							"name" : "InputChequeText",
							"type" : "text",

							"x" : 25,
							"y" : 45,
							"text" : uiScriptLocale.SHOP_PRICE_WON_DEFAULT,
							"text_horizontal_align" : "left",
						},
                        
						{
							"name" : "InputMoneyText",
							"type" : "text",

							"x" : 81,
							"y" : 45,
							"text" : uiScriptLocale.SHOP_PRICE_YANG_DEFAULT,
							"text_horizontal_align" : "left",
						},
					),
				},

				{
					"name" : "MarketPriceThinboard",
					"type" : "thinboard_circle",

					"x" : MARKET_PRICE_X,
					"y" : MARKET_PRICE_Y,

					"width" : MARKET_PRICE_WIDTH,
					"height" : MARKET_PRICE_HEIGHT,

					"children" : (
						{
							"name" : "MarketPriceTitle",
							"type" : "text",

							"x" : -20,
							"y" : 4,

							"text_horizontal_align" : "center",
							"horizontal_align" : "center",

							"text" : uiScriptLocale.PRIVATE_SHOP_MARKET_PRICE_TITLE,
						},
                        
						{
							"name" : "MarketPriceButton",
							"type" : "button",

							"x" : 45,
							"y" : 7,

							"horizontal_align" : "center",

							"default_image" : "d:/ymir work/ui/game/PRIVATE_SHOP/mini_empty_button_default.sub",
							"over_image" : "d:/ymir work/ui/game/PRIVATE_SHOP/mini_empty_button_over.sub",
							"down_image" : "d:/ymir work/ui/game/PRIVATE_SHOP/mini_empty_button_down.sub",
						},

						{
							"name" : "MarketChequeValue",
							"type" : "text",

							"x" : 0,
							"y" : 4 + 16,
							"text" : localeInfo.PRIVATE_SHOP_MARKET_PRICE_NOT_AVAILABLE,
							"text_horizontal_align" : "center",
							"horizontal_align" : "center",
						},

						{
							"name" : "MarketMoneyValue",
							"type" : "text",

							"x" :  0,
							"y" : 4 + 16 + 16,
							"text" : localeInfo.PRIVATE_SHOP_MARKET_PRICE_NOT_AVAILABLE,
							"text_horizontal_align" : "center",
							"horizontal_align" : "center",
						},
					),
				},

				{
					"name" : "AcceptButton",
					"type" : "button",

					"x" : - 61 - 5 + 30,
					"y" : BOARD_HEIGHT - 31,

					"horizontal_align" : "center",

					"default_image" : "d:/ymir work/ui/public/acceptbutton00.sub",
					"over_image" : "d:/ymir work/ui/public/acceptbutton01.sub",
					"down_image" : "d:/ymir work/ui/public/acceptbutton02.sub",
				},
				{
					"name" : "CancelButton",
					"type" : "button",

					"x" : 5 + 30,
					"y" : BOARD_HEIGHT - 31,
					
					"horizontal_align" : "center",

					"default_image" : "d:/ymir work/ui/public/canclebutton00.sub",
					"over_image" : "d:/ymir work/ui/public/canclebutton01.sub",
					"down_image" : "d:/ymir work/ui/public/canclebutton02.sub",
				},
			),
		},
	),
}