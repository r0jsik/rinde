from rinde.stage.node.box import Box
from rinde.stage.node.box import BoxLayoutComputer


class HBox(Box):
	def __init__(self, nodes=(), align="top", **kwargs):
		super(HBox, self).__init__(nodes, align, **kwargs)
		
		self.style_name = "hbox"
		
		self.__layout_computer = HBoxLayoutComputer(self)
	
	def update_nodes_spacing(self):
		self.__layout_computer.update_nodes_spacing("width", "x")
	
	def update_nodes_align(self):
		self.__layout_computer.update_nodes_align("y")


class HBoxLayoutComputer(BoxLayoutComputer):
	def compute_aligned_position(self, node, align):
		if align == "top":
			return 0
		
		if align == "middle":
			return self.compute_node_center(node, "height")
		
		if align == "bottom":
			return self.get_property("height") - node.get_property("height")
