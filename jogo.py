import pygame
import sys

pygame.init()

LARGURA, ALTURA = 900, 500
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Jogo de Plataforma")

relogio = pygame.time.Clock()

AZUL_CEU = (135, 206, 235)
VERDE = (80, 180, 80)
MARROM = (120, 80, 40)
PRETO = (0, 0, 0)
OURO = (255, 215, 0)

jogador_img = pygame.image.load("artes/jogador.png").convert_alpha()
inimigo_img = pygame.image.load("artes/inimigo.png").convert_alpha()

jogador_img = pygame.transform.scale(jogador_img, (50, 60))
inimigo_img = pygame.transform.scale(inimigo_img, (50, 50))

jogador = pygame.Rect(100, 300, 50, 60)
vel_y = 0
velocidade = 5
gravidade = 0.8
forca_pulo = -15
no_chao = False

LARGURA_NIVEL = 2600

plataformas = [
    pygame.Rect(0, 440, 700, 60),
    pygame.Rect(760, 440, 500, 60),
    pygame.Rect(1350, 440, 500, 60),
    pygame.Rect(1950, 440, 650, 60),

    pygame.Rect(220, 350, 180, 25),
    pygame.Rect(520, 300, 160, 25),
    pygame.Rect(850, 360, 180, 25),
    pygame.Rect(1120, 310, 170, 25),
    pygame.Rect(1450, 350, 180, 25),
    pygame.Rect(1730, 290, 160, 25),
    pygame.Rect(2050, 340, 180, 25),
    pygame.Rect(2320, 260, 170, 25),
]

inimigos = [
    {"rect": pygame.Rect(520, 250, 50, 50), "vel": 2, "min": 500, "max": 680},
    {"rect": pygame.Rect(920, 390, 50, 50), "vel": 2, "min": 760, "max": 1260},
    {"rect": pygame.Rect(1500, 390, 50, 50), "vel": 3, "min": 1350, "max": 1850},
    {"rect": pygame.Rect(2100, 390, 50, 50), "vel": 2, "min": 1950, "max": 2600},
]

objetivo = pygame.Rect(2500, 190, 50, 70)

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

    jogador.x += dx

    if jogador.left < 0:
        jogador.left = 0
    if jogador.right > LARGURA_NIVEL:
        jogador.right = LARGURA_NIVEL

    vel_y += gravidade
    jogador.y += vel_y

    no_chao = False

    for plataforma in plataformas:
        if jogador.colliderect(plataforma):
            if vel_y > 0:
                jogador.bottom = plataforma.top
                vel_y = 0
                no_chao = True
            elif vel_y < 0:
                jogador.top = plataforma.bottom
                vel_y = 0

    for inimigo in inimigos:
        inimigo["rect"].x += inimigo["vel"]

        if inimigo["rect"].left < inimigo["min"] or inimigo["rect"].right > inimigo["max"]:
            inimigo["vel"] *= -1

        if jogador.colliderect(inimigo["rect"]):
            jogador.x, jogador.y = 100, 300
            vel_y = 0

    if jogador.top > ALTURA:
        jogador.x, jogador.y = 100, 300
        vel_y = 0

    venceu = jogador.colliderect(objetivo)

    camera_x = jogador.centerx - LARGURA // 2
    camera_x = max(0, min(camera_x, LARGURA_NIVEL - LARGURA))

    tela.fill(AZUL_CEU)

    for plataforma in plataformas:
        p = plataforma.move(-camera_x, 0)
        pygame.draw.rect(tela, MARROM, p)
        pygame.draw.rect(tela, VERDE, (p.x, p.y, p.width, 8))

    objetivo_tela = objetivo.move(-camera_x, 0)
    pygame.draw.rect(tela, OURO, objetivo_tela)

    for inimigo in inimigos:
        tela.blit(inimigo_img, inimigo["rect"].move(-camera_x, 0))

    tela.blit(jogador_img, jogador.move(-camera_x, 0))

    if venceu:
        mostrar_texto("Você venceu!")

    pygame.display.flip()
