from mca_tools.peakSelector import peakSelector

lang = "gl"

Bi = peakSelector("Bi.mca", bkg_file = "Background.mca")
Co = peakSelector("Co.mca", bkg_file= "Background.mca", bins_fused = 20)

Bi.select_peaks()
Bi.fit_peak
