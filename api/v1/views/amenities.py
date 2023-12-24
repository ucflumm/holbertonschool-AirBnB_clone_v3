#!/usr/bin/python3
"""
Runs the amenities.py file
"""

from flask import Flask, jsonify, abort, request
from models import storage
from models.amenity import Amenity

app = Flask(__name__)

# @app.route('/api/v1/amenities', methods=['GET'])
# def get_amenities():
#     amenities = storage.all(Amenity).values()
#     return jsonify([amenity.to_dict() for amenity in amenities]), 200

@app.route('/api/v1/amenities', methods=['GET'])
def get_amenities():
    amenities = storage.all(Amenity).values()
    return jsonify([amenity.to_dict() for amenity in amenities])


@app.route('/api/v1/amenities/<amenity_id>', methods=['GET'])
def get_amenity(amenity_id):
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    return jsonify(amenity.to_dict())


@app.route('/api/v1/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity(amenity_id):
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


@app.route('/api/v1/amenities', methods=['POST'])
def create_amenity():
    if not request.get_json():
        abort(400, 'Not a JSON')
    if 'name' not in request.get_json():
        abort(400, 'Missing name')
    amenity = Amenity(**request.get_json())
    amenity.save()
    return jsonify(amenity.to_dict()), 201


@app.route('/api/v1/amenities/<amenity_id>', methods=['PUT'])
def update_amenity(amenity_id):
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    data = request.get_json()
    ignore_keys = ['id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(amenity, key, value)
    amenity.save()
    return jsonify(amenity.to_dict()), 200

