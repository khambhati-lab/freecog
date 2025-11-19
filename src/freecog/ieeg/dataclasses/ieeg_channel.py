"""ieeg_channel.py
Dataclass Specification for Channel-level information
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
from typing import List

# Third-Party Packages #
import numpy as np

# Local Packages #
from .ieeg_sensor import IntracranialEEGSensor

# Definitions #
# Classes #
@dataclass
class IntracranialEEGChannel:
    anode: List[IntracranialEEGSensor] = None
    cathode: List[IntracranialEEGSensor] = None

    def __post_init__(self):
        self.anode_idx = [el.idx for el in self.anode] if self.anode is not None else []
        self.cathode_idx = [el.idx for el in self.cathode] if self.cathode is not None else []

    @property
    def name(self) -> str:
        anode_str = "REF" if self.anode is None else '_'.join([el.name for el in self.anode])
        cathode_str = "REF" if self.cathode is None else '_'.join([el.name for el in self.cathode])
        return f"{anode_str}-{cathode_str}"

    @property
    def abbr(self) -> str:
        anode_str = "REF" if self.anode is None else '_'.join([el.abbr for el in self.anode])
        cathode_str = "REF" if self.cathode is None else '_'.join([el.abbr for el in self.cathode])
   
    def apply_reference(self, signal: np.array) -> np.array:
        anode_signal = signal[self.anode_idx].mean(axis=0) if self.anode is not None else 0
        cathode_signal = signal[self.cathode_idx].mean(axis=0) if self.cathode is not None else 0
        return anode_signal - cathode_signal


