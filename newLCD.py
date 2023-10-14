import RPi.GPIO as GPIO
import time
import drivers
from time import sleep, strftime


# Define the GPIO pins for the keypad rows and columns
rows = [19, 26, 16, 20, 12]  # GPIO 19, 26, 16, 20
cols = [21, 13, 6, 5]  # GPIO 21, 13, 6, 5, 12
cursor = 0
input_text = ""

# Define the keypad matrix

keys = [
    ['F1', 'F2', '=', '*'],
    ['1', '2', '3', 'Up'],
    ['4', '5', '6', 'Down'],
    ['7', '8', '9', 'Esc'],
    ['+', '0', '-', 'Enter']
]



# Setup GPIO mode and initial state
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)



# Setup row pins as outputs and set them to high
for row in rows:
    GPIO.setup(row, GPIO.OUT)
    GPIO.output(row, GPIO.HIGH)



# Setup column pins as inputs with pull-up resistors
for col in cols:
    GPIO.setup(col, GPIO.IN, pull_up_down=GPIO.PUD_UP)



# Function to read the keypad

def read_keypad():
    key = None
    # Scan rows
    for i, row in enumerate(rows):
        GPIO.output(row, GPIO.LOW)
        # Check column inputs
        for j, col in enumerate(cols):
            if GPIO.input(col) == GPIO.LOW:
                key = keys[i][j]
                time.sleep(0.1)  # Debounce delay
        GPIO.output(row, GPIO.HIGH)
    return key

lcdDisplay = drivers.Lcd()
lcdDisplay.lcd_clear()

def calculate(txt):
    txt2 = txt.replace("=","")
    nums = txt2.split('+')
    nums = list(map(int, nums))
    sum = 0
    print(txt2)
    for x in nums:
        sum += x
    print(sum)
    return sum

# Main loop

try:
    lcdDisplay.lcd_backlight(0)
    # while True:
    #     pressed_key = read_keypad()
    #     if pressed_key is not None:
    #         input_text += str(pressed_key)
    #         print("Pressed key:", pressed_key)
    #         lcdDisplay.lcd_display_string(input_text,1)
    #         if pressed_key == 'F1':
    #             lcdDisplay.lcd_clear()
    #             input_text = ""
    #         if pressed_key == '=':
    #             lcdDisplay.lcd_clear()
    #             input_text =  str(calculate(input_text))
    #             lcdDisplay.lcd_display_string(input_text,1)
    #         else:
    #             lcdDisplay.lcd_display_string(input_text,1)
    #         time.sleep(0.3)  # Delay between scans
except KeyboardInterrupt:
    pass

finally:
    GPIO.cleanup()









