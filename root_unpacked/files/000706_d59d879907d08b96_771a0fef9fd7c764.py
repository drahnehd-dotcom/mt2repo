import os


class MusicManager(object):
    """Internal music manager with modern implementation."""
    
    def __init__(self):
        super(MusicManager, self).__init__()
        self.default_theme = "M2BG.mp3"
        self.login_music = "login_window.mp3"
        self.create_music = "characterselect.mp3"
        self.select_music = "characterselect.mp3"
        self.field_music = self.default_theme
        self.last_play_file_path = "BGM/lastplay.inf"
    
    def save_last_play_field_music(self):
        """Internal method to save field music."""
        try:
            bgm_dir = os.path.dirname(self.last_play_file_path)
            if bgm_dir and not os.path.exists(bgm_dir):
                os.makedirs(bgm_dir)
            
            with open(self.last_play_file_path, "w") as last_play_file:
                last_play_file.write(self.field_music)
                
        except (IOError, OSError):
            pass
    
    def load_last_play_field_music(self):
        """Internal method to load field music."""
        try:
            with open(self.last_play_file_path, "r") as last_play_file:
                loaded_music = last_play_file.read().strip()
                if loaded_music:
                    self.field_music = loaded_music
                    
        except (IOError, OSError):
            # Silently handle errors for backward compatibility  
            pass


# Create internal manager instance
_music_manager = MusicManager()

# Backward compatibility - expose original global variables with exact same names
METIN2THEMA = _music_manager.default_theme
loginMusic = _music_manager.login_music
createMusic = _music_manager.create_music
selectMusic = _music_manager.select_music
fieldMusic = _music_manager.field_music

# Handle the old_open reference that was in original code
try:
    old_open = open  # Assume old_open was aliased to open
except NameError:
    old_open = open


def SaveLastPlayFieldMusic():
    """
    Original function name maintained for backward compatibility.
    Modern implementation using file context managers internally.
    """
    global fieldMusic
    
    # Sync global variable to manager
    _music_manager.field_music = fieldMusic
    
    # Use original approach for maximum compatibility
    try:
        # Ensure BGM directory exists (improvement)
        bgm_dir = "BGM"
        if not os.path.exists(bgm_dir):
            try:
                os.makedirs(bgm_dir)
            except OSError:
                pass
        
        lastPlayFile = old_open("BGM/lastplay.inf", "w")
        try:
            lastPlayFile.write(fieldMusic)
        finally:
            lastPlayFile.close()  # Ensure file is closed
            
    except (IOError, ValueError, Exception):
        # Original behavior - silently return on error
        return


def LoadLastPlayFieldMusic():
    """
    Original function name maintained for backward compatibility.
    Modern implementation using file context managers internally.
    """
    global fieldMusic
    
    try:
        lastPlayFile = old_open("BGM/lastplay.inf", "r")
        try:
            loaded_music = lastPlayFile.read()
            if loaded_music.strip():  # Only update if file has content
                fieldMusic = loaded_music
                _music_manager.field_music = fieldMusic
        finally:
            lastPlayFile.close()  # Ensure file is closed
            
    except (IOError, ValueError, Exception):
        # Original behavior - silently return on error
        return


# Helper class for advanced usage (optional, doesn't break compatibility)
class MusicManagerInterface(object):
    """Optional modern interface that doesn't break backward compatibility."""
    
    def __init__(self):
        super(MusicManagerInterface, self).__init__()
    
    def get_field_music(self):
        """Get current field music."""
        return fieldMusic
    
    def set_field_music(self, music_file):
        """Set field music and update global variable."""
        global fieldMusic
        fieldMusic = music_file
        _music_manager.field_music = music_file
    
    def save_state(self):
        """Save current music state."""
        SaveLastPlayFieldMusic()
    
    def load_state(self):
        """Load music state."""
        LoadLastPlayFieldMusic()
    
    def get_all_tracks(self):
        """Get all music tracks as dictionary."""
        return {
            'theme': METIN2THEMA,
            'login': loginMusic,
            'create': createMusic,
            'select': selectMusic,
            'field': fieldMusic
        }


# Create optional modern interface instance
_modern_interface = MusicManagerInterface()


def get_music_interface():
    """
    Optional function to get modern interface.
    This doesn't break backward compatibility since it's a new function.
    """
    return _modern_interface
