import uiScriptLocale
LOCALE_PATH = "d:/ymir work/ui/privatesearch/"

window = {
	"name" : "ItemShopEditorDialog",
	"style" : ("movable", "float",),

	"x" : 0,
	"y" : 0,

	"width" : 684,
	"height" : 453 + 52,

	"children" :
	(
		{
			"name" : "Board",
			"type" : "board_with_titlebar",
			"style" : ("attach",),

			"x" : 0,
			"y" : 0,

			"width" : 684,
			"height" : 453 + 52,
			"title" : uiScriptLocale.ITEMSHOP_TITLE,
			"children" :
			(
				{
					"name": "categories_board",
					"type": "board",

					"x": 9,
					"y" : 31,

					"width" : 220,
					"height" : 413 + 52,

					"children" : (
						{
							"name" : "categories_listbox",
							"type" : "unfoldlistbox",

							"x" : 0,
							"y" : -20,

							"width" : 220,
							"height" : 413 + 52,

						},
					),
				},

				{
					"name": "items_board",
					"type": "board",

					"x": 235,
					"y" : 31,

					"width" : 440,
					"height" : 413 + 52,

					"children" : (
						{
							"name" : "bar",
							"type" : "bar",

							"x" : 0,
							"y" : 0,

							"width" : 440,
							"height" : 123,

							"color" : 0x70000000,

							"children" :
							(
								{
									"name" : "slotbar",
									"type" : "image",

									"x" : 0,
									"y" : 0,

									"image" : "d:/ymir work/ui/tab_menu_01.tga",

									"children" : (
										{
											"name" : "main_text",
											"type" : "text",

											"x" : 8,
											"y" : 4,

											"text" : uiScriptLocale.ITEMSHOP_EDITOR_ITEM_MAIN,

											"outline" : True,
										},
									),
								},
								{
									"name" : "item_slot",
									"type" : "grid_table",

									"x" : 16,
									"y" : 24,

									"start_index" : 0,
									"x_count" : 1,
									"y_count" : 3,

									"x_step" : 32,
									"y_step" : 32,

									"image" : "d:/ymir work/ui/public/Slot_Base.sub",

								},
							),
						},

						{
							"name": "item_name_slot",
							"type": "thinboardcircle",

							"x": 30 + 32 + 16,
							"y" : 30 + 12,

							"width" : 184,
							"height" : 16,

							"children" : (
								{
									"name": "item_name_value",
									"type": "text",

									"x": 5,
									"y": 0,

									"text": uiScriptLocale.ITEMSHOP_EDITOR_ITEM_NAME
								},
							),
						},
						{
							"name": "item_count_slot",
							"type": "thinboardcircle",

							"x": 30 + 32 + 16 + 26,
							"y" : 30 + 12 + 32,

							"width" : 64,
							"height" : 16,

							"children" : (
								{
									"name": "item_count_value",
									"type": "editline",

									"x": 5,
									"y": 0,

									"width": 64,
									"height": 16,

									"input_limit": 3,

									"only_number" : True,
								},
								{
									"name": "item_count_info",
									"type": "text",

									"x": -28,
									"y": 0,

									"text": uiScriptLocale.ITEMSHOP_EDITOR_ITEM_COUNT,
								},
							),
						},
						{
							"name": "item_price_slot",
							"type": "thinboardcircle",

							"x": 30 + 32 + 16 + 26,
							"y" : 30 + 12 + 32 + 32,

							"width" : 64,
							"height" : 16,

							"children" : (
								{
									"name": "item_price_value",
									"type": "editline",

									"x": 5,
									"y": 0,

									"width": 64,
									"height": 16,

									"input_limit": 10,

									"only_number" : True,
								},
								{
									"name": "item_price_info",
									"type": "text",

									"x": -28,
									"y": 0,

									"text": uiScriptLocale.ITEMSHOP_EDITOR_ITEM_PRICE,
								},
							),
						},
						{
							"name" : "checkbox_window",
							"type" : "window",

							"width" : 48,
							"height" : 20,

							"x": 30 + 32 + 16 + 26 + 64 + 16,
							"y" : 30 + 12 + 32 - 2 ,

							"children" : (
								{
									"name": "unfixed_count_checkbox",
									"type": "checkbox_biolog",

									"x": 0,
									"y": 0,

								},
							),
						},
						{
							"name" : "bar2",
							"type" : "bar",

							"x" : 0,
							"y" : 123 + 5,

							"width" : 440,
							"height" : 24 + 26 + 26 + 18,

							"color" : 0x70000000,

							"children" :
							(
								{
									"name" : "slotbar",
									"type" : "image",

									"x" : 0,
									"y" : 0,

									"image" : "d:/ymir work/ui/tab_menu_01.tga",

									"children" : (
										{
											"name" : "main_text",
											"type" : "text",

											"x" : 8,
											"y" : 4,

											"text" : uiScriptLocale.ITEMSHOP_EDITOR_ITEM_SOCKET,

											"outline" : True,
										},
									),
								},
								{
									"name" : "socket_window_01",
									"type" : "thinboardcircle",

									"x" : 16 + 46,
									"y" : 24,

									"width" : 184,
									"height" : 16,

									"children" : (
										{
											"name" : "main_text",
											"type" : "text",

											"x" : -46,
											"y" : 0,

											"text" : uiScriptLocale.ITEMSHOP_EDITOR_ITEM_SOCKET_TEXT % 1,
										},
										{
											"name": "socket_text_01",
											"type": "text",

											"x": 5,
											"y": 0,

											"text": ""
										},
									),

								},
								{
									"name" : "socket_window_02",
									"type" : "thinboardcircle",

									"x" : 16 + 46,
									"y" : 24 + 26,

									"width" : 184,
									"height" : 16,

									"children" : (
										{
											"name" : "main_text",
											"type" : "text",

											"x" : -46,
											"y" : 0,

											"text" : uiScriptLocale.ITEMSHOP_EDITOR_ITEM_SOCKET_TEXT % 2,
										},
										{
											"name": "socket_text_02",
											"type": "text",

											"x": 5,
											"y": 0,

											"text": ""
										},
									),

								},
								{
									"name" : "socket_window_03",
									"type" : "thinboardcircle",

									"x" : 16 + 46,
									"y" : 24 + 26 + 26,

									"width" : 184,
									"height" : 16,

									"children": (
										{
											"name": "main_text",
											"type": "text",

											"x": -46,
											"y": 0,

											"text": uiScriptLocale.ITEMSHOP_EDITOR_ITEM_SOCKET_TEXT % 3,
										},
										{
											"name": "socket_text_03",
											"type": "text",

											"x": 5,
											"y": 0,

											"text": ""
										},
									),

								},
								{
									"name" : "socket_window_04",
									"type" : "thinboardcircle",

									"x" : 16 + 46,
									"y" : 24 + 26 + 26+ 26,

									"width" : 184,
									"height" : 16,

									"children": (
										{
											"name": "main_text",
											"type": "text",

											"x": -46,
											"y": 0,

											"text": uiScriptLocale.ITEMSHOP_EDITOR_ITEM_SOCKET_TEXT % 4,
										},
										{
											"name": "socket_text_04",
											"type": "text",

											"x": 5,
											"y": 0,

											"text": ""
										},
									),

								},
								{
									"name" : "socket_window_05",
									"type" : "thinboardcircle",

									"x" : 16 + 46,
									"y" : 24 + 26 + 26+ 26+ 26,

									"width" : 184,
									"height" : 16,

									"children": (
										{
											"name": "main_text",
											"type": "text",

											"x": -46,
											"y": 0,

											"text": uiScriptLocale.ITEMSHOP_EDITOR_ITEM_SOCKET_TEXT % 5,
										},
										{
											"name": "socket_text_05",
											"type": "text",

											"x": 5,
											"y": 0,

											"text": ""
										},
									),

								},
								{
									"name" : "socket_window_06",
									"type" : "thinboardcircle",

									"x" : 16 + 46,
									"y" : 24 + 26 + 26+ 26+ 26,

									"width" : 184,
									"height" : 16,

									"children": (
										{
											"name": "main_text",
											"type": "text",

											"x": -46,
											"y": 0,

											"text": uiScriptLocale.ITEMSHOP_EDITOR_ITEM_SOCKET_TEXT % 6,
										},
										{
											"name": "socket_text_06",
											"type": "text",

											"x": 5,
											"y": 0,

											"text": ""
										},
									),

								},
							),
						},
						{
							"name" : "bar2",
							"type" : "bar",

							"x" : 0,
							"y" : 227,

							"width" : 440,
							"height" : 24 + 26 * 6 + 18,

							"color" : 0x70000000,

							"children" :
							(
								{
									"name" : "slotbar",
									"type" : "image",

									"x" : 0,
									"y" : 0,

									"image" : "d:/ymir work/ui/tab_menu_01.tga",

									"children" : (
										{
											"name" : "main_text",
											"type" : "text",

											"x" : 8,
											"y" : 4,

											"text" : uiScriptLocale.ITEMSHOP_EDITOR_ITEM_ATTR,

											"outline" : True,
										},
									),
								},
								{
									"name" : "attr_window_01",
									"type" : "thinboardcircle",

									"x" : 16 + 46,
									"y" : 24,

									"width" : 184,
									"height" : 16,

									"children" : (
										{
											"name" : "main_text",
											"type" : "text",

											"x" : -46,
											"y" : 0,

											"text" : uiScriptLocale.ITEMSHOP_EDITOR_ITEM_ATTR_TEXT % 1,
										},
										{
											"name": "attr_text_01",
											"type": "text",

											"x": 5,
											"y": 0,

											"text": ""
										},
									),

								},
								{
									"name" : "attr_window_02",
									"type" : "thinboardcircle",

									"x" : 16 + 46,
									"y" : 24 + 26 * 1,

									"width" : 184,
									"height" : 16,

									"children" : (
										{
											"name" : "main_text",
											"type" : "text",

											"x" : -46,
											"y" : 0,

											"text" : uiScriptLocale.ITEMSHOP_EDITOR_ITEM_ATTR_TEXT % 2,
										},
										{
											"name": "attr_text_02",
											"type": "text",

											"x": 5,
											"y": 0,

											"text": ""
										},
									),

								},
								{
									"name" : "attr_window_03",
									"type" : "thinboardcircle",

									"x" : 16 + 46,
									"y" : 24 + 26 * 2,

									"width" : 184,
									"height" : 16,

									"children": (
										{
											"name": "main_text",
											"type": "text",

											"x": -46,
											"y": 0,

											"text": uiScriptLocale.ITEMSHOP_EDITOR_ITEM_ATTR_TEXT % 3,
										},
										{
											"name": "attr_text_03",
											"type": "text",

											"x": 5,
											"y": 0,

											"text": ""
										},
									),

								},
								{
									"name" : "attr_window_04",
									"type" : "thinboardcircle",

									"x" : 16 + 46,
									"y" : 24 + 26 * 3,

									"width" : 184,
									"height" : 16,

									"children": (
										{
											"name": "main_text",
											"type": "text",

											"x": -46,
											"y": 0,

											"text": uiScriptLocale.ITEMSHOP_EDITOR_ITEM_ATTR_TEXT % 4,
										},
										{
											"name": "attr_text_04",
											"type": "text",

											"x": 5,
											"y": 0,

											"text": ""
										},
									),

								},
								{
									"name" : "attr_window_05",
									"type" : "thinboardcircle",

									"x" : 16 + 46,
									"y" : 24 + 26 * 4,

									"width" : 184,
									"height" : 16,

									"children": (
										{
											"name": "main_text",
											"type": "text",

											"x": -46,
											"y": 0,

											"text": uiScriptLocale.ITEMSHOP_EDITOR_ITEM_ATTR_TEXT % 5,
										},
										{
											"name": "attr_text_05",
											"type": "text",

											"x": 5,
											"y": 0,

											"text": ""
										},
									),

								},
								{
									"name": "attr_window_06",
									"type": "thinboardcircle",

									"x": 16 + 46,
									"y": 24 + 26 * 5,

									"width": 184,
									"height": 16,

									"children": (
										{
											"name": "main_text",
											"type": "text",

											"x": -46,
											"y": 0,

											"text": uiScriptLocale.ITEMSHOP_EDITOR_ITEM_ATTR_TEXT % 6,
										},
										{
											"name": "attr_text_06",
											"type": "text",

											"x": 5,
											"y": 0,

											"text": ""
										},
									),

								},
								{
									"name": "attr_window_07",
									"type": "thinboardcircle",

									"x": 16 + 46,
									"y": 24 + 26 * 6,

									"width": 184,
									"height": 16,

									"children": (
										{
											"name": "main_text",
											"type": "text",

											"x": -46,
											"y": 0,

											"text": uiScriptLocale.ITEMSHOP_EDITOR_ITEM_ATTR_TEXT % 7,
										},
										{
											"name": "attr_text_07",
											"type": "text",

											"x": 5,
											"y": 0,

											"text": ""
										},
									),

								},
								{
									"name": "attr_value_window_01",
									"type": "thinboardcircle",

									"x": 16 + 46 + 184 + 16 + 64,
									"y": 24,

									"width": 64,
									"height": 16,

									"children": (
										{
											"name": "main_text",
											"type": "text",

											"x": -55,
											"y": 0,

											"text": uiScriptLocale.ITEMSHOP_EDITOR_ITEM_ATTR_VALUE_TEXT % 1,
										},
										{
											"name": "attr_value_text_01",
											"type": "editline",

											"x": 5,
											"y": 0,

											"width": 64,
											"height": 16,

											"input_limit": 5,

											"only_number" : True,
										},
									),

								},
								{
									"name": "attr_value_window_02",
									"type": "thinboardcircle",

									"x": 16 + 46 + 184 + 16 + 64,
									"y": 24 + 26 * 1,

									"width": 64,
									"height": 16,

									"children": (
										{
											"name": "main_text",
											"type": "text",

											"x": -55,
											"y": 0,

											"text": uiScriptLocale.ITEMSHOP_EDITOR_ITEM_ATTR_VALUE_TEXT % 2,
										},
										{
											"name": "attr_value_text_02",
											"type": "editline",

											"x": 5,
											"y": 0,

											"width": 64,
											"height": 16,

											"input_limit": 5,

											"only_number": True,
										},
									),

								},
								{
									"name": "attr_value_window_03",
									"type": "thinboardcircle",

									"x": 16 + 46 + 184 + 16 + 64,
									"y": 24 + 26 * 2,

									"width": 64,
									"height": 16,

									"children": (
										{
											"name": "main_text",
											"type": "text",

											"x": -55,
											"y": 0,

											"text": uiScriptLocale.ITEMSHOP_EDITOR_ITEM_ATTR_VALUE_TEXT % 3,
										},
										{
											"name": "attr_value_text_03",
											"type": "editline",

											"x": 5,
											"y": 0,

											"width": 64,
											"height": 16,

											"input_limit": 5,

											"only_number": True,
										},
									),

								},
								{
									"name": "attr_value_window_04",
									"type": "thinboardcircle",

									"x": 16 + 46 + 184 + 16 + 64,
									"y": 24 + 26 * 3,

									"width": 64,
									"height": 16,

									"children": (
										{
											"name": "main_text",
											"type": "text",

											"x": -55,
											"y": 0,

											"text": uiScriptLocale.ITEMSHOP_EDITOR_ITEM_ATTR_VALUE_TEXT % 4,
										},
										{
											"name": "attr_value_text_04",
											"type": "editline",

											"x": 5,
											"y": 0,

											"width": 64,
											"height": 16,

											"input_limit": 5,

											"only_number": True,
										},
									),

								},
								{
									"name": "attr_value_window_05",
									"type": "thinboardcircle",

									"x": 16 + 46 + 184 + 16 + 64,
									"y": 24 + 26 * 4,

									"width": 64,
									"height": 16,

									"children": (
										{
											"name": "main_text",
											"type": "text",

											"x": -55,
											"y": 0,

											"text": uiScriptLocale.ITEMSHOP_EDITOR_ITEM_ATTR_VALUE_TEXT % 5,
										},
										{
											"name": "attr_value_text_05",
											"type": "editline",

											"x": 5,
											"y": 0,

											"width": 64,
											"height": 16,

											"input_limit": 5,

											"only_number": True,
										},
									),
								},
								{
									"name": "attr_value_window_06",
									"type": "thinboardcircle",

									"x": 16 + 46 + 184 + 16 + 64,
									"y": 24 + 26 * 5,

									"width": 64,
									"height": 16,

									"children": (
										{
											"name": "main_text",
											"type": "text",

											"x": -55,
											"y": 0,

											"text": uiScriptLocale.ITEMSHOP_EDITOR_ITEM_ATTR_VALUE_TEXT % 6,
										},
										{
											"name": "attr_value_text_06",
											"type": "editline",

											"x": 5,
											"y": 0,

											"width": 64,
											"height": 16,

											"input_limit": 5,

											"only_number": True,
										},
									),
								},
								{
									"name": "attr_value_window_07",
									"type": "thinboardcircle",

									"x": 16 + 46 + 184 + 16 + 64,
									"y": 24 + 26 * 6,

									"width": 64,
									"height": 16,

									"children": (
										{
											"name": "main_text",
											"type": "text",

											"x": -55,
											"y": 0,

											"text": uiScriptLocale.ITEMSHOP_EDITOR_ITEM_ATTR_VALUE_TEXT % 7,
										},
										{
											"name": "attr_value_text_07",
											"type": "editline",

											"x": 5,
											"y": 0,

											"width": 64,
											"height": 16,

											"input_limit": 5,

											"only_number": True,
										},
									),
								},
							),
						},
						{
							"name": "edit_button",
							"type": "button",

							"x": -60,
							"y": 35,

							"text": uiScriptLocale.ITEMSHOP_EDITOR_EDIT_ITEM,
							"horizontal_align": "center",
							"vertical_align": "bottom",

							"default_image": "d:/ymir work/ui/public/large_Button_01.sub",
							"over_image": "d:/ymir work/ui/public/large_Button_02.sub",
							"down_image": "d:/ymir work/ui/public/large_Button_03.sub",
						},
						{
							"name": "delete_button",
							"type": "button",

							"x": 60,
							"y": 35,

							"text": uiScriptLocale.ITEMSHOP_EDITOR_DELETE_ITEM,
							"horizontal_align": "center",
							"vertical_align": "bottom",

							"default_image": "d:/ymir work/ui/public/large_Button_01.sub",
							"over_image": "d:/ymir work/ui/public/large_Button_02.sub",
							"down_image": "d:/ymir work/ui/public/large_Button_03.sub",
						},
						{
							"name": "add_button",
							"type": "button",

							"x": 0,
							"y": 35,

							"text": uiScriptLocale.ITEMSHOP_EDITOR_ADD_ITEM,
							"horizontal_align": "center",
							"vertical_align": "bottom",

							"default_image": "d:/ymir work/ui/public/large_Button_01.sub",
							"over_image": "d:/ymir work/ui/public/large_Button_02.sub",
							"down_image": "d:/ymir work/ui/public/large_Button_03.sub",
						},
					),
				},
			),
		},
	),
}