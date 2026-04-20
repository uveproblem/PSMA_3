import sys
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow,QPushButton,QVBoxLayout,QWidget
# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("My app")
#         self.button=QPushButton("Push Me")
#         self.setFixedSize(QSize(400,300))
#         self.button.setCheckable(True)
#         self.button.clicked.connect(self.the_button_was_clicked)
#         self.button.clicked.connect(self.the_button_was_toggled)
#         self.setCentralWidget(self.button)
#     def the_button_was_clicked(self):
#         self.button.setText("You already clicked me.")
#         self.button.setEnabled(False)
#         self.setWindowTitle("My oneshot app")
#     def the_button_was_toggled(self, checked):
#         print("checked?", checked)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My app")
        layout1 = QVBoxLayout()
        layout2 = QVBoxLayout()
        layout3= QVBoxLayout()
        layout1.setContentsMargins(50,20,50,20)
        layout1.setSpacing(20)
        layout2.addWidget(QPushButton('red'))
        layout2.addWidget(QPushButton('yellow'))
        layout2.addWidget(QPushButton('purple'))
        layout1.addLayout(layout2)

        layout1.addWidget(QPushButton('green'))

        layout3.addWidget(QPushButton('red'))
        layout3.addWidget(QPushButton('purple'))

        layout1.addLayout(layout3)

        # layout.addWidget(QPushButton("don't click me"))
        # layout.addWidget(QPushButton("..."))
        widget = QWidget()
        widget.setLayout(layout1)
        self.setCentralWidget(widget)


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()