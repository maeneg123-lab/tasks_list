from idlelib.history import History
from pstats import Stats
from tokenize import Comment
from unittest import result

import requests
from flask import Flask, jsonify, request
from database import SessionLocal, User, Subscription
from datetime import datetime, timedelta



app = Flask(__name__)
#пользователи
@app.route("/subscribe/<int:user_id>", methods=["GET"])
def get_subscribe(user_id):
    db = SessionLocal()
    try:
        result =[]
        subs = db.query(Subscription).filter(Subscription.user_id == user_id).all()
        if not subs:
            return jsonify({"error" : "subs not found"})
        for sub in subs:
            result.append({
                "id": sub.id,
                "user_id": sub.user_id,
                "renewal_date": sub.renewal_date,
                "cost": sub.cost,
                "name": sub.name,
            })
        return jsonify({"result" : result})
    finally:
        db.close()

@app.route("/subscribe", methods=["post"])
def add_subscribe():
    db = SessionLocal()
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data"})
        if "user_id" not in data:
            return jsonify({"error": "No user_id"})
        if "renewal_date" not in data:
            return jsonify({"error": "No renewal_date"})
        if "cost" not in data:
            return jsonify({"error": "No cost"})
        if "name" not in data:
            return jsonify({"error": "No name"})
        new_sub = Subscription(
            user_id=data["user_id"],
            renewal_date=data["renewal_date"],
            cost=data["cost"],
            name=data["name"],
        )
        db.add(new_sub)
        db.commit()
        db.refresh(new_sub)
        return jsonify({"result" : "success"})
    finally:
        db.close()

@app.route("/subscribe/<int:user_id>", methods=["PUT"])
def update_subscribe(user_id):
    db = SessionLocal()
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data"})
        if "renewal_date" not in data:
            return jsonify({"error": "No renewal_date"})
        sub = db.query(Subscription).filter(Subscription.user_id == user_id).first()
        if not sub:
            return jsonify({"error": "No sub "})
        sub.renewal_date = data["renewal_date"]
        db.commit()
        return jsonify({"result": "success"})
    finally:
        db.close()

@app.route("/subscribe/<int:user_id>", methods=["DELETE"])
def delete_subscribe(user_id):
    db = SessionLocal()
    try:
        sub = db.query(Subscription).filter(Subscription.user_id == user_id).first()
        if not sub:
            return jsonify({"error": "No sub "})
        db.delete(sub)
        db.commit()
        return jsonify({"success"})
    finally:
        db.close()


@app.route("/subscribe/<int:user_id>/expiring", methods=["GET"])
def get_subscribe_7(user_id):
    db = SessionLocal()
    try:
        today = datetime.now()
        result = []

        subs = db.query(Subscription).filter(Subscription.user_id == user_id).all()

        for sub in subs:
            days_left = (sub.renewal_date - today).days
            if 0 <= days_left < 7:  # подписки, которые истекают в ближайшие 7 дней
                result.append({
                    "id": sub.id,
                    "user_id": sub.user_id,
                    "name": sub.name,
                    "cost": sub.cost,
                    "renewal_date": sub.renewal_date.isoformat(),
                    "days_left": days_left
                })

        return jsonify({"result": result}), 200
    finally:
        db.close()


@app.route("/user", methods=["POST"])
def create_user():
    db = SessionLocal()
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data"})
        if "name" not in data:
            return jsonify({"error": "No name"})
        if "telegram_id" not in data:
            return jsonify({"error": "No telegram_id"})
        new_user = User(
            name=data["name"],
            telegram_id=data["telegram_id"],
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return jsonify({"result" : "success"})
    finally:
        db.close()


if __name__ == '__main__':
    app.run(debug=True)