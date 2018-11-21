from rinde.stage.node import Node
from rinde.stage.node.view import CanvasView


class Region(Node):
	def __init__(self, **kwargs):
		super(Region, self).__init__(**kwargs)
		
		self.properties.create_integer("border-stroke", self.update)
		self.properties.create_integer("border-color", self.update)
		self.properties.create_integer("content-color", self.update)
		
		self.__init_canvas_view()
	
	def __init_canvas_view(self):
		self.__canvas_view = CanvasView()
		
		self._borrow_property(self.__canvas_view, "width")
		self._borrow_property(self.__canvas_view, "height")
		self._insert_node(self.__canvas_view)
	
	def update(self):
		canvas = self.__canvas_view.get_content()
		
		self.__redraw_outer_rect(canvas)
		self.__redraw_inner_rect(canvas)
	
	def __redraw_outer_rect(self, canvas):
		border_color = self.get_property("border-color")
		width, height = self.get_size()
		border_rect = (0, 0, width, height)
		
		canvas.draw_rect(border_color, border_rect, 0)
	
	def __redraw_inner_rect(self, canvas):
		border_stroke = self.get_property("border-stroke")
		content_color = self.get_property("content-color")
		width, height = self.get_size()
		background_rect = (border_stroke, border_stroke, width - 2*border_stroke, height - 2*border_stroke)
		
		canvas.draw_rect(content_color, background_rect, 0)
