from rinde.stage.node.pane import Pane
from rinde.stage.node.util import PaneLayoutComputer
from rinde.error import RindeException


class Box(Pane):
	def __init__(self, nodes, align, spacing=0, **kwargs):
		super(Box, self).__init__(nodes, **kwargs)
		
		self._property["spacing"] = self._create_property(self._update_nodes_spacing, spacing)
		self._property["align"] = self._create_property(self._update_nodes_align, align)
	
	def _update_nodes_spacing(self):
		pass
	
	def _update_nodes_align(self):
		pass
	
	def update(self):
		self._update_nodes_spacing()
		self._update_nodes_align()


class BoxLayoutComputer(PaneLayoutComputer):
	def update_nodes_spacing(self, dimension, axis):
		spacing = self.get_property("spacing")
		position = 0
		
		for node in self.get_nodes():
			property = node.property("position_%s" % axis)
			property.set(position)
			position += node.get_property(dimension) + spacing
	
	def update_nodes_align(self, axis):
		align = self.get_property("align")
		
		for node in self.get_nodes():
			property = node.property("position_%s" % axis)
			position = self.__get_aligned_position(node, align)
			property.set(position)
	
	def __get_aligned_position(self, node, align):
		position = self._compute_aligned_position(node, align)
		
		if position is None:
			raise RindeException("Unknown alignment: '%s'" % align)
		
		return position
	
	def _compute_aligned_position(self, node, align):
		return 0
