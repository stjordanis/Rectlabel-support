import numpy as np
import os, pydicom
import PIL.Image
import sys

dcm_file = sys.argv[1]
output_folder = sys.argv[2]

def pixelArrayToImage(dcm_filename, frame_idx, pixel_array):
    shape = pixel_array.shape
    image_array = pixel_array.astype(float)
    image_array = (np.maximum(image_array, 0) / image_array.max()) * 255.0
    image_array = np.uint8(image_array)
    path_jpg = output_folder + '/' + dcm_filename + '_' + str(frame_idx) + '.jpg'
    im = PIL.Image.fromarray(image_array)
    im.save(path_jpg)

ds = pydicom.dcmread(dcm_file)
dcm_filename = os.path.splitext(os.path.basename(dcm_file))[0]
print(ds)
print(ds.Rows)
print(ds.Columns)
print(ds.SamplesPerPixel)
if 'NumberOfFrames' in ds:
    print(ds.NumberOfFrames)

frame_idx = 0
if not 'NumberOfFrames' in ds:
    pixelArrayToImage(dcm_filename, frame_idx, ds.pixel_array)
elif ds.NumberOfFrames == 1:
    pixelArrayToImage(dcm_filename, frame_idx, ds.pixel_array)
else:
    for frame_idx, pixel_array in enumerate(ds.pixel_array):
        pixelArrayToImage(dcm_filename, frame_idx, pixel_array)
    


