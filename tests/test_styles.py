from typing import Literal, get_type_hints

from tikzplot.styles import Styles


def test_use_accepts_only_supported_style_literals() -> None:
    style_type = get_type_hints(Styles.use)["style"]
    assert style_type == Literal[
        "default",
        "classic",
        "tableau",
        "colorblind10",
        "ggplot",
        "538",
        "seaborn",
        "bmh",
    ]
