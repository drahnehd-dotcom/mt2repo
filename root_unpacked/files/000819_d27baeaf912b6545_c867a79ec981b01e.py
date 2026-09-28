# -*- coding: utf-8 -*-
# Maintenance system — UI klienta dla zaplanowanych przerw technicznych.
#
# Workflow:
#   1. Server (input_login.cpp + maintenance.cpp) wysyła ChatPacket
#      "Maintenancegui <remainingTime> <maintenanceTime>" przy entergame
#      LUB przy aktywacji przerwy (broadcast do wszystkich klientów).
#   2. game.py registruje callback Maintenancegui → MaintenanceWindow.Open(...)
#   3. MaintenanceWindow ma OnUpdate() z live countdown + color coding
#      (zielony >5min, żółty 1-5min, czerwony <1min).
#   4. GM przez /maintadmin → dialog Open → /start_maintenance H M S H M S
#      → server CMaintenance::StartMaintenance + P2P broadcast.
#
# Lokalizacja: wszystkie teksty z localeInfo.MAINTENANCE_* (locale_game.txt
# w 4 językach: pl/cz/en/de — patrz add_maintenance_locales.py).

import ui
import app
import net
import chr
import player
import chat
import localeInfo

# Color thresholds (sekundy) dla countdown — UX hint o pilności
COLOR_GREEN  = "|cff00c000"  # > 5 min — bezpieczny zakres
COLOR_YELLOW = "|cfff0c020"  # 1-5 min — uwaga
COLOR_RED    = "|cffe04040"  # < 1 min — pilne


class MaintenanceDialog(ui.ScriptWindow):
	"""GM panel do aktywacji/anulowania maintenance.

	Layout: 2 sekcje (delay + duration), każda z 3 polami input H/M/S.
	"""

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.__LoadDialog()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __LoadDialog(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "uiscript/maintenanceadmin.py")
		except:
			import exception
			exception.Abort("MaintenanceDialog.__LoadDialog.LoadObject")

		try:
			getObject = self.GetChild
			self.titleName = getObject("TitleName")
			self.GetChild("titlebar").SetCloseEvent(ui.__mem_func__(self.OnCancel))
			self.cancelButton = getObject("cancel_button")
			self.startmaintenanceButton = getObject("start_maintenance")
			self.cancelmaintenanceButton = getObject("cancel_maintenance")
			# 6 input fields — H/M/S × 2 sekcje (delay + duration)
			self.delayHour = getObject("delay_value_Hour")
			self.delayMin = getObject("delay_value_Min")
			self.delaySec = getObject("delay_value_Sec")
			self.durationHour = getObject("duration_value_Hour")
			self.durationMin = getObject("duration_value_Min")
			self.durationSec = getObject("duration_value_Sec")
		except:
			import exception
			exception.Abort("MaintenanceDialog.__LoadDialog.BindObject")

		self.SetCenterPosition()
		self.SetTop()
		self.cancelButton.SetEvent(ui.__mem_func__(self.OnCancel))
		self.startmaintenanceButton.SetEvent(ui.__mem_func__(self.StartMaintenance))
		self.cancelmaintenanceButton.SetEvent(ui.__mem_func__(self.CancelMaintenance))
		self.cancelButton.Hide()

	def Destroy(self):
		self.ClearDictionary()
		self.titleName = None
		self.cancelButton = None
		self.delayHour = None
		self.delayMin = None
		self.delaySec = None
		self.durationHour = None
		self.durationMin = None
		self.durationSec = None

	def SetTitle(self, title):
		self.titleName.SetText(title)

	def __ParseField(self, field):
		"""Bezpieczny int parse — pusty string lub bzdura → 0."""
		try:
			text = field.GetText() or "0"
			val = int(text)
			return val if val >= 0 else 0
		except (ValueError, TypeError):
			return 0

	def StartMaintenance(self):
		# Zlicz sekundy z H/M/S
		delayH = self.__ParseField(self.delayHour)
		delayM = self.__ParseField(self.delayMin)
		delayS = self.__ParseField(self.delaySec)
		durH = self.__ParseField(self.durationHour)
		durM = self.__ParseField(self.durationMin)
		durS = self.__ParseField(self.durationSec)

		delaySec = delayH * 3600 + delayM * 60 + delayS
		durationSec = durH * 3600 + durM * 60 + durS

		if delaySec <= 0:
			chat.AppendChat(chat.CHAT_TYPE_INFO,
				localeInfo.MAINTENANCE_ADMIN_INVALID_DELAY)
			return
		if durationSec <= 0:
			chat.AppendChat(chat.CHAT_TYPE_INFO,
				localeInfo.MAINTENANCE_ADMIN_INVALID_DURATION)
			return

		self.Hide()
		net.SendChatPacket("/start_maintenance %d %d" % (delaySec, durationSec))

	def CancelMaintenance(self):
		self.Hide()
		net.SendChatPacket("/cancel_maintenance")

	def OnCancel(self):
		self.Hide()
		return True


