from rinde.property.animation import Animation


class Properties:
	def __init__(self):
		self.__properties = {}
	
	def create(self, name, trigger=None, value=None):
		self.__properties[name] = Property(value)
		self.__try_to_add_trigger(name, trigger)
	
	def create_number(self, name, trigger=None, value=0):
		self.__properties[name] = NumberProperty(value)
		self.__try_to_add_trigger(name, trigger)
	
	def create_boolean(self, name, trigger=None, value=False):
		self.__properties[name] = BooleanProperty(value)
		self.__try_to_add_trigger(name, trigger)
	
	def insert(self, name, property, trigger=None):
		self.__properties[name] = property
		self.__try_to_add_trigger(name, trigger)
	
	def __try_to_add_trigger(self, name, trigger):
		if trigger:
			self.__properties[name].add_trigger(trigger)
	
	def add_trigger(self, name, trigger):
		self.__properties[name].add_trigger(trigger)
	
	def __setitem__(self, property_name, property):
		self.__properties[property_name] = property
	
	def __getitem__(self, property_name):
		return self.__properties[property_name]


class Property(object):
	def __init__(self, value=None):
		self.__bound_to = None
		self.__bound_properties = set()
		self.__triggers = set()
		
		self._value = self._convert_value(value)
	
	def reset(self, value):
		self._value = self._convert_value(value)
		
		for property in self.__bound_properties:
			property.reset(value)
	
	def _convert_value(self, value):
		return value
	
	def bind_to(self, property):
		if self.__bound_to:
			self.unbind()
		
		self.__bound_to = property
		self.__bound_to.__bound_properties.add(self)
		self.reset(property.get())
	
	def unbind(self):
		self.__bound_to.__bound_properties.remove(self)
		self.__bound_to = None
	
	def set(self, value):
		value = self._convert_value(value)
		
		if self._value != value:
			self._change(value)
		
		return self
	
	def _change(self, value):
		self._value = value
		
		for trigger in self.__triggers:
			trigger()
		
		for property in self.__bound_properties:
			property.set(value)
	
	def add_trigger(self, action):
		self.__triggers.add(action)
	
	def remove_trigger(self, action):
		self.__triggers.remove(action)
	
	def get(self):
		return self._value
	
	def __str__(self):
		return str(self._value)


class NumberProperty(Property):
	def __init__(self, value=0):
		super(NumberProperty, self).__init__(value)
	
	def _convert_value(self, value):
		return int(value)
	
	def animate_to(self, value, callback, speed=2):
		animation = Animation(self, value, callback, speed)
		animation.start()
	
	def animate_by(self, value, callback, speed=2):
		animation = Animation(self, self._value + value, callback, speed)
		animation.start()
	
	def set_in_range(self, min_value, value, max_value):
		self.set(min_value if value < min_value else value if value < max_value else max_value)
	
	def __iadd__(self, other):
		return self.set(self._value + other)
	
	def __isub__(self, other):
		return self.set(self._value - other)
	
	def __imul__(self, other):
		return self.set(self._value * other)
	
	def __idiv__(self, other):
		return self.set(self._value / other)
	
	def __itruediv__(self, other):
		return self.set(self._value / other)
	
	def __ifloordiv__(self, other):
		return self.set(self._value // other)
	
	def __imod__(self, other):
		return self.set(self._value % other)
	
	def __int__(self):
		return self._value


class SizeProperty(Property):
	def __init__(self, node):
		super(SizeProperty, self).__init__((0, 0))
		
		self.__node = node
		
		self.__apply()
	
	def __apply(self):
		self.__node.properties["width"] = NumberProperty()
		self.__node.properties["height"] = NumberProperty()
		self.__node.properties["size"] = self
	
	def set(self, value):
		self.__node.properties["width"].set(value[0])
		self.__node.properties["height"].set(value[1])
		
		super(SizeProperty, self).set(value)
	
	def reset(self, value):
		self.__node.properties["width"].reset(value[0])
		self.__node.properties["height"].reset(value[1])
		
		super(SizeProperty, self).reset(value)


class SpaceProperty(Property):
	def __init__(self):
		super(SpaceProperty, self).__init__([0, 0, 0, 0])
	
	def _convert_value(self, value):
		if isinstance(value, str):
			value = value.split(" ")
		
		elif isinstance(value, int):
			value = (value,)
		
		return [int(value[side]) for side in self.__split_directional(value)]
	
	def __split_directional(self, values):
		if len(values) == 1:
			return 0, 0, 0, 0
		
		if len(values) == 2:
			return 0, 1, 0, 1
		
		if len(values) == 3:
			return 0, 1, 2, 1
		
		if len(values) == 4:
			return 0, 1, 2, 3
		
		raise ValueError("Invalid space value")
	
	def get(self):
		return tuple(self._value)
	
	def __setitem__(self, side, value):
		self._value[side] = value
		self.set(self._value)
	
	def __getitem__(self, side):
		return self._value[side]


class BooleanProperty(Property):
	def __init__(self, value=False):
		super(BooleanProperty, self).__init__(value)
	
	def _convert_value(self, value):
		return value in ("True", "true", True)
	
	def toggle(self):
		self.set(not self._value)
	
	def true(self):
		self.set(True)
	
	def false(self):
		self.set(False)
	
	def __bool__(self):
		return self._value
	
	def __nonzero__(self):
		return self._value


class TupleProperty(Property):
	def __init__(self, value=()):
		super(TupleProperty, self).__init__(value)
	
	def _convert_value(self, value):
		return [item for item in value]
	
	def append(self, item):
		self._value.append(item)
		self._change(self._value)
	
	def insert(self, item, index):
		self._value.insert(index, item)
		self._change(self._value)
	
	def remove(self, item):
		self._value.remove(item)
		self._change(self._value)
	
	def get(self):
		return tuple(self._value)
