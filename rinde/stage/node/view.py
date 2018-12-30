from rinde.stage.node import Node
from rinde.stage.node.util import Canvas
from rinde.stage.node.util import Image


class ImageView(Node):
	def __init__(self, resource, **kwargs):
		super(ImageView, self).__init__(**kwargs)
		
		self.__content = Image(resource)
		
		self.set_style_name("image-view")
	
	def update(self):
		self._set_canvas(self.__content.get())
	
	def resize_content(self, width, height):
		self.__content.resize(width, height)
		self.update()


class CanvasView(Node):
	def __init__(self, **kwargs):
		super(CanvasView, self).__init__(**kwargs)
		
		self.__reset_content_when_resized()
		
		self.set_style_name("canvas-view")
	
	def __reset_content_when_resized(self):
		self.properties.add_trigger("width", self.__reset_content)
		self.properties.add_trigger("height", self.__reset_content)
	
	def __reset_content(self):
		width, height = self.get_size()
		self.__content = Canvas(width, height)
		self._set_canvas(self.__content.get())
	
	def update(self):
		self.__reset_content()
		self.redraw()
	
	def redraw(self):
		pass
	
	def get_content(self):
		return self.__content
