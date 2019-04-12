from rinde.stage import ControllerBase


class Controller(ControllerBase):
	def start(self):
		self.canvas = self.nodes["display"].get_canvas()
		self.canvas.fill(0, 0, 0)
	
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
