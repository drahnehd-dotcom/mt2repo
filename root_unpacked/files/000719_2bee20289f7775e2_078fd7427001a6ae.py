# -*- coding: utf-8 -*-
"""
User Settings Module
Manages user preferences using Windows Registry
"""
import registry

# Registry instance
_reg = registry.get_registry()

# Default values
DEFAULTS = {
    "find_chest_tooltip": 1,
    "split_tooltip": 1,
    "extract_tooltip": 1,
    "add_additional_tooltip": 1,
    "remember_last_page": 0,
    "remember_save_window": 0,
    "remember_boss_tp_window": 0,
    "inventory_auto_open": 0,
    "enable_fast_open": 0,
    "extended_inventory_auto_use": 1,
    # Limit FPS. Kiedys zaszyty na sztywno na 60 (CTimer: "16 + (m_index & 1)"), teraz
    # steruje krokiem zegara gry przez app.SetFPS(). 60 = zachowanie jak dawniej.
    # UWAGA: czytaj przez settings.get("fps_limit"), NIE przez deskryptor modulowy -
    # deskryptory na poziomie modulu w Pythonie nie dzialaja (zwracaja obiekt, nie wartosc).
    "fps_limit": 60,
}

# Dozwolone wartosci limitu FPS (1000 = praktycznie bez limitu)
FPS_LIMIT_CHOICES = (60, 100, 144, 165, 240, 1000)


def get(name, default=None):
    """Get setting value from registry"""
    if default is None:
        default = DEFAULTS.get(name, 0)
    
    try:
        value = _reg.get_value(name)
        if value is None:
            return default
        # Convert to int if it's a numeric string
        if isinstance(value, str):
            try:
                return int(value)
            except ValueError:
                return value
        return value
    except Exception:
        return default


def set(name, value):
    """Set setting value in registry"""
    _reg.set_value(name, str(value))


# Module-level property accessors for easy access
class _SettingsDescriptor:
    """Descriptor for module-level settings access"""
    def __init__(self, name):
        self.name = name
    
    def __get__(self, obj, objtype=None):
        return get(self.name)
    
    def __set__(self, obj, value):
        set(self.name, value)


# Create module-level descriptors for each setting
find_chest_tooltip = _SettingsDescriptor("find_chest_tooltip")
split_tooltip = _SettingsDescriptor("split_tooltip")
extract_tooltip = _SettingsDescriptor("extract_tooltip")
add_additional_tooltip = _SettingsDescriptor("add_additional_tooltip")
remember_last_page = _SettingsDescriptor("remember_last_page")
remember_save_window = _SettingsDescriptor("remember_save_window")
remember_boss_tp_window = _SettingsDescriptor("remember_boss_tp_window")
inventory_auto_open = _SettingsDescriptor("inventory_auto_open")
enable_fast_open = _SettingsDescriptor("enable_fast_open")
extended_inventory_auto_use = _SettingsDescriptor("extended_inventory_auto_use")
