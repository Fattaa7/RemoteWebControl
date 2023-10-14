import RPi.GPIO as GPIO
import time
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
    ['-', '0', '+', 'Enter']
]



def init():


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

