'''Autogenerated by get_gl_extensions script, do not edit!'''
from OpenGL import platform as _p
from OpenGL.GL import glget
EXTENSION_NAME = 'GL_SGIS_texture_edge_clamp'
_p.unpack_constants( """GL_CLAMP_TO_EDGE_SGIS 0x812F""", globals())


def glInitTextureEdgeClampSGIS():
    '''Return boolean indicating whether this extension is available'''
    from OpenGL import extensions
    return extensions.hasGLExtension( EXTENSION_NAME )
