"""ieeg_montage.py
Dataclass Specification for Montage-level information
"""
# Package Header #
from ...header import *

# Header #
__author__ = __author__
__credits__ = __credits__
__maintainer__ = __maintainer__
__email__ = __email__


# Imports #
# Standard Libraries #
from dataclasses import dataclass
import os
from typing import List, Literal

# Third-Party Packages #
import nibabel as nib
import numpy as np

# Local Packages #
from .mri_atlas import MRIAtlas

# Definitions #
# Classes #
@dataclass
class MRIPointAnatomy:
    ras_vol: tuple[float, float, float] = None
    ras_surf: tuple[float, float, float] = None    #tkRAS, tkReg, typical coord space

    def __post_init__(self):
        self.parcellation = {}
    
    def vox_crs(self, affine) -> tuple[int, int, int]:
        tmp_coord = list(self.ras_surf) + [1] 
        return tuple(np.dot(
                np.linalg.inv(affine),
                tmp_coord)[:3].astype(int))

    def parcellate_point(self, mri_atlas: MRIAtlas):
        vox_crs = self.vox_crs(mri_atlas.mgz_dat.affine)

        self.parcellation[mri_atlas.name] = {}
        for lbl in mri_atlas.label2voxel:
            vox_dist = np.sqrt(
                    ((mri_atlas.mgz_dat.header.get_zooms() * 
                      (vox_crs - mri_atlas.label2voxel[lbl]))**2).sum(axis=1))
            self.parcellation[mri_atlas.name][lbl] = min(vox_dist)
