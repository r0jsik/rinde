import pygame


"""
Splits the text in such a way that none of the line rendered by the pygame.font.Font object will exceed expected width.

:returns: a generator that yields string for each line whose rendered surface's length won't exceed expected width
"""
def truncate_to_width(text, font, max_width):
	done = 0
	
	while not done:
		real, done, line = truncate_line(text, font, max_width)
		text = text[real:]
		
		yield line.strip()


"""
Finds how many letters could be rendered in one line (on pygame.Surface) not to exceed maximum width.

:returns: data used by the algorithm to truncate lines
"""
def truncate_line(text, font, max_width):
	real = len(text)
	line = text
	width = font.size(text)[0]
	cut = 0
	a = 0
	done = 1
	
	while width > max_width:
		a += 1
		n = text.rsplit(None, a)[0]
		
		if line == n:
			cut += 1
			line = n[:-cut]
		else:
			line = n
		
		width = font.size(line)[0]
		real = len(line)
		done = 0
	
	return real, done, line


"""
Renders string lines as text blitted into pygame.Surface object.

:returns: pygame.Surface
"""
def render(lines, font, color):
	rendered_lines = []
	width = height = 0
	
	for line in lines:
		rendered_line = font.render(line, color)
		rendered_lines.append(rendered_line)
		
		line_width, line_height = rendered_line.get_size()
		height += line_height
		
		if width < line_width:
			width = line_width
	
	return join_rendered_lines(width, height, rendered_lines)


"""
Joins rendered surfaces (one under the other) into one, total surface.

:returns: pygame.Surface
"""
def join_rendered_lines(width, height, rendered_lines):
	surface = pygame.Surface((width, height), pygame.SRCALPHA)
	position = 0
	
	for rendered_line in rendered_lines:
		surface.blit(rendered_line, (0, position))
		position += rendered_line.get_size()[1]
	
	return surface
