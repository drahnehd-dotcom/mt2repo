import uiScriptLocale
import localeInfo

PRIVATESEARCH_PATH = "d:/ymir work/ui/privatesearch/"

BOARD_WIDTH = 220
BOARD_HEIGHT = 165

window = {
	"name" : "PrivateShopSearchFilterDialog",

	"x" : 0,
	"y" : 0,

	"style" : ("movable", "float",),

	"width" : BOARD_WIDTH,
	"height" : BOARD_HEIGHT,

	"children" :
	(
		{
			"name" : "Board",
			"type" : "board_with_titlebar",

			"x" : 0,
			"y" : 0,

			"width" : BOARD_WIDTH,
			"height" : BOARD_HEIGHT,
			
			"title" : uiScriptLocale.PRIVATESHOPSEARCH_FILTER_SELECT_TITLE,
		
			"children" :
			(
				{
					"name" : "LeftTop",
					"type" : "image",
					"x" : 7,
					"y" : 32,
					"image" : PRIVATESEARCH_PATH+"private_mainboxlefttop.sub",
				},

				{
					"name" : "RightTop",
					"type" : "image",
					"x" : BOARD_WIDTH - 16 -7,
					"y" : 32,
					"image" : PRIVATESEARCH_PATH+"private_mainboxrighttop.sub",
				},

				{
					"name" : "LeftBottom",
					"type" : "image",
					"x" : 7,
					"y" : BOARD_HEIGHT - 16 - 7,
					"image" : PRIVATESEARCH_PATH+"private_mainboxleftbottom.sub",
				},

				{
					"name" : "RightBottom",
					"type" : "image",
					"x" : BOARD_WIDTH - 16 -7,
					"y" : BOARD_HEIGHT - 16 - 7,
					"image" : PRIVATESEARCH_PATH+"private_mainboxrightbottom.sub",
				},

				{
					"name" : "leftcenterImg",
					"type" : "expanded_image",
					"x" : 7,
					"y" : 44,
					"image" : PRIVATESEARCH_PATH+"private_leftcenterImg.tga",
					"rect" : (0.0, 0.0, 0, 5.0),
				},

				{
					"name" : "rightcenterImg",
					"type" : "expanded_image",
					"x" : BOARD_WIDTH - 16 - 8,
					"y" : 44,
					"image" : PRIVATESEARCH_PATH+"private_rightcenterImg.tga",
					"rect" : (0.0, 0.0, 0, 5.0),
				},

				{
					"name" : "topcenterImg",
					"type" : "expanded_image",
					"x" : 7 + 10,
					"y" : 32,
					"image" : PRIVATESEARCH_PATH+"private_topcenterImg.tga",
					"rect" : (0.0, 0.0, 9.6, 0),
				},

				{
					"name" : "bottomcenterImg",
					"type" : "expanded_image",
					"x" : 7 + 10,
					"y" : BOARD_HEIGHT - 16 - 7,
					"image" : PRIVATESEARCH_PATH+"private_bottomcenterImg.tga",
					"rect" : (0.0, 0.0, 9.6, 0),
				},

				{
					"name" : "centerImg",
					"type" : "expanded_image",
					"x" : 7 + 10,
					"y" : 48,
					"image" : PRIVATESEARCH_PATH+"private_centerImg.tga",
					"rect" : (0.0, 0.0, 9.6, 5.0),
				},

				{
					"name" : "FilterScrollBar",
					"type" : "scrollbar",

					"x" : BOARD_WIDTH - 25,
					"y" : 36,

					"size" : 119,
				},

				{
					"name" : "FilterSlotWindowMask",
					"type": "window",

					"x" : 7,
					"y" : 32,

					"width" : 185,
					"height" : 123,
				},
			),
		},
	),
}
