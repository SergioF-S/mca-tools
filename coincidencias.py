import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle


class peakSelector:

    def __init__(self, file, **kwargs):
        """
        Indicate self variables here:
        filePath
        binsFused
        time
        bins
        xbins
        """
        self.filePath = file
        self.binsFused = 10 # Default number of bins fused in rebining
        self.time = 0
        self.bins = []
        self.xbins = []
        self.lang = "en"

        # Modify default values with kwargs
        for k, val in kwargs.items():
            if k == "bins_fused":
                self.binsFused = val
            elif k == "lang":
                if val == "en" or val == "es" or val == "gl":
                    self.lang = val
                else:
                    print("Not a valid language, using English!")


        self.read_mca()

        # Rebining can be disbled by usings kwargs.
        if self.binsFused != 0 and self.binsFused != False:
            self.rebining()


    def read_mca(self):
        f = open(self.filePath, "r")

        bins = []
        line = f.readline()
        while line != "":
            if len(line) > 10 and line[:9] == "LIVE_TIME":
                time = int(line.split("-")[1]) # time in seconds

            if (line.strip()).isdigit():
                bins.append(int(line))

            line = f.readline()

        xbins = np.arange(0, len(bins), 1)

        self.bins = bins
        self.xbins = xbins
        self.time = time

        return bins, time

    def rebining(self):
        """
        Performs a rebining of binsFused channels
        """

        new_xbins = []
        new_bins = []
        j = 0
        sum_bins = 0

        for i in range(len(self.bins)):

            # If we are on the first bin of the fused group,
            # we save the x value
            if j == 0:
                mean_x = self.xbins[i]

            # We keep adding up the bins until we reach
            # j == num_channels_fused.
            sum_bins += self.bins[i]
            j += 1

            # If we are on the last bin of the fused group,
            # we save the sum of counts and we calculate the
            # x value from the mean of the start and end x.
            if j == self.binsFused:
                j = 0
                new_bins.append(sum_bins)
                mean_x += self.xbins[i]
                new_xbins.append(mean_x/2)
                sum_bins = 0

        self.bins = new_bins
        self.xbins = new_xbins

        return new_bins, new_xbins


    def plot(self):

        delta_x = self.xbins[1] - self.xbins[0]

        plt.clf()
        plt.bar(self.xbins, self.bins, delta_x)
        if self.lang == "en":
            plt.xlabel("Channels")
            plt.ylabel("Counts")
            plt.title("Gamma Espectrogram")
        elif self.lang == "es":
            plt.xlabel("Canales")
            plt.ylabel("Cuentas")
            plt.title("Espectrograma Gamma")
        elif self.lang == "gl":
            plt.xlabel("Canais")
            plt.ylabel("Contas")
            plt.title("Espectrograma Gamma")

        plt.show()
