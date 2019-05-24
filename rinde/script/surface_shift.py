def shift_x(surface, expected_width):
	width, height = surface.get_size()
	
	return surface.subsurface(
		max(0, width - expected_width),
		0,
		min(width, expected_width),
		height
	)


def shift_y(surface, expected_height):
	width, height = surface.get_size()
	
	return surface.subsurface(
		0,
		max(0, height - expected_height),
		width,
		min(height, expected_height)
	)


def shift(surface, expected_width, expected_height):
	width, height = surface.get_size()
	
	return surface.subsurface(
		max(0, width - expected_width),
		max(0, height - expected_height),
		min(width, expected_width),
		min(height, expected_height)
	)
