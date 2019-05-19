class LayoutComputer(object):
	def __init__(self, node):
		self.node = node
	
	def center_node(self, node):
		self.center_node_horizontally(node)
		self.center_node_vertically(node)
	
	def center_node_horizontally(self, node):
		node["position-x"] = self.compute_node_center(node, "width")
	
	def center_node_vertically(self, node):
		node["position-y"] = self.compute_node_center(node, "height")
	
	def compute_node_center(self, node, dimension):
		return (self.node.get_absolute_size(dimension) - node.get_absolute_size(dimension))/2
