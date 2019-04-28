from rinde.stage.property import SpaceProperty


class BoundaryBase(object):
	def __init__(self, node):
		self.node = node
	
	def update_parent(self, axis, dimension, side_1, side_2):
		parent = self.get_parent_boundary()
		parent.update_size(axis, dimension, side_1, side_2)
		parent.update_layout()
	
	def update_layout(self):
		self.node.update_layout()
	
	def get_parent_boundary(self):
		return self.node.get_parent_boundary() or NullBoundary()


class SpaceBoundary(BoundaryBase):
	def __init__(self, node):
		super(SpaceBoundary, self).__init__(node)
		
		self.__create_space_property("margin")
		self.__create_space_property("padding")
	
	def __create_space_property(self, name):
		self.node.properties.insert(name, SpaceProperty(), self.update_space)
	
	def update_space(self):
		pass


class PositionBoundary(SpaceBoundary):
	def __init__(self, node, position_x=0, position_y=0):
		super(PositionBoundary, self).__init__(node)
		
		self.__absolute_position = {"x": 0, "y": 0}
		
		self.node.properties.create_number("position-x", self.__update_absolute_position_x, position_x)
		self.node.properties.create_number("position-y", self.__update_absolute_position_y, position_y)
	
	def __update_absolute_position_x(self):
		self.__update("x", "width", 3, 1)
	
	def __update_absolute_position_y(self):
		self.__update("y", "height", 0, 2)
	
	def __update(self, axis, dimension, side_1, side_2):
		self.__update_absolute_position(axis, dimension, side_1, side_2)
		self.update_parent(axis, dimension, side_1, side_2)
	
	def __update_absolute_position(self, axis, dimension, side_1, side_2):
		self.__absolute_position[axis] = self.__get_parent_origin(axis, side_2) + self.__get_local_origin(axis, side_1)
		self.__update_children_position(axis, dimension, side_1, side_2)
	
	def __get_parent_origin(self, axis, side):
		parent = self.node.get_parent()
		
		try:
			return parent.get_absolute_position(axis) + parent["padding"][side]
		except AttributeError:
			return 0
	
	def __get_local_origin(self, axis, side):
		return self.node["position-%s" % axis] + self.node["margin"][side]
	
	def __update_children_position(self, axis, dimension, side_1, side_2):
		for child in self.node.children():
			child.boundary.__update(axis, dimension, side_1, side_2)
	
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
		
		self.node.properties.create_number("width", self.__update_absolute_width)
		self.node.properties.create_number("height", self.__update_absolute_height)
	
	def __update_absolute_width(self):
		self.__update("x", "width", 3, 1)
	
	def __update_absolute_height(self):
		self.__update("y", "height", 0, 2)
	
	def __update(self, axis, dimension, side_1, side_2):
		self.__absolute_size[dimension] = self.node["padding"][side_1] + self.node[dimension] + self.node["padding"][side_2]
		self.update_parent(axis, dimension, side_1, side_2)
	
	def update_size(self, axis, dimension, side_1, side_2):
		size = 0
		
		for child in self.node.children():
			child_end = child["position-%s" % axis] + child.boundary.__absolute_size[dimension]
			child_end_with_margins = child["margin"][side_1] + child_end + child["margin"][side_2]
			size = max(child_end_with_margins, size)
		
		self.node[dimension] = size
	
	def update_absolute_size(self):
		self.__update_absolute_width()
		self.__update_absolute_height()
	
	def absolute_size(self):
		return self.__absolute_size["width"], self.__absolute_size["height"]
	
	def get_absolute_size(self, dimension):
		return self.__absolute_size[dimension]


class Boundary(PositionBoundary, SizeBoundary):
	def update_space(self):
		self.update_absolute_position()
		self.update_absolute_size()
	
	def is_mouse_over(self, mouse_position):
		if self.get_absolute_size("width") > mouse_position[0] - self.get_absolute_position("x") > 0:
			if self.get_absolute_size("height") > mouse_position[1] - self.get_absolute_position("y") > 0:
				return True
		
		return False


class NullBoundary:
	def __getattr__(self, item):
		return lambda *args: 0
