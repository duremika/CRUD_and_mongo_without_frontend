from flask import Flask, Response, request
import pymongo
import json
from bson.objectid import ObjectId

app = Flask(__name__)

try:
	mongo = pymongo.MongoClient(
		host="localhost",
		port=27017,
		serverSelectionTimeoutMS=1000
	)
	mongo.server_info()
	db = mongo.company
except Exception as e:
	print(e)
	print("ERROR Can not connect to MongoDB")


@app.route("/users", methods=['GET'])
def get_some_users():
	try:
		data = list(db.users.find())
		for user in data:
			user["_id"] = str(user["_id"])
		
		return Response(
			response=json.dumps(data),
			status=200,
			mimetype="application/json")
	except Exception as ex:
		print(ex)
		return Response(
			response=json.dumps({"message": "Cannot read users"}),
			status=500,
			mimetype="application/json")


@app.route("/users", methods=['POST'])
def create_user():
	try:
		user = {
			"name": request.form["name"],
			"lastname": request.form["lastname"]
		}
		db.Response = db.users.insert_one(user)
		user_id = db.Response.inserted_id
		return Response(
			response=json.dumps(
				{"message": "user_created", "id": f"{user_id}"}),
			status=200,
			mimetype="application/json"
		)
	except Exception as ex:
		print(ex)


@app.route("/users/<user_id>", methods=['PATCH'])
def update_user(user_id):
	try:
		db_response = db.users.update_one(
			{"_id": ObjectId(user_id)},
			{"$set": {"name": request.form['name'], "lastname": request.form['lastname']}})
		if db_response.modified_count == 1:
			return Response(
				response=json.dumps({"message": "User updated"}),
				status=200,
				mimetype="application/json")
		else:
			return Response(
				response=json.dumps({"message": "Nothing update"}),
				status=500,
				mimetype="application/json")
	except Exception as ex:
		print(ex)
		return Response(
			response=json.dumps({"message": "Can not update user"}),
			status=500,
			mimetype="application/json"
		)


@app.route("/users/<user_id>", methods=['DELETE'])
def delete_user(user_id):
	try:
		db_response = db.users.delete_one({"_id": ObjectId(user_id)})
		if db_response.deleted_count == 1:
			return Response(
				response=json.dumps({"message": "User deleted", "id": f"{user_id}"}),
				status=200,
				mimetype="application/json"
			)
		else:
			return Response(
				response=json.dumps({"message": "User not found"}),
				status=500,
				mimetype="application/json"
			)
	except Exception as ex:
		print(ex)
		return Response(
			response=json.dumps({"message": "Can not delete user"}),
			status=500,
			mimetype="application/json"
		)


if __name__ == '__main__':
	app.run(port=80, debug=True)
