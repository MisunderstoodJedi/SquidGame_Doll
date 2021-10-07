#!/usr/bin/env python

__author__      = "MisunderstoodJedi"
__credits__   = ["Insert Name(s) Here"]
__status__  =  "A work in progress"

### Target Actions ###
# [X] Press button to start
# [o] Music plays (Untested)
# [] Head turns no lighs on
# [] Movement detect
# []     Movement detected lights turn red
# [] No movement after 5 seconds head turns around 

import time
from time import sleep
from gpiozero import Servo, MotionSensor, LED
import RPi.GPIO as GPIO
from pygame import mixer
#import threading
import multiprocessing
from signal import pause

# Load Music #
mixer.init()
music = mixer.Sound('/home/pi/scripts/squidgame_doll_music.wav')
scan = mixer.Sound('/home/pi/scripts/squidgame_doll_scan.wav')
gunshot = mixer.Sound('/home/pi/scripts/gunshot.wav')

GPIO.setmode(GPIO.BOARD)
GPIO.setup(3, GPIO.OUT)
pwm=GPIO.PWM(3, 50)
pwm.start(0)

def SetAngle(angle):
    duty = angle / 18 + 2
    GPIO.output(3, True)
    pwm.ChangeDutyCycle(duty)
    sleep(1)
    GPIO.output(3, False)
    pwm.ChangeDutyCycle(0)

# Initial button press to initiate actions #
def button_pressed(channel):
    #t1.start()
    #time.sleep(5)
    #t1.terminate()
    #t2.start()
    #time.sleep(5)
    #t2.terminate()
    #t3.start()

    game_start()
    time.sleep(5)
    detect_movement() # Needs to only run for 5 seconds
    time.sleep(5)
    reset_game()
    
def game_start():
    print("Game Started")
    print("Red Light")
    music.play() # Doll sings her song
    time.sleep(5) # Untested but I do not know yet if python waits for the sound to stop if not wait 5 seconds while it's playing
    SetAngle(90)  # Ratate head (amounts etc to be "tuned" in when serve's arrive

def detect_movement():
    print("Scanning Movement")
    scan.play()
    # Specify time to scan for
    # If movement detected
    # gunshot.play()
    # LED Turn Red

def reset_game(): # Resets everything and awaits another button press
    SetAngle(0)
    t3.terminate()
    print("Green Light")

#t1 = threading.Thread(target=game_start)  
#t2 = threading.Thread(target=detect_movement) 
#t3 = threading.Thread(target=reset_game)

t1 = multiprocessing.Process(target=game_start)  
t2 = multiprocessing.Process(target=detect_movement) 
t3 = multiprocessing.Process(target=reset_game)

GPIO.setwarnings(False) 
GPIO.setmode(GPIO.BOARD) 
GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(10,GPIO.RISING,callback=button_pressed) 

message = input("Press enter to quit\n\n") # Run until someone presses enter
GPIO.cleanup()
