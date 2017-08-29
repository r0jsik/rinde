from rinde.scene import ControllerBase


class Controller(ControllerBase):
	def start(self, window):
		print self.nodes["blabla"] #Access to node with id="blabla" (id is defined in XML)
	
	#Method invoked when button with action="say_hello" (defined in XML) is clicked
	def say_hello(self):
		print "Hello"
