import uiScriptLocale
import app

ROOT_PATH			= "d:/ymir work/ui/game/PRIVATE_SHOP/"

WINDOW_WIDTH		= 284
WINDOW_HEIGHT		= 452

INFORMATION_GROUP_X		= 40
INFORMATION_GROUP_Y		= 361

BUTTON_GROUP_X			= 22
BUTTON_GROUP_Y			= 413

window = {
		"name" : "PremiumPrivateShopDialog",
		"style" : ("movable", "float",),
		
		"x" : SCREEN_WIDTH - 475,
		"y" : SCREEN_HEIGHT - 605,

		"width"		: WINDOW_WIDTH,
		"height"	: WINDOW_HEIGHT,

		"children" :
		(
			{
				"name" : "board",
				"type" : "board_with_titlebar",
				"style" : ("attach", "ltr",),

				"x" : 0,
				"y" : 0,

				"width"		: WINDOW_WIDTH,
				"height"	: WINDOW_HEIGHT,
				"title"		: uiScriptLocale.PRIVATE_SHOP_TITLE,

				"children" :
				(
					{
						"name"	: "location_button",
						"type"	: "button",

						"x"		: 7 + 7,
						"y"		: 39,

						"default_image" : ROOT_PATH + "position_icon.sub", 
						"over_image" : ROOT_PATH + "position_icon.sub", 
						"down_image" : ROOT_PATH + "position_icon.sub", 
						"image"	: ROOT_PATH + "position_icon.sub",
					},
					
					{
						"name" : "shop_name_text_window", "type" : "window", "style" : ("attach",), "x" : 27 + 7, "y" : 36, "width" : 238, "height" : 19,
						"children" :
						(
							{ 
								"name" : "shop_name_text_button", 
								"type":"button", 
								
								"x":0, 
								"y":0, 
								
								"default_image" : ROOT_PATH + "shop_name_text_bg_large.sub", 
								"over_image" : ROOT_PATH + "shop_name_text_bg_large.sub", 
								"down_image" : ROOT_PATH + "shop_name_text_bg_large.sub", 
								
								"image" : ROOT_PATH + "shop_name_text_bg_large.sub", 
							},

							{
								"name" : "shop_name_text_flash_ani",
								"type" : "ani_image",
								"style" : ("attach",),
								
								"x":0, 
								"y":0, 
								
								"delay" : 5,

								"images" :
								(
									ROOT_PATH + "shop_name_text_large_effect_01.sub",
									ROOT_PATH + "shop_name_text_large_effect_02.sub",
									ROOT_PATH + "shop_name_text_large_effect_03.sub",
									ROOT_PATH + "shop_name_text_large_effect_04.sub",
									ROOT_PATH + "shop_name_text_large_effect_05.sub",
									ROOT_PATH + "shop_name_text_large_effect_06.sub",
									ROOT_PATH + "shop_name_text_large_effect_06.sub",
									ROOT_PATH + "shop_name_text_large_effect_06.sub",
									ROOT_PATH + "shop_name_text_large_effect_05.sub",
									ROOT_PATH + "shop_name_text_large_effect_04.sub",
									ROOT_PATH + "shop_name_text_large_effect_03.sub",
									ROOT_PATH + "shop_name_text_large_effect_02.sub",
									ROOT_PATH + "shop_name_text_large_effect_01.sub",		
									ROOT_PATH + "shop_name_text_large_effect_01.sub",	
									ROOT_PATH + "shop_name_text_large_effect_01.sub",	
									ROOT_PATH + "shop_name_text_large_effect_01.sub",	
									ROOT_PATH + "shop_name_text_large_effect_01.sub",	
									ROOT_PATH + "shop_name_text_large_effect_01.sub",	
									ROOT_PATH + "shop_name_text_large_effect_01.sub",	
									ROOT_PATH + "shop_name_text_large_effect_01.sub",	
									ROOT_PATH + "shop_name_text_large_effect_01.sub",	
									ROOT_PATH + "shop_name_text_large_effect_01.sub",	
								),
							},

							{ "name" : "shop_name_text", "type" : "text", "x" : 0, "y" : 0, "all_align" : "center", "text" : "", "style" : ("not_pick",), },
						),
					},
					
					{
						"name" : "shop_notice_window", "type" : "window", "style" : ("attach",), "x" : 16, "y" : 55, "width" : 253, "height" : 19,
						"children" :
						(
							{ "name" : "shop_notice_bg", "type":"expanded_image", "x":0, "y":0, "image" : ROOT_PATH + "notice_bg.sub", "x_scale" : 1.463, "y_scale" : 1.0, },
							{ "name" : "shop_notice_text", "type" : "text", "x" : 0, "y" : 0, "all_align" : "center", "text" : "", },
						),
					},
					
					{
						"name"	: "BackgroundGroup",
						"type"	: "window",
						
						"x"		: 9,
						"y"		: 73 + 3,
						
						"style"	: ("attach",),
						
						"width"		: 262,
						"height"	: 368,
						
						"children" : (
							{
								"name" : "LeftTop",
								"type" : "image",
								"x" : 0,
								"y" : 0,
								"image" : "d:/ymir work/ui/privatesearch/private_mainboxlefttop.sub",
							},
							{
								"name" : "RightTop",
								"type" : "image",
								"x" : 262 - 13,
								"y" : 0,
								"image" : "d:/ymir work/ui/privatesearch/private_mainboxrighttop.sub",
							},
							{
								"name" : "LeftBottom",
								"type" : "image",
								"x" : 0,
								"y" : 360 - 18 + 10,
								"image" : "d:/ymir work/ui/privatesearch/private_mainboxleftbottom.sub",
							},
							{
								"name" : "RightBottom",
								"type" : "image",
								"x" : 262 - 13,
								"y" : 360 - 18 + 10,
								"image" : "d:/ymir work/ui/privatesearch/private_mainboxrightbottom.sub",
							},
							{
								"name" : "leftcenterImg",
								"type" : "expanded_image",
								"x" : 0,
								"y" : 14,
								"image" : "d:/ymir work/ui/privatesearch/private_leftcenterImg.tga",
								"rect" : (0.0, 0.0, 0, 19),
							},
							{
								"name" : "rightcenterImg",
								"type" : "expanded_image",
								"x" : 262 - 14,
								"y" : 14,
								"image" : "d:/ymir work/ui/privatesearch/private_rightcenterImg.tga",
								"rect" : (0.0, 0.0, 0, 19),
							},
							{
								"name" : "topcenterImg",
								"type" : "expanded_image",
								"x" : 14,
								"y" : 0,
								"image" : "d:/ymir work/ui/privatesearch/private_topcenterImg.tga",
								"rect" : (0.0, 0.0, 13, 0),
							},
							{
								"name" : "bottomcenterImg",
								"type" : "expanded_image",
								"x" : 14,
								"y" : 360 - 18 + 10,
								"image" : "d:/ymir work/ui/privatesearch/private_bottomcenterImg.tga",
								"rect" : (0.0, 0.0, 13, 0),
							},
							{
								"name" : "centerImg",
								"type" : "expanded_image",
								"x" : 14,
								"y" : 14,
								"image" : "d:/ymir work/ui/privatesearch/private_centerImg.tga",
								"rect" : (0.0, 0.0, 13, 19),
							},
						),
					},
					
					{
						"name" : "RenderTarget",
						"type" : "render_target",
						
						"x"		: 12,
						"y"		: 79,
								
						"width"		: 262 - 6,
						"height"	: 325,
								
						"index" : 1,
					},
					
					{
						"name" : "RenderTitle",
						"type" : "thinboard_deco",
								
						"x"		: 9 + 262 / 2 - 190 / 2,
						"y"		: 120,
								
						"width"		: 190,
						"height"	: 32,
						
					},
					
					{ "name" : "RenderTitleText", "type" : "text", "x" : WINDOW_WIDTH / 2, "y" : 130, "text_horizontal_align"  : "center", "text" : "", },
					
					{
						"name"	: "ItemSaleGroup",
						"type"	: "window",
						
						"x"		: 13,
						"y"		: 80,
						
						"width"		: 255,
						"height"	: 325,
						
						"children" :
						(
							{
								"name"	: "ItemSaleTab",
								"type"	: "expanded_image",
								
								"x"		: 0,
								"y"		: 0,
								
								"image" : ROOT_PATH + "shop_name_text_bg.sub", 
								
								"x_scale"	: 1.63,
								"y_scale"	: 1.0,
								
								"children"	:
								(
									{
										"name"	: "ItemNameTextWindow",
										"type"	: "window",
										
										"x"		: 0,
										"y"		: 0,
										
										"width"		: 170,
										"height" 	: 21,
										
										"children" : 
										(
											{ "name" : "ItemNameText", "type" : "text", "x" : 0, "y" : 0, "all_align"  : "center", "text" : uiScriptLocale.PRIVATESHOPSEARCH_ITEMNAME, },
										),
									},

									{
										"name"	: "ItemNameTextWindow",
										"type"	: "window",
										
										"x"		: 170,
										"y"		: 0,
										
										"width"		: 71,
										"height" 	: 21,
										
										"children" : 
										(
											{ "name" : "SaleDateText", "type" : "text", "x" : 0, "y" : 0, "all_align"  : "center", "text" : uiScriptLocale.PRIVATE_SHOP_SALE_DATE, },
										),
									},
								),
							},
							
							{
								"name"	: "ItemSaleScrollBar",
								"type"	: "scrollbar",
								
								"x"		: 241,
								"y"		: 21,
								
								"size"	: 325 - 17,
							},
						),
					},
					
					{
						"name" : "item_slot",
						"type" : "grid_table",

						"x" : 14,
						"y" : 80,

						"start_index" : 0,
						"x_count" : 8,
						"y_count" : 8,
						"x_step" : 32,
						"y_step" : 32,

						"image" : "d:/ymir work/ui/public/Slot_Base.sub",
					},
					
					{
						"name"	: "TabButtonGroup",
						"type"	: "window",
						
						"x"		: 0,
						"y"		: 338 + 3,
						
						"style"	: ("attach",),
						
						"horizontal_align"	: "center",
						
						"width"		: 66,
						"height"	: 18,
						
						"children"	: 
						(
							{
								"name" : "tab1",
								"type" : "radio_button",

								"x" : 0,
								"y" : 0,

								"text" : "I",

								"default_image" : "d:/ymir work/ui/privatesearch/private_pagenumber_00.sub",
								"over_image" : "d:/ymir work/ui/privatesearch/private_pagenumber_01.sub",
								"down_image" : "d:/ymir work/ui/privatesearch/private_pagenumber_02.sub",
							},

							{
								"name" : "tab2",
								"type" : "radio_button",

								"x" : 34,
								"y" : 0,

								"text" : "II",

								"default_image" : "d:/ymir work/ui/privatesearch/private_pagenumber_00.sub",
								"over_image" : "d:/ymir work/ui/privatesearch/private_pagenumber_01.sub",
								"down_image" : "d:/ymir work/ui/privatesearch/private_pagenumber_02.sub",
							},
						),
					},
					
					{
						"name"	:	"information_group",
						"type"	:	"window",
						
						"x"		:	INFORMATION_GROUP_X,
						"y"		:	INFORMATION_GROUP_Y,
						
						"style"	:	("attach",),
						
						"width"		:	200,
						"height"	:	18 + 26 + 18,
						
						"children"	:
						(
							{
								"name"	: "sandglass_icon",
								"type"	: "image",
								"x"		: 0,
								"y"		: 0,
								
								"style"	:	("attach",),
								
								"image"	: ROOT_PATH + "sandglass_icon.sub",
							},
							
							{
								"name" : "remain_time_text_window", "type" : "window", "style" : ("attach",), "x" : 24, "y" : 0, "width" : 178, "height" : 18,
								"children" :
								(
									{ "name" : "remain_time_text_bg", "type":"expanded_image", "x":0, "y":0, "image" : ROOT_PATH + "remain_time_text_bg.sub", "x_scale" : 1.3, "y_scale" : 1.0, },
									{ "name" : "remain_time_text", "type" : "text", "x" : 0, "y" : 0, "all_align" : "center", "text" : "", },
								),
							},
							
							{
								"name":"cheque_icon",
								"type":"image",
								
								"x": 0,
								"y": 2 + 26,

								"image":"d:/ymir work/ui/game/windows/cheque_icon.sub",
							},
							
							{
								"name" : "cheque_text_window", "type" : "window", "style" : ("attach",), "x" : 24, "y" : 26, "width" : 32, "height" : 18,
								"children" :
								(
									{ "name" : "cheque_text_bg", "type":"expanded_image", "x":0, "y":0, "image" : ROOT_PATH + "won_text_bg.sub", "x_scale" : 1.3, "y_scale" : 1.0, },
									{ "name" : "cheque_text", "type" : "text", "x" : 0, "y" : 0, "all_align" : "center", "text" : "", },
								),
							},
							
							{
								"name":"gold_icon",
								"type":"image",
								
								"x": 62,
								"y": 2 + 26,

								"image":"d:/ymir work/ui/game/windows/money_icon.sub",
							},
							
							{
								"name" : "gold_text_window", "type" : "window", "style" : ("attach",), "x" : 85, "y" : 26, "width" : 117, "height" : 18,
								"children" :
								(
									{ "name" : "gold_text_bg", "type":"expanded_image", "x":0, "y":0, "image" : ROOT_PATH + "yang_text_bg.sub", "x_scale" : 1.3, "y_scale" : 1.0, },
									{ "name" : "gold_text", "type" : "text", "x" : 0, "y" : 0, "all_align" : "center", "text" : "", },
								),
							},
						),
					},
					
					{
						"name"	:	"button_group",
						"type"	:	"window",
						
						"x"		:	BUTTON_GROUP_X,
						"y"		:	BUTTON_GROUP_Y,
						
						"style"	:	("attach",),
						
						"width"		:	243,
						"height"	:	25,
						
						"children"	:
						(
							{
								"name" : "modify_button",
								"type" : "button",

								"x" : 0,
								"y" : 0,
								
								"default_image" : ROOT_PATH + "modify_button_default.sub",
								"over_image" : ROOT_PATH + "modify_button_over.sub",
								"down_image" : ROOT_PATH + "modify_button_down.sub",
							},
							
							{
								"name" : "deco_button",
								"type" : "button",

								"x" : 0,
								"y" : 0,
								
								"default_image" : ROOT_PATH + "deco_button_default.sub",
								"over_image" : ROOT_PATH + "deco_button_over.sub",
								"down_image" : ROOT_PATH + "deco_button_down.sub",
							},
							
							{
								"name" : "reopen_button",
								"type" : "button",

								"x" : 0,
								"y" : 0,
								
								"horizontal_align"	: "center",

								"default_image" : ROOT_PATH + "reopen_button_default.sub",
								"over_image" : ROOT_PATH + "reopen_button_over.sub",
								"down_image" : ROOT_PATH + "reopen_button_down.sub",
							},
							
							{
								"name" : "tax_adjustment_button",
								"type" : "button",

								"x" : 57 + 5,
								"y" : 0,
								
								"default_image" : ROOT_PATH + "tax_adjustment_button_default.sub",
								"over_image" : ROOT_PATH + "tax_adjustment_button_over.sub",
								"down_image" : ROOT_PATH + "tax_adjustment_button_down.sub",
							},
							
							{
								"name" : "shop_close_button",
								"type" : "button",

								"x" : (57 + 5) * 2,
								"y" : 0,
								
								"default_image" : ROOT_PATH + "shop_close_button_default.sub",
								"over_image" : ROOT_PATH + "shop_close_button_over.sub",
								"down_image" : ROOT_PATH + "shop_close_button_down.sub",
							},
							
							{
								"name" : "shop_sales_button",
								"type" : "button",

								"x" : (57 + 5) * 3,
								"y" : 0,
								
								"default_image" : ROOT_PATH + "sale_button_default.sub",
								"over_image" : ROOT_PATH + "sale_button_over.sub",
								"down_image" : ROOT_PATH + "sale_button_down.sub",
							},
						),
					},
				),
			},
		),
	}