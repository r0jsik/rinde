from rinde.stage import ControllerBase
from rinde.stage.animation import AnimationTo


class Summary(ControllerBase):
	def __init__(self, difficulty, checkbox_1, checkbox_2):
		super(Summary, self).__init__()
		
		self.summary = "Difficulty: %s, checkbox_1: %s, checkbox_2: %s" % (difficulty, checkbox_1, checkbox_2)
	
	def start(self):
		self.center_header()
		self.show_header()
	
	def center_header(self):
		window_width, window_height = self.window.get_size()
		
		label = self.nodes["header"]
		label_width = label.get_property("width")
		position = (window_width - label_width)/2
		
		label.set_property("position-x", position)
	
	def show_header(self):
		property = self.nodes["header"].properties["position-y"]
		animation = AnimationTo(property, 50, self.show_summary)
		animation.start()
	
	def show_summary(self):
		self.nodes["summary"].set_property("text", self.summary)
