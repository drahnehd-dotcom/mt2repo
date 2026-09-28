#-*- coding: iso-8859-1 -*-
import os
import app
import dbg
import grp
import item
import background
import chr
import chrmgr
import player
import snd
import chat
import textTail
import snd
import net
import wndMgr
import acce
import systemSetting
import quest
import guild
import skill
import messenger
import localeInfo
import constInfo
import settings
import exchange
import ime

import ui
import uiCommon
import uiPhaseCurtain
import uiMapNameShower
import uiAffectShower
import uiPlayerGauge
import uiCharacter
import uiTarget
import uiMount
import uiPrivateShopBuilder

import mouseModule
import consoleModule
import localeInfo
import interfaceModule
if app.ENABLE_SKILL_SELECT_FEATURE:
	import uiskillchoose
if app.ENABLE_OFFLINE_SHOP:
    import uiOfflineShop, offlineshop
if app.ENABLE_NEW_PET_SYSTEM:
	import pet

import musicInfo
import debugInfo
import stringCommander

# DIAGNOSTYKA SCINEK: flaga instalacji sondy garbage collectora (patrz __InstallGcProbe)
_gcProbeInstalled = False
if app.ENABLE_KEYCHANGE_SYSTEM:
	import uiKeyChange
if app.ENABLE_OFFLINE_SHOP_SYSTEM:
	import uiOfflineShopBuilder
	import uiOfflineShop

if hasattr(app, "ENABLE_PREMIUM_PRIVATE_SHOP_OFFICIAL") and app.ENABLE_PREMIUM_PRIVATE_SHOP_OFFICIAL:
	import uiPrivateShop

import uiCube
import uisecurity
import uiRanking
import uiEnlightenment
import uiFishWiki

from _weakref import proxy

SCREENSHOT_CWDSAVE = True
SCREENSHOT_DIR = None

cameraDistance = 1550.0
cameraPitch = 27.0
cameraRotation = 0.0
cameraHeight = 100.0

testAlignment = 0

