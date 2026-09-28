import uiScriptLocale
import item
import app

import player
EQUIPMENT_START_INDEX = player.EQUIPMENT_SLOT_START

if app.ENABLE_EXTEND_INVEN_SYSTEM and app.ENABLE_CHEQUE_SYSTEM:
	window = {
		"name" : "InventoryWindow",

		"x" : SCREEN_WIDTH - 176,
		"y" : SCREEN_HEIGHT - 37 - 572,

		"style" : ("movable", "float",),

		"width" : 176,
		"height" : 585,

		"children" :
		(
			{
				"name" : "board",
				"type" : "board",
				"style" : ("attach",),

				"x" : 0,
				"y" : 0,

				"width" : 176,
				"height" : 585+20,

				"children" :
				(
					{
						"name" : "TitleBar",
						"type" : "titlebar",
						"style" : ("attach",),

						"x" : 8,
						"y" : 7,

						"width" : 161,
						"color" : "yellow",

						"children" :
						(
							{ "name":"TitleName", "type":"text", "x":81, "y":0, "text":uiScriptLocale.INVENTORY_TITLE, "text_horizontal_align":"center","outline":"1" },
						),
					},

					{
						"name" : "RefreshButton",
						"type" : "button",

						"x" : 19,
						"y" : 10,

						"tooltip_text_new" : uiScriptLocale.INVENTORY_EX_STACK_ITEMS,
						"tooltip_text_color" : 0xfff1e6c0,
						"tooltip_x" : 0,
						"tooltip_y" : -35,

						"default_image" : "d:/ymir work/ui/item_stack_btn0.png",
						"over_image" : "d:/ymir work/ui/item_stack_btn1.png",
						"down_image" : "d:/ymir work/ui/item_stack_btn2.png",
					},

					{
						"name" : "Equipment_Base",
						"type" : "image",

						"x" : 10,
						"y" : 33,

						"image" : "d:/ymir work/ui/equipment_bg_without_ring.tga",

						"children" :
						(

							{
								"name" : "EquipmentSlot",
								"type" : "slot",

								"x" : 3,
								"y" : 3,

								"width" : 150,
								"height" : 182,

								"slot" : (
											{"index":item.EQUIPMENT_BODY, "x":39, "y":37, "width":32, "height":64},
											{"index":item.EQUIPMENT_HEAD, "x":39, "y":2, "width":32, "height":32},
											{"index":item.EQUIPMENT_SHOES, "x":39, "y":145, "width":32, "height":32},
											{"index":item.EQUIPMENT_WRIST, "x":75, "y":67, "width":32, "height":32},
											{"index":item.EQUIPMENT_WEAPON, "x":3, "y":3, "width":32, "height":96},
											{"index":item.EQUIPMENT_NECK, "x":114, "y":67, "width":32, "height":32},
											{"index":item.EQUIPMENT_EAR, "x":114, "y":35, "width":32, "height":32},
											{"index":item.EQUIPMENT_UNIQUE1, "x":2, "y":145, "width":32, "height":32},
											{"index":item.EQUIPMENT_UNIQUE2, "x":75, "y":145, "width":32, "height":32},
											{"index":item.EQUIPMENT_ARROW, "x":114, "y":2, "width":32, "height":32},
											{"index":item.EQUIPMENT_SHIELD, "x":75, "y":35, "width":32, "height":32},
											{"index":item.EQUIPMENT_RING1, "x":2, "y":106, "width":32, "height":32},
											{"index":item.EQUIPMENT_RING2, "x":75, "y":106, "width":32, "height":32},
											{"index":item.EQUIPMENT_BELT, "x":39, "y":106, "width":32, "height":32}
										),
							},
							{
								"name" : "DSSButton",
								"type" : "button",

								"x" : 114,
								"y" : 107,

								"tooltip_text_new" : uiScriptLocale.INVENTORY_EX_ALCHEMY,
								"tooltip_text_color" : 0xfff1e6c0,
								"tooltip_x" : 0,
								"tooltip_y" : -35,

								"default_image" : "d:/ymir work/ui/dragonsoul/dss_inventory_button_01.tga",
								"over_image" : "d:/ymir work/ui/dragonsoul/dss_inventory_button_02.tga",
								"down_image" : "d:/ymir work/ui/dragonsoul/dss_inventory_button_03.tga",
							},
							{
								"name" : "MallButton",
								"type" : "button",

								"x" : 118,
								"y" : 148,

								"tooltip_text" : uiScriptLocale.MALL_TITLE,

								"default_image" : "d:/ymir work/ui/game/TaskBar/Mall_Button_01.tga",
								"over_image" : "d:/ymir work/ui/game/TaskBar/Mall_Button_02.tga",
								"down_image" : "d:/ymir work/ui/game/TaskBar/Mall_Button_03.tga",
							},
							{
								"name" : "CostumeButton",
								"type" : "button",

								"x" : 78,
								"y" : 5,

								"tooltip_text_new" : uiScriptLocale.COSTUME_TITLE,
								"tooltip_text_color" : 0xfff1e6c0,
								"tooltip_x" : 0,
								"tooltip_y" : -35,

								"default_image" : "d:/ymir work/ui/game/taskbar/costume_Button_01.tga",
								"over_image" : "d:/ymir work/ui/game/taskbar/costume_Button_02.tga",
								"down_image" : "d:/ymir work/ui/game/taskbar/costume_Button_03.tga",
							},
							{
								"name" : "Equipment_Tab_01",
								"type" : "radio_button",

								"x" : 86,
								"y" : 161,

								"default_image" : "d:/ymir work/ui/game/windows/tab_button_small_01.sub",
								"over_image" : "d:/ymir work/ui/game/windows/tab_button_small_02.sub",
								"down_image" : "d:/ymir work/ui/game/windows/tab_button_small_03.sub",

								"children" :
								(
									{
										"name" : "Equipment_Tab_01_Print",
										"type" : "text",

										"x" : 0,
										"y" : 0,

										"all_align" : "center",

										"text" : "I",
									},
								),
							},
							{
								"name" : "Equipment_Tab_02",
								"type" : "radio_button",

								"x" : 86 + 32,
								"y" : 161,

								"default_image" : "d:/ymir work/ui/game/windows/tab_button_small_01.sub",
								"over_image" : "d:/ymir work/ui/game/windows/tab_button_small_02.sub",
								"down_image" : "d:/ymir work/ui/game/windows/tab_button_small_03.sub",

								"children" :
								(
									{
										"name" : "Equipment_Tab_02_Print",
										"type" : "text",

										"x" : 0,
										"y" : 0,

										"all_align" : "center",

										"text" : "II",
									},
								),
							},

						),
					},

					{
						"name" : "Inventory_Tab_01",
						"type" : "radio_button",

						"x" : 10,
						"y" : 33 + 191,

						"default_image" : "d:/ymir work/ui/game/windows/tab_button_large_half_01.sub",
						"over_image" : "d:/ymir work/ui/game/windows/tab_button_large_half_02.sub",
						"down_image" : "d:/ymir work/ui/game/windows/tab_button_large_half_03.sub",

						"children" :
						(
							{
								"name" : "Inventory_Tab_01_Print",
								"type" : "text",

								"x" : 0,
								"y" : 0,

								"all_align" : "center",

								"text" : "I",
								"outline":"1",
							},
						),
					},
					{
						"name" : "Inventory_Tab_02",
						"type" : "radio_button",

						"x" : 10 + 39,
						"y" : 33 + 191,

						"default_image" : "d:/ymir work/ui/game/windows/tab_button_large_half_01.sub",
						"over_image" : "d:/ymir work/ui/game/windows/tab_button_large_half_02.sub",
						"down_image" : "d:/ymir work/ui/game/windows/tab_button_large_half_03.sub",

						"children" :
						(
							{
								"name" : "Inventory_Tab_02_Print",
								"type" : "text",

								"x" : 0,
								"y" : 0,

								"all_align" : "center",

								"text" : "II",
								"outline":"1",
							},
						),
					},

					{
						"name" : "Inventory_Tab_03",
						"type" : "radio_button",

						"x" : 10 + 39 + 39,
						"y" : 33 + 191,

						"default_image" : "d:/ymir work/ui/game/windows/tab_button_large_half_01.sub",
						"over_image" : "d:/ymir work/ui/game/windows/tab_button_large_half_02.sub",
						"down_image" : "d:/ymir work/ui/game/windows/tab_button_large_half_03.sub",

						"children" :
						(
							{
								"name" : "Inventory_Tab_03_Print",
								"type" : "text",

								"x" : 0,
								"y" : 0,

								"all_align" : "center",

								"text" : "III",
								"outline":"1",
							},
						),
					},

					{
						"name" : "Inventory_Tab_04",
						"type" : "radio_button",

						"x" : 10 + 39 + 39 + 39,
						"y" : 33 + 191,

						"default_image" : "d:/ymir work/ui/game/windows/tab_button_large_half_01.sub",
						"over_image" : "d:/ymir work/ui/game/windows/tab_button_large_half_02.sub",
						"down_image" : "d:/ymir work/ui/game/windows/tab_button_large_half_03.sub",

						"children" :
						(
							{
								"name" : "Inventory_Tab_04_Print",
								"type" : "text",

								"x" : 0,
								"y" : 0,

								"all_align" : "center",

								"text" : "IV",
								"outline":"1",
							},
						),
					},

					{
						"name" : "ItemSlot",
						"type" : "grid_table",

						"x" : 8,
						"y" : 246,

						"start_index" : 0,
						"x_count" : 5,
						"y_count" : 9,
						"x_step" : 32,
						"y_step" : 32,

						"image" : "d:/ymir work/ui/public/Slot_Base.sub"
					},

					{
						"name":"Money_Icon",
						"type":"image",
						"vertical_align":"bottom",

						"x":12,
						"y":66,

						"image":"d:/ymir work/ui/game/windows/money_icon.sub",
					},
					{
						"name":"Cheque_Icon",
						"type":"image",

						"x":12,
						"y":46,
						"vertical_align":"bottom",
						"image":"d:/ymir work/ui/game/windows/cheque_icon.sub",
					},
					{
						"name":"Pkt_Osiag_Icon",
						"type":"image",

						"x":12,
						"y":26,
						"vertical_align":"bottom",
						"image":"d:/ymir work/ui/stone_point/stone_point.tga",
					},
					{
						"name":"Money_Slot",
						"type":"button",

						"x":32,
						"y":68,

						"vertical_align":"bottom",

						"default_image" : "d:/ymir work/ui/public/parameter_slot_05.sub",
						"over_image" : "d:/ymir work/ui/public/parameter_slot_05.sub",
						"down_image" : "d:/ymir work/ui/public/parameter_slot_05.sub",

						"children" :
						(
							{
								"name" : "Money",
								"type" : "text",

								"x" : 3,
								"y" : 3,

								"horizontal_align" : "right",
								"text_horizontal_align" : "right",

								"text" : "123456789",
							},
						),
					},
					{
						"name":"Cheque_Slot",
						"type":"button",

						"x":32,
						"y":48,

						"default_image" : "d:/ymir work/ui/public/parameter_slot_05.sub",
						"over_image" : "d:/ymir work/ui/public/parameter_slot_05.sub",
						"down_image" : "d:/ymir work/ui/public/parameter_slot_05.sub",
						"vertical_align":"bottom",
						"children" :
						(
							{
								"name" : "Cheque",
								"type" : "text",

								"x" : 3,
								"y" : 3,

								"horizontal_align" : "right",
								"text_horizontal_align" : "right",

								"text" : "99",
							},
						),
					},
					{
						"name":"Pkt_Osiag_Slot",
						"type":"button",

						"x":32,
						"y":28,

						"default_image" : "d:/ymir work/ui/public/parameter_slot_05.sub",
						"over_image" : "d:/ymir work/ui/public/parameter_slot_05.sub",
						"down_image" : "d:/ymir work/ui/public/parameter_slot_05.sub",
						"vertical_align":"bottom",
						"children" :
						(
							{
								"name" : "Pkt_Osiag",
								"type" : "text",

								"x" : 3,
								"y" : 3,

								"horizontal_align" : "right",
								"text_horizontal_align" : "right",

								"text" : "99",
							},
						),
					},
				),
			},
		),
	}
