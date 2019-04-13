import cssutils

from rinde.data import Resources


class StylesParser:
	__PATH_TO_RINDE_STYLESHEET = Resources.get_path_to_rinde_file("rinde.css")
	
	def __init__(self, stage_directory):
		self.__path_to_stage_stylesheet = "%s/style.css" % stage_directory
	
	def parse(self):
		data = {}
		
		stylesheet_parser = StylesheetParser(self.__PATH_TO_RINDE_STYLESHEET)
		stylesheet_parser.parse_to(data)
		
		stylesheet_parser = StylesheetParser(self.__path_to_stage_stylesheet)
		stylesheet_parser.parse_to(data)
		
		return Styles(data)


class StylesheetParser(object):
	cssutils.ser.prefs.minimizeColorHash = False
	cssutils.log.enabled = False
	
	def __init__(self, file):
		try:
			self.__stylesheet = cssutils.parseFile(file)
		except IOError:
			raise IOError("Cannot load file: '%s'" % file)
	
	def parse_to(self, data):
		for rule_group in self.__stylesheet.cssRules:
			if self.__not_comment(rule_group):
				self.__parse_rule(rule_group, data)
	
	def __not_comment(self, rule_group):
		return not isinstance(rule_group, cssutils.css.CSSComment)
	
	def __parse_rule(self, rule_group, data):
		declarations = self.__get_declarations(rule_group)
		
		for rule in self.__get_subrules(rule_group):
			selector_groups = rule.strip().split()
			selector, state = self.__split_selector_group(selector_groups.pop(0))
			
			if selector not in data:
				data[selector] = Style(selector)
			
			style = data[selector]
			continuous = True
			
			for selector_group in selector_groups:
				child_selector, child_state = self.__split_selector_group(selector_group)
				
				if continuous and style.has_child(state, child_selector):
					child = style.get_child(state, child_selector)
				else:
					child = Style(child_selector)
					style.add_child(state, child)
					continuous = False
				
				style = child
				state = child_state
			
			style.add_declarations(state, declarations)
	
	def __get_declarations(self, rule_group):
		return {declaration.name: self.__parse_value(declaration.value) for declaration in rule_group.style}
	
	def __parse_value(self, value):
		if value.startswith("#"):
			return int(value[1:], 16)
		
		if value.lstrip("-").isdigit():
			return int(value)
		
		# If value between quotes
		if value[0] == value[-1] and value[0] in ["\"", "'"]:
			return value[1:-1]
		
		return value.strip()
	
	def __get_subrules(self, rule_group):
		return rule_group.selectorText.split(",")
	
	def __split_selector_group(self, selector_group):
		if ":" in selector_group:
			return selector_group.split(":", 1)
		else:
			return selector_group, None


class Styles:
	def __init__(self, data):
		self.__data = data
	
	def get_for(self, node):
		style = []
		
		for selector in node.style_selectors():
			if selector in self.__data:
				style.append(self.__data[selector])
		
		return style


class Style:
	def __init__(self, selector):
		self.__selector = selector
		self.__children = {}
		self.__declarations = {}
	
	def add_child(self, state, child):
		if state in self.__children:
			self.__children[state].append(child)
		else:
			self.__children[state] = [child]
	
	def has_child(self, state, selector):
		return state in self.__children and selector in self.__children[state]
	
	def get_child(self, state, selector):
		for child in self.get_children(state):
			if child == selector:
				return child
	
	def get_children(self, state):
		return self.__children.get(state, ())
	
	def add_declarations(self, state, declarations):
		if state in self.__declarations:
			self.__declarations[state].update(declarations)
		else:
			self.__declarations[state] = declarations.copy()
	
	def get_declarations(self, state):
		if state in self.__declarations:
			return self.__declarations[state].items()
		
		return ()
	
	def __eq__(self, object):
		return object == self.__selector
