import unittest

from cykhash import Int64Set


class Int64Tester(unittest.TestCase): 

   def test_created_empty(self):
      s=Int64Set()

   def test_add_once(self):
      s=Int64Set()
      s.add(1)
      self.assertEqual(len(s), 1)

   def test_add_twice(self):
      s=Int64Set()
      s.add(1)
      s.add(1)
      self.assertEqual(len(s), 1)

   def test_add_two(self):
      s=Int64Set()
      s.add(1)
      s.add(2)
      self.assertEqual(len(s), 2)

   def test_add_many_twice(self):
     N=1000
     s=Int64Set()
     for i in range(N):
       s.add(i)
       self.assertEqual(len(s), i+1)
     #no changes for the second insert:
     for i in range(N):
       s.add(i)
       self.assertEqual(len(s), N)


   def test_contains_none(self):
     N=1000
     s=Int64Set()
     for i in range(N):
       self.assertFalse(i in s)


   def test_contains_all(self):
     N=1000
     s=Int64Set()
     for i in range(N):
       s.add(i)
     for i in range(N):
       self.assertTrue(i in s)

   def test_contains_odd(self):
     N=1000
     s=Int64Set()
     for i in range(N):
       if i%2==1:
        s.add(i)
     for i in range(N):
       self.assertEqual(i in s, i%2==1)

   def test_contains_even(self):
     N=1000
     s=Int64Set()
     for i in range(N):
       if i%2==0:
        s.add(i)
     for i in range(N):
       self.assertEqual(i in s, i%2==0)


   def test_delete_even(self):
     N=1000
     s=Int64Set()
     for i in range(N):
       s.add(i)
 
     #delete even:
     for i in range(N):
       if i%2==0:
          n=len(s)
          s.discard(i)
          self.assertEqual(len(s), n-1)
          s.discard(i)
          self.assertEqual(len(s), n-1)

     #check odd is still inside:
     for i in range(N):
        self.assertEqual(i in s, i%2==1)
      
