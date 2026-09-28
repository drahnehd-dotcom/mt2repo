#-*- coding: iso-8859-1 -*-
import uiScriptLocale
BOARD_WIDTH = 217
BOARD_HEIGHT = 160

window = {
    "name" : "Fragments_Window",
    "style" : ("movable", "float",),
    "x" : 0, "y" : 0,
    "width": BOARD_WIDTH,"height": BOARD_HEIGHT+40,
    "children" :
    (
        {
            "name" : "board_button",
            "type" : "board",
            "x": 0, "y": 132,
            "horizontal_align":"center",
            "width": 120,"height": 30,
            "children" :
            (
                {
                    "name":"AcceptButton",
                    "type":"button",
                    "x":0,"y":28,
                    "veritcal_align":"center",
                    "horizontal_align":"center",
                    "default_image":"d:/ymir work/ui/marmur_window/buy_btn.png",
                    "over_image":"d:/ymir work/ui/marmur_window/buy_btn1.png",
                    "down_image":"d:/ymir work/ui/marmur_window/buy_btn2.png",
                },
            ),
        },
        {
            "name" : "board",
            "type" : "board",
            "x": 0, "y": 0,
            "width": BOARD_WIDTH,"height": BOARD_HEIGHT,
            "children" :
            (
                {
                    "name" : "TitleBar",
                    "type" : "titlebar",
                    "style" : ("attach",),
                    "x" : 8,"y" : 7,
                    "width" : BOARD_WIDTH-15,
                    "color" : "yellow",
                    "children" :
                    (
                        { 
                            "name": "TitleName",
                            "type":"text",
                            "x":0,"y":-4,
                            "text": uiScriptLocale.STONEWINDOW_TITLE,
                            "outline":"1",
                            "all_align":"center",
                        },
                    ),
                },
                {
                    "name":"info",
                    "type":"image",
                    "x":16,"y":7,
                    "image":"d:/ymir work/ui/pattern/q_mark_01.tga",
                },
                {
                    "name":"window",
                    "type":"thinboard_circle",
                    "x":10,"y":28,
                    "width":BOARD_WIDTH-21,"height":BOARD_HEIGHT-61,
                    "children":
                    (
                        {
                            "name" : "ItemSlot",
                            "type" : "grid_table",

                            "x" : 1,
                            "y" : 1,

                            "start_index" : 0,
                            "x_count" : 6,
                            "y_count" : 3,
                            "x_step" : 32,
                            "y_step" : 32,
                            "x_blank": 0,
                            "y_blank": 0,
                            
                            "image" : "d:/ymir work/ui/public/Slot_Base.sub"
                        },
                    ),
                },
                {
                    "name":"fast_add",
                    "type":"text",
                    "x":0,
                    "y":58,
                    "all_align":"center",
                    "text":"fast_add_text",
                    "fontname" : "Tahoma:14",
                    "outline" : 1,
                },
            ),
        },
    ),
}