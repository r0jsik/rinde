from rinde.property import BooleanProperty


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
		for state in self.states():
			for property_name, value in style.get_declarations(state):
				self.node.properties[property_name].reset(value)
	
	def states(self):
		yield None
		
		for state in self.state:
			if self.state[state]:
				yield state
	
	def apply_from_parents(self, path):
		for i in range(len(path) - 1):
			self.apply_from_parent(path[i].appearance.style, path, i + 1)
	
	# I don't know how to explain this monster, but it works
	def apply_from_parent(self, styles, path, i):
		children_style = tuple(path[i - 1].appearance.style_children_of(styles, path[i].appearance))
		
		if children_style:
			if path[i] is path[-1]:
				for child_style in children_style:
					path[i].appearance.__reset_properties(child_style)
			else:
				path[i].appearance.apply_from_parent(children_style, path, i + 1)
	
	def style_children_of(self, styles, appearance):
		for style in styles:
			for state in self.states():
				for selector in appearance.selectors():
					if style.has_child(state, selector):
						yield style.get_child(state, selector)
	
	def create_state(self, name, value=False):
		self.state[name] = BooleanProperty(value)
		self.state[name].add_trigger(self.__update_state)
	
	def __update_state(self):
		for style in self.style:
			self.__set_properties(style)
	
	def __set_properties(self, style):
		for state in self.states():
			for property_name, value in style.get_declarations(state):
				self.node.properties[property_name].set(value)
			
			for child_style in style.get_children(state):
				self.__extend_children_appearance(child_style)
	
	def __extend_children_appearance(self, child_style):
		for child in self.node.children():
			if child.appearance.matches(child_style):
				child.appearance.__set_properties(child_style)
	
	def matches(self, style):
		return style in self.selectors()
	
	def selectors(self):
		if self.style_name:
			yield self.style_name
		
		if self.style_class:
			yield ".%s" % self.style_class
		
		if self.id:
			yield "#%s" % self.id
	
	def __setitem__(self, property_name, value):
		self.state[property_name].set(value)
	
	def __getitem__(self, property_name):
		return self.state[property_name].get()
