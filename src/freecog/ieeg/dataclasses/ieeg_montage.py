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
from typing import List, Literal

# Third-Party Packages #
import numpy as np

# Local Packages #
from .ieeg_channel import IntracranialEEGChannel
from .ieeg_sensor import IntracranialEEGSensor

# Definitions #
# Classes #
@dataclass
class IntracranialEEGMontage:
    sensors: List[IntracranialEEGSensor]
    reference: Literal[
            "referential",
            "common_global_reference",
            "common_electrode_reference",
            "bipolar"] = "bipolar"

    def __post_init__(self):
        channels = []
        match self.reference:
            case "referential":
                for s in self.sensors:
                    channels.append(
                        IntracranialEEGChannel(anode=[s], cathode=None)
                    )

            case "common_global_reference":
                for s in self.sensors:
                    channels.append(
                        IntracranialEEGChannel(anode=[s], cathode=self.sensors)
                    )

            case "common_electrode_reference":
                electrodes_name = np.array([s.electrode.name for s in self.sensors])
                for el_name in np.unique(electrodes_name):
                    el_sensors = [s for s in self.sensors if s.electrode.name == el_name]
                    for s in el_sensors:
                        channels.append(
                            IntracranialEEGChannel(anode=[s], cathode=el_sensors)
                        )

            case "bipolar":
                electrodes_name = np.array([s.electrode.name for s in self.sensors])
                for el_name in np.unique(electrodes_name):
                    el_sensors = [s for s in self.sensors if s.electrode.name == el_name]
                    el_size = el_sensors[0].electrode.size 
                    el_type = el_sensors[0].electrode.type
                    el_geom = el_sensors[0].electrode.geometry
                   
                    nr, nc = el_geom

                    CA = np.arange(el_size).reshape((nr, nc), order='F')
                    if nr > 1:
                        for ii, (bp1, bp2) in enumerate(zip(
                            CA[:-1, :].flatten(),
                            CA[1:, :].flatten()
                        )):
                            channels.append(
                                IntracranialEEGChannel(
                                    anode=[s for s in el_sensors if s.id == (bp1+1)],
                                    cathode=[s for s in el_sensors if s.id == (bp2+1)]
                                )
                            )
        self.channels = channels

    def apply_reference(self, signal: np.array) -> np.array:
        return np.array([ch.apply_reference(signal) for ch in self.channels])
