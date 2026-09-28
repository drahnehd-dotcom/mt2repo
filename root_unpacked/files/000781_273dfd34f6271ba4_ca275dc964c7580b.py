import ui
import net
import localeInfo
import uiScriptLocale
import event
import uiCommon


class CardsInfoWindow(ui.ScriptWindow):
    """Main information window for the cards game with rules and start options."""
    
    class DescriptionBox(ui.Window):
        """Inner class for handling description rendering."""
        
        def __init__(self):
            super(CardsInfoWindow.DescriptionBox, self).__init__()
            self.descIndex = 0
            
        def __del__(self):
            super(CardsInfoWindow.DescriptionBox, self).__del__()
            
        def SetIndex(self, index):
            """Set the description index for rendering."""
            self.descIndex = index
            
        def OnRender(self):
            """Render the event set for the description."""
            event.RenderEventSet(self.descIndex)

    def __init__(self):
        super(CardsInfoWindow, self).__init__()
        self.descIndex = 0
        self.scrollPos = 0
        self.safemode = 1
        self.questionDialog = None
        self.descriptionBox = None
        
        # UI elements
        self.titleBar = None
        self.textBoard = None
        self.scrollBar = None
        self.checkButton = None
        self.checkButton2 = None
        self.startButton = None
        
        self.LoadWindow()

    def __del__(self):
        super(CardsInfoWindow, self).__del__()

    def LoadWindow(self):
        """Load the UI script and bind all UI elements."""
        try:
            pyScrLoader = ui.PythonScriptLoader()
            pyScrLoader.LoadScriptFile(self, "UIScript/minigamerumiwaitingpage.py")
        except Exception:
            import exception
            exception.Abort("CardsInfoWindow.LoadWindow.LoadScript")

        self._BindObjects()
        self._SetupEvents()

    def _BindObjects(self):
        """Bind all UI objects from the script."""
        try:
            GetObject = self.GetChild
            self.titleBar = GetObject("titlebar")
            self.textBoard = GetObject("desc_board")
            self.scrollBar = GetObject("scrollbar")
            self.checkButton = GetObject("check_image")
            self.checkButton2 = GetObject("confirm_check_button")
            self.startButton = GetObject("game_start_button")
        except Exception:
            import exception
            exception.Abort("CardsInfoWindow._BindObjects")

    def _SetupEvents(self):
        """Setup all event handlers for UI elements."""
        self.titleBar.SetCloseEvent(ui.__mem_func__(self._OnCloseButtonClick))
        self.scrollBar.SetPos(0.0)
        self.scrollBar.SetScrollEvent(ui.__mem_func__(self.OnScroll))
        self.checkButton.SetEvent(ui.__mem_func__(self._OnSafeMode))
        self.checkButton2.SetEvent(ui.__mem_func__(self._OnSafeMode))
        self.startButton.SetEvent(ui.__mem_func__(self._OnStartQuestion))

    def Destroy(self):
        """Clean up all resources."""
        self.ClearDictionary()
        self.titleBar = None
        self.textBoard = None
        self.descriptionBox = None
        self.scrollPos = None
        self.safemode = None
        self.questionDialog = None
    
    def Open(self):
        """Open the cards info window."""
        self._SetDescriptionEvent()
        self._CreateDescriptionBox()
        self.scrollBar.SetPos(0.0)
        self.Show()

    def Close(self):
        """Close the cards info window and clean up events."""
        event.ClearEventSet(self.descIndex)
        self.descIndex = 0
        self.Hide()
        
    def _OnStartQuestion(self):
        """Show confirmation dialog before starting the game."""
        questionDialog = uiCommon.QuestionDialog2()
        questionDialog.SetText1(localeInfo.MINI_GAME_RUMI_START_QUESTION % (3000, 1))
        questionDialog.SetText2(localeInfo.MINI_GAME_RUMI_START_QUESTION2)
        questionDialog.SetAcceptEvent(ui.__mem_func__(self._OnStart))
        questionDialog.SetCancelEvent(ui.__mem_func__(self.OnCloseQuestionDialog))
        questionDialog.Open()
        self.questionDialog = questionDialog
        
    def OnCloseQuestionDialog(self):
        """Close the currently open question dialog."""
        if self.questionDialog:
            self.questionDialog.Close()
            self.questionDialog = None
        
    def _OnStart(self):
        """Start the cards game with current settings."""
        self.OnCloseQuestionDialog()
        self.Close()
        net.SendChatPacket("/cards o " + str(self.safemode))
        
    def _OnSafeMode(self):
        """Toggle safe mode on/off."""
        if self.safemode == 0:
            self.safemode = 1
            self.checkButton.Show()
        else:
            self.checkButton.Hide()
            self.safemode = 0
        
    def OnUpdate(self):
        """Update the description box position and content."""
        xposEventSet, yposEventSet = self.textBoard.GetGlobalPosition()
        event.UpdateEventSet(
            self.descIndex, 
            xposEventSet + 7, 
            -(yposEventSet + 7 - (int(self.scrollPos) * 16))
        )
        self.descriptionBox.SetIndex(self.descIndex)
        
    def OnScroll(self):
        """Handle scrollbar events."""
        import math
        pos = self.scrollBar.GetPos()
        line_count = event.GetLineCount(self.descIndex) - 18
        if line_count > 0:
            self.scrollPos = math.floor(pos / (1.0 / line_count) + 0.001)
        else:
            self.scrollPos = 0
        event.SetVisibleStartLine(self.descIndex, int(self.scrollPos))
        event.Skip(self.descIndex)

    def _SetDescriptionEvent(self):
        """Setup the description event set."""
        event.ClearEventSet(self.descIndex)
        self.descIndex = event.RegisterEventSet(uiScriptLocale.CARDS_DESC)
        event.SetRestrictedCount(self.descIndex, 100)
        event.SetVisibleLineCount(self.descIndex, 18)

    def _CreateDescriptionBox(self):
        """Create and show the description box."""
        self.descriptionBox = self.DescriptionBox()
        self.descriptionBox.Show()

    def _OnCloseButtonClick(self):
        """Handle close button click."""
        self.Close()

    def OnPressEscapeKey(self):
        """Handle escape key press."""
        if hasattr(self, 'eventClose') and self.eventClose:
            self.eventClose()
        return True


