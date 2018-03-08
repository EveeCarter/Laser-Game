from __future__ import division
import time
import Adafruit_GPIO.I2C as I2C
import Adafruit_PCA9685
import Mux
import Adafruit_TCS34725
import RPi.GPIO as GPIO

i2c = I2C
servo = Adafruit_PCA9685.PCA9685(address=0x40, busnum=1)
servo_min = 180 # 150  # Min pulse length out of 4096
servo_max = 600  # Max pulse length out of 4096
servo_mid = 350
mux = Mux.Mux()
GPIO.setmode(GPIO.BOARD)
# Set frequency to 60hz, good for servos.
servo.set_pwm_freq(60)


class Target(object):
    def __init__(self, mux, muxnum, servo, servonum, lednum):
        self.mux = mux
        self.muxnum = muxnum
        self.servo = servo
        self.servonum = servonum

        self.mux.channel(self.muxnum)
        self.sensor = Adafruit_TCS34725.TCS34725(address=0x29, busnum=1)

        self.lednum = lednum
        GPIO.setup(lednum, GPIO.OUT)

    def led_on(self):
        GPIO.output(self.lednum, True)
        
    def led_off(self):
        GPIO.output(self.lednum, False)
        
    def reading(self):
        self.mux.channel(self.muxnum)
        r, g, b, c = self.sensor.get_raw_data()
        return r, g, b, c

    def up(self):
        self.servo.set_pwm(0, self.servonum, servo_mid)
        self.led_on()

    def down(self):
        self.servo.set_pwm(0, self.servonum, servo_min)
        self.led_off()
        
t1 = Target(mux, 0, servo, 1, 7)
t2 = Target(mux, 1, servo, 2, 11)

t1.up()

while True:
    time.sleep(0.1)
    r1, g1, b1, c1 = t1.reading()
    print(b1)
    if b1 >= 1000:
        t1.down()
        time.sleep(3)
        t1.up()

# servo.set_pwm(0, 0, servo_max)


