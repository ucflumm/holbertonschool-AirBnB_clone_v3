#!/usr/bin/python3
"""
Creates a view for State objects that handles all default RESTFul API actions
"""
from models.state import State
from models import storage
from models.base_model import BaseModel
from api.v1.views import app_views
from flask import request, jsonify, abort


@app_views.route('/states', strict_slashes=False)
def list_all_states():
    states_list = []
    for value in storage.all(State).values():
        states_list.append(value.to_dict())
    return jsonify(states_list)


@app_views.route('/states/<state_id>', strict_slashes=False)
def list_state_by_id(state_id):
    state = storage.get(State, state_id)
    not_found_error(state)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state_by_id(state_id):
    state = storage.get(State, state_id)
    not_found_error(state)
    state.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    if request.headers.get('Content-Type') != 'application/json':
        abort(400)

    json_dict = request.get_json()
    not_json_format(json_dict)

    if 'name' not in json_dict:
        abort(400, description="Missing name")
    new_state = State(**json_dict)
    new_state.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    if request.headers.get('Content-Type') != 'application/json':
        abort(400)

    state = storage.get(State, state_id)
    not_found_error(state)
    json_dict = request.get_json()
    not_json_format(json_dict)

    for key, value in json_dict.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(state, key, value)
    storage.save()
    return jsonify(state.to_dict()), 200


def not_found_error(state):
    if state is None:
        abort(404)


def not_json_format(json_dict):
    if not json_dict:
        abort(400, description="Not a JSON")
