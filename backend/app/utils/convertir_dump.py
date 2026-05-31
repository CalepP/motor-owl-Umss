import json
import os

DUMP_JSON = os.path.join(os.path.dirname(__file__), "../../data/dbpedia/animales_dump.json")
DUMP_TTL  = os.path.join(os.path.dirname(__file__), "../../data/dbpedia/animales_dump.ttl")

NOMBRES_ES = {
    "Dog": "Perro", "Cat": "Gato", "Lion": "León", "Tiger": "Tigre",
    "Bear": "Oso", "Wolf": "Lobo", "Fox": "Zorro", "Dolphin": "Delfín",
    "Blue whale": "Ballena azul", "Gorilla": "Gorila", "Horse": "Caballo",
    "Golden eagle": "Águila real", "Penguin": "Pingüino",
    "Nile crocodile": "Cocodrilo del Nilo", "Green iguana": "Iguana verde",
    "Tree frog": "Rana arbórea", "Atlantic salmon": "Salmón atlántico",
    "Monarch butterfly": "Mariposa monarca", "Bengal tiger": "Tigre de Bengala",
    "Polar bear": "Oso polar", "German Shepherd": "Pastor alemán",
    "Labrador Retriever": "Labrador retriever", "Golden Retriever": "Golden retriever",
    "Poodle": "Caniche", "Bulldog": "Bulldog", "Beagle": "Beagle",
    "Chihuahua": "Chihuahua", "Rottweiler": "Rottweiler",
    "Siberian Husky": "Husky siberiano", "Dachshund": "Dachshund",
    "Persian cat": "Gato persa", "Siamese cat": "Gato siamés",
    "Maine Coon": "Maine Coon", "Bengal cat": "Gato de Bengala",
    "Great white shark": "Tiburón blanco", "Whale shark": "Tiburón ballena",
    "Hammerhead shark": "Tiburón martillo", "Bull shark": "Tiburón toro",
    "Tiger shark": "Tiburón tigre", "Octopus": "Pulpo",
    "Giant squid": "Calamar gigante", "Green sea turtle": "Tortuga verde",
    "Leatherback sea turtle": "Tortuga laúd", "King cobra": "Cobra real",
    "Black mamba": "Mamba negra", "Anaconda": "Anaconda",
    "Boa constrictor": "Boa constrictor", "Reticulated python": "Pitón reticulada",
    "Komodo dragon": "Dragón de Komodo", "African elephant": "Elefante africano",
    "Asian elephant": "Elefante asiático", "Giraffe": "Jirafa",
    "Zebra": "Cebra", "Hippopotamus": "Hipopótamo",
    "White rhinoceros": "Rinoceronte blanco", "Black rhinoceros": "Rinoceronte negro",
    "Cheetah": "Guepardo", "Leopard": "Leopardo", "Jaguar": "Jaguar",
    "Puma": "Puma", "Snow leopard": "Leopardo de las nieves",
    "Chimpanzee": "Chimpancé", "Orangutan": "Orangután",
    "Kangaroo": "Canguro", "Koala": "Koala", "Platypus": "Ornitorrinco",
    "Clownfish": "Pez payaso", "Seahorse": "Caballito de mar",
    "Piranha": "Piraña", "Swordfish": "Pez espada", "Tuna": "Atún",
    "Salmon": "Salmón", "Bald eagle": "Águila calva",
    "Harpy eagle": "Águila harpía", "Peregrine falcon": "Halcón peregrino",
    "Great horned owl": "Búho real", "Barn owl": "Lechuza común",
    "Flamingo": "Flamenco", "Toucan": "Tucán", "Ostrich": "Avestruz",
    "Emperor penguin": "Pingüino emperador", "Hummingbird": "Colibrí",
    "Honeybee": "Abeja melífera", "Giant panda": "Oso panda gigante",
    "Red panda": "Panda rojo", "Orca": "Orca", "Sperm whale": "Cachalote",
    "Humpback whale": "Ballena jorobada", "Narwhal": "Narval",
    "Sea lion": "León marino", "Walrus": "Morsa", "Harbor seal": "Foca común",
    "European rabbit": "Conejo europeo", "Red fox": "Zorro rojo",
    "Arctic fox": "Zorro ártico", "Gray wolf": "Lobo gris",
    "Coyote": "Coyote", "Spotted hyena": "Hiena manchada",
    "Moose": "Alce", "Reindeer": "Reno", "American bison": "Bisonte americano",
    "Dromedary": "Dromedario", "Llama": "Llama", "Capybara": "Capibara",
    "Beaver": "Castor", "Giant otter": "Nutria gigante", "Meerkat": "Suricata",
    "Electric eel": "Anguila eléctrica", "Axolotl": "Ajolote",
    "Poison dart frog": "Rana dardo venenosa", "Viper": "Víbora",
    "Rattlesnake": "Serpiente de cascabel", "Chameleon": "Camaleón",
    "Gecko": "Gecko","Dalmatian dog":        "Dálmata",
    "Boxer (dog)":          "Boxer",
    "Pomeranian (dog)":     "Pomerania",
    "Ragdoll cat":          "Ragdoll",
    "Mako shark":           "Tiburón mako",
    "Reef shark":           "Tiburón de arrecife",
    "Bullfrog":             "Rana toro",
    "Red-eyed tree frog":   "Rana arbórea de ojos rojos",
    "Manta ray":            "Manta raya",
    "Black bear":           "Oso negro",
    "Grizzly bear":         "Oso grizzly",
    "Sun bear":             "Oso malayo",
    "Monitor lizard":       "Lagarto monitor",
    "Macaw":                "Guacamayo",
    "Cockatoo":             "Cacatúa",
    "Bumblebee":            "Abejorro",
    "Mandrill":             "Mandril",
    "Baboon":               "Babuino",
    "Gibbon":               "Gibón",
    "Bonobo":               "Bonobo",
    "Wombat":               "Wombat",
    "Tasmanian devil":      "Demonio de Tasmania",
    "Donkey":               "Burro",
    "Mule":                 "Mula",
    "Water buffalo":        "Búfalo de agua",
    "Snowshoe hare":        "Liebre americana",
    "Dingo":                "Dingo",
    "Mongoose":             "Mangosta",
    "Beluga whale":         "Ballena beluga",
    "Spinner dolphin":      "Delfín tornillo",
    "Common dolphin":       "Delfín común",
    "Bottlenose dolphin":   "Delfín mular",
    "Saltwater crocodile":  "Cocodrilo marino",
    "Clouded leopard":      "Leopardo nebuloso",
    "Caracal":              "Caracal",
}

