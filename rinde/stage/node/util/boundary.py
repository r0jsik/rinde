from rinde.stage.property import Properties


class BoundaryBase(object):
	def __init__(self, node):
		self.__properties = Properties()
		self.__node = node
	
	def create_property(self, name, trigger, value):
		self.__properties.create_number(name, trigger, value)
	
	def property(self, name):
		return self.__properties[name]
	
	def set_property(self, name, value):
		self.__properties[name].set(value)
	
	def get_property(self, name):
		return self.__properties[name].get()
	
	def update_parent_size(self, axis, dimension):
		parent = self.get_parent()
		parent.update_size(axis, dimension)
	
	def get_parent(self):
		return self.__node.get_parent_boundary() or NullBoundary()
	
	def children_boundaries(self):
		return self.__node.children_boundaries()


class SpaceBoundary(BoundaryBase):
	def __init__(self, node, margin=0, padding=0):
		super(SpaceBoundary, self).__init__(node)
		
		self.create_property("margin", self.update_space, margin)
		self.create_property("padding", self.update_space, padding)
		
		self.__space = margin + padding
	
	def update_space(self):
		self.__space = self.get_property("margin") + self.get_property("padding")
		self.update_position()
	
	def update_position(self):
		pass
	
	def get_space(self):
		return self.__space


class PositionBoundary(SpaceBoundary):
	def __init__(self, node, position_x=0, position_y=0, **kwargs):
		super(PositionBoundary, self).__init__(node, **kwargs)
		
		self.__absolute_position = {"x": 0, "y": 0}
		
		self.create_property("position-x", self.__update_absolute_position_x, position_x)
		self.create_property("position-y", self.__update_absolute_position_y, position_y)
	
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
		
		self.create_property("width", self.__update_absolute_width, width)
		self.create_property("height", self.__update_absolute_height, height)
	
	def __update_absolute_width(self):
		self.__update("x", "width")
	
	def __update_absolute_height(self):
		self.__update("y", "height")
	
	def __update(self, axis, dimension):
		self.__absolute_size[dimension] = self.get_property(dimension) + 2*self.get_space()
		self.update_parent_size(axis, dimension)
	
	def update_size(self, axis, dimension):
		size = 0
		
		for child in self.children_boundaries():
			size = max(child.get_property("position-%s" % axis) + child.__absolute_size[dimension], size)
		
		self.set_property(dimension, size)
	
	def update_absolute_size(self):
		self.__update_absolute_width()
		self.__update_absolute_height()
	
	def get_absolute_size(self):
		return self.__absolute_size["width"], self.__absolute_size["height"]


class Boundary(PositionBoundary, SizeBoundary):
	def is_mouse_over(self, mouse_position):
		absolute_size = self.get_absolute_size()
		absolute_position = self.get_absolute_position()
		
		if absolute_size[0] > mouse_position[0] - absolute_position[0] > 0:
			if absolute_size[1] > mouse_position[1] - absolute_position[1] > 0:
				return True
		
		return False


class NullBoundary(Boundary):
	def __init__(self):
		super(NullBoundary, self).__init__(None)
	
	def children_boundaries(self):
		return ()
