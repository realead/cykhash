from unittestmock import UnitTestMock

import cykhash


class TestVersion(UnitTestMock): 

   def test_major(self):
      self.assertEqual(cykhash.__version__[0], 2)

   def test_minor(self):
      self.assertEqual(cykhash.__version__[1], 0)

   def test_last(self):
      self.assertEqual(cykhash.__version__[2], 1)
