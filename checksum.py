def calculate_bcc(data: bytes) -> int:
    checksum = 0
    for byte in data:
        checksum = (checksum + byte) % 256
    return checksum

if __name__ == '__main__':
    test_data = b'\x12\x34\x56\x78'
    checksum = calculate_bcc(test_data)
    print(f'Data: {test_data}')
    print(f'BCC Checksum: 0x{checksum:02X}')

    # Додати коментарі