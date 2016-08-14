#!/usr/bin/env python3
import logging

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

class PinState(Enum):
    off = 0
    on = 1

def pi_switch_on(pin_id):
    app.logger.debug('Pin %d has been switched on!', pin_id)
    # TODO: Turn hardware pin on here

def pi_switch_off(pin_id):
    app.logger.debug('Pin %d has been switched off!', pin_id)
    # TODO: Turn hardware pin off here

#
# RESTful API functions
#

@app.route('/pins/<int:pin_id>', methods=['PUT'])
def set_pin(pin_id):
    pin = [pin for pin in pins if pin['id'] == pin_id]
    if len(pin) == 0:
        abort(404)

    try:
        if isinstance(PinState(request.json.get('state')), PinState):
            pin[0]['state'] = request.json.get('state')
            if pin[0]['state'] == PinState.on:
                pi_switch_on(pin_id)
            elif pin[0]['state'] == PinState.off:
                pi_switch_off(pin_id)
            return jsonify({'pin': pin[0]})
    except:
        abort(400);

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
