from rinde.scene.node.pane import Pane
from rinde.scene.node.box.hbox import HBox
from rinde.scene.node.view import ImageView
from rinde.scene.node.util import LayoutComputer


class Slider(Pane):
	def __init__(self, model="default_slider", range=100, action=None, **kwargs):
		super(Slider, self).__init__(**kwargs)
		
		self.__model = model
		self.__range = range
		self.__action = action
		self.__layout_computer = SliderLayoutComputer(self)
		
		self.__init_track()
		self.__init_thumb()
		
		self.style_name = "slider"
	
	def __init_track(self):
		self.__track = SliderTrack(self.__model, self.__range)
		self._insert_node(self.__track)
	
	def __init_thumb(self):
		self.__thumb = SliderThumb(self.__model, self.__range, self.__action)
		self._insert_node(self.__thumb)
	
	def update(self):
		self.__layout_computer.center_nodes(self.__track, self.__thumb)
		self.__track.resize_content()
	
	def get_value(self):
		return self.__thumb.get_property("position_x")


class SliderTrack(HBox):
	def __init__(self, model, range):
		super(SliderTrack, self).__init__(align="middle")
		
		self.__model = model
		self.__range = range
		
		self.__left_corner = self.__init_part("l_corner")
		self.__content = self.__init_part("content")
		self.__init_part("r_corner")
		
		self.style_name = None
	
	def __init_part(self, name):
		part = ImageView("%s/%s.png" % (self.__model, name))
		self._insert_node(part)
		
		return part
	
	def resize_content(self):
		height = self.get_property("height")
		
		self.__content.resize_content(self.__range, height)
		self.update()
	
	def get_left_corner_width(self):
		return self.__left_corner.get_property("width")


class SliderThumb(ImageView):
	def __init__(self, model, range, action):
		super(SliderThumb, self).__init__("%s/thumb.png" % model)
		
		self.__range = range
		self.__init_value_property(action)
		
		self.style_name = None
	
	def __init_value_property(self, action):
		self.__value = self.property("position_x")
		self.__value.add_trigger(action)
	
	def drag(self, mouse_offset):
		value = self.__value + mouse_offset[0]
		value = self.__clamp(value)
		
		self.__value.set(value)
	
	def __clamp(self, value):
		return 0 if value < 0 else value if value < self.__range else self.__range


class SliderLayoutComputer(LayoutComputer):
	def center_nodes(self, track, thumb):
		self.__center_node(track)
		self.__center_node(thumb)
		
		indent = thumb.get_property("width")/2 - track.get_left_corner_width()
		track.set_property("position_x", indent)
	
	def __center_node(self, node):
		node_center = self._compute_node_center(node, "height")
		node.set_property("position_y", node_center)
