from rinde.stage import ControllerBase


class Summary(ControllerBase):
	def __init__(self, *args):
		super(Summary, self).__init__()
		
		self.summary = "username='%s'; password='%s'; difficulty='%s'; checkbox_1='%s'; checkbox_2='%s'" % args
	
	def start(self):
		self.center_header()
		self.show_header()
	
	def center_header(self):
		window_width, window_height = self.window.get_size()
		
		label = self.nodes["header"]
		label["position-x"] = (window_width - label["width"])/2
	
	def show_header(self):
		property = self.nodes["header"].property("position-y")
		property.animate_to(50, self.show_summary)
	
	def show_summary(self):
		self.nodes["summary"]["text"] = self.summary
