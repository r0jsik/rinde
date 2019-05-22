from rinde.stage.property import SizeProperty
from rinde.stage.property import SpaceProperty


class BoundaryBase(object):
	def __init__(self, node):
		self.node = node


class SpaceBoundary(BoundaryBase):
	def __init__(self, node):
		super(SpaceBoundary, self).__init__(node)
		
		self.__create_space_property("margin")
		self.__create_space_property("padding")
	
	def __create_space_property(self, name):
		self.node.properties.insert(name, SpaceProperty(), self.update_space)
	
	def update_space(self):
		pass
	
	def get_space(self, side_1, side_2):
		return self.node["margin"][side_1] + self.node["padding"][side_1] + self.node["padding"][side_2] + self.node["margin"][side_2]


class PositionBoundary(SpaceBoundary):
	def __init__(self, node, position_x=0, position_y=0):
		super(PositionBoundary, self).__init__(node)
		
		self.__absolute_position = {"x": 0, "y": 0}
		
		self.node.properties.create_number("position-x", self.__update_absolute_position_x, position_x)
		self.node.properties.create_number("position-y", self.__update_absolute_position_y, position_y)
	
	def __update_absolute_position_x(self):
		self.reset_absolute_position("x", 3, 1)
	
	def __update_absolute_position_y(self):
		self.reset_absolute_position("y", 0, 2)
	
	def reset_absolute_position(self, axis, side_1, side_2):
		self.__absolute_position[axis] = self.compute_absolute_position(axis, side_1, side_2)
	
	def compute_absolute_position(self, axis, side_1, side_2):
		return self.__get_parent_origin(axis, side_2) + self.__get_local_origin(axis, side_1)
	
	def __get_parent_origin(self, axis, side):
		parent = self.node.get_parent()
		
		try:
			return parent.get_absolute_position(axis) + parent["padding"][side]
		except AttributeError:
			return 0
	
	def __get_local_origin(self, axis, side):
		return self.node["position-%s" % axis] + self.node["margin"][side]
	
	def update_absolute_position(self):
		self.__update_absolute_position_x()
		self.__update_absolute_position_y()
	
	def absolute_position(self):
		return self.__absolute_position["x"], self.__absolute_position["y"]
	
	def get_absolute_position(self, axis):
		return self.__absolute_position[axis]


class SizeBoundary(SpaceBoundary):
	def __init__(self, node):
		super(SizeBoundary, self).__init__(node)
		
		self.__absolute_size = {"width": 0, "height": 0}
		
		self.__create_size_property()
	
	def __create_size_property(self):
		property = SizeProperty(self.node)
		property.add_trigger(self.update_absolute_size)
	
	def update_absolute_size(self):
		self.reset_absolute_size("width", 3, 1)
		self.reset_absolute_size("height", 0, 2)
		
		parent_boundary = self.node.get_parent_boundary()
		parent_boundary.update()
	
	def reset_absolute_size(self, dimension, side_1, side_2):
		self.__absolute_size[dimension] = self.node["padding"][side_1] + self.node[dimension] + self.node["padding"][side_2]
	
	def absolute_size(self):
		return self.__absolute_size["width"], self.__absolute_size["height"]
	
	def get_absolute_size(self, dimension):
		return self.__absolute_size[dimension]


class Boundary(PositionBoundary, SizeBoundary):
	def reset(self):
		self.reset_absolute_position("x", 3, 1)
		self.reset_absolute_position("y", 0, 2)
		self.reset_absolute_size("width", 3, 1)
		self.reset_absolute_size("height", 0, 2)
	
	def update_space(self):
		self.update_absolute_position()
		self.update_absolute_size()
	
	def is_mouse_over(self, mouse_position):
		if self.get_absolute_size("width") >= mouse_position[0] - self.get_absolute_position("x") >= 0:
			if self.get_absolute_size("height") >= mouse_position[1] - self.get_absolute_position("y") >= 0:
				return True
		
		return False


class ComplexNodeBoundary(Boundary):
	def update(self):
		self.fit_size_to_children(False)
		self.node.update_layout()
		self.fit_size_to_children(True)
	
	def reset_absolute_position(self, axis,side_1, side_2):
		super(ComplexNodeBoundary, self).reset_absolute_position(axis, side_1, side_2)
		
		for child in self.node.children():
			child.boundary.reset_absolute_position(axis, side_1, side_2)
	
	def fit_size_to_children(self, considering_position):
		width = self.__get_max_child_size("x", "width", 3, 1, considering_position)
		height = self.__get_max_child_size("y", "height", 0, 2, considering_position)
		
		self.node["size"] = width, height
	
	def __get_max_child_size(self, axis, dimension, side_1, side_2, considering_position):
		size = 0
		
		for child in self.node.children():
			child_size = self.__compute_size(child, axis, dimension, side_1, side_2, considering_position)
			size = max(child_size, size)
		
		return size
	
	def __compute_size(self, child, axis, dimension, side_1, side_2, considering_position):
		size = child["margin"][side_1] + child.get_absolute_size(dimension) + child["margin"][side_2]
		
		if considering_position:
			return size + child["position-%s" % axis]
		
		return size


class SimpleNodeBoundary(Boundary):
	def compute_absolute_position(self, axis, side_1, side_2):
		return super(SimpleNodeBoundary, self).compute_absolute_position(axis, side_1, side_2) + self.node["padding"][side_1]


class NullBoundary:
	def __getattr__(self, item):
		return lambda *args: 0
