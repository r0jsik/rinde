import cssutils

from rinde.error import RindeException
from rinde.data import Resources


class StylesParser:
	__RINDE_STYLESHEET = Resources.get_path("rinde.css")
	
	def __init__(self, scene_directory):
		self.__scene_stylesheet = "%s/style.css" % scene_directory
	
	def parse(self):
		rinde_stylesheet = self.__parse_stylesheet(self.__RINDE_STYLESHEET)
		scene_stylesheet = self.__parse_stylesheet(self.__scene_stylesheet)
		styles = Styles(rinde_stylesheet, scene_stylesheet)
		
		return styles
	
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
			name = declaration.name.replace("-", "_")
			value = self.__parse_value(declaration.value)
			declarations[name] = value
		
		return declarations
	
	def __parse_value(self, value):
		if value.startswith("#"):
			return int(value[1:], 16)
		
		if value.lstrip("-").isdigit():
			return int(value)
		
		return value


class Styles:
	def __init__(self, *stylesheets):
		self.__styles = {}
		
		for stylesheet in stylesheets:
			for selector, style in stylesheet.iteritems():
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
	
	def get_style(self, node):
		resultant_style = {None: {}}
		
		self.__update_style(resultant_style, "", node.style_name)
		self.__update_style(resultant_style, ".", node.style_class)
		self.__update_style(resultant_style, "#", node.id)
		
		return resultant_style
	
	def __update_style(self, resultant_style, prefix, variable):
		selector = "%s%s" % (prefix, variable)
		
		if variable and selector in self.__styles:
			styles = self.__styles[selector]
			
			for pseudoclass, style in styles.iteritems():
				if pseudoclass in resultant_style:
					resultant_style[pseudoclass].update(style)
				else:
					resultant_style[pseudoclass] = style
