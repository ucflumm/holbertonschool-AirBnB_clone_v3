#!/usr/bin/python3
""" Restful Api for user objects """

from flask import jsonify, request, abort, make_response
from models import storage
from models.user import User
from api.v1.views import app_views


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """ Retrieves list of all user objects """
    # users = storage.all(User)
    # try:
    #     print(users)
    # except:
    #     print("it effed, bro")
    # return jsonify([user.to_dict() for user in users.values()])
    users_list = []
    for user in storage.all(User).values():
        users_list.append(user.to_dict())
    return jsonify(users_list)


@app_views.route('/users/<user_id>', methods=['GET'],
                 strict_slashes=False)
def get_user(user_id):
    """ Retrieves an user object by ID """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """ Deletes an user object by ID """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return make_response(jsonify({}), 200)
    # 200 status code for success
    # added make_response


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """ Creates new user object"""
    data = request.get_json()
    if data is None:
        abort(400, description="Not a JSON")
    # return jsonify({"Not a JSON"}), 400
    if 'email' not in request.get_json():
        abort(400, description="Missing email")
    # return jsonify({"Missing name"}), 400
    if 'password' not in request.get_json():
        abort(400, description="Missing password")

    new_user = User(**request.get_json())
    new_user.save()
    return make_response(jsonify(new_user.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
def update_user(user_id):
    """ Updates user object """
    data = request.get_json()
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    if not data:
        abort(400, description="Not a JSON")
    ignore_keys = ['id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(user, key, value)
    user.save()
    return make_response(jsonify(user.to_dict()), 200)
