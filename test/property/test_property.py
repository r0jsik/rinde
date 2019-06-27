import unittest

from rinde.property import Property
from rinde.property import SpaceProperty
from rinde.property import TupleProperty


class PropertyTest(unittest.TestCase):
	def test_bind_to(self):
		property_1 = Property("correct")
		property_2 = Property()
		property_2.bind_to(property_1)
		
		assert property_2.get() == "correct"
	
	def test_bound_property_update(self):
		property_1 = Property()
		property_2 = Property()
		property_2.bind_to(property_1)
		
		property_1.reset("correct reset")
		assert property_2.get() == "correct reset"
		
		property_1.set("correct set")
		assert property_2.get() == "correct set"
	
	def test_unbind(self):
		property_1 = Property("correct")
		property_2 = Property()
		
		property_2.bind_to(property_1)
		property_2.unbind()
		property_1.set("error")
		
		assert property_2.get() != "error"
	
	def test_triggering(self):
		property_1 = Property()
		property_2 = Property()
		property_3 = Property()
		
		property_2.add_trigger(lambda: property_3.set("triggered"))
		property_2.bind_to(property_1)
		property_1.set("correct")
		
		assert property_3.get() == "triggered"
		
		property_3.set("not triggered")
		property_2.unbind()
		property_1.set("error")
		
		assert property_3.get() == "not triggered"
	
	def test_triggering_on_setting_the_same_value(self):
		property_1 = Property("value")
		property_2 = Property()
		
		property_1.add_trigger(lambda: property_2.set("triggered"))
		property_1.set("value")
		
		assert property_2.get() != "triggered"


class SpacePropertyTest(unittest.TestCase):
	def test_set(self):
		property = SpaceProperty()
		property.set("1")
		
		assert property.get() == (1, 1, 1, 1)
		
		property.set((2, 3))
		
		assert property.get() == (2, 3, 2, 3)
		
		property.set("1 2 3")
		
		assert property.get() == (1, 2, 3, 2)
		
		property.set((4, 3, 2, 1))
		
		assert property.get() == (4, 3, 2, 1)
	
	def test_reset(self):
		property = SpaceProperty()
		property.reset(1)
		
		assert property.get() == (1, 1, 1, 1)
		
		property.reset("2 3")
		
		assert property.get() == (2, 3, 2, 3)
		
		property.reset((1, 2, 3))
		
		assert property.get() == (1, 2, 3, 2)
		
		property.reset("4 3 2 1")
		
		assert property.get() == (4, 3, 2, 1)
	
	def test_invalid_value(self):
		property = SpaceProperty()
		
		with self.assertRaises(ValueError):
			property.set("a b c")
		
		with self.assertRaises(ValueError):
			property.set((1, 2, 3, 4, 5))
		
		with self.assertRaises(TypeError):
			property.set(None)
	
	def test_sides(self):
		property = SpaceProperty()
		property.set((1, 2, 3, 4))
		
		assert property[0] == 1
		assert property[3] == 4
		
		property[2] = 8
		
		assert property.get() == (1, 2, 8, 4)
		
		with self.assertRaises(IndexError):
			property[256] = 8


class TuplePropertyTest(unittest.TestCase):
	def test_append(self):
		property = TupleProperty((1, 2, 3))
		property.append(4)
		
		assert property.get() == (1, 2, 3, 4)
	
	def test_insert(self):
		property = TupleProperty((1, 2, 4))
		property.insert(3, 2)
		
		assert property.get() == (1, 2, 3, 4)
	
	def test_remove(self):
		property = TupleProperty((1, 2, 8, 3))
		property.remove(8)
		
		assert property.get() == (1, 2, 3)
	
	def test_binding(self):
		property_1 = TupleProperty((1, 2, 3))
		property_2 = TupleProperty()
		
		property_2.bind_to(property_1)
		property_1.append(4)
		
		assert property_2.get() == (1, 2, 3, 4)
		
		property_1.set((4, 5, 6))
		
		assert property_2.get() == (4, 5, 6)
