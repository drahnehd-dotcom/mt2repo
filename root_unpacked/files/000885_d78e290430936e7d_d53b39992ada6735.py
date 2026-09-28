import uiScriptLocale

window = {
	"name" : "InventoryWindow",

	"x" : SCREEN_WIDTH/1.7,
	"y" : SCREEN_HEIGHT/2-250,

	"style" : ("movable", "float",),

	"width" : 287,
	"height" : 505,

	"children" :
	(
		{
			"name" : "board",
			"type" : "board",
			"style" : ("attach",),

			"x" : 0,
			"y" : 0,

			"width" : 287,
			"height" : 505,

			"children" :
			(
				{
					"name" : "Equipment_Base",
					"type" : "expanded_image",

					"x" : 0,
					"y" : 0,

					"image" : "d:/ymir work/ui/dragonsoul/dragon_soul_bg.tga",

				},
				{
					"name" : "Inventory_Tab_01", "type" : "radio_button",
					"x" : 16, "y" : 331,
					"default_image"	: "d:/ymir work/ui/dragonsoul/btn_soul_01_1.tga",
					"over_image"	: "d:/ymir work/ui/dragonsoul/btn_soul_01_2.tga",
					"down_image"	: "d:/ymir work/ui/dragonsoul/btn_soul_01_3.tga",
				},
				{
					"name" : "Inventory_Tab_02", "type" : "radio_button",
					"x" : 59, "y" : 331,
					"default_image"	: "d:/ymir work/ui/dragonsoul/btn_soul_02_1.tga",
					"over_image"	: "d:/ymir work/ui/dragonsoul/btn_soul_02_2.tga",
					"down_image"	: "d:/ymir work/ui/dragonsoul/btn_soul_02_3.tga",
				},
				{
					"name" : "Inventory_Tab_03", "type" : "radio_button",
					"x" : 102, "y" : 331,
					"default_image"	: "d:/ymir work/ui/dragonsoul/btn_soul_03_1.tga",
					"over_image"	: "d:/ymir work/ui/dragonsoul/btn_soul_03_2.tga",
					"down_image"	: "d:/ymir work/ui/dragonsoul/btn_soul_03_3.tga",
				},
				{
					"name" : "Inventory_Tab_04", "type" : "radio_button",
					"x" : 145, "y" : 331,
					"default_image"	: "d:/ymir work/ui/dragonsoul/btn_soul_04_1.tga",
					"over_image"	: "d:/ymir work/ui/dragonsoul/btn_soul_04_2.tga",
					"down_image"	: "d:/ymir work/ui/dragonsoul/btn_soul_04_3.tga",
				},
				{
					"name" : "Inventory_Tab_05", "type" : "radio_button",
					"x" : 188, "y" : 331,
					"default_image"	: "d:/ymir work/ui/dragonsoul/btn_soul_05_1.tga",
					"over_image"	: "d:/ymir work/ui/dragonsoul/btn_soul_05_2.tga",
					"down_image"	: "d:/ymir work/ui/dragonsoul/btn_soul_05_3.tga",
				},
				{
					"name" : "Inventory_Tab_06", "type" : "radio_button",
					"x" : 231, "y" : 331,
					"default_image"	: "d:/ymir work/ui/dragonsoul/btn_soul_06_1.tga",
					"over_image"	: "d:/ymir work/ui/dragonsoul/btn_soul_06_2.tga",
					"down_image"	: "d:/ymir work/ui/dragonsoul/btn_soul_06_3.tga",
				},
				
				{
					"name" : "ItemSlot",
					"type" : "grid_table",

					"x" : 15,
					"y" : 355,

					"start_index" : 0,
					"x_count" : 8,
					"y_count" : 4,
					"x_step" : 32,
					"y_step" : 32,

				},
				{
					"name" : "EquipmentSlot",
					"type" : "slot",

					"x" : 0,
					"y" : 0,

					"width" : 287,
					"height" : 280,

					"slot" : (
								{"index":DRAGON_SOUL_EQUIPMENT_SLOT_START+0, "x":128, "y":53, "width":32, "height":32},
								{"index":DRAGON_SOUL_EQUIPMENT_SLOT_START+1, "x":59, "y":93, "width":32, "height":32},
								{"index":DRAGON_SOUL_EQUIPMENT_SLOT_START+2, "x":59, "y":179, "width":32, "height":32},
								{"index":DRAGON_SOUL_EQUIPMENT_SLOT_START+3, "x":128, "y":219, "width":32, "height":32},
								{"index":DRAGON_SOUL_EQUIPMENT_SLOT_START+4, "x":194, "y":179, "width":32, "height":32},
								{"index":DRAGON_SOUL_EQUIPMENT_SLOT_START+5, "x":194, "y":93, "width":32, "height":32},
							),
				},
				{
					"name" : "deck1",
					"type" : "toggle_button",

					"x" : 21,
					"y" : 230,

					"default_image" : "d:/ymir work/ui/dragonsoul/deck1_1.tga",
					"over_image" : "d:/ymir work/ui/dragonsoul/deck1_2.tga",
					"down_image" : "d:/ymir work/ui/dragonsoul/deck1_3.tga",
				},
				{
					"name" : "deck2",
					"type" : "toggle_button",

					"x" : 234,
					"y" : 230,

					"default_image" : "d:/ymir work/ui/dragonsoul/deck2_1.tga",
					"over_image" : "d:/ymir work/ui/dragonsoul/deck2_2.tga",
					"down_image" : "d:/ymir work/ui/dragonsoul/deck2_3.tga",
				},
				{
					"name" : "TitleBar",
					"type" : "titlebar",
					"style" : ("attach",),

					"x" : 8,
					"y" : 7,

					"width" : 271,
					"color" : "yellow",

					"children" :
					(
						{ "name":"TitleName", "type":"text", "x":134, "y":1, "text":uiScriptLocale.DRAGONSOUL_TITLE, "outline":"1","text_horizontal_align":"center" },
					),
				},
				{
					"name" : "TabControl",
					"type" : "window",

					"x" : 7,
					"y" : 278,

					"width" : 271,
					"height" : 32,

					"children" :
					(
						{
							"name" : "Tab_01",
							"type" : "expanded_image",

							"x" : 0,
							"y" : 0,

							"width" : 271,
							"height" : 32,

							"image" : "d:/ymir work/ui/dragonsoul/tab01.png",
						},
						{
							"name" : "Tab_02",
							"type" : "expanded_image",

							"x" : 0,
							"y" : 0,

							"width" : 271,
							"height" : 32,

							"image" : "d:/ymir work/ui/dragonsoul/tab02.png",
						},
						{
							"name" : "Tab_03",
							"type" : "expanded_image",

							"x" : 0,
							"y" : 0,

							"width" : 271,
							"height" : 32,

							"image" : "d:/ymir work/ui/dragonsoul/tab03.png",
						},
						{
							"name" : "Tab_04",
							"type" : "expanded_image",

							"x" : 0,
							"y" : 0,

							"width" : 271,
							"height" : 32,

							"image" : "d:/ymir work/ui/dragonsoul/tab04.png",
						},
						{
							"name" : "Tab_05",
							"type" : "expanded_image",

							"x" : 0,
							"y" : 0,

							"width" : 271,
							"height" : 32,

							"image" : "d:/ymir work/ui/dragonsoul/tab05.png",
						},
						{
							"name" : "Tab_06",
							"type" : "expanded_image",

							"x" : 0,
							"y" : 0,

							"width" : 271,
							"height" : 32,

							"image" : "d:/ymir work/ui/dragonsoul/tab06.png",
						},
						{
							"name" : "Tab_Button_01",
							"type" : "radio_button",

							"x" : 35,
							"y" : 2,

							"width" : 28,
							"height" : 27,
						},
						{
							"name" : "Tab_Button_02",
							"type" : "radio_button",

							"x" : 70,
							"y" : 2,

							"width" : 28,
							"height" : 27,
						},
						{
							"name" : "Tab_Button_03",
							"type" : "radio_button",

							"x" : 104,
							"y" : 2,

							"width" : 28,
							"height" : 27,
						},
						{
							"name" : "Tab_Button_04",
							"type" : "radio_button",

							"x" : 139,
							"y" : 2,

							"width" : 28,
							"height" : 27,
						},
						{
							"name" : "Tab_Button_05",
							"type" : "radio_button",

							"x" : 174,
							"y" : 2,

							"width" : 28,
							"height" : 27,
						},
						{
							"name" : "Tab_Button_06",
							"type" : "radio_button",

							"x" : 210,
							"y" : 2,

							"width" : 28,
							"height" : 27,
						},
					),
				},
				{
					"name" : "tab_text_window",
					"type" : "window",

					"x" : 18,
					"y" : 309,
					"width":250,
					"height":18,

					"children":
					(
						{
							"name" : "tab_text_area",
							"type" : "text",

							"x" : 0,
							"y" : 0,
							"all_align" : True,
							"fontname":"Tahoma:14",

							"text" : uiScriptLocale.DRAGONSOUL_TAP_TITLE_1,
							"color" : 0xFFC0C0C0,
						},
					),
				},
				{					
					"name" : "activate",
					"type" : "toggle_button",

					"x" : 217,
					"y" : 492,

					"default_image" : "d:/ymir work/ui/button_example_040.png",
					"over_image" : "d:/ymir work/ui/button_example_041.png",
					"down_image" : "d:/ymir work/ui/button_example_042.png",
				},
				{
					"name" : "renew_btn",
					"type" : "button",

					"x" : 15,
					"y" : 38,

					"default_image" : "d:/ymir work/ui/renew_ds0.png",
					"over_image" : "d:/ymir work/ui/renew_ds1.png",
					"down_image" : "d:/ymir work/ui/renew_ds2.png",
				},
			),
		},
	),
}
