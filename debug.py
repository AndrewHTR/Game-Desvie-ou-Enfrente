import pygame

def draw_text(texto,color, surface, x, y):
	font = pygame.font.SysFont(None, 32)
	textobj = font.render(texto, True, color)
	textrect = textobj.get_rect()
	textrect.topleft = (x, y)
	surface.blit(textobj, textrect)
	
def display_fps(clock):
	screen = pygame.display.get_surface()

	draw_text(str(int(clock.get_fps())),(0, 255, 255), screen, 20, 20)