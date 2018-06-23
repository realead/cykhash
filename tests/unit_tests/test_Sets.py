import unittest
import uttemplate as uttemplate

from cykhash import Int64Set, Int32Set

@uttemplate.from_templates([Int64Set, Int32Set])
class SetTester(unittest.TestCase): 

   def template_created_empty(self, set_type):
      s=set_type()
      self.assertEqual(len(s), 0)

   def template_add_once(self, set_type):
      s=set_type()
      s.add(1)
      self.assertEqual(len(s), 1)

   def template_add_twice(self, set_type):
      s=set_type()
      s.add(1)
      s.add(1)
      self.assertEqual(len(s), 1)

   def template_add_two(self, set_type):
      s=set_type()
      s.add(1)
      s.add(2)
      self.assertEqual(len(s), 2)

   def template_add_many_twice(self, set_type):
     N=1000
     s=set_type()
     for i in range(N):
       s.add(i)
       self.assertEqual(len(s), i+1)
     #no changes for the second insert:
     for i in range(N):
       s.add(i)
       self.assertEqual(len(s), N)


   def template_contains_none(self, set_type):
     N=1000
     s=set_type()
     for i in range(N):
       self.assertFalse(i in s)


   def template_contains_all(self, set_type):
     N=1000
     s=set_type()
     for i in range(N):
       s.add(i)
     for i in range(N):
       self.assertTrue(i in s)

   def template_contains_odd(self, set_type):
     N=1000
     s=set_type()
     for i in range(N):
       if i%2==1:
        s.add(i)
     for i in range(N):
       self.assertEqual(i in s, i%2==1)

   def template_contains_even(self, set_type):
     N=1000
     s=set_type()
     for i in range(N):
       if i%2==0:
        s.add(i)
     for i in range(N):
       self.assertEqual(i in s, i%2==0)


   def template_delete_even(self, set_type):
     N=1000
     s=set_type()
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
      
