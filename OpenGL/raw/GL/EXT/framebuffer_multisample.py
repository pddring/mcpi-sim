'''Autogenerated by get_gl_extensions script, do not edit!'''
from OpenGL import platform as _p, constants as _cs, arrays
from OpenGL.GL import glget
import ctypes
EXTENSION_NAME = 'GL_EXT_framebuffer_multisample'
def _f( function ):
    return _p.createFunction( function,_p.GL,'GL_EXT_framebuffer_multisample',False)
_p.unpack_constants( """GL_RENDERBUFFER_SAMPLES_EXT 0x8CAB
GL_FRAMEBUFFER_INCOMPLETE_MULTISAMPLE_EXT 0x8D56
GL_MAX_SAMPLES_EXT 0x8D57""", globals())
glget.addGLGetConstant( GL_MAX_SAMPLES_EXT, (1,) )
@_f
@_p.types(None,_cs.GLenum,_cs.GLsizei,_cs.GLenum,_cs.GLsizei,_cs.GLsizei)
def glRenderbufferStorageMultisampleEXT( target,samples,internalformat,width,height ):pass


def glInitFramebufferMultisampleEXT():
    '''Return boolean indicating whether this extension is available'''
    from OpenGL import extensions
    return extensions.hasGLExtension( EXTENSION_NAME )
