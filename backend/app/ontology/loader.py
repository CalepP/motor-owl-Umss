import os
from rdflib import Graph, Namespace, RDF, RDFS, OWL, Literal
from rdflib.namespace import SKOS

# Namespaces
ANIMAL = Namespace("http://www.semanticweb.org/grupo10/animales#")
DBR    = Namespace("http://dbpedia.org/resource/")

OWL_FILE = os.path.join(os.path.dirname(__file__), 
                        "../../data/owl/animales.owl")

_graph = None

def get_ontology_graph():
    global _graph
    if _graph is None:
        _graph = Graph()
        if os.path.exists(OWL_FILE):
            _graph.parse(OWL_FILE, format="xml")
    return _graph

def get_all_animals():
    g = get_ontology_graph()
    animals = []

    for subj in g.subjects(RDF.type, OWL.NamedIndividual):
        animal = _build_animal_dict(g, subj)
        if animal:
            animals.append(animal)

    return sorted(animals, key=lambda x: x["nombre"])

def get_animal_by_id(animal_id):
    g = get_ontology_graph()
    uri = ANIMAL[animal_id]

    if (uri, RDF.type, OWL.NamedIndividual) not in g:
        return None

    return _build_animal_dict(g, uri)

def search_local(query, lang="es"):
    g = get_ontology_graph()
    results = []
    query_lower = query.lower()

    for subj in g.subjects(RDF.type, OWL.NamedIndividual):
        for label in g.objects(subj, RDFS.label):
            if (hasattr(label, 'language') and
                label.language == lang and
                query_lower in str(label).lower()):
                animal = _build_animal_dict(g, subj)
                if animal:
                    results.append(animal)
                break

    return results

def _build_animal_dict(g, uri):
    labels = {}
    for label in g.objects(uri, RDFS.label):
        if hasattr(label, 'language') and label.language:
            labels[label.language] = str(label)

    if not labels:
        return None

    same_as = str(next(g.objects(uri, OWL.sameAs), ""))
    nombre  = labels.get("es") or next(iter(labels.values()))

    return {
        "id":       str(uri).split("#")[-1],
        "uri":      str(uri),
        "nombre":   nombre,
        "labels":   labels,
        "same_as":  same_as,
        "fuente":   "local"
    }