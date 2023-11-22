import numpy as np
import matplotlib.pyplot as plt
import pyaudio

# Define o tempo de gravação e a taxa de amostragem
record_time = float(input('Defina o tempo de gravação: '))
sampling_rate = int(input('Defina a taxa de amostragem: '))

# Configura a gravação com pyaudio
chunk = 1024
formato = pyaudio.paInt16
canais = 1

p = pyaudio.PyAudio()
stream = p.open(format=formato,
                channels=canais,
                rate=sampling_rate,
                input=True,
                frames_per_buffer=chunk)

print("Comece a falar.")
frames = []

for i in range(0, int(sampling_rate / chunk * record_time)):
    data = stream.read(chunk)
    frames.append(np.frombuffer(data, dtype=np.int16))

print("Pare de falar.")

stream.stop_stream()
stream.close()
p.terminate()

# Converte os frames para um array numpy
vetorGravacao = np.concatenate(frames)

# Cria o vetor de tempo
periodoDeAmostragem = 1 / sampling_rate
x_axis = np.arange(0, len(vetorGravacao)) * periodoDeAmostragem

# Plota o sinal gravado
plt.subplot(2, 1, 1)
plt.plot(x_axis, vetorGravacao)
plt.title("Sinal adquirido na entrada")
plt.xlabel("Tempo (s)")
plt.ylabel("Amplitude")

# Calcula e plote a FFT
saidaFFT = np.abs(np.fft.fftshift(np.fft.fft(vetorGravacao)))
eixoX_FFT = np.fft.fftshift(np.fft.fftfreq(len(vetorGravacao), periodoDeAmostragem))

indice_central = len(eixoX_FFT) // 2

plt.subplot(2, 1, 2)
plt.plot(eixoX_FFT[indice_central:], saidaFFT[indice_central:], linewidth=3)
plt.title("Magnitude Complexa do Espectro da FFT")
plt.xlabel("f (Hz)")
plt.ylabel("Módulo FFT")
plt.subplots_adjust(hspace=0.5)
plt.show()
