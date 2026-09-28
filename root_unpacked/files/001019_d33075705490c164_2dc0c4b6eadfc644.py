import constInfo
import app
import ime
import item
import grp
import net
import ui
from uiToolTip import ItemToolTip
import player
import mouseModule
import localeInfo
import wndMgr
import json
import io
import switchbot
import uiScriptLocale
import uiCommon
import chat
from _weakref import proxy

# DEBUG: ustaw na True zeby logi szly do chatu i syserr (debugowanie switchbota).
SWITCHBOT_DEBUG = False

def debug(*args):
	if not SWITCHBOT_DEBUG:
		return
	try:
		msg = "[switchbot] " + " ".join(str(a) for a in args)
		chat.AppendChat(chat.CHAT_TYPE_INFO, msg)
		import dbg
		dbg.TraceError(msg)
	except Exception:
		pass

SAVES_FILE_PATH = 'switchbot_new.json'

COLOR_INACTIVE = grp.GenerateColor(1.0, 0.0, 0.0, 0.2)
COLOR_ACTIVE   = grp.GenerateColor(1.0, 0.6, 0.1, 0.2)
COLOR_FINISHED = grp.GenerateColor(0.0, 1.0, 0.0, 0.2)
COLOR_SELECTED = grp.GenerateColor(1.0, 1.0, 1.0, 1.0)

SKILL_DAMAGE_BONUS_MAX = 33
NORMAL_HIT_DAMAGE_BONUS_MAX = 65
ADDON_TYPES = {item.APPLY_SKILL_DAMAGE_BONUS : SKILL_DAMAGE_BONUS_MAX, item.APPLY_NORMAL_HIT_DAMAGE_BONUS : NORMAL_HIT_DAMAGE_BONUS_MAX}

BOARD_WIDTH = 535
INPUT_HEIGHT = 27

BORDER_SPACE = 8
BORDER_SPACE_TOP = 30

ITEM_TAB_NAME_BOX_HEIGHT = 20
ITEM_TAB_SPACE = 2
ITEM_TAB_WIDTH = 32+(BORDER_SPACE*2)+ITEM_TAB_SPACE
ITEM_TAB_HEIGHT = (BORDER_SPACE * 2) + (3 * 32) + ITEM_TAB_NAME_BOX_HEIGHT
	
TOP_PANEL_HEIGHT = ((BORDER_SPACE * 2) + (3 * 32) + ITEM_TAB_NAME_BOX_HEIGHT)*2
TOP_PANEL_WIDTH = BOARD_WIDTH - (BORDER_SPACE * 2)

# Slot 0-4 = normalne atrybuty (1-5), Slot 5-6 = rare atrybuty (6-7).
# Musi byc zgodne z MAX_NORM_ATTR_NUM (5) + MAX_RARE_ATTR_NUM (2) z serwera.
ATTR_SLOT_COUNT = 7

# Wysokosc pojedynczego rzedu atrybutu — mniejsze od INPUT_HEIGHT (27) zeby
# zmiescic 7 rzedow w prawie tej samej przestrzeni co poprzednio 5 rzedow.
ATTR_ROW_HEIGHT = 20

MAIN_PANEL_WIDTH = BOARD_WIDTH - BORDER_SPACE * 2
MAIN_PANEL_HEIGHT = INPUT_HEIGHT + (ATTR_ROW_HEIGHT * ATTR_SLOT_COUNT)  # 1 AlternativeRow (27) + 7 attr rows (20 each) = 167

BOT_PANEL_HEIGHT = 50
BOT_PANEL_WIDTH = BOARD_WIDTH - BORDER_SPACE * 2

BOARD_HEIGHT = BORDER_SPACE_TOP + TOP_PANEL_HEIGHT + MAIN_PANEL_HEIGHT + BOT_PANEL_HEIGHT + BORDER_SPACE

SWITCH_TYPE_MAX = 5
SWITCH_ICON_LIST = {
	71084 : "71084.tga",
	71052 : "71052.tga",
	79012 : "zmianka_glove.tga",
	79011 : "200211.tga",
}
SWITCH_TYPE_LIST_BY_ITEM = {
	"normal" : [71084],  # Only normal bonus switching item
	"rare" : [71052],    # Only rare bonus switching item  
	"belt" : [79011],
	"gloves" : [79012],
}

def GetAffectString(affectType, affectValue):
	if not affectType:
		return None

	try:
		text = ItemToolTip.AFFECT_DICT[affectType](affectValue)
		text = text.replace("+-", "-")
		return text
	except TypeError:
		return "UNKNOWN_VALUE[{}] {}".format(affectType, affectValue)
	except KeyError:
		return "UNKNOWN_TYPE[{}] {}".format(affectType, affectValue)


class SwitchbotItemTab(ui.ThinBoardCircle):
	def __init__(self, slot_num):
		ui.ThinBoardCircle.__init__(self)
		
		self.slot_num = slot_num
		
		self.__Initialize()
		self.__LoadItemTab()
		
	def __del__(self):
		ui.ThinBoardCircle.__del__(self)
		
	def __Initialize(self):	
		self.tooltipItem = None
		self.onSelectEvent = None
		
		self.statusBar = None
		self.itemSlot = None
		self.selectButton = None
		
		self.lastSelectAlpha = 255
		self.lastSelectAlphaDir = 1
		self.popup = None
		
	def __LoadItemTab(self):	
		self.SetSize(ITEM_TAB_WIDTH, ITEM_TAB_HEIGHT)
	
		self.statusBar = ui.Bar()
		self.statusBar.SetParent(self)
		self.statusBar.SetSize(ITEM_TAB_WIDTH - 4, ITEM_TAB_HEIGHT - 4)
		self.statusBar.SetPosition(2, 2)
		
		self.selectBox = ui.Box()
		self.selectBox.SetParent(self)
		self.selectBox.SetPosition(1, 1)
		self.selectBox.SetSize(ITEM_TAB_WIDTH - 2, ITEM_TAB_HEIGHT - 2)
		self.selectBox.SetColor(COLOR_SELECTED)
			
		self.selectButton = ui.RadioButton()
		self.selectButton.SetParent(self)
		self.selectButton.SetUpVisual("kowal/switchbot/small_btn.png")
		self.selectButton.SetOverVisual("kowal/switchbot/small_btn_over.png")
		self.selectButton.SetDownVisual("kowal/switchbot/small_btn_down.png")
		self.selectButton.SetDisableVisual("kowal/switchbot/small_btn.png")
		self.selectButton.SetWindowHorizontalAlignCenter()
		self.selectButton.SetPosition(0, 5)
		self.selectButton.SetText(str(self.slot_num+1))
		self.selectButton.SetEvent(ui.__mem_func__(self.__OnSelectButtonClick))
		self.selectButton.Show()
	
		self.itemSlot = ui.GridSlotWindow()
		self.itemSlot.SetParent(self)
		self.itemSlot.ArrangeSlot(0, 1, 3, 32, 32, 0, 0)
		self.itemSlot.SetSlotBaseImage("d:/ymir work/ui/public/slot_base.sub", 1.0, 1.0, 1.0, 1.0)
		self.itemSlot.SetWindowHorizontalAlignCenter()
		self.itemSlot.SetPosition(0, 30)
		self.itemSlot.SetOverInItemEvent(ui.__mem_func__(self.OverInItem))
		self.itemSlot.SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))
		self.itemSlot.SetSelectEmptySlotEvent(ui.__mem_func__(self.SelectEmptySlot))
		self.itemSlot.SetSelectItemSlotEvent(ui.__mem_func__(self.SelectItemSlot))
		self.itemSlot.SetUnselectItemSlotEvent(ui.__mem_func__(self.UseItemSlot))
		self.itemSlot.SetUseSlotEvent(ui.__mem_func__(self.UseItemSlot))	
		self.itemSlot.Show()
		
	def Destroy(self):
		self.slot_num = None
		self.tooltipItem = None
		self.onSelectEvent = None
		self.statusBar = None
		self.itemSlot = None
		self.selectButton = None
		self.lastSelectAlpha = None
		self.lastSelectAlphaDir = None
		self.popup = None
		self.selectBox = None
		
	def SetItemToolTip(self, tooltipItem):
		self.tooltipItem = proxy(tooltipItem)
		
	def OnPlacedItem(self, slot_num):
		pass
		
	def OverOutItem(self):
		self.itemSlot.SetUsableItem(False)
		if self.tooltipItem:
			self.tooltipItem.HideToolTip()			
			
	def OverInItem(self, overSlotPos):
		self.itemSlot.SetUsableItem(True)

		if self.IsEmpty():
			return

		self.tooltipItem.ClearToolTip()
		self.tooltipItem.SetRenderOnKey(True)

		itemVnum = player.GetItemIndex(player.SWITCHBOT, self.slot_num)
		metinSlot = [player.GetItemMetinSocket(player.SWITCHBOT, self.slot_num, i) for i in range(player.METIN_SOCKET_MAX_NUM)]
		attrSlot = [player.GetItemAttribute(player.SWITCHBOT, self.slot_num, i) for i in range(player.ATTRIBUTE_SLOT_MAX_NUM)]
		
		self.tooltipItem.AddItemData(itemVnum, metinSlot, attrSlot)
		self.tooltipItem.ShowToolTip()
		
	def SelectEmptySlot(self, selectedSlotPos):
		if constInfo.GET_ITEM_QUESTION_DIALOG_STATUS() == 1:
			return
			
		check = player.GetItemIndex(player.SWITCHBOT, self.slot_num)
		if check:
			mouseModule.mouseController.DeattachObject()
			return

		if mouseModule.mouseController.isAttached():

			attachedSlotType = mouseModule.mouseController.GetAttachedType()
			attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
			attachedItemCount = mouseModule.mouseController.GetAttachedItemCount()
			attachedItemIndex = mouseModule.mouseController.GetAttachedItemIndex()

			if player.SLOT_TYPE_INVENTORY == attachedSlotType:
				attachedCount = mouseModule.mouseController.GetAttachedItemCount()
				net.SendItemMovePacket(player.INVENTORY, attachedSlotPos, player.SWITCHBOT, self.slot_num, int(attachedItemCount))
			elif player.SLOT_TYPE_SWITCHBOT == attachedSlotType:
				attachedCount = mouseModule.mouseController.GetAttachedItemCount()
				net.SendItemMovePacket(player.SWITCHBOT, attachedSlotPos, player.SWITCHBOT, self.slot_num, int(attachedItemCount))
				
			mouseModule.mouseController.DeattachObject()

			self.OnPlacedItem(self.slot_num)
		
	def SelectItemSlot(self, itemSlotIndex):
		if constInfo.GET_ITEM_QUESTION_DIALOG_STATUS() == 1:
			return
			
		if switchbot.IsActive(self.slot_num):
			return
		
		if mouseModule.mouseController.isAttached():
			mouseModule.mouseController.DeattachObject()
		else:

			if app.IsPressed(app.DIK_LALT):
				link = player.GetItemLink(player.SWITCHBOT, self.slot_num)
				ime.PasteString(link)
			else:
				itemVnum = player.GetItemIndex(player.SWITCHBOT, self.slot_num)
				itemCount = player.GetItemCount(player.SWITCHBOT, self.slot_num)
				mouseModule.mouseController.AttachObject(self, player.SLOT_TYPE_SWITCHBOT, self.slot_num, itemVnum, itemCount)
				
	def UseItemSlot(self, slotIndex):
		curCursorNum = app.GetCursor()
		if app.SELL == curCursorNum:
			return

		if constInfo.GET_ITEM_QUESTION_DIALOG_STATUS() == 1:
			return

		net.SendItemUsePacket(player.SWITCHBOT, self.slot_num)
		mouseModule.mouseController.DeattachObject()
		self.OverOutItem()
			
	def RefreshItemSlot(self):
		if self.IsEmpty():
			self.itemSlot.ClearSlot(0)
			self.statusBar.Hide()
		else:
			itemCount = player.GetItemCount(player.SWITCHBOT, self.slot_num)
			itemVnum = player.GetItemIndex(player.SWITCHBOT, self.slot_num)
			if itemCount == 1:
				itemCount = 0

			self.itemSlot.SetItemSlot(0, itemVnum, itemCount)

			self.statusBar.Show()
			if self.IsFinished():
				self.itemSlot.DeactivateSlot(0)
				self.statusBar.SetColor(COLOR_FINISHED)
			elif self.IsActive():
				self.itemSlot.ActivateSlot(0)
				self.statusBar.SetColor(COLOR_ACTIVE)
			else:
				self.itemSlot.DeactivateSlot(0)
				self.statusBar.SetColor(COLOR_INACTIVE)
		
		self.itemSlot.RefreshSlot()
		
	def IsEmpty(self):
		itemVnum = player.GetItemIndex(player.SWITCHBOT, self.slot_num)	
		return not itemVnum
		
	def IsActive(self):
		return switchbot.IsActive(self.slot_num)
		
	def IsFinished(self):
		return switchbot.IsFinished(self.slot_num)
		
	def GetSlotNum(self):
		return self.slot_num
		
	def SetOnSelectEvent(self, event):
		self.onSelectEvent = event
		
	def __OnSelectButtonClick(self):
		if self.onSelectEvent:
			self.onSelectEvent(self.slot_num)
			
	def SetUp(self):
		if self.selectButton:
			self.selectButton.SetUp()
			self.selectBox.Hide()
			
	def Down(self):
		if self.selectButton:
			self.selectButton.Down()
			
			self.lastSelectAlpha = 255
			self.selectBox.Show()
			
	def OnUpdate(self):
		if self.selectBox.IsShow():
			rate = 3
			
			self.lastSelectAlpha -= (rate * self.lastSelectAlphaDir)
		
			if self.lastSelectAlpha <= 0:
				self.lastSelectAlpha = 0
				self.lastSelectAlphaDir = -1
			elif self.lastSelectAlpha >= 255:
				self.lastSelectAlpha = 255
				self.lastSelectAlphaDir = 1
				
			self.selectBox.SetColor(grp.GenerateColor(1.0, 1.0, 1.0, float(self.lastSelectAlpha) / 255.0))
			
