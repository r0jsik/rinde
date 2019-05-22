from rinde.stage.node.region import ComplexNodeWithBackground
from rinde.stage.node.text import PlaceholdedText


class Field(ComplexNodeWithBackground):
	def __init__(self, text="", placeholder="", **kwargs):
		super(Field, self).__init__(**kwargs)
		
		self.properties.create("text", self.update, text)
		
		self.__init_placeholded_text(text, placeholder)
	
	def __init_placeholded_text(self, text, placeholder):
		self.__placeholded_text = PlaceholdedText(text, placeholder)
		self.__placeholded_text.postprocess = self.__shit_content
		
		self._borrow_property(self.__placeholded_text, "text", name_as="content-text")
		self._borrow_property(self.__placeholded_text, "placeholder")
		self._insert_node(self.__placeholded_text)
	
	def __shit_content(self, surface):
		width, height = surface.get_size()
		expected_width = self.background["width"] - self.__placeholded_text.boundary.get_space(3, 1)
		bounds = max(0, width - expected_width), 0, min(width, expected_width), height
		
		return surface.subsurface(bounds)
	
	def key_pressed(self, code, char):
		if code == 8:
			self["text"] = self["text"][:-1]
		else:
			self["text"] += char


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
