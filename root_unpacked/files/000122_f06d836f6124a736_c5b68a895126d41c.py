#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Modern Loading Window
Rewritten for Python 3 with better maintainability and cleaner code structure
"""

from __future__ import annotations

import ui
import net
import app
import uiScriptLocale
import uiWarpShower


__all__ = [
    "LoadingConstants",
    "BaseLoadingWindow",
    "GameLoadingState",
    "NetworkManager",
    "LoadingWindow",
    "LoadingWindowFactory",
    "create_loading_window",
    "is_performance_loading_enabled",
]


class LoadingConstants:
    """Constants for loading window"""
    SCRIPT_PATH: str = "kowal/ui/loadingwindow.py"
    DEFAULT_FRAME_SKIP_ENABLED: int = 1
    DEFAULT_FRAME_SKIP_DISABLED: int = 0


class BaseLoadingWindow(ui.ScriptWindow):
    """Base class for loading windows with common functionality"""
    
    def __init__(self, stream) -> None:
        super().__init__()
        self.stream = stream
        self.script_loader = ui.PythonScriptLoader()
        self._is_open: bool = False
    
    def __del__(self) -> None:
        """Cleanup on destruction"""
        self._cleanup()
        super().__del__()
    
    def Open(self) -> None:
        """Open the loading window"""
        if self._is_open:
            return
            
        self._load_ui_script()
        self._setup_window()
        self._on_open()
        self._is_open = True
    
    def Close(self) -> None:
        """Close the loading window"""
        if not self._is_open:
            return
            
        self._on_close()
        self._cleanup_ui()
        self._is_open = False
    
    def _load_ui_script(self) -> None:
        """Load UI script file"""
        try:
            self.script_loader.LoadScriptFile(self, LoadingConstants.SCRIPT_PATH)
        except Exception:
            import exception
            exception.Abort("BaseLoadingWindow._load_ui_script - LoadScriptFile Error")
    
    def _setup_window(self) -> None:
        """Setup window properties"""
        self.Show()
        self._set_frame_skip(LoadingConstants.DEFAULT_FRAME_SKIP_DISABLED)
    
    def _cleanup_ui(self) -> None:
        """Clean up UI resources"""
        self._set_frame_skip(LoadingConstants.DEFAULT_FRAME_SKIP_ENABLED)
        self.ClearDictionary()
        self.Hide()
    
    def _cleanup(self) -> None:
        """General cleanup method"""
        if self._is_open:
            self.Close()
    
    def _set_frame_skip(self, value: int) -> None:
        """Set frame skip value"""
        app.SetFrameSkip(value)
    
    def _on_open(self) -> None:
        """Called when window opens - to be overridden"""
        pass
    
    def _on_close(self) -> None:
        """Called when window closes - to be overridden"""
        pass
    
    def OnPressEscapeKey(self) -> bool:
        """Handle escape key press"""
        self._handle_escape()
        return True
    
    def _handle_escape(self) -> None:
        """Handle escape key logic - to be overridden"""
        self._set_frame_skip(LoadingConstants.DEFAULT_FRAME_SKIP_ENABLED)
        self.stream.SetLoginPhase()


class GameLoadingState:
    """Manages game loading state and player position"""
    
    def __init__(self) -> None:
        self.player_x: int = 0
        self.player_y: int = 0
        self.update_count: int = 0
        self.is_loading_complete: bool = False
    
    def reset(self) -> None:
        """Reset loading state"""
        self.player_x = 0
        self.player_y = 0
        self.update_count = 0
        self.is_loading_complete = False
    
    def set_player_position(self, x: int, y: int) -> None:
        """Set player position"""
        self.player_x = x
        self.player_y = y
    
    def get_player_position(self) -> tuple[int, int]:
        """Get player position tuple"""
        return (self.player_x, self.player_y)
    
    def increment_update(self) -> None:
        """Increment update counter"""
        self.update_count += 1
    
    def mark_loading_complete(self) -> None:
        """Mark loading as complete"""
        self.is_loading_complete = True


class NetworkManager:
    """Manages network operations for loading"""
    
    @staticmethod
    def send_character_selection(character_slot) -> None:
        """Send character selection packet"""
        if character_slot is not None:
            net.SendSelectCharacterPacket(character_slot)
    
    @staticmethod
    def start_game_session(player_x: int, player_y: int) -> None:
        """Start game session with player position"""
        app.SetGlobalCenterPosition(player_x, player_y)
        net.StartGame()
    
    @staticmethod
    def set_loading_phase_window(window: BaseLoadingWindow) -> None:
        """Set the loading phase window"""
        net.SetPhaseWindow(net.PHASE_WINDOW_LOAD, window)
    
    @staticmethod
    def clear_loading_phase_window() -> None:
        """Clear the loading phase window"""
        net.SetPhaseWindow(net.PHASE_WINDOW_LOAD, 0)


class LoadingWindow(BaseLoadingWindow):
    """Main loading window for game initialization"""
    
    def __init__(self, stream) -> None:
        super().__init__(stream)
        
        self._init_as_window()
        
        self.loading_state = GameLoadingState()
        self.network_manager = NetworkManager()
        
        self.network_manager.set_loading_phase_window(self)
    
    def _init_as_window(self) -> None:
        """Initialize as ui.Window for compatibility"""
        # Reset to ui.Window base class behavior
        ui.Window.__init__(self)
    
    def __del__(self) -> None:
        """Cleanup on destruction"""
        self.network_manager.clear_loading_phase_window()
        ui.Window.__del__(self)
    
    def _on_open(self) -> None:
        """Handle window opening"""
        character_slot = self.stream.GetCharacterSlot()
        self.network_manager.send_character_selection(character_slot)
    
    def LoadData(self, player_x: int, player_y: int) -> None:
        """Load game data with player position"""
        self.loading_state.set_player_position(player_x, player_y)
        self._start_game()
    
    def DEBUG_LoadData(self, player_x: int, player_y: int) -> None:
        """Debug version of LoadData"""
        self.LoadData(player_x, player_y)
    
    def _start_game(self) -> None:
        """Start the game session"""
        player_x, player_y = self.loading_state.get_player_position()
        self.network_manager.start_game_session(player_x, player_y)
        self.loading_state.mark_loading_complete()
    
    def get_loading_state(self) -> GameLoadingState:
        """Get current loading state"""
        return self.loading_state


if app.ENABLE_LOADING_PERFORMANCE:
    class NewLoadingWindow(BaseLoadingWindow):
        """Optimized loading window for improved performance"""
        
        def __init__(self, stream) -> None:
            super().__init__(stream)
            self.loading_image = None
            
            self._send_initial_character_selection()
        
        def __del__(self) -> None:
            """Cleanup on destruction"""
            self._cleanup_loading_image()
            super().__del__()
        
        def _send_initial_character_selection(self) -> None:
            """Send character selection packet during initialization"""
            character_slot = self.stream.GetCharacterSlot()
            NetworkManager.send_character_selection(character_slot)
        
        def _on_open(self) -> None:
            """Handle window opening"""
            # Send character selection again on open for redundancy
            character_slot = self.stream.GetCharacterSlot()
            NetworkManager.send_character_selection(character_slot)
        
        def _on_close(self) -> None:
            """Handle window closing"""
            self._cleanup_loading_image()
        
        def _cleanup_loading_image(self) -> None:
            """Clean up loading image resources"""
            self.loading_image = None
        
        def set_loading_image(self, image) -> None:
            """Set the loading image"""
            self.loading_image = image
        
        def get_loading_image(self):
            """Get the loading image"""
            return self.loading_image


class LoadingWindowFactory:
    """Factory for creating appropriate loading window instances"""
    
    @staticmethod
    def create_loading_window(stream):
        """Create appropriate loading window based on configuration"""
        if hasattr(app, 'ENABLE_LOADING_PERFORMANCE') and app.ENABLE_LOADING_PERFORMANCE:
            return NewLoadingWindow(stream)
        else:
            return LoadingWindow(stream)
    
    @staticmethod
    def get_loading_window_type() -> str:
        """Get the type of loading window that would be created"""
        if hasattr(app, 'ENABLE_LOADING_PERFORMANCE') and app.ENABLE_LOADING_PERFORMANCE:
            return "NewLoadingWindow"
        else:
            return "LoadingWindow"


# Utility functions for external use
def create_loading_window(stream):
    """Utility function to create a loading window"""
    return LoadingWindowFactory.create_loading_window(stream)


def is_performance_loading_enabled() -> bool:
    """Check if performance loading is enabled"""
    return hasattr(app, 'ENABLE_LOADING_PERFORMANCE') and app.ENABLE_LOADING_PERFORMANCE
