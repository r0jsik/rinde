class Property(object):
	def __init__(self, value):
		self.__default_value = value
		self.__value = value
		self.__bound_properties = []
		self.__bound_to = None
	
	def bind_to(self, property):
		if self.__bound_to:
			self.unbind()
		
		self.__bound_to = property
		self.__bound_to.__bound_properties.append(self)
		self.__value = property.__value
	
	def reset(self, value):
		self.__default_value = value
		self.set(value)
	
	def set(self, value):
		self.__value = value
		self.__update_bound_properties()
		self.value_changed()
	
	def __update_bound_properties(self):
		for property in self.__bound_properties:
			property.reset(self.__value)
	
	def value_changed(self):
		pass
	
	def unbind(self):
		self.__bound_to.__bound_properties.remove(self)
		self.__bound_to = None
	
	def default_value(self):
		self.set(self.__default_value)
	
	def get(self):
		return self.__value


class IntegerProperty(Property):
	def __init__(self, value=0):
		super(IntegerProperty, self).__init__(value)
	
	def increase(self, value):
		self.reset(self.get() + value)
	
	def decrease(self, value):
		self.reset(self.get() - value)


class BooleanProperty(Property):
	def __init__(self, value=False):
		super(BooleanProperty, self).__init__(value)
	
	def true(self):
		self.reset(True)
	
	def false(self):
		self.reset(False)
