# -*- coding: utf-8 -*-

import logging
import app
import net
import ui
import grp
import snd
import wndMgr
import musicInfo
import systemSetting
import localeInfo
import uiScriptLocale
import constInfo
import ime
import server_config

from account_manager import AccountManager
from utility import MakeEvent, Event, NOOP

if app.ENABLE_PERFORMANCE_IMPROVEMENTS_NEW:
	import uiGuild


class LanguageDropdown(ui.Window):
	"""Language dropdown selector."""

	class DropdownListBox(ui.ListBox):
		def __init__(self):
			ui.ListBox.__init__(self)
			self.itemHeight = 15
			self.itemStep = 17
			self.parentDropdown = None

		def SetParentDropdown(self, parent):
			self.parentDropdown = parent

		def OnMouseLeftButtonDown(self):
			if not self.IsInPosition():
				if self.parentDropdown:
					self.parentDropdown.CloseList()
				return True
			return ui.ListBox.OnMouseLeftButtonDown(self)

		def OnRender(self):
			x, y = self.GetGlobalPosition()
			w, h = self.GetWidth(), self.GetHeight()

			grp.SetColor(ui.BACKGROUND_COLOR)
			grp.RenderBar(x, y, w, h)

			grp.SetColor(ui.DARK_COLOR)
			grp.RenderLine(x, y, w, 0)
			grp.RenderLine(x, y, 0, h)

			grp.SetColor(ui.BRIGHT_COLOR)
			grp.RenderLine(x, y + h, w, 0)
			grp.RenderLine(x + w, y, 0, h)

			ui.ListBox.OnRender(self)

	LANGUAGE_LIST = [
		("pl", "Polski"),
		("cz", "Cesky"),
		("de", "Deutsch"),
		("en", "English"),
	]

	def __init__(self):
		ui.Window.__init__(self)
		self.isOpen = False
		self.selectedIndex = 0
		self.languages = self.LANGUAGE_LIST
		self.callback = None
		self.focusTarget = None

		self.button = ui.Button()
		self.button.SetParent(self)
		self.button.SetUpVisual("d:/ymir work/ui/public/small_button_01.sub")
		self.button.SetOverVisual("d:/ymir work/ui/public/small_button_02.sub")
		self.button.SetDownVisual("d:/ymir work/ui/public/small_button_03.sub")
		self.button.SetEvent(self.ToggleList)
		self.button.Show()

		self.buttonText = ui.TextLine()
		self.buttonText.SetParent(self.button)
		self.buttonText.SetPosition(5, 0)
		self.buttonText.SetVerticalAlignCenter()
		self.buttonText.Show()

		self.listBox = self.DropdownListBox()
		self.listBox.SetParent(self)
		self.listBox.SetParentDropdown(self)
		self.listBox.SetEvent(self.OnSelectItem)
		self.listBox.SetPosition(0, 22)

		for index, (code, name) in enumerate(self.languages):
			self.listBox.InsertItem(index, f" {name}")

		self.listBox.Hide()
		self.UpdateButtonText()

	def SetPosition(self, x, y):
		ui.Window.SetPosition(self, x, y)

	def SetSize(self, width, height):
		self.button.SetSize(width, height)
		max_items = min(10, len(self.languages))
		list_height = max_items * self.listBox.itemStep
		self.listBox.SetSize(width, list_height)
		ui.Window.SetSize(self, width, height + list_height + 5)

	def UpdateButtonText(self):
		if self.selectedIndex < len(self.languages):
			_, name = self.languages[self.selectedIndex]
			self.buttonText.SetText(name)

	def ToggleList(self):
		if self.isOpen:
			self.CloseList()
		else:
			self.OpenList()

	def OpenList(self):
		self.isOpen = True
		self.listBox.Show()
		self.listBox.SetTop()
		self.listBox.CaptureMouse()

	def CloseList(self):
		self.isOpen = False
		self.listBox.ReleaseMouse()
		self.listBox.Hide()
		if self.focusTarget:
			self.focusTarget.SetFocus()

	def SetFocusTarget(self, target):
		self.focusTarget = target

	def OnSelectItem(self, index):
		self.selectedIndex = index
		self.UpdateButtonText()
		self.CloseList()
		if self.callback:
			self.callback(index)

	def SetEvent(self, callback):
		self.callback = callback

	def Destroy(self):
		self.button = None
		self.buttonText = None
		self.listBox = None
		self.callback = None


