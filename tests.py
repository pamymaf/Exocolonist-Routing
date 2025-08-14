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

  def test_apply_complex(self):
    augment = AUGMENTS["Eagle Eyes"]
    friend = FRIENDS["Dys"]
    state = State()
    state.apply(augment)
    self.assertEqual(["perception", "animals"], state.rewards)
    state.apply(friend)
    self.assertEqual(21, state.perception)

  def test_do_job_threshold(self):
    state = State()
    activity = JOBS["Shovelling Dirt"]
    state.do_job(activity)
    self.assertEqual(3, state.toughness)
    self.assertEqual(15, state.stress)
    state.do_job(activity)
    self.assertEqual(6, state.toughness)
    state.do_job(activity)
    self.assertEqual(9, state.toughness)
    state.do_job(activity)
    self.assertEqual(13, state.toughness)
  
  def test_do_job_primary(self):
    state = State()
    activity = JOBS["Shovelling Dirt"]
    state.apply(AUGMENTS["Super Strength"])
    state.do_job(activity)
    self.assertEqual(4, state.toughness)
    self.assertEqual(15, state.stress)

    state = State()
    state.apply(AUGMENTS["Calm Temperament"])
    state.do_job(activity)
    self.assertEqual(13, state.stress)

  def test_do_job_time(self):
    state = State()
    activity = JOBS["Shovelling Dirt"]
    state.do_job(activity)
    self.assertEqual(10, state.age)
    self.assertEqual(2, state.month)

  def test_undo_job_simple(self):
    state = State()
    activity = JOBS["Shovelling Dirt"]
    state.do_job(activity)
    self.assertEqual(3, state.toughness)
    self.assertEqual(15, state.stress)
    state.undo_job()
    self.assertEqual(0, state.toughness)
    self.assertEqual(0, state.stress)

  def test_undo_job_stress(self):
    state = State()
    augment = AUGMENTS["Calm Temperament"]
    activity = JOBS["Shovelling Dirt"]
    state.apply(augment)
    state.do_job(activity)
    self.assertEqual(3, state.toughness)
    self.assertEqual(13, state.stress)
    state.undo_job()
    self.assertEqual(0, state.toughness)
    self.assertEqual(0, state.stress)

  def test_undo_job_primary(self):
    state = State()
    augment = AUGMENTS["Super Strength"]
    activity = JOBS["Shovelling Dirt"]
    state.apply(augment)
    state.do_job(activity)
    self.assertEqual(4, state.toughness)
    self.assertEqual(15, state.stress)
    state.undo_job()
    self.assertEqual(0, state.toughness)
    self.assertEqual(0, state.stress)

  def test_undo_job_threshold(self):
    state = State()
    activity = JOBS["Shovelling Dirt"]
    state.do_job(activity)
    self.assertEqual(3, state.toughness)
    self.assertEqual(15, state.stress)
    state.do_job(activity)
    self.assertEqual(6, state.toughness)
    state.do_job(activity)
    self.assertEqual(9, state.toughness)
    state.do_job(activity)
    self.assertEqual(13, state.toughness)
    state.undo_job()
    self.assertEqual(9, state.toughness)

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
  
  def test_check_reward(self):
    activity = JOBS["Xenobotany"]
    bonus = AUGMENTS["Super Strength"]
    state = State()
    state.apply(bonus)
    result = activity.check_reward("toughness", state)
    self.assertEqual(True, result)

  def test_check_threshold(self):
    activity = JOBS["Shovelling Dirt"] # toughness threshold of 6
    state = State()
    state.toughness = 5
    self.assertEqual(False, activity.check_threshold("toughness", state))
    state.toughness = 6
    self.assertEqual(False, activity.check_threshold("toughness", state))
    state.toughness = 7
    self.assertEqual(True, activity.check_threshold("toughness", state))
    state.biology = 7
    self.assertEqual(False, activity.check_threshold("biology", state))
    

if __name__ == '__main__':
    unittest.main()