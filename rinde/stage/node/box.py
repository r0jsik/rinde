from rinde.stage.node.pane import Pane
from rinde.stage.node.util import LayoutComputer


class Box(Pane):
	def __init__(self, **kwargs):
		super(Box, self).__init__(**kwargs)
		
		self.properties.create_number("spacing", self.update_nodes_spacing)
		self.properties.create("align", self.update_nodes_align)
	
	def update_nodes_spacing(self):
		raise NotImplementedError
	
	def update_nodes_align(self):
		raise NotImplementedError
	
	def update_layout(self):
		self.update_nodes_spacing()
		self.update_nodes_align()


class BoxLayoutComputer(LayoutComputer):
	def update_nodes_spacing(self, axis, dimension, side_1, side_2):
		spacing = self.node["spacing"]
		position = 0
		
		for node in self.node.children():
			node["position-%s" % axis] = position
			position += node["margin"][side_1] + node.get_absolute_size(dimension) + node["margin"][side_2] + spacing
	
	def update_nodes_align(self, axis):
		align = self.node["align"]
		
		for node in self.node.children():
			node["position-%s" % axis] = self.__get_aligned_position(node, align)
	
	def __get_aligned_position(self, node, align):
		position = self.compute_aligned_position(node, align)
		
		if position is None:
			raise ValueError("Unknown alignment: '%s'" % align)
		
		return position
	
	def compute_aligned_position(self, node, align):
		raise NotImplementedError


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


class VBox(Box):
	def __init__(self, **kwargs):
		super(VBox, self).__init__(**kwargs)
		
		self.__layout_computer = VBoxLayoutComputer(self)
		
		self.set_style_name("vbox")
	
	def update_nodes_spacing(self):
		self.__layout_computer.update_nodes_spacing("y", "height", 0, 2)
	
	def update_nodes_align(self):
		self.__layout_computer.update_nodes_align("x")


class VBoxLayoutComputer(BoxLayoutComputer):
	def compute_aligned_position(self, node, align):
		if align == "left":
			return 0
		
		if align == "center":
			return self.compute_node_center(node, "width")
		
		if align == "right":
			return self.node.get_absolute_size("width") - node.get_absolute_size("width")
