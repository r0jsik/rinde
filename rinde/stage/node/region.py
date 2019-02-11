from rinde.stage.node.view import CanvasView


class Region(CanvasView):
	def __init__(self, **kwargs):
		super(Region, self).__init__(**kwargs)
		
		self._create_number_property("stroke-width", self.redraw)
		self._create_number_property("stroke-color", self.redraw)
		self._create_number_property("inside-color", self.redraw)
		self._create_number_property("radius", self.redraw)
		
		self.set_style_name("region")
	
	def update(self):
		super(Region, self).update()
		
		self.redraw()
	
	def redraw(self):
		bounds = (0, 0, *self.get_size())
		canvas = self.get_content()
		canvas.draw_rounded_rect(self["inside-color"], bounds, self["radius"], self["stroke-width"], self["stroke-color"])
