from rinde.stage import ControllerBase
from example_3.summary import Summary


# Controller must be a subclass of rinde.stage.ControllerBase
class Controller(ControllerBase):
	
	# Method invoked when stage gets ready
	def start(self):
		
		# It is possible to center the direct child of the stage in that way:
		self.window.center_in_stage(self.nodes["header"], "x")
	
	# Method invoked when button with action="confirm" (defined in XML) is clicked
	def confirm(self):
		
		# Disables the form component to prevent the user from editing its content during animation
		self.nodes["form"]["enabled"] = False
		
		# Starts the first animation
		self.hide_header()
	
	# This method invokes an animation which gradually hides header
	def hide_header(self):
		
		# Gradually changes 'position-y' property of the header to -40 and invokes next animation when finished
		property = self.nodes["header"].properties["position-y"]
		property.animate_to(-40, self.hide_form)
	
	# This method invokes an animation which gradually hides form
	def hide_form(self):
		
		# Gradually changes 'position-x' property of the form to -220 with triple speed and shows a summary when finished
		property = self.nodes["form"].properties["position-x"]
		property.animate_by(-220, self.show_summary, 3)
	
	# This method creates new Summary object and changes stage of the window
	def show_summary(self):
		
		# To get text from the field with id="field_id" (defined in XML), use the following command:
		# self.nodes["field_id"]["text"]
		#
		# To get name of the selected item in the group (like RadioSwitch), use the following command:
		# self.groups["group_name"].get_selected_name()
		# Notice, that every node that belongs to the group has to define group="group_name" attribute in the XML file
		
		controller = Summary({
			"Username": self.nodes["username"]["text"],
			"Password": self.nodes["password"]["text"],
			"Diffiulty": self.groups["difficulty"].get_selected_name(),
			"CheckSwitch 1": self.nodes["checkbox 1"]["selected"],
			"CheckSwitch 2": self.nodes["checkbox 2"]["selected"],
			"Option": self.groups["options"].get_selected_name()
		})
		
		# Changes stage of the window to the new one, built from the 'summary' directory, with a custom controller
		self.window.set_stage("summary", controller)
