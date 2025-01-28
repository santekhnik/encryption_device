import subprocess
import sys
import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QSpacerItem, QSizePolicy, QFileDialog, QGraphicsDropShadowEffect
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import serial  # For UART communication

# Ensure required libraries are installed
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

        # Spacer for layout balance
        self.main_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Header label
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

        # Encrypt button
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

        # Decrypt button
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
        decrypt_button.clicked.connect(self.decrypt_files)

        # Add buttons to layout
        self.main_layout.addWidget(encrypt_button)
        self.main_layout.addSpacing(20)
        self.main_layout.addWidget(decrypt_button)

        self.main_layout.addStretch()

        # Footer
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
            self.process_file(file_path, mode=1)  # Encryption mode
        else:
            messagebox.showinfo("Information", "No file selected for encryption.")

    def decrypt_files(self):
        root = tk.Tk()
        root.withdraw()
        folder_path = filedialog.askdirectory(title="Select folder with encrypted files")
        if folder_path:
            self.process_folder(folder_path, mode=2)  # Decryption mode
        else:
            messagebox.showinfo("Information", "No folder selected for decryption.")

    def process_file(self, file_path, mode):
        try:
            file_size = os.path.getsize(file_path)
            chunks = []
            with open(file_path, "rb") as file:
                while chunk := file.read(255):
                    chunks.append(chunk)

            # Initialize an empty bytearray for the final result
            result_data = bytearray()

            # Create a new folder for saving processed files
            folder_name = os.path.join(os.path.dirname(file_path), "Processed_Files")
            os.makedirs(folder_name, exist_ok=True)

            # Folder for received fragments
            received_folder = os.path.join(os.path.dirname(file_path), "Received_Fragments")
            os.makedirs(received_folder, exist_ok=True)

            with serial.Serial('COM5', 9600, timeout=1) as ser:
                for idx, chunk in enumerate(chunks):
                    command = mode.to_bytes(1, 'big')
                    size = len(chunk).to_bytes(1, 'big')
                    bcc = command[0] ^ size[0] ^ sum(chunk) % 256
                    packet = command + size + chunk + bytes([bcc])
                    ser.write(packet)

                    # Wait and read response
                    response = ser.read(len(chunk))  # Assuming STM returns the same chunk size
                    result_data.extend(response)  # Add the response to result_data

                    # Save each fragment separately to the 'Received_Fragments' folder
                    fragment_file = os.path.join(received_folder, f"fragment_{idx + 1}.bin")
                    with open(fragment_file, "wb") as fragment_out:
                        fragment_out.write(response)

            # After all fragments are received, save the complete file
            output_file = os.path.join(folder_name, os.path.basename(file_path) + (".enc" if mode == 1 else ".dec"))
            with open(output_file, "wb") as out_file:
                out_file.write(result_data)

            messagebox.showinfo("Success", f"File processed successfully. Output saved as {output_file}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def process_folder(self, folder_path, mode):
        try:
            # Create a new folder for saving processed files
            output_folder = os.path.join(folder_path, "Processed_Files")
            os.makedirs(output_folder, exist_ok=True)

            # Folder for received fragments
            received_folder = os.path.join(folder_path, "Received_Fragments")
            os.makedirs(received_folder, exist_ok=True)

            files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
            with serial.Serial('COM5', 9600, timeout=1) as ser:
                for file_path in files:
                    with open(file_path, "rb") as file:
                        data = file.read()
                        command = mode.to_bytes(1, 'big')
                        size = len(data).to_bytes(1, 'big')
                        bcc = command[0] ^ size[0] ^ sum(data) % 256
                        packet = command + size + data + bytes([bcc])
                        ser.write(packet)

                        # Wait and read response
                        response = ser.read(len(data))  # Assuming STM returns the same data size

                        # Save the processed data to the new folder
                        output_file = os.path.join(output_folder, os.path.basename(file_path) + (".enc" if mode == 1 else ".dec"))
                        with open(output_file, "wb") as out_file:
                            out_file.write(response)

                        # Save each fragment separately to the 'Received_Fragments' folder
                        fragment_file = os.path.join(received_folder, os.path.basename(file_path) + ".frag")
                        with open(fragment_file, "wb") as fragment_out:
                            fragment_out.write(response)

            messagebox.showinfo("Success", "Folder processed successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
