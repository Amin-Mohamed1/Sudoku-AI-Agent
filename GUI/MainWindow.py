import time
from copy import deepcopy

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QLineEdit, QMessageBox, QApplication, QProgressDialog
from PyQt5.uic import loadUi

from modules.worker_thread import WorkerThread
from services.game_service import solve_sudoku, is_board_solvable, \
    is_board_uniquely_solvable


class MainWindow(QDialog):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("GUI\\sudoku-gui-2.ui", self)
        self.setWindowTitle("Sudoku Solver")

        self.difficulty: str = "Easy"
        self.loading_dialog = None

        self.sudoku_grid: list[list[int]] = [[0 for _ in range(9)] for _ in range(9)]
        self.gui_grid: list[list[QLineEdit]] = self.set_up_gui_grid()
        self.set_up_cells_change_event()
        modes: list[str] = ["Easy", "Medium", "Hard"]

        self.mode_combobox.addItems(modes)
        self.mode_combobox.setCurrentIndex(0)
        self.mode_combobox.currentIndexChanged.connect(self.set_difficulty)

        self.solve_button.clicked.connect(self.solve_board)
        self.clear_button.clicked.connect(self.clear_sudoku)
        self.randomize_button.clicked.connect(self.randomize_sudoku)

    def set_difficulty(self):
        self.difficulty = self.mode_combobox.currentText()

    def clear_sudoku(self):
        self.change_QLineEdit_signal(True)
        self.sudoku_grid = [[0 for _ in range(9)] for _ in range(9)]
        for i in range(9):
            for j in range(9):
                self.gui_grid[i][j].setText("")
        self.change_QLineEdit_signal(False)

    def show_board(self):
        self.change_QLineEdit_signal(True)
        for i in range(9):
            for j in range(9):
                if self.sudoku_grid[i][j] != 0:
                    self.gui_grid[i][j].setText(str(self.sudoku_grid[i][j]))
                else:
                    self.gui_grid[i][j].setText("")
        self.change_QLineEdit_signal(False)

    def read_board(self):
        for i in range(9):
            for j in range(9):
                value = self.gui_grid[i][j].text()
                if value == "":
                    self.sudoku_grid[i][j] = 0
                else:
                    self.sudoku_grid[i][j] = int(value)

    def set_up_gui_grid(self) -> list[list[QLineEdit]]:
        widget_list = []
        for i in range(9):
            row = []
            for j in range(9):
                widget = self.findChild(QLineEdit, f"board_label{i}{j}")
                row.append(widget)
            widget_list.append(row)

        return widget_list

    def set_up_cells_change_event(self):
        for i in range(9):
            for j in range(9):
                self.gui_grid[i][j].textChanged.connect(lambda _, row=i, col=j: self.validate_user_input(row, col))

    def solve_board(self):
        if not self.is_valid_input_number():
            self.show_error_message("Please enter a valid number between 1 and 9")
            return
        self.read_board()
        if is_board_uniquely_solvable(deepcopy(self.sudoku_grid)):
            self.sudoku_grid = solve_sudoku(self.sudoku_grid)
            self.show_board()
        else:
            if self.show_warning_message("The current board is not uniquely solvable"):
                self.sudoku_grid = solve_sudoku(self.sudoku_grid)
                self.show_board()

    def randomize_sudoku(self):
        self.setEnabled(False)
        self.loading_dialog = QProgressDialog("Loading, please wait...", None, 0, 100, self)
        self.loading_dialog.setWindowModality(Qt.WindowModal)
        self.loading_dialog.setFixedSize(300, 100)
        self.loading_dialog.setWindowTitle("Loading")
        self.loading_dialog.setCancelButton(None)
        self.loading_dialog.setWindowFlags(self.windowFlags() & ~Qt.WindowCloseButtonHint)
        self.loading_dialog.setValue(10)
        self.loading_dialog.show()

        QApplication.processEvents()

        worker_thread = WorkerThread(self.difficulty)
        worker_thread.finished.connect(self.thread_complete_handler)
        time.sleep(0.5)
        self.loading_dialog.setValue(30)
        QApplication.processEvents()
        worker_thread.run()

    def validate_user_input(self, row: int, col: int) -> None:
        if not self.is_valid_input_number():
            self.show_error_message("Please enter a valid number between 1 and 9")
            self.change_QLineEdit_signal(True)
            self.gui_grid[row][col].setText("")
            self.change_QLineEdit_signal(False)
            return
        self.read_board()
        if is_board_solvable(self.sudoku_grid):
            self.gui_grid[row][col].setStyleSheet(
                """
                border: 1px groove rgb(215, 225, 244);
                background-color: white;
                """
            )
        else:
            self.gui_grid[row][col].setStyleSheet(
                """
                border: 1px groove red;
                background-color: white;
                """
            )
            self.show_error_message(
                f"The value {self.sudoku_grid[row][col]} in cell ({row + 1}, {col + 1}) is invalid")
            self.gui_grid[row][col].setText("")

    def show_error_message(self, message: str) -> None:
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle("Error")
        msg.setText(message)
        msg.setInformativeText("It will be deleted")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    def show_warning_message(self, message: str) -> bool:
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle("Warning")
        msg.setText(message)
        msg.setInformativeText("Do you want to continue?")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        return msg.exec_() == QMessageBox.Yes

    def change_QLineEdit_signal(self, disable: bool):
        for i in range(9):
            for j in range(9):
                self.gui_grid[i][j].blockSignals(disable)

    def thread_complete_handler(self, result):
        self.loading_dialog.setValue(100)
        time.sleep(0.5)
        self.loading_dialog.close()
        self.sudoku_grid = result
        self.setEnabled(True)
        self.show_board()

    def is_valid_input_number(self):
        for i in range(9):
            for j in range(9):
                value = self.gui_grid[i][j].text()
                if value == "":
                    continue
                else:
                    if not value.isdigit() or int(value) < 1 or int(value) > 9:
                        return False

        return True
