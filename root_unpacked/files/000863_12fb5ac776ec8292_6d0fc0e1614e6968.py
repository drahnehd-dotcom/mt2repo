import uiScriptLocale
import player

IMG_PATH = "d:/ymir work/ui/buff/"
IMG_PATH2 = "d:/ymir work/ui/mount_window/"
SKILL_IMG_PATH = "d:/ymir work/ui/skill/shaman/"
PUBLIC_IMG_PATH = "d:/ymir work/ui/public/"
GAME_IMG_PATH = "d:/ymir work/ui/game/windows/"

BOARD_WIDTH = 241
BOARD_HEIGHT = 340

GOLD_COLOR	= 0xFFFEE3AE
WHITE_COLOR = 0xFFFFFFFF

BUFF_EQUIPMENT_START_INDEX = player.BUFF_EQUIPMENT_SLOT_START

window = {
	"name" : "BuffNPCWindow",
	"x" : 0,
	"y" : 0,
	"style" : ("movable", "float",),
	"width" : BOARD_WIDTH,
	"height" : BOARD_HEIGHT,
	"children" :
	(
		{
			"name" : "board",
			"type" : "board_with_titlebar",
			"x" : 0, "y" : 0,
			"width" : BOARD_WIDTH,
			"height" : BOARD_HEIGHT,
			"title" : uiScriptLocale.ASLAN_BUFF_TITLE_MAIN_BOARD,
			"children" :
			(
				{
					"name" : "Page_01",
					"type" : "window",
					"style" : ("attach",),
					"x" : 0, "y" : 30,
					"width" : BOARD_WIDTH,
					"height" : BOARD_HEIGHT-30,
					"children":
					(
						{
							"name" : "tb_board",
							"type" : "thinboard_circle",
							"x" : 10, "y" : 0,
							"width" : 220, "height" : 300,
							"children":
							(
								{ "name" : "b0ard", "type" : "image", "style" : ("not_pick",), "x" : 1, "y" : 1, "image" : IMG_PATH + "board_real.png"},

								{ "name" : "face_icon_empty",   "type" : "image", "style" : ("not_pick",), "x" : 155, "y" : 16, "image" : IMG_PATH + "icon_face_empty.tga"},
								{ "name" : "face_icon_0",       "type" : "image", "style" : ("not_pick",), "x" : 155, "y" : 16, "image" : "icon/face/shaman_m.tga" },
								{ "name" : "face_icon_1",       "type" : "image", "style" : ("not_pick",), "x" : 155, "y" : 16, "image" : "icon/face/shaman_w.tga" },
								{ "name" : "face_icon_overlay", "type" : "image", "style" : ("not_pick",), "x" : 153, "y" : 12, "image" : IMG_PATH + "face_slot.sub"},

								{
									"name" : "info_board", "type" : "text", "x" : 25, "y" : 4, "text":"",
									"children" :
									(
										{ "name":"buff_name",  "type":"text", "x":0, "y":5,  "text":"", "outline":1, "fontname":"Tahoma:14", },
									),
								},

								{
									"name":"header", "type":"image", "style" : ("not_pick",),
									"x" : 0, "y" : 80,
									"image":IMG_PATH+"header.png",
									"children":
									(
										{ "name":"header_text", "type":"text", "x":0, "y":0, "text": uiScriptLocale.ASLAN_BUFF_EQUIPMENT, "outline":1, "all_align":"center", },
									),
								},
								{
									"name" : "eq_board", "type" : "image", "style" : ("not_pick",), "x" : 45, "y" : 113, "image" : IMG_PATH + "equipment.png",
									"children" :
									(
										{
											"name" : "equipment_slots", "type" : "slot", "x" : 0, "y" : 0,
											"width" : 115, "height" : 178,
											"slot" :	(
												{"index": BUFF_EQUIPMENT_START_INDEX+0, "x":  1, "y":  36, "width":32, "height":32},
												{"index": BUFF_EQUIPMENT_START_INDEX+1, "x": 50, "y":   0, "width":32, "height":32},
												{"index": BUFF_EQUIPMENT_START_INDEX+2, "x": 51, "y":  36, "width":32, "height":64},
												{"index": BUFF_EQUIPMENT_START_INDEX+3, "x": 98, "y":   7, "width":32, "height":32},
											),
										},
									),
								},
								{
									"name":"header", "type":"image", "style" : ("not_pick",),
									"x" : 0, "y" : 223,
									"image":IMG_PATH+"header.png",
									"children":
									(
										{ "name":"header_text", "type":"text", "x":0, "y":0, "text": uiScriptLocale.ASLAN_BUFF_SKILLS, "outline":1, "all_align":"center", },
									),
								},
								{
									"name" : "skill_slots", "type" : "grid_table",
									"x" : 8, "y" : 248,
									"start_index" : 0,
									"x_count" : 3,
									"y_count" : 1,
									"x_step" : 0 + 70,
									"y_step" : 32,
									"image" : IMG_PATH+"slot.png",
								},
								{
									"name" : "skill_slots",
									"type" : "slot", "x" : 24, "y" : 206,
									"width" : 170, "height" : 100,
									"image" : "d:/ymir work/ui/public/Slot_Base.sub",
									"slot" :	(
										{"index": 0, "x":   0, "y":  50, "width":32, "height":32},
										{"index": 1, "x":  70, "y":  50, "width":32, "height":32},
										{"index": 2, "x": 140, "y":  50, "width":32, "height":32},
									),
								},

								{
									"name" : "summon_button1", "type" : "button", "x" : 24, "y" : 50,
									"default_image" : "d:/ymir work/ui/public/large_button_01.sub",
									"over_image" : "d:/ymir work/ui/public/large_button_02.sub",
									"down_image" : "d:/ymir work/ui/public/large_button_03.sub",
									"text" : uiScriptLocale.ASLAN_BUFF_UNSUMMON,
								},
								{
									"name" : "summon_button2", "type" : "button", "x" : 24, "y" : 50,
									"default_image" : "d:/ymir work/ui/public/large_button_01.sub",
									"over_image" : "d:/ymir work/ui/public/large_button_02.sub",
									"down_image" : "d:/ymir work/ui/public/large_button_03.sub",
									"text" : uiScriptLocale.ASLAN_BUFF_SUMMON,
								},
							),
						},
					),
				},
			)
		},
	),
}
