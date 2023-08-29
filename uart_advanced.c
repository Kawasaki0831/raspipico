 #include <stdio.h>
#include "pico/stdlib.h"
#include "hardware/uart.h" 
// #include "hardware/irq.h"  けした

/// \tag::uart_advanced[]p

#define UART_ID uart1
#define BAUD_RATE 115200
#define DATA_BITS 8
#define STOP_BITS 1
#define PARITY    UART_PARITY_NONE

#define UART_TX_PIN 4
#define UART_RX_PIN 5

#define BUFFER_SIZE 16

// uint8_t data;

char buffer[BUFFER_SIZE];
int buffer_index = 0;

//　処理ー３
void processReceivedData() {
    printf( "%s", buffer);
}

//　処理ー２
void receiveData(char c) {
    if (buffer_index < BUFFER_SIZE - 1) {
        buffer[buffer_index++] = c;
    }

    // 終了条件のチェック
    if (c == '\n') {
        buffer[buffer_index] = '\0';  // 文字列の終端にヌル文字を追加
        processReceivedData();  // 受信データの処理
        buffer_index = 0;  // バッファをリセット
    }
}

int main() {

    stdio_init_all();
    uart_init(UART_ID, BAUD_RATE);
    gpio_set_function(UART_TX_PIN, GPIO_FUNC_UART);
    gpio_set_function(UART_RX_PIN, GPIO_FUNC_UART);
    // int actual = uart_set_baudrate(UART_ID, BAUD_RATE);  けした
    uart_set_hw_flow(UART_ID, false, false);
    uart_set_format(UART_ID, DATA_BITS, STOP_BITS, PARITY);
    uart_set_fifo_enabled(UART_ID, false);  


      
    //　処理ー１
    while (1) {
        while (uart_is_readable(UART_ID)) {
            char c = uart_getc(UART_ID);
            receiveData(c);
        }
    }

    return 0;

}


/// \end:uart_advanced[]
