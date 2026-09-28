import ui
import net
import grp
import snd
import item
import acce
import player
import uiToolTip
import localeInfo
import uiInventory
import mouseModule
import uiScriptLocale
import math
import constInfo
import renderTarget
import app

MOUNT_BONUS_INFO = (
	(	localeInfo.MOUNT_TOOLTIP_MAX_HP,						( 0, 250, 500, 750, 1000, 1000, 1250, 1500, 1750, 2000, 2000, 2250, 2500, 2750, 3000, 3000, 3250, 3500, 3750, 4000, 4250, 4500, 4750, 5000, 5000, 5250, 5500, 5750, 6000, 6000, 6250, 6500, 6750, 7000, 7000, 7250, 7500, 7750, 8000, 8000, 8250, 8500, 8750, 9000, 9000, 9250, 9500, 9750, 10000, 10000, 10250, 10500, 10750, 11000, 11000, 11250, 11500, 11750, 12000, 12000, 12250, 12500, 12750, 13000, 13000, 13250, 13500, 13750, 14000, 14000, 14250, 14500, 14750, 15000, 15000, 15250, 15500, 15750, 16000, 16000, 16250, 16500, 16750, 17000, 17000, 17250, 17500, 17750, 18000, 18000, 18250, 18500, 18750, 19000, 19000, 19250, 19500, 19750, 20000, 20000, 20000, 20250, 20500, 20750, 21000, 21000, 21250, 21500, 21750, 22000, 22000, 22250, 22500, 22750, 23000, 23000, 23250, 23500, 23750, 24000, 24000, 24250, 24500, 24750, 25000, 25000, 25250, 25500, 25750, 26000, 26000, 26250, 26500, 26750, 27000, 27000, 27250, 27500, 27750, 28000, 28000, 28250, 28500, 28750, 29000, 29000, 29250, 29500, 29750, 30000, 30000, 30000 ) ),
	(	localeInfo.MOUNT_TOOLTIP_APPLY_ATTBONUS_MONSTER,		( 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5, 6, 6, 6, 6, 6, 7, 7, 7, 7, 7, 8, 8, 8, 8, 8, 9, 9, 9, 9, 9, 10, 10, 10, 10, 10, 11, 11, 11, 11, 11, 12, 12, 12, 12, 12, 13, 13, 13, 13, 13, 14, 14, 14, 14, 14, 15, 15, 15, 15, 15, 16, 16, 16, 16, 16, 17, 17, 17, 17, 17, 18, 18, 18, 18, 18, 19, 19, 19, 19, 19, 20, 20, 20, 20, 20, 21, 21, 21, 21, 21, 22, 22, 22, 22, 22, 23, 23, 23, 23, 23, 24, 24, 24, 24, 24, 25, 25, 25, 25, 25, 26, 26, 26, 26, 26, 27, 27, 27, 27, 27, 28, 28, 28, 28, 28, 29, 29, 29, 29, 29, 30 ) ),
	(	localeInfo.MOUNT_TOOLTIP_APPLY_ATTBONUS_STONE,		( 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10 ) ),
	(	localeInfo.MOUNT_TOOLTIP_APPLY_ATTBONUS_BOSS,		( 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 10, 10, 10, 10, 10, 10 ) ),
	(	localeInfo.MOUNT_TOOLTIP_ATTBONUS_DUNGEON,			( 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 10, 10, 10, 10, 10, 10 ) ),
	)

