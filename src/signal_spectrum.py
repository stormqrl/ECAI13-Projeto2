from defines import *


def main():
    record_time = float(input("Defina o tempo de gravação: "))
    sampling_rate = int(input("Defina a taxa de amostragem: "))
    window_size = int(input("[TDF] Defina o tamanho da janela: "))
    window_pos = int(input("[TDF] Defina a posição da janela: "))

    audio_count = encontrar_proximo_numero()

    file_name = f"audio_{audio_count}.wav"
    sampling_rate = 44100

    # Gravação do áudio
    vetor_gravacao = gravar_audio(file_name, sampling_rate, record_time)

    record_time = len(vetor_gravacao) / (sampling_rate / 2)
    window_size = 2048
    window_pos = 0

    vetor_gravacao = pf_f(vetor_gravacao, sampling_rate)

    vec_size = vetor_gravacao.size
    vowels = ["a", "e", "i", "o", "u"]
    n = 5

    for i in range(0, n):
        if i > 4:
            break
        print(f"{vowels[i]} - ", end="")
        g = plt.figure(f"TDF_{vowels[i]}")
        plotar_tdf_com_picos(
            vetor_gravacao[int(vec_size * i / n) : int(vec_size * (i + 1) / n)],
            sampling_rate,
            window_size,
            window_pos,
        )
        g.show()
        f = plt.figure(f"Signal_{vowels[i]}")
        plotar_sinal_temporal(
            vetor_gravacao[int(vec_size * i / n) : int(vec_size * (i + 1) / n)],
            sampling_rate,
        )
        f.show()

    # Plotagem da FFT
    g = plt.figure("TDF")
    plotar_tdf(vetor_gravacao, sampling_rate, window_size, window_pos)
    g.show()

    # Plotagem do espectrograma
    h = plt.figure("Spectogram")
    plotar_espectrograma(vetor_gravacao, sampling_rate, window_size, n_fft=window_size)
    h.show()

    if input():
        return


if __name__ == "__main__":
    main()
