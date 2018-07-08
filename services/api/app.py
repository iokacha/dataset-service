from flask import Flask
from flask import request
from flask import jsonify
from flask_pymongo import PyMongo
from flask import Response
from utils import upload_dataset, csvify
import json
app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://mongo:27017/relevanc"
mongo = PyMongo(app)


# Create empty dataset with provided schema
@app.route('/dataset/<key>', methods=['POST'])
def create_dataset(key):
    schema = request.json
    is_inserted = mongo.db.datasets.insert({
        'key' : key,
        'schema' : schema,
        'data' : []
    })

    if is_inserted : 
        return jsonify({
            'status' : 200
        })
    else :
        return jsonify({
            'status' : 500
        })


# Get all recorded datasets 
@app.route('/dataset', methods=['GET'])
def get_all_available_datasets():
    r = mongo.db.datasets.find_one({}, {
            'key' : True, 
            'schema': True,
            'data' : True ,
            '_id': False
        })
    return jsonify({
            'results' : r,
            'status' : 200
        })


# Get a dataset schema by key
@app.route('/dataset/<key>/schema', methods=['GET'])
def get_dataset_by_key(key):
    r = mongo.db.datasets.find_one({
            'key' : str(key)
        }, {
            'key' : True,
            'schema' : True,
            '_id' : False
        })
    return jsonify({
            'results' : r,
            'status' : 200
        })



@app.route('/dataset/<key>/data', methods=['GET'])
def get_dataset_by_key__(key):
    r = mongo.db.datasets.find_one({
            'key' : str(key)
        }, {
            'data' : True,
            '_id' : False
        })
    return csvify(r['data'])

# Insert data into a dataset
@app.route('/dataset/<key>/data', methods=['POST'])
def upload_dataset_by_key(key):
    separator = request.args.get('separator', default='|')
    filepath = request.files['data']
    schema = mongo.db.datasets.find_one({
            'key' : str(key)
        }, {
            'schema' : True,
            '_id' : False
        })
    raw_data = upload_dataset(filepath, schema['schema'], separator)
    
    is_inserted = mongo.db.datasets.update({
        'key': key
        }, {
        '$push': {
            'data': {
                '$each' : raw_data
            }}
        })

    if is_inserted : 
        return jsonify({
            'status' : 200
        })
    else :
        return jsonify({
            'status' : 500
        })



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)

