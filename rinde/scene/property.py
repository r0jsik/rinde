class Property(object):
	def __init__(self, value):
		self.__value = value
		self.__bound_properties = []
		self.__bound_to = None
	
	def reset(self, value):
		self.__value = value
		
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
		if self.__value != value:
			self.__change(value)
	
	def __change(self, value):
		self.__value = value
		self.value_changed()
		
		for property in self.__bound_properties:
			property.set(value)
	
	def value_changed(self):
		pass
	
	def get(self):
		return self.__value


class IntegerProperty(Property):
	def __init__(self, value=0):
		super(IntegerProperty, self).__init__(value)
	
	def increase(self, value):
		self.set(self.get() + value)
	
	def decrease(self, value):
		self.set(self.get() - value)


class BooleanProperty(Property):
	def __init__(self, value=False):
		super(BooleanProperty, self).__init__(value)
	
	def negate(self):
		self.set(not self.get())
	
	def true(self):
		self.set(True)
	
	def false(self):
		self.set(False)
	
	def get(self):
		return super(BooleanProperty, self).get() in [True, "true"]
