from flask import jsonify, request
from bson import ObjectId
from config.database import db
from models.customer_model import serialize_customer, validate_customer_data

customers_collection = db["customers"]
# Controller

def index():
    customers = [serialize_customer(c) for c in customers_collection.find()]
    return jsonify(customers), 200

def show(customer_id):
    try:
        customer = customers_collection.find_one({"_id": ObjectId(customer_id)})
    except:
        return jsonify({"error": "Invalid ID format"}), 400

    if not customer:
        return jsonify({"error": "Customer not found"}), 404

    return jsonify(serialize_customer(customer)), 200

def store():
    data = request.json
    is_valid, result = validate_customer_data(data)

    if not is_valid:
        return jsonify({"errors": result}), 400 

    result_insert = customers_collection.insert_one(result)
    new_customer = customers_collection.find_one({"_id": result_insert.inserted_id})
    return jsonify(serialize_customer(new_customer)), 201


def update(customer_id):
    data = request.json
    is_valid, result = validate_customer_data(data, is_update=True)

    if not is_valid:
        return jsonify({"errors": result}), 400

    customers_collection.update_one(
        {"_id": ObjectId(customer_id)}, {"$set": result}
    )
    updated = customers_collection.find_one({"_id": ObjectId(customer_id)})
    return jsonify(serialize_customer(updated)), 200


def destroy(customer_id):
    try:
        result = customers_collection.delete_one({"_id": ObjectId(customer_id)})
    except:
        return jsonify({"error": "Invalid ID format"}), 400

    if result.deleted_count == 0:
        return jsonify({"error": "Customer not found"}), 404

    return jsonify({"message": "Customer deleted successfully"}), 200
