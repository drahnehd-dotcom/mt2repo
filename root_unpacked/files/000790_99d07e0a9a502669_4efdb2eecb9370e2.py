import ui
import localeInfo
import app
import ime
import uiScriptLocale
import re
import constInfo
import chat
# uzywane nizej (wndMgr.GetScreenHeight w powiadomieniu o zakupie, uiToolTip.ToolTip w oknie
# czeku) - brak tych importow konczyl sie NameError przy pierwszym trafieniu
import wndMgr
import uiToolTip


def FrameLerpRatio(perFrameRatio):
	"""Współczynnik wykładniczego dojazdu (cur += (dest - cur) * ratio) przeliczony z KLATEK na CZAS.

	Animacje pisane jako `cur += (dest - cur) / 10.0` liczą się per klatka, więc działały tylko
	dopóki klient siedział na 60 FPS — po odblokowaniu limitu domykają się tyle razy szybciej,
	ile mamy klatek ponad 60. Ten wzór dla dt = 1/60 zwraca dokładnie `perFrameRatio`, czyli
	tempo jest identyczne z dawnym 60 FPS przy dowolnym FPS.

	`app.GetElapsedTime()` to czas poprzedniej klatki w sekundach (clamp 100 ms robi już CTimer).
	"""
	elapsed = app.GetElapsedTime()
	if elapsed <= 0.0:
		return perFrameRatio
	if elapsed > 0.1:	# bezpiecznik: po alt-tabie nie domykaj całej animacji w jednej klatce
		elapsed = 0.1
	return 1.0 - pow(1.0 - perFrameRatio, elapsed * 60.0)


class PopupDialog(ui.ScriptWindow):

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.__LoadDialog()
		self.acceptEvent = lambda *arg: None
		self.is_autoclose = FALSE
		self.autoclose_timer = 0

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __LoadDialog(self):
		try:
			PythonScriptLoader = ui.PythonScriptLoader()
			PythonScriptLoader.LoadScriptFile(self, "UIScript/PopupDialog.py")

			self.board = self.GetChild("board")
			self.message = self.GetChild("message")
			self.accceptButton = self.GetChild("accept")
			self.accceptButton.SetEvent(ui.__mem_func__(self.Close))

		except:
			import exception
			exception.Abort("PopupDialog.LoadDialog.BindObject")

	def Open(self):
		self.SetCenterPosition()
		self.SetTop()
		self.Show()

	def Close(self):
		self.Hide()
		self.acceptEvent()

	def Destroy(self):
		self.Close()
		self.ClearDictionary()

	def SetWidth(self, width):
		height = self.GetHeight()
		self.SetSize(width, height)
		self.board.SetSize(width, height)
		self.SetCenterPosition()
		self.UpdateRect()

	def SetText(self, text):
		self.message.SetText(text)

	def SetAcceptEvent(self, event):
		self.acceptEvent = event

	def SetAutoClose(self, flag, time = 2.5):
		self.is_autoclose = flag
		self.autoclose_timer = app.GetTime() + time

	def SetAutoCloseLong(self, flag, time = 5.0):
		self.is_autoclose = flag
		self.autoclose_timer = app.GetTime() + time

	def SetButtonName(self, name):
		self.accceptButton.SetText(name)

	def OnPressEscapeKey(self):
		self.Close()
		return True

	def OnIMEReturn(self):
		self.Close()
		return True

class InputDialog(ui.ScriptWindow):

	def __init__(self):
		ui.ScriptWindow.__init__(self)

		self.__CreateDialog()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __CreateDialog(self):

		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, "uiscript/inputdialog.py")

		getObject = self.GetChild
		self.board = getObject("Board")
		self.acceptButton = getObject("AcceptButton")
		self.cancelButton = getObject("CancelButton")
		self.inputSlot = getObject("InputSlot")
		self.inputValue = getObject("InputValue")

	def Open(self):
		self.inputValue.SetFocus()
		self.SetCenterPosition()
		self.SetTop()
		self.Show()

	def Close(self):
		self.ClearDictionary()
		self.board = None
		self.acceptButton = None
		self.cancelButton = None
		self.inputSlot = None
		self.inputValue = None
		self.Hide()

	def SetTitle(self, name):
		self.board.SetTitleName(name)

	def SetNumberMode(self):
		self.inputValue.SetNumberMode()

	def SetSecretMode(self):
		self.inputValue.SetSecret()

	def SetFocus(self):
		self.inputValue.SetFocus()

	def SetMaxLength(self, length):
		width = length * 6 + 10
		self.SetBoardWidth(max(width + 50, 160))
		self.SetSlotWidth(width)
		self.inputValue.SetMax(length)

	def SetSlotWidth(self, width):
		self.inputSlot.SetSize(width, self.inputSlot.GetHeight())
		self.inputValue.SetSize(width, self.inputValue.GetHeight())
	def SetBoardWidth(self, width):
		self.SetSize(max(width + 50, 160), self.GetHeight())
		self.board.SetSize(max(width + 50, 160), self.GetHeight())
		self.UpdateRect()

	def SetAcceptEvent(self, event):
		self.acceptButton.SetEvent(event)
		self.inputValue.OnIMEReturn = event

	def SetCancelEvent(self, event):
		self.board.SetCloseEvent(event)
		self.cancelButton.SetEvent(event)
		self.inputValue.OnPressEscapeKey = event

	def GetText(self):
		return self.inputValue.GetText()

class InputDialogWithDescription(InputDialog):

	def __init__(self):
		ui.ScriptWindow.__init__(self)

		self.__CreateDialog()

	def __del__(self):
		InputDialog.__del__(self)

	def __CreateDialog(self):

		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, "uiscript/inputdialogwithdescription.py")

		try:
			getObject = self.GetChild
			self.board = getObject("Board")
			self.acceptButton = getObject("AcceptButton")
			self.cancelButton = getObject("CancelButton")
			self.inputSlot = getObject("InputSlot")
			self.inputValue = getObject("InputValue")
			self.description = getObject("Description")

		except:
			import exception
			exception.Abort("InputDialogWithDescription.LoadBoardDialog.BindObject")

	def SetDescription(self, text):
		self.description.SetText(text)

