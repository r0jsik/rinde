from rinde.stage import ControllerBase
from example_3.summary import Summary


class Controller(ControllerBase):
	def start(self):
		self.window.center_in_stage(self.nodes["header"], "x")
	
	def confirm(self):
		self.nodes["form"]["enabled"] = False
		self.hide_header()
	
	def hide_header(self):
		property = self.nodes["header"].properties["position-y"]
		property.animate_to(-40, self.hide_form)
	
	def hide_form(self):
		property = self.nodes["form"].properties["position-x"]
		property.animate_by(-220, self.show_summary, 3)
	
	def show_summary(self):
		summary = Summary({
			"Username": self.nodes["username"]["text"],
			"Password": self.nodes["password"]["text"],
			"Diffiulty": self.groups["difficulty"].get_selected_name(),
			"Checkbox 1": self.nodes["checkbox 1"]["selected"],
			"Checkbox 2": self.nodes["checkbox 2"]["selected"],
			"Option": self.groups["options"].get_selected_name()
		})
		
		self.window.set_stage("summary", summary)
