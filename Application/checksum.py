def calculate_bcc(data):
    """
    Обчислює BCC (Block Check Character) для заданого блоку даних.

    :param data: Масив байтів (наприклад, b'123' або [0x31, 0x32, 0x33])
    :return: Однобайтове значення BCC
    """
    bcc = 0x00  # Початкове значення CRC
    for byte in data:
        bcc ^= byte  # Виконуємо XOR з кожним байтом
    return bcc


test_data = b'\x12\x34\x56\x78'
checksum = calculate_bcc(test_data)
print(f'Data: {test_data}')
print(f'BCC Checksum: 0x{checksum:02X}')

