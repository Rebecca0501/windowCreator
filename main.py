import sys
from PyQt6.QtWidgets import (QApplication )
from PreviewArea import *
from windowCreator import *

def main():
    app = QApplication(sys.argv)
    window = WindowGeneratorApp()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()