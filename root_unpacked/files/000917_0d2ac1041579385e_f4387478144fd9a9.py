
import app
import uiScriptLocale

BOARD_WIDTH = 283
BOARD_HEIGHT = 210
IMG_PATH = "d:/ymir work/ui/mount_window/"

window = {
        "name" : "Mount_Window",
        "style" : ("movable", "float",),
        "x" : 0, "y" : 0,
        "width": BOARD_WIDTH,"height": BOARD_HEIGHT+40,
        "children" :
        (
            {
                "name" : "board_button",
                "type" : "board",
                "x": 0, "y": 180,
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
                                "text": uiScriptLocale.HORSE_HOE_TITLE,
                                "outline":"1",
                                "all_align":"center",
                            },
                        ),
                    },
                    {
                        "name":"window",
                        "type":"thinboard_circle",
                        "x":10,"y":33,
                        "width":262,"height":65,
                        "children":
                        (
                            {
                                "name" : "board",
                                "type" : "image",
                                "x" : 0,
                                "y" : 2,
                                "vertical_align":"center",
                                "horizontal_align":"center",
                                "image":"d:/ymir work/ui/chest_board.png",
                                "children":
                                (
                                    {
                                        "name" : "HorseShoeSlot",
                                        "type" : "slot", 
                                        "x" : 113,"y" : 15,
                                        "width" : 32,"height" : 32,
                                        "slot" : (
                                            { "index" : 0, "x" : 0, "y" : 0, "width" : 32, "height" : 32 },
                                        ),
                                    },
                                ),
                            },
                        ),
                    },
                    {
                        "name":"window",
                        "type":"thinboard_circle",
                        "x":10,"y":98,
                        "width":262,"height":70,
                        "children":
                        (
                            {
                                "name" : "header",
                                "type" : "image",
                                "x" : 0,
                                "y" : 0,
                                "horizontal_align":"center",
                                "image":IMG_PATH+"header.png",
                                "children":
                                (
                                    {
                                        "name":"HeaderText",
                                        "type":"text",
                                        "x":0,"y":-1,
                                        "all_align":"center",
                                        "text":uiScriptLocale.HORSESHOE_REQUIRED_ITEMS,
                                        "fontname":"Tahoma:14b",
                                        "outline":"1",
                                    },
                                ),
                            },
                            {
                                "name":"Background",
                                "type":"image",
                                "image":IMG_PATH+"background.png",
                                "x":0,"y":9,
                                "vertical_align":"center",
                                "horizontal_align":"center",
                            },
                            {
                                "name" : "Real_Slot0",
                                "type" : "slot",
                                "x" : 51,"y" : 28,
                                "width" : 32,"height" : 32,
                                "slot" : (
                                    {"index":0, "x":0, "y":0, "width":32, "height":32},
                                ),
                            },
                            {
                                "name" : "Real_Slot1",
                                "type" : "slot",
                                "x" : 94,"y" : 28,
                                "width" : 32,"height" : 32,
                                "slot" : (
                                    {"index":0, "x":0, "y":0, "width":32, "height":32},
                                ),
                            },
                        ),
                    },
                    {
                        "name":"window",
                        "type":"thinboard_circle",
                        "x":10,"y":167,
                        "width":262,"height":30,
                        "children":
                        (
                            {
                                "name":"Background",
                                "type":"image",
                                "image":IMG_PATH+"background2.png",
                                "x":0,"y":0,
                                "vertical_align":"center",
                                "horizontal_align":"center",
                            },
                            {
                                "name":"Price",
                                "type":"text",
                                "x":0,"y":-2,
                                "all_align":"center",
                                "text":uiScriptLocale.HORSESHOE_PRICE,
                                "outline":"1",
                            },
                        ),
                    },
                ),
            },
        ),
    }
