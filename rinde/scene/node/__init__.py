from rinde.scene.property import *
from rinde.scene.util import Fonts
from rinde.scene.util import Image
from rinde.error import RindeException


class NodeBase(object):
	def __init__(self, id=None, style_class=None):
		self.id = id
		self.style_class = style_class
		self.style_name = None
		self.hovered = self.__create_state_property()
		self.focused = self.__create_state_property()
		
		self._property = {}
		self.__style = None
	
	def __create_state_property(self):
		property = BooleanProperty()
		property.value_changed = self.__update_state
		
		return property
	
	def __update_state(self):
		self.__apply_style(None)
		
		if self.hovered.get():
			self.__apply_style("hover")
		
		if self.focused.get():
			self.__apply_style("focus")
	
	def __apply_style(self, state):
		if state in self.__style:
			for property_name, value in self.__style[state].iteritems():
				self.set_property(property_name, value)
	
	def set_property(self, name, value):
		self.property(name).set(value)
	
	def property(self, name):
		try:
			return self._property[name]
		except KeyError:
			raise RindeException("Unknown property: '%s'" % name)
	
	def get_property(self, name):
		return self.property(name).get()
	
	def set_style(self, style):
		self.__style = style
		
		for property_name, value in style[None].iteritems():
			self._property[property_name].reset(value)


class Boundary(NodeBase):
	def __init__(self, position_x=0, position_y=0, **kwargs):
		super(Boundary, self).__init__(**kwargs)
		
		self._property["position_x"] = self.__create_position_property()
		self._property["position_y"] = self.__create_position_property()
		self._property["width"] = IntegerProperty()
		self._property["height"] = IntegerProperty()
		
		self.__parent_position_x = self.__create_position_property()
		self.__parent_position_y = self.__create_position_property()
		self.__absolute_position_x = self.__create_position_property()
		self.__absolute_position_y = self.__create_position_property()
		
		self.set_position(position_x, position_y)
	
	def __create_position_property(self):
		property = IntegerProperty()
		property.value_changed = self.update_absolute_position
		
		return property
	
	def update_absolute_position(self):
		absolute_position_x = self.get_property("position_x") + self.__parent_position_x.get()
		absolute_position_y = self.get_property("position_y") + self.__parent_position_y.get()
		
		self.__absolute_position_x.set(absolute_position_x)
		self.__absolute_position_y.set(absolute_position_y)
	
	def bind_parent_position(self, parent):
		self.__parent_position_x.bind_to(parent.__absolute_position_x)
		self.__parent_position_y.bind_to(parent.__absolute_position_y)
		self.update_absolute_position()
	
	def unbind_parent_position(self):
		self.__parent_position_x.unbind()
		self.__parent_position_y.unbind()
	
	def bind_size(self, boundary):
		width = boundary.property("width")
		height = boundary.property("height")
		
		self.property("width").bind_to(width)
		self.property("height").bind_to(height)
	
	def unbind_size(self):
		self.property("width").unbind()
		self.property("height").unbind()
	
	def is_mouse_over(self, mouse_position):
		if self.get_property("width") > mouse_position[0] - self.__absolute_position_x.get() > 0:
			if self.get_property("height") > mouse_position[1] - self.__absolute_position_y.get() > 0:
				return True
		
		return False
	
	def set_position(self, position_x, position_y):
		self.set_property("position_x", position_x)
		self.set_property("position_y", position_y)
	
	def get_position(self):
		return self.get_property("position_x"), self.get_property("position_y")
	
	def set_size(self, width, height):
		self.set_property("width", width)
		self.set_property("height", height)
	
	def get_size(self):
		return self.get_property("width"), self.get_property("height")
	
	def get_absolute_position(self):
		return self.__absolute_position_x.get(), self.__absolute_position_y.get()


class Node(Boundary):
	def __init__(self, **kwargs):
		super(Node, self).__init__(**kwargs)
		
		self.__canvas = None
		self.__parent = None
		
		self._nodes = []
		self._property["visible"] = BooleanProperty(True)
		self._property["enabled"] = BooleanProperty(True)
	
	def hover(self):
		if self.get_property("enabled"):
			self.hovered.true()
	
	def leave(self):
		self.hovered.false()
	
	def focus(self):
		if self.get_property("enabled"):
			self.focused.true()
	
	def unfocus(self):
		self.focused.false()
	
	def drag(self, mouse_offset):
		pass
	
	def click(self):
		pass
	
	def scroll_up(self):
		pass
	
	def scroll_down(self):
		pass
	
	def repaint(self, surface):
		if self.get_property("visible"):
			if self.__canvas:
				surface.blit(self.__canvas, self.get_absolute_position())
			
			for node in self._nodes:
				node.repaint(surface)
	
	def _create_updating_property(self, value=None):
		property = Property(value)
		property.value_changed = self.update
		
		return property
	
	def update(self):
		pass
	
	def reset(self):
		self.update_style_request(self)
		self.update_absolute_position()
		
		for node in self._nodes:
			node.reset()
		
		self.update()
	
	def update_style_request(self, node):
		try:
			self.__parent.update_style_request(node) #Scene is at the end of chain
		except AttributeError:
			raise RindeException("Node is not on scene so cannot update style")
	
	def _add_node(self, node):
		node.set_parent(self)
		node.bind_parent_position(self)
		self._nodes.append(node)
	
	def _remove_node(self, node):
		node.set_parent(None)
		node.unbind_parent_position()
		self._nodes.remove(node)
	
	def _set_canvas(self, canvas):
		self.__canvas = canvas
		
		size = canvas.get_size()
		self.set_size(*size)
	
	def get_hovered_node(self, mouse_position):
		last_hovered_node = None
		
		for node in self._nodes:
			if node.is_mouse_over(mouse_position):
				last_hovered_node = node
		
		return last_hovered_node
	
	def set_parent(self, parent):
		self.__parent = parent


