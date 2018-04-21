import pygame
import re

from rinde.data import Resources
from rinde.error import RindeException


class Screen:
	SIZE = None
	
	@staticmethod
	def init_size():
		screen_size = pygame.display.Info()
		Screen.SIZE = (screen_size.current_w, screen_size.current_h)


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
		is_external_font = Fonts.__get_external_font_pattern()
		external_font = re.match(is_external_font, file)
		
		if external_font:
			return external_font.group(1)
		else:
			return Resources.get_path("%s.ttf" % file)
	
	@staticmethod
	def __get_external_font_pattern():
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
		return self.__pygame_font.render(unicode(text), True, self.__int_to_rgb(color))
	
	def __int_to_rgb(self, color):
		return [(color >> offset) & 255 for offset in [16, 8, 0]]


class Image:
	def __init__(self, file):
		try:
			self.__image = pygame.image.load(file)
		except pygame.error:
			raise RindeException("File '%s' not found" % file)
	
	def get(self):
		return self.__image.convert_alpha()
	
	def resize(self, width, height):
		self.__image = pygame.transform.scale(self.__image, (width, height))
	
	def get_size(self):
		return self.__image.get_size()


class Canvas:
	def __init__(self, width, height):
		self.__canvas = pygame.Surface((width, height))
		self.fill(0, 0, 0)
	
	def fill(self, red, green, blue):
		self.__canvas.fill((red, green, blue))
	
	def draw_line(self, color, start, end, width=1):
		pygame.draw.line(self.__canvas, color, start, end, width)
	
	def get_size(self):
		return self.__canvas.get_size()
	
	def get(self):
		return self.__canvas
