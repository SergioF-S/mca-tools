import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.text import Text

class peakSelector:
    """

    """
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

        time = None
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

    def interactive_plot(self):

        peakPositions = []
        delta_x = self.xbins[1] - self.xbins[0]
        sensibility = 0.01 * max(self.xbins) # 1% of the width

        def click_event(event):
            if isinstance(event.artist, Rectangle):
                x = event.artist.get_x()
                # We only want to add new data if it's far enough,
                # to avoid problems with multiple firings in one click
                if len(peakPositions) == 0:
                    peakPositions.append(x)
                    vertical_line_1.set_xdata([x, x])
                    print(peakPositions)
                    # Inside click events, we must ask implicitly
                    # to redraw the changes, if this line isn't here,
                    # it won't change unless you resize the window.
                    fig.canvas.draw()
                elif len(peakPositions) == 1:
                    if abs(peakPositions[0]-x) > sensibility:
                        peakPositions.append(x)
                        vertical_line_2.set_xdata([x,x])
                        # If we don't ask for it, it won't redraw it
                        fig.canvas.draw()
                else:
                    print(peakPositions)
                    return

            elif isinstance(event.artist, Text):
                text = event.artist.get_text()
                if text == "Reset points":
                    # It seems you cannot define this variable inside,
                    # you can only append values to it
                    for i in range(len(peakPositions)):
                        # Every time you remove a value, the index adapt.
                        # index 1 turns to index 0
                        peakPositions.pop(0)

                    # We return the vertical lines to their
                    # original position
                    vertical_line_1.set_xdata([max(self.xbins),
                                               max(self.xbins)])
                    vertical_line_2.set_xdata([0, 0])
                    # If we don't ask for it, it won't redraw it
                    fig.canvas.draw()

                    print("Reset!")

        # We define the plot. The bar plot and the vertical lines
        fig, ax = plt.subplots()
        ax.bar(self.xbins, self.bins, delta_x, picker = True)
        vertical_line_1 = ax.axvline(linestyle = "--", color = "gray")
        vertical_line_2 = ax.axvline(x = max(self.xbins),
                                     linestyle = "--", color = "gray")

        # Here we add the interactive text

        # Peak options
        ax.text(0.65 * max(self.xbins), 0.95 * max(self.bins),
                "Peak options", size="x-large")

        ax.text(0.65 * max(self.xbins), 0.85 * max(self.bins),
                'Mark as single', picker = True, size="large", style =
                "italic")

        ax.text(0.65 * max(self.xbins), 0.75 * max(self.bins),
                'Mark as double', picker = True, size="large", style =
                "italic")

        ax.text(0.65 * max(self.xbins), 0.65 * max(self.bins),
                'Add new peak', picker = True, size="large", style =
                "italic")

        # Global options
        ax.text(0.25 * max(self.xbins), 0.95 * max(self.bins),
                "Global options", size="x-large")

        ax.text(0.25 * max(self.xbins), 0.85 * max(self.bins),
                'Add new peak', picker = True, size="large", style =
                "italic")

        ax.text(0.25 * max(self.xbins), 0.75 * max(self.bins),
                'Reset all', picker = True, size="large", style =
                "italic")



        fig.canvas.mpl_connect('pick_event', click_event)
        fig.show()



file = "/home/stoneboy/Nextcloud/USC/Técnicas IV/Nuclear/Coincidencias gamma-gamma/Datos/Caracterización espectros/19-09-26/Detector 1/Bi/Bi_1_19-02_14-00.mca"
p = peakSelector(file)

#
# bins, time = read_mca(file)
# x_bins = np.arange(0,len(bins),1)
# bins2, x_bins2 = rebining(10, bins)
#
# delta_x = x_bins2[1] - x_bins2[0]

