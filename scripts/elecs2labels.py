#!/usr/bin/env -S uv run
import os
import sys
import csv
import json
import numpy as np
import scipy.io as sio
import nibabel as nib

elecsall_file = sys.argv[1]
aseg_file = sys.argv[2]
lut_file = sys.argv[3]

###
elecall = sio.loadmat(elecsall_file)
elecmatrix = elecall['elecmatrix']

###
dat = nib.freesurfer.load(aseg_file)
aparc_dat = dat.get_fdata()

###
affine = np.array([[  -1.,    0.,    0.,  128.],
                   [   0.,    0.,    1., -128.],
                   [   0.,   -1.,    0.,  128.],
                   [   0.,    0.,    0.,    1.]])
intercept = np.ones(len(elecmatrix))
elecs_ones = np.column_stack((elecmatrix, intercept))
VoxCRS = np.dot(np.linalg.inv(affine), elecs_ones.transpose()).transpose().astype(int)

# Get the names of these labels using Freesurfer's lookup table (LUT)
print("Loading lookup table for freesurfer labels")
fid = open(lut_file)
LUT = fid.readlines()
fid.close()

# Dictionary of labels
LUT = [row.split() for row in LUT]
lab = {}
for row in LUT:
    if len(row)>1 and row[0][0] is not '#' and row[0][0] is not '\\': # Get rid of the comments
        lname = row[1]
        lab[int(row[0])] = lname

# Label the electrodes according to the aseg volume
nchans = VoxCRS.shape[0]
anatomy = np.empty((nchans,), dtype=object)
print("Labeling electrodes...")

for elec in np.arange(nchans):
    anatomy[elec] = lab[aparc_dat[VoxCRS[elec,0], VoxCRS[elec,1], VoxCRS[elec,2]]]

##
sio.savemat(elecsall_file, {
    "eleclabels": elecall["eleclabels"],
    "elecmatrix": elecall["elecmatrix"],
    "anatomy": anatomy})

print(sio.loadmat(elecsall_file))
