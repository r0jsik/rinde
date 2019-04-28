from rinde.stage.node.util.appearance import Appearance
from rinde.stage.node.util.boundary import Boundary
from rinde.stage.property import Properties


class NodeBase(object):
	def __init__(self, **kwargs):
		self.properties = Properties()
	
	def borrow_property(self, node, name, trigger=None, name_as=None):
		property = node.properties[name]
		
		if name_as:
			self.properties.insert(name_as, property, trigger)
		else:
			self.properties.insert(name, property, trigger)
	
	def property(self, property_name):
		return self.properties[property_name]
	
	def __setitem__(self, property_name, value):
		self.properties[property_name].set(value)
	
	def __getitem__(self, property_name):
		return self.properties[property_name].get()


class StylizableNode(NodeBase):
	def __init__(self, id=None, style_class=None, **kwargs):
		super(StylizableNode, self).__init__(**kwargs)
		
		self.appearance = Appearance(self, id, style_class)
		
		self.__create_state_property("hovered")
		self.__create_state_property("active")
		self.__create_state_property("focused")
	
	def __create_state_property(self, name):
		self.properties.create_boolean(name, trigger=self.__update_state)
	
	def __update_state(self):
		self.appearance.apply(None)
		
		if self["hovered"]:
			self.appearance.apply("hovered")
		
		if self["active"]:
			self.appearance.apply("active")
		
		if self["focused"]:
			self.appearance.apply("focused")
	
	def set_style_name(self, value):
		self.appearance.style_name = value


class BoundaryNode(NodeBase):
	def __init__(self, **kwargs):
		super(BoundaryNode, self).__init__(**kwargs)
		
		self.boundary = Boundary(self, **kwargs)
	
	def update_boundary(self):
		self.boundary.update_absolute_position()
		self.boundary.update_absolute_size()
	
	def update_layout(self):
		pass
	
	def is_mouse_over(self, mouse_position):
		return self.boundary.is_mouse_over(mouse_position)
	
	def absolute_position(self):
		return self.boundary.absolute_position()
	
	def get_absolute_position(self, axis):
		return self.boundary.get_absolute_position(axis)
	
	def absolute_size(self):
		return self.boundary.absolute_size()
	
	def get_absolute_size(self, dimension):
		return self.boundary.get_absolute_size(dimension)
	
	def set_position(self, position_x, position_y):
		self["position-x"], self["position-y"] = position_x, position_y
	
	def set_size(self, width, height):
		self["width"], self["height"] = width, height
	
	def get_size(self):
		return self["width"], self["height"]


class InteractiveNode(StylizableNode, BoundaryNode):
	def __init__(self, visible=True, enabled=True, **kwargs):
		super(InteractiveNode, self).__init__(**kwargs)
		
		self.properties.create_boolean("visible", value=visible)
		self.properties.create_boolean("enabled", value=enabled)
	
	def can_be_hovered(self, mouse_position):
		return self["visible"] and self["enabled"] and self.is_mouse_over(mouse_position)
	
	def hover(self):
		self["hovered"] = True
	
	def leave(self):
		self["hovered"] = False
	
	def activate(self):
		self["active"] = True
	
	def deactivate(self):
		self["active"] = False
	
	def focus(self):
		self["focused"] = True
	
	def unfocus(self):
		self["focused"] = False
	
	def drag(self, mouse_offset):
		pass
	
	def click(self):
		pass
	
	def scroll_up(self):
		pass
	
	def scroll_down(self):
		pass
	
	def key_pressed(self, code, char):
		pass


class StageNode(StylizableNode, BoundaryNode):
	def __init__(self, **kwargs):
		super(StageNode, self).__init__(**kwargs)
		
		self.__nodes = []
		self.__parent = None
	
	# Chain of responsibility
	def update_style_request(self, node):
		if self.__parent is None:
			raise RuntimeError("Node is not inserted to the stage")
		
		self.__parent.update_style_request(node)
	
	def set_parent(self, node):
		if self.__parent and node:
			raise RuntimeError("Node has already got parent")
		
		self.__parent = node
	
	def _insert_node(self, node, index=None):
		if index is None:
			self.__nodes.append(node)
		else:
			self.__nodes.insert(index, node)
		
		node.set_parent(self)
	
	def _remove_node(self, node):
		node.set_parent(None)
		self.__nodes.remove(node)
	
	def get_hovered_node(self, mouse_position):
		return self
	
	def get_parent(self):
		return self.__parent
	
	def get_parent_boundary(self):
		try:
			return self.__parent.boundary
		except AttributeError:
			return None
	
	def children(self):
		return self.__nodes


class Node(InteractiveNode, StageNode):
	def __init__(self, **kwargs):
		super(Node, self).__init__(**kwargs)
		
		self.__canvas = None
	
	def repaint(self, surface):
		if self["visible"]:
			if self.__canvas:
				surface.blit(self.__canvas, self.absolute_position())
			
			for node in self.children():
				node.repaint(surface)
	
	def reset(self):
		self.update_style()
		self.update_boundary()
		
		for node in self.children():
			node.reset()
		
		self.update()
	
	def update_style(self):
		self.update_style_request(self)
	
	def update(self):
		pass
	
	def _set_canvas(self, canvas):
		self.__canvas = canvas
	
	def _fit_size(self):
		width, height = self.__canvas.get_size()
		self.set_size(width, height)
	
	def _get_canvas(self):
		return self.__canvas
