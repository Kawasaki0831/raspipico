//  #include <stdio.h>
// #include "pico/stdlib.h"
// #include "hardware/uart.h" 
// // #include "hardware/irq.h"  けした

// /// \tag::uart_advanced[]p

// #define UART_ID uart1
// #define BAUD_RATE 115200
// #define DATA_BITS 8
// #define STOP_BITS 1
// #define PARITY    UART_PARITY_NONE

// #define UART_TX_PIN 4
// #define UART_RX_PIN 5

// #define BUFFER_SIZE 16

// // uint8_t data;

// char buffer[BUFFER_SIZE];
// int buffer_index = 0;

// //　処理ー３
// void processReceivedData() {
//     printf( "%s", buffer);
// }

// //　処理ー２
// void receiveData(char c) {
//     if (buffer_index < BUFFER_SIZE - 1) {
//         buffer[buffer_index++] = c;
//     }

//     // 終了条件のチェック
//     if (c == '\n') {
//         buffer[buffer_index] = '\0';  // 文字列の終端にヌル文字を追加
//         processReceivedData();  // 受信データの処理
//         buffer_index = 0;  // バッファをリセット
//     }
// }

// int main() {

//     stdio_init_all();
//     uart_init(UART_ID, BAUD_RATE);
//     gpio_set_function(UART_TX_PIN, GPIO_FUNC_UART);
//     gpio_set_function(UART_RX_PIN, GPIO_FUNC_UART);
//     // int actual = uart_set_baudrate(UART_ID, BAUD_RATE);  けした
//     uart_set_hw_flow(UART_ID, false, false);
//     uart_set_format(UART_ID, DATA_BITS, STOP_BITS, PARITY);
//     uart_set_fifo_enabled(UART_ID, false);  
          
//     //　処理ー１
//     while (1) {
//         while (uart_is_readable(UART_ID)) {
//             char c = uart_getc(UART_ID);
//             receiveData(c);
//         }
//     }
//     return 0;
// }

/// \end:uart_advanced[]















//  #include <stdio.h>
// #include "pico/stdlib.h"
// #include "hardware/uart.h" 
// // #include "hardware/irq.h"  けした

// /// \tag::uart_advanced[]p

// #define UART_ID uart1
// #define BAUD_RATE 115200
// #define DATA_BITS 8
// #define STOP_BITS 1
// #define PARITY    UART_PARITY_NONE

// #define UART_TX_PIN 4
// #define UART_RX_PIN 5

// #define BUFFER_SIZE 16

// // uint8_t data;

// uint8_t buffer[BUFFER_SIZE];
// int buffer_index = 0;

// //　処理ー３
// void processReceivedData() {
//     if (buffer_index == BUFFER_SIZE){
//         int x_zure = buffer[0];
//         int theta_left = buffer[1];
//         printf("zure = %f, angle = %f \n" , x_zure, theta_left);
//     }
// }

// //　処理ー２
// void receiveData(uint8_t c) {
//     if (buffer_index < BUFFER_SIZE) {
//         buffer[buffer_index++] = c;
//     }

//     // 終了条件のチェック
//     if (buffer_index == BUFFER_SIZE) {
//         processReceivedData();  // 受信データの処理
//         buffer_index = 0;  // バッファをリセット
//     }
// }

// int main() {

//     stdio_init_all();
//     uart_init(UART_ID, BAUD_RATE);
//     gpio_set_function(UART_TX_PIN, GPIO_FUNC_UART);
//     gpio_set_function(UART_RX_PIN, GPIO_FUNC_UART);
//     // int actual = uart_set_baudrate(UART_ID, BAUD_RATE);  けした
//     uart_set_hw_flow(UART_ID, false, false);
//     uart_set_format(UART_ID, DATA_BITS, STOP_BITS, PARITY);
//     uart_set_fifo_enabled(UART_ID, false);  
          
//     //　処理ー１
//     while (1) {
//         while (uart_is_readable(UART_ID)) {
//             uint8_t c = uart_getc(UART_ID);
//             receiveData(c);
//         }
//     }
//     return 0;
// }

// /// \end:uart_advanced[]


#include <stdio.h>
#include "pico/stdlib.h"
#include "hardware/uart.h"

// UART設定
#define UART_ID uart0
#define BAUD_RATE 115200
#define UART_TX_PIN 0
#define UART_RX_PIN 1

// 構造体定義：直線の情報
typedef struct {
    float x1;
    float y1;
    float x2;
    float y2;
} LineInfo;

int main() {
    stdio_init_all();

    // UART初期化
    uart_init(UART_ID, BAUD_RATE);
    gpio_set_function(UART_TX_PIN, GPIO_FUNC_UART);
    gpio_set_function(UART_RX_PIN, GPIO_FUNC_UART);
    uart_set_hw_flow(UART_ID, false, false);
    uart_set_format(UART_ID, 8, 1, UART_PARITY_NONE);
    uart_set_fifo_enabled(UART_ID, false);

    while (true) {
        // データを受信
        LineInfo line_info;
        if (uart_is_readable(UART_ID)) {
            size_t bytes_read = uart_read_blocking(UART_ID, (uint8_t *)&line_info, sizeof(LineInfo));

            if (bytes_read == sizeof(LineInfo)) {
                // データが正常に受信された場合の処理
                printf("直線の情報: x1=%f, y1=%f, x2=%f, y2=%f\n", line_info.x1, line_info.y1, line_info.x2, line_info.y2);
            }
        }
    }

    return 0;
}
