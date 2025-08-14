from abc import ABC
from pprint import pprint

YELLOW_SKILLS = ["Empathy", "Creativity", "Persuasion", "Bravery"]
BLUE_SKILLS = ["Reasoning", "Organization", "Biology", "Engineering"]
RED_SKILLS = ["Toughness", "Perception", "Combat", "Animals"]
CHARACTERS = ["Nomi", "Vace", "Rex", "Anemone", "Cal", "Dys", "Marz", "Tammy", "Tangent"]
ALL_ATTRs = YELLOW_SKILLS + BLUE_SKILLS + RED_SKILLS + CHARACTERS + ["Stress"]

class Stats(ABC):
  """
  Class to hold common functions

  Arguments:
      ABC -- Abstract Base Class
  """
  def __init__(self, *args, **kwargs):
    for attr in ALL_ATTRs:
      setattr(self, attr.lower(), 0)
    for arg in kwargs:
      setattr(self, arg, kwargs[arg])

  def output(self):
    output = ""
    output = f"{output}Stress - {self.stress}"
    for color in [YELLOW_SKILLS, BLUE_SKILLS, RED_SKILLS]:
      for skill in color:
        output = f"{output}\n{skill} - {getattr(self, skill.lower())}"
    for chara in CHARACTERS:
      output = f"{output}\n{chara} - {getattr(self, chara.lower())}"
    return output

  def check_reward(self, skill, state):
    """
    Check if the state should be given an extra point according to matching augment skill

    Arguments:
        skill -- Skill to check
        state -- State object
    """
    if skill in state.rewards:
      return True
    return False

class State(Stats):
  """
  Class to hold the current state and skills

  Arguments:
      Stats -- Abstract class
  """
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.age = 10
    self.month = 1
    self.rewards = []
    self.job_list = [] # [(Activity, threshold_met, prev_stress)] - Makes it easier to undo

  def apply(self, bonus):
    """
    Apply a bonus to the state

    Arguments:
        bonus -- Bonus object
    """
    for attr in ALL_ATTRs:
      attr = attr.lower()
      if getattr(bonus, attr):
        before = getattr(self, attr)
        increase = getattr(bonus, attr)
        new = before + increase
        if attr in self.rewards and increase > 0:
          new += 1
        setattr(self, attr, new)
    
    if "rewards" in dir(bonus):
      self.rewards = bonus.rewards


  def do_job(self, job):
    """
    Apply an activity/job to the state

    Arguments:
        job -- Activity object
    """
    threshold = False
    old_stress = self.stress
    for attr in ALL_ATTRs:
      attr = attr.lower()
      job_value = getattr(job, attr)
      if job_value > 0:
        old = getattr(self, attr)
        new = old + job_value
        if job.check_reward(attr, self):
          if self.rewards == ["stress"]:
            new -= 2
          else:
            new += 1
        if job.check_threshold(attr, self):
          threshold = True
          new += 1
        setattr(self, attr, new)
    self.job_list.append((job, threshold, old_stress))

    if self.month < 13:
      self.month += 1
    elif self.month == 13:
      self.age += 1
      self.month = 1

  def undo_job(self):
    """
    Unapply the last activity/job from the state
    """
    old_job = self.job_list[-1]
    job = old_job[0]
    threshold = old_job[1]
    old_stress = old_job[2]
    for attr in ALL_ATTRs:
      attr = attr.lower()
      if attr == "stress":
        continue # We deal with this later
      else:
        previous = getattr(self, attr)
        decrease = getattr(job, attr)
        if decrease > 0:
          if job.check_reward(attr, self):
            decrease += 1
          if attr == job.primary and threshold:
            decrease += 1
          new = previous - decrease
          setattr(self, attr, new)

    if self.month == 1:
      self.age -= 1
      self.month = 13
    else:
      self.month -= 1
    
    self.stress = old_stress
    self.job_list.pop()

class Bonus(Stats):
  """
  Class to hold bonuses to your stats, normally used during character creation

  Arguments:
      Stats -- Abstract class
  """
  def __init__(self, name, *args, **kwargs):
    super().__init__(*args, **kwargs)

class Activity(Stats):
  """
  Class to hold activities you can do

  Arguments:
      Stats -- Abstract class
  """
  def __init__(self, name, *args, threshold=7, **kwargs):
    self.threshold = threshold
    super().__init__(*args, **kwargs)
  
  def check_threshold(self, skill, state):
    """
    Check if state stat score passes the threshold to receive a bonus point

    Arguments:
        skill -- Skill to check
        state -- State object
    """
    if skill != self.primary:
      return False
    elif getattr(state, skill) > self.threshold:
      return True
    else:
      return False
    




