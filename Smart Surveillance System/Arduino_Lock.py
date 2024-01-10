from pyfirmata import Arduino, SERVO
import time 

Arduino_Port = "COM5"
board = Arduino(Arduino_Port)
led_green = 12
led_red = 13
servo_pin = 9
board.digital[servo_pin].mode = SERVO

def Start():
    board.digital[led_red].write(1)

def Unlock():
    board.digital[led_green].write(1)
    time.sleep(0.1)
    board.digital[led_red].write(0)
    time.sleep(0.1)
    board.digital[servo_pin].write(90)
    time.sleep(0.1)
    
    
def Lock():
    board.digital[servo_pin].write(0)
    time.sleep(0.1)
    board.digital[led_green].write(0)
    time.sleep(0.1)
    board.digital[led_red].write(1)
    time.sleep(0.1)