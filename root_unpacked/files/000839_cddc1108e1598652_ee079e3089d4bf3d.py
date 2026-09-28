# -*- coding:cp949 -*-
import ui
import dbg
import app
import grp
import event
import time
import wndMgr
import net

QUEST_BOARD_IMAGE_DIR = 'd:/ymir work/ui/game/questboard/'

cur_questpage_number = 1
entire_questbutton_number = 0
entire_questpage_number = 1


class ToolTipImageBox(ui.ImageBox):
	def __init__(self):
		ui.ImageBox.__init__(self)
		self.DestroyToolTip()
	def __del__(self):
		ui.ImageBox.__del__(self)

	def CreateToolTip(self, parent, title, desc, x, y):
		import uiToolTip
		self.toolTip = uiToolTip.ToolTip()
		self.toolTip.SetWindowHorizontalAlignCenter()
		self.toolTip.SetFollow(False)
		self.toolTip.SetTitle(title)
		self.toolTip.SetPosition(x, y)

		desc = desc.replace("|", "/")
		for line in desc.split("/"):
			self.toolTip.AutoAppendTextLine(line)

		self.toolTip.ResizeToolTip()
		self.toolTip.Hide()

	def DestroyToolTip(self):
		self.toolTip = None

	def OnMouseOverIn(self):
		if self.toolTip:
			self.toolTip.SetTop()
			self.toolTip.Show()

	def OnMouseOverOut(self):
		if self.toolTip:
			self.toolTip.Hide()

class QuestCurtain(ui.Window):
	CURTAIN_TIME = 0.25
	CURTAIN_SPEED = 200
	MAX_FRAME_TIME = 0.25    # alt-tab / doczytanie mapy nie moze katapultowac kurtyny
	CLOSE_TIMEOUT = 3.0      # bezpiecznik: HUD nigdy nie zostaje ukryty na stale
	BarHeight = 60
	OnDoneEventList = []
	def __init__(self,layer="TOP_MOST"):
		ui.Window.__init__(self,layer)
		self.TopBar = ui.Bar("TOP_MOST")
		self.BottomBar = ui.Bar("TOP_MOST")

		self.TopBar.Show()
		self.BottomBar.Show()

		self.TopBar.SetColor(0xff000000)
		self.BottomBar.SetColor(0xff000000)

		# Pozycje trzymamy we float. wndMgr zna tylko int, wiec przy >200 FPS krok
		# (dt * 200 px/s) byl mniejszy niz 1 px i int() zjadal go w CALOSCI - kurtyna
		# stala w miejscu, a razem z nia caly HUD (OnDoneEventList -> __ShowWindows).
		self.topY = float(-self.BarHeight)
		self.bottomY = float(wndMgr.GetScreenHeight())

		self.TopBar.SetSize(wndMgr.GetScreenWidth(),self.BarHeight)
		self.BottomBar.SetSize(wndMgr.GetScreenWidth(),self.BarHeight)
		self.__ApplyBarPosition()

		self.CurtainMode = 0
		self.lastCurtainMode = 0
		self.closeStartTime = 0.0

		self.lastclock = time.perf_counter()

	def __ApplyBarPosition(self):
		self.TopBar.SetPosition(0, int(self.topY))
		self.BottomBar.SetPosition(0, int(self.bottomY))

	def __OnCurtainModeChanged(self, now):
		self.lastCurtainMode = self.CurtainMode

		if self.CurtainMode > 0:
			self.closeStartTime = 0.0
			# BarHeight to atrybut KLASY, przeliczany per dialog (zalezy od proporcji
			# ekranu) - paski trzeba przeskalowac, inaczej zostaja w starym rozmiarze.
			self.TopBar.SetSize(wndMgr.GetScreenWidth(), self.BarHeight)
			self.BottomBar.SetSize(wndMgr.GetScreenWidth(), self.BarHeight)
			if self.topY < -self.BarHeight:
				self.topY = float(-self.BarHeight)
				self.bottomY = float(wndMgr.GetScreenHeight())
				self.__ApplyBarPosition()
		elif self.CurtainMode < 0:
			self.closeStartTime = now
		else:
			self.closeStartTime = 0.0

	def Close(self):
		self.CurtainMode = 0
		self.lastCurtainMode = 0
		self.closeStartTime = 0.0
		self.topY = float(-self.BarHeight-1)
		self.bottomY = float(wndMgr.GetScreenHeight()+1)
		self.__ApplyBarPosition()
		for OnDoneEvent in QuestCurtain.OnDoneEventList:
			OnDoneEvent(*(self,))
		QuestCurtain.OnDoneEventList = []

	def OnUpdate(self):
		now = time.perf_counter()
		dt = now - self.lastclock
		self.lastclock = now

		if self.CurtainMode != self.lastCurtainMode:
			self.__OnCurtainModeChanged(now)

		if not self.CurtainMode:
			return

		if dt < 0.0:
			dt = 0.0
		elif dt > self.MAX_FRAME_TIME:
			dt = self.MAX_FRAME_TIME

		step = dt * self.CURTAIN_SPEED

		if self.CurtainMode>0:
			self.topY += step
			self.bottomY -= step
			if self.topY > 0.0:
				self.topY = 0.0
				self.bottomY = float(wndMgr.GetScreenHeight()-self.BarHeight)
				self.CurtainMode = 0
				self.lastCurtainMode = 0
			self.__ApplyBarPosition()

		else:
			self.topY -= step
			self.bottomY += step
			timedOut = self.closeStartTime and (now - self.closeStartTime) > self.CLOSE_TIMEOUT
			if self.topY < -self.BarHeight or timedOut:
				self.Close()
			else:
				self.__ApplyBarPosition()

