"""Battle Pass - UI klienta (KowalMT2).

Layout wg projektu graficznego 799x415, assety w d:/ymir work/ui/battle_pass/.
Statyczna chromowka: uiscript/battlepasswindow.py
Elementy dynamiczne (kolumny nagrod, wiersze zadan, scrollbary) buduje ten plik.

Nagrody przyznaje serwer automatycznie przy awansie poziomu
(char.cpp BattlePassAction -> AutoGiveItem), nie ma packetu "odbierz",
wiec slot ma tylko dwa stany: odebrane (ptaszek) albo zablokowane (klodka).

Przewijanie obu list jest skokowe (o cale kolumny/wiersze). Dzieki temu
zaden slot nie wystaje poza kontener i nie trzeba recznego klipowania,
ktore w poprzedniej wersji odpowiadalo za znikajace teksty.
"""

import datetime
from _weakref import proxy

import app
import battlepass
import localeInfo
import net
import ui
import uiCommon
import uiToolTip


# ---------------------------------------------------------------- stale

IMAGE_PATH = "d:/ymir work/ui/battle_pass/"

BOARD_REWARDS = 0
BOARD_MISSIONS = 1

POINTS_PER_LEVEL = 10000
MAX_LEVEL = 30

PERIOD_DAILY = 0
PERIOD_WEEKLY = 1

# Misje, ktorych progres serwer liczy w MINUTACH, a gracz ma widziec GODZINY.
# Serwer nie przysyla typu misji (GCMissionDef go nie niesie), wiec rozpoznajemy je
# po kluczu locale z pola "desc" w battlepass.json. Gdy klucz sie zmieni, licznik
# pokaze minuty - brzydko, ale bez wyjatku.
MINUTES_PER_HOUR = 60
HOUR_PROGRESS_MISSIONS = frozenset((
    "BATTLEPASS_MISSION_PLAYTIME_WEEKLY",
))

# --- tor nagrod (wsp. wzgledem kontenera RewardColumnSlot) ---
REWARD_VISIBLE_COLUMNS = 7
REWARD_STEP_X = 95
REWARD_COLUMN_W = 93
REWARD_COLUMN_H = 259
REWARD_PREMIUM_DY = 146
REWARD_ICON_POS = (30, 28)
REWARD_LOCK_POS = (27, 78)
REWARD_DONE_POS = (30, 76)
REWARD_PLATE_TEXT_POS = (46, 127)

# --- lista zadan (wsp. wzgledem kontenera MissionRowSlot) ---
MISSION_VISIBLE_ROWS = 4
MISSION_COLUMN_X = (0, 361)
MISSION_ROW_STEP_Y = 80
MISSION_ROW_W = 350
MISSION_ROW_H = 82
MISSION_REWARD_TEXT_POS = (42, 65)
MISSION_TITLE_POS = (100, 15)
MISSION_TITLE_LIMIT_W = 232          # pasmo tytulu konczy sie na x=334
MISSION_GAUGE_POS = (108, 33)
MISSION_PROGRESS_TEXT_POS = (213, 39)
MISSION_PERIOD_TEXT_POS = (148, 62)
MISSION_STATUS_TEXT_POS = (277, 62)

COLOR_TEXT = 0xFFE8E0CC
COLOR_DIM = 0xFF9A8F78
COLOR_DONE = 0xFF8CE05A


# ---------------------------------------------------------------- helpery

def FormatNumber(number):
    """Skraca duze liczby: 12500 -> 12.5k (progres misji potrafi byc ogromny)."""
    for exponent, suffix in ((12, "kkkk"), (9, "kkk"), (6, "kk"), (3, "k")):
        if number >= 10 ** exponent:
            return "%.1f%s" % (number / float(10 ** exponent), suffix)
    return str(number)


