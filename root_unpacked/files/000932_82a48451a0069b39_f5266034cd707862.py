import uiScriptLocale

# ====================================================================
# KowalMT2 login window (redesign)
# Board image: Assets/kowal/intrologin/board.png (766 x 349)
# Layout: logo (top), center board with 3 inputs + login button,
#         saved accounts in TWO columns (left/right) inside the board,
#         channel buttons CH1-CH6 row below the board, exit top-right.
# Child names kept compatible with intrologin.py GetChild() bindings.
# ====================================================================

BOARD_W = 766
BOARD_H = 349

# center login column (inside board)
INPUT_W = 218
INPUT_H = 44
CENTER_X = (BOARD_W - INPUT_W) // 2          # 274
LOGIN_BTN_W = 179

# saved-account columns (inside board)
ROW_W = 236
ROW_H = 44
ROW_SPACING = 46
LEFT_COL_X = 16
RIGHT_COL_X = BOARD_W - ROW_W - 16           # 514
ACC_TOP_Y = 56

window = {
	"name": "LoginWindow",
	"style": ("movable",),

	"x": 0,
	"y": 0,
	"width": SCREEN_WIDTH,
	"height": SCREEN_HEIGHT,

	"children": (
		# ---- full-screen background ----
		{
			"name": "background",
			"type": "expanded_image",
			"x": 0,
			"y": 0,
			"x_scale": float(SCREEN_WIDTH) / 1920.0,
			"y_scale": float(SCREEN_HEIGHT) / 1080.0,
			"image": "Assets/kowal/intrologin/bg.png",
			"not_pick": 1,
		},

		# ---- dark overlay (for popups) ----
		{
			"name": "dark_background",
			"type": "bar",
			"x": 0,
			"y": 0,
			"width": SCREEN_WIDTH,
			"height": SCREEN_HEIGHT,
			"color": 0x70000000,
		},

		# ---- logo (top center) ----
		{
			"name": "logo",
			"type": "image",
			"x": 0,
			"y": -275,
			"horizontal_align": "center",
			"vertical_align": "center",
			"image": "Assets/kowal/intrologin/logo.png",
			"not_pick": 1,
		},

		# ---- exit button (top-right corner) ----
		{
			"name": "exit_button",
			"type": "button",
			"x": SCREEN_WIDTH - 70,
			"y": 5,
			"default_image": "Assets/kowal/intrologin/exit0.png",
			"over_image": "Assets/kowal/intrologin/exit1.png",
			"down_image": "Assets/kowal/intrologin/exit2.png",
		},

		# =============================================================
		# MAIN LOGIN BOARD (centered) -- board.png 766x349
		# =============================================================
		{
			"name": "login_board",
			"type": "expanded_image",
			"x": 0,
			"y": 10,
			"horizontal_align": "center",
			"vertical_align": "center",
			"image": "Assets/kowal/intrologin/board.png",

			"children": (
				# ---- saved accounts container (rendered as 2 columns in Python) ----
				{
					"name": "accounts_board",
					"not_pick": 1,
					"type": "window",
					"x": 0,
					"y": 0,
					"width": BOARD_W,
					"height": BOARD_H,

					"children": (
						{
							"name": "accounts_list",
							"not_pick": 1,
							"type": "window",
							"x": 0,
							"y": 0,
							"width": BOARD_W,
							"height": BOARD_H,
							"children": (),
						},
					),
				},

				# ---- header "LOGOWANIE" ----
				{
					"name": "userpanel_title",
					"type": "text",
					"x": BOARD_W // 2,
					"y": 91,
					"text": uiScriptLocale.LOGIN_PANEL_TITLE,
					"text_horizontal_align": "center",
					"not_pick": 1,
				},

				# ---- username input ----
				{
					"name": "username_input_bg",
					"type": "image",
					"x": CENTER_X,
					"y": 126,
					"image": "Assets/kowal/intrologin/input.png",
					"not_pick": 1,
				},
				{
					"name": "login_input",
					"type": "editline",
					"x": CENTER_X + 23,
					"y": 139,
					"width": INPUT_W - 28,
					"height": 18,
					"input_limit": 16,
					"enable_codepage": 0,
				},

				# ---- password input ----
				{
					"name": "password_input_bg",
					"type": "image",
					"x": CENTER_X,
					"y": 161,
					"image": "Assets/kowal/intrologin/input.png",
					"not_pick": 1,
				},
				{
					"name": "password_input",
					"type": "editline",
					"x": CENTER_X + 23,
					"y": 174,
					"width": INPUT_W - 28,
					"height": 18,
					"input_limit": 16,
					"secret_flag": 1,
					"enable_codepage": 0,
				},

				# ---- PIN input ----
				{
					"name": "pin_input_bg",
					"type": "image",
					"x": CENTER_X,
					"y": 196,
					"image": "Assets/kowal/intrologin/input.png",
					"not_pick": 1,
				},
				{
					"name": "pin_input",
					"type": "editline",
					"x": CENTER_X + 23,
					"y": 209,
					"width": INPUT_W - 28,
					"height": 18,
					"input_limit": 8,
					"secret_flag": 1,
					"enable_codepage": 0,
				},

				# ---- login button ----
				{
					"name": "login_button",
					"type": "button",
					"x": (BOARD_W - LOGIN_BTN_W) // 2,
					"y": 240,
					"default_image": "Assets/kowal/intrologin/loginbtn0.png",
					"over_image": "Assets/kowal/intrologin/loginbtn1.png",
					"down_image": "Assets/kowal/intrologin/loginbtn2.png",
					"text": uiScriptLocale.LOGIN_BUTTON_TEXT,
				},
			),
		},

		# =============================================================
		# CHANNEL ROW (below the board) -- CH1..CH6 buttons in Python
		# =============================================================
		{
			"name": "channel_board",
			"type": "window",
			"x": 0,
			"y": 230,
			"horizontal_align": "center",
			"vertical_align": "center",
			"width": 600,
			"height": 49,

			"children": (
				{
					"name": "channel_list",
					"type": "window",
					"x": 0,
					"y": 0,
					"width": 600,
					"height": 49,
					"children": (),
				},
			),
		},

		# ---- bottom panel placeholder (language selector created in Python) ----
		{
			"name": "bottom_panel",
			"type": "window",
			"x": 0, "y": 0,
			"width": 1, "height": 1,
		},
	),
}
