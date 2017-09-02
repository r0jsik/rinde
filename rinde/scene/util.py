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
		is_rinde_font = re.compile("^[\'\"]([\w\s]+)[\'\"]$")
		rinde_font = re.match(is_rinde_font, file)
		
		if rinde_font:
			return Resources.get_path("%s.ttf" % rinde_font.group(1))
		else:
			is_custom_font = re.compile("^src\([\'\"]([\w\s./\\\\]+)[\'\"]\)$")
			custom_font = re.match(is_custom_font, file)
			
			if custom_font:
				return custom_font.group(1)
	
	@staticmethod
	def __load(file, size):
		font = Fonts.__CACHE[(file, size)] = Font(file, size)
		return font


class Font:
	def __init__(self, file, size):
		try:
			self.__pygame_font = pygame.font.Font(file, size)
		except IOError:
			raise RindeException("Font '%s' not found" % file)
	
	def render(self, text, color):
		return self.__pygame_font.render(text, True, self.__int_to_rgb(color))
	
	def __int_to_rgb(self, color):
		return [(color >> offset) & 255 for offset in [16, 8, 0]]


class Image:
	def __init__(self, resource):
		self.__pygame_image = pygame.image.load(resource)
	
	def convert_alpha(self):
		self.__pygame_image = self.__pygame_image.convert_alpha()
	
	def get(self):
		return self.__pygame_image
