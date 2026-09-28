import ui
import constInfo
import wndMgr
import player
import chr
import item
import net
import localeInfo

class CardsLottery(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.rotate = 0
		self.rect = 1.0
		self.direction = 0
		self.cards = {}
		self.items = []
		self.items_count = 0
		self.LoadDialog()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def LoadDialog(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "uiscript/cardslottery.py")
		except:
			import exception
			exception.Abort("CardsLottery.LoadDialog.LoadObject")

		try:
			GetObject = self.GetChild
			self.board = GetObject("board")
			self.CloseButton = GetObject("CloseButton")
		except:
			import exception
			exception.Abort("CardsLottery.LoadDialog.BindObject")

		self.CloseButton.SetEvent(self.Close)

		self.titleText = ui.TextLine()
		self.titleText.SetParent(self.board)
		self.titleText.SetPosition(0, 55)
		self.titleText.SetText(localeInfo.CARDS_LOTTERY_CHOOSE)
		self.titleText.SetFontName("Verdana:18")
		self.titleText.SetPackedFontColor(0xFFFFD700)
		self.titleText.SetOutline()
		self.titleText.SetHorizontalAlignCenter()
		self.titleText.SetWindowHorizontalAlignCenter()
		self.titleText.Show()

		for i in range(4):
			c = Card(self, i, self)
			c.SetParent(self)
			c.SetPosition(-55 + (i * 150), 150)
			self.cards[i] = c

	def Reward(self, id):
		id = int(id)
		index  = 0
		for i in range(4):
			if self.cards[i].rotate == 1 or self.cards[i].direction == 1:
				index = i
				break

		item.SelectItem(id)
		itemIcon = item.GetIconImageFileName()
		(width, height) = item.GetItemSize()
  
		self.cards[index].itemImage.LoadImage(itemIcon)
		if height == 3:
			self.cards[index].itemImage.SetPosition(53, 20)
		else:
			self.cards[index].itemImage.SetPosition(53, 60 - ((height * 32) // 2))
		self.cards[index].itemImage.SetScale(0, 1)
		self.cards[index].itemImage.Show()

	def Open(self):
		self.Show()

	def Destroy(self):
		self.ClearDictionary()
		self.rotate = 0
		self.rect = 1.0
		self.direction = 0
		self.cards = {}
		self.items = []
		self.items_count = 0

	def Close(self):
		self.Hide()

class Card(ui.Window):
	def __init__(self, lottery, index, background):
		ui.Window.__init__(self)
		self.lottery = lottery
		self.index = index
		self.rotate = 0
		self.rect = 1.0
		self.direction = 0
		# animacja obrotu chodzi w stalym rytmie 60 Hz niezaleznie od FPS (patrz OnUpdate)
		self.__lastAnimTime = 0.0
		self.__animAccumulator = 0.0
		self.background = background
		self.LoadDialog(background)

	def __del__(self):
		ui.Window.__del__(self)

	def LoadDialog(self, background):
		self.SetSize(203, 157)
		self.front_card = ui.ExpandedImageBox()
		self.front_card.SetParent(self)
		self.front_card.LoadImage("kowal/dungeon_cards/card_open.png")
		self.front_card.SetPosition(50, 0)
		self.front_card.Show()
		self.front_card.SetScale(0, 1)

		item.SelectItem(109)
		itemIcon = item.GetIconImageFileName()
		(width, height) = item.GetItemSize()

		self.itemImage = ui.ExpandedImageBox()
		self.itemImage.SetParent(self.front_card)

		self.back_card = ui.ExpandedImageBox()
		self.back_card.SetParent(self)
		self.back_card.LoadImage("kowal/dungeon_cards/card_back.png")
		self.back_card.SetPosition(0, 0)
		self.back_card.SetEvent(ui.__mem_func__(self.OpenCard), "mouse_click")
		self.back_card.SetTop()
		self.back_card.Show()

		self.Show()

	def OpenCard(self):
		for i in range(0, 4):
			if self.lottery.cards[i].direction == 1 or self.lottery.cards[i].rotate == 1:
				return

		net.SendChatPacket("/dungeon_cards %i", self.index)
		self.rotate = 1

	def OnUpdate(self):
		# Obrot karty liczyl staly krok NA KLATKE (rect +/- 0.06), wiec po odblokowaniu
		# limitu FPS przy 144 Hz karta obracalaby sie 2.4x szybciej. Odpalamy animacje
		# w stalym rytmie 60 Hz - wyglada tak jak dawniej, przy dowolnym FPS.
		scale, self.__lastAnimTime = ui.GetFrameStepScale(self.__lastAnimTime)
		self.__animAccumulator += scale

		steps = int(self.__animAccumulator)
		if steps <= 0:
			return

		self.__animAccumulator -= steps

		for _ in range(steps):
			self.__AnimationStep()

	def __AnimationStep(self):
		if self.rotate == 1:
			if self.direction == 0:
				self.rect = self.rect - 0.06
				if self.rect > 0.0:
					self.back_card.SetScale(self.rect, 1)
					x, y = self.back_card.GetLocalPosition()
					self.back_card.SetPosition(x + 3, 0)
				else:
					self.direction = 1
			else:
				self.back_card.Hide()
				if self.rect < 1.00:
					self.rect = self.rect + 0.06
					self.front_card.SetScale(self.rect, 1)
					self.itemImage.SetScale(self.rect, 1)
					x, y = self.front_card.GetLocalPosition()
					self.front_card.SetPosition(x - 3, 0)
					ix, iy = self.itemImage.GetLocalPosition()
					self.itemImage.SetPosition(ix + 2, iy + 1)
				else:
					self.rotate = 0
