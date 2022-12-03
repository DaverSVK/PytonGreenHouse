import requests
import Adafruit_DHT
import time
import RPi.GPIO as GPIO
import drivers
from datetime import datetime
import Adafruit_ADS1x15

display = drivers.Lcd()
motor = 13
chanel = 21
GPIO.setmode(GPIO.BCM)
GPIO.setup(chanel, GPIO.IN)

adc = Adafruit_ADS1x15.ADS1115()
GAIN = 1

DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 4
url="https://fathomless-dusk-03713.herokuapp.com/servitka"
url2="https://greenhouseapp-a928f-default-rtdb.firebaseio.com/data"
GPIO.add_event_detect(chanel, GPIO.BOTH, bouncetime=300)
time.sleep(1)

try:

        while True:
                file = open("/home/pi/garden/lcd/Datalog.csv", "a")
                humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
                if humidity is not None and temperature is not None:
                        display.lcd_display_string("Tep:{0:0.1f}C Vlh:{1:0.1f}%".format(temperature, humidity),1)
                        print("Telota: {0:0.1f}°C, Vlhkost: {1:0.2f}%".format(temperature, humidity),1);
                        water = str(int(100-(100/11056*(adc.read_adc(0, gain=GAIN)-6688))))
                        water2 = str(int(100-(100/11056*(adc.read_adc(1, gain=GAIN)-6688))))
                        water3 = str(int(100-(100/11056*(adc.read_adc(2, gain=GAIN)-6688))))
                        water4 = str(int(100-(100/11056*(adc.read_adc(3, gain=GAIN)-6688))))
                        display.lcd_display_extended_string("Water:"+water+"/"+water2+"%", 2)
                        print(water)
                        print(water2)
                        print(water3)
                        print(water4)
                        now = datetime.now()
                        file.write(str(now)+",   "+str(temperature)+"°C"+",   "+str(humidity)+"%"+",    "+ water+",   "+water2+",   "+water3+",   "+water4+"\n")
                        data={"date": str(now), "temperature": float(temperature), "humidity": float(humidity), "water": water, "water2": water2, "water3": water3, "water4": water4}
                        requests.post(url2 + ".json", json=data)
                        time.sleep(1800)
                else:
                        display.lcd_display_string("Pixi zas to nejdze",1)
                        print("Sensor failure.");
                        time.sleep(3)
                file.flush()
                file.close()

except KeyboardInterrupt:
    # If there is a KeyboardInterrupt (when you press ctrl+c), exit the program and cleanup
    print("Cleaning up!")
    display.lcd_clear()
    file.close()
