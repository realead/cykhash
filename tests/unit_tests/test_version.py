import unittest

import cykhash


class VersionTester(unittest.TestCase): 

   def test_major(self):
      self.assertEqual(cykhash.__version__[0], 0)

   def test_minor(self):
      self.assertEqual(cykhash.__version__[1], 2)

   def test_last(self):
      self.assertEqual(cykhash.__version__[2], 0)
