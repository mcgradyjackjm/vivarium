# Import necessary libraries
from datetime import datetime, time
import time as tm
import Adafruit_DHT
import requests
from energenie import switch_on, switch_off
from gpiozero import TimeOfDay

# Define sensor and pin
DHT_SENSOR = Adafruit_DHT.AM2302
DHT_PIN = 4
humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)

# Define daytime and temperature bounds
daytime = TimeOfDay(time(7), time(20))
dayLower = 24
dayUpper = 28
nightLower = 20
nightUpper = 24

# Define ThingSpeak API key
thingspeak_key = 'XXXXXXXXXXXXXXXX'

# Function to format temperature for console output
def get_temp():
    return "{:.2f}".format(float(temperature))

# Function to format humidity for console output
def get_hum():
    return "{:.2f}".format(float(humidity))

# Function to check temperature and control heat mat
def check_temp():
    heat_mat_status = 0
    humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
    now = datetime.now()
    cur_time = now.strftime("%H:%M:%S")

    # Check if it's daytime and control heat mat accordingly
    if daytime.is_active:
        if temperature < dayLower:
            switch_on(4)
            heat_mat_status = 1
            print('daytime low temp')
        elif temperature > dayUpper:
            switch_off(4)
            heat_mat_status = 0
            print('daytime high temp')
        else:
            heat_mat_status = 1
            print('daytime okay temp')
    # Check if it's nighttime and control heat mat accordingly
    else:
        if temperature < nightLower:
            switch_on(4)
            heat_mat_status = 1
            print('night low temp')
        elif temperature > nightUpper:
            switch_off(4)
            heat_mat_status = 0
            print('night high temp')
        else:
            heat_mat_status = 1
            print('night okay temp')

    # Send data to ThingSpeak
    r = requests.post('https://api.thingspeak.com/update.json',
                      data={'api_key': thingspeak_key,
                            'field1': temperature,
                            'field2': humidity,
                            'field3': heat_mat_status})
    print(cur_time, ', T:', "{:.2f}".format(temperature), ', H:', "{:.2f}".format(humidity))

# Function to check if it's daytime or nighttime and control the lights accordingly
def check_daytime():
    if daytime.is_active:
        switch_on(1)
        switch_on(2)
        switch_off(3)
    else:
        switch_off(1)
        switch_off(2)
        switch_on(3)

# Main function to run the program
def main():
    while True:
        humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
        if temperature is None or humidity is None:
            f = requests.post('https://api.thingspeak.com/update.json',
                              data={'api_key': thingspeak_key, 'status': 'failed to get reading'})
        else:
            check_daytime()
            check_temp()
            tm.sleep(120)

# Run the main function
if __name__ == "__main__":
    print('Program is starting...')
    main()
