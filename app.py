import json
import traceback
import uuid
import os
from redis import Redis
from flask import Flask, request, jsonify, Response, abort
from worker import crawler_broker

app = Flask(__name__)
crawler_repo = Redis(
    host=os.environ.get('REDIS_DEFAULT_HOST','localhost'),
    port=os.environ.get('REDIS_DEFAULT_PORT',6379),
    db=0,
    password=os.environ.get('REDIS_DEFAULT_PASSWORD','')) 

@app.route('/crawl', methods=['POST'])
def crawl():
    req = request.get_data()
    crawl_url, depth = get_parameters(req)
    public_id = str(uuid.uuid1())
    crawler_broker.delay(public_id, crawl_url, depth)
    crawler_repo.set(public_id+":exists","true")
    data = {}
    data["public_id"] = public_id
    return jsonify(data)

def get_parameters(req):
    json_request = json.loads(req)
    crawl_url = json_request.get('crawl_url')
    crawl_depth = json_request.get('crawl_depth',1)
    return crawl_url,crawl_depth

@app.route('/data/<string:public_id>')
def get_crawl_data(public_id):
    if crawler_repo.exists(public_id+":exists"):
        if crawler_repo.exists(public_id+":data"):
            return crawler_repo.get(public_id+":data"),200
        else:
            Response("crawl in progress",status=102)    
    else:
        abort(404,"public_id doesn't exists")

@app.route('/_health', methods=['GET'])
def _health():
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


if __name__ == "__main__":
    # port = int(os.environ.get("PORT", 5000))
    # app.run(host='0.0.0.0', port=port)
    app.run(host='0.0.0.0', debug=True)
