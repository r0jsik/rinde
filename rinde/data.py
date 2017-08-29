import os


class Resources:
	__PATH = os.path.dirname(__file__)
	
	@staticmethod
	def get_path(resource):
		return os.path.join(Resources.__PATH, "res", resource)
