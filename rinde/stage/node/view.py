from rinde.stage.node import Node
from rinde.stage.node.util import Canvas
from rinde.stage.node.util import Image


class View(Node):
	def __init__(self, content, **kwargs):
		super(View, self).__init__(**kwargs)
		
		self.__content = content
	
	def update(self):
		self._set_canvas(self.__content.get())
		self._fit_size()
	
	def set_content(self, canvas):
		self.__content = canvas
		self.update()
	
	def get_content(self):
		return self.__content


class ImageView(View):
	def __init__(self, resource, **kwargs):
		super(ImageView, self).__init__(Image(resource), **kwargs)
		
		self.set_style_name("image-view")


class CanvasView(View):
	def __init__(self, width, height, **kwargs):
		super(CanvasView, self).__init__(Canvas(width, height), **kwargs)
		
		self.set_style_name("canvas-view")