class CardsWindow(ui.ScriptWindow):
    """Main game window for playing the cards game."""
    
    CARDS_ICONS = {    
        1: "d:/ymir work/ui/minigame/rumi/card/card_blue_%d.sub",
        2: "d:/ymir work/ui/minigame/rumi/card/card_red_%d.sub",
        3: "d:/ymir work/ui/minigame/rumi/card/card_yellow_%d.sub",
    }
    
    def __init__(self):
        super(CardsWindow, self).__init__()
        self.safemode = 0
        self.questionDialog = None
        
        # UI elements
        self.titleBar = None
        self.handSlot = None
        self.fieldSlot = None
        self.deckSlot = None
        self.score_completion_effect1 = None
        self.score_completion_effect2 = None
        self.score_completion_effect3 = None
        self.score_completion_text_effect = None
        self.deck_flush_effect = None
        self.cards_count = None
        self.total_points = None
        self.field_points = None
        self.exitButton = None
        
        self.LoadWindow()

    def __del__(self):
        super(CardsWindow, self).__del__()

    def LoadWindow(self):
        """Load the game UI script and setup all elements."""
        try:
            pyScrLoader = ui.PythonScriptLoader()
            pyScrLoader.LoadScriptFile(self, "UIScript/minigamerumigamepage.py")
        except Exception:
            import exception
            exception.Abort("CardsWindow.LoadWindow.LoadScript")

        self._BindObjects()
        self._SetupEvents()
        self.HideEffects()

    def _BindObjects(self):
        """Bind all UI objects from the script."""
        try:
            GetObject = self.GetChild
            self.titleBar = GetObject("titlebar")
            self.handSlot = GetObject("HandCardSlot")
            self.fieldSlot = GetObject("FieldCardSlot")
            self.deckSlot = GetObject("DeckCardSlot")
            self.score_completion_effect1 = GetObject("score_completion_effect1")
            self.score_completion_effect2 = GetObject("score_completion_effect2")
            self.score_completion_effect3 = GetObject("score_completion_effect3")
            self.score_completion_text_effect = GetObject("score_completion_text_effect")
            self.deck_flush_effect = GetObject("deck_flush_effect")
            self.cards_count = GetObject("card_cnt_text")
            self.total_points = GetObject("total_score")
            self.field_points = GetObject("score_number_text")
            self.exitButton = GetObject("game_exit_button")
        except Exception:
            import exception
            exception.Abort("CardsWindow._BindObjects")

    def _SetupEvents(self):
        """Setup all event handlers for UI elements."""
        self.titleBar.SetCloseEvent(ui.__mem_func__(self._OnCloseButtonClick))
        self.handSlot.SAFE_SetButtonEvent("LEFT", "EXIST", self.SetSelectItemSlotEvent)
        self.handSlot.SAFE_SetButtonEvent("RIGHT", "EXIST", self.SetUnselectItemSlotEvent)
        self.fieldSlot.SAFE_SetButtonEvent("LEFT", "EXIST", self.SetSelectItemSlotEvent2)
        self.score_completion_effect1.SetOnEndFrame(ui.__mem_func__(self._OnEndFrame))
        self.deckSlot.SAFE_SetButtonEvent("LEFT", "ALWAYS", self.SetPickCardFromDeck)
        self.exitButton.SetEvent(ui.__mem_func__(self._EndGame))
        
    def SetPickCardFromDeck(self, slotIndex):
        """Handle picking a card from the deck."""
        if int(self.cards_count.GetText()) < 1:
            return
        net.SendChatPacket("/cards p")
        
    def SetSelectItemSlotEvent(self, slotIndex):
        """Handle selecting a card from hand."""
        net.SendChatPacket("/cards a " + str(slotIndex))
        
    def SetSelectItemSlotEvent2(self, slotIndex):
        """Handle selecting a card from field."""
        net.SendChatPacket("/cards r " + str(slotIndex))
        
    def SetUnselectItemSlotEvent(self, slotIndex):
        """Handle unselecting/discarding a card."""
        if self.safemode == 1:
            questionDialog = uiCommon.QuestionDialog()
            questionDialog.SetText(localeInfo.MINI_GAME_RUMI_DISCARD_QUESTION)
            questionDialog.SetAcceptEvent(lambda: self.DestroyCard(slotIndex))
            questionDialog.SetCancelEvent(ui.__mem_func__(self.OnCloseQuestionDialog))
            questionDialog.Open()
            self.questionDialog = questionDialog
        else:
            self.DestroyCard(slotIndex)
            
    def _EndGame(self):
        """Show confirmation dialog before ending the game."""
        questionDialog = uiCommon.QuestionDialog2()
        questionDialog.SetText1(localeInfo.MINI_GAME_RUMI_EXIT_QUESTION)
        questionDialog.SetText2(localeInfo.MINI_GAME_RUMI_EXIT_QUESTION2)
        questionDialog.SetAcceptEvent(ui.__mem_func__(self.OnEndGame))
        questionDialog.SetCancelEvent(ui.__mem_func__(self.OnCloseQuestionDialog))
        questionDialog.Open()
        self.questionDialog = questionDialog
        
    def OnEndGame(self):
        """End the game and close the window."""
        net.SendChatPacket("/cards e")
        self.OnCloseQuestionDialog()
        self.Close()
        
    def DestroyCard(self, index):
        """Destroy/discard a card at the given index."""
        net.SendChatPacket("/cards d " + str(index))
        self.OnCloseQuestionDialog()
        
    def OnCloseQuestionDialog(self):
        """Close the currently open question dialog."""
        if self.questionDialog:
            self.questionDialog.Close()
            self.questionDialog = None
        
    def _OnEndFrame(self):
        """Handle end of effect animation frame."""
        self.HideEffects()
        
    def UpdateCardsInfo(self, hand_1, hand_1_v, hand_2, hand_2_v, hand_3, hand_3_v, 
                       hand_4, hand_4_v, hand_5, hand_5_v, cards_left, points):
        """Update the display of cards in hand and game stats."""
        hand_cards = [
            (hand_1, hand_1_v, 0),
            (hand_2, hand_2_v, 1),
            (hand_3, hand_3_v, 2),
            (hand_4, hand_4_v, 3),
            (hand_5, hand_5_v, 4)
        ]
        
        for card_type, card_value, slot_index in hand_cards:
            if card_type == 0:
                self.handSlot.ClearSlot(slot_index)
            else:
                icon_path = self.CARDS_ICONS[card_type] % int(card_value)
                self.handSlot.SetCardSlot(slot_index, 10, icon_path)
                
        self.cards_count.SetText(str(cards_left))
        self.total_points.SetText(str(points))
        self.UpdateDeckSlot()
        
    def UpdateCardsFieldInfo(self, slot1, slot1_v, slot2, slot2_v, slot3, slot3_v, points):
        """Update the display of cards in the field."""
        field_cards = [
            (slot1, slot1_v, 0),
            (slot2, slot2_v, 1),
            (slot3, slot3_v, 2)
        ]
        
        for card_type, card_value, slot_index in field_cards:
            if card_type == 0:
                self.fieldSlot.ClearSlot(slot_index)
            else:
                icon_path = self.CARDS_ICONS[card_type] % int(card_value)
                self.fieldSlot.SetCardSlot(slot_index, 10, icon_path)
                
        self.field_points.SetText(str(points))
        
    def UpdateDeckSlot(self):
        """Update the visual representation of the deck based on remaining cards."""
        cards_remaining = int(self.cards_count.GetText())
        
        # Clear all deck slots first
        for i in range(3):
            self.deckSlot.ClearSlot(i)
            
        if cards_remaining > 16:
            self.deckSlot.SetCardSlot(2, 10, "d:/ymir work/ui/minigame/rumi/deck/deck3.sub")
            self.deckSlot.SetCardSlot(1, 10, "d:/ymir work/ui/minigame/rumi/deck/deck2.sub")
        elif 8 < cards_remaining <= 16:
            self.deckSlot.SetCardSlot(1, 10, "d:/ymir work/ui/minigame/rumi/deck/deck2.sub")
        elif 0 < cards_remaining <= 8:
            self.deckSlot.SetCardSlot(0, 10, "d:/ymir work/ui/minigame/rumi/deck/deck1.sub")
        
    def CardsPutReward(self, slot1, slot1_v, slot2, slot2_v, slot3, slot3_v, points):
        """Display reward effects when cards are successfully placed."""
        effects = [
            self.score_completion_effect1,
            self.score_completion_effect2,
            self.score_completion_effect3,
            self.score_completion_text_effect
        ]
        
        for effect in effects:
            effect.ResetFrame()
            effect.Show()

    def HideEffects(self):
        """Hide all visual effects and reset field points."""
        effects = [
            self.score_completion_effect1,
            self.score_completion_effect2,
            self.score_completion_effect3,
            self.score_completion_text_effect,
            self.deck_flush_effect
        ]
        
        for effect in effects:
            effect.Hide()
            
        self.field_points.SetText("0")

    def Destroy(self):
        """Clean up all resources."""
        self.ClearDictionary()
        
        # Clear all UI element references
        ui_elements = [
            'titleBar', 'handSlot', 'fieldSlot', 'deckSlot',
            'score_completion_effect1', 'score_completion_effect2',
            'score_completion_effect3', 'score_completion_text_effect',
            'deck_flush_effect', 'cards_count', 'total_points',
            'field_points', 'exitButton'
        ]
        
        for element in ui_elements:
            setattr(self, element, None)
            
        self.safemode = None
        self.questionDialog = None

    def Open(self, safemode):
        """Open the cards game window with specified safe mode."""
        self.safemode = safemode
        self.Show()

    def Close(self):
        """Close the cards game window."""
        self.Hide()

    def _OnCloseButtonClick(self):
        """Handle close button click."""
        self.Close()

    def OnPressEscapeKey(self):
        """Handle escape key press."""
        if hasattr(self, 'eventClose') and self.eventClose:
            self.eventClose()
        return True


