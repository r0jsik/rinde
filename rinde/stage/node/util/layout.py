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
		return (self.node[dimension] - node[dimension])/2


class PaneLayoutComputer(LayoutComputer):
	def __init__(self, pane):
		super(PaneLayoutComputer, self).__init__(pane)
		
		self.__pane = pane
	
	def get_nodes(self):
		return self.__pane.get_nodes()
