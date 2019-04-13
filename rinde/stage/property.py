from rinde.stage.animation import Animation


class Property(object):
	def __init__(self, value=None):
		self.__bound_to = None
		self.__bound_properties = set()
		self.__triggers = set()
		
		self._value = value
	
	def reset(self, value):
		self._value = value
		
		for property in self.__bound_properties:
			property.reset(value)
	
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
		if self._value != value:
			self.__change(value)
		
		return self
	
	def __change(self, value):
		self._value = value
		self.__invoke_triggers()
		
		for property in self.__bound_properties:
			property.set(value)
	
	def __invoke_triggers(self):
		for trigger in self.__triggers:
			trigger()
	
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
		super(NumberProperty, self).__init__(int(value))
	
	def animate_to(self, value, callback, speed=2):
		animation = Animation(self, value, callback, speed)
		animation.start()
	
	def animate_by(self, value, callback, speed=2):
		animation = Animation(self, self._value + value, callback, speed)
		animation.start()
	
	def set_in_range(self, min_value, value, max_value):
		self.set(min_value if value < min_value else value if value < max_value else max_value)
	
	def get(self):
		return int(self._value)
	
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
		return int(self._value)


class SpaceProperty(Property):
	def __init__(self):
		super(SpaceProperty, self).__init__((0, 0, 0, 0))
		
		self.__sides = (
			self.__create_property(),
			self.__create_property(),
			self.__create_property(),
			self.__create_property()
		)
	
	def __create_property(self):
		property = NumberProperty()
		property.add_trigger(self.__update)
		
		return property
	
	def __update(self):
		self.set(self.__sides)
	
	def set(self, value):
		values = self.__split_directional(value)
		
		for side, value in enumerate(values):
			self.__sides[side].set(value)
		
		super(SpaceProperty, self).set(values)
	
	def __split_directional(self, value):
		values = str(value).split(" ")
		
		if len(values) == 1:
			return int(values[0]), int(values[0]), int(values[0]), int(values[0])
		
		if len(values) == 2:
			return int(values[0]), int(values[1]), int(values[0]), int(values[1])
		
		if len(values) == 3:
			return int(values[0]), int(values[1]), int(values[2]), int(values[1])
		
		if len(values) == 4:
			return int(values[0]), int(values[1]), int(values[2]), int(values[3])
		
		raise ValueError("Invalid space value")
	
	def reset(self, value):
		values = self.__split_directional(value)
		
		for side, value in enumerate(values):
			self.__sides[side].reset(value)
		
		super(SpaceProperty, self).reset(values)
	
	def __setitem__(self, side, value):
		self.__sides[side].set(value)
	
	def __getitem__(self, side):
		return self.__sides[side].get()


class BooleanProperty(Property):
	def __init__(self, value=False):
		super(BooleanProperty, self).__init__(value)
	
	def toggle(self):
		self.set(not self.get())
	
	def true(self):
		self.set(True)
	
	def false(self):
		self.set(False)
	
	def get(self):
		return self._value in [True, "true"]
	
	def __bool__(self):
		return self.get()
