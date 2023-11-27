from PySide6.QtCore import QThread, Signal
import pyaudio, numpy as np
from scipy.io import wavfile

class AudioThread(QThread):
    finished = Signal(np.ndarray)

    def __init__(self, file_name, sampling_rate, record_time):
        super().__init__()
        self.file_name = file_name
        self.sampling_rate = sampling_rate
        self.record_time = record_time

    def run(self):
        chunk = 1024
        formato = pyaudio.paInt16
        canais = 1

        p = pyaudio.PyAudio()
        stream = p.open(
            format=formato,
            channels=canais,
            rate=self.sampling_rate,
            input=True,
            frames_per_buffer=chunk,
        )

        frames = []

        print("Comece a falar.")
        for i in range(0, int(self.sampling_rate / chunk * self.record_time)):
            data = stream.read(chunk)
            frames.append(np.frombuffer(data, dtype=np.int16))

        print("Pare de falar.")

        stream.stop_stream()
        stream.close()
        p.terminate()

        vetor_gravacao = np.concatenate(frames)
        wavfile.write(self.file_name, self.sampling_rate, vetor_gravacao)

        self.finished.emit(vetor_gravacao)