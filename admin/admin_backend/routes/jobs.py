from flask import Flask, request, jsonify, Blueprint
from routes.auth_utils import requires_auth
from db import get_mongo_connection, get_rdbms_connection
from bson import ObjectId
import json
jobs = Blueprint('jobs', __name__,url_prefix='/jobs')

@jobs.route('/create',methods=["POST"])
@requires_auth
def post_job():
    # Get the job posting data from the request
    mongodb=get_mongo_connection()
    job_postings=mongodb['job_postings']
    job_posting = request.json
    try:
        # Insert the job posting into the collection
        jobid=job_postings.insert_one(job_posting)
        return jsonify({"jobid":str(jobid.inserted_id)}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@jobs.route('/application') ##job id user id are query parameters
def apply():
    jobid:str=request.args.get('jobid')
    userid:str=request.args.get('userid')
    conn=get_rdbms_connection()
    cur=conn.cursor()
    cur.execute('''
        INSERT INTO applns (jobid,userid) VALUES (?,?)
    ''',(jobid,userid))
    cur.close()
    conn.commit()
    return jsonify({"msg": str(e)}), 201

@jobs.route('/segragate')## jobid query param
@requires_auth
def segragate():
    jobid=request.args.get('jobid')
    conn=get_rdbms_connection()
    cur=conn.cursor()
    cur.execute("""
        SELECT applnid,userid,at FROM applns WHERE jobid=?
    """,(jobid,))
    applns=cur.fetchall()
    return jsonify({"applns": applns}), 200

@jobs.route('/shortlist')
@requires_auth
def shortlist():
    applnid=request.args.get('applnid')
    userid=request.args.get('userid')
    conn=get_rdbms_connection()
    cur=conn.cursor()
    cur.execute("""
        UPDATE applns SET shortlisted='YES' WHERE applnid=? AND userid=?
    """,(applnid,userid))
    cur.close()
    conn.commit()
    return jsonify({"msg": "Done"}), 200

@jobs.route('/collect')
@requires_auth
def collect():
    jobid:str=request.args.get('jobid')
    mongodb=get_mongo_connection()
    data=mongodb['job_postings'].find_one({'_id':ObjectId(jobid)},{"_id": 0})
    return jsonify({"data":data}),200