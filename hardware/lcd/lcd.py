# encoding:utf-8


# Bad-quality fork from
# http://www.raspberrypi-spy.co.uk/2012/08/20x4-lcd-module-control-using-python/

import RPi.GPIO as GPIO
import time


class LCD20x4(object):
    '''
    LCD20x4
    '''
    def __init__(self, LCD_RS, LCD_E, LCD_D4, LCD_D5, LCD_D6, LCD_D7, LED_ON):
        # Define GPIO to LCD mapping
        self.LCD_RS = LCD_RS
        self.LCD_E = LCD_E
        self.LCD_D4 = LCD_D4
        self.LCD_D5 = LCD_D5
        self.LCD_D6 = LCD_D6
        self.LCD_D7 = LCD_D7
        self.LED_ON = LED_ON # Think on this pin! Do you need it?

        # Define some device constants
        self.LCD_WIDTH = 20 # Maximum characters per line
        self.LCD_CHR = True
        self.LCD_CMD = False

        self.LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
        self.LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line
        self.LCD_LINE_3 = 0x94 # LCD RAM address for the 3rd line
        self.LCD_LINE_4 = 0xD4 # LCD RAM address for the 4th line 

        # Timing constants
        self.E_PULSE = 0.00005
        self.E_DELAY = 0.00005



        self.start_LCD()

    def start_LCD(self):
        GPIO.setmode(GPIO.BOARD)

        GPIO.setup(self.LCD_E, GPIO.OUT)  # E
        GPIO.setup(self.LCD_RS, GPIO.OUT) # RS
        GPIO.setup(self.LCD_D4, GPIO.OUT) # DB4
        GPIO.setup(self.LCD_D5, GPIO.OUT) # DB5
        GPIO.setup(self.LCD_D6, GPIO.OUT) # DB6
        GPIO.setup(self.LCD_D7, GPIO.OUT) # DB7
        GPIO.setup(self.LED_ON, GPIO.OUT) # Backlight enable


        # Initialise display
        self.lcd_init()

        # Toggle backlight off-on
        GPIO.output(self.LED_ON, False)
        time.sleep(1)
        GPIO.output(self.LED_ON, True)
        time.sleep(1)

    def lcd_init(self):
        '''
        Initialise display
        '''
        self.lcd_byte(0x33, self.LCD_CMD)
        self.lcd_byte(0x32, self.LCD_CMD)
        self.lcd_byte(0x28, self.LCD_CMD)
        self.lcd_byte(0x0C, self.LCD_CMD)
        self.lcd_byte(0x06, self.LCD_CMD)
        self.lcd_byte(0x01, self.LCD_CMD)

    def lcd_byte(self, bits, mode):
        '''
        Send byte to data pins
        bits = data
        mode = True    for character
                       False for command
        '''

        GPIO.output(self.LCD_RS, mode) # RS

        # High bits
        GPIO.output(self.LCD_D4, False)
        GPIO.output(self.LCD_D5, False)
        GPIO.output(self.LCD_D6, False)
        GPIO.output(self.LCD_D7, False)
        if bits&0x10==0x10:
            GPIO.output(self.LCD_D4, True)
        if bits&0x20==0x20:
            GPIO.output(self.LCD_D5, True)
        if bits&0x40==0x40:
            GPIO.output(self.LCD_D6, True)
        if bits&0x80==0x80:
            GPIO.output(self.LCD_D7, True)

        # Toggle 'Enable' pin
        time.sleep(self.E_DELAY)        
        GPIO.output(self.LCD_E, True)    
        time.sleep(self.E_PULSE)
        GPIO.output(self.LCD_E, False)    
        time.sleep(self.E_DELAY)            

        # Low bits
        GPIO.output(self.LCD_D4, False)
        GPIO.output(self.LCD_D5, False)
        GPIO.output(self.LCD_D6, False)
        GPIO.output(self.LCD_D7, False)
        if bits&0x01==0x01:
            GPIO.output(self.LCD_D4, True)
        if bits&0x02==0x02:
            GPIO.output(self.LCD_D5, True)
        if bits&0x04==0x04:
            GPIO.output(self.LCD_D6, True)
        if bits&0x08==0x08:
            GPIO.output(self.LCD_D7, True)

        # Toggle 'Enable' pin
        time.sleep(self.E_DELAY)        
        GPIO.output(self.LCD_E, True)    
        time.sleep(self.E_PULSE)
        GPIO.output(self.LCD_E, False)    
        time.sleep(self.E_DELAY)    

    def lcd_string(self, message, style):
        '''
        Send string to display
        style=1 Left justified
        style=2 Centred
        style=3 Right justified
        '''
        if style==1:
            message = message.ljust(self.LCD_WIDTH," ")
        elif style==2:
            message = message.center(self.LCD_WIDTH," ")
        elif style==3:
            message = message.rjust(self.LCD_WIDTH," ")

        for i in range(self.LCD_WIDTH):
            self.lcd_byte(ord(message[i]),self.LCD_CHR)

    def center_text(self, s1, s2, s3, s4):
        self.lcd_byte(self.LCD_LINE_1, self.LCD_CMD)
        self.lcd_string(s1,2) 
        self.lcd_byte(self.LCD_LINE_2, self.LCD_CMD)
        self.lcd_string(s2,2)
        self.lcd_byte(self.LCD_LINE_3, self.LCD_CMD)
        self.lcd_string(s3,2)
        self.lcd_byte(self.LCD_LINE_4, self.LCD_CMD)
        self.lcd_string(s4,2)

    def line1_center(self, s):
        '''
        Print text on 1st line
        For short string ( len(string) =< LCD_WIDTH )
        '''
        self.lcd_byte(self.LCD_LINE_1, self.LCD_CMD)
        self.lcd_string(s,2)

    def line2_center(self, s):
        '''
        Print text on 2nd line
        For short string ( len(string) =< LCD_WIDTH )
        '''
        self.lcd_byte(self.LCD_LINE_2, self.LCD_CMD)
        self.lcd_string(s,2)

    def line3_center(self, s):
        '''
        Print text on 4rd line
        For short string ( len(string) =< LCD_WIDTH )
        '''
        self.lcd_byte(self.LCD_LINE_3, self.LCD_CMD)
        self.lcd_string(s,2)

    def line4_center(self, s):
        '''
        Print text on 4th line
        For short string ( len(string) =< LCD_WIDTH )
        '''
        self.lcd_byte(self.LCD_LINE_4, self.LCD_CMD)
        self.lcd_string(s,2)

    
        


if __name__ == '__main__':
    my_lcd = LCD20x4(26, 24, 22, 18, 16, 12, 10)
    my_lcd.center_text("11111111112222222222", "12345678901234567890", "It works!", "абвгдеёжзий")
