import pygame as pg
import sys
from random import randint

tamanho_da_janela = 900
tamanho_da_celula = tamanho_da_janela // 3
inf = float('inf')
vec2 = pg.math.Vector2
central_celula = vec2(tamanho_da_celula / 2)


class JogoDaVelha:
    def __init__(self, jogar):
        self.linha_do_vencedor = None
        self.jogo = jogar
        self.campo_imagem = self.pegar_imagem_em_escala(caminho='imagens/campo.png', resolucao=[tamanho_da_janela] * 2)
        self.X_imagem = self.pegar_imagem_em_escala(caminho='imagens/x.png', resolucao=[tamanho_da_celula] * 2)
        self.O_imagem = self.pegar_imagem_em_escala(caminho='imagens/o.png', resolucao=[tamanho_da_celula] * 2)

        self.jogo_array = [[inf, inf, inf],
                           [inf, inf, inf],
                           [inf, inf, inf]]
        self.jogador = randint(0, 1)

        self.linha_dos_indices_da_matriz = [[(0, 0), (0, 1), (0, 2)],
                                            [(1, 0), (1, 1), (1, 2)],
                                            [(2, 0), (2, 1), (2, 2)],
                                            [(0, 0), (1, 0), (2, 0)],
                                            [(0, 1), (1, 1), (2, 1)],
                                            [(0, 2), (1, 2), (2, 2)],
                                            [(0, 0), (1, 1), (2, 2)],
                                            [(0, 2), (1, 1), (2, 0)]]
        self.vencedor = None
        self.passos_jogados = 0
        self.font = pg.font.SysFont('Verdana', tamanho_da_janela // 4, True)

    def verifica_vencedor(self):
        for linha_dos_indices in self.linha_dos_indices_da_matriz:
            soma_linha = sum([self.jogo_array[i][j] for i, j in linha_dos_indices])
            if soma_linha in {0, 3}:
                self.vencedor = 'XO'[soma_linha == 0]
                self.linha_do_vencedor = [vec2(linha_dos_indices[0][::-1]) * tamanho_da_celula + central_celula,
                                          vec2(linha_dos_indices[2][::-1]) * tamanho_da_celula + central_celula]

    def iniciar_processos_do_jogo(self):
        celula_atual = vec2(pg.mouse.get_pos()) // tamanho_da_celula
        coluna, linha = map(int, celula_atual)
        click_esquerdo = pg.mouse.get_pressed()[0]

        if click_esquerdo and self.jogo_array[linha][coluna] == inf and not self.vencedor:
            self.jogo_array[linha][coluna] = self.jogador
            self.jogador = not self.jogador
            self.passos_jogados += 1
            self.verifica_vencedor()

    def desenhar_objetos(self):
        for y, linha in enumerate(self.jogo_array):
            for x, obj in enumerate(linha):
                if obj != inf:
                    self.jogo.tela.blit(self.X_imagem if obj else self.O_imagem, vec2(x, y) * tamanho_da_celula)

    def desenho_vencedor(self):
        if self.vencedor:
            pg.draw.line(self.jogo.tela, 'red', *self.linha_do_vencedor, tamanho_da_celula // 8)
            label = self.font.render(f'Jogador "{self.vencedor}" Ganhou!', True, 'white', 'black')
            label = pg.transform.scale(label, (int(label.get_width() * 0.2), int(label.get_height() * 0.2)))
            self.jogo.tela.blit(label, (tamanho_da_janela // 2 - label.get_width() // 2, tamanho_da_janela // 4))
        elif self.passos_jogados == 9:
            label = self.font.render('Deu Velha! Pressione espaço', True, 'white', 'black')
            label = pg.transform.scale(label, (int(label.get_width() * 0.2), int(label.get_height() * 0.2)))
            self.jogo.tela.blit(label, (tamanho_da_janela // 2 - label.get_width() // 2, tamanho_da_janela // 4))

    def desenhar(self):
        self.jogo.tela.blit(self.campo_imagem, (0, 0))
        self.desenhar_objetos()
        self.desenho_vencedor()

    @staticmethod
    def pegar_imagem_em_escala(caminho, resolucao):
        img = pg.image.load(caminho).convert_alpha()
        return pg.transform.smoothscale(img, resolucao)

    def imprimir_legenda(self):
        pg.display.set_caption(f'Jogador "{"OX"[self.jogador]}" sua vez')
        if self.vencedor:
            pg.display.set_caption(f'Jogador "{self.vencedor}" Ganhou! Pressione espaço para um novo jogo')
        elif self.passos_jogados == 9:
            pg.display.set_caption(f'Deu velha! Pressione espaço para um novo jogo')

    def iniciar(self):
        self.imprimir_legenda()
        self.desenhar()
        self.iniciar_processos_do_jogo()


class Jogo:
    def __init__(self):
        pg.init()
        self.tela = pg.display.set_mode([tamanho_da_janela] * 2)
        self.relogio = pg.time.Clock()
        self.jogo_da_velha = JogoDaVelha(self)

    def novo_jogo(self):
        self.jogo_da_velha = JogoDaVelha(self)

    def verifica_eventos(self):
        for evento in pg.event.get():
            if evento.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if evento.type == pg.KEYDOWN:
                if evento.key == pg.K_SPACE:
                    self.novo_jogo()

    def iniciar(self):
        while True:
            self.jogo_da_velha.iniciar()
            self.verifica_eventos()
            pg.display.update()
            self.relogio.tick(60)


if __name__ == '__main__':
    jogo = Jogo()
    jogo.iniciar()