class EventCurtain(ui.Bar):

	COLOR_WHITE = 0.0
	COLOR_BLACK = 1.0

	DEFAULT_FADE_SPEED = 0.035

	STATE_WAIT = 0
	STATE_OUT = 1
	STATE_IN = 2

	def __init__(self, index):
		ui.Bar.__init__(self, "CURTAIN")
		self.SetWindowName("EventCurtain")
		self.AddFlag("float")
		self.SetSize(wndMgr.GetScreenWidth(), wndMgr.GetScreenHeight())
		self.Hide()

		self.fadeColor = 1.0
		self.curAlpha = 0.0
		self.FadeInFlag = False
		self.state = self.STATE_WAIT
		self.speed = 1.0
		self.eventIndex = index
		self.lastFadeTime = 0.0

	def __del__(self):
		ui.Bar.__del__(self)

	def SetAlpha(self, alpha):
		color = grp.GenerateColor(self.fadeColor, self.fadeColor, self.fadeColor, alpha)
		self.SetColor(color)

	def FadeOut(self, speed):
		self.curAlpha = 0.0
		self.__StartFade(self.STATE_OUT, 0.0, speed)

	def FadeIn(self, speed):
		self.curAlpha = 1.0
		self.__StartFade(self.STATE_IN, 0.0, speed)

	def WhiteOut(self, speed):
		self.curAlpha = 0.0
		self.__StartFade(self.STATE_OUT, 1.0, speed)

	def WhiteIn(self, speed):
		self.curAlpha = 1.0
		self.__StartFade(self.STATE_IN, 1.0, speed)

	def __StartFade(self, state, color, speed):
		self.state = state
		self.fadeColor = color
		self.Show()
		self.lastFadeTime = 0.0   # reset, zeby pierwsza klatka nie skoczyla

		self.speed = self.DEFAULT_FADE_SPEED
		if 0 != speed:
			self.speed = speed

	def __EndFade(self):
		event.EndEventProcess(self.eventIndex)

	def OnUpdate(self):

		# Fade szedl stalym krokiem na KLATKE (0.035), wiec po odblokowaniu limitu FPS
		# przy 1000 FPS trwal 35 ms zamiast ~0.58 s - questowe fade_out/fade_in bylo
		# mignieciem. Skalujemy krokiem czasu: tempo jak przy 60 FPS, niezaleznie od FPS.
		scale, self.lastFadeTime = ui.GetFrameStepScale(self.lastFadeTime)
		step = self.speed * scale

		if self.STATE_OUT == self.state:

			self.curAlpha += step

			if self.curAlpha >= 1.0:

				self.state = self.STATE_WAIT
				self.curAlpha = 1.0
				self.__EndFade()

		elif self.STATE_IN == self.state:

			self.curAlpha -= step

			if self.curAlpha <= 0.0:

				self.state = self.STATE_WAIT
				self.curAlpha = 0.0
				self.__EndFade()
				self.Hide()

		self.SetAlpha(self.curAlpha)