elif app.ENABLE_EXTEND_INVEN_SYSTEM and not app.ENABLE_CHEQUE_SYSTEM:
	window = {
		"name" : "InventoryWindow",

		"x" : SCREEN_WIDTH - 176,
		"y" : SCREEN_HEIGHT - 37 - 565,

		"style" : ("movable", "float",),

		"width" : 176,
		"height" : 565,

		"children" :
		(
			{
				"name" : "board",
				"type" : "board",
				"style" : ("attach",),

				"x" : 0,
				"y" : 0,

				"width" : 176,
				"height" : 565,

				"children" :
				(
					{
						"name" : "TitleBar",
						"type" : "titlebar",
						"style" : ("attach",),

						"x" : 8,
						"y" : 7,

						"width" : 161,
						"color" : "yellow",

						"children" :
						(
							{ "name":"TitleName", "type":"text", "x":81, "y":0, "text":uiScriptLocale.INVENTORY_TITLE, "text_horizontal_align":"center","outline":"1" },
						),
					},

					{
						"name" : "RefreshButton",
						"type" : "button",

						"x" : 8,
						"y" : 7,

						"tooltip_text_new" : uiScriptLocale.INVENTORY_EX_STACK_ITEMS,
						"tooltip_text_color" : 0xfff1e6c0,
						"tooltip_x" : 0,
						"tooltip_y" : -35,

						"default_image" : "d:/ymir work/ui/pattern/titlebar_inv_refresh_baseframe.tga",
						"over_image" : "d:/ymir work/ui/pattern/titlebar_inv_refresh_baseframe1.tga",
						"down_image" : "d:/ymir work/ui/pattern/titlebar_inv_refresh_baseframe2.tga",
					},

					{
						"name" : "Equipment_Base",
						"type" : "image",

						"x" : 10,
						"y" : 33,

						"image" : "d:/ymir work/ui/equipment_bg_without_ring.tga",

						"children" :
						(

							{
								"name" : "EquipmentSlot",
								"type" : "slot",

								"x" : 3,
								"y" : 3,

								"width" : 150,
								"height" : 182,

								"slot" : (
											{"index":EQUIPMENT_START_INDEX+0, "x":39, "y":37, "width":32, "height":64},
											{"index":EQUIPMENT_START_INDEX+1, "x":39, "y":2, "width":32, "height":32},
											{"index":EQUIPMENT_START_INDEX+2, "x":39, "y":145, "width":32, "height":32},
											{"index":EQUIPMENT_START_INDEX+3, "x":75, "y":67, "width":32, "height":32},
											{"index":EQUIPMENT_START_INDEX+4, "x":3, "y":3, "width":32, "height":96},
											{"index":EQUIPMENT_START_INDEX+5, "x":114, "y":67, "width":32, "height":32},
											{"index":EQUIPMENT_START_INDEX+6, "x":114, "y":35, "width":32, "height":32},
											{"index":EQUIPMENT_START_INDEX+7, "x":2, "y":145, "width":32, "height":32},
											{"index":EQUIPMENT_START_INDEX+8, "x":75, "y":145, "width":32, "height":32},
											{"index":EQUIPMENT_START_INDEX+9, "x":114, "y":2, "width":32, "height":32},
											{"index":EQUIPMENT_START_INDEX+10, "x":75, "y":35, "width":32, "height":32},
											{"index":item.EQUIPMENT_BELT, "x":39, "y":106, "width":32, "height":32},
										),
							},
							{
								"name" : "DSSButton",
								"type" : "button",

								"x" : 114,
								"y" : 107,

								"tooltip_text_new" : uiScriptLocale.INVENTORY_EX_ALCHEMY,
								"tooltip_text_color" : 0xfff1e6c0,
								"tooltip_x" : 0,
								"tooltip_y" : -35,

								"default_image" : "d:/ymir work/ui/dragonsoul/dss_inventory_button_01.tga",
								"over_image" : "d:/ymir work/ui/dragonsoul/dss_inventory_button_02.tga",
								"down_image" : "d:/ymir work/ui/dragonsoul/dss_inventory_button_03.tga",
							},
							{
								"name" : "MallButton",
								"type" : "button",

								"x" : 118,
								"y" : 148,

								"tooltip_text" : uiScriptLocale.MALL_TITLE,

								"default_image" : "d:/ymir work/ui/game/TaskBar/Mall_Button_01.tga",
								"over_image" : "d:/ymir work/ui/game/TaskBar/Mall_Button_02.tga",
								"down_image" : "d:/ymir work/ui/game/TaskBar/Mall_Button_03.tga",
							},
							{
								"name" : "CostumeButton",
								"type" : "button",

								"x" : 78,
								"y" : 5,

								"tooltip_text_new" : "test\ntest",
								"tooltip_text_color" : 0xfff1e6c0,
								"tooltip_x" : 0,
								"tooltip_y" : -35,

								"default_image" : "d:/ymir work/ui/game/taskbar/costume_Button_01.tga",
								"over_image" : "d:/ymir work/ui/game/taskbar/costume_Button_02.tga",
								"down_image" : "d:/ymir work/ui/game/taskbar/costume_Button_03.tga",
							},
							{
								"name" : "Equipment_Tab_01",
								"type" : "radio_button",

								"x" : 86,
								"y" : 161,

								"default_image" : "d:/ymir work/ui/game/windows/tab_button_small_01.sub",
								"over_image" : "d:/ymir work/ui/game/windows/tab_button_small_02.sub",
								"down_image" : "d:/ymir work/ui/game/windows/tab_button_small_03.sub",

								"children" :
								(
									{
										"name" : "Equipment_Tab_01_Print",
										"type" : "text",

										"x" : 0,
										"y" : 0,

										"all_align" : "center",

										"text" : "I",
									},
								),
							},
							{
								"name" : "Equipment_Tab_02",
								"type" : "radio_button",

								"x" : 86 + 32,
								"y" : 161,

								"default_image" : "d:/ymir work/ui/game/windows/tab_button_small_01.sub",
								"over_image" : "d:/ymir work/ui/game/windows/tab_button_small_02.sub",
								"down_image" : "d:/ymir work/ui/game/windows/tab_button_small_03.sub",

								"children" :
								(
									{
										"name" : "Equipment_Tab_02_Print",
										"type" : "text",

										"x" : 0,
										"y" : 0,

										"all_align" : "center",

										"text" : "II",
									},
								),
							},

						),
					},

					{
						"name" : "Inventory_Tab_01",
						"type" : "radio_button",

						"x" : 10,
						"y" : 33 + 191,

						"default_image" : "d:/ymir work/ui/game/windows/tab_button_large_half_01.sub",
						"over_image" : "d:/ymir work/ui/game/windows/tab_button_large_half_02.sub",
						"down_image" : "d:/ymir work/ui/game/windows/tab_button_large_half_03.sub",

						"children" :
						(
							{
								"name" : "Inventory_Tab_01_Print",
								"type" : "text",

								"x" : 0,
								"y" : 0,

								"all_align" : "center",

								"text" : "I",
								"outline":"1",
							},
						),
					},
					{
						"name" : "Inventory_Tab_02",
						"type" : "radio_button",

						"x" : 10 + 39,
						"y" : 33 + 191,

						"default_image" : "d:/ymir work/ui/game/windows/tab_button_large_half_01.sub",
						"over_image" : "d:/ymir work/ui/game/windows/tab_button_large_half_02.sub",
						"down_image" : "d:/ymir work/ui/game/windows/tab_button_large_half_03.sub",

						"children" :
						(
							{
								"name" : "Inventory_Tab_02_Print",
								"type" : "text",

								"x" : 0,
								"y" : 0,

								"all_align" : "center",

								"text" : "II",
								"outline":"1",
							},
						),
					},

					{
						"name" : "Inventory_Tab_03",
						"type" : "radio_button",

						"x" : 10 + 39 + 39,
						"y" : 33 + 191,

						"default_image" : "d:/ymir work/ui/game/windows/tab_button_large_half_01.sub",
						"over_image" : "d:/ymir work/ui/game/windows/tab_button_large_half_02.sub",
						"down_image" : "d:/ymir work/ui/game/windows/tab_button_large_half_03.sub",

						"children" :
						(
							{
								"name" : "Inventory_Tab_03_Print",
								"type" : "text",

								"x" : 0,
								"y" : 0,

								"all_align" : "center",

								"text" : "III",
								"outline":"1",
							},
						),
					},

					{
						"name" : "Inventory_Tab_04",
						"type" : "radio_button",

						"x" : 10 + 39 + 39 + 39,
						"y" : 33 + 191,

						"default_image" : "d:/ymir work/ui/game/windows/tab_button_large_half_01.sub",
						"over_image" : "d:/ymir work/ui/game/windows/tab_button_large_half_02.sub",
						"down_image" : "d:/ymir work/ui/game/windows/tab_button_large_half_03.sub",

						"children" :
						(
							{
								"name" : "Inventory_Tab_04_Print",
								"type" : "text",

								"x" : 0,
								"y" : 0,

								"all_align" : "center",

								"text" : "IV",
								"outline":"1",
							},
						),
					},

					{
						"name" : "ItemSlot",
						"type" : "grid_table",

						"x" : 8,
						"y" : 246,

						"start_index" : 0,
						"x_count" : 5,
						"y_count" : 9,
						"x_step" : 32,
						"y_step" : 32,

						"image" : "d:/ymir work/ui/public/Slot_Base.sub"
					},

					{
						"name":"Money_Icon",
						"type":"image",

						"x":10,
						"y":26,

						"image":"d:/ymir work/ui/game/windows/money_icon.sub",
					},
					{
						"name":"Cheque_Icon",
						"type":"image",
						"vertical_align":"bottom",
						
						"x":10,
						"y":46,

						"image":"d:/ymir work/ui/game/windows/cheque_icon.sub",
					},

					{
						"name":"Money_Slot",
						"type":"button",

						"x":28,
						"y":28,

						"horizontal_align":"center",
						"vertical_align":"bottom",

						"default_image" : "d:/ymir work/ui/public/parameter_slot_05.sub",
						"over_image" : "d:/ymir work/ui/public/parameter_slot_05.sub",
						"down_image" : "d:/ymir work/ui/public/parameter_slot_05.sub",

						"children" :
						(
							{
								"name" : "Money",
								"type" : "text",

								"x" : 3,
								"y" : 3,

								"horizontal_align" : "right",
								"text_horizontal_align" : "right",

								"text" : "123456789",
							},
						),
					},
					{
						"name":"Cheque_Slot",
						"type":"button",

						"x":28,
						"y":48,

						"vertical_align":"bottom",

						"default_image" : "d:/ymir work/ui/public/cheque_slot.sub",
						"over_image" : "d:/ymir work/ui/public/cheque_slot.sub",
						"down_image" : "d:/ymir work/ui/public/cheque_slot.sub",

						"children" :
						(
							{
								"name" : "Cheque",
								"type" : "text",

								"x" : 3,
								"y" : 3,

								"horizontal_align" : "right",
								"text_horizontal_align" : "right",

								"text" : "99",
							},
						),
					},
				),
			},
		),
	}
