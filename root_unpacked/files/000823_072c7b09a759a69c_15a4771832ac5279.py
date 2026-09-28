import os
import ui
import app
import uiScriptLocale
import net
import miniMap
import player
import chat
import time
import localeInfo

class MiniMapDungeonInfo(ui.ScriptWindow):
	def __init__(self):
		self.gauge_type = 0
		self.rotateGaugeSpace = [ 20, 160]
		self.startTime = -1
		self.timer_status = 0
		self.endTime = -1
		self.startTime1 = 0
		self.endTime1 = 0
		self.fixed_time_counter = 0
		sliderString = None
		
		ui.ScriptWindow.__init__(self)
		self.__LoadWindow()

	def __del__(self):
		self.gauge_type = 0
		self.startTime = -1
		self.timer_status = 0
		self.endTime = -1

		self.startTime1 = 0
		self.endTime1 = 0
		self.fixed_time_counter = 0
		sliderString = None
		ui.ScriptWindow.__del__(self)

	def Show(self):
		self.GetChild("BaseBoard").Show()
		ui.ScriptWindow.Show(self)
			
	def Close(self):
		self.Hide()
	
	def Destroy(self):
		self.Hide()
		self.ClearDictionary()
		
	def __LoadWindow(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "uiscript/minimapdungeoninfo.py")
		except:
			import exception
			exception.Abort("MiniMapDungeonInfo.LoadWindow.LoadObject")
			
		try:
			self.GetChild("BaseBoard").Hide()
			
			self.slideText = ui.TextSlide()
			self.slideText.SetParent(self.GetChild("SlideTextWindow"))
			self.slideText.SetPosition(0, 0)
			self.slideText.Show()

			self.serverInfo = self.GetChild("ServerInfo")
			self.positionInfo = self.GetChild("PositionInfo")
			self.timer_text = self.GetChild("Timer_text")
			
		except:
			import exception
			exception.Abort("MiniMapDungeonInfo.LoadWindow.BindObject")

		self.powtorzbg = self.GetChild("PowtorzBackground")
		self.GetChild("PowtorzButton").SetEvent(ui.__mem_func__(self.Powtorz))
		self.powtorzbg.Hide()

		self.serverInfo.SetText(net.GetServerInfo())

	def Powtorz(self):
		net.SendChatPacket("/dungeons")

	def SetStage(self, cur_stage, max_stage):
		self.GetChild("StageText").SetText("E%d" % cur_stage)
		stage_perc = 140 * (float(cur_stage) / float(max_stage))
		self.GetChild("RotateGauge").SetRotation(20 + int(stage_perc))
			
	def SetButton(self, status):
		if status == 1:
			self.HideAll()
			self.powtorzbg.Show()


	def HideAll(self):
		self.GetChild("BaseBoard").Hide()
		self.GetChild("RotateGaugeBackground").Hide()
		self.GetChild("RotateGauge").Hide()
		self.GetChild("StageText").Hide()
		self.GetChild("SlideTextWindow").Hide()
		self.GetChild("SlideTextShadow").Hide()
		self.GetChild("CountGauge").Hide()
		self.GetChild("CountText").Hide()

	def SetGauge(self, gauge_type, value1, value2):
		self.gauge_type = gauge_type
		
		if self.gauge_type == 0:
			self.GetChild("CountText").SetText("")
			self.GetChild("CountGauge").SetPercentage(0, 100)

		if self.gauge_type == 1:
			self.GetChild("CountText").SetText("%d / %d" % (value1, value2))
			self.GetChild("CountGauge").SetPercentage(value1, value2)

		if self.gauge_type == 2:
			self.startTime = app.GetGlobalTimeStamp()
			self.endTime = app.GetGlobalTimeStamp() + value1
				
	def SetTimer(self, status, time):
		self.timer_status = status
		if time != 0:
			self.startTime1 = time
		else:
			self.startTime1 = app.GetGlobalTimeStamp()
		self.endTime1 = app.GetGlobalTimeStamp()

	def SetNotice(self, notice):
		self.slideText.SetText(notice, self.GetChild("SlideTextWindow").GetWidth() -1, "right")
		self.slideText.Show()

	def SecondToHM(self, time):
		second = int(time % 60)
		minute = int((time // 60) % 60)
		hour = int((time // 60) / 60) % 24
		return "%dm %ds" % (minute, second)
	
	def SecondToHMSGolbal(self, time):
		second = int(time % 60)
		minute = int((time // 60) % 60)
		hour = int((time // 60) / 60) % 24
		text = ""
		if hour > 9:
			text += str(hour) + ":"
		else:
			text += "0" + str(hour) + ":"
		if minute > 9:
			text += str(minute) + ":"
		else:
			text += "0" + str(minute) + ":"
		if second > 9:
			text += str(second)
		else:
			text += "0" + str(second)
		return text
		
	def OnUpdate(self):
		(x, y, z) = player.GetMainCharacterPosition()
		miniMap.Update(x, y)

		self.GetChild("dayInfo").SetText(time.strftime("%d.%m.%y")+" - "+time.strftime("%H:%M:%S"))
		self.GetChild("fpsInfo").SetText(localeInfo.MINIMAP_FPS_INFO.format(app.GetRenderFPS()))

		self.positionInfo.SetText("(%.0f, %.0f)" % (x//100, y//100))

		if self.timer_status == 1:
			self.endTime1 = app.GetGlobalTimeStamp()
			if not self.timer_status == 0:
				self.fixed_time_counter = self.endTime1 - self.startTime1
				self.timer_text.SetText("%s" % self.SecondToHMSGolbal(self.fixed_time_counter))

		if self.gauge_type == 2 and self.endTime != -1:
			remaining = self.endTime - app.GetGlobalTimeStamp()
			self.GetChild("CountText").SetText(self.SecondToHM(remaining))
			self.GetChild("CountGauge").SetPercentageEx(self.endTime, app.GetGlobalTimeStamp(), self.startTime)
			
