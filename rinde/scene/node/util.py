from rinde.scene.property import IntegerProperty


class LayoutComputer(object):
	def __init__(self, node):
		self._node = node
	
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
		return self._node.get_property(property_name)


class PaneLayoutComputer(LayoutComputer):
	def get_nodes(self):
		return self._node.get_nodes()


class BoundaryBase(object):
	def __init__(self):
		self.__children = []
		
		self._parent = None
	
	def update_position(self):
		pass
	
	def update_parent_width(self):
		pass
	
	def update_parent_height(self):
		pass
	
	def _create_property(self, value, trigger):
		property = IntegerProperty(value)
		property.add_trigger(trigger)
		
		return property
	
	def set_parent(self, parent):
		if self._parent:
			self._parent.__children.remove(self)
		else:
			self._parent = parent
			self._parent.__children.append(self)
	
	def _get_children(self):
		return self.__children


class SpaceBoundary(BoundaryBase):
	def __init__(self, margin=0, padding=0):
		super(SpaceBoundary, self).__init__()
		
		self.__margin = self._create_property(margin, self.update)
		self.__padding = self._create_property(padding, self.update)
		self.__space = margin + padding
	
	def update(self):
		self.__space = self.__margin.get() + self.__padding.get()
		self.update_position()
	
	def margin(self):
		return self.__margin
	
	def get_margin(self):
		return self.__margin.get()
	
	def padding(self):
		return self.__padding
	
	def get_padding(self):
		return self.__padding.get()
	
	def get_space(self):
		return self.__space


class PositionBoundary(SpaceBoundary):
	def __init__(self, position_x=0, position_y=0, **kwargs):
		super(PositionBoundary, self).__init__(**kwargs)
		
		self.__position_x = self._create_property(position_x, self.update_absolute_position_x)
		self.__position_y = self._create_property(position_y, self.update_absolute_position_y)
		self.__absolute_position_x = 0
		self.__absolute_position_y = 0
	
	def update_absolute_position_x(self):
		self.__absolute_position_x = self.__position_x.get() + self.get_margin()
		
		if self._parent:
			self.__absolute_position_x += self._parent.__absolute_position_x + self._parent.get_padding()
		
		self.update_children_position_x()
		self.update_parent_width()
	
	def update_children_position_x(self):
		for children in self._get_children():
			children.update_absolute_position_x()
	
	def update_absolute_position_y(self):
		self.__absolute_position_y = self.__position_y.get() + self.get_margin()
		
		if self._parent:
			self.__absolute_position_y += self._parent.__absolute_position_y + self._parent.get_padding()
		
		self.update_children_position_y()
		self.update_parent_height()
	
	def update_children_position_y(self):
		for children in self._get_children():
			children.update_absolute_position_y()
	
	def update_position(self):
		self.update_absolute_position_x()
		self.update_absolute_position_y()
	
	def position_x(self):
		return self.__position_x
	
	def position_y(self):
		return self.__position_y
	
	def get_absolute_position(self):
		return self.__absolute_position_x, self.__absolute_position_y
	
	def get_absolute_position_x(self):
		return self.__absolute_position_x
	
	def get_absolute_position_y(self):
		return self.__absolute_position_y
	
	def get_position_x(self):
		return self.__position_x.get()
	
	def get_position_y(self):
		return self.__position_y.get()


class SizeBoundary(SpaceBoundary):
	def __init__(self, width=0, height=0, **kwargs):
		super(SizeBoundary, self).__init__(**kwargs)
		
		self.__width = self._create_property(width, self.update_absolute_width)
		self.__height = self._create_property(height, self.update_absolute_height)
		self.__absolute_width = 0
		self.__absolute_height = 0
	
	def update_absolute_width(self):
		self.__absolute_width = self.__width.get() + self.get_space()
		self.update_parent_width()
	
	def update_parent_width(self):
		if self._parent:
			self._parent.update_width()
	
	def update_width(self):
		width = 0
		
		for children in self._get_children():
			width = max(children.get_position_x() + children.__absolute_width, width)
		
		self.__width.set(width)
	
	def update_absolute_height(self):
		self.__absolute_height = self.__height.get() + self.get_space()
		self.update_parent_height()
	
	def update_parent_height(self):
		if self._parent:
			self._parent.update_height()
	
	def update_height(self):
		height = 0
		
		for children in self._get_children():
			height = max(children.get_position_y() + children.__absolute_height, height)
		
		self.__height.set(height)
	
	def width(self):
		return self.__width
	
	def height(self):
		return self.__height
	
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
