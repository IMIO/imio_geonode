from ctypes import byref, POINTER, c_char_p, c_double, c_int, c_void_p

from django.contrib.gis.gdal.envelope import OGREnvelope
from django.contrib.gis.gdal.libgdal import lgdal
from django.contrib.gis.gdal.prototypes.errcheck import check_envelope
from django.contrib.gis.gdal.prototypes.generation import (
    const_string_output, double_output, geom_output, int_output, srs_output,
    string_output, void_output,
)

def to_gml3(OGRGeom):
    gml3_capi = string_output(lgdal.OGR_G_ExportToGMLEx, [c_void_p, POINTER(c_char_p)], str_result=True, decoding='ascii')
    return gml3_capi(OGRGeom.ptr,byref(c_char_p('FORMAT=GML3'.encode())))
