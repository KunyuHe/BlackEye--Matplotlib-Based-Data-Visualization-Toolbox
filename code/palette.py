import json
import os
import numpy as np
import matplotlib.pyplot as plt

PATH = "../palettes/"


class Palette:

    def __init__(self):
        self.color_dict = None
        self.color_lst = None
        self.n = None
        self.pair = None

    def getPallete(self, name):
        # Check if there is a palette with the specified name
        path = os.path.join(PATH, name + ".json")
        if not os.path.isfile(path):
            raise FileNotFoundError("Cannot find palette named '%s'." % name)

        with open(path, 'r') as json_file:
            palette = json.load(json_file)

        self.color_dict = palette['colors']
        self.color_lst = self.color_dict.values()
        self.n = palette['n']
        self.pair = palette['pair']

    @staticmethod
    def getAllPalttesNames(preview=True):
        """
        Adapted partly from Matplotlib.
        (Source: https://matplotlib.org/3.1.0/tutorials/colors/colormaps.html)
        :param preview:
        :return:
        """
        names = [palette.split(".")[0] for palette in os.listdir(PATH)]

        if preview:
            gradient = np.linspace(0, 1, 256)
            gradient = np.vstack((gradient, gradient))

    def previewPalette(self):
        next
