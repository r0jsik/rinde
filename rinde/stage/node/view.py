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
	
	def resize(self, width, height):
		self.__content.resize(width, height)
		self.update()
	
	def set_image(self, image):
		self.__content = image
		self.update()


class CanvasView(Node):
	def __init__(self, **kwargs):
		super(CanvasView, self).__init__(**kwargs)
		
		self.__update_when_resized()
		
		self.set_style_name("canvas-view")
	
	def __update_when_resized(self):
		self._add_trigger_to_property("width", self.update)
		self._add_trigger_to_property("height", self.update)
	
	def update(self):
		width, height = self.get_size()
		self.__content = Canvas(width, height)
		self._set_canvas(self.__content.get())
	
	def get_content(self):
		return self.__content
