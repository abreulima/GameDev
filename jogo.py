import pygame
import sys
import os

pygame.init()

tela = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
LARGURA, ALTURA = tela.get_size()
ALTURA_BASE = 500
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
boss_img = pygame.image.load("artes/boss.png").convert_alpha()
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
boss_img = pygame.transform.scale(boss_img, (96, 96))
inimigo_img_esquerda = pygame.transform.flip(inimigo_img, True, False)
especial_img_esquerda = pygame.transform.flip(especial_img, True, False)
boss_img_esquerda = pygame.transform.flip(boss_img, True, False)


def ajustar_y(y):
    return y + ALTURA - ALTURA_BASE


def criar_rect(x, y, largura, altura):
    return pygame.Rect(x, ajustar_y(y), largura, altura)


def criar_inimigo(x, y, vel, minimo, maximo):
    return {"rect": criar_rect(x, y, 50, 50), "vel": vel, "min": minimo, "max": maximo}


niveis = [
    {
        "nome": "Nivel 1",
        "largura": 2600,
        "inicio": (100, 300),
        "plataformas": [
            (0, 440, 700, 60), (760, 440, 500, 60),
            (1350, 440, 500, 60), (1950, 440, 650, 60),
            (220, 350, 180, 25), (520, 300, 160, 25),
            (850, 360, 180, 25), (1120, 310, 170, 25),
            (1450, 350, 180, 25), (1730, 290, 160, 25),
            (2050, 340, 180, 25), (2320, 260, 170, 25),
        ],
        "inimigos": [
            (520, 250, 2, 500, 680), (920, 390, 2, 760, 1260),
            (1500, 390, 3, 1350, 1850), (2100, 390, 2, 1950, 2600),
            (1130, 260, 2, 1120, 1290), (2330, 210, 2, 2320, 2490),
        ],
        "coletaveis": [
            (290, 310), (585, 260), (925, 320), (1185, 270),
            (1515, 310), (1785, 250), (2115, 300), (2385, 220),
            (2200, 400), (2400, 400),
        ],
        "vida_extra": (1450, 310),
        "objetivo": (2500, 376),
    },
    {
        "nome": "Nivel 2",
        "largura": 3200,
        "inicio": (80, 300),
        "plataformas": [
            (0, 440, 520, 60), (620, 440, 420, 60),
            (1150, 440, 360, 60), (1640, 440, 430, 60),
            (2180, 440, 360, 60), (2650, 440, 550, 60),
            (210, 345, 150, 25), (500, 295, 130, 25),
            (820, 350, 145, 25), (1080, 285, 135, 25),
            (1400, 345, 145, 25), (1700, 290, 130, 25),
            (1990, 335, 145, 25), (2290, 280, 130, 25),
            (2580, 330, 150, 25), (2920, 250, 150, 25),
        ],
        "inimigos": [
            (300, 295, 3, 210, 360), (680, 390, 3, 620, 1040),
            (1180, 390, 4, 1150, 1510), (1430, 295, 3, 1400, 1545),
            (1730, 240, 3, 1700, 1830), (2240, 390, 4, 2180, 2540),
            (2600, 280, 3, 2580, 2730), (2930, 200, 3, 2920, 3070),
        ],
        "coletaveis": [
            (265, 305), (550, 255), (875, 310), (1130, 245),
            (1455, 305), (1745, 250), (2045, 295), (2340, 240),
            (2635, 290), (2985, 210),
        ],
        "vida_extra": (1455, 305),
        "objetivo": (3060, 376),
    },
    {
        "nome": "Nivel 3",
        "largura": 3800,
        "inicio": (70, 300),
        "plataformas": [
            (0, 440, 460, 60), (570, 440, 330, 60),
            (1030, 440, 310, 60), (1500, 440, 300, 60),
            (1960, 440, 320, 60), (2420, 440, 290, 60),
            (2860, 440, 300, 60), (3300, 440, 500, 60),
            (180, 340, 125, 25), (430, 285, 115, 25),
            (720, 330, 120, 25), (980, 260, 110, 25),
            (1250, 335, 120, 25), (1490, 270, 110, 25),
            (1760, 320, 120, 25), (2050, 250, 110, 25),
            (2320, 335, 120, 25), (2580, 275, 110, 25),
            (2860, 320, 120, 25), (3160, 250, 110, 25),
            (3440, 315, 120, 25),
        ],
        "inimigos": [
            (210, 290, 3, 180, 305), (600, 390, 4, 570, 900),
            (1040, 390, 5, 1030, 1340), (1260, 285, 3, 1250, 1370),
            (1510, 220, 4, 1490, 1600), (1780, 270, 4, 1760, 1880),
            (1990, 390, 5, 1960, 2280), (2060, 200, 4, 2050, 2160),
            (2450, 390, 5, 2420, 2710), (2590, 225, 4, 2580, 2690),
            (2890, 270, 4, 2860, 2980), (3170, 200, 4, 3160, 3270),
            (3450, 265, 4, 3440, 3560), (3360, 390, 5, 3300, 3800),
        ],
        "coletaveis": [
            (225, 300), (465, 245), (760, 290), (1015, 220),
            (1285, 295), (1525, 230), (1795, 280), (2085, 210),
            (2355, 295), (2615, 235),
        ],
        "vida_extra": (1795, 280),
        "objetivo": (3680, 376),
    },
    {
        "nome": "Boss",
        "largura": 1800,
        "inicio": (120, 300),
        "boss": True,
        "plataformas": [
            (0, 440, 1800, 60),
            (260, 335, 180, 25), (660, 285, 170, 25),
            (1050, 335, 180, 25), (1360, 260, 170, 25),
        ],
        "inimigos": [],
        "coletaveis": [],
        "vida_extra": None,
        "objetivo": None,
        "boss_pos": (1380, 344),
        "boss_vida": 18,
    },
]

