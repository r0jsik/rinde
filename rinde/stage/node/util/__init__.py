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
		
		if size not in Font.__CACHE[path]:
			Font.__CACHE[path][size] = pygame.font.Font(path, size)
		
		return Font.__CACHE[path][size]
	
	def render(self, text, color):
		return self.__pygame_font.render(str(text), True, self.__int_to_rgb(color))
	
	def __int_to_rgb(self, color):
		return tuple((color >> offset) & 255 for offset in (16, 8, 0))


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
		
		if path not in Image.__CACHE:
			Image.__CACHE[path] = pygame.image.load(path)
		
		return Image.__CACHE[path]
	
	def resize(self, width, height):
		self.__image = pygame.transform.scale(self.__image, (width, height))
	
	def get(self):
		return self.__image.convert_alpha()


class Canvas:
	def __init__(self, width, height):
		try:
			self.__canvas = pygame.Surface((width, height), pygame.SRCALPHA)
		except pygame.error:
			raise RindeException("Invalid canvas size")
	
	def fill(self, red, green, blue, alpha=255):
		self.__canvas.fill((red, green, blue, alpha))
	
	def clear(self):
		self.__canvas.fill(0)
	
	def draw_line(self, color, start, end, stroke=1):
		pygame.draw.line(self.__canvas, color, start, end, stroke)
	
	def draw_rect(self, color, rect, stroke=1):
		pygame.draw.rect(self.__canvas, color, rect, stroke)
	
	def fill_rect(self, color, rect):
		pygame.draw.rect(self.__canvas, color, rect)
	
	def draw_rounded_rect(self, inside_color, bounds, radius, stroke_width, stroke_color):
		inside_bounds = (
			bounds[0] + stroke_width,
			bounds[1] + stroke_width,
			bounds[2] - 2*stroke_width,
			bounds[3] - 2*stroke_width
		)
		
		self.fill_rounded_rect(stroke_color, bounds, radius)
		self.fill_rounded_rect(inside_color, inside_bounds, radius)
	
	def fill_rounded_rect(self, color, bounds, radius):
		if radius < 0 or radius > 100:
			raise RindeException("Radius must be in range <0, 100>")
		else:
			radius /= 100
		
		rectangle = pygame.Rect(0, 0, bounds[2], bounds[3])
		surface = pygame.Surface(rectangle.size, pygame.SRCALPHA)
		color = pygame.Color(color << 8)
		
		corner = pygame.Surface([min(rectangle.size) * 2] * 2, pygame.SRCALPHA)
		pygame.draw.ellipse(corner, (0, 0, 0), corner.get_rect())
		corner = pygame.transform.smoothscale(corner, [int(min(rectangle.size) * radius)] * 2)
		
		radius = surface.blit(corner, (0, 0))
		
		radius.bottomright = rectangle.bottomright
		surface.blit(corner, radius)
		
		radius.topright = rectangle.topright
		surface.blit(corner, radius)
		
		radius.bottomleft = rectangle.bottomleft
		surface.blit(corner, radius)
		
		surface.fill((0, 0, 0), rectangle.inflate(-radius.w, 0))
		surface.fill((0, 0, 0), rectangle.inflate(0, -radius.h))
		surface.fill((255, 255, 255), special_flags=pygame.BLEND_RGBA_MIN)
		surface.fill(color, special_flags=pygame.BLEND_RGBA_MAX)
		
		self.__canvas.blit(surface, bounds)
	
	def get(self):
		return self.__canvas


class Group:
	def __init__(self):
		self.__nodes = {}
		self.__selected = None
	
	def insert(self, node, name):
		self.__nodes[node] = name
	
	def remove(self, node):
		self.__nodes.pop(node)
	
	def select(self, target):
		for node, name in self.__nodes.items():
			if node is target:
				self.__selected = node
			
			node.set_property("selected", node is target)
	
	def get(self):
		return self.__selected
