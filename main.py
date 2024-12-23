import ctypes
import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication

from GUI.MainWindow import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("GUI\\assets\\game_icon.jpeg"))
    if sys.platform == "win32":
        app_id = "Sudoku Solver"
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())