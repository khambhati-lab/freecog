"""ieeg_e2e_montage.py
End-to-End Montage Creation
"""
# Imports #
# Standard Libraries #
import os
import sys

# third-Party Packages #
from glob import glob
import numpy as np
import pickle as pkl
import scipy.io as sio
from tqdm import tqdm

# Local Packages #
from freecog import mri, ieeg

# Main Scripts #
def main(SUBJECT, FREESURFER_SUBJECT_PATH, PARCELLATION, ELECS, REREF):

    ## Define paths
    PARC_PATH = os.path.join(FREESURFER_SUBJECT_PATH, SUBJECT, "mri", PARCELLATION + ".mgz")
    
    ## Read electrode data
    ELECS_DAT = {'elecmatrix': [],
                 'eleclabels': []}
    for elecs in ELECS:
        ELECS_PATH = os.path.join(FREESURFER_SUBJECT_PATH, SUBJECT, "elecs", elecs + ".mat")
        elecs_dat = sio.loadmat(ELECS_PATH)
        ELECS_DAT['eleclabels'].append(elecs_dat['eleclabels'])
        ELECS_DAT['elecmatrix'].append(elecs_dat['elecmatrix'])
    ELECS_DAT['eleclabels'] = np.concatenate(ELECS_DAT['eleclabels'], axis=0)
    ELECS_DAT['elecmatrix'] = np.concatenate(ELECS_DAT['elecmatrix'], axis=0)

    ## Extract sensor information
    print("Extracting sensors...")
    sensors = []
    for ii, el in tqdm(enumerate(ELECS_DAT['eleclabels'])):
        el_s_id = ''.join(filter(lambda x: x.isdigit(), el[1][0]))
        el_full_name = ''.join(filter(lambda x: x.isalpha(), el[1][0]))
        el_abbr_name = ''.join(filter(lambda x: x.isalpha(), el[0][0]))
        el_type = el[2][0]
        if el_full_name == "NaN":
            continue
        coord = ELECS_DAT['elecmatrix'][ii]
        sensors.append((ii, el_full_name, el_abbr_name, el_type, el_s_id, coord[0], coord[1], coord[2]))
    sensors = np.array(sensors)
    

    ## Construct Electrodes and Sensors objects
    print("Constructing electrodes and sensor objects...")
    ieeg_electrodes = []
    ieeg_sensors = []
    for el in tqdm(np.unique(sensors[:,1])):
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

    ## Construct Montage
    print("Constructing montage...")
    ieeg_montage = ieeg.IntracranialEEGMontage(ieeg_sensors, "bipolar")

    ## PointAnatomy
    print("Parcellating channels...")
    ieeg_parc = mri.MRIAtlas(PARC_PATH)
    for ch in tqdm(ieeg_montage.channels):
        ch.anatomy.parcellate_point(ieeg_parc)

    return ieeg_montage

if __name__ == "__main__":
    FREESURFER_SUBJECT_PATH = "/media/ds2_imaging_subjects"
    PARCELLATION = "aparc.a2009s+aseg"
    ELECS = [["clinical_elecs_all"],
             ["stereo_elecs_alll",
              "stereo_elecs_allr"]]
    REREF = "bipolar"
    for SUBJECT in ["PR01", "PR03", "PR04", "PR05", "PR06", "PR07", "PR08", "PR09"]: 
        print(SUBJECT)

        OUT = f"/home/akhambhati/Holocron/montages/{SUBJECT}.pkl"
        if os.path.exists(OUT):
            assert True == False

        elecs_found = False
        for _ELECS in ELECS:
            if elecs_found:
                break

            try: 
                ieeg_montage = main(
                    SUBJECT,
                    FREESURFER_SUBJECT_PATH,
                    PARCELLATION,
                    _ELECS,
                    REREF
                )

                with open(OUT, "wb") as f:
                    pkl.dump(ieeg_montage, f)
                elecs_found = True
            except Exception as E:
                print(E)
                continue

    """
    #ELECS = ["clinical_elecs_all"]
    #ELECS = ["stereo_elecs_alll",
    #         "stereo_elecs_allr"]
    ELECS = [["clinical_elecs_all"],
             ["clinical_TDT_elecs_all"],
             ["TDT_clinical_elecs_all"],
             ["TDT_elecs_all"]]
    REREF = "bipolar"
    for SUBJECT_FULL in glob(os.path.join("/media/jaspernas/root_store/epilepsy_subjects/sub-EC*")):
        SUBJECT = SUBJECT_FULL.split('/')[-1]
        SUBJECT = SUBJECT.split('sub-EC')[1]
        SUBJECT = "EC" + str(int(SUBJECT))
        print(SUBJECT)

        OUT = f"/home/akhambhati/Holocron/montages/{SUBJECT}.pkl"
        if os.path.exists(OUT):
            assert True == False

        elecs_found = False
        for _ELECS in ELECS:
            if elecs_found:
                break

            try: 
                ieeg_montage = main(
                    SUBJECT,
                    FREESURFER_SUBJECT_PATH,
                    PARCELLATION,
                    _ELECS,
                    REREF
                )

                with open(OUT, "wb") as f:
                    pkl.dump(ieeg_montage, f)
                elecs_found = True
            except Exception as E:
                print(E)
                continue
    """
