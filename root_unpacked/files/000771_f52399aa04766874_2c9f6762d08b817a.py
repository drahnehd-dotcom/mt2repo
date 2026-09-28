# -*- coding: utf-8 -*-
"""
AttachMetinDialog Module - Interface for attaching metin stones to items
Refactored for modern Python 2.7 practices with improved error handling and class design
"""

import dbg
import player
import item
import net
import snd
import ui
import uiToolTip
import localeInfo
import app


class AttachMetinDialog(ui.ScriptWindow):
    """Dialog for attaching metin stones to equipment items"""
    
    # Class constants
    UI_SCRIPT_PATH = "uiscript/attachstonedialog.py"
    SOUND_PATH = "sound/ui/metinstone_insert.wav"
    
    # UI positioning constants
    TOOLTIP_SPACING = 60
    ARROW_OFFSET = 28
    SLOT_OFFSET_Y = 40
    BOARD_PADDING = 70
    BOARD_HEIGHT_OFFSET = 98
    TITLE_BAR_OFFSET = 15
    
    def __init__(self, wnd_inventory=None):
        """Initialize AttachMetinDialog
        
        Args:
            wnd_inventory: Inventory window reference (only used if WJ_ENABLE_TRADABLE_ICON is enabled)
        """
        super(AttachMetinDialog, self).__init__()
        
        # Core state
        self._metin_item_pos = 0
        self._target_item_pos = 0
        
        # UI components
        self._board = None
        self._title_bar = None
        self._metin_image = None
        self._metin_slot = None
        self._attach_metin_arrow = None
        self._old_tooltip = None
        self._new_tooltip = None
        
        # Feature-specific initialization
        if self._has_tradable_icon_feature():
            self._wnd_inventory = wnd_inventory
            self._locked_items = {i: (-1, -1) for i in range(2)}
        else:
            self._wnd_inventory = None
            self._locked_items = None
        
        # Load UI
        self._load_script()
    
    def __del__(self):
        """Cleanup resources"""
        super(AttachMetinDialog, self).__del__()
    
    @staticmethod
    def _has_tradable_icon_feature():
        """Check if tradable icon feature is enabled"""
        return hasattr(app, 'WJ_ENABLE_TRADABLE_ICON') and app.WJ_ENABLE_TRADABLE_ICON
    
    def _load_script(self):
        """Load UI script and initialize components"""
        try:
            self._load_ui_script()
            self._bind_ui_objects()
            self._setup_tooltips()
            self._setup_events()
        except Exception as e:
            self._log_error("Failed to load script", e)
            raise
    
    def _load_ui_script(self):
        """Load the UI script file"""
        try:
            py_scr_loader = ui.PythonScriptLoader()
            py_scr_loader.LoadScriptFile(self, self.UI_SCRIPT_PATH)
        except Exception as e:
            import exception
            exception.Abort("AttachStoneDialog.__LoadScript.LoadObject")
            raise e
    
    def _bind_ui_objects(self):
        """Bind UI objects from the loaded script"""
        try:
            self._board = self.GetChild("Board")
            self._title_bar = self.GetChild("TitleBar")
            self._metin_image = self.GetChild("MetinImage")
            self._metin_slot = self.GetChild("MetinSlot")
            self._attach_metin_arrow = self.GetChild("AttachMetinArrow")
        except Exception as e:
            import exception
            exception.Abort("AttachStoneDialog.__LoadScript.BindObject")
            raise e
    
    def _setup_tooltips(self):
        """Setup tooltip components"""
        self._old_tooltip = self._create_tooltip(15, 38)
        self._new_tooltip = self._create_tooltip(300, 38)
    
    def _create_tooltip(self, x, y):
        """Create and configure a tooltip
        
        Args:
            x (int): X position
            y (int): Y position
            
        Returns:
            uiToolTip.ItemToolTip: Configured tooltip
        """
        tooltip = uiToolTip.ItemToolTip()
        tooltip.SetParent(self)
        tooltip.SetPosition(x, y)
        tooltip.SetModelShow(False)
        tooltip.SetFollow(False)
        tooltip.Show()
        return tooltip
    
    def _setup_events(self):
        """Setup UI event handlers"""
        self.GetChild("AcceptButton").SetEvent(ui.__mem_func__(self._on_accept))
        self.GetChild("CancelButton").SetEvent(ui.__mem_func__(self.Close))
        self._title_bar.SetCloseEvent(ui.__mem_func__(self.Close))
    
    def Destroy(self):
        """Destroy dialog and cleanup resources"""
        self.ClearDictionary()
        
        # Clear references
        self._board = None
        self._title_bar = None
        self._metin_image = None
        self._metin_slot = None
        self._attach_metin_arrow = None
        self._old_tooltip = None
        self._new_tooltip = None
        
        if self._has_tradable_icon_feature():
            self._wnd_inventory = None
            self._locked_items = None
    
    def can_attach_metin(self, socket_type, metin_type):
        """Check if metin can be attached to socket
        
        Args:
            socket_type: Type of socket (silver/gold)
            metin_type: Type of metin stone
            
        Returns:
            bool: True if attachment is possible
        """
        if metin_type == item.METIN_NORMAL:
            return socket_type in (player.METIN_SOCKET_TYPE_SILVER, player.METIN_SOCKET_TYPE_GOLD)
        elif metin_type == item.METIN_GOLD:
            return socket_type == player.METIN_SOCKET_TYPE_GOLD
        
        return False
    
    def Open(self, metin_item_pos, target_item_pos):
        """Open the dialog with specified items
        
        Args:
            metin_item_pos (int): Position of metin stone in inventory
            target_item_pos (int): Position of target item in inventory
        """
        try:
            self._metin_item_pos = metin_item_pos
            self._target_item_pos = target_item_pos
            
            self._setup_dialog_content()
            self._update_dialog_layout()
            self._show_dialog()
            
            if self._has_tradable_icon_feature():
                self._lock_item_slots()
                
        except Exception as e:
            self._log_error("Failed to open dialog", e)
    
    def _setup_dialog_content(self):
        """Setup dialog content with item data"""
        metin_index = player.GetItemIndex(self._metin_item_pos)
        target_index = player.GetItemIndex(self._target_item_pos)
        
        self._old_tooltip.ClearToolTip()
        self._new_tooltip.ClearToolTip()
        
        self._load_metin_image(metin_index)
        
        self._setup_tooltip_data(metin_index, target_index)
    
    def _load_metin_image(self, metin_index):
        """Load metin stone image
        
        Args:
            metin_index (int): Index of metin item
        """
        try:
            item.SelectItem(metin_index)
            self._metin_image.LoadImage(item.GetIconImageFileName())
        except Exception as e:
            self._log_error("Failed to load metin image", e)
    
    def _setup_tooltip_data(self, metin_index, target_index):
        """Setup tooltip data for old and new item states
        
        Args:
            metin_index (int): Index of metin stone
            target_index (int): Index of target item
        """
        current_sockets = self._get_item_sockets(self._target_item_pos)
        
        self._old_tooltip.AddItemData(target_index, current_sockets)
        
        item.SelectItem(metin_index)
        metin_sub_type = item.GetItemSubType()
        
        projected_sockets = self._calculate_projected_sockets(
            current_sockets, metin_index, metin_sub_type
        )
        self._new_tooltip.AddItemData(target_index, projected_sockets)
    
    def _get_item_sockets(self, item_pos):
        """Get all metin sockets for an item
        
        Args:
            item_pos (int): Item position in inventory
            
        Returns:
            list: List of socket values
        """
        return [
            player.GetItemMetinSocket(item_pos, i) 
            for i in range(player.METIN_SOCKET_MAX_NUM)
        ]
    
    def _calculate_projected_sockets(self, current_sockets, metin_index, metin_sub_type):
        """Calculate what sockets would look like after attachment
        
        Args:
            current_sockets (list): Current socket configuration
            metin_index (int): Index of metin to attach
            metin_sub_type: Subtype of metin stone
            
        Returns:
            list: Projected socket configuration
        """
        projected_sockets = list(current_sockets)
        
        for i in range(player.METIN_SOCKET_MAX_NUM):
            if self.can_attach_metin(projected_sockets[i], metin_sub_type):
                projected_sockets[i] = metin_index
                break
        
        return projected_sockets
    
    def _update_dialog_layout(self):
        """Update dialog layout based on tooltip sizes"""
        old_width = self._old_tooltip.GetWidth()
        new_width = self._new_tooltip.GetWidth()
        
        # Calculate new dimensions
        total_width = old_width + new_width + self.BOARD_PADDING
        total_height = self._new_tooltip.GetHeight() + self.BOARD_HEIGHT_OFFSET
        
        # Position elements
        self._position_dialog_elements(old_width)
        
        # Update dialog size
        self._update_dialog_size(total_width, total_height)
    
    def _position_dialog_elements(self, old_width):
        """Position dialog elements based on old tooltip width
        
        Args:
            old_width (int): Width of old tooltip
        """
        arrow_x = old_width + self.ARROW_OFFSET
        arrow_y = self._old_tooltip.GetHeight() // 2
        
        slot_x = old_width + self.ARROW_OFFSET - 8  # Slight adjustment for slot
        slot_y = arrow_y + self.SLOT_OFFSET_Y
        
        self._new_tooltip.SetPosition(old_width + self.TOOLTIP_SPACING, 38)
        self._attach_metin_arrow.SetPosition(arrow_x, arrow_y)
        self._metin_slot.SetPosition(slot_x, slot_y)
    
    def _update_dialog_size(self, width, height):
        """Update dialog size and position
        
        Args:
            width (int): New width
            height (int): New height
        """
        self._board.SetSize(width, height)
        self._title_bar.SetWidth(width - self.TITLE_BAR_OFFSET)
        self.SetSize(width, height)
        
        # Maintain current position
        x, y = self.GetLocalPosition()
        self.SetPosition(x, y)
    
    def _show_dialog(self):
        """Show the dialog"""
        self.SetTop()
        self.Show()
    
    def _lock_item_slots(self):
        """Lock item slots to prevent interaction (tradable icon feature)"""
        if self._has_tradable_icon_feature() and self._wnd_inventory:
            self._set_cant_mouse_event_slot(0, self._metin_item_pos)
            self._set_cant_mouse_event_slot(1, self._target_item_pos)
    
    def _on_accept(self):
        """Handle accept button click"""
        try:
            net.SendItemUseToItemPacket(self._metin_item_pos, self._target_item_pos)
            self._play_attach_sound()
            self.Close()
        except Exception as e:
            self._log_error("Failed to accept attachment", e)
    
    def _play_attach_sound(self):
        """Play attachment sound effect"""
        try:
            snd.PlaySound(self.SOUND_PATH)
        except Exception as e:
            self._log_error("Failed to play sound", e)
    
    def Close(self):
        """Close the dialog"""
        self.Hide()
        
        if self._has_tradable_icon_feature():
            self._unlock_item_slots()
    
    def _unlock_item_slots(self):
        """Unlock item slots (tradable icon feature)"""
        if self._wnd_inventory:
            self._set_can_mouse_event_slot(0, self._metin_item_pos)
            self._set_can_mouse_event_slot(1, self._target_item_pos)
    
    # Tradable icon feature methods
    def _set_can_mouse_event_slot(self, slot_type, slot_index):
        """Enable mouse events for slot
        
        Args:
            slot_type (int): Type identifier for slot
            slot_index (int): Inventory slot index
        """
        if not self._has_tradable_icon_feature() or not self._wnd_inventory:
            return
        
        item_page, local_pos = self._calculate_slot_position(slot_index)
        self._locked_items[slot_type] = (-1, -1)
        
        if item_page == self._wnd_inventory.GetInventoryPageIndex():
            self._wnd_inventory.wndItem.SetCanMouseEventSlot(local_pos)
    
    def _set_cant_mouse_event_slot(self, slot_type, slot_index):
        """Disable mouse events for slot
        
        Args:
            slot_type (int): Type identifier for slot
            slot_index (int): Inventory slot index
        """
        if not self._has_tradable_icon_feature() or not self._wnd_inventory:
            return
        
        item_page, local_pos = self._calculate_slot_position(slot_index)
        self._locked_items[slot_type] = (item_page, local_pos)
        
        if item_page == self._wnd_inventory.GetInventoryPageIndex():
            self._wnd_inventory.wndItem.SetCantMouseEventSlot(local_pos)
    
    def _calculate_slot_position(self, slot_index):
        """Calculate page and local position for slot
        
        Args:
            slot_index (int): Global slot index
            
        Returns:
            tuple: (page_index, local_position)
        """
        item_page = slot_index // player.INVENTORY_PAGE_SIZE
        local_pos = slot_index - (item_page * player.INVENTORY_PAGE_SIZE)
        return item_page, local_pos
    
    def refresh_locked_slot(self):
        """Refresh locked slots when page changes"""
        if not self._has_tradable_icon_feature() or not self._wnd_inventory:
            return
        
        try:
            current_page = self._wnd_inventory.GetInventoryPageIndex()
            
            for slot_type, (item_page, slot_pos) in self._locked_items.items():
                if current_page == item_page and slot_pos >= 0:
                    self._wnd_inventory.wndItem.SetCantMouseEventSlot(slot_pos)
            
            self._wnd_inventory.wndItem.RefreshSlot()
            
        except Exception as e:
            self._log_error("Failed to refresh locked slots", e)
    
    def _log_error(self, message, error=None):
        """Log error messages
        
        Args:
            message (str): Error message
            error (Exception): Optional exception object
        """
        full_message = "AttachMetinDialog: {}".format(message)
        if error:
            full_message += " - Error: {}".format(str(error))
        
        try:
            dbg.TraceError(full_message)
        except Exception:
            print(full_message
)
    
    def CanAttachMetin(self, slot, metin):
        """Legacy compatibility method"""
        return self.can_attach_metin(slot, metin)
    
    def Accept(self):
        """Legacy compatibility method"""
        return self._on_accept()
    
    def SetCanMouseEventSlot(self, what, slot_index):
        """Legacy compatibility method"""
        return self._set_can_mouse_event_slot(what, slot_index)
    
    def SetCantMouseEventSlot(self, what, slot_index):
        """Legacy compatibility method"""
        return self._set_cant_mouse_event_slot(what, slot_index)
    
    def RefreshLockedSlot(self):
        """Legacy compatibility method"""
        return self.refresh_locked_slot()
    
    def UpdateDialog(self):
        """Legacy compatibility method"""
        return self._update_dialog_layout()


def CreateAttachMetinDialog(wnd_inventory=None):
    """Factory function to create AttachMetinDialog instance
    
    Args:
        wnd_inventory: Inventory window reference (optional)
        
    Returns:
        AttachMetinDialog: New dialog instance or None on failure
    """
    try:
        return AttachMetinDialog(wnd_inventory)
    except Exception as e:
        import dbg
        dbg.TraceError("Failed to create AttachMetinDialog: {}".format(str(e)))
        return None
		