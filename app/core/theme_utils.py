from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QPalette


def is_dark_mode() -> bool:
    app = QApplication.instance()
    if app:
        palette = app.palette()
        bg_color = palette.color(QPalette.ColorRole.Window)
        text_color = palette.color(QPalette.ColorRole.WindowText)
        
        bg_luminance = (0.299 * bg_color.red() + 
                       0.587 * bg_color.green() + 
                       0.114 * bg_color.blue())
        
        return bg_luminance < 128
    
    return False


def get_logo_path(logo_type: str = "horizontal") -> str:
    is_dark = is_dark_mode()
    
    if logo_type == "horizontal":
        if is_dark:
            return "brand/campushub-high-resolution-logo-transparent.png"
        else:
            return "brand/campushub-high-resolution-logo-grayscale-transparent.png"
    elif logo_type == "icon":
        if is_dark:
            return "brand/campushub-icon-transparent.png"
        else:
            return "brand/campushub-icon-grayscale-transparent.png"
    
    return ""