# -*- coding: utf-8 -*-
import ui
import net
import wndMgr
import app
import logging
import localeInfo
import _weakref

# Ported faithfully from S3ll introempire.py:
# - areas/flags are alpha-faded (hidden by default, fade in on hover/select)
# - invisible buttons placed over each atlas area catch hover + click
# - left/right buttons cycle the empire (Chunjo/2 skipped)
# Only Shinsoo (1/A) and Jinno (3/C) exist on this server. Empire/class
# description (EMPIREDESC) does not exist in our locale, so the description
# box + prev/next_text buttons are omitted/hidden.


class SelectEmpireWindow(ui.ScriptWindow):

	EMPIRE_LIST = [1, 3]  # 1, 3 (skip Chunjo/2)
	EMPIRE_NAME = {1: localeInfo.EMPIRE_A, 3: localeInfo.EMPIRE_C}

	class EmpireButton(ui.Window):
		def __init__(self, owner, arg):
			ui.Window.__init__(self)
			self.owner = owner
			self.arg = arg

		def __del__(self):
			ui.Window.__del__(self)

		def OnMouseOverIn(self):
			self.owner.OnOverInEmpire(self.arg)

		def OnMouseOverOut(self):
			self.owner.OnOverOutEmpire(self.arg)

		def OnMouseLeftButtonDown(self):
			if self.owner.empireID != self.arg:
				self.owner.OnSelectEmpire(self.arg)

	def __init__(self, stream):
		ui.ScriptWindow.__init__(self)
		net.SetPhaseWindow(net.PHASE_WINDOW_EMPIRE, self)

		self.stream = stream
		self.empireID = self.EMPIRE_LIST[app.GetRandom(0, len(self.EMPIRE_LIST) - 1)]

		self.leftButton = None
		self.rightButton = None
		self.selectButton = None
		self.exitButton = None
		self.empireNameText = None

		self.empireArea = {}
		self.empireAreaFlag = {}
		self.empireFlag = {}
		self.empireAreaButton = {}

		zero = dict((e, 0.0) for e in self.EMPIRE_LIST)
		self.empireAreaCurAlpha = dict(zero)
		self.empireAreaDestAlpha = dict(zero)
		self.empireAreaFlagCurAlpha = dict(zero)
		self.empireAreaFlagDestAlpha = dict(zero)
		self.empireFlagCurAlpha = dict(zero)
		self.empireFlagDestAlpha = dict(zero)

	def __del__(self):
		ui.ScriptWindow.__del__(self)
		net.SetPhaseWindow(net.PHASE_WINDOW_EMPIRE, 0)

	def Close(self):
		self.ClearDictionary()
		self.leftButton = None
		self.rightButton = None
		self.selectButton = None
		self.exitButton = None
		self.empireNameText = None
		self.empireArea = {}
		self.empireAreaFlag = {}
		self.empireFlag = {}
		self.empireAreaButton = {}

		self.KillFocus()
		self.Hide()
		app.HideCursor()

	def Open(self):
		self.SetSize(wndMgr.GetScreenWidth(), wndMgr.GetScreenHeight())
		self.SetWindowName("SelectEmpireWindow")
		self.Show()

		if not self.__LoadScript("uiScript/SelectEmpireWindow.py"):
			logging.warning("SelectEmpireWindow.Open - __LoadScript Error")
			return False

		self.OnSelectEmpire(self.empireID)
		self.__CreateButtons()
		app.ShowCursor()

	def __Bind(self, GetObject, name):
		try:
			return GetObject(name)
		except:
			logging.warning("SelectEmpireWindow: %s not found", name)
			return None

	def __LoadScript(self, fileName):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, fileName)
		except:
			logging.warning("SelectEmpireWindow.__LoadScript.LoadObject")
			return False

		GetObject = self.GetChild

		self.leftButton = self.__Bind(GetObject, "left_button")
		self.rightButton = self.__Bind(GetObject, "right_button")
		self.selectButton = self.__Bind(GetObject, "select_button")
		self.exitButton = self.__Bind(GetObject, "exit_button")
		self.empireNameText = self.__Bind(GetObject, "empire_name")

		self.empireArea[1] = self.__Bind(GetObject, "EmpireArea_A")
		self.empireArea[3] = self.__Bind(GetObject, "EmpireArea_C")
		self.empireAreaFlag[1] = self.__Bind(GetObject, "EmpireAreaFlag_A")
		self.empireAreaFlag[3] = self.__Bind(GetObject, "EmpireAreaFlag_C")
		self.empireFlag[1] = self.__Bind(GetObject, "EmpireFlag_A")
		self.empireFlag[3] = self.__Bind(GetObject, "EmpireFlag_C")

		# Chunjo (B/2) is unused on this server - hide its art if present
		for nm in ("EmpireArea_B", "EmpireAreaFlag_B", "EmpireFlag_B"):
			img = self.__Bind(GetObject, nm)
			if img:
				img.Hide()

		# No empire description on this server -> hide the description scroll buttons
		for nm in ("prev_text_button", "next_text_button"):
			btn = self.__Bind(GetObject, nm)
			if btn:
				btn.Hide()

		if self.selectButton:
			self.selectButton.SetEvent(ui.__mem_func__(self.ClickSelectButton))
		if self.exitButton:
			self.exitButton.SetEvent(ui.__mem_func__(self.ClickExitButton))
		if self.leftButton:
			self.leftButton.SetEvent(ui.__mem_func__(self.ClickLeftButton))
		if self.rightButton:
			self.rightButton.SetEvent(ui.__mem_func__(self.ClickRightButton))

		# areas + flags start fully transparent (fade in on hover/select)
		for img in self.empireArea.values():
			if img:
				img.SetAlpha(0.0)
		for img in self.empireAreaFlag.values():
			if img:
				img.SetAlpha(0.0)
		for img in self.empireFlag.values():
			if img:
				img.SetAlpha(0.0)

		return True

	def __CreateButtons(self):
		# invisible click/hover zones placed over each atlas area
		for key, img in self.empireArea.items():
			if not img:
				continue
			(x, y) = img.GetGlobalPosition()
			btn = self.EmpireButton(_weakref.proxy(self), key)
			btn.SetParent(self)
			btn.SetPosition(x, y)
			btn.SetSize(img.GetWidth(), img.GetHeight())
			btn.Show()
			self.empireAreaButton[key] = btn

	def OnOverInEmpire(self, arg):
		if arg in self.empireAreaDestAlpha:
			self.empireAreaDestAlpha[arg] = 1.0

	def OnOverOutEmpire(self, arg):
		if arg != self.empireID and arg in self.empireAreaDestAlpha:
			self.empireAreaDestAlpha[arg] = 0.0

	def OnSelectEmpire(self, arg):
		for key in self.EMPIRE_LIST:
			self.empireAreaDestAlpha[key] = 0.0
			self.empireAreaFlagDestAlpha[key] = 0.0
			self.empireFlagDestAlpha[key] = 0.0
		self.empireAreaDestAlpha[arg] = 1.0
		self.empireAreaFlagDestAlpha[arg] = 1.0
		self.empireFlagDestAlpha[arg] = 1.0
		self.empireID = arg

		if self.empireNameText:
			self.empireNameText.SetText(self.EMPIRE_NAME.get(arg, ""))

	def ClickLeftButton(self):
		idx = self.EMPIRE_LIST.index(self.empireID) if self.empireID in self.EMPIRE_LIST else 0
		idx = (idx - 1) % len(self.EMPIRE_LIST)
		self.OnSelectEmpire(self.EMPIRE_LIST[idx])

	def ClickRightButton(self):
		idx = self.EMPIRE_LIST.index(self.empireID) if self.empireID in self.EMPIRE_LIST else 0
		idx = (idx + 1) % len(self.EMPIRE_LIST)
		self.OnSelectEmpire(self.EMPIRE_LIST[idx])

	def ClickSelectButton(self):
		net.SendSelectEmpirePacket(self.empireID)
		self.stream.SetSelectCharacterPhase()
		self.Hide()

	def ClickExitButton(self):
		self.stream.SetLoginPhase()
		self.Hide()

	def __UpdateAlpha(self, imgDict, curDict, destDict):
		for key, img in imgDict.items():
			if not img:
				continue
			curAlpha = curDict[key]
			destAlpha = destDict[key]
			if abs(destAlpha - curAlpha) / 10 > 0.0001:
				curAlpha += (destAlpha - curAlpha) / 7
			else:
				curAlpha = destAlpha
			curDict[key] = curAlpha
			img.SetAlpha(curAlpha)

	def OnUpdate(self):
		self.__UpdateAlpha(self.empireArea, self.empireAreaCurAlpha, self.empireAreaDestAlpha)
		self.__UpdateAlpha(self.empireAreaFlag, self.empireAreaFlagCurAlpha, self.empireAreaFlagDestAlpha)
		self.__UpdateAlpha(self.empireFlag, self.empireFlagCurAlpha, self.empireFlagDestAlpha)

	def OnPressEscapeKey(self):
		self.ClickExitButton()
		return True

	def OnPressExitKey(self):
		self.ClickExitButton()
		return True


class ReselectEmpireWindow(SelectEmpireWindow):
	def ClickSelectButton(self):
		net.SendSelectEmpirePacket(self.empireID)
		self.stream.SetCreateCharacterPhase()
		self.Hide()

	def ClickExitButton(self):
		self.stream.SetLoginPhase()
		self.Hide()
