import json
from pathlib import Path

class _TikzConfig:

    def __init__(self):

        self.USE_DECIMAL_COMMA: bool = False

        self.LEGEND_REL_X: float = 0.03
        self.LEGEND_REL_Y: float = 0.03

        self.LEFT_PADDING: float = 0.1
        self.RIGHT_PADDING: float = 0.1
        self.TOP_PADDING: float = 0.1
        self.BOTTOM_PADDING: float = 0.1
        self.Y_LABEL_PADDING: float = 0.6
        self.SEC_Y_PADDING: float = 0.8
        self.SEC_Y_LABEL_PADDING: float = 0.6
        self.TITLE_PADDING: float = 0.6
        self.X_LABEL_PADDING: float = 0.6
        self.XTICK_PADDING: float = 0.7
        self.YTICK_PADDING: float = 0.7

        self.DEFAULT_WIDTH: float = 12
        self.DEFAULT_HEIGHT: float = 10

        self.SHARED_AXIS_REL_MARGIN: float = 0.03

        self.SAVE_DATAPOINTS: bool = True
        self.DATAPOINTS_DIR: str = "datapoints"  # ignored if SAVE_DATAPOINTS == False
        self.UPDATE_DATA_ONLY: bool = False       # ignored if SAVE_DATAPOINTS == False
        self.UPDATE_STYLE_ONLY: bool = False      # ignored if SAVE_DATAPOINTS == False
        self.SHOW_SAVENAME: str = "showplot"
        self.IMSHOW_SAVENAME: str = "imshow"

        self.REDUCE_NUM_POINTS: bool = True
        self.REDUCE_METHOD: int = 1              # 0: remove based on index; 1: remove based on plot distance; 2: remove based on curvature (good for line plots)
        self.MAX_POINTS_PER_FIGURE: int = 10000
        self.MAX_POINTS_PER_ELEMENT: int = 1000

        self.STANDALONE: bool = False
        self.TIKZ_COMPAT: float = 1.18 # only for standalone, used to change the setting in preambule, but does not guarantee the compatibility of the generated code wito older versions of pgfplots.
        self.USE_XCOLOR: bool = True
        self.USE_GROUPPLOTS: bool = True
        self.SCHOOL_AXIS: bool = False
        self.SCHOOL_AXIS_LABEL_MARGIN: float = 0.1

        self.CBAR_X_OFFSET: float = 0.05
        self.CBAR_Y_OFFSET: float = 0.2
        self.CBAR_X_MARGIN: float = 0.5
        self.CBAR_Y_MARGIN: float = 0.5

        self.CBAR3_Z_OFFSET: float = 0.2   # for 3D vertical
        self.CBAR3_H_OFFSET: float = 0.2    # for 3D horizontal

        self.DEFAULT_3D_ROLL: float = 0
        self.DEFAULT_3D_AZIM: float = 0
        self.DEFAULT_3D_ELEV: float = 0

        self._config_file: Path = Path.home() / ".tikz_userconf.json"

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