# python-abx #

<http://github.com/gogins/python-abx>

## About

This is a simple GTK application for performing ABX testing using python3 and 
gstreamer.

The ABX Comparator tool makes it easy to perform a scientific, double-blind 
experiment to decide whether you can tell the difference between two 
soundfiles. This is useful when trying to find out whether a simple change in 
the software used to produce two soundfiles, representing the same piece of 
music or the same original sound, can be heard by you.

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

4. After a number of trials, click "Show" to print the probability you identified 
   X correctly just by accident. It may take a dozen or so trials to obtain 
   confidence in your results.
   
For looping, while playing, click the Start button at the desired position for 
the start of the loop, then click the End button at the desired position for 
the end of the loop. Click on the "Loop" button to enable or disable looping. 
When looping is enabled, playback will loop between the Start and End 
positions. To hear another sample between the same points, toggle the original 
play button to stop looping, and click another play button to start looping 
that sample.
