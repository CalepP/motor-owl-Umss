from rdflib import Graph, Namespace, RDF, RDFS, OWL, Literal, URIRef
from rdflib.namespace import XSD, FOAF
import os

ANIMAL = Namespace("http://www.semanticweb.org/grupo10/animales#")
DBR    = Namespace("http://dbpedia.org/resource/")
DBO    = Namespace("http://dbpedia.org/ontology/")

# 15 individuos con labels en 5 idiomas
ANIMALES = [
    {
        "id": "Leon",
        "labels": {"es": "León", "en": "Lion", "fr": "Lion", "pt": "Leão", "de": "Löwe"},
        "clase": "Felino",
        "dbpedia": "Lion",
        "dieta": "Carnivoro"
    },
    {
        "id": "Delfin",
        "labels": {"es": "Delfín", "en": "Dolphin", "fr": "Dauphin", "pt": "Golfinho", "de": "Delfin"},
        "clase": "Cetaceo",
        "dbpedia": "Dolphin",
        "dieta": "Carnivoro"
    },
    {
        "id": "BallenaAzul",
        "labels": {"es": "Ballena Azul", "en": "Blue Whale", "fr": "Baleine bleue", "pt": "Baleia-azul", "de": "Blauwal"},
        "clase": "Cetaceo",
        "dbpedia": "Blue_whale",
        "dieta": "Carnivoro"
    },
    {
        "id": "Gorila",
        "labels": {"es": "Gorila", "en": "Gorilla", "fr": "Gorille", "pt": "Gorila", "de": "Gorilla"},
        "clase": "Primate",
        "dbpedia": "Gorilla",
        "dieta": "Herbivoro"
    },
    {
        "id": "TigreBengala",
        "labels": {"es": "Tigre de Bengala", "en": "Bengal Tiger", "fr": "Tigre du Bengale", "pt": "Tigre-de-bengala", "de": "Bengalischer Tiger"},
        "clase": "Felino",
        "dbpedia": "Bengal_tiger",
        "dieta": "Carnivoro"
    },
    {
        "id": "OsoPolar",
        "labels": {"es": "Oso Polar", "en": "Polar Bear", "fr": "Ours polaire", "pt": "Urso-polar", "de": "Eisbär"},
        "clase": "Mamifero",
        "dbpedia": "Polar_bear",
        "dieta": "Carnivoro"
    },
    {
        "id": "Caballo",
        "labels": {"es": "Caballo", "en": "Horse", "fr": "Cheval", "pt": "Cavalo", "de": "Pferd"},
        "clase": "Mamifero",
        "dbpedia": "Horse",
        "dieta": "Herbivoro"
    },
    {
        "id": "Perro",
        "labels": {"es": "Perro", "en": "Dog", "fr": "Chien", "pt": "Cachorro", "de": "Hund"},
        "clase": "Mamifero",
        "dbpedia": "Dog",
        "dieta": "Omnivoro"
    },
    {
        "id": "AguilaReal",
        "labels": {"es": "Águila Real", "en": "Golden Eagle", "fr": "Aigle royal", "pt": "Águia-real", "de": "Steinadler"},
        "clase": "AveRapaz",
        "dbpedia": "Golden_eagle",
        "dieta": "Carnivoro"
    },
    {
        "id": "Pinguino",
        "labels": {"es": "Pingüino", "en": "Penguin", "fr": "Manchot", "pt": "Pinguim", "de": "Pinguin"},
        "clase": "Ave",
        "dbpedia": "Penguin",
        "dieta": "Carnivoro"
    },
    {
        "id": "CocodriloNilo",
        "labels": {"es": "Cocodrilo del Nilo", "en": "Nile Crocodile", "fr": "Crocodile du Nil", "pt": "Crocodilo-do-nilo", "de": "Nilkrokodil"},
        "clase": "Cocodrilo",
        "dbpedia": "Nile_crocodile",
        "dieta": "Carnivoro"
    },
    {
        "id": "IguanaVerde",
        "labels": {"es": "Iguana Verde", "en": "Green Iguana", "fr": "Iguane vert", "pt": "Iguana-verde", "de": "Grüner Leguan"},
        "clase": "Reptil",
        "dbpedia": "Green_iguana",
        "dieta": "Herbivoro"
    },
    {
        "id": "RanaArborea",
        "labels": {"es": "Rana Arbórea", "en": "Tree Frog", "fr": "Rainette", "pt": "Perereca", "de": "Laubfrosch"},
        "clase": "Anfibio",
        "dbpedia": "Tree_frog",
        "dieta": "Carnivoro"
    },
    {
        "id": "SalmonAtlantico",
        "labels": {"es": "Salmón Atlántico", "en": "Atlantic Salmon", "fr": "Saumon atlantique", "pt": "Salmão-do-atlântico", "de": "Atlantischer Lachs"},
        "clase": "Pez",
        "dbpedia": "Atlantic_salmon",
        "dieta": "Carnivoro"
    },
    {
        "id": "MariposaMonarca",
        "labels": {"es": "Mariposa Monarca", "en": "Monarch Butterfly", "fr": "Papillon monarque", "pt": "Borboleta-monarca", "de": "Monarchfalter"},
        "clase": "Insecto",
        "dbpedia": "Monarch_butterfly",
        "dieta": "Herbivoro"
    },
]

