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

if __name__ == '__main__':
    unittest.main()