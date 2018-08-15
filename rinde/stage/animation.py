import threading
import pygame

from rinde.error import RindeException


class Animation(object):
	def __init__(self):
		self.__running = False
	
	def start(self):
		if self.__running:
			raise RindeException("Animation is already running")
		
		self.__running = True
		self.__start()
	
	def __start(self):
		thread = threading.Thread(target=self.__updating)
		thread.setDaemon(True)
		thread.start()
	
	def __updating(self):
		clock = pygame.time.Clock()
		
		while self.__running:
			self.next_frame()
			
			clock.tick(60)
	
	def next_frame(self):
		pass
	
	def stop(self):
		self.__running = False


class AnimationTo(Animation):
	def __init__(self, property, value):
		super(AnimationTo, self).__init__()
		
		self.__property = property
		self.__value = value
	
	def next_frame(self):
		difference = self.__value - self.__property.get()
		
		if difference < 0:
			self.__property.decrease()
		
		elif difference > 0:
			self.__property.increase()
		
		else:
			self.stop()
