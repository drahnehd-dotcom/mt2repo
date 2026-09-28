import app
import ui
import player
import net


class GameButtonWindow(ui.ScriptWindow):
    """Game button window for managing various game interface buttons"""
    
    def __init__(self):
        super(GameButtonWindow, self).__init__()
        self._initialize_attributes()
        self.__LoadWindow("UIScript/gamewindow.py")
    
    def __del__(self):
        super(GameButtonWindow, self).__del__()
    
    def _initialize_attributes(self):
        """Initialize instance attributes"""
        self.gameButtonDict = {}
    
    def __LoadWindow(self, filename):
        """Load the window UI from script file - maintains original API"""
        if not self._load_script_file(filename):
            return False
        
        if not self._bind_ui_objects():
            return False
        
        self._setup_initial_state()
        return True
    
    def _load_script_file(self, filename):
        """Load the UI script file"""
        try:
            pyScrLoader = ui.PythonScriptLoader()
            pyScrLoader.LoadScriptFile(self, filename)
            return True
        except Exception as msg:
            import dbg
            dbg.TraceError("GameButtonWindow.LoadScript - %s" % (msg))
            pass
            return False
    
    def _bind_ui_objects(self):
        """Bind UI objects to the button dictionary"""
        try:
            self.gameButtonDict = {
                "STATUS": self.GetChild("StatusPlusButton"),
                "QUEST": self.GetChild("QuestButton"),
                "BUILD": self.GetChild("BuildGuildBuilding"),
                "EXIT_OBSERVER": self.GetChild("ExitObserver"),
            }
            
            # Setup button events
            self._setup_button_events()
            return True
            
        except Exception as msg:
            import dbg
            dbg.TraceError("GameButtonWindow.LoadScript - %s" % (msg))
            pass
            return False
    
    def _setup_button_events(self):
        """Setup default button events"""
        self.gameButtonDict["EXIT_OBSERVER"].SetEvent(
            ui.__mem_func__(self.__OnClickExitObserver)
        )
    
    def _setup_initial_state(self):
        """Setup the initial state of the window"""
        self.__HideAllGameButton()
        self.SetObserverMode(player.IsObserverMode())
    
    def Destroy(self):
        """Clean up resources and event handlers - maintains original API"""
        for key in self.gameButtonDict:
            self.gameButtonDict[key].SetEvent(0)
        self.gameButtonDict = {}
    
    def SetButtonEvent(self, name, event):
        """Set event handler for a specific button - maintains original API
        
        Args:
            name (str): Name of the button
            event: Event handler function
        """
        try:
            self.gameButtonDict[name].SetEvent(event)
        except Exception as msg:
            print("GameButtonWindow.LoadScript - %s" % (msg))
            pass
            return
    
    def ShowBuildButton(self):
        """Show the build guild building button - maintains original API"""
        self.gameButtonDict["BUILD"].Show()
    
    def HideBuildButton(self):
        """Hide the build guild building button - maintains original API"""
        self.gameButtonDict["BUILD"].Hide()
    
    def CheckGameButton(self):
        """Check and update game button visibility - maintains original API"""
        if not self.IsShow():
            return
        
        statusPlusButton = self.gameButtonDict["STATUS"]
        if player.GetStatus(player.STAT) > 0:
            statusPlusButton.Show()
        else:
            statusPlusButton.Hide()
    
    def __IsSkillStat(self):
        """Check if skill stat points are available - maintains original API
        
        Returns:
            bool: True if skill points are available, False otherwise
        """
        if player.GetStatus(player.SKILL_ACTIVE) > 0:
            return True
        return False
    
    def __OnClickExitObserver(self):
        """Handle click on exit observer button - maintains original API"""
        net.SendChatPacket("/observer_exit")
    
    def __HideAllGameButton(self):
        """Hide all game buttons - maintains original API"""
        for btn in self.gameButtonDict.values():
            btn.Hide()
    
    def SetObserverMode(self, isEnable):
        """Set observer mode state - maintains original API
        
        Args:
            isEnable (bool): True to enable observer mode, False to disable
        """
        if isEnable:
            self.gameButtonDict["EXIT_OBSERVER"].Show()
        else:
            self.gameButtonDict["EXIT_OBSERVER"].Hide()
    
    # Additional helper methods for internal use (not breaking existing API)
    def _show_button(self, button_name):
        """Show a specific button by name (internal helper)"""
        if button_name in self.gameButtonDict:
            self.gameButtonDict[button_name].Show()
    
    def _hide_button(self, button_name):
        """Hide a specific button by name (internal helper)"""
        if button_name in self.gameButtonDict:
            self.gameButtonDict[button_name].Hide()
    
    def _is_button_visible(self, button_name):
        """Check if a button is currently visible (internal helper)
        
        Args:
            button_name (str): Name of the button to check
            
        Returns:
            bool: True if button is visible, False otherwise
        """
        if button_name in self.gameButtonDict:
            return self.gameButtonDict[button_name].IsShow()
        return False
    
    def _get_button(self, button_name):
        """Get a button object by name (internal helper)
        
        Args:
            button_name (str): Name of the button
            
        Returns:
            UI button object or None if not found
        """
        return self.gameButtonDict.get(button_name)
    
    def _update_button_states(self):
        """Update all button states based on current game state (internal helper)"""
        self.CheckGameButton()
    
    def _set_buttons_visible(self, button_names, visible=True):
        """Set visibility for multiple buttons at once (internal helper)
        
        Args:
            button_names (list): List of button names
            visible (bool): True to show, False to hide
        """
        for button_name in button_names:
            if visible:
                self._show_button(button_name)
            else:
                self._hide_button(button_name)