class BarButton(ui.Button):
	ColorUp = 0x40999999
	ColorDown = 0x40aaaacc
	ColorOver = 0x40ddddff

	UP=0
	DOWN=1
	OVER=2

	def __init__(self, layer = "UI",
			aColorUp   = ColorUp,
			aColorDown = ColorDown,
			aColorOver = ColorOver):
		ui.Button.__init__(self,layer)
		self.state = self.UP
		self.colortable = aColorUp, aColorDown, aColorOver

	def OnRender(self):
		x,y = self.GetGlobalPosition()
		grp.SetColor(self.colortable[self.state])
		grp.RenderBar(x,y,self.GetWidth(),self.GetHeight())

	def CallEvent(self):
		self.state = self.UP
		ui.Button.CallEvent(self)

	def DownEvent(self):
		self.state = self.DOWN

	def ShowToolTip(self):
		self.state = self.OVER

	def HideToolTip(self):
		self.state = self.UP

class DescriptionWindow(ui.Window):
	def __init__(self,idx):
		ui.Window.__init__(self, "TOP_MOST")
		self.descIndex = idx
	def __del__(self):
		ui.Window.__del__(self)
	def OnRender(self):
		event.RenderEventSet(self.descIndex)

class QuestDialog(ui.ScriptWindow):

	TITLE_STATE_NONE = 0
	TITLE_STATE_APPEAR = 1
	TITLE_STATE_SHOW = 2
	TITLE_STATE_DISAPPEAR = 3

	SKIN_NONE = 0
	SKIN_CINEMA = 5

	QUEST_BUTTON_MAX_NUM = 8

	def __init__(self,skin,idx):

		ui.ScriptWindow.__init__(self)
		self.SetWindowName("quest dialog")

		self.focusIndex = 0

		self.board = None
		self.sx = 0
		self.sy = 0

		self.skin = skin
		if skin == 3:
			event.SetRestrictedCount(idx,36)
		else:
			event.SetRestrictedCount(idx,60)

		QuestCurtain.BarHeight = (wndMgr.GetScreenHeight()-wndMgr.GetScreenWidth()*9//16)//2

		if QuestCurtain.BarHeight<0:
			QuestCurtain.BarHeight = 50
		if not ('QuestCurtain' in QuestDialog.__dict__):
			QuestDialog.QuestCurtain = QuestCurtain()
			QuestDialog.QuestCurtain.Show()

		QuestDialog.QuestCurtain.CurtainMode = 1
		self.nextCurtainMode = 0
		if self.skin:
			QuestDialog.QuestCurtain.CurtainMode = 1
			self.nextCurtainMode = 0
			self.LoadDialog(self.skin)
		else:
			QuestDialog.QuestCurtain.CurtainMode = -1
			self.nextCurtainMode = -1

		self.descIndex = idx
		self.descWindow = DescriptionWindow(idx)
		self.descWindow.Show()
		self.eventCurtain = EventCurtain(idx)
		event.SetEventHandler(idx, self)

		self.OnCloseEvent = None
		self.btnAnswer = None
		self.btnNext = None
		self.imgLeft = None
		self.imgTop = None
		self.imgBackground = None
		self.imgTitle = None
		self.titleState = self.TITLE_STATE_NONE
		self.titleShowTime = 0
		self.images = []
		self.prevbutton = None
		self.nextbutton = None

		self.needInputString = False
		self.editSlot = None
		self.editLine = None

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def LoadDialog(self, skin):
		try:
			PythonScriptLoader = ui.PythonScriptLoader()
			PythonScriptLoader.LoadScriptFile(self, "kowal/ui/questdialog.py")
		except RuntimeError:
			dbg.TraceError("QuestDialog.LoadDialog")

		try:
			self.board = self.GetChild('board')
		except RuntimeError:
			dbg.TraceError("QuestDialog.BindObject")

		self.SetCenterPosition()
		if self.SKIN_CINEMA == skin:
			self.board.Hide()

	def OnCancel(self):
		self.nextCurtainMode = -1
		self.CloseSelf()

	def CloseSelf(self):
		QuestDialog.QuestCurtain.CurtainMode = self.nextCurtainMode
		self.btnNext = None
		self.descWindow = None
		self.btnAnswer = None
		self.Destroy()
		if self.descIndex is not None:	# indeks 0 jest prawidlowy - "if self.descIndex" pomijal go (wyciek + wiszacy wskaznik)
			event.ClearEventSet(self.descIndex)
			self.descIndex = None

		self.focusIndex = 0

	def Destroy(self):
		self.ClearDictionary()
		if self.OnCloseEvent:
			self.OnCloseEvent()
			self.OnCloseEvent = None

			if self.needInputString:
				if self.editLine:
					text = self.editLine.GetText()
					net.SendQuestInputStringPacket(text)

		self.imgTitle = None
		self.images = None
		self.eventCurtain = None
		self.board = None

	def OnUpdate(self):
		if self.skin == self.SKIN_CINEMA:
			event.UpdateEventSet(self.descIndex, 50, -(wndMgr.GetScreenHeight() - 44))

		elif self.skin == 3:
			if self.board:
				event.UpdateEventSet(self.descIndex, self.board.GetGlobalPosition()[0]+20+self.sx, -self.board.GetGlobalPosition()[1]-20-self.sy)
				event.SetEventSetWidth(self.descIndex, self.board.GetWidth()-40)
		elif self.skin:
			if self.board:
				event.UpdateEventSet(self.descIndex, self.board.GetGlobalPosition()[0]+20, -self.board.GetGlobalPosition()[1]-20)
				event.SetEventSetWidth(self.descIndex, self.board.GetWidth()-40)
		else:
			event.UpdateEventSet(self.descIndex, 0, 0)

		if self.TITLE_STATE_NONE != self.titleState:

			curTime = app.GetTime()
			elapsedTime = app.GetTime() - self.titleShowTime

			if self.TITLE_STATE_APPEAR == self.titleState:
				self.imgTitle.SetAlpha(elapsedTime*2)
				if elapsedTime > 0.5:
					self.titleState = self.TITLE_STATE_SHOW
					self.titleShowTime = curTime

			elif self.TITLE_STATE_SHOW == self.titleState:
				if elapsedTime > 1.0:
					self.titleState = self.TITLE_STATE_DISAPPEAR
					self.titleShowTime = curTime

			elif self.TITLE_STATE_DISAPPEAR == self.titleState:
				self.imgTitle.SetAlpha(1.0 - elapsedTime*2)
				if elapsedTime > 0.5:
					self.titleState = self.TITLE_STATE_NONE
					self.titleShowTime = curTime


	def AddOnCloseEvent(self,f):
		if self.OnCloseEvent:
			self.OnCloseEvent = lambda z=[self.OnCloseEvent, f]:[fn() for fn in z]
		else:
			self.OnCloseEvent = f

	def AddOnDoneEvent(self,f):
		QuestCurtain.OnDoneEventList.append(f)

	def SetOnCloseEvent(self,f):
		self.OnCloseEvent = f

	def SetEventSetPosition(self, x, y):
		self.sx = x
		self.sy = y

	def AdjustEventSetPosition(self, x, y):
		self.sx += x
		self.sy += y

	def MakeNextButton(self, button_type):
		if self.SKIN_NONE == self.skin:
			return

		yPos = event.GetEventSetLocalYPosition(self.descIndex)

		b = BarButton()
		b.SetParent(self.board)

		b.SetSize(100,26)
		b.SetPosition(self.sx+self.board.GetWidth() // 2-50,self.sy+yPos)

		self.nextButtonType = button_type;

		import localeInfo
		if event.BUTTON_TYPE_CANCEL == button_type:
			b.SetEvent(lambda s=self:event.SelectAnswer(s.descIndex, 254) or s.OnCancel())
			b.SetText(localeInfo.UI_CANCEL)
		elif event.BUTTON_TYPE_DONE == button_type:
			b.SetEvent(lambda s=self:s.CloseSelf())
			b.SetText(localeInfo.UI_OK)
		elif event.BUTTON_TYPE_NEXT == button_type:
			b.SetEvent(lambda s=self:event.SelectAnswer(s.descIndex, 254) or s.CloseSelf())
			b.SetText(localeInfo.UI_NEXT)
		b.Show()
		b.SetTextColor(0xffffffff)
		self.btnNext = b


	def MakeQuestion(self, n):
		global entire_questbutton_number
		global entire_questpage_number
		global cur_questpage_number
		entire_questpage_number = ((n-2)//7)+1
		entire_questbutton_number = n

		if not self.board:
			return

		self.btnAnswer = [self.MakeEachButton(i) for i in range (n)]

		import localeInfo
		self.prevbutton = self.MakeNextPrevPageButton()
		self.prevbutton.SetPosition(self.sx+self.board.GetWidth() // 2-164, self.board.GetHeight() // 2-16)
		self.prevbutton.SetText(localeInfo.UI_PREVPAGE)
		self.prevbutton.SetEvent(self.PrevQuestPageEvent, 1, n)

		self.nextbutton = self.MakeNextPrevPageButton()
		self.nextbutton.SetPosition(self.sx+self.board.GetWidth() // 2+112, self.board.GetHeight() // 2-16)
		self.nextbutton.SetText(localeInfo.UI_NEXTPAGE)
		self.nextbutton.SetEvent(self.NextQuestPageEvent, 1, n)

		if cur_questpage_number != 1:
			cur_questpage_number = 1

	def MakeEachButton(self, i):
		if self.skin == 3:
			button = BarButton("TOP_MOST",0x50000000, 0x50404040, 0x50606060)
			button.SetParent(self.board)
			button.SetSize(106,26)
			button.SetPosition(self.sx + self.board.GetWidth() // 2+((i*2)-1)*56-56, self.sy+(event.GetLineCount(self.descIndex))*16+20+5)
			button.SetText("a")
			button.SetTextColor(0xff000000)
		else:
			i = i % 8
			button = BarButton("TOP_MOST")
			button.SetParent(self.board)
			button.SetSize(200,26)
			button.SetPosition(self.sx + self.board.GetWidth() // 2-100,self.sy+(event.GetLineCount(self.descIndex)+i*2)*16+20+5)
			button.SetText("a")
			button.SetTextColor(0xffffffff)
		return button

	def MakeNextPrevPageButton(self):
		button = BarButton("TOP_MOST")
		button.SetParent(self.board)
		button.SetSize(52,26)
		button.SetText("a")
		button.SetTextColor(0xffffffff)
		return button

	def RefreshQuestPage(self, n):
		global cur_questpage_number
		global entire_questpage_number
		num = 0
		Showing_button_inx = (cur_questpage_number-1)* self.QUEST_BUTTON_MAX_NUM

		while num < n:
			if num >= Showing_button_inx and num < Showing_button_inx + self.QUEST_BUTTON_MAX_NUM:
				self.btnAnswer[num].Show()
			else:
				self.btnAnswer[num].Hide()
			num = num + 1

		if cur_questpage_number == 1:
			self.prevbutton.Hide()
			self.nextbutton.Show()
		elif cur_questpage_number == entire_questpage_number:
			self.prevbutton.Show()
			self.nextbutton.Hide()
		else:
			self.prevbutton.Show()
			self.nextbutton.Show()

	def NextQuestPageEvent(self, one, n):
		global cur_questpage_number
		cur_questpage_number = cur_questpage_number + one
		self.RefreshQuestPage(n)

	def PrevQuestPageEvent(self, one, n):
		global cur_questpage_number
		cur_questpage_number = cur_questpage_number - one
		self.RefreshQuestPage(n)

	def ClickAnswerEvent(self, ai):
		event.SelectAnswer(self.descIndex, ai)
		self.nextbutton = None
		self.prevbutton = None
		self.CloseSelf()

	def AppendQuestion(self, name, idx):
		if not self.btnAnswer:
			return

		self.btnAnswer[idx].SetText(name)
		x, y= self.btnAnswer[idx].GetGlobalPosition()

		self.btnAnswer[idx].SetEvent(self.ClickAnswerEvent, idx)

		global entire_questbutton_number

		Showing_button_idx = (cur_questpage_number-1)* self.QUEST_BUTTON_MAX_NUM

		if Showing_button_idx <= idx and idx < Showing_button_idx + self.QUEST_BUTTON_MAX_NUM:
			self.btnAnswer[idx].Show()
		else:
			self.btnAnswer[idx].Hide()
		if entire_questbutton_number >= self.QUEST_BUTTON_MAX_NUM:
			self.nextbutton.Show()

	def FadeOut(self, speed):
		self.eventCurtain.FadeOut(speed)

	def FadeIn(self, speed):
		self.eventCurtain.FadeIn(speed)

	def WhiteOut(self, speed):
		self.eventCurtain.WhiteOut(speed)

	def WhiteIn(self, speed):
		self.eventCurtain.WhiteIn(speed)

	def DoneEvent(self):
		self.nextCurtainMode = -1
		if self.SKIN_NONE == self.skin or self.SKIN_CINEMA == self.skin:
			self.CloseSelf()

	def __GetQuestImageFileName(self, filename):
		if len(filename) > 1:
			if filename[1]!=':':
				filename = QUEST_BOARD_IMAGE_DIR+filename

		return filename

	def OnKeyDown(self, key):
		if self.btnAnswer == None:
																		 
			if None != self.btnNext:
				if app.DIK_RETURN == key:
					self.OnPressEscapeKey()

				if app.DIK_UP == key or app.DIK_DOWN == key:
					self.btnNext.ShowToolTip()

			return True

		focusIndex = self.focusIndex;
		lastFocusIndex = focusIndex;


		answerCount = len(self.btnAnswer)

		if app.DIK_DOWN == key:
			focusIndex += 1

		if app.DIK_UP == key:
			focusIndex -= 1

		if focusIndex < 0:
			focusIndex = answerCount - 1

		if focusIndex >= answerCount:
			focusIndex = 0

		self.focusIndex = focusIndex;

		focusBtn = self.btnAnswer[focusIndex]
		lastFocusBtn = self.btnAnswer[lastFocusIndex]

		if focusIndex != lastFocusIndex:
			focusBtn.ShowToolTip()
			lastFocusBtn.HideToolTip()

		if app.DIK_RETURN == key:
			focusBtn.CallEvent()

		return True

	def OnPressEscapeKey(self):

																	
		if None != self.btnNext:
			if event.BUTTON_TYPE_CANCEL == self.nextButtonType:
				event.SelectAnswer(self.descIndex, 254)
				self.OnCancel()
			elif event.BUTTON_TYPE_DONE == self.nextButtonType:
				self.CloseSelf()
			elif event.BUTTON_TYPE_NEXT == self.nextButtonType:
				event.SelectAnswer(self.descIndex, 254)
				self.CloseSelf()
		else:
			event.SelectAnswer(self.descIndex, entire_questbutton_number - 1)
			self.nextbutton = None
			self.prevbutton = None
			self.CloseSelf()
		return True

	def OnIMEReturn(self):
		if self.needInputString:
			self.CloseSelf()
			return True

	def OnIMEUpdate(self):
		if not self.needInputString:
			return

		if not self.editLine:
			return

		self.editLine.OnIMEUpdate()

	def OnInput(self):

		self.needInputString = True

		event.AddEventSetLocalYPosition(self.descIndex, 5+10)
		yPos = event.GetEventSetLocalYPosition(self.descIndex)

		self.editSlot = ui.SlotBar()
		self.editSlot.SetSize(200, 18)
		self.editSlot.SetPosition(0, yPos)
		self.editSlot.SetParent(self.board)
		self.editSlot.SetWindowHorizontalAlignCenter()
		self.editSlot.Show()

		self.editLine = ui.EditLine()
		self.editLine.SetParent(self.editSlot)
		self.editLine.SetPosition(3, 3)
		self.editLine.SetSize(200, 17)
		self.editLine.SetMax(30)
		self.editLine.SetFocus()
		self.editLine.Show()

		event.AddEventSetLocalYPosition(self.descIndex, 25+10)

		self.MakeNextButton(event.BUTTON_TYPE_DONE)

		self.editLine.UpdateRect()
		self.editSlot.UpdateRect()
		self.board.UpdateRect()

	def OnImage(self, x, y, filename, desc=""):
		filename = self.__GetQuestImageFileName(filename)

		try:
			img = ui.MakeImageBox(self.board, filename, x, y)
			self.images.append(img)
		except RuntimeError:
			pass

	def OnInsertItemIcon(self, type, idx, title, desc, index=0, total=1):
		if "item" != type:
			return

		import item
		item.SelectItem(idx)
		filename = item.GetIconImageFileName()

		underTitle = title

		# Quest moze nie podac tytulu/opisu (say_item_vnum2 wysyla puste pola) - wtedy
		# bierzemy je z danych itemu po stronie klienta. underTitle ustawiamy razem z
		# tytulem, bo inaczej ikona zostaje bez zadnego podpisu.
		if not title:
			title = item.GetItemName()
			underTitle = title

		if not desc:
			tempDesc = item.GetItemDescription()
			desc = ""

			if tempDesc:
				import grpText
				lineCount = grpText.GetSplitingTextLineCount(tempDesc, 25)
				for i in range(lineCount):
					desc += grpText.GetSplitingTextLine(tempDesc, 25, i) + "/"

				desc = desc[:-1]

		self.OnInsertImage(filename, underTitle, title, desc, index, total)

	def OnInsertImage(self, filename, underTitle, title, desc, index=0, total=1):

		if index == 0:
			event.AddEventSetLocalYPosition(self.descIndex, 24)

		y = event.GetEventSetLocalYPosition(self.descIndex)
		xBoard, yBoard = self.board.GetGlobalPosition()

		try:
			img = ToolTipImageBox()
			img.SetParent(self.board)
			img.LoadImage(filename)
			pos_x = (self.board.GetWidth() * (index + 1) // (total + 1)) - (img.GetWidth() // 2)
			img.SetPosition(pos_x, y)
			img.DestroyToolTip()
			if title and desc:
				img.CreateToolTip(self.board, title, desc, 0, yBoard + y + img.GetHeight())
			img.Show()
			self.images.append(img)
		except RuntimeError:
			pass

		event.AddEventSetLocalYPosition(self.descIndex, img.GetHeight() - 20)

		if underTitle:
			event.AddEventSetLocalYPosition(self.descIndex, 3)
			event.InsertTextInline(self.descIndex, underTitle, (self.board.GetWidth() * (index + 1) // (total + 1)))
			if index != total - 1:
				event.AddEventSetLocalYPosition(self.descIndex, -( 3 + 16 ))
		else:
			if index == total - 1:
				event.AddEventSetLocalYPosition(self.descIndex, 4)

		if index != total - 1:
			event.AddEventSetLocalYPosition(self.descIndex, -(img.GetHeight() - 20))



	def OnSize(self, width, height):
		self.board.SetSize(width, height)

	def OnTitleImage(self, filename):
		img = ui.ImageBox("TOP_MOST")

		try:
			img.SetWindowHorizontalAlignCenter()
			img.LoadImage(filename)
			img.SetPosition(0, wndMgr.GetScreenHeight() - (75//2) - (32//2))
			img.SetAlpha(0.0)
			img.Show()
		except RuntimeError:
			dbg.TraceError("QuestDialog.OnTitleImage(%s)" % filename)
			img.Hide()

		self.imgTitle = img
		self.titleState = self.TITLE_STATE_APPEAR
		self.titleShowTime = app.GetTime()

	def OnLeftImage(self, imgfile):
		imgfile = self.__GetQuestImageFileName(imgfile)
		if not self.imgLeft:
			self.imgLeft = ui.ExpandedImageBox("TOP_MOST")
			self.imgLeft.SetParent(self)
			self.imgLeft.SetPosition(0,0)
			bd = self.board
			bx, by = bd.GetLocalPosition()
			bd.SetPosition(160,by)
			if self.imgTop:
				tx, ty = self.imgTop.GetLocalPosition()
				self.imgTop.SetPosition(160,ty)

		try:
			self.imgLeft.LoadImage(imgfile)
			self.imgLeft.SetSize(400,450)
			self.imgLeft.SetOrigin(self.imgLeft.GetWidth() // 2,self.imgLeft.GetHeight() // 2)
			self.imgLeft.Show()
		except RuntimeError:
			import dbg
			dbg.TraceError("QuestDialog.OnLeftImage(%s)" % imgfile)
			self.imgLeft.Hide()

	def OnTopImage(self, imgfile):
		imgfile = self.__GetQuestImageFileName(imgfile)

		bd = self.board
		bx, by = bd.GetLocalPosition()
		if not self.imgTop:
			self.imgTop = ui.ExpandedImageBox("TOP_MOST")
			self.imgTop.SetParent(self)
			bd.SetPosition(bx,190)
			self.imgTop.SetPosition(bx,10)

		try:
			self.imgTop.LoadImage(imgfile)
			h = self.imgTop.GetHeight()
			if h>170:
				bd.SetPosition(bx,20+h)
				bd.SetSize(350,420-h)
				self.imgTop.SetSize(350,h)
			else:
				self.imgTop.SetSize(350,170)
				bd.SetPosition(bx,190)
				bd.SetSize(350,250)
			self.imgTop.SetOrigin(self.imgTop.GetWidth() // 2,self.imgTop.GetHeight() // 2)
			self.imgTop.Show()
		except RuntimeError:
			dbg.TraceError("QuestDialog.OnTopImage(%s)" % imgfile)
			self.imgTop.Hide()

	def OnBackgroundImage(self, imgfile):
		imgfile = self.__GetQuestImageFileName(imgfile)
		c = self.board
		w = c.GetWidth()
		h = c.GetHeight()
		px, py = c.GetLocalPosition()
		moved = 0
		if not self.imgBackground:
			self.imgBackground = ui.ExpandedImageBox("TOP_MOST")
			self.imgBackground.SetParent(c)
			self.imgBackground.SetPosition(0,0)
		try:
			self.imgBackground.LoadImage(imgfile)
		except RuntimeError:
			dbg.TraceError("QuestDialog.OnBackgroundImage(%s)" % imgfile)
			self.imgBackground.Hide()
			return
		iw = self.imgBackground.GetWidth()
		ih = self.imgBackground.GetHeight()
		if self.skin==3:
			iw = 256
			ih = 333
			self.imgBackground.SetSize(iw,ih)
		if w < iw:
			px -= (iw-w)//2
			c.SetPosition(px,py)
			w = iw
		if h < ih:
			py -= (ih-h)//2
			c.SetPosition(px,py)
			h = ih
		if self.skin == 3:
			w=256
			h = 333
			self.sx = 0
			self.sy = 100

		c.SetSize(w,h)
		c.HideInternal()

		c.SetWindowHorizontalAlignCenter()
		c.SetWindowVerticalAlignCenter()

		c.SetPosition(0,0)
		if self.skin==3:
			c.SetPosition(-190,0)

		self.imgBackground.SetWindowHorizontalAlignCenter()
		self.imgBackground.SetWindowVerticalAlignCenter()
		self.imgBackground.SetPosition(0,0)
		self.imgBackground.Show()
