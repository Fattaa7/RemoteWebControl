import boto3
import vlc
import RPi.GPIO as GPIO
import time
import drivers
import threading
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


# AWS S3 Configuration
aws_access_key_id = "AKIASTCUAEMDIYODMZG4"
aws_secret_access_key = "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"
aws_s3_bucket = "late-start"

# Initialize S3 client
s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

# List objects in the S3 bucket
response = s3.list_objects_v2(Bucket=aws_s3_bucket)

# Create a list to store object keys
object_keys = [obj['Key'] for obj in response.get('Contents', [])]

# Initialize VLC media player
p = vlc.MediaPlayer()
current_audio_index = 0
audio_thread = None

# Function to play the current audio
def play_current_audio(index):
    if 0 <= index < len(object_keys):
        url = s3.generate_presigned_url('get_object', Params={'Bucket': aws_s3_bucket, 'Key': object_keys[index]})
        p.set_mrl(url)
        p.play()
        lcdDisplay.lcd_clear()
        str = object_keys[index][:-4]
        str1 = str[:16]
        lcdDisplay.lcd_display_string(str1,1)
        str2 = str[16:]
        if len(str2) > 1:
            lcdDisplay.lcd_display_string(str2,2)

# Play the initial audio
#play_current_audio(current_audio_index)

def audio_thread_function():
    play_current_audio(current_audio_index)


# Function to play the previous audio
def previous_audio():
    global current_audio_index
    if current_audio_index > 0:
        current_audio_index -= 1
        p.stop()
        play_current_audio(current_audio_index)

# Function to play the next audio
def next_audio():
    global current_audio_index
    if current_audio_index < len(object_keys) - 1:
        current_audio_index += 1
        p.stop()
        play_current_audio(current_audio_index)

# Function to pause or resume playback
def pause_audio():
    if p.is_playing() == 1:
        p.pause()
        print("Paused")
    else:
        p.play()
        print("Resumed")

play_current_audio()

while True:
    pressed_key = read_keypad()
    if pressed_key is not None:
        print("Pressed key:", pressed_key)
        if pressed_key == '-':
            previous_audio()
        if pressed_key == '+':
            next_audio()
        if pressed_key == '0':
            pause_audio()
    time.sleep(0.3)  # Delay between scans

