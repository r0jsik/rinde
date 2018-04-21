from rinde.scene.property import Property
from rinde.scene.property import BooleanProperty
from rinde.scene.util import Fonts
from rinde.scene.util import Image
from rinde.scene.util import Canvas
from rinde.scene.node.util import Boundary
from rinde.scene.node.util import VBoxLayoutComputer
from rinde.scene.node.util import HBoxLayoutComputer
from rinde.error import RindeException


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
	
	def set_size(self, width, height):
		self.set_property("width", width)
		self.set_property("height", height)
	
	def update_position(self):
		self._boundary.update_position()
	
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


class SceneNode(StylizableNode, BoundaryNode):
	def __init__(self, **kwargs):
		super(SceneNode, self).__init__(**kwargs)
		
		self.__nodes = []
		self.__parent = None
	
	def update_style_request(self, node):
		if self.__parent:
			self.__parent.update_style_request(node)  # Scene is at the end of execution chain
		else:
			raise RindeException("Node is not on scene so cannot update style")
	
	def _add_node(self, node):
		node.set_parent(self)
		node.set_boundary_parent(self._boundary)
		self.__nodes.append(node)
	
	def set_parent(self, parent):
		if None not in [self.__parent, parent]:
			raise RindeException("Node has already got parent")
		
		self.__parent = parent
	
	def _remove_node(self, node):
		node.set_parent(None)
		node.set_boundary_parent(None)
		self.__nodes.remove(node)
	
	def get_hovered_node(self, mouse_position):
		return self
	
	def get_nodes(self):
		return self.__nodes


class Node(InteractiveNode, SceneNode):
	def __init__(self, **kwargs):
		super(Node, self).__init__(**kwargs)
		
		self.__canvas = None
		
		self.style_name = "node"
	
	def repaint(self, surface):
		if self.get_property("visible"):
			if self.__canvas:
				surface.blit(self.__canvas, self._boundary.get_absolute_position())
			
			for node in self.get_nodes():
				node.repaint(surface)
	
	def _borrow_property(self, node, property_name):
		property = node.property(property_name)
		property.add_trigger(self.update)
		
		return property
	
	def _create_property(self, trigger, value=None):
		property = Property(value)
		property.add_trigger(trigger)
		
		return property
	
	def reset(self):
		self.update_style_request(self)
		
		for node in self.get_nodes():
			node.reset()
		
		self.update()
	
	def update(self):
		pass
	
	def _set_canvas(self, canvas):
		self.__canvas = canvas
		
		width, height = canvas.get_size()
		self.set_size(width, height)


class Label(Node):
	def __init__(self, text, **kwargs):
		super(Label, self).__init__(**kwargs)
		
		self.style_name = "label"
		
		self._property["text"] = Property(text)
		self._property["font"] = Property()
		self._property["font_size"] = Property()
		
		self.__init_shadow()
		self.__init_face()
	
	def __init_shadow(self):
		shadow = TextDisplay(self)
		
		self._property["shadow_offset_x"] = shadow.property("position_x")
		self._property["shadow_offset_y"] = shadow.property("position_y")
		self._property["shadow_color"] = shadow.property("color")
		self._property["shadow_visible"] = shadow.property("visible")
		
		self._add_node(shadow)
	
	def __init_face(self):
		face = TextDisplay(self)
		
		self._property["color"] = face.property("color")
		
		self._add_node(face)


class TextDisplay(Node):
	def __init__(self, label):
		super(TextDisplay, self).__init__()
		
		self._property["text"] = self._borrow_property(label, "text")
		self._property["font"] = self._borrow_property(label, "font")
		self._property["font_size"] = self._borrow_property(label, "font_size")
		self._property["color"] = self._create_property(self.update)
	
	def update(self):
		text = self.get_property("text")
		color = self.get_property("color")
		font = self.__get_font()
		
		canvas = font.render(text, color)
		self._set_canvas(canvas)
	
	def __get_font(self):
		file = self.get_property("font")
		size = self.get_property("font_size")
		
		return Fonts.get(file, size)


class DraggableLabel(Label):
	def __init__(self, **kwargs):
		super(DraggableLabel, self).__init__(**kwargs)
		
		self.style_name = "draggable-label"
	
	def drag(self, mouse_offset):
		self.property("position_x").increase(mouse_offset[0])
		self.property("position_y").increase(mouse_offset[1])


class TextButton(Label):
	def __init__(self, action, **kwargs):
		super(TextButton, self).__init__(**kwargs)
		
		self.click = action
		self.style_name = "text-button"


class ImageView(Node):
	def __init__(self, resource, **kwargs):
		super(ImageView, self).__init__(**kwargs)
		
		self.style_name = "image-view"
		
		self.__content = Image(resource)
	
	def update(self):
		self._set_canvas(self.__content.get())
	
	def resize_content(self, width, height):
		self.__content.resize(width, height)
		self.update()


class CanvasView(Node):
	def __init__(self, width, height, **kwargs):
		super(CanvasView, self).__init__(**kwargs)
		
		self.style_name = "canvas-view"
		
		self.__content = Canvas(width, height)
	
	def update(self):
		self._set_canvas(self.__content.get())
	
	def get_content(self):
		return self.__content


class Pane(Node):
	def __init__(self, nodes=(), **kwargs):
		super(Pane, self).__init__(**kwargs)
		
		self._property["margin"] = self._boundary.margin()
		self._property["padding"] = self._boundary.padding()
		
		self.style_name = "pane"
		
		map(self._add_node, nodes)
	
	def get_hovered_node(self, mouse_position):
		hovered_node = self
		
		for node in self.get_nodes():
			if node.can_be_hovered(mouse_position):
				hovered_node = node.get_hovered_node(mouse_position)
		
		return hovered_node


class Box(Pane):
	def __init__(self, nodes, align, spacing=0, **kwargs):
		super(Box, self).__init__(nodes, **kwargs)
		
		self._property["spacing"] = self._create_property(self._update_nodes_spacing, spacing)
		self._property["align"] = self._create_property(self._update_nodes_align, align)
	
	def _update_nodes_spacing(self):
		pass
	
	def _update_nodes_align(self):
		pass
	
	def update(self):
		self._update_nodes_spacing()
		self._update_nodes_align()


class VBox(Box):
	def __init__(self, nodes=(), align="left", **kwargs):
		super(VBox, self).__init__(nodes, align, **kwargs)
		
		self.style_name = "vbox"
		
		self.__layout_computer = VBoxLayoutComputer(self)
	
	def _update_nodes_spacing(self):
		self.__layout_computer.update_nodes_spacing("height", "y")
	
	def _update_nodes_align(self):
		self.__layout_computer.update_nodes_align("x")


class HBox(Box):
	def __init__(self, nodes=(), align="top", **kwargs):
		super(HBox, self).__init__(nodes, align, **kwargs)
		
		self.style_name = "hbox"
		
		self.__layout_computer = HBoxLayoutComputer(self)
	
	def _update_nodes_spacing(self):
		self.__layout_computer.update_nodes_spacing("width", "x")
	
	def _update_nodes_align(self):
		self.__layout_computer.update_nodes_align("y")
