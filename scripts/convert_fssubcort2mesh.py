#!/usr/bin/env -S uv run
import os
import sys
import numpy as np
import nibabel as nib
import scipy
from scipy.io import savemat


ascii2nuc_list = {
        'aseg_058.asc': 'rAcumb',
        'aseg_054.asc': 'rAmgd',
        'aseg_050.asc': 'rCaud',
        'aseg_052.asc': 'rGP',
        'aseg_053.asc': 'rHipp',
        'aseg_051.asc': 'rPut',
        'aseg_049.asc': 'rThal',
        'aseg_043.asc': 'rLatVent',
        'aseg_044.asc': 'rInfLatVent',
        'aseg_060.asc': 'rVentDienceph',
        'aseg_004.asc': 'lLatVent',
        'aseg_005.asc': 'lInfLatVent',
        'aseg_010.asc': 'lThal',
        'aseg_011.asc': 'lCaud',
        'aseg_012.asc': 'lPut',
        'aseg_013.asc': 'lGP',
        'aseg_017.asc': 'lHipp',
        'aseg_018.asc': 'lAmgd',
        'aseg_026.asc': 'lAcumb',
        'aseg_028.asc': 'lVentDienceph',
        'aseg_014.asc': 'lthirdVent',
        'aseg_015.asc': 'lFourthVent',
        'aseg_016.asc': 'lBrainstem'
    }

dir_ascii = sys.argv[1]
dir_subcort = sys.argv[2]


for key, val in ascii2nuc_list.items():
    with open(os.path.join(dir_ascii, key), 'r') as fv:
        subcort_mat = fv.readlines()
        subcort_mat.pop(0)
        subcort_mat = [item.strip("\n") for item in subcort_mat]

        subcort_inds = subcort_mat.pop(0)
        subcort_inds = subcort_inds.split(' ')
        subcort_inds = [int(i) for i in subcort_inds]

        subcort_vert = [item.strip(' 0')
                for item in subcort_mat[:subcort_inds[0]]]
        subcort_vert = [item.split('  ')
                for item in subcort_vert]
        subcort_vert = np.array(np.vstack((subcort_vert)), dtype=float)

        subcort_tri = [item[:-2] for item in subcort_mat[subcort_inds[0] + 1:]]
        subcort_tri = [item.split(' ')
                for item in subcort_tri]
        subcort_tri = np.array(np.vstack((subcort_tri)), dtype=int)

        savemat(os.path.join(dir_subcort, f"{val}_subcort_trivert.mat"),
                {'tri': subcort_tri, 'vert': subcort_vert})        

        savemat(os.path.join(dir_subcort, f"{val}_subcort_inds.mat"),
                {'inds': np.array(subcort_inds)})

        savemat(os.path.join(dir_subcort, f"{val}_subcort.mat"),
                {'cortex': {'tri': subcort_tri+1, 'vert': subcort_vert}})
