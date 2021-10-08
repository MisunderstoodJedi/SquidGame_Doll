import time
import asyncio
from time import sleep
import RPi.GPIO as GPIO
from pygame import mixer

pir_sensor = 11
servo_pin = 3
GPIO.setmode(GPIO.BOARD)
pwm=GPIO.PWM(servo_pin, 50)
GPIO.setup(pir_sensor, GPIO.IN)
GPIO.setup(servo_pin, GPIO.OUT)
pwm.start(0)
current_state = 0

mixer.init()
music = mixer.Sound('/home/pi/scripts/squidgame_doll_music.wav')
scan = mixer.Sound('/home/pi/scripts/squidgame_doll_scan.wav')
gunshot = mixer.Sound('/home/pi/scripts/gunshot.wav')

def SetAngle(angle):
    duty = angle / 18 + 2
    GPIO.output(servo_pin, True)
    pwm.ChangeDutyCycle(duty)
    #sleep(1)
    #GPIO.output(3, False)
    #pwm.ChangeDutyCycle(0)

async def game_start():
    print("Red Light")
    music.play()
    time.sleep(5)
    SetAngle(90)

async def game_scan(delay):
    await asyncio.sleep(delay)
    print("Scanning")
    scan.play()
    try:
    while True:
        time.sleep(0.1)
        current_state = GPIO.input(pir_sensor)
        if current_state == 1:
            print("A player has been eliminated")
            # LED's make go red
            gunshot.play()
            time.sleep(0.2)

async def game_finished(delay):
    await asyncio.sleep(delay)
    SetAngle(0)
    print("Green Light")

async def main():
    print(f"Game Start")

    game_start()
    await game_scan(10)
    await game_finished(15)

    print(f"Game Finished")

asyncio.run(main())

pwm.stop()
GPIO.cleanup()
