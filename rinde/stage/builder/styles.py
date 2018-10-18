import cssutils

from rinde.data import Resources
from rinde.error import RindeException


class StylesParser:
	__RINDE_STYLESHEET = Resources.get_path("rinde.css")
	
	def __init__(self, stage_directory):
		self.__stage_stylesheet = "%s/style.css" % stage_directory
	
	def parse(self):
		rinde_stylesheet = self.__parse_stylesheet(self.__RINDE_STYLESHEET)
		stage_stylesheet = self.__parse_stylesheet(self.__stage_stylesheet)
		
		return Styles(rinde_stylesheet, stage_stylesheet)
	
	def __parse_stylesheet(self, stylesheet):
		return StylesheetParser(stylesheet).parse()


class StylesheetParser(object):
	cssutils.ser.prefs.minimizeColorHash = False
	cssutils.log.enabled = False
	
	def __init__(self, file):
		try:
			self.__stylesheet = cssutils.parseFile(file)
		except IOError:
			raise RindeException("File %s not found" % file)
	
	def parse(self):
		stylesheet = {}
		
		for rule in self.__stylesheet.cssRules:
			if isinstance(rule, cssutils.css.CSSComment):
				continue
			
			for selector in self.__get_selectors(rule):
				declarations = self.__get_declarations(rule)
				
				if selector in stylesheet:
					stylesheet[selector].update(declarations)
				else:
					stylesheet[selector] = declarations
		
		return stylesheet
	
	def __get_selectors(self, rule):
		return [selector.strip() for selector in rule.selectorText.split(",")]
	
	def __get_declarations(self, rule):
		declarations = {}
		
		for declaration in rule.style:
			value = self.__parse_value(declaration.value)
			declarations[declaration.name] = value
		
		return declarations
	
	def __parse_value(self, value):
		if value.startswith("#"):
			return int(value[1:], 16)
		
		if value.lstrip("-").isdigit():
			return int(value)
		
		# If value between quotes
		if value[0] == value[-1] and value[0] in ["\"", "'"]:
			return value[1:-1]
		
		return value.strip()


class Styles:
	def __init__(self, *stylesheets):
		self.__styles = {}
		
		for stylesheet in stylesheets:
			for selector, style in stylesheet.items():
				self.__insert_style(selector, style)
	
	def __insert_style(self, selector, style):
		style_name, pseudoclass = self.__split_selector(selector)
		
		if style_name not in self.__styles:
			self.__styles[style_name] = {}
		
		if pseudoclass in self.__styles[style_name]:
			self.__styles[style_name][pseudoclass].update(style)
		else:
			self.__styles[style_name][pseudoclass] = style
	
	def __split_selector(self, selector):
		part = selector.split(":")
		
		try:
			return part[0], part[1]
		except IndexError:
			return part[0], None
	
	def get_declarations_for(self, node):
		declarations = {None: {}}
		
		for selector in node.get_style_selectors():
			self.__update_declarations(declarations, selector)
		
		return declarations
	
	def __update_declarations(self, declarations, selector):
		if selector in self.__styles:
			styles = self.__styles[selector]
			
			for state, style in styles.items():
				if state in declarations:
					declarations[state].update(style)
				else:
					declarations[state] = style