class FlatNode(Node):
	def get_hovered_node(self, mouse_position):
		return None


class TextDisplay(FlatNode):
	def __init__(self, label):
		super(TextDisplay, self).__init__()
		
		self.__text_property = self.__create_label_property(label, "text")
		self.__font_property = self.__create_label_property(label, "font")
		self.__font_size_property = self.__create_label_property(label, "font_size")
		
		self._property["color"] = self._create_updating_property()
	
	def __create_label_property(self, label, property_name):
		property = label.property(property_name)
		
		label_property = self._create_updating_property()
		label_property.bind_to(property)
		
		return label_property
	
	def update(self):
		text = self.__text_property.get()
		font = self.__get_font()
		color = self.get_property("color")
		
		canvas = font.render(text, color)
		self._set_canvas(canvas)
	
	def __get_font(self):
		file = self.__font_property.get()
		size = self.__font_size_property.get()
		
		return Fonts.get(file, size)


class Label(FlatNode):
	def __init__(self, text, **kwargs):
		super(Label, self).__init__(**kwargs)
		
		text = str(text)
		
		self._property["text"] = self._create_updating_property(text)
		self._property["font"] = self._create_updating_property()
		self._property["font_size"] = self._create_updating_property()
		
		self.__init_shadow()
		self.__init_face()
		self.bind_size(self.__face)
		
		self.style_name = "label"
	
	def __init_shadow(self):
		self.__shadow = TextDisplay(self)
		self.__add_shadow_properties()
		self._add_node(self.__shadow)
	
	def __add_shadow_properties(self):
		self._property["shadow_offset_x"] = self.__shadow.property("position_x")
		self._property["shadow_offset_y"] = self.__shadow.property("position_y")
		self._property["shadow_color"] = self.__shadow.property("color")
		self._property["shadow_visible"] = self.__shadow.property("visible")
	
	def __init_face(self):
		self.__face = TextDisplay(self)
		self.__add_face_properties()
		self._add_node(self.__face)
	
	def __add_face_properties(self):
		self._property["color"] = self.__face.property("color")
	
	def update(self):
		self.__shadow.update()
		self.__face.update()


class DraggableLabel(Label):
	def __init__(self, text, **kwargs):
		super(DraggableLabel, self).__init__(text, **kwargs)
		
		self.style_name = "draggable-label"
	
	def drag(self, mouse_offset):
		self.property("position_x").increase(mouse_offset[0])
		self.property("position_y").increase(mouse_offset[1])


class TextButton(Label):
	def __init__(self, text, action, **kwargs):
		super(TextButton, self).__init__(text, **kwargs)
		
		self.__action = action
		
		self.style_name = "text-button"
	
	def click(self):
		try:
			self.__action()
		except TypeError:
			raise RindeException("Action method cannot take any extra argument")


class ImageView(FlatNode):
	def __init__(self, resource, **kwargs):
		super(ImageView, self).__init__(**kwargs)
		
		self.__create_image_property(resource)
		
		self.style_name = "image-view"
	
	def __create_image_property(self, resource):
		image = Image(resource)
		self._property["image"] = self._create_updating_property(image)
	
	def update(self):
		image = self.get_property("image")
		image = image.get()
		
		self._set_canvas(image)


class Pane(Node):
	def __init__(self, nodes, **kwargs):
		super(Pane, self).__init__(**kwargs)
		
		map(self._add_node, nodes)


class VBox(Pane):
	def __init__(self, nodes, align="left", spacing=0, **kwargs):
		super(VBox, self).__init__(nodes, **kwargs)
		
		self._property["align"] = self._create_updating_property(align)
		self._property["spacing"] = self._create_updating_property(spacing)
		
		self.style_name = "vbox"
	
	def update(self):
		self.__update_width()
		self.__update_height()
		self.__update_nodes_positions()
	
	def __update_width(self):
		max_node_width = 0
		
		for node in self._nodes:
			node_width = node.get_property("width")
			
			if node_width > max_node_width:
				max_node_width = node_width
		
		self.set_property("width", max_node_width)
	
	def __update_height(self):
		total_height = 0
		
		for node in self._nodes:
			total_height += node.get_property("height") + self.get_property("spacing")
		
		self.set_property("height", total_height)
	
	def __update_nodes_positions(self):
		position_y = 0
		
		for index, node in enumerate(self._nodes):
			position_x = self.__compute_node_position_x(node)
			
			node.set_position(position_x, position_y)
			
			position_y += node.get_property("height") + self.get_property("spacing")
	
	def __compute_node_position_x(self, node):
		align = self.get_property("align")
		
		if align == "left":
			return 0
		
		if align == "center":
			return (self.get_property("width") - node.get_property("width"))/2
		
		if align == "right":
			return self.get_property("width") - node.get_property("width")
		
		raise RindeException("Unknown alignment: '%s'" % align)
