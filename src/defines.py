import numpy as np
import matplotlib.pyplot as plt
import pyaudio
from scipy.io import wavfile
import librosa
import librosa.display
import glob
from scipy.signal import find_peaks, butter, lfilter

from scipy.signal import butter, lfilter


def pf_f(
    sinal,
    taxa_amostragem,
    frequencia_corte_inferior=50,
    frequencia_corte_superior=3200,
    ordem=4,
):
    # Normaliza as frequências de corte para a frequência de Nyquist
    frequencia_corte_inferior_normalizada = frequencia_corte_inferior / (
        taxa_amostragem / 2
    )
    frequencia_corte_superior_normalizada = frequencia_corte_superior / (
        taxa_amostragem / 2
    )

    # Projeta o filtro passa-banda Butterworth
    b, a = butter(
        ordem,
        [frequencia_corte_inferior_normalizada, frequencia_corte_superior_normalizada],
        btype="band",
        analog=False,
    )

    # Aplica o filtro ao sinal
    sinal_filtrado = lfilter(b, a, sinal)

    return sinal_filtrado


def pb_f(sinal, taxa_amostragem, frequencia_corte=4000, ordem=4):
    # Normaliza a frequência de corte para a frequência de Nyquist
    frequencia_corte_normalizada = frequencia_corte / (taxa_amostragem / 2)

    # Projeta o filtro passa-baixas Butterworth
    b, a = butter(ordem, frequencia_corte_normalizada, btype="low", analog=False)

    # Aplica o filtro ao sinal
    sinal_filtrado = lfilter(b, a, sinal)

    return sinal_filtrado


def gravar_audio(file_name, sampling_rate, record_time=5):
    chunk = 1024
    formato = pyaudio.paInt16
    canais = 1

    p = pyaudio.PyAudio()
    stream = p.open(
        format=formato,
        channels=canais,
        rate=sampling_rate,
        input=True,
        frames_per_buffer=chunk,
    )

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


def abrir_arquivo_audio(file_name):
    vetor_gravacao, _ = librosa.load(file_name, sr=None)
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

    plt.plot(x_axis, vetor_gravacao, linewidth=0.5)
    plt.title("Sinal adquirido na entrada")
    plt.xlabel("Tempo (s)")
    plt.ylabel("Amplitude")
    plt.subplots_adjust(hspace=0.5, wspace=0.5)


def plotar_espectrograma(vetor_gravacao, sampling_rate, window_size, n_fft=2048):
    y, sr = vetor_gravacao, sampling_rate
    dt = 1 / sr

    print(f"{y.size} {sr} time {y.size/sr}")
    plt.specgram(y, NFFT=n_fft, Fs=sr, noverlap=int(window_size / 2), cmap="gnuplot")
    plt.colorbar(format="%+2.0f dB")
    plt.title("Espectrograma")
    plt.xlabel("Tempo (s)")
    plt.subplots_adjust(hspace=0.5, wspace=0.5)


def calcular_tdf(sinal, tamanho_janela=2048, posicao_janela=0):
    janela = np.hamming(tamanho_janela)
    sinal_janelado = sinal[posicao_janela : posicao_janela + tamanho_janela] * janela
    tdf = np.fft.fft(sinal_janelado)
    frequencias = np.fft.fftfreq(tamanho_janela)
    return frequencias, tdf


def encontrar_maiores_picos_tdf(
    sinal, taxa_amostragem, tamanho_janela=2048, posicao_janela=0, num_picos=5
):
    frequencias, tdf = calcular_tdf(sinal, tamanho_janela, posicao_janela)
    frequencias_hz = frequencias * taxa_amostragem

    # Encontra o índice correspondente à metade positiva das frequências
    metade_tamanho = tamanho_janela // 2

    # Considera apenas a parte positiva da TDF
    tdf_positiva = np.abs(tdf[:metade_tamanho])

    # Encontra os índices dos maiores picos
    indices_maiores_picos = np.argsort(tdf_positiva)[-num_picos:][::-1]

    # Retorna as frequências e magnitudes dos maiores picos
    frequencias_maiores_picos = frequencias_hz[indices_maiores_picos]
    magnitudes_maiores_picos = tdf_positiva[indices_maiores_picos]

    return frequencias_maiores_picos, magnitudes_maiores_picos


def identificar_vogal(melhores_frequencias):
    frequencias_vogais = {
        "a": [0.0, 172.265625, 1033.59375, 689.0625, 1722.65625],
        "e": [0.0, 172.265625, 344.53125, 689.0625, 516.796875],
        "i": [0.0, 172.265625, 516.796875, 689.0625, 1205.859375],
        "o": [172.265625, 0.0, 344.53125, 2756.25, 2583.984375],
        "u": [172.265625, 344.53125, 0.0, 689.0625, 1550.390625],
    }

    # Inicializa uma lista de tuplas contendo a vogal e a distância média
    distancias = []

    # Condições para identificar a vogal com base nas frequências passadas
    for vogal, freq_vogal in frequencias_vogais.items():
        distancias_vogal = []
        for freq in melhores_frequencias:
            distancias_vogal.append(min([abs(freq - f) for f in freq_vogal]))

        distancia_media = sum(distancias_vogal) / len(distancias_vogal)
        distancias.append((vogal, distancia_media))

    # Retorna a vogal com a menor distância média
    if distancias:
        return min(distancias, key=lambda x: x[1])[0]
    else:
        # Se não houver vogais definidas, retorna None
        return None


def plotar_tdf(sinal, taxa_amostragem, tamanho_janela=2048, posicao_janela=0):
    frequencias, tdf = calcular_tdf(sinal, tamanho_janela, posicao_janela)
    frequencias_hz = frequencias * taxa_amostragem

    # Encontra o índice correspondente à metade positiva das frequências
    metade_tamanho = tamanho_janela // 2

    # Plota apenas a parte positiva da TDF
    plt.plot(
        frequencias_hz[:metade_tamanho], np.abs(tdf[:metade_tamanho]), linewidth=0.5
    )
    plt.title("Transformada Discreta de Fourier (TDF)")
    plt.xlabel("Frequência (Hz)")
    plt.ylabel("Magnitude")
    plt.subplots_adjust(hspace=0.5, wspace=0.5)


def plotar_tdf_com_picos(sinal, taxa_amostragem, tamanho_janela=2048, posicao_janela=0):
    frequencias_picos, magnitudes_picos = encontrar_maiores_picos_tdf(
        sinal, taxa_amostragem, tamanho_janela, posicao_janela
    )

    print(f"Vogal: {identificar_vogal(frequencias_picos)}")

    # Plota a TDF
    frequencias, tdf = calcular_tdf(sinal, tamanho_janela, posicao_janela)
    frequencias_hz = frequencias * taxa_amostragem
    metade_tamanho = tamanho_janela // 2

    plt.plot(
        frequencias_hz[:metade_tamanho],
        np.abs(tdf[:metade_tamanho]),
        linewidth=0.5,
        label="TDF",
    )

    # Plota os picos
    plt.plot(frequencias_picos, magnitudes_picos, "ro", label="Picos")

    # print(*frequencias_picos, sep=",")

    plt.title("Transformada Discreta de Fourier (TDF) com Picos")
    plt.xlabel("Frequência (Hz)")
    plt.ylabel("Magnitude")
