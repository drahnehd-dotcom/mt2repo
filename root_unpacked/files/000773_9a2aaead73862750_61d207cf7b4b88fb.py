# -*- coding: utf-8 -*-
# author: dracaryS (adaptacja py3 / Kowal)

# static
import ui, dbg, mouseModule, constInfo, localeInfo

# dynamic
import item, player, miniMap, chat, net

RANGE_CIRCLE = 60.0

IMG_DIR = "auto_hunt/"

# === KONFIGURACJA: vnumy 3 itemow auto-uzywanych przez bota ===
# PODSTAW TU SWOJE VNUMY. Te same vnumy MUSZA byc w PythonPlayer.cpp (__GetAutoHuntItemData).
# Slot 0/1/2 odpowiada kolejnym ikonom w oknie.
AUTO_HUNT_ITEM_VNUMS = {
	0 : 70038,
}

class Window(ui.BoardWithTitleBar):
	def __init__(self):
		ui.BoardWithTitleBar.__init__(self)
		self.__children = {}
		self.__LoadWindow()
	def Destroy(self):
		if len(self.__children) != 0:
			if self.IsActive():
				if self.__children["newOptions"]["auto_login"] == 1:
					constInfo.autoHuntAutoLoginDict["status"] = 1
					constInfo.autoHuntAutoLoginDict["leftTime"] = 0
					constInfo.autoHuntAutoLoginDict["skillDict"] = self.__children["skillDict"] if "skillDict" in self.__children else {}
					constInfo.autoHuntAutoLoginDict["newOptions"] = self.__children["newOptions"]
					slotItemDict = self.__children["slotItemDict"] if "slotItemDict" in self.__children else {}
					for key, itemIdx in slotItemDict.items():
						constInfo.autoHuntAutoLoginDict["slotStatus"][key] = self.__children["slotStatus" + str(key)] if ("slotStatus" + str(key)) in self.__children else False

		self.__children = {}
	def __LoadWindow(self):
		self.Destroy()
		self.AddFlag("animate")
		self.AddFlag("float")
		self.AddFlag("movable")
		self.SetTitleName(localeInfo.AUTO_HUNT_TITLE)
		self.SetCloseEvent(ui.__mem_func__(self.Close))

		bg = CreateWindow(ui.ImageBox(), self, (8, 29), IMG_DIR+"bg.tga")
		bg.AddFlag("attach")
		self.__children["bg"] = bg

		slotItemDict = dict(AUTO_HUNT_ITEM_VNUMS)

		for key, itemIdx in slotItemDict.items():
			item.SelectItem(itemIdx)
			itemImg = CreateWindow(ui.ImageBox(), bg, (20 + (key * 50), 99), item.GetIconImageFileName())
			itemImg.SetEvent(ui.__mem_func__(self.__OverInItem), "mouse_over_in", itemIdx)
			itemImg.SAFE_SetStringEvent("MOUSE_OVER_OUT", self.__OverOut)
			itemImg.SetEvent(ui.__mem_func__(self.__ClickStatus), "mouse_click", key)
			self.__children["itemImg"+str(key)] = itemImg

			status = CreateWindow(ui.ImageBox(), itemImg, (itemImg.GetWidth() - 12, itemImg.GetHeight() - 11), IMG_DIR+"check_0.tga")
			status.SetEvent(ui.__mem_func__(self.__ClickStatus), "mouse_click", key)
			self.__children["status"+str(key)] = status
		self.__children["slotItemDict"] = slotItemDict

		slot = CreateWindow(ui.SlotWindow(), bg, (10, 31), "", "", (205, 32))
		slot.SetSelectEmptySlotEvent(ui.__mem_func__(self.SelectSlot))
		slot.SetSelectItemSlotEvent(ui.__mem_func__(self.__ClickSkillSlot))
		slot.SetUnselectItemSlotEvent(ui.__mem_func__(self.__ClickSkillSlot))
		slot.SetUseSlotEvent(ui.__mem_func__(self.__ClickSkillSlot))
		for j in range(6):
			slot.AppendSlot(j, (j * 35), 0, 32, 32)
		slot.SetOverInItemEvent(ui.__mem_func__(self.__OverInSkill))
		slot.SetOverOutItemEvent(ui.__mem_func__(self.__OverOut))
		self.__children["slot"] = slot

		self.__children["text0"] = CreateWindow(ui.TextLine(), bg, (bg.GetWidth() // 2, 9), localeInfo.AUTO_HUNT_SKILLS, "horizontal:center")

		resetBtn = CreateWindow(ui.Button(), bg, (205, 6))
		resetBtn.SetUpVisual(IMG_DIR+"reset_0.tga")
		resetBtn.SetOverVisual(IMG_DIR+"reset_1.tga")
		resetBtn.SetDownVisual(IMG_DIR+"reset_2.tga")
		resetBtn.SetEvent(ui.__mem_func__(self.__ResetBtn))
		resetBtn.SetToolTipText(localeInfo.AUTO_HUNT_RESET)
		self.__children["resetBtn"] = resetBtn

		optionBtn = CreateWindow(ui.ToggleButton(), bg, (0, 151), "", "horizontal:center")
		optionBtn.SetUpVisual("d:/ymir work/ui/public/large_button_01.sub")
		optionBtn.SetOverVisual("d:/ymir work/ui/public/large_button_02.sub")
		optionBtn.SetDownVisual("d:/ymir work/ui/public/large_button_03.sub")
		optionBtn.SetToggleUpEvent(ui.__mem_func__(self.__OptionBtn))
		optionBtn.SetToggleDownEvent(ui.__mem_func__(self.__OptionBtn))
		optionBtn.SetText(localeInfo.AUTO_HUNT_OPTION)
		self.__children["optionBtn"] = optionBtn

		startBtn = CreateWindow(ui.RadioButton(), bg, (-55, 178), "", "horizontal:center")
		startBtn.SetUpVisual("d:/ymir work/ui/public/large_button_01.sub")
		startBtn.SetOverVisual("d:/ymir work/ui/public/large_button_02.sub")
		startBtn.SetDownVisual("d:/ymir work/ui/public/large_button_03.sub")
		startBtn.SetEvent(ui.__mem_func__(self.__StartBtn))
		startBtn.SetText(localeInfo.AUTO_HUNT_START)
		self.__children["startBtn"] = startBtn

		stopBtn = CreateWindow(ui.RadioButton(), bg, (55, 178), "", "horizontal:center")
		stopBtn.SetUpVisual("d:/ymir work/ui/public/large_button_01.sub")
		stopBtn.SetOverVisual("d:/ymir work/ui/public/large_button_02.sub")
		stopBtn.SetDownVisual("d:/ymir work/ui/public/large_button_03.sub")
		stopBtn.SetEvent(ui.__mem_func__(self.__StopBtn))
		stopBtn.SetText(localeInfo.AUTO_HUNT_STOP)
		self.__children["stopBtn"] = stopBtn

		self.SetSize(8 + bg.GetWidth() + 8, 29 + bg.GetHeight() + 9)

		self.__children["rangeText"] = CreateWindow(ui.TextLine(), self, (100, self.GetHeight()-7), localeInfo.AUTO_HUNT_RANGE)

		sliderBar = CreateWindow(ui.SliderBar(), self, (30, self.GetHeight() + 15))
		sliderBar.SetEvent(ui.__mem_func__(self.__OnChangeRange))
		sliderBar.Hide()
		self.__children["sliderBar"] = sliderBar

		self.__children["mobFarmCheckBox"] = CreateWindow(ui.ImageBox(), self, (30, self.GetHeight() + 15 + 18), IMG_DIR+"unselected.tga")
		self.__children["mobFarmCheckBox"].SetEvent(ui.__mem_func__(self.__ClickOption), "mouse_click", "mob")
		self.__children["mobFarmText"] = CreateWindow(ui.TextLine(), self, (30 + 15, self.GetHeight() + 15 + 20), localeInfo.AUTO_HUNT_MOB_FARM)

		self.__children["stoneFarmCheckBox"] = CreateWindow(ui.ImageBox(), self, (30 + 100, self.GetHeight() + 15 + 18), IMG_DIR+"unselected.tga")
		self.__children["stoneFarmCheckBox"].SetEvent(ui.__mem_func__(self.__ClickOption), "mouse_click", "stone")
		self.__children["stoneFarmText"] = CreateWindow(ui.TextLine(), self, (30 + 100 + 15, self.GetHeight() + 15 + 20), localeInfo.AUTO_HUNT_STONE_FARM)

		self.__children["autoLoginCheckBox"] = CreateWindow(ui.ImageBox(), self, (30, self.GetHeight() + 15 + 18 + 22), IMG_DIR+"unselected.tga")
		self.__children["autoLoginCheckBox"].SetEvent(ui.__mem_func__(self.__ClickOption), "mouse_click", "auto_login")
		self.__children["autoLoginText"] = CreateWindow(ui.TextLine(), self, (30 + 15, self.GetHeight() + 15 + 20 + 22), localeInfo.AUTO_HUNT_AUTO_LOGIN)

		self.__children["mountCheckBox"] = CreateWindow(ui.ImageBox(), self, (30 + 100, self.GetHeight() + 15 + 18 + 22), IMG_DIR+"unselected.tga")
		self.__children["mountCheckBox"].SetEvent(ui.__mem_func__(self.__ClickOption), "mouse_click", "mount")
		self.__children["mountText"] = CreateWindow(ui.TextLine(), self, (30 + 100 + 15, self.GetHeight() + 15 + 20 + 22), localeInfo.AUTO_HUNT_MOUNT)

		self.__children["mobRange"] = RANGE_CIRCLE

		self.__children["newOptions"] = {
			"auto_login" : 1,
			"stone" : 0,
			"mob" : 1,
			"mount" : 1,
		}

		self.SetCenterPosition()

	def __ClickOption(self, emptyArg, option):
		if self.IsActive():
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.AUTO_HUNT_CANT_CHANGE_ACTIVE)
			return
		self.__children["newOptions"][option] = 1 if not self.__children["newOptions"][option] else 0
		self.Refresh()

	def Refresh(self):
		slotItemDict = self.__children["slotItemDict"] if "slotItemDict" in self.__children else {}
		for key, itemIdx in slotItemDict.items():
			slotStatus = self.__children["slotStatus" + str(key)] if ("slotStatus" + str(key)) in self.__children else False
			self.__children["status"+str(key)].LoadImage(IMG_DIR+"check_1.tga" if slotStatus else IMG_DIR+"check_0.tga")

		bg = self.__children["bg"]

		if (self.__children["rangeStatus"] if "rangeStatus" in self.__children else False):
			miniMap.SetAutoHuntRangeStatus(True)
			self.__children["optionBtn"].Down()
			self.__children["rangeText"].Show()
			self.__children["sliderBar"].Show()
			self.__children["autoLoginCheckBox"].LoadImage(IMG_DIR + "selected.tga" if self.__children["newOptions"]["auto_login"] else IMG_DIR + "unselected.tga")
			self.__children["autoLoginCheckBox"].Show()
			self.__children["mobFarmCheckBox"].Show()
			self.__children["mobFarmCheckBox"].LoadImage(IMG_DIR + "selected.tga" if self.__children["newOptions"]["mob"] else IMG_DIR + "unselected.tga")
			self.__children["mobFarmText"].Show()
			self.__children["stoneFarmCheckBox"].Show()
			self.__children["stoneFarmCheckBox"].LoadImage(IMG_DIR + "selected.tga" if self.__children["newOptions"]["stone"] else IMG_DIR + "unselected.tga")
			self.__children["stoneFarmText"].Show()
			self.__children["autoLoginText"].Show()
			self.__children["mountCheckBox"].Show()
			self.__children["mountCheckBox"].LoadImage(IMG_DIR + "selected.tga" if self.__children["newOptions"]["mount"] else IMG_DIR + "unselected.tga")
			self.__children["mountText"].Show()
			self.SetSize(8 + bg.GetWidth() + 8, 29 + bg.GetHeight() + 9 + 25 + 62)

			mobRange = self.__children["mobRange"] if "mobRange" in self.__children else 0.0
			self.__children["sliderBar"].SetSliderPos((1.0/RANGE_CIRCLE) * mobRange if mobRange > 0 else 0.0)

		else:
			self.SetSize(8 + bg.GetWidth() + 8, 29 + bg.GetHeight() + 9)
			self.__children["rangeText"].Hide()
			self.__children["sliderBar"].Hide()
			self.__children["autoLoginText"].Hide()
			self.__children["autoLoginCheckBox"].Hide()
			self.__children["mobFarmCheckBox"].Hide()
			self.__children["mobFarmText"].Hide()
			self.__children["stoneFarmCheckBox"].Hide()
			self.__children["stoneFarmText"].Hide()
			self.__children["mountCheckBox"].Hide()
			self.__children["mountText"].Hide()
			self.__children["optionBtn"].SetUp()
			miniMap.SetAutoHuntRangeStatus(False)

		slot = self.__children["slot"]
		skillDict = self.__children["skillDict"] if "skillDict" in self.__children else {}
		for j in range(6):
			slot.ClearSlot(j)
			if j not in skillDict:
				continue
			slotNumber = skillDict[j]
			(skillIndex, skillGrade, skillLevel) = (player.GetSkillIndex(slotNumber), player.GetSkillGrade(slotNumber), player.GetSkillLevel(slotNumber))
			slot.SetSkillSlotNew(j, skillIndex, skillGrade, skillLevel)
			slot.SetSlotCountNew(j, skillGrade, skillLevel)
		slot.RefreshSlot()

		activeStatus = self.IsActive()
		self.__children["startBtn" if activeStatus else "stopBtn"].Down()
		self.__children["startBtn" if not activeStatus else "stopBtn"].SetUp()

	def CheckAutoLogin(self):
		autoHuntAutoLoginDict = constInfo.autoHuntAutoLoginDict
		if autoHuntAutoLoginDict["status"] == 1:
			constInfo.autoHuntAutoLoginDict["status"] = 0
			self.__children["skillDict"] = autoHuntAutoLoginDict["skillDict"]
			self.__children["slotStatus"] = autoHuntAutoLoginDict["slotStatus"]
			self.__children["newOptions"] = autoHuntAutoLoginDict["newOptions"]

			slotItemDict = self.__children["slotItemDict"] if "slotItemDict" in self.__children else {}
			for key, itemIdx in slotItemDict.items():
				self.__children["slotStatus" + str(key)] = autoHuntAutoLoginDict["slotStatus"][key]

			self.Refresh()
			self.__StartBtn()

	def __OnChangeRange(self):
		# Guard re-entrancy: SetSliderPos -> cursor.SetPosition -> (C++ OnMove) -> __OnMove ->
		# eventChange(__OnChangeRange) tworzy nieskonczona rekurencje (stack overflow). Przerwij ja.
		if self.__children.get("__inRange", False):
			return
		self.__children["__inRange"] = True
		try:
			if self.IsActive():
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.AUTO_HUNT_NEED_DEACTIVE)
				self.Refresh()
				return
			sliderBar = self.__children["sliderBar"]
			mobRange = ((1.0/RANGE_CIRCLE) * (sliderBar.GetSliderPos()*RANGE_CIRCLE)) * RANGE_CIRCLE
			self.__children["mobRange"] = mobRange
			miniMap.SetAutoHuntRange(mobRange)
		finally:
			self.__children["__inRange"] = False

	def __OptionBtn(self):
		rangeStatus = self.__children["rangeStatus"] if "rangeStatus" in self.__children else False
		self.__children["rangeStatus"] = not rangeStatus
		miniMap.SetAutoHuntRange(self.__children["mobRange"] if "mobRange" in self.__children else 0.0)
		self.Refresh()

	def IsActive(self):
		return self.__children["activeStatus"] if "activeStatus" in self.__children else False

	def __ResetBtn(self):
		if self.IsActive():
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.AUTO_HUNT_NEED_DEACTIVE)
			return
		self.__children["skillDict"] = {}
		slotItemDict = self.__children["slotItemDict"] if "slotItemDict" in self.__children else {}
		for key, itemIdx in slotItemDict.items():
			self.__children["slotStatus" + str(key)] = False
		self.Refresh()

	def SetStatus(self, status):
		self.__children["activeStatus"] = status
		#miniMap.SetAutoHuntStatus(status)
		self.Refresh()

	def __StartBtn(self):
		if self.IsActive():
			self.Refresh()
			return
		selectedItemText = ""
		selectedSkillText = ""
		slotItemDict = self.__children["slotItemDict"] if "slotItemDict" in self.__children else {}
		for key, itemIdx in slotItemDict.items():
			if selectedItemText != "":
				selectedItemText += "?"
			selectedItemText += "1" if (self.__children["slotStatus" + str(key)] if ("slotStatus" + str(key)) in self.__children else False) else "0"
		if selectedItemText == "":
			selectedItemText = "empty"

		skillDict = self.__children["skillDict"] if "skillDict" in self.__children else {}
		for key, skillSlotNumber in skillDict.items():
			if skillSlotNumber != -1:
				if selectedSkillText != "":
					selectedSkillText += "?"
				selectedSkillText += str(skillSlotNumber)
		if selectedSkillText == "":
			selectedSkillText = "empty"
		# Zsynchronizuj zasieg z C++ przed startem (inaczej, gdy gracz nie otworzyl Option/nie ruszyl
		# suwaka, bot uzylby domyslnej wartosci z Create zamiast mobRange = brak realnego zasiegu).
		mobRange = self.__children["mobRange"] if "mobRange" in self.__children else RANGE_CIRCLE
		miniMap.SetAutoHuntRange(mobRange)
		net.SendChatPacket("/auto_hunt start {} {} {} {} {} {}".format(selectedItemText, selectedSkillText, int(mobRange), self.__children["newOptions"]["mob"], self.__children["newOptions"]["stone"], self.__children["newOptions"]["mount"]))
		self.Refresh()

	def __StopBtn(self):
		if not self.IsActive():
			self.Refresh()
			return
		net.SendChatPacket("/auto_hunt end")
		self.Refresh()

	def __ClickStatus(self, emptyArg, slotIdx):
		if self.IsActive():
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.AUTO_HUNT_NEED_DEACTIVE)
			self.Refresh()
			return
		slotStatus = self.__children["slotStatus" + str(slotIdx)] if ("slotStatus" + str(slotIdx)) in self.__children else False
		self.__children["slotStatus" + str(slotIdx)] = not slotStatus
		self.Refresh()

	def __ClickSkillSlot(self, slotIndex):
		if self.IsActive():
			self.Refresh()
			return
		skillDict = self.__children["skillDict"] if "skillDict" in self.__children else {}
		if slotIndex not in skillDict:
			return
		self.__children["skillDict"][slotIndex] = -1
		self.Refresh()

	def SelectSlot(self, slotIndex):
		if self.IsActive():
			self.Refresh()
			return
		if True != mouseModule.mouseController.isAttached():
			return
		attachedSlotType = mouseModule.mouseController.GetAttachedType()
		if attachedSlotType == player.SLOT_TYPE_SKILL:
			attachedSlotNumber = mouseModule.mouseController.GetAttachedSlotNumber()
			skillDict = self.__children["skillDict"] if "skillDict" in self.__children else {}
			for key, skillSlotNumber in skillDict.items():
				if skillSlotNumber == attachedSlotNumber:
					skillDict[key] = -1
					break
			skillDict[slotIndex] = attachedSlotNumber
			self.__children["skillDict"] = skillDict
			self.Refresh()
		mouseModule.mouseController.DeattachObject()

	def __OverInSkill(self, index):
		skillDict = self.__children["skillDict"] if "skillDict" in self.__children else {}
		if index not in skillDict:
			return
		skillNumber = skillDict[index]
		interface = constInfo.GetInterfaceInstance()
		if interface:
			if interface.tooltipSkill:
				interface.tooltipSkill.SetSkillNew(skillNumber, player.GetSkillIndex(skillNumber), player.GetSkillGrade(skillNumber), player.GetSkillLevel(skillNumber))

	def __OverInItem(self, emptyArg, itemIdx):
		interface = constInfo.GetInterfaceInstance()
		if interface:
			if interface.tooltipItem:
				interface.tooltipItem.SetItemToolTip(itemIdx)

	def __OverOut(self, *args):
		interface = constInfo.GetInterfaceInstance()
		if interface:
			if interface.tooltipItem:
				interface.tooltipItem.HideToolTip()
			if interface.tooltipSkill:
				interface.tooltipSkill.HideToolTip()

	def Open(self):
		self.Refresh()
		self.Show()
		self.SetTop()

	def Close(self):
		miniMap.SetAutoHuntRangeStatus(False)
		self.Hide()

	def OnPressEscapeKey(self):
		self.Close()
		return True

