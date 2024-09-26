from flask import Blueprint, request, jsonify

from models.mission import Mission


mission_bp = Blueprint('mission', __name__)



@mission_bp.route('/', methods=['GET'])
def get_mission():
    missions = Mission.query.all()
    mission_list = [mission.to_dict() for mission in missions]
    return jsonify(mission_list)


@mission_bp.route('/<int:id>', methods=['GET'])
def get_mission_by_id(id):
    mission = Mission.query.get_or_404(id)
    return jsonify(mission.to_dict())

