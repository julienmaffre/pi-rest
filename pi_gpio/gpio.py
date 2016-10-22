import RPi.GPIO

# Handy wrapper
GPIO_HIGH = RPi.GPIO.HIGH
GPIO_LOW = RPi.GPIO.LOW

# Physical Pi GPIOs pins we want to use
GPIO_PIN_1 = 37
GPIO_PIN_2 = 35

#
#   Pi Specific functions (to be moved to another file later on)
#

def pi_switch_on(pi_gpio_id):
    RPi.GPIO.output(pi_gpio_id, RPi.GPIO.HIGH)

def pi_switch_off(pi_gpio_id):
    RPi.GPIO.output(pi_gpio_id, RPi.GPIO.LOW)

# Set Raspberry Pi GPIOs
def pi_setup_gpio():
    RPi.GPIO.setmode(RPi.GPIO.BOARD)
    RPi.GPIO.setwarnings(False)
    RPi.GPIO.setup(GPIO_PIN_1, RPi.GPIO.OUT)
    RPi.GPIO.setup(GPIO_PIN_2, RPi.GPIO.OUT)
