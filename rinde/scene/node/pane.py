from rinde.scene.node import Node


class Pane(Node):
	def __init__(self, nodes=(), **kwargs):
		super(Pane, self).__init__(**kwargs)
		
		self._property["margin"] = self._boundary.margin()
		self._property["padding"] = self._boundary.padding()
		
		self.style_name = "pane"
		
		map(self._insert_node, nodes)
	
	def get_hovered_node(self, mouse_position):
		hovered_node = self
		
		for node in self.get_nodes():
			if node.can_be_hovered(mouse_position):
				hovered_node = node.get_hovered_node(mouse_position)
		
		return hovered_node
	
	def insert_node(self, node):
		self._insert_node(node)
		
		if self._parent:
			self._parent.insert_to_scene(node)
	
	def get_nodes(self):
		return self._nodes
