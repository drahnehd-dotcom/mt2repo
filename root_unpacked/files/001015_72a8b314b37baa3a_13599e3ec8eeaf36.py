# -*- coding: utf-8 -*-
#
# Wyszukiwarka sklepow offline - wierne odwzorowanie okna z nostalgii
# (IkarusSearchShopBoard / IkarusSearchShopItem z uiikashop.py), podpiete
# pod NASZ backend offlineshop zamiast ich ikashop.
#
# Layout 1:1 wg oryginalu:
#   - pole nazwy (input_name.png) w (14,40), szerokosc 155
#   - przycisk szukania tuz obok, dalej reset
#   - skrzynka wynikow (result_box.png) w (227,40), wysokosc skalowana do 469
#   - 4 wiersze wynikow (result_item_box.png, 339x111) w (5, 4 + 116*i)
#   - scrollbar w (szerokosc - 19, 3)
# Lewa kolumna filtrow w oryginale jest poza ekranem (+99999) - nie odtwarzam
# jej wcale, bo taki jest zamierzony wyglad tej wersji.
#
# Przycisk na wierszu w oryginale nazywa sie "Kup", ale w tym buildzie NIE kupuje -
# lokalizuje sklep na mapie (efekt + waypoint). U nas przez offlineshop.LocateShopAt,
# ktore uzywa pozycji z wyniku wyszukiwarki (serwer) - dziala tez dla sklepow spoza
# zasiegu widoku, w przeciwienstwie do starego LocateShopByOwner (tylko m_vecShopInstance).
#
# Kod nostalgii nie zostal skopiowany doslownie - nie dziala na Pythonie 3
# (cp1250 w zrodle, xrange, long(), vars().values() + list) i ma wycieki
# callbackow. Odtworzony jest uklad i zachowanie, nie litery kodu.

import ui
import offlineshop
import item
import localeInfo
import chat
import snd
import grp
import background

RESULT_ITEM_VIEW_COUNT = 4
RESULT_ITEM_STEP = 116
SLOT_SIZE = 32

WINDOW_WIDTH = 604
WINDOW_HEIGHT = 519

IMG_INPUT_NAME = "offlineshop/search/input_name.png"
IMG_RESULT_BOX = "offlineshop/search/result_box.png"
IMG_RESULT_ITEM_BOX = "offlineshop/search/result_item_box.png"
IMG_SLOT_BASE = "offlineshop/search/slot/default.png"

BTN_SEARCH = ("offlineshop/search/mini_search_button/default.png",
			  "offlineshop/search/mini_search_button/hover.png")
BTN_RESET = ("offlineshop/search/reset_filter_button/default.png",
			 "offlineshop/search/reset_filter_button/hover.png")
BTN_LOCATE = ("offlineshop/search/buy_button/default.png",
			  "offlineshop/search/buy_button/hover.png")

INPUT_NAME_WIDTH = 155

# Kierunki 0..7 zgodnie z ruchem wskazowek od polnocy (tak liczy je C++).
# Skladane z osobnych kluczy, bo plik locale trzyma pojedyncze stringi, nie listy.
SHOPSEARCH_DIRECTIONS = (
	localeInfo.SHOPSEARCH_DIR_N, localeInfo.SHOPSEARCH_DIR_NE,
	localeInfo.SHOPSEARCH_DIR_E, localeInfo.SHOPSEARCH_DIR_SE,
	localeInfo.SHOPSEARCH_DIR_S, localeInfo.SHOPSEARCH_DIR_SW,
	localeInfo.SHOPSEARCH_DIR_W, localeInfo.SHOPSEARCH_DIR_NW,
)
FILTER_NAME_MAX_LEN = 24

# Wyszukiwarka dziala tylko w miastach (a1 = map index 1, c1 = 41). Serwer ma ten sam
# warunek (RecvShopFilterRequestClientPacket) - tu tylko po to, by pokazac komunikat.
SHOPSEARCH_ALLOWED_MAPS = ("metin2_map_a1", "metin2_map_c1")


