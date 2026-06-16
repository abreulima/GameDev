import pygame
import sys

pygame.init()

LARGURA, ALTURA = 900, 500
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Jogo de Plataforma")

relogio = pygame.time.Clock()

# Cores
AZUL_CEU = (135, 206, 235)
VERDE = (80, 180, 80)
MARROM = (120, 80, 40)
PRETO = (0, 0, 0)

# Imagens
jogador_img = pygame.image.load("artes/jogador.png").convert_alpha()
inimigo_img = pygame.image.load("artes/inimigo.png").convert_alpha()

jogador_img = pygame.transform.scale(jogador_img, (50, 60))
inimigo_img = pygame.transform.scale(inimigo_img, (50, 50))

# Jogador
jogador = pygame.Rect(100, 300, 50, 60)
vel_y = 0
velocidade = 5
gravidade = 0.8
forca_pulo = -15
no_chao = False

# Plataformas
plataformas = [
    pygame.Rect(0, 440, 900, 60),
    pygame.Rect(200, 350, 180, 25),
    pygame.Rect(460, 280, 180, 25),
    pygame.Rect(700, 210, 140, 25),
]

# Inimigo
inimigo = pygame.Rect(500, 230, 50, 50)
inimigo_vel = 2

# Objetivo
objetivo = pygame.Rect(800, 160, 40, 50)

fonte = pygame.font.SysFont(None, 40)

def mostrar_texto(texto):
    img = fonte.render(texto, True, PRETO)
    tela.blit(img, (LARGURA // 2 - img.get_width() // 2, 40))

while True:
    relogio.tick(60)

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    teclas = pygame.key.get_pressed()

    dx = 0
    if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
        dx = -velocidade
    if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
        dx = velocidade

    if (teclas[pygame.K_SPACE] or teclas[pygame.K_UP]) and no_chao:
        vel_y = forca_pulo
        no_chao = False

    # Movimento horizontal
    jogador.x += dx

    # Gravidade
    vel_y += gravidade
    jogador.y += vel_y

    no_chao = False

    # Colisão com plataformas
    for plataforma in plataformas:
        if jogador.colliderect(plataforma):
            if vel_y > 0:
                jogador.bottom = plataforma.top
                vel_y = 0
                no_chao = True
            elif vel_y < 0:
                jogador.top = plataforma.bottom
                vel_y = 0

    # Limites da tela
    if jogador.left < 0:
        jogador.left = 0
    if jogador.right > LARGURA:
        jogador.right = LARGURA

    # Movimento do inimigo
    inimigo.x += inimigo_vel
    if inimigo.left < 460 or inimigo.right > 640:
        inimigo_vel *= -1

    # Derrota
    if jogador.colliderect(inimigo) or jogador.top > ALTURA:
        jogador.x, jogador.y = 100, 300
        vel_y = 0

    # Vitória
    venceu = jogador.colliderect(objetivo)

    # Desenho
    tela.fill(AZUL_CEU)

    for plataforma in plataformas:
        pygame.draw.rect(tela, MARROM, plataforma)
        pygame.draw.rect(tela, VERDE, (plataforma.x, plataforma.y, plataforma.width, 8))

    pygame.draw.rect(tela, (255, 215, 0), objetivo)

    tela.blit(jogador_img, jogador)
    tela.blit(inimigo_img, inimigo)

    if venceu:
        mostrar_texto("Você venceu!")

    pygame.display.flip()
