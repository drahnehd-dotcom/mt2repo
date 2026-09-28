# -*- coding: utf-8 -*-
import ui
import acce
import player
import chat
import localeInfo
import chr
import uiToolTip
import mouseModule
import constInfo
import emoji


class MaterialDataManager(object):
    """Manages material data for accessory combination"""
    
    def __init__(self):
        self.data = {"materials": {"info": {}}}
    
    def store_material(self, material_id, vnum, count):
        """Store material information"""
        self.data["materials"][material_id] = []
        self.data["materials"][material_id].append([0, 0])
        self.data["materials"][material_id][0][0] = vnum
        self.data["materials"][material_id][0][1] = count
        
        if chr.IsGameMaster(0):
            chat.AppendChat(chat.CHAT_TYPE_INFO, str(self.data["materials"]))
    
    def get_material(self, material_id):
        """Get material information"""
        if material_id in self.data["materials"]:
            return self.data["materials"][material_id][0]
        return [0, 0]
    
    def get_material_vnum(self, material_id):
        """Get material vnum"""
        material_data = self.get_material(material_id)
        return material_data[0] if material_data else 0
    
    def get_material_count(self, material_id):
        """Get material count"""
        material_data = self.get_material(material_id)
        return material_data[1] if material_data else 0
    
    def clear_materials(self):
        """Clear all material data"""
        self.data["materials"] = {"info": {}}


class SlotManager(object):
    """Manages slot operations for UI windows"""
    
    def __init__(self, acce_slot, required_slots=None):
        self.acce_slot = acce_slot
        self.required_slots = required_slots
        self.tooltip_item = None
        self.material_manager = None
    
    def set_tooltip(self, tooltip_item):
        """Set tooltip item reference"""
        self.tooltip_item = tooltip_item
    
    def set_material_manager(self, material_manager):
        """Set material manager reference"""
        self.material_manager = material_manager
    
    def clear_all_slots(self):
        """Clear all slots in the UI"""
        acce.Clear()
        
        if self.acce_slot:
            for i in range(acce.WINDOW_MAX_MATERIALS + 1):
                self.acce_slot.ClearSlot(i)
        
        if self.required_slots:
            for x in range(2):
                self.required_slots.ClearSlot(x)
    
    def handle_empty_slot_selection(self, selected_slot_pos):
        """Handle selection of empty slot"""
        is_attached = mouseModule.mouseController.isAttached()
        if not is_attached or selected_slot_pos == acce.WINDOW_MAX_MATERIALS:
            return
        
        attached_slot_type = mouseModule.mouseController.GetAttachedType()
        attached_slot_pos = mouseModule.mouseController.GetAttachedSlotNumber()
        attached_inven_type = player.SlotTypeToInvenType(attached_slot_type)
        
        mouseModule.mouseController.DeattachObject()
        
        if (attached_slot_type == player.SLOT_TYPE_INVENTORY and 
            attached_inven_type == player.INVENTORY):
            acce.Add(attached_inven_type, attached_slot_pos, selected_slot_pos)
    
    def handle_item_slot_selection(self, selected_slot_pos):
        """Handle selection of item slot"""
        if selected_slot_pos == acce.WINDOW_MAX_MATERIALS:
            return
        
        mouseModule.mouseController.DeattachObject()
        acce.Remove(selected_slot_pos)
    
    def handle_tooltip_over_in(self, selected_slot_pos, is_result_slot=False):
        """Handle mouse over for tooltip display"""
        if not self.tooltip_item:
            return
        
        if selected_slot_pos == acce.WINDOW_MAX_MATERIALS:
            self._handle_result_slot_tooltip(is_result_slot)
        else:
            self._handle_regular_slot_tooltip(selected_slot_pos)
    
    def handle_required_slot_tooltip(self, slot_number):
        """Handle tooltip for required material slots"""
        if not self.tooltip_item or not self.material_manager:
            return
        
        vnum = self.material_manager.get_material_vnum(slot_number)
        if vnum > 0:
            self.tooltip_item.ClearToolTip()
            self.tooltip_item.AddItemData(vnum, metinSlot=[0 for _ in range(player.METIN_SOCKET_MAX_NUM)])
    
    def _handle_result_slot_tooltip(self, is_absorption=False):
        """Handle tooltip for result slot"""
        if is_absorption:
            is_here1, i_cell1 = acce.GetAttachedItem(0)
            is_here2, i_cell2 = acce.GetAttachedItem(1)
            if is_here1 and is_here2:
                self.tooltip_item.ClearToolTip()
                self.tooltip_item.SetInventoryItem(i_cell1)
                self.tooltip_item.SetAcceResultAbsItem(i_cell1, i_cell2)
        else:
            is_here, i_cell = acce.GetAttachedItem(0)
            if is_here:
                self.tooltip_item.ClearToolTip()
                self.tooltip_item.SetInventoryItem(i_cell)
                self.tooltip_item.SetAcceResultItem(i_cell)
    
    def _handle_regular_slot_tooltip(self, selected_slot_pos):
        """Handle tooltip for regular slots"""
        is_here, i_cell = acce.GetAttachedItem(selected_slot_pos)
        if is_here:
            self.tooltip_item.SetInventoryItem(i_cell)
    
    def handle_tooltip_over_out(self):
        """Handle mouse out for tooltip"""
        if self.tooltip_item:
            self.tooltip_item.HideToolTip()
    
    def refresh_slots(self, material_manager):
        """Refresh slot display with current data"""
        self.acce_slot.ClearSlot(acce.WINDOW_MAX_MATERIALS)
        
        if self.required_slots:
            for x in range(2):
                vnum = material_manager.get_material_vnum(x)
                count = material_manager.get_material_count(x)
                self.required_slots.ClearSlot(x)
                if vnum > 0:
                    self.required_slots.SetItemSlot(x, vnum, count)
        
        for i in range(acce.WINDOW_MAX_MATERIALS):
            self.acce_slot.ClearSlot(i)
            is_here, i_cell = acce.GetAttachedItem(i)
            if is_here:
                self.acce_slot.SetItemSlot(i, player.GetItemIndex(i_cell), 0)
                
                if i == int(acce.WINDOW_MAX_MATERIALS - 1):
                    item_vnum, min_abs, max_abs = acce.GetResultItem()
                    if item_vnum:
                        self.acce_slot.SetItemSlot(i + 1, item_vnum, 0)
                        break


