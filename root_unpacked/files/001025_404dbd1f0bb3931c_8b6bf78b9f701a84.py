import ui
import net
import app

ASSET_PATH = "kowal/teleportwindow/"
class TeleportMap(ui.ScriptWindow):
    """Simple teleport map window."""

    def __init__(self):
        super(TeleportMap, self).__init__()
        self._buttons = []
        self._teleport_indices = {}  # Store button -> index mapping
        self._setup()

    def _setup(self):
        """Setup the window."""
        self.SetSize(800, 584)
        self.SetCenterPosition()
        self.AddFlag("movable")
        self.AddFlag("float")

        self._map = ui.ImageBox()
        self._map.SetParent(self)
        self._map.SetPosition(0, 0)
        self._map.LoadImage(ASSET_PATH + 'map.png')

        self._create_teleports()

    def _create_teleports(self):
        """Create all teleport buttons."""
        # Simple list: [name, index, x, y, image_prefix]
        teleports = [
            ("jinno_m1", 1, 150, 370, "jinno_m1"),
            ("jinno_m2", 2, 200, 410, "jinno_m2"),
            ("shinso_m1", 3, 75, 240, "shinsoo_m1"),
            ("shinso_m2", 4, 150, 275, "shinsoo_m2"),
            ("zakatki", 5, 120, 320, "dalszezakatki"),
            ("sohan", 6, 368, 230, "sohan"),
            ("orki", 7, 215, 220, "dolina_orkow"),
            ("las", 8, 300, 275, "lasduchow"),
            ("pajaki", 9, 325, 322, "loch_pajakow"),
            ("cyklopy", 10, 320, 370, "dolina_cyklopow"),
            ("pustynia", 11, 513, 340, "pustkowie"),
            ("mrozna", 12, 470, 285, "mroznakraina"),
            ("ognista", 13, 510, 235, "ognistaziemia"),
            ("las_zacz", 14, 420, 183, "zaczarowanylas"),
            ("mining", 15, 325, 415, "mining"),
            ("fishing", 16, 475, 390, "fishing"),
            ("baziny", 17, 502, 151, "baziny"),
            ("zakleteudoli", 18, 596, 193, "zakleteudoli"),
        ]

        for name, index, x, y, img in teleports:
            self._add_teleport_button(name, index, x, y, img)

    def _add_teleport_button(self, name, index, x, y, image_prefix):
        """Add single teleport button."""
        btn = ui.Button()
        btn.SetParent(self._map)
        btn.SetPosition(x, y)

        btn.SetUpVisual(ASSET_PATH + image_prefix + "_0.png")
        btn.SetOverVisual(ASSET_PATH + image_prefix + "_1.png")
        btn.SetDownVisual(ASSET_PATH + image_prefix + "_2.png")

        self._teleport_indices[btn] = index

        btn.SetEvent(ui.__mem_func__(self._on_button_click), btn)

        self._buttons.append(btn)
    
    def _on_button_click(self, button):
        """Handle button click event."""
        # Get the teleport index for this button
        map_index = self._teleport_indices.get(button, 0)
        if map_index > 0:
            self._teleport(map_index)
    
    def _teleport(self, map_index):
        """Execute teleport and close window."""
        net.SendChatPacket("/teleport {}".format(map_index))
        self.Hide()
    
    def toggle(self):
        """Toggle window visibility."""
        if self.IsShow():
            self.Hide()
        else:
            self.Show()
            self._map.Show()
            for btn in self._buttons:
                btn.Show()
    
    def Close(self):
        """Close the UI window."""
        self.Hide()
    
    def OnPressEscapeKey(self):
        """Close on escape."""
        self.Close()
        return True