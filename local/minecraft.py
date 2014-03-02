import pygame, threading
from OpenGL.GL import *
from OpenGL.GLU import *
from block import * 
import os
import numpy

class Minecraft:
    """
    Attempts to simulate the minecraft pi interface
    """
    
    class Camera:
        pos = numpy.array([0, 10, 80])
            
        def setPos(self, x,y,z):
            self.pos = numpy.array([x,y,z])
    
    camera = Camera()
    
    blocks = {}
    saved_blocks = {}
    grid = 10
    
    v_grid = numpy.array([])
    i_grid = numpy.array([])
    
    def setGrid(self, width):
        """
        Not part of the minecraft api: just for the simulator.
        Width is the number of pixels between each grid line
        """
        self.grid = width
        vertices = []
                
        for i in xrange(-100, 100, width):
            vertices.append([-100,0,i])
            vertices.append([100, 0, i])
            vertices.append([i, 0, -100])
            vertices.append([i, 0, 100])
            
        self.v_grid = numpy.array(vertices)
        self.i_grid = numpy.array(range(len(vertices)))
    
    
    
    def getBlock(self, *args):
        """
        Gets the block id at the position (x,y,z)
        """
        x,y,z = args
        try:
            id = self.blocks[(x,y,z)]
        except:
            id = 0
        return id
    
    def getBlockWithData(self, *args):
        raise Exception("Not implemented yet: use getBlock instead of getBlockWithData")
    
    def getBlocks(self, *args):
        raise Exception("Not implemented yet: use getBlock instead of getBlocks")
    
    def getHeight(self, *args):
        """
        Get the height of the world at (x,z) 
        Returns an integer
        """
        x,z = args
        max_y = 0
        for pos in self.blocks:
            px,py,pz = pos
            if py > max_y:
                max_y = py
        return max_y
    
    def getPlayerEntityIds(self):
        """
        Get the entity ids of the connected players
        Returns a list of integers
        
        At the moment this just returns [0] as there'll only ever
        be one player using this simulator at a time
        """  
        return [0]
    
    def saveCheckPoint(self):
        """
        Saves the current state of the world so you can load it again
        with restoreCheckPoint()
        """
        self.saved_blocks = {}
        for block in self.blocks:
            self.saved_blocks[block] = self.blocks[block]
        
    def restoreCheckPoint(self):
        """
        Restores the current state of the world after you've saved it
        by using saveCheckPoint()
        """
        self.blocks = {}
        for block in self.saved_blocks:
            self.blocks[block] = self.saved_blocks[block]
    
    def setBlocks(self, *args):
        """
        setBlocks(x1,y1,z1,x2,y2,z2,id)
        Sets a range of blocks from (x1,y1,z1) to (x2,y2,z2) all to id
        """
        x1,y1,z1,x2,y2,z2,id = args
        if x2 >= x1 and y2 >= y1 and z2 >= z1:
            x = x1
            while x <= x2:
                y = y1
                while y <= y2:
                    z = z1
                    while z <= z2:
                        self.setBlock(x,y,z, id)
                        z += 1
                    y += 1
                x += 1

    def setBlock(self, *args):
        """
        setBlock(x,y,z,id)
        Sets the block id at the position (x,y,z)
        """
        x,y,z,type = args
        self.blocks[(x,y,z)] = type
    
    def build_cube(self):
        """
        Internal function - used to create a 3d cube for each block
        """
        tex_coords = []
        v_cube = []
        tex_x = tex_y = 0
        x = y = z = 0
        def tc(stage):
            if stage == 0:
                tex_coords.append([tex_x, tex_y])
                glTexCoord2f(tex_x, tex_y)
            if stage == 1:
                tex_coords.append([tex_x + 0.0625, tex_y])
                glTexCoord2f(tex_x + 0.0625, tex_y)
            if stage == 3:
                tex_coords.append([tex_x, tex_y + 0.0625])
                glTexCoord2f(tex_x, tex_y + 0.0625)
            if stage == 2:
                tex_coords.append([tex_x + 0.0625, tex_y + 0.0625])
                glTexCoord2f(tex_x + 0.0625, tex_y + 0.0625)
        
        def addCubeVertex(x, y, z):
            v_cube.append([x,y,z])
        
        # bottom
        tc(3)
        addCubeVertex(x, y, z)
        tc(2)
        addCubeVertex(x+1, y, z)
        tc(0)
        addCubeVertex(x, y+1, z)
        tc(1)
        addCubeVertex(x+1, y+1, z)
        
        # back
        tc(3)
        addCubeVertex(x, y+1, z+1)
        tc(2)
        addCubeVertex(x+1, y+1, z+1)
        
        # top
        tc(0)
        addCubeVertex(x, y, z+1)
        tc(1)
        addCubeVertex(x+1, y, z+1)
        
        #front
        tc(3)
        addCubeVertex(x, y, z)
        tc(2)
        addCubeVertex(x+1, y, z)
        
        
        # left
        tc(3)
        addCubeVertex(x, y, z)
        tc(2)
        addCubeVertex(x, y+1, z)
        tc(1)
        addCubeVertex(x, y+1, z+1)
        tc(0)
        addCubeVertex(x, y, z+1)
        
        tc(3)
        addCubeVertex(x+1, y, z)
        tc(2)
        addCubeVertex(x+1, y+1, z)
        tc(1)
        addCubeVertex(x+1, y+1, z+1)
        tc(0)
        addCubeVertex(x+1, y, z+1)
        self.v_cube = numpy.array(v_cube)
        self.t_cube = numpy.array(tex_coords)
        
        
        self.quad_strip_indices = range(len(self.v_cube) - 8)
        self.quad_indices = range(len(self.v_cube) - 8, len(self.v_cube))
        
    def draw_cube(self, block, texture):
        """
        Internal function: Draws the 3d cube for a given block
        """
        (x,y,z),tex = block
        
        if tex == AIR:
            return    
        
        try:
            tex_x, tex_y = Block.lookup[tex]
        except:
            tex_x = tex_y = 0.0625
        
        
                
        try:
            vertices = self.v_cube
        except:
            self.build_cube()
            vertices = self.v_cube
         
        glTranslatef(x, y, z)
        tex_coords = self.t_cube + numpy.array([tex_x, tex_y])
        
        glEnableClientState(GL_VERTEX_ARRAY)
        glVertexPointerf( self.v_cube )
        glEnableClientState(GL_TEXTURE_COORD_ARRAY)
        glTexCoordPointerf(tex_coords)
        
        glDrawElementsui(GL_QUAD_STRIP, self.quad_strip_indices)
        glDrawElementsui(GL_QUADS, self.quad_indices)
        
        glTranslatef(-x, -y, -z)
        
    def pygameThread(self):
        """
        Main simulator thread
        """
          
        
        # set up the screen (800x600 resolution)
        screen_size = [800, 600]
        pygame.init()
        screen = pygame.display.set_mode(screen_size, 
                                         pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.OPENGL)
        
        glViewport( 0, 0, screen_size[ 0 ], screen_size[ 1 ] )
        glShadeModel(GL_SMOOTH)
        glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST )
        viewport = glGetIntegerv( GL_VIEWPORT )
        glMatrixMode( GL_PROJECTION )
        glLoadIdentity( )
        gluPerspective( 45.0, float( viewport[ 2 ] ) / float( viewport[ 3 ] ), 0.1, 300.0 )
        glMatrixMode( GL_MODELVIEW )
        glLoadIdentity( )

        icon = pygame.image.load("local/img/rpi.png")
        pygame.display.set_caption("Minecraft on Raspberry Pi API simulator (Press Tab to release mouse and Q to quit)")
        pygame.display.set_icon(icon)
        running = True
        clock = pygame.time.Clock()
        
        
        
        glEnable(GL_TEXTURE_2D)
        glEnable(GL_LINE_SMOOTH)
        glEnable(GL_BLEND)
        glBlendFunc (GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glHint (GL_LINE_SMOOTH_HINT, GL_NICEST)
        glEnable(GL_DEPTH_TEST)
        
        
        
        # load textures
        try:
            img_tex = pygame.image.load("local/img/terrain.png")
        except:
            img_tex = pygame.image.load("img/terrain.png")
        texture_data = pygame.image.tostring(img_tex, "RGBA", 1)
        texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, 256, 256, 0, GL_RGBA,
        GL_UNSIGNED_BYTE, texture_data)
                
        look_at = numpy.array([0, 0, 0])
        rotation = numpy.array([3.14, 0, 0])
        direction_fd = numpy.array([1,0,0])
        direction_rt = numpy.array([0,1,0])
        direction_up = numpy.array([0,0,1])
        mouse_capture = True
        
        MOUSE_SPEED = 0.005
        KEY_SPEED = 0.5
        
        def centre_mouse():
            pygame.mouse.set_pos(viewport[2] / 2, viewport[3] / 2)
            pygame.mouse.get_rel()
            
        def get_mouse_rel():
            pos = pygame.mouse.get_pos()
            return pos[0] - viewport[2] / 2, pos[1] - viewport[3] / 2
                
        def update_directions():
            direction_fd = [numpy.cos(rotation[1]) * numpy.sin(rotation[0]),
                                     numpy.sin(rotation[1]),
                                     numpy.cos(rotation[1]) * numpy.cos(rotation[0])]
            direction_rt = [numpy.sin(rotation[0] - 3.14/2.0),
                            0,
                            numpy.cos(rotation[0] - 3.14/2.0)]
            direction_up = numpy.cross(direction_rt, direction_fd)
            return direction_fd, direction_rt, direction_up
        
        centre_mouse()
        
        direction_fd, direction_rt, direction_up = update_directions()
        while running:
            for event in pygame.event.get():
                # close the window
                if event.type == pygame.QUIT:
                    running = False
                    
                # mouse events
                if event.type == pygame.MOUSEMOTION:
                    dx, dy = get_mouse_rel()
                    if mouse_capture:
                        key_mods = pygame.key.get_mods()
                        speed = MOUSE_SPEED
                        if key_mods & pygame.KMOD_CTRL:
                            speed = MOUSE_SPEED / 5
                        rotation[0] -= dx * speed
                        rotation[1] -= dy * speed
                        direction_fd, direction_rt, direction_up = update_directions()
                        centre_mouse()
                    
                # handle single key presses
                if event.type == pygame.KEYDOWN:
                    keys = pygame.key.get_pressed()
                    # press escape or q to quit
                    if keys[pygame.K_q] or keys[pygame.K_ESCAPE]:
                        running = False
                    
                    if keys[pygame.K_TAB]:
                        mouse_capture = not mouse_capture
                        centre_mouse()

                    if keys[pygame.K_p]:
                        print "Current position [x =" , int(self.camera.pos[0]), ",y =", int(self.camera.pos[1]), ",z =", int(self.camera.pos[2]), "]"
            
                    
            keys = pygame.key.get_pressed()
            key_mods = pygame.key.get_mods()
            
            speed = KEY_SPEED
            if key_mods & pygame.KMOD_CTRL:
                speed = KEY_SPEED / 5
            
            
            # handle repeat key presses
            if keys[pygame.K_w]:
                move_dir = numpy.array(direction_fd)
                move_dir[1] = 0
                self.camera.pos += numpy.multiply(move_dir, speed)
            
            if keys[pygame.K_s]:
                move_dir = numpy.array(direction_fd)
                move_dir[1] = 0
                self.camera.pos = self.camera.pos - numpy.multiply(move_dir, speed)
                
            if keys[pygame.K_a]:
                self.camera.pos = self.camera.pos - numpy.multiply(direction_rt, speed)
                    
            if keys[pygame.K_d]:
                self.camera.pos = self.camera.pos + numpy.multiply(direction_rt, speed)
                
            if keys[pygame.K_SPACE]:
                if key_mods & pygame.KMOD_SHIFT:
                    self.camera.pos = self.camera.pos - numpy.multiply((0,1,0), speed)
                else:
                    self.camera.pos = self.camera.pos + numpy.multiply((0,1,0), speed)

            
            #look_at = position + direction
            
            glClearColor( 1.0, 1.0, 1.0, 0.1 )
            glClear( GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT )
            glLoadIdentity( )
            look_at = self.camera.pos + direction_fd            
            gluLookAt( self.camera.pos[0], self.camera.pos[1], self.camera.pos[2], 
                       look_at[0], look_at[1], look_at[2], 
                       direction_up[0], direction_up[1], direction_up[2])
            
            
            # display blocks
            max = 0
            glColor3f(1.0, 1.0, 1.0)
            for pos in self.blocks:
                id = self.blocks[pos]
                max += 1
                self.draw_cube((pos, id), texture)
                
            # display grid
            if self.grid > 0:
                glEnableClientState(GL_VERTEX_ARRAY);
                glDisableClientState(GL_TEXTURE_COORD_ARRAY)
                glColor4f(0.8,0.8,0.8,0.8)
                glVertexPointerf(self.v_grid)
                indices = self.i_grid
                glDrawElementsui(GL_LINES, self.i_grid)
                
            pygame.display.flip()
            pygame.display.set_caption("Minecraft Pi Simulator (x: " + str(int(self.camera.pos[0]))+
                                       ", y: " + str(int(self.camera.pos[1]))+
                                       ", z: " + str(int(self.camera.pos[2]))+
                                       ") Press Tab to release mouse and Q to quit")
            clock.tick(40)
                    
    
    def __init__(self):
        print """Welcome to the Minecraft emulator by P. Dring
        This program is designed for use with the Raspberry Pi edition of
        Minecraft (available from: http://pi.minecraft.net/).
        This program allows you to test your code on your own computer before
        letting it loose on a live game of minecraft on a raspberry pi.
        This project is not affiliated with the Raspberry Pi Foundation
        or Mojang / Minecraft and is for educational use only.

    Controls:
        Use the mouse to look around
        Use WASD to move
        Press Space to move up
        Press Shift + Space to move down
        Press P to display the current position of the camera
        Press Q to Quit.
        """
        
        self.setGrid(10)
        pyg = threading.Thread(target=self.pygameThread)
        pyg.start()
        
    
    def postToChat(self, msg):
        """
        Display a message in the minecraft window
        """
        print os.environ["USERNAME"] + "@" + os.environ["COMPUTERNAME"] + ": " + msg
        
    @staticmethod
    def create(address = "localhost", port=4711):
        return Minecraft()
    
if __name__ == "__main__":
    mc = Minecraft.create()
    mc.postToChat("Hello, Minecraft!")
    mc.grid = 10
    mc.setBlock(0, 0, 0, LAVA)
