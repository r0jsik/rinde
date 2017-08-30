from rinde.scene import ControllerBase

class LauncherController(ControllerBase):
	def start(self, window):
		self.__window = window
	
	def start_game(self):
		self.__window.set_scene("board", BoardController())


class BoardController(ControllerBase):
	def game_over(self):
		self.nodes["label"].set_property("text", "Game over")
		
		#Hide button
		self.nodes["button"].set_property("visible", False)
