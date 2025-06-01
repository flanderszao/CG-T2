from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
from Ponto import *

import random
import math

class Objeto3D:
        
    def __init__(self):
        self.vertices = []
        self.faces    = []
        self.speed    = []
        self.angle    = []
        self.radius   = []
        self.position = Ponto(0,0,0)
        self.rotation = (0,0,0,0)
        self.center   = Ponto(0,0,0)
        self.offsets  = []

    def LoadFile(self, file: str):
        f = open(file, "r")

        # leitor de .obj baseado na descrição em https://en.wikipedia.org/wiki/Wavefront_.obj_file    
        for line in f:
            values = line.split(' ')
            if values[0] == 'v': 
                # item é um vértice
                ponto = Ponto(float(values[1]), float(values[2]), float(values[3]))
                self.vertices.append(ponto)
                self.speed.append((random.random() + 0.1))
                self.angle.append(math.atan2(ponto.z, ponto.x))
                self.radius.append(math.hypot(ponto.x, ponto.z))

            if values[0] == 'f':
                # item é uma face
                self.faces.append([])
                for fVertex in values[1:]:
                    fInfo = fVertex.split('/')
                    self.faces[-1].append(int(fInfo[0]) - 1)  # índice do vértice
        f.close()

        # Calcula o centro da cabeça
        cx = sum(v.x for v in self.vertices) / len(self.vertices)
        cy = sum(v.y for v in self.vertices) / len(self.vertices)
        cz = sum(v.z for v in self.vertices) / len(self.vertices)
        self.center = Ponto(cx, cy, cz)

        # Calcula vetores de deslocamento (offsets) para separar as partículas
        self.offsets = []
        for v in self.vertices:
            offset = v - self.center
            comprimento = math.sqrt(offset.x**2 + offset.y**2 + offset.z**2 + 0.0001)
            offset = offset * (1.5 / comprimento)  # normaliza e escala
            self.offsets.append(offset)

    def DesenhaVertices(self):
        glPushMatrix()
        glTranslatef(self.position.x, self.position.y, self.position.z)
        glRotatef(self.rotation[3], self.rotation[0], self.rotation[1], self.rotation[2])
        glColor3f(.0, .0, .0)
        glPointSize(8)

        for v in self.vertices:
            glPushMatrix()
            glTranslate(v.x, v.y, v.z)
            glutSolidSphere(.05, 20, 20)
            glPopMatrix()
        
        glPopMatrix()

    def DesenhaWireframe(self):
        glPushMatrix()
        glTranslatef(self.position.x, self.position.y, self.position.z)
        glRotatef(self.rotation[3], self.rotation[0], self.rotation[1], self.rotation[2])
        glColor3f(0, 0, 0)
        glLineWidth(2)        
        
        for f in self.faces:            
            glBegin(GL_LINE_LOOP)
            for iv in f:
                v = self.vertices[iv]
                glVertex(v.x, v.y, v.z)
            glEnd()
        
        glPopMatrix()

    def Desenha(self):
        glPushMatrix()
        glTranslatef(self.position.x, self.position.y, self.position.z)
        glRotatef(self.rotation[3], self.rotation[0], self.rotation[1], self.rotation[2])
        glColor3f(0.34, .34, .34)
        glLineWidth(2)        
        
        for f in self.faces:            
            glBegin(GL_TRIANGLE_FAN)
            for iv in f:
                v = self.vertices[iv]
                glVertex(v.x, v.y, v.z)
            glEnd()
        
        glPopMatrix()

    def ProximaPos(self, v):
        for i in range(len(self.vertices)):
            if v:
                self.angle[i] += self.speed[i] * (1/30)
            else:
                self.angle[i] -= self.speed[i] * (1/30)

            x = self.radius[i] * math.cos(self.angle[i])
            z = self.radius[i] * math.sin(self.angle[i])

            # Aplica separação
            self.vertices[i].x = self.center.x + x + self.offsets[i].x
            self.vertices[i].y = self.center.y + self.offsets[i].y
            self.vertices[i].z = self.center.z + z + self.offsets[i].z
