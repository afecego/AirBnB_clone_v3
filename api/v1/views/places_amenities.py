#!/usr/bin/python3
""" objects that handle all default RestFul API actions for Place -
Amenity """
from models.place import Place
from models.amenity import Amenity
from models import storage
from api.v1.views import app_views
from os import environ
from flask import abort, jsonify, make_response
from flasgger.utils import swag_from


@app_views.route('places/<string:place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
@swag_from('documentation/place_amenity/get_places_amenities.yml',
           methods=['GET'])
def get_place_amenities(place_id):
    """
    Retrieves the list of all Amenity objects of a Place
    """
    place = storage.get('Place', place_id)

    if place is None:
        abort(404, 'Not found')

    if environ.get('HBNB_TYPE_STORAGE') == "db":
        amenities = [amenity.to_dict() for amenity in place.amenities]
    else:
        amenities = [storage.get('Amenity', amenity_id).to_dict()
                     for amenity_id in place.amenity_ids]

    return jsonify(amenities)


@app_views.route('/places/<string:place_id>/amenities/<string:amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_place_amenity(place_id=None, amenity_id=None):
    """
    Deletes a Amenity object of a Place
    """
    place = storage.get('Place', place_id)
    if place is None:
        abort(404, 'Not found')
    amenity = storage.get('Amenity', amenity_id)
    if amenity is None:
        abort(404, 'Not found')

    if amenity not in place.amenities and amenity.id not in place.amenities:
        abort(404, 'Not found')
    if environ.get('HBNB_TYPE_STORAGE') == "db":
        place.amenities.remove(amenity)
    else:
        place.amenity_ids.pop(amenity.id, None)
    place.save()
    return jsonify({}), 200


@app_views.route('/places/<string:place_id>/amenities/<string:amenity_id>',
                 methods=['POST'],
                 strict_slashes=False)
def post_place_amenity(place_id=None, amenity_id=None):
    """
    Link a Amenity object to a Place
    """
    place = storage.get('Place', place_id)
    if place is None:
        abort(404, 'Not found')
    amenity = storage.get('Amenity', amenity_id)
    if amenity is None:
        abort(404, 'Not found')
    if amenity in place.amenities or amenity.id in place.amenities:
        return jsonify(amenity.to_dict()), 200
    if environ.get('HBNB_TYPE_STORAGE') == "db":
        place_amenities = place.amenities
    else:
        place_amenities = place.amenity_ids
        return jsonify(amenity.to_dict())
    place_amenities.append(amenity)
    place.save()
    return make_response(jsonify(amenity.to_dict()), 201)