def CreateWindow(window, parent, windowPos, windowArgument = "", windowPositionRule = "", windowSize = (-1, -1), windowFontName = -1):
	window.SetParent(parent)
	window.SetPosition(*windowPos)
	if windowSize != (-1, -1):
		window.SetSize(*windowSize)
	if windowPositionRule:
		splitList = windowPositionRule.split(":")
		if len(splitList) == 2:
			(type, mode) = (splitList[0], splitList[1])
			if type == "horizontal":
				if isinstance(window, ui.TextLine):
					if mode == "center":
						window.SetHorizontalAlignCenter()
					elif mode == "right":
						window.SetHorizontalAlignRight()
					elif mode == "left":
						window.SetHorizontalAlignLeft()
				else:
					if mode == "center":
						window.SetWindowHorizontalAlignCenter()
					elif mode == "right":
						window.SetWindowHorizontalAlignRight()
					elif mode == "left":
						window.SetWindowHorizontalAlignLeft()
			elif type == "vertical":
				if isinstance(window, ui.TextLine):
					if mode == "center":
						window.SetVerticalAlignCenter()
					elif mode == "top":
						window.SetVerticalAlignTop()
					elif mode == "bottom":
						window.SetVerticalAlignBottom()
				else:
					if mode == "top":
						window.SetWindowVerticalAlignTop()
					elif mode == "center":
						window.SetWindowVerticalAlignCenter()
					elif mode == "bottom":
						window.SetWindowVerticalAlignBottom()
	if windowArgument:
		if isinstance(window, ui.TextLine):
			if windowFontName != -1:
				window.SetFontName(windowFontName)
			window.SetText(windowArgument)
		elif isinstance(window, ui.NumberLine):
			window.SetNumber(windowArgument)
		elif isinstance(window, ui.ExpandedImageBox) or isinstance(window, ui.ImageBox):
			window.LoadImage(windowArgument if windowArgument.find("gr2") == -1 else "icon/item/27995.tga")
	window.Show()
	return window
