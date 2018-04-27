import os
import re


class Resources:
	__PATH = os.path.dirname(__file__)
	
	@staticmethod
	def get_path(resource):
		external_resource = re.match("^src\([\'\"]([\w\s./\\\\]+)[\'\"]\)$", resource)
		
		if external_resource:
			return external_resource.group(1)
		else:
			return os.path.join(Resources.__PATH, "res", resource)
