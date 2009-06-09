from abjad import *
import py.test


def test_mathtools_sums_01( ):
   '''Return list of the cumulative sums of the integer elements in input.'''

   assert mathtools.sums([1, 2, 3]) == [1, 3, 6]
   assert mathtools.sums([10, -9, -8]) == [10, 1, -7]
   assert mathtools.sums([0, 0, 0, 5]) == [0, 0, 0, 5]
   assert mathtools.sums([-10, 10, -10, 10]) == [-10, 0, -10, 0]


def test_mathtools_sums_02( ):
   '''Raise TypeError when l is neither tuple nor list.
      Raise ValueError when l is empty.'''

   assert py.test.raises(TypeError, "mathtools.products('foo')")
   assert py.test.raises(ValueError, 'mathtools.products([ ])')
