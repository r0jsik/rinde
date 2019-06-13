import importlib
import re
import xml.etree.cElementTree as xml

from rinde.stage import StageFactory
from rinde.stage.node import ComplexNode
from rinde.stage.node import SimpleNode
from rinde.stage.node.util import Group


class AbstractXMLParser(object):
	def __init__(self, file):
		try:
			self.__parse_file(file)
		except IOError:
			raise IOError("Cannot load file: '%s'" % file)
	
	def __parse_file(self, file):
		document = open(file).read()
		
		self.__imported_types = self.__import_types(document)
		self.__root = xml.fromstring(document)
	
	def __import_types(self, document):
		types = {}
		regex = re.compile("<\?import (\w.+) \?>")
		
		for module in re.findall(regex, document):
			module_name, type_name = module.rsplit(".", 1)
			module = importlib.import_module(module_name)
			types[type_name] = getattr(module, type_name)
		
		return types
	
	def parse_root(self):
		return self.create_root(self.__parse_attributes(self.__root), self.__root.tag)
	
	def __parse_attributes(self, element):
		return {property: value for property, value in element.attrib.items()}
	
	def create_root(self, attributes, tag):
		raise NotImplementedError
	
	def parse(self):
		return self.__parse_elements(self.__root)
	
	def __parse_elements(self, elements):
		nodes = []
		
		for element in elements:
			attributes, children = self.__parse_element(element)
			node = self.parse_element(element.tag, attributes, children)
			nodes.append(node)
		
		return nodes
	
	def __parse_element(self, element):
		return self.__parse_attributes(element), self.__parse_elements(element)
	
	def parse_element(self, type_name, attributes, children):
		raise NotImplementedError
	
	def get_imported(self, type_name):
		try:
			return self.__imported_types[type_name]
		except KeyError:
			raise TypeError("Type not imported: '%s'" % type_name)


class AbstractLayoutParser(AbstractXMLParser):
	def __init__(self, stage_directory):
		super(AbstractLayoutParser, self).__init__("%s/layout.xml" % stage_directory)
	
	def parse_stage(self):
		stage = self.parse_root()
		self.__controller = stage.get_controller()
		
		return stage
	
	def create_root(self, attributes, tag):
		try:
			return self.create_stage(attributes, tag)
		except TypeError:
			raise TypeError("Invalid stage argumentation")
	
	def create_stage(self, attributes, tag):
		raise NotImplementedError
	
	def parse_element(self, type_name, attributes, children):
		if "action" in attributes:
			self.__convert_node_action(attributes)
		
		if "group" in attributes:
			self.__convert_node_group(attributes)
		
		try:
			node = self.__create_node(type_name, attributes, children)
		except TypeError as exception:
			raise TypeError("Invalid '%s' argumentation: %s" % (type_name, exception))
		
		if not isinstance(node, (SimpleNode, ComplexNode)):
			raise TypeError("Node must be a subclass of rinde.stage.node.ComplexNode or rinde.stage.node.SimpleNode")
		
		if "id" in attributes:
			self.__controller.nodes[attributes["id"]] = node
		
		return node
	
	def __convert_node_action(self, attributes):
		try:
			attributes["action"] = getattr(self.__controller, attributes["action"])
		except AttributeError:
			raise TypeError("Controller must implement method '%s'" % attributes["action"])
	
	def __convert_node_group(self, attributes):
		group_name = attributes["group"]
		
		if group_name not in self.__controller.groups:
			self.__controller.groups[group_name] = Group()
		
		attributes["group"] = self.__controller.groups[group_name]
	
	def __create_node(self, type_name, attributes, children):
		type = self.get_imported(type_name)
		
		if children:
			return type(children=children, **attributes)
		else:
			return type(**attributes)


class LayoutParserWithExistingController(AbstractLayoutParser):
	def __init__(self, stage_directory, controller):
		super(LayoutParserWithExistingController, self).__init__(stage_directory)
		
		self.__controller = controller
	
	def create_stage(self, attributes, tag):
		return StageFactory.create(tag, attributes, self.__controller)


class LayoutParserWithCreatingController(AbstractLayoutParser):
	def create_stage(self, attributes, tag):
		controller = self.__extract_controller_from_attributes(attributes)
		controller = self.__create_controller(controller)
		
		return StageFactory.create(tag, attributes, controller)
	
	def __extract_controller_from_attributes(self, attributes):
		try:
			return attributes.pop("controller")
		except KeyError:
			raise ValueError("Stage controller not specified")
	
	def __create_controller(self, controller):
		try:
			return self.__try_to_create_controller(controller)
		except ImportError:
			raise ImportError("Controller module not found")
		except AttributeError:
			raise ImportError("Controller class not found")
		except TypeError:
			raise TypeError("Controller constructor cannot take any argument")
	
	def __try_to_create_controller(self, controller):
		module_name, class_name = controller.rsplit(".", 1)
		module = importlib.import_module(module_name)
		controller = getattr(module, class_name)
		
		return controller()
