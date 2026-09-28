import ui
import dbg
import snd
import systemSetting
import net
import chat
import app
import localeInfo
import constInfo
import settings
import uiScriptLocale
import player
import uiPrivateShopBuilder
import background
import musicInfo
import uiSelectMusic

blockMode = 0
viewChatMode = 0

MUSIC_FILENAME_MAX_LEN = 25
VOICE_DEVICE_NAME_MAX_LEN = 18

MOBILE = False

if app.ENABLE_VOICE_CHAT:
	# DIK code -> display name. Only codes exported by app (PythonApplicationModule).
	# Unknown codes fall back to "Key %d" via VoiceGetDIKName().
	VOICE_DIK_NAME_MAP = {}

	def __VoiceBuildDIKNameMap():
		m = VOICE_DIK_NAME_MAP
		# letters
		for c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
			attr = "DIK_" + c
			if hasattr(app, attr):
				m[getattr(app, attr)] = c
		# digits
		for c in "0123456789":
			attr = "DIK_" + c
			if hasattr(app, attr):
				m[getattr(app, attr)] = c
		# function keys
		for i in range(1, 13):
			attr = "DIK_F" + str(i)
			if hasattr(app, attr):
				m[getattr(app, attr)] = "F" + str(i)
		# numpad
		for i in range(0, 10):
			attr = "DIK_NUMPAD" + str(i)
			if hasattr(app, attr):
				m[getattr(app, attr)] = "Num " + str(i)
		# common named keys: (app attr, label)
		named = (
			("DIK_SPACE", "Space"), ("DIK_TAB", "Tab"), ("DIK_RETURN", "Enter"),
			("DIK_LSHIFT", "L-Shift"), ("DIK_RSHIFT", "R-Shift"),
			("DIK_LCONTROL", "L-Ctrl"), ("DIK_RCONTROL", "R-Ctrl"),
			("DIK_LALT", "L-Alt"), ("DIK_RALT", "R-Alt"),
			("DIK_GRAVE", "`"), ("DIK_MINUS", "-"), ("DIK_EQUALS", "="),
			("DIK_LBRACKET", "["), ("DIK_RBRACKET", "]"), ("DIK_BACKSLASH", "\\"),
			("DIK_SEMICOLON", ";"), ("DIK_APOSTROPHE", "'"), ("DIK_COMMA", ","),
			("DIK_PERIOD", "."), ("DIK_SLASH", "/"),
			("DIK_INSERT", "Insert"), ("DIK_DELETE", "Delete"),
			("DIK_HOME", "Home"), ("DIK_END", "End"),
			("DIK_PGUP", "PageUp"), ("DIK_PGDN", "PageDown"),
			("DIK_UP", "Up"), ("DIK_DOWN", "Down"),
			("DIK_LEFT", "Left"), ("DIK_RIGHT", "Right"),
			("DIK_BACK", "Backspace"), ("DIK_CAPITAL", "CapsLock"),
			("DIK_ADD", "Num +"), ("DIK_SUBTRACT", "Num -"),
			("DIK_MULTIPLY", "Num *"), ("DIK_DIVIDE", "Num /"),
			("DIK_DECIMAL", "Num ."), ("DIK_NUMPADENTER", "Num Enter"),
		)
		for attr, label in named:
			if hasattr(app, attr):
				m[getattr(app, attr)] = label

	__VoiceBuildDIKNameMap()

	def VoiceGetDIKName(code):
		if code in VOICE_DIK_NAME_MAP:
			return VOICE_DIK_NAME_MAP[code]
		return "Key %d" % int(code)

	class VoiceDeviceDropDown(ui.Window):
		# Lightweight popup: bordered board + one Middle_Button row per device,
		# positioned under the trigger button. Memory-safe callbacks only.
		ROW_HEIGHT = 22
		ROW_WIDTH = 150
		PAD = 8
		MAX_VISIBLE = 8
		ROW_NAME_MAX_LEN = 22

		def __init__(self):
			ui.Window.__init__(self, "TOP_MOST")
			self.__Initialize()
			self.AddFlag("float")
			self.board = ui.ThinBoard()
			self.board.SetParent(self)
			self.board.Show()

		def __del__(self):
			ui.Window.__del__(self)

		def __Initialize(self):
			self.board = None
			self.rowButtons = []
			self.event = None

		def Destroy(self):
			for btn in self.rowButtons:
				if btn:
					btn.SetEvent(0)
			self.rowButtons = []
			self.board = None
			self.event = None
			self.__Initialize()

		def SetEvent(self, event):
			# event(index) -- called on row click
			self.event = event

		def __ClearRows(self):
			for btn in self.rowButtons:
				if btn:
					btn.SetEvent(0)
			self.rowButtons = []

		def SetItems(self, nameList):
			self.__ClearRows()
			count = len(nameList)
			if count <= 0:
				count = 0
			width = self.ROW_WIDTH + self.PAD * 2
			height = count * self.ROW_HEIGHT + self.PAD * 2
			if height < self.PAD * 2 + self.ROW_HEIGHT:
				height = self.PAD * 2 + self.ROW_HEIGHT
			self.SetSize(width, height)
			self.board.SetSize(width, height)
			for i in range(count):
				name = nameList[i]
				if len(name) > self.ROW_NAME_MAX_LEN:
					name = name[:self.ROW_NAME_MAX_LEN]
				btn = ui.Button()
				btn.SetParent(self)
				btn.SetUpVisual("d:/ymir work/ui/public/Middle_Button_01.sub")
				btn.SetOverVisual("d:/ymir work/ui/public/Middle_Button_02.sub")
				btn.SetDownVisual("d:/ymir work/ui/public/Middle_Button_03.sub")
				btn.SetPosition(self.PAD, self.PAD + i * self.ROW_HEIGHT)
				btn.SetText(name)
				btn.SetEvent(ui.__mem_func__(self.__OnSelectRow), i)
				btn.Show()
				self.rowButtons.append(btn)

		def __OnSelectRow(self, index):
			self.Close()
			if self.event:
				self.event(index)

		def OpenAt(self, x, y):
			self.SetPosition(x, y)
			self.SetTop()
			self.Show()

		def Close(self):
			self.Hide()

		def OnPressEscapeKey(self):
			self.Close()
			return True

