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
		
		self.set_style_name("slider")
	
	def __init_track(self):
		self.__track = Region()
		self.__track.set_style_name("track")
		
		self._insert_node(self.__track)
	
	def __init_range(self, value):
		range = self.__track.property("width")
		range.reset(value)
		
		self.properties.insert("range", range, self.__clamp_value)
	
	# Prevents thumb from getting out of the range
	def __clamp_value(self):
		self.property("value").set_in_range(0, self["value"], self["range"])
	
	def __init_thumb(self):
		self.__thumb = Thumb(self)
		self.__thumb.set_style_name("thumb")
		
		self._insert_node(self.__thumb)
	
	def __init_value(self, action):
		self.borrow_property(self.__thumb, "position-x", action, "value")
		self.properties.add_trigger("value", self.__clamp_value)
	
	def update(self):
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
	
	def drag(self, mouse_offset):
		self.property("position-x").set_in_range(0, self["position-x"] + mouse_offset[0], self.__slider["range"])
