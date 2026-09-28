"""Item deposit window - safebox and mall access."""

import ui
import exception
import net


class DepositWindow(ui.ScriptWindow):
    """Dialog for choosing between deposit (safebox) and item shop (mall)."""

    def __init__(self):
        ui.ScriptWindow.__init__(self)
        self.isLoaded = 0
        self._load_window()

    def __del__(self):
        ui.ScriptWindow.__del__(self)

    def Show(self):
        self._load_window()
        ui.ScriptWindow.Show(self)

    def Open(self):
        if self.IsShow():
            self.Close()
        else:
            self.Show()

    def _load_window(self):
        """Load UI script and bind components."""
        if self.isLoaded:
            return

        self.isLoaded = 1
        try:
            ui.PythonScriptLoader().LoadScriptFile(self, "uiscript/depositwindow.py")
        except Exception:
            exception.Abort("DepositWindow.LoadDialog.LoadScript")

        try:
            self.titleBar = self.GetChild("TitleBar")
            self.depo = self.GetChild("DepoButton")
            self.itemshop = self.GetChild("IsButton")
            self.depo.SetEvent(ui.__mem_func__(self.OpenDepo))
            self.itemshop.SetEvent(ui.__mem_func__(self.OpenIS))
            self.titleBar.SetCloseEvent(ui.__mem_func__(self.Close))
        except Exception:
            exception.Abort("DepositWindow.LoadDialog.BindObject")

        self.SetCenterPosition()
        self.SetTop()

    def Destroy(self):
        self.Hide()
        self.ClearDictionary()

    def Close(self):
        self.Hide()

    def OnPressEscapeKey(self):
        self.Close()
        return True

    def OpenDepo(self):
        self.Close()
        net.SendChatPacket("/click_safebox")

    def OpenIS(self):
        self.Close()
        net.SendChatPacket("/click_mall")

# Legacy aliases

