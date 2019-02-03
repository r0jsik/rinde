from rinde.stage import ControllerBase


class Controller(ControllerBase):
	def start(self):
		self.display = self.nodes["display"].get_content()
		self.display.fill(0, 0, 0)
	
	def change_color(self):
		r = self.get_slider_value("r")
		g = self.get_slider_value("g")
		b = self.get_slider_value("b")
		
		self.display.fill(r, g, b)
	
	def get_slider_value(self, id):
		return self.nodes[id].get_property("value")