class PositionTracker(object):
    """Tracks player position for window constraints"""
    
    def __init__(self):
        self.position_out = 0
        self.position_start_x = 0
        self.position_start_y = 0
    
    def initialize_position(self):
        """Initialize starting position"""
        self.position_out = 0
        self.position_start_x, self.position_start_y, _ = player.GetMainCharacterPosition()
    
    def check_position_limit(self, on_limit_exceeded):
        """Check if player has moved beyond limit"""
        limit_range = acce.LIMIT_RANGE
        x, y, _ = player.GetMainCharacterPosition()
        
        if (abs(x - self.position_start_x) >= limit_range or 
            abs(y - self.position_start_y) >= limit_range):
            if not self.position_out:
                self.position_out += 1
                on_limit_exceeded()
    
    def reset(self):
        """Reset position tracking"""
        self.position_out = 0
        self.position_start_x = 0
        self.position_start_y = 0


class PriceFormatter(object):
    """Utility class for formatting prices and costs"""
    
    @staticmethod
    def format_cost_string(cost):
        """Format cost with thousand separators"""
        cost_str = str(cost)
        return ".".join([
            cost_str[max(0, i - 3):i] 
            for i in range(len(cost_str) % 3, len(cost_str) + 1, 3) 
            if i
        ])
    
    @staticmethod
    def format_price_display(cost, cost2):
        """Format complete price display with emojis"""
        cost_str = PriceFormatter.format_cost_string(cost)
        return localeInfo.PRICE_FORMAT.format(
            cost_str,
            emoji.AppendEmoji("icon/emoji/money_icon.png"),
            cost2,
            emoji.AppendEmoji("icon/emoji/cheque_icon.png")
        )