class InputDialogWithDescription2(InputDialog):

	def __init__(self):
		ui.ScriptWindow.__init__(self)

		self.__CreateDialog()

	def __del__(self):
		InputDialog.__del__(self)

	def __CreateDialog(self):

		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, "uiscript/inputdialogwithdescription2.py")

		try:
			getObject = self.GetChild
			self.board = getObject("Board")
			self.acceptButton = getObject("AcceptButton")
			self.cancelButton = getObject("CancelButton")
			self.inputSlot = getObject("InputSlot")
			self.inputValue = getObject("InputValue")
			self.description1 = getObject("Description1")
			self.description2 = getObject("Description2")

		except:
			import exception
			exception.Abort("InputDialogWithDescription.LoadBoardDialog.BindObject")

	def SetDescription1(self, text):
		self.description1.SetText(text)

	def SetDescription2(self, text):
		self.description2.SetText(text)

class QuestionDialog(ui.ScriptWindow):

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.__CreateDialog()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __CreateDialog(self):
		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, "uiscript/questiondialog.py")

		self.board = self.GetChild("board")
		self.textLine = self.GetChild("message")
		self.acceptButton = self.GetChild("accept")
		self.cancelButton = self.GetChild("cancel")

	def Open(self):
		self.SetCenterPosition()
		self.SetTop()
		self.Show()
		self.SetWidth(self.textLine.GetTextWidth()+50)

	def Close(self):
		self.Hide()

	def SetWidth(self, width):
		height = self.GetHeight()
		self.SetSize(width, height)
		self.board.SetSize(width, height)
		self.SetCenterPosition()
		self.UpdateRect()

	def SAFE_SetAcceptEvent(self, event):
		self.acceptButton.SAFE_SetEvent(event)

	def SAFE_SetCancelEvent(self, event):
		self.cancelButton.SAFE_SetEvent(event)

	def SetAcceptEvent(self, event):
		self.acceptButton.SetEvent(event)

	def SetCancelEvent(self, event):
		self.cancelButton.SetEvent(event)

	def SetText(self, text):
		self.textLine.SetText(text)

	def SetAcceptText(self, text):
		self.acceptButton.SetText(text)

	def SetCancelText(self, text):
		self.cancelButton.SetText(text)

	def OnPressEscapeKey(self):
		self.Close()
		return True

class QuestionDialog2(QuestionDialog):

	def __init__(self):
		QuestionDialog.__init__(self)
		self.__CreateDialog()

	def __del__(self):
		QuestionDialog.__del__(self)

	def __CreateDialog(self):
		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, "uiscript/questiondialog2.py")

		self.board = self.GetChild("board")
		self.textLine1 = self.GetChild("message1")
		self.textLine2 = self.GetChild("message2")
		self.acceptButton = self.GetChild("accept")
		self.cancelButton = self.GetChild("cancel")

	def SetText1(self, text):
		self.textLine1.SetText(text)

	def SetText2(self, text):
		self.textLine2.SetText(text)

	def SetWidth(self, width):
		height = self.GetHeight()
		self.SetSize(width, height)
		self.board.SetSize(width, height)
		self.SetCenterPosition()
		self.UpdateRect()

	def SAFE_SetAcceptEvent(self, event):
		self.acceptButton.SAFE_SetEvent(event)

	def SAFE_SetCancelEvent(self, event):
		self.cancelButton.SAFE_SetEvent(event)

	def SetAcceptEvent(self, event):
		self.acceptButton.SetEvent(event)

	def SetCancelEvent(self, event):
		self.cancelButton.SetEvent(event)

	def SetAcceptText(self, text):
		self.acceptButton.SetText(text)

	def SetCancelText(self, text):
		self.cancelButton.SetText(text)

	def Open(self):
		self.SetCenterPosition()
		self.SetTop()
		self.Show()
		self.SetWidth(self.textLine1.GetTextWidth()+50)

	def Close(self):
		self.Hide()

	def OnPressEscapeKey(self):
		self.Close()
		return True

class QuestionDialogWithTimeLimit(QuestionDialog2):

	def __init__(self):
		ui.ScriptWindow.__init__(self)

		self.__CreateDialog()
		self.endTime = 0

	def __del__(self):
		QuestionDialog2.__del__(self)

	def __CreateDialog(self):
		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, "uiscript/questiondialog2.py")

		self.board = self.GetChild("board")
		self.textLine1 = self.GetChild("message1")
		self.textLine2 = self.GetChild("message2")
		self.acceptButton = self.GetChild("accept")
		self.cancelButton = self.GetChild("cancel")

	def Open(self, msg, timeout):
		self.SetCenterPosition()
		self.SetTop()
		self.Show()

		self.SetText1(msg)
		self.endTime = app.GetTime() + timeout

	def OnUpdate(self):
		leftTime = max(0, self.endTime - app.GetTime())
		self.SetText2(localeInfo.UI_LEFT_TIME % (leftTime))