class MountWindow(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.isLoaded = 0
		self.skillLv = {}
		self.tooltipItem = None
		self.levelToolTip = uiToolTip.ToolTip(230)
		self.mountLevel = 0
		self.bonusLabels = {}
		self.LoadWindow()
		
	def __del__(self):
		ui.ScriptWindow.__del__(self)
		
	def Destroy(self):
		# Podglad 3D musi zgasnac razem z oknem - dopoki render target jest "widoczny",
		# silnik deformuje jego model CO KLATKE (do 53 ms/klatke wg hitch_log).
		renderTarget.SetVisibility(202, False)

	def LoadWindow(self):
		if self.isLoaded:
			return
			
		self.isLoaded = 1

		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "uiscript/mountwindow.py")
		except:
			import exception
			exception.Abort("MountWindow.LoadDialog.LoadScript")
			
		try:
			self.equipSlots = self.GetChild("equip_slot")
			self.costumeSlot = self.GetChild("costume_slot")
			
			self.valueName = self.GetChild("value_name")
			self.valueExpCurrent = self.GetChild("value_exp_current")
			self.valueExpNeed = self.GetChild("value_exp_need")
			self.valueLevel = self.GetChild("value_level")
			self.titleBar = self.GetChild("TitleBar")
			self.titleBar.SetCloseEvent(ui.__mem_func__(self.Close))
			self.mountFeedItem = self.GetChild("mount_feed_item")
			self.expBar = self.GetChild("exp_bar")
			
			self.mountButton = self.GetChild("mount_button")
			self.mountButtonOdwolaj = self.GetChild("mount_button_unsummon")
			self.bonusLabels['max_hp'] = self.GetChild("label_max_hp")
			self.bonusLabels['att_bonus_monster'] = self.GetChild("label_att_bonus_monster")
			self.bonusLabels['att_bonus_metine'] = self.GetChild("label_att_bonus_metine")
			self.bonusLabels['att_bonus_sefi'] = self.GetChild("label_att_bonus_sefi")
			self.bonusLabels['att_bonus_dungeon'] = self.GetChild("label_att_bonus_dungeon")
        
		except:
			import exception
			exception.Abort("MountWindow.LoadDialog.BindObject")
			
		self.equipSlots.SetSelectEmptySlotEvent(ui.__mem_func__(self.__OnSelectEmptySlot))
		self.equipSlots.SetSelectItemSlotEvent(ui.__mem_func__(self.__OnSelectItemSlot))
		self.equipSlots.SetUnselectItemSlotEvent(ui.__mem_func__(self.__OnUnselectItemSlot))
		self.equipSlots.SetUseSlotEvent(ui.__mem_func__(self.__OnSelectItemSlot))
		self.equipSlots.SetOverInItemEvent(ui.__mem_func__(self.__OnOverInItem))
		self.equipSlots.SetOverOutItemEvent(ui.__mem_func__(self.__OnOverOutItem))
		
		self.costumeSlot.SetSelectEmptySlotEvent(ui.__mem_func__(self.__OnSelectEmptySlot))
		self.costumeSlot.SetSelectItemSlotEvent(ui.__mem_func__(self.__OnSelectItemSlot))
		self.costumeSlot.SetUnselectItemSlotEvent(ui.__mem_func__(self.__OnUnselectItemSlot))
		self.costumeSlot.SetUseSlotEvent(ui.__mem_func__(self.__OnSelectItemSlot))
		self.costumeSlot.SetOverInItemEvent(ui.__mem_func__(self.__OnOverInItem))
		self.costumeSlot.SetOverOutItemEvent(ui.__mem_func__(self.__OnOverOutItem))

		self.mountButtonOdwolaj.SetEvent(ui.__mem_func__(self.__UnsummonMount))
		self.mountButton.SetEvent(ui.__mem_func__(self.__SummonMount))


		renderTarget.SetBackground(202, "kowal/petmount/bg_render.png")
		renderTarget.SetVisibility(202, True)
		
	def SetItemToolTip(self, itemTooltip):
		self.tooltipItem = itemTooltip
		
	def Open(self):
		if self.IsShow():
			self.Close()
		else:
			self.SetCenterPosition()
			self.Show()
		
	def SetBasicInfo(self, vnum, name, level, exp, req_exp, summoned):
		renderTarget.SelectModel(202, vnum)
		self.valueName.SetFontName(localeInfo.UI_DEF_FONT_LARGE)
		self.valueName.SetOutline()
		self.valueName.SetText(name)
		self.valueLevel.SetFontName(localeInfo.UI_DEF_FONT_LARGE)
		self.valueLevel.SetOutline()
		self.valueLevel.SetText(str(level))
		self.mountLevel = level
		self.valueExpCurrent.SetFontName(localeInfo.UI_DEF_FONT_LARGE)
		self.valueExpCurrent.SetOutline()
		self.valueExpCurrent.SetText(localeInfo.MOUNT_WINDOW_CURRENT_EXP.format(str(exp)))
		self.valueExpNeed.SetFontName(localeInfo.UI_DEF_FONT_LARGE)
		self.valueExpNeed.SetOutline()
		self.valueExpNeed.SetText(localeInfo.MOUNT_WINDOW_NEED_EXP.format(str(req_exp)))
		self.mountFeedItem.SetFontName(localeInfo.UI_DEF_FONT_LARGE)
		self.UpdateBonusLabels(level)
		if level <= 24:
			self.mountFeedItem.SetText("|Eemoji/feed_1|e" + localeInfo.MOUNT_WINDOW_FEED_ITEM_1)
		elif level >= 25 and level <= 49:
			self.mountFeedItem.SetText("|Eemoji/feed_2|e" + localeInfo.MOUNT_WINDOW_FEED_ITEM_2)
		elif level >= 50 and level <= 74:
			self.mountFeedItem.SetText("|Eemoji/feed_3|e" + localeInfo.MOUNT_WINDOW_FEED_ITEM_3)
		else:
			self.mountFeedItem.SetText("|Eemoji/feed_4|e" + localeInfo.MOUNT_WINDOW_FEED_ITEM_4)
		
		self.expBar.SetRenderingRect(0.0, -1.0 + float(exp) / float(req_exp), 0.0, 0.0)
		
		
		if summoned == True:
			self.mountButton.Hide()
			self.mountButtonOdwolaj.Show()
		else:
			self.mountButton.Show()
			self.mountButtonOdwolaj.Hide()
			
	def UpdateBonusLabels(self, level):
		max_hp = MOUNT_BONUS_INFO[0][1][level-1]
		att_bonus_monster = MOUNT_BONUS_INFO[1][1][level-1]
		att_bonus_metine = MOUNT_BONUS_INFO[2][1][level-1]
		att_bonus_sefi = MOUNT_BONUS_INFO[3][1][level-1]
		att_bonus_dungeon = MOUNT_BONUS_INFO[4][1][level-1]
		
		self.bonusLabels['max_hp'].SetFontName(localeInfo.UI_DEF_FONT_LARGE)
		self.bonusLabels['att_bonus_monster'].SetFontName(localeInfo.UI_DEF_FONT_LARGE)
		self.bonusLabels['att_bonus_metine'].SetFontName(localeInfo.UI_DEF_FONT_LARGE)
		self.bonusLabels['att_bonus_sefi'].SetFontName(localeInfo.UI_DEF_FONT_LARGE)
		self.bonusLabels['att_bonus_dungeon'].SetFontName(localeInfo.UI_DEF_FONT_LARGE)
		
		self.bonusLabels['max_hp'].SetText("|cffb0dfb4|H|h{}|H|h: |cff329c4a|H|h{}|H|h".format(localeInfo.MOUNT_TOOLTIP_MAX_HP, max_hp))
		self.bonusLabels['att_bonus_monster'].SetText("|cffb0dfb4|H|h{}|H|h: |cff329c4a|H|h{}|H|h".format(localeInfo.MOUNT_TOOLTIP_APPLY_ATTBONUS_MONSTER, att_bonus_monster))
		self.bonusLabels['att_bonus_metine'].SetText("|cffb0dfb4|H|h{}|H|h: |cff329c4a|H|h{}|H|h".format(localeInfo.MOUNT_TOOLTIP_APPLY_ATTBONUS_STONE, att_bonus_metine))
		self.bonusLabels['att_bonus_sefi'].SetText("|cffb0dfb4|H|h{}|H|h: |cff329c4a|H|h{}|H|h".format(localeInfo.MOUNT_TOOLTIP_APPLY_ATTBONUS_BOSS, att_bonus_sefi))
		self.bonusLabels['att_bonus_dungeon'].SetText("|cffb0dfb4|H|h{}|H|h: |cff329c4a|H|h{}|H|h".format(localeInfo.MOUNT_TOOLTIP_ATTBONUS_DUNGEON, att_bonus_dungeon))
			
	def __UnsummonMount(self):
		net.SendChatPacket("/horse_unsummon")
		
	def __SummonMount(self):
		net.SendChatPacket("/horse_summon")
		
	def RefreshEquipmentSlots(self):
		getItemVNum=player.GetItemIndex
		for i in range(item.MOUNT_SLOT_COUNT):
			self.equipSlots.SetItemSlot(item.MOUNT_SLOT_START + i, getItemVNum(item.MOUNT_SLOT_START + i), 0)
		self.equipSlots.RefreshSlot()
		
		self.costumeSlot.SetItemSlot(item.COSTUME_SLOT_MOUNT, getItemVNum(item.COSTUME_SLOT_MOUNT), 0)
		self.costumeSlot.RefreshSlot()
				
	def __OnUnselectItemSlot(self, slotIndex):
		net.SendItemUsePacket(slotIndex)
		
	def __OnSelectEmptySlot(self, slotIndex):
		pass
			
	def __OnSelectItemSlot(self, slotIndex):
		if constInfo.GET_ITEM_QUESTION_DIALOG_STATUS() == 1:
			return
	
		if mouseModule.mouseController.isAttached():
			attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
			attachedSlotType = mouseModule.mouseController.GetAttachedType()
			attachedItemCount = mouseModule.mouseController.GetAttachedItemCount()
	
			if attachedSlotPos != slotIndex and player.SLOT_TYPE_INVENTORY == attachedSlotType:
				net.SendItemMovePacket(attachedSlotPos, slotIndex, attachedItemCount)
	
			mouseModule.mouseController.DeattachObject()
		else:
			selectedItemVNum = player.GetItemIndex(player.INVENTORY, slotIndex)
			itemCount = player.GetItemCount(player.INVENTORY, slotIndex)
			mouseModule.mouseController.AttachObject(self, player.SLOT_TYPE_INVENTORY, slotIndex, selectedItemVNum, itemCount)
	
	def __OnOverInItem(self, slotIndex):
		if self.tooltipItem:
			self.tooltipItem.SetInventoryItem(slotIndex)
	
	def __OnOverOutItem(self):
		if self.tooltipItem:
			self.tooltipItem.HideToolTip()
	
	def Close(self):
		if self.tooltipItem:
			self.tooltipItem.HideToolTip()

		renderTarget.SetVisibility(202, False)
		self.Hide()
		
	def OnPressEscapeKey(self):
		self.Close()
		return True
		
	def OnUpdate(self):
		self.RefreshEquipmentSlots()
