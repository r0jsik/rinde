"""
Crops the surface from the left side to fit its width to the expected value.

:returns: pygame.Surface
"""
def shift_x(surface, expected_width):
	width, height = surface.get_size()
	
	return surface.subsurface(
		max(0, width - expected_width),
		0,
		min(width, expected_width),
		height
	)


"""
Crops the surface from the top side to fit its height to the expected value.

:returns: pygame.Surface
"""
def shift_y(surface, expected_height):
	width, height = surface.get_size()
	
	return surface.subsurface(
		0,
		max(0, height - expected_height),
		width,
		min(height, expected_height)
	)


"""
Crops the surface from the top-left point to fit its size to the expected value.

:returns: pygame.Surface
"""
def shift(surface, expected_width, expected_height):
	width, height = surface.get_size()
	
	return surface.subsurface(
		max(0, width - expected_width),
		max(0, height - expected_height),
		min(width, expected_width),
		min(height, expected_height)
	)
