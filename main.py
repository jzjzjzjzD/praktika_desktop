import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox
)
from datetime import datetime
from database import initialize_db, add_item, get_items, update_item, delete_item, receive_item, ship_item, generate_report

class WarehouseApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        initialize_db()
        self.setWindowTitle('Система управления складом')
        self.setGeometry(100, 100, 800, 600)
        self.layout = QVBoxLayout()

        # Форма для добавления товара
        self.form_layout = QHBoxLayout()
        self.name_input = QLineEdit(self)
        self.name_input.setPlaceholderText('Название товара')
        self.quantity_input = QLineEdit(self)
        self.quantity_input.setPlaceholderText('Количество')
        self.location_input = QLineEdit(self)
        self.location_input.setPlaceholderText('Местоположение')
        self.add_button = QPushButton('Добавить товар', self)
        self.add_button.clicked.connect(self.add_item)

        self.form_layout.addWidget(self.name_input)
        self.form_layout.addWidget(self.quantity_input)
        self.form_layout.addWidget(self.location_input)
        self.form_layout.addWidget(self.add_button)

        # Таблица для отображения товаров
        self.table = QTableWidget(self)
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(['ID', 'Название', 'Количество', 'Местоположение'])
        self.load_items()

        # Форма для приёмки и отгрузки
        self.receive_ship_layout = QHBoxLayout()
        self.item_id_input = QLineEdit(self)
        self.item_id_input.setPlaceholderText('ID товара')
        self.quantity_input_rs = QLineEdit(self)
        self.quantity_input_rs.setPlaceholderText('Количество')
        self.receive_button = QPushButton('Принять', self)
        self.receive_button.clicked.connect(self.receive_item)
        self.ship_button = QPushButton('Отгрузить', self)
        self.ship_button.clicked.connect(self.ship_item)

        self.receive_ship_layout.addWidget(self.item_id_input)
        self.receive_ship_layout.addWidget(self.quantity_input_rs)
        self.receive_ship_layout.addWidget(self.receive_button)
        self.receive_ship_layout.addWidget(self.ship_button)

        # Форма для удаления товара
        self.delete_layout = QHBoxLayout()
        self.delete_id_input = QLineEdit(self)
        self.delete_id_input.setPlaceholderText('ID товара для удаления')
        self.delete_button = QPushButton('Удалить товар', self)
        self.delete_button.clicked.connect(self.delete_item)

        self.delete_layout.addWidget(self.delete_id_input)
        self.delete_layout.addWidget(self.delete_button)

        # Кнопка для генерации отчётов
        self.report_button = QPushButton('Сгенерировать отчёт', self)
        self.report_button.clicked.connect(self.generate_report)

        # Добавление элементов в основной макет
        self.layout.addLayout(self.form_layout)
        self.layout.addWidget(self.table)
        self.layout.addLayout(self.receive_ship_layout)
        self.layout.addLayout(self.delete_layout)  # Добавляем форму удаления
        self.layout.addWidget(self.report_button)
        self.setLayout(self.layout)

    def add_item(self):
        name = self.name_input.text()
        quantity = self.quantity_input.text()
        location = self.location_input.text()

        if name and quantity and location:
            add_item(name, int(quantity), location)
            self.name_input.clear()
            self.quantity_input.clear()
            self.location_input.clear()
            self.load_items()
        else:
            QMessageBox.warning(self, 'Ошибка', 'Заполните все поля')

    def load_items(self):
        self.table.setRowCount(0)
        items = get_items()
        for row_number, row_data in enumerate(items):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))

    def receive_item(self):
        item_id = self.item_id_input.text()
        quantity = self.quantity_input_rs.text()
        if item_id and quantity:
            try:
                receive_item(int(item_id), int(quantity), datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                self.item_id_input.clear()
                self.quantity_input_rs.clear()
                self.load_items()
            except Exception as e:
                QMessageBox.warning(self, 'Ошибка', str(e))
        else:
            QMessageBox.warning(self, 'Ошибка', 'Заполните все поля')

    def ship_item(self):
        item_id = self.item_id_input.text()
        quantity = self.quantity_input_rs.text()
        if item_id and quantity:
            try:
                ship_item(int(item_id), int(quantity), datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                self.item_id_input.clear()
                self.quantity_input_rs.clear()
                self.load_items()
            except Exception as e:
                QMessageBox.warning(self, 'Ошибка', str(e))
        else:
            QMessageBox.warning(self, 'Ошибка', 'Заполните все поля')

    def delete_item(self):
        item_id = self.delete_id_input.text()
        if item_id:
            try:
                delete_item(int(item_id))
                self.delete_id_input.clear()
                self.load_items()
                QMessageBox.information(self, 'Успех', 'Товар успешно удалён')
            except Exception as e:
                QMessageBox.warning(self, 'Ошибка', str(e))
        else:
            QMessageBox.warning(self, 'Ошибка', 'Введите ID товара для удаления')

    def generate_report(self):
        report = generate_report()
        report_text = "Отчёт:\n"
        for row in report:
            report_text += f"Товар: {row[0]}, Остаток: {row[1]}, Принято: {row[2]}, Отгружено: {row[3]}\n"
        QMessageBox.information(self, 'Отчёт', report_text)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = WarehouseApp()
    window.show()
    sys.exit(app.exec_())