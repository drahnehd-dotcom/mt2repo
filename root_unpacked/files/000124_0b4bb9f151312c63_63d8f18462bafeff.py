#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Modern Logo Window - Clean Version
Rewritten for Python 3 with better maintainability and cleaner code structure
"""

from __future__ import annotations

import app
import net
import ui
import wndMgr


__all__ = [
    "LogoConstants",
    "VideoManager",
    "LogoWindowState",
    "LogoWindow",
    "SkippableLogoWindow",
    "ConfigurableLogoWindow",
    "create_logo_window",
    "get_default_video_list",
    "set_default_video_list",
]


class LogoConstants:
    """Constants for logo window configuration"""
    DEFAULT_GUILD_MARK_PATH: str = "test"
    WINDOW_NAME: str = "SelectLogoWindow"
    
    # Video configuration
    DEFAULT_VIDEO_LIST: list[str] = ["logo1.avi", "logo2.avi"]
    
    # Video states
    VIDEO_STOPPED: int = 0
    VIDEO_PLAYING: int = 1


class VideoManager:
    """Manages video playback and sequencing"""
    
    def __init__(self, video_list = None) -> None:
        self.video_list: list[str] = video_list or LogoConstants.DEFAULT_VIDEO_LIST[:]
        self.current_index: int = 0
        self.video_handle: int = LogoConstants.VIDEO_STOPPED
        self.is_playing: bool = False
    
    def has_next_video(self) -> bool:
        """Check if there are more videos to play"""
        return self.current_index < len(self.video_list)
    
    def get_current_video_name(self):
        """Get current video filename"""
        if self.current_index < len(self.video_list):
            return self.video_list[self.current_index]
        return None
    
    def load_next_video(self) -> bool:
        """Load and start the next video"""
        if not self.has_next_video():
            return False
        
        video_filename = self.video_list[self.current_index]
        print(f"Loading video: {video_filename}")
        
        self.video_handle = app.OnLogoOpen(video_filename)
        
        if self.video_handle != LogoConstants.VIDEO_STOPPED:
            self.is_playing = True
            self.current_index += 1
            return True
        else:
            print(f"Failed to load video: {video_filename}")
            self.current_index += 1
            return False
    
    def update_video(self) -> int:
        """Update video playback state"""
        if self.is_playing:
            self.video_handle = app.OnLogoUpdate()
            if self.video_handle == LogoConstants.VIDEO_STOPPED:
                self.is_playing = False
        
        return self.video_handle
    
    def close_video(self) -> None:
        """Close current video"""
        if self.is_playing or self.video_handle != LogoConstants.VIDEO_STOPPED:
            app.OnLogoClose()
            self.is_playing = False
            self.video_handle = LogoConstants.VIDEO_STOPPED
    
    def reset(self) -> None:
        """Reset video manager to initial state"""
        self.close_video()
        self.current_index = 0
    
    def is_sequence_complete(self) -> bool:
        """Check if all videos have been played"""
        return not self.has_next_video() and not self.is_playing
    
    def get_progress(self) -> tuple[int, int]:
        """Get playback progress as (current, total)"""
        return (self.current_index, len(self.video_list))
    
    def skip_current_video(self) -> None:
        """Skip the currently playing video"""
        if self.is_playing:
            self.close_video()
    
    def get_video_list(self) -> list[str]:
        """Get list of all videos"""
        return self.video_list[:]
    
    def set_video_list(self, video_list: list[str]) -> None:
        """Set new video list"""
        self.close_video()
        self.video_list = video_list[:]
        self.current_index = 0


class LogoWindowState:
    """Manages logo window state"""
    
    def __init__(self) -> None:
        self.needs_update: bool = True
        self.is_open: bool = False
        self.sequence_complete: bool = False
    
    def reset(self) -> None:
        """Reset state to initial values"""
        self.needs_update = True
        self.is_open = False
        self.sequence_complete = False
    
    def start_sequence(self) -> None:
        """Start logo sequence"""
        self.needs_update = True
        self.is_open = True
        self.sequence_complete = False
    
    def complete_sequence(self) -> None:
        """Mark sequence as complete"""
        self.needs_update = False
        self.sequence_complete = True
    
    def should_update(self) -> bool:
        """Check if window should update"""
        return self.needs_update and self.is_open and not self.sequence_complete


class LogoWindow(ui.ScriptWindow):
    """Modern logo window with clean video management"""
    
    def __init__(self, stream, video_list = None) -> None:
        super().__init__()
        
        print("NEW LOGO WINDOW")
        
        # Core components
        self.stream = stream
        self.video_manager = VideoManager(video_list)
        self.window_state = LogoWindowState()
        
        # Setup network phase and guild mark
        net.SetPhaseWindow(net.PHASE_WINDOW_LOGO, self)
        app.SetGuildMarkPath(LogoConstants.DEFAULT_GUILD_MARK_PATH)
    
    def __del__(self) -> None:
        """Cleanup on destruction"""
        print("DELETE LOGO WINDOW")
        
        self._cleanup()
        super().__del__()
    
    def Open(self) -> None:
        """Open the logo window and start video sequence"""
        print("OPEN LOGO WINDOW")
        
        self._setup_window()
        self._start_sequence()
        self._show_window()
    
    def Close(self) -> None:
        """Close the logo window"""
        print("CLOSE LOGO WINDOW")
        
        self._cleanup()
        self._hide_window()
    
    def OnUpdate(self) -> None:
        """Update logo window state and video playback"""
        if not self.window_state.should_update():
            return
        
        video_handle = self.video_manager.update_video()
        
        # Check if current video finished
        if video_handle == LogoConstants.VIDEO_STOPPED and not self.video_manager.is_playing:
            if self.video_manager.has_next_video():
                self._load_next_video()
            else:
                self._complete_sequence()
    
    def OnRender(self) -> None:
        """Render current video if playing"""
        if self.video_manager.is_playing and self.video_manager.video_handle != LogoConstants.VIDEO_STOPPED:
            app.OnLogoRender()
    
    def set_video_list(self, video_list: list[str]) -> None:
        """Set custom video list"""
        self.video_manager.set_video_list(video_list)
    
    def add_video(self, video_filename: str) -> None:
        """Add video to the sequence"""
        self.video_manager.video_list.append(video_filename)
    
    def get_playback_progress(self) -> tuple[int, int]:
        """Get current playback progress"""
        return self.video_manager.get_progress()
    
    def skip_current_video(self) -> None:
        """Skip currently playing video"""
        self.video_manager.skip_current_video()
        if self.video_manager.has_next_video():
            self._load_next_video()
        else:
            self._complete_sequence()
    
    def skip_all_videos(self) -> None:
        """Skip all remaining videos and go to login"""
        self.video_manager.close_video()
        self._complete_sequence()
    
    # Event handlers for user interaction
    def OnPressEscapeKey(self) -> bool:
        """Handle escape key - skip to login"""
        self.skip_all_videos()
        return True
    
    def OnPressEnterKey(self) -> bool:
        """Handle enter key - skip current video"""
        self.skip_current_video()
        return True
    
    def OnMouseLeftButtonDown(self) -> bool:
        """Handle mouse click - skip current video"""
        self.skip_current_video()
        return True
    
    def OnPressExitKey(self) -> bool:
        """Handle exit key - skip to login"""
        self.skip_all_videos()
        return True
    
    # Private methods
    def _setup_window(self) -> None:
        """Setup window properties"""
        screen_width = wndMgr.GetScreenWidth()
        screen_height = wndMgr.GetScreenHeight()
        self.SetSize(screen_width, screen_height)
        self.SetWindowName(LogoConstants.WINDOW_NAME)
    
    def _start_sequence(self) -> None:
        """Start the video sequence"""
        self.window_state.start_sequence()
        self._load_next_video()
    
    def _show_window(self) -> None:
        """Show window and cursor"""
        self.Show()
        app.ShowCursor()
    
    def _hide_window(self) -> None:
        """Hide window and cursor"""
        self.KillFocus()
        self.Hide()
        app.HideCursor()
    
    def _load_next_video(self) -> None:
        """Load the next video in sequence"""
        if not self.video_manager.load_next_video():
            if self.video_manager.has_next_video():
                self._load_next_video()
            else:
                self._complete_sequence()
    
    def _complete_sequence(self) -> None:
        """Complete the logo sequence and transition to login"""
        self.window_state.complete_sequence()
        self.video_manager.reset()
        
        if self.stream:
            self.stream.SetLoginPhase()
    
    def _cleanup(self) -> None:
        """Cleanup resources"""
        self.video_manager.close_video()
        net.SetPhaseWindow(net.PHASE_WINDOW_LOGO, 0)


class SkippableLogoWindow(LogoWindow):
    """Logo window variant with enhanced skipping and auto-skip"""
    
    def __init__(self, stream, video_list = None, auto_skip_delay = None) -> None:
        super().__init__(stream, video_list)
        self.auto_skip_delay = auto_skip_delay  # seconds
        self.start_time: float = 0
    
    def Open(self) -> None:
        """Open with auto-skip timer"""
        super().Open()
        if self.auto_skip_delay:
            self.start_time = app.GetTime()
    
    def OnUpdate(self) -> None:
        """Update with auto-skip check"""
        # Check for auto-skip
        if self.auto_skip_delay and self.start_time:
            current_time = app.GetTime()
            if current_time - self.start_time >= self.auto_skip_delay * 1000:  # Convert to milliseconds
                print(f"Auto-skip triggered after {self.auto_skip_delay} seconds")
                self.skip_all_videos()
                return
        
        # Normal update
        super().OnUpdate()
    
    def OnKeyDown(self, key) -> bool:
        """Handle any key press to skip"""
        self.skip_current_video()
        return True


class ConfigurableLogoWindow(LogoWindow):
    """Logo window with configuration options"""
    
    def __init__(self, stream, config = None) -> None:
        self.config = config or {}
        
        # Extract video list from config
        video_list = self.config.get('video_list', LogoConstants.DEFAULT_VIDEO_LIST)
        
        super().__init__(stream, video_list)
        
        # Apply configuration
        self._apply_configuration()
    
    def _apply_configuration(self) -> None:
        """Apply configuration settings"""
        guild_mark_path = self.config.get('guild_mark_path', LogoConstants.DEFAULT_GUILD_MARK_PATH)
        app.SetGuildMarkPath(guild_mark_path)
        
        window_name = self.config.get('window_name', LogoConstants.WINDOW_NAME)
        LogoConstants.WINDOW_NAME = window_name
        
        self.skip_on_click = self.config.get('skip_on_click', True)
        self.skip_on_key = self.config.get('skip_on_key', True)
        self.auto_skip_delay = self.config.get('auto_skip_delay', None)
        
        if self.auto_skip_delay:
            self.start_time = 0
    
    def Open(self) -> None:
        """Open with configuration"""
        super().Open()
        if self.auto_skip_delay:
            self.start_time = app.GetTime()
    
    def OnUpdate(self) -> None:
        """Update with configuration options"""
        if self.auto_skip_delay and self.start_time:
            current_time = app.GetTime()
            if current_time - self.start_time >= self.auto_skip_delay * 1000:
                self.skip_all_videos()
                return
        
        super().OnUpdate()
    
    def OnMouseLeftButtonDown(self) -> bool:
        """Handle mouse click based on configuration"""
        if self.skip_on_click:
            return super().OnMouseLeftButtonDown()
        return False
    
    def OnPressEscapeKey(self) -> bool:
        """Handle escape key based on configuration"""
        if self.skip_on_key:
            return super().OnPressEscapeKey()
        return False
    
    def OnPressEnterKey(self) -> bool:
        """Handle enter key based on configuration"""
        if self.skip_on_key:
            return super().OnPressEnterKey()
        return False


# Factory function for creating logo windows
def create_logo_window(stream, window_type = "default", **kwargs):
    """Factory function for creating different types of logo windows"""
    
    if window_type == "skippable":
        return SkippableLogoWindow(stream, **kwargs)
    elif window_type == "configurable":
        return ConfigurableLogoWindow(stream, **kwargs)
    else:
        return LogoWindow(stream, **kwargs)


def get_default_video_list() -> list[str]:
    """Get default video list"""
    return LogoConstants.DEFAULT_VIDEO_LIST[:]


def set_default_video_list(video_list: list[str]) -> None:
    """Set default video list"""
    LogoConstants.DEFAULT_VIDEO_LIST = video_list[:]
