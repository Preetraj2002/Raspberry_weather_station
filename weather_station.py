import Adafruit_DHT
import RPi.GPIO as GPIO
import time
import lcddriver

# Initialize LCD display
lcd = lcddriver.lcd()

# Set GPIO mode
GPIO.setmode(GPIO.BCM)

# Set sensor pins
DHT_PIN = 17  # GPIO pin for DHT-11 sensor
RAIN_PIN = 18  # GPIO pin for Rain Drop sensor
ULTRASONIC_TRIG_PIN = 23  # GPIO pin for Ultrasonic sensor (Trig pin)
ULTRASONIC_ECHO_PIN = 24  # GPIO pin for Ultrasonic sensor (Echo pin)

# Set up Ultrasonic sensor
GPIO.setup(ULTRASONIC_TRIG_PIN, GPIO.OUT)
GPIO.setup(ULTRASONIC_ECHO_PIN, GPIO.IN)


def get_distance():
    # Trigger ultrasonic sensor to measure distance
    GPIO.output(ULTRASONIC_TRIG_PIN, True)
    time.sleep(0.00001)
    GPIO.output(ULTRASONIC_TRIG_PIN, False)
    
    # Wait for the echo signal to be high (start time)
    while GPIO.input(ULTRASONIC_ECHO_PIN) == 0:
        pulse_start = time.time()
    
    # Wait for the echo signal to be low again (end time)
    while GPIO.input(ULTRASONIC_ECHO_PIN) == 1:
        pulse_end = time.time()
    
    # Calculate pulse duration and convert it to distance in centimeters
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150  # Speed of sound = 343 meters/second (in air) = 17150 centimeters/second
    distance = round(distance, 2)  # Round the distance to 2 decimal places
    
    return distance

def get_temperature_humidity():
    # Attempt to read temperature and humidity from DHT-11 sensor
    humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, DHT_PIN)
    
    # Check if the reading was successful
    if humidity is not None and temperature is not None:
        # Round the values to 2 decimal places
        temperature = round(temperature, 2)
        humidity = round(humidity, 2)
        return temperature, humidity
    else:
        # Return default values in case of sensor reading failure
        return 0, 0

def is_rainy():
    # Read digital output from Rain Drop sensor
    if GPIO.input(RAIN_PIN) == GPIO.HIGH:
        # Return True if the sensor detects rain, else False
        return True
    else:
        return False
    
while True:
    # Read sensor data
    temperature, humidity = get_temperature_humidity()
    distance = get_distance()
    rainy = is_rainy()
    print(f'Temp: {temperature}C')
    print(f'Humidity: {humidity}%')
    print(f'Distance: {distance} cm')
    print('Rainy: Yes' if rainy else 'Rainy:No')
    print("Printing on LCD display")

    # Display data on LCD
    lcd.lcd_clear()
    lcd.lcd_display_string(f'Temp: {temperature}C', 1)
    lcd.lcd_display_string(f'Humidity: {humidity}%', 2)
    lcd.lcd_display_string(f'Distance: {distance} cm', 3)
    lcd.lcd_display_string('Rainy: Yes' if rainy else 'Rainy: No', 4)

    # Wait for a few seconds before updating the display again
    time.sleep(10)

# Cleanup GPIO on program exit
GPIO.cleanup()