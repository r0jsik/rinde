from rinde.stage.node import ComplexNode
from rinde.stage.node.util.layout import LayoutComputer


class Pane(ComplexNode):
	def __init__(self, nodes=(), **kwargs):
		super(Pane, self).__init__(**kwargs)
		
		for node in nodes:
			self._insert_node(node)
		
		self.set_style_name("pane")
	
	def get_hovered_node(self, mouse_position):
		hovered_node = self
		
		for node in self.get_nodes():
			if node.can_be_hovered(mouse_position):
				hovered_node = node.get_hovered_node(mouse_position)
		
		return hovered_node
	
	def insert_node(self, node):
		self._insert_node(node)
		node.reset()
		self.update_layout()
	
	def remove_node(self, node):
		self._remove_node(node)
		self.update_layout()
	
	def get_nodes(self):
		return self.children()


class StackPane(Pane):
	def __init__(self, **kwargs):
		super(StackPane, self).__init__(**kwargs)
		
		self.__layout_computer = LayoutComputer(self)
		
		self.set_style_name("stack-pane")
	
	def update_layout(self):
		for node in self.get_nodes():
			self.__layout_computer.center_node(node)
