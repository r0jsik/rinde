import pygame

from rinde.data import Resources
from rinde.script import rounded_rect


class Font:
	__CACHE = {}
	
	@staticmethod
	def remove_from_cache(resource):
		del Font.__CACHE[Resources.get_path(resource)]
	
	def __init__(self, resource, size):
		try:
			self.__pygame_font = self.__load(resource, size)
		except IOError:
			raise IOError("Cannot load file: '%s'" % resource)
		except RuntimeError:
			raise IOError("Incorrect font: '%s'" % resource)
	
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
	
	def pygame(self):
		return self.__pygame_font


class Image:
	def __init__(self, resource):
		path = Resources.get_path(resource)
		
		try:
			self.__image = pygame.image.load(path)
		except pygame.error:
			raise IOError("Cannot load file: '%s'" % path)
	
	def get(self):
		return self.__image.convert_alpha()


class Canvas:
	def __init__(self, width, height):
		try:
			self.__canvas = pygame.Surface((width, height), pygame.SRCALPHA)
		except pygame.error:
			raise ValueError("Invalid canvas size")
	
	def clear(self):
		self.__canvas.fill((0, 0, 0, 0))
	
	def fill(self, red, green, blue, alpha=255):
		self.__canvas.fill((red, green, blue, alpha))
	
	def draw_line(self, color, start, end, stroke_width=1):
		pygame.draw.line(self.__canvas, self.__convert_color(color), start, end, stroke_width)
	
	def __convert_color(self, color):
		return pygame.Color(color << 8 | 0xFF)
	
	def draw_rect(self, color, bounds, stroke_width=1):
		pygame.draw.rect(self.__canvas, self.__convert_color(color), bounds, stroke_width)
	
	def fill_rect(self, color, bounds):
		pygame.draw.rect(self.__canvas, self.__convert_color(color), bounds)
	
	def draw_rounded_rect(self, inside_color, bounds, radius, stroke_width, stroke_color):
		inner_bounds = self.__compute_inner_rect_bounds(bounds, stroke_width)
		
		self.fill_rounded_rect(stroke_color, bounds, radius)
		self.fill_rounded_rect(inside_color, inner_bounds, radius)
	
	def __compute_inner_rect_bounds(self, bounds, stroke_width):
		return bounds[0] + stroke_width, bounds[1] + stroke_width, bounds[2] - 2*stroke_width, bounds[3] - 2*stroke_width
	
	def fill_rounded_rect(self, color, bounds, radius):
		if bounds[2] > 0 and bounds[3] > 0:
			self.__canvas.blit(rounded_rect.render(color, bounds[2], bounds[3], radius), bounds)
	
	def get(self):
		return self.__canvas


class Group:
	def __init__(self):
		self.__selected = None
		self.__items = {}
		self.__triggers = []
	
	def insert(self, item, name):
		self.__items[name] = item
		
		if item.is_selected():
			self.select(name)
	
	def remove(self, name):
		item = self.__items.pop(name)
		
		if item.is_selected():
			self.select(None)
	
	def select(self, name):
		if name is None or name in self.__items:
			self.__select(name)
		else:
			raise KeyError("Unknown item name: '%s'" % name)
	
	def __select(self, name):
		self.__selected = name
		
		for item_name, item in self.__items.items():
			item.set_selected(item_name == name)
		
		for trigger in self.__triggers:
			trigger()
	
	def add_trigger(self, trigger):
		self.__triggers.append(trigger)
	
	def get_selected_name(self):
		return self.__selected
	
	def get_selected_item(self):
		try:
			return self.__items[self.__selected]
		except KeyError:
			return None
	
	def get_item_by_name(self, name):
		return self.__items[name]
	
	def __eq__(self, other):
		return self.__selected == other


class LayoutComputer(object):
	def __init__(self, node):
		self.node = node
	
	def center_node(self, node):
		self.center_node_horizontally(node)
		self.center_node_vertically(node)
	
	def center_node_horizontally(self, node):
		node["position-x"] = self.compute_node_center(node, "width")
	
	def center_node_vertically(self, node):
		node["position-y"] = self.compute_node_center(node, "height")
	
	def compute_node_center(self, node, dimension):
		return (self.node.get_absolute_size(dimension) - node.get_absolute_size(dimension))/2
