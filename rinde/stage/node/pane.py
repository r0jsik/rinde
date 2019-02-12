from rinde.stage.node import Node
from rinde.stage.node.util.layout import LayoutComputer


class Pane(Node):
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
	
	def remove_node(self, node):
		self._remove_node(node)
		self.update_boundary()
	
	def get_nodes(self):
		return self._get_nodes()


class StackPane(Pane):
	def __init__(self, **kwargs):
		super(StackPane, self).__init__(**kwargs)
		
		self._add_trigger_to_property("width", self.update)
		self._add_trigger_to_property("height", self.update)
		
		self.set_style_name("stack-pane")
		
		self.__layout_computer = LayoutComputer(self)
	
	def update(self):
		for node in self.get_nodes():
			self.__layout_computer.center_node(node)
