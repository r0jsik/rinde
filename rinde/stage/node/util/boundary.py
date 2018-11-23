from rinde.stage.property import Properties


class BoundaryBase(object):
	def __init__(self, node):
		self.properties = Properties()
		
		self.__node = node
	
	def update_position(self):
		pass
	
	def update_parent_size(self, axis, dimension):
		parent = self.get_parent()
		parent.update_size(axis, dimension)
	
	def get_parent(self):
		return self.__node.get_parent_boundary() or NullBoundary()
	
	def set_property(self, name, value):
		self.properties[name].set(value)
	
	def get_property(self, name):
		return self.properties[name].get()
	
	def children_boundaries(self):
		return self.__node.children_boundaries()


class SpaceBoundary(BoundaryBase):
	def __init__(self, node, margin=0, padding=0):
		super(SpaceBoundary, self).__init__(node)
		
		self.properties.create_number("margin", self.update_space, margin)
		self.properties.create_number("padding", self.update_space, padding)
		
		self.__space = margin + padding
	
	def update_space(self):
		self.__space = self.get_property("margin") + self.get_property("padding")
		self.update_position()
	
	def get_space(self):
		return self.__space


class PositionBoundary(SpaceBoundary):
	def __init__(self, node, position_x=0, position_y=0, **kwargs):
		super(PositionBoundary, self).__init__(node, **kwargs)
		
		self.__absolute_position = {"x": 0, "y": 0}
		
		self.properties.create_number("position-x", self.__update_absolute_position_x, position_x)
		self.properties.create_number("position-y", self.__update_absolute_position_y, position_y)
	
	def __update_absolute_position_x(self):
		self.__update("x", "width")
	
	def __update_absolute_position_y(self):
		self.__update("y", "height")
	
	def __update(self, axis, dimension):
		self.__update_absolute_position(axis, dimension)
		self.update_parent_size(axis, dimension)
	
	def __update_absolute_position(self, axis, dimension):
		self.__absolute_position[axis] = self.__get_parent_origin(axis) + self.__get_local_origin(axis)
		self.__update_children_position(axis, dimension)
	
	def __get_parent_origin(self, axis):
		parent = self.get_parent()
		origin = parent.__absolute_position[axis] + parent.get_property("padding")
		
		return origin
	
	def __get_local_origin(self, axis):
		return self.get_property("position-%s" % axis) + self.get_property("margin")
	
	def __update_children_position(self, axis, dimension):
		for child in self.children_boundaries():
			child.__update(axis, dimension)
	
	def update_position(self):
		self.__update_absolute_position_x()
		self.__update_absolute_position_y()
	
	def get_absolute_position(self):
		return self.__absolute_position["x"], self.__absolute_position["y"]


class SizeBoundary(SpaceBoundary):
	def __init__(self, node, width=0, height=0, **kwargs):
		super(SizeBoundary, self).__init__(node, **kwargs)
		
		self.__absolute_size = {"width": 0, "height": 0}
		
		self.properties.create_number("width", self.update_absolute_width, width)
		self.properties.create_number("height", self.update_absolute_height, height)
	
	def update_absolute_width(self):
		self.__update_absolute_size("width")
		self.update_parent_size("x", "width")
	
	def __update_absolute_size(self, dimension):
		self.__absolute_size[dimension] = self.get_property(dimension) + self.get_space()
	
	def update_absolute_height(self):
		self.__update_absolute_size("height")
		self.update_parent_size("y", "height")
	
	def update_size(self, axis, dimension):
		size = 0
		
		for child in self.children_boundaries():
			size = max(child.get_property("position-%s" % axis) + child.__absolute_size[dimension], size)
		
		self.set_property(dimension, size)
	
	def get_absolute_width(self):
		return self.__absolute_size["width"]
	
	def get_absolute_height(self):
		return self.__absolute_size["height"]


class Boundary(PositionBoundary, SizeBoundary):
	def is_mouse_over(self, mouse_position):
		absolute_position = self.get_absolute_position()
		
		if self.get_absolute_width() > mouse_position[0] - absolute_position[0] > 0:
			if self.get_absolute_height() > mouse_position[1] - absolute_position[1] > 0:
				return True
		
		return False


class NullBoundary(Boundary):
	def __init__(self):
		super(NullBoundary, self).__init__(None)
	
	def children_boundaries(self):
		return ()
