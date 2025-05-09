import os

# Third-Party Packages
import numpy as np
import nibabel as nib

def get_freesurfer_geometry(subject_fs_dir, surf_name='pial'):
    geom = {'lh': {'vert': None, 'tri': None},
            'rh': {'vert': None, 'tri': None}}

    for h in geom:
        surf_dir = os.path.join(subject_fs_dir, 'surf')
        mesh_fn = os.path.join(surf_dir, h+'.'+surf_name)
        geom[h]['vert'], geom[h]['tri'] = nib.freesurfer.read_geometry(mesh_fn)
    return geom