from rinde.stage.node import ComplexNode
from rinde.stage.node.region import Region
from rinde.stage.node.text import Text


class Field(ComplexNode):
	def __init__(self, text="", placeholder="", **kwargs):
		super(Field, self).__init__(**kwargs)
		
		self.properties.create("text", self.update, text)
		
		self.__init_background()
		self.__init_placeholder(placeholder)
		self.__init_text(text)
	
	def __init_background(self):
		self.__background = Region()
		self.__background.set_style_name("background")
		
		self._insert_node(self.__background)
	
	def __init_placeholder(self, text):
		self.__placeholder = Text(text)
		self.__placeholder.set_style_name("placeholder")
		
		self._insert_node(self.__placeholder)
	
	def __init_text(self, text):
		self.__text = Text(text)
		self.__text.properties.add_trigger("text", self.update)
		
		self._insert_node(self.__text)
	
	def update(self):
		self.__text["text"] = self._get_content_text()
		self.__placeholder["visible"] = (self.__text["text"] == "")
		self.__fit_content_size()
	
	def _get_content_text(self):
		raise NotImplementedError
	
	def __fit_content_size(self):
		offset = self.__text.get_absolute_size("width") - self.__background.get_absolute_size("width")
		
		if offset > 0:
			self.__text.crop_display_surface(offset, 0, self.__text["width"] - offset, self.__text["height"])
	
	def key_pressed(self, code, char):
		if code == 8:
			self["text"] = self["text"][:-1]
		else:
			self["text"] += char


class TextField(Field):
	def __init__(self, **kwargs):
		super(TextField, self).__init__(**kwargs)
		
		self.set_style_name("text-field")
	
	def _get_content_text(self):
		return self["text"]


class PasswordField(Field):
	def __init__(self, **kwargs):
		super(PasswordField, self).__init__(**kwargs)
		
		self.set_style_name("password-field")
	
	def _get_content_text(self):
		return "*" * len(self["text"])
