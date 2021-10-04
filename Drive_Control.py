import RPi.GPIO as GPIO          
from time import sleep

GPIO.setwarnings(False)

GPIO.setmode(GPIO.BOARD)

motor1a = 7
motor1b = 11
motor1c = 22

motor2a = 13
motor2b = 16
motor2c = 15

GPIO.setup(motor1a, GPIO.OUT)
GPIO.setup(motor1b, GPIO.OUT)
GPIO.setup(motor1c, GPIO.OUT)
GPIO.setup(motor2a, GPIO.OUT)
GPIO.setup(motor2b, GPIO.OUT)
GPIO.setup(motor2c, GPIO.OUT)

pwm1a = GPIO.PWM(motor1a, 100)
pwm1b = GPIO.PWM(motor1b, 100)
pwm1c = GPIO.PWM(motor1c, 100)
pwm2a = GPIO.PWM(motor2a, 100)
pwm2b = GPIO.PWM(motor2b, 100)
pwm2c = GPIO.PWM(motor2c, 100)

pwm1a.start(0)
pwm1b.start(0)
pwm1c.start(0)
pwm2a.start(0)
pwm2b.start(0)
pwm2c.start(0)

def forward():
    GPIO.output(motor1a, GPIO.HIGH)
    GPIO.output(motor1b, GPIO.LOW)
    GPIO.output(motor1c, GPIO.HIGH)
    GPIO.output(motor2a, GPIO.HIGH)
    GPIO.output(motor2b, GPIO.LOW)
    GPIO.output(motor2c, GPIO.HIGH)

def reverse():
    GPIO.output(motor1a, GPIO.LOW)
    GPIO.output(motor1b, GPIO.HIGH)
    GPIO.output(motor1c, GPIO.HIGH)
    GPIO.output(motor2a, GPIO.LOW)
    GPIO.output(motor2b, GPIO.HIGH)
    GPIO.output(motor2c, GPIO.HIGH)

def right():
    GPIO.output(motor1a, GPIO.LOW)
    GPIO.output(motor1b, GPIO.HIGH)
    GPIO.output(motor1c, GPIO.HIGH)
    GPIO.output(motor2a, GPIO.HIGH)
    GPIO.output(motor2b, GPIO.LOW)
    GPIO.output(motor2c, GPIO.HIGH)

def left():
    GPIO.output(motor1a, GPIO.HIGH)
    GPIO.output(motor1b, GPIO.LOW)
    GPIO.output(motor1c, GPIO.HIGH)
    GPIO.output(motor2a, GPIO.LOW)
    GPIO.output(motor2b, GPIO.HIGH)
    GPIO.output(motor2c, GPIO.HIGH)

def stop():
    GPIO.output(motor1a, GPIO.LOW)
    GPIO.output(motor1b, GPIO.LOW)
    GPIO.output(motor1c, GPIO.LOW)
    GPIO.output(motor2a, GPIO.LOW)
    GPIO.output(motor2b, GPIO.LOW)
    GPIO.output(motor2c, GPIO.LOW)



while(1):

pwm.stop()
GPIO.cleanup()

