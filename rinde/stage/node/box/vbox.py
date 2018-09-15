from rinde.stage.node.box import Box
from rinde.stage.node.box import BoxLayoutComputer


class VBox(Box):
	def __init__(self, nodes=(), align="left", **kwargs):
		super(VBox, self).__init__(nodes, align, **kwargs)
		
		self.set_style_name("vbox")
		
		self.__layout_computer = VBoxLayoutComputer(self)
	
	def update_nodes_spacing(self):
		self.__layout_computer.update_nodes_spacing("height", "y")
	
	def update_nodes_align(self):
		self.__layout_computer.update_nodes_align("x")


class VBoxLayoutComputer(BoxLayoutComputer):
	def compute_aligned_position(self, node, align):
		if align == "left":
			return 0
		
		if align == "center":
			return self.compute_node_center(node, "width")
		
		if align == "right":
			return self.get_property("width") - node.get_property("width")
