import pygame

from rinde.error import RindeException


class Font:
	def __init__(self, pygame_font):
		self.__pygame_font = pygame_font
	
	def render(self, text, color):
		return self.__pygame_font.render(text, True, self.__int_to_rgb(color))
	
	def __int_to_rgb(self, color):
		return [(color >> offset) & 255 for offset in [16, 8, 0]]


class SystemFonts:
	
	@staticmethod
	def get(name, size):
		pygame_font = pygame.font.SysFont(name, size)
		font = Font(pygame_font)
		
		return font


class CustomFonts:
	__CACHE = {}
	
	@staticmethod
	def get(file, size):
		try:
			return CustomFonts.__CACHE[(file, size)]
		except KeyError:
			return CustomFonts.__load(file, size)
	
	@staticmethod
	def __load(file, size):
		try:
			return CustomFonts.__try_to_load(file, size)
		except IOError:
			raise RindeException("Font file '%s' not found" % file)
	
	@staticmethod
	def __try_to_load(file, size):
		pygame_font = pygame.font.Font(file, size)
		font = CustomFonts.__CACHE[(file, size)] = Font(pygame_font)
		
		return font