elif not app.ENABLE_EXTEND_INVEN_SYSTEM and app.ENABLE_CHEQUE_SYSTEM:
	window = {
		"name" : "InventoryWindow",

		"x" : SCREEN_WIDTH - 176,
		"y" : SCREEN_HEIGHT - 37 - 565,

		"style" : ("movable", "float",),

		"width" : 176,
		"height" : 565,

		"children" :
		(
			{
				"name" : "board",
				"type" : "board",
				"style" : ("attach",),

				"x" : 0,
				"y" : 0,

				"width" : 176,
				"height" : 565,

				"children" :
				(
					{
						"name" : "TitleBar",
						"type" : "titlebar",
						"style" : ("attach",),

						"x" : 8,
						"y" : 7,

						"width" : 161,
						"color" : "yellow",

						"children" :
						(
							{ "name":"TitleName", "type":"text", "x":81, "y":0, "text":uiScriptLocale.INVENTORY_TITLE, "text_horizontal_align":"center","outline":"1" },
						),
					},

					{
						"name" : "RefreshButton",
						"type" : "button",

						"x" : 8,
						"y" : 7,

						"tooltip_text_new" : uiScriptLocale.INVENTORY_EX_STACK_ITEMS,
						"tooltip_text_color" : 0xfff1e6c0,
						"tooltip_x" : 0,
						"tooltip_y" : -35,

						"default_image" : "d:/ymir work/ui/pattern/titlebar_inv_refresh_baseframe.tga",
						"over_image" : "d:/ymir work/ui/pattern/titlebar_inv_refresh_baseframe1.tga",
						"down_image" : "d:/ymir work/ui/pattern/titlebar_inv_refresh_baseframe2.tga",
					},

					{
						"name" : "Equipment_Base",
						"type" : "image",

						"x" : 10,
						"y" : 33,

						"image" : "d:/ymir work/ui/equipment_bg_without_ring.tga",

						"children" :
						(

							{
								"name" : "EquipmentSlot",
								"type" : "slot",

								"x" : 3,
								"y" : 3,

								"width" : 150,
								"height" : 182,

								"slot" : (
											{"index":EQUIPMENT_START_INDEX+0, "x":39, "y":37, "width":32, "height":64},
											{"index":EQUIPMENT_START_INDEX+1, "x":39, "y":2, "width":32, "height":32},
											{"index":EQUIPMENT_START_INDEX+2, "x":39, "y":145, "width":32, "height":32},
											{"index":EQUIPMENT_START_INDEX+3, "x":75, "y":67, "width":32, "height":32},
											{"index":EQUIPMENT_START_INDEX+4, "x":3, "y":3, "width":32, "height":96},
											{"index":EQUIPMENT_START_INDEX+5, "x":114, "y":67, "width":32, "height":32},
											{"index":EQUIPMENT_START_INDEX+6, "x":114, "y":35, "width":32, "height":32},
											{"index":EQUIPMENT_START_INDEX+7, "x":2, "y":145, "width":32, "height":32},
											{"index":EQUIPMENT_START_INDEX+8, "x":75, "y":145, "width":32, "height":32},
											{"index":EQUIPMENT_START_INDEX+9, "x":114, "y":2, "width":32, "height":32},
											{"index":EQUIPMENT_START_INDEX+10, "x":75, "y":35, "width":32, "height":32},
											{"index":item.EQUIPMENT_BELT, "x":39, "y":106, "width":32, "height":32},
										),
							},
							{
								"name" : "DSSButton",
								"type" : "button",

								"x" : 114,
								"y" : 107,

								"tooltip_text_new" : uiScriptLocale.INVENTORY_EX_ALCHEMY,
								"tooltip_text_color" : 0xfff1e6c0,
								"tooltip_x" : 0,
								"tooltip_y" : -35,

								"default_image" : "d:/ymir work/ui/dragonsoul/dss_inventory_button_01.tga",
								"over_image" : "d:/ymir work/ui/dragonsoul/dss_inventory_button_02.tga",
								"down_image" : "d:/ymir work/ui/dragonsoul/dss_inventory_button_03.tga",
							},
							{
								"name" : "MallButton",
								"type" : "button",

								"x" : 118,
								"y" : 148,

								"tooltip_text" : uiScriptLocale.MALL_TITLE,

								"default_image" : "d:/ymir work/ui/game/TaskBar/Mall_Button_01.tga",
								"over_image" : "d:/ymir work/ui/game/TaskBar/Mall_Button_02.tga",
								"down_image" : "d:/ymir work/ui/game/TaskBar/Mall_Button_03.tga",
							},
							{
								"name" : "CostumeButton",
								"type" : "button",

								"x" : 78,
								"y" : 5,

								"tooltip_text_new" : uiScriptLocale.COSTUME_TITLE,
								"tooltip_text_color" : 0xfff1e6c0,
								"tooltip_x" : 0,
								"tooltip_y" : -35,
								
								"default_image" : "d:/ymir work/ui/game/taskbar/costume_Button_01.tga",
								"over_image" : "d:/ymir work/ui/game/taskbar/costume_Button_02.tga",
								"down_image" : "d:/ymir work/ui/game/taskbar/costume_Button_03.tga",
							},
							{
								"name" : "Equipment_Tab_01",
								"type" : "radio_button",

								"x" : 86,
								"y" : 161,

								"default_image" : "d:/ymir work/ui/game/windows/tab_button_small_01.sub",
								"over_image" : "d:/ymir work/ui/game/windows/tab_button_small_02.sub",
								"down_image" : "d:/ymir work/ui/game/windows/tab_button_small_03.sub",

								"children" :
								(
									{
										"name" : "Equipment_Tab_01_Print",
										"type" : "text",

										"x" : 0,
										"y" : 0,

										"all_align" : "center",

										"text" : "I",
									},
								),
							},
							{
								"name" : "Equipment_Tab_02",
								"type" : "radio_button",

								"x" : 86 + 32,
								"y" : 161,

								"default_image" : "d:/ymir work/ui/game/windows/tab_button_small_01.sub",
								"over_image" : "d:/ymir work/ui/game/windows/tab_button_small_02.sub",
								"down_image" : "d:/ymir work/ui/game/windows/tab_button_small_03.sub",

								"children" :
								(
									{
										"name" : "Equipment_Tab_02_Print",
										"type" : "text",

										"x" : 0,
										"y" : 0,

										"all_align" : "center",

										"text" : "II",
									},
								),
							},

						),
					},

					{
						"name" : "Inventory_Tab_01",
						"type" : "radio_button",

						"x" : 10,
						"y" : 33 + 191,

						"default_image" : "d:/ymir work/ui/game/windows/tab_button_large_01.sub",
						"over_image" : "d:/ymir work/ui/game/windows/tab_button_large_02.sub",
						"down_image" : "d:/ymir work/ui/game/windows/tab_button_large_03.sub",

						"children" :
						(
							{
								"name" : "Inventory_Tab_01_Print",
								"type" : "text",

								"x" : 0,
								"y" : 0,

								"all_align" : "center",

								"text" : "I",
							},
						),
					},
					{
						"name" : "Inventory_Tab_02",
						"type" : "radio_button",

						"x" : 10 + 78,
						"y" : 33 + 191,

						"default_image" : "d:/ymir work/ui/game/windows/tab_button_large_01.sub",
						"over_image" : "d:/ymir work/ui/game/windows/tab_button_large_02.sub",
						"down_image" : "d:/ymir work/ui/game/windows/tab_button_large_03.sub",

						"children" :
						(
							{
								"name" : "Inventory_Tab_02_Print",
								"type" : "text",

								"x" : 0,
								"y" : 0,

								"all_align" : "center",

								"text" : "II",
							},
						),
					},

					{
						"name" : "ItemSlot",
						"type" : "grid_table",

						"x" : 8,
						"y" : 246,

						"start_index" : 0,
						"x_count" : 5,
						"y_count" : 9,
						"x_step" : 32,
						"y_step" : 32,

						"image" : "d:/ymir work/ui/public/Slot_Base.sub"
					},

					{
						"name":"Money_Icon",
						"type":"image",
						"vertical_align":"bottom",

						"x":57,
						"y":26,

						"image":"d:/ymir work/ui/game/windows/money_icon.sub",
					},
					{
						"name":"Money_Slot",
						"type":"button",

						"x":75,
						"y":28,

						"vertical_align":"bottom",

						"default_image" : "d:/ymir work/ui/public/gold_slot.sub",
						"over_image" : "d:/ymir work/ui/public/gold_slot.sub",
						"down_image" : "d:/ymir work/ui/public/gold_slot.sub",

						"children" :
						(
							{
								"name" : "Money",
								"type" : "text",

								"x" : 3,
								"y" : 3,

								"horizontal_align" : "right",
								"text_horizontal_align" : "right",

								"text" : "123456789",
							},
						),
					},
					{
						"name":"Cheque_Icon",
						"type":"image",
						"vertical_align":"bottom",

						"x":10,
						"y":26,

						"image":"d:/ymir work/ui/game/windows/cheque_icon.sub",
					},
					{
						"name":"Cheque_Slot",
						"type":"button",

						"x":28,
						"y":28,

						"vertical_align":"bottom",

						"default_image" : "d:/ymir work/ui/public/cheque_slot.sub",
						"over_image" : "d:/ymir work/ui/public/cheque_slot.sub",
						"down_image" : "d:/ymir work/ui/public/cheque_slot.sub",

						"children" :
						(
							{
								"name" : "Cheque",
								"type" : "text",

								"x" : 3,
								"y" : 3,

								"horizontal_align" : "right",
								"text_horizontal_align" : "right",

								"text" : "99",
							},
						),
					},
				),
			},
		),
	}
