from rinde.stage import ControllerBase
from example_3.summary import Summary


class Controller(ControllerBase):
	def start(self):
		window_width, window_height = self.window.get_size()
		
		label = self.nodes["header"]
		label["position-x"] = (window_width - label["width"])/2
	
	def confirm(self):
		self.nodes["form"]["enabled"] = False
		self.hide_header()
	
	def hide_header(self):
		property = self.nodes["header"].property("position-y")
		property.animate_to(-40, self.hide_form)
	
	def hide_form(self):
		property = self.nodes["form"].property("position-x")
		property.animate_by(-210, self.show_summary, 3)
	
	def show_summary(self):
		difficulty = self.groups["difficulty"]
		checkbox_1 = self.nodes["checkbox 1"]["selected"]
		checkbox_2 = self.nodes["checkbox 2"]["selected"]
		summary = Summary(difficulty, checkbox_1, checkbox_2)
		
		self.window.set_stage("summary", summary)