JOBS = {
  "Xenobotany": Activity("Xenobotany", "Geoponics", organization=2, biology=3, stress=10, primary="biology"),
  "Shovelling Dirt": Activity("Shovelling Dirt", "Geoponics", toughness=3, stress=15, primary="toughness", threshold=6),
  "Farming": Activity("Farming", "Geoponics", biology=3, toughness=2, stress=10, primary="biology"),
  "Relax in the Park": Activity("Relax in the Park", "Geoponics", stress=-100),
  "Tending Animals": Activity("Tending Animals", "Geoponics", empathy=2, animals=4, stress=10, primary="animals"),

  "Study Life Sciences": Activity("Study Life Sciences", "Engineering", reasoning=1, biology=3, stress=15, primary="biology", threshold=7),
  "Study Humanities": Activity("Study Humanities", "Engineering", persuasion=2, creativity=2, stress=15, primary="creativity", threshold=8),
  "Study Engineering": Activity("Study Engineering", "Engineering", reasoning=2, engineering=1, stress=15, primary="engineering", threshold=7),
  "Tutoring": Activity("Tutoring", "Engineering", empathy=1, reasoning=4, stress=10, primary="reasoning"),
  "Robot Repair": Activity("Robot Repair", "Engineering", creativity=2, engineering=4, stress=10, primary="engineering"),
  "Rebuild": Activity("Rebuild", "Engineering", organization=3, toughness=4, stress=10, primary="toughness"),
  "Nursing Assistant": Activity("Nursing Assistant", "Engineering", empathy=3, biology=4, stress=15, primary="biology"),
  "Mourn": Activity("Mourn", "Engineering", stress=-100),

  "Sportsball": Activity("Sportsball", "Garrison", bravery=2, toughness=1, stress=10, primary="toughness", threshold=7),
  "Defense Training": Activity("Defense Training", "Garrison", combat=3, animals=1, stress=15, primary="combat"),
  "Lookout Duty": Activity("Lookout Duty", "Garrison", perception=4, animals=1, stress=10, primary="perception"),
  "Guard Duty": Activity("Guard Duty", "Garrison", bravery=2, combat=4, stress=20, primary="combat"),
  "Relax on the Walls": Activity("Relax on the Walls", "Garrison", stress=-100),

  "Sneak Out": Activity("Sneak Out", "Expeditions", bravery=3, perception=1),
  "Explore Nearby": Activity("Explore Nearby", "Expeditions", bravery=3, perception=1),
  "Survey the Plains": Activity("Survey the Plains", "Expeditions", perception=4, animals=1),
  "Forage in the Valley": Activity("Forage in the valley", "Expeditions", biology=2, perception=3),
  "Survey the Ridge": Activity("Survey the Ridge", "Expeditions", engineering=2, perception=3),
  "Explore Glow": Activity("Explore Glow", "Expeditions", bravery=3, perception=1),
  "Hunting the Swamps": Activity("Hunting the Swamps", "Expeditions", combat=2, animals=4),
  
  "Babysitting": Activity("Babysitting", "Living Quarters", empathy=3, creativity=1, stress=10, primary="empathy"),
  "Relax in the Lounge": Activity("Relax in the Lounge", "Living Quarters", stress=-100),
  "Play the Photophonor": Activity("Play the Photophonor", "Living Quarters", creativity=4, bravery=1, stress=5, primary="creativity"),
  "Cooking": Activity("Cooking", "Living Quarters", empathy=2, creativity=3, stress=10, primary="creativity"),
  "Barista": Activity("Barista", "Living Quarters", empathy=4, creativity=3, stress=15, primary="empathy"),
  
  "Deliver Supplies": Activity("Deliver Supplies", "Command", organization=3, perception=1, stress=10),
  "Depot Clerk": Activity("Depot Clerk", "Command", persuasion=2, organization=3, stress=10, primary="organization"),
  "Construction": Activity("Construction", "Command", engineering=4, toughness=2, stress=15, primary="engineering"),
  "Administration": Activity("Administration", "Command", persuasion=4, organization=3, stress=10, primary="persuasion"),
  "Govern": Activity("Govern", "Command", persuasion=4, bravery=3, stress=15, primary="persuasion"),
}

AUGMENTS = {"Eagle Eyes": Bonus("Eagle Eyes", perception=10, rewards=["perception", "animals"]), 
  "Extra Fingers": Bonus("Extra Fingers", creativity=10, rewards=["creativity", "organizing"]), 
  "Absorbent Brain": Bonus("Absorbent Brain", reasoning=10, rewards=["engineering", "biology"]), 
  "Super Strength": Bonus("Super Strength", combat=10, rewards=["toughness", "combat"]), 
  "Calm Temperament": Bonus("Calm Temperament", empathy=10, rewards=["stress"])}

FRIENDS = {"Anemone": Bonus("Anemone", toughness=10, combat=10, anemone=10), 
  "Cal": Bonus("Cal", biology=10, animals=10, cal=10), 
  "Dys": Bonus("Dys", bravery=10, perception=10, dys=10), 
  "Marz": Bonus("Marz", persuasion=10, organization=10, marz=10), 
  "Tammy": Bonus("Tammy", empathy=10, creativity=10, tammy=10), 
  "Tangent": Bonus("Tangent", reasoning=10, engineering=10, tangent=10), 
  "Congruence": Bonus("Conguence", reasoning=10, engineering=10)}

CHARACTERS = ["Nomi", "Vace", "Rex", "Anemone", "Cal", "Dys", "Marz", "Tammy", "Tangent"]

START_ITEMS = {"Eudicot's old hat": Bonus("Eudicot's old hat", persuasion=5), 
  "Gardening Trowel": Bonus("Gardening Trowel", biology=5), 
  "A Sportsball": Bonus("A Sportsball", toughness=5), 
  "Animal book": Bonus("Animal Book", animals=5)}

START_STORIES = {"Futurism": Bonus("Futurism", engineering=5), 
  "Idealism": Bonus("Idealism", combat=5), 
  "Tradition": Bonus("Tradition", creativity=5), 
  "Ship Engineering Manuals": Bonus("Ship Engineering Manuals", engineering=5)}


if __name__ == '__main__':
  state = State()
  print(state.output())