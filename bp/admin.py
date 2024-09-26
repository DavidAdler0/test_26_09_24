from flask import Blueprint, request, jsonify

from services.admin_service import create_user_table

admin_bp = Blueprint('admin', __name__)



@admin_bp.route('/create', methods=['post'])
def create_users():
    res = create_user_table()
    if res:
        return jsonify({"result": res}), 201
    else:
        return jsonify({"result": res}), 400

