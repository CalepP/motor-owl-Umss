import os
import json
import unicodedata
from SPARQLWrapper import SPARQLWrapper, JSON

ENDPOINT_EN = os.getenv("DBPEDIA_ENDPOINT", "https://dbpedia.org/sparql")
TIMEOUT     = int(os.getenv("DBPEDIA_TIMEOUT", 30))
RETRIES     = int(os.getenv("SPARQL_RETRIES", 1))
DUMP_FILE   = os.path.join(os.path.dirname(__file__),
                           "../../data/dbpedia/animales_dump.json")

TRADUCCIONES_EN = {
    "perro": "dog", "gato": "cat", "leon": "lion", "león": "lion",
    "tigre": "tiger", "oso": "bear", "lobo": "wolf", "zorro": "fox",
    "delfin": "dolphin", "delfín": "dolphin", "ballena": "whale",
    "gorila": "gorilla", "caballo": "horse", "aguila": "eagle",
    "águila": "eagle", "pinguino": "penguin", "pingüino": "penguin",
    "cocodrilo": "crocodile", "iguana": "iguana", "rana": "frog",
    "salmon": "salmon", "salmón": "salmon", "mariposa": "butterfly",
    "pez": "fish", "serpiente": "snake", "vibora": "viper",
    "víbora": "viper", "tortuga": "turtle", "conejo": "rabbit",
    "elefante": "elephant", "jirafa": "giraffe", "cebra": "zebra",
    "mono": "monkey", "puma": "puma", "jaguar": "jaguar",
    "leopardo": "leopard", "guepardo": "cheetah", "orca": "orca",
    "tiburon": "shark", "tiburón": "shark", "pulpo": "octopus",
    "cangrejo": "crab", "loro": "parrot", "buho": "owl", "búho": "owl",
    "flamingo": "flamingo", "colibri": "hummingbird", "colibrí": "hummingbird",
    "pez payaso": "clownfish", "oso panda": "panda",
    "oso polar": "polar bear", "ballena azul": "blue whale",
    "tigre de bengala": "bengal tiger", "aguila real": "golden eagle",
    "águila real": "golden eagle", "cocodrilo del nilo": "nile crocodile",
    "iguana verde": "green iguana", "rana arborea": "tree frog",
    "rana arbórea": "tree frog", "salmon atlantico": "atlantic salmon",
    "salmón atlántico": "atlantic salmon",
    "mariposa monarca": "monarch butterfly",
    "rinoceronte": "rhinoceros", "hipopotamo": "hippopotamus",
    "hipopótamo": "hippopotamus", "chimpance": "chimpanzee",
    "chimpancé": "chimpanzee", "canguro": "kangaroo", "koala": "koala",
    "ornitorrinco": "platypus", "pavo real": "peacock", "tucan": "toucan",
    "tucán": "toucan", "piraña": "piranha", "anaconda": "anaconda",
    "cobra": "cobra", "tibur": "shark",
}

# Cache del dump en memoria
_dump_cache = None

def _normalizar(texto):
    return ''.join(
        c for c in unicodedata.normalize('NFD', texto.lower())
        if unicodedata.category(c) != 'Mn'
    )

def _a_ingles(query):
    q = query.lower().strip()
    q_norm = _normalizar(q)
    return TRADUCCIONES_EN.get(q) or TRADUCCIONES_EN.get(q_norm) or q_norm

def _cargar_dump():
    global _dump_cache
    if _dump_cache is None:
        if os.path.exists(DUMP_FILE):
            with open(DUMP_FILE, "r", encoding="utf-8") as f:
                _dump_cache = json.load(f)
            print(f"📦 Dump cargado: {len(_dump_cache)} animales")
        else:
            _dump_cache = []
            print("⚠️ Dump no encontrado")
    return _dump_cache

def _buscar_en_dump(query_en, lang):
    dump = _cargar_dump()
    query_lower = query_en.lower()
    resultados = []
    vistos = set()

    for animal in dump:
        label_en = animal.get("labels", {}).get("en", "").lower()
        label_lang = animal.get("labels", {}).get(lang, "").lower()
        nombre = animal.get("nombre", "").lower()

        if (query_lower in label_en or
            query_lower in label_lang or
            query_lower in nombre):

            key = animal.get("uri", "")
            if key not in vistos:
                vistos.add(key)
                resultados.append(animal)

    return resultados

def _buscar_en_vivo(query_en, lang):
    sparql = SPARQLWrapper(ENDPOINT_EN)
    sparql.setTimeout(TIMEOUT)

    q = f"""
    SELECT DISTINCT ?animal ?labelEn ?labelLang ?abstract ?scientificName
    WHERE {{
        ?animal a <http://dbpedia.org/ontology/Animal> .
        ?animal rdfs:label ?labelEn .
        FILTER (lang(?labelEn) = "en")
        FILTER (CONTAINS(LCASE(str(?labelEn)), LCASE("{query_en}")))
        OPTIONAL {{
            ?animal rdfs:label ?labelLang .
            FILTER (lang(?labelLang) = "{lang}")
        }}
        OPTIONAL {{
            ?animal <http://dbpedia.org/ontology/abstract> ?abstract .
            FILTER (lang(?abstract) = "{lang}")
        }}
        OPTIONAL {{
            ?animal <http://dbpedia.org/ontology/scientificName> ?scientificName .
        }}
    }}
    ORDER BY ?labelEn
    LIMIT 50
    """

    sparql.setQuery(q)
    sparql.setReturnFormat(JSON)

    try:
        results = sparql.query().convert()
        animales = _parse_results(results, lang)
        print(f"🌐 DBpedia en vivo '{query_en}' → {len(animales)} resultados")
        return animales
    except Exception as e:
        print(f"⚠️ DBpedia en vivo falló: {e}")
        return []

def search_dbpedia(query, lang="es"):
    query_en = _a_ingles(query)

    # 1. Buscar en dump offline
    offline = _buscar_en_dump(query_en, lang)
    print(f"📦 Dump '{query_en}' → {len(offline)} resultados")

    # 2. Buscar en vivo y combinar
    online = _buscar_en_vivo(query_en, lang)

    # Combinar sin duplicados (offline primero)
    uris_offline = {a["uri"] for a in offline}
    combinados = offline + [a for a in online if a["uri"] not in uris_offline]

    print(f"✅ Total combinado: {len(combinados)}")
    return combinados

def _parse_results(results, lang):
    animales = []
    vistos   = set()

    for r in results.get("results", {}).get("bindings", []):
        uri      = r.get("animal",    {}).get("value", "")
        label_en = r.get("labelEn",   {}).get("value", "")
        label_lg = r.get("labelLang", {}).get("value", "")
        sci      = r.get("scientificName", {}).get("value", "")

        if not label_en or uri in vistos:
            continue
        vistos.add(uri)

        label = label_lg if label_lg else label_en
        labels = {"en": label_en}
        if label_lg:
            labels[lang] = label_lg

        animales.append({
            "id":                uri.split("/")[-1],
            "uri":               uri,
            "nombre":            label,
            "labels":            labels,
            "abstract":          r.get("abstract", {}).get("value", ""),
            "nombre_cientifico": sci,
            "same_as":           uri,
            "fuente":            "dbpedia"
        })

    return animales