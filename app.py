#!/usr/bin/env python3
import logging
import json

from enum import Enum
from flask import Flask, jsonify, request, abort, make_response

app = Flask(__name__)

pins = [
    {
        'id': 1,
        'title': 'Orange LED',
        'state': 0,
    },
    {
        'id': 2,
        'title': 'Blue LED',
        'state': 1,
    }
]

#
# Pi Specific functions (to be moved to another file later on)
#

# GPIO Pin states
PIN_HIGH_STATE = 1
PIN_TEST = 7
PIN_LOW_STATE = 0
VALID_PIN_STATE = [PIN_HIGH_STATE, PIN_LOW_STATE]

def pi_switch_on(pin_id):
    app.logger.debug('Pin %d has been switched on!', pin_id)
    # TODO: Turn hardware pin on here

def pi_switch_off(pin_id):
    app.logger.debug('Pin %d has been switched off!', pin_id)
    # TODO: Turn hardware pin off here

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
            pi_switch_on(pin_id)
        elif pin[0]['state'] == PIN_LOW_STATE:
            pi_switch_off(pin_id)
        return jsonify({'pin': pin[0]})
    else:
        abort(400);

@app.route('/pins/<int:pin_id>/switch_on', methods=['PATCH'])
def switch_pin_on(pin_id):
    pin = [pin for pin in pins if pin['id'] == pin_id]
    if len(pin) == 0:
        abort(404)

    pin[0]['state'] = 1
    pi_switch_on(pin_id)
    return jsonify({'pin': pin[0]})

@app.route('/pins/<int:pin_id>/switch_off', methods=['PATCH'])
def switch_pin_off(pin_id):
    pin = [pin for pin in pins if pin['id'] == pin_id]
    if len(pin) == 0:
        abort(404)

    pin[0]['state'] = 0
    pi_switch_off(pin_id)
    return jsonify({'pin': pin[0]})


@app.route('/pins/<int:pin_id>', methods=['GET'])
def get_pin(pin_id):
    pin = [pin for pin in pins if pin['id'] == pin_id]
    if len(pin) == 0:
        abort(404)
    return jsonify({'pin': pin[0]})

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
    app.run(debug=True, host='0.0.0.0')
