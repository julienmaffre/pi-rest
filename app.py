#!/usr/bin/env python3
import logging
import json
import RPi.GPIO as GPIO

from enum import Enum
from flask import Flask, jsonify, request, abort, make_response

app = Flask(__name__)

# Default pins value
pins = [
    {
        'id': 1,
        'title': 'Orange LED',
        'state': 0,
        'pi_map': 37,
    },
    {
        'id': 2,
        'title': 'Blue LED',
        'state': 0,
        'pi_map': 35,
    }
]

#
# Pi Specific functions (to be moved to another file later on)
#

# GPIO Pin states
PIN_HIGH_STATE = GPIO.HIGH
PIN_LOW_STATE = GPIO.LOW
VALID_PIN_STATE = [PIN_HIGH_STATE, PIN_LOW_STATE]

def pi_switch_on(pi_gpio_id):
    app.logger.debug('Pin %d has been switched on!', pi_gpio_id)
    GPIO.output(pi_gpio_id, GPIO.HIGH)

def pi_switch_off(pi_gpio_id):
    app.logger.debug('Pin %d has been switched off!', pi_gpio_id)
    GPIO.output(pi_gpio_id, GPIO.LOW)

#
# RESTful API functions
#

@app.route('/pins/<int:pin_id>', methods=['PATCH'])
def set_pin(pin_id):
    pin = [pin for pin in pins if pin['id'] == pin_id]
    if len(pin) == 0:
        abort(404)

    if request.json.get('state') in VALID_PIN_STATE:
        app.logger.debug(request.json.get('state'))
        pin[0]['state'] = request.json.get('state')
        if pin[0]['state'] == PIN_HIGH_STATE:
            pi_switch_on(pin[0]['pi_map'])
        elif pin[0]['state'] == PIN_LOW_STATE:
            pi_switch_off(pin[0]['pi_map'])
        return jsonify({'pin': pin[0]})
    else:
        abort(400);

@app.route('/pins/<int:pin_id>/switch_on', methods=['PATCH'])
def switch_pin_on(pin_id):
    pin = [pin for pin in pins if pin['id'] == pin_id]
    if len(pin) == 0:
        abort(404)

    pin[0]['state'] = PIN_HIGH_STATE
    pi_switch_on(pin[0]['pi_map'])
    return jsonify({'pin': pin[0]})

@app.route('/pins/<int:pin_id>/switch_off', methods=['PATCH'])
def switch_pin_off(pin_id):
    pin = [pin for pin in pins if pin['id'] == pin_id]
    if len(pin) == 0:
        abort(404)

    pin[0]['state'] = PIN_LOW_STATE
    pi_switch_off(pin[0]['pi_map'])
    return jsonify({'pin': pin[0]})

@app.route('/pins/<int:pin_id>', methods=['GET'])
def get_pin(pin_id):
    pin = [pin for pin in pins if pin['id'] == pin_id]
    if len(pin) == 0:
        abort(404)
    return jsonify({'pin': pin[0]})

@app.route('/pins/save', methods=['GET'])
def save_pins():
    with open('pins.json','w') as f:
        json.dump(pins, f)
    return jsonify({'pins': pins})

@app.route('/pins/load', methods=['POST'])
def load_pins():
    global pins
    with open('pins.json', 'r') as f:
        pins = json.load(f)
    # TODO update GPIO accordingly
    return jsonify({'pins': pins})

@app.route('/pins', methods=['GET'])
def get_pins():
    return jsonify({'pins': pins})

@app.route('/')
def index():
    return "Hello, World!"

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad Request'}), 400)

if __name__ == '__main__':
    # TODO export GPIO setting to an init function
    # TODO set GPIO pins based on "pins.json" file if it exists
    #       or pins global variable otherwise
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    GPIO.setup(37, GPIO.OUT)
    GPIO.setup(35, GPIO.OUT)
    app.run(debug=True, host='0.0.0.0')