class ConnectingDialog(ui.ScriptWindow):
	"""Dialog shown while connecting to server."""

	def __init__(self):
		super().__init__()
		self.board = None
		self.message = None
		self.cancelButton = None
		self.cancelEvent = None
		self._build_dialog()

	def _build_dialog(self):
		try:
			self.SetSize(280, 95)

			self.board = ui.Board()
			self.board.SetParent(self)
			self.board.SetSize(280, 95)
			self.board.SetPosition(0, 0)
			self.board.Show()

			self.message = ui.TextLine()
			self.message.SetParent(self.board)
			self.message.SetPosition(140, 30)
			self.message.SetHorizontalAlignCenter()
			self.message.Show()

			self.cancelButton = ui.Button()
			self.cancelButton.SetParent(self.board)
			self.cancelButton.SetPosition(100, 58)
			self.cancelButton.SetUpVisual("d:/ymir work/ui/public/canclebutton00.sub")
			self.cancelButton.SetOverVisual("d:/ymir work/ui/public/canclebutton01.sub")
			self.cancelButton.SetDownVisual("d:/ymir work/ui/public/canclebutton02.sub")
			self.cancelButton.SetEvent(MakeEvent(self._on_cancel))
			self.cancelButton.Show()
		except Exception as e:
			logging.exception("ConnectingDialog build error: %s", e)

	def SetCancelEvent(self, event):
		self.cancelEvent = event

	def _on_cancel(self):
		self.Close()
		if self.cancelEvent:
			self.cancelEvent()

	def Open(self, message: str = None):
		if message is None:
			message = localeInfo.LOGIN_CONNETING

		self.message.SetText(message)

		self.SetCenterPosition()
		self.SetTop()
		self.Show()

	def Close(self):
		self.Hide()


