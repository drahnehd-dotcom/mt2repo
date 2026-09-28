import wndMgr
import ui
import ime
import localeInfo
import constInfo
import app

class PickMoneyDialog(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)

		self.unitValue = 1
		self.maxValue = 0
		self.eventAccept = 0
		if app.ENABLE_CHEQUE_SYSTEM:
			self.chequeMaxValue = 0

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def LoadDialog(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "UIScript/PickMoneyDialog.py")
		except:
			import exception
			exception.Abort("MoneyDialog.LoadDialog.LoadScript")

		try:
			self.board = self.GetChild("board")
			self.pickValueEditLine = self.GetChild("money_value")
			self.acceptButton = self.GetChild("accept_button")
			self.cancelButton = self.GetChild("cancel_button")
			if app.ENABLE_CHEQUE_SYSTEM:
				self.pickChequeValueEditLine = self.GetChild("cheque_value")
				self.pickChequeValueEditLine.OnMouseLeftButtonDown = ui.__mem_func__(self.__ClickChequeEditLine)
				self.pickValueEditLine.OnMouseLeftButtonDown = ui.__mem_func__(self.__ClickValueEditLine)
		except:
			import exception
			exception.Abort("MoneyDialog.LoadDialog.BindObject")

		self.pickValueEditLine.SetReturnEvent(ui.__mem_func__(self.OnAccept))
		self.pickValueEditLine.SetEscapeEvent(ui.__mem_func__(self.Close))
		self.acceptButton.SetEvent(ui.__mem_func__(self.OnAccept))
		self.cancelButton.SetEvent(ui.__mem_func__(self.Close))
		self.board.SetCloseEvent(ui.__mem_func__(self.Close))

	def Destroy(self):
		self.ClearDictionary()
		self.eventAccept = 0
		self.pickValueEditLine = 0
		if app.ENABLE_CHEQUE_SYSTEM:
			self.pickChequeValueEditLine = 0
		self.acceptButton = 0
		self.cancelButton = 0
		self.board = None

	def SetTitleName(self, text):
		self.board.SetTitleName(text)

	def SetAcceptEvent(self, event):
		self.eventAccept = event

	def SetMax(self, max):
		self.pickValueEditLine.SetMax(max)

	if app.ENABLE_CHEQUE_SYSTEM:
		def SetMaxCheque(self, max):
			self.pickChequeValueEditLine.SetMax(max)

		def SetFocus(self, focus_idx) :
			if focus_idx == 1:
				self.pickChequeValueEditLine.SetText(str(0))
				self.pickChequeValueEditLine.SetFocus()
				self.pickValueEditLine.SetText(str(0))
			else :
				return
		
		def __ClickChequeEditLine(self) :
			self.pickChequeValueEditLine.SetFocus()
			if len(self.pickValueEditLine.GetText()) <= 0:
				self.pickValueEditLine.SetText(str(0))

		def __ClickValueEditLine(self) :
			self.pickValueEditLine.SetFocus()
			if len(self.pickChequeValueEditLine.GetText()) <= 0:
				self.pickChequeValueEditLine.SetText(str(0))

		def Open(self, maxValue, chequeMaxValue):

			width = self.GetWidth()
			(mouseX, mouseY) = wndMgr.GetMousePosition()

			if mouseX + width // 2 > wndMgr.GetScreenWidth():
				xPos = wndMgr.GetScreenWidth() - width
			elif mouseX - width // 2 < 0:
				xPos = 0
			else:
				xPos = mouseX - width // 2

			self.SetPosition(xPos, mouseY - self.GetHeight() - 20)
			
			self.pickChequeValueEditLine.SetText(str(0))
			self.pickValueEditLine.SetText(str(0))
			self.pickValueEditLine.SetFocus()

			ime.SetCursorPosition(1)

			self.chequeMaxValue = chequeMaxValue
			self.maxValue = maxValue
			self.Show()
			self.SetTop()
	else:
		def Open(self, maxValue, unitValue=1):

			width = self.GetWidth()
			(mouseX, mouseY) = wndMgr.GetMousePosition()

			if mouseX + width // 2 > wndMgr.GetScreenWidth():
				xPos = wndMgr.GetScreenWidth() - width
			elif mouseX - width // 2 < 0:
				xPos = 0
			else:
				xPos = mouseX - width // 2

			self.SetPosition(xPos, mouseY - self.GetHeight() - 20)

			self.pickValueEditLine.SetText(str(unitValue))
			self.pickValueEditLine.SetFocus()

			ime.SetCursorPosition(1)

			self.unitValue = unitValue
			self.maxValue = maxValue
			self.Show()
			self.SetTop()

	def Close(self):
		self.pickValueEditLine.KillFocus()
		if app.ENABLE_CHEQUE_SYSTEM:
			self.pickChequeValueEditLine.KillFocus()
		self.Hide()

	if app.ENABLE_CHEQUE_SYSTEM:
		def OnAccept(self):
			cheque_text	= self.pickChequeValueEditLine.GetText()
			money_text	= self.pickValueEditLine.GetText()

			if money_text or cheque_text:
				moneyValue = min(constInfo.ConvertMoneyText(money_text), self.maxValue)
				chequeValue = min(constInfo.ConvertChequeText(cheque_text), self.chequeMaxValue)
				if moneyValue or cheque_text:
					if self.eventAccept:
						self.eventAccept(moneyValue, chequeValue)

			elif money_text and cheque_text:
				moneyValue = min(constInfo.ConvertMoneyText(money_text), self.maxValue)
				chequeValue = min(constInfo.ConvertChequeText(cheque_text), self.chequeMaxValue)
				if moneyValue and cheque_text:
					if self.eventAccept:
						self.eventAccept(moneyValue, chequeValue)

			if len(cheque_text) > 0 and cheque_text.isdigit() \
				 and len(money_text) > 0 and money_text.isdigit():
				
				cheque = int(cheque_text)
				cheque = min(cheque, self.chequeMaxValue)
				money = int(money_text)
				money = min(money, self.maxValue)

				if cheque > 0 or money > 0 :
					if self.eventAccept:
						self.eventAccept(money, cheque)
			self.Close()
	else :
		def OnAccept(self):

			text = self.pickValueEditLine.GetText()

			if text:
				moneyValue = min(constInfo.ConvertMoneyText(text), self.maxValue)
				if moneyValue:
					if self.eventAccept:
						self.eventAccept(moneyValue)

			if len(text) > 0 and text.isdigit():

				money = int(text)
				money = min(money, self.maxValue)

				if money > 0:
					if self.eventAccept:
						self.eventAccept(money)

			self.Close()
