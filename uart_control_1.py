# UART Control
#
# This example shows how to use the serial port on your OpenMV Cam. Attach pin
# P4 to the serial input of a serial LCD screen to see "Hello World!" printed
# on the serial LCD display.

import sensor, image, time, math
import utime
import pyb, ustruct
import time


from pyb import UART
import ustruct


uart = UART(1, 115200, timeout_char=1000)
# init with given baudrate
uart.init(115200, bits=8, parity=None, stop=2, timeout_char=1000)
# init with given parameters




sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_pixformat(sensor.GRAYSCALE)
sensor.set_framesize(sensor.QQVGA) # we run out of memory if the resolution is much bigger...
sensor.skip_frames(time = 2000)
sensor.set_auto_gain(False)  # must turn this off to prevent image washout...
sensor.set_auto_whitebal(False)  # must turn this off to prevent image washout...
clock = time.clock()


tag_families = 0
tag_families |= image.TAG36H11

# Always pass UART 3 for the UART number for your OpenMV Cam.
# The second argument is the UART baud rate. For a more advanced UART control
# example see the BLE-Shield driver.



f_x = (2.8 / 3.984) * 160 # find_apriltags defaults to this if not set
f_y = (2.8 / 2.952) * 120 # find_apriltags defaults to this if not set
c_x = 160 * 0.5 # find_apriltags defaults to this if not set (the image.w * 0.5)
c_y = 120 * 0.5 # find_apriltags defaults to this if not set (the image.h * 0.5)

def degrees(radians):
    return (180 * radians) / math.pi


def family_name(tag):
    if(tag.family() == image.TAG36H11):
        return "TAG36H11"



while(True):
    #uart.write("Hello World!\r")
    #time.sleep_ms(1000)


    img = sensor.snapshot().lens_corr(1.8)
    for tag in img.find_apriltags(families=tag_families): # defaults to TAG36H11 without "families".
                img.draw_rectangle(tag.rect(), color = (255, 0, 0))
                img.draw_cross(tag.cx(), tag.cy(), color = (0, 255, 0))
                print_args = (family_name(tag), tag.id(), (180 * tag.rotation()) / math.pi)


                #position = (tag.x_translation(), tag.y_translation(), -tag.z_translation())
                #print("x: %f, y: %f, z: %f"% position)
                #x = tag.x_translation()

                #print(tag.id())

                uart.writechar(ustruct.pack((tag.id()))
