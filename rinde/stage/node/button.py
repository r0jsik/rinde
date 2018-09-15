from rinde.stage.node.text import Label


class TextButton(Label):
	def __init__(self, action, **kwargs):
		super(TextButton, self).__init__(**kwargs)
		
		self.click = action
		
		self.set_style_name("text-button")
