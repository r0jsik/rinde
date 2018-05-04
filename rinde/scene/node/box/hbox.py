from rinde.scene.node.box import Box
from rinde.scene.node.box import BoxLayoutComputer


class HBox(Box):
	def __init__(self, nodes=(), align="top", **kwargs):
		super(HBox, self).__init__(nodes, align, **kwargs)
		
		self.style_name = "hbox"
		
		self.__layout_computer = HBoxLayoutComputer(self)
	
	def _update_nodes_spacing(self):
		self.__layout_computer.update_nodes_spacing("width", "x")
	
	def _update_nodes_align(self):
		self.__layout_computer.update_nodes_align("y")


class HBoxLayoutComputer(BoxLayoutComputer):
	def _compute_aligned_position(self, node, align):
		if align == "top":
			return 0
		
		if align == "middle":
			return self._compute_node_center(node, "height")
		
		if align == "bottom":
			return self._get_container_property("height") - node.get_property("height")
