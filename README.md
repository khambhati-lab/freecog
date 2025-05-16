# freecog

## Prerequisites
  1. Working install of [Python UV](https://docs.astral.sh/uv/getting-started/installation/) for environment management.
  2. Working install of FreeSurfer (v7 or v8).
 
## Installation Steps
  1. Clone repo from github

## Recons Generation
  1. Copy T1w NIFTI to the `mri` folder.
  2. Copy the T1w NIFTI to the `acpc` folder and rename to `T1_orig.nii.gz`.
  3. Use `freeview` to load `T1_orig.nii.gz` and align the RAS origin (0,0,0) to the ACPC line.
  4. Save the rotated and transformed image as `T1.nii.gz` in the `acpc` folder.

## Electrode Marking
  1. Uses freesurfers `freeview` program.
  2. Helpful to add all surfaces and volumes to the scene render.
  3. Adjust min/max range of the rCT volume to resolve electrode contacts. 
  4. Create a new `Point Set` to store contacts for each lead.
    i. `File` -> `New Point Set`; name the set after the lead.
    ii. Add a new control point for each contact in the lead. 
    iii. Name the contact using the convention {LEAD NAME}{CONTACT NUMBER ON LEAD} in the Comments section for that specific control point.
  5. Export the Point Set (`File` -> `Save Point Set As`) to JSON.
  6. Coordinates are exported in Scanner RAS format. They need to be converted to TkRegister RAS format for alignment to surface meshes, etc.

## Brainly
  1. WIP.
