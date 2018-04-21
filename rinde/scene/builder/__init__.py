from rinde.scene.builder.layout import LayoutParserWithExistingController
from rinde.scene.builder.layout import LayoutParserWithCreatingController
from rinde.scene.builder.styles import StylesParser


class SceneBuilder:
	def __init__(self, scene_directory, controller=None):
		self.__layout_parser = self.__create_layout_parser(scene_directory, controller)
		self.__scene = self.__layout_parser.get_scene()
		self.__styles_parser = StylesParser(scene_directory)
	
	def __create_layout_parser(self, scene_directory, controller):
		if controller:
			return LayoutParserWithExistingController(scene_directory, controller)
		else:
			return LayoutParserWithCreatingController(scene_directory)
	
	def finalize(self, window):
		layout = self.__layout_parser.parse()
		styles = self.__styles_parser.parse()
		
		self.__scene.show(layout, styles)
		self.__scene.start_controller(window)
	
	def get_scene(self):
		return self.__scene
