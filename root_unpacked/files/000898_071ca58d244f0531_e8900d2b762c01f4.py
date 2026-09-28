import uiScriptLocale

BUTTON_ROOT = "d:/ymir work/ui/public/"

X = 40
Y = 133
START = 20
SUB_START = 23
BOARD_WIDTH = 255
BOARD_HEIGHT = 445
HEIGHT = 144

window = {
	"name" : "ExtendedInventoryWindow",
	"x" : SCREEN_WIDTH - 515,
	"y" : SCREEN_HEIGHT - 37 - 565,
	"style" : ("movable", "float",),
	"width" : BOARD_WIDTH,
	"height" : BOARD_HEIGHT,
	"children" :
	(
        {
            "name" : "window",
            "type" : "window",
            "x": 182,
            "y":130,
            "width":70,
            "height":144,
            "children":
            (
				{
					"name" : "board",
					"type" : "board",
					"x" : 0,
					"y" : 0,
					"width" : 70,
					"height" : 144,
					"children":
					(
						{
							"name" : "SkillBookButton",
							"type" : "radio_button",
							"x" : START,
							"y" : Y,
							"vertical_align" : "bottom",
							"default_image" : "d:/ymir work/ui/extended_inventory/category0_0.png",
							"over_image" : "d:/ymir work/ui/extended_inventory/category0_1.png",
							"down_image" : "d:/ymir work/ui/extended_inventory/category0_2.png",
						},
						{
							"name" : "UpgradeItemsButton",
							"type" : "radio_button",
							"x" : START,
							"y" : Y-20,
							"vertical_align" : "bottom",
							"default_image" : "d:/ymir work/ui/extended_inventory/category1_0.png",
							"over_image" : "d:/ymir work/ui/extended_inventory/category1_1.png",
							"down_image" : "d:/ymir work/ui/extended_inventory/category1_2.png",
						},
						{
							"name" : "StoneButton",
							"type" : "radio_button",
							"x" : START,
							"y" : Y-20-20,
							"vertical_align" : "bottom",
							"default_image" : "d:/ymir work/ui/extended_inventory/category2_0.png",
							"over_image" : "d:/ymir work/ui/extended_inventory/category2_1.png",
							"down_image" : "d:/ymir work/ui/extended_inventory/category2_2.png",
						},
						{
							"name" : "BoxButton",
							"type" : "radio_button",
							"x" : START,
							"y" : Y-20-20-20,
							"vertical_align" : "bottom",
							"default_image" : "d:/ymir work/ui/extended_inventory/category3_0.png",
							"over_image" : "d:/ymir work/ui/extended_inventory/category3_1.png",
							"down_image" : "d:/ymir work/ui/extended_inventory/category3_2.png",
						},
						{
							"name" : "EfsunButton",
							"type" : "radio_button",
							"x" : START,
							"y" : Y-20-20-20-20,
							"vertical_align" : "bottom",
							"default_image" : "d:/ymir work/ui/extended_inventory/category4_0.png",
							"over_image" : "d:/ymir work/ui/extended_inventory/category4_1.png",
							"down_image" : "d:/ymir work/ui/extended_inventory/category4_2.png",
						},
						{
							"name" : "CicekButton",
							"type" : "radio_button",
							"x" : START,
							"y" : Y-20-20-20-20-20,
							"vertical_align" : "bottom",
							"default_image" : "d:/ymir work/ui/extended_inventory/category5_0.png",
							"over_image" : "d:/ymir work/ui/extended_inventory/category5_1.png",
							"down_image" : "d:/ymir work/ui/extended_inventory/category5_2.png",
						},
					),
				},
			),
		},
        {
            "name" : "window_settings",
            "type" : "window",
            "x":8,
            "y":365,
            "width":184,
            "height":45,
            "children":
            (
				{
					"name" : "board_settings",
					"type" : "board",
					"x" : 0,
					"y" : 0,
                    "horizontal_align":"center",
                    "vertical_align":"center",
					"width" : 184,
					"height" : 45,
					"children":
					(
                        {
                            "name" : "SettingsTitle",
                            "type" : "text",
                            "x":20,"y":2,
                            "vertical_align":"center",
                            "text": uiScriptLocale.SETTINGS,
                            "outline":"1",
                            "color":0xFFc2c2c2,
                            "fontname":"Tahoma:16",
						},
						{
							"name" : "DirectUseButton",
							"type" : "toggle_button",
							"x" : SUB_START+77,
							"y" : 36,
							"default_image" : "d:/ymir work/ui/new_weekly_rank/select_title0.png",
							"over_image" : "d:/ymir work/ui/new_weekly_rank/select_title1.png",
							"down_image" : "d:/ymir work/ui/new_weekly_rank/select_title2.png",
						},
						{
							"name" : "OpenWithInventoryButton",
							"type" : "toggle_button",
							"x" : SUB_START+102,
							"y" : 36,
							"default_image" : "d:/ymir work/ui/new_weekly_rank/select_title0.png",
							"over_image" : "d:/ymir work/ui/new_weekly_rank/select_title1.png",
							"down_image" : "d:/ymir work/ui/new_weekly_rank/select_title2.png",
						},
						{
							"name" : "OpenWhenFastMoveButton",
							"type" : "toggle_button",
							"x" : SUB_START+127,
							"y" : 36,
							"default_image" : "d:/ymir work/ui/new_weekly_rank/select_title0.png",
							"over_image" : "d:/ymir work/ui/new_weekly_rank/select_title1.png",
							"down_image" : "d:/ymir work/ui/new_weekly_rank/select_title2.png",
						},
					),
				},
			),
		},
		{
			"name" : "board",
			"type" : "board",
			"x" : 0,
			"y" : 0,
			"width" : BOARD_WIDTH-54,
			"height" : BOARD_HEIGHT-55,
			"children" :
			(
				{
					"name" : "TitleBar",
					"type" : "titlebar",
					"style" : ("attach",),
					"x" : 8,
					"y" : 7,
					"width" : BOARD_WIDTH-70,
					"color" : "yellow",
					"children" :
					(
						{ "name":"TitleName", "type":"text", "x":0, "y":-4,"all_align":"center", "text": uiScriptLocale.SPECIAL_INVENTORY, "text_horizontal_align":"center","outline":"1" },
					),
				},
				{
					"name" : "SettingsButton",
					"type" : "button",
					"x" :BOARD_WIDTH-96,
					"y" : 8,
					"tooltip_text_new" : uiScriptLocale.SPECIAL_INVENTORY_SETTINGS,
					"tooltip_text_color" : 0xfff1e6c0,
					"tooltip_x" : 0,
					"tooltip_y" : -35,
					"default_image" : "d:/ymir work/ui/options_btn0.png",
					"over_image" : "d:/ymir work/ui/options_btn1.png",
					"down_image" : "d:/ymir work/ui/options_btn2.png",
				},
				{
					"name" : "RefreshButton",
					"type" : "button",

					"x" : 18,
					"y" : 10,

					"default_image" : "d:/ymir work/ui/item_stack_btn0.png",
					"over_image" : "d:/ymir work/ui/item_stack_btn1.png",
					"down_image" : "d:/ymir work/ui/item_stack_btn2.png",
				},
                {
                    "name" : "thinboard",
                    "type" : "border_a",
                    "width":BOARD_WIDTH-79,"height":BOARD_HEIGHT-98,
                    "x":0,"y":30,
                    "horizontal_align":"center",
                    "children":
                    (
                        {
                            "name":"inventoryheader",
                            "type":"image",
                            "x":0,"y":2,
                            "horizontal_align":"center",
                            "image":"d:/ymir work/ui/header_inventory.png",
                            "children":
                            (
                                {
                                    "name":"inventory_title",
                                    "type":"text",
                                    "x":1,"y":-1,
                                    "all_align":"center",
                                    "text":uiScriptLocale.SPECIAL_INVENTORY,
                                    "outline":"1",
                                },
                            ),
                        },
						{
							"name" : "PackAllButton",
							"type" : "button",
							"x" : -5,
							"y" : 0,
							"default_image" : "d:/ymir work/ui/pack_all0.png",
							"over_image" : "d:/ymir work/ui/pack_all1.png",
							"down_image" : "d:/ymir work/ui/pack_all2.png",
						},
                        {
                            "name" : "ItemSlot",
                            "type" : "grid_table",
                            "x" : 8,
                            "y" : 26,
                            "start_index" : 0,
                            "x_count" : 5,
                            "y_count" : 9,
                            "x_step" : 32,
                            "y_step" : 32,
                            "image" : "d:/ymir work/ui/public/Slot_Base.sub"
                        },
						{
							"name" : "Inventory_Tab_01",
							"type" : "radio_button",

							"x" : 12,
							"y" : 319,

							"default_image" : "d:/ymir work/ui/extended_inventory/tab_button0.png",
							"over_image" : "d:/ymir work/ui/extended_inventory/tab_button1.png",
							"down_image" : "d:/ymir work/ui/extended_inventory/tab_button2.png",

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

							"x" : 62,
							"y" : 319,

							"default_image" : "d:/ymir work/ui/extended_inventory/tab_button0.png",
							"over_image" : "d:/ymir work/ui/extended_inventory/tab_button1.png",
							"down_image" : "d:/ymir work/ui/extended_inventory/tab_button2.png",

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

							"x" : 112,
							"y" : 319,

							"default_image" : "d:/ymir work/ui/extended_inventory/tab_button0.png",
							"over_image" : "d:/ymir work/ui/extended_inventory/tab_button1.png",
							"down_image" : "d:/ymir work/ui/extended_inventory/tab_button2.png",

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
                    ),
                },


			),
		},
	),
}
