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

jogador_img = pygame.image.load("artes/jogador.png").convert_alpha()
inimigo_img = pygame.image.load("artes/inimigo.png").convert_alpha()
fundo_img = pygame.image.load("artes/fundo.png").convert()
vida_img = pygame.image.load("artes/vida.png").convert_alpha()
coletavel_img = pygame.image.load("artes/coletavel.png").convert_alpha()
objetivo_img = pygame.image.load("artes/objetivo.png").convert_alpha()
especial_img = pygame.image.load("artes/especial.png").convert_alpha()

jogador_img = pygame.transform.scale(jogador_img, (50, 60))
inimigo_img = pygame.transform.scale(inimigo_img, (50, 50))
fundo_img = pygame.transform.scale(fundo_img, (LARGURA, ALTURA))
vida_img = pygame.transform.scale(vida_img, (32, 32))
coletavel_img = pygame.transform.scale(coletavel_img, (32, 32))
objetivo_img = pygame.transform.scale(objetivo_img, (64, 64))
especial_img = pygame.transform.scale(especial_img, (24, 24))

jogador = pygame.Rect(100, 300, 50, 60)
vel_y = 0
velocidade = 5
gravidade = 0.8
forca_pulo = -15
forca_salto_duplo = -11
no_chao = False
saltos_restantes = 2
vidas = 3
jogo_terminou = False
direcao_jogador = 1
especiais = []
cooldown_especial = 5000
ultimo_arremesso = -cooldown_especial

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

coletaveis = [
    pygame.Rect(290, 310, 32, 32),
    pygame.Rect(585, 260, 32, 32),
    pygame.Rect(925, 320, 32, 32),
    pygame.Rect(1185, 270, 32, 32),
    pygame.Rect(1515, 310, 32, 32),
    pygame.Rect(1785, 250, 32, 32),
    pygame.Rect(2115, 300, 32, 32),
    pygame.Rect(2385, 220, 32, 32),
]
total_coletaveis = len(coletaveis)

objetivo = pygame.Rect(2500, 196, 64, 64)

fonte = pygame.font.SysFont(None, 40)

def desenhar_fundo(camera_x):
    deslocamento = int(camera_x * 0.35) % LARGURA

    tela.blit(fundo_img, (-deslocamento, 0))
    tela.blit(fundo_img, (LARGURA - deslocamento, 0))

def mostrar_texto(texto):
    img = fonte.render(texto, True, PRETO)
    tela.blit(img, (LARGURA // 2 - img.get_width() // 2, 40))

def mostrar_vidas():
    for i in range(vidas):
        tela.blit(vida_img, (20 + i * 38, 20))

def mostrar_coletaveis():
    texto = f"{total_coletaveis - len(coletaveis)}/{total_coletaveis}"
    img = fonte.render(texto, True, PRETO)
    tela.blit(coletavel_img, (20, 60))
    tela.blit(img, (60, 60))

def mostrar_cooldown_especial():
    largura_barra = 150
    altura_barra = 14
    x, y = 20, 105
    agora = pygame.time.get_ticks()
    progresso = min(1, (agora - ultimo_arremesso) / cooldown_especial)
    preenchimento = int((largura_barra - 4) * progresso)

    tela.blit(especial_img, (x, y - 5))
    pygame.draw.rect(tela, PRETO, (x + 34, y, largura_barra, altura_barra), 2)
    pygame.draw.rect(tela, VERDE, (x + 36, y + 2, preenchimento, altura_barra - 4))

def arremessar_especial():
    global ultimo_arremesso

    agora = pygame.time.get_ticks()
    if agora - ultimo_arremesso < cooldown_especial:
        return

    rect = especial_img.get_rect(center=jogador.center)
    especiais.append({"rect": rect, "vel": direcao_jogador * 10})
    ultimo_arremesso = agora

def atualizar_especiais():
    for especial in especiais[:]:
        especial["rect"].x += especial["vel"]

        if especial["rect"].right < 0 or especial["rect"].left > LARGURA_NIVEL:
            especiais.remove(especial)
            continue

        for inimigo in inimigos[:]:
            if especial["rect"].colliderect(inimigo["rect"]):
                especiais.remove(especial)
                inimigos.remove(inimigo)
                break

def reiniciar_jogador():
    global vel_y, no_chao, saltos_restantes

    jogador.x, jogador.y = 100, 300
    vel_y = 0
    no_chao = False
    saltos_restantes = 2

def perder_vida():
    global vidas

    vidas -= 1
    reiniciar_jogador()

while True:
    relogio.tick(60)

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if evento.type == pygame.KEYDOWN and evento.key in (pygame.K_SPACE, pygame.K_UP) and not jogo_terminou:
            if saltos_restantes > 0:
                vel_y = forca_pulo if saltos_restantes == 2 else forca_salto_duplo
                no_chao = False
                saltos_restantes -= 1
        if evento.type == pygame.KEYDOWN and evento.key == pygame.K_f and not jogo_terminou:
            arremessar_especial()

    venceu = not coletaveis and jogador.colliderect(objetivo)
    jogo_terminou = venceu or vidas <= 0

    if not jogo_terminou:
        teclas = pygame.key.get_pressed()

        dx = 0
        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            dx = -velocidade
            direcao_jogador = -1
        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            dx = velocidade
            direcao_jogador = 1

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
                    saltos_restantes = 2
                elif vel_y < 0:
                    jogador.top = plataforma.bottom
                    vel_y = 0

        for inimigo in inimigos:
            inimigo["rect"].x += inimigo["vel"]

            if inimigo["rect"].left < inimigo["min"] or inimigo["rect"].right > inimigo["max"]:
                inimigo["vel"] *= -1

            if jogador.colliderect(inimigo["rect"]):
                perder_vida()
                break

        atualizar_especiais()

        for coletavel in coletaveis[:]:
            if jogador.colliderect(coletavel):
                coletaveis.remove(coletavel)

        if jogador.top > ALTURA:
            perder_vida()

        venceu = not coletaveis and jogador.colliderect(objetivo)
        jogo_terminou = venceu or vidas <= 0

    camera_x = jogador.centerx - LARGURA // 2
    camera_x = max(0, min(camera_x, LARGURA_NIVEL - LARGURA))

    desenhar_fundo(camera_x)

    for plataforma in plataformas:
        p = plataforma.move(-camera_x, 0)
        pygame.draw.rect(tela, MARROM, p)
        pygame.draw.rect(tela, VERDE, (p.x, p.y, p.width, 8))

    for coletavel in coletaveis:
        tela.blit(coletavel_img, coletavel.move(-camera_x, 0))

    tela.blit(objetivo_img, objetivo.move(-camera_x, 0))

    for inimigo in inimigos:
        tela.blit(inimigo_img, inimigo["rect"].move(-camera_x, 0))

    for especial in especiais:
        tela.blit(especial_img, especial["rect"].move(-camera_x, 0))

    jogador_desenho = jogador_img
    if direcao_jogador == -1:
        jogador_desenho = pygame.transform.flip(jogador_img, True, False)

    tela.blit(jogador_desenho, jogador.move(-camera_x, 0))
    mostrar_vidas()
    mostrar_coletaveis()
    mostrar_cooldown_especial()

    if venceu:
        mostrar_texto("Você venceu!")
    elif vidas <= 0:
        mostrar_texto("Fim de jogo!")

    pygame.display.flip()