# ─────────────────────────────────────────────────────────────────────────────
# 22 CLASES organizadas jerárquicamente
# ─────────────────────────────────────────────────────────────────────────────
CLASES = [
    # Raíz
    {
        "id": "Animal", "parent": None,
        "labels": {"es": "Animal", "en": "Animal", "fr": "Animal", "pt": "Animal", "de": "Tier"},
        "dbo": "Animal",
        "comment": {"es": "Clase raíz que representa a todos los animales del reino Animalia."}
    },
    # 6 clases básicas (subclases directas de Animal)
    {
        "id": "Mamifero", "parent": "Animal",
        "labels": {"es": "Mamífero", "en": "Mammal", "fr": "Mammifère", "pt": "Mamífero", "de": "Säugetier"},
        "dbo": "Mammal",
        "comment": {"es": "Vertebrado de sangre caliente que alimenta a sus crías con leche materna."}
    },
    {
        "id": "Ave", "parent": "Animal",
        "labels": {"es": "Ave", "en": "Bird", "fr": "Oiseau", "pt": "Ave", "de": "Vogel"},
        "dbo": "Bird",
        "comment": {"es": "Vertebrado ovíparo con plumas, pico y extremidades anteriores adaptadas como alas."}
    },
    {
        "id": "Reptil", "parent": "Animal",
        "labels": {"es": "Reptil", "en": "Reptile", "fr": "Reptile", "pt": "Réptil", "de": "Reptil"},
        "dbo": "Reptile",
        "comment": {"es": "Vertebrado ectotermo con escamas o placas córneas."}
    },
    {
        "id": "Anfibio", "parent": "Animal",
        "labels": {"es": "Anfibio", "en": "Amphibian", "fr": "Amphibien", "pt": "Anfíbio", "de": "Amphibie"},
        "dbo": "Amphibian",
        "comment": {"es": "Vertebrado ectotermo que puede vivir en agua y en tierra."}
    },
    {
        "id": "Pez", "parent": "Animal",
        "labels": {"es": "Pez", "en": "Fish", "fr": "Poisson", "pt": "Peixe", "de": "Fisch"},
        "dbo": "Fish",
        "comment": {"es": "Vertebrado acuático con branquias y aletas."}
    },
    {
        "id": "Insecto", "parent": "Animal",
        "labels": {"es": "Insecto", "en": "Insect", "fr": "Insecte", "pt": "Inseto", "de": "Insekt"},
        "dbo": "Insect",
        "comment": {"es": "Artrópodo con tres pares de patas y cuerpo dividido en cabeza, tórax y abdomen."}
    },
    # 5 subclases de Mamifero
    {
        "id": "Cetaceo", "parent": "Mamifero",
        "labels": {"es": "Cetáceo", "en": "Cetacean", "fr": "Cétacé", "pt": "Cetáceo", "de": "Wal"},
        "dbo": None,
        "comment": {"es": "Mamífero marino del orden Cetacea; incluye ballenas, delfines y marsopas."}
    },
    {
        "id": "Felino", "parent": "Mamifero",
        "labels": {"es": "Felino", "en": "Feline", "fr": "Félin", "pt": "Felino", "de": "Felide"},
        "dbo": None,
        "comment": {"es": "Mamífero carnívoro de la familia Felidae; incluye leones, tigres y gatos."}
    },
    {
        "id": "Primate", "parent": "Mamifero",
        "labels": {"es": "Primate", "en": "Primate", "fr": "Primate", "pt": "Primata", "de": "Primat"},
        "dbo": None,
        "comment": {"es": "Mamífero del orden Primates; incluye humanos, simios y monos."}
    },
    {
        "id": "Roedor", "parent": "Mamifero",
        "labels": {"es": "Roedor", "en": "Rodent", "fr": "Rongeur", "pt": "Roedor", "de": "Nagetier"},
        "dbo": None,
        "comment": {"es": "Mamífero del orden Rodentia con dientes incisivos de crecimiento continuo."}
    },
    {
        "id": "Marsupial", "parent": "Mamifero",
        "labels": {"es": "Marsupial", "en": "Marsupial", "fr": "Marsupial", "pt": "Marsupial", "de": "Beuteltier"},
        "dbo": None,
        "comment": {"es": "Mamífero que cría a sus hijos en una bolsa o marsupio; ej. canguro y koala."}
    },
    # 1 subclase de Ave
    {
        "id": "AveRapaz", "parent": "Ave",
        "labels": {"es": "Ave Rapaz", "en": "Bird of Prey", "fr": "Rapace", "pt": "Ave de Rapina", "de": "Greifvogel"},
        "dbo": None,
        "comment": {"es": "Ave carnívora con pico ganchudo y garras afiladas; ej. águilas y halcones."}
    },
    # 2 subclases de Reptil
    {
        "id": "Cocodrilo", "parent": "Reptil",
        "labels": {"es": "Cocodrilo", "en": "Crocodilian", "fr": "Crocodilien", "pt": "Crocodiliano", "de": "Krokodil"},
        "dbo": None,
        "comment": {"es": "Reptil del orden Crocodilia; semiacuático y de gran tamaño."}
    },
    {
        "id": "Serpiente", "parent": "Reptil",
        "labels": {"es": "Serpiente", "en": "Snake", "fr": "Serpent", "pt": "Serpente", "de": "Schlange"},
        "dbo": None,
        "comment": {"es": "Reptil escamoso sin extremidades del suborden Serpentes."}
    },
    # 4 clases de invertebrados
    {
        "id": "Invertebrado", "parent": "Animal",
        "labels": {"es": "Invertebrado", "en": "Invertebrate", "fr": "Invertébré", "pt": "Invertebrado", "de": "Wirbelloser"},
        "dbo": None,
        "comment": {"es": "Animal que carece de columna vertebral; constituye el 97% de las especies animales."}
    },
    {
        "id": "Aracnido", "parent": "Invertebrado",
        "labels": {"es": "Arácnido", "en": "Arachnid", "fr": "Arachnide", "pt": "Arácnido", "de": "Spinnentier"},
        "dbo": None,
        "comment": {"es": "Artrópodo con cuatro pares de patas; incluye arañas, escorpiones y ácaros."}
    },
    {
        "id": "Crustaceo", "parent": "Invertebrado",
        "labels": {"es": "Crustáceo", "en": "Crustacean", "fr": "Crustacé", "pt": "Crustáceo", "de": "Krebstier"},
        "dbo": None,
        "comment": {"es": "Artrópodo con exoesqueleto de quitina y dos pares de antenas; ej. cangrejos y langostas."}
    },
    {
        "id": "Molusco", "parent": "Invertebrado",
        "labels": {"es": "Molusco", "en": "Mollusk", "fr": "Mollusque", "pt": "Molusco", "de": "Weichtier"},
        "dbo": None,
        "comment": {"es": "Invertebrado de cuerpo blando, frecuentemente protegido por una concha; ej. pulpos y caracoles."}
    },
    # 3 clases por dieta (disjuntas entre sí, subclases de Animal)
    {
        "id": "Carnivoro", "parent": "Animal",
        "labels": {"es": "Carnívoro", "en": "Carnivore", "fr": "Carnivore", "pt": "Carnívoro", "de": "Fleischfresser"},
        "dbo": None,
        "comment": {"es": "Animal cuya dieta consiste principalmente en carne de otros animales."}
    },
    {
        "id": "Herbivoro", "parent": "Animal",
        "labels": {"es": "Herbívoro", "en": "Herbivore", "fr": "Herbivore", "pt": "Herbívoro", "de": "Pflanzenfresser"},
        "dbo": None,
        "comment": {"es": "Animal cuya dieta consiste exclusivamente en plantas y vegetales."}
    },
    {
        "id": "Omnivoro", "parent": "Animal",
        "labels": {"es": "Omnívoro", "en": "Omnivore", "fr": "Omnivore", "pt": "Onívoro", "de": "Allesfresser"},
        "dbo": None,
        "comment": {"es": "Animal que consume tanto plantas como carne de otros animales."}
    },
]

