from rinde.stage.node import ComplexNode
from rinde.stage.node import SimpleNode
from rinde.stage.node.util import Canvas


class Region(SimpleNode):
	def __init__(self, **kwargs):
		super(Region, self).__init__(**kwargs)
		
		self.properties.create_number("stroke-width", self.__redraw)
		self.properties.create_number("stroke-color", self.__redraw)
		self.properties.create_number("inside-color", self.__redraw)
		self.properties.create_number("radius", self.__redraw)
		
		self.__update_when_resized()
		
		self.set_style_name("region")
	
	def __update_when_resized(self):
		self.properties.add_trigger("size", self.update)
	
	def update(self):
		self.__update_canvas()
		self.__redraw()
	
	def __update_canvas(self):
		self.__canvas = Canvas(self["width"], self["height"])
		self._set_surface(self.__canvas.get())
	
	def __redraw(self):
		bounds = (0, 0, self["width"], self["height"])
		
		self.__canvas.clear()
		self.__canvas.draw_rounded_rect(self["inside-color"], bounds, self["radius"], self["stroke-width"], self["stroke-color"])
	
	def draw_stroke(self, start, end):
		self.__canvas.draw_line(self["stroke-color"], start, end, self["stroke-width"])


class HybridNode(ComplexNode):
	def __init__(self, **kwargs):
		super(HybridNode, self).__init__(**kwargs)
		
		self.__init_background()
	
	def __init_background(self):
		self.background = Region()
		self.background.set_style_name("background")
		self.background.properties["size"].bind_to(self.properties["size"])
		
		self._insert_node(self.background)
