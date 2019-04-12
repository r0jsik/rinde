from rinde.error import RindeException
from rinde.stage.node.util.appearance import Appearance
from rinde.stage.node.util.boundary import Boundary
from rinde.stage.property import BooleanProperty
from rinde.stage.property import NumberProperty
from rinde.stage.property import Property


class NodeBase(object):
	def __init__(self, **kwargs):
		self.__properties = {}
	
	def _create_property(self, name, trigger=None, value=None):
		self.__properties[name] = Property(value)
		self.__try_to_add_trigger_to_property(name, trigger)
	
	def _create_number_property(self, name, trigger=None, value=0):
		self.__properties[name] = NumberProperty(value)
		self.__try_to_add_trigger_to_property(name, trigger)
	
	def _create_boolean_property(self, name, value=False, trigger=None):
		self.__properties[name] = BooleanProperty(value)
		self.__try_to_add_trigger_to_property(name, trigger)
	
	def _borrow_property(self, node, name, trigger=None, name_as=None):
		property = node.property(name)
		
		if name_as:
			self._insert_property(name_as, property, trigger)
		else:
			self._insert_property(name, property, trigger)
	
	def _insert_property(self, name, property, trigger=None):
		self.__properties[name] = property
		self.__try_to_add_trigger_to_property(name, trigger)
	
	def __try_to_add_trigger_to_property(self, name, trigger):
		if trigger:
			self.__properties[name].add_trigger(trigger)
	
	def _add_trigger_to_property(self, name, trigger):
		self.__properties[name].add_trigger(trigger)
	
	def property(self, name):
		return self.__properties[name]
	
	def __setitem__(self, property_name, value):
		self.__properties[property_name].set(value)
	
	def __getitem__(self, property_name):
		return self.__properties[property_name].get()


class StylizableNode(NodeBase):
	def __init__(self, id=None, style_class=None, **kwargs):
		super(StylizableNode, self).__init__(**kwargs)
		
		self.__appearance = Appearance(self, id, style_class)
		
		self.__create_state_property("hovered")
		self.__create_state_property("active")
		self.__create_state_property("focused")
	
	def __create_state_property(self, name):
		self._create_boolean_property(name, trigger=self.__update_state)
	
	def __update_state(self):
		self.__appearance.apply(None)
		
		if self["hovered"]:
			self.__appearance.apply("hovered")
		
		if self["active"]:
			self.__appearance.apply("active")
		
		if self["focused"]:
			self.__appearance.apply("focused")
	
	def set_style(self, style):
		self.__appearance.set_style(style)
		self.__appearance.apply_default()
	
	def get_appearance(self):
		return self.__appearance
	
	def set_id(self, value):
		self.__appearance.set_id(value)
	
	def set_style_class(self, value):
		self.__appearance.set_style_class(value)
	
	def set_style_name(self, value):
		self.__appearance.set_style_name(value)
	
	def style_selectors(self):
		return self.__appearance.style_selectors()


class BoundaryNode(NodeBase):
	def __init__(self, **kwargs):
		super(BoundaryNode, self).__init__(**kwargs)
		
		self.__boundary = Boundary(self, **kwargs)
	
	def update_boundary(self):
		self.__boundary.update_absolute_position()
		self.__boundary.update_absolute_size()
	
	def update_layout(self):
		pass
	
	def is_mouse_over(self, mouse_position):
		return self.__boundary.is_mouse_over(mouse_position)
	
	def absolute_position(self):
		return self.__boundary.absolute_position()
	
	def get_absolute_position(self, axis):
		return self.__boundary.get_absolute_position(axis)
	
	def absolute_size(self):
		return self.__boundary.absolute_size()
	
	def get_absolute_size(self, dimension):
		return self.__boundary.get_absolute_size(dimension)
	
	def set_position(self, position_x, position_y):
		self["position-x"], self["position-y"] = position_x, position_y
	
	def set_size(self, width, height):
		self["width"], self["height"] = width, height
	
	def get_size(self):
		return self["width"], self["height"]
	
	def get_boundary(self):
		return self.__boundary


class InteractiveNode(StylizableNode, BoundaryNode):
	def __init__(self, visible=True, enabled=True, **kwargs):
		super(InteractiveNode, self).__init__(**kwargs)
		
		self._create_boolean_property("visible", visible)
		self._create_boolean_property("enabled", enabled)
	
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
			raise RindeException("Node is not inserted to the stage")
		
		self.__parent.update_style_request(node)
	
	def set_parent(self, node):
		if self.__parent and node:
			raise RindeException("Node has already got parent")
		
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
	
	def children_boundaries(self):
		for node in self.__nodes:
			yield node.get_boundary()
	
	def get_parent_boundary(self):
		if self.__parent:
			return self.__parent.get_boundary()
		
		return None
	
	def children_appearances(self):
		for node in self.__nodes:
			yield node.get_appearance()
	
	def _get_nodes(self):
		return self.__nodes


class Node(InteractiveNode, StageNode):
	def __init__(self, **kwargs):
		super(Node, self).__init__(**kwargs)
		
		self.__canvas = None
	
	def repaint(self, surface):
		if self["visible"]:
			if self.__canvas:
				surface.blit(self.__canvas, self.absolute_position())
			
			for node in self._get_nodes():
				node.repaint(surface)
	
	def reset(self):
		self.update_style()
		self.update_boundary()
		
		for node in self._get_nodes():
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
