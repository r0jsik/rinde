from rinde.stage.node.util.appearance import Appearance
from rinde.stage.node.util.boundary import ComplexNodeBoundary
from rinde.stage.node.util.boundary import NullBoundary
from rinde.stage.node.util.boundary import SimpleNodeBoundary
from rinde.property import Properties


class NodeBase(object):
	def __init__(self, **kwargs):
		self.properties = Properties()
	
	def _borrow_property(self, node, name, trigger=None, name_as=None):
		property = node.properties[name]
		
		if name_as:
			self.properties.insert(name_as, property, trigger)
		else:
			self.properties.insert(name, property, trigger)
	
	def __setitem__(self, property_name, value):
		self.properties[property_name].set(value)
	
	def __getitem__(self, property_name):
		return self.properties[property_name].get()


class StylizableNode(NodeBase):
	def __init__(self, id=None, style_class=None, **kwargs):
		super(StylizableNode, self).__init__(**kwargs)
		
		self.appearance = Appearance(self, id, style_class)
		
		self.appearance.create_state("hovered")
		self.appearance.create_state("active")
		self.appearance.create_state("focused")
	
	def set_style_name(self, value):
		self.appearance.style_name = value


class BoundaryNode(NodeBase):
	def __init__(self, boundary_type, **kwargs):
		super(BoundaryNode, self).__init__(**kwargs)
		
		self.boundary = boundary_type(self, **kwargs)
	
	def absolute_position(self):
		return self.boundary.absolute_position()
	
	def get_absolute_position(self, axis):
		return self.boundary.get_absolute_position(axis)
	
	def absolute_size(self):
		return self.boundary.absolute_size()
	
	def get_absolute_size(self, dimension):
		return self.boundary.get_absolute_size(dimension)


class InteractiveNode(StylizableNode, BoundaryNode):
	def __init__(self, visible=True, enabled=True, **kwargs):
		super(InteractiveNode, self).__init__(**kwargs)
		
		self.properties.create_boolean("visible", value=visible)
		self.properties.create_boolean("enabled", value=enabled)
	
	def can_be_hovered(self, mouse_position):
		return self["visible"] and self["enabled"] and self.boundary.is_mouse_over(mouse_position)
	
	def hover(self):
		self.appearance["hovered"] = True
	
	def leave(self):
		self.appearance["hovered"] = False
	
	def activate(self):
		self.appearance["active"] = True
	
	def deactivate(self):
		self.appearance["active"] = False
	
	def focus(self):
		self.appearance["focused"] = True
	
	def unfocus(self):
		self.appearance["focused"] = False
	
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
		
		self.__parent = None
	
	def update_style(self):
		self.update_style_request(self, [self])
	
	# Chain of responsibility
	def update_style_request(self, node, path):
		if self.__parent is None:
			raise RuntimeError("Node is not inserted to the stage")
		
		if isinstance(self.__parent, Node):
			self.__parent.update_style_request(node, [self.__parent] + path)
		else:
			self.__parent.update_style_request(node, path)
	
	def set_parent(self, node):
		if self.__parent and node:
			raise RuntimeError("Node has already got parent")
		
		self.__parent = node
	
	def get_hovered_node(self, mouse_position):
		return self
	
	def get_parent(self):
		return self.__parent
	
	def get_parent_boundary(self):
		try:
			return self.__parent.boundary
		except AttributeError:
			return NullBoundary()


class Node(InteractiveNode, StageNode):
	def reset(self):
		pass
	
	def repaint(self, surface):
		pass
	
	def update(self):
		pass


class ComplexNode(Node):
	def __init__(self, **kwargs):
		super(ComplexNode, self).__init__(boundary_type=ComplexNodeBoundary, **kwargs)
		
		self.__nodes = []
	
	def reset(self):
		self.update_style()
		
		for node in self.children():
			node.reset()
		
		self.boundary.fit_size_to_children(True)
		self.boundary.reset()
		self.update()
		self.update_layout()
	
	def repaint(self, surface):
		if self["visible"]:
			for node in self.__nodes:
				node.repaint(surface)
	
	def _insert_node(self, node, index=None):
		if not isinstance(node, (SimpleNode, ComplexNode)):
			raise TypeError("Node must be a subclass of rinde.stage.node.ComplexNode or rinde.stage.node.SimpleNode")
		
		if index is None:
			self.__nodes.append(node)
		else:
			self.__nodes.insert(index, node)
		
		node.set_parent(self)
	
	def _remove_node(self, node):
		node.set_parent(None)
		self.__nodes.remove(node)
	
	def update_layout(self):
		pass
	
	def children(self):
		return iter(self.__nodes)
	
	def _debug_lookup_element(self, selector):
		for element in self.__nodes:
			for node_selector in element.appearance.selectors():
				if node_selector == selector:
					return element


class SimpleNode(Node):
	def __init__(self, **kwargs):
		super(SimpleNode, self).__init__(boundary_type=SimpleNodeBoundary, **kwargs)
		
		self.__surface = None
	
	def reset(self):
		self.update_style()
		self.boundary.reset()
		self.update()
	
	def repaint(self, surface):
		if self["visible"]:
			surface.blit(self.__surface, self.absolute_position())
	
	def _set_surface(self, surface):
		self.__surface = surface
	
	def _get_surface(self):
		return self.__surface
	
	def _fit_size_to_surface(self):
		self["size"] = self.__surface.get_size()
