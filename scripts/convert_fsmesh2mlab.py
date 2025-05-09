#!/usr/bin/env -S uv run
import os
import sys
import nibabel as nib
from scipy.io import savemat

mesh_surf = sys.argv[1]
out_file = sys.argv[2]
out_file_struct = sys.argv[3]

vert, tri = nib.freesurfer.read_geometry(mesh_surf)
savemat(out_file, {"tri": tri, "vert": vert})

cortex = {"tri": tri+1, "vert": vert}
savemat(out_file_struct, {"cortex": cortex})
