#!/usr/bin/python3
# -*- coding: utf-8 -*-
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk 
gi.require_version("Gst", "1.0")
from gi.repository import Gst 
import sys
import random
import time
from gi.repository import GObject
from gi.repository import GLib
import math

Gst.init(sys.argv)

class AbxComparator:
    sound_player = Gst.ElementFactory.make("playbin3", "sound_player")
    soundfile_a = None
    soundfile_a_duration_nanoseconds = None
    soundfile_b = None
    soundfile_b_duration_nanoseconds = None
    soundfile_comparison_nanoseconds = None
    soundfile_current = None
    correct = 0
    incorrect = 0
    playback_segment_start_nanoseconds = 0
    playback_segment_end_nanoseconds = 0
    playback_current_position_nanoseconds = 0
    # keep track of whether we're dragging the position bar
    mouse_active_on_hscale = False
    # set the soundfiles, if available
    def __init__(self, soundfile_a=None, soundfile_b=None):
        ui = "abx-comparator.ui"
        builder = Gtk.Builder()
        builder.add_from_file(ui)
        builder.connect_signals(self)
        window = builder.get_object("abx_audio_window")
        window.show_all()
        self.state_change_latency = 1000000000 * .5
        self.a_button = builder.get_object("a_button")
        self.b_button = builder.get_object("b_button")
        self.x_button = builder.get_object("x_button")
        self.isa_button = builder.get_object("isa_button")
        self.isb_button = builder.get_object("isb_button")
        self.stop_button = builder.get_object("stop_button")
        self.repeat_button = builder.get_object("repeat_button")
        self.audio_position = builder.get_object("audio_position")
        self.audio_adjustment = builder.get_object("adjustment1")
        self.show_results_button = builder.get_object("show_results_button")
        self.text_buffer = builder.get_object("resultsview").get_buffer()
        self.begin_button = builder.get_object("startbutton")
        self.end_button = builder.get_object("endbutton")
        self.play_position = builder.get_object("play_position")

    def _on_main_window_delete_event(self, *args):
        self.quit()

    def _on_quit_button_clicked(self, *args):
        self.quit()

    def _on_show_results_button_toggled(self, *args):
        self.update_results()

    def _on_clear_results_button_clicked(self, *args):
        self.correct, self.incorrect = 0, 0
        self.update_results()

    def _on_a_button_toggled(self, *args):
        if self.a_button.get_active():
            # if paused, unpause
            if self.sound_player.get_state(self.state_change_latency)[1] == Gst.State.PAUSED:
                self.sound_player.set_state(Gst.State.PLAYING)
                GLib.timeout_add(50, self.update_slider)
                return
            if self.sound_player.get_state(self.state_change_latency)[1] == Gst.State.PLAYING:
                #self.playback_current_position_nanoseconds = self.sound_player.query_position(Gst.Format.TIME)[0]
                self.playback_current_position_nanoseconds = self.playback_segment_start_nanoseconds
            else:
                self.playback_current_position_nanoseconds = self.playback_segment_start_nanoseconds
            self.phoenix()
            self.x_button.set_active(False)
            self.b_button.set_active(False)
            self.sound_player.set_property('uri', self.soundfile_a)
            self.sound_player.set_state(Gst.State.PLAYING)
            # workaround for a playbin bug - we have to get the current state before it starts playing for some reason. check upstream?
            self.sound_player.get_state(self.state_change_latency)
            self.sound_player.seek_simple(Gst.Format.TIME, Gst.SeekFlags.FLUSH, self.playback_current_position_nanoseconds)
            #self.begin_button.set_sensitive(True)
            #self.end_button.set_sensitive(True)
            # set a 50 msec timeout to update the position slider
            GLib.timeout_add(50, self.update_slider)
        else:
            self.sound_player.set_state(Gst.State.PAUSED)

    # the other buttons are similar...
    def _on_b_button_toggled(self, *args):
        if self.b_button.get_active():
            if self.sound_player.get_state(self.state_change_latency)[1] == Gst.State.PAUSED:
                self.sound_player.set_state(Gst.State.PLAYING)
                GLib.timeout_add(50, self.update_slider)
                return
            if self.sound_player.get_state(self.state_change_latency)[1] == Gst.State.PLAYING:
                #self.playback_current_position_nanoseconds = self.sound_player.query_position(Gst.Format.TIME)[0]
                self.playback_current_position_nanoseconds = self.playback_segment_start_nanoseconds
            else:
                self.playback_current_position_nanoseconds = self.playback_segment_start_nanoseconds
            self.phoenix()
            self.a_button.set_active(False)
            self.x_button.set_active(False)
            self.sound_player.set_property('uri', self.soundfile_b)
            self.sound_player.set_state(Gst.State.PLAYING)
            self.sound_player.get_state(self.state_change_latency)
            self.sound_player.seek_simple(Gst.Format.TIME, Gst.SeekFlags.FLUSH, self.playback_current_position_nanoseconds)
            #self.begin_button.set_sensitive(True)
            #self.end_button.set_sensitive(True)
            GLib.timeout_add(50, self.update_slider)
        else:
            self.sound_player.set_state(Gst.State.PAUSED)

    def _on_x_button_toggled(self, *args):
        if self.x_button.get_active():
            if self.sound_player.get_state(self.state_change_latency)[1] == Gst.State.PAUSED:
                self.sound_player.set_state(Gst.State.PLAYING)
                GLib.timeout_add(50, self.update_slider)
                return
            if self.sound_player.get_state(self.state_change_latency)[1] == Gst.State.PLAYING:
                #self.playback_current_position_nanoseconds = self.sound_player.query_position(Gst.Format.TIME)[0]
                self.playback_current_position_nanoseconds = self.playback_segment_start_nanoseconds
            else:
                self.playback_current_position_nanoseconds = self.playback_segment_start_nanoseconds
            self.phoenix()
            self.a_button.set_active(False)
            self.b_button.set_active(False)
            self.sound_player.set_property('uri', self.soundfile_current)
            self.sound_player.set_state(Gst.State.PLAYING)
            self.sound_player.get_state(self.state_change_latency)
            self.sound_player.seek_simple(Gst.Format.TIME, Gst.SeekFlags.FLUSH, self.playback_current_position_nanoseconds)
            #self.begin_button.set_sensitive(True)
            #self.end_button.set_sensitive(True)
            GLib.timeout_add(50, self.update_slider)
        else:
            self.sound_player.set_state(Gst.State.PAUSED)
    
    # if user IDs a song, stop playing, and check for correct, giving points accordingly
    def _on_isa_button_clicked(self, *args):
        self.stop()
        if self.soundfile_current == self.soundfile_a: 
            self.correct += 1
        else:
            self.incorrect += 1
        self.prepare_trial()

    def _on_isb_button_clicked(self, *args):
        self.stop()
        if self.soundfile_current == self.soundfile_b: 
            self.correct += 1
        else:
            self.incorrect += 1
        self.prepare_trial()

    def _start_selection_button_toggled(self, *args):
        if self.begin_button.get_active():
            # set rounded version of time as label text
            self.begin_button.set_label(str("%.2f" %(self.audio_adjustment.get_value() / 1000000000)))
            # record position to playback_segment_start_nanoseconds
            self.playback_segment_start_nanoseconds = self.audio_adjustment.get_value()
        else:
            self.begin_button.set_label("Start")
            self.playback_segment_start_nanoseconds = 0

    def _end_selection_button_toggled(self, *args):
        if self.end_button.get_active():
            self.end_button.set_label(str("%.2f" %(self.audio_adjustment.get_value() / 1000000000)))
            self.playback_segment_end_nanoseconds = self.audio_adjustment.get_value()
            # we've just set an "end position", so immediately loop to the playback_segment_start_nanoseconds
            self.sound_player.seek_simple(Gst.Format.TIME, Gst.SeekFlags.FLUSH, self.playback_segment_start_nanoseconds)
        else:
            self.end_button.set_label("End")
            self.playback_segment_end_nanoseconds = 0

    def _on_stop_button_clicked(self, *args):
        self.stop()

    def _a_file_chosen(self, button):
        self.soundfile_a = button.get_uri()
        self.soundfile_a_duration_nanoseconds = self.load_file(self.soundfile_a)
        self.prepare_trial()

    def _b_file_chosen(self, button):
        self.soundfile_b = button.get_uri()
        self.soundfile_b_duration_nanoseconds = self.load_file(self.soundfile_b)
        self.prepare_trial()

    # set the bool for mouse dragging when we're active
    def _hscale_button_press(self, *args):
        self.mouse_active_on_hscale = True

    def _hscale_button_release(self, *args):
        current_position = self.audio_adjustment.get_value()
        self.play_position.set_label("{:9.4f}".format(current_position / 1000000000))
        self.sound_player.seek_simple(Gst.Format.TIME, Gst.SeekFlags.FLUSH, self.audio_adjustment.get_value())
        # and then set the bool. not the other way around to avoid potential problems with timing
        self.mouse_active_on_hscale = False
        return
        
    def load_file(self, location):
        # load a temporary playbin instance, and use it to determine duration
        tempPlayer = Gst.ElementFactory.make("playbin3", "sound_player")
        tempPlayer.set_property('uri', location)
        tempPlayer.set_state(Gst.State.PAUSED)
        tempPlayer.get_state(self.state_change_latency)
        # Simulate synchronous call...
        for i in range(10):
            tempPlayer.get_state(self.state_change_latency)
            duration_ = tempPlayer.query_duration(Gst.Format.TIME)
            print("duration_:", duration_)
            duration = duration_[1]
            if duration_:
                break
        if duration_[0] == False:
            dialog = Gtk.MessageDialog(parent=None, 
                message_type=Gtk.MessageType.ERROR,
                buttons=Gtk.ButtonsType.OK, 
                text="Couldn't determine stream duration.",
                secondary_text="Either this is an unsupported soundfile format, or you should just try reloading the file.")
            dialog.run()
            dialog.destroy() 
        else:            
            print("Loaded: {}, {} seconds.".format(location, duration / 1000000000))
        tempPlayer.set_state(Gst.State.NULL)
        return duration

    def prepare_trial(self, *args):
        # only run if both files are loaded
        if (self.soundfile_a_duration_nanoseconds != None and self.soundfile_b_duration_nanoseconds != None):
            # set pos. slider to min of two files to prevent user from "cheating"    
            self.audio_adjustment.set_upper(min(self.soundfile_a_duration_nanoseconds, self.soundfile_b_duration_nanoseconds))
            self.enable_buttons()
            # prepare test
            if random.random() > 0.5:
                self.soundfile_current = self.soundfile_a
            else:
                self.soundfile_current = self.soundfile_b
        self.update_results()

    def update_results(self, *args):
        if self.show_results_button.get_active():
            score_value = str(self.correct)
            # hackish way of calculating p
            # p = 0.5 ^ (number of trials) * summation of the binominal coefficient from (number of guesses) to (number of attempts)
            # see http://mathforum.org/library/drmath/view/71267.html and http://vassarstats.net/textbook/index.html chapter 5 append. 5
            n = self.correct + self.incorrect
            k = self.correct
            p = 0
            for x in range(k, n + 1):
                p = p + math.factorial(n) / (math.factorial(x) * math.factorial(n - x)) * 0.5 ** n
            p_str = "{:10.8f}".format(p)
        else:
            score_value, p_str = "hidden", "hidden"
        self.text_buffer.set_text("Score: " + score_value + " / " + str(self.correct + self.incorrect) + "\np = " + str(p_str))

    # run on a timer every 50msec whenever sound_player is playing
    def update_slider(self, *args):
        current_position = self.sound_player.query_position(Gst.Format.TIME)[1] / 1000000000
        self.play_position.set_label("{:9.4f}".format(current_position))
        # don't deactivate if dragging position slider, just bypass
        if self.mouse_active_on_hscale:
            return True
        # if we're not playing, stop the timer
        if self.sound_player.get_state(self.state_change_latency)[1] == Gst.State.NULL:
            return False
        # if we've run past the slider or past the user's limit, stop
        if self.sound_player.query_position(Gst.Format.TIME)[1] > self.audio_adjustment.get_upper() or self.sound_player.query_position(Gst.Format.TIME)[1] > self.playback_segment_end_nanoseconds and self.playback_segment_end_nanoseconds != 0:
            #repeat if selected
            if self.repeat_button.get_active():
                # sanity check the playback_segment_start_nanoseconds, and go there if appropriate
                if self.playback_segment_end_nanoseconds > self.playback_segment_start_nanoseconds:
                    self.sound_player.seek_simple(Gst.Format.TIME, Gst.SeekFlags.FLUSH, self.playback_segment_start_nanoseconds)
                else:
                    self.sound_player.seek_simple(Gst.Format.TIME, Gst.SeekFlags.FLUSH, 0.0)
            else:
                self.stop()
                return False
        # seems to fail occasionally if still seeking, so simply get_state() and wait for the next timed update
        try:
            self.audio_adjustment.set_value(self.sound_player.query_position(Gst.Format.TIME)[1])
        except:
            self.sound_player.get_state(self.state_change_latency)
        self.sound_player.get_state(self.state_change_latency)[1] == Gst.State.PLAYING
        return True

    # phoenix(), a dirty hack to work around bugs in playbin2
    # idea from the quodlibet player
    # see http://code.google.com/p/quodlibet/source/browse/quodlibet/quodlibet/player/gstbe.py

    def phoenix (self, *args):
        self.sound_player.set_state(Gst.State.NULL)
        self.sound_player.get_state(self.state_change_latency)
        self.sound_player = None
        self.sound_player = Gst.ElementFactory.make("playbin3", "sound_player")
     
    # and a few obvious handlers   
    def enable_buttons(self, *args):
        self.begin_button.set_sensitive(True)
        self.end_button.set_sensitive(True)
        self.a_button.set_sensitive(True)
        self.x_button.set_sensitive(True)
        self.b_button.set_sensitive(True)
        self.isa_button.set_sensitive(True)
        self.isb_button.set_sensitive(True)
        self.stop_button.set_sensitive(True)
        self.audio_position.set_sensitive(True)

    def stop(self, *args):
        self.a_button.set_active(False)
        self.b_button.set_active(False)
        self.x_button.set_active(False)
        #self.begin_button.set_sensitive(False)
        #self.end_button.set_sensitive(False)
        self.sound_player.set_state(Gst.State.NULL)
        self.audio_adjustment.set_value(self.playback_segment_start_nanoseconds)
    
    def quit(self, *args):
        Gtk.main_quit(*args)

Gtk.Window.set_default_icon_from_file("abx-comparator.svg")

a, b = None, None
# if we have at least 2 arguments, go ahead and set file A
if 2 < len(sys.argv) <= 3:
    a = sys.argv[1]
    if not Gst.uri_is_valid(a):
        a = "file://" + os.path.abspath(a)

# and if we have 3, set file B as well
if len(sys.argv) == 3:
    b = sys.argv[2]
    if not Gst.uri_is_valid(b):
        b = "file://" + os.path.abspath(b)

app = AbxComparator(a, b)
Gtk.main()