class MaintenanceWindow(ui.ScriptWindow):
	"""Live countdown widget — pokazany każdemu graczowi gdy maintenance aktywne.

	Ulepszenia względem oldschool:
	  - color coding countdown'u (zielony→żółty→czerwony)
	  - lokalizacja per gracz (4 języki via localeInfo)
	  - format Days/Hours/Min/Sec (zamiast tylko Min/Sek)
	  - 2 linie info (czas trwania + countdown do shutdown)
	"""

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.LoadWindow()
		self.shutdownTimestamp = 0    # absolute global time gdy shutdown
		self.maintenanceDuration = 0  # ile potrwa (info display)

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def LoadWindow(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "uiscript/maintenance.py")
		except:
			import exception
			exception.Abort("MaintenanceWindow.LoadWindow.LoadObject")
		try:
			self.board = self.GetChild("Thinboard")
			self.titleText = self.GetChild("maintitle")
			self.textLine1 = self.GetChild("message1")
			self.textLine2 = self.GetChild("message2")
		except:
			import exception
			exception.Abort("MaintenanceWindow.LoadWindow.BindObject")

		# Set localized title (uiscript ma placeholder, tu set z localeInfo)
		self.titleText.SetText(localeInfo.MAINTENANCE_TITLE)

	def Open(self, shutdownTimestamp, duration):
		self.SetTop()
		self.Show()
		self.shutdownTimestamp = int(shutdownTimestamp)
		self.maintenanceDuration = int(duration)
		# Linia 1 — czas trwania (info statyczne, lokalizowane)
		self.textLine1.SetText(
			localeInfo.MAINTENANCE_DURATION_INFO % self.SecondToHMD(self.maintenanceDuration))

	def Close(self):
		self.shutdownTimestamp = 0
		self.maintenanceDuration = 0
		self.Hide()

	def SecondToHMD(self, time):
		"""Format używający lokalnych jednostek z localeInfo.MAINTENANCE_UNIT_*."""
		if time < 0:
			time = 0
		second = int(time % 60)
		minute = int((time / 60) % 60)
		hour = int(((time / 60) / 60) % 24)
		day = int((((time / 60) / 60) / 24) % 30)

		dStr = localeInfo.MAINTENANCE_UNIT_DAY
		hStr = localeInfo.MAINTENANCE_UNIT_HOUR
		mStr = localeInfo.MAINTENANCE_UNIT_MIN
		sStr = localeInfo.MAINTENANCE_UNIT_SEC

		if day > 0:
			return "%d %s %d %s %02d %s %02d %s." % (day, dStr, hour, hStr, minute, mStr, second, sStr)
		if hour > 0:
			if time % 3600 == 0:
				return "%d %s." % (hour, hStr)
			if time % 60 == 0:
				return "%d %s %02d %s." % (hour, hStr, minute, mStr)
			return "%d %s %02d %s %02d %s." % (hour, hStr, minute, mStr, second, sStr)
		if minute > 0:
			if time % 60 == 0:
				return "%d %s." % (minute, mStr)
			return "%d %s %02d %s." % (minute, mStr, second, sStr)
		return "%d %s." % (second, sStr)

	def __ColorForTime(self, remainingSec):
		"""Color coding — UX urgency hint."""
		if remainingSec < 60:
			return COLOR_RED
		if remainingSec < 300:
			return COLOR_YELLOW
		return COLOR_GREEN

	def OnUpdate(self):
		if self.shutdownTimestamp <= 0:
			return
		remain = self.shutdownTimestamp - app.GetGlobalTimeStamp()
		if remain > 0:
			color = self.__ColorForTime(remain)
			self.textLine2.SetText(
				localeInfo.MAINTENANCE_COUNTDOWN % (color, self.SecondToHMD(remain)))
		else:
			self.textLine2.SetText(localeInfo.MAINTENANCE_IN_PROGRESS)
