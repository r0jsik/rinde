from rinde.stage.property import BooleanProperty


class Appearance:
	def __init__(self, node, id, style_class):
		self.node = node
		self.id = id
		self.style_class = style_class
		self.style_name = None
		self.style = ()
		self.state = {}
	
	def apply_default(self):
		for style in self.style:
			self.__reset_properties(style)
	
	def __reset_properties(self, style):
		for state_name in self.states():
			for property_name, value in style.get_declarations(state_name):
				self.node.properties[property_name].reset(value)
			
			for style_child in style.get_children(state_name):
				self.__reset_children_appearance(style_child)
	
	def __reset_children_appearance(self, style):
		for node in self.node.children():
			for selector in node.appearance.selectors():
				if selector == style:
					node.appearance.__reset_properties(style)
	
	def states(self):
		yield None
		
		for state_name in self.state:
			if self.state[state_name]:
				yield state_name
	
	def selectors(self):
		if self.style_name:
			yield self.style_name
		
		if self.style_class:
			yield ".%s" % self.style_class
		
		if self.id:
			yield "#%s" % self.id
	
	def create_state(self, name, value=False):
		self.state[name] = BooleanProperty(value)
		self.state[name].add_trigger(self.__update_state)
	
	def __update_state(self):
		for style in self.style:
			self.__set_properties(style)
	
	def __set_properties(self, style):
		for state_name in self.states():
			for property_name, value in style.get_declarations(state_name):
				self.node.properties[property_name].set(value)
			
			for style_child in style.get_children(state_name):
				self.__extend_children_appearance(style_child)
	
	def __extend_children_appearance(self, style):
		for child in self.node.children():
			for selector in child.appearance.selectors():
				if selector == style:
					child.appearance.__set_properties(style)
	
	def __setitem__(self, property_name, value):
		self.state[property_name].set(value)
	
	def __getitem__(self, property_name):
		return self.state[property_name].get()
