from rinde.stage.property import Properties


class LayoutComputer(object):
	def __init__(self, node):
		self.__node = node
	
	def center_node(self, node):
		self.center_node_vertically(node)
		self.center_node_horizontally(node)
	
	def center_node_horizontally(self, node):
		position = self.compute_node_center(node, "width")
		node.set_property("position_x", position)
	
	def center_node_vertically(self, node):
		position = self.compute_node_center(node, "height")
		node.set_property("position_y", position)
	
	def compute_node_center(self, node, dimension):
		return (self.get_property(dimension) - node.get_property(dimension))/2
	
	def get_property(self, property_name):
		return self.__node.get_property(property_name)


class PaneLayoutComputer(LayoutComputer):
	def __init__(self, pane):
		super(PaneLayoutComputer, self).__init__(pane)
		
		self.__pane = pane
	
	def get_nodes(self):
		return self.__pane.get_nodes()


class BoundaryBase(object):
	def __init__(self):
		self.__children = []
		
		self._parent = None
		
		self.properties = Properties()
	
	def update_position(self):
		pass
	
	def update_parent_width(self):
		pass
	
	def update_parent_height(self):
		pass
	
	def set_parent(self, parent):
		if self._parent:
			self._parent.__children.remove(self)
		else:
			self._parent = parent
			self._parent.__children.append(self)
	
	def set_property(self, name, value):
		self.properties[name].set(value)
	
	def get_property(self, name):
		return self.properties[name].get()
	
	def get_children(self):
		return self.__children


class SpaceBoundary(BoundaryBase):
	def __init__(self, margin=0, padding=0):
		super(SpaceBoundary, self).__init__()
		
		self.properties.create_integer("margin", self.update, margin)
		self.properties.create_integer("padding", self.update, padding)
		
		self.__space = margin + padding
	
	def update(self):
		self.__space = self.get_property("margin") + self.get_property("padding")
		self.update_position()
	
	def get_space(self):
		return self.__space


class PositionBoundary(SpaceBoundary):
	def __init__(self, position_x=0, position_y=0, **kwargs):
		super(PositionBoundary, self).__init__(**kwargs)
		
		self.properties.create_integer("position_x", self.update_absolute_position_x, position_x)
		self.properties.create_integer("position_y", self.update_absolute_position_y, position_y)
		
		self.__absolute_position_x = 0
		self.__absolute_position_y = 0
	
	def update_absolute_position_x(self):
		self.__absolute_position_x = self.get_property("position_x") + self.get_property("margin")
		
		if self._parent:
			self.__absolute_position_x += self._parent.__absolute_position_x + self._parent.get_property("padding")
		
		self.update_children_position_x()
		self.update_parent_width()
	
	def update_children_position_x(self):
		for child in self.get_children():
			child.update_absolute_position_x()
	
	def update_absolute_position_y(self):
		self.__absolute_position_y = self.get_property("position_y") + self.get_property("margin")
		
		if self._parent:
			self.__absolute_position_y += self._parent.__absolute_position_y + self._parent.get_property("padding")
		
		self.update_children_position_y()
		self.update_parent_height()
	
	def update_children_position_y(self):
		for child in self.get_children():
			child.update_absolute_position_y()
	
	def update_position(self):
		self.update_absolute_position_x()
		self.update_absolute_position_y()
	
	def get_absolute_position(self):
		return self.__absolute_position_x, self.__absolute_position_y
	
	def get_absolute_position_x(self):
		return self.__absolute_position_x
	
	def get_absolute_position_y(self):
		return self.__absolute_position_y


class SizeBoundary(SpaceBoundary):
	def __init__(self, width=0, height=0, **kwargs):
		super(SizeBoundary, self).__init__(**kwargs)
		
		self.properties.create_integer("width", self.update_absolute_width, width)
		self.properties.create_integer("height", self.update_absolute_height, height)
		
		self.__absolute_width = 0
		self.__absolute_height = 0
	
	def update_absolute_width(self):
		self.__absolute_width = self.get_property("width") + self.get_space()
		self.update_parent_width()
	
	def update_parent_width(self):
		if self._parent:
			self._parent.update_width()
	
	def update_width(self):
		width = 0
		
		for child in self.get_children():
			width = max(child.get_property("position_x") + child.__absolute_width, width)
			
		self.set_property("width", width)
	
	def update_absolute_height(self):
		self.__absolute_height = self.get_property("height") + self.get_space()
		self.update_parent_height()
	
	def update_parent_height(self):
		if self._parent:
			self._parent.update_height()
	
	def update_height(self):
		height = 0
		
		for child in self.get_children():
			height = max(child.get_property("position_y") + child.__absolute_height, height)
		
		self.set_property("height", height)
	
	def get_absolute_width(self):
		return self.__absolute_width
	
	def get_absolute_height(self):
		return self.__absolute_height


class Boundary(PositionBoundary, SizeBoundary):
	def is_mouse_over(self, mouse_position):
		if self.get_absolute_width() > mouse_position[0] - self.get_absolute_position_x() > 0:
			if self.get_absolute_height() > mouse_position[1] - self.get_absolute_position_y() > 0:
				return True
		
		return False
