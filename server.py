import sys
import json
import random
import multiprocessing

import numpy as np
import librosa
import librosa.display

from scipy import signal
from flask import Flask, request

class MP3Processor():
    def __init__(self, f):
        self.f = f
        self.y, self.sr = librosa.load(self.f)
        self.beat_samples = []

    def get_beat_locs(self):
        _, beats = librosa.beat.beat_track(y=self.y, sr=self.sr)

        self.beat_samples = librosa.frames_to_samples(beats)
    
    def export(self):
        beats_played = []
        for ts in self.beat_samples:
            beats_played.append((ts, random.randint(1, 3)))

        beats_played_str = ""
        for beat in beats_played:
            beats_played_str += str(beat[0]) + " " + str(beat[1]) + "\n"

        return beats_played_str

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    f = request.args.get('filename')
    
    my_processor = MP3Processor(f)
    my_processor.get_beat_locs()
    return my_processor.export()

if __name__ == '__main__':
    app.run(debug=True, port=65432)

