from rinde.stage import ControllerBase


class Summary(ControllerBase):
	def __init__(self, form_data):
		super(Summary, self).__init__()
		
		self.form_data = form_data
	
	# Method invoked when stage gets ready
	def start(self):
		self.window.center_in_stage(self.nodes["header"], "x")
		self.show_header()
	
	# This method invokes an animation that shows the header
	def show_header(self):
		
		# Gradually changes 'position-y' property of the header to 50 and shows the summary when finished
		property = self.nodes["header"].properties["position-y"]
		property.animate_to(50, self.show_summary)
	
	# Shows summary
	def show_summary(self):
		
		# Fills content of the table with items from a dictionary
		self.nodes["summary"]["records"] = self.form_data.items()
		
		# Changes visibility of the table (which is hidden by default by the visible="false" attribute in the XML file)
		self.nodes["summary"]["visible"] = True
		
		# Centers table in the stage
		self.window.center_in_stage(self.nodes["summary"], "x")
		self.window.center_in_stage(self.nodes["summary"], "y")
