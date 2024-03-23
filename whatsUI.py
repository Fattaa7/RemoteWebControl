import time
from remote import Whats
from lcd import LCD
import  threading 
class UI:
    def __init__(self):
        self.whats = Whats()
        self.lcd = LCD()
        self.messageIndex = 0
        self.col_one = []
        self.col_two = []
        self.col_three = []
        self.col_four = []
        self.t1 = threading.Thread()
        self.t2 = None
        self.getData()
        
        
    def getData(self):
        self.col_one, self.col_two, self.col_three, self.col_four = self.whats.fill_lists()
    
    def incrementIndex(self):
        if self.messageIndex == 13:
            self.messageIndex = 0
        elif self.messageIndex < 13:
            self.messageIndex += 1
        
    def decrementIndex(self):
        if self.messageIndex > 0:
            self.messageIndex -= 1
        elif self.messageIndex == 0:
            self.messageIndex = 13
        
    def display_message(self, index):
        self.breakLongMessage()
        header = self.col_one[index] + " " + self.col_four[index]
        msg = self.col_two[index] + " - " + self.col_three[index] 
        self.lcd.lcdDisplay.lcd_clear()
        self.lcd.lcdDisplay.lcd_display_string(msg,2)
        
        def up():
            self.lcd.long_string(self.lcd.lcdDisplay, header, 1)
            self.lcd.long_string(self.lcd.lcdDisplay, msg, 2)
            
            
        self.t1 = threading.Thread(target=up)
        
        self.lcd.breakFunc = False
        self.t1.start()
        
        
    def send_message(self, message, index = 0):
        self.breakLongMessage()
        index = self.messageIndex
        self.whats.send_message(index, message)


    def breakLongMessage(self):
        self.lcd.breakFunc = True
        try:
            self.t1.join()
        except:
            pass
        time.sleep(0.1)

# ui = UI()
# ui.display_message(2)