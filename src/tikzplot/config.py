import json
from pathlib import Path


class _TikzConfig:

    def __init__(self):

        self.USE_DECIMAL_COMMA = True

        self.LEGEND_REL_X = 0.03
        self.LEGEND_REL_Y = 0.03

        self.LEFT_PADDING = 0.8
        self.RIGHT_PADDING = 0.2
        self.TOP_PADDING = 0.2
        self.BOTTOM_PADDING = 0.8
        self.Y_LABEL_PADDING = 0.6
        self.SEC_Y_PADDING = 0.8
        self.SEC_Y_LABEL_PADDING = 0.6
        self.TITLE_PADDING = 0.6
        self.X_LABEL_PADDING = 0.6

        self.DEFAULT_WIDTH = 12
        self.DEFAULT_HEIGHT = 10

        self.SHARED_AXIS_REL_MARGIN = 0.03

        self.SAVE_DATAPOINTS = True
        self.DATAPOINTS_DIR = "datapoints"  # ignored if SAVE_DATAPOINTS == False
        self.UPDATE_DATA_ONLY = False       # ignored if SAVE_DATAPOINTS == False
        self.UPDATE_STYLE_ONLY = False      # ignored if SAVE_DATAPOINTS == False
        self.SHOW_SAVENAME = "showplot"

        self.REDUCE_NUM_POINTS = True
        self.REDUCE_METHOD = 1              # 0: remove based on index; 1: remove based on plot distance; 2: remove based on curvature
        self.MAX_POINTS_PER_FIGURE = 10000
        self.MAX_POINTS_PER_ELEMENT = 1000

        self.USE_XCOLOR = True

        self._config_file = Path.home() / ".tikz_userconf.json"

        self._load_user_config()

    def modifyParam(self, **kwargs):
        for k, v in kwargs.items():
            if not hasattr(self, k):
                raise ValueError(f"Unknown TikzConfig parameter: {k}")
            setattr(self, k, v)

    def setPermanent(self, **kwargs):

        self.modifyParam(**kwargs)

        data = self._read_file()
        data.update(kwargs)

        with open(self._config_file, "w") as f:
            json.dump(data, f, indent=2)

    def _load_user_config(self):

        if not self._config_file.exists():
            return

        with open(self._config_file) as f:
            data = json.load(f)

        for k, v in data.items():
            if hasattr(self, k):
                setattr(self, k, v)

    def _read_file(self):

        if not self._config_file.exists():
            return {}

        with open(self._config_file) as f:
            return json.load(f)

TikzConfig = _TikzConfig()