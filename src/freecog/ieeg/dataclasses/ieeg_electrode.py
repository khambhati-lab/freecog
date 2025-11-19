"""ieeg_electrode.py
Dataclass Specification for Electrode-level information
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
from typing import Tuple

# Third-Party Packages #
# Local Packages #

# Definitions #
# Classes #
@dataclass                                                                                                                                                 
class IntracranialEEGElectrode:                                                                                                                            
    name: str   # e.g. RightOrbitofrontalCortex                                                                                                            
    abbr: str   # e.g. ROFC                                                                                                                                
    type: str   # e.g. grid, strip, depth                                                                                                                  
    geometry: Tuple[int, int]  # row, col, Assumes Euclidean

    @property
    def size(self):
        return self.geometry[0]*self.geometry[1]

    def n_digits(self):                                                                                                                                    
        return len(str(self.size))
