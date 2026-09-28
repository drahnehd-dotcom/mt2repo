import ui
import player
import net
import item
import uiToolTip

CHEST_ITEMS = {}


class CasketItemWidget(ui.BoxedBoard):
    """Individual item widget for displaying casket contents."""
    
    # Class constants
    ITEM_SIZE = (134, 134)
    ITEM_Y_OFFSET = 200
    ITEM_SLOT_SIZE = 32
    NAME_PANEL_HEIGHT = 34
    NAME_PANEL_Y_OFFSET = 100
    IMAGE_Y_OFFSET = -16
    
    def __init__(self, item_vnum, item_count):
        super(CasketItemWidget, self).__init__()
        self._item_vnum = item_vnum
        self._item_count = item_count
        self._tooltip = None
        self._name_background = None
        self._item_name_label = None
        self._item_image_slot = None
        
        self._initialize_widget()
        self._setup_item_display()
    
    def _initialize_widget(self):
        """Initialize the base widget properties."""
        self.SetSize(*self.ITEM_SIZE)
        item.SelectItem(self._item_vnum)
    
    def _setup_item_display(self):
        """Setup all visual components for the item display."""
        self._create_name_background()
        self._create_name_label()
        self._create_item_image()
        self._create_tooltip()
    
    def _create_name_background(self):
        """Create the background panel for item name."""
        self._name_background = ui.BoxedBoard()
        self._name_background.SetParent(self)
        self._name_background.SetPosition(0, self.NAME_PANEL_Y_OFFSET)
        self._name_background.SetSize(self.ITEM_SIZE[0], self.NAME_PANEL_HEIGHT)
        self._name_background.Show()
    
    def _create_name_label(self):
        """Create and configure the item name label."""
        self._item_name_label = ui.TextLine()
        self._item_name_label.SetParent(self._name_background)
        self._item_name_label.SetPosition(0, 0)
        
        # Configure text properties
        self._item_name_label.SetOutline()
        self._item_name_label.SetFeather()
        self._item_name_label.SetLimitWidth(self.ITEM_SIZE[0])
        self._item_name_label.SetMultiLine()
        self._item_name_label.SetWindowHorizontalAlignCenter()
        self._item_name_label.SetHorizontalAlignCenter()
        
        # Set the formatted text with count and name
        item_name = item.GetItemName()
        formatted_text = "{}x {}".format(self._item_count, item_name)
        self._item_name_label.SetText(formatted_text)
        self._item_name_label.Show()
    
    def _create_item_image(self):
        """Create the item image slot."""
        item_height = item.GetItemSize()[1] * self.ITEM_SLOT_SIZE
        
        self._item_image_slot = ui.SlotWindow()
        self._item_image_slot.SetParent(self)
        self._item_image_slot.SetWindowHorizontalAlignCenter()
        self._item_image_slot.SetWindowVerticalAlignCenter()
        self._item_image_slot.SetPosition(0, self.IMAGE_Y_OFFSET)
        self._item_image_slot.AppendSlot(0, 0, 0, self.ITEM_SLOT_SIZE, item_height)
        self._item_image_slot.SetSize(self.ITEM_SLOT_SIZE, item_height)
        
        self._item_image_slot.SetOverInItemEvent(ui.__mem_func__(self._on_mouse_over_item))
        self._item_image_slot.SetOverOutItemEvent(ui.__mem_func__(self._on_mouse_out_item))
        
        self._item_image_slot.SetItemSlot(0, self._item_vnum, 0)
        self._item_image_slot.RefreshSlot()
        self._item_image_slot.Show()
    
    def _create_tooltip(self):
        """Create the tooltip for this item."""
        self._tooltip = uiToolTip.ItemToolTip()
    
    def _on_mouse_over_item(self):
        """Handle mouse over event to show tooltip."""
        if self._tooltip:
            self._tooltip.SetItemToolTip(self._item_vnum)
            self._tooltip.ShowToolTip()
    
    def _on_mouse_out_item(self):
        """Handle mouse out event to hide tooltip."""
        if self._tooltip:
            self._tooltip.HideToolTip()
    
    def cleanup(self):
        """Clean up resources."""
        self._name_background = None
        self._item_image_slot = None
        self._item_name_label = None
        self._tooltip = None
        self._item_vnum = 0
        self._item_count = 0
    
    def __del__(self):
        super(CasketItemWidget, self).__del__()
        self.cleanup()


