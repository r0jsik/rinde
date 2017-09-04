import pygame

from rinde.error import RindeException


class Scene:
	def __init__(self, controller, width, height):
		self.__init_controller(controller)
		self.__size = (width, height)
		self.__focused_node = None
		self.__hovered_node = None
		self.__events_handler = EventsHandler(self)
	
	def __init_controller(self, controller):
		if isinstance(controller, ControllerBase):
			self.__controller = controller
		else:
			raise RindeException("Controller must be subclass of rinde.scene.ControllerBase")
	
	def show(self, nodes, styles):
		self.__nodes = nodes
		self.__styles = styles
		
		for node in nodes:
			node.set_parent(self)
			node.reset()
	
	def update_style_request(self, node):
		style = self.__styles.get_style(node)
		node.set_style(style)
	
	def start_controller(self, window):
		self.__controller.start(window)
	
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
		last_hovered_node = None
		
		for node in self.__nodes:
			if node.is_mouse_over(mouse_position):
				hovered_node = node.get_hovered_node(mouse_position)
				
				if hovered_node:
					last_hovered_node = hovered_node
				else:
					last_hovered_node = node
		
		return last_hovered_node
	
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
	
	def update(self, surface):
		self.__events_handler.handle_events()
		self.__repaint(surface)
	
	def __repaint(self, surface):
		surface.fill(0xEEEEEE)
		
		for node in self.__nodes:
			node.repaint(surface)
	
	def get_size(self):
		return self.__size
	
	def get_controller(self):
		return self.__controller


class ControllerBase(object):
	def __init__(self):
		self.nodes = {}
	
	def add_node(self, node_id, node):
		self.nodes[node_id] = node
	
	def start(self, window):
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
		if event.type == 2:
			self.__handle_key_down_event(event)
		
		elif event.type == 4:
			self.__handle_mouse_motion(event)
		
		elif event.type == 5:
			self.__handle_mouse_press(event)
		
		elif event.type == 6:
			self.__handle_mouse_release(event)
		
		elif event.type == 12:
			exit()
	
	def __handle_key_down_event(self, event):
		if event.key == 285 and self.__is_alt_down():
			exit()
		else:
			self.__scene.key_pressed(event.key, event.unicode)
	
	def __is_alt_down(self):
		return pygame.key.get_mods() & 768
	
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
