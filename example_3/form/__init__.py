from rinde.stage import ControllerBase
from rinde.stage.animation import AnimationTo
from example_3.summary import Summary


class Controller(ControllerBase):
	def start(self):
		self.animations_finished = False
		self.center_header()
	
	def center_header(self):
		window_width, window_height = self.window.get_size()
		
		label = self.nodes["header"]
		label_width = label.get_property("width")
		position = (window_width - label_width)/2
		
		label.set_property("position-x", position)
	
	def confirm(self):
		self.nodes["form"].set_property("enabled", False)
		self.hide_header()
	
	def hide_header(self):
		property = self.nodes["header"].properties["position-y"]
		animation = AnimationTo(property, -40, self.hide_form, 2)
		animation.start()
	
	def hide_form(self):
		property = self.nodes["form"].properties["position-x"]
		animation = AnimationTo(property, -180, self.finish, 2)
		animation.start()
	
	def finish(self):
		self.animations_finished = True
	
	# Multithreaded animations causes that only by main thread can you change the stage
	def update(self):
		if self.animations_finished:
			self.show_summary()
	
	def show_summary(self):
		difficulty = self.groups["difficulty"].get()
		checkbox_1 = self.nodes["checkbox 1"].get_property("selected")
		checkbox_2 = self.nodes["checkbox 2"].get_property("selected")
		summary = Summary(difficulty, checkbox_1, checkbox_2)
		
		self.window.set_stage("summary", summary)
