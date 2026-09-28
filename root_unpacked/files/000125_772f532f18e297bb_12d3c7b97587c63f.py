# -*- coding: utf-8 -*-
import chr
import grp
import app
import math
import wndMgr
import snd
import net
import systemSetting
import localeInfo
import logging
import player
import ui
import musicInfo
import playerSettingModule
import uiCommon
import chat

from utility import MakeEvent, Event

LEAVE_BUTTON_FOR_POTAL = False
NOT_NEED_DELETE_CODE = False
ENABLE_ENGNUM_DELETE_CODE = True


def unsigned32(n):
	return n & 0xFFFFFFFF


class SelectCharacterWindow(ui.Window):

	SLOT_ROTATION = [135.0, 225.0, 315.0, 45.0]
	SLOT_COUNT = 4
	CHARACTER_TYPE_COUNT = 4

	EMPIRE_NAME = {1: localeInfo.SELECT_EMPIRE_SHINSOO, 2: localeInfo.SELECT_EMPIRE_CHUNJO, 3: localeInfo.SELECT_EMPIRE_JINNO}

	class CharacterRenderer(ui.Window):
		def OnRender(self):
			grp.ClearDepthBuffer()
			grp.SetGameRenderState()
			grp.PushState()
			grp.SetOmniLight()

			screenWidth = wndMgr.GetScreenWidth()
			screenHeight = wndMgr.GetScreenHeight()
			newScreenWidth = float(screenWidth - 270)
			newScreenHeight = float(screenHeight)

			# board is on the LEFT (~270px) - render the character to the right of it
			grp.SetViewport(270.0 / screenWidth, 0.0, newScreenWidth / screenWidth, newScreenHeight / screenHeight)

			app.SetCenterPosition(0.0, 0.0, 0.0)
			app.SetCamera(1550.0, 15.0, 180.0, 95.0)
			grp.SetPerspective(10.0, newScreenWidth / newScreenHeight, 1000.0, 3000.0)

			(x, y) = app.GetCursorPosition()
			grp.SetCursorPosition(x, y)

			chr.Deform()
			chr.Render()

			grp.RestoreViewport()
			grp.PopState()
			grp.SetInterfaceRenderState()

	def __init__(self, stream):
		ui.Window.__init__(self)
		net.SetPhaseWindow(net.PHASE_WINDOW_SELECT, self)

		self.stream = stream
		self.slot = self.stream.GetCharacterSlot()

		self.openLoadingFlag = False
		self.startIndex = -1
		self.startReservingTime = 0

		self.curRotation = []
		self.destRotation = []
		self.jobsLocale = [
			localeInfo.SELECT_WARRIOR,
			localeInfo.SELECT_ASSASSIN,
			localeInfo.SELECT_SURA,
			localeInfo.SELECT_SHAMAN,
		]
		for rot in self.SLOT_ROTATION:
			self.curRotation.append(rot)
			self.destRotation.append(rot)

		self.curGauge = [0.0, 0.0, 0.0, 0.0]
		self.destGauge = [0.0, 0.0, 0.0, 0.0]

		self.dlgBoard = 0
		self.dlgQuestion = None
		self.dlgQuestionText = None
		self.dlgQuestionAcceptButton = None
		self.dlgQuestionCancelButton = None
		self.changeNameFlag = False
		self.nameInputBoard = None
		self.sendedChangeNamePacket = False
		self.privateInputBoard = None
		self.isLoad = 0
		self.changingPhase = False

		# UI elements - initialized here so they always exist
		self.btnStart = None
		self.btnCreate = None
		self.btnDelete = None
		self.btnExit = None
		self.btnLeft = None
		self.btnRight = None
		self.CharName = None
		self.CharLevel = None
		self.PlayTime = None
		self.GuildName = None
		self.empireName = None
		self.GaugeList = []
		self.GaugeListVal = []
		self.nameImages = {}
		self.flagImages = {}
		self.backGround = None
		self.chrRenderer = None

	def __del__(self):
		ui.Window.__del__(self)
		net.SetPhaseWindow(net.PHASE_WINDOW_SELECT, 0)

	def Open(self):
		net.SetPhaseWindow(net.PHASE_WINDOW_SELECT, self)

		if not self.__LoadBoardDialog("uiScript/selectcharacterwindow.py"):
			logging.warning("SelectCharacterWindow.Open - __LoadScript Error")
			return False

		if not self.__LoadQuestionDialog("uiScript/questiondialog.py"):
			return

		if not app.ENABLE_PERFORMANCE_IMPROVEMENTS_NEW:
			playerSettingModule.LoadGameData("INIT")

		self.InitCharacterBoard()

		if self.btnStart:
			self.btnStart.Enable()
		if self.btnCreate:
			self.btnCreate.Enable()
		if self.btnDelete:
			self.btnDelete.Enable()
		if self.btnExit:
			self.btnExit.Enable()

		self.SetSize(wndMgr.GetScreenWidth(), wndMgr.GetScreenHeight())
		self.SetPosition(0, 0)
		if self.dlgBoard:
			self.dlgBoard.Show()
		self.SetWindowName("SelectCharacterWindow")
		self.Show()
		self.SetFocus()

		if musicInfo.selectMusic != "":
			snd.SetMusicVolume(systemSetting.GetMusicVolume())
			snd.FadeInMusic("BGM/" + musicInfo.selectMusic)

		app.SetCenterPosition(0.0, 0.0, 0.0)
		app.SetCamera(1550.0, 15.0, 180.0, 95.0)

		self.isLoad = 1
		self.Refresh()

		# Select first existing character (or empty slot 0 -> create mode)
		selected = False
		for index in range(4):
			charId = net.GetAccountCharacterSlotDataInteger(index, net.ACCOUNT_CHARACTER_SLOT_ID)
			if charId:
				self.SelectSlot(index)
				selected = True
				break
		if not selected:
			self.SelectSlot(0)

		if self.stream.isAutoSelect:
			chrSlot = self.stream.GetCharacterSlot()
			self.SelectSlot(chrSlot)
			self.StartGame()

		self.SetEmpire(net.GetEmpireID())
		app.ShowCursor()

		if app.__AUTO_HUNT__:
			import constInfo
			if constInfo.autoHuntAutoLoginDict["status"] == 1 and constInfo.autoHuntAutoLoginDict["leftTime"] == -1:
				constInfo.autoHuntAutoLoginDict["leftTime"] = app.GetGlobalTimeStamp() + 2
				self.SelectSlot(constInfo.autoHuntAutoLoginDict["slot"])

	def Close(self):
		if musicInfo.selectMusic != "":
			snd.FadeOutMusic("BGM/" + musicInfo.selectMusic)

		self.stream.popupWindow.Close()

		if self.dlgBoard:
			self.dlgBoard.ClearDictionary()

		self.empireName = None
		self.dlgBoard = None
		self.btnStart = None
		self.btnCreate = None
		self.btnDelete = None
		self.btnExit = None
		self.btnLeft = None
		self.btnRight = None
		self.backGround = None
		self.chrRenderer = None
		self.CharName = None
		self.CharLevel = None
		self.PlayTime = None
		self.GuildName = None
		self.GaugeList = []
		self.GaugeListVal = []
		self.nameImages = {}
		self.flagImages = {}

		if self.dlgQuestion:
			self.dlgQuestion.ClearDictionary()
		self.dlgQuestion = None
		self.dlgQuestionText = None
		self.dlgQuestionAcceptButton = None
		self.dlgQuestionCancelButton = None
		self.privateInputBoard = None
		self.nameInputBoard = None

		for i in range(self.SLOT_COUNT):
			chr.DeleteInstance(i)

		self.Hide()
		self.KillFocus()
		app.HideCursor()

	def SetEmpire(self, id):
		# show only the matching empire flag (1=Shinsoo/A, 2=Chunjo/B, 3=Jinno/C)
		for flagId, flagImg in self.flagImages.items():
			if not flagImg:
				continue
			if flagId == id:
				flagImg.Show()
			else:
				flagImg.Hide()
		if self.empireName:
			self.empireName.SetText(self.EMPIRE_NAME.get(id, localeInfo.SELECT_NOT_CHOSEN))

	def Refresh(self):
		if not self.isLoad:
			return

		for index in range(4):
			id = net.GetAccountCharacterSlotDataInteger(index, net.ACCOUNT_CHARACTER_SLOT_ID)
			race = net.GetAccountCharacterSlotDataInteger(index, net.ACCOUNT_CHARACTER_SLOT_RACE)
			form = net.GetAccountCharacterSlotDataInteger(index, net.ACCOUNT_CHARACTER_SLOT_FORM)
			name = net.GetAccountCharacterSlotDataString(index, net.ACCOUNT_CHARACTER_SLOT_NAME)
			hair = net.GetAccountCharacterSlotDataInteger(index, net.ACCOUNT_CHARACTER_SLOT_HAIR)
			acce = net.GetAccountCharacterSlotDataInteger(index, net.ACCOUNT_CHARACTER_SLOT_ACCE)

			if id:
				self.MakeCharacter(index, id, name, race, form, hair, acce)
				self.SelectSlot(index)

		self.SelectSlot(self.slot)

	def GetCharacterSlotID(self, slotIndex):
		return net.GetAccountCharacterSlotDataInteger(slotIndex, net.ACCOUNT_CHARACTER_SLOT_ID)

	def __LoadQuestionDialog(self, fileName):
		self.dlgQuestion = ui.ScriptWindow()

		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self.dlgQuestion, fileName)
		except:
			logging.warning("SelectCharacterWindow.LoadQuestionDialog.LoadScript")

		try:
			GetObject = self.dlgQuestion.GetChild
			self.dlgQuestionText = GetObject("message")
			self.dlgQuestionAcceptButton = GetObject("accept")
			self.dlgQuestionCancelButton = GetObject("cancel")
		except:
			logging.warning("SelectCharacterWindow.LoadQuestionDialog.BindObject")

		self.dlgQuestionText.SetText(localeInfo.SELECT_DO_YOU_DELETE_REALLY)
		self.dlgQuestionAcceptButton.SetEvent(MakeEvent(self.RequestDeleteCharacter))
		self.dlgQuestionCancelButton.SetEvent(MakeEvent(self.dlgQuestion.Hide))
		return 1

	def __Bind(self, GetObject, name):
		try:
			return GetObject(name)
		except:
			logging.warning("SelectCharacterWindow: %s not found", name)
			return None

	def __LoadBoardDialog(self, fileName):
		self.dlgBoard = ui.ScriptWindow()
		self.dlgBoard.SetParent(self)

		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self.dlgBoard, fileName)
		except:
			logging.warning("SelectCharacterWindow.LoadBoardDialog.LoadScript")
			import traceback
			traceback.print_exc()

		GetObject = self.dlgBoard.GetChild

		self.backGround = self.__Bind(GetObject, "BackGround")

		# buttons
		self.btnStart = self.__Bind(GetObject, "start_button")
		self.btnCreate = self.__Bind(GetObject, "create_button")
		# uiScriptLocale.SELECT_CREATE is repurposed to "Utworz sklep offline" in the
		# kowal locale, so set the create-character label from a clean localeInfo key.
		if self.btnCreate:
			self.btnCreate.SetText(localeInfo.CHARACTER_CREATE_MODE)
		self.btnDelete = self.__Bind(GetObject, "delete_button")
		self.btnExit = self.__Bind(GetObject, "exit_button")
		self.btnLeft = self.__Bind(GetObject, "left_button")
		self.btnRight = self.__Bind(GetObject, "right_button")

		# texts
		self.CharName = self.__Bind(GetObject, "character_name_value")
		self.CharLevel = self.__Bind(GetObject, "character_level_value")
		self.PlayTime = self.__Bind(GetObject, "character_play_time_value")
		self.GuildName = self.__Bind(GetObject, "GuildName")
		self.empireName = self.__Bind(GetObject, "EmpireName")

		# class name banners (S3ll graphics) + empire flags
		self.nameImages = {
			0: self.__Bind(GetObject, "name_warrior"),
			1: self.__Bind(GetObject, "name_assassin"),
			2: self.__Bind(GetObject, "name_sura"),
			3: self.__Bind(GetObject, "name_shaman"),
		}
		self.flagImages = {
			1: self.__Bind(GetObject, "EmpireFlag_A"),
			2: self.__Bind(GetObject, "EmpireFlag_B"),
			3: self.__Bind(GetObject, "EmpireFlag_C"),
		}
		self.__ShowClassName(-1)
		for flagImg in self.flagImages.values():
			if flagImg:
				flagImg.Hide()

		# gauges + value texts
		self.GaugeList = []
		self.GaugeListVal = []
		for gaugeName, valName in [("gauge_hth", "character_hth_value"), ("gauge_int", "character_int_value"), ("gauge_str", "character_str_value"), ("gauge_dex", "character_dex_value")]:
			self.GaugeList.append(self.__Bind(GetObject, gaugeName))
			self.GaugeListVal.append(self.__Bind(GetObject, valName))

		# events
		if self.btnStart:
			self.btnStart.SetEvent(MakeEvent(self.StartGame))
		if self.btnCreate:
			self.btnCreate.SetEvent(MakeEvent(self.CreateCharacter))
		if self.btnExit:
			self.btnExit.SetEvent(MakeEvent(self.ExitSelect))
		if self.btnLeft:
			self.btnLeft.SetEvent(MakeEvent(self.PrevSlot))
		if self.btnRight:
			self.btnRight.SetEvent(MakeEvent(self.NextSlot))
		if self.btnDelete:
			if NOT_NEED_DELETE_CODE:
				self.btnDelete.SetEvent(MakeEvent(self.PopupDeleteQuestion))
			else:
				self.btnDelete.SetEvent(MakeEvent(self.InputPrivateCode))

		if self.backGround:
			self.chrRenderer = self.CharacterRenderer()
			self.chrRenderer.SetParent(self.backGround)
			self.chrRenderer.Show()

		return 1

	def __ShowClassName(self, job):
		for j, img in self.nameImages.items():
			if not img:
				continue
			if j == job:
				img.Show()
			else:
				img.Hide()

	def __SetButtonMode(self, hasChar):
		if hasChar:
			if self.btnStart:
				self.btnStart.Show()
			if self.btnCreate:
				self.btnCreate.Hide()
			if self.btnDelete:
				self.btnDelete.Show()
		else:
			if self.btnStart:
				self.btnStart.Hide()
			if self.btnCreate:
				self.btnCreate.Show()
			if self.btnDelete:
				self.btnDelete.Hide()

	def SameLoginDisconnect(self):
		self.stream.popupWindow.Close()
		self.stream.popupWindow.Open(localeInfo.LOGIN_FAILURE_SAMELOGIN, self.BackSelect, localeInfo.UI_OK)

	def MakeCharacter(self, index, id, name, race, form, hair, acce):
		if 0 == id:
			return

		chr.CreateInstance(index)
		chr.SelectInstance(index)
		chr.SetVirtualID(index)
		chr.SetNameString(name)
		chr.SetRace(race)
		chr.SetArmor(form)
		chr.SetHair(hair)
		chr.SetAcce(acce)
		chr.Refresh()
		chr.SetMotionMode(chr.MOTION_MODE_GENERAL)
		chr.SetLoopMotion(chr.MOTION_INTRO_WAIT)
		chr.SetRotation(0.0)

	def StartGame(self):
		if self.sendedChangeNamePacket:
			return

		if self.changeNameFlag:
			self.OpenChangeNameDialog()
			return

		if -1 != self.startIndex:
			return

		if 0 == self.GetCharacterSlotID(self.slot):
			return

		if musicInfo.selectMusic != "":
			snd.FadeLimitOutMusic("BGM/" + musicInfo.selectMusic, systemSetting.GetMusicVolume() * 0.05)

		if self.btnStart:
			self.btnStart.SetUp()
			self.btnStart.Disable()
		if self.btnCreate:
			self.btnCreate.Disable()
		if self.btnDelete:
			self.btnDelete.SetUp()
			self.btnDelete.Disable()
		if self.btnExit:
			self.btnExit.SetUp()
			self.btnExit.Disable()

		if self.dlgQuestion:
			self.dlgQuestion.Hide()

		self.stream.SetCharacterSlot(self.slot)

		self.startIndex = self.slot
		self.startReservingTime = app.GetTime()

		for i in range(self.SLOT_COUNT):
			if False == chr.HasInstance(i):
				continue

			chr.SelectInstance(i)
			if i == self.slot:
				chr.PushOnceMotion(chr.MOTION_INTRO_SELECTED, 0.1)
				continue

			chr.PushOnceMotion(chr.MOTION_INTRO_NOT_SELECTED, 0.1)

	def PrevSlot(self):
		self.SelectSlot((self.slot - 1 + self.SLOT_COUNT) % self.SLOT_COUNT)

	def NextSlot(self):
		self.SelectSlot((self.slot + 1) % self.SLOT_COUNT)

	def onExistingCharClick(self, slotIndex, create=False):
		self.SelectSlot(slotIndex)
		if create:
			self.CreateCharacter()

	def OpenChangeNameDialog(self):
		nameInputBoard = uiCommon.InputDialogWithDescription()
		nameInputBoard.SetTitle(localeInfo.SELECT_CHANGE_NAME_TITLE)
		nameInputBoard.SetAcceptEvent(MakeEvent(self.AcceptInputName))
		nameInputBoard.SetCancelEvent(MakeEvent(self.CancelInputName))
		nameInputBoard.SetMaxLength(chr.PLAYER_NAME_MAX_LEN)
		nameInputBoard.SetBoardWidth(200)
		nameInputBoard.SetDescription(localeInfo.SELECT_INPUT_CHANGING_NAME)
		nameInputBoard.Open()
		nameInputBoard.slot = self.slot
		self.nameInputBoard = nameInputBoard

	def OnChangeName(self, id, name):
		self.SelectSlot(id)
		self.sendedChangeNamePacket = False
		self.PopupMessage(localeInfo.SELECT_CHANGED_NAME)

	def AcceptInputName(self):
		changeName = self.nameInputBoard.GetText()
		if not changeName:
			return

		self.sendedChangeNamePacket = True
		net.SendChangeNamePacket(self.nameInputBoard.slot, changeName)
		return self.CancelInputName()

	def CancelInputName(self):
		if self.nameInputBoard:
			self.nameInputBoard.Close()
			self.nameInputBoard = None
		return True

	def OnCreateFailure(self, type):
		self.sendedChangeNamePacket = False
		if 0 == type:
			self.PopupMessage(localeInfo.SELECT_CHANGE_FAILURE_STRANGE_NAME)
		elif 1 == type:
			self.PopupMessage(localeInfo.SELECT_CHANGE_FAILURE_ALREADY_EXIST_NAME)
		elif 100 == type:
			self.PopupMessage(localeInfo.SELECT_CHANGE_FAILURE_STRANGE_INDEX)

	def CreateCharacter(self):
		if self.changingPhase:
			return
		id = self.GetCharacterSlotID(self.slot)
		if 0 == id:
			self.changingPhase = True
			self.stream.SetCharacterSlot(self.slot)
			EMPIRE_MODE = 1
			if EMPIRE_MODE:
				if self.__AreAllSlotEmpty():
					self.stream.SetReselectEmpirePhase()
				else:
					self.stream.SetCreateCharacterPhase()
			else:
				self.stream.SetCreateCharacterPhase()

	def __AreAllSlotEmpty(self):
		for iSlot in range(self.SLOT_COUNT):
			if 0 != net.GetAccountCharacterSlotDataInteger(iSlot, net.ACCOUNT_CHARACTER_SLOT_ID):
				return 0
		return 1

	def PopupDeleteQuestion(self):
		id = self.GetCharacterSlotID(self.slot)
		if 0 == id:
			return
		if self.dlgQuestion:
			self.dlgQuestion.Show()
			self.dlgQuestion.SetTop()

	def RequestDeleteCharacter(self):
		if self.dlgQuestion:
			self.dlgQuestion.Hide()
		id = self.GetCharacterSlotID(self.slot)
		if 0 == id:
			self.PopupMessage(localeInfo.SELECT_EMPTY_SLOT)
			return
		net.SendDestroyCharacterPacket(self.slot, "1234567")
		self.PopupMessage(localeInfo.SELECT_DELEING)

	def InputPrivateCode(self):
		id = self.GetCharacterSlotID(self.slot)
		if 0 == id:
			return
		privateInputBoard = uiCommon.InputDialogWithDescription()
		privateInputBoard.SetTitle(localeInfo.INPUT_PRIVATE_CODE_DIALOG_TITLE)
		privateInputBoard.SetAcceptEvent(MakeEvent(self.AcceptInputPrivateCode))
		privateInputBoard.SetCancelEvent(MakeEvent(self.CancelInputPrivateCode))
		if ENABLE_ENGNUM_DELETE_CODE:
			pass
		else:
			privateInputBoard.SetNumberMode()
		privateInputBoard.SetSecretMode()
		privateInputBoard.SetMaxLength(7)
		privateInputBoard.SetBoardWidth(250)
		privateInputBoard.SetDescription(localeInfo.INPUT_PRIVATE_CODE_DIALOG_DESCRIPTION)
		privateInputBoard.Open()
		self.privateInputBoard = privateInputBoard

	def AcceptInputPrivateCode(self):
		privateCode = self.privateInputBoard.GetText()
		if not privateCode:
			return

		id = self.GetCharacterSlotID(self.slot)
		if 0 == id:
			self.PopupMessage(localeInfo.SELECT_EMPTY_SLOT)
			return

		net.SendDestroyCharacterPacket(self.slot, privateCode)
		self.PopupMessage(localeInfo.SELECT_DELEING)
		self.CancelInputPrivateCode()
		return True

	def CancelInputPrivateCode(self):
		self.privateInputBoard = None
		return True

	def OnDeleteSuccess(self, slot):
		self.PopupMessage(localeInfo.SELECT_DELETED)
		self.DeleteCharacter(slot)

	def OnDeleteFailure(self):
		self.PopupMessage(localeInfo.SELECT_CAN_NOT_DELETE)

	def DeleteCharacter(self, index):
		chr.DeleteInstance(index)
		self.SelectSlot(self.slot)

	def BackSelect(self):
		if self.dlgQuestion:
			self.dlgQuestion.Hide()
		if LEAVE_BUTTON_FOR_POTAL:
			if app.loggined:
				self.stream.SetPhaseWindow(0)
			else:
				self.stream.SetLoginPhase()
		else:
			self.stream.SetLoginPhase()
		self.Hide()

	def ExitSelect(self):
		self.BackSelect()

	def GetSlotIndex(self):
		return self.slot

	def SelectSlot(self, index):
		if index < 0:
			return
		if index >= self.SLOT_COUNT:
			return

		self.slot = index
		chr.SelectInstance(self.slot)

		for i in range(self.SLOT_COUNT):
			self.destRotation[(i + self.slot) % self.SLOT_COUNT] = self.SLOT_ROTATION[i]

		self.destGauge = [0.0, 0.0, 0.0, 0.0]

		id = net.GetAccountCharacterSlotDataInteger(self.slot, net.ACCOUNT_CHARACTER_SLOT_ID)
		if 0 != id:
			playTime = net.GetAccountCharacterSlotDataInteger(self.slot, net.ACCOUNT_CHARACTER_SLOT_PLAYTIME)
			level = net.GetAccountCharacterSlotDataInteger(self.slot, net.ACCOUNT_CHARACTER_SLOT_LEVEL)
			race = net.GetAccountCharacterSlotDataInteger(self.slot, net.ACCOUNT_CHARACTER_SLOT_RACE)
			valueHTH = net.GetAccountCharacterSlotDataInteger(self.slot, net.ACCOUNT_CHARACTER_SLOT_HTH)
			valueINT = net.GetAccountCharacterSlotDataInteger(self.slot, net.ACCOUNT_CHARACTER_SLOT_INT)
			valueSTR = net.GetAccountCharacterSlotDataInteger(self.slot, net.ACCOUNT_CHARACTER_SLOT_STR)
			valueDEX = net.GetAccountCharacterSlotDataInteger(self.slot, net.ACCOUNT_CHARACTER_SLOT_DEX)
			name = net.GetAccountCharacterSlotDataString(self.slot, net.ACCOUNT_CHARACTER_SLOT_NAME)
			guildName = net.GetAccountCharacterSlotDataString(self.slot, net.ACCOUNT_CHARACTER_SLOT_GUILD_NAME)
			self.changeNameFlag = net.GetAccountCharacterSlotDataInteger(self.slot, net.ACCOUNT_CHARACTER_SLOT_CHANGE_NAME_FLAG)

			job = chr.RaceToJob(race)
			self.__ShowClassName(job)

			if self.CharName:
				self.CharName.SetText(name)
			if self.CharLevel:
				self.CharLevel.SetText(str(level))
			if self.PlayTime:
				self.PlayTime.SetText(localeInfo.MinuteToHM(playTime))
			if self.GuildName:
				if guildName:
					self.GuildName.SetText(guildName)
				else:
					self.GuildName.SetText(localeInfo.SELECT_NOT_JOIN_GUILD)

			statesSummary = float(valueHTH + valueINT + valueSTR + valueDEX)
			if statesSummary > 0.0:
				self.destGauge = [
					float(valueHTH) / 90,
					float(valueINT) / 90,
					float(valueSTR) / 90,
					float(valueDEX) / 90,
				]

			self.__SetButtonMode(True)
		else:
			self.__ShowClassName(-1)
			self.InitCharacterBoard()
			self.__SetButtonMode(False)

	def InitCharacterBoard(self):
		if self.CharName:
			self.CharName.SetText("")
		if self.CharLevel:
			self.CharLevel.SetText("")
		if self.PlayTime:
			self.PlayTime.SetText("")
		if self.GuildName:
			self.GuildName.SetText(localeInfo.SELECT_NOT_JOIN_GUILD)
		for i in range(len(self.GaugeListVal)):
			if self.GaugeListVal[i]:
				self.GaugeListVal[i].SetText("0")

	def OnKeyUp(self, key):
		return True

	def OnKeyDown(self, key):
		if key == app.DIK_ESCAPE:
			return self.OnPressEscapeKey()

		if key == app.DIK_RETURN or key == app.DIK_NUMPADENTER:
			id = net.GetAccountCharacterSlotDataInteger(self.slot, net.ACCOUNT_CHARACTER_SLOT_ID)
			if 0 == id:
				self.CreateCharacter()
			else:
				self.StartGame()
			return True

		if key == app.DIK_LEFT or key == app.DIK_UP:
			self.PrevSlot()
			return True

		if key == app.DIK_RIGHT or key == app.DIK_DOWN:
			self.NextSlot()
			return True

		if key == app.DIK_1:
			self.SelectSlot(0)
			return True
		if key == app.DIK_2:
			self.SelectSlot(1)
			return True
		if key == app.DIK_3:
			self.SelectSlot(2)
			return True
		if key == app.DIK_4:
			self.SelectSlot(3)
			return True

		return True

	def OnUpdate(self):
		if app.__AUTO_HUNT__:
			import constInfo
			if constInfo.autoHuntAutoLoginDict["status"] == 1 and constInfo.autoHuntAutoLoginDict["leftTime"] > 0 and constInfo.autoHuntAutoLoginDict["leftTime"] < app.GetGlobalTimeStamp():
				constInfo.autoHuntAutoLoginDict["leftTime"] = -2
				self.SelectSlot(constInfo.autoHuntAutoLoginDict["slot"])
				self.StartGame()

		chr.Update()

		valueHTH = net.GetAccountCharacterSlotDataInteger(self.slot, net.ACCOUNT_CHARACTER_SLOT_HTH)
		valueINT = net.GetAccountCharacterSlotDataInteger(self.slot, net.ACCOUNT_CHARACTER_SLOT_INT)
		valueSTR = net.GetAccountCharacterSlotDataInteger(self.slot, net.ACCOUNT_CHARACTER_SLOT_STR)
		valueDEX = net.GetAccountCharacterSlotDataInteger(self.slot, net.ACCOUNT_CHARACTER_SLOT_DEX)
		playerval = [valueHTH, valueINT, valueSTR, valueDEX]

		# karuzela + paski: dojazd liczony z czasu, nie z klatek (patrz uiCommon.FrameLerpRatio)
		ratio = uiCommon.FrameLerpRatio(0.1)

		for i in range(4):
			self.curGauge[i] += (self.destGauge[i] - self.curGauge[i]) * ratio
			if abs(self.curGauge[i] - self.destGauge[i]) < 0.005:
				self.curGauge[i] = self.destGauge[i]
			if i < len(self.GaugeList) and self.GaugeList[i]:
				self.GaugeList[i].SetPercentage(self.curGauge[i], 1.0)
			if i < len(self.GaugeListVal) and self.GaugeListVal[i]:
				self.GaugeListVal[i].SetText(str(playerval[i]))

		for i in range(self.SLOT_COUNT):
			if False == chr.HasInstance(i):
				continue

			chr.SelectInstance(i)

			distance = 50.0
			rotRadian = self.curRotation[i] * (math.pi * 2) / 360.0
			x = distance * math.sin(rotRadian) + distance * math.cos(rotRadian)
			y = distance * math.cos(rotRadian) - distance * math.sin(rotRadian)
			chr.SetPixelPosition(int(x), int(y), 30)

			dir = app.GetRotatingDirection(self.destRotation[i], self.curRotation[i])
			rot = app.GetDegreeDifference(self.destRotation[i], self.curRotation[i])

			if app.DEGREE_DIRECTION_RIGHT == dir:
				self.curRotation[i] += rot * ratio
			elif app.DEGREE_DIRECTION_LEFT == dir:
				self.curRotation[i] -= rot * ratio

			self.curRotation[i] = (self.curRotation[i] + 360.0) % 360.0

		if -1 != self.startIndex:
			if app.GetTime() - self.startReservingTime > 0.0:
				if False == self.openLoadingFlag:
					chrSlot = self.stream.GetCharacterSlot()
					net.DirectEnter(chrSlot)
					self.openLoadingFlag = True

					playTime = net.GetAccountCharacterSlotDataInteger(self.slot, net.ACCOUNT_CHARACTER_SLOT_PLAYTIME)
					player.SetPlayTime(playTime)
					chat.Clear()

	def EmptyFunc(self):
		pass

	def PopupMessage(self, msg, func=0):
		if not func:
			func = self.EmptyFunc
		self.stream.popupWindow.Close()
		self.stream.popupWindow.Open(msg, func, localeInfo.UI_OK)

	def OnPressExitKey(self):
		self.BackSelect()
		return True

	def OnPressEscapeKey(self):
		if self.dlgQuestion and self.dlgQuestion.IsShow():
			self.dlgQuestion.Hide()
			return True
		if self.nameInputBoard:
			self.CancelInputName()
			return True
		if self.privateInputBoard:
			self.CancelInputPrivateCode()
			return True
		return self.OnPressExitKey()

	def OnIMEReturn(self):
		id = net.GetAccountCharacterSlotDataInteger(self.slot, net.ACCOUNT_CHARACTER_SLOT_ID)
		if 0 == id:
			self.CreateCharacter()
		else:
			self.StartGame()
		return True