class SwitchbotAttribute(ui.Window):
	VALUE_WIDTH = 50
	
	typeInput = None
	typeTextLine = None
	searchTypeButton = None
	deleteAttributeButton = None
	valueInput = None
	valueEditLine = None	
	
	def __init__(self, switchBotWindow):
		ui.Window.__init__(self, "UI")	
		self.__Initialize()
		self.wndSwitch = proxy(switchBotWindow)
		
	def __del__(self):
		ui.Window.__del__(self)
		
	def __Initialize(self):
		self.selectedSlot = -1
		self.alternative = 0
		self.index = -1
		
		self.attributeType = 0
		self.attributeValue = 0
		
		self.searchEvent = None
		self.attributeMaxValue = 0	
	
		self.typeInput = None
		self.typeTextLine = None
		self.searchTypeButton = None
		self.deleteAttributeButton = None
		self.valueInput = None
		self.valueEditLine = None
		self.wndSwitch = None

	def Create(self, width, index):
		self.index = index
		self.SetSize(width, ATTR_ROW_HEIGHT)

		self.typeInput = ui.ThinBoardCircle()
		self.typeInput.SetParent(self)
		self.typeInput.SetSize(width - self.VALUE_WIDTH, ATTR_ROW_HEIGHT)
		self.typeInput.SetPosition(0, 0)
		self.typeInput.Show()
		
		self.typeTextLine = ui.TextLine()
		self.typeTextLine.SetParent(self.typeInput)
		self.typeTextLine.SetText(localeInfo.SWITCHBOT_EMPTY_ATTR)
		self.typeTextLine.SetVerticalAlignCenter()
		self.typeTextLine.SetWindowVerticalAlignCenter()
		self.typeTextLine.SetHorizontalAlignCenter()
		self.typeTextLine.SetWindowHorizontalAlignCenter()
		self.typeTextLine.SetPosition(-20, -1)
		self.typeTextLine.Show()
			
		self.searchTypeButton = ui.Button()
		self.searchTypeButton.SetParent(self.typeInput)
		self.searchTypeButton.SetUpVisual("d:/ymir work/ui/switchbot/search_attr_01.sub")
		self.searchTypeButton.SetOverVisual("d:/ymir work/ui/switchbot/search_attr_02.sub")
		self.searchTypeButton.SetDownVisual("d:/ymir work/ui/switchbot/search_attr_03.sub")
		self.searchTypeButton.SetDisableVisual("d:/ymir work/ui/switchbot/search_attr_03.sub")
		self.searchTypeButton.SetWindowHorizontalAlignRight()
		self.searchTypeButton.SetWindowVerticalAlignCenter()
		self.searchTypeButton.SetPosition(24 * 2 + 2, 1)
		self.searchTypeButton.SetEvent(ui.__mem_func__(self.__OnClickSearchButton))
		self.searchTypeButton.Show()
		
		self.deleteAttributeButton = ui.Button()
		self.deleteAttributeButton.SetParent(self.typeInput)
		self.deleteAttributeButton.SetUpVisual("d:/ymir work/ui/switchbot/delete_attr_01.sub")
		self.deleteAttributeButton.SetOverVisual("d:/ymir work/ui/switchbot/delete_attr_02.sub")
		self.deleteAttributeButton.SetDownVisual("d:/ymir work/ui/switchbot/delete_attr_03.sub")
		self.deleteAttributeButton.SetDisableVisual("d:/ymir work/ui/switchbot/delete_attr_03.sub")
		self.deleteAttributeButton.SetWindowHorizontalAlignRight()
		self.deleteAttributeButton.SetWindowVerticalAlignCenter()
		self.deleteAttributeButton.SetPosition(24 + 2, 1)
		self.deleteAttributeButton.SetToolTipText(localeInfo.SWITCHBOT_CLEAR_ATTR)
		self.deleteAttributeButton.SetEvent(ui.__mem_func__(self.OnClickClearButton))
		self.deleteAttributeButton.Show()		
		
		self.valueInput = ui.ThinBoardCircle()
		self.valueInput.SetParent(self)
		self.valueInput.SetSize(self.VALUE_WIDTH, ATTR_ROW_HEIGHT)
		self.valueInput.SetPosition(width - self.VALUE_WIDTH, 0)
		self.valueInput.Show()
		
		self.valueEditLine = ui.EditLine()
		self.valueEditLine.SetParent(self.valueInput)
		self.valueEditLine.SetSize(self.VALUE_WIDTH, 18)
		self.valueEditLine.SetMax(4)
		self.valueEditLine.SetNumberMode()
		self.valueEditLine.SetText("0")
		self.valueEditLine.SetPosition(10, 7)
		self.valueEditLine.Show()
		self.valueEditLine.OnIMEUpdate = self.__OnEditLineIMEUpdate
		self.valueEditLine.SetEscapeEvent(ui.__mem_func__(self.__OnEscapeEvent))
		
	def Destroy(self):
		if self.wndSwitch:
			self.wndSwitch.Destroy()
			self.wndSwitch = None
		self.selectedSlot = None
		self.alternative = None
		self.index = None
		self.attributeType = None
		self.attributeValue = None
		self.searchEvent = None
		self.attributeMaxValue = None
		self.typeInput = None
		self.typeTextLine = None
		self.searchTypeButton = None
		self.deleteAttributeButton = None
		self.valueInput = None
		self.valueEditLine = None
		self.attributeUpdateEvent = None
		self.escapeEvent = None

	def Hide(self):
		ui.Window.Hide(self)
		
		if self.valueEditLine:
			self.valueEditLine.KillFocus()
			
	def RefreshAttributeRow(self, slot_num, alternative, index):
		self.selectedSlot = slot_num
		self.alternative = alternative
		self.index = index	
	
		if switchbot.IsActive(slot_num):
			self.searchTypeButton.Disable()
			self.deleteAttributeButton.Disable()
			self.valueEditLine.Hide()
		else:
			self.searchTypeButton.Enable()
			self.deleteAttributeButton.Enable()	
			self.valueEditLine.Show()
		
		# Get the switching item to determine how to handle attribute mapping
		switchItemVnum = self.wndSwitch.switchItemVnum[self.wndSwitch.selectedSlot]
		
		debug("RefreshAttributeRow: slot={}, alt={}, index={}, switchItemVnum={}".format(
			slot_num, alternative, index, switchItemVnum))
		
		if switchItemVnum in (71052,):
			# For rare bonuses: map UI index (0,1) to actual rare slots (5,6)
			actualSlotIndex = player.ATTRIBUTE_SLOT_RARE_START + index
			debug("Rare bonus: mapping UI index {} to actual slot {}".format(index, actualSlotIndex))
			
			# Check if this UI slot corresponds to a valid rare slot
			if actualSlotIndex >= player.ATTRIBUTE_SLOT_RARE_END:
				debug("UI index {} maps to slot {} which is beyond rare range, hiding".format(index, actualSlotIndex))
				self.SetAttribute(localeInfo.SWITCHBOT_EMPTY_ATTR, 0)
				return
			
			(actualType, actualValue) = player.GetItemAttribute(player.SWITCHBOT, slot_num, actualSlotIndex)
			debug("Actual rare attribute: type={}, value={}".format(actualType, actualValue))
			
			if actualType and actualValue:
				affectString = GetAffectString(actualType, actualValue)
				debug("Rare affectString: '{}'".format(affectString))
				if affectString:
					self.SetAttribute(affectString, actualValue)
					return
			
			# No rare attribute in this slot
			self.SetAttribute(localeInfo.SWITCHBOT_EMPTY_ATTR, 0)
		else:
			# For normal bonuses: use the configured switchbot attribute
			(type, value) = switchbot.GetAttribute(slot_num, alternative, index)
			debug("Normal attribute: type={}, value={}".format(type, value))
			
			if not type:
				self.SetAttribute(localeInfo.SWITCHBOT_EMPTY_ATTR, 0)
				return
	
			affectString = GetAffectString(type, value)
			debug("Normal affectString: '{}'".format(affectString))
			
			if not affectString:
				self.SetAttribute(localeInfo.SWITCHBOT_EMPTY_ATTR, 0)
				return
				
			self.SetAttribute(affectString, value)

	def __OnEditLineIMEUpdate(self):
		switchItemVnum = self.wndSwitch.switchItemVnum[self.wndSwitch.selectedSlot]

		ui.EditLine.OnIMEUpdate(self.valueEditLine)
		
		text = self.valueEditLine.GetText()
		if len(text) > 0 and text.isdigit():
			(curType, curValue) = switchbot.GetAttribute(self.selectedSlot, self.alternative, self.index)
			
			maxValue = 0
			if curType not in ADDON_TYPES:
				maxValue = switchbot.GetAttributeMaxValue(self.selectedSlot, curType, switchItemVnum)
				
			value = int(text)
			
			if value == curValue:
				return
			
			if maxValue != 0 and value > maxValue:
				value = maxValue
				self.valueEditLine.SetText(str(value))
				
			switchbot.SetAttribute(self.selectedSlot, self.alternative, self.index, curType, value)
			self.typeTextLine.SetText(GetAffectString(curType, value))
			self.__OnAttributeUpdate()
		
	def SetSearchEvent(self, event):
		self.searchEvent= event
		
	def __OnClickSearchButton(self):
		if self.searchEvent:
			self.searchEvent(self.index)
		
	def SetAttributeUpdateEvent(self, event):
		self.attributeUpdateEvent = event		
		
	def __OnAttributeUpdate(self):
		if self.attributeUpdateEvent:
			self.attributeUpdateEvent(self.index)
			
	def SetEscapeEvent(self, event):
		self.escapeEvent = event			
			
	def __OnEscapeEvent(self):
		if self.escapeEvent:
			self.escapeEvent()
			
	def OnClickClearButton(self, all = False):
		self.SetAttribute(localeInfo.SWITCHBOT_EMPTY_ATTR, 0)
		if all:
			for i in range(switchbot.ALTERNATIVE_COUNT):
				switchbot.SetAttribute(self.selectedSlot, i, self.index, 0, 0)
				switchbot.SetAttribute(self.selectedSlot, i, self.index, 0, 0)
		else:
			switchbot.SetAttribute(self.selectedSlot, self.alternative, self.index, 0, 0)
		self.__OnAttributeUpdate()		
			
	def SetAttribute(self, applyname, maxValue):
		self.typeTextLine.SetText(applyname)
		self.valueEditLine.SetText(str(maxValue))
		
	def GetIndex(self):
		return self.index

