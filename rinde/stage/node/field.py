from rinde.stage.node import Node
from rinde.stage.node.region import Region
from rinde.stage.node.text import Text


class Field(Node):
	def __init__(self, text="", **kwargs):
		super(Field, self).__init__(**kwargs)
		
		self._create_property("text", self.update, text)
		
		self.__init_background()
		self.__init_content(text)
	
	def __init_background(self):
		self.__background = Region()
		self.__background.set_style_name("background")
		
		self._insert_node(self.__background)
	
	def __init_content(self, text):
		self.__content = Text(text)
		
		self._borrow_property(self.__content, "text", name_as="content-text")
		self._insert_node(self.__content)
	
	def key_pressed(self, code, char):
		self.__update_text_property(code, char)
		self.__fit_content_size()
	
	def __update_text_property(self, code, char):
		if code == 8:
			self["text"] = self["text"][:-1]
		else:
			self["text"] += char
	
	def __fit_content_size(self):
		offset = self.__content.get_absolute_size("width") - self.__background.get_absolute_size("width")
		
		if offset > 0:
			width = self.__background["width"] - self.__content.get_absolute_size("width") + self.__content["width"]
			height = self.__background["height"] - self.__content.get_absolute_size("height") + self.__content["height"]
			
			self.__content._crop_display_canvas(offset, 0, width, height)


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
