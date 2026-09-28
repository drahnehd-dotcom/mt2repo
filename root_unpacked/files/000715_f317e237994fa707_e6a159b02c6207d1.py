# -*- coding: utf-8 -*-
"""
Centralized Windows Registry Module
Handles all registry operations for the game client
"""

import app

try:
    import _winreg
except ImportError:
    import winreg as _winreg


__all__ = [
    "Registry",
    "get_registry",
]


class Registry:
    """Centralized Windows registry handler"""
    
    # Default registry paths for different game features
    DEFAULT_PATH = r"SOFTWARE\Kowal\LoginInfo"
    FONT_PATH = r"SOFTWARE\Kowal"
    
    def __init__(self, path=None):
        """
        Initialize registry handler with optional custom path
        :param path: Registry path (uses DEFAULT_PATH if None)
        """
        self._path = path or self.DEFAULT_PATH
    
    def set_value(self, name, value, path=None):
        """
        Set a registry string value
        :param name: Value name
        :param value: Value to store
        :param path: Optional custom registry path
        :return: True if successful, False otherwise
        """
        reg_path = path or self._path
        try:
            _winreg.CreateKey(_winreg.HKEY_CURRENT_USER, reg_path)
            registry_key = _winreg.OpenKey(
                _winreg.HKEY_CURRENT_USER, 
                reg_path, 
                0, 
                _winreg.KEY_WRITE
            )
            _winreg.SetValueEx(registry_key, name, 0, _winreg.REG_SZ, str(value))
            _winreg.CloseKey(registry_key)
            return True
        except OSError:
            return False
    
    def get_value(self, name, default=None, path=None):
        """
        Get a registry string value
        :param name: Value name
        :param default: Default value if not found
        :param path: Optional custom registry path
        :return: Value as string, or default if not found
        """
        reg_path = path or self._path
        try:
            registry_key = _winreg.OpenKey(
                _winreg.HKEY_CURRENT_USER, 
                reg_path, 
                0, 
                _winreg.KEY_READ
            )
            value, regtype = _winreg.QueryValueEx(registry_key, name)
            _winreg.CloseKey(registry_key)
            return str(value)
        except OSError:
            return default
    
    def delete_value(self, name, path=None):
        """
        Delete a registry value (sets to empty string)
        :param name: Value name
        :param path: Optional custom registry path
        :return: True if successful, False otherwise
        """
        return self.set_value(name, "", path)
    
    def value_exists(self, name, path=None):
        """
        Check if a registry value exists
        :param name: Value name
        :param path: Optional custom registry path
        :return: True if exists, False otherwise
        """
        return self.get_value(name, None, path) is not None


# Global registry instance for login info
_login_registry = None

def get_registry(path=None):
    """
    Get or create a registry instance
    :param path: Optional custom registry path
    :return: Registry instance
    """
    global _login_registry
    if path is None:
        if _login_registry is None:
            _login_registry = Registry(Registry.DEFAULT_PATH)
        return _login_registry
    return Registry(path)
