from flask import Blueprint, request, jsonify, url_for


# routes.py files will contain the endpoints for the blueprint we have
# core directory will store all pages in DragonFlow's '/' root

# establishing a blueprint, its prefix-url and its endpoint
core = Blueprint("core", __name__)
@core.route("/")
def index():
    return {"Hello": "DragonFlow"}