class MoneyInputDialog(ui.ScriptWindow):

	def __init__(self):
		ui.ScriptWindow.__init__(self)

		self.moneyHeaderText = localeInfo.MONEY_INPUT_DIALOG_SELLPRICE
		self.__CreateDialog()
		self.SetMaxLength(13)

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __CreateDialog(self):

		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, "uiscript/moneyinputdialog.py")

		getObject = self.GetChild
		self.board = self.GetChild("board")
		self.acceptButton = getObject("AcceptButton")
		self.cancelButton = getObject("CancelButton")
		self.inputValue = getObject("InputValue")
		self.inputValue.SetNumberMode()
		self.inputValue.OnIMEUpdate = ui.__mem_func__(self.__OnValueUpdate)
		self.moneyText = getObject("MoneyValue")
		if app.ENABLE_CHEQUE_SYSTEM:
			self.chequeText = getObject("ChequeValue")
			self.inputChequeValue = getObject("InputValue_Cheque")
			self.inputChequeValue.OnIMEUpdate = ui.__mem_func__(self.__OnValueUpdate)
			self.inputChequeValue.OnMouseLeftButtonDown = ui.__mem_func__(self.__ClickChequeEditLine)
			self.inputValue.OnMouseLeftButtonDown = ui.__mem_func__(self.__ClickValueEditLine)

	def Open(self):
		self.inputValue.SetText("")
		self.inputValue.SetFocus()
		self.__OnValueUpdate()
		self.SetCenterPosition()
		self.SetTop()
		self.Show()

	def Close(self):
		self.ClearDictionary()
		self.board = None
		self.acceptButton = None
		self.cancelButton = None
		self.inputValue = None
		if app.ENABLE_CHEQUE_SYSTEM:
			self.inputChequeValue = None
		self.Hide()

	def SetTitle(self, name):
		self.board.SetTitleName(name)

	def SetFocus(self):
		self.inputValue.SetFocus()

	def SetMaxLength(self, length):
		length = min(13, length)
		self.inputValue.SetMax(length)

	def SetMoneyHeaderText(self, text):
		self.moneyHeaderText = text

	def SetAcceptEvent(self, event):
		self.acceptButton.SetEvent(event)
		self.inputValue.OnIMEReturn = event

	def SetCancelEvent(self, event):
		self.board.SetCloseEvent(event)
		self.cancelButton.SetEvent(event)
		self.inputValue.OnPressEscapeKey = event

	def SetValue(self, value):
		value=str(value)
		self.inputValue.SetText(value)
		self.__OnValueUpdate()
		ime.SetCursorPosition(len(value))

	def GetText(self):
		return self.inputValue.GetText()

	if app.ENABLE_CHEQUE_SYSTEM:
		def SetCheque(self, cheque):
			cheque=str(cheque)
			self.inputChequeValue.SetText(cheque)
			self.__OnValueUpdate()
			ime.SetCursorPosition(len(cheque)+1)

		def GetTextCheque(self):
			return self.inputChequeValue.GetText()

		def __ClickChequeEditLine(self):
			self.inputChequeValue.SetFocus()
			if len(self.inputValue.GetText()) <= 0:
				self.inputValue.SetText(str(0))

		def __ClickValueEditLine(self):
			self.inputValue.SetFocus()
			if len(self.inputChequeValue.GetText()) <= 0:
				self.inputChequeValue.SetText(str(0))

		def GetCheque(self):
			return self.inputChequeValue.GetText()

		def __OnValueUpdate(self):
			if self.inputValue.IsFocus():
				ui.EditLine.OnIMEUpdate(self.inputValue)
			elif self.inputChequeValue.IsFocus():
				ui.EditLine.OnIMEUpdate(self.inputChequeValue)
			else:
				pass

			text = self.inputValue.GetText()
			cheque_text = self.inputChequeValue.GetText()

			money = 0
			cheque = 0
			GOLD_MAX = 1000000000000000
			CHEQUE_MAX = 1000000000000000

			if text and text.isdigit():
				try:
					money = int(text)
					
					if money >= GOLD_MAX:
						money = GOLD_MAX - 1
						self.inputValue.SetText(str(money))
				except ValueError:
					money = 0

			if cheque_text and cheque_text.isdigit():
				try:
					cheque = int(cheque_text)
					
					if cheque >= CHEQUE_MAX:
						cheque = CHEQUE_MAX - 1
						self.inputValue.SetText(str(cheque))
				except ValueError:
					cheque = 0
			self.chequeText.SetText(localeInfo.NumberToCheque(cheque))
			self.moneyText.SetText(localeInfo.NumberToMoneyString(money))
	else:
		def __OnValueUpdate(self):
			ui.EditLine.OnIMEUpdate(self.inputValue)

			text = self.inputValue.GetText()

			money = 0
			if text and text.isdigit():
				try:
					money = int(text)
				except ValueError:
					money = 199999999

			self.moneyText.SetText(self.moneyHeaderText + localeInfo.NumberToMoneyString(money))


class ChatColorMenu(ui.ImageBox):
	COLOR_LIST = { 
        "colors": [
			ui.GenerateColor(255, 255, 255),
			ui.GenerateColor(0, 128, 255),
			ui.GenerateColor(255, 0, 0),
			ui.GenerateColor(255, 255, 0),
			ui.GenerateColor(0, 255, 0),
			ui.GenerateColor(255, 165, 0),
			ui.GenerateColor(64, 224, 208),
			ui.GenerateColor(0, 0, 0),
			ui.GenerateColor(160, 32, 240),
			ui.GenerateColor(255, 105, 180),
		],
		"hex" : [
			"|cffe3e6e4",
			"|cff284feb",
			"|cffd6151f",
			"|cffd6bf15",
			"|cff15d618",
			"|cffd69f15",
			"|cff15d6c9",
			"|cff020303",
			"|cff9204de",
			"|cfff26beb",
		]
	}

	def __init__(self):
		ui.ImageBox.__init__(self)
		self.AddFlag("float")
		self.is_loaded = False
		self.selectedColor = self.COLOR_LIST["hex"][0]

	def __del__(self):
		ui.ImageBox.__del__(self)

	def Destroy(self):
		pass

	def __LoadWindow(self):
		self.LoadImage("d:/ymir work/ui/game/chat/color_bg.tga")

		self.bars = []
		y_start = 8
		for i in range(len(self.COLOR_LIST["colors"])):
			bar = ui.Bar()
			bar.SetParent(self)
			bar.SetSize(30, 16)
			bar.SetColor(self.COLOR_LIST["colors"][i])
			bar.SetPosition(6, y_start)
			bar.Hide()
			bar.OnMouseLeftButtonDown = lambda arg=i: self.OnMouseLeftButtonDown(arg)

			self.bars.append(bar)
			y_start += 21

		self.is_loaded = True

	def Open(self):
		if not self.is_loaded:
			self.__LoadWindow()

		self.Show()
		self.SetTop()

		for bar in self.bars:
			bar.Show()

	def Close(self):
		self.Hide()

	def OnMouseLeftButtonDown(self, key=-1):
		if key not in range(len(self.COLOR_LIST["colors"])):
			return


		self.selectedColor = self.COLOR_LIST["hex"][key]

		self.Close()

	def GetColor(self):
		return self.selectedColor
		
class QuestionDialogWithTimeLimit(QuestionDialog2):
	def __init__(self):
		ui.ScriptWindow.__init__(self)

		self.__CreateDialog()
		self.endTime = 0
		self.timeoverMsg = None
		self.isCancelOnTimeover = False

	def __del__(self):
		QuestionDialog2.__del__(self)

	def __CreateDialog(self):
		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, "uiscript/questiondialog2.py")

		self.board = self.GetChild("board")
		self.textLine1 = self.GetChild("message1")
		self.textLine2 = self.GetChild("message2")
		self.acceptButton = self.GetChild("accept")
		self.cancelButton = self.GetChild("cancel")

	def Open(self, msg, timeout):
		self.SetCenterPosition()
		self.SetTop()
		self.Show()

		self.SetText1(msg)
		self.endTime = app.GetTime() + timeout

	def OnUpdate(self):
		leftTime = max(0, self.endTime - app.GetTime())
		self.SetText2(localeInfo.UI_LEFT_TIME % (leftTime))
		if leftTime<0.5:
			if self.timeoverMsg:
				chat.AppendChat(chat.CHAT_TYPE_INFO, self.timeoverMsg)
			if self.isCancelOnTimeover:
				self.cancelButton.CallEvent()

	def SetTimeOverMsg(self, msg):
		self.timeoverMsg = msg

	def SetCancelOnTimeOver(self):
		self.isCancelOnTimeover = True

