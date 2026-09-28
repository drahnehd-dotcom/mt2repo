"""
Chest Drop Info Window - Displays item drop information from chests
Refactored for better maintainability and modern Python practices
"""

import ui
import item
import uiToolTip
import app
import player
import constInfo


class ChestDropConstants(object):
    """Constants for the chest drop window."""
    
    # Slot configuration
    # 7 x 6 = 42 sloty. Musi zgadzac sie z uiscript/chestdropinfowindow.py
    # ("x_count": 7, "y_count": 6) ORAZ z CGrid(7, 6) w PythonItemModule.cpp
    # (__CreateDropPage). Bylo tu 5 * 8 = 40, wiec petla czyszczaca omijala dwa
    # ostatnie sloty i zostawaly w nich itemy z poprzednio ogladanej skrzynki.
    DROP_SLOT_SIZE = 7 * 6
    
    # Data indices
    ITEM_INDEX = 0
    COUNT_INDEX = 1
    
    # Script path
    SCRIPT_PATH = "UIScript/ChestDropInfoWindow.py"


class ItemSlotManager(object):
    """Manages item slot operations and tooltips."""
    
    def __init__(self, window_instance):
        self._window = window_instance
        self._tooltip = uiToolTip.ItemToolTip()
    
    def setup_main_item_slot(self, slot_widget):
        """Setup main item slot events."""
        slot_widget.SetOverInItemEvent(ui.__mem_func__(self._on_main_item_hover))
        slot_widget.SetOverOutItemEvent(ui.__mem_func__(self._on_item_hover_out))
    
    def setup_drop_item_slot(self, slot_widget):
        """Setup drop item slot events."""
        slot_widget.SetOverInItemEvent(ui.__mem_func__(self._on_drop_item_hover))
        slot_widget.SetOverOutItemEvent(ui.__mem_func__(self._on_item_hover_out))
        slot_widget.SAFE_SetButtonEvent("RIGHT", "EXIST", self._on_drop_item_use)
    
    def _on_main_item_hover(self, slot_index):
        """Handle main item slot hover."""
        if self._tooltip and hasattr(self._window, '_current_item_vnum'):
            self._tooltip.SetItemToolTip(self._window._current_item_vnum)
    
    def _on_drop_item_hover(self, slot_index):
        """Handle drop item slot hover."""
        if not self._tooltip:
            return
        
        drop_data = self._window.get_drop_data_at_slot(slot_index)
        if drop_data:
            item_vnum = drop_data[ChestDropConstants.ITEM_INDEX]
            self._tooltip.SetItemToolTip(item_vnum)
    
    def _on_item_hover_out(self):
        """Handle item hover out."""
        if self._tooltip:
            self._tooltip.HideToolTip()
            self._tooltip.ClearToolTip()
    
    def _on_drop_item_use(self, slot_index):
        """Handle drop item slot right-click."""
        self._window.handle_drop_item_use(slot_index)
    
    def cleanup(self):
        """Clean up resources."""
        if self._tooltip:
            self._tooltip.HideToolTip()
            self._tooltip.ClearToolTip()
        self._tooltip = None


class NavigationManager(object):
    """Manages page navigation."""
    
    def __init__(self, window_instance):
        self._window = window_instance
        self._current_page = 0
        self._total_pages = 0
    
    def setup_navigation_buttons(self, prev_button, next_button, page_text):
        """Setup navigation button events."""
        prev_button.SetEvent(ui.__mem_func__(self._navigate_previous))
        next_button.SetEvent(ui.__mem_func__(self._navigate_next))
        self._page_text_widget = page_text
    
    def _navigate_previous(self):
        """Navigate to previous page."""
        self._navigate_to_page(self._current_page - 1)
    
    def _navigate_next(self):
        """Navigate to next page."""
        self._navigate_to_page(self._current_page + 1)
    
    def _navigate_to_page(self, target_page):
        """Navigate to specific page."""
        if 0 <= target_page <= self._total_pages:
            self._current_page = target_page
            self._update_page_display()
            self._window.update_displayed_items()
    
    def _update_page_display(self):
        """Update page display text."""
        if hasattr(self, '_page_text_widget') and self._page_text_widget:
            self._page_text_widget.SetText(str(self._current_page + 1))
    
    def set_page_info(self, current_page, total_pages):
        """Set current page information."""
        self._current_page = current_page
        self._total_pages = total_pages
        self._update_page_display()
    
    def get_current_page(self):
        """Get current page number."""
        return self._current_page
    
    def reset_to_first_page(self):
        """Reset to first page."""
        self._current_page = 0
        self._update_page_display()


