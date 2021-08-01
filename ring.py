from RPi import GPIO
from time import sleep

import time
import board
import neopixel

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# Configure neopixel

R = 0
G = 0
B = 255

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

# Configure keypad

L1 = 5
L2 = 6
L3 = 13
L4 = 19

C1 = 12
C2 = 16
C3 = 20
C4 = 21

GPIO.setup(L1, GPIO.OUT)
GPIO.setup(L2, GPIO.OUT)
GPIO.setup(L3, GPIO.OUT)
GPIO.setup(L4, GPIO.OUT)

GPIO.setup(C1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


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


def readLine(line, characters):
    global R, G, B

    GPIO.output(line, GPIO.HIGH)
    if(GPIO.input(C1) == 1):
        print(characters[0])
        R = 255
        G = 0
        B = 0
    if(GPIO.input(C2) == 1):
        print(characters[1])
    if(GPIO.input(C3) == 1):
        print(characters[2])
    if(GPIO.input(C4) == 1):
        print(characters[3])
    GPIO.output(line, GPIO.LOW)

    pixels.fill((R * brightness, G * brightness, B * brightness))
    pixels.show()


try:
    while True:
        # Keypad
        GPIO.output(L1, GPIO.HIGH)
        GPIO.output(L2, GPIO.HIGH)
        GPIO.output(L3, GPIO.HIGH)

        if(GPIO.input(C1) == 1):  # RED
            R = 255
            G = 0
            B = 0
        if(GPIO.input(C2) == 1):  # GREEN
            R = 0
            G = 255
            B = 0
        if(GPIO.input(C3) == 1):  # BLUE
            R = 0
            G = 0
            B = 255

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

        clkLastState = clkState

        pixels.fill((R * brightness, G * brightness, B * brightness))
        pixels.show()

        sleep(0.01)
finally:
    GPIO.cleanup()