class LoginWindow(ui.ScriptWindow):

	def __init__(self, stream):
		super().__init__()
		self.stream = stream

		self.current_environment = "live"

		self.account_manager = AccountManager()

		# UI Elements
		self.background = None
		self.env_selector = None
		self.live_button = None
		self.dev_button = None

		self.login_board = None
		self.channel_board = None
		self.accounts_board = None
		self.bottom_panel = None
		self.select_language_text = None
		self.bg_dark = None

		self.login_input = None
		self.password_input = None
		self.pin_input = None
		self.login_placeholder = None
		self.password_placeholder = None
		self.pin_placeholder = None
		self.channel_list = None
		self.accounts_list = None
		self.save_account_button = None

		self.language_selector = None
		self.connecting_dialog = None
		self.channels = []
		self.accounts = []
		self.selected_channel_index = -1

		# Login failure dicts
		self.login_failure_msg_dict = {}
		self.login_failure_func_dict = {}

		if app.ENABLE_PERFORMANCE_IMPROVEMENTS_NEW:
			self.loading_prob = False

		net.SetPhaseWindow(net.PHASE_WINDOW_LOGIN, self)
		net.SetAccountConnectorHandler(self)

	def __del__(self):
		super().__del__()
		net.ClearPhaseWindow(net.PHASE_WINDOW_LOGIN, self)
		net.SetAccountConnectorHandler(0)

	if app.ENABLE_PERFORMANCE_IMPROVEMENTS_NEW:
		def BINARY_SetGuildBuildingList(self, obj):
			uiGuild.BUILDING_DATA_LIST = obj

		def GameLoaded(self):
			constInfo.isGameLoaded = True
			if self.loading_prob:
				self.loading_prob = False
				self.stream.popupWindow.Close()
				self._on_login_click()

	def Open(self):
		"""Open and initialize the login window."""
		self._setup_login_failure_messages()
		self.SetSize(wndMgr.GetScreenWidth(), wndMgr.GetScreenHeight())
		self.SetWindowName("LoginWindow")

		if not self._load_ui():
			logging.error("Failed to load login UI")
			return

		if musicInfo.loginMusic:
			snd.SetMusicVolume(systemSetting.GetMusicVolume())
			snd.FadeInMusic(f"BGM/{musicInfo.loginMusic}")

		snd.SetSoundVolumef(systemSetting.GetSoundVolumef())

		ime.AddExceptKey(91)
		ime.AddExceptKey(93)

		self._show_login_screen()
		self.Show()
		app.ShowCursor()

		if app.__AUTO_HUNT__:
			# Auto Hunt auto-login: wystartuj odliczanie do auto-reconnectu gdy bot byl aktywny
			if constInfo.autoHuntAutoLoginDict["leftTime"] == 0:
				constInfo.autoHuntAutoLoginDict["leftTime"] = app.GetGlobalTimeStamp() + 2 if constInfo.autoHuntAutoLoginDict["status"] == 1 else 0

		if app.ENABLE_PERFORMANCE_IMPROVEMENTS_NEW:
			# Wyjatek tutaj przerwalby Open() po Show() — okno widoczne, a GameLoaded nigdy
			# nie przychodzi (wieczne LOADING_IN_PROGRESS). Ponowienie jest w _on_login_click.
			try:
				net.LoadResourcesInCache()
			except Exception:
				logging.exception("LoadResourcesInCache failed in LoginWindow.Open")

	def _setup_login_failure_messages(self):
		"""Setup login failure message dictionaries."""
		self.login_failure_msg_dict = {
			"ALREADY": localeInfo.LOGIN_FAILURE_ALREAY,
			"NOID": localeInfo.LOGIN_FAILURE_NOT_EXIST_ID,
			"WRONGPWD": localeInfo.LOGIN_FAILURE_WRONG_PASSWORD,
			"FULL": localeInfo.LOGIN_FAILURE_TOO_MANY_USER,
			"SHUTDOWN": localeInfo.LOGIN_FAILURE_SHUTDOWN,
			"REPAIR": localeInfo.LOGIN_FAILURE_REPAIR_ID,
			"BLOCK": localeInfo.LOGIN_FAILURE_BLOCK_ID,
			"WRONGMAT": localeInfo.LOGIN_FAILURE_WRONG_MATRIX_CARD_NUMBER,
			"QUIT": localeInfo.LOGIN_FAILURE_WRONG_MATRIX_CARD_NUMBER_TRIPLE,
			"BESAMEKEY": localeInfo.LOGIN_FAILURE_BE_SAME_KEY,
			"NOTAVAIL": localeInfo.LOGIN_FAILURE_NOT_AVAIL,
			"NOBILL": localeInfo.LOGIN_FAILURE_NOBILL,
			"BLKLOGIN": localeInfo.LOGIN_FAILURE_BLOCK_LOGIN,
			"WEBBLK": localeInfo.LOGIN_FAILURE_WEB_BLOCK,
			"NOPIN": localeInfo.LOGIN_FAILURE_PIN,
			"NOPREM": localeInfo.LOGIN_FAILURE_NOPREMIUM,
		}

		if app.ENABLE_PERFORMANCE_IMPROVEMENTS_NEW:
			self.login_failure_msg_dict["LOADING_IN_PROGRESS"] = localeInfo.LOGIN_FAILURE_LOADING_IN_PROGRESS

		# UWAGA: to slownik FUNKCJI close-eventu (nie komunikatow). WRONGPWD/WRONGMAT
		# mialy tu bledne stringi locale (duplikat z login_failure_msg_dict) -> CloseEvent
		# stawal sie stringiem i Close() crashowal ('str' object is not callable). Brak wpisu
		# => domyslnie EmptyFunc (patrz .get(error, self.EmptyFunc)).
		self.login_failure_func_dict = {
			"QUIT": app.Exit,
		}

		if app.ENABLE_HWID_SYSTEM:
			self.login_failure_msg_dict["HWID"] = localeInfo.LOGIN_FAILURE_HWID
			self.login_failure_func_dict["HWID"] = app.Exit

		if app.CHECK_CLIENT_VERSION:
			self.login_failure_msg_dict["VERSION"] = localeInfo.LOGIN_WRONG_VERSION
			self.login_failure_func_dict["VERSION"] = app.Exit

	def Close(self):
		"""Close the login window and cleanup."""
		if self.login_input:
			self.login_input.SetTabEvent(None)
			self.login_input.SetReturnEvent(None)
		if self.password_input:
			self.password_input.SetTabEvent(None)
			self.password_input.SetReturnEvent(None)
		if self.pin_input:
			self.pin_input.SetTabEvent(None)
			self.pin_input.SetReturnEvent(None)

		if self.connecting_dialog:
			self.connecting_dialog.Close()
			self.connecting_dialog = None

		for channel in self.channels:
			if channel and 'container' in channel:
				channel['container'].Destroy()
		self.channels.clear()

		for account in self.accounts:
			if account and 'container' in account:
				account['container'].Destroy()
		self.accounts.clear()

		self.selected_channel_index = -1

		if musicInfo.loginMusic and musicInfo.selectMusic:
			snd.FadeOutMusic(f"BGM/{musicInfo.loginMusic}")

		if self.stream.popupWindow:
			self.stream.popupWindow.Close()

		self.Hide()
		app.HideCursor()
		ime.ClearExceptKey()

		net.ClearPhaseWindow(net.PHASE_WINDOW_LOGIN, self)
		net.SetAccountConnectorHandler(None)

	def _load_ui(self):
		"""Load UI elements from script."""
		try:
			loader = ui.PythonScriptLoader()
			loader.LoadScriptFile(self, "uiScript/LoginWindow.py")

			self.background = self.GetChild("background")

			# env selector (live/dev) removed in new layout
			self.env_selector = None
			self.live_button = None
			self.dev_button = None

			self.login_board = self.GetChild("login_board")
			self.login_input = self.GetChild("login_input")
			self.password_input = self.GetChild("password_input")
			self.pin_input = self.GetChild("pin_input")
			login_button = self.GetChild("login_button")
			exit_button = self.GetChild("exit_button")

			self.channel_board = self.GetChild("channel_board")
			self.channel_list = self.GetChild("channel_list")

			self.accounts_board = self.GetChild("accounts_board")
			self.accounts_list = self.GetChild("accounts_list")
			# save button removed in new layout (saving handled on login)
			self.save_account_button = None

			self.bottom_panel = self.GetChild("bottom_panel")
			self.bg_dark = self.GetChild("dark_background")

			# Setup events
			login_button.SetEvent(MakeEvent(self._on_login_click))
			try:
				login_button.SetTextAddPos(uiScriptLocale.LOGIN_BUTTON_TEXT, 0, -8)
			except Exception:
				pass
			title = self.GetChild("userpanel_title")
			if title:
				try:
					title.SetFontName(localeInfo.UI_DEF_FONT_LARGE)
					title.SetFontColor(0.88, 0.76, 0.55)
					title.SetOutline()
				except Exception:
					pass
			try:
				login_button.SetTextColor(0xffe0c18c)
			except Exception:
				pass
			exit_button.SetEvent(MakeEvent(self.OnPressExitKey))

			self.login_input.SetReturnEvent(MakeEvent(self.password_input.SetFocus))
			self.login_input.SetTabEvent(MakeEvent(self.password_input.SetFocus))
			self.password_input.SetReturnEvent(MakeEvent(self.pin_input.SetFocus))
			self.password_input.SetTabEvent(MakeEvent(self.pin_input.SetFocus))
			self.pin_input.SetReturnEvent(MakeEvent(self._on_login_click))
			self.pin_input.SetTabEvent(MakeEvent(self.login_input.SetFocus))

			# Create placeholder labels
			self.login_placeholder = self._create_placeholder(
				self.login_input, localeInfo.LOGIN_PLACEHOLDER_ID
			)
			self.password_placeholder = self._create_placeholder(
				self.password_input, localeInfo.LOGIN_PLACEHOLDER_PASSWORD
			)
			self.pin_placeholder = self._create_placeholder(
				self.pin_input, localeInfo.LOGIN_PLACEHOLDER_PIN
			)

			self.current_environment = "live"

			self._load_saved_accounts()
			self._setup_language_selector()

			return True

		except Exception as e:
			logging.exception("LoginWindow._load_ui error: %s", e)
			return False

	LANGUAGE_CODEPAGES = {"pl": 1250, "en": 1252, "cz": 1250, "de": 1252}
	LANGUAGE_LIST = ("pl", "en", "cz", "de")

	def _setup_language_selector(self):
		"""Create language flag buttons programmatically."""
		self.languageButtonDict = {}
		current_lang = app.GetLocaleName()

		sw = wndMgr.GetScreenWidth()
		sh = wndMgr.GetScreenHeight()

		self.lang_bg = ui.ImageBox()
		self.lang_bg.SetParent(self)
		self.lang_bg.LoadImage("kowal/game/login/lang_bg.png")
		bg_w = self.lang_bg.GetWidth()
		bg_h = self.lang_bg.GetHeight()
		base_x = int((sw - bg_w) / 2)
		base_y = int(sh - bg_h - 20)
		self.lang_bg.SetPosition(base_x, base_y)
		self.lang_bg.Hide()

		label = uiScriptLocale.LOGIN_SELECT_LANGUAGE if hasattr(uiScriptLocale, 'LOGIN_SELECT_LANGUAGE') else "Select Language"

		self.lang_text = ui.TextLine()
		self.lang_text.SetParent(self)
		self.lang_text.SetFontName(localeInfo.UI_DEF_FONT_LARGE)
		self.lang_text.SetFontColor(0.65, 0.576, 0.439)
		self.lang_text.SetPosition(base_x + 15, base_y + int((bg_h - 16) / 2))
		self.lang_text.SetText(label + "  |")
		self.lang_text.Hide()

		flags_w = len(self.LANGUAGE_LIST) * 28
		flag_h = 20
		flag_y = base_y + int((bg_h - flag_h) / 2)
		flags_x = base_x + int((bg_w - flags_w) / 2)

		for i, lang in enumerate(self.LANGUAGE_LIST):
			btn = ui.Button()
			btn.SetParent(self)
			btn.SetPosition(int(flags_x + i * 28), flag_y)
			btn.SetUpVisual("kowal/game/login/lang/%s_button_01.png" % lang)
			btn.SetOverVisual("kowal/game/login/lang/%s_button_02.png" % lang)
			btn.SetDownVisual("kowal/game/login/lang/%s_button_03.png" % lang)
			btn.SetEvent(lambda l=lang: self.__OnClickLanguageFlag(l))
			btn.Show()
			self.languageButtonDict[lang] = btn

			if lang == current_lang:
				btn.Down()
				btn.Disable()

	def __OnClickLanguageFlag(self, lang):
		if app.GetLocaleName() == lang:
			return
		import uiCommon
		self.questionDialog = uiCommon.QuestionDialog()
		self.questionDialog.SetText(uiScriptLocale.CHANGE_LANGUAGE_QUESTION if hasattr(uiScriptLocale, 'CHANGE_LANGUAGE_QUESTION') else "Change language?")
		self.questionDialog.SetAcceptEvent(lambda l=lang: self.__ApplyLanguageChange(l))
		self.questionDialog.SetCancelEvent(self.__CancelLanguageChange)
		self.questionDialog.Open()

	def __ApplyLanguageChange(self, lang):
		self.questionDialog.Close()
		self.questionDialog = None
		codepage = self.LANGUAGE_CODEPAGES.get(lang, 1252)
		with open("_cfg/locale.cfg", "w") as f:
			f.write("10022 %d %s" % (codepage, lang))
		app.ForceSetLocale(lang, "locale/%s" % lang)
		import os
		os.startfile("KowalMT2.exe")
		app.Exit()

	def __CancelLanguageChange(self):
		self.questionDialog.Close()
		self.questionDialog = None

	def _create_placeholder(self, editline, text):
		"""Create a placeholder TextLine inside an editline."""
		placeholder = ui.TextLine()
		placeholder.SetParent(editline)
		placeholder.SetPosition(0, 0)
		placeholder.SetFontColor(0.5, 0.5, 0.5)
		placeholder.SetOutline()
		placeholder.SetText(text)
		placeholder.Show()
		return placeholder

	def _update_placeholders(self):
		"""Show/hide placeholders based on editline content."""
		if self.login_placeholder:
			if self.login_input.GetText():
				self.login_placeholder.Hide()
			else:
				self.login_placeholder.Show()
		if self.password_placeholder:
			if self.password_input.GetText():
				self.password_placeholder.Hide()
			else:
				self.password_placeholder.Show()
		if self.pin_placeholder:
			if self.pin_input.GetText():
				self.pin_placeholder.Hide()
			else:
				self.pin_placeholder.Show()

	def _show_login_screen(self):
		"""Display the login screen with all panels."""
		self.login_board.Show()
		self.channel_board.Show()
		self.accounts_board.Show()
		self.bottom_panel.Show()
		self.bg_dark.Hide()
		self._load_channels()
		self.login_input.SetFocus()

	CHANNEL_ITEM_W = 185
	ACCOUNT_ITEM_W = 185
	ITEM_H = 25
	ITEM_SPACING = 37
	ITEM_START_Y = 0

	def _load_channels(self):
		"""Load available channels for selected environment."""
		try:
			for channel in self.channels:
				if channel and 'container' in channel:
					channel['container'].Destroy()
			self.channels.clear()

			channels = server_config.get_channels(self.current_environment)

			CH_W = 90
			CH_GAP = 10
			total = len(channels)
			row_w = total * CH_W + (total - 1) * CH_GAP if total > 0 else 0
			start_x = max(0, (600 - row_w) // 2)

			for index, channel in enumerate(channels):
				channel_name = channel.get("name", f"CH{index + 1}")

				radio = ui.RadioButton()
				radio.SetParent(self.channel_list)
				radio.SetPosition(start_x + index * (CH_W + CH_GAP), 0)
				if index == 4:
					radio.SetUpVisual("Assets/kowal/intrologin/chbtn0_gold.png")
					radio.SetOverVisual("Assets/kowal/intrologin/chbtn1_gold.png")
					radio.SetDownVisual("Assets/kowal/intrologin/chbtn2_gold.png")
				else:
					radio.SetUpVisual("Assets/kowal/intrologin/chbtn0.png")
					radio.SetOverVisual("Assets/kowal/intrologin/chbtn1.png")
					radio.SetDownVisual("Assets/kowal/intrologin/chbtn2.png")
				radio.SetText(channel_name)
				try:
					radio.SetTextColor(0xffe0c18c)
				except Exception:
					pass
				radio.SetEvent(Event(self._on_channel_select, index))
				radio.Show()

				channel_data = {
					'container': radio,
					'radio': radio,
					'index': index,
					'name': channel_name,
				}
				self.channels.append(channel_data)

			if len(self.channels) > 0:
				self._on_channel_select(0)

		except Exception as e:
			logging.exception("Failed to load channels: %s", e)

	def _on_channel_select(self, channel_index):
		"""Handle channel selection."""
		try:
			for i, channel_data in enumerate(self.channels):
				channel_data['radio'].SetUp()
			self.channels[channel_index]['radio'].Down()
			self.selected_channel_index = channel_index
			self._restore_focus()
		except Exception as e:
			logging.exception("Failed to select channel: %s", e)

	def _on_live_click(self):
		self.current_environment = "live"
		self.live_button.Down()
		self.dev_button.SetUp()
		self._load_channels()
		self._restore_focus()

	def _on_dev_click(self):
		self.current_environment = "dev"
		self.dev_button.Down()
		self.live_button.SetUp()
		self._load_channels()
		self._restore_focus()

	def _save_account(self):
		"""Save current account to saved accounts list."""
		username = self.login_input.GetText().strip()
		password = self.password_input.GetText().strip()
		pin = self.pin_input.GetText().strip()

		if not username:
			self._show_message(localeInfo.LOGIN_INPUT_ID)
			return

		try:
			success = self.account_manager.save_account(username, password, pin, self.current_environment)

			if success:
				self._show_message(localeInfo.INTROLOGIN_SAVED)
				self._load_saved_accounts()
			else:
				accounts = self.account_manager.get_saved_accounts()
				for acc_username, acc_env, acc_password, acc_pin in accounts:
					if acc_username == username and acc_env == self.current_environment:
						self._show_message(localeInfo.INTROLOGIN_ACCOUNT_REQUIRED)
						return
				self._show_message(localeInfo.LOGIN_MAX_ACCOUNTS)
		except Exception as e:
			logging.exception("Failed to save account: %s", e)

	def _load_saved_accounts(self):
		"""Load saved accounts into the list."""
		for account in self.accounts:
			if account and 'container' in account:
				account['container'].Destroy()
		self.accounts.clear()

		try:
			accounts = list(self.account_manager.get_saved_accounts())

			ROW_W = 236
			ROW_SPACING = 35
			LEFT_X = 16
			RIGHT_X = 766 - ROW_W - 16
			TOP_Y = 80
			PER_COL = 6
			TOTAL_SLOTS = PER_COL * 2

			for slot in range(TOTAL_SLOTS):
				col_x = LEFT_X if slot < PER_COL else RIGHT_X
				row = slot % PER_COL
				filled = slot < len(accounts)

				account_container = ui.Window()
				account_container.SetParent(self.accounts_list)
				account_container.SetPosition(col_x, TOP_Y + row * ROW_SPACING)
				account_container.SetSize(ROW_W + 14, 44)
				account_container.Show()

				account_bg = ui.ImageBox()
				account_bg.SetParent(account_container)
				account_bg.LoadImage("Assets/kowal/intrologin/savedrow.png")
				account_bg.SetPosition(0, 0)
				account_bg.Show()

				slot_data = {'container': account_container, 'background': account_bg, 'index': slot}

				if filled:
					username, environment, password, pin = accounts[slot]

					account_text = ui.TextLine()
					account_text.SetParent(account_container)
					account_text.SetPosition(22, 18)
					account_text.SetVerticalAlignCenter()
					account_text.SetFontColor(0.85, 0.73, 0.52)
					account_text.SetOutline()
					account_text.SetText(username)
					account_text.Show()

					left_btn = ui.Button()
					left_btn.SetParent(account_container)
					left_btn.SetPosition(ROW_W - 72, 3)
					left_btn.SetUpVisual("Assets/kowal/intrologin/play0.png")
					left_btn.SetOverVisual("Assets/kowal/intrologin/play1.png")
					left_btn.SetDownVisual("Assets/kowal/intrologin/play2.png")
					left_btn.SetEvent(Event(self._on_account_select, slot))
					left_btn.Show()

					slot_data.update({'text': account_text, 'enter': left_btn,
						'environment': environment, 'username': username,
						'password': password, 'pin': pin})
				else:
					left_btn = ui.Button()
					left_btn.SetParent(account_container)
					left_btn.SetPosition(ROW_W - 72, 3)
					left_btn.SetUpVisual("Assets/kowal/intrologin/save0.png")
					left_btn.SetOverVisual("Assets/kowal/intrologin/save1.png")
					left_btn.SetDownVisual("Assets/kowal/intrologin/save2.png")
					left_btn.SetEvent(MakeEvent(self._save_account))
					left_btn.Show()
					slot_data['enter'] = left_btn

				del_btn = ui.Button()
				del_btn.SetParent(account_container)
				del_btn.SetPosition(ROW_W - 44, 3)
				del_btn.SetUpVisual("Assets/kowal/intrologin/del0.png")
				del_btn.SetOverVisual("Assets/kowal/intrologin/del1.png")
				del_btn.SetDownVisual("Assets/kowal/intrologin/del2.png")
				if filled:
					del_btn.SetEvent(Event(self._on_delete_account, slot))
				del_btn.Show()
				slot_data['delete'] = del_btn

				self.accounts.append(slot_data)

		except Exception as e:
			logging.exception("Failed to load saved accounts: %s", e)

	def _on_account_select(self, index):
		"""Handle account selection from saved accounts list."""
		try:
			if index < 0 or index >= len(self.accounts):
				return

			account = self.accounts[index]
			username = account['username']
			password = account['password']
			pin = account['pin']
			environment = account['environment']

			self.current_environment = environment if environment else "live"

			self.login_input.SetText(username)
			self.password_input.SetText(password)
			self.pin_input.SetText(pin)
			self.pin_input.SetFocus()

		except Exception as e:
			logging.exception("Failed to select account: %s", e)

	def _on_delete_account(self, index):
		"""Delete selected saved account."""
		try:
			success = self.account_manager.delete_account(index)
			if success:
				self._show_message(localeInfo.INTROLOGIN_ACCOUNT_DELETED)
				self._load_saved_accounts()
			else:
				self._show_message(localeInfo.INTROLOGIN_NO_ACCOUNT)
		except Exception as e:
			logging.exception("Failed to delete account: %s", e)

	def _on_login_click(self):
		"""Handle login button click."""
		if app.ENABLE_PERFORMANCE_IMPROVEMENTS_NEW:
			if not constInfo.isGameLoaded:
				self.PopupNotifyMessage(
					self.login_failure_msg_dict["LOADING_IN_PROGRESS"],
					self.EmptyFunc
				)
				self.loading_prob = True
				# Flaga nie przyszla (Open() przerwany wyjatkiem itp.) — ponow ladowanie.
				# Load() jest idempotentny i zawsze wola GameLoaded(), ktory dokonczy logowanie.
				try:
					net.LoadResourcesInCache()
				except Exception:
					logging.exception("LoadResourcesInCache retry failed")
				return

		self._on_connect_click()

	def _on_connect_click(self):
		"""Initiate connection to game server."""
		username = self.login_input.GetText()
		password = self.password_input.GetText()
		pin = self.pin_input.GetText()

		if not username:
			self._show_message(localeInfo.LOGIN_INPUT_ID)
			return

		if not password:
			self._show_message(localeInfo.LOGIN_INPUT_PASSWORD)
			return

		if not pin:
			self._show_message(localeInfo.LOGIN_INPUT_PIN)
			return

		if self.selected_channel_index < 0:
			self._show_message(localeInfo.LOGIN_SELECT_CHANNEL)
			return

		try:
			channel = server_config.get_channel_by_index(self.current_environment, self.selected_channel_index)

			if not channel:
				self._show_message(localeInfo.LOGIN_SELECT_CHANNEL)
				return

			server = server_config.get_server(self.current_environment)

			ip = channel["ip"]
			tcp_port = channel["port"]
			auth_port = channel["auth_port"]

			try:
				net.SetMarkServer(server["ip"], server["mark_port"])
				app.SetGuildMarkPath(f"{server['mark_path']}.tga")
				app.SetGuildSymbolPath(server["mark_path"])
			except Exception as e:
				logging.warning("Failed to set mark server: %s", e)

			server_name = server["name"]
			channel_name = channel["name"]
			net.SetServerInfo(f"{server_name}, {channel_name}")

			self.stream.SetConnectInfo(ip, tcp_port, ip, auth_port)

			if constInfo.SEQUENCE_PACKET_ENABLE:
				net.SetPacketSequenceMode()

			net.SetVersionId(constInfo.CLIENT_VERSION)
			self.stream.SetLoginInfo(username, password, pin)

			self.connecting_dialog = ConnectingDialog()
			self.connecting_dialog.SetCancelEvent(MakeEvent(self._on_connect_cancel))
			self.connecting_dialog.Open(localeInfo.LOGIN_CONNETING)

			self.stream.Connect()

		except Exception as e:
			logging.exception("Connection error: %s", e)
			self._show_message(localeInfo.LOGIN_CONNECT_FAILURE)

	def _on_connect_cancel(self):
		"""Called when user cancels the connecting dialog."""
		net.Disconnect()
		self.connecting_dialog = None
		self._restore_focus()

	def _show_message(self, message):
		"""Display a popup message to the user."""
		self.stream.popupWindow.Close()
		self.stream.popupWindow.Open(message, MakeEvent(self._restore_focus), localeInfo.UI_OK)

	def PopupDisplayMessage(self, msg):
		"""Display a popup message."""
		self.stream.popupWindow.Close()
		self.stream.popupWindow.Open(msg)

	def PopupNotifyMessage(self, msg, func=None):
		"""Display a notification popup with callback."""
		if func is None:
			func = self.EmptyFunc
		self.stream.popupWindow.Close()
		self.stream.popupWindow.Open(msg, func, localeInfo.UI_OK)

	def EmptyFunc(self):
		pass

	def _restore_focus(self):
		"""Restore focus to appropriate input field."""
		if not self.login_input.GetText():
			self.login_input.SetFocus()
		elif not self.password_input.GetText():
			self.password_input.SetFocus()
		elif not self.pin_input.GetText():
			self.pin_input.SetFocus()
		else:
			self.login_input.SetFocus()

	# ============================================================
	# Network Callbacks
	# ============================================================

	def OnConnectFailure(self):
		"""Called when connection to server fails."""
		if self.connecting_dialog:
			self.connecting_dialog.Close()
			self.connecting_dialog = None

		snd.PlaySound("sound/ui/loginfail.wav")
		self._show_message(localeInfo.LOGIN_CONNECT_FAILURE)

		if app.__AUTO_HUNT__:
			if constInfo.autoHuntAutoLoginDict["status"] == 1 and constInfo.autoHuntAutoLoginDict["leftTime"] != 0:
				constInfo.autoHuntAutoLoginDict["leftTime"] = app.GetGlobalTimeStamp() + 2

	def OnHandShake(self):
		"""Called when handshake with server succeeds."""
		snd.PlaySound("sound/ui/loginok.wav")
		if self.connecting_dialog:
			self.connecting_dialog.message.SetText(localeInfo.LOGIN_CONNECT_SUCCESS)

	def OnLoginStart(self):
		"""Called when login process starts."""
		if self.connecting_dialog:
			self.connecting_dialog.message.SetText(localeInfo.LOGIN_PROCESSING)

	def OnLoginFailure(self, error):
		"""Called when login fails with error code."""
		if self.connecting_dialog:
			self.connecting_dialog.Close()
			self.connecting_dialog = None

		try:
			login_failure_msg = self.login_failure_msg_dict[error]
		except KeyError:
			if error == "INACTIVE":
				login_failure_msg = localeInfo.INTROLOGIN_CONFIRM_MAIL
			else:
				login_failure_msg = localeInfo.LOGIN_FAILURE_UNKNOWN + error

		login_failure_func = self.login_failure_func_dict.get(error, self.EmptyFunc)
		self.PopupNotifyMessage(login_failure_msg, login_failure_func)
		snd.PlaySound("sound/ui/loginfail.wav")

		if app.__AUTO_HUNT__:
			if error == "ALREADY" and constInfo.autoHuntAutoLoginDict["status"] == 1 and constInfo.autoHuntAutoLoginDict["leftTime"] != 0:
				constInfo.autoHuntAutoLoginDict["leftTime"] = app.GetGlobalTimeStamp() + 2

	def OnPressExitKey(self):
		"""Handle exit key press."""
		if self.stream.popupWindow:
			self.stream.popupWindow.Close()
		self.stream.SetPhaseWindow(0)
		return True

	def OnMouseLeftButtonDown(self):
		"""Handle mouse click - close language dropdown if open."""
		if self.language_selector and self.language_selector.isOpen:
			self.language_selector.CloseList()
		return False

	def OnUpdate(self):
		"""Called every frame."""
		self._update_placeholders()

		if app.__AUTO_HUNT__:
			# Auto Hunt auto-login: po uplywie odliczania odtworz polaczenie z zapamietanymi danymi
			d = constInfo.autoHuntAutoLoginDict
			if d["status"] == 1 and d["leftTime"] > 0 and d["leftTime"] < app.GetGlobalTimeStamp():
				self.stream.SetConnectInfo(d["addr"], d["port"], d["account_addr"], d["account_port"])
				if constInfo.SEQUENCE_PACKET_ENABLE:
					net.SetPacketSequenceMode()
				net.SetVersionId(constInfo.CLIENT_VERSION)
				self.stream.SetLoginInfo(d["id"], d["pwd"], d["pin"])
				self.stream.Connect()
				constInfo.autoHuntAutoLoginDict["leftTime"] = -1

		if self.bg_dark:
			if self.stream.popupWindow and self.stream.popupWindow.IsShow():
				if not self.bg_dark.IsShow():
					self.bg_dark.Show()
			else:
				self.bg_dark.Hide()
