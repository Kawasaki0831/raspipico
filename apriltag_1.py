import sensor, image, time, math
from pyb import LED
from pyb import Pin

led_r = LED(1)
led_g = LED(2)
led_b = LED(3)

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QQVGA) # we run out of memory if the resolution is much bigger...
sensor.skip_frames(time = 2000)
sensor.set_auto_gain(False)  # must turn this off to prevent image washout...
sensor.set_auto_whitebal(False)  # must turn this off to prevent image washout...
clock = time.clock()

f_x = (2.8 / 3.984) * 160 # find_apriltags defaults to this if not set
f_y = (2.8 / 2.952) * 120 # find_apriltags defaults to this if not set
c_x = 160 * 0.5 # find_apriltags defaults to this if not set (the image.w * 0.5)
c_y = 120 * 0.5 # find_apriltags defaults to this if not set (the image.h * 0.5)

def light_red():
    led_r.on()
    led_g.off()
    led_b.off()

def light_green():
    led_r.off()
    led_g.on()
    led_b.off()

def light_white():
    led_r.on()
    led_g.on()
    led_b.on()

def light_off():
    led_r.off()
    led_g.off()
    led_b.off()

pin_out_right = Pin('P0', Pin.OUT_PP)
pin_out_left  = Pin('P1', Pin.OUT_PP)

while(True):
    clock.tick()
    img = sensor.snapshot()
    num_of_tag = 0

    for tag in img.find_apriltags(fx=f_x, fy=f_y, cx=c_x, cy=c_y): # defaults to TAG36H11
        num_of_tag = num_of_tag + 1
        img.draw_rectangle(tag.rect(), color = (255, 0, 0))
        img.draw_cross(tag.cx(), tag.cy(), color = (0, 255, 0))
        position = (tag.x_translation(), tag.y_translation(), -tag.z_translation())
        print("x: %f, y %f, z %f" % position)
        x = tag.x_translation()
        if (x > 0.5):
            light_red()
            pin_out_right.low()
            pin_out_left.high()
        elif (x > -0.5):
            light_white()
            pin_out_right.high()
            pin_out_left.high()
        else:
            light_green()
            pin_out_right.high()
            pin_out_left.low()

    if num_of_tag == 0:
        light_off()
        pin_out_right.high()
        pin_out_left.high()
