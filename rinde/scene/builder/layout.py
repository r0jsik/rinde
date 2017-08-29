import importlib
import xml.etree.cElementTree
import rinde.scene.node

from rinde.error import RindeException
from rinde.scene import Scene


class XMLParserBase(object):
	def __init__(self, file):
		try:
			self.__root = self.__get_root(file)
		except IOError:
			raise RindeException("File '%s' not found" % file)
		except xml.etree.cElementTree.ParseError as exception:
			raise RindeException("Layout %s" % exception)
	
	def __get_root(self, file):
		element_tree = xml.etree.cElementTree.parse(file)
		element = element_tree.getroot()
		
		return element
	
	def parse_root(self):
		attributes = self.__parse_attributes(self.__root)
		parent = self._parse_root(attributes)
		
		return parent
	
	def __parse_attributes(self, element):
		attributes = {}
		
		for property, value in element.attrib.iteritems():
			attributes[property] = self.__parse_value(value)
		
		return attributes
	
	def __parse_value(self, value):
		if value.isdigit():
			return int(value)
		else:
			return value
	
	def _parse_root(self, attributes):
		pass
	
	def parse(self):
		return self.__parse_nodes(self.__root)
	
	def __parse_nodes(self, elements):
		objects = []
		
		for element in elements:
			attributes, children = self.__parse_element(element)
			object = self._parse_node(element.tag, attributes, children)
			objects.append(object)
		
		return objects
	
	def __parse_element(self, element):
		return self.__parse_attributes(element), self.__parse_nodes(element)
	
	def _parse_node(self, type, attributes, children):
		pass


class LayoutParserBase(XMLParserBase):
	def __init__(self, scene_directory):
		super(LayoutParserBase, self).__init__("%s/layout.xml" % scene_directory)
		
		self.__scene = self.parse_root()
		self.__controller = self.__scene.get_controller()
	
	def _parse_root(self, attributes):
		try:
			return self._create_scene(attributes)
		except TypeError:
			raise RindeException("Incorrect scene argumentation")
	
	def _create_scene(self, attributes):
		pass
	
	def _parse_node(self, type, attributes, children):
		try:
			return self.__try_to_parse_node(type, attributes)
		except AttributeError:
			raise RindeException("Unknown node type: '%s'" % type)
		except TypeError:
			raise RindeException("Incorrect %s argumentation" % type)
	
	def __try_to_parse_node(self, type, attributes):
		self.__convert_action(attributes)
		
		node = self.__create_node(type, attributes)
		
		if "id" in attributes:
			self.__controller.add_node(attributes["id"], node)
		
		return node
	
	def __convert_action(self, attributes):
		try:
			attributes["action"] = getattr(self.__controller, attributes["action"])
		except KeyError:
			pass
		except AttributeError:
			raise RindeException("Controller must implement method '%s'" % attributes["action"])
	
	def __create_node(self, type, attributes):
		type = self.__camel_case(type)
		node_type = getattr(rinde.scene.node, type)
		node = node_type(**attributes)
		
		return node
	
	def __camel_case(self, string):
		return string.title().replace("-", "")
	
	def get_scene(self):
		return self.__scene


class LayoutParserWithCustomController(LayoutParserBase):
	def __init__(self, scene_directory, controller):
		super(LayoutParserWithCustomController, self).__init__(scene_directory)
		
		self.__controller = controller
	
	def _create_scene(self, attributes):
		return Scene(self.__controller, **attributes)


class LayoutParserWhichMakesController(LayoutParserBase):
	def _create_scene(self, attributes):
		controller = self.__extract_controller_from_attributes(attributes)
		controller = self.__create_controller(controller)
		scene = Scene(controller, **attributes)
		
		return scene
	
	def __extract_controller_from_attributes(self, attributes):
		try:
			return attributes.pop("controller")
		except KeyError:
			raise RindeException("Scene controller not specified")
	
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
		module_name, class_name = controller.rsplit(".", 1)
		module = importlib.import_module(module_name)
		controller = getattr(module, class_name)
		
		return controller()
