import pygame

from rinde.error import RindeException
from rinde.data import Resources
from rinde.scene.builder import SceneBuilder


class Application:
	def __init__(self, title, scene_directory):
		self.__init_pygame()
		
		self.__window = Window(title, scene_directory)
		self.__updating()
	
	def __init_pygame(self):
		pygame.init()
		pygame.mixer.init()
		pygame.font.init()
	
	def __updating(self):
		while True:
			self.__window.update()


class Window:
	__INSTANCE = None
	
	def __init__(self, title, scene_directory):
		self.__init_instance()
		self.__init_favicon()
		
		self.set_title(title)
		self.set_scene(scene_directory)
		
		self.__init_surface()
	
	def __init_instance(self):
		if Window.__INSTANCE:
			raise RindeException("Window already exists")
		
		Window.__INSTANCE = self
	
	def __init_favicon(self):
		try:
			self.__try_to_init_favicon()
		except pygame.error:
			raise RindeException("Favicon not found")
	
	def __try_to_init_favicon(self):
		favicon = Resources.get_path("favicon.png")
		favicon = pygame.image.load(favicon)
		pygame.display.set_icon(favicon)
	
	def set_title(self, title):
		pygame.display.set_caption(title)
	
	def set_scene(self, scene_directory, controller=None):
		self.__scene_builder = SceneBuilder(scene_directory, controller)
		self.__scene = self.__scene_builder.get_scene()
		
		self.__set_up_display()
		
		self.__scene_builder.finalize(self)
	
	def __set_up_display(self):
		try:
			pygame.display.set_mode(self.__scene.get_size())
		except TypeError:
			raise RindeException("Incorrect scene size")
	
	def __init_surface(self):
		self.__surface = pygame.display.get_surface()
	
	def update(self):
		self.__scene.update(self.__surface)
		pygame.display.update()
