'''Autogenerated by get_gl_extensions script, do not edit!'''
from OpenGL import platform as _p
from OpenGL.GL import glget
EXTENSION_NAME = 'GL_SGIX_texture_scale_bias'
_p.unpack_constants( """GL_POST_TEXTURE_FILTER_BIAS_SGIX 0x8179
GL_POST_TEXTURE_FILTER_SCALE_SGIX 0x817A
GL_POST_TEXTURE_FILTER_BIAS_RANGE_SGIX 0x817B
GL_POST_TEXTURE_FILTER_SCALE_RANGE_SGIX 0x817C""", globals())
glget.addGLGetConstant( GL_POST_TEXTURE_FILTER_BIAS_RANGE_SGIX, (1,) )
glget.addGLGetConstant( GL_POST_TEXTURE_FILTER_SCALE_RANGE_SGIX, (1,) )


def glInitTextureScaleBiasSGIX():
    '''Return boolean indicating whether this extension is available'''
    from OpenGL import extensions
    return extensions.hasGLExtension( EXTENSION_NAME )
