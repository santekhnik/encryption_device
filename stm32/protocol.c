#include <stdint.h>
#include <string.h>

// Максимальний розмір даних
#define MAX_DATA_SIZE 256

// Команди
#define CMD_ENCRYPT 0x01
#define CMD_DECRYPT 0x02
#define CMD_ERROR   0xFF

// Структура пакету
typedef struct {
    uint8_t command;  // Ідентифікатор команди
    uint8_t size;     // Розмір даних
    uint8_t data[MAX_DATA_SIZE]; // Дані
    uint8_t bcc;      // Контрольна сума
} Packet;

// Функція для обчислення BCC
uint8_t calculate_bcc(const uint8_t *data, uint8_t length) {
    uint8_t bcc = 0;
    for (uint8_t i = 0; i < length; i++) {
        bcc ^= data[i];
    }
    return bcc;
}

// Функція для шифрування
void encrypt_data(uint8_t *data, uint8_t size) {
    for (uint8_t i = 0; i < size; i++) {
        data[i] ^= 0xAA; // Просте XOR-шифрування
    }
}

// Функція для дешифрування
void decrypt_data(uint8_t *data, uint8_t size) {
    for (uint8_t i = 0; i < size; i++) {
        data[i] ^= 0xAA; // Просте XOR-дешифрування (зворотнє шифруванню)
    }
}

// Функція обробника
void handle_packet(const Packet *input, Packet *response) {
    // Перевірка BCC
    uint8_t calculated_bcc = calculate_bcc((uint8_t *)input, input->size + 2); // 2 байти: команда і розмір
    if (calculated_bcc != input->bcc) {
        // Некоректна контрольна сума
        response->command = CMD_ERROR;
        response->size = 0;
        response->bcc = CMD_ERROR;
        return;
    }

    // Обробка команди
    response->command = input->command;
    response->size = input->size;
    memcpy(response->data, input->data, input->size);

    switch (input->command) {
        case CMD_ENCRYPT:
            encrypt_data(response->data, response->size);
            break;
        case CMD_DECRYPT:
            decrypt_data(response->data, response->size);
            break;
        default:
            // Невідома команда
            response->command = CMD_ERROR;
            response->size = 0;
            response->bcc = CMD_ERROR;
            return;
    }

    // Обчислення BCC для відповіді
    response->bcc = calculate_bcc((uint8_t *)response, response->size + 2);
}

// Основна функція
int main() {
    // Вхідний пакет (приклад для тестування)
    Packet input = {CMD_ENCRYPT, 5, {0x89, 0x23, 0x7A, 0x56, 0x41}, 0x00};
    Packet response;

    // Розрахунок BCC для вхідного пакета
    input.bcc = calculate_bcc((uint8_t *)&input, input.size + 2);

    // Виклик обробника
    handle_packet(&input, &response);

    // Для відладки: перевірка результату
    for (uint8_t i = 0; i < response.size; i++) {
        // Наприклад, вивід даних у консоль або аналіз отриманого пакета
    }

    return 0;
}
