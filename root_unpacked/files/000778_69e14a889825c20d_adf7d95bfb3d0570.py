# -*- coding: iso-8859-1 -*-
import ui
import dbg
import app
import chat
import player
import os
import net
import json
from _weakref import proxy
import uiToolTip
import localeInfo
import exchange

SLOT_X_COUNT = 8
SLOT_Y_COUNT = 3
CHECKED_SLOTS_COUNT = SLOT_X_COUNT * SLOT_Y_COUNT

SLOT_COUNTS = [SLOT_X_COUNT] * SLOT_Y_COUNT
Y_POSITIONS = [40, 72, 102]
CHECKBOX_START_X = 22
CHECKBOX_SPACING = 32

DEFAULT_ITEM_IDS = [
    80400, 80401, 80402, 80403, 80404, 80405, 80406, 80407, 80408,
    50835, 50837, 50838, 50839, 50840, 71016
]


class CheckBox(ui.ImageBox):
    """Custom checkbox widget with on/off states."""
    
    def __init__(self, parent, x, y, event, filename="d:/ymir work/ui/dop_off.png"):
        super(CheckBox, self).__init__()
        self._initialize_attributes(parent, x, y, event, filename)
        self._create_ui_components()

    def _initialize_attributes(self, parent, x, y, event, filename):
        """Initialize all instance attributes."""
        self.Enable = True
        self.event = event
        self.image = None
        
        self.SetParent(parent)
        self.SetPosition(x, y)
        self.LoadImage(filename)

    def _create_ui_components(self):
        """Create the checkbox UI components."""
        self.image = ui.MakeImageBox(self, "d:/ymir work/ui/dop_on.png", 0, 0)
        if self.image:
            self.image.AddFlag("not_pick")
            self.image.SetWindowHorizontalAlignCenter()
            self.image.SetWindowVerticalAlignCenter()
            self.image.Hide()
        
        self.Show()

    def __del__(self):
        self._cleanup_resources()
        super(CheckBox, self).__del__()

    def _cleanup_resources(self):
        """Clean up resources to prevent memory leaks."""
        if self.image:
            self.image.Hide()
            self.image = None
        self.event = None

    def SetCheck(self, flag):
        """Set checkbox checked state."""
        if self.image:
            if flag:
                self.image.Show()
            else:
                self.image.Hide()

    def IsChecked(self):
        """Check if checkbox is checked."""
        if self.image:
            return self.image.IsShow()
        return False

    def Disable(self):
        """Disable the checkbox."""
        self.Enable = False

    def Enable(self):
        """Enable the checkbox."""
        self.Enable = True

    def OnMouseLeftButtonDown(self):
        """Handle mouse button down event."""
        if not self.Enable:
            return

    def OnMouseLeftButtonUp(self):
        """Handle mouse button up event (trigger checkbox)."""
        if not self.Enable:
            return
        
        if self.event:
            self.event()


