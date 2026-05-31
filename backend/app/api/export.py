from flask import Blueprint, jsonify, Response
from ..ontology.loader import get_ontology_graph

bp = Blueprint("export", __name__)

@bp.route("/jsonld", methods=["GET"])
def export_jsonld():
    g = get_ontology_graph()
    data = g.serialize(format="json-ld", indent=2)
    return Response(data, mimetype="application/ld+json")

@bp.route("/turtle", methods=["GET"])
def export_turtle():
    g = get_ontology_graph()
    data = g.serialize(format="turtle")
    return Response(data, mimetype="text/turtle")

@bp.route("/rdf", methods=["GET"])
def export_rdf():
    g = get_ontology_graph()
    data = g.serialize(format="xml")
    return Response(data, mimetype="application/rdf+xml")