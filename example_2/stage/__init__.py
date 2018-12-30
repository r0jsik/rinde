from rinde.stage import ControllerBase


class Controller(ControllerBase):
	def start(self, window):
		self.__display = self.nodes["display"].get_content()
		self.__display.fill(0, 0, 0)
	
	def change_color(self):
		r = self.__get_slider_value("r")
		g = self.__get_slider_value("g")
		b = self.__get_slider_value("b")
		
		self.__display.fill(r, g, b)
	
	def __get_slider_value(self, id):
		return self.nodes[id].get_property("value")
