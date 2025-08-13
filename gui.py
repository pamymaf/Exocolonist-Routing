import sys

from PyQt6.QtGui import QColor, QPalette
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtWidgets import (
    QApplication,
    QCheckBox,
    QPushButton,
    QComboBox,
    QDial,
    QDoubleSpinBox,
    QLabel,
    QLineEdit,
    QListWidget,
    QMainWindow,
    QSlider,
    QSpinBox,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QStackedLayout,
    QGridLayout,
)

from router import *

class MainWindow(QMainWindow):
  def __init__(self):
    super() .__init__()
    self.setWindowTitle("Exocolonist Routing")

if __name__ == "__main__":
  app = QApplication(sys.argv)
  window = MainWindow()
  window.show()
  app.exec()