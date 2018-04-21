from rinde.error import RindeException
from rinde.scene.property import IntegerProperty


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
		
		self.__margin = self._create_property(margin, self.__update_space)
		self.__padding = self._create_property(padding, self.__update_space)
		self.__space = margin + padding
	
	def __update_space(self):
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
	
	def position_x(self):
		return self.__position_x
	
	def position_y(self):
		return self.__position_y
	
	def update_position(self):
		self.update_absolute_position_x()
		self.update_absolute_position_y()
	
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
		self.__absolute_width = self.__width.get() + 2*self.get_space()
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
		self.__absolute_height = self.__height.get() + 2*self.get_space()
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
	
	def get_absolute_size(self):
		return self.__absolute_width, self.__absolute_height
	
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


class LayoutComputer(object):
	def __init__(self, container):
		self.__container = container
	
	def _get_container_property(self, property_name):
		return self.__container.get_property(property_name)
	
	def _get_container_nodes(self):
		return self.__container.get_nodes()


class BoxLayoutComputer(LayoutComputer):
	def update_nodes_spacing(self, dimension, axis):
		spacing = self._get_container_property("spacing")
		position = 0
		
		for node in self._get_container_nodes():
			property = node.property("position_%s" % axis)
			property.set(position)
			position += node.get_property(dimension) + spacing
	
	def update_nodes_align(self, axis):
		align = self._get_container_property("align")
		
		for node in self._get_container_nodes():
			property = node.property("position_%s" % axis)
			position = self.__get_aligned_position(node, align)
			property.set(position)
	
	def __get_aligned_position(self, node, align):
		position = self._compute_aligned_position(node, align)
		
		if position is None:
			raise RindeException("Unknown alignment: '%s'" % align)
		
		return position
	
	def _compute_aligned_position(self, node, align):
		return 0


class VBoxLayoutComputer(BoxLayoutComputer):
	def _compute_aligned_position(self, node, align):
		if align == "left":
			return 0
		
		if align == "center":
			return (self._get_container_property("width") - node.get_property("width"))/2
		
		if align == "right":
			return self._get_container_property("width") - node.get_property("width")


class HBoxLayoutComputer(BoxLayoutComputer):
	def _compute_aligned_position(self, node, align):
		if align == "top":
			return 0
		
		if align == "middle":
			return (self._get_container_property("height") - node.get_property("height"))/2
		
		if align == "bottom":
			return self._get_container_property("height") - node.get_property("height")
