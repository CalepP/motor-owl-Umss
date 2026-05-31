import json
import os
import time
from SPARQLWrapper import SPARQLWrapper, JSON

ENDPOINT = "https://dbpedia.org/sparql"
DUMP_FILE = "data/dbpedia/animales_dump.json"

ANIMALES_URI = [
    # Perros y razas
    "Dog", "German_Shepherd", "Labrador_Retriever", "Golden_Retriever",
    "Poodle", "Bulldog", "Beagle", "Chihuahua", "Rottweiler",
    "Siberian_Husky", "Dachshund", "Boxer_(dog)", "Pomeranian_(dog)",
    "Shih_Tzu", "Yorkshire_Terrier", "Dobermann", "Great_Dane",
    "Border_Collie", "Australian_Shepherd", "Dalmatian_dog",
    # Gatos y razas
    "Cat", "Persian_cat", "Siamese_cat", "Maine_Coon", "Bengal_cat",
    "Ragdoll_cat", "Sphynx_cat", "British_Shorthair", "Scottish_Fold",
    "Abyssinian_cat",
    # Felinos salvajes
    "Lion", "Tiger", "Bengal_tiger", "Cheetah", "Leopard",
    "Jaguar", "Puma", "Snow_leopard", "Clouded_leopard", "Caracal",
    # Osos
    "Bear", "Polar_bear", "Giant_panda", "Red_panda", "Brown_bear",
    "Black_bear", "Grizzly_bear", "Sun_bear", "Spectacled_bear",
    # Tiburones
    "Great_white_shark", "Whale_shark", "Hammerhead_shark",
    "Bull_shark", "Tiger_shark", "Nurse_shark", "Mako_shark",
    "Blue_shark", "Lemon_shark", "Reef_shark",
    # Ballenas y delfines
    "Blue_whale", "Humpback_whale", "Sperm_whale", "Orca",
    "Narwhal", "Beluga_whale", "Dolphin", "Bottlenose_dolphin",
    "Spinner_dolphin", "Common_dolphin",
    # Aves
    "Golden_eagle", "Bald_eagle", "Harpy_eagle", "Peregrine_falcon",
    "Great_horned_owl", "Barn_owl", "Snowy_owl", "Flamingo",
    "Toucan", "Ostrich", "Emperor_penguin", "African_penguin",
    "Hummingbird", "Peacock", "Macaw", "Parrot", "Cockatoo",
    # Reptiles
    "Nile_crocodile", "Saltwater_crocodile", "Green_iguana",
    "Komodo_dragon", "King_cobra", "Black_mamba", "Anaconda",
    "Boa_constrictor", "Reticulated_python", "Chameleon",
    "Gecko", "Gila_monster", "Monitor_lizard",
    # Anfibios
    "Tree_frog", "Poison_dart_frog", "Axolotl", "Bullfrog",
    "Red-eyed_tree_frog", "Salamander",
    # Peces
    "Atlantic_salmon", "Clownfish", "Piranha", "Swordfish",
    "Seahorse", "Manta_ray", "Stingray", "Electric_eel", "Tuna",
    "Great_white_shark",
    # Insectos y artrópodos
    "Monarch_butterfly", "Blue_morpho_butterfly", "Painted_lady",
    "Honeybee", "Bumblebee", "Carpenter_bee", "Dragonfly",
    "Praying_mantis", "Firefly", "Ant", "Termite",
    "Goliath_beetle", "Stick_insect",
    # Arácnidos
    "Black_widow_spider", "Tarantula", "Scorpion", "Wolf_spider",
    # Crustáceos y moluscos
    "Mantis_shrimp", "Horseshoe_crab", "Japanese_spider_crab",
    "Lobster", "Shrimp", "Crayfish", "Hermit_crab",
    "Octopus", "Giant_squid", "Nautilus", "Giant_clam",
    # Equinodermos y cnidarios
    "Starfish", "Sea_urchin", "Jellyfish", "Box_jellyfish",
    # Primates
    "Gorilla", "Chimpanzee", "Orangutan", "Gibbon", "Bonobo",
    "Mandrill", "Baboon",
    # Mamíferos grandes
    "African_elephant", "Asian_elephant", "Giraffe", "Zebra",
    "Hippopotamus", "White_rhinoceros", "Black_rhinoceros",
    "American_bison", "Water_buffalo", "Moose", "Reindeer",
    "Dromedary", "Bactrian_camel", "Llama", "Alpaca",
    # Mamíferos medianos
    "Wolf", "Gray_wolf", "Fox", "Red_fox", "Arctic_fox",
    "Coyote", "Dingo", "Meerkat", "Mongoose", "Spotted_hyena",
    "Kangaroo", "Koala", "Platypus", "Wombat", "Tasmanian_devil",
    "Capybara", "Beaver", "Giant_otter", "Sea_otter",
    "Sea_lion", "Walrus", "Harbor_seal", "Elephant_seal",
    "European_rabbit", "Snowshoe_hare",
    # Caballos y ungulados
    "Horse", "Donkey", "Mule",
]
# Quitar duplicados manteniendo orden
vistos_uri = set()
ANIMALES_URI_UNICOS = []
for u in ANIMALES_URI:
    if u not in vistos_uri:
        vistos_uri.add(u)
        ANIMALES_URI_UNICOS.append(u)

