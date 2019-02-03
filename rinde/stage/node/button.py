from rinde.stage.node.region import Region
from rinde.stage.node.text import Label
from rinde.stage.node.text import Text


class TextButton(Label):
	def __init__(self, action, **kwargs):
		super(TextButton, self).__init__(**kwargs)
		
		self.click = action
		
		self.set_style_name("text-button")


class Button(Region):
	def __init__(self, action, text):
		super(Button, self).__init__()
		
		self.__init_text(text)
		
		self.click = action
		
		self.set_style_name("button")
	
	def __init_text(self, text):
		self.__text = Text(text)
		self.__text.set_style_name("text")
		
		self._insert_node(self.__text)
