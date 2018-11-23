from rinde.error import RindeException


class Properties:
	def __init__(self):
		self.__data = {}
	
	def create(self, name, trigger=None, value=None):
		self[name] = Property(value)
		self.add_trigger(name, trigger)
	
	def add_trigger(self, name, trigger):
		if trigger:
			self[name].add_trigger(trigger)
	
	def insert(self, property, name, trigger=None):
		self[name] = property
		self.add_trigger(name, trigger)
	
	def create_number(self, name, trigger=None, value=0):
		self[name] = NumberProperty(value)
		self.add_trigger(name, trigger)
	
	def create_boolean(self, name, trigger=None, value=False):
		self[name] = BooleanProperty(value)
		self.add_trigger(name, trigger)
	
	def borrow(self, properties, name):
		self[name] = properties[name]
	
	def __setitem__(self, name, property):
		self.__data[name] = property
	
	def __getitem__(self, name):
		try:
			return self.__data[name]
		except KeyError:
			raise RindeException("Unknown property: '%s'" % name)


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


class NumberProperty(Property):
	def __init__(self, value=0):
		super(NumberProperty, self).__init__(float(value))
	
	def __add__(self, other):
		return self._value + other
	
	def __iadd__(self, other):
		return self.set(self._value + other)
	
	def __sub__(self, other):
		return self._value - other
	
	def __isub__(self, other):
		return self.set(self._value - other)
	
	def __mul__(self, other):
		return self._value * other
	
	def __imul__(self, other):
		return self.set(self._value * other)
	
	# For Python 2.7
	def __div__(self, other):
		return self._value / other
	
	# For Python 3.x
	def __divmod__(self, other):
		return self._value / other
	
	def __ifloordiv__(self, other):
		return self.set(self._value / other)
	
	def __idiv__(self, other):
		return self.set(self._value / other)
	
	def __mod__(self, other):
		return self._value % other
	
	def __imod__(self, other):
		return self.set(self._value % other)
	
	def set_in_range(self, min_value, value, max_value):
		self.set(min_value if value < min_value else value if value < max_value else max_value)
	
	def get(self):
		return int(self._value)


class BooleanProperty(Property):
	def __init__(self, value=False):
		super(BooleanProperty, self).__init__(bool(value))
	
	def toggle(self):
		self._value = not self.get()
	
	def true(self):
		self._value = True
	
	def false(self):
		self._value = False
	
	def get(self):
		return self._value in [True, "true"]
