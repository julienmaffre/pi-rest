#!/usr/bin/env python3
import logging
import json

import os.path
from pi_gpio import gpio

from enum import Enum
from termcolor import colored
from flask import Flask, jsonify, request, abort, make_response
from flask_restful import Resource, Api, abort

app = Flask(__name__)
api = Api()

# GPIO Pin states
PIN_STATE_HIGH = gpio.GPIO_HIGH
PIN_STATE_LOW = gpio.GPIO_LOW
VALID_PIN_STATE = [PIN_STATE_HIGH, PIN_STATE_LOW]

# Default pins value
pins = [
    {
        'id': 1,
        'title': 'Red LED',
        'state': 0,
        'pi_map': gpio.GPIO_PIN_1,
    },
    {
        'id': 2,
        'title': 'Green LED',
        'state': 1,
        'pi_map': gpio.GPIO_PIN_2,
    }
]

#
# GPIO related functions
#
def pin_switch_on(pin):
    gpio.pi_switch_on(pin['pi_map'])
    app.logger.debug(colored('Pin %d has been switched on!', 'green'), pin['id'])

def pin_switch_off(pin):
    gpio.pi_switch_off(pin['pi_map'])
    app.logger.debug(colored('Pin %d has been switched off!', 'red'), pin['id'])

#
#   Initialisation functions
#
# Load pins from a file into global variable pins
def load_pins(file):
    global pins
    if os.path.isfile(file):
        with open(file, 'r') as f:
            app.logger.debug('Loading file...      ' + colored(file, 'green'))
            pins = json.load(f)

# Set pins according to a set of pins
def set_pins():
    for pin in pins:
        app.logger.debug(pin)
        app.logger.debug(pin)
        if pin['state'] == PIN_STATE_HIGH:
            pin_switch_on(pin)
        elif pin['state'] == PIN_STATE_LOW:
            pin_switch_off(pin)

def setup_app():
    gpio.pi_setup_gpio()
    load_pins('pins.json')
    set_pins()

#
#   RESTful API functions
#

def abort_if_pin_does_not_exist(pin_id):
    pin = [pin for pin in pins if pin['id'] == pin_id]
    if len(pin) == 0:
        abort(404, message="Pin {} does not exist!".format(pin_id))
    else:
        return pin
#
#   Pin Resource - set of methods to read and set a pin
#
class Pin(Resource):
    def get(self, pin_id):
        pin = abort_if_pin_does_not_exist(pin_id)
        return pin

    def patch(self, pin_id):
        pin = abort_if_pin_does_not_exist(pin_id)
        if request.json.get('state') in VALID_PIN_STATE:
            pin[0]['state'] = request.json.get('state')

            if pin[0]['state'] == PIN_STATE_HIGH:
                pin_switch_on(pin[0])
            elif pin[0]['state'] == PIN_STATE_LOW:
                pin_switch_off(pin[0])
            return jsonify({'pin': pin[0]})
        else:
            abort(400)

class PinSwitchOn(Resource):
    def patch(self, pin_id):
        pin = abort_if_pin_does_not_exist(pin_id)

        pin[0]['state'] = PIN_STATE_HIGH
        pin_switch_on(pin[0])
        return jsonify({'pin': pin[0]})

class PinSwitchOff(Resource):
    def patch(self, pin_id):
        pin = abort_if_pin_does_not_exist(pin_id)

        pin[0]['state'] = PIN_STATE_LOW
        pin_switch_off(pin[0])
        return jsonify({'pin': pin[0]})

#
#   Pins Resource - set of methods to read, save and load the entire set of pins
#
class Pins(Resource):
    def get(self):
        return jsonify({'pins': pins})

class PinsSave(Resource):
    def get(self):
        with open('pins.json','w') as f:
            json.dump(pins, f)
        return jsonify({'pins': pins})

class PinsLoad(Resource):
    def post(self):
        load_pins('pins.json')
        gpio.pi_set_gpio(pins)
        return jsonify({'pins': pins})

class Hello(Resource):
    def get(self):
        return {'Welcome to the pi-rest project.': 'Enjoy yourself!'}

#
#   Error handlers
#
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad Request'}), 400)

#
#   API endpoints
#
api.add_resource(Hello, '/')
api.add_resource(Pin, '/pins/<int:pin_id>')
api.add_resource(PinSwitchOn, '/pins/<int:pin_id>/switch_on')
api.add_resource(PinSwitchOff, '/pins/<int:pin_id>/switch_off')

api.add_resource(Pins, '/pins')
api.add_resource(PinsSave, '/pins/save')
api.add_resource(PinsLoad, '/pins/load')

app.before_first_request(setup_app)
api.init_app(app)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
