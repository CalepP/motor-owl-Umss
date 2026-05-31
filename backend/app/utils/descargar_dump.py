import json
import os
import time
from SPARQLWrapper import SPARQLWrapper, JSON

ENDPOINT = "https://dbpedia.org/sparql"
DUMP_FILE = os.path.join(os.path.dirname(__file__),
                         "../../data/dbpedia/animales_dump.json")

# URIs directas de animales conocidos en DBpedia
ANIMALES_URI = [
    "Dog", "Cat", "Lion", "Tiger", "Bear", "Wolf", "Fox", "Dolphin",
    "Blue_whale", "Gorilla", "Horse", "Golden_eagle", "Penguin",
    "Nile_crocodile", "Green_iguana", "Tree_frog", "Atlantic_salmon",
    "Monarch_butterfly", "Bengal_tiger", "Polar_bear", "German_Shepherd",
    "Labrador_Retriever", "Golden_Retriever", "Poodle", "Bulldog",
    "Beagle", "Chihuahua", "Rottweiler", "Siberian_Husky", "Dachshund",
    "Persian_cat", "Siamese_cat", "Maine_Coon", "Bengal_cat",
    "Great_white_shark", "Whale_shark", "Hammerhead_shark", "Bull_shark",
    "Tiger_shark", "Octopus", "Giant_squid", "Blue_ringed_octopus",
    "Green_sea_turtle", "Leatherback_sea_turtle", "Galapagos_tortoise",
    "King_cobra", "Black_mamba", "Anaconda", "Boa_constrictor",
    "Reticulated_python", "Komodo_dragon", "Gila_monster",
    "African_elephant", "Asian_elephant", "Giraffe", "Zebra",
    "Hippopotamus", "White_rhinoceros", "Black_rhinoceros",
    "Cheetah", "Leopard", "Jaguar", "Puma", "Snow_leopard",
    "Chimpanzee", "Bonobo", "Orangutan", "Gorilla", "Gibbon",
    "Kangaroo", "Koala", "Platypus", "Tasmanian_devil", "Wombat",
    "Clownfish", "Seahorse", "Manta_ray", "Stingray", "Piranha",
    "Swordfish", "Tuna", "Salmon", "Trout", "Catfish",
    "Bald_eagle", "Harpy_eagle", "Peregrine_falcon", "Osprey",
    "Great_horned_owl", "Barn_owl", "Snowy_owl",
    "Flamingo", "Toucan", "Peacock", "Ostrich", "Emu",
    "African_penguin", "Emperor_penguin", "King_penguin",
    "Hummingbird", "Ruby-throated_hummingbird",
    "Monarch_butterfly", "Blue_morpho_butterfly", "Painted_lady",
    "Honeybee", "Bumblebee", "Carpenter_bee",
    "Giant_panda", "Red_panda", "Spectacled_bear",
    "Orca", "Sperm_whale", "Humpback_whale", "Narwhal",
    "Sea_lion", "Walrus", "Harbor_seal", "Elephant_seal",
    "European_rabbit", "Snowshoe_hare", "Pika",
    "Red_fox", "Arctic_fox", "Gray_wolf", "Coyote", "Dingo",
    "Spotted_hyena", "Striped_hyena", "Aardwolf",
    "Giraffe", "Okapi", "Moose", "Reindeer", "White-tailed_deer",
    "American_bison", "Water_buffalo", "Yak",
    "Dromedary", "Bactrian_camel", "Llama", "Alpaca",
    "Capybara", "Beaver", "Giant_otter", "Sea_otter",
    "African_wild_dog", "Meerkat", "Mongoose",
    "Electric_eel", "Axolotl", "Poison_dart_frog",
    "Mantis_shrimp", "Horseshoe_crab", "Japanese_spider_crab",
    "Viper", "Rattlesnake", "Copperhead_snake", "Corn_snake",
    "Chameleon", "Gecko", "Bearded_dragon",
]

def _obtener_animal(uri_id, lang="es"):
    sparql = SPARQLWrapper(ENDPOINT)
    sparql.setTimeout(15)

    uri = f"http://dbpedia.org/resource/{uri_id}"

    q = f"""
    SELECT ?labelEn ?labelEs ?scientificName ?abstract
    WHERE {{
        <{uri}> rdfs:label ?labelEn .
        FILTER (lang(?labelEn) = "en")
        OPTIONAL {{
            <{uri}> rdfs:label ?labelEs .
            FILTER (lang(?labelEs) = "es")
        }}
        OPTIONAL {{
            <{uri}> <http://dbpedia.org/ontology/scientificName> ?scientificName .
        }}
        OPTIONAL {{
            <{uri}> <http://dbpedia.org/ontology/abstract> ?abstract .
            FILTER (lang(?abstract) = "es")
        }}
    }}
    LIMIT 1
    """

    sparql.setQuery(q)
    sparql.setReturnFormat(JSON)

    try:
        results = sparql.query().convert()
        bindings = results.get("results", {}).get("bindings", [])
        if not bindings:
            return None

        r        = bindings[0]
        label_en = r.get("labelEn",        {}).get("value", "")
        label_es = r.get("labelEs",        {}).get("value", "")
        sci      = r.get("scientificName", {}).get("value", "")
        abstract = r.get("abstract",       {}).get("value", "")

        if not label_en:
            return None

        return {
            "id":                uri_id,
            "uri":               uri,
            "nombre":            label_es if label_es else label_en,
            "labels":            {"en": label_en, "es": label_es} if label_es else {"en": label_en},
            "abstract":          abstract,
            "nombre_cientifico": sci,
            "same_as":           uri,
            "fuente":            "dbpedia"
        }

    except Exception as e:
        print(f"  ❌ Error con '{uri_id}': {e}")
        return None

def descargar_dump():
    print("🚀 Descargando dump de DBpedia por URI directa...")
    os.makedirs(os.path.dirname(DUMP_FILE), exist_ok=True)

    animales = []
    vistos   = set()

    for i, uri_id in enumerate(ANIMALES_URI):
        if uri_id in vistos:
            continue
        vistos.add(uri_id)

        print(f"  [{i+1}/{len(ANIMALES_URI)}] {uri_id}...")
        animal = _obtener_animal(uri_id)

        if animal:
            animales.append(animal)
            nombre = animal.get("nombre", "")