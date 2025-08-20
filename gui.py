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
    self.choice_area = QVBoxLayout()
    self.choice_display = QLabel("")
    self.choice_info = QLabel("")
    self.confirm_button = QPushButton("")
    self.choice_buttons = {}


    #SECTION Jobs area
    self.job_area = QHBoxLayout()
    self.job_locations_areas = {}
    self.job_buttons = {}


    #SECTION Setup
    self.wrapper.addLayout(self.menu_area, 0, 0)
    self.wrapper.addLayout(self.stats_area, 1, 0)
    self.wrapper.addLayout(self.choice_area, 1, 1)
    widget = QWidget()
    widget.setLayout(self.wrapper)
    self.setCentralWidget(widget)

    self.ask("What augment do you choose?", AUGMENTS)

  def reset(self):
    """
    Reset state and gui
    """
    self.refresh_stats()

  def clear_choice_buttons(self):
    """
    Delete all buttons in the choices area
    """
    for choice in self.choice_buttons:
      button = self.choice_buttons[choice]
      self.choice_area.removeWidget(button)
    self.choice_buttons = {}
    self.clear_choice_display()

  def clear_choice_display(self):
    """
    Clear the choice display, extra info display, and confirm button
    """
    self.choice_area.removeWidget(self.choice_display)
    self.choice_area.removeWidget(self.choice_info)
    self.choice_area.removeWidget(self.confirm_button)
    self.choice_display = QLabel("")
    self.choice_info = QLabel("")
    self.confirm_button = QPushButton("")

  def refresh_choice_display(self, choice):
    """
    Refresh the choice display and choice info

    Arguments:
        choice -- Choice to display
        extra -- Extra info about the choice to display
    """
    self.clear_choice_display()

    extra = ""
    if choice in ALL_BONUSES:
      attrs = dir(ALL_BONUSES[choice])
      for attr in attrs:
        value = getattr(ALL_BONUSES[choice], attr)
        if not attr.startswith("_") and (isinstance(value, list) or (isinstance(value, int) and value > 0)) and attr != "name":
          extra = f"{extra}{attr} - {value}\n"
    elif choice in JOBS:
      job = JOBS[choice]
      for attr in dir(job):
        if not attr.startswith("_") and isinstance(getattr(job, attr), int) and attr != "threshold":
          value = getattr(job, attr)
          if getattr(job, attr) != 0:
            before = getattr(self.state, attr)
            increase = getattr(job, attr)
            if attr != "stress":
              if job.check_threshold(attr, self.state):
                increase += 1
              if job.check_reward(attr, self.state):
                increase += 1
            elif attr == "stress" and job.check_reward(attr, self.state) and job.stress != -100:
              increase -= 2
            if increase != 0:
              extra = f"{extra}{attr} - {increase}\n"
    elif choice in ["1st playthrough", "2nd+ playthrough", "Yes", "No"]:
      extra = ""
    elif choice == "":
      choice = ""
      extra = ""
    elif choice == "stressed":
      choice = "You are too stressed for that"
      extra = "Please rest"
    else:
      choice = "INVALID"
      extra = "Choice invalid"

    self.choice_display = QLabel(choice)
    self.choice_info = QLabel(extra)
    self.confirm_button = QPushButton("Confirm")
    self.confirm_button.clicked.connect(self.confirm)

    self.choice_area.addWidget(self.choice_display)
    self.choice_area.addWidget(self.choice_info)
    self.choice_area.addWidget(self.confirm_button)


  def undo_job(self):
    """
    Undo the last job
    """
    self.state.undo_job()
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

  def populate_jobs(self):
    """
    Make a button for each job
    """
    self.clear_choice_buttons()
    self.clear_choice_display()
    self.choice_display = QLabel("What job would you like to do?")
    self.choice_area.addWidget(self.choice_display)
    
    for job in JOBS:
      job = JOBS[job]
      if not job.location in self.job_locations_areas:
        self.job_locations_areas[job.location] = QVBoxLayout()
        self.job_buttons[job.location] = []
        location_area = self.job_locations_areas[job.location]
        location_label = QLabel(job.location, alignment=Qt.AlignmentFlag.AlignTop)
        location_area.addWidget(location_label)
        self.job_buttons[job.location].append(location_label)
      location_area = self.job_locations_areas[job.location]
      button = QPushButton(job.name)
      button.clicked.connect(self.select)
      location_area.addWidget(button)
      self.job_buttons[job.location].append(button)

    for location in self.job_locations_areas:
      location_area = self.job_locations_areas[location]
      
      self.job_area.addLayout(location_area)
    self.wrapper.addWidget(self.undo_button,0,1)
    self.wrapper.addLayout(self.job_area, 1,2)

  def ask(self, question, choices):
    """
    Ask a question and make a button for each choice

    Arguments:
        question -- Question to ask
        choices -- List of choices
    """
    self.clear_choice_buttons()
    self.clear_choice_display()
    for choice in choices:
      button = QPushButton(choice)
      button.clicked.connect(self.select)
      self.choice_buttons[choice] = button
      self.choice_area.addWidget(button)
    self.choice_display = QLabel(question)
    self.choice_area.addWidget(self.choice_display)
  
  def select(self):
    """
    Capture the user's choice and update the confirmation display
    """
    choice = self.sender().text()
    self.refresh_choice_display(choice)

  def confirm(self):
    """
    Apply the user's selection
    """
    choice = self.choice_display.text()
    print(choice)
    if choice in AUGMENTS:
      self.state.apply(AUGMENTS[choice])
      self.ask("Who is your bestest friend?", FRIENDS)
    elif choice in FRIENDS:
      self.state.apply(FRIENDS[choice])
      self.ask("Is this the first playthrough?", ["1st playthrough", "2nd+ playthrough"])
    elif choice == "1st playthrough":
      self.populate_jobs()
    elif choice == "2nd+ playthrough":
      self.ask("What is your favorite bedtime story?", START_STORIES)
    elif choice in START_STORIES:
      self.state.apply(START_STORIES[choice])
      self.ask("What is your favorite item?", START_ITEMS)
    elif choice in START_ITEMS:
      self.populate_jobs()
    elif choice in JOBS:
      if self.state.stress >= 100 and JOBS[choice].stress != -100:
        self.refresh_choice_display("stressed")
      else:
        self.state.do_job(JOBS[choice])
        self.refresh_choice_display(choice)
    self.refresh_stats()
    


if __name__ == "__main__":
  app = QApplication(sys.argv)
  window = MainWindow()
  window.show()
  app.exec()