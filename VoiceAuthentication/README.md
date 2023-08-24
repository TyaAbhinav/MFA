
from future import division import numpy import decimal import math import logging from scipy.fftpack import dct import scipy.io.wavfile from functools import reduce from collections import defaultdict import matplotlib.pyplot as plt import pickle import wave import sys import pyaudio

register -> live audio record -------- microphone store in db ------------ microphone folder name = user name

login -> live audio save in login authn folder ----------- microphone + match_file match from database folder
if match: show user name if not: print msg

[x] Enter 1 to insert voices in our file\n -------- insert_voice_in_file [ ] Enter 2 to read Voices from our file\n [ ] Enter 3 to Check matching with other voices by inputting a new voice\n [ ] Enter 4 to print file\n [ ] Enter 5 to delete a voice from Database\n [ ] Enter 6 to check shape of file\n [x] Enter 7 to Store a new voice to database live(Through Microphone)\n ------------ microphone + read_audio [x] Enter 8 to check best matching voice by inputting a live new voice(Through Microphone)") ------ microphone + match_file


register ->
	live audio record -------- microphone
	store in db ------------ microphone
	folder name = user name

login ->
	live audio
	save in login authn folder ----------- microphone + match_file
	match from database folder    
		if match: show user name
		if not: print msg


[x]    Enter 1 to insert voices in our file\n  -------- insert_voice_in_file
[x]    Enter 7 to Store a new voice to database live(Through Microphone)\n ------------ microphone + read_audio
[x]    Enter 8 to check best matching voice by inputting a live new voice(Through Microphone)")  ------ microphone + match_file