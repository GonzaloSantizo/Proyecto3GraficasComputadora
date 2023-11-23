from OpenGL.GL import *
import glm
from OpenGL.GL import *
from pygame.display import flip
from numpy import array, float32
import pygame

class Model(object):
    def __init__(self, data):
        self.vertBuffer = array(data, dtype = float32)
        self.VBO = glGenBuffers(1)
        self.VAO = glGenVertexArrays(1)

        self.position = glm.vec3(0,0,0)
        self.rotation = glm.vec3(0,0,0)
        self.scale = glm.vec3(1,1,1)

    def getModelMatrix(self):
        identity = glm.mat4(1)

        translateMat = glm.translate(identity, self.position)

        pitch = glm.rotate(identity, glm.radians(self.rotation.x), glm.vec3(1,0,0)) 
        yaw = glm.rotate(identity, glm.radians(self.rotation.y), glm.vec3(0,1,0)) 
        roll = glm.rotate(identity, glm.radians(self.rotation.z), glm.vec3(0,0,1)) 

        rotationMat = pitch * yaw * roll

        scaleMat = glm.scale(identity, self.scale)

        return  translateMat * rotationMat * scaleMat
    

    def loadTexture(self, textureName):
        self.textureSurface =  pygame.image.load(textureName)
        self.textureData = pygame.image.tostring(self.textureSurface, "RGB", True)
        self.textureBuffer = glGenTextures(1)
        


    def render(self):
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
        glBindVertexArray(self.VAO)
        glBufferData(GL_ARRAY_BUFFER,
                     self.vertBuffer.nbytes,
                     self.vertBuffer,
                     GL_STATIC_DRAW)
        glVertexAttribPointer(0,
                              3,
                              GL_FLOAT,
                              GL_FALSE,
                              4 * 8,
                              ctypes.c_void_p(0))
        
        glEnableVertexAttribArray(0)
   
        glVertexAttribPointer(1,
                              2,
                              GL_FLOAT,
                              GL_FALSE,
                              4 * 8,
                              ctypes.c_void_p(4*3))
        

        
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(2,
                              3,
                              GL_FLOAT,
                              GL_FALSE,
                              4 * 8,
                              ctypes.c_void_p(4*5))
        

        
        glEnableVertexAttribArray(2)
        
        
    
        glActiveTexture( GL_TEXTURE0 )
        glBindTexture(GL_TEXTURE_2D, self.textureBuffer)
        glTexImage2D(GL_TEXTURE_2D, 
        0,
        GL_RGB,
        self.textureSurface.get_width(),
        self.textureSurface.get_height(),
        0,
        GL_RGB,
        GL_UNSIGNED_BYTE,
        self.textureData)
 
        glGenerateTextureMipmap(self.textureBuffer)

        glDrawArrays(GL_TRIANGLES, 0, int(len(self.vertBuffer) / 8))