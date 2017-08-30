from rinde.scene.property import *
from rinde.scene.util import SystemFonts
from rinde.scene.util import CustomFonts
from rinde.data import Resources
from rinde.error import RindeException


class NodeBase(object):
	def __init__(self, id=None, style_class=None):
		self.id = id
		self.style_class = style_class
		self.style_name = None
		self.hovered = self.__create_state_property()
		self.focused = self.__create_state_property()
		self.property = {}
		
		self.__style = None
	
	def __create_state_property(self):
		property = BooleanProperty()
		property.value_changed = self.__update_state
		
		return property
	
	def __update_state(self):
		self.__apply_default_style()
		
		if self.hovered.get():
			self.__apply_style("hover")
		
		if self.focused.get():
			self.__apply_style("focus")
	
	def __apply_default_style(self):
		for property_name in self.property:
			if self.property[property_name].is_changed() and property_name not in self.__style[None]:
				self.property[property_name].default_value()
		
		self.__apply_style(None)
	
	def __apply_style(self, state):
		if state in self.__style:
			for property_name, value in self.__style[state].iteritems():
				self.__set_appearance(property_name, value)
	
	def __set_appearance(self, property_name, value):
		try:
			self.__try_to_set_appearance(property_name, value)
		except KeyError:
			raise RindeException("Unknown property '%s'" % property_name)
	
	def __try_to_set_appearance(self, property_name, value):
		appearance_name = property_name.replace("-", "_")
		appearance = self.property[appearance_name]
		appearance.change(value)
	
	def set_style(self, style):
		self.__style = style
		self.__apply_style(None)
	
	def set_property(self, name, value):
		self.property[name].set(value)
	
	def get_property(self, name):
		return self.property[name].get()


class Boundary(NodeBase):
	def __init__(self, position_x=0, position_y=0, **kwargs):
		super(Boundary, self).__init__(**kwargs)
		
		self.property["position_x"] = self.__create_position_property()
		self.property["position_y"] = self.__create_position_property()
		self.property["width"] = IntegerProperty()
		self.property["height"] = IntegerProperty()
		
		self.__parent_position_x = self.__create_position_property()
		self.__parent_position_y = self.__create_position_property()
		self.__absolute_position = (0, 0)
		
		self.set_position(position_x, position_y)
	
	def __create_position_property(self):
		property = IntegerProperty()
		property.value_changed = self.__update_absolute_position
		
		return property
	
	def __update_absolute_position(self):
		self.__absolute_position = (
			self.get_property("position_x") + self.__parent_position_x.get(),
			self.get_property("position_y") + self.__parent_position_y.get()
		)
	
	def bind_parent_position(self, parent):
		parent_position_x = parent.property["position_x"]
		parent_position_y = parent.property["position_y"]
		
		self.__parent_position_x.bind_to(parent_position_x)
		self.__parent_position_y.bind_to(parent_position_y)
		self.__update_absolute_position()
	
	def unbind_parent_position(self):
		self.__parent_position_x.unbind()
		self.__parent_position_y.unbind()
	
	def bind_size(self, boundary):
		self.__bind_width(boundary)
		self.__bind_height(boundary)
	
	def __bind_width(self, boundary):
		width = self.property["width"]
		boundary_width = boundary.property["width"]
		width.bind_to(boundary_width, True)
	
	def __bind_height(self, boundary):
		height = self.property["height"]
		boundary_height = boundary.property["height"]
		height.bind_to(boundary_height, True)
	
	def unbind_size(self):
		self.property["width"].unbind()
		self.property["height"].unbind()
	
	def is_mouse_over(self, mouse_position):
		if self.get_property("width") > mouse_position[0] - self.get_property("position_x") > 0:
			if self.get_property("height") > mouse_position[1] - self.get_property("position_y") > 0:
				return True
		
		return False
	
	def set_position(self, position_x, position_y):
		self.set_property("position_x", position_x)
		self.set_property("position_y", position_y)
	
	def get_position(self):
		position_x = self.get_property("position_x")
		position_y = self.get_property("position_y")
		
		return position_x, position_y
	
	def set_size(self, width, height):
		self.set_property("width", width)
		self.set_property("height", height)
	
	def get_size(self):
		width = self.get_property("width")
		height = self.get_property("height")
		
		return width, height
	
	def get_absolute_position(self):
		return self.__absolute_position


