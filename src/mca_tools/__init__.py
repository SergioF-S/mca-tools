from .translations import valid_languages

# Default value
lang = "en"
def select_language(new_lang):
    global lang
    if new_lang in valid_languages:
        lang = new_lang
    else:
        print("Not a valid language, using English!")
        lang = "en"


# These are loaded after the lang to avoid circular import
from .peakSelector import peakSelector
from .calibration import calibration, calibration_helper


__all__ = ["peakSelector",
            "calibration",
            "calibration_helper"
            "select_language"]







