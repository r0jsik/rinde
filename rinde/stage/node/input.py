from rinde.stage.node import ComplexNode
from rinde.stage.node.region import Region
from rinde.stage.node.region import ComplexNodeWithBackground
from rinde.stage.node.text import Text
from rinde.stage.node.util import LayoutComputer


class Input(ComplexNode):
	def __init__(self, text="", selected=False, **kwargs):
		super(Input, self).__init__(**kwargs)
		
		self.properties.create("align", self.update)
		self.properties.create_number("spacing", self.update)
		
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
	
	def update_layout(self):
		self.__layout_computer.align_nodes(self.__selector, self.__text)


class Selector(ComplexNodeWithBackground):
	def __init__(self, selected):
		super(Selector, self).__init__()
		
		self.__layout_computer = LayoutComputer(self)
		
		self.__init_pipe()
		self.__init_selected(selected)
		
		self.set_style_name("selector")
	
	def __init_pipe(self):
		self.__pipe = Region()
		self.__pipe.set_style_name("pipe")
		
		self._insert_node(self.__pipe)
	
	def __init_selected(self, selected):
		property = self.__pipe.properties["visible"]
		property.reset(selected)
		
		self.properties.insert("selected", property)
	
	def update_layout(self):
		self.__layout_computer.center_node(self.__pipe)


class InputLayoutComputer(LayoutComputer):
	def align_nodes(self, selector, label):
		nodes = self.__sort_nodes(selector, label)
		position_x = 0
		
		for node in nodes:
			position_x = self.__align_node(node, position_x)
	
	def __sort_nodes(self, selector, label):
		align = self.node["align"]
		
		if align == "right":
			return selector, label
		
		if align == "left":
			return label, selector
		
		raise ValueError("Unknown alignment: '%s'" % align)
	
	def __align_node(self, node, position_x):
		node["position-x"] = position_x
		node["position-y"] = self.compute_node_center(node, "height")
		position_x = node["width"] + self.node["spacing"]
		
		return position_x


class CheckBox(Input):
	def __init__(self, **kwargs):
		super(CheckBox, self).__init__(**kwargs)
		
		self.set_style_name("check-box")
	
	def click(self):
		self.properties["selected"].toggle()


class RadioBox(Input):
	def __init__(self, group, name, **kwargs):
		super(RadioBox, self).__init__(**kwargs)
		
		self.__group = group
		self.__group.insert(self, name)
		self.__name = name
		
		self.set_style_name("radio-box")
	
	def click(self):
		self.__group.select(self.__name)
	
	def is_selected(self):
		return self["selected"]
	
	def set_selected(self, value):
		self["selected"] = value
