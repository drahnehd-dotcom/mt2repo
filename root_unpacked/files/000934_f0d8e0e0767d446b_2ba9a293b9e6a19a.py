# -*- coding: utf-8 -*-
# MaintenanceDialog — GM panel z H/M/S input + lokalizacja 4 jezyki.
# Wszystkie teksty z uiScriptLocale (alias na localeInfo, locale_game.txt).

import uiScriptLocale
ROOT_PATH = "d:/ymir work/ui/public/"

# Helper: 3 inputy (Godz/Min/Sek) w jednej linii.
def _make_hms_row(name_prefix, base_x, base_y):
	field_w = 48
	gap = 10
	label_h = 12

	children = []
	# 3 boxy: Godziny | Minuty | Sekundy (lokalizowane labelki)
	field_specs = [
		(uiScriptLocale.MAINTENANCE_ADMIN_LABEL_HOUR, "Hour"),
		(uiScriptLocale.MAINTENANCE_ADMIN_LABEL_MIN, "Min"),
		(uiScriptLocale.MAINTENANCE_ADMIN_LABEL_SEC, "Sec"),
	]
	for idx, (lbl, suffix) in enumerate(field_specs):
		x_off = base_x + idx * (field_w + gap)
		children.append({
			"name" : "%s_label_%s" % (name_prefix, suffix),
			"type" : "text",
			"x" : x_off, "y" : base_y,
			"text" : lbl,
			"text_horizontal_align" : "center",
			"horizontal_align" : "left",
		})
		children.append({
			"name" : "%s_slot_%s" % (name_prefix, suffix),
			"type" : "slotbar",
			"x" : x_off, "y" : base_y + label_h + 2,
			"width" : field_w, "height" : 18,
			"children" : (
				{
					"name" : "%s_value_%s" % (name_prefix, suffix),
					"type" : "editline",
					"x" : 3, "y" : 3,
					"width" : field_w - 5, "height" : 18,
					"input_limit" : 3,
				},
			),
		})
	return children


# Dimensions
DIALOG_W = 220
DIALOG_H = 230

# 3 fields × 48px + 2 × 10gap = 164px → centered: (220 - 164) / 2 = 28
ROW_X = 28

window = {
	"name" : "MaintenanceDialog",
	"x" : 0, "y" : 0,
	"style" : ("movable", "float",),
	"width" : DIALOG_W,
	"height" : DIALOG_H,
	"children" :
	(
		{
			"name" : "board",
			"type" : "board",
			"x" : 0, "y" : 0,
			"width" : DIALOG_W, "height" : DIALOG_H,
			"children" :
			(
				{
					"name" : "titlebar",
					"type" : "titlebar",
					"style" : ("attach",),
					"x" : 8, "y" : 8,
					"width" : DIALOG_W - 16,
					"color" : "gray",
					"children" :
					(
						{
							"name" : "TitleName",
							"type" : "text",
							"x" : (DIALOG_W - 16) / 2, "y" : 3,
							"text" : uiScriptLocale.MAINTENANCE_ADMIN_TITLE,
							"text_horizontal_align" : "center"
						},
					),
				},
				# === SEKCJA 1: Czas do shutdown ===
				{
					"name" : "delay_title",
					"type" : "text",
					"x" : 0, "y" : 38,
					"text" : uiScriptLocale.MAINTENANCE_ADMIN_DELAY,
					"horizontal_align" : "center",
					"text_horizontal_align" : "center",
				},
			)
			+ tuple(_make_hms_row("delay", ROW_X, 56))
			+ (
				# === SEKCJA 2: Czas trwania ===
				{
					"name" : "duration_title",
					"type" : "text",
					"x" : 0, "y" : 110,
					"text" : uiScriptLocale.MAINTENANCE_ADMIN_DURATION,
					"horizontal_align" : "center",
					"text_horizontal_align" : "center",
				},
			)
			+ tuple(_make_hms_row("duration", ROW_X, 128))
			+ (
				# === Buttons ===
				{
					"name" : "start_maintenance",
					"type" : "button",
					"x" : 12, "y" : 185,
					"text" : uiScriptLocale.MAINTENANCE_ADMIN_START,
					"default_image" : ROOT_PATH + "large_Button_01.sub",
					"over_image" : ROOT_PATH + "large_Button_02.sub",
					"down_image" : ROOT_PATH + "large_Button_03.sub",
				},
				{
					"name" : "cancel_maintenance",
					"type" : "button",
					"x" : 113, "y" : 185,
					"text" : uiScriptLocale.MAINTENANCE_ADMIN_CANCEL,
					"default_image" : ROOT_PATH + "large_Button_01.sub",
					"over_image" : ROOT_PATH + "large_Button_02.sub",
					"down_image" : ROOT_PATH + "large_Button_03.sub",
				},
				# Hidden cancel (keep for compat)
				{
					"name" : "cancel_button",
					"type" : "button",
					"x" : 0, "y" : 250,  # hidden offscreen
					"text" : uiScriptLocale.CANCEL,
					"horizontal_align" : "center",
					"default_image" : ROOT_PATH + "Middle_Button_01.sub",
					"over_image" : ROOT_PATH + "Middle_Button_02.sub",
					"down_image" : ROOT_PATH + "Middle_Button_03.sub",
				},
			),
		},
	),
}
