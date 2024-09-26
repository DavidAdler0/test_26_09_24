from flask import Blueprint, request, jsonify

from services.worker import insert_worker, find_worker

worker_bp = Blueprint('worker_bp', __name__)

@worker_bp.route('/insert')
def get_worker_to_insert():
    data = request.get_json()
    res = insert_worker(data)
    if res:
        return jsonify({'inserted user'}), 201
    return jsonify({'failed to insert user'}), 400
@worker_bp.route('/find')
def get_params_to_find_by():
    data = request.args
    find_by = data.get('find_by')
    value = data.get('value')
    res = find_worker(find_by, value)
    if res:
        return jsonify({'inserted user'}), 201
    return jsonify({'failed to insert user'}), 400