try:
    print ('Trying to import RPi GPIO!')
    import RPi.GPIO
    from .pi_gpio import *
except (RuntimeError, ImportError):
    print ('RPI.GPIO library cannot be found!')
    from .mock_gpio import *
    print (GPIO_HIGH)
