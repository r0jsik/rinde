from rinde.property.animation import Animation


"""
Represents collection of properties with user-friendly interface.
"""
class Properties:
	
	"""
	Creates new collection of properties.
	"""
	def __init__(self):
		self.__properties = {}
	
	"""
	Inserts new Property object to the collection.
	"""
	def create(self, name, trigger=None, value=None):
		self.__properties[name] = Property(value)
		self.__try_to_add_trigger(name, trigger)
	
	"""
	Inserts new NumberProperty object to the collection.
	"""
	def create_number(self, name, trigger=None, value=0):
		self.__properties[name] = NumberProperty(value)
		self.__try_to_add_trigger(name, trigger)
	
	"""
	Inserts new BooleanProperty object to the collection.
	"""
	def create_boolean(self, name, trigger=None, value=False):
		self.__properties[name] = BooleanProperty(value)
		self.__try_to_add_trigger(name, trigger)
	
	"""
	Inserts a property to the collection.
	"""
	def insert(self, name, property, trigger=None):
		self.__properties[name] = property
		self.__try_to_add_trigger(name, trigger)
	
	"""
	Inserts a trigger to the property only if not None.
	"""
	def __try_to_add_trigger(self, name, trigger):
		if trigger:
			self.__properties[name].add_trigger(trigger)
	
	def __setitem__(self, property_name, property):
		self.__properties[property_name] = property
	
	def __getitem__(self, property_name):
		return self.__properties[property_name]


"""
Represents simple property.
"""
class Property(object):
	
	"""
	Creates new property with specified value.
	"""
	def __init__(self, value=None):
		self.__bound_to = None
		self.__bound_properties = set()
		self.__triggers = set()
		
		self._value = self._convert_value(value)
	
	"""
	Converts a value to fit the property type (for example converts numeric string to suitable number).
	"""
	def _convert_value(self, value):
		return value
	
	"""
	Changes value of the property without invoking trigers.
	"""
	def reset(self, value):
		self._value = self._convert_value(value)
		
		for property in self.__bound_properties:
			property.reset(value)
	
	"""
	Connects property with another one — both properties have synchronized value.
	To stop the synchronization, use 'unbind' method.
	"""
	def bind_to(self, property):
		if self.__bound_to:
			self.unbind()
		
		self.__bound_to = property
		self.__bound_to.__bound_properties.add(self)
		self.reset(property.get())
	
	"""
	Stops the synchronization between properties that has been established via 'bind_to' method.
	"""
	def unbind(self):
		self.__bound_to.__bound_properties.remove(self)
		self.__bound_to = None
	
	"""
	Changes property's value and invokes triggers when an old value is not equal to the new one.
	"""
	def set(self, value):
		value = self._convert_value(value)
		
		if self._value != value:
			self._change(value)
		
		return self
	
	"""
	Changes property's value and invokes triggers.
	"""
	def _change(self, value):
		self._value = value
		
		for trigger in self.__triggers:
			trigger()
		
		for property in self.__bound_properties:
			property.set(value)
	
	"""
	Inserts a trigger to the property.
	"""
	def add_trigger(self, action):
		self.__triggers.add(action)
	
	"""
	Removes a trigger from the property.
	"""
	def remove_trigger(self, action):
		self.__triggers.remove(action)
	
	"""
	Returns current value of the property.
	"""
	def get(self):
		return self._value
	
	def __str__(self):
		return str(self._value)