class CasketDialog(ui.ScriptWindow):
    """Main dialog for displaying casket contents with pagination."""
    
    # Class constants
    MAX_ITEMS_PER_PAGE = 4
    ITEM_Y_POSITION = 200
    ITEM_X_START = 24
    TOOLTIP_Y_OFFSET = 30
    ARROW_Y_OFFSET = 30
    
    def __init__(self):
        super(CasketDialog, self).__init__()
        self._reset_state()
        self._load_ui()
    
    def _reset_state(self):
        """Reset all internal state variables."""
        self._item_widgets = []
        self._current_page = 0
        self._current_slot = -1
        self._current_vnum = 0
        self._is_by_vnum = False
        
        self._item_slot = None
        self._prev_button = None
        self._next_button = None
        self._tooltip = None
        self._arrow_image = None
    
    def _load_ui(self):
        """Load the UI script and setup components."""
        script_loader = ui.PythonScriptLoader()
        script_loader.LoadScriptFile(self, "UIScript/casketwindow.py")
        
        self._setup_ui_components()
        self._setup_tooltip()
    
    def _setup_ui_components(self):
        """Setup main UI components and their events."""
        title_bar = self.GetChild("TitleBar")
        title_bar.SetCloseEvent(self.Hide)
        
        self._item_slot = self.GetChild("ItemSlot")
        
        self._prev_button = self.GetChild("PrevButton")
        self._next_button = self.GetChild("NextButton")
        self._prev_button.SetEvent(ui.__mem_func__(self._navigate_previous_page))
        self._next_button.SetEvent(ui.__mem_func__(self._navigate_next_page))
        
        self._arrow_image = self.GetChild("ItemArrow")
    
    def _setup_tooltip(self):
        """Setup the main tooltip component."""
        self._tooltip = uiToolTip.ItemToolTip()
        self._tooltip.SetParent(self)
        self._tooltip.SetPosition(0, self.TOOLTIP_Y_OFFSET)
        self._tooltip.SetFollow(False)
        self._tooltip.SetWindowHorizontalAlignCenter()
    
    def _navigate_next_page(self):
        """Navigate to the next page of items."""
        next_page = self._get_current_page() + self.MAX_ITEMS_PER_PAGE
        if next_page < self._get_total_item_count():
            self._set_current_page(next_page)
    
    def _navigate_previous_page(self):
        """Navigate to the previous page of items."""
        previous_page = self._get_current_page() - self.MAX_ITEMS_PER_PAGE
        if previous_page >= 0:
            self._set_current_page(previous_page)
    
    def _get_current_page(self):
        """Get the current page index."""
        return self._current_page
    
    def _set_current_page(self, page):
        """Set the current page and refresh display."""
        # Hide current page items
        current_end = self._current_page + self.MAX_ITEMS_PER_PAGE
        for widget in self._item_widgets[self._current_page:current_end]:
            widget.Hide()
        
        self._current_page = page
        self._refresh_current_page()
    
    def _get_total_item_count(self):
        """Get the total number of items."""
        return len(self._item_widgets)
    
    def _refresh_current_page(self):
        """Refresh the display of the current page."""
        page_end = self._current_page + self.MAX_ITEMS_PER_PAGE
        
        for index, widget in enumerate(self._item_widgets[self._current_page:page_end]):
            x_position = self.ITEM_X_START + (CasketItemWidget.ITEM_SIZE[0] * index)
            widget.SetPosition(x_position, self.ITEM_Y_POSITION)
            widget.Show()
    
    def _create_item_widgets(self, item_vnum):
        """Create widgets for all items in the casket."""
        self._item_widgets = []
        
        if item_vnum in CHEST_ITEMS:
            for vnum, count in CHEST_ITEMS[item_vnum]:
                widget = CasketItemWidget(vnum, count)
                widget.SetParent(self)
                self._item_widgets.append(widget)
    
    def _setup_main_item_display(self):
        """Setup the main item display and tooltip."""
        if self._is_by_vnum:
            self._tooltip.ClearToolTip()
            self._tooltip.SetItemToolTip(self._current_vnum)
        else:
            self._tooltip.ClearToolTip()
            self._tooltip.SetInventoryItem(self._current_slot)
        
        self._tooltip.SetWindowHorizontalAlignCenter()
        self._tooltip.Show()
        
        # Position arrow based on tooltip height
        arrow_y = (self._tooltip.GetHeight() + 
                  self._arrow_image.GetHeight() // 2 + 
                  self.ARROW_Y_OFFSET)
        self._arrow_image.SetPosition(0, arrow_y)
        
        # Setup item slot
        self._item_slot.SetItemSlot(0, self._current_vnum, 0)
        self._item_slot.RefreshSlot()
    
    def _request_casket_data(self):
        """Request casket data from server."""
        net.SendChatPacket("/fetch_casket_items {}".format(self._current_vnum))
    
    def _show_dialog(self):
        """Show the dialog and bring it to front."""
        self.SetTop()
        self.Show()
    
    # Public interface methods
    
    def load_item_from_slot(self, slot_index):
        """Load casket contents from an inventory slot."""
        self._current_page = 0
        self._current_slot = slot_index
        self._current_vnum = player.GetItemIndex(slot_index)
        self._is_by_vnum = False
        self.build_display()
    
    def load_item_by_vnum(self, item_vnum):
        """Load casket contents by item vnum."""
        self._current_page = 0
        self._current_vnum = item_vnum
        self._is_by_vnum = True
        self.build_display()
    
    def add_item_to_registry(self, base_vnum, item_vnum, count):
        """Add an item to the global casket registry."""
        if base_vnum not in CHEST_ITEMS:
            CHEST_ITEMS[base_vnum] = []
        
        CHEST_ITEMS[base_vnum].append([item_vnum, count])
    
    def build_display(self):
        """Build and display the casket contents."""
        if self._current_vnum == 0:
            return
        
        if self._current_slot == -1 and not self._is_by_vnum:
            return
        
        if self._current_vnum in CHEST_ITEMS:
            self._create_item_widgets(self._current_vnum)
            self._setup_main_item_display()
            self._refresh_current_page()
            self._show_dialog()
        else:
            self._request_casket_data()
    
    def destroy(self):
        """Clean up and destroy the dialog."""
        self.cleanup()
        self.ClearDictionary()
        self.Hide()
    
    def cleanup(self):
        """Clean up all resources."""
        # Clean up item widgets
        for widget in self._item_widgets:
            widget.cleanup()
        
        self._reset_state()
    
    def OnPressEscapeKey(self):
        """Handle escape key press."""
        self.Hide()
        return True
    
    def __del__(self):
        super(CasketDialog, self).__del__()
        self.cleanup()


CasketDialog.CasketItem = CasketItemWidget
