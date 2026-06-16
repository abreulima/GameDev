import pygame
import sys
import os

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
arma_img = pygame.image.load("artes/arma.png").convert_alpha()
relvatopo_img = pygame.image.load("artes/relvatopo.png").convert_alpha()

if os.path.exists("artes/relvameio.png"):
    relvameio_img = pygame.image.load("artes/relvameio.png").convert_alpha()
else:
    relvameio_img = pygame.Surface(relvatopo_img.get_size(), pygame.SRCALPHA)
    relvameio_img.fill(MARROM)

jogador_img = pygame.transform.scale(jogador_img, (50, 60))
inimigo_img = pygame.transform.scale(inimigo_img, (50, 50))
fundo_img = pygame.transform.scale(fundo_img, (LARGURA, ALTURA))
vida_img = pygame.transform.scale(vida_img, (32, 32))
coletavel_img = pygame.transform.scale(coletavel_img, (32, 32))
objetivo_img = pygame.transform.scale(objetivo_img, (64, 64))
especial_img = pygame.transform.scale(especial_img, (24, 24))
arma_img = pygame.transform.scale(arma_img, (42, 42))
inimigo_img_esquerda = pygame.transform.flip(inimigo_img, True, False)

jogador = pygame.Rect(100, 300, 50, 60)
vel_y = 0
velocidade = 5
gravidade = 0.8
forca_pulo = -15
forca_salto_duplo = -11
no_chao = False
saltos_restantes = 2
vidas = 2
jogo_terminou = False
direcao_jogador = 1
especiais = []
cooldown_especial = 6500
ultimo_arremesso = -cooldown_especial
atacando = False
inicio_ataque = 0
duracao_ataque = 180
cooldown_ataque = 500
ultimo_ataque = -cooldown_ataque
invulneravel_ate = 0
duracao_invulnerabilidade = 900

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
    {"rect": pygame.Rect(520, 250, 50, 50), "vel": 3, "min": 500, "max": 680},
    {"rect": pygame.Rect(920, 390, 50, 50), "vel": 3, "min": 760, "max": 1260},
    {"rect": pygame.Rect(1500, 390, 50, 50), "vel": 4, "min": 1350, "max": 1850},
    {"rect": pygame.Rect(2100, 390, 50, 50), "vel": 3, "min": 1950, "max": 2600},
    {"rect": pygame.Rect(250, 300, 50, 50), "vel": 2, "min": 220, "max": 400},
    {"rect": pygame.Rect(1130, 260, 50, 50), "vel": 3, "min": 1120, "max": 1290},
    {"rect": pygame.Rect(1740, 240, 50, 50), "vel": 3, "min": 1730, "max": 1890},
    {"rect": pygame.Rect(2330, 210, 50, 50), "vel": 2, "min": 2320, "max": 2490},
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

objetivo = pygame.Rect(2500, 376, 64, 64)

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

def desenhar_tiles(img, area):
    largura_tile, altura_tile = img.get_size()

    for y in range(area.top, area.bottom, altura_tile):
        for x in range(area.left, area.right, largura_tile):
            largura = min(largura_tile, area.right - x)
            altura = min(altura_tile, area.bottom - y)
            tela.blit(img, (x, y), pygame.Rect(0, 0, largura, altura))

def desenhar_plataforma(plataforma, camera_x):
    p = plataforma.move(-camera_x, 0)
    altura_topo = min(relvatopo_img.get_height(), p.height)
    topo = pygame.Rect(p.x, p.y, p.width, altura_topo)
    meio = pygame.Rect(p.x, p.y + altura_topo, p.width, p.height - altura_topo)

    desenhar_tiles(relvatopo_img, topo)
    if meio.height > 0:
        desenhar_tiles(relvameio_img, meio)

def arremessar_especial():
    global ultimo_arremesso

    agora = pygame.time.get_ticks()
    if agora - ultimo_arremesso < cooldown_especial:
        return

    rect = especial_img.get_rect(center=jogador.center)
    especiais.append({"rect": rect, "vel": direcao_jogador * 10})
    ultimo_arremesso = agora

