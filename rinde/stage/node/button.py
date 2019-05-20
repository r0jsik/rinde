from rinde.stage.node.region import ComplexNodeWithBackground
from rinde.stage.node.text import Label
from rinde.stage.node.text import Text


class LabelButton(Label):
	def __init__(self, action, **kwargs):
		super(LabelButton, self).__init__(**kwargs)
		
		self.click = action
		
		self.set_style_name("label-button")


class Button(ComplexNodeWithBackground):
	def __init__(self, action, text="", **kwargs):
		super(Button, self).__init__(**kwargs)
		
		self.__init_text(text)
		
		self.click = action
		self.set_style_name("button")
	
	def __init_text(self, text):
		text = Text(text)
		
		self._borrow_property(text, "text")
		self._insert_node(text)
	
	def update(self):
		self.fit_background_size()
