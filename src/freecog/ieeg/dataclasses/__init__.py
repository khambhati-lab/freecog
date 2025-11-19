"""__init__.py
General Dataclasses for IEEG electrode, sensors, channels, and montages.
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

# Third-Party Packages #

# Local Packages #
from .ieeg_channel import IntracranialEEGChannel
from .ieeg_electrode import IntracranialEEGElectrode
from .ieeg_montage import IntracranialEEGMontage
from .ieeg_sensor import IntracranialEEGSensor