class IngameWindow(ui.ScriptWindow):
    """In-game window that provides access to the cards minigame."""
    
    def __init__(self):
        super(IngameWindow, self).__init__()
        self.gameButton = None
        self.window = None
        self.LoadWindow()

    def __del__(self):
        super(IngameWindow, self).__del__()

    def LoadWindow(self):
        """Load the in-game UI script and setup elements."""
        try:
            pyScrLoader = ui.PythonScriptLoader()
            pyScrLoader.LoadScriptFile(self, "UIScript/minigamewindow.py")
        except Exception:
            import exception
            exception.Abort("IngameWindow.LoadWindow.LoadScript")

        self._BindObjects()
        self._SetupEvents()

    def _BindObjects(self):
        """Bind UI objects from the script."""
        try:
            GetObject = self.GetChild
            self.gameButton = GetObject("minigame_rumi_button")
        except Exception:
            import exception
            exception.Abort("IngameWindow._BindObjects")

    def _SetupEvents(self):
        """Setup event handlers for UI elements."""
        self.gameButton.SetEvent(ui.__mem_func__(self._OnClickGame))
        
    def _OnClickGame(self):
        """Handle clicking the game button to open cards info window."""
        self.window = CardsInfoWindow()
        self.window.Open()
        
    def Destroy(self):
        """Clean up all resources."""
        self.ClearDictionary()
        self.gameButton = None
        if self.window:
            self.window.Destroy()
            self.window = None
			