class BaseAcceWindow(ui.ScriptWindow):
    """Base class for accessory windows with common functionality"""
    
    def __init__(self):
        super(BaseAcceWindow, self).__init__()
        self.is_loaded = False
        self.position_tracker = PositionTracker()
        self.slot_manager = None
        self.tooltip_item = None
        
        self.title_bar = None
        self.btn_accept = None
        self.btn_cancel = None
        self.acce_slot = None
    
    def __del__(self):
        super(BaseAcceWindow, self).__del__()
    
    def destroy(self):
        """Clean up window resources"""
        self._clear_ui_references()
        self.position_tracker.reset()
        self.ClearDictionary()
    
    def _clear_ui_references(self):
        """Clear UI component references"""
        self.title_bar = None
        self.btn_accept = None
        self.btn_cancel = None
        self.acce_slot = None
        self.tooltip_item = None
    
    def set_item_tooltip(self, item_tooltip):
        """Set tooltip item reference"""
        self.tooltip_item = item_tooltip
        if self.slot_manager:
            self.slot_manager.set_tooltip(item_tooltip)
    
    def is_opened(self):
        """Check if window is open and loaded"""
        return self.IsShow() and self.is_loaded
    
    def open_window(self):
        """Open the window"""
        self.position_tracker.initialize_position()
        self._perform_open_actions()
        self.SetCenterPosition()
        self.Show()
    
    def close_window(self):
        """Close the window"""
        if self.tooltip_item:
            self.tooltip_item.HideToolTip()
        self._perform_close_actions()
        self.Hide()
    
    def _perform_open_actions(self):
        """Override in subclasses for specific open actions"""
        pass
    
    def _perform_close_actions(self):
        """Override in subclasses for specific close actions"""
        pass
    
    def on_close(self):
        """Handle window close event"""
        acce.SendCloseRequest()
    
    def on_press_escape_key(self):
        """Handle escape key press"""
        self.on_close()
        return True
    
    def on_accept(self):
        """Handle accept button"""
        acce.SendRefineRequest()
    
    def OnUpdate(self):
        """Update window state"""
        self.position_tracker.check_position_limit(self.on_close)
        self._perform_update_actions()
    
    def _perform_update_actions(self):
        """Override in subclasses for specific update actions"""
        pass
    
    def _setup_event_handlers(self):
        """Setup common event handlers"""
        if self.title_bar:
            self.title_bar.SetCloseEvent(ui.__mem_func__(self.on_close))
        if self.btn_cancel:
            self.btn_cancel.SetEvent(ui.__mem_func__(self.on_close))
        if self.btn_accept:
            self.btn_accept.SetEvent(ui.__mem_func__(self.on_accept))
    
    def _setup_slot_events(self):
        """Setup slot event handlers"""
        if self.acce_slot and self.slot_manager:
            self.acce_slot.SetSelectEmptySlotEvent(
                ui.__mem_func__(self.slot_manager.handle_empty_slot_selection)
            )
            self.acce_slot.SetUnselectItemSlotEvent(
                ui.__mem_func__(self.slot_manager.handle_item_slot_selection)
            )
            self.acce_slot.SetUseSlotEvent(
                ui.__mem_func__(self.slot_manager.handle_item_slot_selection)
            )
            self.acce_slot.SetOverOutItemEvent(
                ui.__mem_func__(self.slot_manager.handle_tooltip_over_out)
            )
    
    # Legacy method names for backward compatibility
    def Destroy(self):
        return self.destroy()
    
    def SetItemToolTip(self, itemTooltip):
        return self.set_item_tooltip(itemTooltip)
    
    def IsOpened(self):
        return self.is_opened()
    
    def Open(self):
        return self.open_window()
    
    def Close(self):
        return self.close_window()
    
    def OnClose(self):
        return self.on_close()
    
    def OnPressEscapeKey(self):
        return self.on_press_escape_key()
    
    def OnAccept(self):
        return self.on_accept()


