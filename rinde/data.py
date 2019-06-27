import os


"""
Represents an interface that returns paths to resources used by the library.
"""
class Resources:
	
	"""
	An absolute path to main library's resources directory.
	"""
	__ROOT = os.path.dirname(__file__) + "/res/"
	
	"""
	Returns a path to a specified resource.
	"""
	@staticmethod
	def get_path(resource):
		
		# If the resource looks like: src('path/to/resource.ext')
		if resource.startswith("src"):
			return resource[5:-2]
		
		# If the resource looks like: rinde_src('path/to/resource.ext')
		if resource.startswith("rinde_src"):
			return Resources.__ROOT + resource[11:-2]
		
		return resource
	
	"""
	Returns a path to a specified resource from main library's resource directory.
	"""
	@staticmethod
	def get_path_to_rinde_file(resource):
		return Resources.__ROOT + resource
