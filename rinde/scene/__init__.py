import pygame

from rinde.scene.util import Screen
from rinde.scene.util import Image
from rinde.error import RindeException


class SceneBase(object):
	def __init__(self):
		self._layout = None
		self._styles = None
	
	def show(self, layout, styles):
		self._layout = layout
		self._styles = styles
		
		for node in layout:
			node.set_scene(self)
			node.reset()
	
	def _repaint(self, surface):
		surface.fill(0xEEEEEE)
		
		for node in self._layout:
			node.repaint(surface)
	
	def update_style_request(self, node):
		style = self._styles.get_style(node)
		node.set_style(style)


class InteractiveScene(SceneBase):
	def __init__(self):
		super(InteractiveScene, self).__init__()
		
		self.__focused_node = None
		self.__hovered_node = None
		self.__events_handler = EventsHandler(self)
	
	def _handle_events(self):
		self.__events_handler.handle_events()
	
	def hover(self, mouse_position):
		hovered_node = self.__get_hovered_node(mouse_position)
		
		if hovered_node:
			if hovered_node is not self.__hovered_node:
				self.__leave_hovered_node()
				self.__hovered_node = hovered_node
				self.__hovered_node.hover()
		else:
			self.__leave_hovered_node()
	
	def __get_hovered_node(self, mouse_position):
		hovered_node = None
		
		for node in self._layout:
			if node.can_be_hovered(mouse_position):
				hovered_node = node.get_hovered_node(mouse_position)
		
		return hovered_node
	
	def __leave_hovered_node(self):
		if self.__hovered_node:
			self.__hovered_node.leave()
			self.__hovered_node = None
	
	def scroll_up(self):
		if self.__hovered_node:
			self.__hovered_node.scroll_up()
	
	def scroll_down(self):
		if self.__hovered_node:
			self.__hovered_node.scroll_down()
	
	def press(self):
		if self.__hovered_node:
			self.__focused_node = self.__hovered_node
			self.__focused_node.focus()
	
	def drag(self, mouse_offset):
		if self.__focused_node:
			self.__focused_node.drag(mouse_offset)
	
	def release(self):
		if self.__focused_node:
			self.__focused_node.unfocus()
			
			if self.__focused_node is self.__hovered_node:
				self.__focused_node.click()
			else:
				self.__focused_node.leave()
			
			self.__focused_node = None
	
	def key_pressed(self, code, char):
		pass


class Scene(InteractiveScene):
	def __init__(self, controller, width=0, height=0):
		super(Scene, self).__init__()
		
		self.__init_controller(controller)
		self.__init_window(width, height)
	
	def __init_controller(self, controller):
		if isinstance(controller, ControllerBase):
			self.__controller = controller
		else:
			raise RindeException("Controller must be subclass of rinde.scene.ControllerBase")
	
	def __init_window(self, width, height):
		if width and height:
			self.__size = (width, height)
			self.__mode = 0
		else:
			self.__size = Screen.SIZE
			self.__mode = pygame.FULLSCREEN
	
	def start_controller(self, window):
		self.__controller.start(window)
	
	def update(self, surface):
		self.__controller.update()
		
		self._handle_events()
		self._repaint(surface)
	
	def get_size(self):
		return self.__size
	
	def get_mode(self):
		return self.__mode
	
	def get_controller(self):
		return self.__controller


class ControllerBase(object):
	def __init__(self):
		self._nodes = {}
	
	def add_node(self, node_id, node):
		self._nodes[node_id] = node
	
	def start(self, window):
		pass
	
	def update(self):
		pass


class EventsHandler(object):
	def __init__(self, scene):
		self.__scene = scene
	
	def handle_events(self):
		events = pygame.event.get()
		
		for event in events:
			self.__handle_event(event)
		
		self.__update_hovering()
	
	def __handle_event(self, event):
		if event.type == pygame.KEYDOWN:
			self.__handle_key_down_event(event)
		
		elif event.type == pygame.MOUSEMOTION:
			self.__handle_mouse_motion(event)
		
		elif event.type == pygame.MOUSEBUTTONDOWN:
			self.__handle_mouse_press(event)
		
		elif event.type == pygame.MOUSEBUTTONUP:
			self.__handle_mouse_release(event)
		
		elif event.type == pygame.QUIT:
			exit()
	
	def __handle_key_down_event(self, event):
		if event.key == pygame.K_F4 and self.__is_alt_down():
			exit()
		else:
			self.__scene.key_pressed(event.key, event.unicode)
	
	def __is_alt_down(self):
		return pygame.key.get_mods() & pygame.KMOD_ALT
	
	def __handle_mouse_motion(self, event):
		if event.buttons[0]:
			self.__scene.drag(event.rel)
	
	def __handle_mouse_press(self, event):
		if event.button == 1:
			self.__scene.press()
		
		elif event.button == 4:
			self.__scene.scroll_up()
		
		elif event.button == 5:
			self.__scene.scroll_down()
	
	def __handle_mouse_release(self, event):
		if event.button == 1:
			self.__scene.release()
	
	def __update_hovering(self):
		self.__scene.hover(pygame.mouse.get_pos())
