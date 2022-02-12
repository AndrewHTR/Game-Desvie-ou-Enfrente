import pygame, sys, random
from pygame.locals import *
from debug import *

#Inicializanod pygame
pygame.init()

# Funções

# Função para fechar o jogo
def fechar():
	pygame.quit()
	sys.exit()

# Função para esperar usuario apertar alguma tecla
def esperarUsuario():
	while True:
		for event in pygame.event.get():
			if event.type == QUIT:
				fechar()
			if event.type == KEYDOWN:
				if event.key == K_q:
					fechar()
				return

# Função para desenhar texto na tela
def draw_text(texto, cor, tamanho, surface, x, y):
	font = pygame.font.SysFont("Arial", tamanho)
	text = font.render(texto, True, cor)
	textrect = text.get_rect()
	textrect.topleft = (x, y)
	surface.blit(text, textrect)




# Janela
WIDTH = 400
HEIGHT = 400
screen = pygame.display.set_mode((WIDTH, HEIGHT), 0 ,32)
pygame.display.set_caption("Devie ou enfrente!")
icon = pygame.image.load("Imagens/icon.png")
pygame.display.set_icon(icon)
clock = pygame.time.Clock()


def inicio():
	while True:
		for event in pygame.event.get():
			if event.type == QUIT:
				fechar()
			if event.type == KEYDOWN:
				if event.key == K_q:
					fechar()
				main()

			screen.fill((0, 0, 0))
			draw_text("DODGER GAME!", (255, 50, 30), 50, screen, WIDTH//3 - 130, HEIGHT//3 - 90)
			draw_text("BEM VINDO", (255, 255, 255), 36, screen, WIDTH//3 - 36, HEIGHT//3 - 10)
			draw_text("Aperte qualquer tecla para começar.", (255, 255, 255), 24, screen, WIDTH//3 - 125, HEIGHT//3 + 80)
			draw_text("Aperte Q para sair", (240, 240, 240), 20, screen, WIDTH//3 - 20, HEIGHT//3 + 150)
		pygame.display.update()

def main():
	# Inimigo
	velomin = 2
	velomax = 6
	tammin = 8 
	tammax = 40
	temporizador = 0
	newEnemy = 10
	inimigo = pygame.image.load("Imagens/food.png")
	inimigos = []

	# Jogador
	player = pygame.image.load("Imagens/player.png")
	pontostop = 0
	tamanho_player = 25
	reverseCheat = slowCheat = False

	# Movimentação Jogador	
	player_local = [WIDTH//2, HEIGHT//2]
	left = False
	right = False
	up = False
	down = False
	running = True
	
	pontos = 0
	while running:
		screen.fill((0, 0, 0))
		pontos += 0.1
		# Movimento Inimigo
		if not reverseCheat and not slowCheat:
			temporizador += 1
		if temporizador == newEnemy:
			temporizador = 0
			tamanho = random.randint(tammin, tammax)
			novo_inimigo = {'rect':pygame.Rect(random.randint(0, WIDTH - tamanho), 0 - tamanho, tamanho, tamanho),
							'speed':random.randint(velomin, velomax),
							'surface':pygame.transform.scale(inimigo, (tamanho, tamanho))}
			inimigos.append(novo_inimigo)

		for b in inimigos:
			if not reverseCheat and not slowCheat:
				b['rect'].move_ip(0, b['speed'])
			elif reverseCheat:
				b['rect'].move_ip(0, -5)
			elif slowCheat:
				b['rect'].move_ip(0, 1)

		for b in inimigos[:]:
			if b['rect'].top > HEIGHT:
				inimigos.remove(b)

		# Movimento Jogador
		player_rect = pygame.Rect(player_local[0], player_local[1], tamanho_player, tamanho_player)
		player = pygame.transform.scale(player, (tamanho_player, tamanho_player))
		if left == True:
			player_local[0] -= 5
		if right == True:
			player_local[0] += 5
		if up == True:
			player_local[1] -= 5
		if down == True:
			player_local[1] += 5

		# Checagem de colisão com a borda da tela
		if player_rect.top <= 0:
			if up == True:
				up = False
				player_local[1] = 0
		if player_rect.bottom >= HEIGHT:
			if down == True:
				down = False
				player_local[1] = HEIGHT - tamanho_player
		if player_rect.left <= 0:
			if left == True:
				left = False
				player_local[0] = 0
		if player_rect.right >= WIDTH:
			if right == True:
				right = False
				player_local[0] = WIDTH - tamanho_player

		for b in inimigos[:]:
			if b['rect'].colliderect(player_rect):
				running = False
				if pontostop < pontos:
					pontostop = pontos

		for event in pygame.event.get():
			if event.type == QUIT:
				fechar()

			if event.type == KEYDOWN:
				if event.key == K_LEFT:
					left = True
				if event.key == K_RIGHT:
					right = True
				if event.key == K_UP:
					up = True
				if event.key == K_DOWN:
					down = True

				if event.key == K_x:
					reverseCheat = True
					score = 0
				if event.key == K_z:
					slowCheat = True
					score = 0

			if event.type == KEYUP:
				if event.key == K_LEFT:
					left = False
				if event.key == K_RIGHT:
					right = False
				if event.key == K_UP:
					up = False
				if event.key == K_DOWN:
					down = False

				if event.key == K_x:
					reverseCheat = False
				if event.key == K_z:
					slowCheat = False

		for enemy in inimigos:
			screen.blit(enemy['surface'], enemy['rect'])

		

		draw_text(f"Pontuação: {str(f'{pontos:.0f}')}", (255 ,255, 255), 24, screen, 20, 40)
		draw_text(f"Melhor Pontuação: {str(f'{pontostop:.0f}')}", (255 ,255, 255), 24, screen, 20, 60)
		screen.blit(player, player_rect)
		display_fps(clock)
		pygame.display.update()
		clock.tick(60)
	screen.fill((0,0,0))
	draw_text("Você Perdeu!",(255, 255, 255),24, screen, WIDTH//3, HEIGHT//3)
	draw_text("Aperte qualquer tecla para sair.",(255, 255, 255),24, screen, WIDTH//3 - 100, WIDTH//3 + 40)

	pygame.display.update()
	esperarUsuario()

inicio()