def obter_rect_ataque():
    largura_ataque = 52
    altura_ataque = 38
    y = jogador.centery - altura_ataque // 2

    if direcao_jogador == 1:
        return pygame.Rect(jogador.right, y, largura_ataque, altura_ataque)

    return pygame.Rect(jogador.left - largura_ataque, y, largura_ataque, altura_ataque)

def atacar_com_espada():
    global atacando, inicio_ataque, ultimo_ataque

    agora = pygame.time.get_ticks()
    if agora - ultimo_ataque < cooldown_ataque:
        return

    atacando = True
    inicio_ataque = agora
    ultimo_ataque = agora
    rect_ataque = obter_rect_ataque()

    for inimigo in inimigos[:]:
        if rect_ataque.colliderect(inimigo["rect"]):
            inimigos.remove(inimigo)

def atualizar_ataque():
    global atacando

    if atacando and pygame.time.get_ticks() - inicio_ataque >= duracao_ataque:
        atacando = False

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

def perder_vida(reiniciar=False):
    global vidas, invulneravel_ate, vel_y

    agora = pygame.time.get_ticks()
    if agora < invulneravel_ate and not reiniciar:
        return

    vidas -= 1
    invulneravel_ate = agora + duracao_invulnerabilidade

    if reiniciar:
        reiniciar_jogador()
    else:
        jogador.x -= direcao_jogador * 45
        jogador.left = max(0, jogador.left)
        jogador.right = min(LARGURA_NIVEL, jogador.right)
        vel_y = -7

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
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1 and not jogo_terminou:
            atacar_com_espada()

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
        atualizar_ataque()

        for coletavel in coletaveis[:]:
            if jogador.colliderect(coletavel):
                coletaveis.remove(coletavel)

        if jogador.top > ALTURA:
            perder_vida(reiniciar=True)

        venceu = not coletaveis and jogador.colliderect(objetivo)
        jogo_terminou = venceu or vidas <= 0

    camera_x = jogador.centerx - LARGURA // 2
    camera_x = max(0, min(camera_x, LARGURA_NIVEL - LARGURA))

    desenhar_fundo(camera_x)

    for plataforma in plataformas:
        desenhar_plataforma(plataforma, camera_x)

    for coletavel in coletaveis:
        tela.blit(coletavel_img, coletavel.move(-camera_x, 0))

    tela.blit(objetivo_img, objetivo.move(-camera_x, 0))

    for inimigo in inimigos:
        inimigo_desenho = inimigo_img
        if inimigo["vel"] < 0:
            inimigo_desenho = inimigo_img_esquerda
        tela.blit(inimigo_desenho, inimigo["rect"].move(-camera_x, 0))

    for especial in especiais:
        tela.blit(especial_img, especial["rect"].move(-camera_x, 0))

    if atacando:
        rect_ataque = obter_rect_ataque().move(-camera_x, 0)
        espada_desenho = arma_img
        if direcao_jogador == -1:
            espada_desenho = pygame.transform.flip(arma_img, True, False)
        tela.blit(espada_desenho, espada_desenho.get_rect(center=rect_ataque.center))

    jogador_desenho = jogador_img
    if direcao_jogador == -1:
        jogador_desenho = pygame.transform.flip(jogador_img, True, False)

    agora = pygame.time.get_ticks()
    jogador_visivel = agora >= invulneravel_ate or agora // 100 % 2 == 0
    if jogador_visivel:
        tela.blit(jogador_desenho, jogador.move(-camera_x, 0))
    mostrar_vidas()
    mostrar_coletaveis()
    mostrar_cooldown_especial()

    if venceu:
        mostrar_texto("Você venceu!")
    elif vidas <= 0:
        mostrar_texto("Fim de jogo!")

    pygame.display.flip()
