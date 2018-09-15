from rinde.stage.property import Properties


class BoundaryBase(object):
	def __init__(self, node):
		self.properties = Properties()
		
		self.__node = node
	
	def update_position(self):
		pass
	
	def update_parent_width(self):
		parent = self.get_parent()
		
		if parent:
			parent.update_width()
	
	def update_parent_height(self):
		parent = self.get_parent()
		
		if parent:
			parent.update_height()
	
	def set_property(self, name, value):
		self.properties[name].set(value)
	
	def get_property(self, name):
		return self.properties[name].get()
	
	def children_boundaries(self):
		return self.__node.children_boundaries_generator()
	
	def get_parent(self):
		return self.__node.get_parent_boundary()


class SpaceBoundary(BoundaryBase):
	def __init__(self, node, margin=0, padding=0):
		super(SpaceBoundary, self).__init__(node)
		
		self.properties.create_integer("margin", self.update, margin)
		self.properties.create_integer("padding", self.update, padding)
		
		self.__space = margin + padding
	
	def update(self):
		self.__space = self.get_property("margin") + self.get_property("padding")
		self.update_position()
	
	def get_space(self):
		return self.__space


class PositionBoundary(SpaceBoundary):
	def __init__(self, node, position_x=0, position_y=0, **kwargs):
		super(PositionBoundary, self).__init__(node, **kwargs)
		
		self.properties.create_integer("position_x", self.update_absolute_position_x, position_x)
		self.properties.create_integer("position_y", self.update_absolute_position_y, position_y)
		
		self.__absolute_position_x = 0
		self.__absolute_position_y = 0
	
	def update_absolute_position_x(self):
		self.__absolute_position_x = self.__get_parent_origin_x() + self.__get_local_origin("x")
		
		self.update_children_position_x()
		self.update_parent_width()
	
	def __get_parent_origin_x(self):
		parent = self.get_parent()
		
		if parent:
			return parent.__absolute_position_x + parent.get_property("padding")
		
		return 0
	
	def __get_local_origin(self, axis):
		return self.get_property("position_%s" % axis) + self.get_property("margin")
	
	def update_children_position_x(self):
		for child in self.children_boundaries():
			child.update_absolute_position_x()
	
	def update_absolute_position_y(self):
		self.__absolute_position_y = self.__get_parent_origin_y() + self.__get_local_origin("y")
		
		self.update_children_position_y()
		self.update_parent_height()
	
	def __get_parent_origin_y(self):
		parent = self.get_parent()
		
		if parent:
			return parent.__absolute_position_y + parent.get_property("padding")
		
		return 0
	
	def update_children_position_y(self):
		for child in self.children_boundaries():
			child.update_absolute_position_y()
	
	def update_position(self):
		self.update_absolute_position_x()
		self.update_absolute_position_y()
	
	def get_absolute_position(self):
		return self.__absolute_position_x, self.__absolute_position_y


class SizeBoundary(SpaceBoundary):
	def __init__(self, node, width=0, height=0, **kwargs):
		super(SizeBoundary, self).__init__(node, **kwargs)
		
		self.properties.create_integer("width", self.update_absolute_width, width)
		self.properties.create_integer("height", self.update_absolute_height, height)
		
		self.__absolute_width = 0
		self.__absolute_height = 0
	
	def update_absolute_width(self):
		self.__absolute_width = self.get_property("width") + self.get_space()
		self.update_parent_width()
	
	def update_width(self):
		width = 0
		
		for child in self.children_boundaries():
			width = max(child.get_property("position_x") + child.__absolute_width, width)
		
		self.set_property("width", width)
	
	def update_absolute_height(self):
		self.__absolute_height = self.get_property("height") + self.get_space()
		self.update_parent_height()
	
	def update_height(self):
		height = 0
		
		for child in self.children_boundaries():
			height = max(child.get_property("position_y") + child.__absolute_height, height)
		
		self.set_property("height", height)
	
	def get_absolute_width(self):
		return self.__absolute_width
	
	def get_absolute_height(self):
		return self.__absolute_height


class Boundary(PositionBoundary, SizeBoundary):
	def is_mouse_over(self, mouse_position):
		absolute_position = self.get_absolute_position()
		
		if self.get_absolute_width() > mouse_position[0] - absolute_position[0] > 0:
			if self.get_absolute_height() > mouse_position[1] - absolute_position[1] > 0:
				return True
		
		return False
