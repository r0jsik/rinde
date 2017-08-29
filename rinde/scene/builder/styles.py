import cssutils

from rinde.error import RindeException


class StylesheetParser(object):
	cssutils.ser.prefs.minimizeColorHash = False
	cssutils.log.enabled = False
	
	def __init__(self, file):
		try:
			self.__stylesheet = cssutils.parseFile(file)
		except IOError:
			raise RindeException("File %s not found" % file)
	
	def parse(self):
		styles = {}
		
		for rule in self.__stylesheet.cssRules:
			if isinstance(rule, cssutils.css.CSSComment):
				continue
			
			for selector in self.__get_selectors(rule):
				if selector in styles:
					styles[selector].update(rule)
				else:
					styles[selector] = self.__get_declarations(rule)
		
		return styles
	
	def __get_selectors(self, rule):
		selectors = rule.selectorText.split(",")
		selectors = [selector.strip() for selector in selectors]
		
		return selectors
	
	def __get_declarations(self, rule):
		return {style.name: self.__parse_value(style.value) for style in rule.style}
	
	def __parse_value(self, value):
		if value.startswith("#"):
			return int(value[1:], 16)
		
		elif value.lstrip("-").isdigit():
			return int(value)
		
		else:
			return value


class StylesParser(StylesheetParser):
	def __init__(self, scene_directory):
		super(StylesParser, self).__init__("%s/style.css" % scene_directory)
	
	def parse(self):
		styles = super(StylesParser, self).parse()
		styles = Styles(styles)
		
		return styles


class Styles:
	def __init__(self, styles):
		self.__styles = {}
		
		for selector in styles:
			self.__insert_style(selector, styles)
	
	def __insert_style(self, selector, styles):
		style_name, style_state = self.__split_selector(selector)
		
		if style_name not in self.__styles:
			self.__styles[style_name] = {}
		
		self.__styles[style_name][style_state] = styles[selector]
	
	def __split_selector(self, selector):
		selector = selector.split(":")
		
		try:
			return selector[0], selector[1]
		except IndexError:
			return selector[0], None
	
	def get_style(self, id, style_class, style_name):
		style = {None: {}}
		
		self.__update_style(style, "", style_name)
		self.__update_style(style, ".", style_class)
		self.__update_style(style, "#", id)
		
		return style
	
	def __update_style(self, style, prefix, variable):
		selector = "%s%s" % (prefix, variable)
		
		if variable and selector in self.__styles:
			style.update(self.__styles[selector])
