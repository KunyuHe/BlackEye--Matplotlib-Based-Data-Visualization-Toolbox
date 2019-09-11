import json
import os

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
from utils import create_font_setting

PATH = "../palettes/"


class Palette:

    def __init__(self):
        self.color_dict = None
        self.color_lst = None
        self.n = None
        self.pair = None
        self.cmap = None
        self.type = None

    def getPallete(self, name):
        # Check if there is a palette with the specified name
        path = os.path.join(PATH, name + ".json")
        if not os.path.isfile(path):
            raise FileNotFoundError("Cannot find palette named '%s'." % name)

        with open(path, 'r') as json_file:
            palette = json.load(json_file)

        self.color_dict = palette['colors']
        self.color_lst = list(self.color_dict.values())
        self.n = palette['n']
        self.pair = palette['pair']
        self.cmap = LinearSegmentedColormap.from_list(name, self.color_lst,
                                                      N=self.n)
        self.type = palette['type']

        return self

    def getAllPalttes(self, preview=True):
        """
        Adapted partly from Matplotlib.
        (Source: https://matplotlib.org/3.1.0/tutorials/colors/colormaps.html)
        :param preview:
        :return:
        """
        names = [palette.split(".")[0] for palette in os.listdir(PATH)]
        n = len(names)

        if not preview:
            return "Palettes currently defined:\n\t" + "\n\t".join(names)

        gradient = np.linspace(0, 1, 256)
        gradient = np.vstack((gradient, gradient))

        qualitatives, sequentials = [], []
        for name in names:
            print(name)
            palette = Palette().getPallete(name)
            if palette.type == "qualitative":
                qualitatives.append((name, palette.cmap))
            else:
                sequentials.append((name, palette.cmap))

        title_font, axis_font, _ = create_font_setting((18, 16, 12))

        def preview_type(cmap_type, name_cmap):
            fig, axes = plt.subplots(figsize=(13.08, 1.5 * n), nrows=n, dpi=400)
            fig.subplots_adjust(top=0.95, bottom=0.01, left=0.2, right=0.79)
            if n == 1:
                axes = [axes]
            axes[0].set_title("%s Colormaps" % cmap_type.title(),
                              fontproperties=title_font)

            for ax, (name, cmap) in zip(axes, name_cmap):
                ax.imshow(gradient, aspect='auto', cmap=cmap)
                pos = list(ax.get_position().bounds)
                x_text = pos[0] - 0.2
                y_text = pos[1] + pos[3] / 2.
                fig.text(x_text, y_text, name, va='center', ha='right',
                         fontproperties=axis_font)

                ax.set_axis_off()

        preview_type("qualitative", qualitatives)
        if sequentials:
            preview_type("sequential", sequentials)

        plt.tight_layout()
