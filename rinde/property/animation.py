"""
Represents manager for every animation in the stage.
Every animation that is run in the Rinde thread, has to be inserted to this collection.
"""
class Animations:
	
	"""
	Collection of each animation that is being running.
	"""
	__ACTIVE = set()
	
	"""
	Buffer for each animation that could not be activated directly.
	"""
	__MARKED_TO_INSERT = set()
	
	"""
	Buffer for each animation that could not be deactivated directly.
	"""
	__MARKED_TO_REMOVE = set()
	
	"""
	Inserts new animation to the collection.
	"""
	@staticmethod
	def insert(animation):
		Animations.__MARKED_TO_INSERT.add(animation)
	
	"""
	Removes an animation form the collection.
	"""
	@staticmethod
	def remove(animation):
		Animations.__MARKED_TO_REMOVE.add(animation)
	
	"""
	Invokes single update (frame change) of each animation in the collection.
	This method in invoked automatically in the Rinde thread 60 times per second.
	"""
	@staticmethod
	def update_all():
		if Animations.__MARKED_TO_INSERT:
			Animations.insert_marked_animations()
		
		for animation in Animations.__ACTIVE:
			animation.next_frame()
		
		if Animations.__MARKED_TO_REMOVE:
			Animations.remove_marked_animations()
	
	"""
	Activates each animation that started before (or during) previous iteration of update.
	"""
	@staticmethod
	def insert_marked_animations():
		for animation in Animations.__MARKED_TO_INSERT:
			Animations.__ACTIVE.add(animation)
		
		Animations.__MARKED_TO_INSERT = set()
	
	"""
	Deactivates each animation that finished in a previous iteration of update.
	"""
	@staticmethod
	def remove_marked_animations():
		for animation in Animations.__MARKED_TO_REMOVE:
			Animations.__ACTIVE.remove(animation)
		
		Animations.__MARKED_TO_REMOVE = set()


"""
This class represents animation that changes its property's value gradually, in each frame.
"""
class Animation:
	
	"""
	Creates an animation that changes property's value to the specified value.
	
	:param property: the property whose value will be changed
	:param value: target value of the property (an animation ends when property's value is equal to this parameter)
	:param callback: a method which will be invoked when animation finishes
	:param speed: speed of the animation
	"""
	def __init__(self, property, value, callback, speed):
		self.__property = property
		self.__callback = callback
		self.__value = value
		self.__speed = speed
	
	"""
	Starts an animation. It should be invoked only once for each instance.
	"""
	def start(self):
		Animations.insert(self)
	
	"""
	Changes value of the property towards the goal.
	"""
	def next_frame(self):
		difference = self.__value - self.__property.get()
		
		if difference >= 1:
			self.__property += min(difference, self.__speed)
		
		elif difference <= -1:
			self.__property -= min(-difference, self.__speed)
		
		else:
			Animations.remove(self)
			self.__callback()
