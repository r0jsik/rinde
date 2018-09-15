from rinde.error import RindeException
from rinde.stage.node.util.boundary import Boundary
from rinde.stage.property import Properties


class NodeBase(object):
	def __init__(self, **kwargs):
		self.properties = Properties()
	
	def _borrow_property(self, node, name, trigger=None):
		self.properties.insert(node.properties[name], name, trigger)
	
	def set_property(self, name, value):
		return self.properties[name].set(value)
	
	def get_property(self, name):
		return self.properties[name].get()


class StylizableNode(NodeBase):
	def __init__(self, id=None, style_class=None, **kwargs):
		super(StylizableNode, self).__init__(**kwargs)
		
		self.id = id
		self.style_class = style_class
		self.style_name = None
		
		self.__create_state_property("hover")
		self.__create_state_property("active")
		self.__create_state_property("focus")
		
		self.__style = None
	
	def __create_state_property(self, name):
		self.properties.create_boolean(name, self.__update_state)
	
	def __update_state(self):
		self.__apply_style(None)
		
		if self.get_property("hover"):
			self.__apply_style("hover")
		
		if self.get_property("active"):
			self.__apply_style("active")
		
		if self.get_property("focus"):
			self.__apply_style("focus")
	
	def __apply_style(self, state):
		if state in self.__style:
			for property_name, value in self.__style[state].iteritems():
				self.set_property(property_name, value)
	
	def set_style(self, style):
		self.__style = style
		
		for property_name, value in style[None].iteritems():
			self.properties[property_name].reset(value)


class BoundaryNode(NodeBase):
	def __init__(self, **kwargs):
		super(BoundaryNode, self).__init__(**kwargs)
		
		self.__boundary = Boundary(self, **kwargs)
		
		self.__borrow_boundary_property("position_x")
		self.__borrow_boundary_property("position_y")
		self.__borrow_boundary_property("width")
		self.__borrow_boundary_property("height")
		self.__borrow_boundary_property("margin")
		self.__borrow_boundary_property("padding")
	
	def __borrow_boundary_property(self, name):
		self.properties.borrow(self.__boundary.properties, name)
	
	def update_boundary(self):
		self.__boundary.update()
	
	def is_mouse_over(self, mouse_position):
		return self.__boundary.is_mouse_over(mouse_position)
	
	def get_absolute_position(self):
		return self.__boundary.get_absolute_position()
	
	def set_position(self, position_x, position_y):
		self.set_property("position_x", position_x)
		self.set_property("position_y", position_y)
	
	def set_size(self, width, height):
		self.set_property("width", width)
		self.set_property("height", height)
	
	def get_size(self):
		return self.get_property("width"), self.get_property("height")
	
	def get_boundary(self):
		return self.__boundary


class InteractiveNode(StylizableNode, BoundaryNode):
	def __init__(self, visible=True, enabled=True, **kwargs):
		super(InteractiveNode, self).__init__(**kwargs)
		
		self.properties.create_boolean("visible", value=visible)
		self.properties.create_boolean("enabled", value=enabled)
	
	def can_be_hovered(self, mouse_position):
		visible = self.get_property("visible")
		enabled = self.get_property("enabled")
		
		return visible and enabled and self.is_mouse_over(mouse_position)
	
	def hover(self):
		self.set_property("hover", True)
	
	def leave(self):
		self.set_property("hover", False)
	
	def activate(self):
		self.set_property("active", True)
	
	def deactivate(self):
		self.set_property("active", False)
	
	def focus(self):
		self.set_property("focus", True)
	
	def unfocus(self):
		self.set_property("focus", False)
	
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
		
		self._nodes = []
		
		self.__parent = None
	
	# Chain of responsibility
	def update_style_request(self, node):
		if self.__parent:
			self.__parent.update_style_request(node)
		else:
			raise RindeException("Parent is not inserted to the stage")
	
	def set_parent(self, node):
		if None not in [self.__parent, node]:
			raise RindeException("Node has already got parent")
		
		self.__parent = node
	
	def _insert_node(self, node):
		node.set_parent(self)
		self._nodes.append(node)
	
	def _remove_node(self, node):
		node.set_parent(None)
		self._nodes.remove(node)
	
	def get_hovered_node(self, mouse_position):
		return self
	
	def children_boundaries_generator(self):
		for node in self._nodes:
			yield node.get_boundary()
	
	def get_parent_boundary(self):
		if isinstance(self.__parent, Node):
			return self.__parent.get_boundary()


class Node(InteractiveNode, StageNode):
	def __init__(self, **kwargs):
		super(Node, self).__init__(**kwargs)
		
		self.__canvas = None
		
		self.style_name = "node"
	
	def repaint(self, surface):
		if self.get_property("visible"):
			if self.__canvas:
				surface.blit(self.__canvas, self.get_absolute_position())
			
			for node in self._nodes:
				node.repaint(surface)
	
	def reset(self):
		self.update_style()
		
		for node in self._nodes:
			node.reset()
		
		self.update()
		self.update_boundary()
	
	def update_style(self):
		self.update_style_request(self)
	
	def update(self):
		pass
	
	def _set_canvas(self, canvas):
		self.__canvas = canvas
		
		width, height = canvas.get_size()
		self.set_size(width, height)
