from defines import *

def main():
    record_time = float(input('Defina o tempo de gravação: '))
    sampling_rate = int(input('Defina a taxa de amostragem: '))

    audio_count = encontrar_proximo_numero()
    file_name = f'audio_{audio_count}.wav'

    # Gravação do áudio
    vetor_gravacao = gravar_audio(file_name, sampling_rate, record_time)

    # Define o tamanho da figura
    plt.figure(figsize=(12, 8))

    # Plotagem do sinal temporal
    plotar_sinal_temporal(vetor_gravacao, sampling_rate)

    # Plotagem da FFT
    plotar_fft(vetor_gravacao, sampling_rate)

    # Plotagem do espectrograma
    plotar_espectrograma(file_name)

    plt.show()

if __name__ == "__main__":
    main()
