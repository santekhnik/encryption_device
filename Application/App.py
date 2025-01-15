from PyQt5.QtWidgets import QApplication, QMainWindow
import sys

app = QApplication(sys.argv)
window = QMainWindow()
window.setWindowTitle("Test Decryptor")
window.setGeometry(600, 100, 600, 800)
window.show()
sys.exit(app.exec_())
