import os


class Resources:
	__ROOT = os.path.dirname(__file__)
	
	@staticmethod
	def get_path(resource):
		if resource.startswith("src"):
			return resource[5:-2]
		
		if resource.startswith("rinde_src"):
			return "%s/res/%s" % (Resources.__ROOT, resource[11:-2])
		
		return resource
	
	@staticmethod
	def get_path_to_rinde_file(resource):
		return "%s/res/%s" % (Resources.__ROOT, resource)
