from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi


class MainWindow(QDialog):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("GUI\\sudoku-gui-2.ui", self)
        self.setWindowTitle("Sudoku Solver")
        self.difficulty: str = "Easy"
        self.sudoku_grid: list[list[int]] = []
        modes: list[str] = ["Easy", "Medium", "Hard"]
        self.mode_combobox.addItems(modes)
        self.mode_combobox.setCurrentIndex(0)
        self.mode_combobox.currentIndexChanged.connect(self.set_difficulty)
        self.solve_button.clicked.connect(self.solve_sudoku)
        self.clear_button.clicked.connect(self.clear_sudoku)
        self.randomize_button.clicked.connect(self.randomize_sudoku)

    def set_difficulty(self):
        self.difficulty = self.mode_combobox.currentText()

    def solve_sudoku(self):
        pass

    def clear_sudoku(self):
        self.sudoku_grid = []

    def randomize_sudoku(self):
        pass
