from rinde.stage import ControllerBase


# Controller must be a subclass of rinde.stage.ControllerBase
class Controller(ControllerBase):
	
	# Method invoked when stage gets ready
	def start(self):
		
		# self.nodes[ID] returns a reference to the component which is defined in a XML file with an ID attribute
		self.canvas = self.nodes["display"].get_canvas()
		self.change_color()
	
	# Method invoked when the user changes value of any slider with action="change_color" (defined in XML)
	def change_color(self):
		# To get node's property, use the following command:
		# node[property_name]
		#
		# To set node's property, use the following command:
		# node[property_name] = value
		
		r = self.nodes["r"]["value"]
		g = self.nodes["g"]["value"]
		b = self.nodes["b"]["value"]
		
		self.canvas.fill(r, g, b)
