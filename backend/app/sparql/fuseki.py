import os
import unicodedata
import requests
from SPARQLWrapper import SPARQLWrapper, JSON

FUSEKI_URL  = os.getenv("FUSEKI_URL", "http://localhost:3030/animales")
ENDPOINT_EN = os.getenv("DBPEDIA_ENDPOINT", "https://dbpedia.org/sparql")
TIMEOUT     = int(os.getenv("DBPEDIA_TIMEOUT", 30))
RETRIES     = int(os.getenv("SPARQL_RETRIES", 1))

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
    "chimpancé": "chimpanzee", "canguro": "kangaroo",
    "ornitorrinco": "platypus", "pavo real": "peacock",
    "tucan": "toucan", "tucán": "toucan", "piraña": "piranha",
    "anaconda": "anaconda", "cobra": "cobra",
}

def _normalizar(texto):
    return ''.join(
        c for c in unicodedata.normalize('NFD', texto.lower())
        if unicodedata.category(c) != 'Mn'
    )

def _a_ingles(query):
    q = query.lower().strip()
    q_norm = _normalizar(q)
    return TRADUCCIONES_EN.get(q) or TRADUCCIONES_EN.get(q_norm) or q_norm

def search_fuseki(query, lang="es"):
    """Busca en Fuseki local — funciona offline."""
    query_en = _a_ingles(query)
    query_lower = query.lower()
    query_en_lower = query_en.lower()

    sparql_query = f"""
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX owl:  <http://www.w3.org/2002/07/owl#>
    PREFIX dbo:  <http://dbpedia.org/ontology/>

    SELECT DISTINCT ?animal ?label ?labelEn ?sci ?abstract
    WHERE {{
        ?animal a owl:NamedIndividual .
        ?animal rdfs:label ?label .
        FILTER(lang(?label) = "{lang}")
        OPTIONAL {{ ?animal rdfs:label ?labelEn . FILTER(lang(?labelEn) = "en") }}
        OPTIONAL {{ ?animal dbo:scientificName ?sci . }}
        OPTIONAL {{ ?animal dbo:abstract ?abstract . FILTER(lang(?abstract) = "{lang}") }}
        FILTER(
            CONTAINS(LCASE(str(?label)), "{query_lower}") ||
            CONTAINS(LCASE(str(?labelEn)), "{query_en_lower}")
        )
    }}
    ORDER BY ?label
    LIMIT 50
    """

    try:
        resp = requests.post(
            f"{FUSEKI_URL}/query",
            data={"query": sparql_query},
            headers={"Accept": "application/sparql-results+json"},
            timeout=10
        )
        resp.raise_for_status()
        data = resp.json()
        resultados = _parse_fuseki(data, lang)
        print(f"🔵 Fuseki '{query}' → {len(resultados)} resultados")
        return resultados
    except Exception as e:
        print(f"⚠️ Fuseki no disponible: {e}")
        return []

def search_dbpedia_live(query, lang="es"):
    """Busca en DBpedia en vivo — solo si hay internet."""
    query_en = _a_ingles(query)

    sparql = SPARQLWrapper(ENDPOINT_EN)
    sparql.setTimeout(TIMEOUT)

    q = f"""
    SELECT DISTINCT ?animal ?labelEn ?labelLang ?abstract ?scientificName
    WHERE {{
        ?animal a <http://dbpedia.org/ontology/Animal> .
        ?animal rdfs:label ?labelEn .
        FILTER (lang(?labelEn) = "en")
        FILTER (
            LCASE(str(?labelEn)) = LCASE("{query_en}") ||
            STRSTARTS(LCASE(str(?labelEn)), LCASE("{query_en} ")) ||
            CONTAINS(LCASE(str(?labelEn)), LCASE(" {query_en} ")) ||
            STRENDS(LCASE(str(?labelEn)), LCASE(" {query_en}"))
        )
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

    for intento in range(RETRIES + 1):
        try:
            results = sparql.query().convert()
            animales = _parse_dbpedia(results, lang)
            print(f"🌐 DBpedia live '{query_en}' → {len(animales)} resultados")
            return animales
        except Exception as e:
            if intento == RETRIES:
                print(f"⚠️ DBpedia live falló: {e}")
                return []
    return []

def _parse_fuseki(data, lang):
    animales = []
    vistos   = set()

    for r in data.get("results", {}).get("bindings", []):
        uri      = r.get("animal",   {}).get("value", "")
        label    = r.get("label",    {}).get("value", "")
        label_en = r.get("labelEn",  {}).get("value", "")
        sci      = r.get("sci",      {}).get("value", "")
        abstract = r.get("abstract", {}).get("value", "")

        if not uri or uri in vistos:
            continue
        vistos.add(uri)

        fuente = "local" if "semanticweb.org" in uri else "dbpedia"

        animales.append({
            "id":                uri.split("#")[-1].split("/")[-1],
            "uri":               uri,
            "nombre":            label,
            "labels":            {lang: label, "en": label_en} if label_en else {lang: label},
            "abstract":          abstract,
            "nombre_cientifico": sci,
            "same_as":           uri,
            "fuente":            fuente
        })

    return animales

def _parse_dbpedia(results, lang):
    animales = []
    vistos   = set()

    # Palabras que indican que no es un animal real
    NO_ANIMALES = {"musician", "band", "horse", "painter", "actor",
                   "actress", "politician", "footballer", "singer",
                   "writer", "director", "composer", "footballer"}

    for r in results.get("results", {}).get("bindings", []):
        uri      = r.get("animal",    {}).get("value", "")
        label_en = r.get("labelEn",   {}).get("value", "")
        label_lg = r.get("labelLang", {}).get("value", "")
        sci      = r.get("scientificName", {}).get("value", "")

        if not label_en or uri in vistos:
            continue

        # Filtrar si el nombre contiene indicadores de no-animal
        label_lower = label_en.lower()
        if any(f"({word})" in label_lower for word in NO_ANIMALES):
            continue

        # Solo incluir si tiene etiqueta en el idioma pedido
        if not label_lg:
            continue
        # Verificar que la etiqueta en español contenga algo relacionado
        # con la búsqueda (no solo que el inglés coincida)
        if lang == "es" and label_lg:
            # Si la etiqueta española es igual al inglés, es probable que
            # sea un nombre propio, no un animal
            if label_lg.lower() == label_en.lower():
                continue

        vistos.add(uri)

        labels = {"en": label_en, lang: label_lg}

        animales.append({
            "id":                uri.split("/")[-1],
            "uri":               uri,
            "nombre":            label_lg,
            "labels":            labels,
            "abstract":          r.get("abstract", {}).get("value", ""),
            "nombre_cientifico": sci,
            "same_as":           uri,
            "fuente":            "dbpedia"
        })

    return animales