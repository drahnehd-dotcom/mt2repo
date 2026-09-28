import uiScriptLocale
import emoji

WINDOW_X = 438
WINDOW_Y = 240

SHOP_PATH = "kowal/polysystem/shop/{}"
COLLECT_PATH = "kowal/polysystem/collection/{}"
DEFAULT_PATH = "d:/ymir work/ui/poly_window/"

SKINS_RENDER_INDEX = 7
SHOP_REDNER_INDEX = 8

BORDER_WIDTH = 213
BORDER_WIDTH2 = 196

window = {
	"name" : "PolySystemWindow",
	"x" : (SCREEN_WIDTH-WINDOW_X)/2,
	"y" : (SCREEN_HEIGHT-WINDOW_Y)/2,
	"style" : ("movable", "float"),
	"width" : WINDOW_X, "height" : WINDOW_Y+40,
	"children" :
	(
		{
			"name" : "buy_board",
			"type" : "board",
			"x" : 65, "y" : WINDOW_Y-30,
			"width" : 115, "height" : 50,
			"children":
			(
				{
					"name" : "BuyButton",
					"type" : "button",
					"x" : 0, "y" : 10,
					"horizontal_align" : "center",
					"vertical_align" : "center",
					"default_image" : "d:/ymir work/ui/button-accept-0.png",
					"over_image" : "d:/ymir work/ui/button-accept-1.png",
					"down_image" : "d:/ymir work/ui/button-accept-2.png",
				},
			),
		},
		{
			"name" : "Board",
			"type" : "board",
			"style" : ("attach",),
			"x" : 0, "y" : 0,
			"width" : WINDOW_X, "height" : WINDOW_Y,
			"children" :
			(
				{ "name" : "TitleBar", "type" : "titlebar", "style" : ("attach",), "x" : 8, "y" : 7, "width" : WINDOW_X-15, "children" : ( { 
				  "name":"TitleName", "type":"text", "x":0, "y":-4, "text": uiScriptLocale.POLY_MARBLES_TITLE, "all_align":"center", "outline" : 1 },), 
				},
				{ 
					"name" : "PageShop",
					"type" : "border_a",
					"x" : 0, "y" : 27,
					"width" : WINDOW_X-20, "height" : WINDOW_Y-37,
					"horizontal_align" : "center",
					"children" : ( {
							"name" : "border",
							"type" : "border_a",
							"x" : 4, "y" : 0,
							"width" : BORDER_WIDTH, "height" : WINDOW_Y-45,
							"vertical_align" : "center",
							"children": ( {
									"name" : "bg", "type" : "image", "x" : 0, "y" : 0, "image" : DEFAULT_PATH+"overlay.png", "horizontal_align" : "center", "vertical_align" : "center",
								},
								{
									"name" : "ItemsSlot",
									"type" : "slot", 
									"x" : 9,"y" : 25,
									"width" : 160,"height" : 32,
									"image" : DEFAULT_PATH+"slot_base.png",
									"slot" : (
										{ "index" : 0, "x" : 0, "y" : 0, "width" : 32, "height" : 32 },
										{ "index" : 1, "x" : 32, "y" : 0, "width" : 32, "height" : 32 },
										{ "index" : 2, "x" : 32*2, "y" : 0, "width" : 32, "height" : 32 },
										{ "index" : 3, "x" : 32*3, "y" : 0, "width" : 32, "height" : 32 },
										{ "index" : 4, "x" : 32*4, "y" : 0, "width" : 32, "height" : 32 },
										{ "index" : 5, "x" : 32*5, "y" : 0, "width" : 32, "height" : 32 },
									),
								},
								{
									"name" : "money_slot",
									"type" : "image",
									"x" : 0, "y" : 70,
									"horizontal_align" : "center",
									"image" : DEFAULT_PATH+"slot.png",
									"children": ( {
											"name" : "money_icon",
											"type" : "image",
											"x" : 2, "y" : 2,
											"image" : "icon/emoji/money_icon_small.png",
										},
										{
											"name" : "money_text",
											"type" : "text",
											"x" : 0, "y" : 0,
											"text" : "0",
											"color" : 0xFFf5d442,
											"all_align" : "center",
										},
									),
								},
								{
									"name" : "cheque_slot",
									"type" : "image",
									"x" : 0, "y" : 95,
									"horizontal_align" : "center",
									"image" : DEFAULT_PATH+"slot.png",
									"children": ( {
											"name" : "cheque_icon",
											"type" : "image",
											"x" : 6, "y" : 4,
											"image" : "icon/emoji/cheque_icon.png",
										},
										{
											"name" : "cheque_text",
											"type" : "text",
											"x" : 0, "y" : 0,
											"text" : "0",
											"color" : 0xFFbdbdbd,
											"all_align" : "center",
										},
									),
								},
								{
									"name" : "count_window",
									"type" : "image",
									"x" : 0, "y" : 125,
									"horizontal_align" : "center",
									"image" : DEFAULT_PATH+"slotbat-84x23.png",
									"children": (
										{
											"name" : "left_btn",
											"type" : "button",
											"x" : 5, "y" : 0,
											"horizontal_align" : "left",
											"vertical_align" : "center",
											"default_image" : "d:/ymir work/ui/location_window/btn-left-0.png",
											"over_image" : "d:/ymir work/ui/location_window/btn-left-1.png",
											"down_image" : "d:/ymir work/ui/location_window/btn-left-2.png",
										},
										{
											"name" : "count_text", "type" : "text", "x" : 0, "y" : 0, "text" : "1", "all_align" : "center", "fontname" : "Tahoma:14",
										},
										{
											"name" : "right_btn",
											"type" : "button",
											"x" : 18, "y" : 0,
											"horizontal_align" : "right",
											"vertical_align" : "center",
											"default_image" : "d:/ymir work/ui/location_window/btn-right-0.png",
											"over_image" : "d:/ymir work/ui/location_window/btn-right-1.png",
											"down_image" : "d:/ymir work/ui/location_window/btn-right-2.png",
										},
									),
								},
								{
									"name" : "PageButton",
									"type" : "button",
									"x" : 10, "y" : 161,
									"horizontal_align" : "center",
									"default_image" : DEFAULT_PATH+"button.png",
									"over_image" : DEFAULT_PATH+"button1.png",
									"down_image" : DEFAULT_PATH+"button2.png",
									"children": (
										{
											"name" : "select_skin_text",
											"type" : "text",
											"x" : 0, "y" : -1,
											"text" : uiScriptLocale.POLYSYSTEM_CHOOSE_SKIN,
											"all_align" : "center",
										},
									),
								},
								{
									"name" : "SkinImage",
									"type" : "image",
									"x": 30,
									"y": WINDOW_Y-88,
									"image" : DEFAULT_PATH+"slot_base1.png",
									"horizontal_align" : "left",
									"children":
									(
										{
											"name" : "SkinSlot",
											"type" : "slot",
											"x" : 0, "y" : 0,
											"width" : 32, "height" : 32,
											"slot" : 
											(
												{"index":0, "x":0, "y": 0, "width":32, "height":32},
											),
										},
									),
								},
							),
						},
					),
				},
				{ 
					"name" : "PageCollections",
					"type" : "border_a",
					"x" : 0, "y" : 27,
					"width" : WINDOW_X-20, "height" : WINDOW_Y-37,
					"horizontal_align" : "center",
					"children" : 
					(
						{
							"name" : "border",
							"type" : "border_a",
							"x" : 4, "y" : 0,
							"width" : BORDER_WIDTH, "height" : WINDOW_Y-45,
							"vertical_align" : "center",
							"children":
							(
								{
									"name" : "bg", "type" : "image", "x" : 0, "y" : 0, "image" : DEFAULT_PATH+"overlay.png", "horizontal_align" : "center", "vertical_align" : "center",
								},
								{
									"name" : "CollectBox",
									"type" : "listboxex",
									"x" : 0,
									"y" : 7,
									"horizontal_align" : "center",
									"width" : 200,
									"height" : 180,
								},
								{
									"name" : "SkinButton",
									"type" : "button",
									"x" : 5, "y" : 165,
									"horizontal_align" : "center",
									"default_image" : DEFAULT_PATH+"button.png",
									"over_image" : DEFAULT_PATH+"button1.png",
									"down_image" : DEFAULT_PATH+"button2.png",
									"children": (
										{
											"name" : "select_skin_text",
											"type" : "text",
											"x" : 0, "y" : -1,
											"text" : uiScriptLocale.POLYSYSTEM_CHOOSE_SKIN_SELECT,
											"all_align" : "center",
										},
									),
								},
								{
									"name" : "BackButton",
									"type" : "button",
									"x" : 35, "y" : 165,
									"default_image" : DEFAULT_PATH+"back_btn0.png",
									"over_image" : DEFAULT_PATH+"back_btn1.png",
									"down_image" : DEFAULT_PATH+"back_btn2.png",
								},
							),
						},
					),
				},
				{
					"name" : "border3",
					"type" : "border_a",
					"x" : BORDER_WIDTH+15, "y" : 9,
					"width" : BORDER_WIDTH2, "height" : WINDOW_Y-45,
					"vertical_align" : "center",
					"children" : ( {
							"name" : "Render",
							"type" : "render_target",
							"x" : 0, "y" : 0,
							"horizontal_align" : "center",
							"vertical_align" : "center",
							"width" : 190, "height" : 190,
							"index" : SHOP_REDNER_INDEX,
						},
						{
							"name" : "StageButton1",
							"type" : "radio_button",
							"horizontal_align" : "left",
							"x" : 10,"y" : 9,
							"default_image" : DEFAULT_PATH+"stage_btn0.png",
							"over_image" : DEFAULT_PATH+"stage_btn1.png",
							"down_image" : DEFAULT_PATH+"stage_btn2.png",
							"children":
							(
								{
									"name" : "StageText",
									"type" : "text",
									"x" : 0, "y" : -1,
									"text" : "I",
									"fontname" : "Tahoma:16b",
									"all_align" : "center",
									"color" : 0xFFb8b3a5,
									"outline" : 1,
								},
							),
						},
						{
							"name" : "StageButton2",
							"type" : "radio_button",
							"horizontal_align" : "left",
							"x" : 10,"y" : 36,
							"default_image" : DEFAULT_PATH+"stage_btn0.png",
							"over_image" : DEFAULT_PATH+"stage_btn1.png",
							"down_image" : DEFAULT_PATH+"stage_btn2.png",
							"children":
							(
								{
									"name" : "StageText",
									"type" : "text",
									"x" : 1, "y" : -1,
									"text" : "II",
									"fontname" : "Tahoma:16b",
									"all_align" : "center",
									"color" : 0xFFb8b3a5,
									"outline" : 1,
								},
							),
						},
						{
							"name" : "StageButton3",
							"type" : "radio_button",
							"horizontal_align" : "left",
							"x" : 10,"y" : 66,
							"default_image" : DEFAULT_PATH+"stage_btn0.png",
							"over_image" : DEFAULT_PATH+"stage_btn1.png",
							"down_image" : DEFAULT_PATH+"stage_btn2.png",
							"children":
							(
								{
									"name" : "StageText",
									"type" : "text",
									"x" : 0, "y" : -1,
									"text" : "III",
									"fontname" : "Tahoma:16b",
									"all_align" : "center",
									"color" : 0xFFb8b3a5,
									"outline" : 1,
								},
							),
						},
						{
							"name" : "BonusImage2",
							"type" : "image",
							"x" : 0, "y" : 147,
							"horizontal_align" : "center",
							"image" : DEFAULT_PATH+"slot1.png",
							"children": (
								{
									"name" : "BonusText2",
									"type" : "text",
									"x" : 0, "y" : 0,
									"text" : uiScriptLocale.POLYSYSTEM_NO_BONUSES,
									"fontname" : "Tahoma:12",
									"all_align" : "center",
								},
							),
						},
						{
							"name" : "BonusImage1",
							"type" : "image",
							"x" : 0, "y" : 169,
							"horizontal_align" : "center",
							"image" : DEFAULT_PATH+"slot1.png",
							"children": (
								{
									"name" : "BonusText1",
									"type" : "text",
									"x" : 0, "y" : 0,
									"text" : uiScriptLocale.POLYSYSTEM_NO_BONUSES,
									"fontname" : "Tahoma:12",
									"all_align" : "center",
								},
							),
						},
					),
				},
			),
		},
	),
}