class Node(Boundary):
	def __init__(self, **kwargs):
		super(Node, self).__init__(**kwargs)
		
		self.__nodes = []
		self.__canvas = None
		self.__parent = None
	
	def hover(self):
		self.hovered.true()
	
	def leave(self):
		self.hovered.false()
	
	def focus(self):
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
		if self.__canvas:
			surface.blit(self.__canvas, self.get_absolute_position())
		
		for node in self.__nodes:
			node.repaint(surface)
	
	def _create_updating_property(self, value=None):
		property = Property(value)
		property.value_changed = self.update
		
		return property
	
	def update(self):
		pass
	
	def update_style(self):
		self.update_style_request(self)
		
		for node in self.__nodes:
			node.update_style()
	
	def update_style_request(self, node):
		try:
			self.__parent.update_style_request(node) #Scene is at the end of chain
		except AttributeError:
			raise RindeException("Node is not on scene so cannot update style")
	
	def _add_node(self, node):
		node.set_parent(self)
		node.bind_parent_position(self)
		self.__nodes.append(node)
	
	def _remove_node(self, node):
		node.set_parent(None)
		node.unbind_parent_position()
		self.__nodes.remove(node)
	
	def _set_canvas(self, canvas):
		size = canvas.get_size()
		self.set_size(*size)
		
		self.__canvas = canvas.convert_alpha()
	
	def get_hovered_node(self, mouse_position):
		last_hovered_node = None
		
		for node in self.__nodes:
			if node.is_mouse_over(mouse_position):
				last_hovered_node = node
		
		return last_hovered_node
	
	def set_parent(self, parent):
		self.__parent = parent


class FlatNode(Node):
	def get_hovered_node(self, mouse_position):
		return None


class TextDisplay(FlatNode):
	def __init__(self, text_property, font_property, font_size_property, color):
		super(TextDisplay, self).__init__()
		
		self.__text_property = self._create_updating_property()
		self.__text_property.bind_to(text_property)
		
		self.__font_property = self._create_updating_property()
		self.__font_property.bind_to(font_property)
		
		self.__font_size_property = self._create_updating_property()
		self.__font_size_property.bind_to(font_size_property)
		
		self.property["color"] = self._create_updating_property(color)
		self.update()
	
	def update(self):
		text = self.__text_property.get()
		font = self.__font_property.get()
		color = self.get_property("color")
		
		canvas = font.render(text, color)
		self._set_canvas(canvas)


class Label(FlatNode):
	DEFAULT_FONT_FILE = Resources.get_path("Roboto Condensed Regular.ttf")
	DEFAULT_FONT_SIZE = 32
	DEFAULT_SHADOW_COLOR = 0x111111
	DEFAULT_FACE_COLOR = 0x80FF80
	
	def __init__(self, text, **kwargs):
		super(Label, self).__init__(**kwargs)
		
		self.property["text"] = self._create_updating_property(text)
		self.property["font"] = self.__create_font_property()
		self.property["font_size"] = self._create_updating_property()
		
		self.__init_shadow()
		self.__init_face()
		self.bind_size(self.__face)
		
		self.style_name = "label"
	
	def __create_font_property(self):
		font = CustomFonts.get(self.DEFAULT_FONT_FILE, self.DEFAULT_FONT_SIZE)
		property = self._create_updating_property(font)
		
		return property
	
	def __init_shadow(self):
		self.__shadow = self.__create_text_display(self.DEFAULT_SHADOW_COLOR)
		self.__shadow.set_position(1, 1)
		self._add_node(self.__shadow)
		
		self.__add_shadow_properties()
	
	def __create_text_display(self, color):
		text_property = self.property["text"]
		font_property = self.property["font"]
		font_size_property = self.property["font_size"]
		
		text_display = TextDisplay(text_property, font_property, font_size_property, color)
		
		return text_display
	
	def __add_shadow_properties(self):
		self.property["shadow_offset_x"] = self.__shadow.property["position_x"]
		self.property["shadow_offset_y"] = self.__shadow.property["position_y"]
		self.property["shadow_color"] = self.__shadow.property["color"]
	
	def __init_face(self):
		self.__face = self.__create_text_display(self.DEFAULT_FACE_COLOR)
		self._add_node(self.__face)
		
		self.__add_face_properties()
	
	def __add_face_properties(self):
		self.property["color"] = self.__face.property["color"]
	
	def update(self):
		self.__shadow.update()
		self.__face.update()


class DraggableLabel(Label):
	def __init__(self, text, **kwargs):
		super(DraggableLabel, self).__init__(text, **kwargs)
		
		self.style_name = "draggable-label"
	
	def drag(self, mouse_offset):
		self.property["position_x"].increase(mouse_offset[0])
		self.property["position_y"].increase(mouse_offset[1])


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
