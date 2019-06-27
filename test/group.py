import unittest

from rinde.stage.node.util import Group


class GroupTest(unittest.TestCase):
	def test_empty_group(self):
		group = Group()
		
		assert group.get_selected_name() is None
		assert group.get_selected_item() is None
	
	def test_insert_unselected(self):
		item = MockItem(False)
		
		group = Group()
		group.insert(item, "item")
		
		assert group.get_selected_item() is None
	
	def test_insert_selected(self):
		item = MockItem(True)
		
		group = Group()
		group.insert(item, "item")
		
		assert group == "item"
	
	def test_insert_selected_then_unselected(self):
		item_1 = MockItem(True)
		item_2 = MockItem(False)
		
		group = Group()
		group.insert(item_1, "item_1")
		group.insert(item_2, "item_2")
		
		assert group == "item_1"
	
	def test_insert_unselected_then_selected(self):
		item_1 = MockItem(False)
		item_2 = MockItem(True)
		
		group = Group()
		group.insert(item_1, "item_1")
		group.insert(item_2, "item_2")
		
		assert group == "item_2"
	
	def test_select(self):
		item_1 = MockItem(False)
		item_2 = MockItem(False)
		
		group = Group()
		group.insert(item_1, "item_1")
		group.insert(item_2, "item_2")
		group.select("item_1")
		
		assert group == "item_1"
		assert item_1.is_selected()
		assert not item_2.is_selected()
		
		group.select("item_2")
		
		assert group == "item_2"
		assert not item_1.is_selected()
		assert item_2.is_selected()
	
	def test_remove(self):
		item = MockItem(True)
		
		group = Group()
		group.insert(item, "item")
		group.remove("item")
		
		assert group.get_selected_item() is None
	
	def test_get_item(self):
		item_1 = MockItem(True)
		item_2 = MockItem(False)
		
		group = Group()
		group.insert(item_1, "item_1")
		group.insert(item_2, "item_2")
		
		assert group.get_selected_item() == item_1
		
		group.select("item_2")
		
		assert group.get_selected_item() == item_2
	
	def test_select_not_existing_item(self):
		group = Group()
		
		with self.assertRaises(KeyError):
			group.select("unknown")


class MockItem:
	def __init__(self, selected):
		self.__selected = selected
	
	def set_selected(self, value):
		self.__selected = value
	
	def is_selected(self):
		return self.__selected
