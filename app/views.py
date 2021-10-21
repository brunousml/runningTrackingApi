from flask import request
from flask.json import jsonify
from flask import Blueprint
from app.auth import authenticate
from app.helpers import get_size_querystring, get_sort_by, get_sorted_list

api = Blueprint('api', __name__)

STORE = {}


@api.route('/users/<username>', methods=['POST', 'PATCH'])
def update_user(username):
    data = request.get_json()
    data_keys = list(data)

    if 'ts' in data_keys and 'distance' in data_keys and 'time' in data_keys:
        if username in STORE.keys():
            old_data = STORE[username]

            cumulative_distance = old_data['cumulative_distance'] + data['distance']
            cumulative_time = old_data['cumulative_time'] + data['time']
            average_speed = cumulative_distance / cumulative_time

            STORE[username] = dict(
                cumulative_distance=cumulative_distance,
                cumulative_time=cumulative_time,
                average_speed=average_speed,
                user=username,
                ts=data['ts'],
            )
        else:
            average_speed = data['distance'] / data['time']
            STORE[username] = dict(
                cumulative_distance=data['distance'],
                cumulative_time=data['time'],
                average_speed=average_speed,
                user=username,
                ts=data['ts'],
            )
        return jsonify(STORE[username]), 200

    return "Required fields not found", 400


@api.route('/users/<username>', methods=['GET'])
def fetch_user(username):
    if username in STORE.keys():
        return jsonify(STORE[username]), 200

    return "Not found", 404


@api.route('/users/top/<attribute>', methods=['GET'])
def get_top_users(attribute):
    try:
        size = get_size_querystring(request)
    except ValueError as e:
        return jsonify({"Value Error": e.__str__()}), 400

    sort_by = get_sort_by(attribute)
    _reversed = attribute != 'speed'
    top_users = get_sorted_list(sort_by=sort_by, scope=STORE, reverse=_reversed)

    if size > 0:
        top_users = top_users[0:size]

    return jsonify(top_users), 200


@api.route('/users/<username>/find-partners', methods=['GET'])
def find_partners(username):
    try:
        size = get_size_querystring(request)
    except ValueError as e:
        return jsonify({"Value Error": e.__str__()}), 400

    result = get_sorted_list(sort_by='average_speed', scope=STORE, avoid_user=username)

    if size:
        result = result[0:size]

    return jsonify(result), 200


@api.route('/users/<username>/private', methods=['GET'])
@authenticate
def private_route(username):
    if username in STORE:
        return jsonify(STORE[username]), 200

    return jsonify('User not found'), 404
