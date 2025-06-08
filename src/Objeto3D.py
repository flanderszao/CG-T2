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
        self.speed = []
        self.angle = []
        self.radius = []
        self.y_original = []  # armazena y original
        self.position = Ponto(0, 0, 0)
        self.rotation = (0, 0, 0, 0)
        self.center = Ponto(0, 0, 0)
        self.time = 1.0  # tempo: 1 → 0 (colapso), depois 0 → 1 (retorno)
        self.frame = 0
        self.retornando = False  # fase de retorno

    def LoadFile(self, file: str):
        with open(file, "r") as f:
            for line in f:
                values = line.split(' ')
                if values[0] == 'v':
                    ponto = Ponto(float(values[1]), float(values[2]), float(values[3]))
                    self.vertices.append(ponto)
                    self.y_original.append(ponto.y)  # salva o Y original
                    self.speed.append(random.uniform(0.2, 0.6))
                    self.angle.append(math.atan2(ponto.z, ponto.x))
                    self.radius.append(math.hypot(ponto.x, ponto.z))
                elif values[0] == 'f':
                    self.faces.append([int(f.split('/')[0]) - 1 for f in values[1:]])

        cx = sum(v.x for v in self.vertices) / len(self.vertices)
        cy = sum(v.y for v in self.vertices) / len(self.vertices)
        cz = sum(v.z for v in self.vertices) / len(self.vertices)
        self.center = Ponto(cx, cy, cz)

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
            
            #if v:
            #    self.angle[i] += self.speed[i] * (1 / 30)
            #else:
            #    self.angle[i] -= self.speed[i] * (1 / 30)

            # Interpolação suave do raio: 1 → 0.1 e volta
            base = 0.1
            t_factor = self.time if not self.retornando else (1 - self.time)
            r_factor = base + (1 - base) * t_factor
            r = self.radius[i] * r_factor

            # Espiral
            x = r * math.cos(self.angle[i])
            z = r * math.sin(self.angle[i])

            # Interpolação da altura real para afundar e voltar
            y_collapse = self.center.y - 1  # ponto mais baixo
            y = self.y_original[i] * self.time + y_collapse * (1 - self.time)

            self.vertices[i].x = self.center.x + x
            self.vertices[i].y = y
            self.vertices[i].z = self.center.z + z
    
    def ondaParticulas(self):
        amplitude=0.5
        comprimento=2.0
        velocidade=0.1
        for i, v in enumerate(self.vertices):
            # Onda baseada na posição X e no tempo (frame)
            fase = (v.x + v.z) / comprimento + self.frame * velocidade
            v.y = self.y_original[i] + amplitude * math.sin(fase)


    def ProximaPos(self, v):
        self.frame = self.frame+v
        print(self.frame)

        if (self.frame < 401):
            Objeto3D.cabecaParticulas(self)
        else:
            Objeto3D.ondaParticulas(self)

        # Animação cíclica
        if self.frame < 200:
            if self.time > 0:
                self.time -= 0.005
                if self.time <= 0:
                    self.time = 0
                    self.retornando = True
        else: 
            if self.frame < 400:
                if self.time < 1.0:
                    self.time += 0.005
                    if self.time >= 1.0:
                        self.time = 1.0
                        self.retornando = False
                        #self.frame = 0

    def teste(self, value):
        self.frame = value
