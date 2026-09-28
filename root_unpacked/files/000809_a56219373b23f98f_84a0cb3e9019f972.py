import ui
import net
import wndMgr


class UiGiftCodeWindow(ui.ScriptWindow):
    """Gift code window for handling promotional code input and submission"""
    
    def __init__(self):
        super(UiGiftCodeWindow, self).__init__()
        self._initialize_attributes()
    
    def __del__(self):
        super(UiGiftCodeWindow, self).__del__()
    
    def _initialize_attributes(self):
        """Initialize instance attributes"""
        self.promo_code = None
        self.accept_button = None
        self.cancel_button = None
        self.title_bar = None
    
    def LoadWindow(self):
        """Load the window UI from script - maintains original API"""
        if not self._load_script_file():
            return False
        
        if not self._bind_ui_elements():
            return False
        
        self._setup_event_handlers()
        return True
    
    def _load_script_file(self):
        """Load the UI script file"""
        try:
            pyScrLoader = ui.PythonScriptLoader()
            pyScrLoader.LoadScriptFile(self, "uiscript/giftcodewindow.py")
            return True
        except:
            import exception
            exception.Abort("UiGiftCodeWindow.LoadWindow")
            return False
    
    def _bind_ui_elements(self):
        """Bind UI elements to instance variables"""
        try:
            self.promo_code = self.GetChild("CodeFrameSlotText")
            self.accept_button = self.GetChild("AcceptButton")
            self.cancel_button = self.GetChild("CancelButton")
            self.title_bar = self.GetChild("TitleBar")
            return True
        except:
            import exception
            exception.Abort("UiGiftCodeWindowElements.LoadWindow")
            return False
    
    def _setup_event_handlers(self):
        """Setup event handlers for UI elements"""
        self.title_bar.SetCloseEvent(ui.__mem_func__(self.Close))
        self.accept_button.SetEvent(ui.__mem_func__(self.ClickAccept))
        self.cancel_button.SetEvent(ui.__mem_func__(self.ClickClear))
    
    def ClickAccept(self):
        """Handle accept button click - maintains original API"""
        promo_code = self._get_promo_code()
        
        if self._is_valid_promo_code(promo_code):
            self._send_promo_code(promo_code)
            self.Close()
        else:
            self._handle_invalid_code()
    
    def _get_promo_code(self):
        """Get the current promo code from input field
        
        Returns:
            str: The promotional code entered by user
        """
        if self.promo_code:
            return self.promo_code.GetText().strip()
        return ""
    
    def _is_valid_promo_code(self, code):
        """Validate the promotional code
        
        Args:
            code (str): The promotional code to validate
            
        Returns:
            bool: True if code is valid, False otherwise
        """
        # Basic validation - can be extended
        return len(code) > 0
    
    def _send_promo_code(self, code):
        """Send the promotional code to server
        
        Args:
            code (str): The promotional code to send
        """
        net.SendChatPacket("/promo_code_system check_code %s" % code)
    
    def _handle_invalid_code(self):
        """Handle invalid promotional code input"""
        pass
    
    def ClickClear(self):
        """Clear the promo code input field - maintains original API"""
        self._clear_promo_code()
    
    def _clear_promo_code(self):
        """Clear the promotional code input field"""
        if self.promo_code:
            self.promo_code.SetText("")
    
    def Close(self):
        """Close the window - maintains original API"""
        self.ClickClear()
        self._hide_window()
    
    def _hide_window(self):
        """Hide the window"""
        wndMgr.Hide(self.hWnd)
    
    def OnPressEscapeKey(self):
        """Handle escape key press - maintains original API"""
        self.Close()
    
    def OnPressExitKey(self):
        """Handle exit key press - maintains original API"""
        self.Close()
    
    def _validate_input_length(self, text, min_length=1, max_length=50):
        """Validate input text length
        
        Args:
            text (str): Text to validate
            min_length (int): Minimum allowed length
            max_length (int): Maximum allowed length
            
        Returns:
            bool: True if length is valid, False otherwise
        """
        return min_length <= len(text) <= max_length
    
    def _sanitize_input(self, text):
        """Sanitize user input
        
        Args:
            text (str): Input text to sanitize
            
        Returns:
            str: Sanitized text
        """
        allowed_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_"
        return ''.join(c for c in text if c in allowed_chars)
    
    def _format_promo_code(self, code):
        """Format promotional code to standard format
        
        Args:
            code (str): Raw promotional code
            
        Returns:
            str: Formatted promotional code
        """
        return code.upper().replace(" ", "")
    
    def SetPromoCode(self, code):
        """Set promotional code programmatically
        
        Args:
            code (str): Promotional code to set
        """
        if self.promo_code:
            formatted_code = self._format_promo_code(code)
            self.promo_code.SetText(formatted_code)
    
    def GetPromoCode(self):
        """Get current promotional code
        
        Returns:
            str: Current promotional code
        """
        return self._get_promo_code()
    
    def IsWindowLoaded(self):
        """Check if window is properly loaded
        
        Returns:
            bool: True if all UI elements are loaded, False otherwise
        """
        return all([
            self.promo_code is not None,
            self.accept_button is not None,
            self.cancel_button is not None,
            self.title_bar is not None
        ])
    
    def SetAcceptButtonEnabled(self, enabled):
        """Enable or disable the accept button
        
        Args:
            enabled (bool): True to enable, False to disable
        """
        if self.accept_button:
            if enabled:
                self.accept_button.Enable()
            else:
                self.accept_button.Disable()
    
    def SetInputMaxLength(self, max_length):
        """Set maximum length for promo code input
        
        Args:
            max_length (int): Maximum character length
        """
        if self.promo_code and hasattr(self.promo_code, 'SetMax'):
            self.promo_code.SetMax(max_length)
    
    def FocusInput(self):
        """Set focus to the promo code input field"""
        if self.promo_code and hasattr(self.promo_code, 'SetFocus'):
            self.promo_code.SetFocus()
    
    def Show(self):
        """Show the window and focus input"""
        super(UiGiftCodeWindow, self).Show()
        self.FocusInput()
    
    def Destroy(self):
        """Clean up resources"""
        self.promo_code = None
        self.accept_button = None
        self.cancel_button = None
        self.title_bar = None


