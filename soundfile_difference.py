#!/bin/python
'''
This program computes the difference between two soundfiles and runs Audacity 
to view and hear it. This can show the nature of artifacts caused by 
differences in processing the soundfiles.

Author: Michael Gogins
License: Gnu Lesser General Public License, version 2.1

Requirements:

    --  libsndfile
    --  Python3
    --  soundfile PIP package
    --  numpy or scipy PIP package
    --  Audacity soundfile editor
'''
import numpy
import soundfile
import subprocess
import sys

if len(sys.argv) > 2:
    filename_a = sys.argv[1]
    filename_b = sys.argv[2]
else:
    filename_a = "xanadu.wav"
    filename_b = "xanadu-high-resolution.wav"
filename_difference = "difference.wav"
soundfile_a = soundfile.SoundFile(filename_a)
print(soundfile_a, soundfile_a.frames)
soundfile_b = soundfile.SoundFile(filename_b)
if soundfile_a.samplerate != soundfile_b.samplerate:
    print("Error: Both soundfiles must have the same sample rate.")
    exit()
if soundfile_a.channels != soundfile_b.channels:
    print("Error: Both soundfiles must have the same number of channels.")
    exit()
    
print(soundfile_b, soundfile_b.frames)
frames = min(soundfile_a.frames, soundfile_b.frames)
print("Frames:", frames)
soundfile_difference = soundfile.SoundFile(filename_difference, "w+", samplerate = soundfile_b.samplerate, channels = 2, format = "WAVEX", subtype = "FLOAT")
print(soundfile_difference)
block_frames = int(soundfile_b.samplerate)
block_count = int(frames / block_frames)
shape = (soundfile_b.channels, block_frames)
buffer_a = numpy.zeros(shape, "float64")
buffer_b = numpy.zeros(shape, "float64")
buffer_difference = numpy.zeros(shape, "float64")
for block in range(block_count):
    print("Block {:9d}".format(block))
    soundfile_a.buffer_read_into(buffer_a, "float64")
    soundfile_b.buffer_read_into(buffer_b, "float64")
    numpy.subtract(buffer_a, buffer_b, buffer_difference)
    soundfile_difference.buffer_write(buffer_difference, "float64")
soundfile_a.close()
soundfile_b.close()
soundfile_difference.close()

subprocess.run("audacity {}".format(filename_difference), shell=True)
    