class OptionDialog(ui.ScriptWindow):

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.__Initialize()
		self.__Load()
		self.RefreshViewChat()
		self.RefreshAlwaysShowName()
		self.RefreshShowDamage()
		self.RefreshShowSalesText()
		self.RefreshDesc0Btn()
		self.RefreshDesc1Btn()
		self.RefreshDesc2Btn()
		self.RefreshDesc3Btn()
		self.RefreshFontText()
		self.RefreshAutobuff()
		self.RefreshPetOptions()
		self.RefreshWierzch()
		if app.WJ_SHOW_MOB_INFO:
			self.RefreshShowMobInfo()
		if app.ENABLE_DOG_MODE:
			self.RefreshDogMode()
		if app.ENABLE_SKYBOX_SELECT:
			self.RefreshSkyBoxButtons()

	def __del__(self):
		ui.ScriptWindow.__del__(self)
		print(" -------------------------------------- DELETE GAME OPTION DIALOG"
)

	def __Initialize(self):
		self.board = 0
		self.titleBar = 0
		self.page = 0
		self.vsyncButtonList = []
		self.resizeWindowButtonList = []
		self.fpsLimitButton = 0
		self.fpsLimitValueText = 0
		self.fpsLimitIndex = 0
		self.nameColorModeButtonList = []
		self.viewTargetBoardButtonList = []
		self.pvpModeButtonDict = {}
		self.blockButtonList = []
		self.viewChatButtonList = []
		self.alwaysShowNameButtonList = []
		self.showDamageButtonList = []
		self.showsalesTextButtonList = []
		self.fonttype = []
		if app.WJ_SHOW_MOB_INFO:
			self.showMobInfoButtonList = []

		if app.ENABLE_DOG_MODE:
			self.dogModeButtonList = []
		if app.ENABLE_SKYBOX_SELECT:
			self.skyBoxObjects = []
			self.skyBoxes = [
				"d:/ymir work/environment/sunset_kf.msenv",
				"d:/ymir work/environment/hazysun_kf.msenv", 
				"d:/ymir work/environment/cloudysun_kf.msenv",
				"d:/ymir work/environment/eveningsun_kf.msenv",
				"d:/ymir work/environment/rainyday_kf.msenv",
				"d:/ymir work/environment/overcastday_kf.msenv",
				"d:/ymir work/environment/foggysunset_kf.msenv",
				"d:/ymir work/environment/cloudymonth_kf.msenv"
			]

		self.category_btn5 = None
		self.voicechat_window = None
		if app.ENABLE_VOICE_CHAT:
			self.vc_mic_device = None
			self.vc_spk_device = None
			self.vc_mic_device_text = None
			self.vc_spk_device_text = None
			self.vc_mic_volume = None
			self.vc_hear_volume = None
			self.vc_enable_on = None
			self.vc_enable_off = None
			self.vc_mic_device_index = 0
			self.vc_spk_device_index = 0
			self.vc_ptt_key = None
			self.vc_ptt_key_text = None
			self.vc_device_dropdown = None
			self.vc_ptt_capture = False
			self.vc_mic_meter = None        # #6 metr poziomu mikrofonu (ui.Gauge)
			self.vc_mic_level_label = None
			self.vc_type_local = None       # wybor kanalu glosowego (radio)
			self.vc_type_party = None
			self.vc_type_guild = None

		self.tilingMode = 0
		self.changeMusicButton = 0
		self.selectMusicFile = 0
		self.ctrlMusicVolume = 0
		self.ctrlSoundVolume = 0
		self.musicListDlg = 0
		self.tilingApplyButton = 0
		self.cameraModeButtonList = []
		self.fogModeButtonList = []
		self.tilingModeButtonList = []
		self.ctrlShadowQuality = 0
		if app.ENABLE_FOV_OPTION:
			self.fovController = None
			self.fovResetButton = None
			self.fovValueText = None


	def Destroy(self):
		self.ClearDictionary()
		if app.ENABLE_DYNAMIC_FONTS and self.FontsBoard:
			self.__CloseFonts()
		if app.ENABLE_SKYBOX_SELECT:
			self.skyBoxObjects = []
		if app.ENABLE_VOICE_CHAT:
			constInfo.SetVoicePTTCaptureMode(False)
			app.VoiceChatStopMicMonitor()  # #6: na wszelki wypadek zatrzymaj podglad
			if self.vc_device_dropdown:
				self.vc_device_dropdown.Destroy()
				self.vc_device_dropdown = None
			self.vc_mic_meter = None
			self.vc_mic_level_label = None
			self.vc_type_local = None
			self.vc_type_party = None
			self.vc_type_guild = None
		self.__Initialize()
		print(" -------------------------------------- DESTROY GAME OPTION DIALOG"
)

	def __Load_LoadScript(self, fileName):
		try:
			pyScriptLoader = ui.PythonScriptLoader()
			pyScriptLoader.LoadScriptFile(self, fileName)
		except:
			import exception
			exception.Abort("OptionDialog.__Load_LoadScript")

	def __Load_BindObject(self):
		try:
			GetObject = self.GetChild
			self.board = GetObject("board")
			self.titleBar = GetObject("titlebar")
			self.nameColorModeButtonList.append(GetObject("name_color_normal"))
			self.nameColorModeButtonList.append(GetObject("name_color_empire"))
			self.viewTargetBoardButtonList.append(GetObject("target_board_no_view"))
			self.viewTargetBoardButtonList.append(GetObject("target_board_view"))
			self.pvpModeButtonDict[player.PK_MODE_PEACE] = GetObject("pvp_peace")
			self.pvpModeButtonDict[player.PK_MODE_REVENGE] = GetObject("pvp_revenge")
			self.pvpModeButtonDict[player.PK_MODE_GUILD] = GetObject("pvp_guild")
			self.pvpModeButtonDict[player.PK_MODE_FREE] = GetObject("pvp_free")
			self.blockButtonList.append(GetObject("block_exchange_button"))
			self.blockButtonList.append(GetObject("block_party_button"))
			self.blockButtonList.append(GetObject("block_guild_button"))
			self.blockButtonList.append(GetObject("block_whisper_button"))
			self.blockButtonList.append(GetObject("block_friend_button"))
			self.blockButtonList.append(GetObject("block_party_request_button"))
			self.viewChatButtonList.append(GetObject("view_chat_on_button"))
			self.viewChatButtonList.append(GetObject("view_chat_off_button"))
			self.alwaysShowNameButtonList.append(GetObject("always_show_name_on_button"))
			self.alwaysShowNameButtonList.append(GetObject("always_show_name_off_button"))
			self.showDamageButtonList.append(GetObject("show_damage_on_button"))
			self.showDamageButtonList.append(GetObject("show_damage_off_button"))
			self.showsalesTextButtonList.append(GetObject("salestext_on_button"))
			if app.ENABLE_DOG_MODE:
				self.dogModeButtonList.append(GetObject("dog_mode_open"))
				self.dogModeButtonList.append(GetObject("dog_mode_close"))
			self.showsalesTextButtonList.append(GetObject("salestext_off_button"))
			self.fonttype.append(GetObject("font_type"))
			self.fonttype.append(GetObject("font_type2"))
			if app.WJ_SHOW_MOB_INFO:
				self.showMobInfoButtonList.append(GetObject("show_mob_level_button"))
				self.showMobInfoButtonList.append(GetObject("show_mob_AI_flag_button"))

			# Skybox selection buttons - add these to your UI script file
			if app.ENABLE_SKYBOX_SELECT:
				self.skyBoxList = ["skybox_type_default", "skybox_type_1",
				"skybox_type_2", "skybox_type_3", "skybox_type_4",
				"skybox_type_5", "skybox_type_6", "skybox_type_7"]
				for i in range(len(self.skyBoxList)):
					self.skyBoxObjects.append(i)
					self.skyBoxObjects[i] = GetObject(self.skyBoxList[i])
					self.skyBoxObjects[i].SAFE_SetEvent(self.OnSelectSkyBox, i)

			self.selectMusicFile = GetObject("bgm_file")
			self.changeMusicButton = GetObject("bgm_button")
			self.ctrlMusicVolume = GetObject("music_volume_controller")
			self.ctrlSoundVolume = GetObject("sound_volume_controller")
			self.cameraModeButtonList.append(GetObject("camera_short"))
			self.cameraModeButtonList.append(GetObject("camera_long"))
			self.fogModeButtonList.append(GetObject("fog_level0"))
			self.fogModeButtonList.append(GetObject("fog_level1"))
			self.fogModeButtonList.append(GetObject("fog_level2"))
			self.tilingModeButtonList.append(GetObject("tiling_cpu"))
			self.tilingModeButtonList.append(GetObject("tiling_gpu"))
			self.tilingApplyButton=GetObject("tiling_apply")
			self.vsyncButtonList.append(GetObject("vsync_on"))
			self.vsyncButtonList.append(GetObject("vsync_off"))
			if getattr(app, "ENABLE_RESIZABLE_WINDOW", 0):
				self.resizeWindowButtonList.append(GetObject("resize_window_on"))
				self.resizeWindowButtonList.append(GetObject("resize_window_off"))
			self.fpsLimitButton = GetObject("fps_limit_button")
			self.fpsLimitValueText = GetObject("fps_limit_value")
			if app.ENABLE_FOV_OPTION:
				self.fovController = GetObject("fov_controller")
				self.fovResetButton = GetObject("fov_reset_button")
				self.fovValueText = GetObject("fov_value_text")


			self.autobuff_on = GetObject("autobuff_on")
			self.autobuff_off = GetObject("autobuff_off")

			self.pety_on = GetObject("pety_on")
			self.pety_off = GetObject("pety_off")

			self.wierzchowce_on = GetObject("wierzchowce_on")
			self.wierzchowce_off = GetObject("wierzchowce_off")

			global MOBILE
			if MOBILE:
				self.inputMobileButton = GetObject("input_mobile_button")
				self.deleteMobileButton = GetObject("delete_mobile_button")

			self.global_window = GetObject("global_window")
			self.system_window = GetObject("system_window")
			self.desc_window = GetObject("desc_window")
			self.ukrywanie_window = GetObject("ukrywanie_window")
			self.category_btn1 = GetObject("category_btn1")
			self.category_btn2 = GetObject("category_btn2")
			self.category_btn3 = GetObject("category_btn3")
			self.category_btn4 = GetObject("category_btn4")
			self.category_btn5 = GetObject("category_btn5")
			self.voicechat_window = GetObject("voicechat_window")
			if app.ENABLE_VOICE_CHAT:
				self.vc_mic_device = GetObject("vc_mic_device")
				self.vc_spk_device = GetObject("vc_spk_device")
				self.vc_mic_device_text = GetObject("vc_mic_device_text")
				self.vc_spk_device_text = GetObject("vc_spk_device_text")
				self.vc_mic_volume = GetObject("vc_mic_volume")
				self.vc_hear_volume = GetObject("vc_hear_volume")
				self.vc_enable_on = GetObject("vc_enable_on")
				self.vc_enable_off = GetObject("vc_enable_off")
				self.vc_ptt_key = GetObject("vc_ptt_key")
				self.vc_ptt_key_text = GetObject("vc_ptt_key_text")
				self.vc_type_local = GetObject("vc_type_local")
				self.vc_type_party = GetObject("vc_type_party")
				self.vc_type_guild = GetObject("vc_type_guild")
				# #6: metr poziomu mikrofonu - tworzony w kodzie (ui.Gauge), parentowany
				# do voicechat_window (pokazuje sie/chowa razem z zakladka). Polowany w
				# OnUpdate z app.VoiceChatGetMicLevel(); tryb monitor start/stop sterowany
				# przez OpenVoiceChat / __HideAllPages.
				self.vc_mic_level_label = ui.TextLine()
				self.vc_mic_level_label.SetParent(self.voicechat_window)
				self.vc_mic_level_label.SetPosition(20, 322)
				self.vc_mic_level_label.SetText(localeInfo.VOICE_CHAT_MIC_LEVEL)
				self.vc_mic_level_label.Show()
				self.vc_mic_meter = ui.Gauge()
				self.vc_mic_meter.SetParent(self.voicechat_window)
				self.vc_mic_meter.MakeGauge(150, "lime")
				self.vc_mic_meter.SetPosition(176, 324)
				self.vc_mic_meter.SetPercentage(0, 100)
				self.vc_mic_meter.Show()
			else:
				self.category_btn5.Hide()
				self.voicechat_window.Hide()

			self.desc0_on = GetObject("desc0_on")
			self.desc0_off = GetObject("desc0_off")
			self.desc1_on = GetObject("desc1_on")
			self.desc1_off = GetObject("desc1_off")
			self.desc2_on = GetObject("desc2_on")
			self.desc2_off = GetObject("desc2_off")
			self.desc3_on = GetObject("desc3_on")
			self.desc3_off = GetObject("desc3_off")

			self.category_btn1.SetEvent(ui.__mem_func__(self.OpenOgolne))
			self.category_btn2.SetEvent(ui.__mem_func__(self.OpenSystemowe))
			self.category_btn3.SetEvent(ui.__mem_func__(self.OpenDesc))
			self.category_btn4.SetEvent(ui.__mem_func__(self.OpenUkrywanie))
			if app.ENABLE_VOICE_CHAT:
				self.category_btn5.SetEvent(ui.__mem_func__(self.OpenVoiceChat))

			self.page = 0
			if self.page == 0:
				self.desc_window.Hide()
				self.global_window.Show()
				self.system_window.Hide()
				self.ukrywanie_window.Hide()
				if app.ENABLE_VOICE_CHAT:
					self.voicechat_window.Hide()
				self.category_btn1.Down()
			else:
				self.category_btn1.SetUp()

			if self.page == 1:
				self.desc_window.Hide()
				self.global_window.Hide()
				self.system_window.Show()
				self.ukrywanie_window.Hide()
				if app.ENABLE_VOICE_CHAT:
					self.voicechat_window.Hide()
				self.category_btn2.Down()
			else:
				self.category_btn2.SetUp()

			if self.page == 2:
				self.global_window.Hide()
				self.desc_window.Show()
				self.system_window.Hide()
				self.ukrywanie_window.Hide()
				if app.ENABLE_VOICE_CHAT:
					self.voicechat_window.Hide()
				self.category_btn3.Down()
			else:
				self.category_btn3.SetUp()

			if self.page == 3:
				self.global_window.Hide()
				self.desc_window.Hide()
				self.system_window.Hide()
				self.ukrywanie_window.Show()
				if app.ENABLE_VOICE_CHAT:
					self.voicechat_window.Hide()
				self.category_btn4.Down()
			else:
				self.category_btn4.SetUp()

			if app.ENABLE_VOICE_CHAT:
				if self.page == 4:
					self.global_window.Hide()
					self.desc_window.Hide()
					self.system_window.Hide()
					self.ukrywanie_window.Hide()
					self.voicechat_window.Show()
					self.category_btn5.Down()
				else:
					self.category_btn5.SetUp()

			self.__ApplyYmirSliderSkin()

		except:
			import exception
			exception.Abort("OptionDialog.__Load_BindObject")

	# Klasyczny (ymirowy) wyglad suwakow: tlo sliderbar.tga 177x12 + kursor
	# sliderbar_cursor_button.tga 51x12. Kolejnosc ma znaczenie - SetBackgroundVisual
	# przelicza pageSize z aktualnej szerokosci kursora, wiec kursor ustawiamy pierwszy.
	# Wolane przed pierwszym SetSliderPos (ten leci dopiero w __Load).
	def __ApplyYmirSliderSkin(self):
		if not app.ENABLE_FOV_OPTION:
			return

		path = "d:/ymir work/ui/game/windows/"
		cursor = "sliderbar_cursor_button.tga"

		sliderList = [self.ctrlMusicVolume, self.ctrlSoundVolume]
		if app.ENABLE_FOV_OPTION:
			sliderList.append(self.fovController)
		if app.ENABLE_VOICE_CHAT:
			sliderList.append(self.vc_mic_volume)
			sliderList.append(self.vc_hear_volume)

		for slider in sliderList:
			if not slider:
				continue
			slider.SetButtonVisual(path, cursor, cursor, cursor)
			slider.SetBackgroundVisual(path + "sliderbar.tga")


	def __SetCategoryButtons(self, activeIndex):
		self.category_btn1.SetUp()
		self.category_btn2.SetUp()
		self.category_btn3.SetUp()
		self.category_btn4.SetUp()
		if app.ENABLE_VOICE_CHAT:
			self.category_btn5.SetUp()
		if activeIndex == 0:
			self.category_btn1.Down()
		elif activeIndex == 1:
			self.category_btn2.Down()
		elif activeIndex == 2:
			self.category_btn3.Down()
		elif activeIndex == 3:
			self.category_btn4.Down()
		elif activeIndex == 4 and app.ENABLE_VOICE_CHAT:
			self.category_btn5.Down()

	def __HideAllPages(self):
		self.global_window.Hide()
		self.desc_window.Hide()
		self.system_window.Hide()
		self.ukrywanie_window.Hide()
		if app.ENABLE_VOICE_CHAT and self.voicechat_window:
			self.voicechat_window.Hide()
			self.__CancelVoicePTTCapture()
			if self.vc_device_dropdown:
				self.vc_device_dropdown.Close()
			# #6: zejscie z zakladki voice -> zatrzymaj podglad mikrofonu (KRYTYCZNE:
			# inaczej capture zostaje otwarty). Pojedynczy choke-point wszystkich Open*.
			app.VoiceChatStopMicMonitor()
			if self.vc_mic_meter:
				self.vc_mic_meter.SetPercentage(0, 100)

	def OpenOgolne(self):
		self.page = 0
		self.__SetCategoryButtons(0)
		self.__HideAllPages()
		self.global_window.Show()

	def OpenSystemowe(self):
		self.page = 1
		self.__SetCategoryButtons(1)
		self.__HideAllPages()
		self.system_window.Show()

	def OpenDesc(self):
		self.page = 2
		self.__SetCategoryButtons(2)
		self.__HideAllPages()
		self.desc_window.Show()

	def OpenUkrywanie(self):
		self.page = 3
		self.__SetCategoryButtons(3)
		self.__HideAllPages()
		self.ukrywanie_window.Show()

	if app.ENABLE_VOICE_CHAT:
		def OpenVoiceChat(self):
			self.page = 4
			self.__SetCategoryButtons(4)
			self.__HideAllPages()
			self.voicechat_window.Show()
			self.__RefreshVoiceChat()
			# #6: wlacz podglad mikrofonu (capture bez wysylki) dla paska poziomu.
			app.VoiceChatStartMicMonitor()

		def OnUpdate(self):
			# #6: odswiezaj pasek poziomu mikrofonu tylko gdy zakladka voice widoczna.
			if self.vc_mic_meter and self.voicechat_window and self.voicechat_window.IsShow():
				self.vc_mic_meter.SetPercentage(int(app.VoiceChatGetMicLevel() * 100), 100)

	def __Load(self):
		global MOBILE
		if MOBILE:
			self.__Load_LoadScript("uiscript/gameoptiondialog_formobile.py")
		else:
			self.__Load_LoadScript("uiscript/gameoptiondialog.py")

		self.__Load_BindObject()

		self.SetCenterPosition()

		self.titleBar.SetCloseEvent(ui.__mem_func__(self.Close))

		self.cameraModeButtonList[0].SAFE_SetEvent(self.__OnClickCameraModeShortButton)
		self.cameraModeButtonList[1].SAFE_SetEvent(self.__OnClickCameraModeLongButton)

		self.vsyncButtonList[0].SAFE_SetEvent(self.__OnClickVSyncOnButton)
		self.vsyncButtonList[1].SAFE_SetEvent(self.__OnClickVSyncOffButton)
		if self.resizeWindowButtonList:
			self.resizeWindowButtonList[0].SAFE_SetEvent(self.__OnClickResizeWindowOnButton)
			self.resizeWindowButtonList[1].SAFE_SetEvent(self.__OnClickResizeWindowOffButton)
		self.fpsLimitButton.SAFE_SetEvent(self.__OnClickFpsLimitButton)
		self.__InitGraphicOptions()

		if app.ENABLE_FOV_OPTION:
			if self.fovController:
				self.fovController.SetSliderPos(float(systemSetting.GetFOV()) / float(app.MAX_CAMERA_PERSPECTIVE))
				self.fovController.SetEvent(ui.__mem_func__(self.__OnChangeFOV))

			if self.fovValueText:
				self.fovValueText.SetText(str(int(systemSetting.GetFOV())))

			if self.fovResetButton:
				self.fovResetButton.SetEvent(ui.__mem_func__(self.__OnClickFOVResetButton))
		

		self.autobuff_off.SAFE_SetEvent(self.onclickautobuffOFF)
		self.autobuff_on.SAFE_SetEvent(self.onclickautobuffON)

		self.pety_off.SAFE_SetEvent(self.onclickPetyOFF)
		self.pety_on.SAFE_SetEvent(self.onclickPetyON)

		self.wierzchowce_off.SAFE_SetEvent(self.onclickWierzchOFF)
		self.wierzchowce_on.SAFE_SetEvent(self.onclickWierzchON)

		self.nameColorModeButtonList[0].SAFE_SetEvent(self.__OnClickNameColorModeNormalButton)
		self.nameColorModeButtonList[1].SAFE_SetEvent(self.__OnClickNameColorModeEmpireButton)

		self.viewTargetBoardButtonList[0].SAFE_SetEvent(self.__OnClickTargetBoardViewButton)
		self.viewTargetBoardButtonList[1].SAFE_SetEvent(self.__OnClickTargetBoardNoViewButton)

		self.pvpModeButtonDict[player.PK_MODE_PEACE].SAFE_SetEvent(self.__OnClickPvPModePeaceButton)
		self.pvpModeButtonDict[player.PK_MODE_REVENGE].SAFE_SetEvent(self.__OnClickPvPModeRevengeButton)
		self.pvpModeButtonDict[player.PK_MODE_GUILD].SAFE_SetEvent(self.__OnClickPvPModeGuildButton)
		self.pvpModeButtonDict[player.PK_MODE_FREE].SAFE_SetEvent(self.__OnClickPvPModeFreeButton)

		self.blockButtonList[0].SetToggleUpEvent(self.__OnClickBlockExchangeButton)
		self.blockButtonList[1].SetToggleUpEvent(self.__OnClickBlockPartyButton)
		self.blockButtonList[2].SetToggleUpEvent(self.__OnClickBlockGuildButton)
		self.blockButtonList[3].SetToggleUpEvent(self.__OnClickBlockWhisperButton)
		self.blockButtonList[4].SetToggleUpEvent(self.__OnClickBlockFriendButton)
		self.blockButtonList[5].SetToggleUpEvent(self.__OnClickBlockPartyRequest)

		self.blockButtonList[0].SetToggleDownEvent(self.__OnClickBlockExchangeButton)
		self.blockButtonList[1].SetToggleDownEvent(self.__OnClickBlockPartyButton)
		self.blockButtonList[2].SetToggleDownEvent(self.__OnClickBlockGuildButton)
		self.blockButtonList[3].SetToggleDownEvent(self.__OnClickBlockWhisperButton)
		self.blockButtonList[4].SetToggleDownEvent(self.__OnClickBlockFriendButton)
		self.blockButtonList[5].SetToggleDownEvent(self.__OnClickBlockPartyRequest)

		self.viewChatButtonList[0].SAFE_SetEvent(self.__OnClickViewChatOnButton)
		self.viewChatButtonList[1].SAFE_SetEvent(self.__OnClickViewChatOffButton)

		self.alwaysShowNameButtonList[0].SAFE_SetEvent(self.__OnClickAlwaysShowNameOnButton)
		self.alwaysShowNameButtonList[1].SAFE_SetEvent(self.__OnClickAlwaysShowNameOffButton)

		self.showDamageButtonList[0].SAFE_SetEvent(self.__OnClickShowDamageOnButton)
		self.showDamageButtonList[1].SAFE_SetEvent(self.__OnClickShowDamageOffButton)

		self.showsalesTextButtonList[0].SAFE_SetEvent(self.__OnClickSalesTextOnButton)
		self.showsalesTextButtonList[1].SAFE_SetEvent(self.__OnClickSalesTextOffButton)
		
		self.desc0_on.SAFE_SetEvent(self.desc0_OnButton)
		self.desc0_off.SAFE_SetEvent(self.desc0_OffButton)

		self.desc1_on.SAFE_SetEvent(self.desc1_OnButton)
		self.desc1_off.SAFE_SetEvent(self.desc1_OffButton)

		self.desc2_on.SAFE_SetEvent(self.desc2_OnButton)
		self.desc2_off.SAFE_SetEvent(self.desc2_OffButton)

		self.desc3_on.SAFE_SetEvent(self.desc3_OnButton)
		self.desc3_off.SAFE_SetEvent(self.desc3_OffButton)

		if app.ENABLE_DOG_MODE:
			self.dogModeButtonList[0].SAFE_SetEvent(self.__OnClickDogButton)
			self.dogModeButtonList[1].SAFE_SetEvent(self.__OffClickDogButton)

		self.fonttype[0].SAFE_SetEvent(self.__OnClickFontChangeSmallButton)
		self.fonttype[1].SAFE_SetEvent(self.__OnClickFontChangeBigButton)

		if app.WJ_SHOW_MOB_INFO:
			self.showMobInfoButtonList[0].SetToggleUpEvent(self.__OnClickShowMobLevelButton)
			self.showMobInfoButtonList[0].SetToggleDownEvent(self.__OnClickShowMobLevelButton)
			self.showMobInfoButtonList[1].SetToggleUpEvent(self.__OnClickShowMobAIFlagButton)
			self.showMobInfoButtonList[1].SetToggleDownEvent(self.__OnClickShowMobAIFlagButton)

		self.fogModeButtonList[0].SAFE_SetEvent(self.__OnClickFogModeLevel0Button)
		self.fogModeButtonList[1].SAFE_SetEvent(self.__OnClickFogModeLevel1Button)
		self.fogModeButtonList[2].SAFE_SetEvent(self.__OnClickFogModeLevel2Button)

		self.changeMusicButton.SAFE_SetEvent(self.__OnClickChangeMusicButton)
		self.ctrlMusicVolume.SetSliderPos(float(systemSetting.GetMusicVolume()))
		self.ctrlMusicVolume.SetEvent(ui.__mem_func__(self.OnChangeMusicVolume))
		self.ctrlSoundVolume.SetSliderPos(systemSetting.GetSoundVolumef())
		self.ctrlSoundVolume.SetEvent(ui.__mem_func__(self.OnChangeSoundVolume))

		self.tilingModeButtonList[0].SAFE_SetEvent(self.__OnClickTilingModeCPUButton)
		self.tilingModeButtonList[1].SAFE_SetEvent(self.__OnClickTilingModeGPUButton)
		self.tilingApplyButton.SAFE_SetEvent(self.__OnClickTilingApplyButton)
		self.__SetCurTilingMode()

		self.__ClickRadioButton(self.fogModeButtonList, constInfo.GET_FOG_LEVEL_INDEX())
		self.__ClickRadioButton(self.cameraModeButtonList, constInfo.GET_CAMERA_MAX_DISTANCE_INDEX())

		self.__ClickRadioButton(self.nameColorModeButtonList, constInfo.GET_CHRNAME_COLOR_INDEX())
		self.__ClickRadioButton(self.viewTargetBoardButtonList, constInfo.GET_VIEW_OTHER_EMPIRE_PLAYER_TARGET_BOARD())

		if musicInfo.fieldMusic==musicInfo.METIN2THEMA:
			self.selectMusicFile.SetText(uiSelectMusic.DEFAULT_THEMA)
		else:
			self.selectMusicFile.SetText(musicInfo.fieldMusic[:MUSIC_FILENAME_MAX_LEN])

		self.__SetPeacePKMode()

		if app.ENABLE_VOICE_CHAT:
			self.vc_mic_device.SetEvent(ui.__mem_func__(self.__OnClickVoiceMicDevice))
			self.vc_spk_device.SetEvent(ui.__mem_func__(self.__OnClickVoiceSpkDevice))
			self.vc_mic_volume.SetEvent(ui.__mem_func__(self.__OnChangeVoiceMicVolume))
			self.vc_hear_volume.SetEvent(ui.__mem_func__(self.__OnChangeVoiceHearVolume))
			self.vc_enable_on.SAFE_SetEvent(self.__OnClickVoiceEnableOn)
			self.vc_enable_off.SAFE_SetEvent(self.__OnClickVoiceEnableOff)
			self.vc_type_local.SAFE_SetEvent(self.__OnClickVoiceTypeLocal)
			self.vc_type_party.SAFE_SetEvent(self.__OnClickVoiceTypeParty)
			self.vc_type_guild.SAFE_SetEvent(self.__OnClickVoiceTypeGuild)
			self.vc_ptt_key.SetEvent(ui.__mem_func__(self.__OnClickVoicePTTKey))
			self.vc_device_dropdown = VoiceDeviceDropDown()
			self.vc_device_dropdown.Hide()
			self.vc_mic_device_index = constInfo.GetVoiceChatConfig("VOICE_CHAT_MIC_DEVICE")
			self.vc_spk_device_index = constInfo.GetVoiceChatConfig("VOICE_CHAT_SPK_DEVICE")
			self.__RefreshVoiceChat()

		if MOBILE:
			self.inputMobileButton.SetEvent(ui.__mem_func__(self.__OnChangeMobilePhoneNumber))
			self.deleteMobileButton.SetEvent(ui.__mem_func__(self.__OnDeleteMobilePhoneNumber))

	# Skybox Selection Functions
	if app.ENABLE_SKYBOX_SELECT:
		def OnSelectSkyBox(self, index):
			systemSetting.SetSkyBox(index)
			self.RefreshSkyBoxButtons()

		def RefreshSkyBoxButtons(self):
			index = systemSetting.GetSkyBox()

			if index == 0:
				background.SetDefaultSkybox()
			else:
				background.RegisterEnvironmentData(index, self.skyBoxes[index])
				background.SetEnvironmentData(index)

			self.skyBoxObjects[index].Down()
			for j in range(len(self.skyBoxObjects)):
				if j != index:
					self.skyBoxObjects[j].SetUp()

	def __ClickRadioButton(self, buttonList, buttonIndex):
		try:
			selButton=buttonList[buttonIndex]
		except IndexError:
			return

		for eachButton in buttonList:
			eachButton.SetUp()

		selButton.Down()

	def __InitGraphicOptions(self):
		# VSync: stan poczatkowy z configu klienta (metin2.cfg, strona C++)
		self.__ClickRadioButton(self.vsyncButtonList, 0 if app.GetVSync() else 1)

		# Rozciaganie okna: tez z metin2.cfg. W pelnym ekranie nie ma ramki do zlapania,
		# wiec przelacznik jest wtedy martwy - pokazujemy go jako wylaczony i nie pozwalamy
		# wlaczyc, zeby gracz nie szukal uchwytu, ktorego nie bedzie.
		if not self.resizeWindowButtonList:
			pass
		elif app.IsWindowedMode():
			self.__ClickRadioButton(self.resizeWindowButtonList, 0 if app.IsWindowResizable() else 1)
		else:
			self.__ClickRadioButton(self.resizeWindowButtonList, 1)
			self.resizeWindowButtonList[0].Disable()
			self.resizeWindowButtonList[1].Disable()

		# Limit FPS: wartosc z rejestru. Wartosc spoza listy (wpisana recznie)
		# pokazujemy 1:1; cykl przeskoczy na liste przy pierwszym kliknieciu.
		value = int(settings.get("fps_limit", 60))
		choices = settings.FPS_LIMIT_CHOICES
		if value in choices:
			self.fpsLimitIndex = choices.index(value)
		else:
			self.fpsLimitIndex = -1
		self.__RefreshFpsLimitButton(value)

	def __OnClickVSyncOnButton(self):
		app.SetVSync(True)
		self.__ClickRadioButton(self.vsyncButtonList, 0)

	def __OnClickVSyncOffButton(self):
		app.SetVSync(False)
		self.__ClickRadioButton(self.vsyncButtonList, 1)

	def __OnClickResizeWindowOnButton(self):
		if not app.IsWindowedMode():
			return
		app.SetWindowResizable(True)
		self.__ClickRadioButton(self.resizeWindowButtonList, 0)

	def __OnClickResizeWindowOffButton(self):
		app.SetWindowResizable(False)
		self.__ClickRadioButton(self.resizeWindowButtonList, 1)

	def __OnClickFpsLimitButton(self):
		choices = settings.FPS_LIMIT_CHOICES
		self.fpsLimitIndex = (self.fpsLimitIndex + 1) % len(choices)
		value = choices[self.fpsLimitIndex]
		settings.set("fps_limit", value)
		app.SetFPS(int(value))
		self.__RefreshFpsLimitButton(value)

	def __RefreshFpsLimitButton(self, value):
		if not self.fpsLimitValueText:
			return
		if int(value) >= 1000:
			self.fpsLimitValueText.SetText(uiScriptLocale.OPTION_FPS_UNLIMITED)
		else:
			self.fpsLimitValueText.SetText(str(int(value)))

	def __OnClickTilingModeCPUButton(self):
		self.__NotifyChatLine(localeInfo.SYSTEM_OPTION_CPU_TILING_1)
		self.__NotifyChatLine(localeInfo.SYSTEM_OPTION_CPU_TILING_2)
		self.__NotifyChatLine(localeInfo.SYSTEM_OPTION_CPU_TILING_3)
		self.__SetTilingMode(0)

	def __OnClickTilingModeGPUButton(self):
		self.__NotifyChatLine(localeInfo.SYSTEM_OPTION_GPU_TILING_1)
		self.__NotifyChatLine(localeInfo.SYSTEM_OPTION_GPU_TILING_2)
		self.__NotifyChatLine(localeInfo.SYSTEM_OPTION_GPU_TILING_3)
		self.__SetTilingMode(1)

	def __SetTilingMode(self, index):
		self.__ClickRadioButton(self.tilingModeButtonList, index)
		self.tilingMode=index

	def __OnClickTilingApplyButton(self):
		self.__NotifyChatLine(localeInfo.SYSTEM_OPTION_TILING_EXIT)
		if 0==self.tilingMode:
			background.EnableSoftwareTiling(1)
		else:
			background.EnableSoftwareTiling(0)

		self.Close()
		net.ExitApplication()

	def __SetNameColorMode(self, index):
		constInfo.SET_CHRNAME_COLOR_INDEX(index)
		self.__ClickRadioButton(self.nameColorModeButtonList, index)

	def __SetTargetBoardViewMode(self, flag):
		constInfo.SET_VIEW_OTHER_EMPIRE_PLAYER_TARGET_BOARD(flag)
		self.__ClickRadioButton(self.viewTargetBoardButtonList, flag)

	def __OnClickNameColorModeNormalButton(self):
		self.__SetNameColorMode(0)

	def __OnClickNameColorModeEmpireButton(self):
		self.__SetNameColorMode(1)

	def __OnClickTargetBoardViewButton(self):
		self.__SetTargetBoardViewMode(0)

	def __OnClickTargetBoardNoViewButton(self):
		self.__SetTargetBoardViewMode(1)

	def __OnClickCameraModeShortButton(self):
		self.__SetCameraMode(0)

	def __OnClickCameraModeLongButton(self):
		self.__SetCameraMode(1)

	def __OnClickFogModeLevel0Button(self):
		self.__SetFogLevel(0)

	def __OnClickFogModeLevel1Button(self):
		self.__SetFogLevel(1)

	def __OnClickFogModeLevel2Button(self):
		self.__SetFogLevel(2)

	def __OnClickBlockExchangeButton(self):
		self.RefreshBlock()
		global blockMode
		net.SendChatPacket("/setblockmode " + str(blockMode ^ player.BLOCK_EXCHANGE))
	def __OnClickBlockPartyButton(self):
		self.RefreshBlock()
		global blockMode
		net.SendChatPacket("/setblockmode " + str(blockMode ^ player.BLOCK_PARTY))
	def __OnClickBlockGuildButton(self):
		self.RefreshBlock()
		global blockMode
		net.SendChatPacket("/setblockmode " + str(blockMode ^ player.BLOCK_GUILD))
	def __OnClickBlockWhisperButton(self):
		self.RefreshBlock()
		global blockMode
		net.SendChatPacket("/setblockmode " + str(blockMode ^ player.BLOCK_WHISPER))
	def __OnClickBlockFriendButton(self):
		self.RefreshBlock()
		global blockMode
		net.SendChatPacket("/setblockmode " + str(blockMode ^ player.BLOCK_FRIEND))
	def __OnClickBlockPartyRequest(self):
		self.RefreshBlock()
		global blockMode
		net.SendChatPacket("/setblockmode " + str(blockMode ^ player.BLOCK_PARTY_REQUEST))

	def __OnClickViewChatOnButton(self):
		global viewChatMode
		viewChatMode = 1
		systemSetting.SetViewChatFlag(viewChatMode)
		self.RefreshViewChat()
	def __OnClickViewChatOffButton(self):
		global viewChatMode
		viewChatMode = 0
		systemSetting.SetViewChatFlag(viewChatMode)
		self.RefreshViewChat()

	def __OnClickAlwaysShowNameOnButton(self):
		systemSetting.SetAlwaysShowNameFlag(True)
		self.RefreshAlwaysShowName()

	def __OnClickAlwaysShowNameOffButton(self):
		systemSetting.SetAlwaysShowNameFlag(False)
		self.RefreshAlwaysShowName()

	def __OnClickShowDamageOnButton(self):
		systemSetting.SetShowDamageFlag(True)
		self.RefreshShowDamage()

	def __OnClickShowDamageOffButton(self):
		systemSetting.SetShowDamageFlag(False)
		self.RefreshShowDamage()

	def __OnClickFontChangeSmallButton(self):
		f = open("_cfg/font.cfg", "r+")
		f.write("0")
		f.close()
		self.RefreshFontText()
		chat.AppendChat(chat.CHAT_TYPE_INFO, "K teto zmene je nutny restart hry.")
		self.fonttype[1].SetUp()

	def __OnClickFontChangeBigButton(self):
		f = open("_cfg/font.cfg", "r+")
		f.write("1")
		f.close()
		self.RefreshFontText()
		chat.AppendChat(chat.CHAT_TYPE_INFO, "K teto zmene je nutny restart hry.")
		self.fonttype[0].SetUp()

	def desc0_OnButton(self):
		settings.find_chest_tooltip = 1
		self.RefreshDesc0Btn()

	def desc0_OffButton(self):
		settings.find_chest_tooltip = 0
		self.RefreshDesc0Btn()

	def desc1_OnButton(self):
		settings.split_tooltip = 1
		self.RefreshDesc1Btn()

	def desc1_OffButton(self):
		settings.split_tooltip = 0
		self.RefreshDesc1Btn()

	def desc2_OnButton(self):
		settings.extract_tooltip = 1
		self.RefreshDesc2Btn()

	def desc2_OffButton(self):
		settings.extract_tooltip = 0
		self.RefreshDesc2Btn()

	def desc3_OnButton(self):
		settings.add_additional_tooltip = 1
		self.RefreshDesc3Btn()

	def desc3_OffButton(self):
		settings.add_additional_tooltip = 0
		self.RefreshDesc3Btn()

	def __OnClickSalesTextOnButton(self):
		systemSetting.SetShowSalesTextFlag(True)
		self.RefreshShowSalesText()
		uiPrivateShopBuilder.UpdateADBoard()

	def __OnClickSalesTextOffButton(self):
		systemSetting.SetShowSalesTextFlag(False)
		self.RefreshShowSalesText()

	if app.ENABLE_DOG_MODE:
		def __OnClickDogButton(self):
			systemSetting.SetDogMode(True)
			self.RefreshDogMode()

		def __OffClickDogButton(self):
			systemSetting.SetDogMode(False)
			self.RefreshDogMode()

		def RefreshDogMode(self):
			if systemSetting.GetDogMode():
				self.dogModeButtonList[0].Down()
				self.dogModeButtonList[1].SetUp()
			else:
				self.dogModeButtonList[0].SetUp()
				self.dogModeButtonList[1].Down()

	if app.WJ_SHOW_MOB_INFO:
		def __OnClickShowMobLevelButton(self):
			systemSetting.SetShowMobLevel(not systemSetting.IsShowMobLevel())
			self.RefreshShowMobInfo()
		def __OnClickShowMobAIFlagButton(self):
			systemSetting.SetShowMobAIFlag(not systemSetting.IsShowMobAIFlag())
			self.RefreshShowMobInfo()

	def __CheckPvPProtectedLevelPlayer(self):
		if player.GetStatus(player.LEVEL)<constInfo.PVPMODE_PROTECTED_LEVEL:
			self.__SetPeacePKMode()
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.OPTION_PVPMODE_PROTECT % (constInfo.PVPMODE_PROTECTED_LEVEL))
			return 1

		return 0

	def __SetPKMode(self, mode):
		for btn in self.pvpModeButtonDict.values():
			btn.SetUp()
		if mode in self.pvpModeButtonDict:
			self.pvpModeButtonDict[mode].Down()

	def __SetPeacePKMode(self):
		self.__SetPKMode(player.PK_MODE_PEACE)

	def __RefreshPVPButtonList(self):
		self.__SetPKMode(player.GetPKMode())

	def __OnClickPvPModePeaceButton(self):
		if self.__CheckPvPProtectedLevelPlayer():
			return

		self.__RefreshPVPButtonList()

		if constInfo.PVPMODE_ENABLE:
			net.SendChatPacket("/pkmode 0", chat.CHAT_TYPE_TALKING)
		else:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.OPTION_PVPMODE_NOT_SUPPORT)

	def __OnClickPvPModeRevengeButton(self):
		if self.__CheckPvPProtectedLevelPlayer():
			return

		self.__RefreshPVPButtonList()

		if constInfo.PVPMODE_ENABLE:
			net.SendChatPacket("/pkmode 1", chat.CHAT_TYPE_TALKING)
		else:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.OPTION_PVPMODE_NOT_SUPPORT)

	def __OnClickPvPModeFreeButton(self):
		if self.__CheckPvPProtectedLevelPlayer():
			return

		self.__RefreshPVPButtonList()

		if constInfo.PVPMODE_ENABLE:
			net.SendChatPacket("/pkmode 2", chat.CHAT_TYPE_TALKING)
		else:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.OPTION_PVPMODE_NOT_SUPPORT)

	def __OnClickPvPModeGuildButton(self):
		if self.__CheckPvPProtectedLevelPlayer():
			return

		self.__RefreshPVPButtonList()

		if 0 == player.GetGuildID():
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.OPTION_PVPMODE_CANNOT_SET_GUILD_MODE)
			return

		if constInfo.PVPMODE_ENABLE:
			net.SendChatPacket("/pkmode 4", chat.CHAT_TYPE_TALKING)
		else:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.OPTION_PVPMODE_NOT_SUPPORT)

	def OnChangePKMode(self):
		self.__RefreshPVPButtonList()

	def __OnChangeMobilePhoneNumber(self):
		global MOBILE
		if not MOBILE:
			return

		import uiCommon
		inputDialog = uiCommon.InputDialog()
		inputDialog.SetTitle(localeInfo.MESSENGER_INPUT_MOBILE_PHONE_NUMBER_TITLE)
		inputDialog.SetMaxLength(13)
		inputDialog.SetAcceptEvent(ui.__mem_func__(self.OnInputMobilePhoneNumber))
		inputDialog.SetCancelEvent(ui.__mem_func__(self.OnCloseInputDialog))
		inputDialog.Open()
		self.inputDialog = inputDialog

	def __OnDeleteMobilePhoneNumber(self):
		global MOBILE
		if not MOBILE:
			return

		import uiCommon
		questionDialog = uiCommon.QuestionDialog()
		questionDialog.SetText(localeInfo.MESSENGER_DO_YOU_DELETE_PHONE_NUMBER)
		questionDialog.SetAcceptEvent(ui.__mem_func__(self.OnDeleteMobile))
		questionDialog.SetCancelEvent(ui.__mem_func__(self.OnCloseQuestionDialog))
		questionDialog.Open()
		self.questionDialog = questionDialog

	def OnInputMobilePhoneNumber(self):
		global MOBILE
		if not MOBILE:
			return

		text = self.inputDialog.GetText()

		if not text:
			return

		text.replace('-', '')
		net.SendChatPacket("/mobile " + text)
		self.OnCloseInputDialog()
		return True

	def OnInputMobileAuthorityCode(self):
		global MOBILE
		if not MOBILE:
			return

		text = self.inputDialog.GetText()
		net.SendChatPacket("/mobile_auth " + text)
		self.OnCloseInputDialog()
		return True

	def OnDeleteMobile(self):
		global MOBILE
		if not MOBILE:
			return

		net.SendChatPacket("/mobile")
		self.OnCloseQuestionDialog()
		return True

	def OnCloseInputDialog(self):
		self.inputDialog.Close()
		self.inputDialog = None
		return True

	def OnCloseQuestionDialog(self):
		self.questionDialog.Close()
		self.questionDialog = None
		return True

	def OnPressEscapeKey(self):
		self.Close()
		return True

	def RefreshMobile(self):
		global MOBILE
		if not MOBILE:
			return

		if player.HasMobilePhoneNumber():
			self.inputMobileButton.Hide()
			self.deleteMobileButton.Show()
		else:
			self.inputMobileButton.Show()
			self.deleteMobileButton.Hide()

	def OnMobileAuthority(self):
		global MOBILE
		if not MOBILE:
			return

		import uiCommon
		inputDialog = uiCommon.InputDialogWithDescription()
		inputDialog.SetTitle(localeInfo.MESSENGER_INPUT_MOBILE_AUTHORITY_TITLE)
		inputDialog.SetDescription(localeInfo.MESSENGER_INPUT_MOBILE_AUTHORITY_DESCRIPTION)
		inputDialog.SetAcceptEvent(ui.__mem_func__(self.OnInputMobileAuthorityCode))
		inputDialog.SetCancelEvent(ui.__mem_func__(self.OnCloseInputDialog))
		inputDialog.SetMaxLength(4)
		inputDialog.SetBoardWidth(310)
		inputDialog.Open()
		self.inputDialog = inputDialog

	def RefreshBlock(self):
		global blockMode
		for i in range(len(self.blockButtonList)):
			if 0 != (blockMode & (1 << i)):
				self.blockButtonList[i].Down()
			else:
				self.blockButtonList[i].SetUp()

	def RefreshViewChat(self):
		if systemSetting.IsViewChat():
			self.viewChatButtonList[0].Down()
			self.viewChatButtonList[1].SetUp()
		else:
			self.viewChatButtonList[0].SetUp()
			self.viewChatButtonList[1].Down()

	def RefreshAlwaysShowName(self):
		if systemSetting.IsAlwaysShowName():
			self.alwaysShowNameButtonList[0].Down()
			self.alwaysShowNameButtonList[1].SetUp()
		else:
			self.alwaysShowNameButtonList[0].SetUp()
			self.alwaysShowNameButtonList[1].Down()

	def RefreshShowDamage(self):
		if systemSetting.IsShowDamage():
			self.showDamageButtonList[0].Down()
			self.showDamageButtonList[1].SetUp()
		else:
			self.showDamageButtonList[0].SetUp()
			self.showDamageButtonList[1].Down()

	def RefreshDesc0Btn(self):
		if settings.find_chest_tooltip == 1:
			self.desc0_on.Down()
			self.desc0_off.SetUp()
		else:
			self.desc0_off.Down()
			self.desc0_on.SetUp()

	def RefreshDesc1Btn(self):
		if settings.split_tooltip == 1:
			self.desc1_on.Down()
			self.desc1_off.SetUp()
		else:
			self.desc1_off.Down()
			self.desc1_on.SetUp()

	def RefreshDesc2Btn(self):
		if settings.extract_tooltip == 1:
			self.desc2_on.Down()
			self.desc2_off.SetUp()
		else:
			self.desc2_off.Down()
			self.desc2_on.SetUp()

	def RefreshDesc3Btn(self):
		if settings.add_additional_tooltip == 1:
			self.desc3_on.Down()
			self.desc3_off.SetUp()
		else:
			self.desc3_off.Down()
			self.desc3_on.SetUp()

	def RefreshShowSalesText(self):
		if systemSetting.IsShowSalesText():
			self.showsalesTextButtonList[0].Down()
			self.showsalesTextButtonList[1].SetUp()
		else:
			self.showsalesTextButtonList[0].SetUp()
			self.showsalesTextButtonList[1].Down()

	def RefreshFontText(self):
		f = open("_cfg/font.cfg", "r+")
		hehe = f.read()
		if hehe == "1":
			self.fonttype[1].Down()
		elif hehe == "0":
			self.fonttype[0].Down()
		else:
			self.fonttype[0].Down()
			self.fonttype[1].Down()

	if app.WJ_SHOW_MOB_INFO:
		def RefreshShowMobInfo(self):
			if systemSetting.IsShowMobLevel():
				self.showMobInfoButtonList[0].Down()
			else:
				self.showMobInfoButtonList[0].SetUp()
			if systemSetting.IsShowMobAIFlag():
				self.showMobInfoButtonList[1].Down()
			else:
				self.showMobInfoButtonList[1].SetUp()

	def OnBlockMode(self, mode):
		global blockMode
		blockMode = mode
		self.RefreshBlock()

	def Show(self):
		self.RefreshMobile()
		self.RefreshBlock()
		ui.ScriptWindow.Show(self)

	def Close(self):
		self.__SetCurTilingMode()
		# #6: zamkniecie okna opcji -> zatrzymaj podglad mikrofonu (gdyby zamknieto
		# bedac na zakladce voice).
		if app.ENABLE_VOICE_CHAT:
			app.VoiceChatStopMicMonitor()
		self.Hide()

	def __SetCurTilingMode(self):
		if background.IsSoftwareTiling():
			self.__SetTilingMode(0)
		else:
			self.__SetTilingMode(1)

	def __NotifyChatLine(self, text):
		chat.AppendChat(chat.CHAT_TYPE_INFO, text)

	if app.ENABLE_FOV_OPTION:
		def __OnChangeFOV(self):
			pos = self.fovController.GetSliderPos()
			systemSetting.SetFOV(pos * float(app.MAX_CAMERA_PERSPECTIVE))

			if self.fovValueText:
				self.fovValueText.SetText(str(int(systemSetting.GetFOV())))

		def __OnClickFOVResetButton(self):
			self.fovController.SetSliderPos(float(app.DEFAULT_CAMERA_PERSPECTIVE) / float(app.MAX_CAMERA_PERSPECTIVE))
			systemSetting.SetFOV(float(app.DEFAULT_CAMERA_PERSPECTIVE))

			if self.fovValueText:
				self.fovValueText.SetText(str(int(systemSetting.GetFOV())))


	def onclickautobuffOFF(self):
		systemSetting.SetShowAutoBuffMode(1)
		self.RefreshAutobuff()

	def onclickautobuffON(self):
		systemSetting.SetShowAutoBuffMode(0)
		self.RefreshAutobuff()

	def RefreshAutobuff(self):
		if systemSetting.GetShowAutoBuffMode() == 1:
			self.autobuff_off.Down()
			self.autobuff_on.SetUp()
		else:
			self.autobuff_off.SetUp()
			self.autobuff_on.Down()

	def onclickPetyOFF(self):
		systemSetting.SetShowPetMode(1)
		self.RefreshPetOptions()

	def onclickPetyON(self):
		systemSetting.SetShowPetMode(0)
		self.RefreshPetOptions()

	def RefreshPetOptions(self):
		if systemSetting.GetShowPetMode() == 1:
			self.pety_off.Down()
			self.pety_on.SetUp()
		else:
			self.pety_off.SetUp()
			self.pety_on.Down()

	def onclickWierzchOFF(self):
		systemSetting.SetShowMountMode(1)
		self.RefreshWierzch()

	def onclickWierzchON(self):
		systemSetting.SetShowMountMode(0)
		self.RefreshWierzch()

	def RefreshWierzch(self):
		if systemSetting.GetShowMountMode() == 1:
			self.wierzchowce_off.Down()
			self.wierzchowce_on.SetUp()
		else:
			self.wierzchowce_off.SetUp()
			self.wierzchowce_on.Down()

	def __SetFogLevel(self, index):
		constInfo.SET_FOG_LEVEL_INDEX(index)
		self.__ClickRadioButton(self.fogModeButtonList, index)

	def __SetCameraMode(self, index):
		constInfo.SET_CAMERA_MAX_DISTANCE_INDEX(index)
		self.__ClickRadioButton(self.cameraModeButtonList, index)

	def __OnClickCameraModeShortButton(self):
		self.__SetCameraMode(0)

	def __OnClickCameraModeLongButton(self):
		self.__SetCameraMode(1)

	def __OnChangeMusic(self, fileName):
		self.selectMusicFile.SetText(fileName[:MUSIC_FILENAME_MAX_LEN])

		if musicInfo.fieldMusic != "":
			snd.FadeOutMusic("BGM/"+ musicInfo.fieldMusic)

		if fileName==uiSelectMusic.DEFAULT_THEMA:
			musicInfo.fieldMusic=musicInfo.METIN2THEMA
		else:
			musicInfo.fieldMusic=fileName

		musicInfo.SaveLastPlayFieldMusic()

		if musicInfo.fieldMusic != "":
			snd.FadeInMusic("BGM/" + musicInfo.fieldMusic)

	def __OnClickChangeMusicButton(self):
		if not self.musicListDlg:

			self.musicListDlg=uiSelectMusic.FileListDialog()
			self.musicListDlg.SAFE_SetSelectEvent(self.__OnChangeMusic)

		self.musicListDlg.Open()

	def OnChangeMusicVolume(self):
		pos = self.ctrlMusicVolume.GetSliderPos()
		snd.SetMusicVolume(pos * net.GetFieldMusicVolume())
		systemSetting.SetMusicVolume(pos)

	def OnChangeSoundVolume(self):
		pos = self.ctrlSoundVolume.GetSliderPos()
		snd.SetSoundVolumef(pos)
		systemSetting.SetSoundVolumef(pos)

	if app.ENABLE_VOICE_CHAT:
		def __GetVoiceDeviceName(self, getCount, getName, index):
			count = getCount()
			if count <= 0:
				return localeInfo.VOICE_CHAT_NO_DEVICE
			index = index % count
			name = getName(index)
			if not name:
				return localeInfo.VOICE_CHAT_NO_DEVICE
			return name[:VOICE_DEVICE_NAME_MAX_LEN]

		def __BuildVoiceDeviceList(self, getCount, getName):
			names = []
			count = getCount()
			for i in range(count):
				name = getName(i)
				if not name:
					name = localeInfo.VOICE_CHAT_NO_DEVICE
				names.append(name)
			return names

		def __OpenVoiceDeviceDropDown(self, triggerButton, names, onSelect):
			if not self.vc_device_dropdown:
				return
			if len(names) <= 0:
				return
			self.vc_device_dropdown.SetItems(names)
			self.vc_device_dropdown.SetEvent(onSelect)
			x, y = triggerButton.GetGlobalPosition()
			self.vc_device_dropdown.OpenAt(x, y + triggerButton.GetHeight())

		def __OnClickVoiceMicDevice(self):
			names = self.__BuildVoiceDeviceList(app.VoiceChatGetCaptureDeviceCount, app.VoiceChatGetCaptureDeviceName)
			self.__OpenVoiceDeviceDropDown(self.vc_mic_device, names, ui.__mem_func__(self.__OnSelectVoiceMicDevice))

		def __OnSelectVoiceMicDevice(self, index):
			count = app.VoiceChatGetCaptureDeviceCount()
			if count <= 0:
				return
			self.vc_mic_device_index = index % count
			app.VoiceChatSetCaptureDevice(self.vc_mic_device_index)
			constInfo.SetVoiceChatConfig("VOICE_CHAT_MIC_DEVICE", self.vc_mic_device_index)
			constInfo.SaveVoiceChatConfig()
			self.vc_mic_device_text.SetText(self.__GetVoiceDeviceName(app.VoiceChatGetCaptureDeviceCount, app.VoiceChatGetCaptureDeviceName, self.vc_mic_device_index))

		def __OnClickVoiceSpkDevice(self):
			names = self.__BuildVoiceDeviceList(app.VoiceChatGetPlaybackDeviceCount, app.VoiceChatGetPlaybackDeviceName)
			self.__OpenVoiceDeviceDropDown(self.vc_spk_device, names, ui.__mem_func__(self.__OnSelectVoiceSpkDevice))

		def __OnSelectVoiceSpkDevice(self, index):
			count = app.VoiceChatGetPlaybackDeviceCount()
			if count <= 0:
				return
			self.vc_spk_device_index = index % count
			app.VoiceChatSetPlaybackDevice(self.vc_spk_device_index)
			constInfo.SetVoiceChatConfig("VOICE_CHAT_SPK_DEVICE", self.vc_spk_device_index)
			constInfo.SaveVoiceChatConfig()
			self.vc_spk_device_text.SetText(self.__GetVoiceDeviceName(app.VoiceChatGetPlaybackDeviceCount, app.VoiceChatGetPlaybackDeviceName, self.vc_spk_device_index))

		def __OnChangeVoiceMicVolume(self):
			pos = self.vc_mic_volume.GetSliderPos()
			app.VoiceChatSetMicVolume(pos)
			constInfo.SetVoiceChatVolume("VOICE_MIC_VOLUME", pos)
			constInfo.SaveVoiceChatConfig()

		def __OnChangeVoiceHearVolume(self):
			pos = self.vc_hear_volume.GetSliderPos()
			app.VoiceChatSetVolume(pos)
			constInfo.SetVoiceChatVolume("VOICE_PLAYBACK_VOLUME", pos)
			constInfo.SaveVoiceChatConfig()

		def __OnClickVoiceEnableOn(self):
			app.VoiceChatSetDisabled(0)
			constInfo.SetVoiceChatConfig("VOICE_CHAT_DISABLED", 0)
			constInfo.SaveVoiceChatConfig()
			self.__RefreshVoiceEnable()
			# #6: wlaczono z powrotem na zakladce voice -> wznow podglad mikrofonu.
			if self.voicechat_window and self.voicechat_window.IsShow():
				app.VoiceChatStartMicMonitor()

		def __OnClickVoiceEnableOff(self):
			app.VoiceChatSetDisabled(1)
			constInfo.SetVoiceChatConfig("VOICE_CHAT_DISABLED", 1)
			constInfo.SaveVoiceChatConfig()
			self.__RefreshVoiceEnable()
			# #6: wylaczono -> SetDisabled zatrzymalo capture i wyzerowalo poziom.
			if self.vc_mic_meter:
				self.vc_mic_meter.SetPercentage(0, 100)

		def __RefreshVoiceEnable(self):
			if constInfo.GetVoiceChatConfig("VOICE_CHAT_DISABLED") == 1:
				self.vc_enable_off.Down()
				self.vc_enable_on.SetUp()
			else:
				self.vc_enable_on.Down()
				self.vc_enable_off.SetUp()

		def __SetVoiceChatType(self, vtype):
			app.VoiceChatSetChatType(vtype)
			constInfo.SetVoiceChatConfig("VOICE_CHAT_TYPE", vtype)
			constInfo.SaveVoiceChatConfig()
			self.__RefreshVoiceChatType()

		def __OnClickVoiceTypeLocal(self):
			self.__SetVoiceChatType(app.VOICE_CHAT_TYPE_LOCAL)

		def __OnClickVoiceTypeParty(self):
			self.__SetVoiceChatType(app.VOICE_CHAT_TYPE_PARTY)

		def __OnClickVoiceTypeGuild(self):
			self.__SetVoiceChatType(app.VOICE_CHAT_TYPE_GUILD)

		def __RefreshVoiceChatType(self):
			vtype = constInfo.GetVoiceChatConfig("VOICE_CHAT_TYPE")
			if vtype < app.VOICE_CHAT_TYPE_LOCAL or vtype >= app.VOICE_CHAT_TYPE_MAX_NUM:
				vtype = app.VOICE_CHAT_TYPE_LOCAL
			self.vc_type_local.SetUp()
			self.vc_type_party.SetUp()
			self.vc_type_guild.SetUp()
			if vtype == app.VOICE_CHAT_TYPE_PARTY:
				self.vc_type_party.Down()
			elif vtype == app.VOICE_CHAT_TYPE_GUILD:
				self.vc_type_guild.Down()
			else:
				self.vc_type_local.Down()

		def __OnClickVoicePTTKey(self):
			# Enter capture mode: next key press (routed from game.OnKeyDown) becomes
			# the new PTT key. Rejestrujemy TE instancje jako cel (jest kilka instancji
			# OptionDialog - game.py musi oddac klawisz tej widocznej, nie hardcoded).
			self.vc_ptt_capture = True
			constInfo.SetVoicePTTCaptureMode(True, self)
			self.vc_ptt_key_text.SetText(localeInfo.VOICE_CHAT_PRESS_KEY)

		def OnVoicePTTKeyCapture(self, key):
			# Called by game.OnKeyDown when capture mode is active. ESC cancels.
			# Zrodlo prawdy = globalna flaga constInfo (member self.vc_ptt_capture bywa
			# resetowany niezaleznie - np. __Initialize/odswiezenie - a globalna flaga
			# jest spojna z intercept w game.OnKeyDown).
			if not constInfo.IsVoicePTTCaptureMode():
				return False
			self.vc_ptt_capture = False
			constInfo.SetVoicePTTCaptureMode(False)
			if key != app.DIK_ESC:
				constInfo.SetVoiceChatConfig("VOICE_CHAT_PTT_KEY", int(key))
				constInfo.SaveVoiceChatConfig()
			self.__RefreshVoicePTTKey()
			return True

		def __CancelVoicePTTCapture(self):
			if self.vc_ptt_capture:
				self.vc_ptt_capture = False
				constInfo.SetVoicePTTCaptureMode(False)
				self.__RefreshVoicePTTKey()

		def __RefreshVoicePTTKey(self):
			key = constInfo.GetVoiceChatPTTKey()
			self.vc_ptt_key_text.SetText(VoiceGetDIKName(key))

		def __RefreshVoiceChat(self):
			self.vc_mic_device_index = constInfo.GetVoiceChatConfig("VOICE_CHAT_MIC_DEVICE")
			self.vc_spk_device_index = constInfo.GetVoiceChatConfig("VOICE_CHAT_SPK_DEVICE")
			self.vc_mic_device_text.SetText(self.__GetVoiceDeviceName(app.VoiceChatGetCaptureDeviceCount, app.VoiceChatGetCaptureDeviceName, self.vc_mic_device_index))
			self.vc_spk_device_text.SetText(self.__GetVoiceDeviceName(app.VoiceChatGetPlaybackDeviceCount, app.VoiceChatGetPlaybackDeviceName, self.vc_spk_device_index))
			micPos = float(constInfo.GetVoiceChatVolume("VOICE_MIC_VOLUME"))
			hearPos = float(constInfo.GetVoiceChatVolume("VOICE_PLAYBACK_VOLUME"))
			self.vc_mic_volume.SetSliderPos(micPos)
			self.vc_hear_volume.SetSliderPos(hearPos)
			# SetSliderPos NIE odpala eventu -> aplikuj glosnosci jawnie (inaczej gain
			# zostaje unity dopoki nie ruszysz suwaka -> mikrofon za cichy).
			app.VoiceChatSetMicVolume(micPos)
			app.VoiceChatSetVolume(hearPos)
			self.__RefreshVoiceEnable()
			self.__RefreshVoiceChatType()
			self.__RefreshVoicePTTKey()
