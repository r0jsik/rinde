from rinde.stage.node import SimpleNode
from rinde.stage.node.util import Canvas
from rinde.stage.node.util import Image


class ImageView(SimpleNode):
	def __init__(self, resource, **kwargs):
		super(ImageView, self).__init__(**kwargs)
		
		self.__content = Image(resource)
		
		self.set_style_name("image-view")
	
	def update(self):
		self._set_surface(self.__content.get())
		self._fit_size()
	
	def set_image(self, image):
		self.__content = image
		self.update()
	
	def get_image(self):
		return self.__content


class CanvasView(SimpleNode):
	def __init__(self, width, height, **kwargs):
		super(CanvasView, self).__init__(**kwargs)
		
		self.__content = Canvas(int(width), int(height))
		
		self.set_style_name("canvas-view")
	
	def update(self):
		self._set_surface(self.__content.get())
		self._fit_size()
	
	def set_canvas(self, canvas):
		self.__content = canvas
		self.update()
	
	def get_canvas(self):
		return self.__content
