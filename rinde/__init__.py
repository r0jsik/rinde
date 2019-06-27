import pygame

from rinde.data import Resources
from rinde.stage import Screen
from rinde.stage.builder import StageBuilder


"""
Represents Rinde application.
"""
class Application:
	
	"""
	Creates new application object and starts it. The application's window is built using files from the stage directory.
	This is an entry point for every Rinde application.
	Notice, that invoking this constructor starts an infinite loop so the program continues its execution in a controller.
	
	:param title: title of the window
	:param stage_directory: path to directory with files required to build the stage
	:param favicon: path to image file which will be used as icon of the window
	:param cursor: path to image file which will be used as cursor in the window
	"""
	def __init__(self, title, stage_directory, favicon=None, cursor=None):
		self.__init_pygame()
		
		Screen.init_size()
		
		Window(title, stage_directory, favicon, cursor)
	
	"""
	Initializes required library.
	"""
	def __init_pygame(self):
		pygame.init()
		pygame.mixer.init()
		pygame.font.init()


"""
Represents window of the application.
"""
class Window:
	
	"""
	Creates new window and builds a stage using files from stage directory.
	
	:param title: title of the window
	:param stage_directory: path to directory with files required to build the stage
	:param favicon: path to image file which will be used as icon of the window
	:param cursor: path to image file which will be used as cursor in the window
	"""
	def __init__(self, title, stage_directory, favicon, cursor):
		self.__init_favicon(favicon)
		
		self.set_title(title)
		self.set_stage(stage_directory)
		self.set_cursor(cursor)
		
		self.__updating()
	
	"""
	Changes window's favicon. Should not be invoked after initializing display.
	"""
	def __init_favicon(self, favicon):
		try:
			self.__try_to_init_favicon(favicon)
		except pygame.error:
			raise IOError("Cannot load file: '%s'" % favicon)
	
	"""
	Changes window's favicon. Should not be invoked after initializing display.
	"""
	def __try_to_init_favicon(self, favicon):
		if favicon is None:
			favicon = Resources.get_path_to_rinde_file("favicon.png")
		
		favicon = pygame.image.load(favicon)
		pygame.display.set_icon(favicon)
	
	"""
	Changes window's title.
	"""
	def set_title(self, title):
		try:
			pygame.display.set_caption(title)
		except TypeError:
			raise TypeError("Title of the window must be a string")
	
	"""
	Changes window's stage.
	
	:param stage_directory: path to directory with files required to build the stage
	:param controller: an object that controlls the stage
	"""
	def set_stage(self, stage_directory, controller=None):
		stage_builder = StageBuilder(stage_directory, controller)
		self.__stage = stage_builder.get_stage()
		
		self.__set_up_display()
		
		stage_builder.finalize(self)
	
	"""
	Initializes display.
	"""
	def __set_up_display(self):
		stage_size = self.__stage.get_size()
		stage_mode = self.__stage.get_mode()
		
		try:
			self.__surface = pygame.display.set_mode(stage_size, stage_mode)
		except TypeError:
			raise ValueError("Incorrect stage size")
	
	"""
	Changes window's cursor.
	"""
	def set_cursor(self, cursor):
		try:
			self.__try_to_set_cursor(cursor)
		except pygame.error:
			raise IOError("Cannot load file: '%s'" % cursor)
	
	"""
	Changes window's cursor.
	"""
	def __try_to_set_cursor(self, cursor):
		if cursor:
			image = pygame.image.load(cursor)
			self.__draw_cursor = lambda: self.__surface.blit(image, pygame.mouse.get_pos())
		else:
			image = None
			self.__draw_cursor = lambda: ()
		
		pygame.mouse.set_visible(image is None)
	
	"""
	This method invokes an infinite loop that updates window 60 times per second.
	"""
	def __updating(self):
		clock = pygame.time.Clock()
		
		while True:
			self.__stage.update(self.__surface)
			self.__draw_cursor()
			
			pygame.display.update()
			
			clock.tick(60)
	
	"""
	Centers direct child of a stage in the window on a specified axis.
	"""
	def center_in_stage(self, node, axis):
		self.__stage.center_node(node, axis)
	
	"""
	Returns size of the window.
	"""
	def get_size(self):
		return self.__stage.get_size()
	
	"""
	Returns position of the mouse.
	"""
	def get_mouse_position(self):
		return pygame.mouse.get_pos()
