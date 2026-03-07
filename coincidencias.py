import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.text import Text

# Util funcions to reduce cluttering in the class

"""
Resets the values of the last peak inserted in the plot. It does so
by removing the elements of the sublist that contains the information
of the last peak.

It doesn't have a input because it's suposed to access a variable in
another scope (outside a function)

peak_positions' structure:
Peak positions is a list that contains lists with another list and a
string. The most nested list contains the start and end poins
of the peak. This is inside another list that contains also a string.
The string is the mode of the peak. If two peaks are too close,
they need to be adjusted together in curve_fit.

The main list contains the tuples for every peak in the graph.

Visual expanation:
[ peak1([start point, end point], "single") peak2([start point 1,
end point 1], "single")]
"""
# The code will be like this:
# list = []
# def func():
#   reset_peak_data(list)
#
# We cannot redefine the list inside the function (list = [],
# so we need to remove all the elements by hand





def save_peak_type(peak_type: str):

    if len(peak_positions) == 0:
        print("It's necessary to select two points to create a peak")

    else:
        if len(peak_positions[-1]) != 2:
            print("It's necessary to select two points to create a peak")

        else:
            peak_positions[-1][1] = peak_type
            peak_positions.append([[], None]) # Add the scheme next element
            print("Peak selected!")


def save_peak_data(x):
    """
    Save the data and plot the line
    """

    # Firstly, we check whether the last peak has both points
    if len(peak_positions[-1][0]) == 2 and peak_positions[-1][1] == None:
        print("Both points selected! Please confirm the peak type or " +
              "reset the peak to select the points again")
    else:
        peak_positions[-1][0].append(x)
        save_line_data(x)

def save_line_data(x):

    line = ax.axvline(x=x, ymax=0.5, style = "--", color = "black")

    # We want the lines in pairs. Each list represents a peak, and each
    # list is supposed to elements, one for each line.
    if len(line_positions) == 0:
        line_positions.append([line])

    else:
        if len(line_positions[-1]) == 1:
            line_positions[-1].append(line)

        else:
            line_positions.append([line])




