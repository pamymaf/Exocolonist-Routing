from router import *
import unittest

class TestStats(unittest.TestCase):
  def test_init(self):
    stats = Stats()
    for attr in ALL_ATTRs:
      self.assertEqual(0, getattr(stats, attr.lower()))

class TestState(unittest.TestCase):
  def test_init(self):
    state = State()
    for attr in ALL_ATTRs:
      self.assertEqual(0, getattr(state, attr.lower()))

  def test_apply(self):
    bonus = FRIENDS["Cal"]
    state = State()
    state.apply(bonus)
    self.assertEqual(10, state.biology)
    self.assertEqual(10, state.animals)
    self.assertEqual(10, state.cal)

    bonus = AUGMENTS["Eagle Eyes"]
    state = State()
    state.apply(bonus)
    self.assertEqual(state.rewards, ["perception", "animals"])

    bonus = START_STORIES["Futurism"]
    state = State()
    state.apply(bonus)
    self.assertEqual(5, state.engineering)

    bonus = START_ITEMS["Eudicot's old hat"]
    state = State()
    state.apply(bonus)
    self.assertEqual(5, state.persuasion)

class TestBonus(unittest.TestCase):
  def test_init(self):
    bonus = Bonus(name="Test")
    for attr in ALL_ATTRs:
      self.assertEqual(0, getattr(bonus, attr.lower()))

class TestActivity(unittest.TestCase):
  def test_init(self):
    activity = Activity(name="Test")
    for attr in ALL_ATTRs:
      self.assertEqual(0, getattr(activity, attr.lower()))
  
  def test_check_primary(self):
    activity = JOBS["Xenobotany"]
    bonus = AUGMENTS["Super Strength"]
    state = State()
    state.apply(bonus)
    result = activity.check_primary("toughness", state)
    self.assertEqual(True, result)
    

if __name__ == '__main__':
    unittest.main()