# ─────────────────────────────────────────────────────────────────────────────
# 18 PROPIEDADES: 10 DatatypeProperties + 8 ObjectProperties
# ─────────────────────────────────────────────────────────────────────────────
DATATYPE_PROPERTIES = [
    {
        "id": "nombreCientifico",
        "labels": {"es": "Nombre Científico", "en": "Scientific Name", "fr": "Nom Scientifique", "pt": "Nome Científico", "de": "Wissenschaftlicher Name"},
        "domain": "Animal", "range": XSD.string, "dbo": "scientificName"
    },
    {
        "id": "habitat",
        "labels": {"es": "Hábitat", "en": "Habitat", "fr": "Habitat", "pt": "Habitat", "de": "Lebensraum"},
        "domain": "Animal", "range": XSD.string, "dbo": "habitat"
    },
    {
        "id": "estadoConservacion",
        "labels": {"es": "Estado de Conservación", "en": "Conservation Status", "fr": "Statut de Conservation", "pt": "Estado de Conservação", "de": "Erhaltungszustand"},
        "domain": "Animal", "range": XSD.string, "dbo": "conservationStatus"
    },
    {
        "id": "esperanzaVida",
        "labels": {"es": "Esperanza de Vida", "en": "Life Expectancy", "fr": "Espérance de Vie", "pt": "Expectativa de Vida", "de": "Lebenserwartung"},
        "domain": "Animal", "range": XSD.string, "dbo": "lifeExpectancy"
    },
    {
        "id": "pesoPromedio",
        "labels": {"es": "Peso Promedio", "en": "Average Weight", "fr": "Poids Moyen", "pt": "Peso Médio", "de": "Durchschnittsgewicht"},
        "domain": "Animal", "range": XSD.string, "dbo": None
    },
    {
        "id": "longitudPromedio",
        "labels": {"es": "Longitud Promedio", "en": "Average Length", "fr": "Longueur Moyenne", "pt": "Comprimento Médio", "de": "Durchschnittslänge"},
        "domain": "Animal", "range": XSD.string, "dbo": None
    },
    {
        "id": "regionNativa",
        "labels": {"es": "Región Nativa", "en": "Native Region", "fr": "Région Natale", "pt": "Região Nativa", "de": "Heimatregion"},
        "domain": "Animal", "range": XSD.string, "dbo": None
    },
    {
        "id": "descripcion",
        "labels": {"es": "Descripción", "en": "Description", "fr": "Description", "pt": "Descrição", "de": "Beschreibung"},
        "domain": "Animal", "range": XSD.string, "dbo": "abstract"
    },
    {
        "id": "tipoLocomocion",
        "labels": {"es": "Tipo de Locomoción", "en": "Locomotion Type", "fr": "Type de Locomotion", "pt": "Tipo de Locomoção", "de": "Fortbewegungsart"},
        "domain": "Animal", "range": XSD.string, "dbo": None
    },
    {
        "id": "comportamientoSocial",
        "labels": {"es": "Comportamiento Social", "en": "Social Behaviour", "fr": "Comportement Social", "pt": "Comportamento Social", "de": "Sozialverhalten"},
        "domain": "Animal", "range": XSD.string, "dbo": None
    },
]