animales = []

for i, uri_id in enumerate(ANIMALES_URI_UNICOS):
    sparql = SPARQLWrapper(ENDPOINT)
    sparql.setTimeout(15)
    uri = f"http://dbpedia.org/resource/{uri_id}"

    q = f"""
    SELECT ?labelEn ?labelEs ?labelFr ?labelPt ?labelDe ?abstract ?thumbnail
    WHERE {{
        <{uri}> rdfs:label ?labelEn .
        FILTER (lang(?labelEn) = "en")
        OPTIONAL {{ <{uri}> rdfs:label ?labelEs . FILTER (lang(?labelEs) = "es") }}
        OPTIONAL {{ <{uri}> rdfs:label ?labelFr . FILTER (lang(?labelFr) = "fr") }}
        OPTIONAL {{ <{uri}> rdfs:label ?labelPt . FILTER (lang(?labelPt) = "pt") }}
        OPTIONAL {{ <{uri}> rdfs:label ?labelDe . FILTER (lang(?labelDe) = "de") }}
        OPTIONAL {{
            <{uri}> <http://dbpedia.org/ontology/abstract> ?abstract .
            FILTER (lang(?abstract) = "es")
        }}
        OPTIONAL {{
            <{uri}> <http://dbpedia.org/ontology/thumbnail> ?thumbnail .
        }}
    }} LIMIT 1
    """

    sparql.setQuery(q)
    sparql.setReturnFormat(JSON)

    try:
        results = sparql.query().convert()
        bindings = results.get("results", {}).get("bindings", [])
        if bindings:
            r         = bindings[0]
            label_en  = r.get("labelEn", {}).get("value", "")
            label_es  = r.get("labelEs", {}).get("value", "")
            label_fr  = r.get("labelFr", {}).get("value", "")
            label_pt  = r.get("labelPt", {}).get("value", "")
            label_de  = r.get("labelDe", {}).get("value", "")
            abstract  = r.get("abstract",  {}).get("value", "")
            thumbnail = r.get("thumbnail", {}).get("value", "")

            nombre = label_es if label_es else label_en
            labels = {"en": label_en}
            if label_es: labels["es"] = label_es
            if label_fr: labels["fr"] = label_fr
            if label_pt: labels["pt"] = label_pt
            if label_de: labels["de"] = label_de

            animales.append({
                "id":                uri_id,
                "uri":               uri,
                "nombre":            nombre,
                "labels":            labels,
                "abstract":          abstract,
                "nombre_cientifico": "",
                "thumbnail":         thumbnail,
                "same_as":           uri,
                "fuente":            "dbpedia"
            })
            print(f"[{i+1}/{len(ANIMALES_URI_UNICOS)}] ✅ {nombre}")
        else:
            print(f"[{i+1}/{len(ANIMALES_URI_UNICOS)}] ⚠️  {uri_id} no encontrado")
    except Exception as e:
        print(f"[{i+1}/{len(ANIMALES_URI_UNICOS)}] ❌ {uri_id}: {e}")

    time.sleep(0.5)

os.makedirs(os.path.dirname(DUMP_FILE), exist_ok=True)
with open(DUMP_FILE, "w", encoding="utf-8") as f:
    json.dump(animales, f, ensure_ascii=False, indent=2)

print(f"\n✅ Total: {len(animales)} animales guardados")