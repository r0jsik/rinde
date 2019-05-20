from rinde.stage.node import ComplexNode
from rinde.stage.node.util.layout import LayoutComputer


class Pane(ComplexNode):
	def __init__(self, children=(), **kwargs):
		super(Pane, self).__init__(**kwargs)
		
		for node in children:
			self._insert_node(node)
		
		self.set_style_name("pane")
	
	def get_hovered_node(self, mouse_position):
		hovered_node = self
		
		for node in self.children():
			if node.can_be_hovered(mouse_position):
				hovered_node = node.get_hovered_node(mouse_position)
		
		return hovered_node
	
	def insert_node(self, node, index=None):
		self._insert_node(node, index)
		node.reset()
		self.update_layout()
	
	def remove_node(self, node):
		self._remove_node(node)
		self.update_layout()


class StackPane(Pane):
	def __init__(self, **kwargs):
		super(StackPane, self).__init__(**kwargs)
		
		self.__layout_computer = LayoutComputer(self)
		
		self.set_style_name("stack-pane")
	
	def update_layout(self):
		for node in self.children():
			self.__layout_computer.center_node(node)
