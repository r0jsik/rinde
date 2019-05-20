from rinde.stage.node.region import ComplexNodeWithBackground
from rinde.stage.node.text import PlaceholdedText


class Field(ComplexNodeWithBackground):
	def __init__(self, text="", placeholder="", **kwargs):
		super(Field, self).__init__(**kwargs)
		
		self.properties.create("text", self.update, text)
		
		self.__init_placeholded_text(text, placeholder)
	
	def __init_placeholded_text(self, text, placeholder):
		self.__placeholded_text = PlaceholdedText(text, placeholder)
		self._insert_node(self.__placeholded_text)
	
	def update(self):
		self.__placeholded_text["text"] = self._get_content_text()
		self.__fit_content_size()
	
	def _get_content_text(self):
		raise NotImplementedError
	
	def __fit_content_size(self):
		offset = self.get_absolute_size("width") - self.background.get_absolute_size("width")
		
		if offset > 0:
			self.__placeholded_text.shift_text_surface(offset, 0)
	
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
