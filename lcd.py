import drivers
from drivers import i2c_dev
from time import sleep


class LCD:
	def __init__(self) -> None:
		self.lcdDisplay = drivers.Lcd()
		self.lcdDisplay.lcd_clear()
		self.setBacklight(1)
		self.breakFunc = False
  
	def setBacklight(self, back):
		if back == 1:
			i2c_dev.LCD_BACKLIGHT = 0x08
			self.lcdDisplay.lcd_backlight(1)
		elif back == 0:
			i2c_dev.LCD_BACKLIGHT = 0x00
			self.lcdDisplay.lcd_backlight(1)
            
	def swapBacklight(self):
		if i2c_dev.LCD_BACKLIGHT == 0x08:
			self.setBacklight(0)

	def swapBacklight(self):
		if i2c_dev.LCD_BACKLIGHT == 0x08:
			self.setBacklight(0)

		elif i2c_dev.LCD_BACKLIGHT == 0:
			self.setBacklight(1)
   
	def long_string(self, display, text='', num_line=1, num_cols=16):
			""" 
			Parameters: (driver, string to print, number of line to print, number of columns of your display)
			Return: This function send to display your scrolling string.
			"""
			if len(text) > num_cols:
				if self.breakFunc:
					return
				display.lcd_display_string(text[:num_cols], num_line)
				sleep(0.7)
				if self.breakFunc:
					return
				for i in range(len(text) - num_cols + 1):
					text_to_print = text[i:i+num_cols]
					display.lcd_display_string(text_to_print, num_line)
					sleep(0.2)
					if self.breakFunc:
						return
				sleep(0.7)
				if self.breakFunc:
					return
				for i in range(len(text) - num_cols, -1, -1):
					text_to_print = text[i:i+num_cols]
					display.lcd_display_string(text_to_print, num_line)
					sleep(0.2)
					if self.breakFunc:
						return

			else:
				display.lcd_display_string(text, num_line)

   
              
    