class GameWindow(ui.ScriptWindow):
	def __init__(self, stream):
		ui.ScriptWindow.__init__(self, "GAME")
		self.SetWindowName("game")
		net.SetPhaseWindow(net.PHASE_WINDOW_GAME, self)
		player.SetGameWindow(self)

		# Limit FPS z ustawien gracza. Do tej pory klient byl na sztywno zablokowany na 60
		# (CTimer liczyl krok jako "16 + (m_index & 1)", a app.SetFPS bylo martwe).
		try:
			import settings
			app.SetFPS(int(settings.get("fps_limit", 60)))
		except Exception as e:
			dbg.TraceError("SetFPS from settings failed: %s" % str(e))

		# DIAGNOSTYKA SCINEK: garbage collector Pythona zatrzymuje caly watek glowny.
		# Przy dziesiatkach tysiecy obiektow UI zbiorka pokolenia 2 potrafi trwac
		# kilkadziesiat ms - to jeden z glownych podejrzanych o scinki "bez ladowania".
		# app.HitchNote wrzuca pauze do tej samej listy zdarzen klatki co ladowania z C++,
		# wiec wyladuje w hitch_log.txt. Bez ENABLE_TRACY HitchNote jest pusta.
		self.__InstallGcProbe()

		self.quickSlotPageIndex = 0
		self.lastPKModeSendedTime = 0
		self.pressNumber = None

		if app.ENABLE_BOT_CONTROL:
			self.botControlWnd = None

		if app.ENABLE_SKILL_SELECT_FEATURE:
			self.skillSelect = None

		self.guildWarQuestionDialog = None
		self.interface = None
		self.targetBoard = None
		self.console = None
		self.mapNameShower = None
		self.affectShower = None
		self.playerGauge = None
		if app.ENABLE_KEYCHANGE_SYSTEM:
			self.wndKeyChange = None

		if app.ENABLE_AUTO_SHOUT:
			self.lastShoutTime = 0

		self.stream=stream
		self.interface = interfaceModule.Interface()
		if app.ENABLE_EVENT_MANAGER:
			constInfo.SetInterfaceInstance(self.interface)
		interfaceModule.SetInstance(self.interface)
		self.interface.MakeInterface()
		self.interface.ShowDefaultWindows()
		constInfo.SetInterfaceInstance(self.interface)

		if app.ENABLE_NEW_PET_SYSTEM:
			pet.SendRequestInfo()
			self.__petRetryTime = app.GetTime() + 3.0

		self.curtain = uiPhaseCurtain.PhaseCurtain()
		self.curtain.speed = 0.03
		self.curtain.Hide()

		self.targetBoard = uiTarget.TargetBoard()
		self.targetBoard.SetWhisperEvent(ui.__mem_func__(self.interface.OpenWhisperDialog))
		self.targetBoard.Hide()

		if app.ENABLE_OFFLINE_SHOP:
			offlineshop.HideShopNames()

		if app.ENABLE_SKILL_SELECT_FEATURE:
			self.skillSelect = uiskillchoose.SkillSelectWindow()
			self.skillSelect.Hide()

		self.console = consoleModule.ConsoleWindow()
		self.console.BindGameClass(self)
		self.console.SetConsoleSize(wndMgr.GetScreenWidth(), 200)
		self.console.Hide()

		self.mapNameShower = uiMapNameShower.MapNameShower()
		self.affectShower = uiAffectShower.AffectShower()
		self.enlightWindow = None
		
		self.rankingWindow = uiRanking.RankingWindow()
		self.weeklyRankingWindow = uiRanking.WeeklyRankingWindow()
		self.fishWikiWindow = uiFishWiki.FishingWikipediaWindow()


		self.playerGauge = uiPlayerGauge.PlayerGauge(self)
		self.playerGauge.Hide()
		
		self.itemDropQuestionDialog = None

		self.__SetQuickSlotMode()

		if app.ENABLE_SKYBOX_SELECT:
			self.interface.wndgameOption.RefreshSkyBoxButtons()

		self.__ServerCommand_Build()
		self.__ProcessPreservedServerCommand()
		if app.ENABLE_KEYCHANGE_SYSTEM:
			self.wndKeyChange = uiKeyChange.KeyChangeWindow(self, self.interface)
			self.ADDKEYBUFFERCONTROL = player.KEY_ADDKEYBUFFERCONTROL
			self.ADDKEYBUFFERALT = player.KEY_ADDKEYBUFFERALT
			self.ADDKEYBUFFERSHIFT = player.KEY_ADDKEYBUFFERSHIFT

	def __del__(self):
		player.SetGameWindow(0)
		net.ClearPhaseWindow(net.PHASE_WINDOW_GAME, self)
		ui.ScriptWindow.__del__(self)

	def Open(self):
		app.TracyMsg("GameWindow.Open START")
		app.SetFrameSkip(1)

		self.SetSize(wndMgr.GetScreenWidth(), wndMgr.GetScreenHeight())

		self.quickSlotPageIndex = 0
		self.PickingCharacterIndex = -1
		self.PickingItemIndex = -1
		self.consoleEnable = True
		self.isShowDebugInfo = False
		self.ShowNameFlag = False

		self.enableXMasBoom = False
		self.startTimeXMasBoom = 0.0
		self.indexXMasBoom = 0

		global cameraDistance, cameraPitch, cameraRotation, cameraHeight

		app.SetCamera(cameraDistance, cameraPitch, cameraRotation, cameraHeight)

		constInfo.SET_DEFAULT_CAMERA_MAX_DISTANCE()
		constInfo.SET_DEFAULT_CHRNAME_COLOR()
		constInfo.SET_DEFAULT_FOG_LEVEL()
		constInfo.SET_DEFAULT_CONVERT_EMPIRE_LANGUAGE_ENABLE()
		constInfo.SET_DEFAULT_USE_ITEM_WEAPON_TABLE_ATTACK_BONUS()
		constInfo.SET_DEFAULT_USE_SKILL_EFFECT_ENABLE()

		constInfo.SET_TWO_HANDED_WEAPON_ATT_SPEED_DECREASE_VALUE()

		app.TracyMsg("GameWindow.Open: const setup done")

		import event
		event.SetLeftTimeString(localeInfo.UI_LEFT_TIME)

		textTail.EnablePKTitle(constInfo.PVPMODE_ENABLE)

		try:
			import dungeonInfo
			dungeonInfo.Open()
		except:
			pass

		if constInfo.PVPMODE_TEST_ENABLE:
			self.testPKMode = ui.TextLine()
			self.testPKMode.SetFontName(localeInfo.UI_DEF_FONT)
			self.testPKMode.SetPosition(0, 15)
			self.testPKMode.SetWindowHorizontalAlignCenter()
			self.testPKMode.SetHorizontalAlignCenter()
			self.testPKMode.SetFeather()
			self.testPKMode.SetOutline()
			self.testPKMode.Show()

			self.testAlignment = ui.TextLine()
			self.testAlignment.SetFontName(localeInfo.UI_DEF_FONT)
			self.testAlignment.SetPosition(0, 35)
			self.testAlignment.SetWindowHorizontalAlignCenter()
			self.testAlignment.SetHorizontalAlignCenter()
			self.testAlignment.SetFeather()
			self.testAlignment.SetOutline()
			self.testAlignment.Show()

		if app.ENABLE_KEYCHANGE_SYSTEM:
			pass
		else:
			self.__BuildKeyDict()
		self.__BuildDebugInfo()

		constInfo.IS_BONUS_CHANGER = False
		constInfo.IS_ACCE_WINDOW = False
		constInfo.IS_DRAGON_SOUL_OPEN = False

		app.TracyMsg("GameWindow.Open: dungeon+keydict done")

		uiPrivateShopBuilder.Clear()
		if app.ENABLE_OFFLINE_SHOP_SYSTEM:
			uiOfflineShopBuilder.Clear()

		exchange.InitTrading()

		app.TracyMsg("GameWindow.Open: shop+exchange done")

		if len(constInfo.lastSentenceStack) > 0:
			constInfo.lastSentencePos = 0

		app.TracyMsg("GameWindow.Open: music start")
		snd.SetMusicVolume(systemSetting.GetMusicVolume()*net.GetFieldMusicVolume())
		snd.SetSoundVolumef(systemSetting.GetSoundVolumef())

		netFieldMusicFileName = net.GetFieldMusicFileName()
		if netFieldMusicFileName:
			snd.FadeInMusic("BGM/" + netFieldMusicFileName)
		elif musicInfo.fieldMusic != "":
			snd.FadeInMusic("BGM/" + musicInfo.fieldMusic)
		app.TracyMsg("GameWindow.Open: music done")

		self.__SetQuickSlotMode()
		self.__SelectQuickPage(self.quickSlotPageIndex)

		self.SetFocus()
		self.Show()
		app.ShowCursor()

		app.TracyMsg("GameWindow.Open: pre-SendEnterGame")
		net.SendEnterGamePacket()
		app.TracyMsg("GameWindow.Open: post-SendEnterGame")

		# Jezyk klienta dla serwera - flaga kraju zamiast [Shinsoo]/[Jinno] przy wolaniu.
		# Serwer trzyma go tylko w pamieci, wiec wysylamy przy kazdym wejsciu (takze po warpie).
		try:
			net.SendChatPacket("/client_lang " + app.GetLocaleName())
		except:
			pass

		try:
			self.StartGame()
		except:
			import exception
			exception.Abort("GameWindow.Open")
		app.TracyMsg("GameWindow.Open END")

		if app.ENABLE_AUTO_SHOUT:
			self.lastShoutTime = app.GetTime() + constInfo.SHOUT_PER_SECOND

	def __SafeInterfaceCall(self, window_name, method_name):
		try:
			if self.interface:
				window = getattr(self.interface, window_name, None)
				if window:
					method = getattr(window, method_name, None)
					if method:
						method()
		except:
			pass

	def __OpenCompanionMount(self):
		try:
			if self.interface:
				wnd = getattr(self.interface, 'wndCompanionWindow', None)
				if wnd:
					if wnd.IsShow():
						wnd.SwitchToMountMode()
					else:
						wnd.Open()
						wnd.SwitchToMountMode()
				elif hasattr(self.interface, 'wndMountWindow') and self.interface.wndMountWindow:
					self.interface.wndMountWindow.Open()
		except:
			pass

	def __SafeInterfaceCallMethod(self, method_name):
		try:
			if self.interface:
				method = getattr(self.interface, method_name, None)
				if method:
					method()
		except:
			pass

	# ===== Voice Chat (Opus) — voice-chat/CHANGES_ZARIS.md (Etap 5) =====
	if app.ENABLE_VOICE_CHAT:
		def BINARY_OnVoice(self, name, vcType = 0):
			if self.interface:
				if self.interface.wndVoiceChatConfig:
					self.interface.wndVoiceChatConfig.OnMessage(name, vcType)
				if self.interface.wndVoiceChatOverlay:
					self.interface.wndVoiceChatOverlay.OnMessage(name, vcType)

		def BINARY_ReloadVoiceChatVolumes(self):
			constInfo.SendVoiceChatVolumes()
			# Aplikuj glosnosc mikrofonu + sluchania przy starcie gry (nie tylko przy
			# otwarciu opcji) - inaczej mic gain zostaje unity i mikrofon jest za cichy.
			app.VoiceChatSetMicVolume(constInfo.GetVoiceChatVolume("VOICE_MIC_VOLUME"))
			app.VoiceChatSetVolume(constInfo.GetVoiceChatVolume("VOICE_PLAYBACK_VOLUME"))
			# Aplikuj zapisane urzadzenie nagrywajace/odtwarzajace - domyslny endpoint
			# miniaudio (nullptr) bywa cichy (WASAPI), trzeba otworzyc jawny.
			constInfo.ApplyVoiceChatDevices()
			# #7: re-aplikuj zapisana liste wyciszonych mowcow (C++ czysci ja przy
			# wyjsciu z gry).
			constInfo.ApplyVoiceChatMutes()
			# Aplikuj zapisany stan wlaczenia/wylaczenia voice (radio w opcjach zapisuje
			# tylko config; bez tego po relogu wylaczenie nie przetrwa -> ikonki+dzwiek
			# wracaja mimo OFF w opcjach).
			app.VoiceChatSetDisabled(constInfo.GetVoiceChatConfig("VOICE_CHAT_DISABLED"))
			# Aplikuj zapisany kanal glosowy (Lokalny/Druzyna/Gildia). Default/niepoprawny
			# -> LOCAL. Bez tego po relogu kanal wraca do domyslnego z C++ (LOCAL).
			vt = constInfo.GetVoiceChatConfig("VOICE_CHAT_TYPE")
			if vt < app.VOICE_CHAT_TYPE_LOCAL or vt >= app.VOICE_CHAT_TYPE_MAX_NUM:
				vt = app.VOICE_CHAT_TYPE_LOCAL
			app.VoiceChatSetChatType(vt)

		def OnStartTalking(self):
			# Y = push-to-talk. Ustawienia (urzadzenia, glosnosc, on/off) sa w
			# oknie opcji gry -> zakladka Czat glosowy. Y tylko nadaje.
			app.VoiceChatStartTalking()

		def OnStopTalking(self):
			app.VoiceChatStopTalking()

		def __DisableVoiceChat(self, disabled):
			disabled = int(disabled)
			app.VoiceChatSetDisabled(disabled)

		def __ConfigVoiceChat(self, arg):
			# Stare okno wycofane (ustawienia w opcjach gry). NIE wolno tu wolac
			# OnReceiveConfig/SetRecorderState - resetowalo recorder do OFF przy
			# wejsciu (serwer wysyla voice_chat_config) i psulo push-to-talk (Y).
			# Per-type block (Party/Guild) nieuzywany - LOCAL only + on/off w opcjach.
			pass

		def __VoiceChatLevelRequired(self, level):
			# Lokalizacja per-język po stronie klienta (serwer wysyła tylko poziom).
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.VOICE_CHAT_LEVEL_REQUIRED % int(level))

	def Close(self):
		self.Hide()

		if app.ENABLE_VOICE_CHAT:
			constInfo.SaveVoiceChatConfig()

		global cameraDistance, cameraPitch, cameraRotation, cameraHeight
		(cameraDistance, cameraPitch, cameraRotation, cameraHeight) = app.GetCamera()

		if musicInfo.fieldMusic != "":
			snd.FadeOutMusic("BGM/"+ musicInfo.fieldMusic)

		self.onPressKeyDict = None
		self.onClickKeyDict = None

		chat.Close()
		snd.StopAllSound()
		grp.InitScreenEffect()
		chr.Destroy()
		textTail.Clear()
		quest.Clear()
		background.Destroy()
		guild.Destroy()
		messenger.Destroy()
		if app.ENABLE_SKILL_SELECT_FEATURE and self.skillSelect:
			self.skillSelect.Destroy()
			self.skillSelect = None
		skill.ClearSkillData()
		wndMgr.Unlock()
		mouseModule.mouseController.DeattachObject()

		if self.guildWarQuestionDialog:
			self.guildWarQuestionDialog.Close()

		self.guildNameBoard = None
		self.partyRequestQuestionDialog = None
		self.partyInviteQuestionDialog = None
		self.guildInviteQuestionDialog = None
		self.guildWarQuestionDialog = None
		self.messengerAddFriendQuestion = None

		if app.ENABLE_BOT_CONTROL:
			if self.botControlWnd:
				self.botControlWnd.Destroy()
				self.botControlWnd = None

		self.itemDropQuestionDialog = None

		self.confirmDialog = None

		self.PrintCoord = None
		self.FrameRate = None
		self.Pitch = None
		self.Splat = None
		self.TextureNum = None
		self.ObjectNum = None
		self.ViewDistance = None
		self.PrintMousePos = None

		self.ClearDictionary()

		self.playerGauge = None
		self.mapNameShower = None
		self.affectShower = None

		if self.console:
			self.console.BindGameClass(0)
			self.console.Close()
			self.console=None

		if self.targetBoard:
			self.targetBoard.Destroy()
			self.targetBoard = None
		
		if self.interface:
			self.interface.HideAllWindows()
			self.interface.Close()
			self.interface=None

		if self.fishWikiWindow:
			self.fishWikiWindow.Close()
			self.fishWikiWindow = None
			
		if self.rankingWindow:
			self.rankingWindow.Close()
			self.rankingWindow = None

		if self.enlightWindow != None:
			self.enlightWindow.Close()
			self.enlightWindow = None

		if self.weeklyRankingWindow:
			self.weeklyRankingWindow.Close()
			self.weeklyRankingWindow = None
			
		interfaceModule.SetInstance(None)

		player.ClearSkillDict()
		player.ResetCameraRotation()

		self.KillFocus()
		if app.ENABLE_EVENT_MANAGER:
			constInfo.SetInterfaceInstance(None)
		constInfo.SetInterfaceInstance(None)
		app.HideCursor()
		if app.ENABLE_KEYCHANGE_SYSTEM:
			if self.wndKeyChange:
				self.wndKeyChange.KeyChangeWindowClose(True)
				self.wndKeyChange = None

		print("---------------------------------------------------------------------------- CLOSE GAME WINDOW"
)

	def __PetKeyOrRemovePolymorph(self):
		# Ctrl+P: TYLKO dialog wylaczenia polimorfii (gdy spolimorfowany).
		# Otwieranie okna peta pod tym klawiszem calkowicie wylaczone.
		if self.affectShower:
			self.affectShower.TryOpenPolymorphRemove()

	def __BuildKeyDict(self):
		onPressKeyDict = {}


		onPressKeyDict[app.DIK_1]	= lambda : self.__PressNumKey(1)
		onPressKeyDict[app.DIK_2]	= lambda : self.__PressNumKey(2)
		onPressKeyDict[app.DIK_3]	= lambda : self.__PressNumKey(3)
		onPressKeyDict[app.DIK_4]	= lambda : self.__PressNumKey(4)
		onPressKeyDict[app.DIK_5]	= lambda : self.__PressNumKey(5)
		onPressKeyDict[app.DIK_6]	= lambda : self.__PressNumKey(6)
		onPressKeyDict[app.DIK_7]	= lambda : self.__PressNumKey(7)
		onPressKeyDict[app.DIK_8]	= lambda : self.__PressNumKey(8)
		onPressKeyDict[app.DIK_9]	= lambda : self.__PressNumKey(9)
		onPressKeyDict[app.DIK_F1]	= lambda : self.__PressQuickSlot(4)
		onPressKeyDict[app.DIK_F2]	= lambda : self.__PressQuickSlot(5)
		onPressKeyDict[app.DIK_F3]	= lambda : self.__PressQuickSlot(6)
		onPressKeyDict[app.DIK_F4]	= lambda : self.__PressQuickSlot(7)
		onPressKeyDict[app.DIK_F5]	= lambda : self.__SafeInterfaceCall('wndBoosters', 'btnUse')
		# F6 tymczasowo wylaczone (otwieralo panel auto-hunt/switchbot) — narazie ma nie otwierac nic
		#onPressKeyDict[app.DIK_F6]	= lambda : self.__SafeInterfaceCallMethod('ToggleSwitchbotWindow')
		onPressKeyDict[app.DIK_F7]	= lambda : self.__SafeInterfaceCallMethod('ToggleSaveLocationWindow')
		# F8 wylaczone — system "Teleportacja do Wladcow/Metinow" nieaktywny (client-side)
		#onPressKeyDict[app.DIK_F8]	= lambda : self.__SafeInterfaceCallMethod('OpenRespWindow')
		if app.ENABLE_OFFLINE_SHOP:
			onPressKeyDict[app.DIK_F9]		= lambda : self.OpenShopSearch()
		onPressKeyDict[app.DIK_RETURN]	= lambda : self.ChangeBonus()

		onPressKeyDict[app.DIK_F11]	= lambda : self.__SafeInterfaceCallMethod('ToggleCollectWindow')

		if app.ENABLE_NEW_PET_SYSTEM:
			onPressKeyDict[app.DIK_P]	= lambda : self.__PetKeyOrRemovePolymorph()
		if app.WJ_SPLIT_INVENTORY_SYSTEM:
			onPressKeyDict[app.DIK_U]		= lambda : self.__PressExtendedInventory()
			

		onPressKeyDict[app.DIK_TAB]			= lambda : 		self.ToggleMapWindow()

		onPressKeyDict[app.DIK_LALT]		= lambda : self.ShowName()
		onPressKeyDict[app.DIK_LCONTROL]	= lambda : self.ShowMouseImage()
		onPressKeyDict[app.DIK_SPACE]		= lambda : self.StartAttack()

		onPressKeyDict[app.DIK_UP]			= lambda : self.MoveUp()
		onPressKeyDict[app.DIK_DOWN]		= lambda : self.MoveDown()
		onPressKeyDict[app.DIK_LEFT]		= lambda : self.MoveLeft()
		onPressKeyDict[app.DIK_RIGHT]		= lambda : self.MoveRight()
		onPressKeyDict[app.DIK_W]			= lambda : self.MoveUp()
		onPressKeyDict[app.DIK_S]			= lambda : self.MoveDown()
		onPressKeyDict[app.DIK_A]			= lambda : self.MoveLeft()
		onPressKeyDict[app.DIK_D]			= lambda : self.MoveRight()

		onPressKeyDict[app.DIK_E]			= lambda: app.RotateCamera(app.CAMERA_TO_POSITIVE)
		onPressKeyDict[app.DIK_R]			= lambda: app.ZoomCamera(app.CAMERA_TO_NEGATIVE)
		onPressKeyDict[app.DIK_T]			= lambda: app.PitchCamera(app.CAMERA_TO_NEGATIVE)
		onPressKeyDict[app.DIK_G]			= self.__PressGKey
		onPressKeyDict[app.DIK_Q]			= self.__PressQKey

		onPressKeyDict[app.DIK_NUMPAD9]		= lambda: app.MovieResetCamera()
		onPressKeyDict[app.DIK_NUMPAD4]		= lambda: app.MovieRotateCamera(app.CAMERA_TO_NEGATIVE)
		onPressKeyDict[app.DIK_NUMPAD6]		= lambda: app.MovieRotateCamera(app.CAMERA_TO_POSITIVE)
		onPressKeyDict[app.DIK_PGUP]		= lambda: app.MovieZoomCamera(app.CAMERA_TO_NEGATIVE)
		onPressKeyDict[app.DIK_PGDN]		= lambda: app.MovieZoomCamera(app.CAMERA_TO_POSITIVE)
		onPressKeyDict[app.DIK_NUMPAD8]		= lambda: app.MoviePitchCamera(app.CAMERA_TO_NEGATIVE)
		onPressKeyDict[app.DIK_NUMPAD2]		= lambda: app.MoviePitchCamera(app.CAMERA_TO_POSITIVE)
		onPressKeyDict[app.DIK_GRAVE]		= lambda : self.PickUpItem()
		onPressKeyDict[app.DIK_Z]			= lambda : self.PickUpItem()
		onPressKeyDict[app.DIK_C]			= lambda state = "STATUS": self.__SafeInterfaceCallMethod('ToggleCharacterWindow')
		onPressKeyDict[app.DIK_V]			= lambda state = "SKILL": self.__SafeInterfaceCallMethod('ToggleCharacterWindow')
		onPressKeyDict[app.DIK_N]			= lambda state = "QUEST": self.__SafeInterfaceCallMethod('ToggleCharacterWindow')
		onPressKeyDict[app.DIK_I]			= lambda : self.__SafeInterfaceCallMethod('ToggleInventoryWindow')
		onPressKeyDict[app.DIK_O]			= lambda : self.__SafeInterfaceCallMethod('ToggleDragonSoulWindow')
		if hasattr(app, "ENABLE_PREMIUM_PRIVATE_SHOP_OFFICIAL") and app.ENABLE_PREMIUM_PRIVATE_SHOP_OFFICIAL:
			onPressKeyDict[app.DIK_U]			= lambda : self.interface.TogglePrivateShopPanelWindowCheck()
		onPressKeyDict[app.DIK_M]			= lambda : self.__SafeInterfaceCallMethod('PressMKey')
		onPressKeyDict[app.DIK_ADD]			= lambda : self.__SafeInterfaceCallMethod('MiniMapScaleUp')
		onPressKeyDict[app.DIK_SUBTRACT]	= lambda : self.__SafeInterfaceCallMethod('MiniMapScaleDown')
		onPressKeyDict[app.DIK_L]			= lambda : self.__SafeInterfaceCallMethod('ToggleChatLogWindow')
		onPressKeyDict[app.DIK_COMMA]		= lambda : self.ShowConsole()
		onPressKeyDict[app.DIK_F10]		= lambda : self.ShowConsole()
		onPressKeyDict[app.DIK_LSHIFT]		= lambda : self.__SetQuickPageMode()
		onPressKeyDict[app.DIK_J]			= lambda : self.__PressJKey()
		onPressKeyDict[app.DIK_H]			= lambda : self.__PressHKey()
		onPressKeyDict[app.DIK_B]			= lambda : self.__PressBKey()
		onPressKeyDict[app.DIK_F]			= lambda : self.__PressFKey()

		# Voice Chat push-to-talk: klawisz konfigurowalny w opcjach gry (zakladka
		# Czat glosowy). Obsluga w OnKeyDown/OnKeyUp (czyta constInfo.GetVoiceChatPTTKey),
		# wiec NIE rejestrujemy go w onPressKeyDict/onClickKeyDict (byloby na sztywno Y).


		self.onPressKeyDict = onPressKeyDict

		onClickKeyDict = {}
		onClickKeyDict[app.DIK_UP] = lambda : self.StopUp()
		onClickKeyDict[app.DIK_DOWN] = lambda : self.StopDown()
		onClickKeyDict[app.DIK_LEFT] = lambda : self.StopLeft()
		onClickKeyDict[app.DIK_RIGHT] = lambda : self.StopRight()
		onClickKeyDict[app.DIK_SPACE] = lambda : self.EndAttack()

		onClickKeyDict[app.DIK_W] = lambda : self.StopUp()
		onClickKeyDict[app.DIK_S] = lambda : self.StopDown()
		onClickKeyDict[app.DIK_A] = lambda : self.StopLeft()
		onClickKeyDict[app.DIK_D] = lambda : self.StopRight()
		onClickKeyDict[app.DIK_Q] = lambda: app.RotateCamera(app.CAMERA_STOP)
		onClickKeyDict[app.DIK_E] = lambda: app.RotateCamera(app.CAMERA_STOP)
		onClickKeyDict[app.DIK_R] = lambda: app.ZoomCamera(app.CAMERA_STOP)
		onClickKeyDict[app.DIK_F] = lambda: app.ZoomCamera(app.CAMERA_STOP)
		onClickKeyDict[app.DIK_T] = lambda: app.PitchCamera(app.CAMERA_STOP)
		onClickKeyDict[app.DIK_G] = lambda: self.__ReleaseGKey()
		onClickKeyDict[app.DIK_NUMPAD4] = lambda: app.MovieRotateCamera(app.CAMERA_STOP)
		onClickKeyDict[app.DIK_NUMPAD6] = lambda: app.MovieRotateCamera(app.CAMERA_STOP)
		onClickKeyDict[app.DIK_PGUP] = lambda: app.MovieZoomCamera(app.CAMERA_STOP)
		onClickKeyDict[app.DIK_PGDN] = lambda: app.MovieZoomCamera(app.CAMERA_STOP)
		onClickKeyDict[app.DIK_NUMPAD8] = lambda: app.MoviePitchCamera(app.CAMERA_STOP)
		onClickKeyDict[app.DIK_NUMPAD2] = lambda: app.MoviePitchCamera(app.CAMERA_STOP)
		onClickKeyDict[app.DIK_LALT] = lambda: self.HideName()
		onClickKeyDict[app.DIK_LCONTROL] = lambda: self.HideMouseImage()
		onClickKeyDict[app.DIK_LSHIFT] = lambda: self.__SetQuickSlotMode()

		# Voice Chat PTT key-up: obslugiwane w OnKeyUp (konfigurowalny klawisz),
		# wiec brak wpisu w onClickKeyDict.

		self.onClickKeyDict=onClickKeyDict

	def ChangeBonus(self):
		try:
			if constInfo.IS_BONUS_CHANGER:
				self.interface.wndChangerWindow.ChangeBonus()
			elif constInfo.IS_ACCE_WINDOW:
				acce.SendRefineRequest()
			elif constInfo.IS_DRAGON_SOUL_OPEN:
				self.interface.wndDragonSoulRefine.PressDoRefineButton()
		except:
			pass


	def __PressNumKey(self,num):
		if app.IsPressed(app.DIK_LCONTROL) or app.IsPressed(app.DIK_RCONTROL):

			if num >= 1 and num <= 9:
				if(chrmgr.IsPossibleEmoticon(-1)):
					chrmgr.SetEmoticon(-1,int(num)-1)
					net.SendEmoticon(int(num)-1)
		else:
			if num >= 1 and num <= 4:
				self.pressNumber(num-1)

	def __ClickBKey(self):
		if app.IsPressed(app.DIK_LCONTROL) or app.IsPressed(app.DIK_RCONTROL):
			return
		else:
			if constInfo.PVPMODE_ACCELKEY_ENABLE:
				self.ChangePKMode()
					
	def	__PressJKey(self):
		if app.IsPressed(app.DIK_LCONTROL) or app.IsPressed(app.DIK_RCONTROL):
			if player.IsMountingHorse():
				net.SendChatPacket("/unmount")
			else:
				if not uiPrivateShopBuilder.IsBuildingPrivateShop():
					for i in range(player.INVENTORY_PAGE_SIZE*player.INVENTORY_PAGE_COUNT):
						if player.GetItemIndex(i) in (71114, 71116, 71118, 71120):
							net.SendItemUsePacket(i)
							break
	def	__PressHKey(self):
		if app.IsPressed(app.DIK_LCONTROL) or app.IsPressed(app.DIK_RCONTROL):
			net.SendChatPacket("/user_horse_ride")
		else:
			self.interface.OpenHelpWindow()

	def	__PressBKey(self):
		if app.IsPressed(app.DIK_LCONTROL) or app.IsPressed(app.DIK_RCONTROL):
			net.SendChatPacket("/user_horse_back")
		else:
			state = "EMOTICON"
			self.interface.ToggleCharacterWindow(state)

	def	__PressFKey(self):
		if app.IsPressed(app.DIK_LCONTROL) or app.IsPressed(app.DIK_RCONTROL):
			net.SendChatPacket("/user_horse_feed")
		else:
			app.ZoomCamera(app.CAMERA_TO_POSITIVE)

	def __PressGKey(self):
		if app.IsPressed(app.DIK_LCONTROL) or app.IsPressed(app.DIK_RCONTROL):
			net.SendChatPacket("/user_horse_ride")
		else:
			if self.ShowNameFlag:
				self.interface.ToggleGuildWindow()
			else:
				app.PitchCamera(app.CAMERA_TO_POSITIVE)

	def	__ReleaseGKey(self):
		app.PitchCamera(app.CAMERA_STOP)

	def __PressQKey(self):
		if app.IsPressed(app.DIK_LCONTROL) or app.IsPressed(app.DIK_RCONTROL):
			if 0==interfaceModule.IsQBHide:
				interfaceModule.IsQBHide = 1
				self.interface.HideAllQuestButton()
			else:
				interfaceModule.IsQBHide = 0
				self.interface.ShowAllQuestButton()
		else:
			app.RotateCamera(app.CAMERA_TO_NEGATIVE)

	def __SetQuickSlotMode(self):
		self.pressNumber=ui.__mem_func__(self.__PressQuickSlot)

	def __SetQuickPageMode(self):
		self.pressNumber=ui.__mem_func__(self.__SelectQuickPage)

	def __PressQuickSlot(self, localSlotIndex):
		player.RequestUseLocalQuickSlot(localSlotIndex)

	if app.ENABLE_KEYCHANGE_SYSTEM:
		def OpenKeyChangeWindow(self):
			self.wndKeyChange.Open()

		def OpenWindow(self, type, state):
			if type == player.KEY_OPEN_STATE:
				self.interface.ToggleCharacterWindow(state)
			elif type == player.KEY_OPEN_INVENTORY:
				self.interface.ToggleInventoryWindow()
			elif type == player.KEY_OPEN_DDS:
				self.interface.ToggleDragonSoulWindow()
			elif type == player.KEY_OPEN_MINIMAP:
				self.interface.ToggleMiniMap()
			elif type == player.KEY_OPEN_LOGCHAT:
				self.interface.ToggleChatLogWindow()
			elif type == player.KEY_OPEN_GUILD:
				self.interface.ToggleGuildWindow()
			elif type == player.KEY_OPEN_MESSENGER:
				self.interface.ToggleMessenger()
			elif type == player.KEY_OPEN_HELP:
				self.interface.ToggleHelpWindow()
			elif type == player.KEY_TP_MAP:
				self.interface.ToggleMapWindow()

			elif type == player.KEY_OPEN_EXTENDED_INV:
				self.interface.ToggleExtendedInventoryWindow()
			elif type == player.KEY_OPEN_PET:
				self.__PetKeyOrRemovePolymorph()
			elif type == player.KEY_OPEN_DOPY:
				self.interface.wndBoosters.btnUse()
			elif type == player.KEY_OPEN_MARBLE:
				if app.__AUTO_HUNT__:
					# Auto-hunt tymczasowo wylaczony — F6/KEY_OPEN_MARBLE ma NIE otwierac panelu ani NIE wyswietlac komunikatu
					pass
					#if constInfo.AUTO_HUNT_HAS_AFFECT:
					#	self.interface.OpenAutoHunt()
					#else:
					#	chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.AUTO_HUNT_NO_AFFECT)
				else:
					self.__SafeInterfaceCallMethod('ToggleSwitchbotWindow')
			elif type == player.KEY_OPEN_SAVE_LOCATION:
				self.interface.ToggleSaveLocationWindow()
			# KEY_OPEN_RESP wylaczone — system "Teleportacja do Wladcow/Metinow" nieaktywny
			#elif type == player.KEY_OPEN_RESP:
			#	self.interface.OpenRespWindow()
			elif type == player.KEY_OPEN_BUFF:
				self.OpenShopSearch()
			elif type == player.KEY_OPEN_MISSION:
				self.interface.ToggleCollectWindow()
			elif type == player.KEY_RETURN:
				self.ChangeBonus()
			elif type == player.KEY_OPEN_DUNGEONS:
				self.interface.ToggleDungeonTrackWindow()

			elif type == player.KEY_CHANGECHANNEL1:
				net.MoveChannelGame(1)
			elif type == player.KEY_CHANGECHANNEL2:
				net.MoveChannelGame(2)
			elif type == player.KEY_CHANGECHANNEL3:
				net.MoveChannelGame(3)
			elif type == player.KEY_CHANGECHANNEL4:
				net.MoveChannelGame(4)
			elif type == player.KEY_CHANGECHANNEL5:
				net.MoveChannelGame(5)
			elif type == player.KEY_CHANGECHANNEL6:
				net.MoveChannelGame(6)

		def ScrollOnOff(self):
			if 0 == interfaceModule.IsQBHide:
				interfaceModule.IsQBHide = 1
				self.interface.HideAllQuestButton()
			else:
				interfaceModule.IsQBHide = 0
				self.interface.ShowAllQuestButton()

	def __SelectQuickPage(self, pageIndex):
		self.quickSlotPageIndex = pageIndex
		player.SetQuickPage(pageIndex)

	def ToggleDebugInfo(self):
		self.isShowDebugInfo = not self.isShowDebugInfo

		if self.isShowDebugInfo:
			self.PrintCoord.Show()
			self.FrameRate.Show()
			self.Pitch.Show()
			self.Splat.Show()
			self.TextureNum.Show()
			self.ObjectNum.Show()
			self.ViewDistance.Show()
			self.PrintMousePos.Show()
		else:
			self.PrintCoord.Hide()
			self.FrameRate.Hide()
			self.Pitch.Hide()
			self.Splat.Hide()
			self.TextureNum.Hide()
			self.ObjectNum.Hide()
			self.ViewDistance.Hide()
			self.PrintMousePos.Hide()

	def __BuildDebugInfo(self):
		self.PrintCoord = ui.TextLine()
		self.PrintCoord.SetFontName(localeInfo.UI_DEF_FONT)
		self.PrintCoord.SetPosition(wndMgr.GetScreenWidth() - 270, 0)

		self.FrameRate = ui.TextLine()
		self.FrameRate.SetFontName(localeInfo.UI_DEF_FONT)
		self.FrameRate.SetPosition(wndMgr.GetScreenWidth() - 270, 20)

		self.Pitch = ui.TextLine()
		self.Pitch.SetFontName(localeInfo.UI_DEF_FONT)
		self.Pitch.SetPosition(wndMgr.GetScreenWidth() - 270, 40)

		self.Splat = ui.TextLine()
		self.Splat.SetFontName(localeInfo.UI_DEF_FONT)
		self.Splat.SetPosition(wndMgr.GetScreenWidth() - 270, 60)

		self.PrintMousePos = ui.TextLine()
		self.PrintMousePos.SetFontName(localeInfo.UI_DEF_FONT)
		self.PrintMousePos.SetPosition(wndMgr.GetScreenWidth() - 270, 80)

		self.TextureNum = ui.TextLine()
		self.TextureNum.SetFontName(localeInfo.UI_DEF_FONT)
		self.TextureNum.SetPosition(wndMgr.GetScreenWidth() - 270, 100)

		self.ObjectNum = ui.TextLine()
		self.ObjectNum.SetFontName(localeInfo.UI_DEF_FONT)
		self.ObjectNum.SetPosition(wndMgr.GetScreenWidth() - 270, 120)

		self.ViewDistance = ui.TextLine()
		self.ViewDistance.SetFontName(localeInfo.UI_DEF_FONT)
		self.ViewDistance.SetPosition(0, 0)

	def __NotifyError(self, msg):
		chat.AppendChat(chat.CHAT_TYPE_INFO, msg)

	def ChangePKMode(self):

		if not app.IsPressed(app.DIK_LCONTROL):
			return

		if player.GetStatus(player.LEVEL)<constInfo.PVPMODE_PROTECTED_LEVEL:
			self.__NotifyError(localeInfo.OPTION_PVPMODE_PROTECT % (constInfo.PVPMODE_PROTECTED_LEVEL))
			return

		curTime = app.GetTime()
		if curTime - self.lastPKModeSendedTime < constInfo.PVPMODE_ACCELKEY_DELAY:
			return

		self.lastPKModeSendedTime = curTime

		curPKMode = player.GetPKMode()
		nextPKMode = curPKMode + 1
		if nextPKMode == player.PK_MODE_PROTECT:
			if 0 == player.GetGuildID():
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.OPTION_PVPMODE_CANNOT_SET_GUILD_MODE)
				nextPKMode = 0
			else:
				nextPKMode = player.PK_MODE_GUILD

		elif nextPKMode == player.PK_MODE_MAX_NUM:
			nextPKMode = 0

		net.SendChatPacket("/PKMode " + str(nextPKMode))
		print("/PKMode " + str(nextPKMode)
)

	def OnChangePKMode(self):

		self.interface.OnChangePKMode()

		try:
			self.__NotifyError(localeInfo.OPTION_PVPMODE_MESSAGE_DICT[player.GetPKMode()])
		except KeyError:
			print("UNKNOWN PVPMode[%d]" % (player.GetPKMode())
)

		if constInfo.PVPMODE_TEST_ENABLE:
			curPKMode = player.GetPKMode()
			alignment, grade = chr.testGetPKData()
			self.pkModeNameDict = { 0 : localeInfo.PK_MODE_PEACE, 1 : localeInfo.PK_MODE_REVENGE, 2 : localeInfo.PK_MODE_FREE, 3 : localeInfo.PK_MODE_PROTECT, }
			self.testPKMode.SetText("Current PK Mode : " + self.pkModeNameDict.get(curPKMode, localeInfo.PK_MODE_UNKNOWN))
			self.testAlignment.SetText("Current Alignment : " + str(alignment) + " (" + localeInfo.TITLE_NAME_LIST[grade] + ")")


	def StartGame(self):
		self.RefreshInventory()
		self.RefreshEquipment()
		self.RefreshCharacter()
		self.RefreshSkill()

	def CheckGameButton(self):
		if self.interface:
			self.interface.CheckGameButton()

	def RefreshAlignment(self):
		self.interface.RefreshAlignment()

	def RefreshStatus(self):
		if self.interface:
			self.interface.RefreshStatus()

		if self.playerGauge:
			self.playerGauge.RefreshGauge()

		self.CheckGameButton()

	def RefreshStamina(self):
		self.interface.RefreshStamina()

	def RefreshSkill(self):
		self.CheckGameButton()
		if self.interface:
			self.interface.RefreshSkill()

	def RefreshQuest(self):
		self.interface.RefreshQuest()

	def RefreshMessenger(self):
		self.interface.RefreshMessenger()

	def RefreshGuildInfoPage(self):
		self.interface.RefreshGuildInfoPage()

	def RefreshGuildBoardPage(self):
		self.interface.RefreshGuildBoardPage()

	def RefreshGuildMemberPage(self):
		self.interface.RefreshGuildMemberPage()

	def RefreshGuildMemberPageGradeComboBox(self):
		self.interface.RefreshGuildMemberPageGradeComboBox()

	def RefreshGuildSkillPage(self):
		self.interface.RefreshGuildSkillPage()

	def RefreshGuildGradePage(self):
		self.interface.RefreshGuildGradePage()

	def RefreshMobile(self):
		if self.interface:
			self.interface.RefreshMobile()

	def OnMobileAuthority(self):
		self.interface.OnMobileAuthority()

	def OnBlockMode(self, mode):
		self.interface.OnBlockMode(mode)

	def OpenQuestWindow(self, skin, idx):
		if constInfo.INPUT_IGNORE == 1:
			return
		else:
			self.interface.OpenQuestWindow(skin, idx)

	def AskGuildName(self):

		guildNameBoard = uiCommon.InputDialog()
		guildNameBoard.SetTitle(localeInfo.GUILD_NAME)
		guildNameBoard.SetAcceptEvent(ui.__mem_func__(self.ConfirmGuildName))
		guildNameBoard.SetCancelEvent(ui.__mem_func__(self.CancelGuildName))
		guildNameBoard.Open()

		self.guildNameBoard = guildNameBoard

	def ConfirmGuildName(self):
		guildName = self.guildNameBoard.GetText()
		if not guildName:
			return

		if net.IsInsultIn(guildName):
			self.PopupMessage(localeInfo.GUILD_CREATE_ERROR_INSULT_NAME)
			return

		net.SendAnswerMakeGuildPacket(guildName)
		self.guildNameBoard.Close()
		self.guildNameBoard = None
		return True

	def CancelGuildName(self):
		self.guildNameBoard.Close()
		self.guildNameBoard = None
		return True

	def PopupMessage(self, msg):
		self.stream.popupWindow.Close()
		self.stream.popupWindow.Open(msg, 0, localeInfo.UI_OK)

	def OpenRefineDialog(self, targetItemPos, nextGradeItemVnum, cost, cost2, cost3, prob, type=0, extraProb=0):
		self.interface.OpenRefineDialog(targetItemPos, nextGradeItemVnum, cost, cost2, cost3, prob, type, extraProb)

	def AppendMaterialToRefineDialog(self, vnum, count):
		self.interface.AppendMaterialToRefineDialog(vnum, count)

	def AppendMaterialSourceToRefineDialog(self, materialVnum, sourceType, sourceVnum):
		self.interface.AppendMaterialSourceToRefineDialog(materialVnum, sourceType, sourceVnum)

	def RunUseSkillEvent(self, slotIndex, coolTime):
		self.interface.OnUseSkill(slotIndex, coolTime)

	def ClearAffects(self):
		self.affectShower.ClearAffects()

	def SetAffect(self, affect):
		self.affectShower.SetAffect(affect)

	def ResetAffect(self, affect):
		self.affectShower.ResetAffect(affect)

	def BINARY_NEW_AddAffect(self, type, pointIdx, value, duration):
		self.affectShower.BINARY_NEW_AddAffect(type, pointIdx, value, duration)
		if chr.NEW_AFFECT_DRAGON_SOUL_DECK1 == type or chr.NEW_AFFECT_DRAGON_SOUL_DECK2 == type:
			self.interface.DragonSoulActivate(type - chr.NEW_AFFECT_DRAGON_SOUL_DECK1)
		elif chr.NEW_AFFECT_DRAGON_SOUL_QUALIFIED == type:
			self.BINARY_DragonSoulGiveQuilification()

		if app.__AUTO_HUNT__:
			# Gracz dostal affect-uprawnienie Auto Hunt -> odblokuj panel (F6)
			if type == chr.NEW_AFFECT_AUTO_HUNT:
				constInfo.AUTO_HUNT_HAS_AFFECT = 1
			# Auto-login: po wejsciu do gry (re-load affectow) odpal opoznione wznowienie bota
			if constInfo.autoHuntAutoLoginDict["status"] == 1 and constInfo.autoHuntAutoLoginDict["leftTime"] == -2:
				constInfo.autoHuntAutoLoginDict["leftTime"] = app.GetGlobalTimeStamp() + 2

	def BINARY_NEW_RemoveAffect(self, type, pointIdx):
		self.affectShower.BINARY_NEW_RemoveAffect(type, pointIdx)
		if chr.NEW_AFFECT_DRAGON_SOUL_DECK1 == type or chr.NEW_AFFECT_DRAGON_SOUL_DECK2 == type:
			self.interface.DragonSoulDeactivate()

		if app.__AUTO_HUNT__:
			# Gdy znika affect-uprawnienie Auto Hunt -> zatrzymaj bota na serwerze i zablokuj panel
			if type == chr.NEW_AFFECT_AUTO_HUNT:
				constInfo.AUTO_HUNT_HAS_AFFECT = 0
				net.SendChatPacket("/auto_hunt end")

	if app.ENABLE_AFFECT_FIX:
		def RefreshAffectWindow(self):
			self.affectShower.BINARY_NEW_RefreshAffect()



	def ActivateSkillSlot(self, slotIndex):
		if self.interface:
			self.interface.OnActivateSkill(slotIndex)

	def DeactivateSkillSlot(self, slotIndex):
		if self.interface:
			self.interface.OnDeactivateSkill(slotIndex)

	def RefreshEquipment(self):
		if self.interface:
			self.interface.RefreshInventory()

	def RefreshInventory(self):
		if self.interface:
			self.interface.RefreshInventory()

		if self.affectShower:
			self.affectShower.RefreshInventory()

	def RefreshCharacter(self):
		if self.interface:
			self.interface.RefreshCharacter()

	if app.RENEWAL_DEAD_PACKET:
		def OnGameOver(self, d_time):
			self.CloseTargetBoard()
			self.OpenRestartDialog(d_time)
	else:
		def OnGameOver(self):
			self.CloseTargetBoard()
			self.OpenRestartDialog()

	if app.RENEWAL_DEAD_PACKET:
		def OpenRestartDialog(self, d_time):
			self.interface.OpenRestartDialog(d_time)
	else:
		def OpenRestartDialog(self):
			self.interface.OpenRestartDialog()

	def ChangeCurrentSkill(self, skillSlotNumber):
		self.interface.OnChangeCurrentSkill(skillSlotNumber)

	def SetPCTargetBoard(self, vid, name):
		self.targetBoard.Open(vid, name)

		if app.IsPressed(app.DIK_LCONTROL):

			if not player.IsSameEmpire(vid):
				return

			if player.IsMainCharacterIndex(vid):
				return
			elif chr.INSTANCE_TYPE_BUILDING == chr.GetInstanceType(vid):
				return

			# Autobuff (vnum 10-12, CInstanceBase::IsBuffNPC) jest typu PC, ale to nie gracz - bez szeptu.
			if app.ENABLE_ASLAN_BUFF_NPC_SYSTEM and chr.GetVirtualNumber(vid) in (10, 11, 12):
				return

			self.interface.OpenWhisperDialog(name)


	def RefreshTargetBoardByVID(self, vid):
		self.targetBoard.RefreshByVID(vid)

	def RefreshTargetBoardByName(self, name):
		self.targetBoard.RefreshByName(name)

	def __RefreshTargetBoard(self):
		self.targetBoard.Refresh()

	if app.ENABLE_VIEW_TARGET_DECIMAL_HP:
		def SetHPTargetBoard(self, vid, iMinHP, iMaxHP):
			if vid != self.targetBoard.GetTargetVID():
				self.targetBoard.ResetTargetBoard()
				self.targetBoard.SetEnemyVID(vid)
			
			self.targetBoard.SetHP(iMinHP, iMaxHP)
			self.targetBoard.Show()

	def CloseTargetBoardIfDifferent(self, vid):
		if vid != self.targetBoard.GetTargetVID():
			self.targetBoard.Close()

	def CloseTargetBoard(self):
		self.targetBoard.Close()

	def OpenEquipmentDialog(self, vid):
		self.interface.OpenEquipmentDialog(vid)

	def SetEquipmentDialogItem(self, vid, slotIndex, vnum, count):
		self.interface.SetEquipmentDialogItem(vid, slotIndex, vnum, count)

	def SetEquipmentDialogSocket(self, vid, slotIndex, socketIndex, value):
		self.interface.SetEquipmentDialogSocket(vid, slotIndex, socketIndex, value)

	def SetEquipmentDialogAttr(self, vid, slotIndex, attrIndex, type, value):
		self.interface.SetEquipmentDialogAttr(vid, slotIndex, attrIndex, type, value)

	def ShowMapName(self, mapName, x, y):
		pass
		#if self.mapNameShower:
		#	self.mapNameShower.ShowMapName(mapName, x, y)

		if self.interface:
			self.interface.SetMapName(mapName)
    
	def BINARY_OpenAtlasWindow(self):
		self.interface.BINARY_OpenAtlasWindow()

	def OnRecvWhisper(self, mode, name, line):
		# WHISPER IGNORE (klient-side): nie pokazuj whisperow od zignorowanych nazw.
		# Pokrywa NORMAL, GM i OFFLINE (wszystkie trafiaja tu z RecvWhisperPacket).
		# (zeby wyjac GM-ow z blokady: dodaj `and mode != chat.WHISPER_TYPE_GM`)
		import whisperignore
		if whisperignore.IsIgnored(name):
			return
		if mode == chat.WHISPER_TYPE_GM:
			self.interface.RegisterGameMasterName(name)
		chat.AppendWhisper(mode, name, line)
		self.interface.RecvWhisper(name)

	def OnRecvWhisperSystemMessage(self, mode, name, line):
		chat.AppendWhisper(chat.WHISPER_TYPE_SYSTEM, name, line)
		self.interface.RecvWhisper(name)

	def OnRecvWhisperError(self, mode, name, line):
		if mode in localeInfo.WHISPER_ERROR:
			chat.AppendWhisper(chat.WHISPER_TYPE_SYSTEM, name, localeInfo.WHISPER_ERROR[mode](name))
		else:
			chat.AppendWhisper(chat.WHISPER_TYPE_SYSTEM, name, "Whisper Unknown Error(mode=%d, name=%s)" % (mode, name))
		self.interface.RecvWhisper(name)

	def RecvWhisper(self, name):
		self.interface.RecvWhisper(name)

	def OnPickMoney(self, money):
		self.interface.OnPickMoneyNew(money)

	if app.ENABLE_CHEQUE_SYSTEM:
		def OnPickCheque(self, cheque):
			self.interface.OnPickChequeNew(cheque)

	def OnShopError(self, type):
		try:
			self.PopupMessage(localeInfo.SHOP_ERROR_DICT[type])
		except KeyError:
			self.PopupMessage(localeInfo.SHOP_ERROR_UNKNOWN % (type))

	def OnItemShopError(self, type):
		try:
			self.PopupMessage(localeInfo.ITEMSHOP_ERROR_DICT[type])
		except KeyError:
			self.PopupMessage(localeInfo.SHOP_ERROR_UNKNOWN % (type))

	def OnSafeBoxError(self):
		self.PopupMessage(localeInfo.SAFEBOX_ERROR)

	def OnFishingSuccess(self, isFish, fishName):
		chat.AppendChatWithDelay(chat.CHAT_TYPE_INFO, localeInfo.FISHING_SUCCESS(isFish, fishName), 2000)

	def OnFishingNotifyUnknown(self):
		chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.FISHING_UNKNOWN)

	def OnFishingWrongPlace(self):
		chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.FISHING_WRONG_PLACE)

	def OnFishingNotify(self, isFish, fishName):
		chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.FISHING_NOTIFY(isFish, fishName))

	def OnFishingFailure(self):
		chat.AppendChatWithDelay(chat.CHAT_TYPE_INFO, localeInfo.FISHING_FAILURE, 2000)

	def OnCannotPickItem(self):
		chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.GAME_CANNOT_PICK_ITEM)

	def OnCannotMining(self):
		chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.GAME_CANNOT_MINING)

	def OnCannotUseSkill(self, vid, type):
		if type in localeInfo.USE_SKILL_ERROR_TAIL_DICT:
			textTail.RegisterInfoTail(vid, localeInfo.USE_SKILL_ERROR_TAIL_DICT[type])

		if type in localeInfo.USE_SKILL_ERROR_CHAT_DICT:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.USE_SKILL_ERROR_CHAT_DICT[type])

	def	OnCannotShotError(self, vid, type):
		textTail.RegisterInfoTail(vid, localeInfo.SHOT_ERROR_TAIL_DICT.get(type, localeInfo.SHOT_ERROR_UNKNOWN % (type)))

	def StartPointReset(self):
		self.interface.OpenPointResetDialog()

	def StartShop(self, vid):
		self.interface.OpenShopDialog(vid)

	def EndShop(self):
		self.interface.CloseShopDialog()

	def RefreshShop(self):
		self.interface.RefreshShopDialog()

	def SetShopSellingPrice(self, Price):
		pass

	if app.ENABLE_OFFLINE_SHOP_SYSTEM:
		def StartOfflineShop(self, vid):
			self.interface.OpenOfflineShopDialog(vid)

		def EndOfflineShop(self):
			self.interface.CloseOfflineShopDialog()

		def RefreshOfflineShop(self):
			self.interface.RefreshOfflineShopDialog()

		def __OfflineShop_Open(self):
			self.interface.OpenOfflineShopInputNameDialog()

		def OpenOfflineShopPanel(self):
			if self.interface:
				if self.interface.wndOfflineShopAdminPanel:
					self.interface.wndOfflineShopAdminPanel.Open()

		def OpenOfflineShopLogs(self):
			if self.interface:
				self.interface.ToggleOfflineShopLogWindow()

	def StartExchange(self):
		self.interface.StartExchange()

	def EndExchange(self):
		self.interface.EndExchange()

	def RefreshExchange(self):
		self.interface.RefreshExchange()

	def RecvPartyInviteQuestion(self, leaderVID, leaderName):
		partyInviteQuestionDialog = uiCommon.QuestionDialog()
		partyInviteQuestionDialog.SetText(leaderName + localeInfo.PARTY_DO_YOU_JOIN)
		partyInviteQuestionDialog.SetAcceptEvent(lambda arg=True: self.AnswerPartyInvite(arg))
		partyInviteQuestionDialog.SetCancelEvent(lambda arg=False: self.AnswerPartyInvite(arg))
		partyInviteQuestionDialog.Open()
		partyInviteQuestionDialog.partyLeaderVID = leaderVID
		self.partyInviteQuestionDialog = partyInviteQuestionDialog

	def AnswerPartyInvite(self, answer):

		if not self.partyInviteQuestionDialog:
			return

		partyLeaderVID = self.partyInviteQuestionDialog.partyLeaderVID

		distance = player.GetCharacterDistance(partyLeaderVID)
		if distance < 0.0 or distance > 5000:
			answer = False

		net.SendPartyInviteAnswerPacket(partyLeaderVID, answer)

		self.partyInviteQuestionDialog.Close()
		self.partyInviteQuestionDialog = None

	def AddPartyMember(self, pid, name):
		self.interface.AddPartyMember(pid, name)

	def UpdatePartyMemberInfo(self, pid):
		self.interface.UpdatePartyMemberInfo(pid)

	def RemovePartyMember(self, pid):
		self.interface.RemovePartyMember(pid)
		self.__RefreshTargetBoard()

	def LinkPartyMember(self, pid, vid):
		self.interface.LinkPartyMember(pid, vid)

	def UnlinkPartyMember(self, pid):
		self.interface.UnlinkPartyMember(pid)

	def UnlinkAllPartyMember(self):
		self.interface.UnlinkAllPartyMember()

	def ExitParty(self):
		self.interface.ExitParty()
		self.RefreshTargetBoardByVID(self.targetBoard.GetTargetVID())

	def ChangePartyParameter(self, distributionMode):
		self.interface.ChangePartyParameter(distributionMode)

	def OnMessengerAddFriendQuestion(self, name):
		messengerAddFriendQuestion = uiCommon.QuestionDialog2()
		messengerAddFriendQuestion.SetText1(localeInfo.MESSENGER_DO_YOU_ACCEPT_ADD_FRIEND_1 % (name))
		messengerAddFriendQuestion.SetText2(localeInfo.MESSENGER_DO_YOU_ACCEPT_ADD_FRIEND_2)
		messengerAddFriendQuestion.SetAcceptEvent(ui.__mem_func__(self.OnAcceptAddFriend))
		messengerAddFriendQuestion.SetCancelEvent(ui.__mem_func__(self.OnDenyAddFriend))
		messengerAddFriendQuestion.Open()
		messengerAddFriendQuestion.name = name
		self.messengerAddFriendQuestion = messengerAddFriendQuestion

	def OnAcceptAddFriend(self):
		name = self.messengerAddFriendQuestion.name
		net.SendChatPacket("/messenger_auth y " + name)
		self.OnCloseAddFriendQuestionDialog()
		return True

	def OnDenyAddFriend(self):
		name = self.messengerAddFriendQuestion.name
		net.SendChatPacket("/messenger_auth n " + name)
		self.OnCloseAddFriendQuestionDialog()
		return True

	def OnCloseAddFriendQuestionDialog(self):
		self.messengerAddFriendQuestion.Close()
		self.messengerAddFriendQuestion = None
		return True

	def OpenSafeboxWindow(self, size):
		self.interface.OpenSafeboxWindow(size)

	def RefreshSafebox(self):
		self.interface.RefreshSafebox()

	def RefreshSafeboxMoney(self):
		self.interface.RefreshSafeboxMoney()

	def OpenMallWindow(self, size):
		self.interface.OpenMallWindow(size)

	def RefreshMall(self):
		self.interface.RefreshMall()

	def RecvGuildInviteQuestion(self, guildID, guildName):
		guildInviteQuestionDialog = uiCommon.QuestionDialog()
		guildInviteQuestionDialog.SetText(guildName + localeInfo.GUILD_DO_YOU_JOIN)
		guildInviteQuestionDialog.SetAcceptEvent(lambda arg=True: self.AnswerGuildInvite(arg))
		guildInviteQuestionDialog.SetCancelEvent(lambda arg=False: self.AnswerGuildInvite(arg))
		guildInviteQuestionDialog.Open()
		guildInviteQuestionDialog.guildID = guildID
		self.guildInviteQuestionDialog = guildInviteQuestionDialog

	def AnswerGuildInvite(self, answer):

		if not self.guildInviteQuestionDialog:
			return

		guildLeaderVID = self.guildInviteQuestionDialog.guildID
		net.SendGuildInviteAnswerPacket(guildLeaderVID, answer)

		self.guildInviteQuestionDialog.Close()
		self.guildInviteQuestionDialog = None


	def DeleteGuild(self):
		self.interface.DeleteGuild()

	def ShowClock(self, second):
		self.interface.ShowClock(second)

	def HideClock(self):
		self.interface.HideClock()

	def BINARY_ActEmotion(self, emotionIndex):
		if self.interface.wndCharacter:
			self.interface.wndCharacter.ActEmotion(emotionIndex)


	def CheckFocus(self):
		if False == self.IsFocus():
			if True == self.interface.IsOpenChat():
				self.interface.ToggleChat()

			self.SetFocus()

	def SaveScreen(self):
		return




	def ShowConsole(self):
		if debugInfo.IsDebugMode() or True == self.consoleEnable:
			player.EndKeyWalkingImmediately()
			self.console.OpenWindow()

	def ShowName(self):
		if app.ENABLE_OFFLINE_SHOP:
			offlineshop.ShowShopNames()
		self.ShowNameFlag = True
		self.playerGauge.EnableShowAlways()
		if not app.ENABLE_KEYCHANGE_SYSTEM:
			player.SetQuickPage(self.quickSlotPageIndex + 1)

	def __IsShowName(self):

		if systemSetting.IsAlwaysShowName():
			return True

		if self.ShowNameFlag:
			return True

		return False

	def HideName(self):
		if app.ENABLE_OFFLINE_SHOP:
			offlineshop.HideShopNames()
		self.ShowNameFlag = False
		self.playerGauge.DisableShowAlways()
		if not app.ENABLE_KEYCHANGE_SYSTEM:
			player.SetQuickPage(self.quickSlotPageIndex)

	def ShowMouseImage(self):
		self.interface.ShowMouseImage()

	def HideMouseImage(self):
		self.interface.HideMouseImage()

	def StartAttack(self):
		player.SetAttackKeyState(True)

	def EndAttack(self):
		player.SetAttackKeyState(False)

	def MoveUp(self):
		player.SetSingleDIKKeyState(app.DIK_UP, True)

	def MoveDown(self):
		player.SetSingleDIKKeyState(app.DIK_DOWN, True)

	def MoveLeft(self):
		player.SetSingleDIKKeyState(app.DIK_LEFT, True)

	def MoveRight(self):
		player.SetSingleDIKKeyState(app.DIK_RIGHT, True)

	def StopUp(self):
		player.SetSingleDIKKeyState(app.DIK_UP, False)

	def StopDown(self):
		player.SetSingleDIKKeyState(app.DIK_DOWN, False)

	def StopLeft(self):
		player.SetSingleDIKKeyState(app.DIK_LEFT, False)

	def StopRight(self):
		player.SetSingleDIKKeyState(app.DIK_RIGHT, False)
		
	def PickUpItem(self):
		player.PickCloseItem()
			

	def OnKeyDown(self, key):
		if self.interface.wndWeb and self.interface.wndWeb.IsShow():
			return

		if app.ENABLE_BOT_CONTROL:
			if self.isBotControlActive():
				return

		if key == app.DIK_ESC:
			self.RequestDropItem(False)
			constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(0)

		# Voice Chat push-to-talk: obslugiwane TUTAJ, bo z ENABLE_KEYCHANGE_SYSTEM
		# klawisze ida do player.OnKeyDown (tabela C++) i onPressKeyDict jest pomijany.
		if app.ENABLE_VOICE_CHAT:
			# Tryb capture: okno opcji czeka na nowy klawisz PTT - przechwyc go zamiast
			# nadawania/ruchu. ESC anuluje (obsluzone w OnVoicePTTKeyCapture).
			if constInfo.IsVoicePTTCaptureMode():
				# Oddaj klawisz DO TEJ instancji okna opcji ktora czeka (zarejestrowana
				# przy kliknieciu) - jest kilka instancji OptionDialog, hardcoded
				# self.interface.wndgameOption to czesto NIE ta widoczna.
				dlg = constInfo.GetVoicePTTCaptureDialog()
				if dlg:
					dlg.OnVoicePTTKeyCapture(key)
				else:
					constInfo.SetVoicePTTCaptureMode(False)
				return True
			if key == constInfo.GetVoiceChatPTTKey():
				self.OnStartTalking()
				return True

		# Podglad kolizji dla GM (Ctrl+przecinek). Konsola (collision 1) jest nieosiagalna: klient C++
		# odrzuca komende ConsoleEnable (PythonNetworkStreamCommand.cpp, ServerCommand), a z
		# ENABLE_KEYCHANGE_SYSTEM przecinek i tak nie dochodzi do onPressKeyDict.
		if key == app.DIK_COMMA and (app.IsPressed(app.DIK_LCONTROL) or app.IsPressed(app.DIK_RCONTROL)):
			if chr.IsGameMaster(player.GetMainCharacterIndex()) or debugInfo.IsDebugMode():
				self.console.Console.collision = not self.console.Console.collision
				chat.AppendChat(chat.CHAT_TYPE_INFO, "[GM] podglad kolizji: %s" % ("ON" if self.console.Console.collision else "OFF"))
				return True

		try:
			if app.ENABLE_KEYCHANGE_SYSTEM:
				if self.wndKeyChange.IsOpen() == 1:
					if self.wndKeyChange.IsSelectKeySlot():
						if app.IsPressed(app.DIK_LCONTROL) or app.IsPressed(app.DIK_RCONTROL):
							if self.wndKeyChange.IsChangeKey(self.wndKeyChange.GetSelectSlotNumber()):
								self.wndKeyChange.ChangeKey(key + app.DIK_LCONTROL + self.ADDKEYBUFFERCONTROL)
							else:
								chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.KEYCHANGE_IMPOSSIBLE_CHANGE)
						elif app.IsPressed(app.DIK_LALT) or app.IsPressed(app.DIK_RALT):
							if self.wndKeyChange.IsChangeKey(self.wndKeyChange.GetSelectSlotNumber()):
								self.wndKeyChange.ChangeKey(key + app.DIK_LALT + self.ADDKEYBUFFERALT)
							else:
								chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.KEYCHANGE_IMPOSSIBLE_CHANGE)
						elif app.IsPressed(app.DIK_LSHIFT) or app.IsPressed(app.DIK_RSHIFT):
							if self.wndKeyChange.IsChangeKey(self.wndKeyChange.GetSelectSlotNumber()):
								self.wndKeyChange.ChangeKey(key + app.DIK_LSHIFT + self.ADDKEYBUFFERSHIFT)
							else:
								chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.KEYCHANGE_IMPOSSIBLE_CHANGE)
						else:
							self.wndKeyChange.ChangeKey(key)
				else:
					player.OnKeyDown(key)
			else:
				self.onPressKeyDict[key]()
		except KeyError:
			pass
		except:
			raise

		return True

	def OnKeyUp(self, key):
		if app.ENABLE_VOICE_CHAT and key == constInfo.GetVoiceChatPTTKey():
			self.OnStopTalking()
			return

		if app.ENABLE_KEYCHANGE_SYSTEM:
			player.OnKeyUp(key)
		else:
			try:
				self.onClickKeyDict[key]()
			except KeyError:
				pass
			except:
				raise

	def OnMouseLeftButtonDown(self):
		if self.interface.BUILD_OnMouseLeftButtonDown():
			return

		if mouseModule.mouseController.isAttached():
			self.CheckFocus()
		else:
			hyperlink = ui.GetHyperlink()
			if hyperlink:
				return
			else:
				self.CheckFocus()
				player.SetMouseState(player.MBT_LEFT, player.MBS_PRESS);

		return True

	def OnMouseLeftButtonUp(self):

		if self.interface.BUILD_OnMouseLeftButtonUp():
			return

		if mouseModule.mouseController.isAttached():

			attachedType = mouseModule.mouseController.GetAttachedType()
			attachedItemIndex = mouseModule.mouseController.GetAttachedItemIndex()
			attachedItemSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
			attachedItemCount = mouseModule.mouseController.GetAttachedItemCount()
			if app.ENABLE_OFFLINE_SHOP:
				if uiOfflineShop.IsBuildingShop() and uiOfflineShop.IsSaleSlot(player.SlotTypeToInvenType(attachedType), attachedItemSlotPos):
					chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.CANNOT_DOING_PRIVATE_SHOP_OPEN)
					return

			if player.SLOT_TYPE_QUICK_SLOT == attachedType:
				player.RequestDeleteGlobalQuickSlot(attachedItemSlotPos)

			elif player.SLOT_TYPE_INVENTORY == attachedType or player.SLOT_TYPE_SKILL_BOOK_INVENTORY == attachedType or player.SLOT_TYPE_UPGRADE_ITEMS_INVENTORY == attachedType or player.SLOT_TYPE_STONE_INVENTORY == attachedType or player.SLOT_TYPE_BOX_INVENTORY == attachedType or player.SLOT_TYPE_EFSUN_INVENTORY == attachedType or player.SLOT_TYPE_CICEK_INVENTORY == attachedType:

				if player.ITEM_MONEY == attachedItemIndex:
					self.__PutMoney(attachedType, attachedItemCount, self.PickingCharacterIndex)
				elif player.CHEQUE == attachedItemIndex and app.ENABLE_CHEQUE_SYSTEM:
					self.__PutCheque(attachedType, attachedItemCount, self.PickingCharacterIndex)
				else:
					self.__PutItem(attachedType, attachedItemIndex, attachedItemSlotPos, attachedItemCount, self.PickingCharacterIndex)

			elif player.SLOT_TYPE_DRAGON_SOUL_INVENTORY == attachedType:
				self.__PutItem(attachedType, attachedItemIndex, attachedItemSlotPos, attachedItemCount, self.PickingCharacterIndex)

			mouseModule.mouseController.DeattachObject()

		else:
			hyperlink = ui.GetHyperlink()
			if hyperlink:
				if app.IsPressed(app.DIK_LALT):
					link = chat.GetLinkFromHyperlink(hyperlink)
					ime.PasteString(link)
				else:
					self.interface.MakeHyperlinkTooltip(hyperlink)
				return
			else:
				player.SetMouseState(player.MBT_LEFT, player.MBS_CLICK)

		return True

	def __PutItem(self, attachedType, attachedItemIndex, attachedItemSlotPos, attachedItemCount, dstChrID):
		if player.SLOT_TYPE_INVENTORY == attachedType or player.SLOT_TYPE_DRAGON_SOUL_INVENTORY == attachedType or player.SLOT_TYPE_SKILL_BOOK_INVENTORY == attachedType or player.SLOT_TYPE_UPGRADE_ITEMS_INVENTORY == attachedType or player.SLOT_TYPE_STONE_INVENTORY == attachedType or player.SLOT_TYPE_BOX_INVENTORY == attachedType or player.SLOT_TYPE_EFSUN_INVENTORY == attachedType or player.SLOT_TYPE_CICEK_INVENTORY == attachedType:
			attachedInvenType = player.SlotTypeToInvenType(attachedType)
			if True == chr.HasInstance(self.PickingCharacterIndex) and player.GetMainCharacterIndex() != dstChrID:
				if player.IsEquipmentSlot(attachedItemSlotPos) and player.SLOT_TYPE_DRAGON_SOUL_INVENTORY != attachedType:
					self.stream.popupWindow.Close()
					self.stream.popupWindow.Open(localeInfo.EXCHANGE_FAILURE_EQUIP_ITEM, 0, localeInfo.UI_OK)
				else:
					if chr.IsNPC(dstChrID):
						if app.ENABLE_REFINE_RENEWAL:
							constInfo.AUTO_REFINE_TYPE = 2
							constInfo.AUTO_REFINE_DATA["NPC"][0] = dstChrID
							constInfo.AUTO_REFINE_DATA["NPC"][1] = attachedInvenType
							constInfo.AUTO_REFINE_DATA["NPC"][2] = attachedItemSlotPos
							constInfo.AUTO_REFINE_DATA["NPC"][3] = attachedItemCount
						net.SendGiveItemPacket(dstChrID, attachedInvenType, attachedItemSlotPos, attachedItemCount)
					else:
						net.SendExchangeStartPacket(dstChrID)
						net.SendExchangeItemAddPacket(attachedInvenType, attachedItemSlotPos, 0)
			else:
				self.__DropItem(attachedType, attachedItemIndex, attachedItemSlotPos, attachedItemCount)

	def __PutMoney(self, attachedType, attachedMoney, dstChrID):
		if True == chr.HasInstance(dstChrID) and player.GetMainCharacterIndex() != dstChrID:
			net.SendExchangeStartPacket(dstChrID)
			net.SendExchangeElkAddPacket(attachedMoney)
		else:
			self.__DropMoney(attachedType, attachedMoney)

	def __DropMoney(self, attachedType, attachedMoney):
		if uiPrivateShopBuilder.IsBuildingPrivateShop():
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.DROP_ITEM_FAILURE_PRIVATE_SHOP)
			return

		if app.ENABLE_OFFLINE_SHOP_SYSTEM:
			if (uiOfflineShopBuilder.IsBuildingOfflineShop()):
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.DROP_ITEM_FAILURE_OFFLINE_SHOP)
				return

			if (uiOfflineShop.IsEditingOfflineShop()):
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.DROP_ITEM_FAILURE_OFFLINE_SHOP)
				return

		if attachedMoney>=1000:
			self.stream.popupWindow.Close()
			self.stream.popupWindow.Open(localeInfo.DROP_MONEY_FAILURE_1000_OVER, 0, localeInfo.UI_OK)
			return

		itemDropQuestionDialog = uiCommon.QuestionDialog()
		itemDropQuestionDialog.SetText(localeInfo.DO_YOU_DROP_MONEY % (attachedMoney))
		itemDropQuestionDialog.SetAcceptEvent(lambda arg=True: self.RequestDropItem(arg))
		itemDropQuestionDialog.SetCancelEvent(lambda arg=False: self.RequestDropItem(arg))
		itemDropQuestionDialog.Open()
		itemDropQuestionDialog.dropType = attachedType
		itemDropQuestionDialog.dropCount = attachedMoney
		itemDropQuestionDialog.dropNumber = player.ITEM_MONEY
		self.itemDropQuestionDialog = itemDropQuestionDialog

	if app.ENABLE_CHEQUE_SYSTEM:
		def __PutCheque(self, attachedType, attachedMoney, dstChrID):
			if True == chr.HasInstance(dstChrID) and player.GetMainCharacterIndex() != dstChrID:
				net.SendExchangeStartPacket(dstChrID)
				net.SendExchangeChequeAddPacket(attachedMoney)
			else:
				self.__DropCheque(attachedType, attachedMoney)

		def __DropCheque(self, attachedType, attachedMoney):
			# KowalMT2: wyrzucanie wonow na ziemie jest celowo wylaczone - klient nie eksportuje
			# net.SendGoldChequePacketNew. Wczesniej po potwierdzeniu okna lecial AttributeError.
			return

			if uiPrivateShopBuilder.IsBuildingPrivateShop():
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.DROP_ITEM_FAILURE_PRIVATE_SHOP)
				return
			
			if attachedMoney>=1000:
				self.stream.popupWindow.Close()
				self.stream.popupWindow.Open(localeInfo.DROP_CHEQUE_FAILURE_1000_OVER, 0, localeInfo.UI_OK)
				return

			itemDropQuestionDialog = uiCommon.QuestionDialog()
			itemDropQuestionDialog.SetText(localeInfo.DO_YOU_DROP_CHEQUE % (attachedMoney))
			itemDropQuestionDialog.SetAcceptEvent(lambda arg=True: self.RequestDropItem(arg))
			itemDropQuestionDialog.SetCancelEvent(lambda arg=False: self.RequestDropItem(arg))
			itemDropQuestionDialog.Open()
			itemDropQuestionDialog.dropType = attachedType
			itemDropQuestionDialog.dropCount = attachedMoney
			itemDropQuestionDialog.dropNumber = player.CHEQUE
			self.itemDropQuestionDialog = itemDropQuestionDialog

	def __DropItem(self, attachedType, attachedItemIndex, attachedItemSlotPos, attachedItemCount):
		if uiPrivateShopBuilder.IsBuildingPrivateShop():
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.DROP_ITEM_FAILURE_PRIVATE_SHOP)
			return

		if app.ENABLE_OFFLINE_SHOP_SYSTEM:
			if (uiOfflineShopBuilder.IsBuildingOfflineShop()):
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.DROP_ITEM_FAILURE_OFFLINE_SHOP)
				return

			if (uiOfflineShop.IsEditingOfflineShop()):
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.DROP_ITEM_FAILURE_OFFLINE_SHOP)
				return

		if player.SLOT_TYPE_INVENTORY == attachedType and player.IsEquipmentSlot(attachedItemSlotPos):
			self.stream.popupWindow.Close()
			self.stream.popupWindow.Open(localeInfo.DROP_ITEM_FAILURE_EQUIP_ITEM, 0, localeInfo.UI_OK)

		else:
			if player.SLOT_TYPE_INVENTORY == attachedType or player.SLOT_TYPE_SKILL_BOOK_INVENTORY == attachedType or player.SLOT_TYPE_UPGRADE_ITEMS_INVENTORY == attachedType or player.SLOT_TYPE_STONE_INVENTORY == attachedType or player.SLOT_TYPE_BOX_INVENTORY == attachedType or player.SLOT_TYPE_EFSUN_INVENTORY == attachedType or player.SLOT_TYPE_CICEK_INVENTORY == attachedType:
				dropItemIndex = player.GetItemIndex(attachedItemSlotPos)

				item.SelectItem(dropItemIndex)
				dropItemName = item.GetItemName()

				questionText = localeInfo.HOW_MANY_ITEM_DO_YOU_DROP(dropItemName, attachedItemCount)

				itemDropQuestionDialog = uiCommon.QuestionDialog()
				itemDropQuestionDialog.SetText(questionText)
				itemDropQuestionDialog.SetAcceptEvent(lambda arg=True: self.RequestDropItem(arg))
				itemDropQuestionDialog.SetCancelEvent(lambda arg=False: self.RequestDropItem(arg))
				itemDropQuestionDialog.Open()
				itemDropQuestionDialog.dropType = attachedType
				itemDropQuestionDialog.dropNumber = attachedItemSlotPos
				itemDropQuestionDialog.dropCount = attachedItemCount
				self.itemDropQuestionDialog = itemDropQuestionDialog

				constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(1)
			elif player.SLOT_TYPE_DRAGON_SOUL_INVENTORY == attachedType:
				dropItemIndex = player.GetItemIndex(player.DRAGON_SOUL_INVENTORY, attachedItemSlotPos)

				item.SelectItem(dropItemIndex)
				dropItemName = item.GetItemName()

				questionText = localeInfo.HOW_MANY_ITEM_DO_YOU_DROP(dropItemName, attachedItemCount)

				itemDropQuestionDialog = uiCommon.QuestionDialog()
				itemDropQuestionDialog.SetText(questionText)
				itemDropQuestionDialog.SetAcceptEvent(lambda arg=True: self.RequestDropItem(arg))
				itemDropQuestionDialog.SetCancelEvent(lambda arg=False: self.RequestDropItem(arg))
				itemDropQuestionDialog.Open()
				itemDropQuestionDialog.dropType = attachedType
				itemDropQuestionDialog.dropNumber = attachedItemSlotPos
				itemDropQuestionDialog.dropCount = attachedItemCount
				self.itemDropQuestionDialog = itemDropQuestionDialog

				constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(1)

	def RequestDropItem(self, answer):
		if not self.itemDropQuestionDialog:
			return

		if answer:
			dropType = self.itemDropQuestionDialog.dropType
			dropCount = self.itemDropQuestionDialog.dropCount
			dropNumber = self.itemDropQuestionDialog.dropNumber

			if player.SLOT_TYPE_INVENTORY == dropType or player.SLOT_TYPE_SKILL_BOOK_INVENTORY == dropType or player.SLOT_TYPE_UPGRADE_ITEMS_INVENTORY == dropType or player.SLOT_TYPE_STONE_INVENTORY == dropType or player.SLOT_TYPE_BOX_INVENTORY == dropType or player.SLOT_TYPE_EFSUN_INVENTORY == dropType or player.SLOT_TYPE_CICEK_INVENTORY == dropType:
				if dropNumber == player.ITEM_MONEY:
					net.SendGoldDropPacketNew(dropCount)
					snd.PlaySound("sound/ui/money.wav")
				elif app.ENABLE_CHEQUE_SYSTEM and dropNumber == player.CHEQUE:
					net.SendGoldChequePacketNew(dropCount)
					snd.PlaySound("sound/ui/money.wav")
				else:
					self.__SendDropItemPacket(dropNumber, dropCount)
			elif player.SLOT_TYPE_DRAGON_SOUL_INVENTORY == dropType:
					self.__SendDropItemPacket(dropNumber, dropCount, player.DRAGON_SOUL_INVENTORY)
			elif app.WJ_SPLIT_INVENTORY_SYSTEM:
					if player.SLOT_TYPE_SKILL_BOOK_INVENTORY == dropType or player.SLOT_TYPE_UPGRADE_ITEMS_INVENTORY == dropType or player.SLOT_TYPE_STONE_INVENTORY == dropType or player.SLOT_TYPE_BOX_INVENTORY == dropType or player.SLOT_TYPE_EFSUN_INVENTORY == dropType or player.SLOT_TYPE_CICEK_INVENTORY == dropType:
						self.__SendDropItemPacket(dropNumber, dropCount, player.SLOT_TYPE_SKILL_BOOK_INVENTORY or player.SLOT_TYPE_UPGRADE_ITEMS_INVENTORY or player.SLOT_TYPE_STONE_INVENTORY or player.SLOT_TYPE_BOX_INVENTORY or player.SLOT_TYPE_EFSUN_INVENTORY or player.SLOT_TYPE_CICEK_INVENTORY)

		self.itemDropQuestionDialog.Close()
		self.itemDropQuestionDialog = None

		constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(0)

	def __SendDropItemPacket(self, itemVNum, itemCount, itemInvenType = player.INVENTORY):
		if uiPrivateShopBuilder.IsBuildingPrivateShop():
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.DROP_ITEM_FAILURE_PRIVATE_SHOP)
			return

		if app.ENABLE_OFFLINE_SHOP_SYSTEM:
			if (uiOfflineShopBuilder.IsBuildingOfflineShop()):
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.DROP_ITEM_FAILURE_OFFLINE_SHOP)
				return

			if (uiOfflineShop.IsEditingOfflineShop()):
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.DROP_ITEM_FAILURE_OFFLINE_SHOP)
				return

		net.SendItemDropPacketNew(itemInvenType, itemVNum, itemCount)

	def OnMouseRightButtonDown(self):

		self.CheckFocus()

		if True == mouseModule.mouseController.isAttached():
			mouseModule.mouseController.DeattachObject()

		else:
			player.SetMouseState(player.MBT_RIGHT, player.MBS_PRESS)

		return True

	def OnMouseRightButtonUp(self):
		if True == mouseModule.mouseController.isAttached():
			return True

		player.SetMouseState(player.MBT_RIGHT, player.MBS_CLICK)
		return True

	def OnMouseMiddleButtonDown(self):
		player.SetMouseMiddleButtonState(player.MBS_PRESS)

	def OnMouseMiddleButtonUp(self):
		player.SetMouseMiddleButtonState(player.MBS_CLICK)

	def OnUpdate(self):
		try:
			app.UpdateGame()
		except:
			pass

		if app.ENABLE_OFFLINE_SHOP:
			# Ciagle naprowadzanie do sklepu z wyszukiwarki - przestawia strzalke
			# w miare marszu. Sama funkcja jest tania: wychodzi od razu, gdy
			# naprowadzanie nieaktywne albo gracz nie przeszedl kawalka drogi.
			offlineshop.UpdateShopLocator()

		if app.ENABLE_NEW_PET_SYSTEM and hasattr(self, '__petRetryTime') and self.__petRetryTime > 0:
			if app.GetTime() >= self.__petRetryTime:
				pet.SendRequestInfo()
				self.__petRetryTime = 0

		if app.IsPressed(app.DIK_Z):
			player.PickCloseItem()

		if self.isShowDebugInfo:
			self.UpdateDebugInfo()

		if self.enableXMasBoom:
			self.__XMasBoom_Update()

		try:
			self.interface.BUILD_OnUpdate()
		except:
			pass

		if app.__AUTO_HUNT__:
			# Auto-login: po wejsciu do gry wznow okno + bota
			if constInfo.autoHuntAutoLoginDict["status"] == 1 and constInfo.autoHuntAutoLoginDict["leftTime"] > 0 and constInfo.autoHuntAutoLoginDict["leftTime"] < app.GetGlobalTimeStamp():
				constInfo.autoHuntAutoLoginDict["leftTime"] = 0
				self.interface.CheckAutoLogin()

		if hasattr(app, "ENABLE_PREMIUM_PRIVATE_SHOP_OFFICIAL") and app.ENABLE_PREMIUM_PRIVATE_SHOP_OFFICIAL:
			uiPrivateShop.UpdateTitleBoard()

		if app.ENABLE_AUTO_SHOUT:
			if constInfo.AUTO_SHOUT_ACTIVATED and len(constInfo.LAST_SHOUT_MESSAGE) != 0:
				if self.lastShoutTime <= app.GetTime():
					self.lastShoutTime = app.GetTime() + constInfo.SHOUT_PER_SECOND
					net.SendChatPacket(str(constInfo.LAST_SHOUT_MESSAGE), chat.CHAT_TYPE_SHOUT)

	def UpdateDebugInfo(self):
		(x, y, z) = player.GetMainCharacterPosition()
		nUpdateTime = app.GetUpdateTime()
		nUpdateFPS = app.GetUpdateFPS()
		nRenderFPS = app.GetRenderFPS()
		nFaceCount = app.GetFaceCount()
		fFaceSpeed = app.GetFaceSpeed()
		nST=background.GetRenderShadowTime()
		(fAveRT, nCurRT) =  app.GetRenderTime()
		(iNum, fFogStart, fFogEnd, fFarCilp) = background.GetDistanceSetInfo()
		(iPatch, iSplat, fSplatRatio, sTextureNum) = background.GetRenderedSplatNum()
		if iPatch == 0:
			iPatch = 1


		self.PrintCoord.SetText("Coordinate: %.2f %.2f %.2f ATM: %d" % (x, y, z, app.GetAvailableTextureMemory()//(1024*1024)))
		xMouse, yMouse = wndMgr.GetMousePosition()
		self.PrintMousePos.SetText("MousePosition: %d %d" % (xMouse, yMouse))

		self.FrameRate.SetText("UFPS: %3d UT: %3d FS %.2f" % (nUpdateFPS, nUpdateTime, fFaceSpeed))

		if fAveRT>1.0:
			self.Pitch.SetText("RFPS: %3d RT:%.2f(%3d) FC: %d(%.2f) " % (nRenderFPS, fAveRT, nCurRT, nFaceCount, nFaceCount/fAveRT))

		self.Splat.SetText("PATCH: %d SPLAT: %d BAD(%.2f)" % (iPatch, iSplat, fSplatRatio))
		self.ViewDistance.SetText("Num : %d, FS : %f, FE : %f, FC : %f" % (iNum, fFogStart, fFogEnd, fFarCilp))

	# ---- DIAGNOSTYKA SCINEK: pomiar pauz garbage collectora ----
	def __InstallGcProbe(self):
		global _gcProbeInstalled

		try:
			import gc
			import time

			if _gcProbeInstalled:
				return
			_gcProbeInstalled = True

			state = {"t0": 0.0}

			def gcCallback(phase, info):
				if phase == "start":
					state["t0"] = time.perf_counter()
					return

				ms = (time.perf_counter() - state["t0"]) * 1000.0
				if ms < 1.0:
					return

				try:
					# UWAGA: NIE wolamy gc.get_objects() - samo w sobie przechodzi po wszystkich
					# obiektach i kosztowaloby wiecej niz mierzona pauza. get_count() jest tanie.
					counts = gc.get_count()
					app.HitchNote(
						"PYTHON-GC  gen=%d  zebrano=%d  liczniki=%s"
						% (info.get("generation", -1), info.get("collected", 0), str(counts)),
						ms)
				except Exception:
					pass

			gc.callbacks.append(gcCallback)
		except Exception as e:
			dbg.TraceError("GC probe install failed: %s" % str(e))

	def OnRender(self):
		try:
			app.RenderGame()
		except:
			pass

		if self.console.Console.collision:
			background.RenderCollision()
			chr.RenderCollision()

		(x, y) = app.GetCursorPosition()

		try:
			textTail.UpdateAllTextTail()
		except:
			pass

		if True == wndMgr.IsPickedWindow(self.hWnd):

			self.PickingCharacterIndex = chr.Pick()

			if -1 != self.PickingCharacterIndex:
				textTail.ShowCharacterTextTail(self.PickingCharacterIndex)
			if 0 != self.targetBoard.GetTargetVID():
				textTail.ShowCharacterTextTail(self.targetBoard.GetTargetVID())

			if not self.__IsShowName():
				self.PickingItemIndex = item.Pick()
				if -1 != self.PickingItemIndex:
					textTail.ShowItemTextTail(self.PickingItemIndex)


		if self.__IsShowName():
			textTail.ShowAllTextTail()
			self.PickingItemIndex = textTail.Pick(x, y)

		try:
			textTail.UpdateShowingTextTail()
			textTail.ArrangeTextTail()
		except:
			pass
		if -1 != self.PickingItemIndex:
			textTail.SelectItemName(self.PickingItemIndex)

		grp.PopState()
		grp.SetInterfaceRenderState()

		try:
			textTail.Render()
			textTail.HideAllTextTail()
		except:
			pass

	def OnPressEscapeKey(self):

		if app.ENABLE_BOT_CONTROL:
			if self.isBotControlActive():
				return
		if app.TARGET == app.GetCursor():
			app.SetCursor(app.NORMAL)

		elif True == mouseModule.mouseController.isAttached():
			mouseModule.mouseController.DeattachObject()

		else:
			self.interface.OpenSystemDialog()

		return True

	def OnIMEReturn(self):
		if app.IsPressed(app.DIK_LSHIFT):
			self.interface.OpenWhisperDialogWithoutTarget()
		else:
			self.interface.ToggleChat()
		return True

	def OnPressExitKey(self):
		self.interface.ToggleSystemDialog()
		return True

	
	if app.WJ_ENABLE_TRADABLE_ICON:
		def BINARY_AddItemToExchange(self, inven_type, inven_pos, display_pos):
			if inven_type == player.INVENTORY:
				self.interface.CantTradableItemExchange(display_pos, inven_pos)

	def BINARY_LoverInfo(self, name, lovePoint):
		if self.interface.wndMessenger:
			self.interface.wndMessenger.OnAddLover(name, lovePoint)
		if self.affectShower:
			self.affectShower.SetLoverInfo(name, lovePoint)

	def BINARY_UpdateLovePoint(self, lovePoint):
		if self.interface.wndMessenger:
			self.interface.wndMessenger.OnUpdateLovePoint(lovePoint)
		if self.affectShower:
			self.affectShower.OnUpdateLovePoint(lovePoint)

	def BINARY_OnQuestConfirm(self, msg, timeout, pid):
		confirmDialog = uiCommon.QuestionDialogWithTimeLimit()
		confirmDialog.Open(msg, timeout)
		confirmDialog.SetAcceptEvent(lambda answer=True, pid=pid: net.SendQuestConfirmPacket(answer, pid) or self.confirmDialog.Hide())
		confirmDialog.SetCancelEvent(lambda answer=False, pid=pid: net.SendQuestConfirmPacket(answer, pid) or self.confirmDialog.Hide())
		self.confirmDialog = confirmDialog

	def Gift_Show(self):
		self.interface.ShowGift()

	def BINARY_AddToQueue(self, vnum, value):
		self.interface.AppendQueue(vnum, value)

	def BINARY_Highlight_Item(self, inven_type, inven_pos):
		if self.interface:
			self.interface.Highligt_Item(inven_type, inven_pos)

	def BINARY_Cards_UpdateInfo(self, hand_1, hand_1_v, hand_2, hand_2_v, hand_3, hand_3_v, hand_4, hand_4_v, hand_5, hand_5_v, cards_left, points):
		self.interface.UpdateCardsInfo(hand_1, hand_1_v, hand_2, hand_2_v, hand_3, hand_3_v, hand_4, hand_4_v, hand_5, hand_5_v, cards_left, points)
		
	def BINARY_Cards_FieldUpdateInfo(self, hand_1, hand_1_v, hand_2, hand_2_v, hand_3, hand_3_v, points):
		self.interface.UpdateCardsFieldInfo(hand_1, hand_1_v, hand_2, hand_2_v, hand_3, hand_3_v, points)
		
	def BINARY_Cards_PutReward(self, hand_1, hand_1_v, hand_2, hand_2_v, hand_3, hand_3_v, points):
		self.interface.CardsPutReward(hand_1, hand_1_v, hand_2, hand_2_v, hand_3, hand_3_v, points)
		
	def BINARY_Cards_ShowIcon(self):
		self.interface.CardsShowIcon()
		
	def BINARY_Cards_Open(self, safemode):
		self.interface.OpenCardsWindow(safemode)

	def BINARY_DragonSoulGiveQuilification(self):
		self.interface.DragonSoulGiveQuilification()

	if app.ENABLE_DS_CHANGE_ATTR:
		def BINARY_DragonSoulRefineWindow_Open(self, type):
			self.interface.OpenDragonSoulRefineWindow(type)
	else:
		def BINARY_DragonSoulRefineWindow_Open(self):
			self.interface.OpenDragonSoulRefineWindow()

	def BINARY_DragonSoulRefineWindow_RefineFail(self, reason, inven_type, inven_pos):
		self.interface.FailDragonSoulRefine(reason, inven_type, inven_pos)

	def BINARY_DragonSoulRefineWindow_RefineSucceed(self, inven_type, inven_pos):
		self.interface.SucceedDragonSoulRefine(inven_type, inven_pos)


	def BINARY_SetBigMessage(self, message):
		self.interface.bigBoard.SetTip(message)

	def BINARY_SetTipMessage(self, message):
		self.interface.tipBoard.SetTip(message)

	if app.ENABLE_DUNGEON_INFO_SYSTEM:
		def BINARY_DungeonInfoOpen(self):
			if self.interface:
				self.interface.DungeonInfoOpen()

		def BINARY_DungeonRankingRefresh(self):
			if self.interface:
				self.interface.DungeonRankingRefresh()

		def BINARY_DungeonInfoReload(self, onReset):
			if self.interface:
				self.interface.DungeonInfoReload(onReset)

	def BINARY_AppendNotifyMessage(self, type):
		if not type in localeInfo.NOTIFY_MESSAGE:
			return
		chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.NOTIFY_MESSAGE[type])

	def BINARY_Guild_EnterGuildArea(self, areaID):
		self.interface.BULID_EnterGuildArea(areaID)

	def BINARY_Guild_ExitGuildArea(self, areaID):
		self.interface.BULID_ExitGuildArea(areaID)

	def BINARY_GuildWar_OnSendDeclare(self, guildID):
		pass

	def BINARY_GuildWar_OnRecvDeclare(self, guildID, warType):
		mainCharacterName = player.GetMainCharacterName()
		masterName = guild.GetGuildMasterName()
		if mainCharacterName == masterName:
			self.__GuildWar_OpenAskDialog(guildID, warType)

	def BINARY_GuildWar_OnRecvPoint(self, gainGuildID, opponentGuildID, point):
		self.interface.OnRecvGuildWarPoint(gainGuildID, opponentGuildID, point)

	def BINARY_GuildWar_OnStart(self, guildSelf, guildOpp):
		self.interface.OnStartGuildWar(guildSelf, guildOpp)

	def BINARY_GuildWar_OnEnd(self, guildSelf, guildOpp):
		self.interface.OnEndGuildWar(guildSelf, guildOpp)

	def BINARY_BettingGuildWar_SetObserverMode(self, isEnable):
		self.interface.BINARY_SetObserverMode(isEnable)

	def BINARY_BettingGuildWar_UpdateObserverCount(self, observerCount):
		self.interface.wndMiniMap.UpdateObserverCount(observerCount)

	def __GuildWar_UpdateMemberCount(self, guildID1, memberCount1, guildID2, memberCount2, observerCount):
		guildID1 = int(guildID1)
		guildID2 = int(guildID2)
		memberCount1 = int(memberCount1)
		memberCount2 = int(memberCount2)
		observerCount = int(observerCount)

		self.interface.UpdateMemberCount(guildID1, memberCount1, guildID2, memberCount2)
		self.interface.wndMiniMap.UpdateObserverCount(observerCount)

	def __GuildWar_OpenAskDialog(self, guildID, warType):

		guildName = guild.GetGuildName(guildID)

		if "Noname" == guildName:
			return

		import uiGuild
		questionDialog = uiGuild.AcceptGuildWarDialog()
		questionDialog.SAFE_SetAcceptEvent(self.__GuildWar_OnAccept)
		questionDialog.SAFE_SetCancelEvent(self.__GuildWar_OnDecline)
		questionDialog.Open(guildName, warType)

		self.guildWarQuestionDialog = questionDialog

	def __GuildWar_CloseAskDialog(self):
		self.guildWarQuestionDialog.Close()
		self.guildWarQuestionDialog = None

	def __GuildWar_OnAccept(self):

		guildName = self.guildWarQuestionDialog.GetGuildName()

		net.SendChatPacket("/war " + guildName)
		self.__GuildWar_CloseAskDialog()

		return 1

	def __GuildWar_OnDecline(self):

		guildName = self.guildWarQuestionDialog.GetGuildName()

		net.SendChatPacket("/nowar " + guildName)
		self.__GuildWar_CloseAskDialog()

		return 1

	def __ExitGame(self):
		app.Exit()

	def __ServerCommand_Build(self):
		serverCommandList={
			"quit"					: self.__ExitGame,
			"ConsoleEnable"			: self.__Console_Enable,
			"DayMode"				: self.__DayMode_Update,
			"PRESERVE_DayMode"		: self.__PRESERVE_DayMode_Update,
			"CloseRestartWindow"	: self.__RestartDialog_Close,
			"OpenPrivateShop"		: self.__PrivateShop_Open,
			"PartyHealReady"		: self.PartyHealReady,
			"ShowMeSafeboxPassword"	: self.AskSafeboxPassword,
			"CloseSafebox"			: self.CommandCloseSafebox,

			"CloseMall"				: self.CommandCloseMall,
			"ShowMeMallPassword"	: self.AskMallPassword,
			"item_mall"				: self.__ItemMall_Open,

			"RefineSuceeded"		: self.RefineSuceededMessage,
			"RefineFailed"			: self.RefineFailedMessage,
			"xmas_snow"				: self.__XMasSnow_Enable,
			"xmas_boom"				: self.__XMasBoom_Enable,
			"xmas_song"				: self.__XMasSong_Enable,
			"xmas_tree"				: self.__XMasTree_Enable,
			"newyear_boom"			: self.__XMasBoom_Enable,
			"PartyRequest"			: self.__PartyRequestQuestion,
			"PartyRequestDenied"	: self.__PartyRequestDenied,
			"horse_state"			: self.__Horse_UpdateState,
			"hide_horse_state"		: self.__Horse_HideState,
			"WarUC"					: self.__GuildWar_UpdateMemberCount,
			"test_server"			: self.__EnableTestServerFlag,
			"mall"			: self.__InGameShop_Show,


			"lover_login"			: self.__LoginLover,
			"lover_logout"			: self.__LogoutLover,
			"lover_near"			: self.__LoverNear,
			"lover_far"				: self.__LoverFar,
			"lover_divorce"			: self.__LoverDivorce,
			"PlayMusic"				: self.__PlayMusic,

			"MyShopPriceList"		: self.__PrivateShop_PriceList,

			"REV_CARD_REWARD"		: self.CardsReward,
			"REW_CARD_OPEN"			: self.CardsOpen,
			
			"get_input_start"		: self.GetInputOn,
			"get_input_end"			: self.GetInputOff,
			"AddCasketItem" : self.__RecvCasketItem,
			"SortCasketWindow" : self.__RecvCasketBuild,
			
			"load_server_rank"		: self.ServerRankLoadInfo,
			"load_server_rank_pos"	: self.ServerRankLoadMyPos,	
			"load_rank"				: self.RankLoadInfo,
			"load_rank_pos"			: self.RankLoadMyPos,	
			
			"enlight_o"				: self.EnlightenmentWindowOpen,
			"enlight_r"				: self.EnlightenmentWindowRefresh,
			"enlight_n"				: self.EnlightenmentUpgradeNotice,
			
			"my_ore"				: self.SetMyOreCount,
			"my_fish"				: self.SetMyFishCount,
			"my_ore_fish"			: self.SetMyOreFishCount,
			"fishw_cfgs"			: self.FishWiki_ConfigStart,
			"fishw_cfgf"			: self.FishWiki_ConfigFish,
			"fishw_cfge"			: self.FishWiki_ConfigEnd,
			"fishw_new"				: self.FishWiki_NewFishUnlocked,
			"fishw_ustat"			: self.FishWiki_UnlockStatus,
			"fishw_fdata"			: self.FishWiki_FishData,
			"fishw_ranks"			: self.FishWiki_RankLoadStart,
			"fishw_rankd"			: self.FishWiki_RankLoadData,
			"fishw_ranke"			: self.FishWiki_RankLoadEnd,
			"fishw_loader"			: self.FishWiki_LoadError,

		}

		if app.ENABLE_ASLAN_BUFF_NPC_SYSTEM:
			serverCommandList["BuffNPCSummon"] = self.__SetBuffNPCSummon
			serverCommandList["BuffNPCUnsummon"] = self.__SetBuffNPCUnsummon
			serverCommandList["BuffNPCClear"] = self.__SetBuffNPCClear
			serverCommandList["BuffNPCBasicInfo"] = self.__SetBuffNPCBasicInfo
			serverCommandList["BuffNPCSkillInfo"] = self.__SetBuffNPCSkillInfo
			serverCommandList["BuffNPCSkillCooltime"] = self.__SetBuffNPCSkillSetSkillCooltime
			serverCommandList["BuffNPCCreatePopup"] = self.__SetBuffNPCCreatePopup

		if constInfo.GIFT_CODE_SYSTEM:
			serverCommandList.update({"OpenCodeWindow" : self.__OpenCodeWindow})

		if app.ENABLE_SKILL_SELECT_FEATURE:
			serverCommandList["selectskill_open"] = self.__OpenSkillSelectWindow

		if app.ENABLE_COLLECT_WINDOW:
			serverCommandList.update({"UpdateTime" : self.UpdateTime})
			serverCommandList.update({"UpdateChance" : self.UpdateChance})

		if app.ENABLE_DROP_INFO:
			serverCommandList.update({
				"DropInfoRefresh" : self.DropInfoRefresh,
			})

		if app.ENABLE_HIDE_COSTUME_SYSTEM:
			serverCommandList.update({"SetBodyCostumeHidden" : self.SetBodyCostumeHidden })
			serverCommandList.update({"SetHairCostumeHidden" : self.SetHairCostumeHidden })
			serverCommandList.update({"SetAcceCostumeHidden" : self.SetAcceCostumeHidden })
			serverCommandList.update({"SetWeaponCostumeHidden" : self.SetWeaponCostumeHidden })
			serverCommandList.update({"SetAuraCostumeHidden" : self.SetAuraCostumeHidden })
			serverCommandList.update({"SetStoleCostumeHidden" : self.SetStoleCostumeHidden })

		if app.BL_MOVE_CHANNEL:
			serverCommandList["server_info"] = self.__SeverInfo

		if app.TEAM_MEMBER_STATUS:
			serverCommandList["UpdateTeamMemberStatus"] = self.__BINARY__UpdateTeamMemberStatus
			serverCommandList["ClearTeamMemberList"] = self.__BINARY__ClearTeamMemberList

		serverCommandList["UpdateDungeonDailyCount"] = self.__UpdateDungeonDailyCount

		if app.ENABLE_OFFLINE_SHOP_SYSTEM:
			serverCommandList["OpenOfflineShop"] =self.__OfflineShop_Open
			serverCommandList["OpenOfflineShopPanel"] =self.OpenOfflineShopPanel
			serverCommandList["OpenOfflineShopLogs"]=self.OpenOfflineShopLogs

		# Pet system: data now arrives via GC_PET_INFO packets, not server commands.
		# BINARY_Pet* callbacks are called directly from C++ on this game phase window.


		if app.ENABLE_ODLAMKI_SYSTEM:
			serverCommandList["OpenOdlamki"] = self.OpenFragments

		if app.ENABLE_COLLECT_WINDOW:
			serverCommandList["SetCollectWindowQID"] = self.__SetCollectWindowQID
			serverCommandList["OpenCollectWindow"] = self.OpenCollectWindow

		if hasattr(app, "ENABLE_PREMIUM_PRIVATE_SHOP_OFFICIAL") and app.ENABLE_PREMIUM_PRIVATE_SHOP_OFFICIAL:
			serverCommandList["SetPrivateShopPremiumBuild"] = self.SetPrivateShopPremiumBuild

		if app.ENABLE_VOICE_CHAT:
			serverCommandList["voice_chat_disabled"] = self.__DisableVoiceChat
			serverCommandList["voice_chat_config"] = self.__ConfigVoiceChat
			serverCommandList["voice_chat_level"] = self.__VoiceChatLevelRequired

		if app.__AUTO_HUNT__:
			serverCommandList["AutoHuntStatus"] = self.interface.AutoHuntStatus

		self.serverCommander=stringCommander.Analyzer()
		for serverCommandItem in serverCommandList.items():
			self.serverCommander.SAFE_RegisterCallBack(
				serverCommandItem[0], serverCommandItem[1]
			)

		if app.ENABLE_SECONDARY_LEVEL:
			self.serverCommander.SAFE_RegisterCallBack("OpenSecondaryLevelWindow", self.__SecondaryLevel_Open)

		self.serverCommander.SAFE_RegisterCallBack("EnlightenmentWindowOpen", self.EnlightenmentWindowOpen)

		# Maintenance system — countdown widget. Server wysyła
		# "Maintenancegui <shutdownTimestamp> <duration>" przy entergame
		# (jeśli aktywne) LUB przy GM /start_maintenance broadcast.
		self.serverCommander.SAFE_RegisterCallBack("Maintenancegui", self.Maintenancegui)
		self.serverCommander.SAFE_RegisterCallBack("MaintenanceAdminOpen", self.MaintenanceAdminOpen)

	def Maintenancegui(self, shutdownTimestamp, duration):
		"""Callback z server ChatPacket "Maintenancegui <ts> <dur>"."""
		try:
			ts = int(shutdownTimestamp)
			dur = int(duration)
		except (ValueError, TypeError):
			return
		if not hasattr(self, "maintenance") or self.maintenance is None:
			import uimaintenance
			self.maintenance = uimaintenance.MaintenanceWindow()
		if ts <= 0 and dur <= 0:
			# Server cancel — schowaj okno
			self.maintenance.Close()
		else:
			self.maintenance.Open(ts, dur)

	def MaintenanceAdminOpen(self):
		"""GM-only — otwiera dialog start/cancel maintenance."""
		if not chr.IsGameMaster(player.GetMainCharacterIndex()):
			return
		import uimaintenance
		self.maintenanceDialog = uimaintenance.MaintenanceDialog()
		self.maintenanceDialog.Show()

	if app.ENABLE_HIDE_COSTUME_SYSTEM:
		def SetBodyCostumeHidden(self, hidden):
			try:
				constInfo.HIDDEN_BODY_COSTUME = int(hidden)
				self.interface.RefreshVisibleCostume()
			except:
				pass

		def SetHairCostumeHidden(self, hidden):
			try:
				constInfo.HIDDEN_HAIR_COSTUME = int(hidden)
				self.interface.RefreshVisibleCostume()
			except:
				pass

		def SetAcceCostumeHidden(self, hidden):
			try:
				constInfo.HIDDEN_ACCE_COSTUME = int(hidden)
				self.interface.RefreshVisibleCostume()
			except:
				pass
				
		def SetStoleCostumeHidden(self, hidden):
			try:
				constInfo.HIDDEN_STOLE_COSTUME = int(hidden)
				self.interface.RefreshVisibleCostume()
			except:
				pass

		def SetWeaponCostumeHidden(self, hidden):
			try:
				constInfo.HIDDEN_WEAPON_COSTUME = int(hidden)
				self.interface.RefreshVisibleCostume()
			except:
				pass

		def SetAuraCostumeHidden(self, hidden):
			try:
				constInfo.HIDDEN_AURA_COSTUME = int(hidden)
				self.interface.RefreshVisibleCostume()
			except:
				pass

		def OnPickPktOsiag(self, pkt_osiag):
			self.interface.OnPickPktOsiagNew(pkt_osiag)

	def BINARY_ServerCommand_Run(self, line):
		try:
			return self.serverCommander.Run(line)
		except RuntimeError as msg:
			dbg.TraceError(msg)
			return 0

	def __ProcessPreservedServerCommand(self):
		try:
			command = net.GetPreservedServerCommand()
			while command:
				print(" __ProcessPreservedServerCommand", command
)
				self.serverCommander.Run(command)
				command = net.GetPreservedServerCommand()
		except RuntimeError as msg:
			dbg.TraceError(msg)
			return 0

	def CardsOpen(self):
		import uicardslottery
		self.a = uicardslottery.CardsLottery()
		self.a.Open()
  
	def CardsReward(self, id):
		self.a.Reward(id)

	def PartyHealReady(self):
		try:
			self.interface.PartyHealReady()
		except:
			pass

	def AskSafeboxPassword(self):
		try:
			self.interface.AskSafeboxPassword()
		except:
			pass

	def AskMallPassword(self):
		self.interface.AskMallPassword()

	def __ItemMall_Open(self):
		self.interface.OpenItemMall();

	def CommandCloseMall(self):
		self.interface.CommandCloseMall()



		

	if app.ENABLE_ODLAMKI_SYSTEM:
		def OpenFragments(self):
			self.interface.OpenFragmentsWindow()

		def BINARY_OdlamkiItemRefreshWindow(self):
			self.interface.wndFragments.ClearWindow()

	if app.ENABLE_ASLAN_BUFF_NPC_SYSTEM:
		def __SetBuffNPCSummon(self):
			self.interface.BuffNPC_Summon()
			
		def __SetBuffNPCUnsummon(self):
			self.interface.BuffNPC_Unsummon()
			
		def __SetBuffNPCClear(self):
			self.interface.BuffNPC_Clear()

		def __SetBuffNPCBasicInfo(self, name, sex, intvalue):
			self.interface.BuffNPC_SetBasicInfo(str(name), int(sex), int(intvalue))

		def __SetBuffNPCSkillInfo(self, skill1, skill2, skill3):
			self.interface.BuffNPC_SetSkillInfo(skill1, skill2, skill3)
			
		def __SetBuffNPCSkillSetSkillCooltime(self, slot, timevalue):
			self.interface.BuffNPC_SetSkillCooltime(slot, timevalue)
			
		def __SetBuffNPCCreatePopup(self, type, value0, value1):
			self.interface.BuffNPC_CreatePopup(int(type), int(value0), int(value1))
			
		def BINARY_OpenCreateBuffWindow(self):
			self.interface.BuffNPC_OpenCreateWindow()

	def RefineSuceededMessage(self):
		snd.PlaySound("sound/ui/make_soket.wav")
		self.PopupMessage(localeInfo.REFINE_SUCCESS)
		if app.ENABLE_REFINE_RENEWAL:
			self.interface.CheckRefineDialog(False)

	def RefineFailedMessage(self):
		snd.PlaySound("sound/ui/jaeryun_fail.wav")
		self.PopupMessage(localeInfo.REFINE_FAILURE)
		if app.ENABLE_REFINE_RENEWAL:
			self.interface.CheckRefineDialog(True)

	def CommandCloseSafebox(self):
		self.interface.CommandCloseSafebox()

	def __PrivateShop_PriceList(self, itemVNum, itemPrice):
		uiPrivateShopBuilder.SetPrivateShopItemPrice(itemVNum, itemPrice)

	def __Horse_HideState(self):
		self.affectShower.SetHorseState(0, 0, 0)

	def __Horse_UpdateState(self, level, health, battery):
		self.affectShower.SetHorseState(int(level), int(health), int(battery))

	def __IsXMasMap(self):
		mapDict = ( "metin2_map_n_flame_01",
					"metin2_map_n_desert_01",
					"metin2_map_spiderdungeon",
					"metin2_map_deviltower1", )

		if background.GetCurrentMapName() in mapDict:
			return False

		return True

	def __XMasSnow_Enable(self, mode):

		self.__XMasSong_Enable(mode)

		if "1"==mode:

			if not self.__IsXMasMap():
				return

			print("XMAS_SNOW ON"
)
			background.EnableSnow(1)

		else:
			print("XMAS_SNOW OFF"
)
			background.EnableSnow(0)

	def __XMasBoom_Enable(self, mode):
		if "1"==mode:

			if not self.__IsXMasMap():
				return

			print("XMAS_BOOM ON"
)
			self.__DayMode_Update("dark")
			self.enableXMasBoom = True
			self.startTimeXMasBoom = app.GetTime()
		else:
			print("XMAS_BOOM OFF"
)
			self.__DayMode_Update("light")
			self.enableXMasBoom = False

	def __XMasTree_Enable(self, grade):

		print("XMAS_TREE ", grade
)
		background.SetXMasTree(int(grade))

	def __XMasSong_Enable(self, mode):
		if "1"==mode:
			print("XMAS_SONG ON"
)

			XMAS_BGM = "xmas.mp3"

			if app.IsExistFile("BGM/" + XMAS_BGM)==1:
				if musicInfo.fieldMusic != "":
					snd.FadeOutMusic("BGM/" + musicInfo.fieldMusic)

				musicInfo.fieldMusic=XMAS_BGM
				snd.FadeInMusic("BGM/" + musicInfo.fieldMusic)

		else:
			print("XMAS_SONG OFF"
)

			if musicInfo.fieldMusic != "":
				snd.FadeOutMusic("BGM/" + musicInfo.fieldMusic)

			musicInfo.fieldMusic=musicInfo.METIN2THEMA
			snd.FadeInMusic("BGM/" + musicInfo.fieldMusic)

	def __RestartDialog_Close(self):
		self.interface.CloseRestartDialog()

	def __Console_Enable(self):
		constInfo.CONSOLE_ENABLE = True
		self.consoleEnable = True
		app.EnableSpecialCameraMode()
		ui.EnablePaste(True)

	def __PrivateShop_Open(self):
		self.interface.OpenPrivateShopInputNameDialog()

	def BINARY_PrivateShop_Appear(self, vid, text):
		self.interface.AppearPrivateShop(vid, text)

	def BINARY_PrivateShop_Disappear(self, vid):
		self.interface.DisappearPrivateShop(vid)

	if app.ENABLE_OFFLINE_SHOP:
		def BINARY_OfflineShop_Appear(self, vid, text):
			uiOfflineShop.AppearOfflineShop(vid, text)

		def BINARY_OfflineShop_Disappear(self, vid):
			uiOfflineShop.DisappearOfflineShop(vid)


	def __PRESERVE_DayMode_Update(self, mode):
		if "light"==mode:
			background.SetEnvironmentData(0)
		elif "dark"==mode:

			if not self.__IsXMasMap():
				return

			background.RegisterEnvironmentData(1, constInfo.ENVIRONMENT_NIGHT)
			background.SetEnvironmentData(1)

	def __DayMode_Update(self, mode):
		if "light"==mode:
			self.curtain.SAFE_FadeOut(self.__DayMode_OnCompleteChangeToLight)
		elif "dark"==mode:

			if not self.__IsXMasMap():
				return

			self.curtain.SAFE_FadeOut(self.__DayMode_OnCompleteChangeToDark)

	def __DayMode_OnCompleteChangeToLight(self):
		background.SetEnvironmentData(0)
		self.curtain.FadeIn()

	def __DayMode_OnCompleteChangeToDark(self):
		background.RegisterEnvironmentData(1, constInfo.ENVIRONMENT_NIGHT)
		background.SetEnvironmentData(1)
		self.curtain.FadeIn()

	def __XMasBoom_Update(self):

		self.BOOM_DATA_LIST = ( (2, 5), (5, 2), (7, 3), (10, 3), (20, 5) )
		if self.indexXMasBoom >= len(self.BOOM_DATA_LIST):
			return

		boomTime = self.BOOM_DATA_LIST[self.indexXMasBoom][0]
		boomCount = self.BOOM_DATA_LIST[self.indexXMasBoom][1]

		if app.GetTime() - self.startTimeXMasBoom > boomTime:

			self.indexXMasBoom += 1

			for i in range(boomCount):
				self.__XMasBoom_Boom()

	def __XMasBoom_Boom(self):
		x, y, z = player.GetMainCharacterPosition()
		randX = app.GetRandom(-150, 150)
		randY = app.GetRandom(-150, 150)

		snd.PlaySound3D(x+randX, -y+randY, z, "sound/common/etc/salute.mp3")

	def __PartyRequestQuestion(self, vid):
		vid = int(vid)
		partyRequestQuestionDialog = uiCommon.QuestionDialog()
		partyRequestQuestionDialog.SetText(chr.GetNameByVID(vid) + localeInfo.PARTY_DO_YOU_ACCEPT)
		partyRequestQuestionDialog.SetAcceptText(localeInfo.UI_ACCEPT)
		partyRequestQuestionDialog.SetCancelText(localeInfo.UI_DENY)
		partyRequestQuestionDialog.SetAcceptEvent(lambda arg=True: self.__AnswerPartyRequest(arg))
		partyRequestQuestionDialog.SetCancelEvent(lambda arg=False: self.__AnswerPartyRequest(arg))
		partyRequestQuestionDialog.Open()
		partyRequestQuestionDialog.vid = vid
		self.partyRequestQuestionDialog = partyRequestQuestionDialog

	def __AnswerPartyRequest(self, answer):
		if not self.partyRequestQuestionDialog:
			return

		vid = self.partyRequestQuestionDialog.vid

		if answer:
			net.SendChatPacket("/party_request_accept " + str(vid))
		else:
			net.SendChatPacket("/party_request_deny " + str(vid))

		self.partyRequestQuestionDialog.Close()
		self.partyRequestQuestionDialog = None

	def __PartyRequestDenied(self):
		self.PopupMessage(localeInfo.PARTY_REQUEST_DENIED)

	def __EnableTestServerFlag(self):
		app.EnableTestServerFlag()

	def __InGameShop_Show(self, url):
		if constInfo.IN_GAME_SHOP_ENABLE:
			self.interface.OpenWebWindow(url)

	def __LoginLover(self):
		if self.interface.wndMessenger:
			self.interface.wndMessenger.OnLoginLover()

	def __LogoutLover(self):
		if self.interface.wndMessenger:
			self.interface.wndMessenger.OnLogoutLover()
		if self.affectShower:
			self.affectShower.HideLoverState()

	def __LoverNear(self):
		if self.affectShower:
			self.affectShower.ShowLoverState()

	def __LoverFar(self):
		if self.affectShower:
			self.affectShower.HideLoverState()

	def __LoverDivorce(self):
		if self.interface.wndMessenger:
			self.interface.wndMessenger.ClearLoverInfo()
		if self.affectShower:
			self.affectShower.ClearLoverState()

	def __PlayMusic(self, flag, filename):
		flag = int(flag)
		if flag:
			snd.FadeOutAllMusic()
			musicInfo.SaveLastPlayFieldMusic()
			snd.FadeInMusic("BGM/" + filename)
		else:
			snd.FadeOutAllMusic()
			musicInfo.LoadLastPlayFieldMusic()
			snd.FadeInMusic("BGM/" + musicInfo.fieldMusic)

	if app.ENABLE_LOADING_PERFORMANCE:
		def OpenWarpShowerWindow(self):
			if self.interface:
				self.interface.OpenWarpShowerWindow()

		def CloseWarpShowerWindow(self):
			if self.interface:
				self.interface.CloseWarpShowerWindow()

	def BINARY_RemoveItemRefreshWindow(self):
		self.interface.wndRemoveItem.ClearWindow()

	if app.ENABLE_RESP_SYSTEM:
		def BINARY_SetMobRespData(self, mobVnum, data):
			self.interface.wndResp.SetMobRespData(mobVnum, data)

		def BINARY_SetMobDropData(self, mobVnum, data):
			self.interface.wndResp.SetMobDropData(mobVnum, data)

		def BINARY_SetMapData(self, data, currentBossCount, maxBossCount, currentMetinCount, maxMetinCount):
			self.interface.wndResp.SetMapData(data, currentBossCount, maxBossCount, currentMetinCount, maxMetinCount)

		def BINARY_RefreshResp(self, id, mobVnum, time, cord):
			self.interface.wndResp.RefreshRest(id, mobVnum, time, cord)

	def SendTitleActiveNow(self, id):
		if self.interface:
			self.interface.ActiveTileNow(id)

	def SendTitleEnable(self, id, val):
		if self.interface:
			self.interface.TitleEnable(id, val)

	def SendOfflineShopLogs(self, id, item, count, price, price2, date, action):
		if self.interface:
			self.interface.OfflineShopLogs(id, item, count, price, price2, date, action)

	def SendAntyExp(self, value):
		constInfo.ANTY_EXP_STATUS = value

	def SendWpadanie(self, value):
		settings.extended_inventory_auto_use = value

	if app.WJ_SPLIT_INVENTORY_SYSTEM:
		def __PressExtendedInventory(self):
			if self.interface:
				self.interface.ToggleExtendedInventoryWindow()

	def SendWeeklyPage(self, page, active, season):
		if active == True:
			if self.interface:
				self.interface.SelectPage(page, season)

	def SendWeeklyInfo(self, pos, name, points, empire, job):
		if self.interface:
			self.interface.SendWeeklyInfo(pos, name, points, empire, job)

	def BINARY_ItemShopOpen(self, dataTime):
		self.interface.wndItemShop.Open(dataTime)

	def BINARY_ItemShopSetEditorFlag(self, flag):
		self.interface.wndItemShop.SetEditorFlag(flag)

	def BINARY_ItemShopRefresh(self):
		self.interface.wndItemShop.RefreshPage()

	def BINARY_ItemShopUpdateCoins(self):
		self.interface.wndItemShop.UpdateCoins()

	def BINARY_ItemShopShowPopup(self, type, id, category):
		self.interface.wndItemShop.ShowPopup(type, id, category)

	def BINARY_TombolaStart(self, pos, to_pos, to_spin, time):
		self.interface.TombolaStart(pos, to_pos, to_spin, time)

	def BINARY_TombolaSpinningItem(self, pos, vnum, count):
		self.interface.TombolaSetSpinningItem(pos, vnum, count)

	def BINARY_TombolaOpen(self):
		self.interface.TombolaOpen()

	def BINARY_TombolaSetPrice(self, group, price, price_type):
		self.interface.TombolaSetPrice(group, price, price_type)

	def BINARY_TombolaSetItem(self, group, vnum, count, chance):
		self.interface.TombolaSetItem(group, vnum, count, chance)

	def BINARY_TombolaClear(self):
		self.interface.TombolaClear()

 
	if app.ENABLE_DROP_INFO:
		if app.ENABLE_DROP_INFO_PCT:
			def BINARY_DropInfoAppendItem(self, mob_vnum, vnum, min_count, max_count, percentage):
				if mob_vnum not in constInfo.dropInfoDict:
					constInfo.dropInfoDict[mob_vnum] = []

				constInfo.dropInfoDict[mob_vnum].append({"vnum": [vnum], "min_count": min_count, "max_count": max_count, "percentage": percentage})
		else:
			def BINARY_DropInfoAppendItem(self, mob_vnum, vnum, min_count, max_count):
				if mob_vnum not in constInfo.dropInfoDict:
					constInfo.dropInfoDict[mob_vnum] = []

				constInfo.dropInfoDict[mob_vnum].append({"vnum": [vnum], "min_count": min_count, "max_count": max_count})
				
		def BINARY_DropInfoRefresh(self, mob_vnum):
			self.targetBoard.DropInfoRefresh(mob_vnum)

		def DropInfoRefresh(self):
			constInfo.dropInfoDict = {}
			self.targetBoard.DropInfoClear()

	if app.ENABLE_ACCE_COSTUME_SYSTEM:
		def ActAcce(self, iAct, bWindow):
			if self.interface:
				self.interface.ActAcce(iAct, bWindow)

		def AlertAcce(self, bWindow):
			snd.PlaySound("sound/ui/make_soket.wav")

		def SendAcceMaterials(self, id, vnum, count):
			if self.interface:
				self.interface.AcceMaterials(id, vnum, count)

	if app.ENABLE_AURA_SYSTEM:
		def ActAura(self, iAct, bWindow):
			if self.interface:
				self.interface.ActAura(iAct, bWindow)

		def AlertAura(self, bWindow):
			snd.PlaySound("sound/ui/make_soket.wav")

	def __OpenItemShop(self):
		self.interface.RequestOpenItemShop()

	if app.BL_MOVE_CHANNEL:
		def __SeverInfo(self, channelNumber, mapIndex):
			
			_chNum	= int(channelNumber.strip())
			_mapIdx	= int(mapIndex.strip())
			
			if _chNum == 99 or _mapIdx >= 10000:
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.MOVE_CHANNEL_NOTICE % 0)
			else:
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.MOVE_CHANNEL_NOTICE % _chNum)
				
			net.SetChannelName(_chNum)
			net.SetMapIndex(_mapIdx)
			self.interface.RefreshServerInfo(channelNumber)
	
	def GetInputOn(self):
		constInfo.INPUT_IGNORE = 1
		
	def GetInputOff(self):
		constInfo.INPUT_IGNORE = 0

	# -- Pet system BINARY callbacks (called from C++ via PyCallClassMemberFunc) --
	def BINARY_PetFullSync(self):
		if self.interface:
			self.interface.OnPetFullSync()

	def BINARY_PetExpUpdate(self):
		if self.interface:
			self.interface.OnPetExpUpdate()

	def BINARY_PetSkillUpdate(self, skill_index):
		if self.interface:
			self.interface.OnPetSkillUpdate(skill_index)

	def BINARY_PetDismissed(self):
		if self.interface:
			self.interface.OnPetDismissed()

	if app.ENABLE_SWITCHBOT:
		def RefreshSwitchbotWindow(self):
			if self.interface:
				self.interface.RefreshSwitchbotWindow()
			
		def RefreshSwitchbotItem(self, slot):
			if self.interface:
				self.interface.RefreshSwitchbotItem(slot)
		
	if app.ENABLE_MINIMAP_DUNGEONINFO:
		def BINARY_SetMiniMapDungeonInfoState(self, state):
			if self.interface:
				self.interface.SetMiniMapDungeonInfo(state)
		
		def BINARY_SetMiniMapDungeonInfoStage(self, cur_stage, max_stage):
			if self.interface:
				self.interface.SetMiniMapDungeonInfoStage(cur_stage, max_stage)
		
		def BINARY_SetMiniMapDungeonInfoGauge(self, gauge_type, value1, value2):
			if self.interface:
				self.interface.SetMiniMapDungeonInfoGauge(gauge_type, value1, value2)
		
		def BINARY_SetMiniMapDungeonInfoNotice(self, notice):
			if self.interface:
				self.interface.SetMiniMapDungeonInfoNotice(notice)

		def BINARY_SetMiniMapDungeonInfoButton(self, status):
			if self.interface:
				self.interface.SetMiniMapDungeonInfoButton(status)

		def BINARY_SetMiniMapDungeonInfoTimer(self, status, time):
			if self.interface:
				self.interface.SetMiniMapDungeonInfoTimer(status, time)

	if app.ENABLE_COLLECT_WINDOW:
		def BINARY_UpdateCollectWindow(self, windowType, time, count, itemVnum, countTotal, chance, rendertargetvnum, questindex, requiredlevel):
			if self.interface.wndCollectWindow:
				self.interface.wndCollectWindow.AddData(windowType, time, count, itemVnum, countTotal, chance, rendertargetvnum, questindex, requiredlevel)
				
		def UpdateTime(self, val, time):
			if self.interface.wndCollectWindow:
				self.interface.wndCollectWindow.SendTime(val, time)

		def UpdateChance(self, val, chance):
			if self.interface.wndCollectWindow:
				self.interface.wndCollectWindow.SendChance(val, chance)

		def __SetCollectWindowQID(self, window, value):
			constInfo.CollectWindowQID[int(window)] = int(value)

		def OpenCollectWindow(self):
			self.interface.ToggleCollectWindow()
		
	if constInfo.GIFT_CODE_SYSTEM:
		def __OpenCodeWindow(self):
			self.interface.OpenGiftCodeWindow()

	if app.ENABLE_SKILL_SELECT_FEATURE:
		def __OpenSkillSelectWindow(self):
			if self.skillSelect:
				self.skillSelect.Open()

	if app.ENABLE_EVENT_MANAGER:
		def ClearEventManager(self):
			self.interface.ClearEventManager()
		def RefreshEventManager(self):
			self.interface.RefreshEventManager()
		def RefreshEventStatus(self, eventID, eventStatus, eventendTime, eventEndTimeText):
			self.interface.RefreshEventStatus(int(eventID), int(eventStatus), int(eventendTime), str(eventEndTimeText))
		def AppendEvent(self, dayIndex, eventID, eventIndex, startTime, endTime, empireFlag, channelFlag, value0, value1, value2, value3, startRealTime, endRealTime, isAlreadyStart):
			self.interface.AppendEvent(int(dayIndex),int(eventID), int(eventIndex), str(startTime), str(endTime), int(empireFlag), int(channelFlag), int(value0), int(value1), int(value2), int(value3), int(startRealTime), int(endRealTime), int(isAlreadyStart))

	if app.TAKE_LEGEND_DAMAGE_BOARD_SYSTEM:
		def SendLegendDamageData(self, vid, pos, name, level, race, empire, damage):
			if self.interface:
				self.interface.SendLegendDamageData(vid, pos, name, level, race, empire, damage)

	if hasattr(app, "ENABLE_PREMIUM_PRIVATE_SHOP_OFFICIAL") and app.ENABLE_PREMIUM_PRIVATE_SHOP_OFFICIAL:
		def OpenPrivateShopPanel(self):
			if self.interface:
				self.interface.OpenPrivateShopPanel()

		def ClosePrivateShopPanel(self):
			if self.interface:
				self.interface.ClosePrivateShopPanel()

		def RefreshPrivateShopWindow(self):
			if self.interface:
				self.interface.RefreshPrivateShopWindow()

		def OpenPrivateShopSearch(self, mode):
			self.interface.OpenPrivateShopSearch(mode)

		def PrivateShopSearchRefresh(self):
			if self.interface:
				self.interface.PrivateShopSearchRefresh()

		def PrivateShopSearchUpdate(self, index, state):
			if self.interface:
				self.interface.PrivateShopSearchUpdate(index, state)

		def AppendMarketItemPrice(self, gold, cheque):
			if self.interface:
				self.interface.AppendMarketItemPrice(gold, cheque)

		def AddPrivateShopTitleBoard(self, vid, text, type):
			if self.interface:
				self.interface.AddPrivateShopTitleBoard(vid, text, type)

		def RemovePrivateShopTitleBoard(self, vid):
			if self.interface:
				self.interface.RemovePrivateShopTitleBoard(vid)

		def SetPrivateShopPremiumBuild(self):
			if self.interface:
				self.interface.SetPrivateShopPremiumBuild()

		def PrivateShopStateUpdate(self):
			if self.interface:
				self.interface.PrivateShopStateUpdate()

	def BINARY_BattlePassInit(self):
		self.interface._EnsureBattlePass().RefreshGlobal()

	def BINARY_BattlePassUpdate(self):
		self.interface._EnsureBattlePass().RefreshLocal()
		
	if app.__ENABLE_POLYMORPH_SYSTEM__:
		def BINARY_PolySystem(self, polyStages, polySkins):
			self.interface.wndPolySystem.AppendStages(polyStages)
			self.interface.wndPolySystem.AppendSkins(polySkins)
			self.interface.wndPolySystem.Refresh()

		def BINARY_PolySkinOpen(self):
			self.interface.wndPolySystem.Open()

		def BINARY_PolySkinRefresh(self):
			self.interface.wndPolySystem.RefreshSkins()

		def BINARY_PolySkinForceClose(self):
			self.interface.wndPolySystem.CloseByServer()
		
	def OnCubeOpen(self, recipes):
		self.interface.OpenCubeWindow()
		
		cube = self.interface.GetCubeWindow()
		for recipe in recipes:
			cube.AddRecipe(uiCube.Recipe.CreateFromServer(recipe))
		
		cube.Refresh()
	
	def OnCubeUpdate(self, gold, priceCheque, priceAchievement, chance):
		self.interface.GetCubeWindow().OnUpdateInfo(gold, priceCheque, priceAchievement, chance)
	
	def OnCubeClose(self):
		self.interface.CloseCubeWindow()

	def __RecvCasketItem(self, base_vnum, vnum, count):
		if self.interface and self.interface.wndCasketPreview:
			self.interface.wndCasketPreview.AddItem(int(base_vnum), int(vnum), int(count))

	def __RecvCasketBuild(self):
		if self.interface and self.interface.wndCasketPreview:
			self.interface.wndCasketPreview.Build()

	if app.TEAM_MEMBER_STATUS:
		def __UpdateDungeonDailyCount(self, mapIdx, count):
			import uidungeontrack
			uidungeontrack.UpdateDailyCount(int(mapIdx), int(count))

		def __BINARY__UpdateTeamMemberStatus(self, sName, sLang, bStatus):
			print("Team member status: Name:", sName, "lang:", sLang, "status:", bStatus
)
			self.interface.wndMessenger.CheckoutTeamMemberStatus(sName, sLang, int(bStatus))

		def __BINARY__ClearTeamMemberList(self):
			print("Team member clear"
)
			self.interface.wndMessenger.ClearTeamMemberList()
			

	if app.ENABLE_SAVE_LOCATION_SYSTEM:
		def BINARY_UpdateSaveLocation(self, pos, name, x, y):
			self.interface.UpdateSaveLocation(pos, name, x, y)

		def BINARY_DelSaveLocation(self, pos):
			self.interface.DeleteSaveLocation(pos)

	if app.ENABLE_OFFLINE_SHOP:
		def OpenPrivateShopBuilder(self):
			if self.interface.wndShopOffline:
				if self.interface.wndShopOffline.IsShow() == False or self.interface.wndShopOffline.wBoard[3].IsShow():
					self.interface.wndShopOffline.Open()
				else:
					self.interface.wndShopOffline.Close()

		def OpenShopSearch(self):
			if self.interface.wndShopSearch:
				if not self.interface.wndShopSearch.IsShow():
					self.interface.wndShopSearch.Show()
				else:
					self.interface.wndShopSearch.Close()

	def OpenPrivateMessage(self, name):
		self.interface.OpenWhisperDialog(name)


	if app.ENABLE_BOT_CONTROL:
		# O captchy decyduje wylacznie serwer - klient dostaje gotowe wyzwanie
		# i odsyla klikniety indeks. Nierozwiazane wyzwanie wraca po relogu.
		def BINARY_BotControlOpen(self, challengeID, iconSet, imageMask, seconds):
			if not self.botControlWnd:
				self.botControlWnd = uisecurity.FindTheDifferentCaptcha()

			if not self.botControlWnd:
				return

			# Po relogu wyzwanie potrafi przyjsc zaraz po wejsciu do gry,
			# zanim interface zdazy sie w pelni zbudowac.
			self.EndExchange()

			if self.interface:
				self.interface.CommandCloseSafebox()

			self.botControlWnd.Open(challengeID, iconSet, imageMask, seconds)

		def BINARY_BotControlSolved(self):
			if self.botControlWnd:
				self.botControlWnd.OnAnswerAccepted()

		def BINARY_BotControlWrong(self):
			if self.botControlWnd:
				self.botControlWnd.OnAnswerRejected()

		def isBotControlActive(self):
			if self.botControlWnd:
				return self.botControlWnd.IsShow()

			return False


	def ServerRankLoadInfo(self, info):
		self.rankingWindow.RecvLoadInfo(info)

	def ServerRankLoadMyPos(self, catIdx, position, value):
		self.rankingWindow.RecvLoadMyPosition(int(position), int(value))

	def ServerRankLoadData(self, pName, level, raceWithskillGroup, empire, value):
		self.rankingWindow.RecvLoadData(pName, level, raceWithskillGroup, empire, value)

	def RankLoadInfo(self, info, sundayEndTime):
		self.weeklyRankingWindow.RecvLoadInfo(info, int(sundayEndTime))

	def RankLoadMyPos(self, catIdx, position, value):
		self.weeklyRankingWindow.RecvLoadMyPosition(int(position), int(value))

	def RankLoadData(self, pName, level, race, value):
		chat.AppendChat(1, "pName = %s, level = %d, race = %s, value = %d" % (pName, level, race, value))
		self.weeklyRankingWindow.RecvLoadData(pName, level, race, value)

	if app.ENABLE_SECONDARY_LEVEL:
		def __SecondaryLevel_Open(self):
			self.interface.ToggleSecondaryLevel()
			
	def EnlightenmentWindowOpen(self):
		if self.enlightWindow == None:
			self.enlightWindow = uiEnlightenment.EnlightenmentWindow()
		self.enlightWindow.OpenWindow()

	def EnlightenmentWindowRefresh(self):
		if self.enlightWindow == None:
			self.enlightWindow = uiEnlightenment.EnlightenmentWindow()
		self.enlightWindow.RefreshWindow()

	def EnlightenmentUpgradeNotice(self, name, level):
		if self.enlightWindow == None:
			self.enlightWindow = uiEnlightenment.EnlightenmentWindow()
		self.enlightWindow.OpenNoticeUpgradeBoard(name, int(level))
	
	def SetMyOreCount(self, count):
		constInfo.MY_ORE_COUNT = int(count)

	def SetMyFishCount(self, count):
		constInfo.MY_FISH_COUNT = int(count)

	def SetMyOreFishCount(self, countOre, countFish):
		constInfo.MY_ORE_COUNT = int(countOre)
		constInfo.MY_FISH_COUNT = int(countFish)
		
	def FishWiki_ConfigStart(self, fishCount, categoriesPerRow):
		self.fishWikiWindow.on_config_start(int(fishCount), int(categoriesPerRow))

	def FishWiki_ConfigFish(self, vnum, neededCount, neededLength, successChance, rewardType, rewardValue):
		self.fishWikiWindow.on_config_fish(int(vnum), int(neededCount), int(neededLength), int(successChance), int(rewardType), int(rewardValue))

	def FishWiki_ConfigEnd(self):
		self.fishWikiWindow.on_config_end()

	def FishWiki_NewFishUnlocked(self, fishVnum):
		self.fishWikiWindow.OnUnlockNewFish(int(fishVnum))

	def FishWiki_UnlockStatus(self, unlockStatus1, unlockStatus2):
		self.fishWikiWindow.OnLoadUnlockStatus(int(unlockStatus1), int(unlockStatus2))

	def FishWiki_FishData(self, fishVnum, myGetCount, bestLength, bestPrice, missionGivedCount):
		self.fishWikiWindow.OnLoadMyFishData(int(fishVnum), int(myGetCount), int(bestLength), int(bestPrice), int(missionGivedCount))

	def FishWiki_RankLoadStart(self):
		self.fishWikiWindow.OnLoadRankingStart()

	def FishWiki_RankLoadData(self, pos, name, length, rodLevel):
		self.fishWikiWindow.OnLoadRanking(int(pos), name, int(length), int(rodLevel))

	def FishWiki_RankLoadEnd(self):
		self.fishWikiWindow.OnLoadRankingEnd()

	def FishWiki_LoadError(self, status=""):
		self.fishWikiWindow.OnLoadError(status)	
		
	if app.ENABLE_MOUNT_SYSTEM:
		def BINARY_SetMountInfo(self, vnum, name, level, exp, req_exp, summoned):
			constInfo.MOUNT_LEVEL = level
			try:
				self.interface.wndMountWindow.SetBasicInfo(vnum, name, level, exp, req_exp, summoned)
			except Exception as e:
				import dbg
				dbg.TraceError("BINARY_SetMountInfo ERROR (vnum=%s level=%s): %s" % (str(vnum), str(level), str(e)))
	def ToggleMapWindow(self):
		try:
			self.interface.ToggleMapWindow()
		except:
			pass
