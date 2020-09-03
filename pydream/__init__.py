#!/usr/bin/env python
# -*- coding: utf-8 -*-

#from __future__ import (division, print_function, absolute_import,
#                        unicode_literals)
#from .sampler import *
#from .mh import *
#from .ensemble import *
#from .ptsampler import *
#from . import utils

__modules__ = ['pydream']
from .pydream import pydream,pydreamgrid

__version__ = "0.1.0"

# How to Compile
# /Users/juan/miniconda3/bin/python setup.py build_ext --inplace
#

# x = arange(100,1e5,2)

# How to compile the fortran code
# gfortran -O3 -fno-automatic -ffixed-line-length-132 -mcmodel=large -o dream.exe dream.for misc.for -L/data/jvhs1/star-2018A/lib `pgplot_link`
