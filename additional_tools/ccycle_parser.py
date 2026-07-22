import matplotlib as mpl
import matplotlib.pyplot as plt

# A dictionary mapping your requested names to their exact internal Matplotlib names
style_mapping = {
    "default": "default",
    "classic": "classic",
    "tableau": "tableau",
    "colorblind10": "tableau-colorblind10", 
    "ggplot": "ggplot",
    "538": "fivethirtyeight",
    "seaborn": "seaborn-v0_8",
    "bmh": "bmh"
}

for sb_variant in ['seaborn-v0_8-colorblind', 'seaborn-colorblind']:
    if sb_variant in plt.style.available:
        style_mapping["colorblind"] = sb_variant
        break
else:
    style_mapping["colorblind"] = "tableau-colorblind10"
cycle = {}

for custom_name, internal_name in style_mapping.items():
    if internal_name in plt.style.available or internal_name in ['default', 'classic']:
        # Using a context manager ensures we don't permanently alter global settings
        with plt.style.context(internal_name):
            raw_colors = mpl.rcParams['axes.prop_cycle'].by_key()['color']
            cycle[custom_name] = [mpl.colors.to_hex(c) for c in raw_colors]

import pprint
pprint.pprint(cycle, compact=True, width=500)