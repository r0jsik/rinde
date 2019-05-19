from rinde.stage.node import ComplexNode
from rinde.stage.node import SimpleNode
from rinde.stage.node.util import Font


class Text(ComplexNode):
	def __init__(self, text="", **kwargs):
		super(Text, self).__init__(**kwargs)
		
		self.properties.create("text", self.update, text)
		self.properties.create("font", self.update)
		self.properties.create_number("font-size", self.update)
		
		self.__init_display()
		
		self.set_style_name("text")
	
	def __init_display(self):
		self.__display = TextDisplay(self)
		
		self._borrow_property(self.__display, "color")
		self._insert_node(self.__display)
	
	def update(self):
		self.__display.redraw()
	
	def crop_display_surface(self, offset_x, offset_y, width, height):
		self.__display.crop_surface((offset_x, offset_y, width, height))


class TextDisplay(SimpleNode):
	def __init__(self, text):
		super(TextDisplay, self).__init__()
		
		self._borrow_property(text, "text")
		self._borrow_property(text, "font")
		self._borrow_property(text, "font-size")
		
		self.properties.create_number("color", self.redraw)
		
		self.set_style_name("display")
	
	def redraw(self):
		font = Font(self["font"], self["font-size"])
		surface = font.render(self["text"], self["color"])
		
		self._set_surface(surface)
		self._fit_size()
	
	def crop_surface(self, bounds):
		canvas = self._get_surface()
		canvas = canvas.subsurface(bounds)
		
		self._set_surface(canvas)
		self._fit_size()


class Label(Text):
	def __init__(self, **kwargs):
		super(Label, self).__init__(**kwargs)
		
		self.__init_shadow()
		
		self.set_style_name("label")
	
	def __init_shadow(self):
		self.__shadow = TextDisplay(self)
		self.__shadow.set_style_name("shadow")
		
		self._insert_node(self.__shadow, 0)
	
	def update(self):
		super(Label, self).update()
		
		self.__shadow.redraw()


class DraggableLabel(Label):
	def __init__(self, **kwargs):
		super(DraggableLabel, self).__init__(**kwargs)
		
		self.set_style_name("draggable-label")
	
	def drag(self, mouse_offset):
		self["position-x"] += mouse_offset[0]
		self["position-y"] += mouse_offset[1]
