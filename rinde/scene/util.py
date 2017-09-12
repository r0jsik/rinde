import pygame
import re

from rinde.data import Resources
from rinde.error import RindeException


class Fonts:
	__CACHE = {}
	
	@staticmethod
	def get(file, size):
		file = Fonts.__get_path(file)
		
		try:
			return Fonts.__CACHE[(file, size)]
		except KeyError:
			return Fonts.__load(file, size)
	
	@staticmethod
	def __get_path(file):
		is_custom_font = Fonts.__get_custom_font_pattern()
		custom_font = re.match(is_custom_font, file)
		
		if custom_font:
			return custom_font.group(1)
		else:
			return Resources.get_path("%s.ttf" % file)
	
	@staticmethod
	def __get_custom_font_pattern():
		# Declaration in CSS looks like
		# font: src("example/font.ttf")
		
		return re.compile("^src\([\'\"]([\w\s./\\\\]+)[\'\"]\)$")
	
	@staticmethod
	def __load(file, size):
		font = Fonts.__CACHE[(file, size)] = Font(file, size)
		return font


class Font:
	def __init__(self, file, size):
		try:
			self.__pygame_font = pygame.font.Font(file, size)
		except IOError:
			raise RindeException("File '%s' not found" % file)
		except RuntimeError:
			raise RindeException("Incorrect font '%s'" % file)
	
	def render(self, text, color):
		return self.__pygame_font.render(text, True, self.__int_to_rgb(color))
	
	def __int_to_rgb(self, color):
		return [(color >> offset) & 255 for offset in [16, 8, 0]]


class Image:
	def __init__(self, resource):
		self.__pygame_image = pygame.image.load(resource)
	
	def get(self):
		return self.__pygame_image.convert_alpha()
