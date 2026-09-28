import uiScriptLocale
 
ROOT = "d:/ymir work/ui/game/"
 
window = {
    "name" : "ExchangeDialog",
 
    "x" : 0,
    "y" : 0,
 
    "style" : ("movable", "float",),
 
    "width" : 411,
    "height" : 225,
 
    "children" :
    (
        {
            "name" : "board",
            "type" : "board",
            "style" : ("attach",),
 
            "x" : 0,
            "y" : 0,
 
            "width" : 411,
            "height" : 225,
 
            "children" :
            (
                {
                    "name" : "TitleBar",
                    "type" : "titlebar",
                    "style" : ("attach",),
 
                    "x" : 8,
                    "y" : 8,
 
                    "width" : 398,
                    "color" : "gray",
 
                    "children" :
                    (
                        { "name":"TitleName", "type":"text", "x":192, "y":0, "text":uiScriptLocale.EXCHANGE_TITLE, "outline":"1","text_horizontal_align":"center" },
                    ),
                },
 
                {
                    "name" : "Middle_Bar",
                    "type" : "image",
 
                    "x" : 205,
                    "y" : 30,
 
                    "image" : "d:/ymir work/ui/middletab.tga",
                },
 
                {
                    "name" : "Owner",
                    "type" : "window",
 
                    "x" : 200,
                    "y" : 33,
 
                    "width" : 200,
                    "height" : 225,
 
                    "children" :
                    (
                        {
                            "name" : "Owner_Slot",
                            "type" : "grid_table",
 
                            "start_index" : 0,
 
                            "x" : 11,
                            "y" : 0,
 
                            "x_count" : 6,
                            "y_count" : 4,
                            "x_step" : 32,
                            "y_step" : 32,
                            "x_blank" : 0,
                            "y_blank" : 0,
 
                            "image" : "d:/ymir work/ui/public/slot_base.sub",
                        },
						{
							"name" : "Owner_Cheque",
							"type" : "button",

							"x" : 40,
							"y" : 160,


							"default_image" : "d:/ymir work/ui/public/parameter_slot_04.sub",
							"over_image" : "d:/ymir work/ui/public/parameter_slot_04.sub",
							"down_image" : "d:/ymir work/ui/public/parameter_slot_04.sub",

							"children" :
							(
								{
									"name" : "Owner_Cheque_Value",
									"type" : "text",

									"x" : 111,
									"y" : 2,

									"text" : "1234567",

									"text_horizontal_align" : "right",
								},
							),
						},
                        {
                            "name":"Cheque_Icon1",
                            "type":"image",

                            "x":17,
                            "y":161,

                            "image":"d:/ymir work/ui/game/windows/cheque_icon.sub",
                        },
                        {
                            "name" : "Owner_Money",
                            "type" : "button",
 
                            "x" : 40,
                            "y" : 136,
 
 
                            "default_image" : "d:/ymir work/ui/public/parameter_slot_04.sub",
                            "over_image" : "d:/ymir work/ui/public/parameter_slot_04.sub",
                            "down_image" : "d:/ymir work/ui/public/parameter_slot_04.sub",
 
                            "children" :
                            (
                                {
                                    "name" : "Owner_Money_Value",
                                    "type" : "text",
 
                                    "x" : 111,
                                    "y" : 2,
 
                                    "text" : "1234567",
 
                                    "text_horizontal_align" : "right",
                                },
                            ),
                        },
                        {
                            "name":"Money_Icon1",
                            "type":"image",

                            "x":13,
                            "y":137,

                            "image":"icon/emoji/money_icon.png",
                        },
                        {
                            "name" : "Owner_Accept_Light",
                            "type" : "button",
 
                            "x" : 160,
                            "y" : 135,
 
                            "default_image" : "d:/ymir work/ui/game/windows/accept_button_off.sub",
                            "over_image" : "d:/ymir work/ui/game/windows/accept_button_off.sub",
                            "down_image" : "d:/ymir work/ui/game/windows/accept_button_on.sub",
                        },
                        {
                            "name" : "Owner_Accept_Button",
                            "type" : "toggle_button",
 
                            "x" : 160,
                            "y" : 160,

                            "default_image" : "d:/ymir work/ui/accept0.tga",
                            "over_image" : "d:/ymir work/ui/accept1.tga",
                            "down_image" : "d:/ymir work/ui/accept2.tga",
                        },
                    ),
                },
 
                {
                    "name" : "Target",
                    "type" : "window",
 
                    "x" : 10,
                    "y" : 33,
 
                    "width" : 200,
                    "height" : 150,
 
                    "children" :
                    (
                        {
                            "name" : "Target_Slot",
                            "type" : "grid_table",
 
                            "start_index" : 0,
 
                            "x" : 0,
                            "y" : 0,
 
                            "x_count" : 6,
                            "y_count" : 4,
                            "x_step" : 32,
                            "y_step" : 32,
                            "x_blank" : 0,
                            "y_blank" : 0,
 
                            "image" : "d:/ymir work/ui/public/slot_base.sub",
                        },
                        {
                            "name" : "Target_Money",
                            "type" : "image",
 
                            "x" : 27,
                            "y" : 135,
 
                            "image" : "d:/ymir work/ui/public/parameter_slot_04.sub",
 
                            "children" :
                            (
                                {
                                    "name" : "Target_Money_Value",
                                    "type" : "text",
 
                                    "x" : 111,
                                    "y" : 2,
 
                                    "text" : "1234567",
 
                                    "text_horizontal_align" : "right",
                                },
                            ),
                        },
                        {
                            "name":"Money_Icon2",
                            "type":"image",

                            "x":2,
                            "y":137,

                            "image":"icon/emoji/money_icon.png",
                        },
						{
							"name" : "Target_Cheque",
							"type" : "image",

							"x" : 27,
							"y" : 160,

							"image" : "d:/ymir work/ui/public/parameter_slot_04.sub",

							"children" :
							(
								{
									"name" : "Target_Cheque_Value",
									"type" : "text",

									"x" : 111,
									"y" : 2,

									"text" : "1234567",

									"text_horizontal_align" : "right",
								},
							),
						},
                        {
                            "name":"Cheque_Icon2",
                            "type":"image",

                            "x":6,
                            "y":161,

                            "image":"d:/ymir work/ui/game/windows/cheque_icon.sub",
                        },
                        {
                            "name" : "Target_Accept_Light",
                            "type" : "button",
 
                            "x" : 148,
                            "y" : 135,
 
                            "default_image" : "d:/ymir work/ui/game/windows/accept_button_off.sub",
                            "over_image" : "d:/ymir work/ui/game/windows/accept_button_off.sub",
                            "down_image" : "d:/ymir work/ui/game/windows/accept_button_on.sub",
                        },
                    ),
                },
            ),
        },
    ),
}