OBJECT_PROPERTIES = [
    {
        "id": "imagenRepresentativa",
        "labels": {"es": "Imagen Representativa", "en": "Representative Image", "fr": "Image Représentative", "pt": "Imagem Representativa", "de": "Repräsentatives Bild"},
        "domain": "Animal", "range": None, "dbo": "thumbnail"
    },
    {
        "id": "ordenTaxonomico",
        "labels": {"es": "Orden Taxonómico", "en": "Taxonomic Order", "fr": "Ordre Taxonomique", "pt": "Ordem Taxonômica", "de": "Taxonomische Ordnung"},
        "domain": "Animal", "range": None, "dbo": None
    },
    {
        "id": "familiaTaxonomica",
        "labels": {"es": "Familia Taxonómica", "en": "Taxonomic Family", "fr": "Famille Taxonomique", "pt": "Família Taxonômica", "de": "Taxonomische Familie"},
        "domain": "Animal", "range": None, "dbo": None
    },
    {
        "id": "claseTaxonomica",
        "labels": {"es": "Clase Taxonómica", "en": "Taxonomic Class", "fr": "Classe Taxonomique", "pt": "Classe Taxonômica", "de": "Taxonomische Klasse"},
        "domain": "Animal", "range": None, "dbo": None
    },
    {
        "id": "filumTaxonomico",
        "labels": {"es": "Filo Taxonómico", "en": "Taxonomic Phylum", "fr": "Phylum Taxonomique", "pt": "Filo Taxonômico", "de": "Taxonomisches Phylum"},
        "domain": "Animal", "range": None, "dbo": None
    },
    {
        "id": "tieneDepredador",
        "labels": {"es": "Tiene Depredador", "en": "Has Predator", "fr": "A un Prédateur", "pt": "Tem Predador", "de": "Hat Raubtier"},
        "domain": "Animal", "range": "Animal", "dbo": None
    },
    {
        "id": "esPresa",
        "labels": {"es": "Es Presa de", "en": "Is Prey of", "fr": "Est la Proie de", "pt": "É Presa de", "de": "Ist Beute von"},
        "domain": "Animal", "range": "Animal", "dbo": None
    },
    {
        "id": "vivenEn",
        "labels": {"es": "Viven en", "en": "Live in", "fr": "Vivent dans", "pt": "Vivem em", "de": "Leben in"},
        "domain": "Animal", "range": None, "dbo": "habitat"
    },
]

