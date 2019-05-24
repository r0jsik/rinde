from rinde.script import text_lines
from rinde.stage.node import SimpleNode
from rinde.stage.node.util import Font


class TextualNode(SimpleNode):
	def __init__(self, text, **kwargs):
		super(TextualNode, self).__init__(**kwargs)
		
		self.properties.create("text", self.update, text)
		self.properties.create("font", self.update)
		self.properties.create_number("font-size", self.update)
		self.properties.create_number("color", self.update)
	
	def update(self):
		font = Font(self["font"], self["font-size"])
		
		surface = self.postprocess(self.render(font))
		
		self._set_surface(surface)
		self._fit_size_to_surface()
	
	def postprocess(self, surface):
		return surface
	
	def render(self, font):
		raise NotImplementedError


class Text(TextualNode):
	def __init__(self, text="", **kwargs):
		super(Text, self).__init__(text, **kwargs)
		
		self.set_style_name("text")
	
	def render(self, font):
		return font.render(self["text"], self["color"])
	

class Label(TextualNode):
	def __init__(self, **kwargs):
		super(Label, self).__init__(**kwargs)
		
		self.properties.create_number("shadow-color", self.update)
		
		self.set_style_name("label")
	
	def render(self, font):
		back = font.render(self["text"], self["shadow-color"])
		face = font.render(self["text"], self["color"])
		back.blit(face, (-1, -1))
		
		return back


class DraggableLabel(Label):
	def __init__(self, **kwargs):
		super(DraggableLabel, self).__init__(**kwargs)
		
		self.set_style_name("draggable-label")
	
	def drag(self, mouse_offset):
		self["position-x"] += mouse_offset[0]
		self["position-y"] += mouse_offset[1]


class PlaceholdedText(TextualNode):
	def __init__(self, text="", placeholder="", **kwargs):
		super(PlaceholdedText, self).__init__(text, **kwargs)
		
		self.properties.create("placeholder", self.update, placeholder)
		self.properties.create_number("placeholder-color", self.update)
		
		self.set_style_name("placeholded-text")
	
	def render(self, font):
		if self["text"] == "":
			return font.render(self["placeholder"], self["placeholder-color"])
		else:
			return font.render(self["text"], self["color"])


class TextFlow(TextualNode):
	def __init__(self, text="", **kwargs):
		super(TextFlow, self).__init__(text, **kwargs)
		
		self.set_style_name("text-flow")
	
	def render(self, font):
		return text_lines.render(self["text"].split("\n"), font, self["color"])
