#include "stm32f0xx.h"
#include "stm32f0xx_hal.h"

#define UART_BUFFER_SIZE 256
volatile uint8_t uart_buffer[UART_BUFFER_SIZE];  
volatile uint16_t uart_buffer_index = 0;         
UART_HandleTypeDef huart2;

void SystemClock_Config(void);
void Error_Handler(void);
void UART_Init(void);


int main(void)
{
    HAL_Init();
    SystemClock_Config();
    UART_Init();
    HAL_UART_Receive_IT(&huart2, (uint8_t *)uart_buffer, UART_BUFFER_SIZE);


    while (1)
    {
     
        if (uart_buffer_index > 0) {
       
            for (int i = 0; i < uart_buffer_index; i++) {
                // ??????? ????? ???? ??? ?????????
               HAL_UART_Transmit(&huart2, (const uint8_t *) &uart_buffer[i], 1, HAL_MAX_DELAY);
            }

            
            if (uart_buffer[uart_buffer_index - 1] == '\r') {
                uart_buffer[uart_buffer_index - 1] = '\0'; 
            }

            uart_buffer_index = 0;
        }
    }
}
static uint8_t data_sent_flag = 0;

void USART2_IRQHandler(void)
{
    
    if (__HAL_UART_GET_IT_SOURCE(&huart2, UART_IT_RXNE)) {
        uint8_t received_byte = (uint8_t)(huart2.Instance->RDR & 0xFF); 

        
        if (uart_buffer_index < UART_BUFFER_SIZE - 1) {
            uart_buffer[uart_buffer_index++] = received_byte;

            
            if (received_byte == '\n') {
                uart_buffer[uart_buffer_index] = '\0'; 

                
                if (!data_sent_flag) {
                    
                    HAL_UART_Transmit(&huart2, (const uint8_t *) uart_buffer, uart_buffer_index, HAL_MAX_DELAY);

                    
                    data_sent_flag = 1;
                }

               
                uart_buffer_index = 0;
            }
        } else {
           
            uart_buffer_index = 0;
        }

        
        __HAL_UART_CLEAR_FLAG(&huart2, UART_FLAG_RXNE);
    }
}

// ??????? ??? ???????? ????? ????? ????????
void reset_data_sent_flag(void) {
    data_sent_flag = 0;
}


void UART_Init(void)
{
    __HAL_RCC_GPIOA_CLK_ENABLE();   // ????????? ?????????? GPIOA
    __HAL_RCC_USART2_CLK_ENABLE();  // ????????? ?????????? USART2

    // ???????????? ????? PA2 ? PA3 ??? USART2
    GPIO_InitTypeDef GPIO_InitStruct = {0};
    GPIO_InitStruct.Pin = GPIO_PIN_2 | GPIO_PIN_3;
    GPIO_InitStruct.Mode = GPIO_MODE_AF_PP;
    GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_HIGH;
    HAL_GPIO_Init(GPIOA, &GPIO_InitStruct);

    // ???????????? USART2
    huart2.Instance = USART2;
    huart2.Init.BaudRate = 9600;
    huart2.Init.WordLength = UART_WORDLENGTH_8B;
    huart2.Init.StopBits = UART_STOPBITS_1;
    huart2.Init.Parity = UART_PARITY_NONE;
    huart2.Init.HwFlowCtl = UART_HWCONTROL_NONE;
    huart2.Init.Mode = UART_MODE_TX_RX;
    HAL_UART_Init(&huart2);

    // ????????? ??????????? ??? UART
    __HAL_UART_ENABLE_IT(&huart2, UART_IT_RXNE);
    HAL_NVIC_SetPriority(USART2_IRQn, 0, 0);
    HAL_NVIC_EnableIRQ(USART2_IRQn);
}

void SystemClock_Config(void)
{
    // ???????????? HSI ?? ??????? ??????????
    RCC->CR |= RCC_CR_HSION;
    while ((RCC->CR & RCC_CR_HSIRDY) == 0); // ??????? ?? ?????????? HSI

    // ???????????? HSI ?? ??????? ?????????? ?????
    RCC->CFGR &= ~RCC_CFGR_SW;
    RCC->CFGR |= RCC_CFGR_SW_HSI;
    while ((RCC->CFGR & RCC_CFGR_SWS) != RCC_CFGR_SWS_HSI); // ??????? ?? ??????????? ?? HSI
}

void Error_Handler(void)
{
    // ??? ???? ??? ??????? ???????
    while (1)
    {
    }
}