# owl:equivalentClass para clases que tienen mapeo a DBpedia
EQUIVALENCIAS_DBO = {
    "Animal":   "Animal",
    "Mamifero": "Mammal",
    "Ave":      "Bird",
    "Reptil":   "Reptile",
    "Anfibio":  "Amphibian",
    "Pez":      "Fish",
    "Insecto":  "Insect",
}


def build_ontology():
    g = Graph()
    g.bind("animal", ANIMAL)
    g.bind("dbr",    DBR)
    g.bind("dbo",    DBO)
    g.bind("owl",    OWL)
    g.bind("rdfs",   RDFS)
    g.bind("xsd",    XSD)
    g.bind("foaf",   FOAF)

    # ── Ontología principal ──────────────────────────────────────────────────
    onto_uri = ANIMAL["Ontologia_Animales"]
    g.add((onto_uri, RDF.type, OWL.Ontology))
    g.add((onto_uri, RDFS.label, Literal("Ontología de Animales - Grupo 10 UMSS", lang="es")))
    g.add((onto_uri, RDFS.comment, Literal(
        "Ontología OWL que modela el reino animal con 22 clases, 18 propiedades y 15 individuos. "
        "Alineada con DBpedia mediante owl:equivalentClass y owl:sameAs.",
        lang="es"
    )))

    # ── 22 Clases con owl:equivalentClass donde aplica ───────────────────────
    for cls in CLASES:
        uri = ANIMAL[cls["id"]]
        g.add((uri, RDF.type, OWL.Class))

        for lang, label in cls["labels"].items():
            g.add((uri, RDFS.label, Literal(label, lang=lang)))

        comment_es = cls.get("comment", {}).get("es", "")
        if comment_es:
            g.add((uri, RDFS.comment, Literal(comment_es, lang="es")))

        if cls["parent"]:
            g.add((uri, RDFS.subClassOf, ANIMAL[cls["parent"]]))

        if cls.get("dbo"):
            g.add((uri, OWL.equivalentClass, DBO[cls["dbo"]]))

    # ── 10 DatatypeProperties ────────────────────────────────────────────────
    for prop in DATATYPE_PROPERTIES:
        uri = ANIMAL[prop["id"]]
        g.add((uri, RDF.type, OWL.DatatypeProperty))
        for lang, label in prop["labels"].items():
            g.add((uri, RDFS.label, Literal(label, lang=lang)))
        g.add((uri, RDFS.domain, ANIMAL[prop["domain"]]))
        g.add((uri, RDFS.range,  prop["range"]))
        if prop.get("dbo"):
            g.add((uri, OWL.equivalentProperty, DBO[prop["dbo"]]))

    # ── 8 ObjectProperties ───────────────────────────────────────────────────
    for prop in OBJECT_PROPERTIES:
        uri = ANIMAL[prop["id"]]
        g.add((uri, RDF.type, OWL.ObjectProperty))
        for lang, label in prop["labels"].items():
            g.add((uri, RDFS.label, Literal(label, lang=lang)))
        g.add((uri, RDFS.domain, ANIMAL[prop["domain"]]))
        if prop.get("range") and isinstance(prop["range"], str):
            g.add((uri, RDFS.range, ANIMAL[prop["range"]]))
        if prop.get("dbo"):
            g.add((uri, OWL.equivalentProperty, DBO[prop["dbo"]]))

    # ── 15 Individuos ────────────────────────────────────────────────────────
    for a in ANIMALES:
        uri = ANIMAL[a["id"]]
        g.add((uri, RDF.type, OWL.NamedIndividual))
        g.add((uri, RDF.type, ANIMAL[a["clase"]]))
        # Tipo de dieta como clase adicional
        if a.get("dieta"):
            g.add((uri, RDF.type, ANIMAL[a["dieta"]]))
        # owl:sameAs a DBpedia
        g.add((uri, OWL.sameAs, DBR[a["dbpedia"]]))
        for lang, label in a["labels"].items():
            g.add((uri, RDFS.label, Literal(label, lang=lang)))

    return g


def save_ontology():
    g = build_ontology()
    out = os.path.join(os.path.dirname(__file__), "../../data/owl/animales.owl")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    g.serialize(destination=out, format="xml")
    n_clases = len(CLASES)
    n_props  = len(DATATYPE_PROPERTIES) + len(OBJECT_PROPERTIES)
    n_indiv  = len(ANIMALES)
    print(f"OK Ontologia guardada: {n_clases} clases, {n_props} propiedades, {n_indiv} individuos -> {out}")
    return out


if __name__ == "__main__":
    save_ontology()
