import os


CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
FONT_PATH = os.path.join(CURRENT_DIR, "Arial.ttf")
LOGO_PATH = os.path.join(CURRENT_DIR, "logo.png")
DEVICE = "/dev/usb/lp3"
LABEL_WIDTH = 384  # Стандарт для 58мм ленты (203 dpi)