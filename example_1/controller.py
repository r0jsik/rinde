from rinde.stage import ControllerBase


# Controller must me subclass of rinde.stage.ControllerBase
class Controller(ControllerBase):
	
	# Method invoked when stage gets ready
	def start(self, window):
		
		# Access to node with id="blabla" (defined in XML)
		print "TextButton: ", self.nodes["blabla"]
	
	# Method invoked when button with action="say_hello" (defined in XML) is clicked
	def say_hello(self):
		print "Hello"
