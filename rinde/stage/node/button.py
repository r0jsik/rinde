from rinde.stage.node.region import HybridNode
from rinde.stage.node.text import Label
from rinde.stage.node.text import Text


class LabelButton(Label):
	def __init__(self, action, **kwargs):
		super(LabelButton, self).__init__(**kwargs)
		
		self.click = action
		
		self.set_style_name("label-button")


class Button(HybridNode):
	def __init__(self, action, text, **kwargs):
		super(Button, self).__init__(**kwargs)
		
		self.__init_text(text)
		self.__action = action
		
		self.set_style_name("button")
	
	def __init_text(self, text):
		text = Text(text)
		
		self._borrow_property(text, "text")
		self._insert_node(text)
	
	def click(self):
		self.__action()


class ToggleButton(Button):
	def __init__(self, pressed=False, **kwargs):
		super(ToggleButton, self).__init__(**kwargs)
		
		self.appearance.create_state("pressed", pressed)
		
		self.set_style_name("toggle-button")
	
	def click(self):
		self.appearance.state["pressed"].toggle()
		
		super(ToggleButton, self).click()
