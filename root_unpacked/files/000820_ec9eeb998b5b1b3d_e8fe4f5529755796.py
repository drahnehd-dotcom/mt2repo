import app
import ui
import uiScriptLocale
import wndMgr

LOCALE_PATH = uiScriptLocale.MAPNAME_PATH

BASE_PATH = "kowal/mapname/maps/"

class MapNameShower(ui.Window):

	MAP_NAME_IMAGE =	{}

	STATE_HIDE = 0
	STATE_FADE_IN = 1
	STATE_SHOW = 2
	STATE_FADE_OUT = 3

	def __init__(self):
		self.MAP_NAME_IMAGE =	{
						"metin2_map_a1"							: BASE_PATH+"shinsoo_m1.png",
						"metin2_map_a3"							: BASE_PATH+"shinsoo_m2.png",
						"metin2_map_b1"							: BASE_PATH+"chunjo_m1.png",
						"metin2_map_b3"							: BASE_PATH+"chunjo_m2.png",
						"metin2_map_c1"							: BASE_PATH+"jinno_m1.png",
						"metin2_map_c3"							: BASE_PATH+"jinno_m2.png",
						"metin2_zakatki"								: BASE_PATH+"tajemna_zakouti.png",
						"metin2_map_threeway"							: BASE_PATH+"udoli_orku.png",
						"metin2_map_exp"							: BASE_PATH+"udoli_kyklopu.png",
						"metin2_map_pustynia"						: BASE_PATH+"poust_faraona.png",
						"metin2_map_snow"							: BASE_PATH+"mraziva_krajina.png",
						"natural_map"							: BASE_PATH+"zacarovany_les.png",
						"plechito_lava_map_01"							: BASE_PATH+"ohniva_zeme.png",
						"metin2_map_sohan"							: BASE_PATH+"hora_sohan.png",
						"metin2_map_las"						: BASE_PATH+"les_duchu.png",
						"metin2_map_anglar_dungeon_01"						: BASE_PATH+"jeskyne_pavouku.png",
						"zaris_summer_map"						: BASE_PATH+"laguna.png",
						"zaris_map_swamp"						: BASE_PATH+"baziny.png",
						"alune_map24_exp_dark"						: BASE_PATH+"zaklete_udoli.png",
					}

		ui.Window.__init__(self, "TOP_MOST")

		self.SetSize(358, 121)
		self.AddFlag("not_pick")

		self.STEP = 0

		# animacja chodzi w stalym rytmie 60 Hz niezaleznie od FPS (patrz OnUpdate)
		self.__lastAnimTime = 0.0
		self.__animAccumulator = 0.0

		self.__Initialize()

	def __del__(self):
		ui.Window.__del__(self)

	def __Initialize(self):
		self.floorImage = None
		self.SetWindowHorizontalAlignCenter()
		self.SetPosition(0, wndMgr.GetScreenHeight()*0.15)
		self.Hide()

	def __ResetWindow(self, mapname):
		self.STEP = 1
		self.cooldown = 50
		self.finishAlpha = 1.0

		self.line_x_pos = 0

		self.brush_01 = ui.ExpandedImageBox()
		self.brush_01.SetParent(self)
		self.brush_01.LoadImage("kowal/mapname/brush_01.tga")
		self.brush_01.SetAlpha(0.0)
		self.brush_01.Show()

		self.brush_02 = ui.ExpandedImageBox()
		self.brush_02.SetParent(self)
		self.brush_02.LoadImage("kowal/mapname/brush_02.tga")
		self.brush_02.SetWindowHorizontalAlignCenter()
		self.brush_02.Show()

		self.brush_03 = ui.ExpandedImageBox()
		self.brush_03.SetParent(self)
		self.brush_03.LoadImage("kowal/mapname/brush_03.tga")
		self.brush_03.SetPosition(0, -15)
		self.brush_03.SetWindowHorizontalAlignCenter()
		self.brush_03.SetAlpha(0.0)
		self.brush_03.Show()

		self.map_name = ui.ExpandedImageBox()
		self.map_name.SetParent(self)
		self.map_name.LoadImage(mapname)
		self.map_name.SetPosition(0, -15)
		self.map_name.SetScale(1.2, 1.2)
		self.map_name.SetAlpha(0.0)
		self.map_name.Show()

		self.line_top = ui.ExpandedImageBox()
		self.line_top.SetParent(self)
		self.line_top.LoadImage("kowal/mapname/dash_center.tga")
		self.line_top.SetPosition(0, 10)
		self.line_top.SetWindowHorizontalAlignCenter()
		self.line_top.SetAlpha(0.0)
		self.line_top.Show()

		self.line_bottom = ui.ExpandedImageBox()
		self.line_bottom.SetParent(self)
		self.line_bottom.LoadImage("kowal/mapname/dash_center.tga")
		self.line_bottom.SetPosition(0, 85)
		self.line_bottom.SetWindowHorizontalAlignCenter()
		self.line_bottom.SetAlpha(0.0)
		self.line_bottom.Show()

		self.line_right = ui.ExpandedImageBox()
		self.line_right.SetParent(self)
		self.line_right.LoadImage("kowal/mapname/dash_right.tga")
		self.line_right.SetPosition(0, 7)
		self.line_right.SetWindowHorizontalAlignRight()
		self.line_right.SetAlpha(0.0)
		self.line_right.Show()

		self.line_left = ui.ExpandedImageBox()
		self.line_left.SetParent(self)
		self.line_left.LoadImage("kowal/mapname/dash_left.tga")
		self.line_left.SetPosition(-358, 88)
		self.line_left.SetAlpha(0.0)
		self.line_left.Show()

	def __GetDevilTowerFloor(self, x, y):
		if x > 10000 and y > 58000 and x < 25000 and y < 72000:
			return 1
		elif x > 10000 and y > 35000 and x < 25000 and y < 50000:
			return 2
		elif x > 10000 and y > 10000 and x < 25000 and y < 25000:
			return 3
		elif x > 35000 and y > 61000 and x < 43500 and y < 70500:
			return 4
		elif x > 35000 and y > 38000 and x < 43500 and y < 48000:
			return 5
		elif x > 14000 and y > 14000 and x < 43500 and y < 24500:
			return 6
		elif x > 56000 and y > 60000 and x < 68000 and y < 73000:
			return 7
		elif x > 56000 and y > 38000 and x < 68000 and y < 49000:
			return 8
		elif x > 56000 and y > 13000 and x < 68000 and y < 23000:
			return 9	 
		return 0

	def __GetDevilBase(self, x, y):
		if x > 3000 and y > 4500 and x < 45000 and y < 45000:
			return 1
		elif x > 54000 and y > 3900 and x < 100000 and y < 46200:
			return 2
		elif x > 104800 and y > 3500 and x < 145500 and y < 45800:
			return 3
		elif x > 3100 and y > 54100 and x < 56400 and y < 105800:
			return 4
		elif x > 65000 and y > 54000 and x < 105000 and y < 95500:
			return 5
		elif x > 117500 and y > 57600 and x < 142000 and y < 81000:
			return 6
		elif x > 5000 and y > 104900 and x < 15000 and y < 122000:
			return 7
		return	0

	def ShowMapName(self, mapName, x, y):
		if mapName not in self.MAP_NAME_IMAGE:
			print(" [ERROR] - There is no map name image", mapName
)
			return

		try:
			self.__ResetWindow(self.MAP_NAME_IMAGE[mapName])
		except RuntimeError:
			return

		self.__Initialize()

		if mapName == "metin2_map_deviltower1":
			self.SetPosition(-60, 80)

			self.floorImage = ui.ExpandedImageBox()
			self.floorImage.AddFlag("not_pick")
			self.floorImage.SetWindowHorizontalAlignCenter()
			self.floorImage.SetPosition(0, 93)
			self.floorImage.SetAlpha(0.0)
			self.floorImage.Show()

			try:
				floor = self.__GetDevilTowerFloor(x, y)
				print(x, y, floor
)
				self.floorImage.LoadImage(LOCALE_PATH+"devil1_%df.tga" % floor)
			except RuntimeError:
				self.SetPosition(0, 93)
				self.floorImage.Hide()
				self.floorImage = None

		if mapName == "metin2_map_devilsCatacomb":
			self.SetPosition(-75, 80)

			self.floorImage = ui.ExpandedImageBox()
			self.floorImage.AddFlag("not_pick")
			self.floorImage.SetWindowHorizontalAlignCenter()
			self.floorImage.SetPosition(0, 93)
			self.floorImage.SetAlpha(0.0)
			self.floorImage.Show()

			try:
				floor = self.__GetDevilBase(x, y)
				print(x, y, floor
)
				self.floorImage.LoadImage(LOCALE_PATH+"devil1_%df.tga" % floor)
			except RuntimeError:
				self.SetPosition(0, 93)
				self.floorImage.Hide()
				self.floorImage = None

		self.Show()

	def LinesAnimation(self):
		if self.STEP >= 2:
			if self.line_left.GetAlpha() < 1.0 and self.line_x_pos < 250:
				self.line_left.SetAlpha(self.line_left.GetAlpha()+0.04)
				self.line_right.SetAlpha(self.line_right.GetAlpha()+0.04)

			if self.line_x_pos > 330:
				self.line_left.SetAlpha(self.line_left.GetAlpha()-0.02)
				self.line_right.SetAlpha(self.line_right.GetAlpha()-0.02)

			if self.line_x_pos < 250 or self.line_x_pos > 350:
				self.line_x_pos += 15
			else:
				self.line_x_pos += 2

			self.line_left.SetPosition(-358+self.line_x_pos, 88)
			self.line_right.SetPosition(self.line_x_pos, 7)

	def OnUpdate(self):
		# Cala ta animacja (alfa +0.025, skala -0.01, cooldown -1 ...) liczy stalymi krokami
		# NA KLATKE, wiec po odblokowaniu limitu FPS przy 144 Hz leciala 2.4x szybciej.
		# Zamiast przerabiac kazdy krok z osobna, odpalamy ja w stalym rytmie 60 Hz -
		# wyglada dokladnie tak samo jak dawniej, przy dowolnym FPS.
		scale, self.__lastAnimTime = ui.GetFrameStepScale(self.__lastAnimTime)
		self.__animAccumulator += scale

		steps = int(self.__animAccumulator)
		if steps <= 0:
			return

		self.__animAccumulator -= steps

		for _ in range(steps):
			self.__AnimationStep()

	def __AnimationStep(self):
		self.LinesAnimation()

		if self.STEP > 0 and self.STEP < 3:

			alpha_brush_01 = self.brush_01.GetAlpha()
			if alpha_brush_01 < 1.0:
				alpha_brush_01 += 0.025
				self.brush_01.SetAlpha(alpha_brush_01)

			if alpha_brush_01 >= 0.5:
				if self.brush_02.GetAlpha() < 1.0:
					self.brush_02.SetAlpha(self.brush_02.GetAlpha()+0.05)

				if self.brush_03.GetAlpha() < 1.0:
					self.brush_03.SetAlpha(self.brush_03.GetAlpha()+0.05)

				else:
					self.STEP = 2

			if self.STEP == 2:
				xScale, yScale = self.map_name.GetScale()
				if xScale > 1.0:
					xScale -= 0.01
					self.map_name.SetScale(xScale, xScale)
					self.map_name.SetAlpha(self.map_name.GetAlpha()+0.05)
					self.map_name.SetWindowHorizontalAlignCenter()
					self.map_name.SetWindowVerticalAlignCenter()

					if self.floorImage:
						self.floorImage.SetAlpha(self.floorImage.GetAlpha()+0.05)

					self.line_top.SetAlpha(self.line_top.GetAlpha()+0.05)
					self.line_bottom.SetAlpha(self.line_bottom.GetAlpha()+0.05)

				else:
					self.STEP = 3

		if self.STEP == 3:
			if self.cooldown > 0:
				self.cooldown -= 1
			else:
				self.STEP = 4

		if self.STEP == 4:
			if self.finishAlpha > 0.0:
				self.finishAlpha -= 0.05
				self.brush_01.SetAlpha(self.finishAlpha)
				self.brush_02.SetAlpha(self.finishAlpha)
				self.brush_03.SetAlpha(self.finishAlpha)
				self.map_name.SetAlpha(self.finishAlpha)

				if self.floorImage:
					self.floorImage.SetAlpha(self.finishAlpha)

				self.line_top.SetAlpha(self.finishAlpha)
				self.line_bottom.SetAlpha(self.finishAlpha)
			else:
				self.STEP = 0
				self.Hide()

