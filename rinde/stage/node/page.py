from rinde.stage.node import ComplexNode
from rinde.stage.node.pane import Pane


class Pages(ComplexNode):
	def __init__(self, children, group, select=None, **kwargs):
		super(Pages, self).__init__(**kwargs)
		
		self.__group = group
		
		for child in children:
			self.insert_page(child)
		
		self.__group.select(select)
		
		self.set_style_name("pages")
	
	def insert_page(self, page):
		if isinstance(page, Page):
			page.insert_to(self.__group)
		else:
			raise TypeError("Pages' child must be an instance of rinde.stage.node.page.Page")
		
		self._insert_node(page)
	
	def remove_page(self, name):
		page = self.__group.get_item_by_name(name)
		
		self.__group.remove(name)
		self._remove_node(page)


class Page(Pane):
	def __init__(self, name, **kwargs):
		super(Page, self).__init__(**kwargs)
		
		self.__name = name
		
		self.set_style_name("page")
	
	def set_selected(self, value):
		self["visible"] = value
	
	def is_selected(self):
		return self["visible"]
	
	def insert_to(self, group):
		group.insert(self, self.__name)
