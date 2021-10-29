import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

class Motor():
    def __init__(self,Ena,In1,In2):
        self.Ena = Ena
        self.In1 = In1
        self.In2 = In2
        GPIO.setup(self.Ena, GPIO.OUT)
        GPIO.setup(self.In1, GPIO.OUT)
        GPIO.setup(self.In2, GPIO.OUT)
        
        self.pwm = GPIO.PWM(self.Ena, 100)
        self.pwm.start(0)
    
    def Forward(self, time=0.2):
        GPIO.output(self.In1, GPIO.LOW)
        GPIO.output(self.In2, GPIO.HIGH)
        self.pwm.ChangeDutyCycle(30)
        sleep(time)
        
    def Stop(self, time=0.2):
        self.pwm.ChangeDutyCycle(0)
        sleep(time)
        
        
def Left(motor1, motor2, motor3, motor4):
    print('Left')
    motor1.Stop()
    motor2.Stop()
    motor3.Forward()
    motor4.Forward()

def Right(motor1, motor2, motor3, motor4):
    print('Right')
    motor1.Forward()
    motor2.Forward()
    motor3.Stop()
    motor4.Stop()
    
def Forward(motor1, motor2, motor3, motor4):
    print('Forward')
    motor1.Forward()
    motor2.Forward()
    motor3.Forward()
    motor4.Forward()

def Stop(motor1, motor2, motor3, motor4):
    print('Stop')
    motor1.Stop()
    motor2.Stop()
    motor3.Stop()
    motor4.Stop()
    
motor1 = Motor(2,3,4)
motor2 = Motor(17,27,22)
motor3 = Motor(10,9,11)
motor4 = Motor(5,6,13)


Left(motor1, motor2, motor3, motor4)
Stop(motor1, motor2, motor3, motor4)
Right(motor1, motor2, motor3, motor4)
Stop(motor1, motor2, motor3, motor4)
Forward(motor1, motor2, motor3, motor4)
Stop(motor1, motor2, motor3, motor4)

print("Finished")