from rinde.stage.builder.layout import LayoutParserWithCreatingController
from rinde.stage.builder.layout import LayoutParserWithExistingController
from rinde.stage.builder.styles import StylesParser


class StageBuilder:
	def __init__(self, stage_directory, controller=None):
		self.__layout_parser = self.__create_layout_parser(stage_directory, controller)
		self.__styles_parser = StylesParser(stage_directory)
		
		self.__stage = self.__layout_parser.get_stage()
	
	def __create_layout_parser(self, stage_directory, controller):
		if controller:
			return LayoutParserWithExistingController(stage_directory, controller)
		else:
			return LayoutParserWithCreatingController(stage_directory)
	
	def finalize(self, window):
		layout = self.__layout_parser.parse()
		styles = self.__styles_parser.parse()
		
		self.__stage.show(layout, styles)
		self.__stage.start_controller(window)
	
	def get_stage(self):
		return self.__stage
