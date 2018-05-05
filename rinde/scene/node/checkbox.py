from rinde.scene.node import Node
from rinde.scene.node.view import ImageView
from rinde.scene.node.text import Text
from rinde.scene.node.util import LayoutComputer
from rinde.error import RindeException


class Checkbox(Node):
	def __init__(self, text, model="default_checkbox", selected=False, **kwargs):
		super(Checkbox, self).__init__(**kwargs)
		
		self._property["align"] = self._create_property(self.update)
		self._property["spacing"] = self._create_property(self.update)
		
		self.__init_input(model, selected)
		self.__init_label(text)
		self.__layout_computer = CheckboxLayoutComputer(self)
		
		self.style_name = "checkbox"
	
	def __init_input(self, model, selected):
		self.__input = CheckboxInput(model)
		
		self._property["selected"] = self.__input.selected()
		self._property["selected"].set(selected)
		
		self._insert_node(self.__input)
	
	def __init_label(self, text):
		self.__label = Text(text)
		
		self._property["label_font"] = self.__label.property("font")
		self._property["label_font_size"] = self.__label.property("font_size")
		self._property["label_color"] = self.__label.property("color")
		
		self._insert_node(self.__label)
	
	def click(self):
		self._property["selected"].toggle()
	
	def update(self):
		self.__layout_computer.align_nodes(self.__input, self.__label)


class CheckboxLayoutComputer(LayoutComputer):
	def align_nodes(self, input, label):
		nodes = self.__sort_nodes(input, label)
		position_x = 0
		
		for node in nodes:
			position_x = self.__align_node(node, position_x)
	
	def __sort_nodes(self, input, label):
		align = self.get_property("align")
		
		if align == "right":
			return input, label
		
		if align == "left":
			return label, input
		
		raise RindeException("Unknown alignment: '%s'" % align)
	
	def __align_node(self, node, position_x):
		position_y = self.compute_node_center(node, "height")
		node.set_position(position_x, position_y)
		position_x = node.get_property("width") + self.get_property("spacing")
		
		return position_x


class CheckboxInput(Node):
	def __init__(self, model):
		super(CheckboxInput, self).__init__()
		
		self.__model = model
		self.__layout_computer = LayoutComputer(self)
		
		self.__init_part("background")
		self.__pipe = self.__init_part("pipe")
		
		self.style_name = None
	
	def __init_part(self, name):
		part = ImageView(self.__model + "/" + name + ".png")
		self._insert_node(part)
		
		return part
	
	def update(self):
		self.__layout_computer.center_node(self.__pipe)
	
	def selected(self):
		return self.__pipe.property("visible")