def esc(s):
    return s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", " ")

with open(DUMP_JSON, encoding="utf-8") as f:
    data = json.load(f)

lines = [
    "@prefix rdfs:  <http://www.w3.org/2000/01/rdf-schema#> .",
    "@prefix owl:   <http://www.w3.org/2002/07/owl#> .",
    "@prefix dbo:   <http://dbpedia.org/ontology/> .",
    "@prefix foaf:  <http://xmlns.com/foaf/0.1/> .",
    "",
]

for a in data:
    uri = a.get("uri", "")
    if not uri:
        continue

    label_en  = a.get("labels", {}).get("en", "")
    label_es  = a.get("labels", {}).get("es", "")
    label_fr  = a.get("labels", {}).get("fr", "")
    label_pt  = a.get("labels", {}).get("pt", "")
    label_de  = a.get("labels", {}).get("de", "")

    # Usar traducción manual si existe, si no usar la española del dump
    nombre_es = NOMBRES_ES.get(label_en, label_es if label_es else label_en)

    triples = [f"<{uri}>"]
    triples.append("  a owl:NamedIndividual, dbo:Animal ;")
    triples.append(f'  rdfs:label "{esc(nombre_es)}"@es ;')
    if label_en:
        triples.append(f'  rdfs:label "{esc(label_en)}"@en ;')
    if label_fr:
        triples.append(f'  rdfs:label "{esc(label_fr)}"@fr ;')
    if label_pt:
        triples.append(f'  rdfs:label "{esc(label_pt)}"@pt ;')
    if label_de:
        triples.append(f'  rdfs:label "{esc(label_de)}"@de ;')

    ab = a.get("abstract", "")
    if ab:
        triples.append(f'  dbo:abstract "{esc(ab[:500])}"@es ;')

    thumbnail = a.get("thumbnail", "")
    if thumbnail:
        triples.append(f'  foaf:depiction <{thumbnail}> ;')

    triples[-1] = triples[-1].rstrip(" ;") + " ."
    lines.extend(triples)
    lines.append("")

with open(DUMP_TTL, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print(f"✅ TTL generado con {len(data)} animales → {DUMP_TTL}")