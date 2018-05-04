from rinde.scene.node import Node
from rinde.scene.property import Property
from rinde.scene.util import Font


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
		
		self._insert_node(shadow)
	
	def __init_face(self):
		face = TextDisplay(self)
		
		self._property["color"] = face.property("color")
		
		self._insert_node(face)


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
		
		return Font(file, size)


class DraggableLabel(Label):
	def __init__(self, **kwargs):
		super(DraggableLabel, self).__init__(**kwargs)
		
		self.style_name = "draggable-label"
	
	def drag(self, mouse_offset):
		self.property("position_x").increase(mouse_offset[0])
		self.property("position_y").increase(mouse_offset[1])
