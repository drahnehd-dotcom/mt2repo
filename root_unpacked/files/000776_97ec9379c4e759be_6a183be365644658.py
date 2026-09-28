import ui 
import app
import localeInfo
import player
import chat
import dbg

PATH = "d:/ymir work/ui/itemshop/"
REAL_PATH = "d:/ymir work/ui/bonus_window/"

class BonusConfig(object):
    """Configuration class for bonus data and constants."""
    
    BONUS_DATA = [
        (189, localeInfo.TOOLTIP_ATTBONUS_ELEMENT),
        (190, localeInfo.TOOLTIP_DEFBONUS_ELEMENT),
        (6, localeInfo.TOOLTIP_MAX_HP),
        (8, localeInfo.TOOLTIP_MAX_SP),
        (13, localeInfo.TOOLTIP_CON),
        (15, localeInfo.TOOLTIP_INT),
        (12, localeInfo.TOOLTIP_STR),
        (14, localeInfo.TOOLTIP_DEX),
        (158, localeInfo.TOOLTIP_STAT_BONUS),
        (17, localeInfo.TOOLTIP_ATT_SPEED),
        (19, localeInfo.TOOLTIP_MOV_SPEED),
        (21, localeInfo.TOOLTIP_CAST_SPEED),
        (32, localeInfo.TOOLTIP_HP_REGEN),
        (33, localeInfo.TOOLTIP_SP_REGEN),
        (37, localeInfo.TOOLTIP_APPLY_POISON_PCT),
        (38, localeInfo.TOOLTIP_APPLY_STUN_PCT),
        (39, localeInfo.TOOLTIP_APPLY_SLOW_PCT),
        (40, localeInfo.TOOLTIP_APPLY_CRITICAL_PCT),
        (41, localeInfo.TOOLTIP_APPLY_PENETRATE_PCT),
        (53, localeInfo.TOOLTIP_APPLY_ATTBONUS_MONSTER),
        (44, localeInfo.TOOLTIP_APPLY_ATTBONUS_ANIMAL),
        (45, localeInfo.TOOLTIP_APPLY_ATTBONUS_ORC),
        (46, localeInfo.TOOLTIP_APPLY_ATTBONUS_MILGYO),
        (47, localeInfo.TOOLTIP_APPLY_ATTBONUS_UNDEAD),
        (48, localeInfo.TOOLTIP_APPLY_ATTBONUS_DEVIL),
        (152, localeInfo.TOOLTIP_APPLY_ATTBONUS_BOSS),
        (153, localeInfo.TOOLTIP_APPLY_ATTBONUS_WLADCA),
        (154, localeInfo.TOOLTIP_APPLY_ATTBONUS_STONE),
        (159, localeInfo.TOOLTIP_ATTBONUS_DUNGEON),
        (160, localeInfo.TOOLTIP_APPLY_ATTBONUS_LEGENDA),
        (163, localeInfo.TOOLTIP_APPLY_DMG_BONUS),
        (164, localeInfo.TOOLTIP_APPLY_FINAL_DMG_BONUS),
        (43, localeInfo.TOOLTIP_APPLY_ATTBONUS_HUMAN),
        (54, localeInfo.TOOLTIP_APPLY_ATTBONUS_WARRIOR),
        (55, localeInfo.TOOLTIP_APPLY_ATTBONUS_ASSASSIN),
        (56, localeInfo.TOOLTIP_APPLY_ATTBONUS_SURA),
        (57, localeInfo.TOOLTIP_APPLY_ATTBONUS_SHAMAN),
        (63, localeInfo.TOOLTIP_APPLY_STEAL_HP),
        (64, localeInfo.TOOLTIP_APPLY_STEAL_SP),
        (65, localeInfo.TOOLTIP_APPLY_MANA_BURN_PCT),
        (66, localeInfo.TOOLTIP_APPLY_DAMAGE_SP_RECOVER),
        (67, localeInfo.TOOLTIP_APPLY_BLOCK),
        (68, localeInfo.TOOLTIP_APPLY_DODGE),
        (69, localeInfo.TOOLTIP_APPLY_RESIST_SWORD),
        (70, localeInfo.TOOLTIP_APPLY_RESIST_TWOHAND),
        (71, localeInfo.TOOLTIP_APPLY_RESIST_DAGGER),
        (72, localeInfo.TOOLTIP_APPLY_RESIST_BELL),
        (73, localeInfo.TOOLTIP_APPLY_RESIST_FAN),
        (74, localeInfo.TOOLTIP_RESIST_BOW),
        (79, localeInfo.TOOLTIP_APPLY_REFLECT_MELEE),
        (80, localeInfo.TOOLTIP_APPLY_REFLECT_CURSE),
        (81, localeInfo.TOOLTIP_APPLY_POISON_REDUCE),
        (82, localeInfo.TOOLTIP_APPLY_KILL_SP_RECOVER),
        (83, localeInfo.TOOLTIP_APPLY_EXP_DOUBLE_BONUS),
        (84, localeInfo.TOOLTIP_APPLY_GOLD_DOUBLE_BONUS),
        (85, localeInfo.TOOLTIP_APPLY_ITEM_DROP_BONUS),
        (87, localeInfo.TOOLTIP_APPLY_KILL_HP_RECOVER),
        (88, localeInfo.TOOLTIP_APPLY_IMMUNE_STUN),
        (89, localeInfo.TOOLTIP_APPLY_IMMUNE_SLOW),
        (90, localeInfo.TOOLTIP_APPLY_IMMUNE_FALL),
        (95, localeInfo.TOOLTIP_ATT_GRADE),
        (96, localeInfo.TOOLTIP_DEF_GRADE),
        (97, localeInfo.TOOLTIP_MAGIC_ATT_GRADE),
        (98, localeInfo.TOOLTIP_MAGIC_DEF_GRADE),
        (93, localeInfo.TOOLTIP_MALL_ATTBONUS),
        (115, localeInfo.TOOLTIP_MALL_DEFBONUS),
        (116, localeInfo.TOOLTIP_MALL_EXPBONUS),
        (117, localeInfo.TOOLTIP_MALL_ITEMBONUS),
        (118, localeInfo.TOOLTIP_MALL_GOLDBONUS),
        (121, localeInfo.TOOLTIP_SKILL_DAMAGE_BONUS),
        (188, localeInfo.TOOLTIP_ATTBONUS_PVM_SKILL),
        (122, localeInfo.TOOLTIP_NORMAL_HIT_DAMAGE_BONUS),
        (123, localeInfo.TOOLTIP_SKILL_DEFEND_BONUS),
        (124, localeInfo.TOOLTIP_NORMAL_HIT_DEFEND_BONUS),
        (119, localeInfo.TOOLTIP_APPLY_MAX_HP_PCT),
        (120, localeInfo.TOOLTIP_APPLY_MAX_SP_PCT),
        (131, localeInfo.TOOLTIP_MAGIC_ATTBONUS_PER),
        (132, localeInfo.TOOLTIP_MELEE_MAGIC_ATTBONUS_PER),
        (136, localeInfo.TOOLTIP_ANTI_CRITICAL_PCT),
        (137, localeInfo.TOOLTIP_ANTI_PENETRATE_PCT),
        (151, localeInfo.TOOLTIP_APPLY_RESIST_HUMAN),
        (155, localeInfo.TOOLTIP_RESIST_BOSS),
        (156, localeInfo.TOOLTIP_RESIST_WLADCA),
        (157, localeInfo.TOOLTIP_RESIST_MONSTER),
        (162, localeInfo.TOOLTIP_APPLY_RESIST_KLASY),
        (59, localeInfo.TOOLTIP_APPLY_RESIST_WARRIOR),
        (60, localeInfo.TOOLTIP_APPLY_RESIST_ASSASSIN),
        (61, localeInfo.TOOLTIP_APPLY_RESIST_SURA),
        (62, localeInfo.TOOLTIP_APPLY_RESIST_SHAMAN),
        (77, localeInfo.TOOLTIP_RESIST_MAGIC),
    ]
    
    # Color constants for better readability
    COLOR_ACTIVE = "|cFF89b88d"
    COLOR_INACTIVE = "|cFFe57875"
    
    # Immune bonuses that need special color handling
    IMMUNE_BONUSES = {88, 89, 90}
    
    # Update interval — kiedys 25 KLATEK, czyli ~417 ms przy 60 FPS. Teraz wprost w ms,
    # zeby nie zalezalo od FPS (patrz BonusWindow.OnUpdate).
    UPDATE_INTERVAL_MS = 417


