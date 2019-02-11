from rinde.stage.node import Node
from rinde.stage.node.util import Font


class Text(Node):
	def __init__(self, text, **kwargs):
		super(Text, self).__init__(**kwargs)
		
		self._create_property("text", value=text)
		self._create_property("font")
		self._create_number_property("font-size")
		
		self.__init_display()
		
		self.set_style_name("text")
	
	def __init_display(self):
		display = TextDisplay(self)
		
		self._borrow_property(display, "color")
		self._insert_node(display)


class Label(Text):
	def __init__(self, text, **kwargs):
		super(Label, self).__init__(text, **kwargs)
		
		self.__init_shadow()
		
		self.set_style_name("label")
	
	def __init_shadow(self):
		shadow = TextDisplay(self)
		shadow.set_style_name("shadow")
		
		self._insert_node(shadow, 0)


class TextDisplay(Node):
	def __init__(self, text):
		super(TextDisplay, self).__init__()
		
		self._borrow_property(text, "text", self.update)
		self._borrow_property(text, "font", self.update)
		self._borrow_property(text, "font-size", self.update)
		
		self._create_number_property("color", self.update)
		
		self.set_style_name("display")
	
	def update(self):
		font = Font(self["font"], self["font-size"])
		canvas = font.render(self["text"], self["color"])
		self._set_canvas(canvas)


class DraggableLabel(Label):
	def __init__(self, **kwargs):
		super(DraggableLabel, self).__init__(**kwargs)
		
		self.set_style_name("draggable-label")
	
	def drag(self, mouse_offset):
		self["position-x"] += mouse_offset[0]
		self["position-y"] += mouse_offset[1]
