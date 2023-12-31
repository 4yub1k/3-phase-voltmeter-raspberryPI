################################
#   Author: Salah Ud Din       #
#   GitHUb: @4yub1k            #
################################

# Main.py file generated by New Project wizard

# Created:   Sun Aug 20 2023
# Processor: RPI3
# Compiler:  Python 3 (Proteus)

# Modules
from goto import *
import time
import var
import pio
import resource

# Peripheral Configuration Code (do not edit)
# ---CONFIG_BEGIN---
import cpu
import FileStore
import VFP


def peripheral_setup():
    # Peripheral Constructors
    pio.cpu = cpu.CPU()
    pio.storage = FileStore.FileStore()
    pio.server = VFP.VfpServer()
    pio.storage.begin()
    pio.server.begin(0)


# Install interrupt handlers


def peripheral_loop():
    pio.server.poll()


# ---CONFIG_END---
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

rs, en, d4, d5, d6, d7 = 5, 6, 12, 13, 16, 19
pins_list = [rs, en, d4, d5, d6, d7]

commands_list = {
    # wait for 20ms, LCD ON wait more than 15ms.
    0x02: 20/1e3,      # 4bit mode
    0x28: 37/1e6,      # Initialization of 16X2 LCD in 4bit mode 
    0x0C: 37/1e6,      # Display ON Cursor OFF
    0x06: 37/1e6,      # Auto Increment cursor 
    0x01: 37/1e6,      # Clear display
    0x80: 37/1e6       # Cursor at home position
}

# STEP # 1, Setup Output pins
for pin in pins_list:
    GPIO.setup(pin, GPIO.OUT)
# STEP # 2,
GPIO.output(rs, 0)  # RS pin, 0 or False

# # Select the row.
# row_1 = 0x80  # LCD RAM address for the 1st line
# row_2 = 0xC0

def lcd(byte):
    high_bits = byte >> 4       # High nibbles
    low_bits = byte & 0x0F    # Low nibbles

    # STEP # 3, Send high bits
    for bit, pin in enumerate(pins_list[2:]):    # [0 , 0, 1, 1] , [d4, d5, d6, d7]
        if high_bits >> bit & 0x1:
            GPIO.output(pin, True)
        else:
            GPIO.output(pin, False)

    # STEP # 4, Toggle EN.
    # 37us
    GPIO.output(en, True)
    time.sleep(37/1e6)
    GPIO.output(en, False)
    time.sleep(37/1e6)

    # STEP # 5, Send low bits
    for bit, pin in enumerate(pins_list[2:]):    # [0 , 0, 1, 1] , [d4, d5, d6, d7]
        if low_bits >> bit & 0x1:
            GPIO.output(pin, True)
        else:
            GPIO.output(pin, False)

    # STEP # 6, Toggle EN.
    # 37us
    GPIO.output(en, True)
    time.sleep(37/1e6)
    GPIO.output(en, False)
    time.sleep(37/1e6)

lcd(0x02)
# STEP # 7, Wait after sending new command.
time.sleep(37/1e6)
lcd(0x28)
time.sleep(37/1e6)
lcd(0x0C)
time.sleep(37/1e6)
lcd(0x06)
time.sleep(37/1e6)
lcd(0x01)
time.sleep(37/1e6)

# STEP # 8, for writing data, above commands are also required to initialize LCD
GPIO.output(rs, 1)  # RS pin, 1 or True

while True:
   lcd(ord("a")) # send "a" to LCD
   time.sleep(1)