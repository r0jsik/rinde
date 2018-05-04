from rinde.scene.node.box import Box
from rinde.scene.node.box import BoxLayoutComputer


class VBox(Box):
	def __init__(self, nodes=(), align="left", **kwargs):
		super(VBox, self).__init__(nodes, align, **kwargs)
		
		self.style_name = "vbox"
		
		self.__layout_computer = VBoxLayoutComputer(self)
	
	def _update_nodes_spacing(self):
		self.__layout_computer.update_nodes_spacing("height", "y")
	
	def _update_nodes_align(self):
		self.__layout_computer.update_nodes_align("x")


class VBoxLayoutComputer(BoxLayoutComputer):
	def _compute_aligned_position(self, node, align):
		if align == "left":
			return 0
		
		if align == "center":
			return self._compute_node_center(node, "width")
		
		if align == "right":
			return self._get_container_property("width") - node.get_property("width")
