from rinde.stage.node.view import CanvasView


class Region(CanvasView):
	def __init__(self, **kwargs):
		super(Region, self).__init__(**kwargs)
		
		self.properties.create_number("stroke-width", self.redraw)
		self.properties.create_number("stroke-color", self.redraw)
		self.properties.create_number("inside-color", self.redraw)
		self.properties.create_number("radius", self.redraw)
		
		self.set_style_name("region")
	
	def update(self):
		super(Region, self).update()
		
		self.redraw()
	
	def redraw(self):
		inside_color = self.get_property("inside-color")
		bounds = (0, 0, *self.get_size())
		radius = self.get_property("radius")
		stroke_width = self.get_property("stroke-width")
		stroke_color = self.get_property("stroke-color")
		
		canvas = self.get_content()
		canvas.draw_rounded_rect(inside_color, bounds, radius, stroke_width, stroke_color)
