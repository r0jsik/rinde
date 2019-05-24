import pygame


def truncate_line(text, font, max_width):
	real = len(text)
	stext = text
	width = font.size(text)[0]
	cut = 0
	a = 0
	done = 1
	
	while width > max_width:
		a += 1
		n = text.rsplit(None, a)[0]
		
		if stext == n:
			cut += 1
			stext = n[:-cut]
		else:
			stext = n
		
		width = font.size(stext)[0]
		real = len(stext)
		done = 0
	
	return real, done, stext


def truncate_to_width(text, font, max_width):
	done = 0
	
	while not done:
		nl, done, line = truncate_line(text, font, max_width)
		text = text[nl:]
		
		yield line.strip()


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


def join_rendered_lines(width, height, rendered_lines):
	surface = pygame.Surface((width, height), pygame.SRCALPHA)
	position = 0
	
	for rendered_line in rendered_lines:
		surface.blit(rendered_line, (0, position))
		position += rendered_line.get_size()[1]
	
	return surface