class DropDataManager(object):
    """Manages drop data storage and retrieval."""
    
    def __init__(self):
        self._drop_dict = {}
        self._current_item_vnum = -1
    
    def clear_data(self):
        """Clear all drop data."""
        self._drop_dict.clear()
        self._current_item_vnum = -1
    
    def set_item_vnum(self, item_vnum):
        """Set current item vnum."""
        self._current_item_vnum = item_vnum
    
    def get_item_vnum(self):
        """Get current item vnum."""
        return self._current_item_vnum
    
    def load_drop_data(self, item_vnum, is_main_drop):
        """Load drop data for specified item."""
        self._current_item_vnum = item_vnum
        
        # Get drop information from item system
        page_count, drop_list = item.GetDropInfo(item_vnum, is_main_drop)
        
        # Clear existing data
        self._drop_dict.clear()
        
        # Initialize empty pages
        for page in range(page_count + 1):
            self._drop_dict[page] = {}
        
        # Populate drop data
        for page, position, vnum, count in drop_list:
            self._drop_dict[page][position] = (vnum, count)
        
        return page_count
    
    def get_drop_data_for_page(self, page):
        """Get drop data for specific page."""
        return self._drop_dict.get(page, {})
    
    def get_drop_data_at_slot(self, page, slot_index):
        """Get drop data at specific slot."""
        page_data = self.get_drop_data_for_page(page)
        return page_data.get(slot_index)


