import pygame


def render(color, bounds, radius):
	rectangle = pygame.Rect(0, 0, bounds[2], bounds[3])
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
