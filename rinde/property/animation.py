class Animations:
	__ACTIVE = set()
	__MARKED_TO_INSERT = set()
	__MARKED_TO_REMOVE = set()
	
	@staticmethod
	def insert(animation):
		Animations.__MARKED_TO_INSERT.add(animation)
	
	@staticmethod
	def remove(animation):
		Animations.__MARKED_TO_REMOVE.add(animation)
	
	@staticmethod
	def update_all():
		if Animations.__MARKED_TO_INSERT:
			Animations.insert_marked_animations()
		
		for animation in Animations.__ACTIVE:
			animation.next_frame()
		
		if Animations.__MARKED_TO_REMOVE:
			Animations.remove_marked_animations()
	
	@staticmethod
	def insert_marked_animations():
		for animation in Animations.__MARKED_TO_INSERT:
			Animations.__ACTIVE.add(animation)
		
		Animations.__MARKED_TO_INSERT = set()
	
	@staticmethod
	def remove_marked_animations():
		for animation in Animations.__MARKED_TO_REMOVE:
			Animations.__ACTIVE.remove(animation)
		
		Animations.__MARKED_TO_REMOVE = set()
	
	@staticmethod
	def cancel_all():
		__ACTIVE = set()
		__MARKED_TO_INSERT = set()
		__MARKED_TO_REMOVE = set()


class Animation:
	def __init__(self, property, value, callback, speed):
		self.__property = property
		self.__callback = callback
		self.__value = value
		self.__speed = speed
	
	def start(self):
		Animations.insert(self)
	
	def next_frame(self):
		difference = self.__value - self.__property.get()
		
		if self.__speed >= difference >= -self.__speed:
			Animations.remove(self)
			self.__callback()
		
		elif difference < 0:
			self.__property -= self.__speed
		
		elif difference > 0:
			self.__property += self.__speed
