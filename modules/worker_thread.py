from PyQt5.QtCore import QThread, pyqtSignal

from services.game_service import generate_random_unique_sudoku


class WorkerThread(QThread):
    finished = pyqtSignal(object)

    def __init__(self, difficulty: str):
        super(WorkerThread, self).__init__()
        self.method_name = difficulty

    def run(self):
        solve = generate_random_unique_sudoku(self.method_name)
        self.finished.emit(solve)
