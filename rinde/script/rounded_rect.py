import pygame


"""
Creates new instance of pygame.Surface and fills it with a rounded rectangle with specified parameters.

:param color: color of the content [as (r, g, b, a) tuple/list of ints]
:param width: width of the rectangle [in pixels]
:param height: height of the rectangle [in pixels]
:param radius: radius of the rounding [as number in range <0, 100>]

:returns: pygame.Surface
"""
def render(color, width, height, radius):
	if radius < 0 or radius > 100:
		raise ValueError("Radius must be in range <0, 100>")
	else:
		radius /= 100.0
	
	rectangle = pygame.Rect(0, 0, width, height)
	surface = pygame.Surface(rectangle.size, pygame.SRCALPHA)
	
	corner = pygame.Surface([min(rectangle.size) * 2] * 2, pygame.SRCALPHA)
	pygame.draw.ellipse(corner, (0, 0, 0), corner.get_rect())
	corner = pygame.transform.smoothscale(corner, [int(min(rectangle.size) * radius)] * 2)
	
	radius = surface.blit(corner, (0, 0))
	
	radius.bottomright = rectangle.bottomright
	surface.blit(corner, radius)
	
	radius.topright = rectangle.topright
	surface.blit(corner, radius)
	
	radius.bottomleft = rectangle.bottomleft
	surface.blit(corner, radius)
	
	surface.fill((0, 0, 0), rectangle.inflate(-radius.w, 0))
	surface.fill((0, 0, 0), rectangle.inflate(0, -radius.h))
	surface.fill((255, 255, 255), special_flags=pygame.BLEND_RGBA_MIN)
	surface.fill(color, special_flags=pygame.BLEND_RGBA_MAX)
	
	return surface
