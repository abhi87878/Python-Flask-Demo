from flask import Flask, jsonify, request, abort
app = Flask(__name__)
items = [
    {"id": 1, "name": "Laptop","price": 5200},
    {"id": 2, "name": "Mobile","price": 1500}
]

@app.route("/")
def home():
    return {"message": "welcome to Flask Rest api"}

# get all the items
@app.route("/items", methods=["GET"])
def getitems():
    return jsonify(items)

# get item by id
@app.route("/items/<int:itemid>", methods=["GET"])
def getitem(itemid):
    item = next((item for item in items if item["id"] == itemid), None)
    if item:
        return jsonify(item)
    abort(404, description="item not found")

@app.route("/items", methods=["POST"])
def createitem():
    data = request.get_json()
    if not data or "name" not in data or "price" not in data:
        abort(400, description="invalid data")
    
    newid = items[-1]['id']+1 if items else 1
    item = {
        "id": newid,
        "name": request.json["name"],
        "price": float(request.json["price"])
    }
    items.append(item)
    return jsonify(item), 201
@app.route('/items/<int:itemid>',methods =['PUT'])
def updateitem(itemid):
    item = next((item for item in items if item["id"] == itemid), None)
    if item is None:
        abort(404)
    if not request.is_json:
        abort(400)
    item['name'] = request.json.get('name',item['name'])
    item['price'] = float(request.json.get('price', item['price']))
    return jsonify(item)
#delete item
@app.route('/items/<int:itemid>',methods =['DELETE'])
def deleteitem(itemid):
    global items
    items = [i for i in items if i["id"] != itemid]
    return jsonify({"message": "item deleted"}), 200
if __name__ == "__main__":
    app.run(debug=True)
