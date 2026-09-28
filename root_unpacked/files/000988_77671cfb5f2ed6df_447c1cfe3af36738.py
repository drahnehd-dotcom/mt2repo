#-*- coding: iso-8859-1 -*-
import uiScriptLocale
BUTTON_ROOT = "d:/ymir work/ui/public/"
PATH = "d:/ymir work/ui/"
PATH1 = "d:/ymir work/ui/bonus_window/"
BOARD_WIDTH = 670
BOARD_HEIGHT = 275

window = {
	"name" : "SearchWindow",
	"x" : 200,
	"y" : 200,
	"style" : ("movable", "float",),
	"width" : BOARD_WIDTH,
	"height" : 305,
	"children" :
	(
		{
			"name" : "board0",
			"type" : "board",
			"style" : ("attach",),
			"x": -210, "y": 244,
			"horizontal_align":"center",
			"width": 110,"height": 30,
			"children" :
			(
				{
					"name":"SearchButton0",
					"type":"button",
					"x": 0, "y": 29,
					"veritcal_align":"center",
					"horizontal_align":"center",
					"default_image":"d:/ymir work/ui/marmur_window/buy_btn.png",
					"over_image":"d:/ymir work/ui/marmur_window/buy_btn1.png",
					"down_image":"d:/ymir work/ui/marmur_window/buy_btn2.png",

					"tooltip_text_new" : uiScriptLocale.SHOP_SEARCH_SEARCH_ITEM,
					"tooltip_text_color" : 0xfff1e6c0,
					"tooltip_x" : 0,
					"tooltip_y" : 40,
				},
			),
		},
		{
			"name" : "board1",
			"type" : "board",
			"style" : ("attach",),
			"x": 0, "y": 244,
			"horizontal_align":"center",
			"width": 110,"height": 30,
			"children" :
			(
				{
					"name":"SearchButton1",
					"type":"button",
					"x": 0, "y": 29,
					"veritcal_align":"center",
					"horizontal_align":"center",
					"default_image":"d:/ymir work/ui/marmur_window/buy_btn.png",
					"over_image":"d:/ymir work/ui/marmur_window/buy_btn1.png",
					"down_image":"d:/ymir work/ui/marmur_window/buy_btn2.png",

					"tooltip_text_new" : uiScriptLocale.SHOP_SEARCH_SEARCH_ITEMS,
					"tooltip_text_color" : 0xfff1e6c0,
					"tooltip_x" : 0,
					"tooltip_y" : 40,
				},
			),
		},
		{
			"name" : "board2",
			"type" : "board",
			"style" : ("attach",),
			"x": 210, "y": 244,
			"horizontal_align":"center",
			"width": 110,"height": 30,
			"children" :
			(
				{
					"name":"SearchButton2",
					"type":"button",
					"x": 0, "y": 29,
					"veritcal_align":"center",
					"horizontal_align":"center",
					"default_image":"d:/ymir work/ui/marmur_window/buy_btn.png",
					"over_image":"d:/ymir work/ui/marmur_window/buy_btn1.png",
					"down_image":"d:/ymir work/ui/marmur_window/buy_btn2.png",

					"tooltip_text_new" : "Vyhledat kategorie",
					"tooltip_text_color" : 0xfff1e6c0,
					"tooltip_x" : 0,
					"tooltip_y" : 40,
				},
			),
		},
		{
			"name" : "board",
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
					"y" : 8,
					"width" : BOARD_WIDTH-12,
					"children" :
					(
						{ "name":"TitleName", "type":"text", "x":0, "y":-5, "text":uiScriptLocale.SHOPSEARCH_TITLE, "all_align":"center","outline":1, },
						{
							"name" : "ClearButton0",
							"type" : "button",
							"x" : 10,
							"y" : 0,
							"veritcal_align":"center",
							"default_image" : "d:/ymir work/ui/clear_btn0.png",
							"over_image" : "d:/ymir work/ui/clear_btn1.png",
							"down_image" : "d:/ymir work/ui/clear_btn2.png",

							"tooltip_text_new" : uiScriptLocale.SHOP_SEARCH_CLEAR_SHOPS,
							"tooltip_text_color" : 0xfff1e6c0,
							"tooltip_x" : 0,
							"tooltip_y" : -40,
						},
					),
				},
				{
					"name" : "border",
					"type" : "border_a",
					"x" : 0,
					"y" : 10,
					"horizontal_align":"center",
					"vertical_align":"center",
					"width" : BOARD_WIDTH-20,
					"height" : BOARD_HEIGHT-40,
					"children" :
					(
						{
							"name" : "nazwa_window",
							"type" : "window",
							"x" : 5, "y" : 5,
							"width" : 218, "height" : 225,
							"children":
							(
								{
									"name" : "header_s",
									"type" : "image",
									"x" : 1, "y" : 0,
									"image" : PATH+"header_s.png",
									"children":
									(
										{
											"name" : "header_s_text",
											"type" : "text",
											"x" : 0, "y" : 0,
											"text" : uiScriptLocale.SHOPSEARCH_FIND_BY_NAME,
											"all_align":"center",
											"outline":1,
											"fontname":"Tahoma:16",
										},
									),
								},
								{
									"name" : "border2",
									"type" : "border_a",
									"x" : 0, "y" : 25,
									"width" : 218, "height" : 167,
									"children":
									(
										{
											"name" : "window",
											"type" : "window",
											"x" : 0, "y" : 0,
											"width" : 218, "height" : 167,
											"children":
											(
												{
													"name" : "box",
													"type" : "image",
													"x" : 2, "y" : 2,
													"image" : PATH+"search_box.png",
												},
											),
										},
									),
								},
								{
									"name" : "border1",
									"type" : "border_a",
									"x" : 0, "y" : 225 - 32,
									"width" : 218, "height" : 30,
									"children":
									(
										{
											"name" : "search_icon",
											"type" : "image",
											"x" : 6, "y" : 8,
											"image" : PATH1+"search_icon.png",
										},
										{
											"name" : "InputSlot",
											"type" : "slotbar",
											"x" : 10, "y" : 0,
											"width" : 180, "height" : 17,
											"horizontal_align" : "center",
											"vertical_align" : "center",
											"children" :
											(
												{
													"name" : "InputValue",
													"type" : "editline",
													"x" : 3, "y" : 3,
													"width" : 180, "height" : 18,
													"input_limit" : 12,
												},
											),
										},
									),
								},
							),
						},
						{
							"name" : "slot_window",
							"type" : "window",
							"x" : 225, "y" : 5,
							"width" : 200, "height" : 225,
							"children":
							(
								{
									"name" : "header_s",
									"type" : "image",
									"x" : 0, "y" : 0,
									"image" : PATH+"header_b.png",
									"children":
									(
										{
											"name" : "header_s_text",
											"type" : "text",
											"x" : 0, "y" : 0,
											"text" : uiScriptLocale.SHOPSEARCH_SEARCH_ITEMS,
											"all_align":"center",
											"outline":1,
											"fontname":"Tahoma:16",
										},
										{
											"name" : "ClearButton1",
											"type" : "button",
											"x" : 175,
											"y" : 1,
											"veritcal_align":"center",
											"default_image" : "d:/ymir work/ui/clear_btn3.png",
											"over_image" : "d:/ymir work/ui/clear_btn4.png",
											"down_image" : "d:/ymir work/ui/clear_btn5.png",

											"tooltip_text_new" : uiScriptLocale.SHOP_SEARCH_CLEAR,
											"tooltip_text_color" : 0xfff1e6c0,
											"tooltip_x" : 0,
											"tooltip_y" : -40,
										},
									),
								},
								{
									"name" : "border3",
									"type" : "border_a",
									"x" : 0, "y" : 25,
									"width" : 200, "height" : 200,
									"children":
									(
										{
											"name": "item_slot",
											"type": "grid_table",
											"start_index": 0,
											"x": 4,
											"y": 4,
											"x_count": 6,
											"y_count": 6,
											"x_step": 32,
											"y_step": 32,
											"x_blank": 0,
											"y_blank": 0,
											"image": "d:/ymir work/ui/public/slot_base.sub",
										},
									),
								},
							),
						},
						{
							"name" : "kategoria_window",
							"type" : "window",
							"x" : 427, "y" : 5,
							"width" : 218, "height" : 225,
							"children":
							(
								{
									"name" : "header_s",
									"type" : "image",
									"x" : 0, "y" : 0,
									"image" : PATH+"header_s.png",
									"children":
									(
										{
											"name" : "header_s_text",
											"type" : "text",
											"x" : 0, "y" : 0,
											"text" : uiScriptLocale.SHOPSEARCH_SEARCH_IN_CATEGORY,
											"all_align":"center",
											"outline":1,
											"fontname":"Tahoma:16",
										},
									),
								},
								{
									"name" : "border4",
									"type" : "border_a",
									"x" : 0, "y" : 25,
									"width" : 218, "height" : 167,
									"children":
									(
										{
											"name" : "window",
											"type" : "window",
											"x" : 0, "y" : 0,
											"width" : 218, "height" : 167,
											"children":
											(
												{
													"name" : "box",
													"type" : "image",
													"x" : 2, "y" : 2,
													"image" : PATH+"search_box.png",
												},
											),
										},
									),
								},
								{
									"name" : "border5",
									"type" : "border_a",
									"x" : 0, "y" : 225 - 32,
									"width" : 218, "height" : 30,
									"children":
									(
										{
											"name" : "search_icon",
											"type" : "image",
											"x" : 6, "y" : 8,
											"image" : PATH1+"search_icon.png",
										},
										{
											"name" : "InputSlot1",
											"type" : "slotbar",
											"x" : 10, "y" : 0,
											"width" : 180, "height" : 17,
											"horizontal_align" : "center",
											"vertical_align" : "center",
											"children" :
											(
												{
													"name" : "InputValue1",
													"type" : "editline",
													"x" : 3, "y" : 3,
													"width" : 180, "height" : 18,
													"input_limit" : 12,
												},
											),
										},
									),
								},
							),
						},
					),
				},
			),
		},
	),
}