nivel_atual = 0
LARGURA_NIVEL = niveis[0]["largura"]
plataformas = []
inimigos = []
coletaveis = []
vidas_extras = []
total_coletaveis = 0
objetivo = pygame.Rect(0, 0, 64, 64)
boss = None
boss_vida = 0
boss_vida_max = 0
boss_direcao = -1
boss_projeteis = []
ultimo_tiro_boss = 0
cooldown_tiro_boss = 900

jogador = pygame.Rect(100, ajustar_y(300), 50, 60)
vel_y = 0
velocidade = 5
gravidade = 0.8
forca_pulo = -15
forca_salto_duplo = -11
no_chao = False
saltos_restantes = 2
vidas = 2
jogo_terminou = False
venceu_jogo = False
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

fonte = pygame.font.SysFont(None, 40)


def reiniciar_jogo():
    global vidas, jogo_terminou, venceu_jogo, ultimo_arremesso, ultimo_ataque

    vidas = 2
    jogo_terminou = False
    venceu_jogo = False
    ultimo_arremesso = -cooldown_especial
    ultimo_ataque = -cooldown_ataque
    carregar_nivel(0)


def carregar_nivel(indice):
    global nivel_atual, LARGURA_NIVEL, plataformas, inimigos, coletaveis, vidas_extras
    global total_coletaveis, objetivo, especiais, atacando, invulneravel_ate
    global boss, boss_vida, boss_vida_max, boss_direcao, boss_projeteis, ultimo_tiro_boss

    nivel_atual = indice
    dados = niveis[nivel_atual]
    LARGURA_NIVEL = dados["largura"]
    plataformas = [criar_rect(*p) for p in dados["plataformas"]]
    inimigos = [criar_inimigo(*i) for i in dados["inimigos"]]
    coletaveis = [criar_rect(x, y, 32, 32) for x, y in dados["coletaveis"]]
    if dados["vida_extra"] is None:
        vidas_extras = []
    else:
        vidas_extras = [criar_rect(dados["vida_extra"][0], dados["vida_extra"][1], 32, 32)]
    total_coletaveis = len(coletaveis)
    if dados["objetivo"] is None:
        objetivo = None
    else:
        objetivo = criar_rect(dados["objetivo"][0], dados["objetivo"][1], 64, 64)
    if dados.get("boss"):
        boss = criar_rect(dados["boss_pos"][0], dados["boss_pos"][1], 96, 96)
        boss_vida_max = dados["boss_vida"]
        boss_vida = boss_vida_max
        boss_direcao = -1
        boss_projeteis = []
        ultimo_tiro_boss = pygame.time.get_ticks()
    else:
        boss = None
        boss_vida_max = 0
        boss_vida = 0
        boss_projeteis = []
    especiais.clear()
    atacando = False
    invulneravel_ate = 0
    reiniciar_jogador()


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
    if total_coletaveis == 0:
        return

    texto = f"{total_coletaveis - len(coletaveis)}/{total_coletaveis}"
    img = fonte.render(texto, True, PRETO)
    tela.blit(coletavel_img, (20, 60))
    tela.blit(img, (60, 60))


def mostrar_nivel():
    if niveis[nivel_atual].get("boss"):
        texto = "Boss"
    else:
        texto = f"Nivel {nivel_atual + 1}/{len(niveis) - 1}"
    img = fonte.render(texto, True, PRETO)
    tela.blit(img, (20, 138))


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


def causar_dano_boss(dano):
    global boss_vida, jogo_terminou, venceu_jogo

    if boss is None or boss_vida <= 0:
        return

    boss_vida = max(0, boss_vida - dano)
    if boss_vida == 0:
        venceu_jogo = True
        jogo_terminou = True


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

    if boss is not None and rect_ataque.colliderect(boss):
        causar_dano_boss(2)


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

        if especial in especiais and boss is not None and especial["rect"].colliderect(boss):
            especiais.remove(especial)
            causar_dano_boss(1)


