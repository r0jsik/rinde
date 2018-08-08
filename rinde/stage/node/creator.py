import importlib
import pkgutil

from rinde.error import RindeException


class NodeCreator:
	def __init__(self):
		self.__node_types = NodeTypes()
	
	def create(self, type_name, attributes, children):
		node_type = self.__node_types.get_node_type(type_name)
		
		if node_type:
			return self.__create_node(node_type, attributes, children)
		
		raise RindeException("Unknown node type: '%s'" % type_name)
	
	def __create_node(self, node_type, attributes, children):
		if children:
			return node_type(nodes=children, **attributes)
		else:
			return node_type(**attributes)


class NodeTypes:
	def __init__(self):
		self.__modules = self.__import_modules("rinde.stage.node")
	
	def __import_modules(self, module_name):
		modules = []
		
		module = importlib.import_module(module_name)
		modules.append(module)
		
		submodules = self.__import_submodules(module_name)
		modules.extend(submodules)
		
		return modules
	
	def __import_submodules(self, module_name):
		loader = pkgutil.get_loader(module_name)
		modules = []
		
		for importer, submodule_name, is_package in pkgutil.walk_packages([loader.filename]):
			submodules = self.__import_modules(module_name + "." + submodule_name)
			modules.extend(submodules)
		
		return modules
	
	def get_node_type(self, type_name):
		for module in self.__modules:
			try:
				return module.__dict__[type_name]
			except KeyError:
				continue
