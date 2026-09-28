"""In-game icon buttons panel."""

import ui
import app
import constInfo


class IngameIconPanel(ui.ScriptWindow):
    """Panel with expandable icon buttons for item shop, battlepass, etc."""

    def __init__(self):
        ui.ScriptWindow.__init__(self)

    def __del__(self):
        ui.ScriptWindow.__del__(self)

    def BindInterfaceClass(self, interface):
        self.interface = interface

    def LoadWindow(self):
        """Load UI and bind button events."""
        try:
            pyScrLoader = ui.PythonScriptLoader()
            pyScrLoader.LoadScriptFile(self, "uiscript/iconswindow.py")
        except Exception:
            import exception
            exception.Abort("IconsPanel.LoadWindow.LoadObject")

        try:
            self.button = self.GetChild("ItemShopButton")
            self.button1 = self.GetChild("BattlepassButton")
            self.expander = self.GetChild("expander")
        except Exception:
            import exception
            exception.Abort("IconsPanel.LoadWindow.BindObject")

        try:
            self.buttonAni = self.GetChild("ItemShopButtonAni")
            if self.buttonAni:
                self.buttonAni.Hide()
        except Exception:
            pass
        # Wymuszamy statyczna ikone ItemShopa zamiast animowanej
        self.buttonAni = None

        try:
            self.buttonEventCalendar = self.GetChild("EventCalendarButton")
        except Exception:
            self.buttonEventCalendar = None

        try:
            self.buttonVoiceChat = self.GetChild("VoiceChatButton")
        except Exception:
            self.buttonVoiceChat = None

        self.button.SetEvent(ui.__mem_func__(self._on_click_item_shop))
        self.button.SetScale(1, 1)
        self.button1.SetEvent(ui.__mem_func__(self._on_click_battlepass))
        self.button1.SetScale(1, 1)
        self.expander.SetEvent(ui.__mem_func__(self.Expander))

        if self.buttonEventCalendar:
            self.buttonEventCalendar.SetEvent(ui.__mem_func__(self._on_click_event_calendar))
            self.buttonEventCalendar.SetScale(1, 1)

        if self.buttonVoiceChat:
            self.buttonVoiceChat.SetEvent(ui.__mem_func__(self._on_click_voice_settings))
            self.buttonVoiceChat.SetScale(1, 1)

        buttons = self._icon_buttons()
        if constInfo.iconsExpanded == 0:
            for btn in buttons:
                btn.Hide()
        else:
            for btn in buttons:
                btn.Show()

    def _icon_buttons(self):
        """Wszystkie ikony chowane/pokazywane przez expander."""
        btns = [self.button, self.button1]
        if self.buttonAni:
            btns.append(self.buttonAni)
        if self.buttonEventCalendar:
            btns.append(self.buttonEventCalendar)
        if self.buttonVoiceChat:
            btns.append(self.buttonVoiceChat)
        return btns

    def Expander(self):
        """Toggle visibility of icon buttons."""
        buttons = self._icon_buttons()
        if constInfo.iconsExpanded == 1:
            for btn in buttons:
                btn.Hide()
            constInfo.iconsExpanded = 0
        else:
            for btn in buttons:
                btn.Show()
            constInfo.iconsExpanded = 1

    def _on_click_battlepass(self):
        self.interface.ToggleBattlePass()

    def _on_click_item_shop(self):
        self.interface.RequestOpenItemShop()

    def _on_click_event_calendar(self):
        self.interface.OpenEventCalendar()

    def _on_click_voice_settings(self):
        # Otwiera ustawienia gry (te same co pod ESC) od razu na zakladce Voice Chat.
        # Toggle: gdy okno opcji jest juz otwarte na zakladce Voice Chat (page 4),
        # ponowne klikniecie ikony je zamyka. Otwarte na innej zakladce -> przelacza na voice.
        opt = getattr(self.interface, "wndgameOption", None)
        if not opt:
            return
        if opt.IsShow() and getattr(opt, "page", None) == 4:
            opt.Close()
            return
        opt.Show()
        if app.ENABLE_VOICE_CHAT and hasattr(opt, "OpenVoiceChat"):
            opt.OpenVoiceChat()
        opt.SetTop()

    def Open(self, id):
        self.id = id
        self.Show()

    def Close(self):
        self.Hide()

    def Destroy(self):
        self.ClearDictionary()

# Legacy aliases

IngameIconManager = IngameIconPanel
