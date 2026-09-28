#-*- coding: iso-8859-1 -*-
import ui
import grp
import app
import re
import wndMgr

class TextBar(ui.Window):
	def __init__(self, width, height):
		ui.Window.__init__(self)
		self.handle = grp.CreateTextBar(width, height)

	def __del__(self):
		ui.Window.__del__(self)
		grp.DestroyTextBar(self.handle)

	def ClearBar(self):
		grp.ClearTextBar(self.handle)

	def SetClipRect(self, x1, y1, x2, y2):
		grp.SetTextBarClipRect(self.handle, x1, y1, x2, y2)

	def TextOut(self, x, y, text):
		grp.TextBarTextOut(self.handle, int(x), int(y), text)

	def OnRender(self):
		x, y = self.GetGlobalPosition()
		grp.RenderTextBar(self.handle, x, y)

	def SetTextColor(self, r, g, b):
		grp.TextBarSetTextColor(self.handle, r, g, b)

	def GetTextExtent(self, text):
		return grp.TextBarGetTextExtent(self.handle, text)

class TipBoard(ui.Bar):
	TIP_DURATION = 5.0
	def __init__(self):
		ui.Bar.__init__(self)
		self.AddFlag("not_pick")
		self.tipList = []
		self.nextScrollTime = 0
		self.SetPosition(0, 70)
		self.SetSize(370, 20)
		self.SetColor(grp.GenerateColor(0.0, 0.0, 0.0, 0.5))
		self.SetWindowHorizontalAlignCenter()
		self.__CreateTextBar()

	def __del__(self):
		ui.Bar.__del__(self)

	def __CreateTextBar(self):
		x, y = self.GetGlobalPosition()
		self.textBar = ui.TextLine()
		self.textBar.SetParent(self)
		self.textBar.SetWindowHorizontalAlignCenter()
		self.textBar.SetHorizontalAlignCenter()
		self.textBar.SetPosition(3, 3)	 
		self.textBar.Show()

	def __CleanOldTip(self):
		leaveList = []

		for tip in self.tipList:
			madeTime = tip[0]
			if app.GetTime() - madeTime > self.TIP_DURATION:
				pass
			else:
				leaveList.append(tip)

		self.tipList = leaveList

		if not leaveList:
			self.textBar.Hide()
			self.Hide()
			return

		self.__RefreshBoard()

	def __RefreshBoard(self):
		self.textBar.Hide()
		index = 0
		for tip in self.tipList:
			text = tip[1]
			self.textBar.SetText(str(text))
			self.textBar.Show()
			index += 1

	def SetTip(self, text):
		filtered_word = ['Pokonał', 'Pokonała', 'w czasie:', 'ukończył/a']

		if any(word in text for word in filtered_word):
			return

		if not app.IsVisibleNotice():
			return

		curTime = app.GetTime()
		self.tipList.append((curTime, text))
		self.__RefreshBoard()
		self.nextScrollTime = app.GetTime()

		if not self.IsShow():
			self.Show()

	def OnUpdate(self):
		if not self.tipList:
			self.Hide()
			return

		if (app.GetTime() > (self.nextScrollTime)):
			self.nextScrollTime = app.GetTime()
			self.__CleanOldTip()

class BigTextBar(TextBar):
	def __init__(self, width, height, fontSize):
		ui.Window.__init__(self)
		self.handle = grp.CreateBigTextBar(width, height, fontSize)


