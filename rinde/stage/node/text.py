from rinde.stage.node import ComplexNode
from rinde.stage.node import SimpleNode
from rinde.stage.node.util import Font


class Text(ComplexNode):
	def __init__(self, text="", **kwargs):
		super(Text, self).__init__(**kwargs)
		
		self.properties.create("text", value=text)
		self.properties.create("font")
		self.properties.create_number("font-size")
		
		self.__init_display()
		
		self.set_style_name("text")
	
	def __init_display(self):
		self.__display = TextDisplay(self)
		
		self.borrow_property(self.__display, "color")
		self._insert_node(self.__display)
	
	def crop_display_surface(self, offset_x, offset_y, width, height):
		self.__display.crop_surface((offset_x, offset_y, width, height))


class Label(Text):
	def __init__(self, **kwargs):
		super(Label, self).__init__(**kwargs)
		
		self.__init_shadow()
		
		self.set_style_name("label")
	
	def __init_shadow(self):
		shadow = TextDisplay(self)
		shadow.set_style_name("shadow")
		
		self._insert_node(shadow, 0)


class TextDisplay(SimpleNode):
	def __init__(self, text):
		super(TextDisplay, self).__init__()
		
		self.borrow_property(text, "text", self.update)
		self.borrow_property(text, "font", self.update)
		self.borrow_property(text, "font-size", self.update)
		
		self.properties.create_number("color", self.update)
		
		self.set_style_name("display")
	
	def update(self):
		font = Font(self["font"], self["font-size"])
		surface = font.render(self["text"], self["color"])
		
		self._set_surface(surface)
		self._fit_size()
	
	def crop_surface(self, bounds):
		canvas = self._get_surface()
		canvas = canvas.subsurface(bounds)
		
		self._set_surface(canvas)
		self._fit_size()


class DraggableLabel(Label):
	def __init__(self, **kwargs):
		super(DraggableLabel, self).__init__(**kwargs)
		
		self.set_style_name("draggable-label")
	
	def drag(self, mouse_offset):
		self["position-x"] += mouse_offset[0]
		self["position-y"] += mouse_offset[1]
