import importlib
import xml.etree.cElementTree as xml

from rinde.error import RindeException
from rinde.stage import StageFactory
from rinde.stage.node.creator import NodeCreator


class AbstractXMLParser(object):
	def __init__(self, file):
		try:
			self.__root = self.__get_root(file)
		except IOError:
			raise RindeException("File '%s' not found" % file)
		except xml.ParseError as exception:
			raise RindeException("XML %s" % exception)
	
	def __get_root(self, file):
		element_tree = xml.parse(file)
		element = element_tree.getroot()
		
		return element
	
	def parse_root(self):
		attributes = self.__parse_attributes(self.__root)
		root = self.create_root(attributes, self.__root.tag)
		
		return root
	
	def __parse_attributes(self, element):
		return {property: self.__parse_value(value) for property, value in element.attrib.iteritems()}
	
	def __parse_value(self, value):
		if value.lstrip("-").isdigit():
			return int(value)
		else:
			return value
	
	def create_root(self, attributes, tag):
		pass
	
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
	
	def parse_element(self, type, attributes, children):
		pass


class AbstractLayoutParser(AbstractXMLParser):
	def __init__(self, stage_directory):
		super(AbstractLayoutParser, self).__init__("%s/layout.xml" % stage_directory)
		
		self.__node_creator = NodeCreator()
		self.__stage = self.parse_root()
		self.__controller = self.__stage.get_controller()
	
	def create_root(self, attributes, tag):
		try:
			return self.create_stage(attributes, tag)
		except TypeError:
			raise RindeException("Incorrect stage argumentation")
	
	def create_stage(self, attributes, tag):
		pass
	
	def parse_element(self, type, attributes, children):
		try:
			return self.__parse_node(type, attributes, children)
		except TypeError:
			raise RindeException("Incorrect %s argumentation" % type)
	
	def __parse_node(self, type, attributes, children):
		if "action" in attributes:
			self.__convert_action_to_controller_method(attributes)
		
		node = self.__node_creator.create(type, attributes, children)
		
		if "id" in attributes:
			self.__insert_node_to_controller(attributes["id"], node)
		
		return node
	
	def __insert_node_to_controller(self, id, node):
		self.__controller.nodes[id] = node
	
	def __convert_action_to_controller_method(self, attributes):
		try:
			attributes["action"] = getattr(self.__controller, attributes["action"])
		except AttributeError:
			raise RindeException("Controller must implement method '%s'" % attributes["action"])
	
	def get_stage(self):
		return self.__stage


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
			raise RindeException("Stage controller not specified")
	
	def __create_controller(self, controller):
		try:
			return self.__try_to_create_controller(controller)
		except ImportError:
			raise RindeException("Controller module not found")
		except AttributeError:
			raise RindeException("Controller class not found")
		except TypeError:
			raise RindeException("Controller constructor cannot take any argument")
	
	def __try_to_create_controller(self, controller):
		module_name, class_name = controller.rsplit(".", -1)
		module = importlib.import_module(module_name)
		controller = getattr(module, class_name)
		
		return controller()
