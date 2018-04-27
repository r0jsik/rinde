from rinde.scene import ControllerBase


class Controller(ControllerBase):
	def start(self, window):
		
		# Access to node with id="blabla" (ID is defined in XML)
		print "TextButton: ", self._nodes["blabla"]
	
	# Method invoked when button with action="say_hello" (defined in XML) is clicked
	def say_hello(self):
		print "Hello"
