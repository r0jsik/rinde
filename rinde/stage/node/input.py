from rinde.error import RindeException
from rinde.stage.node import Node
from rinde.stage.node.region import Region
from rinde.stage.node.text import Text
from rinde.stage.node.util.layout import LayoutComputer


class Input(Node):
	def __init__(self, text="", selected=False, **kwargs):
		super(Input, self).__init__(**kwargs)
		
		self._create_property("align", self.update)
		self._create_number_property("spacing", self.update)
		
		self.__init_selector(selected)
		self.__init_text(text)
		self.__layout_computer = InputLayoutComputer(self)
	
	def __init_selector(self, selected):
		self.__selector = Selector(selected)
		
		self._borrow_property(self.__selector, "selected")
		self._insert_node(self.__selector)
	
	def __init_text(self, text):
		self.__text = Text(text)
		
		self._borrow_property(self.__text, "text")
		self._insert_node(self.__text)
	
	def update(self):
		self.__layout_computer.align_nodes(self.__selector, self.__text)


class Selector(Node):
	def __init__(self, selected):
		super(Selector, self).__init__()
		
		self.__layout_computer = LayoutComputer(self)
		
		self.__init_background()
		self.__init_pipe()
		self.__init_selected(selected)
		
		self.set_style_name("selector")
	
	def __init_background(self):
		background = Region()
		background.set_style_name("background")
		
		self._insert_node(background)
	
	def __init_pipe(self):
		self.__pipe = Region()
		self.__pipe.set_style_name("pipe")
		
		self._insert_node(self.__pipe)
	
	def __init_selected(self, selected):
		property = self.__pipe.property("visible")
		property.reset(selected)
		
		self._insert_property("selected", property)
	
	def update(self):
		self.__layout_computer.center_node(self.__pipe)


class InputLayoutComputer(LayoutComputer):
	def align_nodes(self, selector, label):
		nodes = self.__sort_nodes(selector, label)
		position_x = 0
		
		for node in nodes:
			position_x = self.__align_node(node, position_x)
	
	def __sort_nodes(self, selector, label):
		align = self.get_property("align")
		
		if align == "right":
			return selector, label
		
		if align == "left":
			return label, selector
		
		raise RindeException("Unknown alignment: '%s'" % align)
	
	def __align_node(self, node, position_x):
		position_y = self.compute_node_center(node, "height")
		node.set_position(position_x, position_y)
		position_x = node["width"] + self.get_property("spacing")
		
		return position_x


class CheckBox(Input):
	def __init__(self, **kwargs):
		super(CheckBox, self).__init__(**kwargs)
		
		self.set_style_name("check-box")
	
	def click(self):
		self.property("selected").toggle()


class RadioBox(Input):
	def __init__(self, group, name, **kwargs):
		super(RadioBox, self).__init__(**kwargs)
		
		self.__group = group
		self.__group.insert(self, name)
		self.__name = name
		
		self.set_style_name("radio-box")
	
	def click(self):
		self.__group.select(self.__name)
