class LayoutComputer(object):
	def __init__(self, node):
		self.__node = node
	
	def center_node(self, node):
		self.center_node_vertically(node)
		self.center_node_horizontally(node)
	
	def center_node_horizontally(self, node):
		position = self.compute_node_center(node, "width")
		node.set_property("position_x", position)
	
	def center_node_vertically(self, node):
		position = self.compute_node_center(node, "height")
		node.set_property("position_y", position)
	
	def compute_node_center(self, node, dimension):
		return (self.get_property(dimension) - node.get_property(dimension))/2
	
	def get_property(self, property_name):
		return self.__node.get_property(property_name)


class PaneLayoutComputer(LayoutComputer):
	def __init__(self, pane):
		super(PaneLayoutComputer, self).__init__(pane)
		
		self.__pane = pane
	
	def get_nodes(self):
		return self.__pane.get_nodes()
