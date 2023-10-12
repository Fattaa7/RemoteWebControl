from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import RPi.GPIO as GPIO
import time
from RPi_GPIO_i2c_LCD import lcd
from time import sleep, strftime


service = Service(executable_path=r'/home/pi/Desktop/Web/RemoteWebControl/geckodriver')
driver = webdriver.Firefox(service=service)
driver.get('http://52.54.176.49:8080/')
driver.implicitly_wait(6)
driver.find_element(By.CLASS_NAME, "btn_action_pp").click()

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

lcdDisplay = lcd.HD44780(0x27)
lcdDisplay.clear()

def calculate(txt):
    txt2 = txt.replace("=","")
    nums = txt2.split('+')
    nums = list(map(int, nums))
    sum = 0
    print(txt2)
    for x in nums:
        sum += x
    return sum

# Main loop

try:
    while True:
        pressed_key = read_keypad()
        if pressed_key is not None:
            driver.find_element(By.CLASS_NAME, "btn_action_pp").click()
            input_text += str(pressed_key)
			#lcdDisplay.clear()
			#time.sleep(0.03)  # Delay between scans
            print("Pressed key:", pressed_key)
            lcdDisplay.set(input_text,1)
            if pressed_key == 'F1':
                lcdDisplay.clear()
                input_text = ""
                if pressed_key == '=':
                    lcdDisplay.clear()
                    input_text =  str(calculate(input_text))
                    lcdDisplay.set(input_text,1)
                else:
                    lcdDisplay.set(input_text,1)
            # Do something with the key
            # Add your code here
            time.sleep(0.3)  # Delay between scans
except KeyboardInterrupt:
    pass

finally:
    GPIO.cleanup()