class BackgroundShadow(ui.ExpandedImageBox):
	def __init__(self, alpha = 0.15):
		ui.ExpandedImageBox.__init__(self)
		self.FadeOut()
		self.LoadImage("d:/ymir work/ui/game/backgroundshadow/shadow.png")
		self.SetAlpha(alpha)
		self.Hide()

	def __del__(self):
		ui.ExpandedImageBox.__del__(self)

	def FadeIn(self):
		self.SetTop()
		self.Show()

	def FadeOut(self):
		self.Hide()
if app.ENABLE_OFFLINE_SHOP:
	class ShopOfflinePopup(ui.BorderB):
		def __init__(self):
			ui.BorderB.__init__(self)
			
			self.isActiveSlide = False
			self.isActiveSlideOut = False
			self.endTime = 0
			self.wndWidth = 0
			self.__lastSlideTime = 0.0
			self.__slideAccumulator = 0.0

			self.wndIcon = ui.ExpandedImageBox()
			self.wndIcon.SetParent(self)
			self.wndIcon.LoadImage("icon/emoji/others/shopsearchyang.png")
			self.wndIcon.SetPosition(5, 10)
			self.wndIcon.Show()

			self.textInfo = ui.TextLine()
			self.textInfo.SetParent(self.wndIcon)
			self.textInfo.SetWindowHorizontalAlignCenter()
			self.textInfo.SetWindowVerticalAlignCenter()
			self.textInfo.SetHorizontalAlignCenter()
			self.textInfo.SetVerticalAlignCenter()

			self.listNotification = {}

		def AddNotification(self, dwItemID, itemName, itemPrice, dwItemCount):
			self.listNotification[dwItemID] = [itemName, itemPrice, dwItemCount]
			self.Close()

		def __del__(self):
			ui.BorderB.__del__(self)

		def SlideIn(self, dwItemID, itemName, itemPrice, dwItemCount):
			self.SetTop()
			self.Show()
			
			self.isActiveSlide = True
			self.endTime = app.GetGlobalTimeStamp() + 4
			self.__lastSlideTime = 0.0
			self.__slideAccumulator = 0.0

			self.textInfo.SetText("|cffFFD700" + str(itemName) + "|r " + localeInfo.SHOP_BUY_NOTIF_0 + "|cffFFD700"+str(itemPrice)+"|r " + localeInfo.SHOP_BUY_NOTIF_1)
			self.textInfo.SetPosition(160 + len(str(itemPrice)) + 5, 0)
			self.textInfo.Show()

			self.wndWidth = 323 + len(str(itemPrice)) * 2
			self.SetSize(self.wndWidth, 35)
			self.SetPosition(-self.wndWidth, wndMgr.GetScreenHeight() - 100 - 32*4)

		def Close(self):
			if self.isActiveSlide:
				return

			if len(self.listNotification) == 0:
				self.Hide()
			else:
				for itemf in self.listNotification:
					self.SlideIn(itemf, self.listNotification[itemf][0], self.listNotification[itemf][1], self.listNotification[itemf][2])
					del self.listNotification[itemf]
					break

		def Destroy(self):
			self.Hide()
			self.listNotification = {}

		def OnUpdate(self):
			if not self.isActiveSlide and not self.isActiveSlideOut:
				return

			# Slide szedl o 4 px na KLATKE, wiec po odblokowaniu limitu FPS popup
			# wjezdzal tyle razy szybciej, ile mamy klatek ponad 60 (przy 1000 FPS -
			# teleport). Robimy tyle 4-pikselowych krokow, ile "klatek 60 FPS" minelo.
			scale, self.__lastSlideTime = ui.GetFrameStepScale(self.__lastSlideTime)
			self.__slideAccumulator += scale

			steps = int(self.__slideAccumulator)
			if steps <= 0:
				return

			self.__slideAccumulator -= steps

			if self.isActiveSlide and self.isActiveSlide == True:
				x, y = self.GetLocalPosition()
				if x < 0:
					self.SetPosition(min(0, x + 4 * steps), y)

			if self.endTime - app.GetGlobalTimeStamp() <= 0 and self.isActiveSlideOut == False and self.isActiveSlide == True:
				self.isActiveSlide = False
				self.isActiveSlideOut = True

			if self.isActiveSlideOut and self.isActiveSlideOut == True:
				x, y = self.GetLocalPosition()
				if x > -(self.wndWidth):
					x -= 4 * steps
					self.SetPosition(x, y)

				if x <= -(self.wndWidth):
					self.isActiveSlideOut = False
					self.Close()

	class OfflineShopInputDialog(ui.ScriptWindow):
		PATH_ROOT = "offlineshop/lightwork/shopseller/"
		
		def __init__(self, ItemVnum, ItemCount, editItem=False):
			ui.ScriptWindow.__init__(self)
			self.moneyHeaderText = localeInfo.MONEY_INPUT_DIALOG_SELLPRICE
			self.__CreateDialog(ItemVnum,ItemCount, editItem)
			self.SetMaxLength(15)
			self.SetCenterPosition()

		def __del__(self):
			ui.ScriptWindow.__del__(self)

		def __CreateDialog(self, ItemVnum, ItemCount, editItem):

			if not ItemCount:
				ItemCount = 1

			self.avgPrice = 0

			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "uiscript/moneyinputdialog.py")

			getObject = self.GetChild
			self.board = self.GetChild("board")
			self.board.Hide()
			self.acceptButton = getObject("AcceptButton")
			self.cancelButton = getObject("CancelButton")
			self.inputValue = getObject("InputValue")
			self.inputValue.SetText("0")

			self.inputValue.OnIMEUpdate = ui.__mem_func__(self.__OnValueUpdate)
			self.inputValue.OnPressEscapeKey = ui.__mem_func__(self.OnPressEscapeKey)
			self.moneyText = getObject("MoneyValue")

			self.board = ui.ExpandedImageBox()
			self.board.SetParent(self)
			self.board.AddFlag("not_pick")
			self.board.LoadImage(self.PATH_ROOT + "bg.tga")
			self.board.Show()

			self.acceptButton = ui.MakeButton(self, 21.5, 386, False, "offlineshop/lightwork/shopbuilder/", "btn_big_default.png", "btn_big_hover.png", "btn_big_down.png")
			self.acceptButton.SetText(uiScriptLocale.ACCEPT)

			self.cancelButton = ui.MakeButton(self, 121.5, 386, False, "offlineshop/lightwork/shopbuilder/", "btn_big_default.png", "btn_big_hover.png", "btn_big_down.png")
			self.cancelButton.SetText(uiScriptLocale.KEYCHANGE_CANCLE)
			
			self.boardItem = ui.ExpandedImageBox()
			self.boardItem.SetParent(self)
			self.boardItem.SetPosition(0, 246)
			self.boardItem.AddFlag("not_pick")
			self.boardItem.LoadImage(self.PATH_ROOT + "bg_item.png")
			self.boardItem.SetWindowHorizontalAlignCenter()
			self.boardItem.Show()

			self.itemVnum = ItemVnum

			import item
			item.SelectItem(ItemVnum)
			self.ItemIcon = ui.ExpandedImageBox()
			self.ItemIcon.SetParent(self.boardItem)
			self.ItemIcon.SetPosition(0, 0)
			self.ItemIcon.LoadImage(item.GetIconImageFileName())
			self.ItemIcon.SetWindowHorizontalAlignCenter()
			self.ItemIcon.SetWindowVerticalAlignCenter()
			self.ItemIcon.Show()

			self.boardYang = ui.ExpandedImageBox()
			self.boardYang.SetParent(self)
			self.boardYang.SetPosition(25, 111)
			self.boardYang.LoadImage(self.PATH_ROOT + "price.dds")
			self.boardYang.Show()
			
			self.inputValue.SetParent(self.boardYang)
			self.inputValue.SetPosition(29, 8)
		
			self.wndNameItem = ui.MakeTextLineNew(self, 0, 225, item.GetItemName())
			self.wndNameItem.SetWindowHorizontalAlignCenter()
			self.wndNameItem.SetHorizontalAlignCenter()
			
			self.wndNameLine1 = ui.MakeTextLineNew(self, 0, 23, localeInfo.OFFLINESHOP_INPUT_INFO)
			self.wndNameLine1.SetWindowHorizontalAlignCenter()
			self.wndNameLine1.SetHorizontalAlignCenter()

			self.wndNameLine2 = ui.MakeTextLineNew(self, 0, 35, localeInfo.OFFLINESHOP_INPUT_INFO2)
			self.wndNameLine2.SetWindowHorizontalAlignCenter()
			self.wndNameLine2.SetHorizontalAlignCenter()

			self.averagePriceInfo = ui.MakeTextLineNew(self, 0, 58, localeInfo.OFFLINESHOP_AVERAGE_PRICE_INFO)
			self.averagePriceInfo.SetWindowHorizontalAlignCenter()
			self.averagePriceInfo.SetHorizontalAlignCenter()
			self.averagePrice = ui.MakeTextLineNew(self, 0, 73, localeInfo.OFFLINESHOP_AVERAGE_PRICE_NO_INFO)
			self.averagePrice.SetWindowHorizontalAlignCenter()
			self.averagePrice.SetHorizontalAlignCenter()

			self.averagePriceBulk = ui.MakeTextLineNew(self, 0, 88, localeInfo.OFFLINESHOP_AVERAGE_PRICE_NO_INFO)
			self.averagePriceBulk.SetWindowHorizontalAlignCenter()
			self.averagePriceBulk.SetHorizontalAlignCenter()

			self.ItemCount = int(ItemCount)

			self.moneyText.SetParent(self)
			self.moneyText.SetPosition(0, 361)
			self.moneyText.SetWindowHorizontalAlignCenter()
			self.moneyText.SetHorizontalAlignCenter()

			self.sellWithAveragePrice = ui.ExpandedImageBox()
			self.sellWithAveragePrice.SetParent(self)
			self.sellWithAveragePrice.SetPosition(23, 141)
			self.sellWithAveragePrice.LoadImage("d:/ymir work/ui/game/biolog_system/select_button01.png")
			self.sellWithAveragePrice.IsChecked = False
			self.sellWithAveragePrice.OnMouseLeftButtonDown = ui.__mem_func__(self.SellWithAveragePrice)
			self.sellWithAveragePrice.Show()

			self.avgPriceSellText = ui.TextLine()
			self.avgPriceSellText.SetParent(self.sellWithAveragePrice)
			self.avgPriceSellText.SetPosition(25, 2)
			self.avgPriceSellText.SetText(localeInfo.OFFLINESHOP_SELL_WITH_AVG_PRICE)
			self.avgPriceSellText.Show()

			self.sellWithAveragePrice2 = ui.ExpandedImageBox()
			self.sellWithAveragePrice2.SetParent(self)
			self.sellWithAveragePrice2.SetPosition(23, 161)
			self.sellWithAveragePrice2.LoadImage("d:/ymir work/ui/game/biolog_system/select_button01.png")
			self.sellWithAveragePrice2.IsChecked = False
			self.sellWithAveragePrice2.OnMouseLeftButtonDown = ui.__mem_func__(self.SellWithAveragePrice2)
			self.sellWithAveragePrice2.Show()

			self.avgPriceSellText2 = ui.TextLine()
			self.avgPriceSellText2.SetParent(self.sellWithAveragePrice2)
			self.avgPriceSellText2.SetPosition(25, 2)
			self.avgPriceSellText2.SetText(localeInfo.OFFLINESHOP_SELL_WITH_AVG_PRICE2)
			self.avgPriceSellText2.Show()

			self.sellWithAveragePrice3 = ui.ExpandedImageBox()
			self.sellWithAveragePrice3.SetParent(self)
			self.sellWithAveragePrice3.SetPosition(23, 181)
			self.sellWithAveragePrice3.LoadImage("d:/ymir work/ui/game/biolog_system/select_button01.png")
			self.sellWithAveragePrice3.IsChecked = False
			self.sellWithAveragePrice3.OnMouseLeftButtonDown = ui.__mem_func__(self.SellWithAveragePrice3)
			self.sellWithAveragePrice3.Show()

			self.avgPriceSellText3 = ui.TextLine()
			self.avgPriceSellText3.SetParent(self.sellWithAveragePrice3)
			self.avgPriceSellText3.SetPosition(25, 2)
			self.avgPriceSellText3.SetText(localeInfo.OFFLINESHOP_SELL_WITH_AVG_PRICE3)
			self.avgPriceSellText3.Show()

			self.editItem = editItem
			if self.editItem:

				self.changeAllPrice = ui.ExpandedImageBox()
				self.changeAllPrice.SetParent(self)
				self.changeAllPrice.SetPosition(23, 201)
				self.changeAllPrice.LoadImage("d:/ymir work/ui/game/biolog_system/select_button01.png")
				self.changeAllPrice.IsChecked = False
				self.changeAllPrice.OnMouseLeftButtonDown = ui.__mem_func__(self.ChangeAllPrice)
				self.changeAllPrice.Show()

				self.changeAllPriceText = ui.TextLine()
				self.changeAllPriceText.SetParent(self.changeAllPrice)
				self.changeAllPriceText.SetPosition(25, 2)
				self.changeAllPriceText.SetText(localeInfo.OFFLINESHOP_CHANGE_ALL_PRICE)
				self.changeAllPriceText.Show()

			self.interface = constInfo.GetInterfaceInstance()

			self.SetSize(self.board.GetWidth(), self.board.GetHeight())
		def SellWithAveragePrice(self):

			if self.sellWithAveragePrice2.IsChecked:
				self.sellWithAveragePrice2.IsChecked = False
				self.sellWithAveragePrice2.LoadImage("d:/ymir work/ui/game/biolog_system/select_button01.png")

			elif self.sellWithAveragePrice3.IsChecked:
				self.sellWithAveragePrice3.IsChecked = False
				self.sellWithAveragePrice3.LoadImage("d:/ymir work/ui/game/biolog_system/select_button01.png")


			if self.sellWithAveragePrice.IsChecked:
				self.sellWithAveragePrice.IsChecked = False
				self.sellWithAveragePrice.LoadImage("d:/ymir work/ui/game/biolog_system/select_button01.png")
			else:
				self.sellWithAveragePrice.IsChecked = True
				self.sellWithAveragePrice.LoadImage("d:/ymir work/ui/game/biolog_system/select_button02.png")

		def SellWithAveragePrice2(self):

			if self.sellWithAveragePrice.IsChecked:
				self.sellWithAveragePrice.IsChecked = False
				self.sellWithAveragePrice.LoadImage("d:/ymir work/ui/game/biolog_system/select_button01.png")

			elif self.sellWithAveragePrice3.IsChecked:
				self.sellWithAveragePrice3.IsChecked = False
				self.sellWithAveragePrice3.LoadImage("d:/ymir work/ui/game/biolog_system/select_button01.png")


			if self.sellWithAveragePrice2.IsChecked:
				self.sellWithAveragePrice2.IsChecked = False
				self.sellWithAveragePrice2.LoadImage("d:/ymir work/ui/game/biolog_system/select_button01.png")
			else:
				self.sellWithAveragePrice2.IsChecked = True
				self.sellWithAveragePrice2.LoadImage("d:/ymir work/ui/game/biolog_system/select_button02.png")

		def SellWithAveragePrice3(self):

			if self.sellWithAveragePrice.IsChecked:
				self.sellWithAveragePrice.IsChecked = False
				self.sellWithAveragePrice.LoadImage("d:/ymir work/ui/game/biolog_system/select_button01.png")

			elif self.sellWithAveragePrice2.IsChecked:
				self.sellWithAveragePrice2.IsChecked = False
				self.sellWithAveragePrice2.LoadImage("d:/ymir work/ui/game/biolog_system/select_button01.png")


			if self.sellWithAveragePrice3.IsChecked:
				self.sellWithAveragePrice3.IsChecked = False
				self.sellWithAveragePrice3.LoadImage("d:/ymir work/ui/game/biolog_system/select_button01.png")
			else:
				self.sellWithAveragePrice3.IsChecked = True
				self.sellWithAveragePrice3.LoadImage("d:/ymir work/ui/game/biolog_system/select_button02.png")

		def ChangeAllPrice(self):
			if self.changeAllPrice.IsChecked:
				self.changeAllPrice.IsChecked = False
				self.changeAllPrice.LoadImage("d:/ymir work/ui/game/biolog_system/select_button01.png")
			else:
				self.changeAllPrice.IsChecked = True
				self.changeAllPrice.LoadImage("d:/ymir work/ui/game/biolog_system/select_button02.png")

		def OnUpdate(self):
			avgPrice = self.avgPrice * self.ItemCount

			if self.sellWithAveragePrice.IsChecked:
				self.inputValue.SetText(str(avgPrice))
				self.moneyText.SetText(self.moneyHeaderText + localeInfo.NumberToMoneyString(avgPrice))
				self.inputValue.OnKillFocus()
			elif self.sellWithAveragePrice2.IsChecked:
				self.inputValue.SetText(str(int((avgPrice)*110)//100))
				self.moneyText.SetText(self.moneyHeaderText + localeInfo.NumberToMoneyString(str(int((avgPrice)*110)//100)))
				self.inputValue.OnKillFocus()
			elif self.sellWithAveragePrice3.IsChecked:
				self.inputValue.SetText(str(int((avgPrice)*90)//100))
				self.moneyText.SetText(self.moneyHeaderText + localeInfo.NumberToMoneyString(str(int((avgPrice)*90)//100)))
				self.inputValue.OnKillFocus()
			else:
				self.inputValue.OnSetFocus()


		def OnPressEscapeKey(self):
			self.Close()
			return True

		def Open(self):
			self.inputValue.SetText("")
			self.inputValue.SetFocus()
			self.__OnValueUpdate()
			self.SetCenterPosition()
			self.SetTop()
			self.Show()

		def Close(self):
			self.ClearDictionary()
			self.board = None
			self.acceptButton = None
			self.cancelButton = None
			self.inputValue = None
			self.Hide()

		def SetTitle(self, name):
			pass

		def SetFocus(self):
			self.inputValue.SetFocus()

		def SetMaxLength(self, length):
			length = min(15, length)
			self.inputValue.SetMax(length)

		def SetMoneyHeaderText(self, text):
			self.moneyHeaderText = text

		def SetAcceptEvent(self, event):
			self.acceptButton.SetEvent(event)
			self.inputValue.OnIMEReturn = event

		def SetCancelEvent(self, event):
			self.cancelButton.SetEvent(event)
			self.inputValue.OnPressEscapeKey = event

		def SetValue(self, value):
			value=str(value)
			self.inputValue.SetText(value)
			self.__OnValueUpdate()
			ime.SetCursorPosition(len(value))

		def GetText(self):
			return self.inputValue.GetText()

		def __OnValueUpdate(self):
			ui.EditLine.OnIMEUpdate(self.inputValue)

			money = 0
			text = self.inputValue.GetText()
			if text and text.isdigit():
				try:
					money = int(text)
				except ValueError:
					money = 199999999

			if text:
				money = min(constInfo.ConvertMoneyText(text), 999999999999999)

			self.moneyText.SetText(self.moneyHeaderText + localeInfo.NumberToMoneyString(money))
			self.inputValue.OnSetFocus()

		def AveragePriceUpdate(self, amount):
			self.avgPrice = int(amount)
			self.averagePrice.SetText(localeInfo.OFFLINESHOP_AVERAGE_PRICE.format(localeInfo.NumberToMoneyString(amount)))
			self.averagePriceBulk.SetText(localeInfo.OFFLINESHOP_AVERAGE_PRICE2.format(localeInfo.NumberToMoneyString(amount * self.ItemCount)))

		def ArrangeItemPrices(self):
			money = 0
			text = self.inputValue.GetText()
			if text and text.isdigit():
				try:
					money = int(text)
				except ValueError:
					money = 199999999

			if text:
				money = min(constInfo.ConvertMoneyText(text), 999999999999999)

			if self.editItem:
				if self.changeAllPrice.IsChecked:
					self.interface.wndShopOffline.ReArrangeItemPrices(self.itemVnum, money//self.ItemCount)

		def GetEditAllState(self):
			self.interface.wndShopOffline.SetEditAllState(self.changeAllPrice.IsChecked if self.editItem else False)
			
if app.ENABLE_PREMIUM_PRIVATE_SHOP_OFFICIAL:
	class PrivateShopPriceInputDialog(ui.ScriptWindow):

		def __init__(self):
			ui.ScriptWindow.__init__(self)
			self.toolTip = None
			self.cancelEvent = None
			self.itemVnum = -1
			self.itemCount = 1
			self.inputMarketPrice = False
			self.marketGoldValue = 0
			self.marketChequeValue = 0
			self.__CreateDialog()

		def __del__(self):
			ui.ScriptWindow.__del__(self)

		def __CreateDialog(self):

			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "uiscript/privateshoppriceinputdialog.py")

			self.board = self.GetChild("board")
			self.acceptButton = self.GetChild("AcceptButton")
			self.cancelButton = self.GetChild("CancelButton")
			self.inputValue = self.GetChild("InputValue")
			self.inputMoneyText = self.GetChild("InputMoneyText")
			self.marketMoneyText = self.GetChild("MarketMoneyValue")
			self.priceHintButton = self.GetChild("PriceHintButton")
			self.marketPriceButton = self.GetChild("MarketPriceButton")

			self.inputValue.OnIMEUpdate = ui.__mem_func__(self.__OnValueUpdate)

			self.priceHintButton.SetShowToolTipEvent(ui.__mem_func__(self.__OnOverInButton), "PRICE_HINT")
			self.priceHintButton.SetHideToolTipEvent(ui.__mem_func__(self.__OnOverOutButton))

			self.marketPriceButton.SetEvent(ui.__mem_func__(self.__OnClickMarketPriceButton))
			self.marketPriceButton.SetShowToolTipEvent(ui.__mem_func__(self.__OnOverInButton), "AUTO_MARKET_PRICE_INPUT")
			self.marketPriceButton.SetHideToolTipEvent(ui.__mem_func__(self.__OnOverOutButton))
			
			if app.ENABLE_CHEQUE_SYSTEM:
				self.inputChequeText = self.GetChild("InputChequeText")
				self.marketChequeText = self.GetChild("MarketChequeValue")
				self.inputChequeValue = self.GetChild("InputValue_Cheque")

				self.inputChequeValue.OnIMEUpdate = ui.__mem_func__(self.__OnValueUpdate)
				self.inputChequeValue.OnMouseLeftButtonDown = ui.__mem_func__(self.__ClickChequeEditLine)
				self.inputChequeValue.SetTabEvent(self.inputValue.SetFocus)
				self.inputValue.OnMouseLeftButtonDown = ui.__mem_func__(self.__ClickValueEditLine)
				self.inputValue.SetTabEvent(self.inputChequeValue.SetFocus)

			self.toolTip = uiToolTip.ToolTip()
			self.toolTip.HideToolTip()

		def Open(self):
			self.inputChequeText.SetText(localeInfo.NumberToMoneyStringNoUnit(int(0)) + " " + localeInfo.CHEQUE_SYSTEM_UNIT_WON)
			self.inputValue.SetFocus()
			self.__OnValueUpdate()
			self.SetCenterPosition()
			self.SetTop()
			self.Show()

		def Clear(self):
			self.itemVnum = -1
			self.itemCount = 1
			self.marketGoldValue = 0
			self.marketChequeValue = 0

			self.inputValue.SetText("")
			if app.ENABLE_CHEQUE_SYSTEM:
				self.inputChequeValue.SetText("")

		def Close(self):
			self.Clear()
			self.cancelEvent()
			self.Hide()

		def SetItemVnum(self, vnum):
			self.itemVnum = vnum

		def GetItemVnum(self):
			return self.itemVnum
			
		def SetItemCount(self, count):
			self.itemCount = count

		def GetItemCount(self):
			return self.itemCount

		def SetTitle(self, name):
			self.board.SetTitleName(name)

		def SetFocus(self):
			self.inputValue.SetFocus()

		def KillFocus(self):
			if self.inputValue.IsFocus():
				self.inputValue.KillFocus()
			
			if app.ENABLE_CHEQUE_SYSTEM and self.inputChequeValue.IsFocus():
				self.inputChequeValue.KillFocus()

		def SetAcceptEvent(self, event):
			self.acceptButton.SetEvent(event)
			self.inputValue.SetReturnEvent(event)

			if app.ENABLE_CHEQUE_SYSTEM:
				self.inputChequeValue.SetReturnEvent(event)

		def SetCancelEvent(self, event):
			self.cancelEvent = event

			self.board.SetCloseEvent(self.Close)
			self.cancelButton.SetEvent(self.Close)
			self.inputValue.SetEscapeEvent(self.Close)

			if app.ENABLE_CHEQUE_SYSTEM:
				self.inputChequeValue.SetEscapeEvent(self.Close)

		def SetValue(self, value):
			value=str(value)
			self.inputValue.SetText(value)
			self.__OnValueUpdate()
			ime.SetCursorPosition(len(value)+1)		

		def GetText(self):
			if len(self.inputValue.GetText()) <= 0:
				return "0"

			return self.inputValue.GetText()
			
		def SetMarketValue(self, gold, cheque):
			self.marketGoldValue = gold * self.itemCount
			self.marketChequeValue = cheque * self.itemCount

			if gold:
				self.marketMoneyText.SetText(localeInfo.NumberToMoneyString(gold))
				
				if self.inputMarketPrice:
					self.InputMarketPrice()
			else:
				self.marketMoneyText.SetText(localeInfo.PREMIUM_PRIVATE_SHOP_MARKET_PRICE_NOT_AVAILABLE)
				
			if app.ENABLE_CHEQUE_SYSTEM:
				if not gold and not cheque:
					self.marketChequeText.Hide()
				else:
					self.marketChequeText.SetText(localeInfo.NumberToMoneyStringNoUnit(cheque) + " " + localeInfo.CHEQUE_SYSTEM_UNIT_WON)
					self.marketChequeText.Show()

					if self.inputMarketPrice:
						self.InputMarketPrice()

		if app.ENABLE_CHEQUE_SYSTEM:
			def SetCheque(self, cheque):
				cheque=str(cheque)
				self.inputChequeValue.SetText(cheque)
				self.inputChequeText.SetText(localeInfo.NumberToMoneyStringNoUnit(int(cheque)) + " " + localeInfo.CHEQUE_SYSTEM_UNIT_WON)
				self.__OnValueUpdate()
				ime.SetCursorPosition(len(cheque)+1)
			
			def __ClickChequeEditLine(self) :
				self.inputChequeValue.SetFocus()
				if len(self.inputChequeValue.GetText()) <= 0:
					self.inputChequeValue.SetText("")

			def __ClickValueEditLine(self) :
				self.inputValue.SetFocus()
				if len(self.inputValue.GetText()) <= 0:
					self.inputValue.SetText("")
							
			def GetCheque(self):
				if len(self.inputChequeValue.GetText()) <= 0:
					return "0"

				return self.inputChequeValue.GetText()
				
			def __OnValueUpdate(self):
				if self.inputValue.IsFocus() :
					ui.EditLine.OnIMEUpdate(self.inputValue)

					money = self.inputValue.GetText()
					money = money.upper()
					if len(money) <= 0:
						money = "0"
					else:
						k_pos = money.find('K')
						if k_pos >= 0:
							money = re.sub(r'[^0-9K]', '', money)
							money = money[:k_pos] + '000' * money.count('K')
						else:
							money = re.sub(r'\D', '', money)

					self.inputMoneyText.SetText(localeInfo.NumberToMoneyString(int(money)))

				elif self.inputChequeValue.IsFocus() :
					ui.EditLine.OnIMEUpdate(self.inputChequeValue)

					cheque = self.inputChequeValue.GetText()
					if len(cheque) <= 0:
						cheque = "0"

					self.inputChequeText.SetText(localeInfo.NumberToMoneyStringNoUnit(int(cheque)) + " " + localeInfo.CHEQUE_SYSTEM_UNIT_WON)
				else:
					pass
	
		else:
			def __OnValueUpdate(self):
				ui.EditLine.OnIMEUpdate(self.inputValue)
				
				money = self.inputValue.GetText()
				if len(money) <= 0:
					money = "0"
				else:
					k_pos = money.find('K')
					if k_pos >= 0:
						money = money[:k_pos] + '000' * money.count('K')

				self.inputMoneyText.SetText(localeInfo.NumberToMoneyString(int(money)))

		def __OnClickMarketPriceButton(self):
			if self.inputMarketPrice:
				self.inputMarketPrice = False

				self.marketPriceButton.SetUpVisual("d:/ymir work/ui/game/premium_private_shop/mini_empty_button_default.sub")
				self.marketPriceButton.SetOverVisual("d:/ymir work/ui/game/premium_private_shop/mini_empty_button_over.sub")
				self.marketPriceButton.SetDownVisual("d:/ymir work/ui/game/premium_private_shop/mini_empty_button_down.sub")
			else:
				self.inputMarketPrice = True

				self.marketPriceButton.SetUpVisual("d:/ymir work/ui/game/premium_private_shop/mini_accept_button_default.sub")
				self.marketPriceButton.SetOverVisual("d:/ymir work/ui/game/premium_private_shop/mini_accept_button_over.sub")
				self.marketPriceButton.SetDownVisual("d:/ymir work/ui/game/premium_private_shop/mini_accept_button_down.sub")

				self.InputMarketPrice()

		def InputMarketPrice(self):
			if self.marketGoldValue > 0:
				self.SetValue(str(self.marketGoldValue))

			if app.ENABLE_CHEQUE_SYSTEM:
				if self.marketChequeValue > 0:
					self.SetCheque(str(self.marketChequeValue))

		def __OnOverInButton(self, button):
			self.toolTip.ClearToolTip()

			if button == "PRICE_HINT":
				self.toolTip.SetThinBoardSize(len(localeInfo.PREMIUM_PRIVATE_SHOP_MARKET_PRICE_HINT_MSG) * 4 + 50, 10)
				self.toolTip.AppendTextLine(localeInfo.PREMIUM_PRIVATE_SHOP_MARKET_PRICE_HINT_MSG, self.toolTip.SPECIAL_TITLE_COLOR)

			elif button == "AUTO_MARKET_PRICE_INPUT":
				self.toolTip.SetThinBoardSize(len(localeInfo.PREMIUM_PRIVATE_SHOP_AUTO_MARKET_PRICE_INPUT_TOOLTIP) * 4 + 50, 10)
				self.toolTip.AppendTextLine(localeInfo.PREMIUM_PRIVATE_SHOP_AUTO_MARKET_PRICE_INPUT_TOOLTIP, self.toolTip.SPECIAL_TITLE_COLOR)

			self.toolTip.ShowToolTip()
				
			
		def __OnOverOutButton(self):
			if 0 != self.toolTip:
				self.toolTip.HideToolTip()

		def OnPressEscapeKey(self):
			self.Close()
			return True

