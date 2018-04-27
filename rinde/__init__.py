import pygame

from rinde.scene.util import Screen
from rinde.scene.builder import SceneBuilder
from rinde.data import Resources
from rinde.error import RindeException


class Application:
	def __init__(self, title, scene_directory, favicon=None, cursor=None):
		self.__init_pygame()
		
		Screen.init_size()
		
		Window(title, scene_directory, favicon, cursor)
	
	def __init_pygame(self):
		pygame.init()
		pygame.mixer.init()
		pygame.font.init()


class Window:
	__INSTANCE = None
	
	def __init__(self, title, scene_directory, favicon, cursor):
		self.__init_instance()
		self.__init_favicon(favicon)
		
		self.set_title(title)
		self.set_scene(scene_directory)
		self.set_cursor(cursor)
		
		self.__updating()
	
	def __init_instance(self):
		if Window.__INSTANCE:
			raise RindeException("Window already exists")
		
		Window.__INSTANCE = self
	
	def __init_favicon(self, favicon):
		try:
			self.__try_to_init_favicon(favicon)
		except pygame.error:
			raise RindeException("Favicon not found")
	
	def __try_to_init_favicon(self, favicon):
		if favicon is None:
			favicon = Resources.get_path("favicon.png")
		
		favicon = pygame.image.load(favicon)
		pygame.display.set_icon(favicon)
	
	def set_title(self, title):
		pygame.display.set_caption(title)
	
	def set_scene(self, scene_directory, controller=None):
		scene_builder = SceneBuilder(scene_directory, controller)
		self.__scene = scene_builder.get_scene()
		
		self.__set_up_display()
		
		scene_builder.finalize(self)
	
	def __set_up_display(self):
		scene_size = self.__scene.get_size()
		scene_mode = self.__scene.get_mode()
		
		try:
			self.__surface = pygame.display.set_mode(scene_size, scene_mode)
		except TypeError:
			raise RindeException("Incorrect scene size")
	
	def set_cursor(self, cursor):
		try:
			self.__try_to_set_cursor(cursor)
		except pygame.error:
			raise RindeException("Cursor not found")
	
	def __try_to_set_cursor(self, cursor):
		if cursor:
			self.__cursor = pygame.image.load(cursor)
		else:
			self.__cursor = None
		
		pygame.mouse.set_visible(cursor is None)
	
	def __updating(self):
		while True:
			self.__scene.update(self.__surface)
			self.__draw_cursor()
			
			pygame.display.update()
	
	def __draw_cursor(self):
		if self.__cursor:
			self.__surface.blit(self.__cursor, pygame.mouse.get_pos())
