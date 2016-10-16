import RPi.GPIO as GPIO

# Physical Pi GPIOs pins we want to use
GPIO_PIN_1 = 37
GPIO_PIN_2 = 35

#
#   Pi Specific functions (to be moved to another file later on)
#

def pi_switch_on(pi_gpio_id):
    GPIO.output(pi_gpio_id, GPIO.HIGH)

def pi_switch_off(pi_gpio_id):
    GPIO.output(pi_gpio_id, GPIO.LOW)

# Set Raspberry Pi GPIOs
def pi_setup_gpio():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    GPIO.setup(GPIO_PIN_1, GPIO.OUT)
    GPIO.setup(GPIO_PIN_2, GPIO.OUT)