class Boosters(ui.ScriptWindow):
    """Auto booster management window."""
    
    def __init__(self):
        super(Boosters, self).__init__()
        self._initialize_attributes()
        self._create_tooltip()
        self.__LoadWindow()

    def _initialize_attributes(self):
        """Initialize all instance attributes."""
        self.isLoaded = False
        
        self.enableDop = {}
        self.itemsID = {}
        self.checkedItems = [0] * CHECKED_SLOTS_COUNT
        self.itemInSlotID = list(DEFAULT_ITEM_IDS)
        
        self.tooltip = None
        self.board = None
        self.wndItem = None
        self.useButton = None
        self.clearButton = None
        self.titleBar = None

    def _create_tooltip(self):
        """Create and setup tooltip."""
        self.tooltip = uiToolTip.ItemToolTip()
        if self.tooltip:
            self.tooltip.Hide()

    def __del__(self):
        self._cleanup_resources()
        super(Boosters, self).__del__()

    def _cleanup_resources(self):
        """Clean up all resources to prevent memory leaks."""
        if self.tooltip:
            self.tooltip.Hide()
            self.tooltip = None
        
        for checkbox in self.enableDop.values():
            if checkbox:
                checkbox.Hide()
        self.enableDop.clear()
        
        self.board = None
        self.wndItem = None
        self.useButton = None
        self.clearButton = None
        self.titleBar = None
        
        self.itemsID.clear()
        self.checkedItems = [0] * CHECKED_SLOTS_COUNT

    def Destroy(self):
        """Destroy the window and clean up all resources."""
        self._cleanup_resources()
        self._initialize_attributes()
        self.Hide()
        self.ClearDictionary()

    def Open(self):
        """Open the window."""
        self.Show()

    def Show(self):
        """Show the window."""
        self.__LoadWindow()
        super(Boosters, self).Show()

    def Close(self):
        """Close the window."""
        self.Hide()

    def OnPressExitKey(self):
        """Handle exit key press."""
        self.Hide()
        return True

    def OnPressEscapeKey(self):
        """Handle escape key press."""
        self.Hide()
        return True

    def __LoadWindow(self):
        """Load the window UI components."""
        if self.isLoaded:
            return
            
        self.isLoaded = True
        
        try:
            self._load_script()
            self._load_ui_components()
            self._setup_item_slots()
            self._setup_checkboxes()
            self._setup_event_handlers()
            self._load_saved_settings()
            self._finalize_setup()
        except Exception:
            import exception
            exception.Abort("DopalaczeWindow.__LoadWindow.BindObject")

    def _load_script(self):
        """Load the UI script file."""
        try:
            ui.PythonScriptLoader().LoadScriptFile(self, "uiscript/dopalaczewindow.py")
        except Exception:
            import exception
            exception.Abort("DopalaczeWindow.__LoadWindow.LoadObject")

    def _load_ui_components(self):
        """Load all UI components from the script."""
        self.board = self.GetChild("board")
        self.wndItem = self.GetChild("item_slot")
        self.useButton = self.GetChild("use_button")
        self.clearButton = self.GetChild("clear_button")
        self.titleBar = self.GetChild("TitleBar")

    def _setup_item_slots(self):
        """Setup item slots with booster items."""
        if self.wndItem:
            for i, item_id in enumerate(self.itemInSlotID):
                self.wndItem.SetItemSlot(i, item_id, 0)

    def _setup_checkboxes(self):
        """Setup checkboxes for each booster item."""
        if not self.board:
            return
            
        for j, slot_count in enumerate(SLOT_COUNTS):
            y_position = Y_POSITIONS[j]
            
            for i in range(slot_count):
                index = i + sum(SLOT_COUNTS[:j])
                x_position = CHECKBOX_START_X + i * CHECKBOX_SPACING
                
                # Create checkbox with proper event closure
                event = self._create_checkbox_event(index)
                checkbox = CheckBox(self.board, x_position, y_position, event)
                
                # Setup mouse events with proper closures
                checkbox.OnMouseOverIn = self._create_mouse_over_handler(index)
                checkbox.OnMouseOverOut = self.OverOutItem
                
                self.enableDop[index] = checkbox

    def _create_checkbox_event(self, index):
        """Create checkbox event handler with proper closure."""
        def handler():
            self.OnEnableGeneral(index)
        return handler

    def _create_mouse_over_handler(self, index):
        """Create mouse over handler with proper closure."""
        def handler():
            self.OverInItem(index)
        return handler

    def _setup_event_handlers(self):
        """Setup all event handlers."""
        if self.titleBar:
            self.titleBar.SetCloseEvent(ui.__mem_func__(self.Close))
        
        if self.useButton:
            self.useButton.SetEvent(ui.__mem_func__(self.btnUse))
        
        if self.clearButton:
            self.clearButton.SetEvent(ui.__mem_func__(self.btnClear))

    def _load_saved_settings(self):
        """Load saved checkbox settings from JSON file."""
        self._ensure_config_directory()
        
        config_path = self._get_config_path()
        if os.path.exists(config_path):
            try:
                # Otwórz plik w sposób kompatybilny ze starszym Pythonem
                file_handle = None
                try:
                    file_handle = open(config_path, "r")
                    data = json.load(file_handle)
                    
                    # Load checked items
                    if "checked_items" in data:
                        checked_items = data["checked_items"]
                        for i, checked in enumerate(checked_items):
                            if i < len(self.checkedItems):
                                self.checkedItems[i] = int(checked)
                                if i in self.enableDop:
                                    self.enableDop[i].SetCheck(bool(self.checkedItems[i]))
                    
                    # Load custom item IDs if present
                    if "item_ids" in data and len(data["item_ids"]) == len(self.itemInSlotID):
                        self.itemInSlotID = data["item_ids"]
                        self._refresh_item_slots()
                        
                except (IOError, ValueError, KeyError) as e:
                    # JSON parse error or file read error, use defaults
                    chat.AppendChat(chat.CHAT_TYPE_INFO, "Failed to load booster settings: using defaults")
                finally:
                    # Zawsze zamknij plik jeśli został otwarty
                    if file_handle:
                        try:
                            file_handle.close()
                        except:
                            pass
                            
            except Exception:
                # Ogólny błąd - użyj domyślnych ustawień
                chat.AppendChat(chat.CHAT_TYPE_INFO, "Error loading booster settings: using defaults")

    def _refresh_item_slots(self):
        """Refresh item slots display after loading custom IDs."""
        if self.wndItem:
            for i, item_id in enumerate(self.itemInSlotID):
                self.wndItem.SetItemSlot(i, item_id, 0)

    def _ensure_config_directory(self):
        """Ensure configuration directory exists."""
        if not os.path.exists('_cfg'):
            try:
                os.makedirs('_cfg')
            except OSError:
                pass

    def _get_config_path(self):
        """Get configuration file path for current player."""
        return '_cfg/dopalacze_%s.json' % player.GetName()

    def _finalize_setup(self):
        """Finalize window setup."""
        self.SetCenterPosition()
        self.SetTop()

    def OnEnableGeneral(self, arg):
        """Handle checkbox toggle for booster item."""
        if arg >= len(self.itemInSlotID) or arg not in self.enableDop:
            return

        checkbox = self.enableDop[arg]
        
        if checkbox.IsChecked():
            checkbox.SetCheck(False)
            self.checkedItems[arg] = 0
        else:
            checkbox.SetCheck(True)
            self.checkedItems[arg] = 1

        self._save_settings()

    def _save_settings(self):
        """Save current checkbox settings to JSON file."""
        self._ensure_config_directory()
        
        # Prepare data structure
        data = {
            "version": "1.0",
            "player_name": player.GetName(),
            "checked_items": self.checkedItems[:len(self.itemInSlotID)],
            "item_ids": self.itemInSlotID,
            "last_modified": app.GetGlobalTimeStamp()
        }
        
        config_path = self._get_config_path()
        
        # Zapisz plik w sposób kompatybilny ze starszym Pythonem
        file_handle = None
        try:
            file_handle = open(config_path, "w")
            json.dump(data, file_handle, indent=2)
        except IOError:
            chat.AppendChat(chat.CHAT_TYPE_INFO, "Failed to save booster settings")
        finally:
            if file_handle:
                try:
                    file_handle.close()
                except:
                    pass

    def btnUse(self):
        """Use selected booster items."""
        to_use_items = self._get_selected_items()
        
        if not to_use_items['ids']:
            chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.BLEND_WINDOW_1)
            return

        if not to_use_items['slots']:
            chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.BLEND_WINDOW_2)
            return

        if not self._can_use_items():
            return

        for slot in to_use_items['slots']:
            net.SendItemUsePacket(slot)

    def _get_selected_items(self):
        """Get selected item IDs and their inventory slots."""
        selected_ids = []
        selected_slots = []
        
        for i in range(len(self.itemInSlotID)):
            if i < len(self.checkedItems) and int(self.checkedItems[i]) == 1:
                item_id = self.itemInSlotID[i]
                selected_ids.append(item_id)
                
                # Find item in inventory
                item_index = player.GetItemFirstIndexByVnum(item_id)
                if item_index != -1:
                    selected_slots.append(item_index)
        
        return {'ids': selected_ids, 'slots': selected_slots}

    def _can_use_items(self):
        """Check if items can be used (not trading, not in offline shop, etc.)."""
        if exchange.isTrading():
            return False

        return True

    def btnClear(self):
        """Clear all checkbox selections."""
        # Update checkboxes
        for i in range(len(self.itemInSlotID)):
            if i < len(self.checkedItems):
                self.checkedItems[i] = 0
            
            if i in self.enableDop:
                self.enableDop[i].SetCheck(False)

        # Save cleared settings
        self._save_settings()

    def OverInItem(self, overSlotPos):
        """Handle mouse over item event."""
        if (self.tooltip and 
            0 <= overSlotPos < len(self.itemInSlotID)):
            self.tooltip.SetItemToolTip(self.itemInSlotID[overSlotPos])
            self.tooltip.Show()

    def OverOutItem(self):
        """Handle mouse out item event."""
        if self.tooltip:
            self.tooltip.HideToolTip()

    def GetCheckedItems(self):
        """Get list of currently checked items."""
        return [i for i, checked in enumerate(self.checkedItems) if checked]

    def SetItemEnabled(self, index, enabled):
        """Enable or disable specific item checkbox."""
        if index in self.enableDop:
            if enabled:
                self.enableDop[index].Enable()
            else:
                self.enableDop[index].Disable()

    def GetItemInSlotID(self, index):
        """Get item ID for specific slot index."""
        if 0 <= index < len(self.itemInSlotID):
            return self.itemInSlotID[index]
        return None

    def SetItemInSlotID(self, index, item_id):
        """Set item ID for specific slot index."""
        if 0 <= index < len(self.itemInSlotID):
            self.itemInSlotID[index] = item_id
            if self.wndItem:
                self.wndItem.SetItemSlot(index, item_id, 0)
            # Auto-save when item IDs change
            self._save_settings()

    def LoadCustomItemIDs(self, item_ids):
        """Load custom item IDs list."""
        if len(item_ids) == len(self.itemInSlotID):
            self.itemInSlotID = list(item_ids)
            self._refresh_item_slots()
            self._save_settings()
            return True
        return False

    def ResetToDefaultItems(self):
        """Reset to default item IDs."""
        self.itemInSlotID = list(DEFAULT_ITEM_IDS)
        self._refresh_item_slots()
        self._save_settings()

    def ExportSettings(self):
        """Export settings as JSON string for sharing."""
        data = {
            "checked_items": self.checkedItems[:len(self.itemInSlotID)],
            "item_ids": self.itemInSlotID,
            "version": "1.0"
        }
        try:
            return json.dumps(data, indent=2)
        except (TypeError, ValueError):
            return None

    def ImportSettings(self, json_string):
        """Import settings from JSON string."""
        try:
            data = json.loads(json_string)
            
            if "checked_items" in data:
                for i, checked in enumerate(data["checked_items"]):
                    if i < len(self.checkedItems):
                        self.checkedItems[i] = int(checked)
                        if i in self.enableDop:
                            self.enableDop[i].SetCheck(bool(self.checkedItems[i]))
            
            if "item_ids" in data and len(data["item_ids"]) == len(self.itemInSlotID):
                self.itemInSlotID = data["item_ids"]
                self._refresh_item_slots()
            
            self._save_settings()
            return True
            
        except (ValueError, KeyError, TypeError):
            return False
			