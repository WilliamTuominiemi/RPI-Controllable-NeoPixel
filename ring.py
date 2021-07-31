from RPi import GPIO
from time import sleep

import time
import board
import neopixel

GPIO.setmode(GPIO.BCM)

# Configure neopixel

pixel_pin = board.D18

num_pixels = 24

ORDER = neopixel.GRB

pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=1, auto_write=False, pixel_order=ORDER
)

brightness = 0.5
step = 0.05

# Configure rotary

counter = 0

clk = 17
dt = 27

GPIO.setup(clk, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(dt, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

clkLastState = GPIO.input(clk)


def wheel(pos):
    if pos < 0 or pos > 255:
        r = g = b = 0
    elif pos < 85:
        r = int(pos * 3)
        g = int(255 - pos * 3)
        b = 0
    elif pos < 170:
        pos -= 85
        r = int(255 - pos * 3)
        g = 0
        b = int(pos * 3)
    else:
        pos -= 170
        r = 0
        g = int(pos * 3)
        b = int(255 - pos * 3)
    return (r, g, b) if ORDER in (neopixel.RGB, neopixel.GRB) else (r, g, b, 0)


def rainbow_cycle(wait):
    for j in range(255):
        for i in range(num_pixels):
            pixel_index = (i * 256 // num_pixels) + j
            pixels[i] = wheel(pixel_index & 255)
        pixels.show()
        time.sleep(wait)


try:
    while True:
        clkState = GPIO.input(clk)
        dtState = GPIO.input(dt)
        if clkState != clkLastState:
            if dtState != clkState:
                if brightness < 1 - step:
                    brightness = brightness + step
                    print("+")
            else:
                if brightness > 0 + step:
                    brightness = brightness - step
                    print("-")

            colour = 255 * brightness
            print(colour)
            pixels.fill((0, 0, colour))
            pixels.show()
        clkLastState = clkState
        sleep(0.01)
finally:
    GPIO.cleanup()
