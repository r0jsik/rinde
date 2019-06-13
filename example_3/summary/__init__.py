from rinde.stage import ControllerBase


class Summary(ControllerBase):
	def __init__(self, summary):
		super(Summary, self).__init__()
		
		self.summary = summary
	
	def start(self):
		self.window.center_in_stage(self.nodes["header"], "x")
		self.show_header()
	
	def show_header(self):
		property = self.nodes["header"].properties["position-y"]
		property.animate_to(50, self.show_summary)
	
	def show_summary(self):
		self.nodes["summary"]["records"] = self.summary.items()
		self.nodes["summary"]["visible"] = True
		
		self.window.center_in_stage(self.nodes["summary"], "x")
		self.window.center_in_stage(self.nodes["summary"], "y")
