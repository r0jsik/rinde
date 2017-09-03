class Property(object):
	def __init__(self, value):
		self.__default_value = value
		self.__value = value
		self.__bound_properties = []
		self.__bound_to = None
	
	def bind_to(self, property, update=False):
		if self.__bound_to:
			self.unbind()
		
		self.__bound_to = property
		self.__bound_to.__bound_properties.append(self)
		self.__bind_value(property, update)
	
	def __bind_value(self, property, update):
		if update:
			self.set(property.__value)
		else:
			self.__value = property.__value
	
	def set(self, value):
		self.__default_value = value
		self.change(value)
	
	def change(self, value):
		self.__value = value
		self.__update_bound_properties()
		self.value_changed()
	
	def __update_bound_properties(self):
		for property in self.__bound_properties:
			property.set(self.__value)
	
	def reset(self, value):
		self.__default_value = value
		self.__value = value
		
		for property in self.__bound_properties:
			property.reset(value)
	
	def value_changed(self):
		pass
	
	def unbind(self):
		self.__bound_to.__bound_properties.remove(self)
		self.__bound_to = None
	
	def default_value(self):
		self.change(self.__default_value)
	
	def get(self):
		return self.__value
	
	def is_changed(self):
		return self.__value != self.__default_value


class IntegerProperty(Property):
	def __init__(self, value=0):
		super(IntegerProperty, self).__init__(value)
	
	def increase(self, value):
		self.set(self.get() + value)
	
	def decrease(self, value):
		self.set(self.get() - value)


class BooleanProperty(Property):
	def __init__(self, value=True):
		super(BooleanProperty, self).__init__(value)
	
	def negate(self):
		self.set(not self.get())
	
	def true(self):
		self.set(True)
	
	def false(self):
		self.set(False)