class BigBoard(ui.Bar):

	SCROLL_WAIT_TIME = 5.0
	TIP_DURATION = 10.0
	FONT_WIDTH	= 18
	FONT_HEIGHT	= 18
	LINE_WIDTH  = 500
	LINE_HEIGHT	= FONT_HEIGHT + 5
	STEP_HEIGHT = LINE_HEIGHT * 2
	LINE_CHANGE_LIMIT_WIDTH = 350

	FRAME_IMAGE_FILE_NAME_LIST = [
		"season1/interface/oxevent/frame_0.sub",
		"season1/interface/oxevent/frame_1.sub",
		"season1/interface/oxevent/frame_2.sub",
	]

	FRAME_IMAGE_STEP = 256

	FRAME_BASE_X = -20
	FRAME_BASE_Y = -12

	def __init__(self):
		ui.Bar.__init__(self)

		self.AddFlag("not_pick")
		self.tipList = []
		self.curPos = 0
		self.dstPos = 0
		self.nextScrollTime = 0

		self.SetPosition(0, 150)
		self.SetSize(512, 55)
		self.SetColor(grp.GenerateColor(0.0, 0.0, 0.0, 0.5))
		self.SetWindowHorizontalAlignCenter()

		self.__CreateTextBar()
		self.__LoadFrameImages()


	def __LoadFrameImages(self):
		x = self.FRAME_BASE_X
		y = self.FRAME_BASE_Y
		self.imgList = []
		for imgFileName in self.FRAME_IMAGE_FILE_NAME_LIST:
			self.imgList.append(self.__LoadImage(x, y, imgFileName))
			x += self.FRAME_IMAGE_STEP

	def __LoadImage(self, x, y, fileName):
		img = ui.ImageBox()
		img.SetParent(self)
		img.AddFlag("not_pick")
		img.LoadImage(fileName)
		img.SetPosition(x, y)
		img.Show()
		return img

	def __del__(self):
		ui.Bar.__del__(self)

	def __CreateTextBar(self):
		# Przepisane z legacy CTextBar (GDI/DIB - jedyny uzytkownik w kliencie,
		# nie renderowal tekstu) na ui.TextLine, jak dzialajacy TipBoard.
		self.textBar = ui.TextLine()
		self.textBar.SetParent(self)
		self.textBar.SetWindowHorizontalAlignCenter()
		self.textBar.SetHorizontalAlignCenter()
		self.textBar.SetWindowVerticalAlignCenter()
		self.textBar.SetVerticalAlignCenter()
		self.textBar.SetPosition(0, 0)
		self.textBar.SetFontName("Verdana:18")
		self.textBar.SetPackedFontColor(grp.GenerateColor(0.949, 0.906, 0.757, 1.0))
		self.textBar.SetOutline()
		self.textBar.Show()

	def __CleanOldTip(self):
		curTime = app.GetTime()
		leaveList = []
		for madeTime, text in self.tipList:
			if curTime + self.TIP_DURATION <= madeTime:
				leaveList.append(text)

		self.tipList = leaveList

		if not leaveList:
			self.textBar.ClearBar()
			self.Hide()
			return

		self.__RefreshBoard()

	def __RefreshBoard(self):
		if self.tipList:
			self.textBar.SetText(str(self.tipList[-1][1]))
			self.textBar.Show()
		else:
			self.textBar.SetText("")
			self.textBar.Hide()

	def SetTip(self, text):
		filtered_word = ['Pokonał', 'Pokonała', 'w czasie:', 'ukończył/a']

		if any(word in text for word in filtered_word):
			return
			
		if not app.IsVisibleNotice():
			return

		curTime = app.GetTime()
		self.tipList = [(curTime, text)]
		self.__RefreshBoard()

		if not self.IsShow():
			self.Show()

	def __AppendText(self, curTime, text):
		import dbg
		prevPos = 0
		while 1:
			curPos = text.find(" ", prevPos)
			if curPos < 0:
				break

			(text_width, text_height) = self.textBar.GetTextExtent(text[:curPos])
			if text_width > self.LINE_CHANGE_LIMIT_WIDTH:
				self.tipList.append((curTime, text[:prevPos]))
				self.tipList.append((curTime, text[prevPos:]))
				return

			prevPos = curPos + 1

		self.tipList.append((curTime, text))

	def OnUpdate(self):
		if not self.tipList:
			self.Hide()
			return

		curTime = app.GetTime()
		self.tipList = [t for t in self.tipList if curTime - t[0] < self.TIP_DURATION]

		if not self.tipList:
			self.textBar.SetText("")
			self.textBar.Hide()
			self.Hide()

if __name__ == "__main__":
	import app
	import wndMgr
	import systemSetting
	import mouseModule
	import grp
	import ui


	app.SetMouseHandler(mouseModule.mouseController)
	app.SetHairColorEnable(True)
	wndMgr.SetMouseHandler(mouseModule.mouseController)
	wndMgr.SetScreenSize(systemSetting.GetWidth(), systemSetting.GetHeight())
	app.Create("METIN2 CLOSED BETA", systemSetting.GetWidth(), systemSetting.GetHeight(), 1)
	mouseModule.mouseController.Create()

	wnd = BigBoard()
	wnd.Show()
	wnd.SetTip("ľČłçÇĎĽĽżä")
	wnd.SetTip("Ŕú´Â şřŔÚ·ç ŔÔ´Ď´Ů")

	app.Loop()

