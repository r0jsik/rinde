from rinde.scene import ControllerBase


class LauncherController(ControllerBase):
	def start(self, window):
		self.__window = window
	
	def start_game(self):
		self.__window.set_scene("board", BoardController())
	
	def exit(self):
		raise SystemExit


class BoardController(ControllerBase):
	def start(self, window):
		window.set_title("Amazing game started")
	
	def game_over(self):
		self.nodes["label"].set_property("text", "Game over")
		
		#Hide button
		self.nodes["button"].set_property("visible", False)
