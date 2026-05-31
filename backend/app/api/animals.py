from flask import Blueprint, jsonify
from ..ontology.loader import get_all_animals, get_animal_by_id

bp = Blueprint("animals", __name__)

@bp.route("/", methods=["GET"])
def list_animals():
    animals = get_all_animals()
    return jsonify(animals)

@bp.route("/<animal_id>", methods=["GET"])
def get_animal(animal_id):
    animal = get_animal_by_id(animal_id)
    if not animal:
        return jsonify({"error": "Animal no encontrado"}), 404
    return jsonify(animal)