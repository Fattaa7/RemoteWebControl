import RPi.GPIO as GPIO
from audioFuncs import AudioFuncs
from lcd import LCD
from datetime import datetime
from btnControl import Btn_Logic_Handler
from subprocess import check_output
from serverSetup import StorageSetup
from whatsUI import UI
import time
import os
import random
import playlistCreator
import shlex

MODE_MODE = 0
AUDIO_MODE = 5
DOWNLOADED_AUDIO_MODE = 10
LAST_PLAYED_MODE = 9
DEV_MODE = 22
CREATE_PLAYLIST_MODE = 54
CREATED_MODE = 99
CREATED_AUDIO_MODE = 77
TO_COPY_TO_MODE = 44
CREATE_MESSAGE_MODE = 3


class Main:
    def __init__(self):
        lcd = LCD()
        dataBase = StorageSetup()
        audioFuncs = AudioFuncs(lcd, dataBase)
        btnHandler = Btn_Logic_Handler(audioFuncs, dataBase, lcd)
        btnHandler.DevMode()

        while True:
            if btnHandler.flag != CREATE_PLAYLIST_MODE and btnHandler.flag != CREATE_MESSAGE_MODE:
                btnHandler.Toggle_swtich(None)
            time.sleep(2)

if __name__ == "__main__":
    main_instance = Main()
