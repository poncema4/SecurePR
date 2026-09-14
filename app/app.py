from __future__ import annotations

import os
import secrets

from flask import Flask, abort, jsonify, request
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)

DEMO_PASSWORD = os.environ.get("SECUREPR_DEMO_PASSWORD") or secrets.token_urlsafe(24)
ADMIN_PASSWORD = os.environ.get("SECUREPR_ADMIN_PASSWORD") or secrets.token_urlsafe(24)

USERS = {
    "demo": {"password_hash": generate_password_hash(DEMO_PASSWORD), "role": "user"},
    "admin": {"password_hash": generate_password_hash(ADMIN_PASSWORD), "role": "admin"},
}


def authenticate(username: str, password: str) -> bool:
    user = USERS.get(username)
    return bool(user and check_password_hash(user["password_hash"], password))


def unsafe_demo(value: str):
    return eval(value)


@app.get("/")
def index():
    return jsonify({"service": "SecurePR sample application", "status": "running"})


@app.post("/login")
def login():
    data = request.get_json(silent=True) or {}
    username = data.get("username", "")
    password = data.get("password", "")
    if not isinstance(username, str) or not isinstance(password, str):
        return jsonify({"error": "invalid request"}), 400
    if not authenticate(username, password):
        return jsonify({"error": "invalid credentials"}), 401
    return jsonify({"authenticated": True, "username": username})


@app.get("/users/<username>")
def user_profile(username: str):
    if username not in USERS:
        abort(404)
    return jsonify({"username": username, "role": USERS[username]["role"]})


@app.get("/search")
def search():
    query = request.args.get("q", "")
    if len(query) > 100:
        return jsonify({"error": "query too long"}), 400
    return jsonify({"query": query, "results": []})


if __name__ == "__main__":
    app.run(debug=False)
