from flask import Blueprint, request, jsonify
from . import db
from .models import Menu,PreparedDish,OrderedDish,Setdishes
from flask_cors import CORS


main_bp = Blueprint("main", __name__)
CORS(main_bp)

@main_bp.route("/", methods=["POST"])
def addFood():
    datas = request.get_json()
    prices = [Menu(dish_price = data) for data in datas]
    db.session.bulk_save_objects(prices)
    db.session.commit()
    return jsonify({"message": "Prices successfully!"}), 201

@main_bp.route("/get-food", methods=["GET"])
def get_users():
    users = Menu.query.all()
    return jsonify([u.to_dict() for u in users]), 200

@main_bp.route("/setPreparedFood", methods=["POST"])
def set_prepared_food():
    data = request.get_json();
    set_data = PreparedDish(image = data.get("image"), description=data.get("description"), price=data.get("price"))
    db.session.add(set_data)
    db.session.commit()
    return jsonify({"message": "food prepared successfully!"}), 201

@main_bp.route("/getPreparedFood", methods=["GET"])
def get_prepared_food():
    users = PreparedDish.query.all()
    return jsonify([u.to_dict() for u in users]), 200

@main_bp.route("/deletePreparedFood", methods=["POST"])
def delete_prepared_food():
    data = request.get_json()
    food = PreparedDish.query.filter_by(id=data.get("id")).first()
    if food:
        db.session.delete(food)  # ✅ correct method
        db.session.commit()
        return jsonify({"message": "Food deleted successfully"})
    else:
        return jsonify({"error": "Dish not found"}), 404

@main_bp.route("/orderFood", methods=["POST"])
def orderFood():
    try:
        data = request.get_json()
        image = data.get("image")
        description = data.get("description")
        price = data.get("price")

        # Input validation
        if not image or not description or not price:
            return jsonify({"error": "Missing fields"}), 400

        # Check if dish already ordered
        existing_order = OrderedDish.query.filter_by(image=image).first()

        if existing_order:
            existing_order.quantity += 1
            db.session.commit()
            return jsonify({"message": "Dish quantity updated successfully!"})

        # New order
        new_order = OrderedDish(
            image=image,
            description=description,
            price=price,
            quantity=1  # default
        )
        db.session.add(new_order)
        db.session.commit()
        return jsonify({"message": "Dish ordered successfully!"})

    except Exception as e:
        print("Error:", e)
        return jsonify({"error": "Internal server error"}), 500
    
@main_bp.route("/getOrderedDish", methods=["GET"])
def getOrderedDish():
    ordered_dish = OrderedDish.query.all()
    return jsonify([u.to_dict() for u in ordered_dish]), 200

@main_bp.route("/payBill", methods=["POST"])
def payBills():
    data = request.get_json();
    ids = data.get("id", [])

    if not ids :
        return jsonify({"message" : "No IDs provided"})
    try:
        for id in ids:
            orderedFoodId = OrderedDish.query.get(id)
            if orderedFoodId:
                db.session.delete(orderedFoodId)
                db.session.commit()
        return jsonify({"message" : "bills of selected items are paid"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)})

@main_bp.route("/setCooked", methods=["POST"])
def setCooked():
    datas = request.get_json()
    new_cook = [Setdishes(Setdishes = data) for data in datas]
    db.session.add(new_cook)
    db.session.commit()
    return jsonify({"message" : "set cook "})

@main_bp.route("/setOrdered", methods=["POST"])
def setOrdered():
    datas = request.get_json()
    new_order = [Setdishes(setOrdered = data) for data in datas]
    db.session.add(new_order)
    db.session.commit()
    return jsonify({"message" : "set order"})

@main_bp.route("/get_dish_status", methods=["GET"])
def getStatus():
    dish = Setdishes.query.all()
    return jsonify([d.to_dict() for d in dish]), 200

@main_bp.route("/reebotapp")
def rebootingApp():
    db.session.query(Menu).delete()
    db.session.query(PreparedDish).delete()
    db.session.query(OrderedDish).delete()
    db.session.commit();
    return("delete successfully")