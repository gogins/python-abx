# python-abx #

<http://github.com/gogins/python-abx>

## About

python-abx is a simple GTK application for performing ABX testing using 
python3 and gstreamer.

The ABX Comparator tool makes it easy to perform a scientific, double-blind 
experiment to decide whether you can tell the difference between two 
soundfiles. This is useful when trying to find out whether a simple change in 
the software used to produce two soundfiles, representing the same piece of 
music or the same original sound, can be heard by you.

This is an updated fork of https://github.com/lrvick/python-abx. I have ported 
the code to Python3 and Gtk+ 3.0 and clarified the source code, the user 
interface, and the documentation.

I created this program in order to evaluate how Csound renders audio using 
different options and different variants of opcodes. As an example of such 
use, there are two variants of a Csound piece, **__Xanadu__**, in this 
repository --- `xanadu.csd` (the original) and `xanadu-high-resolution.csd` 
(modified by me for quieter and more accurate synthesis). I have described 
how this is done in the document **__Hearing Audio Quality in Csound__**, 
also contained in this repository.

## Installation

Install the following:

  * gstreamer1.0-gtk3 and its dependencies
  * python3
  * python3-gi
  * python3-gst

## Usage

1. Run abx.py: ```python3  abx.py```.

2. Select files for A and B.

3. Play A, B, and X and guess if A is X or B is X.

4. After a number of trials, click "Show" to print the probability you  
   identified X correctly just by accident. It may take a dozen or so trials 
   to obtain high confidence in your results. If you never do obtain a low 
   probability of a false positive, then you should probably conclude that 
   you just can't hear aby difference between the files.
   
The user may set a segment of the soundfiles for comparison. While playing, 
click the Start button at the desired position to set the start of the 
segment, then click the End button at the desired position to set the end of 
the segment. Click on the "Loop" button to enable or disable playing the 
segment in a repeating loop. 

To reset the start or end point of the segment, click again on the Start or 
End button