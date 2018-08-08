from rinde.stage.node import Node
from rinde.stage.util import Canvas
from rinde.stage.util import Image


class ImageView(Node):
	def __init__(self, resource, **kwargs):
		super(ImageView, self).__init__(**kwargs)
		
		self.style_name = "image-view"
		
		self.__content = Image(resource)
	
	def update(self):
		self._set_canvas(self.__content.get())
	
	def resize_content(self, width, height):
		self.__content.resize(width, height)
		self.update()


class CanvasView(Node):
	def __init__(self, width, height, **kwargs):
		super(CanvasView, self).__init__(**kwargs)
		
		self.style_name = "canvas-view"
		
		self.__content = Canvas(width, height)
	
	def update(self):
		self._set_canvas(self.__content.get())
	
	def get_content(self):
		return self.__content
