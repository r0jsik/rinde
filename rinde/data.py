import os
import re


class Resources:
	__ROOT = os.path.dirname(__file__)
	
	@staticmethod
	def get_path(resource):
		external_resource = Resources.__as_external(resource)
		
		if external_resource:
			return external_resource.group(1)
		else:
			return os.path.join(Resources.__ROOT, "res", resource)
	
	@staticmethod
	def __as_external(resource):
		
		# Resource looks like: src('path/to/resource/foo.bar')
		regex = re.compile("^src\([\'\"]([\w\s./\\\\]+)[\'\"]\)$")
		match = re.match(regex, resource)
		
		return match
