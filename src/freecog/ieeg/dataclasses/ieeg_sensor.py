"""ieeg_sensor.py
Dataclass Specification for Sensor-level information
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

# Third-Party Packages #
# Local Packages #
from .ieeg_electrode import IntracranialEEGElectrode

# Definitions #
# Classes #
@dataclass
class IntracranialEEGSensor:
    electrode: IntracranialEEGElectrode
    id: int   # e.g. Sensor number on the electrode
    idx: int = None     # Data index on a digital acquisition system

    @property
    def name(self) -> str:
        return f"{self.electrode.name}{self.id:0{self.electrode.n_digits()}d}"

    @property
    def abbr(self) -> str:
        return f"{self.electrode.abbr}{self.id:0{self.electrode.n_digits()}d}"
