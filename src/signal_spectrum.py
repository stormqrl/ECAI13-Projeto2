from defines import *

def main():
    record_time = float(input('Defina o tempo de gravação: '))
    sampling_rate = int(input('Defina a taxa de amostragem: '))
    window_size = int(input('[TDF] Defina o tamanho da janela: '))
    window_pos = int(input('[TDF] Defina a posição da janela: '))

    audio_count = encontrar_proximo_numero()
    file_name = f'audio_{audio_count}.wav'

    # Gravação do áudio
    vetor_gravacao = gravar_audio(file_name, sampling_rate, record_time)

    f = plt.figure(1)
    plotar_sinal_temporal(vetor_gravacao, sampling_rate)
    f.show()

    g = plt.figure(2)
    # Plotagem da FFT
    plotar_tdf(vetor_gravacao, sampling_rate, window_size, window_pos)
    g.show()

    h = plt.figure(3)
    # Plotagem do espectrograma
    plotar_espectrograma(file_name, n_fft=window_size)
    h.show()

    if input():
        return

if __name__ == "__main__":
    main()
