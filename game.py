from __future__ import division
import time
import Adafruit_GPIO.I2C as I2C
import Adafruit_PCA9685
import Mux
import Adafruit_TCS34725

i2c = I2C
servo = Adafruit_PCA9685.PCA9685(address=0x40, busnum=1)
servo_min = 150  # Min pulse length out of 4096
servo_max = 600  # Max pulse length out of 4096
servo_mid = 400
mux = Mux.Mux()

# Set frequency to 60hz, good for servos.
servo.set_pwm_freq(60)


class Target(object):
    def __init__(self, mux, muxnum, servo, servonum):
        self.mux = mux
        self.muxnum = muxnum
        self.servo = servo
        self.servonum = servonum

        self.mux.channel(self.muxnum)
        self.sensor = Adafruit_TCS34725.TCS34725(address=0x29, busnum=1)

    def reading(self):
        self.mux.channel(self.muxnum)
        r, g, b, c = self.sensor.get_raw_data()
        return r, g, b, c
        
        
servo.set_pwm(0, 0, servo_mid)
t1 = Target(mux, 0, servo, 1)
t2 = Target(mux, 1, servo, 2)
t3 = Target(mux, 2, servo, 3)


while True:
    r1, g1, b1, c1 = t1.reading()
    r2, g2, b2, c2 = t2.reading()
    r3, g3, b3, c3 = t3.reading()
    print("1: {} {} {} {}    2: {} {} {} {}    3: {} {} {} {}".format(r1, g1, b1, c1, r2, g2, b2, c2, r3, g3, b3, c3))
    time.sleep(1)

# servo.set_pwm(0, 0, servo_max)