def FormatTimeLeft(endTimestamp):
    """Zwraca '2d 5h 30min' albo pusty string gdy czas minal."""
    now = app.GetGlobalTimeStamp()
    if now >= endTimestamp:
        return ""

    delta = datetime.timedelta(seconds=endTimestamp - now)
    days = delta.days
    hours = delta.seconds // 3600
    minutes = (delta.seconds // 60) % 60

    parts = []
    if days > 0:
        parts.append("%dd" % days)
    if hours > 0:
        parts.append("%dh" % hours)
    if minutes > 0:
        parts.append("%dmin" % minutes)
    return " ".join(parts) if parts else "<1min"


def ResolveMissionTitle(missionId, description, maxProgress):
    """Opis z serwera to klucz locale; podstawia liczbe do %d jesli jest."""
    if not description or description == "None":
        return localeInfo.BATTLEPASS_MISSION_MISSING.format(missionId)

    text = getattr(localeInfo, description, description)
    try:
        return text % maxProgress
    except (TypeError, ValueError):
        return text


# ---------------------------------------------------------------- scrollbar

class StepScrollBar(ui.Window):
    """Scrollbar na obrazkach przewijajacy o cale kroki.

    Uchwyt jedzie plynnie za mysza, a zawartosc przeskakuje o cala
    kolumne/wiersz. SetStep() ustawia uchwyt programowo - DragButton
    wola OnMove tylko gdy jest wcisniety, wiec nie ma rekurencji.
    """

    def __init__(self, isVertical, backgroundImage, thumbImages, thumbWidth, thumbHeight):
        ui.Window.__init__(self)

        self.isVertical = isVertical
        self.thumbWidth = thumbWidth
        self.thumbHeight = thumbHeight
        self.stepCount = 1
        self.curStep = 0
        self.eventScroll = None

        self.background = ui.ImageBox()
        self.background.SetParent(self)
        self.background.LoadImage(backgroundImage)
        self.background.SetPosition(0, 0)
        self.background.AddFlag("not_pick")
        self.background.Show()

        self.thumb = ui.DragButton()
        self.thumb.SetParent(self)
        self.thumb.SetUpVisual(thumbImages[0])
        self.thumb.SetOverVisual(thumbImages[1])
        self.thumb.SetDownVisual(thumbImages[2])
        self.thumb.SetSize(thumbWidth, thumbHeight)
        self.thumb.SetPosition(0, 0)
        self.thumb.SetMoveEvent(ui.__mem_func__(self.OnThumbMove))
        self.thumb.Show()

    def __del__(self):
        ui.Window.__del__(self)
        self.eventScroll = None

    def Destroy(self):
        self.eventScroll = None
        self.background = None
        self.thumb = None

    def SetScrollEvent(self, event):
        self.eventScroll = event

    def SetTrackSize(self, width, height):
        self.SetSize(width, height)
        self.background.SetSize(width, height)
        if self.isVertical:
            self.thumb.SetRestrictMovementArea(0, 0, self.thumbWidth, height)
        else:
            self.thumb.SetRestrictMovementArea(0, 0, width, self.thumbHeight)

    def GetTravel(self):
        if self.isVertical:
            return max(0, self.GetHeight() - self.thumbHeight)
        return max(0, self.GetWidth() - self.thumbWidth)

    def SetStepCount(self, count):
        # Uchwyt zostaje widoczny nawet przy jednym kroku (tak jest w projekcie);
        # przy stepCount == 1 handlery i tak wychodza wczesniej, wiec nie jedzie.
        self.stepCount = max(1, count)
        self.SetStep(min(self.curStep, self.stepCount - 1), False)

    def GetStep(self):
        return self.curStep

    def SetStep(self, step, notify=True):
        step = max(0, min(self.stepCount - 1, step))
        self.curStep = step

        travel = self.GetTravel()
        offset = 0
        if self.stepCount > 1:
            offset = int(travel * step / float(self.stepCount - 1))
        if self.isVertical:
            self.thumb.SetPosition(0, offset)
        else:
            self.thumb.SetPosition(offset, 0)

        if notify and self.eventScroll:
            self.eventScroll(step)

    def OnThumbMove(self):
        if self.stepCount <= 1:
            return

        travel = self.GetTravel()
        if travel <= 0:
            return

        localX, localY = self.thumb.GetLocalPosition()
        ratio = float(localY if self.isVertical else localX) / float(travel)
        step = int(round(ratio * (self.stepCount - 1)))
        step = max(0, min(self.stepCount - 1, step))

        if step != self.curStep:
            self.curStep = step
            if self.eventScroll:
                self.eventScroll(step)

    def OnMouseLeftButtonDown(self):
        if self.stepCount <= 1:
            return

        travel = self.GetTravel()
        if travel <= 0:
            return

        mouseX, mouseY = self.GetMouseLocalPosition()
        if self.isVertical:
            picked = mouseY - self.thumbHeight // 2
        else:
            picked = mouseX - self.thumbWidth // 2
        self.SetStep(int(round(float(picked) / float(travel) * (self.stepCount - 1))))

    def OnMouseWheel(self, length):
        if self.stepCount <= 1:
            return False

        before = self.curStep
        self.SetStep(before - 1 if length > 0 else before + 1)
        # Na obu koncach toru oddajemy zdarzenie wyzej zamiast je polykac.
        return self.curStep != before


def MakeHorizontalScrollBar():
    return StepScrollBar(
        False,
        IMAGE_PATH + "horizontal_scrollbar_bg.png",
        (IMAGE_PATH + "horizontal_scrollbar_thumb_normal.png",
         IMAGE_PATH + "horizontal_scrollbar_thumb_hover.png",
         IMAGE_PATH + "horizontal_scrollbar_thumb_down.png"),
        29, 16)


def MakeVerticalScrollBar():
    return StepScrollBar(
        True,
        IMAGE_PATH + "vertical_scrollbar_bg.png",
        (IMAGE_PATH + "vertical_scrollbar_thumb_normal.png",
         IMAGE_PATH + "vertical_scrollbar_thumb_hover.png",
         IMAGE_PATH + "vertical_scrollbar_thumb_down.png"),
        16, 29)


# ---------------------------------------------------------------- kolumna nagrod

class RewardColumn(ui.Window):
    """Jedna kolumna toru: slot zwykly + premium + plakietka z numerem poziomu."""

    def __init__(self, parent, columnIndex, overInEvent, overOutEvent):
        ui.Window.__init__(self)

        self.rewardIndex = -1
        self.freeVnum = 0
        self.premiumVnum = 0

        self.SetParent(parent)
        self.SetPosition(columnIndex * REWARD_STEP_X, 0)
        self.SetSize(REWARD_COLUMN_W, REWARD_COLUMN_H)
        # "attach" przekierowuje klikniecie na okno glowne, inaczej kolumna
        # przechwytuje capture i nie da sie przeciagnac okna za tor nagrod.
        self.AddFlag("attach")
        self.Show()

        self.freeBoard = self.__MakeBoard(0, IMAGE_PATH + "bg_zwykle_nagroda.png")
        self.premiumBoard = self.__MakeBoard(REWARD_PREMIUM_DY, IMAGE_PATH + "bg_premium_nagroda.png")

        self.freeSlot = self.__MakeSlot(0)
        self.premiumSlot = self.__MakeSlot(REWARD_PREMIUM_DY)

        self.freeStatus = self.__MakeStatus()
        self.premiumStatus = self.__MakeStatus()

        self.levelText = ui.TextLine()
        self.levelText.SetParent(self)
        self.levelText.SetPosition(*REWARD_PLATE_TEXT_POS)
        self.levelText.SetHorizontalAlignCenter()
        self.levelText.SetVerticalAlignCenter()
        self.levelText.SetPackedFontColor(COLOR_TEXT)
        self.levelText.SetOutline()
        self.levelText.SetText("")
        self.levelText.AddFlag("not_pick")
        self.levelText.Show()

        self.freeSlot.SetOverInItemEvent(
            lambda slotIndex, r=proxy(self), cb=overInEvent: cb(r.freeVnum))
        self.freeSlot.SetOverOutItemEvent(overOutEvent)
        self.premiumSlot.SetOverInItemEvent(
            lambda slotIndex, r=proxy(self), cb=overInEvent: cb(r.premiumVnum))
        self.premiumSlot.SetOverOutItemEvent(overOutEvent)

    def __del__(self):
        ui.Window.__del__(self)

    def __MakeBoard(self, offsetY, imageName):
        board = ui.ImageBox()
        board.SetParent(self)
        board.LoadImage(imageName)
        board.SetPosition(0, offsetY)
        board.AddFlag("not_pick")
        board.Show()
        return board

    def __MakeSlot(self, offsetY):
        slot = ui.SlotWindow()
        slot.SetParent(self)
        slot.SetPosition(REWARD_ICON_POS[0], REWARD_ICON_POS[1] + offsetY)
        slot.SetSize(32, 32)
        slot.AppendSlot(0, 0, 0, 32, 32)
        slot.Show()
        return slot

    def __MakeStatus(self):
        status = ui.ImageBox()
        status.SetParent(self)
        status.AddFlag("not_pick")
        status.Hide()
        return status

    def Destroy(self):
        self.freeBoard = None
        self.premiumBoard = None
        self.freeSlot = None
        self.premiumSlot = None
        self.freeStatus = None
        self.premiumStatus = None
        self.levelText = None

    def Clear(self):
        self.rewardIndex = -1
        self.freeVnum = 0
        self.premiumVnum = 0
        self.freeSlot.ClearSlot(0)
        self.premiumSlot.ClearSlot(0)
        self.freeStatus.Hide()
        self.premiumStatus.Hide()
        self.levelText.SetText("")
        self.Hide()

    def SetReward(self, rewardIndex, freeReward, premiumReward, level, isPremium):
        self.rewardIndex = rewardIndex
        self.Show()

        self.levelText.SetText(str(rewardIndex + 1))

        self.freeVnum = self.__FillSlot(self.freeSlot, freeReward)
        self.premiumVnum = self.__FillSlot(self.premiumSlot, premiumReward)

        unlocked = rewardIndex < level
        self.__SetStatus(self.freeStatus, 0, unlocked)
        self.__SetStatus(self.premiumStatus, REWARD_PREMIUM_DY, unlocked and isPremium)

    def __FillSlot(self, slot, reward):
        if not reward:
            slot.ClearSlot(0)
            return 0
        vnum = reward["vnum"]
        count = reward["count"] if reward["count"] >= 2 else 0
        slot.SetItemSlot(0, vnum, count)
        return vnum

    def __SetStatus(self, status, offsetY, isDone):
        if isDone:
            status.LoadImage(IMAGE_PATH + "reddemed_icon.png")
            status.SetPosition(REWARD_DONE_POS[0], REWARD_DONE_POS[1] + offsetY)
        else:
            status.LoadImage(IMAGE_PATH + "lock_icon.png")
            status.SetPosition(REWARD_LOCK_POS[0], REWARD_LOCK_POS[1] + offsetY)
        status.Show()


# ---------------------------------------------------------------- wiersz zadania

class MissionRow(ui.Window):
    """Jeden wiersz listy zadan: ikona, tytul, pasek postepu, okres, status."""

    def __init__(self, parent, columnIndex, rowIndex):
        ui.Window.__init__(self)

        # None, NIE 0 - zero jest poprawnym ID misji (pierwsza pozycja w tablicy
        # "missions" configu), a jednoczesnie jest falsy w Pythonie. Uzycie 0 jako
        # znacznika "brak misji" wywalalo RefreshProgress dla misji o ID 0.
        self.missionId = None
        self.maxProgress = 0
        self.progressDivisor = 1
        self.isDone = False

        self.SetParent(parent)
        self.SetPosition(MISSION_COLUMN_X[columnIndex], rowIndex * MISSION_ROW_STEP_Y)
        self.SetSize(MISSION_ROW_W, MISSION_ROW_H)
        self.AddFlag("attach")
        self.Show()

        self.board = ui.ImageBox()
        self.board.SetParent(self)
        self.board.LoadImage(IMAGE_PATH + "quest_bg.png")
        self.board.SetPosition(0, 0)
        self.board.AddFlag("not_pick")
        self.board.Show()

        # Okragle gniazdo po lewej zostaje puste - tak jest w projekcie.
        self.gauge = ui.ExpandedImageBox()
        self.gauge.SetParent(self)
        self.gauge.LoadImage(IMAGE_PATH + "level_gauge.png")
        self.gauge.SetPosition(*MISSION_GAUGE_POS)
        self.gauge.AddFlag("not_pick")
        self.gauge.SetPercentage(0, 1)
        self.gauge.Show()

        self.rewardText = self.__MakeText(MISSION_REWARD_TEXT_POS, True, COLOR_TEXT)
        self.titleText = self.__MakeText(MISSION_TITLE_POS, False, COLOR_TEXT)
        self.titleText.SetLimitWidth(MISSION_TITLE_LIMIT_W)
        self.progressText = self.__MakeText(MISSION_PROGRESS_TEXT_POS, True, COLOR_TEXT)
        self.periodText = self.__MakeText(MISSION_PERIOD_TEXT_POS, True, COLOR_DIM)
        self.statusText = self.__MakeText(MISSION_STATUS_TEXT_POS, True, COLOR_DIM)

    def __del__(self):
        ui.Window.__del__(self)

    def __MakeText(self, position, isCentered, color):
        text = ui.TextLine()
        text.SetParent(self)
        text.SetPosition(*position)
        if isCentered:
            text.SetHorizontalAlignCenter()
        text.SetVerticalAlignCenter()
        text.SetPackedFontColor(color)
        text.SetOutline()
        text.SetText("")
        text.AddFlag("not_pick")
        text.Show()
        return text

    def Destroy(self):
        self.board = None
        self.gauge = None
        self.rewardText = None
        self.titleText = None
        self.progressText = None
        self.periodText = None
        self.statusText = None

    def Clear(self):
        self.missionId = None
        self.maxProgress = 0
        self.progressDivisor = 1
        self.isDone = False
        self.Hide()

    def SetMission(self, missionId):
        """Ustawia czesc statyczna wiersza. Progres idzie przez RefreshProgress."""
        self.missionId = missionId
        self.Show()

        maxProgress, points, description = battlepass.get_mission_info(missionId)
        self.maxProgress = maxProgress
        self.progressDivisor = MINUTES_PER_HOUR if description in HOUR_PROGRESS_MISSIONS else 1
        self.isDone = False

        # Tytul dostaje wartosc PO przeliczeniu, zeby "%d godzin" dalo 36, nie 2160.
        self.titleText.SetText(
            ResolveMissionTitle(missionId, description, maxProgress // self.progressDivisor))
        self.rewardText.SetText("+%d" % points)

        period = battlepass.get_mission_progress(missionId)[2]
        if period == PERIOD_WEEKLY:
            self.periodText.SetText(localeInfo.BATTLEPASS_MISSION_PERIOD_WEEKLY)
        else:
            self.periodText.SetText(localeInfo.BATTLEPASS_MISSION_PERIOD_DAILY)

        self.RefreshProgress()

    def RefreshProgress(self):
        """Wolane co sekunde - korzysta z maxProgress zapamietanego w SetMission,
        zeby nie odpytywac get_mission_info przy kazdym tyknieciu."""
        if self.missionId is None:
            return

        maxProgress = self.maxProgress
        progress, endTime, _ = battlepass.get_mission_progress(self.missionId)

        # Pasek jedzie na surowych jednostkach, wiec przy misji czasowej rosnie co minute,
        # a nie skokowo raz na godzine. Licznik obok pokazuje jednostke dla gracza.
        self.gauge.SetPercentage(min(progress, maxProgress), max(maxProgress, 1))

        divisor = self.progressDivisor
        self.progressText.SetText("%s / %s" % (
            FormatNumber(progress // divisor), FormatNumber(maxProgress // divisor)))

        isDone = bool(maxProgress) and progress >= maxProgress
        self.isDone = isDone

        if isDone:
            self.statusText.SetPackedFontColor(COLOR_DONE)
            self.statusText.SetText(localeInfo.BATTLEPASS_MISSION_DONE)
        else:
            self.statusText.SetPackedFontColor(COLOR_DIM)
            self.statusText.SetText(FormatTimeLeft(endTime) if endTime else "")


# ---------------------------------------------------------------- okno glowne

class BattlePassWindow(ui.ScriptWindow):

    def __init__(self):
        ui.ScriptWindow.__init__(self)
        self.__Initialize()
        self.__LoadWindow()

    def __del__(self):
        ui.ScriptWindow.__del__(self)

    def __Initialize(self):
        self.boardIndex = BOARD_REWARDS
        self.isInitiated = False

        self.points = 0
        self.level = 0
        self.isPremium = False

        self.rewardsFree = []
        self.rewardsPremium = []
        self.rewardCount = 0
        self.rewardOffset = 0

        self.missionsDaily = []
        self.missionsWeekly = []
        self.missionOffset = 0

        self.boardRewards = None
        self.boardMissions = None
        self.tabButton = None
        self.levelPanel = None
        self.levelGauge = None
        self.levelText = None
        self.pointsText = None

        self.rewardColumns = []
        self.missionRows = []
        self.rewardScroll = None
        self.missionScroll = None

        self.tooltipItem = None
        self.questionDialog = None
        self.lastTimeText = ""
        self.lastTickStamp = 0

    def __LoadWindow(self):
        try:
            scriptLoader = ui.PythonScriptLoader()
            scriptLoader.LoadScriptFile(self, "uiscript/battlepasswindow.py")
        except Exception:
            import exception
            exception.Abort("BattlePassWindow.__LoadWindow.LoadScriptFile")

        try:
            self.boardRewards = self.GetChild("BoardRewards")
            self.boardMissions = self.GetChild("BoardMissions")
            self.tabButton = self.GetChild("TabButton")
            self.levelPanel = self.GetChild("LevelPanel")
            self.levelGauge = self.GetChild("LevelGauge")
            self.levelText = self.GetChild("LevelText")
            self.pointsText = self.GetChild("PointsText")
            rewardColumnSlot = self.GetChild("RewardColumnSlot")
            rewardScrollSlot = self.GetChild("RewardScrollSlot")
            missionRowSlot = self.GetChild("MissionRowSlot")
            missionScrollSlot = self.GetChild("MissionScrollSlot")
        except Exception:
            import exception
            exception.Abort("BattlePassWindow.__LoadWindow.BindObject")

        self.GetChild("ExitButton").SAFE_SetEvent(self.Close)
        self.tabButton.SAFE_SetEvent(self.__ToggleBoard)
        self.GetChild("BuyPremiumButton").SAFE_SetEvent(self.__OpenBuyPremiumDialog)

        self.tooltipItem = uiToolTip.ItemToolTip()
        self.tooltipItem.Hide()

        overInEvent = ui.__mem_func__(self.__OnOverInReward)
        overOutEvent = ui.__mem_func__(self.__OnOverOutReward)
        for columnIndex in range(REWARD_VISIBLE_COLUMNS):
            self.rewardColumns.append(
                RewardColumn(rewardColumnSlot, columnIndex, overInEvent, overOutEvent))

        for columnIndex in range(len(MISSION_COLUMN_X)):
            for rowIndex in range(MISSION_VISIBLE_ROWS):
                self.missionRows.append(MissionRow(missionRowSlot, columnIndex, rowIndex))

        self.rewardScroll = MakeHorizontalScrollBar()
        self.rewardScroll.SetParent(rewardScrollSlot)
        self.rewardScroll.SetPosition(0, 0)
        self.rewardScroll.SetTrackSize(rewardScrollSlot.GetWidth(), rewardScrollSlot.GetHeight())
        self.rewardScroll.SetScrollEvent(ui.__mem_func__(self.__OnScrollRewards))
        self.rewardScroll.Show()

        self.missionScroll = MakeVerticalScrollBar()
        self.missionScroll.SetParent(missionScrollSlot)
        self.missionScroll.SetPosition(0, 0)
        self.missionScroll.SetTrackSize(missionScrollSlot.GetWidth(), missionScrollSlot.GetHeight())
        self.missionScroll.SetScrollEvent(ui.__mem_func__(self.__OnScrollMissions))
        self.missionScroll.Show()

        self.questionDialog = uiCommon.QuestionDialog()
        self.questionDialog.SetText(localeInfo.BATTLEPASS_PREMIUM_QUESTION_1)
        self.questionDialog.SAFE_SetAcceptEvent(self.__OnAcceptBuyPremium)
        self.questionDialog.SAFE_SetCancelEvent(self.__OnCancelBuyPremium)
        self.questionDialog.Hide()

        self.__SetBoard(BOARD_REWARDS)
        # Bez tego gauge stoi na pelnym obrazku (expanded_image renderuje sie
        # w calosci dopoki nie dostanie SetPercentage), a teksty sa puste -
        # dokladnie tak wyglada okno, gdy serwer nie przysle INIT.
        self.__RefreshHeader()

    # ---------------------------------------------------------- lifecycle

    def Open(self):
        self.Show()
        self.SetTop()

        # Kazde otwarcie prosi serwer o pelny INIT. Wczesniej szlo to raz na sesje
        # (bramka isInitiated tutaj + early-return w do_battle_pass po stronie serwera),
        # przez co okno potrafilo zostac na starych definicjach misji: stary tytul
        # i stary maxProgress obok swiezego progresu.
        net.SendChatPacket("/battle_pass open 1")

        # Zanim przyjdzie odpowiedz, pokazujemy to, co juz mamy - inaczej okno
        # mrugneloby stanem zerowym.
        if self.isInitiated:
            self.RefreshLocal()
        self.isInitiated = True

    def Close(self):
        self.__OnOverOutReward()
        if self.questionDialog:
            self.questionDialog.Close()
        self.Hide()

    def Destroy(self):
        for column in self.rewardColumns:
            column.Destroy()
        for row in self.missionRows:
            row.Destroy()
        if self.rewardScroll:
            self.rewardScroll.Destroy()
        if self.missionScroll:
            self.missionScroll.Destroy()
        if self.questionDialog:
            self.questionDialog.Close()

        self.ClearDictionary()
        self.__Initialize()

    def OnPressEscapeKey(self):
        self.Close()
        return True

    def OnMouseWheel(self, length):
        scrollBar = self.rewardScroll if self.boardIndex == BOARD_REWARDS else self.missionScroll
        if not scrollBar:
            return False
        return scrollBar.OnMouseWheel(length)

    # ---------------------------------------------------------- odswiezanie

    def RefreshGlobal(self):
        """Pelne odswiezenie - nagrody, misje i stan gracza.

        Wolane prosto z handlera packetu (game.py BINARY_BattlePassInit),
        wiec musi przezyc push serwera przychodzacy po Destroy().
        """
        if not self.rewardScroll:
            return

        self.__ReadPlayerState()

        self.rewardsFree = battlepass.get_rewards_free()
        self.rewardsPremium = battlepass.get_rewards_premium()
        self.rewardCount = min(MAX_LEVEL, max(len(self.rewardsFree), len(self.rewardsPremium)))

        self.__ReadMissionLists()

        rewardSteps = max(1, self.rewardCount - REWARD_VISIBLE_COLUMNS + 1)
        self.rewardOffset = min(self.rewardOffset, rewardSteps - 1)
        self.rewardScroll.SetStepCount(rewardSteps)
        self.rewardScroll.SetStep(self.rewardOffset, False)

        missionRowCount = max(len(self.missionsDaily), len(self.missionsWeekly))
        missionSteps = max(1, missionRowCount - MISSION_VISIBLE_ROWS + 1)
        self.missionOffset = min(self.missionOffset, missionSteps - 1)
        self.missionScroll.SetStepCount(missionSteps)
        self.missionScroll.SetStep(self.missionOffset, False)

        self.__RefreshRewards()
        self.__RefreshMissions()
        self.__RefreshHeader()

    def RefreshLocal(self):
        """Lekkie odswiezenie - punkty, premium i progres misji."""
        if not self.levelPanel:
            return

        self.__ReadPlayerState()
        self.__RefreshRewards()

        # UPDATE potrafi przyniesc INNY zestaw misji: reset dobowy/tygodniowy,
        # /bp_fix_missions reset albo podmiana configu sezonu. Wiersz trzyma
        # missionId i maxProgress zapamietane przy SetMission, wiec bez przepiecia
        # pokazywalby stary tytul i stary licznik obok nowego progresu.
        # Pelne SetMission tylko gdy zestaw faktycznie sie zmienil - inaczej
        # zostaje tani RefreshProgress, tak jak bylo.
        if self.__ReadMissionLists():
            self.__RefreshMissions()
        else:
            for row in self.missionRows:
                row.RefreshProgress()

        self.__RefreshHeader()

    def __ReadMissionLists(self):
        """Przebudowuje listy ID misji z danych klienta.

        Zwraca True, gdy zestaw misji rozni sie od poprzedniego - wtedy wiersze
        trzeba przepiac przez __RefreshMissions, a nie tylko odswiezyc progres.
        """
        daily = []
        weekly = []
        for mission in battlepass.get_missions():
            if mission["type"] == PERIOD_WEEKLY:
                weekly.append(mission["id"])
            else:
                daily.append(mission["id"])

        changed = (daily != self.missionsDaily) or (weekly != self.missionsWeekly)
        self.missionsDaily = daily
        self.missionsWeekly = weekly
        return changed

    def __ReadPlayerState(self):
        points, isPremium = battlepass.get_player_info(0)
        self.points = points
        self.level = min(MAX_LEVEL, points // POINTS_PER_LEVEL)
        self.isPremium = bool(isPremium)

    def __RefreshRewards(self):
        for columnIndex, column in enumerate(self.rewardColumns):
            rewardIndex = self.rewardOffset + columnIndex
            if rewardIndex >= self.rewardCount:
                column.Clear()
                continue

            freeReward = self.rewardsFree[rewardIndex] if rewardIndex < len(self.rewardsFree) else None
            premiumReward = self.rewardsPremium[rewardIndex] if rewardIndex < len(self.rewardsPremium) else None
            column.SetReward(rewardIndex, freeReward, premiumReward, self.level, self.isPremium)

    def __RefreshMissions(self):
        columns = (self.missionsDaily, self.missionsWeekly)
        for index, row in enumerate(self.missionRows):
            columnIndex = index // MISSION_VISIBLE_ROWS
            rowIndex = index % MISSION_VISIBLE_ROWS
            missions = columns[columnIndex]
            missionIndex = self.missionOffset + rowIndex

            if missionIndex >= len(missions):
                row.Clear()
            else:
                row.SetMission(missions[missionIndex])

    def __RefreshHeader(self):
        endTime = battlepass.get_season_settings()["endTime"]

        # endTime == 0 = nie dostalismy jeszcze INIT. Dzieje sie tak przez chwile
        # po Open(), ale TAKZE na stale gdy sezon wygasl - char.cpp:12544-12546
        # w ogole nie wysyla pakietu po endTime. Klient nie odroznia tych dwoch
        # sytuacji, wiec pokazuje stan zerowy zamiast zgadywac "zakonczony".
        if endTime and app.GetGlobalTimeStamp() >= endTime:
            self.levelText.SetText(localeInfo.BATTLEPASS_EXPIRED)
            self.pointsText.SetText(localeInfo.BATTLEPASS_EXP_ENDED)
            self.levelGauge.SetPercentage(0, 1)
            self.__SetSeasonTooltip(localeInfo.BATTLEPASS_EXPIRED)
            return

        # Na maksymalnym poziomie pasek stoi na pelnym. Bez tego przy points
        # >= MAX_LEVEL * POINTS_PER_LEVEL wyszlo by "0/10000" z pustym paskiem,
        # a przy nadmiarze SetPercentage dostaje wartosc > 1 i rozciaga
        # 211-pikselowy gauge poza panel (ui.py:1583 -> SetRenderingRect).
        if self.level >= MAX_LEVEL:
            pointsInLevel = POINTS_PER_LEVEL
        else:
            pointsInLevel = max(0, min(POINTS_PER_LEVEL,
                                       self.points - self.level * POINTS_PER_LEVEL))

        self.levelText.SetText(localeInfo.BATTLEPASS_LEVEL_FMT % self.level)
        self.pointsText.SetText(localeInfo.BATTLEPASS_POINTS_FMT % (pointsInLevel, POINTS_PER_LEVEL))
        self.levelGauge.SetPercentage(pointsInLevel, POINTS_PER_LEVEL)

        if endTime:
            self.__SetSeasonTooltip(localeInfo.BATTLEPASS_TIME_LEFT % FormatTimeLeft(endTime))

    def __SetSeasonTooltip(self, text):
        if not text or text == self.lastTimeText:
            return
        self.lastTimeText = text
        self.levelPanel.SetToolTipTextNew(text, 0, 62)

    # ---------------------------------------------------------- plansze

    def __SetBoard(self, boardIndex):
        self.boardIndex = boardIndex
        if boardIndex == BOARD_REWARDS:
            self.boardMissions.Hide()
            self.boardRewards.Show()
        else:
            self.boardRewards.Hide()
            self.boardMissions.Show()
        self.tabButton.SetUp()

    def __ToggleBoard(self):
        self.__OnOverOutReward()
        self.__SetBoard(BOARD_MISSIONS if self.boardIndex == BOARD_REWARDS else BOARD_REWARDS)

    # ---------------------------------------------------------- scroll

    def __OnScrollRewards(self, step):
        if step == self.rewardOffset:
            return
        self.rewardOffset = step
        self.__OnOverOutReward()
        self.__RefreshRewards()

    def __OnScrollMissions(self, step):
        if step == self.missionOffset:
            return
        self.missionOffset = step
        self.__RefreshMissions()

    # ---------------------------------------------------------- tooltipy

    def __OnOverInReward(self, vnum):
        if not self.tooltipItem or not vnum:
            return
        self.tooltipItem.ClearToolTip()
        self.tooltipItem.AddItemData(vnum, [0] * 6)
        self.tooltipItem.ShowToolTip()

    def __OnOverOutReward(self):
        if self.tooltipItem:
            self.tooltipItem.HideToolTip()

    # ---------------------------------------------------------- premium

    def __OpenBuyPremiumDialog(self):
        if self.isPremium:
            return
        if self.questionDialog:
            self.questionDialog.Open()

    def __OnAcceptBuyPremium(self):
        net.SendChatPacket("/battle_pass premium 1")
        if self.questionDialog:
            self.questionDialog.Close()

    def __OnCancelBuyPremium(self):
        if self.questionDialog:
            self.questionDialog.Close()

    # ---------------------------------------------------------- tick

    def OnUpdate(self):
        # Odliczanie sezonu i czasy misji zmieniaja sie raz na minute -
        # odswiezamy raz na sekunde zamiast co klatke.
        if not self.levelPanel:
            return

        now = app.GetGlobalTimeStamp()
        if now == self.lastTickStamp:
            return
        self.lastTickStamp = now

        self.__RefreshHeader()
        if self.boardIndex == BOARD_MISSIONS:
            for row in self.missionRows:
                row.RefreshProgress()
