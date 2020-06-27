import curses
from os import get_terminal_size as get_size
from operator import eq
from time import sleep

from .cores import cor


class Objeto:
    def __init__(self, tela, x: int, y: int, caracter: str, cor: str):
        self._tela = tela
        self.x = x
        self.y = y
        self._caracter = caracter
        self._cor = cor


class Tangivel(Objeto):
    def colisao(self, other):
        self_itens, other_itens = [self.x, self.y], [other.x, other.y]
        igual = all(map(eq, self_itens, other_itens))
        return igual

    def exibir(self):
        self._tela.addstr(self.x, self.y, self._caracter, cor(self._cor))

    def definir_posicao(self, x, y):
        self.x, self.y = x, y

    def __eq__(self, other):
        return [self.x, self.y] == [other.x, other.y]


# x -> linha, y -> coluna
class Ponto(Tangivel):
    def __init__(self, tela):
        colunas, linhas = get_size()
        x = linhas // 2
        y = 0
        super().__init__(
            tela, x, y, '⌬', 'yellow'
        )
        self._sinalx = '-'
        self._sinaly = '+'
        self._numeros = {'+': 1, '-': -1}

    def efeito(self):
        ...

    def andar(self):
        self.x += self._numeros[self._sinalx]
        self.y += self._numeros[self._sinaly]

    def definir_sinalx(self, sinal):
        self._sinalx = sinal

    def definir_sinaly(self, sinal):
        self._sinaly = sinal


class Linha:
    def __init__(self, tela, x=0):
        colunas, linhas = get_size()
        self.linhas = list(map(
            lambda y: Tangivel(tela, x, y, '▬', 'white'), range(colunas)
        ))
        self._sinais = {'+': '-', '-': '+'}

    def exibir(self):
        for item in self.linhas:
            item.exibir()

    def efeito(self, ponto):
        ponto._sinalx = self._sinais[ponto._sinalx]

    def colisao(self, other) -> bool:
        """Método que verifica se dois objetos colediram."""
        colisao = any(map(lambda x: x == other, self.linhas))
        return colisao


class Barra:
    def __init__(self, tela, y=0, tamanho=5):
        colunas, linhas = get_size()
        self._numero_linhas = linhas - 1
        self.colunas = list(map(
            lambda x: Tangivel(tela, x, y, "❚", 'red'), range(tamanho)
        ))
        self._sinais = {'+': '-', '-': '+'}

    def exibir(self):
        for item in self.colunas:
            item.exibir()

    def efeito(self, ponto):
        ponto._sinaly = self._sinais[ponto._sinaly]

    def colisao(self, other) -> bool:
        """Método que verifica se dois objetos colediram."""
        colisao = any(map(lambda x: x == other, self.colunas))
        return colisao

    def mover_cima(self):
        primeiro = self.colunas[0]
        if primeiro.x > 1:
            for item in self.colunas:
                item.x -= 1


    def mover_baixo(self):
        ultimo = self.colunas[-1]
        if ultimo.x < self._numero_linhas -1:
            for item in self.colunas:
                item.x += 1


class Jogo:
    def __init__(self, tela):
        colunas, linhas = get_size()
        self._tela = tela
        self._linha_superior = Linha(tela)
        self._linha_inferior = Linha(tela, linhas - 1)
        self._barra_esquerda = Barra(tela)
        self._barra_direita = Barra(tela, colunas - 1)
        self._ponto = Ponto(tela)
        self._tudo = [
            self._linha_superior, self._linha_inferior, self._barra_direita,
            self._barra_esquerda
        ]

    def rodar(self):
        while True:
            self._tela.erase()
            self._ponto.andar()
            self._mover_barras()
            self._colisoes()
            self._exibir()
            self._tela.refresh()
            sleep(0.05)

    def _mover_barras(self):
        tecla = self._tela.getch()
        self._mover_barra_direita(tecla)
        self._mover_barra_esquerda(tecla)

    def _mover_barra_esquerda(self, tecla):
        if tecla == 119:  # 'w'
            self._barra_esquerda.mover_cima()
        elif tecla == 115:  # 's'
            self._barra_esquerda.mover_baixo()

    def _mover_barra_direita(self, tecla):
        if tecla == 105:  # 'i'
            self._barra_direita.mover_cima()
        elif tecla == 107:  # 'k'
            self._barra_direita.mover_baixo()

    def _exibir(self):
        self._ponto.exibir()
        for item in self._tudo:
            item.exibir()

    def _colisoes(self):
        """Método verifica colisões, aplica os efeitos nos itens."""
        itens = filter(lambda x: x.colisao(self._ponto), self._tudo)
        for tangivel in itens:
            tangivel.efeito(self._ponto)


def configurar(tela):
    curses.curs_set(0)  # oculta o pipeline.
    tela.nodelay(True)  # não espera quando for obter a tecla pressionada.
    curses.noecho()
    curses.start_color()
    curses.use_default_colors()
    for x, y in enumerate(range(10), 1):
        curses.init_pair(x, y, -1)


def main():
    curses.initscr()
    colunas, linhas = get_size()
    tela = curses.newwin(linhas + 1, colunas + 1)  # correção de bug
    configurar(tela)
    try:
        jogo = Jogo(tela)
        jogo.rodar()
    except curses.error:
        pass
    finally:
        curses.endwin()



# ◯ ◉
