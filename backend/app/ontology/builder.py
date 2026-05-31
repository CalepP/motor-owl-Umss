from rdflib import Graph, Namespace, RDF, RDFS, OWL, Literal, URIRef
from rdflib.namespace import XSD
import os

ANIMAL = Namespace("http://www.semanticweb.org/grupo10/animales#")
DBR    = Namespace("http://dbpedia.org/resource/")

ANIMALES = [
    {
        "id": "Leon",
        "labels": {
            "es": "León", "en": "Lion",
            "fr": "Lion", "pt": "Leão", "de": "Löwe"
        },
        "clase": "Mamifero",
        "dbpedia": "Lion"
    },
    {
        "id": "Delfin",
        "labels": {
            "es": "Delfín", "en": "Dolphin",
            "fr": "Dauphin", "pt": "Golfinho", "de": "Delfin"
        },
        "clase": "Mamifero",
        "dbpedia": "Dolphin"
    },
    {
        "id": "BallenaAzul",
        "labels": {
            "es": "Ballena Azul", "en": "Blue Whale",
            "fr": "Baleine bleue", "pt": "Baleia-azul", "de": "Blauwal"
        },
        "clase": "Mamifero",
        "dbpedia": "Blue_whale"
    },
    {
        "id": "Gorila",
        "labels": {
            "es": "Gorila", "en": "Gorilla",
            "fr": "Gorille", "pt": "Gorila", "de": "Gorilla"
        },
        "clase": "Mamifero",
        "dbpedia": "Gorilla"
    },
    {
        "id": "TigreBengala",
        "labels": {
            "es": "Tigre de Bengala", "en": "Bengal Tiger",
            "fr": "Tigre du Bengale", "pt": "Tigre-de-bengala", "de": "Bengalischer Tiger"
        },
        "clase": "Mamifero",
        "dbpedia": "Bengal_tiger"
    },
    {
        "id": "OsoPolar",
        "labels": {
            "es": "Oso Polar", "en": "Polar Bear",
            "fr": "Ours polaire", "pt": "Urso-polar", "de": "Eisbär"
        },
        "clase": "Mamifero",
        "dbpedia": "Polar_bear"
    },
    {
        "id": "Caballo",
        "labels": {
            "es": "Caballo", "en": "Horse",
            "fr": "Cheval", "pt": "Cavalo", "de": "Pferd"
        },
        "clase": "Mamifero",
        "dbpedia": "Horse"
    },
    {
        "id": "Perro",
        "labels": {
            "es": "Perro", "en": "Dog",
            "fr": "Chien", "pt": "Cachorro", "de": "Hund"
        },
        "clase": "Mamifero",
        "dbpedia": "Dog"
    },
    {
        "id": "AguilaReal",
        "labels": {
            "es": "Águila Real", "en": "Golden Eagle",
            "fr": "Aigle royal", "pt": "Águia-real", "de": "Steinadler"
        },
        "clase": "Ave",
        "dbpedia": "Golden_eagle"
    },
    {
        "id": "Pinguino",
        "labels": {
            "es": "Pingüino", "en": "Penguin",
            "fr": "Manchot", "pt": "Pinguim", "de": "Pinguin"
        },
        "clase": "Ave",
        "dbpedia": "Penguin"
    },
    {
        "id": "CocodriloNilo",
        "labels": {
            "es": "Cocodrilo del Nilo", "en": "Nile Crocodile",
            "fr": "Crocodile du Nil", "pt": "Crocodilo-do-nilo", "de": "Nilkrokodil"
        },
        "clase": "Reptil",
        "dbpedia": "Nile_crocodile"
    },
    {
        "id": "IguanaVerde",
        "labels": {
            "es": "Iguana Verde", "en": "Green Iguana",
            "fr": "Iguane vert", "pt": "Iguana-verde", "de": "Grüner Leguan"
        },
        "clase": "Reptil",
        "dbpedia": "Green_iguana"
    },
    {
        "id": "RanaArborea",
        "labels": {
            "es": "Rana Arbórea", "en": "Tree Frog",
            "fr": "Rainette", "pt": "Perereca", "de": "Laubfrosch"
        },
        "clase": "Anfibio",
        "dbpedia": "Tree_frog"
    },
    {
        "id": "SalmonAtlantico",
        "labels": {
            "es": "Salmón Atlántico", "en": "Atlantic Salmon",
            "fr": "Saumon atlantique", "pt": "Salmão-do-atlântico", "de": "Atlantischer Lachs"
        },
        "clase": "Pez",
        "dbpedia": "Atlantic_salmon"
    },
    {
        "id": "MariposaMonarca",
        "labels": {
            "es": "Mariposa Monarca", "en": "Monarch Butterfly",
            "fr": "Papillon monarque", "pt": "Borboleta-monarca", "de": "Monarchfalter"
        },
        "clase": "Insecto",
        "dbpedia": "Monarch_butterfly"
    },
]

def build_ontology():
    g = Graph()
    g.bind("animal", ANIMAL)
    g.bind("dbr",    DBR)
    g.bind("owl",    OWL)
    g.bind("rdfs",   RDFS)

    # Clases principales
    clases = ["Animal", "Mamifero", "Ave", "Reptil", "Anfibio", "Pez", "Insecto"]
    for clase in clases:
        uri = ANIMAL[clase]
        g.add((uri, RDF.type, OWL.Class))
        g.add((uri, RDFS.label, Literal(clase, lang="es")))

    # Subclases de Animal
    for subclase in ["Mamifero", "Ave", "Reptil", "Anfibio", "Pez", "Insecto"]:
        g.add((ANIMAL[subclase], RDFS.subClassOf, ANIMAL["Animal"]))

    # Individuos
    for a in ANIMALES:
        uri = ANIMAL[a["id"]]
        g.add((uri, RDF.type, OWL.NamedIndividual))
        g.add((uri, RDF.type, ANIMAL[a["clase"]]))
        g.add((uri, OWL.sameAs, DBR[a["dbpedia"]]))

        for lang, label in a["labels"].items():
            g.add((uri, RDFS.label, Literal(label, lang=lang)))

    return g

def save_ontology():
    g = build_ontology()
    out = os.path.join(os.path.dirname(__file__), "../../data/owl/animales.owl")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    g.serialize(destination=out, format="xml")
    print(f"✅ Ontología guardada en {out}")
    return out

if __name__ == "__main__":
    save_ontology()