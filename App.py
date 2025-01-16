from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QHBoxLayout,
    QWidget, QSpacerItem, QSizePolicy, QFileDialog, QGraphicsDropShadowEffect
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPainter
import sys

class MainWindow(QMainWindow):
    def __init__(self):  
        super().__init__()
        self.setWindowTitle("File Encryptor/Decryptor")
        self.setGeometry(600, 100, 600, 800)

        # Створюємо основний віджет і вертикальне розташування
        self.central_widget = QWidget(self)
        self.main_layout = QVBoxLayout(self.central_widget)

        # Додаємо вертикальний простір на початку, щоб змістити все вниз
        self.main_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))  # Spacer added at the top

        # Додаємо лейбл для GlobalLogic перед основним заголовком
        global_logic_label = QLabel("GlobalLogic")
        global_logic_label.setAlignment(Qt.AlignCenter)
        global_logic_label.setFont(QFont("Verdana", 20, QFont.Bold))  # Set font to Verdana, size 20
        global_logic_label.setStyleSheet("color: #007bff;")  # Set text color to blue
        self.main_layout.addWidget(global_logic_label)

        # Заголовок
        title_label = QLabel("File Encryptor/Decryptor")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont("Verdana", 26, QFont.Bold))  # Changed font to Verdana
        title_label.setStyleSheet("color: #333333;")
        self.main_layout.addWidget(title_label)

        # Додаємо кнопки Encrypt та Decrypt
        encrypt_button = QPushButton("Encrypt")
        encrypt_button.setStyleSheet(""" 
            QPushButton {
                font-size: 20px;
                padding: 15px;
                height: 50px;
                background-color: #414042;
                color: white; 
                border-radius: 40px;
            }
            QPushButton:hover {
                background-color: #555555;
            }
        """)
        encrypt_button.setFont(QFont("Arial", 18, QFont.Bold))  # Make text bold for Encrypt button
        self.add_shadow(encrypt_button)

        decrypt_button = QPushButton("Decrypt")
        decrypt_button.setStyleSheet("""
            QPushButton {
                font-size: 20px;
                padding: 15px;
                height: 50px;
                background-color: #007bff;
                color: white; 
                border-radius: 40px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
        """)
        decrypt_button.setFont(QFont("Arial", 18, QFont.Bold))  # Make text bold for Decrypt button
        self.add_shadow(decrypt_button)

        # Додаємо кнопки до макету
        self.main_layout.addWidget(encrypt_button)
        self.main_layout.addSpacing(20)
        self.main_layout.addWidget(decrypt_button)

        # Додаємо простір для кнопки "Select File" внизу
        self.main_layout.addStretch()

        # Додаємо кнопку для вибору файлу з сірим кольором
        file_button = QPushButton("Select File")
        file_button.setStyleSheet("""
            QPushButton {
                font-size: 20px;
                padding: 15px;
                height: 50px;
                background-color: #808080;
                color: white; 
                border-radius: 40px;
            }
            QPushButton:hover {
                background-color: #A9A9A9;
            }
        """)
        file_button.setFont(QFont("Arial", 18, QFont.Bold))
        self.add_shadow(file_button)
        file_button.clicked.connect(self.select_file)

        # Додаємо кнопку до макету внизу
        self.main_layout.addWidget(file_button)

        # Додаємо роздільник для простору
        self.main_layout.addStretch()

        # Додаємо підпис у нижній частині
        footer_layout = QHBoxLayout()
        copyright_label = QLabel("2025 Copyright GlobalLogic Inc. All rights reserved.")
        copyright_label.setStyleSheet(
            "font-size: 14px; color: #666666; text-align: center;"
        )
        copyright_label.setAlignment(Qt.AlignCenter)
        copyright_label.setFont(QFont("Verdana", 12))
        footer_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        footer_layout.addWidget(copyright_label)
        footer_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        self.main_layout.addLayout(footer_layout)

        # Призначаємо центральний віджет
        self.setCentralWidget(self.central_widget)

    def add_shadow(self, button):
        """Функція для додавання тіні до кнопки."""
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(8)
        shadow.setOffset(2, 2)
        shadow.setColor(Qt.black)
        button.setGraphicsEffect(shadow)

    def select_file(self):
        # Відкриваємо діалог вибору файлу
        file_name, _ = QFileDialog.getOpenFileName(self, "Select File")
        if file_name:
            print(f"File selected: {file_name}")  # Додати логіку для обробки файлу

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