class CombineWindow(BaseAcceWindow):
    """Window for combining accessories"""
    
    def __init__(self):
        super(CombineWindow, self).__init__()
        self.material_manager = MaterialDataManager()
        self.required_slots = None
        self.need_money = None
        self.chance = None
        self.result = None
        self.do_refine_with_enter = None
    
    def _clear_ui_references(self):
        """Clear UI component references"""
        super(CombineWindow, self)._clear_ui_references()
        self.required_slots = None
        self.need_money = None
        self.chance = None
        self.result = None
        self.do_refine_with_enter = None
    
    def load_window(self):
        """Load the window UI"""
        if self.is_loaded:
            return
        
        self.is_loaded = True
        self._load_script()
        self._bind_ui_components()
        self._setup_components()
        self._setup_event_handlers()
        self._setup_slot_events()
    
    def _load_script(self):
        """Load UI script"""
        try:
            pyScrLoader = ui.PythonScriptLoader()
            pyScrLoader.LoadScriptFile(self, "uiscript/acce_combinewindow.py")
        except:
            import exception
            exception.Abort("Acce_CombineWindow.LoadDialog.LoadScript")
    
    def _bind_ui_components(self):
        """Bind UI components"""
        try:
            self.title_bar = self.GetChild("TitleBar")
            self.btn_accept = self.GetChild("AcceptButton")
            self.btn_cancel = self.GetChild("CancelButton")
            self.need_money = self.GetChild("NeedMoney")
            self.chance = self.GetChild("Chance")
            self.result = self.GetChild("Result")
            self.acce_slot = self.GetChild("AcceSlot")
            self.required_slots = self.GetChild("RequiredItems")
            self.do_refine_with_enter = self.GetChild("DoRefineWithEnter")
        except:
            import exception
            exception.Abort("Acce_CombineWindow.LoadDialog.BindObject")
    
    def _setup_components(self):
        """Setup window components"""
        # Initialize slot manager
        self.slot_manager = SlotManager(self.acce_slot, self.required_slots)
        self.slot_manager.set_material_manager(self.material_manager)
        
        # Setup refine with enter toggle
        self.do_refine_with_enter.SetToggleUpEvent(ui.__mem_func__(self._on_click_enable_refine_with_enter))
        self.do_refine_with_enter.SetToggleDownEvent(ui.__mem_func__(self._on_click_enable_refine_with_enter))
        
        if constInfo.IS_ACCE_WINDOW:
            self.do_refine_with_enter.Down()
        
        # Setup required slots tooltip
        self.required_slots.SetOverInItemEvent(lambda slot_number: self.slot_manager.handle_required_slot_tooltip(slot_number))
        self.required_slots.SetOverOutItemEvent(ui.__mem_func__(self.slot_manager.handle_tooltip_over_out))
    
    def _setup_slot_events(self):
        """Setup slot event handlers with tooltip support"""
        super(CombineWindow, self)._setup_slot_events()
        
        self.acce_slot.SetOverInItemEvent(
            lambda slot_pos: self.slot_manager.handle_tooltip_over_in(slot_pos, False)
        )
    
    def _on_click_enable_refine_with_enter(self):
        """Handle refine with enter toggle"""
        constInfo.IS_ACCE_WINDOW = not constInfo.IS_ACCE_WINDOW
    
    def _perform_open_actions(self):
        """Perform actions when opening window"""
        self._update_price_display()
        
        if self.slot_manager:
            self.slot_manager.clear_all_slots()
    
    def _perform_close_actions(self):
        """Perform actions when closing window"""
        constInfo.IS_ACCE_WINDOW = False
    
    def _perform_update_actions(self):
        """Perform update actions"""
        if constInfo.IS_ACCE_WINDOW:
            self.do_refine_with_enter.Down()
        else:
            self.do_refine_with_enter.SetUp()
    
    def _update_price_display(self):
        """Update price and chance display"""
        pct = str(acce.GetChance())
        cost = str(acce.GetPrice())
        cost2 = str(acce.GetCheque())
        
        price_display = PriceFormatter.format_price_display(cost, cost2)
        self.need_money.SetText(price_display)
        self.chance.SetText(localeInfo.CHANCE_FORMAT.format(pct))
    
    def send_materials(self, material_id, vnum, count):
        """Send materials data using manager"""
        self.material_manager.store_material(material_id, vnum, count)
    
    def refresh(self, i_act):
        """Refresh window display"""
        self._update_price_display()
        
        if self.slot_manager:
            self.slot_manager.refresh_slots(self.material_manager)
    
    # Legacy method names for backward compatibility
    def LoadWindow(self):
        return self.load_window()
    
    def ClearAllSlots(self):
        if self.slot_manager:
            return self.slot_manager.clear_all_slots()
    
    def SendMaterials(self, material_id, vnum, count):
        return self.send_materials(material_id, vnum, count)
    
    def Refresh(self, i_act):
        return self.refresh(i_act)
    
    def OnSelectEmptySlot(self, selectedSlotPos):
        if self.slot_manager:
            return self.slot_manager.handle_empty_slot_selection(selectedSlotPos)
    
    def OnSelectItemSlot(self, selectedSlotPos):
        if self.slot_manager:
            return self.slot_manager.handle_item_slot_selection(selectedSlotPos)
    
    def OnOverInItem(self, selectedSlotPos):
        if self.slot_manager:
            return self.slot_manager.handle_tooltip_over_in(selectedSlotPos, False)
    
    def OnOverOutItem(self):
        if self.slot_manager:
            return self.slot_manager.handle_tooltip_over_out()
    
    def __OnOverInItem(self, slotNumber):
        """Handle tooltip for required material slots (legacy method)"""
        if self.slot_manager:
            return self.slot_manager.handle_required_slot_tooltip(slotNumber)


