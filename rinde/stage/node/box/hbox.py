from rinde.stage.node.box import Box
from rinde.stage.node.box import BoxLayoutComputer


class HBox(Box):
	def __init__(self, **kwargs):
		super(HBox, self).__init__(**kwargs)
		
		self.__layout_computer = HBoxLayoutComputer(self)
		
		self.set_style_name("hbox")
	
	def update_nodes_spacing(self):
		self.__layout_computer.update_nodes_spacing("x", "width", 3, 1)
	
	def update_nodes_align(self):
		self.__layout_computer.update_nodes_align("y")


class HBoxLayoutComputer(BoxLayoutComputer):
	def compute_aligned_position(self, node, align):
		if align == "top":
			return 0
		
		if align == "middle":
			return self.compute_node_center(node, "height")
		
		if align == "bottom":
			return self.node.get_absolute_size("height") - node.get_absolute_size("height")
