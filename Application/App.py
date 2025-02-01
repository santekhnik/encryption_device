import subprocess
import sys
import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QSpacerItem, QSizePolicy, QGraphicsDropShadowEffect
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import serial  # Для UART комунікації
import time  # Для затримок

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

        self.mode = None  # Це буде визначати чи шифруємо чи дешифруємо

    def add_shadow(self, button):
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(8)
        shadow.setOffset(2, 2)
        shadow.setColor(Qt.black)
        button.setGraphicsEffect(shadow)

    def encrypt_file(self):
        self.mode = 'E'  # Встановлюємо режим шифрування
        self.select_file_and_process()

    def decrypt_file(self):
        self.mode = 'D'  # Встановлюємо режим дешифрування
        self.select_file_and_process()

    def select_file_and_process(self):
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename(title="Select file")
        if file_path:
            self.process_file(file_path, self.mode)  # Викликаємо обробку залежно від обраного режиму
        else:
            messagebox.showinfo("Information", "No file selected.")

    def add_command_and_crc(self, chunk):
        # Додавання команди до першого байта: 'E' для шифрування (0x45), 'D' для дешифрування (0x44)
       if self.mode == 'E':
            command = bytearray([0x45])
       elif self.mode == 'D':
            command = bytearray([0x44])
       else:
            raise ValueError("Невідомий режим: потрібно задати 'E' або 'D'.")
        

        # Обчислення CRC (BCC) для всіх байтів, включаючи команду
       checksum = command[0]
       for byte in chunk:
            checksum ^= byte  # XOR кожного байта з попередньою чексу

        # Створення нового фрагмента з командою та чексу
       new_chunk = bytearray([command[0], checksum]) + chunk
       return new_chunk

    def process_file(self, file_path, mode):
        try:
            # Читання файлу як байти
            with open(file_path, "rb") as file:
                file_data = file.read()

            # Розбиваємо файл на фрагменти
            chunks = [file_data[i:i+256] for i in range(0, len(file_data), 256)]  # Розбиваємо на фрагменти

            result_data = bytearray()

            # Створення папки для збереження оброблених файлів
            folder_name = os.path.join(os.path.dirname(file_path), "Processed_Files")
            os.makedirs(folder_name, exist_ok=True)

            received_folder = os.path.join(os.path.dirname(file_path), "Received_Fragments")
            os.makedirs(received_folder, exist_ok=True)

            sending_folder = os.path.join(os.path.dirname(file_path), "Sending_Fragments")
            os.makedirs(sending_folder, exist_ok=True)

            # Відкриття порту для UART
            with serial.Serial('COM5', 9600, timeout=1) as ser:
                for idx, chunk in enumerate(chunks):
                    # Додаємо команду та чексу до фрагмента
                    chunk_with_command_and_crc = self.add_command_and_crc(chunk)

                    # Відправка фрагмента як масиву байтів
                    ser.write(chunk_with_command_and_crc)
                    ser.timeout = 2

                    # Збереження фрагментів до відправки
                    fragment_file = os.path.join(sending_folder, f"fragment_{idx + 1}.bin")
                    with open(fragment_file, "wb") as fragment_out:
                        fragment_out.write(chunk_with_command_and_crc)

                    # Читання відповіді від STM
                    response = ser.read(len(chunk_with_command_and_crc))
                    result_data.extend(response)
                    ser.timeout = 2
                    
                    # Збереження отриманого фрагмента
                    response_fragment_file = os.path.join(received_folder, f"fragment_{idx + 1}.bin")
                    with open(response_fragment_file, "wb") as fragment_out:
                        fragment_out.write(response)

                    # Затримка між відправленням і отриманням фрагментів
                    time.sleep(1)  # Затримка 0.5 секунди (можна налаштувати)

            # Об'єднання всіх фрагментів в один файл
            defrag_file_path = os.path.join(folder_name, os.path.basename(file_path))
            with open(defrag_file_path, "wb") as defrag_file:
                for idx in range(len(chunks)):
                    fragment_file = os.path.join(received_folder, f"fragment_{idx + 1}.bin")
                    with open(fragment_file, "rb") as fragment_in:
                        defrag_file.write(fragment_in.read())

            # Збереження отриманого файлу
            with open(defrag_file_path, "wb") as final_file:
                final_file.write(result_data)

            messagebox.showinfo("Success", f"File processed successfully. Output saved as {defrag_file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
