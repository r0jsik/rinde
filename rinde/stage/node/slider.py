from rinde.stage.node import Node
from rinde.stage.node.region import Region
from rinde.stage.node.util.layout import LayoutComputer


class Slider(Node):
	def __init__(self, range=100, action=None, **kwargs):
		super(Slider, self).__init__(**kwargs)
		
		self.properties.create_integer("range", value=range)
		self.properties.create_integer("value", action)
		
		self.__init_track()
		self.__init_thumb()
		self.__layout_computer = LayoutComputer(self)
		
		self.set_style_name("slider")
	
	def __init_track(self):
		self.__track = Track(self)
		self._insert_node(self.__track)
	
	def __init_thumb(self):
		self.__thumb = Thumb(self)
		self._insert_node(self.__thumb)
	
	def update(self):
		self.__layout_computer.center_node_vertically(self.__track)
		self.__layout_computer.center_node_vertically(self.__thumb)


class Track(Region):
	def __init__(self, slider):
		super(Track, self).__init__()
		
		self._borrow_property(slider, "range")
		
		self.set_style_name("track")


class Thumb(Region):
	def __init__(self, slider):
		super(Thumb, self).__init__()
		
		self.__slider = slider
		self.__init_value_property()
		
		self.set_style_name("thumb")
	
	def __init_value_property(self):
		self.__value = self.properties["position-x"]
		self.__value.add_trigger(self.__keep_value_in_limit)
	
	def __keep_value_in_limit(self):
		range = self.__slider.get_property("range")
		value = self.__slider.get_property("value")
		value = self.__clamp(value, range)
		
		self.__value.reset(value)
	
	def __clamp(self, value, range):
		return 0 if value < 0 else value if value < range else range
	
	def drag(self, mouse_offset):
		range = self.__slider.get_property("range")
		value = self.__value + mouse_offset[0]
		value = self.__clamp(value, range)
		
		self.__value.set_value(value)
