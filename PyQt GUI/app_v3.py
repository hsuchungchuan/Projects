import sys
from PyQt5.QtWidgets import *

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        vbox = QVBoxLayout()
        main_widget.setLayout(vbox)

        label = QLabel('Hello World')
        vbox.addWidget(label)

        self.label = QLabel('Click button to change text')
        vbox.addWidget(self.label)

        button = QPushButton('Click me')
        vbox.addWidget(button)
        button.clicked.connect(self.on_button_clicked)

        self.setGeometry(100, 100, 300, 100)
        self.setWindowTitle('First Program')

    def on_button_clicked(self):
        self.label.setText('Button clicked')

app = QApplication(sys.argv)
m = MainWindow()
m.show()
sys.exit(app.exec_())
