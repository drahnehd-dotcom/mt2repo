import app
import ui
import localeInfo
import uiScriptLocale

ENABLE_HELP_MULTIPAGE = 0


class HelpWindow(ui.ScriptWindow):
    """Help window with support for single page and multi-page layouts"""
    
    def __init__(self):
        super(HelpWindow, self).__init__("TOP_MOST")
        self._initialize_attributes()
    
    def __del__(self):
        super(HelpWindow, self).__del__()
    
    def _initialize_attributes(self):
        """Initialize instance attributes"""
        self.eventClose = 0
        self.btnClose = None
        self.closeButton = 0
        self.pages = {}
        self.btnPages = {}
        self._current_page = 0
        self._is_multipage = False
    
    def LoadDialog(self):
        """Load dialog based on multipage configuration - maintains original API"""
        if ENABLE_HELP_MULTIPAGE:
            self.LoadDialogMultiPage()
        else:
            self.LoadDialogSinglePage()
    
    def LoadDialogSinglePage(self):
        """Load single page dialog - maintains original API"""
        self._is_multipage = False
        
        if not self._load_single_page_script():
            return False
        
        if not self._bind_single_page_objects():
            return False
        
        return True
    
    def _load_single_page_script(self):
        """Load single page UI script"""
        try:
            pyScrLoader = ui.PythonScriptLoader()
            script_path = self._get_single_page_script_path()
            pyScrLoader.LoadScriptFile(self, script_path)
            return True
        except:
            import exception
            exception.Abort("HelpWindow.LoadDialogSinglePage.LoadScript")
            return False
    
    def _get_single_page_script_path(self):
        """Get the appropriate script path for single page layout
        
        Returns:
            str: Path to the UI script file
        """
        return "UIScript/HelpWindow.py"
    
    def _bind_single_page_objects(self):
        """Bind UI objects for single page layout"""
        try:
            GetObject = self.GetChild
            self.btnClose = GetObject("close_button")
            return True
        except:
            import exception
            exception.Abort("DialogWindow.LoadDialogSinglePage.BindObject")
            return False
    
    def LoadDialogMultiPage(self):
        """Load multi-page dialog - maintains original API"""
        self._is_multipage = True
        
        if not self._load_multi_page_script():
            return False
        
        if not self._bind_multi_page_objects():
            return False
        
        self._setup_multi_page_events()
        self.__SelectPage(0)
        return True
    
    def _load_multi_page_script(self):
        """Load multi-page UI script"""
        try:
            pyScrLoader = ui.PythonScriptLoader()
            pyScrLoader.LoadScriptFile(self, "UIScript/HelpWindow2.py")
            return True
        except:
            import exception
            exception.Abort("HelpWindow.LoadDialogMultiPage.LoadScript")
            return False
    
    def _bind_multi_page_objects(self):
        """Bind UI objects for multi-page layout"""
        try:
            GetObject = self.GetChild
            self.btnClose = GetObject("close_button")
            self.pages = {}
            self.btnPages = {}
            self.pages[0] = GetObject("page_1")
            self.pages[1] = GetObject("page_2")
            self.btnPages[0] = GetObject("page_1_button")
            self.btnPages[1] = GetObject("page_2_button")
            return True
        except:
            import exception
            exception.Abort("DialogWindow.LoadDialogMultiPage.BindObject")
            return False
    
    def _setup_multi_page_events(self):
        """Setup event handlers for multi-page buttons"""
        self.btnPages[0].SAFE_SetEvent(self.__OnClickPage1)
        self.btnPages[1].SAFE_SetEvent(self.__OnClickPage2)
    
    def __OnClickPage1(self):
        """Handle page 1 button click - maintains original API"""
        self.__SelectPage(0)
    
    def __OnClickPage2(self):
        """Handle page 2 button click - maintains original API"""
        self.__SelectPage(1)
    
    def __SelectPage(self, pageIndex):
        """Select and display a specific page - maintains original API
        
        Args:
            pageIndex (int): Index of the page to select
        """
        if not self._is_multipage:
            return
        
        if pageIndex not in self.pages:
            return
        
        self._hide_all_pages()
        self._reset_all_buttons()
        self._show_selected_page(pageIndex)
        self._current_page = pageIndex
    
    def _hide_all_pages(self):
        """Hide all pages"""
        for page in self.pages.values():
            page.Hide()
    
    def _reset_all_buttons(self):
        """Reset all page buttons to up state"""
        for btn in self.btnPages.values():
            btn.SetUp()
    
    def _show_selected_page(self, pageIndex):
        """Show the selected page and set button state
        
        Args:
            pageIndex (int): Index of the page to show
        """
        if pageIndex in self.pages:
            self.pages[pageIndex].Show()
        
        if pageIndex in self.btnPages:
            self.btnPages[pageIndex].Down()
    
    def Destroy(self):
        """Clean up resources - maintains original API"""
        self.eventClose = 0
        self.closeButton = 0
        self.btnClose = None
        self.pages = {}
        self.btnPages = {}
        self._current_page = 0
        self._is_multipage = False
    
    def SetCloseEvent(self, event):
        """Set close event handler - maintains original API
        
        Args:
            event: Event handler function
        """
        self.eventClose = event
        if self.btnClose:
            self.btnClose.SetEvent(event)
    
    def Open(self):
        """Open the help window - maintains original API"""
        self.Lock()
        self.Show()
    
    def Close(self):
        """Close the help window - maintains original API"""
        self.Unlock()
        self.Hide()
    
    def OnKeyDown(self, key):
        """Handle key down events - maintains original API
        
        Args:
            key: Key code that was pressed
            
        Returns:
            bool: True if key was handled
        """
        if app.DIK_H == key and 0 != self.eventClose:
            self.eventClose()
        return True
    
    def OnIMEReturn(self):
        """Handle IME return event - maintains original API
        
        Returns:
            bool: Always returns True
        """
        return True
    
    def OnPressEscapeKey(self):
        """Handle escape key press - maintains original API
        
        Returns:
            bool: Always returns True
        """
        if 0 != self.eventClose:
            self.eventClose()
        return True
    
    def OnPressExitKey(self):
        """Handle exit key press - maintains original API
        
        Returns:
            bool: Always returns True
        """
        if 0 != self.eventClose:
            self.eventClose()
        return True
    
    # Additional helper methods for enhanced functionality
    def _get_current_page(self):
        """Get the currently selected page index
        
        Returns:
            int: Current page index
        """
        return self._current_page
    
    def _get_page_count(self):
        """Get the total number of pages
        
        Returns:
            int: Number of pages available
        """
        return len(self.pages)
    
    def _is_valid_page(self, pageIndex):
        """Check if a page index is valid
        
        Args:
            pageIndex (int): Page index to validate
            
        Returns:
            bool: True if page index is valid, False otherwise
        """
        return pageIndex in self.pages
    
    def GetCurrentPage(self):
        """Get the currently selected page index - public API extension
        
        Returns:
            int: Current page index
        """
        return self._get_current_page()
    
    def GetPageCount(self):
        """Get the total number of pages - public API extension
        
        Returns:
            int: Number of pages available
        """
        return self._get_page_count()
    
    def IsMultiPage(self):
        """Check if window is in multi-page mode - public API extension
        
        Returns:
            bool: True if multi-page mode is enabled, False otherwise
        """
        return self._is_multipage
    
    def SelectPage(self, pageIndex):
        """Select a page by index - public API extension
        
        Args:
            pageIndex (int): Index of the page to select
            
        Returns:
            bool: True if page was selected successfully, False otherwise
        """
        if self._is_valid_page(pageIndex):
            self.__SelectPage(pageIndex)
            return True
        return False
    
    def NextPage(self):
        """Go to the next page - public API extension
        
        Returns:
            bool: True if moved to next page, False if already at last page
        """
        if not self._is_multipage:
            return False
        
        next_page = self._current_page + 1
        if self._is_valid_page(next_page):
            self.__SelectPage(next_page)
            return True
        return False
    
    def PreviousPage(self):
        """Go to the previous page - public API extension
        
        Returns:
            bool: True if moved to previous page, False if already at first page
        """
        if not self._is_multipage:
            return False
        
        prev_page = self._current_page - 1
        if self._is_valid_page(prev_page):
            self.__SelectPage(prev_page)
            return True
        return False
    
    def IsWindowLoaded(self):
        """Check if window is properly loaded - public API extension
        
        Returns:
            bool: True if window is loaded successfully, False otherwise
        """
        if self.btnClose is None:
            return False
        
        if self._is_multipage:
            return len(self.pages) > 0 and len(self.btnPages) > 0
        
        return True
    
    def RefreshWindow(self):
        """Refresh the window state - public API extension"""
        if self._is_multipage and self._current_page in self.pages:
            self.__SelectPage(self._current_page)


