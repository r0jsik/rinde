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
	
	def create_integer(self, name, trigger=None, value=0):
		self[name] = IntegerProperty(value)
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
		self.__value = value
		self.__bound_to = None
		self.__bound_properties = set()
		self.__triggers = set()
	
	def reset(self, value):
		self.__value = value
		
		for property in self.__bound_properties:
			property.reset(value)
	
	def bind_to(self, property):
		if self.__bound_to:
			self.unbind()
		
		self.__bound_to = property
		self.__bound_to.__bound_properties.add(self)
		self.reset(property.__value)
	
	def unbind(self):
		self.__bound_to.__bound_properties.remove(self)
		self.__bound_to = None
	
	def set(self, value):
		if self.__value != value:
			self.__change(value)
	
	def __change(self, value):
		self.__value = value
		self.invoke_triggers()
		
		for property in self.__bound_properties:
			property.set(value)
	
	def invoke_triggers(self):
		for trigger in self.__triggers:
			trigger()
	
	def add_trigger(self, action):
		self.__triggers.add(action)
	
	def remove_trigger(self, action):
		self.__triggers.remove(action)
	
	def get(self):
		return self.__value


class IntegerProperty(Property):
	def __init__(self, value=0):
		super(IntegerProperty, self).__init__(value)
	
	def increase(self, value=1):
		self.set(self.get() + value)
	
	def decrease(self, value=1):
		self.set(self.get() - value)
	
	def __add__(self, other):
		return self.get() + other
	
	def __sub__(self, other):
		return self.get() - other
	
	def __mul__(self, other):
		return self.get() * other
	
	def __div__(self, other):
		return self.get() / other
	
	def __mod__(self, other):
		return self.get() % other
	
	def get(self):
		return int(super(IntegerProperty, self).get())


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
		return super(BooleanProperty, self).get() in [True, "true"]