class ChestDropInfoWindow(ui.ScriptWindow):
    """Main window for displaying chest drop information."""
    
    def __init__(self):
        super(ChestDropInfoWindow, self).__init__()
        
        self._is_loaded = False
        self._current_item_vnum = -1
        
        self._slot_manager = ItemSlotManager(self)
        self._navigation_manager = NavigationManager(self)
        self._data_manager = DropDataManager()
        
        self._main_item_slot = None
        self._drop_item_slot = None
        self._prev_button = None
        self._next_button = None
        self._current_page_text = None
        self._back_button = None
        self._title_widget = None
    
    def __del__(self):
        super(ChestDropInfoWindow, self).__del__()
        self._cleanup_resources()
    
    def _cleanup_resources(self):
        """Clean up all resources."""
        if self._slot_manager:
            self._slot_manager.cleanup()
        
        # Clear references
        self._slot_manager = None
        self._navigation_manager = None
        self._data_manager = None
        self._main_item_slot = None
        self._drop_item_slot = None
        self._prev_button = None
        self._next_button = None
        self._current_page_text = None
        self._back_button = None
        self._title_widget = None
    
    def _load_window(self):
        """Load the window if not already loaded."""
        if self._is_loaded:
            return
        
        self._is_loaded = True
        
        try:
            self._load_script()
            self._bind_ui_objects()
            self._bind_events()
        except Exception:
            import exception
            exception.Abort("ChestDropInfoWindow._load_window")
    
    def _load_script(self):
        """Load UI script file."""
        script_loader = ui.PythonScriptLoader()
        script_loader.LoadScriptFile(self, ChestDropConstants.SCRIPT_PATH)
    
    def _bind_ui_objects(self):
        """Bind UI objects from script."""
        self._main_item_slot = self.GetChild("main_item_slot")
        self._drop_item_slot = self.GetChild("drop_item_slot")
        self._prev_button = self.GetChild("prev_button")
        self._next_button = self.GetChild("next_button")
        self._current_page_text = self.GetChild("CurrentPage")
        self._back_button = self.GetChild("BackBtn")
        self._title_widget = self.GetChild("TitleName")
        
        title_bar = self.GetChild("TitleBar")
        title_bar.SetCloseEvent(ui.__mem_func__(self.Close))
    
    def _bind_events(self):
        """Bind UI events."""
        # Setup slot managers
        self._slot_manager.setup_main_item_slot(self._main_item_slot)
        self._slot_manager.setup_drop_item_slot(self._drop_item_slot)
        
        # Setup navigation
        self._navigation_manager.setup_navigation_buttons(
            self._prev_button, self._next_button, self._current_page_text
        )
        
        # Setup back button
        self._back_button.SetEvent(ui.__mem_func__(self._handle_back_button))
    
    def _should_show_back_button(self):
        """Determine if back button should be shown."""
        last_chest_vnum = getattr(constInfo, 'LAST_CHESTINFO_VNUM', 0)
        
        if last_chest_vnum == 0:
            return False
        
        if str(self._current_item_vnum) == str(last_chest_vnum):
            return False
        
        item.SelectItem(int(last_chest_vnum))
        item_type = item.GetItemType()
        
        return item_type in (item.GIFTBOX, item.GACHA)
    
    def _update_back_button_visibility(self):
        """Update back button visibility."""
        if self._should_show_back_button():
            self._back_button.Show()
        else:
            self._back_button.Hide()
    
    def _handle_back_button(self):
        """Handle back button click."""
        last_chest_vnum = getattr(constInfo, 'LAST_CHESTINFO_VNUM', 0)
        if last_chest_vnum == 0:
            return
        
        is_main_drop = not app.IsPressed(app.DIK_LSHIFT)
        
        self.open_chest_info(last_chest_vnum, is_main_drop)
        
        constInfo.LAST_CHESTINFO_VNUM = 0
        self._back_button.Hide()
    
    def handle_drop_item_use(self, slot_index):
        """Handle drop item slot usage (right-click)."""
        # Store current item as last viewed
        constInfo.LAST_CHESTINFO_VNUM = self._current_item_vnum
        
        # Get the item data at the clicked slot
        current_page = self._navigation_manager.get_current_page()
        drop_data = self._data_manager.get_drop_data_at_slot(current_page, slot_index)
        
        if not drop_data:
            return
        
        item_vnum = drop_data[ChestDropConstants.ITEM_INDEX]
        
        # Check if the item is a chest/gacha that can be opened
        item.SelectItem(item_vnum)
        item_type = item.GetItemType()
        
        if item_type in (item.GIFTBOX, item.GACHA):
            # Only open if Ctrl is pressed
            if app.IsPressed(app.DIK_LCONTROL):
                is_main_drop = not app.IsPressed(app.DIK_LSHIFT)
                
                # Check if item has drop info before opening
                if item.HasDropInfo(item_vnum, is_main_drop):
                    self.open_chest_info(item_vnum, is_main_drop)
    
    def get_drop_data_at_slot(self, slot_index):
        """Get drop data at specific slot for current page."""
        current_page = self._navigation_manager.get_current_page()
        return self._data_manager.get_drop_data_at_slot(current_page, slot_index)
    
    def update_displayed_items(self):
        """Update items displayed in drop slots."""
        # Clear all slots first
        for i in range(ChestDropConstants.DROP_SLOT_SIZE):
            self._drop_item_slot.ClearSlot(i)
        
        # Get current page data
        current_page = self._navigation_manager.get_current_page()
        page_data = self._data_manager.get_drop_data_for_page(current_page)
        
        # Set items for current page
        for slot_pos, drop_data in page_data.items():
            item_vnum = drop_data[ChestDropConstants.ITEM_INDEX]
            item_count = drop_data[ChestDropConstants.COUNT_INDEX]
            self._drop_item_slot.SetItemSlot(slot_pos, item_vnum, item_count)
        
        # Refresh the slot display
        self._drop_item_slot.RefreshSlot()
    
    def _setup_window_content(self, item_vnum, is_main_drop):
        """Setup window content for specified item."""
        self._current_item_vnum = item_vnum
        
        self._main_item_slot.SetItemSlot(0, item_vnum, 0)
        self._main_item_slot.RefreshSlot()
        
        item.SelectItem(item_vnum)
        item_name = item.GetItemName()
        self._title_widget.SetText(item_name)
        
        page_count = self._data_manager.load_drop_data(item_vnum, is_main_drop)
        
        self._navigation_manager.set_page_info(0, page_count)
        self._navigation_manager.reset_to_first_page()
        
        self.update_displayed_items()
        self._update_back_button_visibility()
    
    def open_chest_info(self, item_vnum, is_main_drop=True):
        """Open chest drop info for specified item."""
        # Set global state
        constInfo.CHESTDROP_INFO_IS_OPEN = 1
        
        # Close if already open
        if self.IsShow():
            self.Close()
        
        # Load window and setup content
        self._load_window()
        self._setup_window_content(item_vnum, is_main_drop)
        
        # Show window
        self.SetTop()
        self.Show()
    
    def Close(self):
        """Close the window."""
        constInfo.CHESTDROP_INFO_IS_OPEN = 0
        
        if self._slot_manager:
            self._slot_manager._on_item_hover_out()
        
        self.Hide()
    
    def OnPressEscapeKey(self):
        """Handle escape key press."""
        self.Close()
        return True
    
    # Legacy compatibility methods
    def Open(self, item_vnum, is_main):
        """Legacy method for opening window."""
        self.open_chest_info(item_vnum, is_main)
    
    def SetUp(self, item_vnum, is_main):
        """Legacy method for setting up window."""
        self._setup_window_content(item_vnum, is_main)
    
    def SetPage(self, page_offset):
        """Legacy method for page navigation."""
        current_page = self._navigation_manager.get_current_page()
        target_page = current_page + page_offset
        self._navigation_manager._navigate_to_page(target_page)
    
    def UpdateItems(self):
        """Legacy method for updating items."""
        self.update_displayed_items()
    
    def OverInMainItemSlot(self, slot_index):
        """Legacy method for main item hover."""
        self._slot_manager._on_main_item_hover(slot_index)
    
    def OverInDropItemSlot(self, slot_index):
        """Legacy method for drop item hover."""
        self._slot_manager._on_drop_item_hover(slot_index)
    
    def OverOutItem(self):
        """Legacy method for item hover out."""
        self._slot_manager._on_item_hover_out()
    
    def UseSlotEvent(self, slot_index):
        """Legacy method for slot usage."""
        self.handle_drop_item_use(slot_index)
    
    def BackBtn(self):
        """Legacy method for back button."""
        self._handle_back_button()
    
    def BtnCheck(self):
        """Legacy method for button check."""
        self._update_back_button_visibility()
    
    def SetItemToolTip(self, tooltip):
        """Legacy method for setting tooltip."""
        pass


def unsigned32(n):
    """Utility function for 32-bit unsigned integer conversion."""
    return n & 0xFFFFFFFF
	