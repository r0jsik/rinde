from rinde.stage.node import Node


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
	
	def get_nodes(self):
		return self._get_nodes()
