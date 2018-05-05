from rinde.scene.node import Node
from rinde.scene.node.text import Label


class TextField(Node):
	def __init__(self, text="", **kwargs):
		super(TextField, self).__init__(**kwargs)
		
		self.__init_background()
		self.__init_content(text)
	
	def __init_background(self):
		pass
	
	def __init_content(self, text):
		self.__content = Label(text)
		self._insert_node(self.__content)
