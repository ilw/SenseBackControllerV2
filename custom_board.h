/* Copyright (c) 2012 Nordic Semiconductor. All Rights Reserved.
 *
 * The information contained herein is property of Nordic Semiconductor ASA.
 * Terms and conditions of usage are described in detail in NORDIC
 * SEMICONDUCTOR STANDARD SOFTWARE LICENSE AGREEMENT.
 *
 * Licensees are granted free, non-transferable use of the information. NO
 * WARRANTY of ANY KIND is provided. This heading must NOT be removed from
 * the file.
 *
 */
#ifndef REDBEAR_NANO_H__
#define REDBEAR_NANO_H__

#define LED_ACTIVE_STATE 1
#define LEDS_NUMBER    1



#define LED_START  11
#define LED_1	   11
#define LED_STOP   11

#define BSP_LED_0  LED_1


#define BUTTONS_LIST {}
#define LEDS_LIST { BSP_LED_0 }

#define BSP_LED_0_MASK    (1<<BSP_LED_0)

// bsp.c assumes BSP_LED_1_MASK always exists
#define BSP_LED_1_MASK    (1<<BSP_LED_0)

#define LEDS_MASK      (BSP_LED_0_MASK)
#define LEDS_INV_MASK  LEDS_MASK

// there are no buttons on this board
#define BUTTONS_NUMBER 0
#define BUTTONS_MASK   0x00000000

// UART pins connected to J-Link
#define RX_PIN_NUMBER  30
#define TX_PIN_NUMBER  29
#define CTS_PIN_NUMBER 28
#define RTS_PIN_NUMBER 2
#define HWFC           true

#endif /* REDBEAR_NANO_H__ */
