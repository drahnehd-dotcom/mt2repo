import uiScriptLocale

window = {
	"name" : "GuildWindow_BoardPage",

	"x" : 8,
	"y" : 30,

	"width" : 360,
	"height" : 298,

	"children" :
	(

		{
			"name" : "GradeNumber", "type" : "image", "x" : 21, "y" : 8, "image" : "d:/ymir work/ui/number_icon.png",
			"tooltip_text_new" : uiScriptLocale.GUILD_GRADE_NUM,
			"tooltip_text_color" : 0xfff1e6c0,
			"tooltip_x" : 0,
			"tooltip_y" : -35,
		},
		{
			"name" : "GradeName", "type" : "image", "x" : 77, "y" : 8, "image" : "d:/ymir work/ui/rank_image.png",
			"tooltip_text_new" : uiScriptLocale.GUILD_GRADE_RANK,
			"tooltip_text_color" : 0xfff1e6c0,
			"tooltip_x" : 0,
			"tooltip_y" : -35,
		},
		{
			"name" : "InviteAuthority", "type" : "image", "x" : 137, "y" : 8, "image" : "d:/ymir work/ui/invite_icon.png",
			"tooltip_text_new" : uiScriptLocale.GUILD_GRADE_PERMISSION_JOIN,
			"tooltip_text_color" : 0xfff1e6c0,
			"tooltip_x" : 0,
			"tooltip_y" : -35,
		},
		{
			"name" : "DriveOutAuthority", "type" : "image", "x" : 193, "y" : 8, "image" : "d:/ymir work/ui/delete_icon.png",
			"tooltip_text_new" : uiScriptLocale.GUILD_GRADE_PERMISSION_DELETE,
			"tooltip_text_color" : 0xfff1e6c0,
			"tooltip_x" : 0,
			"tooltip_y" : -35,
		},
		{
			"name" : "NoticeAuthority", "type" : "image", "x" : 244, "y" : 8, "image" : "d:/ymir work/ui/notice_icon.png",
			"tooltip_text_new" : uiScriptLocale.GUILD_GRADE_PERMISSION_NOTICE,
			"tooltip_text_color" : 0xfff1e6c0,
			"tooltip_x" : 0,
			"tooltip_y" : -35,
		},
		{
			"name" : "SkillAuthority", "type" : "image", "x" : 304, "y" : 8, "image" : "d:/ymir work/ui/um_icon.png",
			"tooltip_text_new" : uiScriptLocale.GUILD_GRADE_PERMISSION_SKILL,
			"tooltip_text_color" : 0xfff1e6c0,
			"tooltip_x" : 0,
			"tooltip_y" : -35,
		},

	),
}
