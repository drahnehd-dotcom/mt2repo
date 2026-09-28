import uiScriptLocale

window = {
	"name" : "SelectSkillDialog",
	"style" : ("movable", "float",),

	"x" : 0,
	"y" : 0,

	"width" : 360,
	"height" : 200,

	"children" :
	(
		{
			"name" : "Board",
			"type" : "board",
			"style" : ("attach",),

			"x" : 0,
			"y" : 0,

			"width" : 360,
			"height" : 178,

			"children" :
			(
				{
					"name" : "TitleBar",
					"type" : "titlebar",
					"style" : ("attach",),

					"x" : 8,
					"y" : 7,

					"width" : 344,
					"color" : "red",

					"children":
					(
						{ "name" : "TitleName", "type":"text", "x":0, "y":-1, "text":uiScriptLocale.SKILL_SELECT_TITLE, "all_align":"center" },
					),
				},

				# --- Naglowek lewej kolumny (pierwsza grupa skilli) ---
				{
					"name" : "FirstHeaderBar",
					"type" : "bar",
					"style" : ("not_pick",),

					"x" : 20,
					"y" : 34,

					"width" : 150,
					"height" : 20,

					"color" : 0x99000000,
				},
				{
					"name" : "FirstHeaderName",
					"type" : "text",

					"x" : 95,
					"y" : 39,

					"text" : "",
					"text_horizontal_align" : "center",
				},

				# --- Naglowek prawej kolumny (druga grupa skilli) ---
				{
					"name" : "SecondHeaderBar",
					"type" : "bar",
					"style" : ("not_pick",),

					"x" : 190,
					"y" : 34,

					"width" : 150,
					"height" : 20,

					"color" : 0x99000000,
				},
				{
					"name" : "SecondHeaderName",
					"type" : "text",

					"x" : 265,
					"y" : 39,

					"text" : "",
					"text_horizontal_align" : "center",
				},

				# --- Lewa kolumna: siatka ikon 3x2 (pierwsza grupa) ---
				{
					"name" : "FirstSkillSlotBack",
					"type" : "grid_table",

					"x" : 39,
					"y" : 62,

					"start_index" : 0,

					"x_count" : 3,
					"y_count" : 2,

					"x_step" : 40,
					"y_step" : 40,

					"x_blank" : 0,
					"y_blank" : 0,
				},
				{
					"name" : "FirstSkillSlot",
					"type" : "grid_table",

					"x" : 43,
					"y" : 66,

					"start_index" : 0,

					"x_count" : 3,
					"y_count" : 2,

					"x_step" : 40,
					"y_step" : 40,

					"x_blank" : 0,
					"y_blank" : 0,

					"image" : "d:/ymir work/ui/public/Slot_Base.sub",
				},

				# --- Prawa kolumna: siatka ikon 3x2 (druga grupa) ---
				{
					"name" : "SecondSkillSlotBack",
					"type" : "grid_table",

					"x" : 209,
					"y" : 62,

					"start_index" : 0,

					"x_count" : 3,
					"y_count" : 2,

					"x_step" : 40,
					"y_step" : 40,

					"x_blank" : 0,
					"y_blank" : 0,
				},
				{
					"name" : "SecondSkillSlot",
					"type" : "grid_table",

					"x" : 213,
					"y" : 66,

					"start_index" : 0,

					"x_count" : 3,
					"y_count" : 2,

					"x_step" : 40,
					"y_step" : 40,

					"x_blank" : 0,
					"y_blank" : 0,

					"image" : "d:/ymir work/ui/public/Slot_Base.sub",
				},

				# --- Przyciski wyboru (ptaszek) pod kolumnami ---
				{
					"name" : "SelectButtonFirst",
					"type" : "button",

					"x" : 65,
					"y" : 146,

					"default_image" : "d:/ymir work/ui/public/acceptbutton00.sub",
					"over_image" : "d:/ymir work/ui/public/acceptbutton01.sub",
					"down_image" : "d:/ymir work/ui/public/acceptbutton02.sub",
				},
				{
					"name" : "SelectButtonSecond",
					"type" : "button",

					"x" : 235,
					"y" : 146,

					"default_image" : "d:/ymir work/ui/public/acceptbutton00.sub",
					"over_image" : "d:/ymir work/ui/public/acceptbutton01.sub",
					"down_image" : "d:/ymir work/ui/public/acceptbutton02.sub",
				},
			),
		},
	),
}
