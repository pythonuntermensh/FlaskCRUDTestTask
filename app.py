from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from bson.json_util import dumps
from bson.objectid import ObjectId
import os

MONGODB_URI = os.environ["MONGODB_ENDPOINT"]

app = Flask(__name__)
app.config["MONGO_URI"] = MONGODB_URI
mongo = PyMongo(app)

@app.route('/orders', methods=['GET'])
def get_orders():
    return jsonify({'message': 'success', 'data': dumps(mongo.db.items.find())}), 200

@app.route('/orders/<order_id>', methods=['GET'])
def get_order_by_id(order_id):
    return jsonify({'message': 'success', 'data': dumps(mongo.db.items.find_one({'_id': ObjectId(order_id)}))}), 200

@app.route('/orders', methods=['POST'])
def add_order():
    item = request.get_json()
    mongo.db.items.insert_one(item)
    return jsonify({'message': 'Order added successfully'}), 201

@app.route('/orders/<order_id>', methods=['PUT'])
def update_order(order_id):
    item = request.get_json()
    result = mongo.db.items.update_one({'_id': ObjectId(order_id)}, {'$set': item})
    if result.matched_count == 0:
        return jsonify({'error': 'Order not found'}), 404
    return jsonify({'message': 'Order was changed successfully'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)