class GameButtonManager(object):
    """Optional manager class for handling multiple game button windows"""
    
    def __init__(self):
        self.button_windows = {}
        self.active_window = None
    
    def AddButtonWindow(self, name, window):
        """Add a button window to the manager
        
        Args:
            name (str): Name identifier for the window
            window (GameButtonWindow): Button window instance
        """
        self.button_windows[name] = window
    
    def RemoveButtonWindow(self, name):
        """Remove a button window from the manager
        
        Args:
            name (str): Name identifier for the window
        """
        if name in self.button_windows:
            window = self.button_windows[name]
            window.Destroy()
            del self.button_windows[name]
            
            if self.active_window == window:
                self.active_window = None
    
    def SetActiveWindow(self, name):
        """Set the active button window
        
        Args:
            name (str): Name identifier for the window
        """
        if name in self.button_windows:
            self.active_window = self.button_windows[name]
    
    def GetActiveWindow(self):
        """Get the currently active button window
        
        Returns:
            GameButtonWindow or None: Active window instance
        """
        return self.active_window
    
    def UpdateAllWindows(self):
        """Update all managed button windows"""
        for window in self.button_windows.values():
            if window.IsShow():
                window._update_button_states()
    
    def Destroy(self):
        """Clean up all managed windows"""
        for window in self.button_windows.values():
            window.Destroy()
        self.button_windows = {}
        self.active_window = None


# Optional utility functions that don't break existing code
def CreateGameButtonWindow():
    """Factory function to create a new GameButtonWindow instance
    
    Returns:
        GameButtonWindow: New button window instance
    """
    return GameButtonWindow()


def SetupDefaultButtonEvents(button_window, event_handlers):
    """Setup default button events for a button window
    
    Args:
        button_window (GameButtonWindow): Button window instance
        event_handlers (dict): Dictionary mapping button names to event handlers
    """
    for button_name, handler in event_handlers.items():
        button_window.SetButtonEvent(button_name, handler)


def ConfigureButtonVisibility(button_window, config):
    """Configure button visibility based on configuration
    
    Args:
        button_window (GameButtonWindow): Button window instance
        config (dict): Configuration dictionary with button visibility settings
    """
    for button_name, visible in config.items():
        if visible:
            button_window._show_button(button_name)
        else:
            button_window._hide_button(button_name)