import numpy as np
import matplotlib.pyplot as plt
import pyaudio
from scipy.io import wavfile
import librosa
import librosa.display
import glob

def gravar_audio(file_name, sampling_rate, record_time=5):
    chunk = 1024
    formato = pyaudio.paInt16
    canais = 1

    p = pyaudio.PyAudio()
    stream = p.open(format=formato,
                    channels=canais,
                    rate=sampling_rate,
                    input=True,
                    frames_per_buffer=chunk)

    frames = []

    print("Comece a falar.")
    for i in range(0, int(sampling_rate / chunk * record_time)):
        data = stream.read(chunk)
        frames.append(np.frombuffer(data, dtype=np.int16))

    print("Pare de falar.")

    stream.stop_stream()
    stream.close()
    p.terminate()

    vetor_gravacao = np.concatenate(frames)
    wavfile.write(file_name, sampling_rate, vetor_gravacao)

    return vetor_gravacao

def encontrar_proximo_numero():
    audio_files = glob.glob("audio_*.wav")
    numeros = [int(file.split("_")[1].split(".")[0]) for file in audio_files]
    if numeros:
        return max(numeros) + 1
    else:
        return 1

def plotar_sinal_temporal(vetor_gravacao, sampling_rate):
    periodo_amostragem = 1 / sampling_rate
    x_axis = np.arange(0, len(vetor_gravacao)) * periodo_amostragem

    plt.subplot(2, 2, 1)
    plt.plot(x_axis, vetor_gravacao)
    plt.title("Sinal adquirido na entrada")
    plt.xlabel("Tempo (s)")
    plt.ylabel("Amplitude")

def plotar_fft(vetor_gravacao, sampling_rate):
    periodo_amostragem = 1 / sampling_rate
    eixoX_FFT = np.fft.fftshift(np.fft.fftfreq(len(vetor_gravacao), periodo_amostragem))

    indice_central = len(eixoX_FFT) // 2

    saida_fft = np.abs(np.fft.fftshift(np.fft.fft(vetor_gravacao)))

    plt.subplot(2, 2, 3)
    plt.plot(eixoX_FFT[indice_central:], saida_fft[indice_central:], linewidth=3)
    plt.title("Magnitude Complexa do Espectro da FFT")
    plt.xlabel("f (Hz)")
    plt.ylabel("Módulo FFT")
    plt.subplots_adjust(hspace=0.5)

def plotar_espectrograma(file_name):
    y, sr = librosa.load(file_name)
    D = librosa.amplitude_to_db(np.abs(librosa.stft(y)), ref=np.max)

    plt.subplot(1, 2, 2)
    librosa.display.specshow(D, sr=sr, x_axis='time', y_axis='log')
    plt.colorbar(format='%+2.0f dB')
    plt.title('Espectrograma')
    plt.xlabel('Tempo (s)')