"""
Represents simple numeric property.
"""
class NumberProperty(Property):
	
	"""
	Creates new number property with specified value.
	"""
	def __init__(self, value=0):
		super(NumberProperty, self).__init__(value)
	
	"""
	Converts value to int.
	"""
	def _convert_value(self, value):
		return int(value)
	
	"""
	Invokes an animation that changes property's value gradually.
	"""
	def animate_to(self, value, callback=lambda:(), speed=2):
		animation = Animation(self, value, callback, speed)
		animation.start()
	
	"""
	Invokes an animation that changes property's value gradually.
	"""
	def animate_by(self, value, callback=lambda:(), speed=2):
		animation = Animation(self, self._value + value, callback, speed)
		animation.start()
	
	"""
	Sets property's value in specified range.
	"""
	def set_in_range(self, min_value, value, max_value):
		self.set(min_value if value < min_value else value if value < max_value else max_value)
	
	def __iadd__(self, other):
		return self.set(self._value + other)
	
	def __isub__(self, other):
		return self.set(self._value - other)
	
	def __imul__(self, other):
		return self.set(self._value * other)
	
	def __idiv__(self, other):
		return self.set(self._value / other)
	
	def __itruediv__(self, other):
		return self.set(self._value / other)
	
	def __ifloordiv__(self, other):
		return self.set(self._value // other)
	
	def __imod__(self, other):
		return self.set(self._value % other)
	
	def __int__(self):
		return self._value


"""
Represents complex size property.
"""
class SizeProperty(Property):
	
	"""
	Creates new size property and applies it to the specified node.
	"""
	def __init__(self, node):
		super(SizeProperty, self).__init__((0, 0))
		
		self.__node = node
		
		self.__apply()
	
	"""
	Creates two new numeric properties (width and height) and applies them.
	"""
	def __apply(self):
		self.__node.properties["width"] = NumberProperty()
		self.__node.properties["height"] = NumberProperty()
		self.__node.properties["size"] = self
	
	"""
	Changes width and height of the node and invokes triggers.
	"""
	def set(self, value):
		self.__node.properties["width"].set(value[0])
		self.__node.properties["height"].set(value[1])
		
		super(SizeProperty, self).set(value)
	
	"""
	Changes width and height of the node without invoking triggers.
	"""
	def reset(self, value):
		self.__node.properties["width"].reset(value[0])
		self.__node.properties["height"].reset(value[1])
		
		super(SizeProperty, self).reset(value)


"""
Represents complex space property.
"""
class SpaceProperty(Property):
	
	"""
	Creates new space property.
	"""
	def __init__(self):
		super(SpaceProperty, self).__init__([0, 0, 0, 0])
	
	"""
	Converts a value into suitable format, for example changes string "1 2 3 4" to array of ints [1, 2, 3, 4].
	"""
	def _convert_value(self, value):
		if isinstance(value, str):
			value = value.split(" ")
		
		elif isinstance(value, int):
			value = (value,)
		
		return [int(value[side]) for side in self.__split_directional(value)]
	
	"""
	Returns addresses depending on the length of the value.
	
	For example:
		margin: 5 6 7 8
		Returned addresses refers respectively to: top=5, right=6, bottom=7, left=8
		
		margin: 5 6 7
		Returned addresses refers respectively to: top=5, right=6, bottom=7, left=6
		
		margin: 5 9
		Returned addresses refers respectively to: top=5, right=9, bottom=5, left=9
		
		margin: 8
		Returned addresses refers respectively to: top=8, right=8, bottom=8, left=8
	"""
	def __split_directional(self, values):
		if len(values) == 1:
			return 0, 0, 0, 0
		
		if len(values) == 2:
			return 0, 1, 0, 1
		
		if len(values) == 3:
			return 0, 1, 2, 1
		
		if len(values) == 4:
			return 0, 1, 2, 3
		
		raise ValueError("Invalid space value")
	
	"""
	Returns an immutable copy of the value.
	"""
	def get(self):
		return tuple(self._value)
	
	def __setitem__(self, side, value):
		self._value[side] = value
		self.set(self._value)
	
	def __getitem__(self, side):
		return self._value[side]


"""
Represents simple boolean property.
"""
class BooleanProperty(Property):
	
	"""
	Creates new boolean property with specified value.
	"""
	def __init__(self, value=False):
		super(BooleanProperty, self).__init__(value)
	
	"""
	Converts value to True only if is equal to 'true', 'True' or True; or False otherwise.
	"""
	def _convert_value(self, value):
		return value in ("True", "true", True)
	
	"""
	Negates and sets property's value.
	"""
	def toggle(self):
		self.set(not self._value)
	
	"""
	Changes property's value to True.
	"""
	def true(self):
		self.set(True)
	
	"""
	Changes property's value to False.
	"""
	def false(self):
		self.set(False)
	
	def __bool__(self):
		return self._value
	
	def __nonzero__(self):
		return self._value


"""
Represents complex tuple property.
"""
class TupleProperty(Property):
	
	"""
	Creates new tuple property with specified value.
	"""
	def __init__(self, value=()):
		super(TupleProperty, self).__init__(value)
	
	"""
	Converts any iterable value to a list that will be used by the property.
	"""
	def _convert_value(self, value):
		return [item for item in value]
	
	"""
	Appends specified item to the end of the collection.
	"""
	def append(self, item):
		self._value.append(item)
		self._change(self._value)
	
	"""
	Inserts specified item in the collection on specified position.
	"""
	def insert(self, item, index):
		self._value.insert(index, item)
		self._change(self._value)
	
	"""
	Removes specified item from the collection.
	"""
	def remove(self, item):
		self._value.remove(item)
		self._change(self._value)
	
	"""
	Returns an immutable copy of the value.
	"""
	def get(self):
		return tuple(self._value)