else:
	window = {
		"name" : "InventoryWindow",

		"x" : SCREEN_WIDTH - 176,
		"y" : SCREEN_HEIGHT - 37 - 565,

		"style" : ("movable", "float",),

		"width" : 176,
		"height" : 565,

		"children" :
		(
			{
				"name" : "board",
				"type" : "board",
				"style" : ("attach",),

				"x" : 0,
				"y" : 0,

				"width" : 176,
				"height" : 565,

				"children" :
				(
					{
						"name" : "TitleBar",
						"type" : "titlebar",
						"style" : ("attach",),

						"x" : 8,
						"y" : 7,

						"width" : 161,
						"color" : "yellow",

						"children" :
						(
							{ "name":"TitleName", "type":"text", "x":81, "y":0, "text":uiScriptLocale.INVENTORY_TITLE, "text_horizontal_align":"center","outline":"1" },
						),
					},

					{
						"name" : "RefreshButton",
						"type" : "button",

						"x" : 8,
						"y" : 7,

						"tooltip_text_new" : uiScriptLocale.INVENTORY_EX_STACK_ITEMS,
						"tooltip_text_color" : 0xfff1e6c0,
						"tooltip_x" : 0,
						"tooltip_y" : -35,

						"default_image" : "d:/ymir work/ui/pattern/titlebar_inv_refresh_baseframe.tga",
						"over_image" : "d:/ymir work/ui/pattern/titlebar_inv_refresh_baseframe1.tga",
						"down_image" : "d:/ymir work/ui/pattern/titlebar_inv_refresh_baseframe2.tga",
					},

					{
						"name" : "Equipment_Base",
						"type" : "image",

						"x" : 10,
						"y" : 33,

						"image" : "d:/ymir work/ui/equipment_bg_without_ring.tga",

						"children" :
						(

							{
								"name" : "EquipmentSlot",
								"type" : "slot",

								"x" : 3,
								"y" : 3,

								"width" : 150,
								"height" : 182,

								"slot" : (
											{"index":EQUIPMENT_START_INDEX+0, "x":39, "y":37, "width":32, "height":64},
											{"index":EQUIPMENT_START_INDEX+1, "x":39, "y":2, "width":32, "height":32},
											{"index":EQUIPMENT_START_INDEX+2, "x":39, "y":145, "width":32, "height":32},
											{"index":EQUIPMENT_START_INDEX+3, "x":75, "y":67, "width":32, "height":32},
											{"index":EQUIPMENT_START_INDEX+4, "x":3, "y":3, "width":32, "height":96},
											{"index":EQUIPMENT_START_INDEX+5, "x":114, "y":67, "width":32, "height":32},
											{"index":EQUIPMENT_START_INDEX+6, "x":114, "y":35, "width":32, "height":32},
											{"index":EQUIPMENT_START_INDEX+7, "x":2, "y":145, "width":32, "height":32},
											{"index":EQUIPMENT_START_INDEX+8, "x":75, "y":145, "width":32, "height":32},
											{"index":EQUIPMENT_START_INDEX+9, "x":114, "y":2, "width":32, "height":32},
											{"index":EQUIPMENT_START_INDEX+10, "x":75, "y":35, "width":32, "height":32},
											{"index":item.EQUIPMENT_BELT, "x":39, "y":106, "width":32, "height":32},
										),
							},
							{
								"name" : "DSSButton",
								"type" : "button",

								"x" : 114,
								"y" : 107,

								"tooltip_text_new" : uiScriptLocale.INVENTORY_EX_ALCHEMY,
								"tooltip_text_color" : 0xfff1e6c0,
								"tooltip_x" : 0,
								"tooltip_y" : -35,
								
								"default_image" : "d:/ymir work/ui/dragonsoul/dss_inventory_button_01.tga",
								"over_image" : "d:/ymir work/ui/dragonsoul/dss_inventory_button_02.tga",
								"down_image" : "d:/ymir work/ui/dragonsoul/dss_inventory_button_03.tga",
							},
							{
								"name" : "MallButton",
								"type" : "button",

								"x" : 118,
								"y" : 148,

								"tooltip_text" : uiScriptLocale.MALL_TITLE,

								"default_image" : "d:/ymir work/ui/game/TaskBar/Mall_Button_01.tga",
								"over_image" : "d:/ymir work/ui/game/TaskBar/Mall_Button_02.tga",
								"down_image" : "d:/ymir work/ui/game/TaskBar/Mall_Button_03.tga",
							},
							{
								"name" : "RuneButton",
								"type" : "button",

								"x" : 76,
								"y" : 108,

								"tooltip_text" : uiScriptLocale.INVENTORY_RUNE_SYSTEM,

								"default_image" : "kowal/runes_01.tga",
								"over_image" : "kowal/runes_01.tga",
								"down_image" : "kowal/runes_01.tga",
							},
							{
								"name" : "CostumeButton",
								"type" : "button",

								"x" : 78,
								"y" : 5,

								"tooltip_text_new" : uiScriptLocale.COSTUME_TITLE,
								"tooltip_text_color" : 0xfff1e6c0,
								"tooltip_x" : 0,
								"tooltip_y" : -35,

								"default_image" : "d:/ymir work/ui/game/taskbar/costume_Button_01.tga",
								"over_image" : "d:/ymir work/ui/game/taskbar/costume_Button_02.tga",
								"down_image" : "d:/ymir work/ui/game/taskbar/costume_Button_03.tga",
							},
							{
								"name" : "Equipment_Tab_01",
								"type" : "radio_button",

								"x" : 86,
								"y" : 161,

								"default_image" : "d:/ymir work/ui/game/windows/tab_button_small_01.sub",
								"over_image" : "d:/ymir work/ui/game/windows/tab_button_small_02.sub",
								"down_image" : "d:/ymir work/ui/game/windows/tab_button_small_03.sub",

								"children" :
								(
									{
										"name" : "Equipment_Tab_01_Print",
										"type" : "text",

										"x" : 0,
										"y" : 0,

										"all_align" : "center",

										"text" : "I",
									},
								),
							},
							{
								"name" : "Equipment_Tab_02",
								"type" : "radio_button",

								"x" : 86 + 32,
								"y" : 161,

								"default_image" : "d:/ymir work/ui/game/windows/tab_button_small_01.sub",
								"over_image" : "d:/ymir work/ui/game/windows/tab_button_small_02.sub",
								"down_image" : "d:/ymir work/ui/game/windows/tab_button_small_03.sub",

								"children" :
								(
									{
										"name" : "Equipment_Tab_02_Print",
										"type" : "text",

										"x" : 0,
										"y" : 0,

										"all_align" : "center",

										"text" : "II",
									},
								),
							},

						),
					},

					{
						"name" : "Inventory_Tab_01",
						"type" : "radio_button",

						"x" : 10,
						"y" : 33 + 191,

						"default_image" : "d:/ymir work/ui/game/windows/tab_button_large_01.sub",
						"over_image" : "d:/ymir work/ui/game/windows/tab_button_large_02.sub",
						"down_image" : "d:/ymir work/ui/game/windows/tab_button_large_03.sub",

						"children" :
						(
							{
								"name" : "Inventory_Tab_01_Print",
								"type" : "text",

								"x" : 0,
								"y" : 0,

								"all_align" : "center",

								"text" : "I",
							},
						),
					},
					{
						"name" : "Inventory_Tab_02",
						"type" : "radio_button",

						"x" : 10 + 78,
						"y" : 33 + 191,

						"default_image" : "d:/ymir work/ui/game/windows/tab_button_large_01.sub",
						"over_image" : "d:/ymir work/ui/game/windows/tab_button_large_02.sub",
						"down_image" : "d:/ymir work/ui/game/windows/tab_button_large_03.sub",

						"children" :
						(
							{
								"name" : "Inventory_Tab_02_Print",
								"type" : "text",

								"x" : 0,
								"y" : 0,

								"all_align" : "center",

								"text" : "II",
							},
						),
					},

					{
						"name" : "ItemSlot",
						"type" : "grid_table",

						"x" : 8,
						"y" : 246,

						"start_index" : 0,
						"x_count" : 5,
						"y_count" : 9,
						"x_step" : 32,
						"y_step" : 32,

						"image" : "d:/ymir work/ui/public/Slot_Base.sub"
					},

					{
						"name":"Money_Slot",
						"type":"button",

						"x":8,
						"y":28,

						"horizontal_align":"center",
						"vertical_align":"bottom",

						"default_image" : "d:/ymir work/ui/public/parameter_slot_05.sub",
						"over_image" : "d:/ymir work/ui/public/parameter_slot_05.sub",
						"down_image" : "d:/ymir work/ui/public/parameter_slot_05.sub",

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
								"name" : "Money",
								"type" : "text",

								"x" : 3,
								"y" : 3,

								"horizontal_align" : "right",
								"text_horizontal_align" : "right",

								"text" : "123456789",
							},
						),
					},
					{
						"name":"Cheque_Icon",
						"type":"image",
						"vertical_align":"bottom",
						
						"x":10,
						"y":26,

						"image":"d:/ymir work/ui/game/windows/cheque_icon.sub",
					},
					{
						"name":"Cheque_Slot",
						"type":"button",

						"x":28,
						"y":28,

						"vertical_align":"bottom",

						"default_image" : "d:/ymir work/ui/public/cheque_slot.sub",
						"over_image" : "d:/ymir work/ui/public/cheque_slot.sub",
						"down_image" : "d:/ymir work/ui/public/cheque_slot.sub",

						"children" :
						(
							{
								"name" : "Cheque",
								"type" : "text",

								"x" : 3,
								"y" : 3,

								"horizontal_align" : "right",
								"text_horizontal_align" : "right",

								"text" : "99",
							},
						),
					},
				),
			},
		),
	}
