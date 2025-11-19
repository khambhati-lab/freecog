"""mri_atlas.py
Dataclass Specification for Volumetric Atlas Data
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
from pathlib import Path
from typing import List, Literal

# Third-Party Packages #
import nibabel as nib
import numpy as np

# Local Packages #

# Definitions #
# Classes #
@dataclass
class MRIAtlas:
    mgz_path: Path

    def __post_init__(self):
        self.name = '.'.join(self.mgz_path.split('/')[-1].split('.')[:-1])

        self.mgz_dat = nib.freesurfer.load(self.mgz_path)
        data = self.mgz_dat.get_fdata()

        self.labels = np.unique(data)
        self.label2voxel = {}
        for lbl in self.labels:
            self.label2voxel[lbl] = np.vstack(np.nonzero(data == lbl)).T 
