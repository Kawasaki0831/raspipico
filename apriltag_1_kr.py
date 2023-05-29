# Hello World Example
#
# Welcome to the OpenMV IDE! Click on the green run arrow button below to run the script!

import sensor, image, time, math
from pyb import I2C
import utime
import pyb, ustruct

sensor.reset()
#sensor.set_pixformat(sensor.RGB565)
sensor.set_pixformat(sensor.GRAYSCALE)
sensor.set_framesize(sensor.QQVGA) # we run out of memory if the resolution is much bigger...
sensor.skip_frames(time = 2000)
sensor.set_auto_gain(False)  # must turn this off to prevent image washout...
sensor.set_auto_whitebal(False)  # must turn this off to prevent image washout...
clock = time.clock()

bus = pyb.I2C(4, pyb.I2C.SLAVE, addr=0x12)
bus.deinit() # Fully reset I2C device...
bus = pyb.I2C(4, pyb.I2C.SLAVE, addr=0x12)
print("Waiting for raspberry pi")
print(bus)

tag_families = 0
tag_families |= image.TAG16H5 # comment out to disable this family
tag_families |= image.TAG25H7 # comment out to disable this family
tag_families |= image.TAG25H9 # comment out to disable this family
tag_families |= image.TAG36H10 # comment out to disable this family
tag_families |= image.TAG36H11 # comment out to disable this family (default family)
tag_families |= image.ARTOOLKIT # comment out to disable this family

cxDif = 0
mode = b'\x00'

def family_name(tag):
    if(tag.family() == image.TAG16H5):
        return "TAG16H5"
    if(tag.family() == image.TAG25H7):
        return "TAG25H7"
    if(tag.family() == image.TAG25H9):
        return "TAG25H9"
    if(tag.family() == image.TAG36H10):
        return "TAG36H10"
    if(tag.family() == image.TAG36H11):
        return "TAG36H11"
    if(tag.family() == image.ARTOOLKIT):
        return "ARTOOLKIT"

while(True):

    img = sensor.snapshot().lens_corr(1.8)

    try:

        mode = bus.recv(1,timeout=10000)
        print(mode)

        if (mode ==b'\x00') :
        #test = 1
            try:
                bus.send(ustruct.pack("<h", test), timeout=10000) # Send the len first (16-bits).
                print(ustruct.pack("<h", len(test)))
                try:
                    bus.send(test, timeout=10000) # Send the data second.
                    print("Sent Data!") # Only reached on no error.
                except OSError as err:
                    pass
            except OSError as err:
                pass

        if mode == b'\x01':
            print("circle")
            for c in img.find_circles(threshold = 3200,x_margin = 10, y_margin = 10,r_margin =10):
                img.draw_circle(c.x(),c.y(),c.r(),color = (255,0,0))

                text = "Detect Circle!\n"
                data = ustruct.pack("<%ds" % len(text), text)

                try:
                    bus.send(ustruct.pack("<h", len(data)), timeout=10000) # Send the len first (16-bits).
                    try:
                        bus.send(data, timeout=10000) # Send the data second.
                        print("Sent Data!") # Only reached on no error.
                    except OSError as err:
                        pass
                except OSError as err:
                    pass

        if mode == b'\x02':
            print("auto")
            for tag in img.find_apriltags(families=tag_families): # defaults to TAG36H11 without "families".
                img.draw_rectangle(tag.rect(), color = (255, 0, 0))
                img.draw_cross(tag.cx(), tag.cy(), color = (0, 255, 0))
                print_args = (family_name(tag), tag.id(), (180 * tag.rotation()) / math.pi)
                print("Tag Family %s, Tag ID %d, rotation %f (degrees)" % print_args)

                if tag.cx() > 80:
                    cxDif = tag.cx() - 80
                elif tag.cx() < 80:
                    cxDif = tag.cx() - 80
                else:
                    cxDif = 0

                print(f"rotation : {print_args[2]} (degrees)")
                print(f"cxDif : {cxDif}")
                print(f"tagName : {print_args[0]}")
                print(f"tagID : {tag.id()}")

                if print_args[0] == "TAG36H11":
                    text_start = f"{print_args[0]}\n"
                    data_start = ustruct.pack("<%ds" % len(text_start), text_start)
                    try:
                        bus.send(ustruct.pack("<h", len(data_start)), timeout=10000) # Send the len first (16-bits).
                        try:
                            bus.send(data_start, timeout=10000) # Send the data second.
                            print("Sent Start!") # Only reached on no error.
                        except OSError as err:
                            pass
                    except OSError as err:
                        pass


                elif print_args[0] == "TAG25H7":
                    text_goal = f"{print_args[0]}\n"
                    data_goal = ustruct.pack("<%ds" % len(text_goal), text_goal)
                    try:
                        bus.send(ustruct.pack("<h", len(data_goal)), timeout=10000) # Send the len first (16-bits).
                        try:
                            bus.send(data_goal, timeout=10000) # Send the data second.
                            print("Sent Goal!") # Only reached on no error.
                        except OSError as err:
                            pass
                    except OSError as err:
                        pass

                text_int_angle = str(print_args[2])
                text_angle = f"{text_int_angle}\n"
                data_angle = ustruct.pack("<%ds" % len(text_angle), text_angle)

                text_int_cordinate = str(cxDif)
                text_cordinate = f"{text_int_cordinate}\n"
                data_cordinate = ustruct.pack("<%ds" % len(text_cordinate), text_cordinate)

                try:
                    bus.send(ustruct.pack("<h", len(data_cordinate)), timeout=10000) # Send the len first (16-bits).
                    try:
                        bus.send(data_cordinate, timeout=10000) # Send the data second.
                        print("Sent Cordinate!") # Only reached on no error.
                    except OSError as err:
                        pass
                except OSError as err:
                    pass

                try:
                    bus.send(ustruct.pack("<h", len(data_angle)), timeout=10000)
                    try:
                        bus.send(data_angle, timeout=10000)
                        print("Sent Angle!") # Only reached on no error.
                    except OSError as err:
                        pass
                except OSError as err:
                    pass
    except OSError as err:
        pass
