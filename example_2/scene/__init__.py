from rinde.scene import ControllerBase


class Controller(ControllerBase):
	def start(self, window):
		self.__display = self._nodes["display"].get_content()
	
	def change_color(self):
		r = self.__get_slider_value("r")
		g = self.__get_slider_value("g")
		b = self.__get_slider_value("b")
		
		self.__display.fill(r, g, b)
	
	def __get_slider_value(self, id):
		return self._nodes[id].get_value()
