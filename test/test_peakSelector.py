import mca_tools as mca

mca.select_language("gl")

Bi = mca.peakSelector("Bi.mca", bkg_file = "Background.mca", peak_energies = [569.69, 1063.656])
Co = mca.peakSelector("Co.mca", bkg_file= "Background.mca", bins_fused = 20, peak_energies = [1173.228, 1332.492])

mca.calibration([Bi,Co])