class AbsorbWindow(BaseAcceWindow):
    """Window for absorbing accessories"""
    
    def __init__(self):
        super(AbsorbWindow, self).__init__()
    
    def load_window(self):
        """Load the window UI"""
        if self.is_loaded:
            return
        
        self.is_loaded = True
        self._load_script()
        self._bind_ui_components()
        self._setup_components()
        self._setup_event_handlers()
        self._setup_slot_events()
    
    def _load_script(self):
        """Load UI script"""
        try:
            pyScrLoader = ui.PythonScriptLoader()
            pyScrLoader.LoadScriptFile(self, "uiscript/acce_absorbwindow.py")
        except:
            import exception
            exception.Abort("Acce_AbsorbtionWindow.LoadDialog.LoadScript")
    
    def _bind_ui_components(self):
        """Bind UI components"""
        try:
            self.title_bar = self.GetChild("TitleBar")
            self.btn_accept = self.GetChild("AcceptButton")
            self.btn_cancel = self.GetChild("CancelButton")
            self.acce_slot = self.GetChild("AcceSlot")
        except:
            import exception
            exception.Abort("Acce_AbsorbtionWindow.LoadDialog.BindObject")
    
    def _setup_components(self):
        """Setup window components"""
        # Initialize slot manager for absorption
        self.slot_manager = SlotManager(self.acce_slot)
    
    def _setup_slot_events(self):
        """Setup slot event handlers"""
        super(AbsorbWindow, self)._setup_slot_events()
        
        self.acce_slot.SetOverInItemEvent(
            lambda slot_pos: self.slot_manager.handle_tooltip_over_in(slot_pos, True)
        )
    
    def _perform_open_actions(self):
        """Perform actions when opening window"""
        if self.slot_manager:
            self.slot_manager.clear_all_slots()
    
    def refresh(self, i_act):
        """Refresh window display"""
        if self.acce_slot:
            self.acce_slot.ClearSlot(acce.WINDOW_MAX_MATERIALS)
            
            for i in range(acce.WINDOW_MAX_MATERIALS):
                self.acce_slot.ClearSlot(i)
                is_here, i_cell = acce.GetAttachedItem(i)
                if is_here:
                    self.acce_slot.SetItemSlot(i, player.GetItemIndex(i_cell), 0)
                    
                    if i == int(acce.WINDOW_MAX_MATERIALS - 1):
                        item_vnum, min_abs, max_abs = acce.GetResultItem()
                        if item_vnum:
                            self.acce_slot.SetItemSlot(i + 1, item_vnum, 0)
                            break
    
    def LoadWindow(self):
        return self.load_window()
    
    def Refresh(self, i_act):
        return self.refresh(i_act)
    
    def OnSelectEmptySlot(self, selectedSlotPos):
        if self.slot_manager:
            return self.slot_manager.handle_empty_slot_selection(selectedSlotPos)
    
    def OnSelectItemSlot(self, selectedSlotPos):
        if self.slot_manager:
            return self.slot_manager.handle_item_slot_selection(selectedSlotPos)
    
    def OnOverInItem(self, selectedSlotPos):
        if self.slot_manager:
            return self.slot_manager.handle_tooltip_over_in(selectedSlotPos, True)
    
    def OnOverOutItem(self):
        if self.slot_manager:
            return self.slot_manager.handle_tooltip_over_out()


savedData = MaterialDataManager().data