class SearchResultItem(ui.Window):
	# Wiersz wyniku - odpowiednik IkarusSearchShopItem (339x111).

	def __init__(self, parent, board):
		ui.Window.__init__(self)
		self.SetParent(parent)

		self.data = None
		self.board = board

		self.background = ui.ExpandedImageBox()
		self.background.SetParent(self)
		self.background.LoadImage(IMG_RESULT_ITEM_BOX)
		self.background.SetPosition(0, 0)
		self.background.Show()

		self.SetSize(self.background.GetWidth(), self.background.GetHeight())

		self.slot = ui.GridSlotWindow()
		self.slot.SetParent(self)
		self.slot.SetPosition(9, 7)
		self.slot.ArrangeSlot(0, 1, 3, SLOT_SIZE, SLOT_SIZE, 0, 0)
		self.slot.SetSlotBaseImage(IMG_SLOT_BASE, 1.0, 1.0, 1.0, 1.0)
		self.slot.SetOverInItemEvent(ui.__mem_func__(self.__OverInItem))
		self.slot.SetOverOutItemEvent(ui.__mem_func__(self.__OverOutItem))
		self.slot.Show()

		self.itemName = ui.TextLine()
		self.itemName.SetParent(self)
		self.itemName.SetPosition(60, 11)
		self.itemName.Show()

		self.sellerName = ui.TextLine()
		self.sellerName.SetParent(self)
		self.sellerName.SetPosition(78, 35)
		self.sellerName.Show()

		self.price = ui.TextLine()
		self.price.SetParent(self)
		self.price.SetPosition(78, 58)
		self.price.Show()

		self.locateButton = ui.Button()
		self.locateButton.SetParent(self)
		self.locateButton.SetPosition(261, 84)
		self.locateButton.SetUpVisual(BTN_LOCATE[0])
		self.locateButton.SetDownVisual(BTN_LOCATE[0])
		self.locateButton.SetOverVisual(BTN_LOCATE[1])
		self.locateButton.SetText(localeInfo.SHOPSEARCH_LOCATE)
		self.locateButton.SetEvent(ui.__mem_func__(self.__OnClickLocate))
		self.locateButton.Show()

		self.Hide()

	def __del__(self):
		ui.Window.__del__(self)

	def Destroy(self):
		self.data = None
		self.board = None
		self.background = None
		self.slot = None
		self.itemName = None
		self.sellerName = None
		self.price = None
		self.locateButton = None

	def SetData(self, data):
		self.data = data

		vnum = data.get("vnum", 0)
		count = data.get("count", 1)

		item.SelectItem(vnum)

		self.slot.SetItemSlot(0, vnum, count)
		self.slot.RefreshSlot()

		self.itemName.SetText(item.GetItemName())
		self.sellerName.SetText(data.get("owner_name", ""))

		try:
			self.price.SetText(localeInfo.NumberToMoneyString(data.get("price", 0)))
		except Exception:
			self.price.SetText(str(data.get("price", 0)))

		self.Show()

	def Clear(self):
		self.data = None
		if self.slot:
			self.slot.ClearSlot(0)
			self.slot.RefreshSlot()
		self.Hide()

	def __OnClickLocate(self):
		# Przycisk "Kup" w oryginale - u nas lokalizuje sklep na mapie (strzalka + waypoint).
		# Pozycja (x/y) i flaga onmap przychodza z wyniku wyszukiwarki (serwer), wiec dziala
		# tez dla sklepow SPOZA zasiegu widoku - nie tylko tych aktualnie wyrenderowanych.
		if not self.data:
			return

		sellerName = self.data.get("owner_name", "")
		if not sellerName:
			return

		snd.PlaySound("sound/ui/click.wav")

		onMap = self.data.get("onmap", 0)
		shopX = self.data.get("x", 0)
		shopY = self.data.get("y", 0)

		# Zwraca (znaleziony, dystans_w_metrach, kierunek_0_7). onMap=0 -> serwer wyliczyl,
		# ze sklep jest na innej mapie -> found bedzie 0.
		(found, distance, direction) = offlineshop.LocateShopAt(onMap, shopX, shopY, sellerName)

		if not found:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.SHOPSEARCH_NOT_ON_MAP)
			return

		dirName = SHOPSEARCH_DIRECTIONS[direction % 8]
		chat.AppendChat(chat.CHAT_TYPE_INFO,
			localeInfo.SHOPSEARCH_LOCATED % (sellerName, distance, dirName))

	def __OverInItem(self, slotIndex):
		if not self.data or not self.board or not self.board.tooltip:
			return

		# AddItemData(vnum, metinSlot, attrSlot) - kolejnosc wg uitooltip.py
		self.board.tooltip.ClearToolTip()
		self.board.tooltip.AddItemData(
			self.data.get("vnum", 0),
			self.data.get("sockets", []),
			self.data.get("attrs", []))
		self.board.tooltip.Show()

	def __OverOutItem(self):
		if self.board and self.board.tooltip:
			self.board.tooltip.Hide()


