class Property(object):
	def __init__(self, value=None):
		self._value = value
		
		self.__bound_to = None
		self.__bound_properties = []
		self.__triggers = []
	
	def reset(self, value):
		self._value = value
		
		for property in self.__bound_properties:
			property.reset(value)
	
	def bind_to(self, property):
		if self.__bound_to:
			self.unbind()
		
		self.__bound_to = property
		self.__bound_to.__bound_properties.append(self)
		self.reset(property.__value)
	
	def unbind(self):
		self.__bound_to.__bound_properties.remove(self)
		self.__bound_to = None
	
	def set(self, value):
		if self._value != value:
			self.__change(value)
	
	def __change(self, value):
		self._value = value
		self.invoke_triggers()
		
		for property in self.__bound_properties:
			property.set(value)
	
	def invoke_triggers(self):
		for trigger in self.__triggers:
			trigger()
	
	def add_trigger(self, action):
		self.__triggers.append(action)
	
	def remove_trigger(self, action):
		self.__triggers.remove(action)
	
	def get(self):
		return self._value


class IntegerProperty(Property):
	def __init__(self, value=0):
		super(IntegerProperty, self).__init__(value)
	
	def increase(self, value):
		self.set(self._value + value)
	
	def decrease(self, value):
		self.set(self._value - value)
	
	def __add__(self, other):
		return self._value + other
	
	def __sub__(self, other):
		return self._value - other
	
	def __mul__(self, other):
		return self._value * other
	
	def __div__(self, other):
		return self._value / other
	
	def __mod__(self, other):
		return self._value % other


class BooleanProperty(Property):
	def __init__(self, value=False):
		super(BooleanProperty, self).__init__(value)
	
	def toggle(self):
		self.set(not self._value)
	
	def true(self):
		self.set(True)
	
	def false(self):
		self.set(False)
	
	def get(self):
		return self._value in [True, "true"]
