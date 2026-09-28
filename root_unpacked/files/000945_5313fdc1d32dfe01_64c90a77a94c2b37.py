import uiScriptLocale
import item

MOUNT_SLOT_START = item.MOUNT_SLOT_START
IMAGE_PATH = "kowal/petmount/"
NEW_X = 11
NEW_Y = 24

window = {
	"name" : "MountWindow",
	
	"x" : 0,
	"y" : 0,
	
	"style" : ("movable", "float",),
	
	"width" : 586,
	"height" : 419,
	
	"children" :
	(
		{
			"name" : "board",
			"type" : "board",
			"style" : ("attach",),

			"x" : 0,
			"y" : 0,

			"width" : 561,
			"height" : 378,
			

			"children" :
			(
				{
					"name" : "mount_background",
					"type" : "image",
					"x" : 7,
					"y" : 19,
					"image" : IMAGE_PATH+"bg.png",
				},
				{
					"name" : "render_target",
					"type" : "render_target",
					
					"x" : 340,
					"y" : 50,
					
					"width" : 202, "height" : 284,
					
					"index" : 202,
					"children" :
					(
						{
							"type" : "image", "x" : 81, "y" : 37,
							"horizontal_align" : "center",
							"vertical_align" : "bottom",
							"image" : IMAGE_PATH+"skin_slot.png",
							
							"children" :
							(
								{
									"name" : "costume_slot", "type" : "slot", "x" : 0, "y" : 0, "width" : 182, "height" : 83,
									
									"slot" : 
									(
										{ "index" : item.COSTUME_SLOT_MOUNT, "x": 0, "y" : 2, "width" : 32, "height" : 32 },
									),
								},
							),
						},
					),
				},
				{
					"name" : "value_name", "type" : "text", "x" : 66, "y" : 36, "text" : "name", "outline" : 1,
				},
				{
					"name" : "value_level", "type" : "text", "x" : 244, "y" : 36, "text" : "100", "outline" : 1,
				},
				{
					"name" : "value_exp_current", "type" : "text", "x" : 42, "y" : 71, "text" : "exp_now", "outline" : 1,
				},
				{
					"name" : "value_exp_need", "type" : "text", "x" : 42, "y" : 96, "text" : "exp_need", "outline" : 1,
				},
				{
					"name" : "mount_feed_item", "type" : "text", "x" : 18, "y" : 120, "text" : "item", "outline" : 1,
				},
				{
					"name" : "label_max_hp", "type" : "text", "x" :30, "y" : 182, "text" : "name", "outline" : 1,
				},
				{
					"name" : "label_att_bonus_monster", "type" : "text", "x" : 30, "y" : 203, "text" : "name", "outline" : 1,
				},
				{
					"name" : "label_att_bonus_metine", "type" : "text", "x" : 30, "y" : 224, "text" : "name", "outline" : 1,
				},
				{
					"name" : "label_att_bonus_sefi", "type" : "text", "x" : 30, "y" : 245, "text" : "name", "outline" : 1,
				},
				{
					"name" : "label_att_bonus_dungeon", "type" : "text", "x" : 30, "y" : 266, "text" : "name", "outline" : 1,
				},
				{
					"name" : "equip_slot", "type" : "slot", "x" : 53, "y" : 295, "width" : 182, "height" : 83,
					
					"slot" : 
					(
						{ "index" : MOUNT_SLOT_START+0, "x": 33, "y" : 36, "width" : 32, "height" : 32 },
						{ "index" : MOUNT_SLOT_START+1, "x": 75, "y" : 36, "width" : 32, "height" : 32 },
						{ "index" : MOUNT_SLOT_START+2, "x": 117, "y" : 36, "width" : 32, "height" : 32 },
					),
				},
				{
					"name" : "exp_bar",
					"type" : "ani_image",

					"x" : 287,
					"y" : 57,
					
					"delay" : 6,
					"images" :
					(
						IMAGE_PATH+"exp_gauge/1.png",
						IMAGE_PATH+"exp_gauge/2.png",
						IMAGE_PATH+"exp_gauge/3.png",
						IMAGE_PATH+"exp_gauge/4.png",
						IMAGE_PATH+"exp_gauge/5.png",
						IMAGE_PATH+"exp_gauge/6.png",
						IMAGE_PATH+"exp_gauge/7.png",
						IMAGE_PATH+"exp_gauge/8.png",
						IMAGE_PATH+"exp_gauge/9.png",
						IMAGE_PATH+"exp_gauge/10.png",
						IMAGE_PATH+"exp_gauge/11.png",
						IMAGE_PATH+"exp_gauge/12.png",
						IMAGE_PATH+"exp_gauge/13.png",
						IMAGE_PATH+"exp_gauge/14.png",
						IMAGE_PATH+"exp_gauge/15.png",
						IMAGE_PATH+"exp_gauge/16.png",
						IMAGE_PATH+"exp_gauge/17.png",
						IMAGE_PATH+"exp_gauge/18.png",
					),
				},
				{
					"name" : "mount_button",
					"type" : "button",

					"x" : 160,
					"y" : 50,

					"horizontal_align" : "center",
					"vertical_align" : "bottom",

					"default_image" : IMAGE_PATH+"summon_btn_norm.png",
					"over_image" : IMAGE_PATH+"summon_btn_hover.png",
					"down_image" : IMAGE_PATH+"summon_btn_down.png",
				},
				{
					"name" : "mount_button_unsummon",
					"type" : "button",

					"x" : 160,
					"y" : 50,

					"horizontal_align" : "center",
					"vertical_align" : "bottom",

					"default_image" : IMAGE_PATH+"unsummon_btn_norm.png",
					"over_image" : IMAGE_PATH+"unsummon_btn_hover.png",
					"down_image" : IMAGE_PATH+"unsummon_btn_down.png",
				},
				{
					"name" : "TitleBar",
					"type" : "titlebar",
					"style" : ("attach",),

					"x" : 3,
					"y" : 0,

					"width" : 557,
					"color" : "yellow",

					"children" :
					(
						{ "name":"TitleName", "type":"text", "x":-56, "y":1, "text":uiScriptLocale.MOUNT_WINDOW_TITLE, "horizontal_align":"center", "outline" : 1 },
					),
				},
			),
		},
	),
}
