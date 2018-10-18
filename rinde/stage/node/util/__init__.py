import pygame

from rinde.data import Resources
from rinde.error import RindeException


class Font:
	__CACHE = {}
	
	def __init__(self, resource, size):
		try:
			self.__pygame_font = self.__load(resource, size)
		except IOError:
			raise RindeException("File '%s' not found" % resource)
		except RuntimeError:
			raise RindeException("Incorrect font '%s'" % resource)
	
	def __load(self, resource, size):
		path = Resources.get_path(resource)
		
		if path not in Font.__CACHE:
			Font.__CACHE[path] = {}
		
		if size in Font.__CACHE[path]:
			font = Font.__CACHE[path][size]
		else:
			font = Font.__CACHE[path][size] = pygame.font.Font(path, size)
		
		return font
	
	def render(self, text, color):
		return self.__pygame_font.render(str(text), True, self.__int_to_rgb(color))
	
	def __int_to_rgb(self, color):
		return [(color >> offset) & 255 for offset in (16, 8, 0)]


class Image:
	__CACHE = {}
	
	@staticmethod
	def remove_from_cache(resource):
		try:
			Image.__CACHE.pop(resource)
		except KeyError:
			raise RindeException("File '%s' is not cached")
	
	def __init__(self, resource):
		try:
			self.__image = self.__load(resource)
		except pygame.error:
			raise RindeException("File '%s' not found" % resource)
	
	def __load(self, resource):
		path = Resources.get_path(resource)
		
		if path in Image.__CACHE:
			image = Image.__CACHE[path]
		else:
			image = Image.__CACHE[path] = pygame.image.load(path)
		
		return image
	
	def resize(self, width, height):
		self.__image = pygame.transform.scale(self.__image, (width, height))
	
	def get(self):
		return self.__image.convert_alpha()


class Canvas:
	def __init__(self, width, height):
		try:
			self.__canvas = pygame.Surface((width, height))
		except pygame.error:
			raise RindeException("Invalid canvas size")
	
	def fill(self, red, green, blue):
		self.__canvas.fill((red, green, blue))
	
	def draw_line(self, color, start, end, stroke=1):
		pygame.draw.line(self.__canvas, color, start, end, stroke)
	
	def draw_rect(self, color, rect, stroke=1):
		pygame.draw.rect(self.__canvas, color, rect, stroke)
	
	def get(self):
		return self.__canvas
