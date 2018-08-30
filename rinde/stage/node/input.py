from rinde.stage.node import Node
from rinde.stage.node.text import Text


class TextField(Node):
	def __init__(self, text="", **kwargs):
		super(TextField, self).__init__(**kwargs)
		
		self.__init_background()
		self.__init_content(text)
	
	def __init_background(self):
		pass
	
	def __init_content(self, text):
		self.__content = Text(text)
		self._insert_node(self.__content)
	
	def key_pressed(self, code, char):
		text_property = self.__content.properties["text"]
		text = text_property.get()
		
		if code == 8:
			text = text[:-1]
		else:
			text += char
		
		text_property.set(text)
