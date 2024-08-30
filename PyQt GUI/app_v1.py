import sys
from PyQt5.QtWidgets import *

class MainWindow(QMainWindow):
    pass

app = QApplication(sys.argv)
m = MainWindow()
m.show()
sys.exit(app.exec_())
