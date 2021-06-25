# python-abx #
![GitHub All Releases (total)](https://img.shields.io/github/downloads/gogins/csound-extended/total.svg)<br>
[![Github All Releases](https://img.shields.io/github/downloads/gogins/python-abx/total.svg)]()
<br>
https://github.com/gogins<br>
http://michaelgogins.tumblr.com


<http://github.com/gogins/python-abx>

## About

The ABX Comparator tool (`abx.py`) is a simple GTK application for performing 
ABX testing using python3 and gstreamer.

The ABX Comparator tool makes it easy to perform a scientific, double-blind 
experiment to decide whether you can tell the difference between two 
soundfiles. This is useful when trying to find out whether a simple change in 
the software used to produce two soundfiles, representing the same piece of 
music or the same original sound, can be heard by you.

I created this program in order to evaluate how Csound renders audio using 
different options and different variants of opcodes. As an example of such 
use, there are two variants of a Csound piece, **_Xanadu_**, in this 
repository --- `xanadu.csd` (the original) and `xanadu-high-resolution.csd` 
(modified by me for quieter and more accurate synthesis). I have described 
how this is done in the document [_Hearing Audio Quality in Csound_](csound-audio-quality.pdf), 
also contained in this repository.

This is an updated fork of https://github.com/lrvick/python-abx. I have ported 
the code to Python3 and Gtk+ 3.0 and clarified the source code, the user 
interface, and the documentation.

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
   
The user may set a segment of the soundfiles for comparison. Click the Start 
button to set the beginning of the segment, and click the End button to set 
the end of the segment. Click on the "Loop" button to enable or disable 
playing the segment in a repeating loop. Clicking again on the Start or End 
button resets its position.

For more information, see [_Hearing Audio Quality in Csound_](csound-audio-quality.pdf) 
in this repository.

