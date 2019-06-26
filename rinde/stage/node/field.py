from rinde.script import shift_surface
from rinde.script import text_lines
from rinde.stage.node.region import HybridNode
from rinde.stage.node.text import PlaceholdedText


class KeyboardInput(HybridNode):
	def __init__(self, **kwargs):
		super(KeyboardInput, self).__init__(**kwargs)
	
	def key_pressed(self, code, char):
		if code == 8:
			self["text"] = self["text"][:-1]
		else:
			self["text"] += char


class Field(KeyboardInput):
	def __init__(self, text="", placeholder="", **kwargs):
		super(Field, self).__init__(**kwargs)
		
		self.properties.create("text", self.update, text)
		
		self.__init_placeholded_text(text, placeholder)
	
	def __init_placeholded_text(self, text, placeholder):
		self.__placeholded_text = PlaceholdedText(text, placeholder)
		self.__placeholded_text.postprocess = self.__shift_content
		
		self._borrow_property(self.__placeholded_text, "text", name_as="content-text")
		self._borrow_property(self.__placeholded_text, "placeholder")
		self._insert_node(self.__placeholded_text)
	
	def __shift_content(self, surface):
		return shift_surface.shift_x(surface, self.background["width"] - self.__placeholded_text.boundary.get_space(3, 1))


class TextField(Field):
	def __init__(self, **kwargs):
		super(TextField, self).__init__(**kwargs)
		
		self.set_style_name("text-field")
	
	def update(self):
		self["content-text"] = self["text"]


class PasswordField(Field):
	def __init__(self, **kwargs):
		super(PasswordField, self).__init__(**kwargs)
		
		self.set_style_name("password-field")
	
	def update(self):
		self["content-text"] = "*" * len(self["text"])


class TextArea(KeyboardInput):
	def __init__(self, text="", placeholder="", **kwargs):
		super(TextArea, self).__init__(**kwargs)
		
		self.__init_placeholded_text(text, placeholder)
		
		self.set_style_name("text-area")
	
	def __init_placeholded_text(self, text, placeholder):
		self.__placeholded_text = PlaceholdedText(text, placeholder)
		self.__placeholded_text.render = self.__render_wrapped_text
		self.__placeholded_text.postprocess = self.__shift_content
		
		self._borrow_property(self.__placeholded_text, "text")
		self._borrow_property(self.__placeholded_text, "placeholder")
		self._insert_node(self.__placeholded_text)
	
	def __render_wrapped_text(self, font):
		text = self.__placeholded_text["text"]
		width = self.background["width"] - self.__placeholded_text.boundary.get_space(3, 1)
		
		if text == "":
			text, color = self.__placeholded_text["placeholder"], self.__placeholded_text["placeholder-color"]
		else:
			color = self.__placeholded_text["color"]
		
		return text_lines.render(text_lines.truncate_to_width(text, font.pygame(), width), font, color)
	
	def __shift_content(self, surface):
		return shift_surface.shift_y(surface, self.background["height"] - self.__placeholded_text.boundary.get_space(2, 0))
