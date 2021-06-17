# python-abx #

<http://github.com/gogins/python-abx>

## About

A simple GTK application for performing ABX testing using python3 and gstreamer.

This is an updated fork of https://github.com/lrvick/python-abx. I have ported the code to Python3 and Gtk+ 3.0.

## Requirements

  * python3
  * GTK3
  * gstreamer (And various good, bad, and ugly modules as needed)
  * python-gtk
  * python-gst

## Current Features

  * Swap A/B on at any point while playing.
  * Perform any number of tests and show/hide results at any time.

## Usage / Installation

1. Run abx.py: ```python3  abx.py```.

2. Select files for A and B

3. Play A, B, and X and guess if A is X or B is X.

4. Click "Show" after a number of trials to see your results.
