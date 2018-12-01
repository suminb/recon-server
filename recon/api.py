from flask import Blueprint, jsonify


api_module = Blueprint('api', __name__)


@api_module.route('/v1/test')
def test_v1():
    return jsonify({})
