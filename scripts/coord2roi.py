import nibabel as nib
import numpy as np


def coord2roi(vox_crs, fs_mgz_path):
    ###
    dat = nib.freesurfer.load(fs_mgz_path)
    mgz_dat = dat.get_fdata()

    dat_nnz = np.vstack(np.nonzero(mgz_dat)).T
    
    vox_dist = np.sqrt(((vox_crs - dat_nnz)**2).sum(axis=1))
    vox_lbl = np.array([mgz_dat[*crd] for crd in dat_nnz])

    labels = []
    labels_dist = []
    for lbl in np.unique(vox_lbl):
        labels.append(lbl)
        labels_dist.append(np.min(vox_dist[vox_lbl == lbl]))
    labels = np.array(labels)
    labels_dist = np.array(labels_dist)

    labels = labels[np.argsort(labels_dist)]
    labels_dist = labels_dist[np.argsort(labels_dist)]

    return labels, labels_dist
