import subprocess
import sys
import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QSpacerItem, QSizePolicy, QGraphicsDropShadowEffect
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import serial  # Для UART комунікації

# Переконатися, що необхідні бібліотеки встановлені
def install_libraries():
    required_libraries = ['PyQt5', 'tkinter', 'pyserial']
    for library in required_libraries:
        try:
            __import__(library)
        except ImportError:
            print(f"{library} not found. Installing...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", library])
            print(f"{library} installed!")

install_libraries()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("File Encryptor/Decryptor")
        self.setGeometry(600, 100, 600, 800)

        self.central_widget = QWidget(self)
        self.main_layout = QVBoxLayout(self.central_widget)

        # Спейсер для балансування макету
        self.main_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Заголовок
        global_logic_label = QLabel("GlobalLogic")
        global_logic_label.setAlignment(Qt.AlignCenter)
        global_logic_label.setFont(QFont("Verdana", 20, QFont.Bold))
        global_logic_label.setStyleSheet("color: #007bff;")
        self.main_layout.addWidget(global_logic_label)

        title_label = QLabel("File Encryptor/Decryptor")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont("Verdana", 26, QFont.Bold))
        title_label.setStyleSheet("color: #333333;")
        self.main_layout.addWidget(title_label)

        # Кнопка для шифрування
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
        encrypt_button.setFont(QFont("Arial", 18, QFont.Bold))
        self.add_shadow(encrypt_button)
        encrypt_button.clicked.connect(self.encrypt_file)

        # Кнопка для дешифрування
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
        decrypt_button.setFont(QFont("Arial", 18, QFont.Bold))
        self.add_shadow(decrypt_button)
        decrypt_button.clicked.connect(self.decrypt_file)

        # Додати кнопки на макет
        self.main_layout.addWidget(encrypt_button)
        self.main_layout.addSpacing(20)
        self.main_layout.addWidget(decrypt_button)

        self.main_layout.addStretch()

        # Футер
        footer_layout = QHBoxLayout()
        copyright_label = QLabel("2025 Copyright GlobalLogic Inc. All rights reserved.")
        copyright_label.setStyleSheet("font-size: 14px; color: #666666; text-align: center;")
        copyright_label.setAlignment(Qt.AlignCenter)
        copyright_label.setFont(QFont("Verdana", 12))
        footer_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        footer_layout.addWidget(copyright_label)
        footer_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        self.main_layout.addLayout(footer_layout)

        self.setCentralWidget(self.central_widget)

    def add_shadow(self, button):
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(8)
        shadow.setOffset(2, 2)
        shadow.setColor(Qt.black)
        button.setGraphicsEffect(shadow)

    def encrypt_file(self):
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename(title="Select file to encrypt")
        if file_path:
            self.process_file(file_path, mode=1)  # Режим шифрування
        else:
            messagebox.showinfo("Information", "No file selected for encryption.")

    def decrypt_file(self):
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename(title="Select file to decrypt")
        if file_path:
            self.process_file(file_path, mode=2)  # Режим дешифрування
        else:
            messagebox.showinfo("Information", "No file selected for decryption.")

    def process_file(self, file_path, mode):
        try:
            file_size = os.path.getsize(file_path)
            chunks = []
            
            # Читання файлу по 255 байт
            with open(file_path, "rb") as file:
                while True:
                    chunk = file.read(255)
                    if not chunk:
                        break
                    chunks.append(chunk)

            result_data = bytearray()

            # Створення папки для збереження оброблених файлів
            folder_name = os.path.join(os.path.dirname(file_path), "Processed_Files")
            os.makedirs(folder_name, exist_ok=True)

            # Папка для отриманих фрагментів
            received_folder = os.path.join(os.path.dirname(file_path), "Received_Fragments")
            os.makedirs(received_folder, exist_ok=True)

            # Папка для фрагментів до відправки
            sending_folder = os.path.join(os.path.dirname(file_path), "Sending_Fragments")
            os.makedirs(sending_folder, exist_ok=True)

            # Відправка фрагментів через UART
            with serial.Serial('COM5', 9600, timeout=1) as ser:
                for idx, chunk in enumerate(chunks):
                    # Тепер ми не використовуємо контрольну суму, лише байти
                    packet = chunk
                    ser.write(packet)
                    ser.timeout = 0.5

                    # Збереження фрагментів до відправки
                    fragment_file = os.path.join(sending_folder, f"fragment_{idx + 1}.txt")
                    with open(fragment_file, "wb") as fragment_out:
                        fragment_out.write(chunk)

                    # Читання відповіді від STM
                    response = ser.read(len(chunk))
                    result_data.extend(response)

                    # Збереження кожного отриманого фрагмента окремо в папці
                    response_fragment_file = os.path.join(received_folder, f"fragment_{idx + 1}.txt")
                    with open(response_fragment_file, "wb") as fragment_out:
                        fragment_out.write(response)

            # Перевірка розміру результату перед збиранням
            if len(result_data) != file_size:
                messagebox.showerror("Error", "Received file size mismatch. The received data does not match the expected size.")
                return

            # Об'єднання всіх фрагментів в один файл
            defrag_file_path = os.path.join(folder_name, os.path.basename(file_path) + (".enc" if mode == 1 else ".dec"))
            with open(defrag_file_path, "wb") as defrag_file:
                for idx in range(len(chunks)):
                    fragment_file = os.path.join(received_folder, f"fragment_{idx + 1}.txt")
                    with open(fragment_file, "rb") as fragment_in:
                        defrag_file.write(fragment_in.read())

            messagebox.showinfo("Success", f"File processed successfully. Output saved as {defrag_file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
