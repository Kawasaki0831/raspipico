# Hello World Example
#
# Welcome to the OpenMV IDE! Click on the green run arrow button below to run the script!

import sensor, image, time, math

import pyb, ustruct

from pyb import LED
from pyb import Pin


red_led = LED(1)
green_led = LED(2)
blue_led = LED(3)
ir_leds = LED(4)


bus = pyb.I2C(4, pyb.I2C.SLAVE, addr=0x12)
bus.deinit() # Fully reset I2C device...
bus = pyb.I2C(4, pyb.I2C.SLAVE, addr=0x12)
print("Waiting for raspberry pi")
print(bus)



sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QQVGA) # we run out of memory if the resolution is much bigger...
sensor.skip_frames(time = 2000)
sensor.set_auto_gain(False)  # must turn this off to prevent image washout...
sensor.set_auto_whitebal(False)  # must turn this off to prevent image washout...
clock = time.clock()

tag_families = 0
tag_families |= image.TAG36H11

# Note! Unlike find_qrcodes the find_apriltags method does not need lens correction on the image to work.

# What's the difference between tag families? Well, for example, the TAG16H5 family is effectively
# a 4x4 square tag. So, this means it can be seen at a longer distance than a TAG36H11 tag which
# is a 6x6 square tag. However, the lower H value (H5 versus H11) means that the false positve
# rate for the 4x4 tag is much, much, much, higher than the 6x6 tag. So, unless you have a
# reason to use the other tags families just use TAG36H11 which is the default family.

# The AprilTags library outputs the pose information for tags. This is the x/y/z translation and
# x/y/z rotation. The x/y/z rotation is in radians and can be converted to degrees. As for
# translation the units are dimensionless and you must apply a conversion function.

# f_x is the x focal length of the camera. It should be equal to the lens focal length in mm
# divided by the x sensor size in mm times the number of pixels in the image.
# The below values are for the OV7725 camera with a 2.8 mm lens.

# f_y is the y focal length of the camera. It should be equal to the lens focal length in mm
# divided by the y sensor size in mm times the number of pixels in the image.
# The below values are for the OV7725 camera with a 2.8 mm lens.

# c_x is the image x center position in pixels.
# c_y is the image y center position in pixels.

f_x = (2.8 / 3.984) * 160 # find_apriltags defaults to this if not set
f_y = (2.8 / 2.952) * 120 # find_apriltags defaults to this if not set
c_x = 160 * 0.5 # find_apriltags defaults to this if not set (the image.w * 0.5)
c_y = 120 * 0.5 # find_apriltags defaults to this if not set (the image.h * 0.5)

def degrees(radians):
    return (180 * radians) / math.pi

def family_name(tag):
    if(tag.family() == image.TAG36H11):
        return "TAG36H11"


def light_red():
    red_led.on()
    green_led.off()
    blue_led.off()

def light_green():
    red_led.off()
    green_led.on()
    blue_led.off()

def light_blue():
    red_led.off()
    green_led.off()
    blue_led.on()

def light_off():
    red_led.off()
    green_led.off()
    blue_led.off()

pin_out_right = Pin('P0', Pin.OUT_PP)
pin_out_left = Pin('P1', Pin.OUT_PP)


while(True):
    clock.tick()


    num_of_tag = 0


    img = sensor.snapshot().lens_corr(1.8)
    for tag in img.find_apriltags(families=tag_families): # defaults to TAG36H11 without "families".
                img.draw_rectangle(tag.rect(), color = (255, 0, 0))
                img.draw_cross(tag.cx(), tag.cy(), color = (0, 255, 0))
                print_args = (family_name(tag), tag.id(), (180 * tag.rotation()) / math.pi)


                position = (tag.x_translation(), tag.y_translation(), -tag.z_translation())
                print("x: %f, y: %f, z: %f"% position)
                x = tag.x_translation()


                #if tag.cx() > 80:
                 #   cxDif = tag.cx() - 80
                #elif tag.cx() < 80:
                 #   cxDif = tag.cx() - 80
                #else:
                 #  cxDif = 0


                if(x>0.5):
                   light_red()
                   pin_out_right.low()
                   pin_out_left.high()
                elif (x>-0.5):
                   light_green()
                   pin_out_right.high()
                   pin_out_left.high()
                else:
                   light_blue()
                   pin_out_right.high()
                   pin_out_left.low()

                if num_of_tag == 0:
                   light_off()
                   pin_out_right.high()
                   pin_out_left.high()



                print(f"rotation : {print_args[2]} (degrees)")
                #print(f"cxDif : {cxDif}")
                print(f"tagName : {print_args[0]}")
                print(f"tagID : {tag.id()}")



                if tag.id()== 0:
                    text_start = f"{tag.id()}\n"
                    data_start = ustruct.pack("<%ds" % len(text_start), text_start)
                    try:
                        bus.send(ustract.pack(("<h", len(data_start)), text_start))
                        try:
                        bus.send(data_start, timeout=5000) #Send the len first (16-bits)
                            print("Sent Start!")
                        except OSError :
                            pass
                    except OSError :
                        pass



                elif tag.id()== 9:
                    text_goal = f"{tag.id()}\n"
                    data_goal = ustruct.pack("<%ds" % len(text_goal), text_start)
                    try:
                        bus.send(ustract.pack(("<h", len(data_goal)), text_start)
                        try:
                            bus.send(data_goal, timeout=5000)  # Send the len first (16-bits).
                            print("Sent Start!")
                        except OSError as err:
                            pass
                    except OSError as err:
                        pass

    for c in img.find_circles(threshold = 4500, x_margin = 50, y_margin = 50, r_margin = 50,
            r_min = 2, r_max = 100, r_step = 2):
            img.draw_circle(c.x(), c.y(), c.r(), color = (255, 0, 0))
            #print(c)

            #print("FPS %f" % clock.fps())
