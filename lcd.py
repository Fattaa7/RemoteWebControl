import drivers
from drivers import i2c_dev
from time import sleep
import threading

lcdDisplay = 0

def init():
    global lcdDisplay
    lcdDisplay = drivers.Lcd()
    lcdDisplay.lcd_clear()
    setBacklight(1)

def setBacklight(back):
    if back == 1:
        i2c_dev.LCD_BACKLIGHT = 0x08
        lcdDisplay.lcd_backlight(1)
    elif back == 0:
        i2c_dev.LCD_BACKLIGHT = 0x00
        lcdDisplay.lcd_backlight(1)

def swapBacklight():
    if i2c_dev.LCD_BACKLIGHT == 0x08:
        setBacklight(0)

    elif i2c_dev.LCD_BACKLIGHT == 0:
        setBacklight(1)
    
 
def long_string(display, text='', num_line=1, num_cols=16):
		""" 
		Parameters: (driver, string to print, number of line to print, number of columns of your display)
		Return: This function send to display your scrolling string.
		"""
		if len(text) > num_cols:
			display.lcd_display_string(text[:num_cols], num_line)
			sleep(0.7)
			for i in range(len(text) - num_cols + 1):
				text_to_print = text[i:i+num_cols]
				display.lcd_display_string(text_to_print, num_line)
				sleep(0.1)
			sleep(0.7)
			for i in range(len(text) - num_cols, -1, -1):
				text_to_print = text[i:i+num_cols]
				display.lcd_display_string(text_to_print, num_line)
				sleep(0.1)
		else:
			display.lcd_display_string(text, num_line)
   

