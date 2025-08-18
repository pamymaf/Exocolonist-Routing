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

    self.state = State()

    self.wrapper = QGridLayout()


    #SECTION Menu area
    self.menu_area = QHBoxLayout()
    
    self.reset_button = QPushButton("Reset")
    self.reset_button.clicked.connect(self.reset)
    self.menu_area.addWidget(self.reset_button)

    self.undo_button = QPushButton("Undo")
    self.undo_button.clicked.connect(self.undo_job)
    # We will add this later when it's relevant


    #SECTION Stats area
    self.stats_area = QVBoxLayout()
    self.stats_labels = []

    self.refresh_stats()
    
    
    #SECTION Choice area
    self.choice_area = QHBoxLayout()


    #SECTION Setup
    self.wrapper.addLayout(self.menu_area, 0, 0)
    self.wrapper.addLayout(self.stats_area, 1, 0)
    widget = QWidget()
    widget.setLayout(self.wrapper)
    self.setCentralWidget(widget)

  def reset(self):
    """
    Reset state and gui
    """
    self.refresh_stats()

  def undo_job(self):
    """
    Undo the last job
    """
    self.refresh_stats()

  def refresh_stats(self):
    """
    Refresh and draw current stats
    """
    for stat in self.stats_labels:
      stat.deleteLater()
    self.stats_labels = []

    for stat in ["Stress"] + YELLOW_SKILLS + BLUE_SKILLS + RED_SKILLS:
      label = QLabel(f"{stat} - {getattr(self.state, stat.lower())}")
      self.stats_labels.append(label)
      self.stats_area.addWidget(label)
    
    label = QLabel(f"----------")
    self.stats_labels.append(label)
    self.stats_area.addWidget(label)

    for chara in CHARACTERS:
      label = QLabel(f"{chara} - {getattr(self.state, chara.lower())}")
      self.stats_labels.append(label)
      self.stats_area.addWidget(label)

if __name__ == "__main__":
  app = QApplication(sys.argv)
  window = MainWindow()
  window.show()
  app.exec()