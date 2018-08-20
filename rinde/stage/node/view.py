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
	def __init__(self, **kwargs):
		super(CanvasView, self).__init__(**kwargs)
		
		self.__reset_content()
		self.__reset_content_when_resized()
		
		self.style_name = "canvas-view"
	
	def __reset_content(self):
		self.__content = Canvas(*self.get_size())
	
	def __reset_content_when_resized(self):
		self.properties.add_trigger("width", self.__reset_content)
		self.properties.add_trigger("height", self.__reset_content)
	
	def update(self):
		self._set_canvas(self.__content.get())
	
	def get_content(self):
		return self.__content
