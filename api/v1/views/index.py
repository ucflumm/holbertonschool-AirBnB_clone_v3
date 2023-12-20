#!/usr/bin/python3
"""
Runs the index.py file
"""

from flask import jsonify
from api.v1.views import app_views

@app_views.route('/status', methods=['GET'])
def get_status():
    return jsonify({"status": "OK"})
