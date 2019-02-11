class Appearance:
	def __init__(self, node, id, style_class):
		self.__node = node
		self.__id = id
		self.__style_class = style_class
		self.__style_name = None
		self.__style = ()
	
	def apply_default(self):
		for style in self.__style:
			self.__reset_properties(style)
	
	def __reset_properties(self, style):
		for property_name, value in style.get_declarations(None):
			self.__node.property(property_name).reset(value)
		
		self.__reset_children_appearances(style)
	
	def __reset_children_appearances(self, style):
		for style_child in style.get_children(None):
			for node_appearance in self.__node.children_appearances():
				for selector in node_appearance.style_selectors():
					if selector == style_child:
						node_appearance.__reset_properties(style_child)
	
	def apply(self, state):
		for style in self.__style:
			self.__set_properties(style, state)
	
	def __set_properties(self, style, state):
		for property_name, value in style.get_declarations(state):
			self.__node[property_name] = value
		
		self.__extend_children_appearances(style, state)
	
	def __extend_children_appearances(self, style, state):
		for style_child in style.get_children(state):
			for node_appearance in self.__node.children_appearances():
				for selector in node_appearance.style_selectors():
					if selector == style_child:
						node_appearance.__set_properties(style_child, None)
	
	def set_style(self, style):
		self.__style = style
	
	def set_id(self, value):
		self.__id = value
	
	def set_style_class(self, value):
		self.__style_class = value
	
	def set_style_name(self, value):
		self.__style_name = value
	
	def style_selectors(self):
		if self.__style_name:
			yield self.__style_name
		
		if self.__style_class:
			yield ".%s" % self.__style_class
		
		if self.__id:
			yield "#%s" % self.__id
