from PySide6.QtWidgets import QTableWidget, QTableWidgetItem,QHeaderView

class VowelTable(QTableWidget):
    def __init__(self):
        super().__init__(0, 2)  # 0 linhas, 2 colunas
        self.setHorizontalHeaderLabels(["Entrada", "Vogal"])
        self.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.verticalHeader().setVisible(False)
        self.setColumnWidth(0, 70)  # Ajuste a largura da primeira coluna conforme necessário
        self.setColumnWidth(1, 150)  # Ajuste a largura da segunda coluna conforme necessário

    def add_row(self, vogal):
        row_position = self.rowCount()
        self.insertRow(row_position)

        entrada_item = QTableWidgetItem(str(row_position + 1))
        vogal_item = QTableWidgetItem(vogal)

        self.setItem(row_position, 0, entrada_item)
        self.setItem(row_position, 1, vogal_item)