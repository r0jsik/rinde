from rinde.stage.node import Node
from rinde.stage.property import Property
from rinde.stage.util import Font


class Text(Node):
	def __init__(self, text, **kwargs):
		super(Text, self).__init__(**kwargs)
		
		self._property["text"] = Property(text)
		self._property["font"] = Property()
		self._property["font_size"] = Property()
		
		self.__init_display()
		
		self.style_name = "text"
	
	def __init_display(self):
		display = TextDisplay(self)
		
		self._property["color"] = display.property("color")
		
		self._insert_node(display)


class Label(Text):
	def __init__(self, text, **kwargs):
		super(Label, self).__init__(text, **kwargs)
		
		self.__init_shadow()
		
		self._nodes = self._nodes[::-1]
		
		self.style_name = "label"
	
	def __init_shadow(self):
		shadow = TextDisplay(self)
		
		self._property["shadow_offset_x"] = shadow.property("position_x")
		self._property["shadow_offset_y"] = shadow.property("position_y")
		self._property["shadow_color"] = shadow.property("color")
		self._property["shadow_visible"] = shadow.property("visible")
		
		self._insert_node(shadow)


class TextDisplay(Node):
	def __init__(self, text):
		super(TextDisplay, self).__init__()
		
		self._property["text"] = self._borrow_property(text, "text")
		self._property["font"] = self._borrow_property(text, "font")
		self._property["font_size"] = self._borrow_property(text, "font_size")
		self._property["color"] = self._create_integer_property(self.update)
	
	def update(self):
		text = self.get_property("text")
		color = self.get_property("color")
		font = self.__get_font()
		
		canvas = font.render(text, color)
		self._set_canvas(canvas)
	
	def __get_font(self):
		file = self.get_property("font")
		size = self.get_property("font_size")
		
		return Font(file, size)


class DraggableLabel(Label):
	def __init__(self, **kwargs):
		super(DraggableLabel, self).__init__(**kwargs)
		
		self.style_name = "draggable-label"
	
	def drag(self, mouse_offset):
		self.property("position_x").increase(mouse_offset[0])
		self.property("position_y").increase(mouse_offset[1])
