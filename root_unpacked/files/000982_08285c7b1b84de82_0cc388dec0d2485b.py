import uiScriptLocale

ROOT_PATH = "d:/ymir work/ui/game/save/"

window = {
    "name": "SaveMapPreviewDialog",
    "style": (
        "movable",
        "float",
    ),
    "x": 0,
    "y": 0,
    "width": 258,
    "height": 278,
    "children": (
        {
            "name": "Board",
            "type": "save_board",
            "style": ("attach",),
            "x": 0,
            "y": 0,
            "width": 258,
            "height": 278,
            "children": (
                {
                    "name": "header",
                    "type": "expanded_image",
                    "x": 3,
                    "y": 1,
                    "x_scale": 1.0,
                    "y_scale": 1.0,
                    "image": ROOT_PATH + "preview_header.sub",
                    "children": (
                        {
                            "name": "map_name",
                            "type": "text",
                            "x": 0,
                            "y": 0,
                            "all_align": "center",
                            "text": "",
                            "outline": True,
                        },
                    ),
                },
                {
                    "name": "map_image",
                    "type": "expanded_image",
                    "x": 4,
                    "y": 25,
                    "image": "d:/ymir work/ui/atlas/metin2_map_a1/atlas.sub",
                    "children": (
                        {
                            "name": "map_point",
                            "type": "image",
                            "x": 20,
                            "y": 20,
                            "image": "d:/ymir work/ui/minimap/whitemark_new.tga",
                        },
                    ),
                },
            ),
        },
    ),
}
