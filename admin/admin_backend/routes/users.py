from flask import Flask, request, jsonify, Blueprint
from routes.auth_utils import requires_auth
from db import get_mongo_connection, get_rdbms_connection
from bson.objectid import ObjectId
users = Blueprint('user', __name__,url_prefix='/users')

@users.route('/',methods=['GET'])
@requires_auth
def collect_user():
    mongodb=get_mongo_connection()
    userid=request.args.get('userid')
    data=mongodb['users'].find_one({'_id':ObjectId(userid)}, {"_id": 0})
    return jsonify({"data":data}),200