from rinde.error import RindeException
from rinde.stage.node import Node
from rinde.stage.node.text import Text
from rinde.stage.node.util import LayoutComputer
from rinde.stage.node.view import ImageView


class Checkbox(Node):
	def __init__(self, text, model="default_checkbox", selected=False, **kwargs):
		super(Checkbox, self).__init__(**kwargs)
		
		self.properties.create("align", self.update)
		self.properties.create_integer("spacing", self.update)
		
		self.__init_input(model, selected)
		self.__init_label(text)
		self.__layout_computer = CheckboxLayoutComputer(self)
		
		self.style_name = "checkbox"
	
	def __init_input(self, model, selected):
		self.__input = CheckboxInput(model)
		
		property = self.__input.selected()
		property.set(selected)
		self.properties.insert(property, "selected")
		
		self._insert_node(self.__input)
	
	def __init_label(self, text):
		self.__label = Text(text)
		
		self.__create_label_property("font", "label_font")
		self.__create_label_property("font_size", "label_font_size")
		self.__create_label_property("color", "label_color")
		
		self._insert_node(self.__label)
	
	def __create_label_property(self, name, name_as):
		self.properties.insert(self.__label.properties[name], name_as)
	
	def click(self):
		self.properties["selected"].toggle()
	
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
		return self.__pipe.properties["visible"]
