from rinde.stage.node.pane import Pane
from rinde.stage.node.util.layout import PaneLayoutComputer


class Box(Pane):
	def __init__(self, nodes, align, spacing=0, **kwargs):
		super(Box, self).__init__(nodes, **kwargs)
		
		self.properties.create_number("spacing", self.update_nodes_spacing, spacing)
		self.properties.create("align", self.update_nodes_align, align)
	
	def update_nodes_spacing(self):
		pass
	
	def update_nodes_align(self):
		pass
	
	def update_layout(self):
		self.update_nodes_spacing()
		self.update_nodes_align()


class BoxLayoutComputer(PaneLayoutComputer):
	def update_nodes_spacing(self, axis, dimension, side_1, side_2):
		spacing = self.node["spacing"]
		position = 0
		
		for node in self.get_nodes():
			node["position-%s" % axis] = position
			position += node["margin"][side_1] + node.get_absolute_size(dimension) + node["margin"][side_2] + spacing
	
	def update_nodes_align(self, axis):
		align = self.node["align"]
		
		for node in self.get_nodes():
			node["position-%s" % axis] = self.__get_aligned_position(node, align)
	
	def __get_aligned_position(self, node, align):
		position = self.compute_aligned_position(node, align)
		
		if position is None:
			raise ValueError("Unknown alignment: '%s'" % align)
		
		return position
	
	def compute_aligned_position(self, node, align):
		return 0
