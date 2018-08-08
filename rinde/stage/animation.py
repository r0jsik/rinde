import threading
import pygame

from rinde.error import RindeException


class Animation(object):
	def __init__(self, property, value):
		self._property = property
		self._value = value
		
		self.__running = False
	
	def play(self):
		self.__start()
		
		thread = threading.Thread(target=self.__updating)
		thread.setDaemon(True)
		thread.start()
	
	def __start(self):
		if self.__running:
			raise RindeException("Animation is already being played")
		
		self.__running = True
	
	def __updating(self):
		clock = pygame.time.Clock()
		
		while self.__running:
			self._update()
			
			clock.tick(60)
	
	def _update(self):
		pass
	
	def stop(self):
		self.__running = False


class AnimationTo(Animation):
	def _update(self):
		difference = self._value - self._property.get()
		
		if difference < 0:
			self._property.decrease()
		
		elif difference > 0:
			self._property.increase()
		
		else:
			self.stop()
