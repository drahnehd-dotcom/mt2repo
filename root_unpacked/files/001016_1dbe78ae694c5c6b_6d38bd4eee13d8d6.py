import ui
import event
import constInfo
import app
import uiCommon
import chat
import net
import playerSettingModule
import player
import localeInfo
import wndMgr

JOB_NAME_DICT = {
	0	:	[localeInfo.JOB_WARRIOR1,localeInfo.JOB_WARRIOR2],
	1	:	[localeInfo.JOB_ASSASSIN1,localeInfo.JOB_ASSASSIN2],
	2	:	[localeInfo.JOB_SURA1,localeInfo.JOB_SURA2],
	3	:	[localeInfo.JOB_SHAMAN1,localeInfo.JOB_SHAMAN2],
}
if app.ENABLE_WOLFMAN_CHARACTER:
	JOB_NAME_DICT.update({4 : [localeInfo.JOB_WOLFMAN1,localeInfo.JOB_WOLFMAN2],})

JOB_LIST = { 	
	0	:	localeInfo.JOB_WARRIOR,
	1	:	localeInfo.JOB_ASSASSIN,
	2	:	localeInfo.JOB_SURA,
	3	:	localeInfo.JOB_SHAMAN,
}
if app.ENABLE_WOLFMAN_CHARACTER:
	JOB_LIST.update({4 : localeInfo.JOB_WOLFMAN,})

class SkillSelectWindow(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.__LoadWindow()
	
	def __del__(self):
		ui.ScriptWindow.__del__(self)
		
	def __LoadWindow(self):
		try:
			PythonScriptLoader = ui.PythonScriptLoader()
			PythonScriptLoader.LoadScriptFile(self, "UIScript/skillchoosewindow.py")
		except:
			import exception
			exception.Abort("SelectSkill.LoadWindow.LoadObject")
			
		try:
			self.__BindObjects()
		except:
			import exception
			exception.Abort("SelectSkill.LoadWindow.BindObject")
		
		self.__BindEvents()
	
	def __BindObjects(self):
		self.titlebar = self.GetChild("TitleBar")

		self.firstHeaderName = self.GetChild("FirstHeaderName")
		self.secondHeaderName = self.GetChild("SecondHeaderName")

		self.selectButtonFirst = self.GetChild("SelectButtonFirst")
		self.selectButtonSecond = self.GetChild("SelectButtonSecond")

		self.firstSkillSlotBack = self.GetChild("FirstSkillSlotBack")
		self.secondSkillSlotBack = self.GetChild("SecondSkillSlotBack")

		self.firstSkillSlot = self.GetChild("FirstSkillSlot")
		self.secondSkillSlot = self.GetChild("SecondSkillSlot")

	def __BindEvents(self):
		self.titlebar.SetCloseEvent(ui.__mem_func__(self.Close))

		self.selectButtonFirst.SetEvent(ui.__mem_func__(self.SelectFirstJob))
		self.selectButtonSecond.SetEvent(ui.__mem_func__(self.SelectSecondJob))

		race = self.GetRealRace()
		skillCount = self.GetSkillsCount()
		skillIndex = self.GetSkillIndex()

		# Nazwy grup jako naglowki kolumn (zamiast tekstu na przyciskach)
		self.firstHeaderName.SetText(JOB_NAME_DICT[race][0])
		self.secondHeaderName.SetText(JOB_NAME_DICT[race][1])

		# Lewa kolumna - pierwsza grupa skilli
		for i in range(skillCount):
			self.firstSkillSlotBack.SetSlotStyle(wndMgr.SLOT_STYLE_NONE)

			self.firstSkillSlot.SetSkillSlotNew(i, skillIndex+i, 3, 1)
			self.firstSkillSlot.SetSlotStyle(wndMgr.SLOT_STYLE_NONE)

		if race == 4:
			# Wilkolak ma tylko jedna grupe - prawa kolumna nieaktywna
			self.secondHeaderName.SetText("")
			self.selectButtonSecond.SetEvent(ui.__mem_func__(self.EmptyJob))

			for k in range(skillCount):
				self.secondSkillSlotBack.SetSlotStyle(wndMgr.SLOT_STYLE_NONE)

				self.secondSkillSlot.ClearSlot(k)
				self.secondSkillSlot.SetSlotStyle(wndMgr.SLOT_STYLE_NONE)
		else:
			# Prawa kolumna - druga grupa skilli
			for j in range(skillCount):
				self.secondSkillSlotBack.SetSlotStyle(wndMgr.SLOT_STYLE_NONE)

				self.secondSkillSlot.SetSkillSlotNew(j, skillIndex+j+15, 3, 1)
				self.secondSkillSlot.SetSlotStyle(wndMgr.SLOT_STYLE_NONE)

						
	def GetSkillIndex(self):
		if self.GetRealRace() == 4:
			return 170
		else:
			return self.GetRealRace() * 30 + 1
				
	def GetRealRace(self):
		race = net.GetMainActorRace()
		if race >= 4:
			return race-4
		else:
			return race
			
	def GetSkillsCount(self):
		if constInfo.ARE_ENABLED_6TH_SKILLS == 1:
			return 6
		else:
			if self.GetRealRace() < 2:
				return 5
			else:
				return 6
			
	def EmptyJob(self):
		chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.JOB_SELECT_LYCAN_ERROR)
			
	def SelectFirstJob(self):
		net.SendChatPacket("/selectskill_select 1")
		self.Close()
		
	def SelectSecondJob(self):
		net.SendChatPacket("/selectskill_select 2")
		self.Close()
	
	def Open(self):
		self.SetCenterPosition()
		self.SetTop()
		self.Show()

	def OnPressEscapeKey(self):
		self.Close()
		return True
	
	def Close(self):
		self.Hide()
		return True
		
	def Destroy(self):
		self.Close()
		self.ClearDictionary()
