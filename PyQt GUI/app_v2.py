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

        self.setGeometry(100, 100, 300, 100)
        self.setWindowTitle('First Program')

app = QApplication(sys.argv)
m = MainWindow()
m.show()
sys.exit(app.exec_())
