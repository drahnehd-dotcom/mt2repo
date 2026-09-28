import ui
import localeInfo
import net
import app
import chat
import uiCommon


class BaseCaptcha(ui.Board):
    """Okno weryfikacji anty-bot.

    Wyzwanie generuje i ocenia WYLACZNIE serwer - klient dostaje pakietem
    komplet danych do narysowania i odsyla indeks klikniety przez gracza.
    Okno nie wie, ktory obrazek jest poprawny, i nie zamyka sie samo:
    zamkniecie przychodzi dopiero po akceptacji odpowiedzi przez serwer.
    """

    SLOT_COUNT = 12
    MAX_ICON_SET = 13

    def __init__(self):
        super(BaseCaptcha, self).__init__()
        self.Initialize()
        self.Constructor()
        self.LoadWindow()

    def __del__(self):
        super(BaseCaptcha, self).__del__()

    def Initialize(self):
        self.challengeID = 0
        self.answerSeconds = 0
        self.endTime = 0
        self.answered = False
        self.slotButtons = []
        self.BackgroundShadow = None
        self.remainingTimeGauge = None
        self.remainingTimeText = None

    def Destroy(self):
        self.Hide()

        if self.BackgroundShadow:
            self.BackgroundShadow.Hide()

        self.Initialize()

    def Constructor(self):
        self._setup_background_shadow()

    def _setup_background_shadow(self):
        self.BackgroundShadow = uiCommon.BackgroundShadow(1)
        self.BackgroundShadow.Hide()
        self.SetParent(self.BackgroundShadow)

    def LoadWindow(self):
        """Budowa okna - do nadpisania przez konkretny typ wyzwania."""
        pass

    def _setup_common_ui_elements(self):
        self.remainingTimeGauge = ui.Gauge()
        self.remainingTimeGauge.SetParent(self)
        self.remainingTimeGauge.MakeGauge(190, "white")
        self.remainingTimeGauge.Show()

        self.remainingTimeText = ui.TextLine()
        self.remainingTimeText.SetParent(self)
        self.remainingTimeText.Show()

    def Open(self, challengeID, iconSet, imageMask, seconds):
        """Pokazuje wyzwanie przyslane przez serwer."""
        self.challengeID = challengeID
        self.answerSeconds = max(1, int(seconds))
        self.endTime = app.GetTime() + self.answerSeconds
        self.answered = False

        self._apply_challenge(iconSet, imageMask)
        self._update_timer_display()

        self.BackgroundShadow.Show()
        self.Show()

    def Close(self):
        self.answered = True
        self.Hide()
        self.BackgroundShadow.Hide()

    def _apply_challenge(self, iconSet, imageMask):
        """Podmienia grafiki slotow - do nadpisania przez typ wyzwania."""
        pass

    def OnAnswerRejected(self):
        """Serwer odrzucil odpowiedz. Kolejne wyzwanie przyjdzie osobnym pakietem."""
        chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.SECURITY_YOU_HAVE_ONE_MORE_CHANGE)
        self.answered = True

    def OnAnswerAccepted(self):
        chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.SECURITY_ANSWER_SUCCESS)
        self.Close()

    def _send_answer(self, slotIndex):
        # Jedna odpowiedz na wyzwanie - serwer i tak odrzuci kolejne z tym samym ID,
        # ale nie ma po co ich wysylac.
        if self.answered or not self.challengeID:
            return

        self.answered = True
        net.SendBotControlAnswerPacket(self.challengeID, slotIndex)

    def OnUpdate(self):
        self._update_timer_display()

    def _update_timer_display(self):
        # Licznik jest tylko informacyjny - o uplywie czasu decyduje serwer,
        # ktory po przekroczeniu limitu sam przysle kolejne wyzwanie.
        remaining_time = max(0, self.endTime - app.GetTime())

        if self.remainingTimeText:
            self.remainingTimeText.SetText(localeInfo.SECURITY_REMAINING_TIME.format(remaining_time))

        if self.remainingTimeGauge:
            self.remainingTimeGauge.SetPercentage(remaining_time, self.answerSeconds)

    def OnPressEscapeKey(self):
        # Captcha jest modalna - ESC jej nie zamyka.
        return True


class FindTheDifferentCaptcha(BaseCaptcha):
    """Wyzwanie: kliknij obrazek rozniacy sie od pozostalych."""

    PATH_IMAGE = "kowal/pickthewrongone/"

    SLOT_START_X = 30
    SLOT_START_Y = 50
    SLOT_STEP_X = 58
    SLOT_STEP_Y = 58
    SLOTS_PER_ROW = 4

    def Initialize(self):
        super(FindTheDifferentCaptcha, self).Initialize()
        self.bgImage = None
        self.questionText = None

    def LoadWindow(self):
        self.SetSize(280, 275)
        self.SetCenterPosition()

        self._create_background()
        self._create_question_text()
        self._create_slot_buttons()
        self._setup_common_ui_elements()
        self._position_timer_elements()

    def _create_background(self):
        self.bgImage = ui.ThinBoard()
        self.bgImage.SetParent(self)
        self.bgImage.SetSize(260, 255)
        self.bgImage.SetPosition(10, 10)
        self.bgImage.Show()

    def _create_question_text(self):
        self.questionText = ui.TextLine()
        self.questionText.SetParent(self)
        self.questionText.SetPosition(40, 20)
        self.questionText.SetText(localeInfo.SECURITY_FIND_THE_DIFFERENT)
        self.questionText.Show()

    def _create_slot_buttons(self):
        # Sloty powstaja RAZ; kolejne wyzwania tylko podmieniaja grafiki.
        # Wczesniej kazde odswiezenie tworzylo nowy komplet przyciskow, ktore
        # nakladaly sie na poprzednie.
        self.slotButtons = []

        for index in range(self.SLOT_COUNT):
            x_pos, y_pos = self._calculate_slot_position(index)

            button = ui.MakeButton(self, x_pos, y_pos, False, self.PATH_IMAGE,
                                   "0/0.png", "", "", True)
            button.SetEvent(ui.__mem_func__(self.OnSlotClick), index)
            button.Hide()

            self.slotButtons.append(button)

    def _calculate_slot_position(self, index):
        row = index // self.SLOTS_PER_ROW
        column = index % self.SLOTS_PER_ROW

        return (self.SLOT_START_X + self.SLOT_STEP_X * column,
                self.SLOT_START_Y + self.SLOT_STEP_Y * row)

    def _position_timer_elements(self):
        if self.remainingTimeGauge:
            self.remainingTimeGauge.SetPosition(42, 235)
        if self.remainingTimeText:
            self.remainingTimeText.SetPosition(95, 245)

    def _apply_challenge(self, iconSet, imageMask):
        iconSet = max(0, min(int(iconSet), self.MAX_ICON_SET))

        for index, button in enumerate(self.slotButtons):
            imageIndex = (int(imageMask) >> index) & 1
            imagePath = "{}{}/{}.png".format(self.PATH_IMAGE, iconSet, imageIndex)

            button.SetUpVisual(imagePath)
            button.SetOverVisual(imagePath)
            button.SetDownVisual(imagePath)
            button.Show()

    def OnSlotClick(self, index):
        self._send_answer(index)
