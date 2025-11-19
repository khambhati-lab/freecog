"""ieeg_e2e_montage.py
End-to-End Montage Creation
"""
# Imports #
# Standard Libraries #
import sys

# third-Party Packages #
import numpy as np
import scipy.io as sio

# Local Packages #
from freecog import mri, ieeg

# Main Scripts #
## Read electrode data
elecs_all = sio.loadmat("/home/akhambhati/Holocron/scratch/EC320/elecs/TDT_elecs_all.mat")
parc_all = "/home/akhambhati/Holocron/scratch/EC320/mri/aparc.a2009s+aseg.mgz"

## Extract sensor information
sensors = []
for ii, el in enumerate(elecs_all['anatomy']):
    el_s_id = ''.join(filter(lambda x: x.isdigit(), el[1][0]))
    el_full_name = ''.join(filter(lambda x: x.isalpha(), el[1][0]))
    el_abbr_name = ''.join(filter(lambda x: x.isalpha(), el[0][0]))
    el_type = el[2][0]
    if el_full_name == "NaN":
        continue
    coord = elecs_all['elecmatrix'][ii]

    sensors.append((ii, el_full_name, el_abbr_name, el_type, el_s_id, coord[0], coord[1], coord[2]))
sensors = np.array(sensors)

## Construct Electrodes and Sensors objects
ieeg_electrodes = []
ieeg_sensors = []
for el in np.unique(sensors[:,1]):
    el_sensors = sensors[sensors[:,1] == el]

    n = int(len(el_sensors))
    if el_sensors[0][3] == "grid":
        i = int(np.ceil(np.sqrt(n)))
        while True:
            if (n % i) == 0:
                break
            i += 1
        assert n == (i * (n // i))
        geometry = (n // i, i)
    else:
        geometry = (n, 1)

    ieeg_electrodes.append(
        ieeg.IntracranialEEGElectrode(
            name=el_sensors[0][1],
            abbr=el_sensors[0][2],
            type=el_sensors[0][3],
            geometry=geometry
        )
    )

    for s in el_sensors:
        ieeg_sensors.append(
            ieeg.IntracranialEEGSensor(
                electrode=ieeg_electrodes[-1],
                id=int(s[4]),
                idx=int(s[0]),
                anatomy=mri.MRIPointAnatomy(ras_surf=s[5:8].astype(float))
            )
        )
        print(ieeg_sensors[-1])

## Construct Montage
ieeg_montage = ieeg.IntracranialEEGMontage(ieeg_sensors, "common_global_reference")
for ch in ieeg_montage.channels:
    print(ch.name, ch.anatomy, ch.anode[0].anatomy, ch.cathode[0].anatomy)

## Apply Re-Reference Scheme to a Signal
signal = np.random.randn(elecs_all['anatomy'].shape[0], 1024)
signal_reref = ieeg_montage.apply_reference(signal)

## PointAnatomy
ieeg_parc = mri.MRIAtlas(parc_all)

ieeg_sensors[0].anatomy.parcellate_point(ieeg_parc)
print(ieeg_sensors[0].anatomy)
print(ieeg_sensors[0].anatomy.parcellation)
