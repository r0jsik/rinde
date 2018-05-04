from rinde.scene import ControllerBase
from rinde.scene.animation import AnimationTo


class Controller(ControllerBase):
	def start(self, window):
		self.__label = self._nodes["label"]
	
	def start_animation(self):
		property = self.__label.property("position_y")
		animation = AnimationTo(property, 180)
		animation.play()
