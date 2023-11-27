import sys, os
import numpy as np
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, QLineEdit, QPushButton, QLabel
from PySide6.QtCore import Signal
from PySide6.QtGui import QIcon
from Components.GraphTab import GraphTab, ClosableTabWidget
from Components.VowelTable import VowelTable
from Components.AudioThread import AudioThread
from defines import *

if getattr(sys, 'frozen', False):
    # Quando executado como executável
    base_dir = sys._MEIPASS
else:
    # Quando executado como script Python
    base_dir = os.path.dirname(os.path.abspath(__file__))

class AudioRecorderApp(QMainWindow):
    change_label = Signal(str)
    record_thread: AudioThread
    
    vetor_gravacao: np.ndarray
    record_time: float
    sampling_rate: int
    window_size: int
    window_pos: int
    
    def __init__(self):
        super().__init__()

        self.setWindowTitle("J.A.R.V.I.S.")
        self.setGeometry(100, 100, 800, 600)
        self.setup_ui()
        
        self.setWindowIcon(QIcon(f'{base_dir}/assets/JARVIS-logo.png'))
        
        self.change_label.connect(self.update_label)

    def update_label(self, text: str):
        self.info_label.setText(text)
    
    def setup_ui(self):
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Layouts
        main_layout = QHBoxLayout(central_widget)
        left_layout = QVBoxLayout()
        form_layout = QFormLayout()
        right_layout = QVBoxLayout()

        # Line edits
        self.tempo_gravacao = QLineEdit()
        self.taxa_amostragem = QLineEdit()
        self.tam_janela = QLineEdit()
        self.pos_janela = QLineEdit()

        self.info_label = QLabel()
        
        # Left side (formulario)
        form_layout.addRow("Tempo de Gravação:", self.tempo_gravacao)
        form_layout.addRow("Taxa de Amostragem:", self.taxa_amostragem)
        form_layout.addRow("Tamanho da Janela:", self.tam_janela)
        form_layout.addRow("Posição da Janela:", self.pos_janela)
        form_layout.addRow(self.info_label)
    
        
        record_button = QPushButton("Gravar Áudio")
        form_layout.addWidget(record_button)
        left_layout.addLayout(form_layout)
        
        # Creating table
        self.vowel_table = VowelTable()
        left_layout.addWidget(self.vowel_table)
        
        # Button layout
        button_layout = QHBoxLayout()
        self.spectrogram_btn = QPushButton(text="Espectrograma")
        self.temp_signal_btn = QPushButton(text="Sinal [s]")
        button_layout.addWidget(self.spectrogram_btn)
        button_layout.addWidget(self.temp_signal_btn)
        self.spectrogram_btn.clicked.connect(self.spectogram_button_clicked)
        self.spectrogram_btn.setEnabled(False)
        self.temp_signal_btn.clicked.connect(self.sinal_temporal_button_clicked)
        self.temp_signal_btn.setEnabled(False)
        
        left_layout.addLayout(button_layout)
        
        # Right side (gráficos)
        self.tab_widget = ClosableTabWidget()
        right_layout.addWidget(self.tab_widget)

        # Adicione os layouts ao layout principal
        main_layout.addLayout(left_layout, 1)
        main_layout.addLayout(right_layout, 2)

        # Conecte o botão à função add_tab
        record_button.clicked.connect(self.record_button_clicked)
    
    def gravar_audio(self, file_name, sampling_rate, record_time):
        self.record_thread = AudioThread(file_name, sampling_rate, record_time)
        self.record_thread.finished.connect(self.handle_finished)
        self.record_thread.start()

    def handle_finished(self, vetor_gravacao):
        self.change_label.emit("Pare de falar.")
        self.record_time = len(vetor_gravacao) / (self.sampling_rate / 2)
        
        self.spectrogram_btn.setEnabled(True)
        self.temp_signal_btn.setEnabled(True)
        
        window_size = 2048
        window_pos = 0
        
        self.vetor_gravacao = pf_f(vetor_gravacao, self.sampling_rate)

        vec_size = vetor_gravacao.size
        n = 5
        
        for i in range(0, n):
            if i > 4:
                break
            # print(f"{vowels[i]} - ", end="")
            tab = GraphTab()
            tab.vowel_identified.connect(self.vowel_table.add_row)
            self.tab_widget.addTab(tab, f"Gráficos {self.tab_widget.count()+1}")

            # Selecione a guia recém-criada
            self.tab_widget.setCurrentIndex(self.tab_widget.count() - 1)
            tab.plotar_tdf_com_picos(
                vetor_gravacao[int(vec_size * i / n) : int(vec_size * (i + 1) / n)],
                self.sampling_rate,
                window_size,
                window_pos,
            )
            # g.show()
            # f = plt.figure(f"Signal_{vowels[i]}")
            tab.plotar_sinal_temporal(
                vetor_gravacao[int(vec_size * i / n) : int(vec_size * (i + 1) / n)],
                self.sampling_rate,
            )
            # f.show()


    def spectogram_button_clicked(self):
        # Plotagem do espectrograma
        h = plt.figure("Spectogram")
        plotar_espectrograma(self.vetor_gravacao, self.sampling_rate, self.window_size, n_fft=self.window_size)
        h.show()
    
    def sinal_temporal_button_clicked(self):
        # Plotagem da FFT
        g = plt.figure("TDF")
        plotar_sinal_temporal(self.vetor_gravacao, self.sampling_rate)
        g.show()

    def record_button_clicked(self):
        self.record_time = float(self.tempo_gravacao.text())
        self.sampling_rate = int(self.taxa_amostragem.text())
        self.window_size = int(self.tam_janela.text())
        self.window_pos = int(self.pos_janela.text())
        
        audio_count = encontrar_proximo_numero()
        file_name = f"audio_{audio_count}.wav"

        print(file_name)
        
        self.change_label.emit("Comece a falar.")
        self.gravar_audio(file_name, self.sampling_rate, self.record_time)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AudioRecorderApp()
    window.show()
    sys.exit(app.exec())