class SwitchbotWindow(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self, "UI")
		self.isLoaded = 0

		try:
			self.__Initialize()
			self.__LoadWindow()
		except:
			import exception
			exception.Abort("SwitchbotWindow.__init__")
	
	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __Initialize(self):		
		self.selectedSlot = 0
		self.alternative = 0
		self.switchItemVnum = [0 for i in range(switchbot.SLOT_COUNT)]
		self.alternativeButtons = {}
		self.switchTypeBtns = {}
		self.itemTabs = {}
		self.attrDict = {}
		self.attributeSearchWindow = None
		self.attrSearchIdx = -1
		self.configurationSaveWindow = None
		self.petLvl = 0
		self.refreshDelay = None
		self.instantSwitchData = {"cooldownEnd": None}

	def __LoadWindow(self):
		if self.isLoaded == 1:
			return

		self.isLoaded = 1

		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "uiscript/switchbot.py")

		except:
			import exception
			exception.Abort("SwitchbotWindow.__LoadWindow.LoadObject")

		self.board = self.GetChild("board")
		self.board.SetCloseEvent(ui.__mem_func__(self.Close))

		self.SetSize(BOARD_WIDTH, BOARD_HEIGHT)
		self.board.SetSize(BOARD_WIDTH, BOARD_HEIGHT)
		
		self.topPanel = ui.ThinBoardCircle()
		self.topPanel.SetParent(self)
		self.topPanel.SetSize(TOP_PANEL_WIDTH, TOP_PANEL_HEIGHT)
		self.topPanel.SetPosition(BORDER_SPACE, BORDER_SPACE_TOP)
		self.topPanel.Show()
		
		xPos, yPos = 0, 0
		for i in range(switchbot.SLOT_COUNT):	
			itemTab = SwitchbotItemTab(i)
			itemTab.SetParent(self.topPanel)
			itemTab.SetPosition((ITEM_TAB_WIDTH + ITEM_TAB_SPACE) * xPos, yPos)
			itemTab.SetOnSelectEvent(ui.__mem_func__(self.SelectSlot))
			itemTab.OnPlacedItem = self.__OnPlacedItem
			itemTab.Show()

			self.itemTabs[i] = itemTab
			
			xPos += 1

			if xPos >= 10:
				xPos = 0
				yPos = ITEM_TAB_HEIGHT

		self.mainPanel = ui.ThinBoardCircle()
		self.mainPanel.SetParent(self)
		self.mainPanel.SetSize(MAIN_PANEL_WIDTH, MAIN_PANEL_HEIGHT)
		self.mainPanel.SetPosition(BORDER_SPACE, BORDER_SPACE_TOP + TOP_PANEL_HEIGHT)
		self.mainPanel.Show()
		
		self.alternativePanel = ui.ThinBoardCircle()
		self.alternativePanel.SetParent(self.mainPanel)
		self.alternativePanel.SetSize(MAIN_PANEL_WIDTH, INPUT_HEIGHT)
		self.alternativePanel.SetPosition(0, 0)
		self.alternativePanel.Show()
		
		self.alternativeTextLine = ui.TextLine()
		self.alternativeTextLine.SetParent(self.alternativePanel)
		self.alternativeTextLine.SetPosition(5, -1)
		self.alternativeTextLine.SetVerticalAlignCenter()
		self.alternativeTextLine.SetWindowVerticalAlignCenter()
		self.alternativeTextLine.SetText(localeInfo.SWITCHBOT_ALTERNATIVE)
		self.alternativeTextLine.Show()
		
		for i in range(switchbot.ALTERNATIVE_COUNT):
			alternativeButton = ui.RadioButton()
			alternativeButton.SetParent(self.alternativePanel)
			alternativeButton.SetUpVisual("kowal/switchbot/small_btn.png")
			alternativeButton.SetOverVisual("kowal/switchbot/small_btn_over.png")
			alternativeButton.SetDownVisual("kowal/switchbot/small_btn_down.png")
			alternativeButton.SetWindowVerticalAlignCenter()
			alternativeButton.SetPosition(60 + alternativeButton.GetWidth() * i, 0)
			alternativeButton.SetText(str(i+1))
			alternativeButton.SetEvent(lambda arg = i : self.SelectAlternative(arg))
			alternativeButton.Show()
			
			self.alternativeButtons[i] = alternativeButton

		for i in range(SWITCH_TYPE_MAX):
			self.switchTypeBtns[i] = {}
			self.switchTypeBtns[i]["btn"] = ui.RadioButton()
			self.switchTypeBtns[i]["btn"].SetParent(self.mainPanel)
			self.switchTypeBtns[i]["btn"].SetUpVisual("kowal/switchbot/small_btn.png")
			self.switchTypeBtns[i]["btn"].SetOverVisual("kowal/switchbot/small_btn_over.png")
			self.switchTypeBtns[i]["btn"].SetDownVisual("kowal/switchbot/small_btn_down.png")
			self.switchTypeBtns[i]["btn"].SetPosition(5+(self.switchTypeBtns[i]["btn"].GetWidth()+2)*(i+1), 3)
			self.switchTypeBtns[i]["btn"].SetWindowHorizontalAlignRight()

			scale = 0.6
			x = self.switchTypeBtns[i]["btn"].GetWidth() // 2 - (scale*32//2)
			y = self.switchTypeBtns[i]["btn"].GetHeight() // 2 - (scale*32//2)
			self.switchTypeBtns[i]["icon"] = ui.MakeExpandedImageBox(self.switchTypeBtns[i]["btn"], "icon/item/71084.tga", 0, 0)
			self.switchTypeBtns[i]["icon"].SetScale(scale, scale)
			self.switchTypeBtns[i]["icon"].SetPosition(x,y)
			self.switchTypeBtns[i]["icon"].SetSize(0,0)
		
		for i in range(ATTR_SLOT_COUNT):
			attr = SwitchbotAttribute(self)
			attr.SetParent(self.mainPanel)
			attr.Create(MAIN_PANEL_WIDTH, i)
			# Krok rzedu = ATTR_ROW_HEIGHT (mniejszy niz INPUT_HEIGHT, by 7 rzedow zmiescilo sie kompaktowo).
			attr.SetPosition(0, INPUT_HEIGHT + (ATTR_ROW_HEIGHT * i))
			attr.SetSearchEvent(ui.__mem_func__(self.__OnSearchAttribute))
			attr.SetAttributeUpdateEvent(ui.__mem_func__(self.__OnAttributeUpdate))
			attr.SetEscapeEvent(ui.__mem_func__(self.Close))
			attr.Show()

			self.attrDict[i] = attr
			
		self.botPanel = ui.ThinBoardCircle()
		self.botPanel.SetParent(self)
		self.botPanel.SetSize(BOT_PANEL_WIDTH, BOT_PANEL_HEIGHT)
		self.botPanel.SetPosition(BORDER_SPACE, BORDER_SPACE_TOP + TOP_PANEL_HEIGHT + MAIN_PANEL_HEIGHT)
		self.botPanel.Show()			
		
		self.saveButton = ui.Button()
		self.saveButton.SetParent(self.botPanel)
		self.saveButton.SetUpVisual("d:/ymir work/ui/switchbot/save_attr_01.sub")
		self.saveButton.SetOverVisual("d:/ymir work/ui/switchbot/save_attr_02.sub")
		self.saveButton.SetDownVisual("d:/ymir work/ui/switchbot/save_attr_03.sub")
		self.saveButton.SetDisableVisual("d:/ymir work/ui/switchbot/save_attr_03.sub")
		self.saveButton.SetWindowVerticalAlignBottom()
		self.saveButton.SetPosition(BORDER_SPACE, 30)
		self.saveButton.SetToolTipText(localeInfo.SWITCHBOT_SAVE_BUTTON)
		self.saveButton.SetEvent(ui.__mem_func__(self.OpenSaveConfiguration))
		self.saveButton.Show()
		
		self.startButton = ui.Button()
		self.startButton.SetParent(self.botPanel)
		self.startButton.SetUpVisual("d:/ymir work/ui/switchbot/btn_big_01.sub")
		self.startButton.SetOverVisual("d:/ymir work/ui/switchbot/btn_big_02.sub")
		self.startButton.SetDownVisual("d:/ymir work/ui/switchbot/btn_big_03.sub")
		self.startButton.SetDisableVisual("d:/ymir work/ui/switchbot/btn_big_03.sub")
		self.startButton.SetWindowVerticalAlignBottom()
		self.startButton.SetWindowHorizontalAlignCenter()
		self.startButton.SetPosition(-30 - self.startButton.GetWidth() // 2, 30)
		self.startButton.SetText(localeInfo.SWITCHBOT_START)
		self.startButton.SetEvent(ui.__mem_func__(self.SetActive), True)
		self.startButton.Show()
		
		self.stopButton = ui.Button()
		self.stopButton.SetParent(self.botPanel)
		self.stopButton.SetUpVisual("d:/ymir work/ui/switchbot/btn_big_01.sub")
		self.stopButton.SetOverVisual("d:/ymir work/ui/switchbot/btn_big_02.sub")
		self.stopButton.SetDownVisual("d:/ymir work/ui/switchbot/btn_big_03.sub")
		self.stopButton.SetDisableVisual("d:/ymir work/ui/switchbot/btn_big_03.sub")
		self.stopButton.SetWindowVerticalAlignBottom()
		self.stopButton.SetWindowHorizontalAlignCenter()
		self.stopButton.SetPosition(-30 + self.stopButton.GetWidth() // 2 + 20, 30)
		self.stopButton.SetText(localeInfo.SWITCHBOT_STOP)
		self.stopButton.SetEvent(ui.__mem_func__(self.SetActive), False)
		self.stopButton.Show()

		self.instantSlider = ui.SliderBar()
		self.instantSlider.SetParent(self.botPanel)
		self.instantSlider.SetWindowHorizontalAlignCenter()
		self.instantSlider.SetPosition(0, 5)
		self.instantSlider.SetSliderPos(0)
		self.instantSlider.SetEvent(ui.__mem_func__(self.__RefreshButtons))
		self.instantSlider.Hide()

		self.instantSliderTitle = ui.MakeTextLine2(self.instantSlider, -8, -1, localeInfo.SWITCHBOT_INSTANT_COUNT_TITLE)
		self.instantSliderTitle.SetHorizontalAlignRight()
		self.instantSliderTitle.Show()

		self.instantSliderCount = ui.MakeTextLine2(self.instantSlider, self.instantSlider.GetWidth()+8, -1)
		self.instantSliderCount.Show()

		self.instantCheckbox = ui.CheckBox()
		self.instantCheckbox.SetParent(self.botPanel)
		self.instantCheckbox.SetEvent(ui.__mem_func__(self.OnInstantCheckboxChange), "ON_CHECK", True)
		self.instantCheckbox.SetEvent(ui.__mem_func__(self.OnInstantCheckboxChange), "ON_UNCHECK", False)
		self.instantCheckbox.SetWindowVerticalAlignBottom()
		self.instantCheckbox.SetWindowHorizontalAlignRight()
		self.instantCheckbox.SetTextInfo("|Ed:/ymir work/ui/fast_switch.png|e")
		self.instantCheckbox.SetToolTipText(localeInfo.SWITCHBOT_INSTANT, -70, -28)
		self.instantCheckbox.SetPosition(BORDER_SPACE + self.instantCheckbox.GetWidth(), 25)
		self.instantCheckbox.Hide()

		self.refreshDelay = app.GetTime()

		if constInfo.windowIsOpened("switchbot"):
			self.Open()

		slot = constInfo.getWindowValue("switchbot", "slot")
		if slot != None:
			self.SelectSlot(slot)
		else:
			self.SelectSlot(0)

		switchType = constInfo.getWindowValue("switchbot", "switchType")
		switchTypeVnum = constInfo.getWindowValue("switchbot", "switchTypeVnum")

		if switchType != None and switchTypeVnum != None:
			self.SelectSwitchType(switchType, switchTypeVnum)

		pos = constInfo.getWindowValue("switchbot", "pos")
		if pos[0] != None:
			self.SetPosition(pos[0], pos[1])

	def Destroy(self):
		self.isLoaded = None
		self.selectedSlot = None
		self.alternative = None
		self.switchItemVnum = None
		self.alternativeButtons = None
		self.switchTypeBtns = None
		self.itemTabs = None
		self.attrDict = None
		if self.attributeSearchWindow:
			self.attributeSearchWindow.Destroy()
			self.attributeSearchWindow = None
		self.attrSearchIdx = None
		if self.configurationSaveWindow:
			self.configurationSaveWindow.Destroy()
			self.configurationSaveWindow = None
		self.topPanel = None
		self.mainPanel = None
		self.botPanel = None
		self.startButton = None
		self.stopButton = None
		self.instantSlider = None
		self.instantSliderTitle = None
		self.instantSliderCount = None
		self.instantCheckbox = None
		self.petLvl = None
		self.board = None
		self.alternativePanel = None
		self.alternativeTextLine = None
		self.saveButton = None
		self.popup = None
		self.refreshDelay = None
		self.instantSwitchData = None

	def Open(self):
		self.Show()
		# self.SetTop()
		# self.SetCenterPosition()
		self.RefreshSwitchbotWindow()
		constInfo.setWindowValue("switchbot", "status", constInfo.windowStatusOpened)

	def Close(self):
		if self.attributeSearchWindow:
			self.attributeSearchWindow.Close()
			
		if self.configurationSaveWindow:
			self.configurationSaveWindow.Close()
			
		self.Hide()
		constInfo.setWindowValue("switchbot", "status", constInfo.windowStatusClosed)
		return True
		
	def __OnPlacedItem(self, slot_num):
		self.SelectSlot(slot_num)
		
	def SelectSlot(self, selectedSlot):
		self.itemTabs[self.selectedSlot].SetUp()
		self.selectedSlot = selectedSlot
		self.itemTabs[self.selectedSlot].Down()
		constInfo.setWindowValue("switchbot", "slot", selectedSlot)
		self.SelectAlternative(0)
		
	def GetSelectedSlot(self):
		return self.selectedSlot

	def SelectAlternative(self, alternative):
		self.alternativeButtons[self.alternative].SetUp()
		self.alternative = alternative
		self.alternativeButtons[self.alternative].Down()
		
		self.RefreshSwitchbotWindow()
		
	def DebugItemInfo(self):
		slot = self.selectedSlot
		itemVnum = player.GetItemIndex(player.SWITCHBOT, slot)
		if not itemVnum:
			debug("DEBUG: No item in slot", slot)
			return
			
		item.SelectItem(itemVnum)
		itemType = item.GetItemType()
		itemSubType = item.GetItemSubType()
		
		debug("=== ITEM DEBUG ===")
		debug("Slot:", slot)
		debug("ItemVnum:", itemVnum)
		debug("ItemType:", itemType)
		debug("ItemSubType:", itemSubType)
		debug("item.BELT:", getattr(item, 'BELT', 'NOT_FOUND'))
		
		# Check what attributes the item has
		debug("Item attributes:")
		for i in range(player.ATTRIBUTE_SLOT_MAX_NUM):
			(attrType, attrValue) = player.GetItemAttribute(player.SWITCHBOT, slot, i)
			if attrType and attrValue:
				debug("  Slot {}: type={}, value={}".format(i, attrType, attrValue))
		
		# Check switchbot functions
		attributeSet = switchbot.GetAttributesForSet(slot, 79011)  # Test with belt switching item
		debug("AttributeSet for belt (79011):", attributeSet)
		debug("=== END ITEM DEBUG ===")
		
	def TestSearchDebug(self):
		debug("=== TESTING SERVER DATA ===")
		
		# Test what the server is actually sending for different switching items
		attributes_71084 = switchbot.GetAttributesForSet(self.selectedSlot, 71084)
		debug("71084 attributes count:", len(attributes_71084))
		debug("71084 first 3 attributes:")
		for i in range(min(3, len(attributes_71084))):
			debug("  71084[{}]: type={}, value={}".format(i, attributes_71084[i][0], attributes_71084[i][1]))
		
		attributes_71052 = switchbot.GetAttributesForSet(self.selectedSlot, 71052)
		debug("71052 attributes count:", len(attributes_71052))
		debug("71052 first 3 attributes:")
		for i in range(min(3, len(attributes_71052))):
			debug("  71052[{}]: type={}, value={}".format(i, attributes_71052[i][0], attributes_71052[i][1]))
		
		# Check if they're returning the same data (they shouldn't!)
		if len(attributes_71084) > 0 and len(attributes_71052) > 0:
			if attributes_71084[0][0] == attributes_71052[0][0]:
				debug("ERROR: Server sending SAME attributes for 71084 and 71052!")
			else:
				debug("GOOD: Server sending different attributes for 71084 vs 71052")
		
		# Test current switching item
		currentSwitchItem = self.switchItemVnum[self.selectedSlot]
		debug("Current switch item:", currentSwitchItem)
		
		# Check what your item actually has
		debug("Item's actual attributes:")
		for i in range(7):
			(attrType, attrValue) = player.GetItemAttribute(player.SWITCHBOT, self.selectedSlot, i)
			if attrType and attrValue:
				slot_type = "normal" if i < 5 else "rare"
				debug("  Item slot {}: type={}, value={} ({})".format(i, attrType, attrValue, slot_type))
		
		debug("=== END SERVER TEST ===")

	def SelectSwitchType(self, type, iVnum, isManual = False):
		if isManual and self.IsActiveSlot():#disable if slot is active
			self.switchTypeBtns[type]["btn"].SetUp()
			return

		for i in range(SWITCH_TYPE_MAX):
			self.switchTypeBtns[i]["btn"].SetUp()

		self.switchTypeBtns[type]["btn"].Down()
		currSwitchType = self.switchItemVnum[self.selectedSlot]
		self.switchItemVnum[self.selectedSlot] = iVnum
		normalBonusesVnums = (71084,)

		if iVnum in normalBonusesVnums:
			if self.refreshDelay is None:
				self.CheckInstantSwitchCounter()

			self.instantCheckbox.Show()
		else:
			self.instantCheckbox.Hide()

		self.__RefreshButtons()

		if isManual and currSwitchType in normalBonusesVnums and iVnum in normalBonusesVnums:
			return

		self.__RefreshAttributeRows()

		if isManual:
			for i in range(ATTR_SLOT_COUNT):
				row = self.attrDict.get(i, None)
				# if row and not row.IsShow():
				if row:
					row.OnClickClearButton(True)

		constInfo.setWindowValue("switchbot", "switchType", type)
		constInfo.setWindowValue("switchbot", "switchTypeVnum", iVnum)
		
	def SetActive(self, active):
		originalFlag = active

		if self.instantCheckbox.GetCheckStatus() and active == False:
			active = True

		if self.selectedSlot >= switchbot.SLOT_COUNT:
			return
			
		if active and self.IsActiveSlot():
			return
			
		if not active and not self.IsActiveSlot():
			return

		if active:
			if self.switchItemVnum[self.selectedSlot] <= 0:
				popup = uiCommon.PopupDialog()
				popup.SetText(uiScriptLocale.SWITCHBOT_SELECT_ITEM_FIRST)
				popup.SetAcceptEvent(self.__OnClosePopupDialog)
				popup.Open()
				self.popup = popup
				return
			
			switchCount = 0

			if self.instantCheckbox.GetCheckStatus():
				maxSwitchCount = 200000
				switchCount = max(10000, int(round(int(self.instantSlider.GetSliderPos() * maxSwitchCount) // 10000) * 10000))

			switchbot.Start(self.selectedSlot, self.switchItemVnum[self.selectedSlot], switchCount, 0 if originalFlag == True else 1)
		else:
			switchbot.Stop(self.selectedSlot)

	def __OnClosePopupDialog(self):
		self.popup = None

	def OpenSaveConfiguration(self):
		if not self.configurationSaveWindow:
			self.configurationSaveWindow = ConfigurationWindow(self)
				
		if self.configurationSaveWindow.IsShow():
			self.configurationSaveWindow.Close()
		else:
			self.configurationSaveWindow.Open()
			
	def SetItemToolTip(self, tooltipItem):
		for i in range(switchbot.SLOT_COUNT):
			self.itemTabs[i].SetItemToolTip(tooltipItem)
			
	def __AnyAttributeConfigured(self):
		for i in range(switchbot.ALTERNATIVE_COUNT):
			for j in range(ATTR_SLOT_COUNT):
				(type, value) = switchbot.GetAttribute(self.selectedSlot, i, j)
				if type and value:
					return True
				
		return False
		
	def RefreshSwitchbotWindow(self):
		self.__RefreshSwitchItemVnums()
		self.__RefreshItemSlots()
		self.__RefreshAlternatives()
		self.__RefreshAttributeRows()
		self.__RefreshButtons()
		self.__RefreshTypeButtons()

	def RefreshSwitchbotItem(self, slot):
		itemTab = self.itemTabs.get(slot, None)
		if not itemTab:
			return
			
		itemTab.RefreshItemSlot()

	def __RefreshSwitchItemVnums(self):
		for i in range(switchbot.SLOT_COUNT):
			if self.selectedSlot == i and self.switchItemVnum[i] != 0:
				continue

			switchItemVnum = switchbot.GetSwitchItemVnum(i)

			if switchItemVnum != 0:
				self.switchItemVnum[i] = switchItemVnum
		
	def __RefreshItemSlots(self):
		for i in range(switchbot.SLOT_COUNT):
			itemTab = self.itemTabs.get(i, None)
			if not itemTab:
				continue
				
			itemTab.RefreshItemSlot()
			
	def __RefreshAlternatives(self):
		if self.IsEmptySlot():
			self.alternativePanel.Hide()
		else:
			self.alternativePanel.Show()

		#if app.PREMIUM_VIP_SYSTEM:
		#	isVip = constInfo.IsVIP(player.GetName())
		#
		#	for i in range(2, switchbot.ALTERNATIVE_COUNT):
		#		if isVip:
		#			self.alternativeButtons[i].Show()
		#		else:
		#			self.alternativeButtons[i].Hide()
			


	def __RefreshAttributeRows(self):
		# availRows musi miec dlugosc rowna ATTR_SLOT_COUNT (5 normal + 2 rare = 7).
		availRows = [False] * ATTR_SLOT_COUNT
		switchItemVnum = self.switchItemVnum[self.selectedSlot]
		maxRows = ATTR_SLOT_COUNT  # Default: process all rows

		debug("switchItemVnum:", switchItemVnum)

		if switchItemVnum in (71084, 79011, 79012):
			debug("Processing normal + rare bonuses (1-7) — ALWAYS show all 7 rows")
			# Pokazuj WSZYSTKIE 7 rzedow zawsze, by gracz mogl skonfigurowac
			# docelowe atrybuty (zarowno normalne 1-5 jak i rare 6/7), niezaleznie
			# od tego co item aktualnie posiada.
			for i in range(ATTR_SLOT_COUNT):
				availRows[i] = True
			maxRows = ATTR_SLOT_COUNT
		
		elif switchItemVnum in (71052,):
			debug("Processing rare bonuses (6/7)")
			# For 6/7 bonuses - ONLY process rare bonus rows
			rareSlotCount = 0
			for i in range(player.ATTRIBUTE_SLOT_RARE_START, player.ATTRIBUTE_SLOT_RARE_END):
				(applyType, applyValue) = player.GetItemAttribute(player.SWITCHBOT, self.selectedSlot, i)
				if applyType and applyValue:
					debug("  -> Rare slot {} has bonus, enabling UI row {}".format(i, rareSlotCount))
					availRows[rareSlotCount] = True
					rareSlotCount += 1
			
			# IMPORTANT: Only process the number of UI rows that correspond to rare slots
			maxRows = rareSlotCount  # Only process 0-1 rows (or however many rare bonuses exist)
			debug("maxRows set to:", maxRows)
	
		debug("Final availRows:", availRows)
		debug("Will process rows 0 to", maxRows-1)
	
		# ONLY process the required number of rows
		for i in range(maxRows):
			row = self.attrDict.get(i, None)
			if not row:
				continue
	
			if availRows[i]:
				debug("Showing UI row", i)
				row.Show()
			else:
				debug("Hiding UI row", i)
				row.Hide()
			
			row.RefreshAttributeRow(self.selectedSlot, self.alternative, i)
		
		# Hide all remaining rows for rare bonuses
		if switchItemVnum in (71052,):
			for i in range(maxRows, ATTR_SLOT_COUNT):
				row = self.attrDict.get(i, None)
				if row:
					debug("Force hiding UI row", i, "(beyond rare bonus range)")
					row.Hide()
			
	def __RefreshButtons(self):
		if self.instantCheckbox.IsShow() and self.instantCheckbox.GetCheckStatus():
			self.instantSlider.Show()
		else:
			self.instantSlider.Hide()
		
		self.UpdateButtonsText()

		if self.IsEmptySlot() or not self.__AnyAttributeConfigured():
			self.startButton.Disable()
			self.stopButton.Disable()
			return
			
		self.startButton.Enable()
		self.stopButton.Enable()
		
		if self.IsActiveSlot():
			self.stopButton.Enable()
			self.startButton.Disable()
		else:
			self.stopButton.Disable()
			self.startButton.Enable()

		if self.instantCheckbox.IsShow() and self.instantCheckbox.GetCheckStatus():
			self.stopButton.Enable()
	
	def UpdateButtonsText(self):
		if self.instantCheckbox.IsShow() and self.instantCheckbox.GetCheckStatus():
			maxSwitchCount = 200000
			switchCount = max(10000, int(round(int(self.instantSlider.GetSliderPos() * maxSwitchCount) // 10000) * 10000))
			priceGold = switchCount // 10000 * (350000000000 if self.switchItemVnum[self.selectedSlot] == 70096 else 175000000000)
			priceCoins = switchCount // 10000 * (2 if self.switchItemVnum[self.selectedSlot] == 70096 else 1)
			self.instantSliderCount.SetText(localeInfo.NumberToMoneyString(switchCount))
			self.startButton.SetText("%s |Ed:/ymir work/ui/game/windows/money_icon.sub|e %s" % (localeInfo.SWITCHBOT_INSTANT, uiScriptLocale.NumberToKKK(int(priceGold))))
			self.stopButton.SetText("%s |Eicon/item/dm_ico.png|e %s" % (localeInfo.SWITCHBOT_INSTANT, uiScriptLocale.NumberToKKK(int(priceCoins))))
		else:
			self.startButton.SetText(localeInfo.SWITCHBOT_START)
			self.stopButton.SetText(localeInfo.SWITCHBOT_STOP)
	
	def __RefreshTypeButtons(self):
		for iHide in range(SWITCH_TYPE_MAX):
			self.switchTypeBtns[iHide]["btn"].SetUp()
			self.switchTypeBtns[iHide]["btn"].Hide()
			
		itemVnum = player.GetItemIndex(player.SWITCHBOT, self.selectedSlot)
		if not itemVnum:
			return
			
		item.SelectItem(itemVnum)
		itemType = item.GetItemType()
		itemSubType = item.GetItemSubType()
		
		availTypes = []
		
		if itemType in (item.WEAPON, item.ARMOR):
			availTypes.append("normal")  # Add normal bonuses
			availTypes.append("rare")    # Add rare bonuses
		elif itemType == item.BELT:
			availTypes.append("belt")
		elif itemType == item.ARMOR_GLOVE:
			availTypes.append("gloves")
		
		availItemVnums = []
		for at in range(len(availTypes)):
			if availTypes[at] in SWITCH_TYPE_LIST_BY_ITEM:
				availItemVnums += SWITCH_TYPE_LIST_BY_ITEM[availTypes[at]]
		
		if self.switchItemVnum[self.selectedSlot] != 0 and self.switchItemVnum[self.selectedSlot] not in availItemVnums:
			self.switchItemVnum[self.selectedSlot] = 0
			
		i = 0
		for aviv in range(len(availItemVnums)):
			currItemVnum = availItemVnums[aviv]
			self.switchTypeBtns[i]["btn"].SetToolTipText(uiScriptLocale.FindItemName(currItemVnum))
			self.switchTypeBtns[i]["btn"].SetEvent(lambda arg = i, iVnum = currItemVnum : self.SelectSwitchType(arg, iVnum, True))
			self.switchTypeBtns[i]["btn"].Show()
			self.switchTypeBtns[i]["icon"].LoadImage("icon/item/%s" % SWITCH_ICON_LIST[currItemVnum])
			self.switchTypeBtns[i]["icon"].SetScale(0.6, 0.6)
			self.switchTypeBtns[i]["icon"].SetSize(0,0)
			if (self.switchItemVnum[self.selectedSlot] == 0 and i == 0) or (self.switchItemVnum[self.selectedSlot] == currItemVnum):
				self.SelectSwitchType(i, currItemVnum)
			i += 1
		
	def __OnAttributeUpdate(self):
		self.__RefreshButtons()

	def __OnSearchAttribute(self, attrIdx):
		self.TestSearchDebug()
		if self.attributeSearchWindow is None:
			width = 260
			height = 260
	
			self.attributeSearchWindow = SearchListWindow()
			self.attributeSearchWindow.MakeWindow(width, height)
			self.attributeSearchWindow.board.SetTitleName(localeInfo.SWITCHBOT_SELECT_ATTR)
			self.attributeSearchWindow.SetAcceptArgsType("KEY_VALUE")
			self.attributeSearchWindow.SetAcceptEvent(ui.__mem_func__(self.__OnAcceptSearch))
			self.attributeSearchWindow.SetCancelEvent(ui.__mem_func__(self.__OnCancelSearch))
	
			(mouseX, mouseY) = wndMgr.GetMousePosition()
	
			if mouseX + width // 2 > wndMgr.GetScreenWidth():
				xPos = wndMgr.GetScreenWidth() - width
			elif mouseX - width // 2 < 0:
				xPos = 0
			else:
				xPos = mouseX - width // 2
				
			if mouseY + height // 2 > wndMgr.GetScreenHeight():
				yPos = wndMgr.GetScreenHeight() - height
			elif mouseY - height // 2 < 0:
				yPos = 0
			else:
				yPos = mouseY - height // 2
	
			self.attributeSearchWindow.SetPosition(xPos, yPos)
	
		self.attributeSearchWindow.RemoveAllItems()
		self.attrSearchIdx = attrIdx
	
		defaultAttributes = []
		selectedAttributes = [switchbot.GetAttribute(self.selectedSlot, self.alternative, attrIndex)[0] for attrIndex in range(ATTR_SLOT_COUNT)]
		switchItemVnum = self.switchItemVnum[self.selectedSlot]
		attributes = switchbot.GetAttributesForSet(self.selectedSlot, self.switchItemVnum[self.selectedSlot])
	
		debug("=== SEARCH ATTRIBUTE DEBUG ===")
		debug("attrIdx:", attrIdx)
		debug("switchItemVnum:", switchItemVnum)
		debug("selectedAttributes:", selectedAttributes)
		debug("Total attributes from server:", len(attributes))
	
		# Handle normal switching items (71084) - for normal bonuses (1-5)
		if self.switchItemVnum[self.selectedSlot] in (71084,):
			debug("Processing 71084 path - NORMAL BONUSES (1-5)")
			
			# Get default attributes (fixed attributes on item)
			itemVnum = player.GetItemIndex(player.SWITCHBOT, self.selectedSlot)
			item.SelectItem(itemVnum)
			for i in range(item.ITEM_APPLY_MAX_NUM):
				(affectType, affectValue) = item.GetAffect(i)
				if affectType:
					defaultAttributes.append(affectType)
					debug("Default attribute: type={}".format(affectType))
	
			# Add special addon bonuses (skill damage, normal hit damage)
			firstAttrType = player.GetItemAttribute(player.SWITCHBOT, self.selectedSlot, 0)[0]
			if firstAttrType in ADDON_TYPES.keys():
				debug("Adding addon bonuses")
				for addonType, maxValue in ADDON_TYPES.items():
					if addonType in selectedAttributes:
						debug("Skipping addon {} - already selected".format(addonType))
						continue
	
					affectString = GetAffectString(addonType, maxValue)
					if not affectString:
						continue
	
					debug("Adding addon attribute: type={}".format(addonType))
					self.attributeSearchWindow.AppendItem(addonType, affectString)
	
			# Add normal attributes that can be switched
			for (type, value) in attributes:
				debug("Checking normal attribute: type={}, value={}".format(type, value))
				
				if type in selectedAttributes:
					debug("Skipping - already selected in switchbot")
					continue
					
				if type in defaultAttributes:
					debug("Skipping - default attribute on item")
					continue
				
				affectString = GetAffectString(type, value)
				if not affectString:
					debug("No affectString, skipping")
					continue
					
				debug("Adding normal attribute to search window: type={}".format(type))
				self.attributeSearchWindow.AppendItem(type, affectString)
	
		# Handle rare switching items (71052) - for rare bonuses (6/7) ONLY
		elif self.switchItemVnum[self.selectedSlot] in (71052,):
			debug("Processing 71052 path - RARE BONUSES ONLY (6/7)")
			
			# Get ALL existing attributes to exclude them
			existingAllAttrs = []
			
			# Exclude normal bonuses (slots 0-4)
			for i in range(0, player.ATTRIBUTE_SLOT_NORM_NUM):
				(attrType, attrValue) = player.GetItemAttribute(player.SWITCHBOT, self.selectedSlot, i)
				if attrType and attrValue:
					existingAllAttrs.append(attrType)
					debug("Excluding normal attr from slot {}: type={}".format(i, attrType))
			
			# Exclude existing rare bonuses (slots 5-6)
			for i in range(player.ATTRIBUTE_SLOT_RARE_START, player.ATTRIBUTE_SLOT_RARE_END):
				(attrType, attrValue) = player.GetItemAttribute(player.SWITCHBOT, self.selectedSlot, i)
				if attrType and attrValue:
					existingAllAttrs.append(attrType)
					debug("Excluding rare attr from slot {}: type={}".format(i, attrType))
			
			debug("All existing attributes to exclude:", existingAllAttrs)
			
			# Only show attributes that don't exist ANYWHERE on the item
			addedCount = 0
			for (type, value) in attributes:
				
				if type in selectedAttributes:
					debug("Skipping - already selected in switchbot")
					continue
					
				if type in existingAllAttrs:
					continue
	
				affectString = GetAffectString(type, value)
				if not affectString:
					debug("No affectString, skipping")
					continue
				
				self.attributeSearchWindow.AppendItem(type, affectString)
				addedCount += 1
			
			debug("Added {} rare attributes to search".format(addedCount))
	
		else:
			# Handle belt/glove bonuses (79011, 79012)
			debug("Processing belt/glove path")
			for (type, value) in attributes:
				if type in selectedAttributes:
					continue
	
				affectString = GetAffectString(type, value)
				if not affectString:
					continue
					
				self.attributeSearchWindow.AppendItem(type, affectString)
	
		debug("=== END SEARCH ATTRIBUTE DEBUG ===")
	
		self.attributeSearchWindow.SetTop()
		self.attributeSearchWindow.Open()
		
	def __OnAcceptSearch(self, key, value):
		if self.attrSearchIdx < 0 or self.attrSearchIdx >= ATTR_SLOT_COUNT:
			return
			
		attrRow = self.attrDict.get(self.attrSearchIdx, None)
		if not attrRow:
			return

		maxValue = None
		if self.switchItemVnum[self.selectedSlot] in (71084,):
			maxValue = ADDON_TYPES.get(key, 0)

		if not maxValue:
			maxValue = switchbot.GetAttributeMaxValue(self.selectedSlot, key, self.switchItemVnum[self.selectedSlot])
			
		attrRow.SetAttribute(value, maxValue)
		switchbot.SetAttribute(self.selectedSlot, self.alternative, self.attrSearchIdx, key, maxValue)
		
		self.__RefreshButtons()
		
	def SetSavedAttribute(self, slot, alternative, attrIndex, attrType, attrValue):
		if attrIndex < 0 or attrIndex >= ATTR_SLOT_COUNT:
			return
			
		attrRow = self.attrDict.get(attrIndex, None)
		if not attrRow:
			return
		
		if not attrRow.IsShow():
			return
			
		if slot >= switchbot.SLOT_COUNT:
			return
			
		if switchbot.IsActive(slot):
			return
			
		var = switchbot.GetAttributesForSet(slot, self.switchItemVnum[self.selectedSlot])
		attributes = [var[i][0] for i in range(len(var))]
		
		firstAttrType = player.GetItemAttribute(player.SWITCHBOT, slot, 0)[0]
		if firstAttrType in ADDON_TYPES.keys():
			for addon in ADDON_TYPES.keys():
				attributes.append(addon)
		
		if not attrType in attributes:
			switchbot.SetAttribute(slot, alternative, attrIndex, 0, 0)
		else:
			switchbot.SetAttribute(slot, alternative, attrIndex, attrType, attrValue)
		
	def IsEmptySlot(self):
		slot = self.itemTabs.get(self.selectedSlot, None)
		if not slot:
			return True
			
		return slot.IsEmpty()
		
	def IsActiveSlot(self):
		slot = self.itemTabs.get(self.selectedSlot, None)
		if not slot:
			return False
			
		return slot.IsActive()
		
	def GetSlotAttributeCount(self):
		slot = self.itemTabs.get(self.selectedSlot, None)
		if not slot:
			return 0
			
		return slot.GetAttributeCount()
		
	def OnMoveWindow(self, x, y):
		if self.configurationSaveWindow:
			self.configurationSaveWindow.AdjustPosition()
		
	def __OnCancelSearch(self):
		pass
		
	def OnPressEscapeKey(self):
		self.Close()
		return True

	def OnMoveWindow(self, x, y):
		constInfo.setWindowValue("switchbot", "pos", [x, y])

	def OnUpdate(self):
		if self.refreshDelay > 0 and self.refreshDelay + 2.0 < app.GetTime():
			self.refreshDelay = None
			self.CheckInstantSwitchCounter()

		
		if self.instantSwitchData["cooldownEnd"] is not None and self.instantCheckbox.IsShow() and self.instantCheckbox.IsIn():
			timeLeft = max(0, self.instantSwitchData["cooldownEnd"] - app.GetGlobalTimeStamp())
			self.instantCheckbox.SetToolTipText("%s, %s: %s" % (localeInfo.SWITCHBOT_INSTANT, uiScriptLocale.DUNGEON_INFO_COOLDOWN, localeInfo.FormatTime(timeLeft)))

	def CheckInstantSwitchCounter(self):
		if self.instantSwitchData["cooldownEnd"] is None:
			self.refreshDelay = None
			net.SendChatPacket("/switchbot_get_instant_counter")

	def UpdateInstantSwitchCounter(self, cooldownEnd):
		self.instantSwitchData["cooldownEnd"] = int(cooldownEnd)

	def OnInstantCheckboxChange(self, checkType, flag):
		#if app.PREMIUM_VIP_SYSTEM and not constInfo.IsVIP(player.GetName()):
		#	self.instantCheckbox.SetCheckStatus(False)
		#	chat.AppendChat(chat.CHAT_TYPE_INFO, uiScriptLocale.ERROR_VIP_NEEDED)
		#	return

		self.__RefreshButtons()

class SearchListWindow(ui.ScriptWindow):
	class SearchListItem(ui.Window):
		LIST_ITEM_HEIGHT = 12
	
		def __init__(self, key, value):
			ui.Window.__init__(self, "UI")
			
			self.key = key
			self.value = value
			self.isDown = False
			self.onClickEvent = None	

			self.textLine = ui.TextLine()
			self.textLine.AddFlag("not_pick")
			self.textLine.SetParent(self)
			self.textLine.SetVerticalAlignCenter()
			self.textLine.SetWindowVerticalAlignCenter()
			self.textLine.SetPosition(10, -1)
			self.textLine.SetText(str(value))
			self.textLine.UpdateRect()
			self.textLine.Show()
				
		def __del__(self):
			ui.Window.__del__(self)
		
		def Destroy(self):
			self.key = None
			self.value = None
			self.isDown = None
			self.onClickEvent = None
			self.textLine = None
			
		def OnMouseLeftButtonUp(self):
			if not self.isDown:
				self.__OnClick()
				self.Down()
				
		def OnRender(self):
			if self.IsIn() or self.isDown:
				self.RenderHoverOrSelected()
				
		def RenderHoverOrSelected(self):
			x, y = self.GetGlobalPosition()
			grp.SetColor(grp.GenerateColor(0.0, 0.0, 0.7, 0.7))
			grp.RenderBar(x, y, self.GetWidth(), self.GetHeight())
				
		def SetUp(self):
			self.isDown = False
			
		def Down(self):
			self.isDown = True
			
		def IsDown(self):
			return self.isDown
			
		def GetKey(self):
			return self.key
			
		def GetValue(self):
			return self.value
			
		def GetText(self):	
			return self.textLine.GetText()
			
		def MatchText(self, text):
			return text in self.GetText()
			
		def SetOnClickEvent(self, event):
			self.onClickEvent = ui.__mem_func__(event)
			
		def __OnClick(self):
			if self.onClickEvent:
				self.onClickEvent(self.key, self.value)
			
	def __init__(self):
		ui.ScriptWindow.__init__(self, "UI")
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "uiscript/emptyboard.py")

			self.board = self.GetChild("board")
			self.board.SetCloseEvent(ui.__mem_func__(self.Close))
			self.__Initialize()
		except:
			import exception
			exception.Abort("SearchListWindow.init")

	def __Initialize(self):
		self.resultLimit = 0
		self.textLenMin = 0
		self.listItems = []
		self.acceptEvent = None
		self.acceptArgsType = "VALUE"
		self.cancelEvent = None

	def __del__(self):
		ui.ScriptWindow.__del__(self)
	
	def Destroy(self):
		self.ClearDictionary()
		self.board = None
		self.resultLimit = None
		self.textLenMin = None
		self.listItems = None
		self.acceptEvent = None
		self.acceptArgsType = None
		self.cancelEvent = None
		self.searchInput = None
		self.searchEditLine = None
		self.scrollBar = None
		self.container = None
		self.listBox = None
		self.acceptButton = None
		self.cancelButton = None
		
	def MakeWindow(self, width, height, maxInput = 50):
		self.SetSize(width, height)
		self.board.SetSize(width, height)

		self.searchInput = ui.ThinBoardCircle()
		self.searchInput.SetParent(self.board)
		self.searchInput.SetSize(width - (BORDER_SPACE*2), INPUT_HEIGHT)
		self.searchInput.SetPosition(BORDER_SPACE, BORDER_SPACE_TOP)
		self.searchInput.Show()
		
		self.searchEditLine = ui.EditLine()
		self.searchEditLine.SetParent(self.searchInput)
		self.searchEditLine.SetPosition(10, 8)
		self.searchEditLine.SetSize(self.searchInput.GetWidth() - 20, self.searchInput.GetHeight() - 16)
		self.searchEditLine.SetMax(maxInput)
		self.searchEditLine.SetReturnEvent(ui.__mem_func__(self.__OnAccept))
		self.searchEditLine.SetEscapeEvent(ui.__mem_func__(self.Close))
		self.searchEditLine.OnIMEUpdate = self.__OnSearchIMEUpdate
		self.searchEditLine.Show()
		
		containerHeight = height - (BORDER_SPACE_TOP + INPUT_HEIGHT + 30)
		
		self.scrollBar = ui.ScrollBar()
		self.scrollBar.SetParent(self.board)
		self.scrollBar.SetWindowHorizontalAlignRight()
		self.scrollBar.SetPosition(23, BORDER_SPACE_TOP + INPUT_HEIGHT + 2)
		self.scrollBar.SetScrollBarSize(containerHeight - 4)	
		
		self.container = ui.ThinBoardCircle()
		self.container.SetParent(self.board)
		self.container.SetPosition(BORDER_SPACE, BORDER_SPACE_TOP + INPUT_HEIGHT)
		self.container.SetSize(width - (BORDER_SPACE*2), containerHeight)
		self.container.Show()
		
		listBoxHeight = self.container.GetHeight()
		listBoxWidth = self.container.GetWidth()
		
		self.listBox = ui.ListBoxEx()
		self.listBox.SetParent(self.container)
		self.listBox.SetPosition(2, 2)
		self.listBox.SetSize(listBoxWidth, listBoxHeight)
		self.listBox.SetItemStep(self.SearchListItem.LIST_ITEM_HEIGHT)
		self.listBox.SetViewItemCount(self.__GetViewItemCount())
		self.listBox.SetItemSize(listBoxWidth, self.SearchListItem.LIST_ITEM_HEIGHT)
		self.listBox.SetScrollBar(self.scrollBar)
		self.listBox.Show()
		
		buttonWidth = width // 2 - 20
		
		self.acceptButton = ui.Button()
		self.acceptButton.SetParent(self.board)
		self.acceptButton.SetUpVisual("d:/ymir work/ui/public/large_button_01.sub")
		self.acceptButton.SetOverVisual("d:/ymir work/ui/public/large_button_02.sub")
		self.acceptButton.SetDownVisual("d:/ymir work/ui/public/large_button_03.sub")
		self.acceptButton.SetDisableVisual("d:/ymir work/ui/public/large_button_03.sub")
		self.acceptButton.SetWindowVerticalAlignBottom()
		self.acceptButton.SetWindowHorizontalAlignCenter()
		self.acceptButton.SetPosition(-buttonWidth // 2 - 5, 29)
		self.acceptButton.SetText(localeInfo.UI_ACCEPT)
		self.acceptButton.SetEvent(ui.__mem_func__(self.__OnAccept))
		self.acceptButton.Show()
		
		self.cancelButton = ui.Button()
		self.cancelButton.SetParent(self.board)
		self.cancelButton.SetUpVisual("d:/ymir work/ui/public/large_button_01.sub")
		self.cancelButton.SetOverVisual("d:/ymir work/ui/public/large_button_02.sub")
		self.cancelButton.SetDownVisual("d:/ymir work/ui/public/large_button_03.sub")
		self.cancelButton.SetDisableVisual("d:/ymir work/ui/public/large_button_03.sub")
		self.cancelButton.SetWindowVerticalAlignBottom()
		self.cancelButton.SetWindowHorizontalAlignCenter()
		self.cancelButton.SetPosition(buttonWidth // 2 - 5, 29)
		self.cancelButton.SetText(localeInfo.UI_CANCEL)
		self.cancelButton.SetEvent(ui.__mem_func__(self.__OnCancel))
		self.cancelButton.Show()
		
		self.__AdjustScrollbar()
		
	def __OnSearchIMEUpdate(self):
		ui.EditLine.OnIMEUpdate(self.searchEditLine)
		self.__RefreshListBox()
		
	def __GetViewItemCount(self):
		return self.container.GetHeight() // self.SearchListItem.LIST_ITEM_HEIGHT
		
	def __AdjustScrollbar(self):
		if len(self.listBox.GetItems()) > self.__GetViewItemCount():
			listBoxWidth = self.GetWidth() - (BORDER_SPACE*2) - 20
			self.container.SetSize(listBoxWidth, self.container.GetHeight())
			self.listBox.SetSize(listBoxWidth - 4, self.listBox.GetHeight() - 4)
			self.listBox.SetItemSize(listBoxWidth - 4, self.SearchListItem.LIST_ITEM_HEIGHT)
			attachmentCount = len(self.listBox.GetItems())
			scrollBarHeight = min(float(self.__GetViewItemCount()) / float(attachmentCount), 1.0)
			self.scrollBar.SetScrollStep(float(3) / float(attachmentCount - self.__GetViewItemCount()))
			self.scrollBar.SetMiddleBarSize(scrollBarHeight)
			self.scrollBar.Show()
		else:
			listBoxWidth = self.GetWidth() - (BORDER_SPACE*2)
			self.container.SetSize(listBoxWidth, self.container.GetHeight())
			self.listBox.SetSize(listBoxWidth - 4, self.listBox.GetHeight() - 4)
			self.listBox.SetItemSize(listBoxWidth - 4, self.SearchListItem.LIST_ITEM_HEIGHT)
			self.scrollBar.Hide()

	#if app.MOUSE_WHEEL:
	#	def OnRunMouseWheel(self, nLen):
	#		if nLen > 0:
	#			self.scrollBar.OnUp()
	#		else:
	#			self.scrollBar.OnDown()
		
	def RemoveAllItems(self):
		self.listItems = []
		self.listBox.RemoveAllItems()		
		
	def AppendItem(self, key, value = "", sorting = 0):			
		if not value:
			value = key
			
		self.listItems.append({ "key": key, "value": value, "item": None, "sorting": sorting, "lowerValueWithoutDiacritic": uiScriptLocale.RemoveDiacritic(value).lower()})
	
	def SortAppendedItems(self, reversed = False):
		self.listItems = sorted(self.listItems, key=lambda x: str(x['sorting']).lower(), reverse=reversed)
		self.__RefreshListBox()

	def SetResultLimit(self, limit):
		self.resultLimit = limit

	def SetTextLenMin(self, limit):
		self.textLenMin = limit
		
	def __RefreshListBox(self):
		self.listBox.RemoveAllItems()
		text = self.searchEditLine.GetText()

		if self.textLenMin > 0 and len(text) < self.textLenMin:
			return

		resCount = 0
		searchText = uiScriptLocale.RemoveDiacritic(text).lower()

		for val in self.listItems:
			listItem = val["item"]

			if not searchText or searchText in val["lowerValueWithoutDiacritic"]:
				listItem = self.SearchListItem(val["key"], val["value"])
				listItem.SetOnClickEvent(self.__OnClickListItem)
				self.listBox.AppendItem(listItem)
				resCount += 1
			else:
				del listItem
			
			if self.resultLimit > 0 and resCount >= self.resultLimit:
				break

		self.__AdjustScrollbar()
			
	def GetSelectedItem(self):
		for listItem in self.listBox.GetItems():
			if listItem.IsDown():
				return listItem
				
		return None
		
	def SetCancelEvent(self, event):
		self.cancelEvent = event
		
	def SetAcceptEvent(self, event):
		self.acceptEvent = event
		
	def SetAcceptArgsType(self, type):
		self.acceptArgsType = type
		
	def __OnClickListItem(self, key, value):
		curItem = self.GetSelectedItem()
		if curItem:
			curItem.SetUp()
				
	def __OnCancel(self):
		if self.cancelEvent:
			self.cancelEvent()
			
		self.Close()
			
	def __OnAccept(self):
		selItem = self.GetSelectedItem()

		if not selItem:
			# if len(self.listBox.GetItems()) == 1:
			selItem = self.listBox.GetItems()[0]
			# else:
			# 	return
	
		if self.acceptEvent:
			if self.acceptArgsType == "VALUES":
				self.acceptEvent(selItem.GetValue())
			elif self.acceptArgsType == "KEY":
				self.acceptEvent(selItem.GetKey())
			elif self.acceptArgsType == "KEY_VALUE":
				self.acceptEvent(selItem.GetKey(), selItem.GetValue())
			
		self.Close()
		
	def OnPressEscapeKey(self):
		self.Close()
		return True
		
	def Open(self):
		self.__RefreshListBox()
		self.Show()
		self.searchEditLine.SetFocus()
		
	def Close(self):
		self.searchEditLine.SetText("")
		self.searchEditLine.KillFocus()
		self.Hide()
	
	def OnMoveWindow(self, x, y):
		self.SetTop()

class ConfigurationWindow(ui.Window):
	BOARD_WIDTH = 250
	wndSwitchbot = None
	nameInput = None
	valueEditLine = None
	dict = {}
	listItems = {}

	class ConfigurationLine(ui.Window):
		LIST_ITEM_HEIGHT = 26
	
		id = 0
		name = ""
	
		loadEvent = None
		deleteEvent = None
	
		def __init__(self, width):
			ui.Window.__init__(self, "UI", "ConfigurationLine")
			
			self.SetSize(width, 26)
			
			self.nameTextLine = ui.TextLine()
			self.nameTextLine.SetParent(self)
			self.nameTextLine.SetVerticalAlignCenter()
			self.nameTextLine.SetWindowVerticalAlignCenter()
			self.nameTextLine.SetPosition(5, -1)
			self.nameTextLine.Show()
				
			self.loadButton = ui.Button()
			self.loadButton.SetParent(self)
			self.loadButton.SetUpVisual("d:/ymir work/ui/switchbot/load_attr_01.sub")
			self.loadButton.SetOverVisual("d:/ymir work/ui/switchbot/load_attr_02.sub")
			self.loadButton.SetDownVisual("d:/ymir work/ui/switchbot/load_attr_03.sub")
			self.loadButton.SetDisableVisual("d:/ymir work/ui/switchbot/load_attr_03.sub")
			self.loadButton.SetWindowHorizontalAlignRight()
			self.loadButton.SetWindowVerticalAlignCenter()
			self.loadButton.SetPosition(24 * 2 + 2, 1)
			self.loadButton.SetToolTipText(localeInfo.SWITCHBOT_LOAD_CONFIGURATION)
			self.loadButton.SetEvent(ui.__mem_func__(self.__OnClickLoadButton))
			self.loadButton.Show()
			
			self.deleteButton = ui.Button()
			self.deleteButton.SetParent(self)
			self.deleteButton.SetUpVisual("d:/ymir work/ui/switchbot/delete_attr_01.sub")
			self.deleteButton.SetOverVisual("d:/ymir work/ui/switchbot/delete_attr_02.sub")
			self.deleteButton.SetDownVisual("d:/ymir work/ui/switchbot/delete_attr_03.sub")
			self.deleteButton.SetDisableVisual("d:/ymir work/ui/switchbot/delete_attr_03.sub")
			self.deleteButton.SetWindowHorizontalAlignRight()
			self.deleteButton.SetWindowVerticalAlignCenter()
			self.deleteButton.SetPosition(24 + 2, 1)
			self.deleteButton.SetToolTipText(localeInfo.SWITCHBOT_CLEAR_CONFIGURATION)
			self.deleteButton.SetEvent(ui.__mem_func__(self.__OnClickDeleteButton))
			self.deleteButton.Show()
			
		def __del__(self):
			ui.Window.__del__(self)
		
		def Destroy(self):
			self.nameTextLine = None
			self.loadButton = None
			self.deleteButton = None
			self.id = None
			self.name = None
			self.loadEvent = None
			self.deleteEvent = None
			
		def Load(self, id, name):
			self.id = id
			self.name = name
			self.nameTextLine.SetText(name)
			
		def SetLoadEvent(self, event):
			self.loadEvent = event
			
		def SetDeleteEvent(self, event):
			self.deleteEvent = event
			
		def __OnClickLoadButton(self):
			if self.loadEvent:
				self.loadEvent(self.id)
			
		def __OnClickDeleteButton(self):
			if self.deleteEvent:
				self.deleteEvent(self.id)
	
	def __init__(self, wndSwitchbot=None):
		ui.Window.__init__(self)
		
		if not wndSwitchbot:
			import exception
			exception.Abort("ConfigurationWindow.__init__ Cannot initialize without binding to Switchbot window.")
			
		self.wndSwitchbot = wndSwitchbot
		
		self.__LoadWindow()
		
	def __del__(self):
		ui.Window.__del__(self)
		
	def Destroy(self):
		self.wndSwitchbot = None
		self.saveButton = None
		self.nameInput = None
		self.nameEditLine = None
		self.scrollBar = None
		self.container = None
		self.listBox = None
		self.dict = None

	def __LoadWindow(self):
		self.AddFlag("movable")
		self.AddFlag("float")

		self.board = ui.BoardWithTitleBar()
		self.board.SetParent(self)
		self.board.SetPosition(0, 0)
		self.board.AddFlag("attach")
		self.board.HideDecoration()

		self.SetSize(self.BOARD_WIDTH, BOARD_HEIGHT)
		self.board.SetSize(self.GetWidth(), self.GetHeight())
		self.board.SetCloseEvent(ui.__mem_func__(self.Close))
		self.board.SetTitleName(localeInfo.SWITCHBOT_CONFIGURATION_TITLE)
		self.board.Show()
	
		self.saveButton = ui.Button()
		self.saveButton.SetParent(self)
		self.saveButton.SetUpVisual("d:/ymir work/ui/switchbot/btn_small_01.sub")
		self.saveButton.SetOverVisual("d:/ymir work/ui/switchbot/btn_small_02.sub")
		self.saveButton.SetDownVisual("d:/ymir work/ui/switchbot/btn_small_03.sub")
		self.saveButton.SetDisableVisual("d:/ymir work/ui/switchbot/btn_small_01.sub")
		self.saveButton.SetWindowHorizontalAlignRight()
		self.saveButton.SetPosition(self.saveButton.GetWidth() + BORDER_SPACE, BORDER_SPACE_TOP + 3)
		self.saveButton.SetText(localeInfo.SWITCHBOT_SAVE)
		self.saveButton.SetEvent(ui.__mem_func__(self.__OnSave))
		self.saveButton.Show()
	
		self.nameInput = ui.ThinBoardCircle()
		self.nameInput.SetParent(self)
		self.nameInput.SetSize(self.BOARD_WIDTH - (BORDER_SPACE * 2) - self.saveButton.GetWidth() - 3, INPUT_HEIGHT)
		self.nameInput.SetPosition(BORDER_SPACE, BORDER_SPACE_TOP)
		self.nameInput.Show()
		
		self.nameEditLine = ui.EditLine()
		self.nameEditLine.SetParent(self.nameInput)
		self.nameEditLine.SetSize(self.nameInput.GetWidth() - 20, 18)
		self.nameEditLine.SetMax(32)
		self.nameEditLine.SetPosition(10, 7)
		self.nameEditLine.Show()
		self.nameEditLine.SetEscapeEvent(ui.__mem_func__(self.Close))

		height = BOARD_HEIGHT - BORDER_SPACE_TOP - INPUT_HEIGHT - BORDER_SPACE
		
		self.scrollBar = ui.ScrollBar()
		self.scrollBar.SetParent(self)
		self.scrollBar.SetWindowHorizontalAlignRight()
		self.scrollBar.SetPosition(23, BORDER_SPACE_TOP + INPUT_HEIGHT + 2)
		self.scrollBar.SetScrollBarSize(height - 4)	
		
		self.container = ui.ThinBoardCircle()
		self.container.SetParent(self)
		self.container.SetPosition(BORDER_SPACE, BORDER_SPACE_TOP + INPUT_HEIGHT)
		self.container.SetSize(BOARD_WIDTH - (BORDER_SPACE*2), height)
		self.container.Show()
		
		listBoxHeight = self.container.GetHeight()
		listBoxWidth = self.container.GetWidth()
		
		self.listBox = ui.ListBoxEx()
		self.listBox.SetParent(self.container)
		self.listBox.SetPosition(2, 2)
		self.listBox.SetSize(listBoxWidth, listBoxHeight)
		self.listBox.SetItemStep(self.ConfigurationLine.LIST_ITEM_HEIGHT + 1)
		self.listBox.SetViewItemCount(self.__GetViewItemCount())
		self.listBox.SetItemSize(listBoxWidth, self.ConfigurationLine.LIST_ITEM_HEIGHT)
		self.listBox.SetScrollBar(self.scrollBar)
		self.listBox.Show()
		
		self.__AdjustScrollbar()
		
	def LoadConfigurations(self):
		try:
			f = io.open(SAVES_FILE_PATH, 'r', encoding='utf-8')
			self.dict = json.load(f)
			f.close()
		except IOError:
			self.dict = {}	
		
		self.listBox.RemoveAllItems()
			
		lineWidth = self.listBox.GetWidth()
		if len(self.dict) > self.__GetViewItemCount():	
			lineWidth -= 20
			
		self.__AdjustScrollbar()
			
		for key in self.dict.keys():
			config = self.dict.get(key, None)
			if not config:
				continue
				
			line = self.ConfigurationLine(lineWidth)
			line.Load(key, config["name"])
			line.SetLoadEvent(ui.__mem_func__(self.__OnApplyConfiguration))
			line.SetDeleteEvent(ui.__mem_func__(self.__OnDeleteConfiguration))
			self.listBox.AppendItem(line)
			
			self.listItems[key] = line
			
	def SaveConfigurations(self):
		with io.open(SAVES_FILE_PATH, 'w', encoding='utf-8') as f:
			f.write(json.dumps(self.dict))
			
	def __OnApplyConfiguration(self, key):
		config = self.dict.get(key, None)
		if not config:
			return
			
		if not self.wndSwitchbot:
			return
			
		selectedSlot = self.wndSwitchbot.GetSelectedSlot()			
		for alternativeIdx in range(len(config["alternatives"])):
			alternative = config["alternatives"][alternativeIdx]
			for attrIdx in range(len(alternative)):
				(attrType, attrValue) = alternative[attrIdx]
				self.wndSwitchbot.SetSavedAttribute(selectedSlot, alternativeIdx, attrIdx, attrType, attrValue)

		self.wndSwitchbot.RefreshSwitchbotWindow()
		
	def __OnDeleteConfiguration(self, key):
		config = self.dict.get(key, None)
		if not config:
			return
			
		del self.listItems[key]
		del self.dict[key]
		self.SaveConfigurations()
		self.LoadConfigurations()
			
	def Open(self):
		self.Show()
		self.LoadConfigurations()
		self.AdjustPosition()
		self.SetTop()
	
	def Close(self):
		self.Hide()
		
	def AdjustPosition(self):
		if not self.wndSwitchbot:
			return 
			
		(x, y) = self.wndSwitchbot.GetGlobalPosition()
		self.SetPosition(x - self.GetWidth(), y)
		
	def __GetViewItemCount(self):
		return self.container.GetHeight() // (self.ConfigurationLine.LIST_ITEM_HEIGHT + 1)
		
	def __AdjustScrollbar(self):
		if len(self.dict) > self.__GetViewItemCount():
			listBoxWidth = self.GetWidth() - (BORDER_SPACE*2) - 20
			self.container.SetSize(listBoxWidth, self.container.GetHeight())
			self.listBox.SetSize(listBoxWidth - 4, self.listBox.GetHeight() - 4)
			self.listBox.SetItemSize(listBoxWidth - 4, self.ConfigurationLine.LIST_ITEM_HEIGHT)
			attachmentCount = len(self.dict)
			scrollBarHeight = min(float(self.__GetViewItemCount()) / float(attachmentCount), 1.0)
			self.scrollBar.SetMiddleBarSize(scrollBarHeight)
			self.scrollBar.Show()
		else:
			listBoxWidth = self.GetWidth() - (BORDER_SPACE*2)
			self.container.SetSize(listBoxWidth, self.container.GetHeight())
			self.listBox.SetSize(listBoxWidth - 4, self.listBox.GetHeight() - 4)
			self.listBox.SetItemSize(listBoxWidth - 4, self.ConfigurationLine.LIST_ITEM_HEIGHT)
			self.scrollBar.Hide()

	def OnPressEscapeKey(self):
		self.Close()
		return True
		
	def __GetNewKey(self):
		key = 0
		while key in self.dict:
			key += 1
			
		return key
		
	def __BuildDict(self, slot, name):	
		key = self.__GetNewKey()
		alternatives = []
		for alternative in range(switchbot.ALTERNATIVE_COUNT):
			attributes = [switchbot.GetAttribute(slot, alternative, i) for i in range(player.ATTRIBUTE_SLOT_MAX_NUM)]
			alternatives.append(attributes)
		
		new_dict = {
			"name" : name,
			"alternatives" : alternatives,
		}
		
		return (key, new_dict)
		
	def __OnSave(self):
		if not self.wndSwitchbot:
			return
			
		selectedSlot = self.wndSwitchbot.GetSelectedSlot()
		name = self.nameEditLine.GetText()
		
		if not name:
			return
		
		(key, new_dict) = self.__BuildDict(selectedSlot, name)
		self.dict[key] = new_dict
		
		self.nameEditLine.SetText("")
		
		self.SaveConfigurations()
		self.LoadConfigurations()
		
