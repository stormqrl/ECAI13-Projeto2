import numpy as np
import librosa
import librosa.display
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

# Carrega o arquivo de áudio
audio_path = 'vogais.wav'
y, sr = librosa.load(audio_path)

# Obtém o espectrograma
D = librosa.amplitude_to_db(np.abs(librosa.stft(y)), ref=np.max)

# Encontra os picos no espectrograma
peaks, _ = find_peaks(D.mean(axis=1), height=-40, distance=50)

# Plota picos no espectrograma
plt.figure(figsize=(10, 6))
librosa.display.specshow(D, sr=sr, x_axis='time', y_axis='log')
plt.colorbar(format='%+2.0f dB')
plt.plot(librosa.times_like(D, sr=sr)[peaks], D.mean(axis=1)[peaks], 'ro', markersize=8)
plt.title('Espectrograma com Formantes Identificados')
plt.show()

# Obtém as frequências dos formantes
formant_frequencies = librosa.times_like(D, sr=sr)[peaks]

# Exibe as frequências dos formantes
print("Frequências dos Formantes (Hz):", formant_frequencies)
