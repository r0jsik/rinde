from rinde.error import RindeException
from rinde.stage.node.pane import Pane
from rinde.stage.node.util.layout import PaneLayoutComputer


class Box(Pane):
	def __init__(self, nodes, align, spacing=0, **kwargs):
		super(Box, self).__init__(nodes, **kwargs)
		
		self.properties.create_integer("spacing", self.update_nodes_spacing, spacing)
		self.properties.create("align", self.update_nodes_align, align)
	
	def update_nodes_spacing(self):
		pass
	
	def update_nodes_align(self):
		pass
	
	def update(self):
		self.update_nodes_spacing()
		self.update_nodes_align()


class BoxLayoutComputer(PaneLayoutComputer):
	def update_nodes_spacing(self, dimension, axis):
		spacing = self.get_property("spacing")
		position = 0
		
		for node in self.get_nodes():
			property = node.properties["position-%s" % axis]
			property.set(position)
			position += node.get_property(dimension) + spacing
	
	def update_nodes_align(self, axis):
		align = self.get_property("align")
		
		for node in self.get_nodes():
			property = node.properties["position-%s" % axis]
			position = self.__get_aligned_position(node, align)
			property.set(position)
	
	def __get_aligned_position(self, node, align):
		position = self.compute_aligned_position(node, align)
		
		if position is None:
			raise RindeException("Unknown alignment: '%s'" % align)
		
		return position
	
	def compute_aligned_position(self, node, align):
		return 0
