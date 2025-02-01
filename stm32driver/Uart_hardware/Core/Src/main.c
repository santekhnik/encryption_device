#include "stm32f0xx.h"
#include "stm32f0xx_hal.h"
#include <string.h>

#define UART_BUFFER_SIZE 258
#define XOR_KEY 0x5A

volatile uint8_t uart_buffer[UART_BUFFER_SIZE];  
volatile uint16_t uart_buffer_index = 0; 
volatile uint8_t command = 0;
UART_HandleTypeDef huart2;

void SystemClock_Config(void);
void Error_Handler(void);
extern void UART_Init(void);

static uint8_t data_sent_flag = 0;

uint8_t calculate_checksum(uint8_t *data, int length) {
    uint8_t checksum = data[0];
    for (int i = 1; i < length; i++) {
        checksum ^= data[i];
    }
    return checksum;
}

void xor_encrypt_decrypt(uint8_t *data, int length, uint8_t key) {
    for (int i = 0; i < length; i++) {
        data[i] ^= key;
    }
}

void encrypt_uart_data() {
    uint8_t encrypted_buffer[UART_BUFFER_SIZE];
    memcpy(encrypted_buffer, (uint8_t *)uart_buffer, UART_BUFFER_SIZE);  // ???????? ???? ????? ? ?????
    xor_encrypt_decrypt(encrypted_buffer + 2, UART_BUFFER_SIZE - 2, XOR_KEY);  // ???????? ? 2-?? ?????
    encrypted_buffer[1] = calculate_checksum(encrypted_buffer, UART_BUFFER_SIZE);  // ????????? ?????????? ????
    HAL_UART_Transmit(&huart2, encrypted_buffer, UART_BUFFER_SIZE, HAL_MAX_DELAY);  // ?????????
}

void decrypt_uart_data() {
    uint8_t decrypted_buffer[UART_BUFFER_SIZE];
    memcpy(decrypted_buffer, (uint8_t *)uart_buffer, UART_BUFFER_SIZE);  // ???????? ???? ????? ? ?????
    xor_encrypt_decrypt(decrypted_buffer + 2, UART_BUFFER_SIZE - 2, XOR_KEY);  // ?????????? ? 2-?? ?????
    decrypted_buffer[1] = calculate_checksum(decrypted_buffer, UART_BUFFER_SIZE);  // ????????? ?????????? ????
    HAL_UART_Transmit(&huart2, decrypted_buffer, UART_BUFFER_SIZE, HAL_MAX_DELAY);  // ?????????
}

int main(void) {
    HAL_Init();
    SystemClock_Config();
    UART_Init();
    HAL_UART_Receive_IT(&huart2, (uint8_t *)uart_buffer, UART_BUFFER_SIZE);  // ?????? ????? ???????????

    while (1) {
        if (uart_buffer_index > 0) {
            command = uart_buffer[0];
            if (command == 0x45) {
                encrypt_uart_data();  // ??????????
            } else if (command == 0x44) {
                decrypt_uart_data();  // ????????????
            }
            uart_buffer_index = 0;  // ???????? ??????
        }
    }
}

void USART2_IRQHandler(void) {
    if (__HAL_UART_GET_IT_SOURCE(&huart2, UART_IT_RXNE)) {
        uint8_t received_byte = (uint8_t)(huart2.Instance->RDR & 0xFF);
        
        if (uart_buffer_index < UART_BUFFER_SIZE) {
            uart_buffer[uart_buffer_index++] = received_byte;
        } else {
            uart_buffer_index = 0;  // ???????? ????? ??? ????????????
        }
        
        __HAL_UART_CLEAR_FLAG(&huart2, UART_FLAG_RXNE);
    }
}

void SystemClock_Config(void) {
    RCC->CR |= RCC_CR_HSION;
    while ((RCC->CR & RCC_CR_HSIRDY) == 0);
    
    RCC->CFGR &= ~RCC_CFGR_SW;
    RCC->CFGR |= RCC_CFGR_SW_HSI;
    while ((RCC->CFGR & RCC_CFGR_SWS) != RCC_CFGR_SWS_HSI);
}

void Error_Handler(void) {
    while (1) {}
}
