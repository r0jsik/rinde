from rinde.stage.node import Node
from rinde.stage.node.util import Canvas


class Region(Node):
	def __init__(self, **kwargs):
		super(Region, self).__init__(**kwargs)
		
		self._create_number_property("stroke-width", self.__redraw)
		self._create_number_property("stroke-color", self.__redraw)
		self._create_number_property("inside-color", self.__redraw)
		self._create_number_property("radius", self.__redraw)
		
		self.__update_when_resized()
		
		self.set_style_name("region")
	
	def __update_when_resized(self):
		self._add_trigger_to_property("width", self.update)
		self._add_trigger_to_property("height", self.update)
	
	def update(self):
		self.__update_canvas()
		self.__redraw()
	
	def __update_canvas(self):
		width, height = self.get_size()
		self.__canvas = Canvas(width, height)
		self._set_canvas(self.__canvas.get())
	
	def __redraw(self):
		bounds = (0, 0, *self.get_size())
		self.__canvas.clear()
		self.__canvas.draw_rounded_rect(self["inside-color"], bounds, self["radius"], self["stroke-width"], self["stroke-color"])
