from __future__ import division
import time
import Adafruit_GPIO.I2C as I2C
import Adafruit_PCA9685
import Mux
import Target
import Adafruit_TCS34725
import RPi.GPIO as GPIO
import Display
import Button

i2c = I2C
servo = Adafruit_PCA9685.PCA9685(address=0x40, busnum=1)
mux = Mux.Mux()
# GPIO.setmode(GPIO.BOARD)
# Set frequency to 60hz, good for servos.
servo.set_pwm_freq(60)

display = Display.Display(mux, 0)
        
t1 = Target.Target(mux, 1, servo, 2, 4)
t2 = Target.Target(mux, 2, servo, 3, 17)
t3 = Target.Target(mux, 3, servo, 0, 27)
t4 = Target.Target(mux, 4, servo, 4, 22)
t5 = Target.Target(mux, 5, servo, 1, 18)

green = Button.Button(23)
yellow = Button.Button(24)
red = Button.Button(25)
blue = Button.Button(8)

for t in [t1, t2, t3, t4, t5]:
    t.down()
    t.led_off()

display.show("Select Gamemode")

numships = 0

while True:
    if green.pressed():
        display.show("Easy")
        numships = 10
        break
    if yellow.pressed():
        display.show("Medium")
        numships = 20
        break
    if red.pressed():
        display.show("Hard")
        numships = 30
        break 

display.show("Number of ships:\n{}".format(numships))    
t = t5

t.up()
while True:
    time.sleep(0.1)
    r1, g1, b1, c1 = t.reading()
    print(b1)
    if b1 >= 1000:
        t.down()
        time.sleep(3)
        t.up()

# servo.set_pwm(0, 0, servo_max)


