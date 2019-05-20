import pygame

from rinde.data import Resources


class Font:
	__CACHE = {}
	
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
		return self.__pygame_font.render(text, True, self.__int_to_rgb(color))
	
	def __int_to_rgb(self, color):
		return tuple((color >> offset) & 255 for offset in (16, 8, 0))


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
		if radius < 0 or radius > 100:
			raise ValueError("Radius must be in range <0, 100>")
		else:
			radius /= 100
		
		if bounds[2] <= 0 or bounds[3] <= 0:
			return
		
		rectangle = pygame.Rect(0, 0, bounds[2], bounds[3])
		surface = pygame.Surface(rectangle.size, pygame.SRCALPHA)
		
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
		self.__selected = ""
		self.__items = {}
	
	def insert(self, node, name):
		self.__items[name] = node
		
		if node.is_selected():
			self.select(name)
	
	def remove(self, name):
		del self.__items[name]
	
	def select(self, name):
		self.__selected = name
		
		for item_name, item in self.__items.items():
			item.set_selected(item_name == name)
		
		self.on_selected()
	
	def on_selected(self):
		pass
	
	def get(self):
		return self.__selected
	
	def get_item(self):
		return self.__items[self.__selected]
	
	def __eq__(self, other):
		return self.__selected == other
