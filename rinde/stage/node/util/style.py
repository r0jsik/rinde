class Style:
	def __init__(self, node, id, style_class):
		self.__node = node
		self.__declarations = []
		self.__id = id
		self.__style_class = style_class
		self.__style_name = None
	
	def apply_default(self):
		for property_name, value in self.__get_declarations(None):
			self.__node.properties[property_name].reset(value)
	
	def __get_declarations(self, state):
		return self.__declarations[state].iteritems()
	
	def apply(self, state):
		if state in self.__declarations:
			for property_name, value in self.__get_declarations(state):
				self.__node.set_property(property_name, value)
	
	def set_declarations(self, declarations):
		self.__declarations = declarations
	
	def set_id(self, value):
		self.__id = value
	
	def set_style_class(self, value):
		self.__style_class = value
	
	def set_style_name(self, value):
		self.__style_name = value
	
	def get_selectors(self):
		return [
			self.__style_name,
			".%s" % self.__style_class,
			"#%s" % self.__id
		]
