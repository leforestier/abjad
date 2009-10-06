class PC(object):
   '''12-ET pitch-class ranging from [0, 12).'''

   def __init__(self, arg):
      if isinstance(arg, (int, long, float)):
         if 0 <= arg < 12:
            self._number = arg
         else:
            raise ValueError
      elif isinstance(arg, PC):
         self._number = arg.number
      else:
         raise TypeError

   ## OVERLOADS ##

   def __add__(self, arg):
      if not isinstance(arg, PC):
         raise TypeError
      new_number = (self.number + arg.number) % 12
      return PC(new_number)
      
   def __eq__(self, arg):
      if not isinstance(arg, PC):
         raise TypeError
      return self.number == arg.number

   def __ge__(self, arg):
      if not isinstance(arg, PC):
         raise TypeError
      return self.number >= arg.number

   def __gt__(self, arg):
      if not isinstance(arg, PC):
         raise TypeError
      return self.number > arg.number

   def __le__(self, arg):
      if not isinstance(arg, PC):
         raise TypeError
      return self.number <= arg.number

   def __lt__(self, arg):
      if not isinstance(arg, PC):
         raise TypeError
      return self.number < arg.number

   def __ne__(self, arg):
      return not self == arg
   
   def __repr__(self):
      return 'PC(%s)' % self.number

   def __sub__(self, arg):
      if not isinstance(arg, PC):
         raise TypeError
      new_number = (self.number - arg.number) % 12
      return PC(new_number)
      
   ## PUBLIC ATTRIBUTES ##

   @property
   def number(self):
      '''Read-only numeric value of pitch-class.'''
      return self._number
