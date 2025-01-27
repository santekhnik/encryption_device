#include <stdio.h>

unsigned char calculate_bcc(const unsigned char* data, size_t length) {
  
    unsigned char bcc = 0x00; 
    for (size_t i = 0; i < length; i++) {
        bcc ^= data[i]; 
    }
    return bcc;
}

int main() {
    unsigned char test_data[] = { 0x12, 0x34, 0x56, 0x78 };
    size_t length = sizeof(test_data) / sizeof(test_data[0]);

    unsigned char checksum = calculate_bcc(test_data, length);

    printf("Data: ");
    for (size_t i = 0; i < length; i++) {
        printf("0x%02X ", test_data[i]);
    }
    printf("\nBCC Checksum: 0x%02X\n", checksum);

    return 0;
}
