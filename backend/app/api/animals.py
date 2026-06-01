from flask import Blueprint, jsonify, request
from ..ontology.loader import get_all_animals, get_animal_by_id
from ..sparql.fuseki import search_fuseki

bp = Blueprint("animals", __name__)

@bp.route("/", methods=["GET"])
def list_animals():
    animals = get_all_animals()
    return jsonify(animals)

@bp.route("/<animal_id>", methods=["GET"])
def get_animal(animal_id):
    animal = get_animal_by_id(animal_id)
    if not animal:
        return jsonify({"error": "Animal no encontrado"}), 404
    return jsonify(animal)

@bp.route("/details", methods=["GET"])
def get_details():
    uri  = request.args.get("uri", "").strip()
    lang = request.args.get("lang", "es").strip()
    if not uri:
        return jsonify({"error": "URI requerida"}), 400

    if "dbpedia.org/resource/" in uri:
        import requests as req

        resource_id = uri.split("/resource/")[-1]

        # Usar la API REST de DBpedia (más estable que SPARQL)
        try:
            print(f"🔍 Buscando detalles para: {uri} en idioma: {lang}")
            import requests as req
            resource_id    = uri.split("/resource/")[-1]
            nombre_legible = resource_id.replace("_", " ")

            WIKI_ES_TITLES = {
                "Lion": "León_(animal)", "Tiger": "Tigre", "Bear": "Oso",
                "Wolf": "Lobo", "Dog": "Perro_doméstico", "Cat": "Gato_doméstico",
                "Horse": "Caballo", "Dolphin": "Delfín", "Blue_whale": "Ballena_azul",
                "Gorilla": "Gorila", "Golden_eagle": "Águila_real", "Penguin": "Pingüino",
                "Nile_crocodile": "Cocodrilo_del_Nilo", "Green_iguana": "Iguana_verde",
                "Tree_frog": "Rana_arborícola", "Atlantic_salmon": "Salmón_del_Atlántico",
                "Monarch_butterfly": "Danaus_plexippus", "Bengal_tiger": "Tigre_de_Bengala",
                "Polar_bear": "Oso_polar", "Great_white_shark": "Gran_tiburón_blanco",
                "Whale_shark": "Tiburón_ballena", "Hammerhead_shark": "Tiburón_martillo",
                "Bull_shark": "Tiburón_toro", "Tiger_shark": "Tiburón_tigre",
                "Cheetah": "Guepardo", "Leopard": "Leopardo", "Jaguar": "Jaguar",
                "Puma": "Puma", "Snow_leopard": "Leopardo_de_las_nieves",
                "Chimpanzee": "Chimpancé", "Orangutan": "Orangután",
                "African_elephant": "Elefante_africano", "Asian_elephant": "Elefante_asiático",
                "Giraffe": "Jirafa", "Zebra": "Cebra", "Hippopotamus": "Hipopótamo",
                "White_rhinoceros": "Rinoceronte_blanco", "Black_rhinoceros": "Rinoceronte_negro",
                "Orca": "Orca", "Humpback_whale": "Ballena_jorobada",
                "Sperm_whale": "Cachalote", "Narwhal": "Narval",
                "Giant_panda": "Panda_gigante", "Red_panda": "Panda_rojo",
                "Komodo_dragon": "Dragón_de_Komodo", "King_cobra": "Cobra_real",
                "Black_mamba": "Mamba_negra", "Anaconda": "Anaconda",
                "Octopus": "Pulpo", "German_Shepherd": "Pastor_alemán",
                "Labrador_Retriever": "Labrador_retriever",
                "Golden_Retriever": "Golden_retriever", "Bulldog": "Bulldog",
                "Beagle": "Beagle", "Rottweiler": "Rottweiler",
                "Siberian_Husky": "Husky_siberiano", "Dachshund": "Dachshund",
                "Dalmatian_dog": "Dálmata_(perro)", "Persian_cat": "Gato_persa",
                "Siamese_cat": "Gato_siamés", "Flamingo": "Flamenco_(ave)",
                "Toucan": "Tucán", "Ostrich": "Avestruz",
                "Emperor_penguin": "Pingüino_emperador", "Hummingbird": "Colibrí",
                "Kangaroo": "Canguro", "Koala": "Koala", "Platypus": "Ornitorrinco",
                "Capybara": "Capibara", "Piranha": "Piraña",
                "Electric_eel": "Anguila_eléctrica", "Axolotl": "Ajolote",
            }

            # Para idiomas distintos al español, usar el resource_id directamente
            if lang == "es":
                wiki_title = WIKI_ES_TITLES.get(resource_id, resource_id)
            else:
                wiki_title = resource_id

            # Intentar en el idioma solicitado
            wiki_resp = req.get(
                f"https://{lang}.wikipedia.org/api/rest_v1/page/summary/{wiki_title}",
                headers={"User-Agent": "MotorOWL/1.0 (UMSS Grupo10; contacto@umss.edu)"},
                timeout=10
            )
            print(f"📡 Wikipedia {lang.upper()} status: {wiki_resp.status_code} para {wiki_title}")

            if wiki_resp.status_code == 200:
                wiki      = wiki_resp.json()
                extract   = wiki.get("extract", "")
                thumbnail = wiki.get("thumbnail", {}).get("source", "")
                return jsonify({
                    "uri":               uri,
                    "labels":            {lang: wiki.get("title", nombre_legible), "en": nombre_legible},
                    "abstract":          extract,
                    "thumbnail":         thumbnail,
                    "nombre_cientifico": wiki.get("title", "") if wiki.get("type") == "standard" else "",
                    "clasificacion":     {},
                    "descripcion_corta": wiki.get("description", ""),
                    "fuente":            "dbpedia"
                })

            # Fallback a inglés si el idioma pedido no tiene artículo
            if lang != "en":
                wiki_en = req.get(
                    f"https://en.wikipedia.org/api/rest_v1/page/summary/{resource_id}",
                    headers={"User-Agent": "MotorOWL/1.0 (UMSS Grupo10; contacto@umss.edu)"},
                    timeout=10
                )
                print(f"📡 Wikipedia EN fallback status: {wiki_en.status_code}")
                if wiki_en.status_code == 200:
                    wiki      = wiki_en.json()
                    extract   = wiki.get("extract", "")
                    thumbnail = wiki.get("thumbnail", {}).get("source", "")
                    abstract_traducido = _traducir(extract[:800]) if extract and lang not in ["en"] else extract
                    return jsonify({
                        "uri":               uri,
                        "labels":            {"en": nombre_legible},
                        "abstract":          abstract_traducido,
                        "thumbnail":         thumbnail,
                        "nombre_cientifico": "",
                        "clasificacion":     {},
                        "fuente":            "dbpedia"
                    })

        except Exception as e:
            print(f"❌ Error details: {e}")
            # Sin internet — buscar en Fuseki directamente
            try:
                import requests as req2
                sparql_q = f"""
                PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                PREFIX foaf: <http://xmlns.com/foaf/0.1/>
                PREFIX dbo:  <http://dbpedia.org/ontology/>
                SELECT ?label ?thumbnail ?abstract
                WHERE {{
                    <{uri}> rdfs:label ?label .
                    FILTER(lang(?label) = "{lang}")
                    OPTIONAL {{ <{uri}> foaf:depiction ?thumbnail . }}
                    OPTIONAL {{ <{uri}> dbo:abstract ?abstract . FILTER(lang(?abstract) = "{lang}") }}
                }} LIMIT 1
                """
                resp = req2.post(
                    "http://localhost:3030/animales/query",
                    data={"query": sparql_q},
                    headers={"Accept": "application/sparql-results+json"},
                    timeout=5
                )
                if resp.status_code == 200:
                    bindings = resp.json().get("results", {}).get("bindings", [])
                    if bindings:
                        r = bindings[0]
                        return jsonify({
                            "uri":               uri,
                            "labels":            {lang: r.get("label", {}).get("value", "")},
                            "abstract":          r.get("abstract", {}).get("value", ""),
                            "thumbnail":         r.get("thumbnail", {}).get("value", ""),
                            "nombre_cientifico": "",
                            "clasificacion":     {},
                            "fuente":            "dbpedia"
                        })
            except Exception as e2:
                print(f"❌ Fuseki fallback falló: {e2}")

    return jsonify({"error": "No se encontraron detalles"}), 404


def _traducir(texto):
    """Traduce texto del inglés al español usando MyMemory API (gratuita)."""
    import requests as req
    try:
        # Limitamos a 500 chars para no exceder límites
        texto_corto = texto[:500]
        resp = req.get(
            "https://api.mymemory.translated.net/get",
            params={"q": texto_corto, "langpair": "en|es"},
            timeout=5
        )
        data = resp.json()
        traduccion = data.get("responseData", {}).get("translatedText", "")
        if traduccion and len(traduccion) > 20:
            return traduccion
    except Exception as e:
        print(f"⚠️ Traducción falló: {e}")
    return ""