class Slot(ui.NewListBoxItem):
    """Individual bonus slot item with improved encapsulation."""
    
    def __init__(self):
        super(Slot, self).__init__()
        self._text = "-"
        self._LoadWindow()
        self.OnRender = None
    
    def _LoadWindow(self):
        """Initialize the UI components."""
        self.slot = ui.ImageBox()
        self.slot.SetParent(self)
        self.slot.SetPosition(0, 0)
        self.slot.LoadImage(REAL_PATH + "left_box.png")
        self.slot.Show()

        self.txt = ui.TextLine()
        self.txt.SetParent(self.slot)
        self.txt.SetFontName("Tahoma:14")
        self.txt.SetPosition(self.slot.GetWidth() // 2, 3)
        self.txt.SetHorizontalAlignCenter()
        self.txt.SetText(self._text)
        self.txt.Show()

        self.RegisterComponent(self.slot)
        self.RegisterComponent(self.txt)
        self.SetSize(self.slot.GetWidth(), self.slot.GetHeight())
    
    def SetText(self, text):
        """Set the text content of the slot."""
        self._text = text
        self.txt.SetText(text)
    
    def GetText(self):
        """Get the text content of the slot."""
        return self._text
    
    def ClearDictionary(self):
        """Clean up components."""
        if hasattr(self, 'slot') and self.slot:
            self.UnregisterComponent(self.slot)
            self.slot = 0
        
        if hasattr(self, 'txt') and self.txt:
            self.UnregisterComponent(self.txt)
            self.txt = 0
        
        self.Hide()
    
    def __del__(self):
        super(Slot, self).__del__()


class ScrollBar(ui.Window):
    """Enhanced scroll bar with smooth scrolling support - maintains original interface."""
    
    # Class constants
    SCROLLBAR_WIDTH = 17
    SCROLLBAR_MIDDLE_HEIGHT = 9
    SCROLLBAR_BUTTON_HEIGHT = 0
    MIDDLE_BAR_POS = 8
    MIDDLE_BAR_UPPER_PLACE = 3
    MIDDLE_BAR_DOWNER_PLACE = 5
    TEMP_SPACE = MIDDLE_BAR_UPPER_PLACE + MIDDLE_BAR_DOWNER_PLACE
    
    if app.__BL_SMOOTH_SCROLL__:
        SMOOTH_RATIO = 1.5
    
    def __init__(self):
        super(ScrollBar, self).__init__()
        
        # Initialize properties (keeping original names for compatibility)
        self.pageSize = 1
        self.curPos = 0.0
        self.eventScroll = lambda *arg: None
        self.lockFlag = False
        self.scrollStep = 0.20
        
        # Smooth scrolling properties
        if app.__BL_SMOOTH_SCROLL__:
            self.smooth_mode = False
            self.actual_pos = 0.0
            self._lastSmoothTime = 0.0   # do skalowania plynnego scrolla czasem
            self.target_pos = 0.0
        
        self.CreateScrollBar()
    
    def CreateScrollBar(self):
        """Create the scroll bar UI components."""
        barSlot = ui.ExpandedImageBox()
        barSlot.SetParent(self)
        barSlot.AddFlag("not_pick")
        barSlot.LoadImage(PATH + "scroll_slot.png")
        barSlot.Show()

        middleBar = ui.DragButton()
        middleBar.SetParent(self)
        middleBar.AddFlag("movable")
        middleBar.SetMoveEvent(ui.__mem_func__(self.OnMove))
        middleBar.SetUpVisual(PATH + "scroll_button.png")
        middleBar.SetOverVisual(PATH + "scroll_button.png")
        middleBar.SetDownVisual(PATH + "scroll_button.png")
        middleBar.Show()

        self.middleBar = middleBar
        self.barSlot = barSlot

        self.SCROLLBAR_WIDTH = self.middleBar.GetWidth()
        self.SCROLLBAR_MIDDLE_HEIGHT = self.middleBar.GetHeight()
    
    def Destroy(self):
        """Clean up the scroll bar."""
        self.middleBar = None
        self.eventScroll = lambda *arg: None
    
    def SetScrollEvent(self, event):
        """Set the scroll event callback."""
        self.eventScroll = event
    
    def SetMiddleBarSize(self, pageScale):
        """Set middle bar size (kept for compatibility)."""
        pass
    
    def SetScrollBarSize(self, height):
        """Set the size of the scroll bar."""
        self.pageSize = (height - self.SCROLLBAR_BUTTON_HEIGHT * 2) - self.SCROLLBAR_MIDDLE_HEIGHT - self.TEMP_SPACE
        self.SetSize(self.SCROLLBAR_WIDTH, height)
        
        self.middleBar.SetRestrictMovementArea(
            self.MIDDLE_BAR_POS,
            self.SCROLLBAR_BUTTON_HEIGHT + self.MIDDLE_BAR_UPPER_PLACE,
            self.MIDDLE_BAR_POS + 2,
            height - self.SCROLLBAR_BUTTON_HEIGHT * 2 - self.TEMP_SPACE
        )
        self.middleBar.SetPosition(self.MIDDLE_BAR_POS, 0)
        self.UpdateBarSlot()
    
    def UpdateBarSlot(self):
        """Update the bar slot scaling."""
        if hasattr(self, 'barSlot') and self.barSlot:
            barHeight = self.barSlot.GetHeight()
            if barHeight <= 0:
                return
            scale_y = float(self.GetHeight()) / float(barHeight)
            self.barSlot.SetScale(1.0, scale_y)
    
    def GetPos(self):
        """Get current scroll position."""
        return self.curPos
    
    def SetPos(self, pos):
        """Set scroll position."""
        pos = max(0.0, min(1.0, pos))
        
        newPos = float(self.pageSize) * pos
        self.middleBar.SetPosition(
            self.MIDDLE_BAR_POS,
            int(newPos) + self.SCROLLBAR_BUTTON_HEIGHT + self.MIDDLE_BAR_UPPER_PLACE
        )
        self.OnMove()
    
    def SetScrollStep(self, step):
        """Set the scroll step size."""
        self.scrollStep = step
    
    def GetScrollStep(self):
        """Get the scroll step size."""
        return self.scrollStep
    
    def OnMouseWheel(self, nLen):
        """Handle mouse wheel events."""
        if nLen > 0:
            self.OnUp()
            return True
        elif nLen < 0:
            self.OnDown()
            return True
        return False
    
    def OnUp(self):
        """Handle scroll up."""
        if app.__BL_SMOOTH_SCROLL__ and hasattr(self, 'smooth_mode') and self.smooth_mode:
            self.actual_pos = max(0.0, min(1.0, self.curPos))
            self.target_pos = max(0.0, min(1.0, self.curPos - self.scrollStep))
        else:
            self.SetPos(self.curPos - self.scrollStep)
    
    def OnDown(self):
        """Handle scroll down."""
        if app.__BL_SMOOTH_SCROLL__ and hasattr(self, 'smooth_mode') and self.smooth_mode:
            self.actual_pos = max(0.0, min(1.0, self.curPos))
            self.target_pos = max(0.0, min(1.0, self.curPos + self.scrollStep))
        else:
            self.SetPos(self.curPos + self.scrollStep)
    
    def OnMove(self):
        """Handle middle bar movement."""
        if self.lockFlag or self.pageSize == 0:
            return

        (xLocal, yLocal) = self.middleBar.GetLocalPosition()
        self.curPos = float(yLocal - self.SCROLLBAR_BUTTON_HEIGHT - self.MIDDLE_BAR_UPPER_PLACE) / float(self.pageSize)
        self.eventScroll()
    
    def OnMouseLeftButtonDown(self):
        """Handle mouse click on scroll bar."""
        (xMouseLocalPosition, yMouseLocalPosition) = self.GetMouseLocalPosition()
        pickedPos = yMouseLocalPosition - self.SCROLLBAR_BUTTON_HEIGHT - self.SCROLLBAR_MIDDLE_HEIGHT // 2
        newPos = float(pickedPos) / float(self.pageSize)
        
        if app.__BL_SMOOTH_SCROLL__ and hasattr(self, 'smooth_mode') and self.smooth_mode:
            self.actual_pos = max(0.0, min(1.0, self.curPos))
            self.target_pos = max(0.0, min(1.0, newPos))
        else:
            self.SetPos(newPos)
    
    def LockScroll(self):
        """Lock scrolling."""
        self.lockFlag = True
    
    def UnlockScroll(self):
        """Unlock scrolling."""
        self.lockFlag = False
    
    if app.__BL_SMOOTH_SCROLL__:
        def EnableSmoothMode(self):
            """Enable smooth scrolling mode."""
            self.smooth_mode = True
        
        def OnUpdate(self):
            """Update smooth scrolling animation."""
            if not hasattr(self, 'smooth_mode') or not self.smooth_mode:
                return
                
            if self.lockFlag or self.pageSize == 0:
                return
            
            if self.actual_pos == self.target_pos:
                return

            # Plynne przewijanie liczylo krok NA KLATKE, wiec po odblokowaniu limitu FPS
            # przy 144 Hz scroll dojezdzal do celu 2.4x szybciej. Skalujemy krok czasem.
            scale, self._lastSmoothTime = ui.GetFrameStepScale(self._lastSmoothTime)
            distance = abs(self.actual_pos - self.target_pos)
            smooth_step = max(distance / self.SMOOTH_RATIO, 0.005) * scale
        
            if self.actual_pos < self.target_pos:
                self.actual_pos = min(self.actual_pos + smooth_step, self.target_pos)
            elif self.actual_pos > self.target_pos:
                self.actual_pos = max(self.actual_pos - smooth_step, self.target_pos)
            
            self.SetPos(self.actual_pos)


class BonusWindow(ui.ScriptWindow):
    """Main bonus window class with modern Python practices."""
    
    def __init__(self):
        super(BonusWindow, self).__init__()
        
        # Initialize state (keeping original names for compatibility)
        self.isLoaded = 0
        self.BonusUpdate = 0
        self.slot = {}
        self.textLine = {}
        self.previous_search_text = ""
        
        # Setup window
        self.RefreshBonus()
        self.__LoadWindow()
    
    def __del__(self):
        super(BonusWindow, self).__del__()
    
    def __LoadWindow(self):
        """Load and initialize the window UI."""
        if self.isLoaded == 1:
            return
        
        self.isLoaded = 1
        
        try:
            ui.PythonScriptLoader().LoadScriptFile(self, "uiscript/bonus.py")
        except:
            import exception
            exception.Abort("BonusWindow.LoadDialog.LoadScript")

        self.board = self.GetChild("border")
        self.titleBar = self.GetChild("TitleBar")
        self.titleBar.SetCloseEvent(ui.__mem_func__(self.Close))
        self.InputValue = self.GetChild("InputValue")

        self.scrollBar = ScrollBar()
        self.scrollBar.SetParent(self)
        self.scrollBar.SetScrollBarSize(380)
        self.scrollBar.SetPosition(282, 29)
        
        if app.__BL_SMOOTH_SCROLL__:
            self.scrollBar.EnableSmoothMode()
        
        self.scrollBar.Show()

        self.test = ui.NewListBox()
        self.test.SetParent(self.board)
        self.test.SetSize(260, 340)
        self.test.SetPosition(3, 2)
        self.test.itemStep = 0
        self.test.Show()

        self.test.SetScrollBar(self.scrollBar)
        self.test.OnMouseWheel = self.scrollBar.OnMouseWheel

        for i in range(len(BonusConfig.BONUS_DATA)):
            self.slot[i] = Slot()
            self.slot[i].SetText("-")
            self.test.AppendItem(self.slot[i])
        
        self.SetCenterPosition()
    
    def RefreshBonus(self):
        """Refresh all bonus values."""
        if self.isLoaded == 0:
            return
        
        try:
            for i in range(len(BonusConfig.BONUS_DATA)):
                bonus_id, tooltip_func = BonusConfig.BONUS_DATA[i]
                status_value = player.GetStatus(bonus_id)
                text = tooltip_func(status_value)
                
                # Apply special color formatting for immune bonuses
                if bonus_id in BonusConfig.IMMUNE_BONUSES:
                    if status_value >= 1:
                        text = BonusConfig.COLOR_ACTIVE + text
                    else:
                        text = BonusConfig.COLOR_INACTIVE + text
                
                self.slot[i].SetText(text)
        
        except:
            import exception
            exception.Abort("BonusWindow.RefreshBonus error.")
    
    def OnUpdate(self):
        """Handle window updates."""
        # Licznik byl w KLATKACH (25 klatek = ~417 ms przy 60 FPS). Po odblokowaniu limitu
        # FPS przy 144 Hz odswiezaloby sie 2.4x czesciej. Liczymy czasem rzeczywistym.
        curTime = app.GetGlobalTime()
        if curTime - self.BonusUpdate >= BonusConfig.UPDATE_INTERVAL_MS:
            self.BonusUpdate = curTime
            self.RefreshBonus()
        
        search_text = self.InputValue.GetText().lower()
        
        if not hasattr(self, 'previous_search_text'):
            self.previous_search_text = ""
        
        if search_text != self.previous_search_text:
            self.previous_search_text = search_text
            self.test.ClearItems()
            
            if search_text:
                matched_indices = [i for i in range(len(BonusConfig.BONUS_DATA)) 
                                 if search_text in self.slot[i].GetText().lower()]
                for i in matched_indices:
                    self.test.AppendItem(self.slot[i])
            else:
                for i in range(len(BonusConfig.BONUS_DATA)):
                    self.test.AppendItem(self.slot[i])
    
    def Close(self):
        """Close the window."""
        self.Hide()
    
    def Destroy(self):
        """Destroy the window and clean up resources."""
        for slot in self.slot.values():
            if hasattr(slot, 'ClearDictionary'):
                slot.ClearDictionary()
        
        self.slot.clear()
        
        if hasattr(self, 'scrollBar') and self.scrollBar:
            self.scrollBar.Destroy()
            self.scrollBar = None
        
        self.Hide()
        self.ClearDictionary()
    
    def Show(self):
        """Show the window."""
        self.__LoadWindow()
        super(BonusWindow, self).Show()
    
    def Open(self):
        """Open the window (alias for Show)."""
        self.Show()
    
    def OnPressEscapeKey(self):
        """Handle escape key press."""
        self.Close()
        return True