class ShopSearchSimple(ui.BoardWithTitleBar):

	def __init__(self):
		ui.BoardWithTitleBar.__init__(self)

		self.resultItems = []
		self.items = []
		self.scrollPos = 0
		self.tooltip = None
		self.interface = None
		self.isLoading = False
		self.suggestion = ""

		self.__LoadWindow()

	def __del__(self):
		ui.BoardWithTitleBar.__del__(self)

	def __LoadWindow(self):
		self.SetSize(WINDOW_WIDTH, WINDOW_HEIGHT)
		# Bez tego okna nie da sie przesuwac ani wyciagnac na wierzch.
		self.AddFlag("movable")
		self.AddFlag("float")
		self.SetTitleName(localeInfo.SHOPSEARCH_TITLE)
		self.SetCloseEvent(ui.__mem_func__(self.Close))

		# --- pole nazwy + przyciski (lewa gora) ---
		self.inputNameBox = ui.ExpandedImageBox()
		self.inputNameBox.SetParent(self)
		self.inputNameBox.LoadImage(IMG_INPUT_NAME)
		self.inputNameBox.SetPosition(14, 40)
		imgW = self.inputNameBox.GetWidth()
		if imgW > 0:
			self.inputNameBox.SetScale(float(INPUT_NAME_WIDTH) / imgW, 1.0)
		self.inputNameBox.Show()

		boxH = self.inputNameBox.GetHeight()

		self.searchButton = ui.Button()
		self.searchButton.SetParent(self)
		self.searchButton.SetPosition(14 + INPUT_NAME_WIDTH + 2, 42)
		self.searchButton.SetUpVisual(BTN_SEARCH[0])
		self.searchButton.SetDownVisual(BTN_SEARCH[0])
		self.searchButton.SetOverVisual(BTN_SEARCH[1])
		self.searchButton.SetEvent(ui.__mem_func__(self.OnSearch))
		self.searchButton.SetToolTipText(localeInfo.SHOPSEARCH_SEARCH)
		self.searchButton.Show()

		self.resetButton = ui.Button()
		self.resetButton.SetParent(self)
		self.resetButton.SetPosition(14 + INPUT_NAME_WIDTH + 2 + self.searchButton.GetWidth() + 3, 42)
		self.resetButton.SetUpVisual(BTN_RESET[0])
		self.resetButton.SetDownVisual(BTN_RESET[0])
		self.resetButton.SetOverVisual(BTN_RESET[1])
		self.resetButton.SetEvent(ui.__mem_func__(self.OnReset))
		self.resetButton.SetToolTipText(localeInfo.SHOPSEARCH_RESET)
		self.resetButton.Show()

		editW = INPUT_NAME_WIDTH - self.searchButton.GetWidth() - 6
		editH = max(1, boxH - 6)

		# Ghost-text jak w uishopsearch.Search_RefreshTextHint: pokazuje wpisany
		# tekst + reszte dopasowanej nazwy. Tworzony PRZED nameEdit, zeby pole
		# edycji rysowalo sie na wierzchu.

		self.nameEdit = ui.EditLine()
		self.nameEdit.SetParent(self.inputNameBox)
		self.nameEdit.SetPosition(6, 6)
		self.nameEdit.SetSize(max(1, editW), editH)
		self.nameEdit.SetMax(FILTER_NAME_MAX_LEN)
		self.nameEdit.SetReturnEvent(ui.__mem_func__(self.OnSearch))
		self.nameEdit.SetEscapeEvent(ui.__mem_func__(self.nameEdit.KillFocus))
		self.nameEdit.SetUpdateEvent(ui.__mem_func__(self.__OnUpdateName))
		self.nameEdit.SetTabEvent(ui.__mem_func__(self.__OnTabName))
		self.nameEdit.Show()

		self.searchEditHint = ui.TextLine()
		self.searchEditHint.SetParent(self.nameEdit)
		self.searchEditHint.SetPackedFontColor(grp.GenerateColor(1.0, 1.0, 1.0, 0.5))
		self.searchEditHint.Show()

		self.inputNameBox.SetOnMouseLeftButtonUpEvent(ui.__mem_func__(self.nameEdit.SetFocus))


		# --- skrzynka wynikow (prawa strona) ---
		self.resultBox = ui.ExpandedImageBox()
		self.resultBox.SetParent(self)
		self.resultBox.LoadImage(IMG_RESULT_BOX)
		self.resultBox.SetPosition(227, 40)
		boxW = self.resultBox.GetWidth()
		boxHeight = self.resultBox.GetHeight()
		if boxW > 0 and boxHeight > 0:
			self.resultBox.SetScale(float(boxW - 10) / boxW, 469.0 / boxHeight)
		self.resultBox.Show()

		self.resultItems = []
		for i in range(RESULT_ITEM_VIEW_COUNT):
			row = SearchResultItem(self.resultBox, self)
			row.SetPosition(5, 4 + RESULT_ITEM_STEP * i)
			self.resultItems.append(row)

		self.scrollBar = ui.ScrollBar()
		self.scrollBar.SetParent(self.resultBox)
		self.scrollBar.SetPosition(boxW - 19, 3)
		self.scrollBar.SetScrollBarSize(max(1, boxHeight - 6))
		self.scrollBar.SetScrollEvent(ui.__mem_func__(self.__OnScroll))
		self.scrollBar.Hide()

		self.emptyLine = ui.TextLine()
		self.emptyLine.SetParent(self.resultBox)
		self.emptyLine.SetPosition(boxW // 2, 220)
		self.emptyLine.SetHorizontalAlignCenter()
		self.emptyLine.SetText(localeInfo.SHOPSEARCH_NO_RESULT)
		self.emptyLine.Hide()

		# Druga linia komunikatu "zla mapa" (lista map) - jedna linia nie miesci sie w skrzynce.
		self.emptyLine2 = ui.TextLine()
		self.emptyLine2.SetParent(self.resultBox)
		self.emptyLine2.SetPosition(boxW // 2, 238)
		self.emptyLine2.SetHorizontalAlignCenter()
		self.emptyLine2.Hide()

		self.SetCenterPosition()

		# Rejestracja juz TUTAJ, nie tylko w Show(). uishopsearch.ShopSearch robi
		# to samo w swoim __init__ (linia 982) i jest tworzona wczesniej przez
		# uiofflineshop.py - inaczej przejmuje plansze wynikow i nasze handlery
		# nigdy nie dostaja odpowiedzi z serwera.
		offlineshop.SetShopSearchBoard(self)

	def Destroy(self):
		offlineshop.SetShopSearchBoard(None)	# C++ trzyma surowy wskaznik tego okna - wyrejestruj przed zniszczeniem

		for row in self.resultItems:
			row.Destroy()

		self.resultItems = []
		self.items = []

		# Tooltip jest wspoldzielony z interfejsem - tylko zwalniamy referencje.
		if self.tooltip:
			self.tooltip.Hide()
		self.tooltip = None
		self.interface = None

		self.inputNameBox = None
		self.nameEdit = None
		self.searchButton = None
		self.resetButton = None
		self.resultBox = None
		self.scrollBar = None
		self.emptyLine = None
		self.emptyLine2 = None
		self.searchEditHint = None
		# Bez ClearDictionary() - to metoda ScriptWindow, a to okno jest budowane
		# kodem (BoardWithTitleBar), wiec nie ma slownika elementow.

	# --- kontrakt interfacemodule ---------------------------------------

	def SetItemToolTip(self, tooltip):
		self.tooltip = tooltip

	def BindInterface(self, interface):
		self.interface = interface

	# uiofflineshop.BindInterface wola SetInterface - stara ShopSearch tak to nazywala.
	def SetInterface(self, interface):
		self.interface = interface

	# --- lifecycle -------------------------------------------------------

	def Show(self, bFastSearch = False):
		# Rejestracja MUSI byc tutaj - game.py OpenShopSearch (F9) wola Show(),
		# nie Open(). W oryginale Open() w ogole nie wolalo Show() i przy braku
		# odpowiedzi serwera okno nigdy sie nie otwieralo.
		offlineshop.SetShopSearchBoard(self)
		ui.BoardWithTitleBar.Show(self)

		# Po otwarciu od razu pokazujemy oferty - tak jak nasza uishopsearch, ktora
		# w Show() wola OnSearch() z pustym filtrem (serwer zwraca wtedy wszystko
		# do limitu OFFLINESHOP_MAX_SEARCH_RESULT). Nostalgia robi to inaczej -
		# osobnym pakietem random-fill, ktorego nasz serwer nie ma.
		self.OnSearch()

	def Open(self):
		self.SetCenterPosition()
		self.SetTop()
		self.Show()

	def Close(self, IsFromGame = False):
		offlineshop.SetShopSearchBoard(None)
		offlineshop.ClearShopLocator()

		# Zabezpieczenie: gdy serwer nie odpowie (limit 3s miedzy wyszukiwaniami),
		# isLoading zostaloby na True i przycisk "Szukaj" przestalby dzialac.
		self.isLoading = False

		if self.tooltip:
			self.tooltip.Hide()

		self.Hide()
		return True

	def OnPressEscapeKey(self):
		self.Close()
		return True

	# --- akcje -----------------------------------------------------------

	def OnSearch(self):
		if self.isLoading:
			return True

		if background.GetCurrentMapName() not in SHOPSEARCH_ALLOWED_MAPS:
			self.__ShowWrongMap()
			return True

		self.isLoading = True
		self.__ClearRows()

		# Wartosci neutralne potwierdzone w kodzie SERWERA (new_offlineshop_manager.cpp):
		#   bType    -> porownywany z ITEM::NONE, czyli 0 = brak filtra (linia 2581)
		#   bSubType -> porownywany z SUBTYPE_NOSET = 255 (linia 2584)
		#   dwWearFlag -> MatchWearFlag zwraca true gdy 0 (linia 198), wiec 0 = brak filtra.
		#                 NIE wysylac tu sumy antyflag - to aktywnie odsiewa itemy.
		offlineshop.SendFilterRequest(
			0,						# type - 0 = wszystkie
			255,					# subtype - 255 = wszystkie
			self.nameEdit.GetText(),
			(0, 0),					# cena min/max
			(0, 0),					# poziom min/max
			0,						# wearFlag - 0 = bez filtra klasowego
			False,					# szukanie po nazwie gracza
			(0, 0),					# ilosc min/max
			(0, 0),					# absorpcja min/max
			0,						# min. srednia
			0,						# alchemyGrade
			0,						# alchemyPurity
			0,						# sashLevel
		)
		return True

	def __ShowWrongMap(self):
		self.__ClearRows()
		self.items = []
		self.scrollPos = 0
		self.scrollBar.Hide()
		self.emptyLine.SetText(localeInfo.SHOPSEARCH_WRONG_MAP)
		self.emptyLine.Show()
		self.emptyLine2.SetText(localeInfo.SHOPSEARCH_WRONG_MAP_LIST % (localeInfo.MAP_A1, localeInfo.MAP_C1))
		self.emptyLine2.Show()

	def __HideEmptyInfo(self):
		self.emptyLine.Hide()
		self.emptyLine2.Hide()

	def __OnUpdateName(self):
		# 1:1 wg uishopsearch.Search_RefreshTextHint: hint pokazuje wpisany tekst
		# + reszte nazwy, a przy braku dopasowania pole robi sie czerwone.
		EDIT_TEXT_BASE_COLOR = grp.GenerateColor(0.8549, 0.8549, 0.8549, 1.0)
		EDIT_TEXT_NOT_FOUND_COLOR = grp.GenerateColor(1.0, 0.2, 0.2, 1.0)

		self.suggestion = ""
		self.searchEditHint.SetText("")
		self.nameEdit.SetPackedFontColor(EDIT_TEXT_BASE_COLOR)

		searchText = self.nameEdit.GetText()
		if not searchText:
			return

		try:
			(hintName, vnum) = item.GetItemDataByNamePart(searchText)
		except AttributeError:
			(hintName, vnum) = ("", -1)

		if vnum == -1:
			self.nameEdit.SetPackedFontColor(EDIT_TEXT_NOT_FOUND_COLOR)
		else:
			self.suggestion = hintName
			self.searchEditHint.SetText(searchText + " " + hintName[len(searchText):])

	def __OnTabName(self):
		# 1:1 wg uishopsearch: hint ma format "wpisane + spacja + reszta",
		# stad przesuniecie o len(oldText)+1.
		if not self.searchEditHint.GetText():
			return True

		oldText = self.nameEdit.GetText()
		self.nameEdit.SetText(oldText + self.searchEditHint.GetText()[len(oldText) + 1:])
		self.searchEditHint.SetText("")
		self.suggestion = ""
		return True

	def OnReset(self):
		# W oryginale reset nie czyscil pol (zakomentowane) - u nas czysci.
		self.nameEdit.SetText("")
		self.searchEditHint.SetText("")
		self.suggestion = ""
		self.__ClearRows()
		self.items = []
		self.scrollPos = 0
		self.scrollBar.Hide()
		self.__HideEmptyInfo()
		offlineshop.ClearShopLocator()
		return True

	def __OnScroll(self):
		if not self.items:
			return

		maxScroll = max(0, len(self.items) - RESULT_ITEM_VIEW_COUNT)
		self.scrollPos = int(self.scrollBar.GetPos() * maxScroll)
		self.__RefreshRows()

	def OnMouseWheel(self, delta):
		if len(self.items) <= RESULT_ITEM_VIEW_COUNT:
			return True

		if delta > 0:
			self.scrollPos = max(0, self.scrollPos - 1)
		else:
			self.scrollPos = min(len(self.items) - RESULT_ITEM_VIEW_COUNT, self.scrollPos + 1)

		self.__RefreshRows()
		return True

	# --- odbior wynikow z serwera ---------------------------------------
	# Kontrakt C++ (PythonOfflineshop.cpp):
	#   ShopFilterResult(n) -> ShopFilterResultItem_Alloc()
	#   -> ShopFilterResultItem_SetValue(klucz, i, ...) -> ShopFilterResult_Show()

	def ShopFilterResult(self, count):
		self.items = []

	def ShopFilterResultItem_Alloc(self):
		self.items.append({"attrs": [], "sockets": []})

	def ShopFilterResultItem_SetValue(self, key, index, *args):
		if index < 0 or index >= len(self.items):
			return

		data = self.items[index]

		if key == "attr":
			if len(args) >= 3:
				data["attrs"].append((args[1], args[2]))
		elif key == "socket":
			if len(args) >= 2:
				data["sockets"].append(args[1])
		elif args:
			data[key] = args[0]

	def ShopFilterResult_Show(self):
		self.isLoading = False
		self.scrollPos = 0

		self.emptyLine2.Hide()

		if not self.items:
			self.__ClearRows()
			self.scrollBar.Hide()
			self.emptyLine.SetText(localeInfo.SHOPSEARCH_NO_RESULT)
			self.emptyLine.Show()
			return

		self.emptyLine.Hide()

		if len(self.items) > RESULT_ITEM_VIEW_COUNT:
			self.scrollBar.SetPos(0)
			self.scrollBar.Show()
		else:
			self.scrollBar.Hide()

		self.__RefreshRows()

	def SearchFilter_BuyFromSearch(self, ownerID, itemID):
		# Ta wersja okna nie kupuje - zostawione dla zgodnosci z kontraktem C++.
		pass

	# --- render ----------------------------------------------------------

	def __ClearRows(self):
		for row in self.resultItems:
			row.Clear()

	def __RefreshRows(self):
		for i, row in enumerate(self.resultItems):
			dataIndex = self.scrollPos + i
			if dataIndex < len(self.items):
				row.SetData(self.items[dataIndex])
			else:
				row.Clear()
