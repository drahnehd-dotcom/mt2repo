import localeInfo
import uiScriptLocale

LOCALE_PATH = uiScriptLocale.WINDOWS_PATH
ICON_SLOT_FILE = "d:/ymir work/ui/public/Slot_Base.sub"

WINDOW_SIZE = (400, 442)

window = {
	"name" : "CubeWindow",

	"x" : SCREEN_WIDTH - 176 - 200 - 80,
	"y" : SCREEN_HEIGHT - 37 - 563,


	"style" : ("movable", "float",),

	"width" : WINDOW_SIZE[0],
	"height" : WINDOW_SIZE[1],

	"children" :
	(
		{
			"name" : "board",
			"type" : "board_with_titlebar",
			"style" : ("attach",),

			"x" : 0,
			"y" : 0,

			"width" : WINDOW_SIZE[0],
			"height" : WINDOW_SIZE[1],
            
			"title" : uiScriptLocale.CUBE_TITLE,

			"children" :
			(
                {
                    "name" : "SlotBarAchiev",
                    "type" : "image",
                    
					"x" : 100,
                    "y" : 370,
                    
					"image" : "Assets/ui/cube/slotbar-empty.png",
                    "children" : (
						{
							"name" : "NeedAchiev",
							"type" : "text",

							"x" : 5,
							"y" : 0,

							"horizontal_align" : "right",
							"text_horizontal_align" : "right",

							"text" : localeInfo.NumberToMoneyString(0),
						},
					),
				},

                {
                    "name" : "SlotBarMoney",
                    "type" : "image",
                    
					"x" : 100,
                    "y" : 390,
                    
					"image" : "Assets/ui/cube/slotbar-empty.png",
                    "children" : (
						{
							"name" : "NeedMoney",
							"type" : "text",

							"x" : 5,
							"y" : 0,

							"horizontal_align" : "right",
							"text_horizontal_align" : "right",

							"text" : "",
						},
					),
				},

                {
                    "name" : "SlotBarCheque",
                    "type" : "image",
                    
					"x" : 100,
                    "y" : 390 + 20,
                    
					"image" : "Assets/ui/cube/slotbar-empty.png",
                    "children" : (
						{
							"name" : "NeedCheque",
							"type" : "text",

							"x" : 5,
							"y" : 0,

							"horizontal_align" : "right",
							"text_horizontal_align" : "right",

							"text" : "",
						},
					),
				},


				{
					"name" : "percentage",
					"type" : "text",
					
					"x" : 360,
					"y" : 390,
					
					"text" : "",
				},
				
				{
                    "name" : "CategoryThin",
                    "type" : "thinboard_circle",
                    
					"x" : 10,
                    "y" : 40,
                    
					"width" : 380,
                    "height" : 200,
				},
				{
					"name": "CubeManager-CategoryContainer",
					"type": "listboxex",
					
					"x": 50,
					"y": 60,
					
					"width": 290,
					"height": 170,
					
					"itemsize_x": 290,
					"itemsize_y": 31,
					"itemstep": 31,
					"viewcount": 170 / 31,
				},

				{
					"name" : "CubeManager-CategoryScrollbar",
					"type" : "modern_scrollbar",

					"x" : 375,
					"y": 60,
					
					"content_height": 60 * 30,
					"size": 170,
					
					"width": 7,
				},

				{
					"name" : "CubeManager-RewardSlot",
					"type" : "grid_table",

					"x" : 50, "y" : 245,

					"start_index" : 0,
					"x_count" : 1,
					"y_count" : 3,
					"x_step" : 40,
					"y_step" : 32,

					"image" : "Assets/ui/cube/slot-reward.png",
				},

				{
					"name" : "result1board",
					"type" : "window",
					
					"x" : 100,
					"y" : 245,
					
					"width" : 200,
					"height" : 96,
                    
					"color" : 0xFFffffff,

					"children" : 
					(
						{
							"name" : "material11", 
							"type" : "grid_table",
							"start_index" : 0,
						
							"x_count" : 1,
							"y_count" : 3,
							"x_step" : 32,
							"y_step" : 32,

							"x" : 0,
							"y" : 0,
							"image" : "Assets/ui/cube/slot-item.png",

							"children" : (
								{
									"name" : "material_qty_window_1",
									"type" : "image",
									"x" : -5, "y" : 0,
									"image" : "Assets/ui/cube/input-count.png",
                                    "vertical_align" : "bottom",
									"children" :
									(
										{
											"name" : "material_qty_text_1",
											"type" : "text", "text" : "",
											"x" : 0, "y" : 0, "all_align" : "center",
										},
									)
								},
							),
						},
						{
							"name" : "material12", 
							"type" : "grid_table",
							"start_index" : 0,
						
							"x_count" : 1,
							"y_count" : 3,
							"x_step" : 32,
							"y_step" : 32,

							"x" : (32 + 8) * 1,
							"y" : 0,
							"image" : "Assets/ui/cube/slot-item.png",

							"children" : (
								{
									"name" : "material_qty_window_2",
									"type" : "image",
									"x" : -5, "y" : 0,
									"image" : "Assets/ui/cube/input-count.png",
                                    "vertical_align" : "bottom",
									"children" :
									(
										{
											"name" : "material_qty_text_2",
											"type" : "text", "text" : "",
											"x" : 0, "y" : 0, "all_align" : "center",
										},
									)
								},
							),
						},
						{
							"name" : "material13", 
							"type" : "grid_table",
							"start_index" : 0,
						
							"x_count" : 1,
							"y_count" : 3,
							"x_step" : 32,
							"y_step" : 32,

							"x" : (32 + 8) * 2,
							"y" : 0,
                            
							"image" : "Assets/ui/cube/slot-item.png",
							"children" : (
								{
									"name" : "material_qty_window_3",
									"type" : "image",
									"x" : -5, "y" : 0,
									"image" : "Assets/ui/cube/input-count.png",
                                    "vertical_align" : "bottom",
									"children" :
									(
										{
											"name" : "material_qty_text_3",
											"type" : "text", "text" : "",
											"x" : 0, "y" : 0, "all_align" : "center",
										},
									)
								},
							),
						},
						{
							"name" : "material14", 
							"type" : "grid_table",
							"start_index" : 0,
						
							"x_count" : 1,
							"y_count" : 3,
							"x_step" : 32,
							"y_step" : 32,

							"x" : (32 + 8) * 3,
							"y" : 0,
							"image" : "Assets/ui/cube/slot-item.png",

							"children" : (
								{
									"name" : "material_qty_window_4",
									"type" : "image",
									"x" : -5, "y" : 0,
									"image" : "Assets/ui/cube/input-count.png",
                                    "vertical_align" : "bottom",
									"children" :
									(
										{
											"name" : "material_qty_text_4",
											"type" : "text", "text" : "",
											"x" : 0, "y" : 0, "all_align" : "center",
										},
									)
								},
							),
						},
						{
							"name" : "material15", 
							"type" : "grid_table",
							"start_index" : 0,
						
							"x_count" : 1,
							"y_count" : 3,
							"x_step" : 32,
							"y_step" : 32,

							"x" : (32 + 8) * 4,
							"y" : 0,
							"image" : "Assets/ui/cube/slot-item.png",

							"children" : (
								{
									"name" : "material_qty_window_5",
									"type" : "image",
									"x" : -5, "y" : 0,
									"image" : "Assets/ui/cube/input-count.png",
                                    "vertical_align" : "bottom",
									"children" :
									(
										{
											"name" : "material_qty_text_5",
											"type" : "text", "text" : "",
											"x" : 0, "y" : 0, "all_align" : "center",
										},
									)
								},
							),
						},
						{
							"name" : "material16", 
							"type" : "grid_table",
							"start_index" : 0,
						
							"x_count" : 1,
							"y_count" : 3,
							"x_step" : 32,
							"y_step" : 32,

							"x" : (32 + 8) * 5,
							"y" : 0,
							"image" : "Assets/ui/cube/slot-item.png",

							"children" : (
								{
									"name" : "material_qty_window_6",
									"type" : "image",
									"x" : -5, "y" : 0,
									"image" : "Assets/ui/cube/input-count.png",
                                    "vertical_align" : "bottom",
									"children" :
									(
										{
											"name" : "material_qty_text_6",
											"type" : "text", "text" : "",
											"x" : 0, "y" : 0, "all_align" : "center",
										},
									)
								},
							),
						},
						{
							"name" : "material17", 
							"type" : "grid_table",
							"start_index" : 0,
						
							"x_count" : 1,
							"y_count" : 3,
							"x_step" : 32,
							"y_step" : 32,

							"x" : (32 + 8) * 6,
							"y" : 0,
							"image" : "Assets/ui/cube/slot-item.png",

							"children" : (
								{
									"name" : "material_qty_window_7",
									"type" : "image",
									"x" : -5, "y" : 0,
									"image" : "Assets/ui/cube/input-count.png",
                                    "vertical_align" : "bottom",
									"children" :
									(
										{
											"name" : "material_qty_text_7",
											"type" : "text", "text" : "",
											"x" : 0, "y" : 0, "all_align" : "center",
										},
									)
								},
							),
						},
					),
				},

				{
					"name" : "craft_count_window",
					"type" : "window",
					"x" : 12, "y" : 287,
					"width"	: 32, "height" : 19,
					"children" :
					(
						{
							"name" : "craft_count_text",
							"type" : "editline",
                            "x" : 16, "y" : 3,
							"width" : 32, "height" : 19,
                            "input_limit" : 3,
                            
							"text_horizontal_align"  :"center",
                            "horizontal_align" : "center",
                            "limit_width" : 32,

							"text" : "",
						},
					)
				},

				{
					"name" : "increase_button",
					"type" : "button",

					"x" : 20,
					"y" : 270,

					"default_image" : "Assets/ui/cube/btn_move_up.png",
					"over_image" : "Assets/ui/cube/btn_move_up_hover.png",
					"down_image" : "Assets/ui/cube/btn_move_up_clicked.png",
				},
				
				{
					"name" : "decrease_button",
					"type" : "button",

					"x" : 20,
					"y" : 310,

					"default_image" : "Assets/ui/cube/btn_move_down.png",
					"over_image" : "Assets/ui/cube/btn_move_down_hover.png",
					"down_image" : "Assets/ui/cube/btn_move_down_clicked.png",
				},
			

				{
					"name": "CubeManager-ChanceSlot",
					"type": "slot",

					"x": 85,
					"y": 375,

					"width": 32,
					"height": 32,

					"slot" : (
						{"index": 0, "x": 0, "y": 0, "width": 32, "height": 32},
					),
				},

				{
					"name" : "AcceptAllButton",
					"type" : "button",

					"x" : 280,
					"y" : 40,
					"vertical_align" : "bottom",

					"text" : uiScriptLocale.CUBE_CRAFT_100,

					"default_image" : "Assets/ui/cube/button_ac_normal.png",
					"over_image" : "Assets/ui/cube/button_ac_light.png",
					"down_image" : "Assets/ui/cube/button_ac_push.png",
				},
				{
					"name" : "AcceptButton",
					"type" : "button",

					"x" : 280,
					"y" : 75,
					"vertical_align" : "bottom",

					"text" : uiScriptLocale.CUBE_CRAFT,

					"default_image" : "Assets/ui/cube/button_ac_normal.png",
					"over_image" : "Assets/ui/cube/button_ac_light.png",
					"down_image" : "Assets/ui/cube/button_ac_push.png",
				},
			),
		},
	),
}
