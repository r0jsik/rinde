from rinde.stage.node import Node
from rinde.stage.node.region import Region
from rinde.stage.node.util.layout import LayoutComputer


class Slider(Node):
	def __init__(self, range=100, action=None, **kwargs):
		super(Slider, self).__init__(**kwargs)
		
		self.__layout_computer = LayoutComputer(self)
		self.__init_track()
		self.__init_range(range)
		self.__init_thumb()
		self.__init_value(action)
		
		self.properties.add_trigger("width", self.__clamp_value)
		self.properties.add_trigger("height", self.__update_layout)
		
		self.set_style_name("slider")
	
	def __init_track(self):
		self.__track = Region()
		self.__track.set_style_name("track")
		
		self._insert_node(self.__track)
	
	def __init_range(self, range):
		track_width = self.__track.properties["width"]
		track_width.set(range)
		
		self.properties.insert(track_width, "range", self.__clamp_value)
	
	# Prevents thumb from getting out of slider range
	def __clamp_value(self):
		value = self.get_property("value")
		range = self.get_property("range")
		
		self.properties["value"].set_in_range(0, value, range)
	
	def __init_thumb(self):
		self.__thumb = Thumb(self)
		self._insert_node(self.__thumb)
	
	def __init_value(self, action):
		thumb_position = self.__thumb.properties["position-x"]
		thumb_position.add_trigger(action)
		
		self.properties.insert(thumb_position, "value")
	
	def __update_layout(self):
		self.__layout_computer.center_node_vertically(self.__track)
		self.__layout_computer.center_node_vertically(self.__thumb)
	
	def get_hovered_node(self, mouse_position):
		if self.__thumb.is_mouse_over(mouse_position):
			return self.__thumb
		
		return self


class Thumb(Region):
	def __init__(self, slider):
		super(Thumb, self).__init__()
		
		self.__slider = slider
		
		self.set_style_name("thumb")
	
	def drag(self, mouse_offset):
		range = self.__slider.get_property("range")
		value = self.properties["position-x"]
		value.set_in_range(0, value.get() + mouse_offset[0], range)
