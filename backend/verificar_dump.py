import json
import os
import time
from SPARQLWrapper import SPARQLWrapper, JSON

ENDPOINT = "https://dbpedia.org/sparql"
DUMP_FILE = "data/dbpedia/animales_dump.json"

ANIMALES_URI = [
    "Dog", "Cat", "Lion", "Tiger", "Bear", "Wolf", "Fox", "Dolphin",
    "Blue_whale", "Gorilla", "Horse", "Golden_eagle", "Penguin",
    "Nile_crocodile", "Green_iguana", "Tree_frog", "Atlantic_salmon",
    "Monarch_butterfly", "Bengal_tiger", "Polar_bear", "German_Shepherd",
    "Labrador_Retriever", "Golden_Retriever", "Poodle", "Bulldog",
    "Beagle", "Chihuahua", "Rottweiler", "Siberian_Husky", "Dachshund",
    "Persian_cat", "Siamese_cat", "Maine_Coon", "Bengal_cat",
    "Great_white_shark", "Whale_shark", "Hammerhead_shark", "Bull_shark",
    "Tiger_shark", "Octopus", "Giant_squid", "Green_sea_turtle",
    "Leatherback_sea_turtle", "King_cobra", "Black_mamba", "Anaconda",
    "Boa_constrictor", "Reticulated_python", "Komodo_dragon",
    "African_elephant", "Asian_elephant", "Giraffe", "Zebra",
    "Hippopotamus", "White_rhinoceros", "Black_rhinoceros",
    "Cheetah", "Leopard", "Jaguar", "Puma", "Snow_leopard",
    "Chimpanzee", "Orangutan", "Kangaroo", "Koala", "Platypus",
    "Clownfish", "Seahorse", "Piranha", "Swordfish", "Tuna", "Salmon",
    "Bald_eagle", "Harpy_eagle", "Peregrine_falcon", "Great_horned_owl",
    "Barn_owl", "Flamingo", "Toucan", "Ostrich", "Emperor_penguin",
    "Hummingbird", "Honeybee", "Giant_panda", "Red_panda", "Orca",
    "Sperm_whale", "Humpback_whale", "Narwhal", "Sea_lion", "Walrus",
    "Harbor_seal", "European_rabbit", "Red_fox", "Arctic_fox",
    "Gray_wolf", "Coyote", "Spotted_hyena", "Moose", "Reindeer",
    "American_bison", "Dromedary", "Llama", "Capybara", "Beaver",
    "Giant_otter", "Meerkat", "Electric_eel", "Axolotl",
    "Poison_dart_frog", "Viper", "Rattlesnake", "Chameleon", "Gecko",
]

animales = []

for i, uri_id in enumerate(ANIMALES_URI):
    sparql = SPARQLWrapper(ENDPOINT)
    sparql.setTimeout(15)
    uri = f"http://dbpedia.org/resource/{uri_id}"

    q = f"""
    SELECT ?labelEn ?labelEs ?abstract
    WHERE {{
        <{uri}> rdfs:label ?labelEn .
        FILTER (lang(?labelEn) = "en")
        OPTIONAL {{
            <{uri}> rdfs:label ?labelEs .
            FILTER (lang(?labelEs) = "es")
        }}
        OPTIONAL {{
            <{uri}> <http://dbpedia.org/ontology/abstract> ?abstract .
            FILTER (lang(?abstract) = "es")
        }}
    }} LIMIT 1
    """

    sparql.setQuery(q)
    sparql.setReturnFormat(JSON)

    try:
        results = sparql.query().convert()
        bindings = results.get("results", {}).get("bindings", [])
        if bindings:
            r        = bindings[0]
            label_en = r.get("labelEn", {}).get("value", "")
            label_es = r.get("labelEs", {}).get("value", "")
            abstract = r.get("abstract", {}).get("value", "")

            # nombre visible: español si existe, si no inglés
            nombre = label_es if label_es else label_en

            # solo guardar labels reales
            labels = {"en": label_en}
            if label_es:
                labels["es"] = label_es

            animales.append({
                "id":                uri_id,
                "uri":               uri,
                "nombre":            nombre,
                "labels":            labels,
                "abstract":          abstract,
                "nombre_cientifico": "",
                "same_as":           uri,
                "fuente":            "dbpedia"
            })
            print(f"[{i+1}] ✅ {nombre}")
        else:
            print(f"[{i+1}] ⚠️  {uri_id} no encontrado")
    except Exception as e:
        print(f"[{i+1}] ❌ {uri_id}: {e}")

    time.sleep(0.5)

os.makedirs(os.path.dirname(DUMP_FILE), exist_ok=True)
with open(DUMP_FILE, "w", encoding="utf-8") as f:
    json.dump(animales, f, ensure_ascii=False, indent=2)

print(f"\n✅ Total: {len(animales)} animales guardados")