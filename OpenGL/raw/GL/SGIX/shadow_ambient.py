'''Autogenerated by get_gl_extensions script, do not edit!'''
from OpenGL import platform as _p
from OpenGL.GL import glget
EXTENSION_NAME = 'GL_SGIX_shadow_ambient'
_p.unpack_constants( """GL_SHADOW_AMBIENT_SGIX 0x80BF""", globals())


def glInitShadowAmbientSGIX():
    '''Return boolean indicating whether this extension is available'''
    from OpenGL import extensions
    return extensions.hasGLExtension( EXTENSION_NAME )
