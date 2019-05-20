from rinde.stage.node import ComplexNode
from rinde.stage.node.pane import Pane
from rinde.stage.node.region import ComplexNodeWithBackground
from rinde.stage.node.text import Text
from rinde.stage.node.text import PlaceholdedText
from rinde.stage.node.view import ImageView


class ChoiceBox(ComplexNode):
	def __init__(self, children, group, placeholder="", **kwargs):
		super(ChoiceBox, self).__init__(**kwargs)
		
		self.__group = group
		self.__group.on_selected = self.update
		
		self.__init_disposer(placeholder)
		self.__init_list_view(children, group)
		
		self.set_style_name("choice-box")
	
	def __init_disposer(self, placeholder):
		self.__disposer = Disposer(self, placeholder)
		self._insert_node(self.__disposer)
	
	def __init_list_view(self, children, group):
		self.__list_view = ListView(children, group)
		self.__list_view.properties["visible"] = self.__disposer.appearance.state["focused"]
		
		self._insert_node(self.__list_view)
	
	def get_hovered_node(self, mouse_position):
		for node in self.children():
			if node.can_be_hovered(mouse_position):
				return node.get_hovered_node(mouse_position)
		
		return self
	
	def update(self):
		if self.__group.get():
			option = self.__group.get_item()
			self.__disposer["text"] = option.get_text()
		else:
			self.__disposer["text"] = ""
	
	def update_layout(self):
		self.__list_view["position-y"] = self.__disposer.get_absolute_size("height")
	
	def insert_option(self, text, name, selected=False, index=None):
		self.__list_view.insert_option(text, name, selected, index)
	
	def remove_option_by_name(self, name):
		self.__list_view.remove_option(name)


class Disposer(ComplexNodeWithBackground):
	def __init__(self, combo_box, placeholder, **kwargs):
		super(Disposer, self).__init__(**kwargs)
		
		self.__combo_box = combo_box
		
		self.__init_placeholded_text(placeholder)
		self.__init_arrow()
		
		self.set_style_name("disposer")
	
	def __init_placeholded_text(self, placeholder):
		self.__placeholded_text = PlaceholdedText(placeholder=placeholder)
		
		self._borrow_property(self.__placeholded_text, "text")
		self._insert_node(self.__placeholded_text)
	
	def __init_arrow(self):
		self.__arrow = ImageView("rinde_src('disposer-arrow.png')")
		self.__arrow.set_style_name("arrow")
		
		self._insert_node(self.__arrow)
	
	def update_layout(self):
		self.__arrow["position-x"] = self.get_absolute_size("width") - self.__arrow.get_absolute_size("width")


class ListView(ComplexNodeWithBackground):
	def __init__(self, children, group, **kwargs):
		super(ListView, self).__init__(**kwargs)
		
		self.__group = group
		
		self.__init_pane(children)
		self.__insert_options_to_group(children)
		
		self.set_style_name("list-view")
	
	def __init_pane(self, nodes):
		self.__pane = Pane(nodes)
		self._insert_node(self.__pane)
	
	def __insert_options_to_group(self, options):
		for option in options:
			if isinstance(option, Option):
				option.insert_to_group(self.__group)
			else:
				raise TypeError("ListView's child must be an instance of rinde.stage.node.list.Option")
	
	def get_hovered_node(self, mouse_position):
		return self.__pane.get_hovered_node(mouse_position)
	
	def update_layout(self):
		position = 0
		
		for node in self.__pane.children():
			node["position-y"] = position
			position += node.get_absolute_size("height") + 1
		
		self.fit_background_size()
	
	def insert_option(self, text, name, selected=False, index=None):
		option = Option(text, name, selected)
		option.insert_to_group(self.__group)
		
		self.__pane._insert_node(option, index)
	
	def remove_option(self, name):
		for option in self.children():
			if option == name:
				self.__pane._remove_node(option)
				self.__group.remove(name)
				break


class Option(ComplexNodeWithBackground):
	def __init__(self, text, name, selected=False, **kwargs):
		super(Option, self).__init__(**kwargs)
		
		self.__text = text
		self.__name = name
		self.__group = None
		
		self.__init_text(text)
		
		self.appearance.create_state("selected", selected)
		self.set_style_name("option")
	
	def __init_text(self, text):
		text = Text(text)
		self._insert_node(text)
	
	def insert_to_group(self, group):
		self.__group = group
		self.__group.insert(self, self.__name)
	
	def activate(self):
		self.__group.select(self.__name)
	
	def is_selected(self):
		return self.appearance["selected"]
	
	def set_selected(self, value):
		self.appearance["selected"] = value
	
	def get_text(self):
		return self.__text
	
	def __eq__(self, other):
		return self.__name == other
