# -*- coding: utf-8 -*-
import chr
import grp
import app
import net
import snd
import wndMgr
import event
import systemSetting
import localeInfo
import logging

import ui
import math
import musicInfo
import playerSettingModule
import uiScriptLocale
import uiCommon
from utility import MakeEvent, Event

MAN = 0
WOMAN = 1
SHAPE0 = 0
SHAPE1 = 1
PAGE_COUNT = 2
SLOT_COUNT = 4
BASE_CHR_ID = 3


class CreateCharacterWindow(ui.Window):

	SLOT_ROTATION = [135.0, 225.0, 315.0, 45.0]

	CREATE_STAT_POINT = 0

	STAT_CON = 0
	STAT_INT = 1
	STAT_STR = 2
	STAT_DEX = 3

	STAT_DESCRIPTION = {
		STAT_CON: localeInfo.STAT_TOOLTIP_CON,
		STAT_INT: localeInfo.STAT_TOOLTIP_INT,
		STAT_STR: localeInfo.STAT_TOOLTIP_STR,
		STAT_DEX: localeInfo.STAT_TOOLTIP_DEX,
	}

	START_STAT = (  ## CON INT STR DEX
		[4, 3, 6, 3],  ## Warrior
		[3, 3, 4, 6],  ## Assassin
		[3, 5, 5, 3],  ## Sura
		[4, 6, 3, 3],  ## Shaman
		[4, 3, 6, 3],  ## Warrior (female)
		[3, 3, 4, 6],  ## Assassin (female)
		[3, 5, 5, 3],  ## Sura (female)
		[4, 6, 3, 3],  ## Shaman (female)
	)

	CLASS_NAMES = [
		localeInfo.SELECT_WARRIOR,
		localeInfo.SELECT_ASSASSIN,
		localeInfo.SELECT_SURA,
		localeInfo.SELECT_SHAMAN,
	]

	# Per-language class descriptions are the original S3ll event-text files
	# (locale/<lang>/jobdesc_*.txt), rendered through the event system with
	# prev/next pagination. File names per class (path is resolved per language
	# in Open() via app.GetLocalePath()).
	DESC_FILE_NAMES = [
		"jobdesc_warrior.txt",
		"jobdesc_assassin.txt",
		"jobdesc_sura.txt",
		"jobdesc_shaman.txt",
	]

	CLASS_ICONS = [
		"Assets/kowal/selectcharacter/warrior-icon.png",
		"Assets/kowal/selectcharacter/ninja-icon.png",
		"Assets/kowal/selectcharacter/sura-icon.png",
		"Assets/kowal/selectcharacter/shaman-icon.png",
	]

	class DescriptionBox(ui.Window):
		# Renders the registered job-description event set (S3ll-style).
		def __init__(self):
			ui.Window.__init__(self)
			self.descIndex = 0

		def __del__(self):
			ui.Window.__del__(self)

		def SetIndex(self, index):
			self.descIndex = index

		def OnRender(self):
			# descIndex 0 is a VALID event-set slot - never guard with `if descIndex`
			event.RenderEventSet(self.descIndex)

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
		net.SetPhaseWindow(net.PHASE_WINDOW_CREATE, self)
		self.stream = stream

	def Open(self):
		net.SetPhaseWindow(net.PHASE_WINDOW_CREATE, self)

		if hasattr(app, 'ENABLE_PERFORMANCE_IMPROVEMENTS_NEW') and not app.ENABLE_PERFORMANCE_IMPROVEMENTS_NEW:
			playerSettingModule.LoadGameData("INIT")

		self.reservingRaceIndex = -1
		self.reservingShapeIndex = -1
		self.reservingStartTime = 0
		self.stat = [0, 0, 0, 0]
		self.gender = 0
		self.slot = -1
		# carousel rotation (4 classes shown at once, like the select screen)
		self.curRotation = list(self.SLOT_ROTATION)
		self.destRotation = list(self.SLOT_ROTATION)
		self.shapeList = [
			[0, 0, 0, 0],
			[0, 0, 0, 0],
		]

		# Initialize all UI attributes to None
		self.dlgBoard = None
		self.GaugeList = []
		self.btnCreate = None
		self.btnCancel = None
		self.genderButtonList = []
		self.shapeButtonList = []
		self.editCharacterName = None
		self.statValue = []
		self.backGround = None
		self.nameImages = {}
		self.statButtonList = []
		self.lastStatPoint = self.CREATE_STAT_POINT
		self.btnPrev = None
		self.btnNext = None
		self.btnLeft = None
		self.btnRight = None
		# class description (S3ll jobdesc_*.txt rendered via the event system)
		self.textBoard = None
		self.descriptionBox = None
		self.descIndex = 0
		self.DESC_FILES = [app.GetLocalePath() + "/" + n for n in self.DESC_FILE_NAMES]

		try:
			dlgBoard = ui.ScriptWindow()
			pythonScriptLoader = ui.PythonScriptLoader()
			pythonScriptLoader.LoadScriptFile(dlgBoard, "uiScript/createcharacterwindow.py")
		except:
			logging.warning("CreateCharacterWindow.Open.LoadObject")
			return False

		getChild = dlgBoard.GetChild

		# Bind UI elements individually with try/except per element
		try:
			self.GaugeList = [
				getChild("hth_gauge"),
				getChild("int_gauge"),
				getChild("str_gauge"),
				getChild("dex_gauge"),
			]
		except:
			logging.warning("CreateCharacterWindow.Open.BindGauges")
			self.GaugeList = []

		try:
			self.btnCreate = getChild("create_button")
		except:
			logging.warning("CreateCharacterWindow.Open.BindCreateButton")

		try:
			self.btnCancel = getChild("cancel_button")
		except:
			logging.warning("CreateCharacterWindow.Open.BindCancelButton")

		# class-cycle buttons (prev/next in board + dragon arrows)
		def _bind(name):
			try:
				return getChild(name)
			except:
				logging.warning("CreateCharacterWindow.Open.Bind %s", name)
				return None
		self.btnPrev = _bind("prev_button")
		self.btnNext = _bind("next_button")
		self.btnLeft = _bind("left_button")
		self.btnRight = _bind("right_button")
		self.nameImages = {
			0: _bind("name_warrior"),
			1: _bind("name_assassin"),
			2: _bind("name_sura"),
			3: _bind("name_shaman"),
		}
		self.textBoard = _bind("text_board")

		# +stat buttons exist in the layout but are hidden (CREATE_STAT_POINT == 0),
		# exactly like S3ll. Binding+hiding them avoids "button not found" warnings.
		for nm in ("hth_button", "int_button", "str_button", "dex_button"):
			btn = _bind(nm)
			if btn:
				btn.Hide()

		try:
			self.genderButtonList = [
				getChild("gender_button_01"),
				getChild("gender_button_02"),
			]
		except:
			logging.warning("CreateCharacterWindow.Open.BindGenderButtons")
			self.genderButtonList = []

		try:
			self.shapeButtonList = [
				getChild("shape_button_01"),
				getChild("shape_button_02"),
			]
		except:
			logging.warning("CreateCharacterWindow.Open.BindShapeButtons")
			self.shapeButtonList = []

		try:
			self.editCharacterName = getChild("character_name_value")
		except:
			logging.warning("CreateCharacterWindow.Open.BindEditName")

		try:
			self.backGround = getChild("BackGround")
		except:
			logging.warning("CreateCharacterWindow.Open.BindBackground")

		try:
			self.statValue = [
				getChild("hth_value"),
				getChild("int_value"),
				getChild("str_value"),
				getChild("dex_value"),
			]
		except:
			logging.warning("CreateCharacterWindow.Open.BindStatValues")
			self.statValue = []

		# Bind events
		if self.btnCreate:
			self.btnCreate.SetEvent(MakeEvent(self.CreateCharacter))
		if self.btnCancel:
			self.btnCancel.SetEvent(MakeEvent(self.CancelCreate))

		# prev/next page the class description (S3ll); dragon arrows cycle class
		if self.btnPrev:
			self.btnPrev.SetEvent(MakeEvent(self.PrevDescriptionPage))
		if self.btnNext:
			self.btnNext.SetEvent(MakeEvent(self.NextDescriptionPage))
		if self.btnLeft:
			self.btnLeft.SetEvent(MakeEvent(self.PrevClass))
		if self.btnRight:
			self.btnRight.SetEvent(MakeEvent(self.NextClass))

		if len(self.genderButtonList) >= 2:
			self.genderButtonList[0].SetEvent(Event(self.__SelectGender, MAN))
			self.genderButtonList[1].SetEvent(Event(self.__SelectGender, WOMAN))

		if len(self.shapeButtonList) >= 2:
			self.shapeButtonList[0].SetEvent(Event(self.__SelectShape, SHAPE0))
			self.shapeButtonList[1].SetEvent(Event(self.__SelectShape, SHAPE1))

		if self.editCharacterName:
			self.editCharacterName.SetReturnEvent(MakeEvent(self.CreateCharacter))
			self.editCharacterName.SetEscapeEvent(MakeEvent(self.CancelCreate))
			self.editCharacterName.SetText("")

		self.dlgBoard = dlgBoard
		self.curGauge = [0.0, 0.0, 0.0, 0.0]
		self.destGauge = [0.0, 0.0, 0.0, 0.0]

		self.chrRenderer = self.CharacterRenderer()
		if self.backGround:
			self.chrRenderer.SetParent(self.backGround)
		self.chrRenderer.Show()

		# description box renders the event-set on top of the text_board
		self.descriptionBox = self.DescriptionBox()
		self.descriptionBox.SetParent(self.dlgBoard)
		self.descriptionBox.Show()

		self.EnableWindow()

		# Create all character instances for both genders
		male_races = [
			playerSettingModule.RACE_WARRIOR_M,
			playerSettingModule.RACE_ASSASSIN_M,
			playerSettingModule.RACE_SURA_M,
			playerSettingModule.RACE_SHAMAN_M,
		]
		female_races = [
			playerSettingModule.RACE_WARRIOR_W,
			playerSettingModule.RACE_ASSASSIN_W,
			playerSettingModule.RACE_SURA_W,
			playerSettingModule.RACE_SHAMAN_W,
		]

		for page in range(PAGE_COUNT):
			races = male_races if page == MAN else female_races
			for slot in range(SLOT_COUNT):
				self.__MakeCharacter(page, slot, races[slot])

		self.slot = 0
		self.__SelectGender(MAN)
		self.__SelectShape(SHAPE0)
		self.__SelectClass(0)
		self.__ShowCurrentGender()

		self.dlgBoard.Show()
		self.Show()

		if musicInfo.createMusic != "":
			snd.SetMusicVolume(systemSetting.GetMusicVolume())
			snd.FadeInMusic("BGM/" + musicInfo.createMusic)

		app.ShowCursor()

	def ExitSelect(self):
		app.Exit()

	def Close(self):
		if self.editCharacterName:
			self.editCharacterName.Enable()

		if self.dlgBoard:
			self.dlgBoard.ClearDictionary()

		self.stream = 0
		self.shapeButtonList = []
		self.genderButtonList = []
		self.btnCreate = None
		self.btnCancel = None
		self.btnPrev = None
		self.btnNext = None
		self.btnLeft = None
		self.btnRight = None
		self.nameImages = {}
		event.ClearEventSet(self.descIndex)
		self.descIndex = 0
		self.descriptionBox = None
		self.textBoard = None
		self.statButtonList = []
		self.editCharacterName = None
		self.backGround = None
		self.GaugeList = []
		self.statValue = []

		if musicInfo.createMusic != "":
			snd.FadeOutMusic("BGM/" + musicInfo.createMusic)

		for id in range(BASE_CHR_ID + SLOT_COUNT * PAGE_COUNT):
			chr.DeleteInstance(id)

		if self.dlgBoard:
			self.dlgBoard.Hide()

		net.SetPhaseWindow(net.PHASE_WINDOW_CREATE, 0)
		self.Hide()
		app.HideCursor()
		event.Destroy()

	def EnableWindow(self):
		self.reservingRaceIndex = -1
		self.reservingShapeIndex = -1

		if self.btnCreate:
			self.btnCreate.Enable()
		if self.btnCancel:
			self.btnCancel.Enable()
		if self.editCharacterName:
			self.editCharacterName.SetFocus()
			self.editCharacterName.Enable()

		for page in range(PAGE_COUNT):
			for slot in range(SLOT_COUNT):
				chr_id = self.__GetSlotChrID(page, slot)
				chr.SelectInstance(chr_id)
				chr.BlendLoopMotion(chr.MOTION_INTRO_WAIT, 0.1)

	def DisableWindow(self):
		if self.btnCreate:
			self.btnCreate.Disable()
			self.btnCreate.SetUp()
		if self.btnCancel:
			self.btnCancel.Disable()
		if self.editCharacterName:
			self.editCharacterName.Disable()

	## Character Management

	def __GetSlotChrID(self, page, slot):
		return BASE_CHR_ID + page * SLOT_COUNT + slot

	def __MakeCharacter(self, page, slot, race):
		chr_id = self.__GetSlotChrID(page, slot)
		chr.CreateInstance(chr_id)
		chr.SelectInstance(chr_id)
		chr.SetVirtualID(chr_id)
		chr.SetRace(race)
		chr.SetArmor(0)
		chr.SetHair(0)
		if hasattr(chr, 'SetAcce'):
			chr.SetAcce(0)
		chr.Refresh()
		chr.SetMotionMode(chr.MOTION_MODE_GENERAL)
		chr.SetLoopMotion(chr.MOTION_INTRO_WAIT)
		chr.SetRotation(0.0)
		chr.Hide()

	def __ApplyShape(self, slot):
		# apply the chosen body shape to a character of the current gender
		chr_id = self.__GetSlotChrID(self.gender, slot)
		if chr.HasInstance(chr_id):
			chr.SelectInstance(chr_id)
			shape = self.shapeList[self.gender][slot]
			chr.ChangeShape(shape)
			chr.SetMotionMode(chr.MOTION_MODE_GENERAL)
			chr.SetLoopMotion(chr.MOTION_INTRO_WAIT)

	def __ShowCurrentGender(self):
		# carousel: show all 4 classes of the current gender, hide the other gender
		for page in range(PAGE_COUNT):
			for i in range(SLOT_COUNT):
				chr_id = self.__GetSlotChrID(page, i)
				if not chr.HasInstance(chr_id):
					continue
				chr.SelectInstance(chr_id)
				if page == self.gender:
					chr.Show()
					self.__ApplyShape(i)
				else:
					chr.Hide()

	def __SetCarouselRotation(self):
		for i in range(SLOT_COUNT):
			self.destRotation[(i + self.slot) % SLOT_COUNT] = self.SLOT_ROTATION[i]

	def __SyncShapeButtons(self):
		if self.slot < 0:
			return
		active_shape = self.shapeList[self.gender][self.slot]
		for idx, btn in enumerate(self.shapeButtonList):
			if idx == active_shape:
				btn.Down()
			else:
				btn.SetUp()

	## Selection

	def __SelectGender(self, gender):
		for button in self.genderButtonList:
			button.SetUp()
		if gender < len(self.genderButtonList):
			self.genderButtonList[gender].Down()

		self.gender = gender
		self.__SyncShapeButtons()
		self.__ShowCurrentGender()
		self.__SetCarouselRotation()

	def __SelectSlot(self, slot):
		if slot < 0 or slot >= SLOT_COUNT:
			return

		self.slot = slot
		self.ResetStat()

		if self.IsShow():
			snd.PlaySound("sound/ui/click.wav")

		self.__SyncShapeButtons()
		self.__SetCarouselRotation()

	def __SelectShape(self, shape):
		if self.slot < 0:
			return
		self.shapeList[self.gender][self.slot] = shape

		for button in self.shapeButtonList:
			button.SetUp()
		if shape < len(self.shapeButtonList):
			self.shapeButtonList[shape].Down()

		self.__ApplyShape(self.slot)

	def __SelectClass(self, slot):
		self.__SelectSlot(slot)

		# class name banner (S3ll graphics)
		for j, img in self.nameImages.items():
			if not img:
				continue
			if j == slot:
				img.Show()
			else:
				img.Hide()
		# class description (S3ll event-text), reset to first page
		self.__SetDescription(slot)

	def __SetDescription(self, slot):
		# register the job description event set (S3ll __UpdateScene). Position +
		# descriptionBox.SetIndex happen every frame in OnUpdate. descIndex is a
		# slot index that can legitimately be 0 - ClearEventSet/RegisterEventSet
		# are unconditional (a `if self.descIndex` guard would drop slot 0).
		if slot < 0 or slot >= len(self.DESC_FILES):
			return
		event.ClearEventSet(self.descIndex)
		self.descIndex = event.RegisterEventSet(self.DESC_FILES[slot])

	def PrevDescriptionPage(self):
		if event.IsWait(self.descIndex):
			if event.GetVisibleStartLine(self.descIndex) - event.BOX_VISIBLE_LINE_COUNT >= 0:
				event.SetVisibleStartLine(self.descIndex, event.GetVisibleStartLine(self.descIndex) - event.BOX_VISIBLE_LINE_COUNT)
				event.Skip(self.descIndex)
		else:
			event.Skip(self.descIndex)

	def NextDescriptionPage(self):
		if event.IsWait(self.descIndex):
			event.SetVisibleStartLine(self.descIndex, event.GetVisibleStartLine(self.descIndex) + event.BOX_VISIBLE_LINE_COUNT)
			event.Skip(self.descIndex)
		else:
			event.Skip(self.descIndex)

	def __CycleClass(self, delta):
		newSlot = (self.slot + delta) % SLOT_COUNT
		self.__SelectClass(newSlot)

	def PrevClass(self):
		self.__CycleClass(-1)

	def NextClass(self):
		self.__CycleClass(1)

	## Stats

	def GetSlotIndex(self):
		return self.slot

	def RefreshStat(self):
		statSummary = self.stat[0] + self.stat[1] + self.stat[2] + self.stat[3]
		if statSummary == 0:
			statSummary = 1
		self.destGauge = (
			float(self.stat[0]) / float(statSummary),
			float(self.stat[1]) / float(statSummary),
			float(self.stat[2]) / float(statSummary),
			float(self.stat[3]) / float(statSummary),
		)

		for i in range(4):
			if i < len(self.statValue):
				self.statValue[i].SetText(str(self.stat[i]))

	def ResetStat(self):
		for i in range(4):
			self.stat[i] = self.START_STAT[self.slot][i]
		self.lastStatPoint = self.CREATE_STAT_POINT
		self.RefreshStat()

	## Character Creation

	def CreateCharacter(self):
		if -1 != self.reservingRaceIndex:
			return

		textName = self.editCharacterName.GetText() if self.editCharacterName else ""
		if not self.__CheckCreateCharacter(textName):
			return

		if musicInfo.selectMusic != "":
			snd.FadeLimitOutMusic("BGM/" + musicInfo.selectMusic, systemSetting.GetMusicVolume() * 0.05)

		self.DisableWindow()

		chr_id = self.__GetSlotChrID(self.gender, self.slot)
		chr.SelectInstance(chr_id)

		self.reservingRaceIndex = chr.GetRace()
		self.reservingShapeIndex = self.shapeList[self.gender][self.slot]
		self.reservingStartTime = app.GetTime()

		for eachSlot in range(SLOT_COUNT):
			sel_id = self.__GetSlotChrID(self.gender, eachSlot)
			chr.SelectInstance(sel_id)
			if eachSlot == self.slot:
				chr.PushOnceMotion(chr.MOTION_INTRO_SELECTED)
			else:
				chr.PushOnceMotion(chr.MOTION_INTRO_NOT_SELECTED)

	def CancelCreate(self):
		self.stream.SetSelectCharacterPhase()

	def __CheckCreateCharacter(self, name):
		if len(name) == 0:
			self.PopupMessage(localeInfo.CREATE_INPUT_NAME, self.EnableWindow)
			return False

		if localeInfo.CREATE_GM_NAME in name:
			self.PopupMessage(localeInfo.CREATE_ERROR_GM_NAME, self.EnableWindow)
			return False

		if net.IsInsultIn(name):
			self.PopupMessage(localeInfo.CREATE_ERROR_INSULT_NAME, self.EnableWindow)
			return False

		return True

	## Events

	def OnCreateSuccess(self):
		self.stream.SetSelectCharacterPhase()

	def OnCreateFailure(self, type):
		if 1 == type:
			self.PopupMessage(localeInfo.CREATE_EXIST_SAME_NAME, self.EnableWindow)
		else:
			self.PopupMessage(localeInfo.CREATE_FAILURE, self.EnableWindow)

	def OnKeyDown(self, key):
		if key == 2:
			self.__SelectClass(0)
		elif key == 3:
			self.__SelectClass(1)
		elif key == 4:
			self.__SelectClass(2)
		elif key == 5:
			self.__SelectClass(3)
		elif key == 59:
			self.__SelectGender(MAN)
		elif key == 60:
			self.__SelectGender(WOMAN)
		return True

	def OnUpdate(self):
		chr.Update()

		# render the class description over the text_board (S3ll OnUpdate):
		# re-anchor position and re-assert the box index every frame. descIndex 0
		# is valid - guard only the window refs, never `if self.descIndex`.
		if self.textBoard and self.descriptionBox:
			(gx, gy) = self.textBoard.GetGlobalPosition()
			event.UpdateEventSet(self.descIndex, int(gx) + 7, -(int(gy) + 7))
			self.descriptionBox.SetIndex(self.descIndex)

		# karuzela + paski: dojazd liczony z czasu, nie z klatek (patrz uiCommon.FrameLerpRatio)
		ratio = uiCommon.FrameLerpRatio(0.1)

		# Carousel: rotate the 4 classes of the current gender (selected one to front)
		for slot in range(SLOT_COUNT):
			chr_id = self.__GetSlotChrID(self.gender, slot)
			if not chr.HasInstance(chr_id):
				continue
			chr.SelectInstance(chr_id)

			distance = 50.0
			rotRadian = self.curRotation[slot] * (math.pi * 2) / 360.0
			x = distance * math.sin(rotRadian) + distance * math.cos(rotRadian)
			y = distance * math.cos(rotRadian) - distance * math.sin(rotRadian)
			chr.SetPixelPosition(int(x), int(y), 30)

			direction = app.GetRotatingDirection(self.destRotation[slot], self.curRotation[slot])
			rot = app.GetDegreeDifference(self.destRotation[slot], self.curRotation[slot])
			if app.DEGREE_DIRECTION_RIGHT == direction:
				self.curRotation[slot] += rot * ratio
			elif app.DEGREE_DIRECTION_LEFT == direction:
				self.curRotation[slot] -= rot * ratio
			self.curRotation[slot] = (self.curRotation[slot] + 360.0) % 360.0

		# Smooth gauge animation
		for i in range(4):
			self.curGauge[i] += (self.destGauge[i] - self.curGauge[i]) * ratio
			if abs(self.curGauge[i] - self.destGauge[i]) < 0.005:
				self.curGauge[i] = self.destGauge[i]
			if i < len(self.GaugeList):
				self.GaugeList[i].SetPercentage(self.curGauge[i], 1.0)

		# Handle character creation timing
		if -1 != self.reservingRaceIndex:
			if app.GetTime() - self.reservingStartTime >= 1.5:
				chrSlot = self.stream.GetCharacterSlot()
				textName = self.editCharacterName.GetText() if self.editCharacterName else ""
				raceIndex = self.reservingRaceIndex
				shapeIndex = self.reservingShapeIndex

				startStat = self.START_STAT[raceIndex]
				statCon = self.stat[0] - startStat[0]
				statInt = self.stat[1] - startStat[1]
				statStr = self.stat[2] - startStat[2]
				statDex = self.stat[3] - startStat[3]

				net.SendCreateCharacterPacket(chrSlot, textName, raceIndex, shapeIndex, statCon, statInt, statStr, statDex)
				self.reservingRaceIndex = -1

	def EmptyFunc(self):
		pass

	def PopupMessage(self, msg, func=0):
		if not func:
			func = self.EmptyFunc
		self.stream.popupWindow.Close()
		self.stream.popupWindow.Open(msg, func, localeInfo.UI_OK)

	def OnPressExitKey(self):
		self.CancelCreate()
		return True
