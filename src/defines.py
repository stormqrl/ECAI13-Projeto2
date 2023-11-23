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

    plt.plot(x_axis, vetor_gravacao, linewidth=.5)
    plt.title("Sinal adquirido na entrada")
    plt.xlabel("Tempo (s)")
    plt.ylabel("Amplitude")
    plt.subplots_adjust(hspace=0.5, wspace=0.5)    

def plotar_espectrograma(file_name, hop_length=512, n_fft=2048):
    y, sr = librosa.load(file_name)
    D = librosa.amplitude_to_db(np.abs(librosa.stft(y, hop_length=hop_length, n_fft=n_fft)), ref=np.max)

    librosa.display.specshow(D, sr=sr, hop_length=hop_length, x_axis='time', y_axis='log')
    plt.colorbar(format='%+2.0f dB')
    plt.title('Espectrograma')
    plt.xlabel('Tempo (s)')
    plt.subplots_adjust(hspace=0.5, wspace=0.5)
    
def calcular_tdf(sinal, tamanho_janela = 2048, posicao_janela = 0):
    janela = np.hamming(tamanho_janela)
    sinal_janelado = sinal[posicao_janela:posicao_janela + tamanho_janela] * janela
    tdf = np.fft.fft(sinal_janelado)
    frequencias = np.fft.fftfreq(tamanho_janela)
    return frequencias, tdf

def plotar_tdf(sinal, taxa_amostragem, tamanho_janela = 2048, posicao_janela = 0):
    frequencias, tdf = calcular_tdf(sinal, tamanho_janela, posicao_janela)
    frequencias_hz = frequencias * taxa_amostragem

    # Encontra o índice correspondente à metade positiva das frequências
    metade_tamanho = tamanho_janela // 2

    # Plota apenas a parte positiva da TDF
    plt.plot(frequencias_hz[:metade_tamanho], np.abs(tdf[:metade_tamanho]), linewidth=.5)
    plt.title('Transformada Discreta de Fourier (TDF)')
    plt.xlabel('Frequência (Hz)')
    plt.ylabel('Magnitude')
    plt.subplots_adjust(hspace=0.5, wspace=0.5)
