from datetime import datetime, time
from time import sleep
import Adafruit_DHT # sensor library
import requests # pushes data to cloud
from energenie import switch_on, switch_off # controls lead
from gpiozero import TimeOfDay # used to set sunrise and sunset time

DHT_SENSOR = Adafruit_DHT.AM2302 # define temp sensor
DHT_PIN = 4  # define sensor GPIO pin
humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)

daytime = TimeOfDay(time(7), time(20)) #daytime from 8am-9pm
dayLower = 24
dayUpper = 28
nightLower = 20
nightUpper = 24

thingspeak_key = 'XXXXXXXXXXXXXXXX'


def getTemp(): # structures data for console
	return"{:.2f}".format(float(temperature))


def getHum(): # structures data for console
	return"{:.2f}".format(float(humidity))


def checkTemp():
	heat_mat_status = 0
	humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
	now = datetime.now()
	cur_time = now.strftime("%H:%M:%S")
	# if daytime check bounds for heat mat
	if daytime.is_active:
		if temperature < dayLower:
			daytime.when_activated = switch_on(4)
			heat_mat_status = 1
			print('daytime low temp')
		elif temperature > dayUpper:
			daytime.when_activated = switch_off(4)
			heat_mat_status = 0
			print('daytime high temp')
		else:
			heat_mat_status = 1
			print('daytime okay temp')
			pass
	# if night check bounds for heat mat
	else:
		if temperature < nightLower:
			daytime.when_deactivated = switch_on(4)
			heat_mat_status = 1
			print('night low temp')
		elif temperature > nightUpper:
			daytime.when_deactivated = switch_off(4)
			heat_mat_status = 0
			print('night high temp')
		else:
			heat_mat_status = 1
			print('night okay temp')
			pass

	r = requests.post('https://api.thingspeak.com/update.json', data = {'api_key' : thingspeak_key, 'field1':temperature, 'field2':humidity, 'field3':heat_mat_status})
	print(cur_time, ', T:', "{:.2f}".format(temperature) , ', H:', "{:.2f}".format(humidity))


def checkDaytime():
	if daytime.is_active: #day
		daytime.when_activated = switch_on(1) # led on
		daytime.when_activated = switch_on(2) # heat lamp on
		daytime.when_activated = switch_off(3) # night lamp off
	else: #night
		daytime.when_deactivated = switch_off(1) # led off
		daytime.when_deactivated = switch_off(2) # heat lamp off
		daytime.when_deactivated = switch_on(3) # night lamp on


def main():
	while True:
		humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
		# no reading then send error
		if temperature is None or humidity is None:
			f = requests.post('https://api.thingspeak.com/update.json', data = {'api_key':thingspeak_key, 'status':'failed to get reading'})
		# no errors then validate input and upload data to cloud
		else:
			checkDaytime()
			checkTemp()
			sleep(120) # wait 2 minutes before retrying

# RUNTIME PROCEDURE
if __name__=="__main__":
	print('Program is starting...')
	main()
