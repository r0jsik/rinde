from rinde.stage import ControllerBase
from rinde.stage.animation import AnimationTo


class Controller(ControllerBase):
	def start(self, window):
		self.__label = self.nodes["label"]
	
	def start_animation(self):
		property = self.__label.properties["position-y"]
		animation = AnimationTo(property, 150)
		animation.start()
