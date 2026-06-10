import re
import requests

DBPEDIA_SPARQL  = "https://dbpedia.org/sparql"
DBPEDIA_LOOKUP  = "https://lookup.dbpedia.org/api/search"
HEADERS = {
    "Accept":     "application/sparql-results+json",
    "User-Agent": "MotorOWL/1.0 (UMSS Grupo10; contacto@umss.edu)"
}

# Traducción a inglés para la consulta en DBpedia
_A_EN = {
    # ES
    "perro":"dog","gato":"cat","pato":"duck","leon":"lion","tigre":"tiger",
    "oso":"bear","lobo":"wolf","zorro":"fox","delfin":"dolphin","ballena":"whale",
    "tiburon":"shark","aguila":"eagle","buho":"owl","serpiente":"snake",
    "vibora":"viper","cobra":"cobra","anaconda":"anaconda","cocodrilo":"crocodile",
    "tortuga":"turtle","rana":"frog","sapo":"toad","axolotl":"axolotl",
    "elefante":"elephant","jirafa":"giraffe","cebra":"zebra","hipopotamo":"hippopotamus",
    "rinoceronte":"rhinoceros","gorila":"gorilla","chimpance":"chimpanzee",
    "orangutan":"orangutan","canguro":"kangaroo","koala":"koala","pinguino":"penguin",
    "flamenco":"flamingo","tucan":"toucan","loro":"parrot","colibri":"hummingbird",
    "arana":"spider","escorpion":"scorpion","cangrejo":"crab","langosta":"lobster",
    "pulpo":"octopus","calamar":"squid","mariposa":"butterfly","abeja":"bee",
    "salmon":"salmon","atun":"tuna","pirana":"piranha","piraña":"piranha",
    "foca":"seal","morsa":"walrus","nutria":"otter","castor":"beaver",
    "capibara":"capybara","llama":"llama","alpaca":"alpaca","camello":"camel",
    "caballo":"horse","burro":"donkey","bisonte":"bison","alce":"moose",
    "reno":"reindeer","ciervo":"deer","jabali":"boar","puma":"puma",
    "jaguar":"jaguar","leopardo":"leopard","guepardo":"cheetah","hiena":"hyena",
    "orca":"orca","narval":"narwhal","beluga":"beluga","delfines":"dolphin",
    "tiburones":"shark","ballenas":"whale","peces":"fish","aves":"bird",
    "reptiles":"reptile","anfibios":"amphibian","insectos":"insect",
    "mamiferos":"mammal","primates":"primate","felinos":"feline",
    "leon":"lion","erizo":"hedgehog","murcielago":"bat","conejo":"rabbit",
    # FR
    "chien":"dog","chat":"cat","canard":"duck","renard":"fox",
    "ours":"bear","loup":"wolf","dauphin":"dolphin","baleine":"whale",
    "requin":"shark","aigle":"eagle","serpent":"snake","crocodile":"crocodile",
    "grenouille":"frog","elephant":"elephant","girafe":"giraffe","manchot":"penguin",
    "perroquet":"parrot","pieuvre":"octopus","abeille":"bee","papillon":"butterfly",
    # PT
    "cao":"dog","leao":"lion","urso":"bear","raposa":"fox",
    "golfinho":"dolphin","tubarao":"shark","aguia":"eagle",
    "jacare":"crocodile","pinguim":"penguin","papagaio":"parrot",
    "polvo":"octopus","borboleta":"butterfly","abelha":"bee",
    # DE
    "hund":"dog","katze":"cat","ente":"duck","loewe":"lion","baer":"bear",
    "wolf":"wolf","fuchs":"fox","wal":"whale","hai":"shark",
    "adler":"eagle","schlange":"snake","krokodil":"crocodile","frosch":"frog",
    "elefant":"elephant","giraffe":"giraffe","pinguin":"penguin","papagei":"parrot",
}

# Categorías DBpedia que corresponden a animales
_ANIMAL_CATEGORIES = {
    "Animal", "Mammal", "Bird", "Reptile", "Amphibian", "Fish", "Insect",
    "Arachnid", "Crustacean", "Mollusca", "Dog", "Cat", "Horse",
    "Shark", "Whale", "Dolphin", "Primate", "Snake",
}


def _a_ingles(query: str) -> str:
    q = query.lower().strip()
    for src, dst in zip("áàäéèëíìïóòöúùüñ", "aaaeeeiiioooouuun"):
        q = q.replace(src, dst)
    return _A_EN.get(q, q)


def _limpiar_html(texto: str) -> str:
    return re.sub(r'<[^>]+>', '', texto or '').strip()


def _es_animal(categories: list) -> bool:
    """Verifica si alguna de las categorías del resultado de Lookup corresponde a un animal."""
    for cat in categories:
        cat_label = cat.get("label", "") or ""
        cat_uri   = cat.get("uri",   "") or ""
        for a in _ANIMAL_CATEGORIES:
            if a.lower() in cat_label.lower() or a.lower() in cat_uri.lower():
                return True
    return False


