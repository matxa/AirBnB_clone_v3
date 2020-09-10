#!/usr/bin/python3
"""amenities app_view
"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities/', methods=['GET'])
def all_amenites():
    """list all amenites
    """
    if request.method == 'GET':
        all_amenites = []
        for amenity in storage.all(Amenity).values():
            all_amenites.append(amenity.to_dict())
        return make_response(jsonify(all_amenites))


@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def one_amenity(amenity_id):
    """get amenity by id
    """
    if request.method == 'GET':
        for value in storage.all(Amenity).values():
            if value.id == amenity_id:
                return make_response(jsonify(value.to_dict()))
        return abort(404)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity(amenity_id):
    """delete amenity by id
    """
    if request.method == 'DELETE':
        for value in storage.all(Amenity).values():
            if value.id == amenity_id:
                value.delete()
                storage.save()
                return make_response(jsonify({}), 200)
        return abort(404)


@app_views.route('/amenities/', methods=['POST'])
def post_amenites():
    """post new amenities
    """
    if request.method == 'POST':
        try:
            data = request.get_json()
            if 'name' not in data.keys():
                return make_response(jsonify(error="Missing name"), 400)
            ignore_keys = ['id', 'created_at', 'updated_at']
            for key, value in data.items():
                if key not in ignore_keys and hasattr(Amenity, key):
                    if key == 'name':
                        new_amenity = Amenity()
                        setattr(new_amenity, key, value)
                        new_amenity.save()
                        return make_response(new_amenity.to_dict(), 200)
        except Exception:
            return make_response(jsonify(error="Not a JSON"), 400)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def put_amenites(amenity_id):
    """update amenity instance
    """
    if request.method == 'PUT':
        try:
            data = request.get_json()
        except Exception:
            return make_response(jsonify(error="Not a JSON"), 400)
        ignore_keys = ['id', 'created_at', 'updated_at']
        for value in storage.all(Amenity).values():
            if value.id == amenity_id:
                for k, v in data.items():
                    if k not in ignore_keys and hasattr(Amenity, k):
                        setattr(value, k, v)
                        value.save()
                        return make_response(value.to_dict(), 200)
        return abort(404)
