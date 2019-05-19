from rinde.stage import ControllerBase


# Controller must be a subclass of rinde.stage.ControllerBase
class Controller(ControllerBase):
	
	# Method invoked when stage gets ready
	def start(self):
		
		# Access to node with id="button" (defined in XML)
		print("LabelButton: ", self.nodes["button"])
	
	# Method invoked when button with action="say_hello" (defined in XML) is clicked
	def say_hello(self):
		print("Hello")
