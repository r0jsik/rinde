from rinde.stage import ControllerBase


class Controller(ControllerBase):
	def start(self):
		self.display = self.nodes["display"].get_content()
		self.display.fill(0, 0, 0)
	
	def change_color(self):
		
		# To get node's property use following command:
		# node[property_name]
		#
		# To set node's property use following command:
		# node[property_name] = value
		
		r = self.nodes["r"]["value"]
		g = self.nodes["g"]["value"]
		b = self.nodes["b"]["value"]
		
		self.display.fill(r, g, b)
