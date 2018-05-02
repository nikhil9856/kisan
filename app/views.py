#Add all global routes in this file

from flask import request
from flask import Blueprint
import logging

from lib.decorators import jsonify, logrequest
logger = logging.getLogger()

global_routes = Blueprint('global_routes', __name__)

@global_routes.route('/', methods=['GET'])
@jsonify
@logrequest
def test():
  logger.info("Getting call for test function with request data %s", request.data)
  result = {"msg": "welcome to flask-template app"}
  return result
