import item
import app
import uiScriptLocale

BOARD_WIDTH = 273
BOARD_HEIGHT = 399
MOUNT_SLOT_START = item.MOUNT_SLOT_START
PET_PATH = "kowal/game/companion{}"

window = {
	"name" : "companionWindow",
	"style" : ("movable", "float",),
	"x" : 0, "y" : 0,
	"width": 286+39,"height": 399,
	"children" :
	(
		{
			"name" : "board_01",
			"type" : "window",
			"style" : ("attach",),
			"x" : 0, "y" : 0,
			"width" : 286+39, "height" : BOARD_HEIGHT,
			"children":
			(
				{
					"name" : "bg",
					"type" : "image",
					"x" : 39,
					"y" : 0,
					"image" : PET_PATH.format("/bg_pet.png"),
				},
				{
					"name" : "petNameHeader",
					"type" : "window",
					"x" : 110,
					"y" : 67,
					"width" : 90,
					"height" : 18,
					"children":
					(
						{
							"name" : "petNameText",
							"type" : "text",
							"text": uiScriptLocale.COMPANION_LABEL_NAME,
							"x": 0,
							"y" : 0,
							"color":0xFFeed8c3,
							"outline": 1,
							"all_align" : "center"
						},
					),
				},
				{
					"name" : "petFeedItemHeader",
					"type" : "window",
					"x" : 110,
					"y" : 67+21,
					"width" : 90,
					"height" : 18,
					"children":
					(
						{
							"name" : "petFeedItemText",
							"type" : "text",
							"text": uiScriptLocale.COMPANION_LABEL_FEED_ITEM,
							"x": 0,
							"y" : 0,
							"color":0xFFeed8c3,
							"outline": 1,
							"all_align" : "center"
						},
					),
				},
				{
					"name" : "petLevelHeader",
					"type" : "window",
					"x" : 110,
					"y" : 67+21+21,
					"width" : 90,
					"height" : 18,
					"children":
					(
						{
							"name" : "petLevelText",
							"type" : "text",
							"text": uiScriptLocale.COMPANION_LABEL_LEVEL,
							"x": 0,
							"y" : 0,
							"color":0xFFeed8c3,
							"outline": 1,
							"all_align" : "center"
						},
					),
				},
				{
					"name" : "petNameValue",
					"type" : "window",
					"x" : 203,
					"y" : 66,
					"width" : 111,
					"height" : 18,
					"children":
					(
						{
							"name" : "pet_name",
							"type" : "text",
							"text": "",
							"x": 0,
							"y" : 0,
							"all_align" : "center"
						},
					),
				},
				{
					"name" : "petFeedItemValue",
					"type" : "window",
					"x" : 203,
					"y" : 66+21,
					"width" : 111,
					"height" : 18,
					"children":
					(
						{
							"name" : "pet_feed_item",
							"type" : "text",
							"text": "",
							"x": 0,
							"y" : 0,
							"all_align" : "center"
						},
					),
				},
				{
					"name" : "petLevelValue",
					"type" : "window",
					"x" : 203,
					"y" : 66+21+21,
					"width" : 111,
					"height" : 18,
					"children":
					(
						{
							"name" : "pet_level",
							"type" : "text",
							"text": "",
							"x": 0,
							"y" : 0,
							"all_align" : "center"
						},
					),
				},
				{
					"name" : "petExpWindow",
					"type" : "window",
					"x" : 48,
					"y" : 150,
					"width" : 265,
					"height" : 38,
					"children":
					(
						{
							"name" : "exp_bar_base",
							"type" : "image",
							"x" : 74,
							"y" : 8,
							"image": PET_PATH.format("/exp_base.png"),
						},
						{ "name" : "exp_gauge_01", "type" : "expanded_image", "x" : 75 + 0, "y" : 7, "image" : PET_PATH.format("/exp_full.png") },
						{ "name" : "exp_gauge_02", "type" : "expanded_image", "x" : 75 + 31, "y" : 7, "image" : PET_PATH.format("/exp_full.png") },
						{ "name" : "exp_gauge_03", "type" : "expanded_image", "x" : 75 + 62, "y" : 7, "image" : PET_PATH.format("/exp_full.png") },
						{ "name" : "exp_gauge_04", "type" : "expanded_image", "x" : 75 + 93, "y" : 7, "image" : PET_PATH.format("/exp_full.png") },
						{ "name" : "exp_hover_info", "type" : "window", "x" : 0, "y" : 0, "width" : 265, "height" : 38},
					),
				},
				{
					"name" : "islot",
					"type" : "slot",
					"x" : 65,
					"y" : 80,
					"width" : 32,
					"height" : 32,
					"slot" : (
						{"index":item.SLOT_ITEM_NEW_PET, "x":0, "y":0, "width":32, "height":32},
					),
				},
				{
					"name" : "generalInfoHeader",
					"type" : "window",
					"x" : 48, "y" : 34,
					"width" : 267, "height" : 31,
					"children":
					(
						{
							"name":"header_text",
							"type":"text",
							"x":0,
							"y":0,
							"text":uiScriptLocale.PET_GENERAL_INFORMATIONS,
							"outline" : 1,
	
							"color":0xFFeed8c3,
							"all_align" : "center",
						},
					),
				},
				{
					"name" : "petSkillsHeader",
					"type" : "window",
					"x" : 48, "y" : 190,
					"width" : 267, "height" : 31,
					"children":
					(
						{
							"name":"header_text",
							"type":"text",
							"x":0,
							"y":0,
							"text":uiScriptLocale.PET_SKILS,
							"outline" : 1,
	
							"color":0xFFeed8c3,
							"all_align" : "center",
						},
					),
				},
				{
					"name" : "petEquipmentHeader",
					"type" : "window",
					"x" : 48, "y" : 311,
					"width" : 267, "height" : 31,
					"children":
					(
						{
							"name":"header_text",
							"type":"text",
							"x":0,
							"y":0,
							"text":uiScriptLocale.PET_EQUIPMENT,
							"outline" : 1,
	
							"color":0xFFeed8c3,
							"all_align" : "center",
						},
					),
				},
				{
					"name":"petSkillPoints",
					"type":"image",
					"x" : 280,
					"y" : 201,
					"image": PET_PATH.format("/skillpoints.png"),
					"children":
					(
						{
							"name":"skill_points",
							"type":"text",
							"x":0,"y":-1,
							"all_align":"center",
							"outline":"1",
							"text":"0",
						},
					),
				},
				{
					"name":"petSkillSlots",
					"type":"image",
					"x":57,"y":226,
					"image": PET_PATH.format("/skill_pet.png"),
					"children":
					(
						{
							"name" : "skills", "type" : "grid_table",
							"x" : 4, "y" : 4,
							"start_index" : 0,
							# 7 umiejetnosci: 6 w gornym rzedzie, 1 w dolnym.
							# Siatka zgodna z tlem skill_pet.png (250x82, 6x2 ramek).
							"x_count" : 6,
							"y_count" : 2,
							"x_step" : 42,
							"y_step" : 42,
						},
					),
				},
				{
					"name":"petEquipmentSlots",
					"type":"image",
					"x":73,"y":347,
					"image": PET_PATH.format("/item_pet.png"),
					"children":
					(
						{
							"name" : "eqs",
							"type" : "slot",
							"x" : 3,
							"y" : 3,
							"width" : 250,
							"height" : 50,
							"slot" : (
								{"index":item.SLOT_ITEM_NEW_PET_EQ_START, "x":0, "y":0, "width":32, "height":32},
								{"index":item.SLOT_ITEM_NEW_PET_EQ_START + 1, "x":44, "y":0, "width":32, "height":32},
								{"index":item.SLOT_ITEM_NEW_PET_EQ_START + 2, "x":44+44, "y":0, "width":32, "height":32},
							),
						},
					),
				},
			),
		},
		{
			"name" : "board_02",
			"type" : "window",
			"style" : ("attach",),
			"x" : 0, "y" : 0,
			"width" : 286+39, "height" : BOARD_HEIGHT,
			"children":
			(
				{
					"name" : "bg",
					"type" : "image",
					"x" : 39,
					"y" : 0,
					"image" : PET_PATH.format("/bg_mount.png"),
				},
				{
					"name" : "mountNameHeader",
					"type" : "window",
					"x" : 110,
					"y" : 67,
					"width" : 90,
					"height" : 18,
					"children":
					(
						{
							"name" : "mountNameText",
							"type" : "text",
							"text": uiScriptLocale.COMPANION_LABEL_NAME,
							"x": 0,
							"y" : 0,
							"color":0xFFeed8c3,
							"outline": 1,
							"all_align" : "center"
						},
					),
				},
				{
					"name" : "petFeedItemHeader",
					"type" : "window",
					"x" : 110,
					"y" : 67+21,
					"width" : 90,
					"height" : 18,
					"children":
					(
						{
							"name" : "petFeedItemText",
							"type" : "text",
							"text": uiScriptLocale.COMPANION_LABEL_FEED_ITEM,
							"x": 0,
							"y" : 0,
							"color":0xFFeed8c3,
							"outline": 1,
							"all_align" : "center"
						},
					),
				},
				{
					"name" : "petLevelHeader",
					"type" : "window",
					"x" : 110,
					"y" : 67+21+21,
					"width" : 90,
					"height" : 18,
					"children":
					(
						{
							"name" : "petLevelText",
							"type" : "text",
							"text": uiScriptLocale.COMPANION_LABEL_LEVEL,
							"x": 0,
							"y" : 0,
							"color":0xFFeed8c3,
							"outline": 1,
							"all_align" : "center"
						},
					),
				},
				{
					"name" : "mountNameValue",
					"type" : "window",
					"x" : 203,
					"y" : 66,
					"width" : 111,
					"height" : 18,
					"children":
					(
						{
							"name" : "value_name",
							"type" : "text",
							"text": "",
							"x": 0,
							"y" : 0,
							"all_align" : "center"
						},
					),
				},
				{
					"name" : "mountFeedItemValue",
					"type" : "window",
					"x" : 203,
					"y" : 66+21,
					"width" : 111,
					"height" : 18,
					"children":
					(
						{
							"name" : "mount_feed_item",
							"type" : "text",
							"text": "",
							"x": 0,
							"y" : 0,
							"all_align" : "center"
						},
					),
				},
				{
					"name" : "mountLevelValue",
					"type" : "window",
					"x" : 203,
					"y" : 66+21+21,
					"width" : 111,
					"height" : 18,
					"children":
					(
						{
							"name" : "value_level",
							"type" : "text",
							"text": "",
							"x": 0,
							"y" : 0,
							"all_align" : "center"
						},
					),
				},
				{
					"name" : "mountExpWindow",
					"type" : "window",
					"x" : 48,
					"y" : 150,
					"width" : 265,
					"height" : 38,
					"children":
					(
						{
							"name" : "mount_exp_bar_base",
							"type" : "image",
							"x" : 74,
							"y" : 8,
							"image": PET_PATH.format("/exp_base.png"),
						},
						{ "name" : "mount_exp_gauge_01", "type" : "expanded_image", "x" : 75 + 0, "y" : 7, "image" : PET_PATH.format("/exp_full.png") },
						{ "name" : "mount_exp_gauge_02", "type" : "expanded_image", "x" : 75 + 31, "y" : 7, "image" : PET_PATH.format("/exp_full.png") },
						{ "name" : "mount_exp_gauge_03", "type" : "expanded_image", "x" : 75 + 62, "y" : 7, "image" : PET_PATH.format("/exp_full.png") },
						{ "name" : "mount_exp_gauge_04", "type" : "expanded_image", "x" : 75 + 93, "y" : 7, "image" : PET_PATH.format("/exp_full.png") },
						{ "name" : "mount_exp_hover_info", "type" : "window", "x" : 0, "y" : 0, "width" : 265, "height" : 38},
					),
				},
				{
					"name":"mountBonuses",
					"type":"image",
					"x":48,"y":223,
					"image": PET_PATH.format("/mount_bonuses.png"),
				},
				{
					"name" : "label_att_bonus_monster", "type" : "text", "x" : 73, "y" : 226, "text" : "", "outline" : 1,
				},
				{
					"name" : "label_block_chance", "type" : "text", "x" : 73, "y" : 226+23, "text" : "", "outline" : 1,
				},
				{
					"name" : "label_resist_monster", "type" : "text", "x" : 73, "y" : 226+23+23, "text" : "", "outline" : 1,
				},
				{
					"name" : "label_mount_movement_speed", "type" : "text", "x" : 73, "y" : 226+23+23+23, "text" : "", "outline" : 1,
				},
				{
					"name" : "mount_slot",
					"type" : "image",
					"x" : 59,
					"y" : 77,
					"image": PET_PATH.format("/mount_slot.png"),
					"children" :
					(
						{
							"name" : "costume_slot", "type" : "slot", "x" : 3, "y" : 2, "width" : 32, "height" : 32,
							"slot" :
							(
								{ "index" : item.COSTUME_SLOT_MOUNT, "x": 0, "y" : 0, "width" : 32, "height" : 32 },
							),
						},
					),
				},
				{
					"name" : "mount_button",
					"type" : "button",
					"x" : 135,
					"y" : 47,
					"horizontal_align" : "center",
					"vertical_align" : "bottom",
					"default_image" : PET_PATH.format("/summon_btn_norm.png"),
					"over_image" : PET_PATH.format("/summon_btn_hover.png"),
					"down_image" : PET_PATH.format("/summon_btn_down.png"),
				},
				{
					"name" : "mount_button_unsummon",
					"type" : "button",
					"x" : 135,
					"y" : 47,
					"horizontal_align" : "center",
					"vertical_align" : "bottom",
					"default_image" : PET_PATH.format("/unsummon_btn_norm.png"),
					"over_image" : PET_PATH.format("/unsummon_btn_hover.png"),
					"down_image" : PET_PATH.format("/unsummon_btn_down.png"),
				},
				{
					"name" : "generalInfoHeader",
					"type" : "window",
					"x" : 48, "y" : 34,
					"width" : 267, "height" : 31,
					"children":
					(
						{
							"name":"header_text",
							"type":"text",
							"x":0,
							"y":0,
							"text":uiScriptLocale.PET_GENERAL_INFORMATIONS,
							"outline" : 1,
	
							"color":0xFFeed8c3,
							"all_align" : "center",
						},
					),
				},
				{
					"name" : "mountBonusesHeader",
					"type" : "window",
					"x" : 48, "y" : 190,
					"width" : 267, "height" : 31,
					"children":
					(
						{
							"name":"header_text",
							"type":"text",
							"x":0,
							"y":0,
							"text":uiScriptLocale.MOUNT_BONUSES,
							"outline" : 1,
	
							"color":0xFFeed8c3,
							"all_align" : "center",
						},
					),
				},
				{
					"name" : "mountEquipmentHeader",
					"type" : "window",
					"x" : 48, "y" : 314,
					"width" : 267, "height" : 31,
					"children":
					(
						{
							"name":"header_text",
							"type":"text",
							"x":0,
							"y":0,
							"text":uiScriptLocale.PET_EQUIPMENT,
							"outline" : 1,
	
							"color":0xFFeed8c3,
							"all_align" : "center",
						},
					),
				},
				{
					"name":"mountEquipmentSlots",
					"type":"image",
					"x":116,"y":347,
					"image": PET_PATH.format("/item_mount.png"),
					"children":
					(
						{
							"name" : "equip_slot", "type" : "slot", "x" : 0, "y" : 0, "width" : 128, "height" : 40,
							"slot" :
							(
								{ "index" : MOUNT_SLOT_START-1+0, "x": 5, "y" : 5, "width" : 32, "height" : 32 },
								{ "index" : MOUNT_SLOT_START-1+1, "x": 5+44, "y" : 5, "width" : 32, "height" : 32 },
								{ "index" : MOUNT_SLOT_START-1+2, "x": 5+44+44, "y" : 5, "width" : 32, "height" : 32 },
							),
						},
					),
				},
			),
		},
		{
			"name" : "TitleBar",
			"type" : "titlebar",
			"style" : ("attach",),
			"x" : 21+39,
			"y" : 11,
			"width" : 243,
			"color" : "red",
			"children" :
			(
				{
					"name" : "TitleName",
					"type" : "text",
					"text" : uiScriptLocale.COMPANION_TITLE,
					"horizontal_align" : "center",
					"text_horizontal_align" : "center",
					"outline": 1,
					"x" : 0,
					"y" : 2,
				},
			),
		},
	),
}
