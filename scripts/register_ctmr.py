#!/usr/bin/env -S uv run
import os
import sys
from nipy.core.api import AffineTransform
import nipy.algorithms
import nipy.algorithms.resample
import nipy.algorithms.registration.histogram_registration

SIMILARITY="nmi"
SMOOTH=0.0
REG_TYPE="rigid"
INTERP="pv"
XTOL=0.0001
FTOL=0.0001

source_file = sys.argv[1]
target_file = sys.argv[2]
output_file = sys.argv[3]

print("Computing registration from %s to %s"%(source_file, target_file))
ctimg  = nipy.load_image(source_file)
mriimg = nipy.load_image(target_file)

ct_cmap = ctimg.coordmap  
mri_cmap = mriimg.coordmap

# Compute registration
ct_to_mri_reg = nipy.algorithms.registration.histogram_registration.HistogramRegistration(ctimg, mriimg, similarity=SIMILARITY, smooth=SMOOTH, interp=INTERP)
aff = ct_to_mri_reg.optimize(REG_TYPE).as_affine()   

ct_to_mri = AffineTransform(ct_cmap.function_range, mri_cmap.function_range, aff)  
reg_CT = nipy.algorithms.resample.resample(ctimg, mri_cmap, ct_to_mri.inverse(), mriimg.shape)    

print("Saving registered CT image as %s"%(output_file))
nipy.save_image(reg_CT, output_file)
