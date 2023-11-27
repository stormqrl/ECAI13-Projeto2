from PySide6.QtWidgets import QTabWidget, QVBoxLayout, QWidget
from PySide6.QtCore import Signal
import pyqtgraph as pg
from defines import *

class ClosableTabWidget(QTabWidget):
    def __init__(self):
        super().__init__()
        self.setTabsClosable(True)
        self.tabBar().tabCloseRequested.connect(self.close_tab)

    def close_tab(self, index):
        self.removeTab(index)

class GraphTab(QWidget):
    vowel_identified = Signal(str)
    
    def __init__(self):
        super().__init__()

        self.setup_ui()

    def setup_ui(self):
        tab_layout = QVBoxLayout(self)

        # Adicione três widgets de plotagem
        self.plot_widget1 = pg.PlotWidget()
        self.plot_widget1.setBackground("w")
        tab_layout.addWidget(self.plot_widget1)

        self.plot_widget2 = pg.PlotWidget()
        self.plot_widget2.setBackground("w")
        tab_layout.addWidget(self.plot_widget2)

    def plotar_sinal_temporal(self, vetor_gravacao, sampling_rate):
        periodo_amostragem = 1 / sampling_rate
        x_axis = np.arange(0, len(vetor_gravacao)) * periodo_amostragem

        # Limpar o gráfico antes de adicionar um novo
        self.plot_widget1.clear()

        # Plotar o sinal no primeiro gráfico da tab
        self.plot_widget1.plot(x_axis, vetor_gravacao, pen='b')
        self.plot_widget1.setTitle("Sinal adquirido na entrada")
        self.plot_widget1.setLabel('left', 'Amplitude')
        self.plot_widget1.setLabel('bottom', 'Tempo (s)')

    def plotar_tdf_com_picos(self, sinal, taxa_amostragem, tamanho_janela=2048, posicao_janela=0):
        frequencias_picos, magnitudes_picos = encontrar_maiores_picos_tdf(
            sinal, taxa_amostragem, tamanho_janela, posicao_janela
        )

        self.vowel_identified.emit(f"Vogal: {identificar_vogal(frequencias_picos)}")

        # Calcular a TDF
        frequencias, tdf = calcular_tdf(sinal, tamanho_janela, posicao_janela)
        frequencias_hz = frequencias * taxa_amostragem
        metade_tamanho = tamanho_janela // 2

        # Limpar o gráfico antes de adicionar um novo
        self.plot_widget2.clear()

        # Plotar TDF no segundo gráfico da tab
        self.plot_widget2.plot(
            frequencias_hz[:metade_tamanho],
            np.abs(tdf[:metade_tamanho]),
            pen='b',
            name='TDF'
        )

        # Plotar picos no segundo gráfico da tab
        self.plot_widget2.plot(
            frequencias_picos,
            magnitudes_picos,
            pen=None,
            symbol='o',
            symbolPen='r',
            symbolBrush='r',
            name='Picos'
        )

        self.plot_widget2.setTitle("Transformada Discreta de Fourier (TDF) com Picos")
        self.plot_widget2.setLabel('left', 'Magnitude')
        self.plot_widget2.setLabel('bottom', 'Frequência (Hz)')