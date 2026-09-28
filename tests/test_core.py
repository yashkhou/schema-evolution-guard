import unittest,sys; sys.path.insert(0,'src')
from schema_evolution_guard.core import *
class T(unittest.TestCase):
 def test_required_breaks(self): self.assertTrue(any(x.breaking for x in compare({'type':'object','properties':{'x':{'type':'string'}}},{'type':'object','required':['x'],'properties':{'x':{'type':'string'}}})))
 def test_optional_add_safe(self): self.assertFalse(any(x.breaking for x in compare({'type':'object','properties':{}},{'type':'object','properties':{'x':{'type':'string'}}})))
 def test_enum_narrow_breaks(self): self.assertTrue(any(x.breaking for x in compare({'type':'string','enum':['a','b']},{'type':'string','enum':['a']})))
