import uiScriptLocale
import item

# Tlo kowal/artefakty.png ma 320x320 i cztery ramki w ukladzie rombu.
# Pozycje slotow = srodki wnetrz ramek minus 16 (polowa ikony 32x32).
BASE_SIZE = 320

BOARD_WIDTH = BASE_SIZE + 32
BOARD_HEIGHT = BASE_SIZE + 43

window = {
	"name" : "ArtifactSystemWindow",

	"x" : 0,
	"y" : 0,

	"style" : ("movable", "float",),

	"width" : BOARD_WIDTH,
	"height" : BOARD_HEIGHT,

	"children" :
	(
		{
			"name" : "Board",
			"type" : "board",
			"style" : ("movable","float",),

			"x" : 0,
			"y" : 0,

			"width" : BOARD_WIDTH,
			"height" : BOARD_HEIGHT,

			"children" :
			(
				{
					"name" : "TitleBar",
					"type" : "titlebar",
					"style" : ("attach",),

					"x" : 8,
					"y" : 7,

					"width" : BOARD_WIDTH-16,
					"color" : "yellow",

					"children" :
					(
						{ "name":"TitleName", "x": 0, "y": 0, "type":"text", "text": uiScriptLocale.ARTEFAKT_WINDOW_TITLE, "horizontal_align" : "center", "outline":"1","text_horizontal_align" : "center", },
					),
				},

				{
					"name" : "Artifact_Base",
					"type" : "image",

					"x" : 0,
					"y" : 29,

					"image" : "kowal/artefakty.png",
					"horizontal_align":"center",

					"children" :
					(

						{
							"name" : "ArtifactSlots",
							"type" : "slot",

							"x" : 0,
							"y" : 0,

							"width" : BASE_SIZE,
							"height" : BASE_SIZE,

							# System zredukowany do 4 slotow. Kolejnosc = subtype 0..3 z item_proto:
							#   ARTEFAKT1 = 56000 Trofeum KowalMT2 (gora)
							#   ARTEFAKT2 = 56002 Trofeum Alastora (lewo)
							#   ARTEFAKT3 = 56003 Trofeum Hydry    (prawo)
							#   ARTEFAKT4 = 56004 Trofeum Fortuny  (dol)
							"slot" : (
										{"index":item.EQUIPMENT_ARTEFAKT1, "x":144, "y":71, "width":32, "height":32},
										{"index":item.EQUIPMENT_ARTEFAKT2, "x":67, "y":142, "width":32, "height":32},
										{"index":item.EQUIPMENT_ARTEFAKT3, "x":220, "y":142, "width":32, "height":32},
										{"index":item.EQUIPMENT_ARTEFAKT4, "x":143, "y":212, "width":32, "height":32},
									),
						},
					),
				},
			),
		},
	),
}
