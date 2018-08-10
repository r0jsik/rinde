from rinde.error import RindeException
from rinde.stage.node.util import Boundary
from rinde.stage.property import BooleanProperty
from rinde.stage.property import IntegerProperty
from rinde.stage.property import Property


class NodeBase(object):
	def __init__(self, **kwargs):
		self._property = {}
	
	def set_property(self, name, value):
		self.property(name).set(value)
	
	def property(self, name):
		try:
			return self._property[name]
		except KeyError:
			raise RindeException("Unknown property: '%s'" % name)
	
	def get_property(self, name):
		return self.property(name).get()


class StylizableNode(NodeBase):
	def __init__(self, id=None, style_class=None, **kwargs):
		super(StylizableNode, self).__init__(**kwargs)
		
		self.id = id
		self.style_class = style_class
		self.style_name = None
		
		self._property["hovered"] = self.__create_state_property()
		self._property["active"] = self.__create_state_property()
		self._property["focused"] = self.__create_state_property()
		
		self.__style = None
	
	def __create_state_property(self):
		property = BooleanProperty()
		property.add_trigger(self.__update_state)
		
		return property
	
	def __update_state(self):
		self.__apply_style(None)
		
		if self.get_property("hovered"):
			self.__apply_style("hover")
		
		if self.get_property("active"):
			self.__apply_style("active")
		
		if self.get_property("focused"):
			self.__apply_style("focus")
	
	def __apply_style(self, state):
		if state in self.__style:
			for property_name, value in self.__style[state].iteritems():
				self.set_property(property_name, value)
	
	def set_style(self, style):
		self.__style = style
		
		for property_name, value in style[None].iteritems():
			self.property(property_name).reset(value)


class BoundaryNode(NodeBase):
	def __init__(self, **kwargs):
		super(BoundaryNode, self).__init__(**kwargs)
		
		self._boundary = Boundary(**kwargs)
		
		self._property["position_x"] = self._boundary.position_x()
		self._property["position_y"] = self._boundary.position_y()
		self._property["width"] = self._boundary.width()
		self._property["height"] = self._boundary.height()
	
	def update_boundary(self):
		self._boundary.update()
	
	def set_position(self, position_x, position_y):
		self.set_property("position_x", position_x)
		self.set_property("position_y", position_y)
	
	def set_size(self, width, height):
		self.set_property("width", width)
		self.set_property("height", height)
	
	def get_size(self):
		return self.get_property("width"), self.get_property("height")
	
	def set_boundary_parent(self, boundary):
		self._boundary.set_parent(boundary)


class InteractiveNode(StylizableNode, BoundaryNode):
	def __init__(self, visible=True, enabled=True, **kwargs):
		super(InteractiveNode, self).__init__(**kwargs)
		
		self._property["visible"] = BooleanProperty(visible)
		self._property["enabled"] = BooleanProperty(enabled)
	
	def can_be_hovered(self, mouse_position):
		return self.get_property("visible") and self.get_property("enabled") and self._boundary.is_mouse_over(mouse_position)
	
	def hover(self):
		self.set_property("hovered", True)
	
	def leave(self):
		self.set_property("hovered", False)
	
	def activate(self):
		self.set_property("active", True)
	
	def deactivate(self):
		self.set_property("active", False)
	
	def focus(self):
		self.set_property("focused", True)
	
	def unfocus(self):
		self.set_property("focused", False)
	
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
		self._parent = None
	
	def _insert_node(self, node):
		node.set_parent(self)
		node.set_boundary_parent(self._boundary)
		self._nodes.append(node)
	
	def set_parent(self, parent):
		if None not in [self._parent, parent]:
			raise RindeException("Node has already got parent")
		
		self._parent = parent
	
	def _remove_node(self, node):
		node.set_parent(None)
		node.set_boundary_parent(None)
		self._nodes.remove(node)
	
	def get_hovered_node(self, mouse_position):
		return self


class Node(InteractiveNode, StageNode):
	def __init__(self, **kwargs):
		super(Node, self).__init__(**kwargs)
		
		self.__canvas = None
		
		self.style_name = "node"
	
	def repaint(self, surface):
		if self.get_property("visible"):
			if self.__canvas:
				surface.blit(self.__canvas, self._boundary.get_absolute_position())
			
			for node in self._nodes:
				node.repaint(surface)
	
	def _borrow_property(self, node, property_name):
		property = node.property(property_name)
		property.add_trigger(self.update)
		
		return property
	
	def _create_property(self, trigger, value=None):
		property = Property(value)
		property.add_trigger(trigger)
		
		return property
	
	def _create_integer_property(self, trigger, value=0):
		property = IntegerProperty(value)
		property.add_trigger(trigger)
		
		return property
	
	def reset(self):
		for node in self._nodes:
			self.insert_to_stage(node)
		
		self.update_boundary()
		self.update()
	
	def insert_to_stage(self, node):
		if isinstance(self._parent, Node):
			self._parent.insert_to_stage(node)
		else:
			self._parent.insert(node)
	
	def update(self):
		pass
	
	def _set_canvas(self, canvas):
		self.__canvas = canvas
		
		width, height = canvas.get_size()
		self.set_size(width, height)
