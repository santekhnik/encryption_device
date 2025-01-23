import serial
import serial.tools.list_ports


class UARTCommunication:
    def __init__(self, port, baudrate=9600, timeout=1):
        """
        Ініціалізація UART з параметрами.
        :param port: Назва COM-порту (наприклад, 'COM3').
        :param baudrate: Швидкість передачі даних.
        :param timeout: Час очікування для читання (в секундах).
        """
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.serial_connection = None

    def open_port(self):
        """Відкриває COM-порт."""
        try:
            self.serial_connection = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                timeout=self.timeout,
            )
            print(f"Порт {self.port} відкрито.")
        except serial.SerialException as e:
            print(f"Помилка відкриття порту: {e}")

    def close_port(self):
        """Закриває COM-порт."""
        if self.serial_connection and self.serial_connection.is_open:
            self.serial_connection.close()
            print(f"Порт {self.port} закрито.")

    def send_data(self, data):
        """
        Відправляє дані через UART.
        :param data: Дані для відправки (стрічка або байти).
        """
        if self.serial_connection and self.serial_connection.is_open:
            if isinstance(data, str):
                data = data.encode('utf-8')  # Перетворення в байти
            self.serial_connection.write(data)
            print(f"Дані відправлено: {data}")
        else:
            print("Порт не відкрито!")

    def receive_data(self):
        """
        Читає дані з UART.
        :return: Прочитані дані (байти).
        """
        if self.serial_connection and self.serial_connection.is_open:
            data = self.serial_connection.readline()  # Читає до символу кінця рядка
            print(f"Отримано дані: {data}")
            return data
        else:
            print("Порт не відкрито!")
            return None


def list_available_ports():
    """Виводить список доступних COM-портів."""
    ports = serial.tools.list_ports.comports()
    return [port.device for port in ports]


# Приклад використання
if __name__ == "__main__":
    # Список доступних портів
    available_ports = list_available_ports()
    print(f"Доступні порти: {available_ports}")

    if available_ports:
        uart = UARTCommunication(port=available_ports[0], baudrate=9600)
        uart.open_port()

        # Відправка даних
        uart.send_data("Hello UART!")

        # Прийом даних
        response = uart.receive_data()

        # Закриття порту
        uart.close_port()
    else:
        print("Немає доступних портів!")

