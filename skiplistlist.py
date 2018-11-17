"""A skiplist implementation of the List interface

W. Pugh. Skip Lists: A probabilistic alternative to balanced trees. 
  In Communications of the ACM, 33(6), pp. 668-676, June 1990.

W. Pugh. A skip list cookbook. CS-TR-2286.1, University of Maryland, 
  College Park, 1990.
"""
import random
import numpy
from utils import new_array
from base import BaseList
import pprint

        
class SkiplistList(BaseList):
    class Node(object):
        """A node in a skip list"""
        def __init__(self, x, h):
            self.x = x
            self.next = new_array(h+1)
            self.length = numpy.ones(h+1, dtype=int)

        def height(self):
            return len(self.next) - 1

    def _new_node(self, x, h):
        return SkiplistList.Node(x, h)
        
    def __init__(self, iterable=[]):
        self._initialize()
        self.add_all(iterable)
        
    def _initialize(self):
        self.h = 0
        self.n = 0
        self.sentinel = self._new_node(None, 32)
        self.stack = new_array(self.sentinel.height()+1)
    
    def find_pred(self, i):
        u = self.sentinel
        r = self.h
        j = -1
        while r >= 0:
            while u.next[r] is not None and j + u.length[r] < i:
                j += u.length[r]
                u = u.next[r]  # go right in list r
            r -= 1  # go down into list r-1
        return u

    def get(self, i):
        if i < 0 or i > self.n-1: raise IndexError()
        return self.find_pred(i).next[0].x

    def set(self, i, x):
        if i < 0 or i > self.n-1: raise IndexError()
        u = self.find_pred(i).next[0]
        y = u.x
        u.x = x
        return y
        
    def _add(self, i, w):
        u = self.sentinel
        k = w.height()
        r = self.h
        j = -1
        while r >= 0:
            while u.next[r] is not None and j+u.length[r] < i:
                j += u.length[r]
                u = u.next[r]
            u.length[r] += 1
            if r <= k:
                w.next[r] = u.next[r]
                u.next[r] = w
                w.length[r] = u.length[r] - (i-j)
                u.length[r] = i - j
            r -= 1
        self.n += 1
        return u
        
    def add(self, i, x):
        if i < 0 or i > self.n: raise IndexError()
        w = self._new_node(x, self.pick_height())
        if w.height() > self.h:
            self.h = w.height()
        self._add(i, w)
        
    def remove(self, i):
        if i < 0 or i > self.n-1: raise IndexError()
        u = self.sentinel
        r = self.h
        j = -1
        while r >= 0:
            while u.next[r] is not None and j + u.length[r] < i:
                j += u.length[r]
                u = u.next[r]
            u.length[r] -= 1
            if j + u.length[r] + 1 == i and u.next[r] is not None:
                x = u.next[r].x
                u.length[r] += u.next[r].length[r]
                u.next[r] = u.next[r].next[r]
                if u == self.sentinel and u.next[r] is None:
                    self.h -= 1
            r -= 1
        self.n -= 1
        return x    

    def __iter__(self):
        u = self.sentinel.next[0]
        while u is not None:
            yield u.x
            u = u.next[0]

    def pick_height(self):
        z = random.getrandbits(32)
        k = 0
        while z & 1:
            k += 1
            z = z // 2
        return k


    def truncar2(self, i):
        u = self.sentinel
        r = self.h
        j = -1
        h2 = None
        h1 = None
        y = self.find_pred(i)
        while r >= 0:
            while u.next[r] != None and j + u.length[r] < i:
                if h1 == None:
                    h1 = r
                j += u.length[r]
                u = u.next[r]
            if u.next[r] != None:
                if h2 == None:
                    h2 = r
                u.next[r] = None
            r = r - 1

        if h1 == None:
            h1 = 0

        w = self._new_node(None, h2)
        self._add(i, w)

        numero_de_elementos_2_parte = self.n - i

        self.h = h1
        self.n = i

        print('y.height()', y.height())
        print('h1', h1)
        print('h2', h2)
        return {
            'sentinel': w,
            'n': numero_de_elementos_2_parte,
            'h': h2,
        }


    def truncar(self, i):
        u = self.sentinel
        h = self.h
        j = -1
        h2 = None
        h1 = None
        while h > 0:
            while u.next[h] != None:
                j = j + u.length[h]
                if j < i and h1 == None:
                    h1 = u.next[h].height()
                if j > i:
                    if h2 == None:
                        h2 = u.next[h].height()
                    u.next[h] = None
                    print('breakou')
                    break
                u = u.next[h]
            print('entrou')
            h = h - 1

        if h1 == None:
            h1 = 0

        if h2 == None:
            h2 = 0

        print('h1: ', h1)
        print('h2: ', h2)
        return

    def truncate(self, i):
        if i <= 0 or i > self.n-2: raise IndexError()
        maior_altura_depois_do_corte = self._getMaiorAlturaDoNo(i, 'depois')
        maior_altura_antes_do_corte = self._getMaiorAlturaDoNo(i, 'antes')
        print('maior_altura_depois_do_corte', maior_altura_depois_do_corte)
        print('maior_altura_antes_do_corte', maior_altura_antes_do_corte)
        qtde_elementos_anterior = self.n
        self._reduzAlturaDoSentinela(maior_altura_antes_do_corte)
        novo_sentinela_depois = self._new_node(None, maior_altura_depois_do_corte)
        no_antes_corte = self.find_pred(i)
        novo_sentinela = self._add(i, novo_sentinela_depois)
        self._limpaOsNext(no_antes_corte)
        self.n = i

        return novo_sentinela

        # Ajeitar retorno para um classe
        return {
            'n': qtde_elementos_anterior - i, 
            'sentinel': novo_sentinela_depois, 
            'h': maior_altura_depois_do_corte
        }

    def _reduzAlturaDoSentinela(self, altura):
        while self.h > altura:
            self.h -= 1


    def _getMaiorAlturaDoNo(self, i, direcao):
        h = self.h
        no = None
        while no == None:
            indices_maior_h = self._getIndicesDosNosDeAltura(h)
            if direcao == 'antes':
                no = self._getIndiceAntesDoNo(i, indices_maior_h)
            else:
                no = self._getIndiceDepoisDoNo(i, indices_maior_h)
            h = h - 1
        return h+1


    def _getIndicesDosNosDeAltura(self, h):
        j = -1
        posicoes = []
        u = self.sentinel
        while u.next[h] != None:
            j += u.length[h]
            posicoes.append(j)
            u = u.next[h]
        return posicoes

    def _getIndiceAntesDoNo(self, i, indices):
        for x in indices:
            if x < i:
                return x 
        return None
    def _getIndiceDepoisDoNo(self, i, indices):
        for x in indices:
            if x >= i:
                return x
        return None

    def _limpaOsNext(self, no):
        for x in range(no.height()+1):
            print('entrou')
            no.next[x] = None