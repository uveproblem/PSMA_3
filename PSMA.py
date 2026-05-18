import datetime

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import sys

from PyQt6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QPushButton, QHBoxLayout,
QLineEdit, QMessageBox, QLabel, QPushButton, QHBoxLayout,)

today = datetime.datetime.today()
data = today.strftime('%Y-%m-%d')
class MplCanvas(FigureCanvas):
    def __init__(self):
        self.figure = Figure()
        self.ax = self.figure.add_subplot(111)
        super().__init__(self.figure)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ilu żydów popełniło lichwę")
        self.resize(1000, 800)

        self.values = []

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        input_layout = QHBoxLayout()
        self.label = QLabel("Podaj wartość:")
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Np. 125")
        self.add_button = QPushButton("Dodaj")
        self.add_button.clicked.connect(self.add_value)
        input_layout.addWidget(self.label)
        input_layout.addWidget(self.input_field)
        input_layout.addWidget(self.add_button)
        self.canvas = MplCanvas()

        main_layout.addLayout(input_layout)
        main_layout.addWidget(self.canvas)
        self.update_plot()

    def add_value(self):
        text = self.input_field.text().strip()
        if not text:
            QMessageBox.warning(self, "Błąd", "Wpisz wartość.")
            return
        try:
            value = float(text)
        except ValueError:
            QMessageBox.warning(self, "Błąd", "Podaj poprawną liczbę.")
            return
        self.values.append(value)
        self.input_field.clear()
        self.update_plot()
    def update_plot(self):
        self.canvas.ax.clear()
        if self.values:
            x = list(range(1, len(self.values) + 1))
            self.canvas.ax.plot(x, self.values, marker='o')
            self.canvas.ax.set_title("Dzisiejsze lichwy:")
            self.canvas.ax.set_xlabel("Numer punktu")
            self.canvas.ax.set_ylabel("Ilość lichw")
            self.canvas.ax.grid(True)
        else:
            self.canvas.ax.set_title("Brak danych z dnia:")
            self.canvas.ax.set_xlabel("Seria danych")
            self.canvas.ax.set_ylabel("Ilośc lichw")
            self.canvas.ax.grid(True)
        self.canvas.draw()
app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