def atualizar_boss():
    global boss_direcao, ultimo_tiro_boss

    if boss is None or boss_vida <= 0:
        return

    boss.x += boss_direcao * 3
    if boss.left < 1180 or boss.right > LARGURA_NIVEL - 90:
        boss_direcao *= -1

    if jogador.colliderect(boss):
        perder_vida()

    agora = pygame.time.get_ticks()
    if agora - ultimo_tiro_boss >= cooldown_tiro_boss:
        direcao = -1 if jogador.centerx < boss.centerx else 1
        tiro = pygame.Rect(boss.centerx, boss.centery - 6, 28, 12)
        boss_projeteis.append({"rect": tiro, "vel": direcao * 7})
        ultimo_tiro_boss = agora

    for projetil in boss_projeteis[:]:
        projetil["rect"].x += projetil["vel"]

        if projetil["rect"].right < 0 or projetil["rect"].left > LARGURA_NIVEL:
            boss_projeteis.remove(projetil)
            continue

        if projetil["rect"].colliderect(jogador):
            boss_projeteis.remove(projetil)
            perder_vida()


def mostrar_barra_boss():
    if boss is None or boss_vida <= 0:
        return

    largura_barra = min(520, LARGURA - 80)
    altura_barra = 22
    x = LARGURA // 2 - largura_barra // 2
    y = 28
    progresso = boss_vida / boss_vida_max

    pygame.draw.rect(tela, PRETO, (x, y, largura_barra, altura_barra), 2)
    pygame.draw.rect(tela, (180, 40, 55), (x + 3, y + 3, int((largura_barra - 6) * progresso), altura_barra - 6))


def reiniciar_jogador():
    global vel_y, no_chao, saltos_restantes

    inicio_x, inicio_y = niveis[nivel_atual]["inicio"]
    jogador.x, jogador.y = inicio_x, ajustar_y(inicio_y)
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


def avancar_nivel():
    global jogo_terminou, venceu_jogo

    if nivel_atual + 1 >= len(niveis):
        venceu_jogo = True
        jogo_terminou = True
        return

    carregar_nivel(nivel_atual + 1)


carregar_nivel(0)

while True:
    relogio.tick(60)

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()
        if evento.type == pygame.KEYDOWN and evento.key == pygame.K_r and jogo_terminou:
            reiniciar_jogo()
        if evento.type == pygame.KEYDOWN and evento.key in (pygame.K_SPACE, pygame.K_UP) and not jogo_terminou:
            if saltos_restantes > 0:
                vel_y = forca_pulo if saltos_restantes == 2 else forca_salto_duplo
                no_chao = False
                saltos_restantes -= 1
        if evento.type == pygame.KEYDOWN and evento.key == pygame.K_f and not jogo_terminou:
            arremessar_especial()
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1 and not jogo_terminou:
            atacar_com_espada()
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 3 and not jogo_terminou:
            arremessar_especial()

    venceu_nivel = objetivo is not None and not coletaveis and jogador.colliderect(objetivo)

    if venceu_nivel and not jogo_terminou:
        avancar_nivel()

    if vidas <= 0:
        jogo_terminou = True

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
        atualizar_boss()

        for coletavel in coletaveis[:]:
            if jogador.colliderect(coletavel):
                coletaveis.remove(coletavel)

        for vida_extra in vidas_extras[:]:
            if jogador.colliderect(vida_extra):
                vidas += 1
                vidas_extras.remove(vida_extra)

        if jogador.top > ALTURA:
            perder_vida(reiniciar=True)

    camera_x = jogador.centerx - LARGURA // 2
    camera_x = max(0, min(camera_x, LARGURA_NIVEL - LARGURA))

    desenhar_fundo(camera_x)

    for plataforma in plataformas:
        desenhar_plataforma(plataforma, camera_x)

    for coletavel in coletaveis:
        tela.blit(coletavel_img, coletavel.move(-camera_x, 0))

    for vida_extra in vidas_extras:
        tela.blit(vida_img, vida_extra.move(-camera_x, 0))

    if objetivo is not None:
        tela.blit(objetivo_img, objetivo.move(-camera_x, 0))

    if boss is not None and boss_vida > 0:
        boss_desenho = boss_img
        if boss_direcao < 0:
            boss_desenho = boss_img_esquerda
        tela.blit(boss_desenho, boss.move(-camera_x, 0))

    for projetil in boss_projeteis:
        p = projetil["rect"].move(-camera_x, 0)
        pygame.draw.rect(tela, (180, 40, 55), p)
        pygame.draw.rect(tela, PRETO, p, 2)

    for inimigo in inimigos:
        inimigo_desenho = inimigo_img
        if inimigo["vel"] < 0:
            inimigo_desenho = inimigo_img_esquerda
        tela.blit(inimigo_desenho, inimigo["rect"].move(-camera_x, 0))

    for especial in especiais:
        especial_desenho = especial_img
        if especial["vel"] < 0:
            especial_desenho = especial_img_esquerda
        tela.blit(especial_desenho, especial["rect"].move(-camera_x, 0))

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
    mostrar_nivel()
    mostrar_barra_boss()

    if venceu_jogo:
        mostrar_texto("Voce venceu todos os niveis!")
    elif vidas <= 0:
        mostrar_texto("Fim de jogo! Pressione R para reiniciar")

    pygame.display.flip()
