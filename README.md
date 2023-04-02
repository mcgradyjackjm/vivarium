# Automatic Vivarium Controller

This repository contains a Python script that controls an automatic vivarium system using a Raspberry Pi, a DHT temperature and humidity sensor, and other connected devices such as heat lamps and heat mats.

## Features

- Reads temperature and humidity data from a DHT sensor (AM2302)
- Controls heat mat based on temperature and time of day
- Controls daytime and nighttime lamps based on time of day
- Sends temperature, humidity, and heat mat status data to ThingSpeak

## Hardware Requirements

- Raspberry Pi (tested on Raspberry Pi 3 Model B+)
- DHT sensor (tested with AM2302)
- Energenie-compatible devices (e.g., heat mat, heat lamp, night lamp)

## Software Requirements

- Python 3
- Adafruit_DHT library
- gpiozero library
- energenie library
- requests library

## Installation

1. Clone this repository:

'git clone https://github.com/mcgradyjackjm/vivarium'
'cd vivarium'


2. Install the required Python libraries:

'pip3 install Adafruit_DHT gpiozero energenie requests'


3. Update the `thingspeak_key` variable in the `vivarium_controller.py` script with your ThingSpeak API key.

4. Connect your DHT sensor, heat mat, and lamps to your Raspberry Pi and configure the appropriate GPIO pins in the script.

## Usage

Run the script with:

python3 main.py

The script will start monitoring temperature and humidity, controlling the heat mat and lamps based on the time of day, and sending data to ThingSpeak. You must set up your own thingspeak profile, and of course change the thingspeak API from "XXX...' to your own API code.