class peakSelector:
    """
    Class for getting the curve_fit parameters of the Gaussian peaks
    in a spectrogram. Is asks for the user to select the peaks to be
    adjusted, by hand. After that, it computes the curve_fit and returns
    the optimal parameters.

    Input:
    file_path: the path to the mca file that contains spectroscopic info

    **kwargs:
        bins_fused: the amount of bins whose data is being "fused" in
                    the rebining. Setting it to 0 or False cancells
                    automatic rebining.

    Methods:
    read_mca: reads the number of counts in each channel and the total
              time of the measurement.

    rebining: joins the data counts of a number of channels to reduce
              uncertainty on the parametric optimization. By default,
              it makes a 10 bin rebining. .rebining takes as an argument
              the number of bins fused.

    plot: represents the data in a static, non-interactive way. It's used
          to test if the data was loaded properly.

    interactive_plot: let's the user select the desired peaks to be
                      analyzed by curve_fit. It works with matplotlib
                      picker events.

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
        self.file_path = file
        self.bins_fused = 10 # Default number of bins fused in rebining
        self.time = 0
        self.bins = []
        self.xbins = []
        self.lang = "en"
        self.peak_positions = []

        # Modify default values with kwargs
        for k, val in kwargs.items():
            if k == "bins_fused":
                self.bins_fused = val
            elif k == "lang":
                if val == "en" or val == "es" or val == "gl":
                    self.lang = val
                else:
                    print("Not a valid language, using English!")


        self.read_mca()

        # Rebining can be disbled by usings kwargs.
        if self.bins_fused != 0 and self.bins_fused != False:
            self.rebining(self.bins_fused)


    def read_mca(self):
        f = open(self.file_path, "r")

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

    def rebining(self, bins_fused):
        """
        Performs a rebining of bins_fused channels
        """

        # We make it posible to update the rebining
        if bins_fused != self.bins_fused:
            self.bins_fused = bins_fused


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
            if j == self.bins_fused:
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
            plt.title("Gamma Spectrogram")
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

        peak_positions = [ [ [], None ], ]
        line_positions = []

        delta_x = self.xbins[1] - self.xbins[0]
        sensibility = 0.01 * max(self.xbins) # 1% of the width


        def save_peak_type(peak_type: str):

            if len(peak_positions) == 0:
                print("It's necessary to select two points to create a peak")

            else:
                if len(peak_positions[-1]) != 2:
                    print("It's necessary to select two points to create a peak")

                else:
                    peak_positions[-1][1] = peak_type
                    # Add the scheme next element
                    peak_positions.append([[], None])

                    for line in line_positions[-1]:
                        line.set(color = "gray")

                    print("Peak selected!")

        def save_peak_data(x):
            """
            Save the data and plot the line
            """

            # Firstly, we check whether the last peak has both points
            if len(peak_positions[-1][0]) == 2 and peak_positions[-1][1] == None:
                print("Both points selected! Please confirm the peak " +
                    "type or reset the peak to select the points again")
            else:
                if len(peak_positions[-1][0]) == 1:
                    if abs(x - peak_positions[-1][0][0]) > sensibility:
                        peak_positions[-1][0].append(x)
                        save_line_data(x)

                else:
                    peak_positions[-1][0].append(x)
                    save_line_data(x)

        def save_line_data(x):

            line = ax.axvline(x=x, ymax=0.5, ls = "--", color = "black")

            # We want the lines in pairs. Each list represents a peak, and each
            # list is supposed to elements, one for each line.
            if len(line_positions) == 0:
                line_positions.append([line])

            else:
                if len(line_positions[-1]) == 1:
                    line_positions[-1].append(line)

                else:
                    line_positions.append([line])

        def reset_peak_data():
            print(peak_positions)
            if len(peak_positions[-1][0]) != 0:
                peak_positions.pop(-1)
                peak_positions.append([ [ ], None])

                for line in line_positions[-1]:
                    line.remove()
                line_positions.pop(-1)


        def reset_global_data():
            for lines in line_positions:
                for line in lines:
                    line.remove()

            for i in range(len(peak_positions)):
                # Every time you remove a value, the indexes adapt.
                # index 1 turns to index 0
                peak_positions.pop(0)
                if i < (len(peak_positions) - 2):
                    line_positions.pop(0)

            peak_positions.append([ [], None ])



        def click_event(event):
            if isinstance(event.artist, Rectangle):
                x = event.artist.get_x()
                save_peak_data(x)
                fig.canvas.draw()

            elif isinstance(event.artist, Text):
                text = event.artist.get_text()
                if text == "Reset current peak":
                    reset_peak_data()
                    fig.canvas.draw()
                    print("Reset!")

                elif text == "Reset all peaks":
                    reset_global_data()
                    fig.canvas.draw()

                elif text == "Mark as single":
                    save_peak_type("single")
                    fig.canvas.draw()


                elif text == "Mark as double":
                    save_peak_type("single")
                    fig.canvas.draw()

        def close_event(event):
            if peak_positions[-1][1] == None:
                self.peak_positions = peak_positions[:-1]


        # We define the plot. The bar plot and the vertical lines
        fig, ax = plt.subplots()
        ax.bar(self.xbins, self.bins, delta_x, picker = True)


        # Here we add the interactive text

        # Peak options
        max_xbins = max(self.xbins)
        max_bins = max(self.bins)

        ax.text(0.65 * max_xbins , 0.95 * max_bins ,
                "Confirm peak", size="x-large")

        ax.text(0.65 * max_xbins, 0.85 * max_bins,
                'Mark as single', picker = True, size="large", style =
                "italic")

        ax.text(0.65 * max_xbins, 0.75 * max_bins,
                'Mark as double', picker = True, size="large", style =
                "italic")


        # Global options
        ax.text(0.25 * max_xbins, 0.95 * max_bins,
                "Reset peak", size="x-large")

        ax.text(0.25 * max_xbins, 0.85 * max_bins,
                'Reset current peak', picker = True, size="large", style =
                "italic")

        ax.text(0.25 * max_xbins, 0.75 * max_bins,
                'Reset all peaks', picker = True, size="large", style =
                "italic")



        fig.canvas.mpl_connect('pick_event', click_event)
        fig.canvas.mpl_connect('close_event', close_event)
        fig.show()



file = "/home/stoneboy/Nextcloud/USC/Técnicas IV/Nuclear/Coincidencias gamma-gamma/Datos/Caracterización espectros/19-09-26/Detector 1/Bi/Bi_1_19-02_14-00.mca"
p = peakSelector(file)

#
# bins, time = read_mca(file)
# x_bins = np.arange(0,len(bins),1)
# bins2, x_bins2 = rebining(10, bins)
#
# delta_x = x_bins2[1] - x_bins2[0]

