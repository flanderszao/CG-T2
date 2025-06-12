from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
from Ponto import *

import random
import math

class Objeto3D:

    def __init__(self):
        self.vertices = []
        self.faces = []
        self.original_vertices = []  # ← Guardar cópia original completa
        self.speed = []
        self.angle = []
        self.radius = []
        self.y_original = []
        self.dx = []
        self.dy = []
        self.dz = []
        self.position = Ponto(0, 0, 0)
        self.rotation = (0, 0, 0, 0)
        self.center = Ponto(0, 0, 0)
        self.time = 1.0
        self.frame = 0
        self.retornando = False
        self.historico_vertices = [{} for _ in range(0)]

    def LoadFile(self, file: str):
        with open(file, "r") as f:
            for line in f:
                values = line.split(' ')
                if values[0] == 'v':
                    ponto = Ponto(float(values[1]), float(values[2]), float(values[3]))
                    self.vertices.append(ponto)
                    self.original_vertices.append(Ponto(ponto.x, ponto.y, ponto.z))  # ← Salva cópia
                    self.y_original.append(ponto.y)
                    self.speed.append(random.uniform(0.2, 0.6))
                    self.angle.append(math.atan2(ponto.z, ponto.x))
                    self.radius.append(math.hypot(ponto.x, ponto.z))
                elif values[0] == 'f':
                    self.faces.append([int(f.split('/')[0]) - 1 for f in values[1:]])

        self.historico_vertices = [{} for _ in self.vertices]

        cx = sum(v.x for v in self.vertices) / len(self.vertices)
        cy = sum(v.y for v in self.vertices) / len(self.vertices)
        cz = sum(v.z for v in self.vertices) / len(self.vertices)
        self.center = Ponto(cx, cy, cz)

        for _ in self.vertices:
            self.dx.append(random.uniform(-10.0, 10.0))
            self.dy.append(random.uniform(-7.0, 7.0))
            self.dz.append(random.uniform(-10.0, 10.0))

    def DesenhaVertices(self):
        glPushMatrix()
        glTranslatef(self.position.x, self.position.y, self.position.z)
        glRotatef(self.rotation[3], self.rotation[0], self.rotation[1], self.rotation[2])
        glColor3f(0.0, 0.0, 0.0)
        glPointSize(8)

        for v in self.vertices:
            glPushMatrix()
            glTranslate(v.x, v.y, v.z)
            glutSolidSphere(0.05, 20, 20)
            glPopMatrix()

        glPopMatrix()

    def cabecaParticulas(self):
        for i in range(len(self.vertices)):
            self.angle[i] += self.speed[i] * (1 / 30)
            t_factor = 10 - self.time if self.retornando else self.time
            base = 0.5
            r_factor = base + (1 - base) * t_factor
            r = self.radius[i] * r_factor
            dir = 1 if i % 2 == 0 else -1
            ang = self.angle[i]

            if self.retornando:
                spiral = (1 - self.time)
                intensidade = 600
                x_s = r * math.cos(ang * dir + spiral * intensidade)
                z_s = r * math.sin(ang * dir + spiral * intensidade)

                orig = self.original_vertices[i]
                x = orig.x * self.time + (self.center.x + x_s) * (1 - self.time)
                y = orig.y * self.time + (self.center.y - 10 + self.dy[i]) * (1 - self.time)
                z = orig.z * self.time + (self.center.z + z_s) * (1 - self.time)
            else:
                dispersao = (1 - self.time)
                intensidade = 5
                x = r * math.cos(ang * dir) + self.dx[i] * dispersao * intensidade
                z = r * math.sin(ang * dir) + self.dz[i] * dispersao * intensidade
                gravidade = 50.0
                y = self.y_original[i] * self.time + (self.center.y - gravidade + self.dy[i] * intensidade) * dispersao
                x += self.center.x
                z += self.center.z

            self.vertices[i].x = x
            self.vertices[i].y = max(y, -1)
            self.vertices[i].z = z

    def ondaParticulas(self):
        amplitude = 0.5
        comprimento = 2.0
        velocidade = 0.1
        for i, v in enumerate(self.vertices):
            fase = (v.x + v.z) / comprimento + self.frame * velocidade
            v.y = self.y_original[i] + amplitude * math.sin(fase)

    def salvar_historico(self):
        for i, v in enumerate(self.vertices):
            if self.frame not in self.historico_vertices[i]:
                # Salva uma cópia do vértice atual para o frame
                self.historico_vertices[i][self.frame] = {
                    'vertice': Ponto(v.x, v.y, v.z),
                    'time': self.time
                }

<<<<<<< HEAD
        # Fase 1: Movimento de onda (balanço da cabeça)
        if self.frame < 200:
            self.ondaParticulas()

        # Fase 2: Dispersão e retorno das partículas
        else:
            self.cabecaParticulas()

        # Controle da variável `time` para controlar dispersão/retorno
        if 200 <= self.frame < 400:
            if self.time > 0:
                self.time -= 0.002
                if self.time <= 0:
                    self.time = 0
                    self.retornando = True

        elif 400 <= self.frame < 600:
            if self.time < 1.0:
                self.time += 0.005
                if self.time >= 1.0:
                    self.time = 1.0
                    self.retornando = False
=======
    def ProximaPos(self, v):
        if self.frame + v < 0:
            self.frame = 0
        elif self.frame > 700:
            self.frame = 700
        else:
            self.frame += v
            
        if v == -1 and self.frame > 0 and self.frame < 600:
            for i, historico in enumerate(self.historico_vertices):
                if self.frame in historico:
                    vertice_hist = historico[self.frame]
                    self.vertices[i].x = vertice_hist['vertice'].x
                    self.vertices[i].y = vertice_hist['vertice'].y
                    self.vertices[i].z = vertice_hist['vertice'].z
                    self.time = vertice_hist['time']
                    self.retornando = True if self.frame > 300 else False
            print(self.frame)
            return

        print(self.frame)

        if self.frame < 101:
            self.ondaParticulas()
        elif self.frame < 501:
            self.cabecaParticulas()
        #elif self.frame < 600: criar mais um movimento pro trabalho
        else:
            self.ondaParticulas()

        if self.frame > 100:
            if self.frame < 300:
                if self.time > 0:
                    self.time -= 0.05
                    if self.time < 0:
                        print(self.time)
                        self.time = 0
                        self.retornando = True
            elif self.frame < 500:
                if self.time < 1.0:
                    self.time += 0.005
                    if self.time > 1.0:
                        print(self.time)
                        self.time = 1.0
                        self.retornando = False
        
        self.salvar_historico()

    def teste(self, value):
        total_historico = sum(len(h) for h in self.historico_vertices)
        if total_historico > 600:
            self.frame = value
            for i, historico in enumerate(self.historico_vertices):
                if self.frame in historico:
                    vertice_hist = historico[self.frame]
                    self.vertices[i].x = vertice_hist['vertice'].x
                    self.vertices[i].y = vertice_hist['vertice'].y
                    self.vertices[i].z = vertice_hist['vertice'].z
                    self.time = vertice_hist['time']
            print(self.frame)