def CreateHelpWindow(enable_multipage=None):
    """Factory function to create a new HelpWindow instance
    
    Args:
        enable_multipage (bool, optional): Override for multipage setting
        
    Returns:
        HelpWindow: New help window instance
    """
    global ENABLE_HELP_MULTIPAGE
    
    if enable_multipage is not None:
        original_setting = ENABLE_HELP_MULTIPAGE
        ENABLE_HELP_MULTIPAGE = 1 if enable_multipage else 0
        
        window = HelpWindow()
        window.LoadDialog()
        
        ENABLE_HELP_MULTIPAGE = original_setting
    else:
        window = HelpWindow()
        window.LoadDialog()
    
    return window


def SetMultiPageEnabled(enabled):
    """Set the global multipage setting
    
    Args:
        enabled (bool): True to enable multipage mode, False for single page
    """
    global ENABLE_HELP_MULTIPAGE
    ENABLE_HELP_MULTIPAGE = 1 if enabled else 0


def IsMultiPageEnabled():
    """Check if multipage mode is globally enabled
    
    Returns:
        bool: True if multipage mode is enabled, False otherwise
    """
    return bool(ENABLE_HELP_MULTIPAGE)


class HelpWindowManager(object):
    """Manager class for handling multiple help windows"""
    
    def __init__(self):
        self.help_windows = {}
        self.active_window = None
    
    def CreateWindow(self, name, enable_multipage=None):
        """Create a new help window
        
        Args:
            name (str): Name identifier for the window
            enable_multipage (bool, optional): Override for multipage setting
            
        Returns:
            HelpWindow: Created help window instance
        """
        window = CreateHelpWindow(enable_multipage)
        self.help_windows[name] = window
        return window
    
    def GetWindow(self, name):
        """Get a help window by name
        
        Args:
            name (str): Name identifier for the window
            
        Returns:
            HelpWindow or None: Help window instance if found
        """
        return self.help_windows.get(name)
    
    def RemoveWindow(self, name):
        """Remove a help window
        
        Args:
            name (str): Name identifier for the window
        """
        if name in self.help_windows:
            window = self.help_windows[name]
            window.Destroy()
            del self.help_windows[name]
            
            if self.active_window == window:
                self.active_window = None
    
    def SetActiveWindow(self, name):
        """Set the active help window
        
        Args:
            name (str): Name identifier for the window
        """
        if name in self.help_windows:
            self.active_window = self.help_windows[name]
    
    def GetActiveWindow(self):
        """Get the currently active help window
        
        Returns:
            HelpWindow or None: Active window instance
        """
        return self.active_window
    
    def CloseAllWindows(self):
        """Close all help windows"""
        for window in self.help_windows.values():
            window.Close()
    
    def DestroyAllWindows(self):
        """Destroy all help windows"""
        for window in self.help_windows.values():
            window.Destroy()
        self.help_windows = {}
        self.active_window = None
