from rinde.stage.node import Node
from rinde.stage.node.util import Font


class Text(Node):
	def __init__(self, text, **kwargs):
		super(Text, self).__init__(**kwargs)
		
		self.properties.create("text", value=text)
		self.properties.create("font")
		self.properties.create("font-size")
		
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
		self.__shadow = TextDisplay(self)
		
		self.__borrow_shadow_property("position-x", "shadow-offset-x")
		self.__borrow_shadow_property("position-y", "shadow-offset-y")
		self.__borrow_shadow_property("color", "shadow-color")
		self.__borrow_shadow_property("visible", "shadow-visible")
		
		self._insert_node(self.__shadow, 0)
	
	def __borrow_shadow_property(self, name, name_as):
		self.properties.insert(self.__shadow.properties[name], name_as)


class TextDisplay(Node):
	def __init__(self, text):
		super(TextDisplay, self).__init__()
		
		self._borrow_property(text, "text")
		self._borrow_property(text, "font")
		self._borrow_property(text, "font-size")
		
		self.properties.create("color", self.update)
	
	def update(self):
		text = self.get_property("text")
		color = self.get_property("color")
		font = self.__get_font()
		
		canvas = font.render(text, color)
		self._set_canvas(canvas)
	
	def __get_font(self):
		file = self.get_property("font")
		size = self.get_property("font-size")
		
		return Font(file, size)


class DraggableLabel(Label):
	def __init__(self, text, **kwargs):
		super(DraggableLabel, self).__init__(text, **kwargs)
		
		self.set_style_name("draggable-label")
	
	def drag(self, mouse_offset):
		self.properties["position-x"].increase(mouse_offset[0])
		self.properties["position-y"].increase(mouse_offset[1])
