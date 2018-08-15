from rinde.stage.node import Node
from rinde.stage.node.box.hbox import HBox
from rinde.stage.node.util import LayoutComputer
from rinde.stage.node.view import ImageView


class Slider(Node):
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
		
		self.properties.insert(self.__thumb.value(), "value")
	
	def update(self):
		self.__layout_computer.align_nodes(self.__track, self.__thumb)
		self.__track.resize_content()
	
	def get_hovered_node(self, mouse_position):
		if self.__thumb.can_be_hovered(mouse_position):
			return self.__thumb


class SliderLayoutComputer(LayoutComputer):
	def align_nodes(self, track, thumb):
		self.center_node_vertically(track)
		self.center_node_vertically(thumb)
		
		self.__indent_track(track, thumb)
	
	def __indent_track(self, track, thumb):
		position_x = thumb.get_property("width")/2 - track.get_left_corner_width()
		track.set_property("position_x", position_x)


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
		self.__value = self.properties["position_x"]
		self.__value.add_trigger(self.__keep_value_in_limit)
		self.__value.add_trigger(action)
	
	def __keep_value_in_limit(self):
		value = self.__value.get()
		value = self.__clamp(value)
		
		self.__value.reset(value)
	
	def drag(self, mouse_offset):
		value = self.__value + mouse_offset[0]
		value = self.__clamp(value)
		
		self.__value.set(value)
	
	def __clamp(self, value):
		return 0 if value < 0 else value if value < self.__range else self.__range
	
	def value(self):
		return self.__value
