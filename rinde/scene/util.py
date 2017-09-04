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
		try:
			return Resources.get_path("%s.ttf" % Fonts.__get_rinde_font_name(file))
		except AttributeError:
			return Fonts.__get_custom_font_path(file)
	
	@staticmethod
	def __get_rinde_font_name(file):
		# Declaration in CSS looks like
		# font: "Example Font"
		
		pattern = re.compile("^[\'\"]([\w\s]+)[\'\"]$")
		rinde_font = re.match(pattern, file)
		
		return rinde_font.group(1)
	
	@staticmethod
	def __get_custom_font_path(file):
		try:
			return Fonts.__to_custom_font(file)
		except AttributeError:
			raise RindeException("Incorrect font")
	
	@staticmethod
	def __to_custom_font(file):
		# Declaration in CSS looks like
		# font: src("example/font.ttf")
		
		pattern = re.compile("^src\([\'\"]([\w\s./\\\\]+)[\'\"]\)$")
		custom_font = re.match(pattern, file)
		
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
