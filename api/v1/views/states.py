#!/usr/bin/python3
""" states routes """
from api.v1.views import app_views
from flask import Flask, jsonify, abort, make_response, request
from models import storage
from models.state import State


@app_views.route('/states', strict_slashes=False)
def states():
    """ list of states """
    states = storage.all('State')
    return jsonify([value.to_dict() for value in states.values()])


@app_views.route('/states/<string:id>', strict_slashes=False)
def state_id(id):
    """ json data of a sngle state """
    single_state = storage.get('State', id)
    if single_state:
        return jsonify(single_state.to_dict()), 200
    abort(404)


@app_views.route('/states', strict_slashes=False, methods=['POST'])
def insert_state():
    """ Creates a new state """
    dictionary = request.get_json()
    if dictionary is None:
        abort(400, 'Not a JSON')
    if dictionary.get('name') is None:
        abort(400, 'Missing name')
    state = State(**dictionary)
    state.save()
    return make_response(jsonify(state.to_dict()), 201)


@app_views.route('/states/<string:id>', strict_slashes=False, methods=['PUT'])
def update_state(id):
    """ Updates an state """
    dictionary = request.get_json()
    if dictionary is None:
        abort(400, 'Not a Json')
    single_state = storage.get('State', id)
    if single_state is None:
        abort(404)
    [setattr(single_state, key, value) for key, value in dictionary.items()
        if key not in ['id', 'created_at', 'updated_at']]
    single_state.save()
    return jsonify(single_state.to_dict())


@app_views.route('/states/<string:id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_state(id):
    """ Deletes an state """
    single_state = storage.get('State', id)
    if single_state is None:
        abort(404, 'Not found')
    single_state.delete()
    storage.save()
    return jsonify({})
