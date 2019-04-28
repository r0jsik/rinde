class Appearance:
	def __init__(self, node, id, style_class):
		self.node = node
		self.id = id
		self.style_class = style_class
		self.style_name = None
		self.style = ()
	
	def apply_default(self):
		for style in self.style:
			self.__reset_properties(style)
	
	def __reset_properties(self, style):
		for property_name, value in style.get_declarations(None):
			self.node.property(property_name).reset(value)
		
		self.__reset_children_appearances(style)
	
	def __reset_children_appearances(self, style):
		for style_child in style.get_children(None):
			for child in self.node.children():
				for selector in child.appearance.selectors():
					if selector == style_child:
						child.appearance.__reset_properties(style_child)
	
	def apply(self, state):
		for style in self.style:
			self.__set_properties(style, state)
	
	def __set_properties(self, style, state):
		for property_name, value in style.get_declarations(state):
			self.node[property_name] = value
		
		self.__extend_children_appearances(style, state)
	
	def __extend_children_appearances(self, style, state):
		for style_child in style.get_children(state):
			for child in self.node.children():
				for selector in child.appearance.selectors():
					if selector == style_child:
						child.appearance.__set_properties(style_child, None)
	
	def selectors(self):
		if self.style_name:
			yield self.style_name
		
		if self.style_class:
			yield ".%s" % self.style_class
		
		if self.id:
			yield "#%s" % self.id