# Utility functions for gift code management
def CreateGiftCodeWindow():
    """Factory function to create a new UiGiftCodeWindow instance
    
    Returns:
        UiGiftCodeWindow: New gift code window instance
    """
    window = UiGiftCodeWindow()
    return window


def ValidatePromoCodeFormat(code):
    """Validate promotional code format
    
    Args:
        code (str): Promotional code to validate
        
    Returns:
        bool: True if format is valid, False otherwise
    """
    if not code or len(code) < 3:
        return False
    
    # Check for valid characters
    allowed_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_"
    return all(c in allowed_chars for c in code)


def FormatPromoCode(code):
    """Format promotional code to standard format
    
    Args:
        code (str): Raw promotional code
        
    Returns:
        str: Formatted promotional code
    """
    if not code:
        return ""
    
    # Convert to uppercase, remove spaces and invalid characters
    formatted = code.upper().replace(" ", "")
    allowed_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_"
    return ''.join(c for c in formatted if c in allowed_chars)


class GiftCodeManager(object):
    """Manager class for handling gift code operations"""
    
    def __init__(self):
        self.active_window = None
        self.code_history = []
        self.max_history = 10
    
    def SetActiveWindow(self, window):
        """Set the active gift code window
        
        Args:
            window (UiGiftCodeWindow): Gift code window instance
        """
        self.active_window = window
    
    def GetActiveWindow(self):
        """Get the active gift code window
        
        Returns:
            UiGiftCodeWindow or None: Active window instance
        """
        return self.active_window
    
    def AddToHistory(self, code):
        """Add a promotional code to history
        
        Args:
            code (str): Promotional code to add
        """
        if code and code not in self.code_history:
            self.code_history.insert(0, code)
            if len(self.code_history) > self.max_history:
                self.code_history = self.code_history[:self.max_history]
    
    def GetHistory(self):
        """Get promotional code history
        
        Returns:
            list: List of previously used promotional codes
        """
        return list(self.code_history)
    
    def ClearHistory(self):
        """Clear promotional code history"""
        self.code_history = []
    
    def SubmitCode(self, code):
        """Submit a promotional code
        
        Args:
            code (str): Promotional code to submit
            
        Returns:
            bool: True if code was submitted, False if invalid
        """
        formatted_code = FormatPromoCode(code)
        
        if ValidatePromoCodeFormat(formatted_code):
            net.SendChatPacket("/promo_code_system check_code %s" % formatted_code)
            self.AddToHistory(formatted_code)
            return True
        
        return False