# -*- coding: utf-8 -*-
"""Artifact equipment window - interface for managing artifact slots."""

import ui
import item
import uiToolTip
import player
import constInfo
import net
import mouseModule
import snd

UI_SCRIPT_PATH = "uiscript/artifactsystemwindow.py"
PICK_SOUND_PATH = "sound/ui/pick.wav"


class ArtifactWindow(ui.ScriptWindow):
    """Window for managing artifact equipment slots."""

    def __init__(self):
        ui.ScriptWindow.__init__(self)
        self._is_loaded = False
        self._tooltip_item = None
        self._artifact_slots = None
        self._board = None
        self._initialize_tooltip()
        self._attempt_load_window()

    def __del__(self):
        self._cleanup_tooltip()
        ui.ScriptWindow.__del__(self)

    def Destroy(self):
        """Teardown wolany z interfacemodule.Close() przy wylogowaniu.

        Bez tego dziedziczone ui.Window.Destroy() jest pustym 'pass', wiec okno
        zostaje zarejestrowane w wndMgr i widoczne na ekranie wyboru postaci.
        """
        self.Hide()
        self._cleanup_tooltip()
        self._artifact_slots = None
        self._board = None
        self._is_loaded = False
        self.ClearDictionary()

    def _initialize_tooltip(self):
        """Initialize tooltip component."""
        try:
            self._tooltip_item = uiToolTip.ItemToolTip()
            self._tooltip_item.Hide()
        except Exception as e:
            self._log_error("Failed to initialize tooltip", e)

    def _cleanup_tooltip(self):
        """Clean up tooltip resources."""
        if self._tooltip_item:
            self._tooltip_item.Hide()
            self._tooltip_item = None

    def _attempt_load_window(self):
        """Attempt to load window on initialization."""
        try:
            self._load_window()
        except Exception as e:
            self._log_error("Failed to load window during initialization", e)

    def Open(self):
        """Open the artifact window."""
        if self._is_loaded:
            self._refresh_slot()
            self.Show()
        else:
            self._load_window()
            if self._is_loaded:
                self.Show()

    def Close(self):
        """Close the artifact window."""
        self.Hide()

    def OnPressEscapeKey(self):
        self.Close()
        return True

    def _load_window(self):
        """Load window UI from script file."""
        if self._is_loaded:
            return

        try:
            self._load_ui_script()
            self._setup_ui_components()
            self._finalize_window_setup()
            self._is_loaded = True
        except Exception as e:
            self._log_error("Failed to load window", e)

    def _load_ui_script(self):
        """Load UI script file."""
        try:
            py_scr_loader = ui.PythonScriptLoader()
            py_scr_loader.LoadScriptFile(self, UI_SCRIPT_PATH)
        except Exception:
            import exception
            exception.Abort("ArtifactSystemWindow.LoadWindow.LoadObject")
            raise

    def _setup_ui_components(self):
        """Setup UI components and event handlers."""
        self._board = self.GetChild("Board")

        title_bar = self.GetChild("TitleBar")
        title_bar.SetCloseEvent(ui.__mem_func__(self.Close))

        self._setup_artifact_slots()

    def _setup_artifact_slots(self):
        """Setup artifact slots with event handlers."""
        artifact_slots = self.GetChild("ArtifactSlots")

        event_mappings = [
            ("SetOverInItemEvent", self._on_over_in_item),
            ("SetOverOutItemEvent", self._on_over_out_item),
            ("SetUseSlotEvent", self._on_use_item),
            ("SetUnselectItemSlotEvent", self._on_use_item),
            ("SetSelectEmptySlotEvent", self._on_select_empty_slot),
            ("SetSelectItemSlotEvent", self._on_select_empty_slot),
        ]

        for method_name, handler in event_mappings:
            try:
                getattr(artifact_slots, method_name)(ui.__mem_func__(handler))
            except AttributeError as e:
                self._log_error("Failed to set event handler: {}".format(method_name), e)

        self._artifact_slots = artifact_slots

    def _finalize_window_setup(self):
        """Finalize window setup."""
        self._refresh_slot()
        self.SetCenterPosition()

    def _on_over_in_item(self, slot):
        """Handle mouse over item event."""
        if self._tooltip_item:
            try:
                self._tooltip_item.SetInventoryItem(slot)
                self._tooltip_item.Show()
            except Exception as e:
                self._log_error("Failed to show tooltip for slot {}".format(slot), e)

    def _on_over_out_item(self):
        """Handle mouse out item event."""
        if self._tooltip_item:
            try:
                self._tooltip_item.HideToolTip()
            except Exception as e:
                self._log_error("Failed to hide tooltip", e)

    def _on_select_empty_slot(self, slot):
        """Handle selection of empty slot."""
        try:
            if mouseModule.mouseController.isAttached():
                self._handle_attached_item_placement(slot)
            else:
                self._handle_item_pickup(slot)
        except Exception as e:
            self._log_error("Failed to handle empty slot selection for slot {}".format(slot), e)

    def _handle_attached_item_placement(self, slot):
        """Handle placement of attached item."""
        attached_slot_type = mouseModule.mouseController.GetAttachedType()
        attached_slot_number = mouseModule.mouseController.GetAttachedSlotNumber()

        if not self._is_valid_artifact_item(attached_slot_number):
            return

        if attached_slot_type == player.SLOT_TYPE_INVENTORY:
            self._place_item_in_slot(attached_slot_number)

    def _is_valid_artifact_item(self, slot_number):
        """Check if item is a valid artifact."""
        try:
            vnum = player.GetItemIndex(slot_number)
            item.SelectItem(vnum)
            return item.GetItemType() == item.ARTEFAKT
        except Exception as e:
            self._log_error("Failed to validate artifact item for slot {}".format(slot_number), e)
            return False

    def _place_item_in_slot(self, slot_number):
        """Place item in artifact slot."""
        try:
            net.SendItemUsePacket(slot_number)
            self._on_over_out_item()
            self._refresh_slot()
            mouseModule.mouseController.DeattachObject()
        except Exception as e:
            self._log_error("Failed to place item from slot {}".format(slot_number), e)

    def _handle_item_pickup(self, slot):
        """Handle picking up item from slot."""
        try:
            item_index = player.GetItemIndex(slot)
            item_count = player.GetItemCount(slot)
            mouseModule.mouseController.AttachObject(
                self, player.SLOT_TYPE_INVENTORY, slot, item_index, item_count,
            )
            snd.PlaySound(PICK_SOUND_PATH)
        except Exception as e:
            self._log_error("Failed to pickup item from slot {}".format(slot), e)

    def _on_use_item(self, slot):
        """Handle item use event."""
        try:
            if constInfo.GET_ITEM_QUESTION_DIALOG_STATUS():
                return
        except Exception:
            pass

        try:
            net.SendItemUsePacket(slot)
            mouseModule.mouseController.DeattachObject()
            self._on_over_out_item()
            self._refresh_slot()
        except Exception as e:
            self._log_error("Failed to use item in slot {}".format(slot), e)

    def _refresh_slot(self):
        """Refresh all artifact slots."""
        if not self._artifact_slots:
            return

        try:
            for i in range(item.ARTEFAKT_SLOT_MAX):
                slot_number = item.EQUIPMENT_ARTEFAKT1 + i
                item_index = player.GetItemIndex(slot_number)
                self._artifact_slots.SetItemSlot(slot_number, item_index, 0)
            self._artifact_slots.RefreshSlot()
        except Exception as e:
            self._log_error("Failed to refresh slots", e)

    def _log_error(self, message, error=None):
        """Log error messages."""
        full_message = "ArtifactWindow: {}".format(message)
        if error:
            full_message += " - Error: {}".format(str(error))
        try:
            import dbg
            dbg.TraceError(full_message)
        except ImportError:
            pass

    # Legacy compatibility methods
    def OverInItem(self, slot):
        return self._on_over_in_item(slot)

    def OverOutItem(self):
        return self._on_over_out_item()

    def SelectEmptySlot(self, slot):
        return self._on_select_empty_slot(slot)

    def UseItem(self, slot):
        return self._on_use_item(slot)

    def RefreshSlot(self):
        return self._refresh_slot()


def CreateArtifactWindow():
    """Factory function to create ArtifactWindow instance."""
    try:
        return ArtifactWindow()
    except Exception as e:
        import dbg
        dbg.TraceError("Failed to create ArtifactWindow: {}".format(str(e)))
        return None


# Legacy aliases