def search_dbpedia_owl(query: str, lang: str = "es") -> list:
    """
    Busca en DBpedia usando la Lookup API (más rápida y fiable que SPARQL).
    Filtra por categoría de animal para evitar resultados irrelevantes.
    Traduce la query al inglés primero para evitar "Perrotia" al buscar "perro".
    """
    query_en    = _a_ingles(query)
    query_lower = query_en.lower()

    # Lookup API acepta hasta 30 resultados por consulta
    try:
        resp = requests.get(
            DBPEDIA_LOOKUP,
            params={
                "query":    query_en,
                "format":   "json",
                "maxResults": 30,
            },
            headers={"User-Agent": HEADERS["User-Agent"], "Accept": "application/json"},
            timeout=10
        )
        if resp.status_code not in (200, 206):
            print(f"[DBpedia Lookup] HTTP {resp.status_code}")
            return _search_dbpedia_sparql(query, lang)  # fallback a SPARQL

        docs    = resp.json().get("docs", [])
        results = []
        seen    = set()

        for doc in docs:
            uri        = (doc.get("resource", [None])[0] or "")
            label_list = doc.get("label", [])
            label_en   = _limpiar_html(label_list[0] if label_list else "")
            cats       = [{"label": c, "uri": ""} for c in doc.get("category", [])]
            comment    = _limpiar_html((doc.get("comment") or [""])[0])
            # thumbnail desde depiction
            dep_list   = doc.get("depiction", [])
            thumbnail  = dep_list[0] if dep_list else ""

            if not uri or not label_en or uri in seen:
                continue

            # Verificar que es un animal
            if not _es_animal(cats):
                # Segunda verificación: el comment menciona animal?
                comment_lower = comment.lower()
                if not any(w in comment_lower for w in ("species", "animal", "mammal", "bird", "fish",
                                                         "reptile", "insect", "amphibian", "especie",
                                                         "animal", "mamífero", "ave", "pez")):
                    continue

            # Verificar que el label coincide con la búsqueda
            label_lower = label_en.lower()
            if len(query_lower) <= 4:
                if label_lower != query_lower:
                    continue
            else:
                if not (label_lower == query_lower
                        or label_lower.startswith(query_lower + " ")
                        or (" " + query_lower + " ") in label_lower
                        or label_lower.endswith(" " + query_lower)):
                    continue

            seen.add(uri)
            # Labels: siempre incluir inglés; buscar español/idioma pedido en typeName o comment
            labels = {"en": label_en}

            results.append({
                "id":                uri.split("/")[-1],
                "uri":               uri,
                "nombre":            label_en,
                "labels":            labels,
                "abstract":          comment,
                "nombre_cientifico": "",
                "thumbnail":         thumbnail,
                "fuente":            "dbpedia_owl"
            })

        print(f"[DBpedia Lookup] '{query}'->'{query_en}' ({lang}) -> {len(results)} resultados")
        return results

    except Exception as e:
        print(f"[DBpedia Lookup] error: {e}")
        return _search_dbpedia_sparql(query, lang)


def _search_dbpedia_sparql(query: str, lang: str = "es") -> list:
    """Fallback: SPARQL directo a DBpedia (puede ser lento)."""
    query_en    = _a_ingles(query)
    query_lower = query_en.lower()

    if len(query_lower) <= 4:
        label_filter = f'LCASE(str(?label)) = "{query_lower}"'
    else:
        label_filter = (
            f'LCASE(str(?label)) = "{query_lower}" || '
            f'STRSTARTS(LCASE(str(?label)), "{query_lower} ") || '
            f'CONTAINS(LCASE(str(?label)), " {query_lower} ") || '
            f'STRENDS(LCASE(str(?label)), " {query_lower}")'
        )

    sparql = f"""
PREFIX dbo:  <http://dbpedia.org/ontology/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

SELECT DISTINCT ?animal ?label ?labelReq ?thumbnail WHERE {{
  ?animal rdf:type ?tipo .
  FILTER(?tipo IN (
    dbo:Animal, dbo:Mammal, dbo:Bird, dbo:Reptile, dbo:Amphibian,
    dbo:Fish, dbo:Insect, dbo:Arachnid, dbo:Crustacean, dbo:Mollusca
  ))
  ?animal rdfs:label ?label .
  FILTER(lang(?label) = "en")
  FILTER({label_filter})
  OPTIONAL {{ ?animal rdfs:label ?labelReq . FILTER(lang(?labelReq) = "{lang}") }}
  OPTIONAL {{ ?animal dbo:thumbnail ?thumbnail . }}
}}
ORDER BY ?label
LIMIT 50
"""
    try:
        resp = requests.get(
            DBPEDIA_SPARQL,
            params={"query": sparql, "format": "application/sparql-results+json", "timeout": "9000"},
            headers=HEADERS,
            timeout=12
        )
        if resp.status_code not in (200, 206):
            return []

        bindings = resp.json().get("results", {}).get("bindings", [])
        results  = []
        seen     = set()

        for r in bindings:
            uri       = r.get("animal",   {}).get("value", "")
            label_en  = _limpiar_html(r.get("label",    {}).get("value", ""))
            label_req = _limpiar_html(r.get("labelReq", {}).get("value", ""))
            thumbnail = _limpiar_html(r.get("thumbnail",{}).get("value", ""))

            if not uri or not label_en or uri in seen:
                continue

            nombre = label_req or label_en
            labels = {"en": label_en}
            if label_req and lang != "en":
                labels[lang] = label_req

            seen.add(uri)
            results.append({
                "id":                uri.split("/")[-1],
                "uri":               uri,
                "nombre":            nombre,
                "labels":            labels,
                "abstract":          "",
                "nombre_cientifico": "",
                "thumbnail":         thumbnail,
                "fuente":            "dbpedia_owl"
            })

        print(f"[DBpedia SPARQL] '{query}'->'{query_en}' -> {len(results)} resultados")
        return results
    except Exception as e:
        print(f"[DBpedia SPARQL] error: {e}")
        return []
