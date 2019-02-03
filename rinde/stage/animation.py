import threading
import pygame

from rinde.error import RindeException


class Animation(object):
	def __init__(self, callback):
		self.__callback = callback
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
			
			clock.tick(120)
		
		self.__callback()
	
	def next_frame(self):
		pass
	
	def stop(self):
		self.__running = False


class AnimationTo(Animation):
	def __init__(self, property, value, callback, speed=1):
		super(AnimationTo, self).__init__(callback)
		
		self.__property = property
		self.__value = value
		self.__speed = speed
	
	def next_frame(self):
		difference = self.__value - self.__property.get()
		
		if self.__speed >= difference >= -self.__speed:
			self.stop()
		
		elif difference < 0:
			self.__property -= self.__speed
		
		elif difference > 0:
			self.__property += self.__speed
