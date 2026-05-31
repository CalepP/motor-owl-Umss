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
    uri = request.args.get("uri", "").strip()
    if not uri:
        return jsonify({"error": "URI requerida"}), 400

    if "dbpedia.org/resource/" in uri:
        from SPARQLWrapper import SPARQLWrapper, JSON
        import requests as req

        sparql = SPARQLWrapper("https://dbpedia.org/sparql")
        sparql.setTimeout(40)

        q = f"""
        SELECT ?labelEn ?labelEs ?labelFr ?labelPt ?labelDe
               ?abstractEs ?abstractEn ?thumbnail ?scientificName
               ?kingdom ?phylum ?order ?family ?genus
        WHERE {{
            <{uri}> rdfs:label ?labelEn .
            FILTER (lang(?labelEn) = "en")
            OPTIONAL {{ <{uri}> rdfs:label ?labelEs . FILTER (lang(?labelEs) = "es") }}
            OPTIONAL {{ <{uri}> rdfs:label ?labelFr . FILTER (lang(?labelFr) = "fr") }}
            OPTIONAL {{ <{uri}> rdfs:label ?labelPt . FILTER (lang(?labelPt) = "pt") }}
            OPTIONAL {{ <{uri}> rdfs:label ?labelDe . FILTER (lang(?labelDe) = "de") }}
            OPTIONAL {{ <{uri}> <http://dbpedia.org/ontology/abstract> ?abstractEs . FILTER (lang(?abstractEs) = "es") }}
            OPTIONAL {{ <{uri}> <http://dbpedia.org/ontology/abstract> ?abstractEn . FILTER (lang(?abstractEn) = "en") }}
            OPTIONAL {{ <{uri}> <http://dbpedia.org/ontology/thumbnail> ?thumbnail . }}
            OPTIONAL {{ <{uri}> <http://dbpedia.org/ontology/scientificName> ?scientificName . }}
            OPTIONAL {{ <{uri}> <http://dbpedia.org/ontology/kingdom> ?kingdom . }}
            OPTIONAL {{ <{uri}> <http://dbpedia.org/ontology/phylum> ?phylum . }}
            OPTIONAL {{ <{uri}> <http://dbpedia.org/ontology/order> ?order . }}
            OPTIONAL {{ <{uri}> <http://dbpedia.org/ontology/family> ?family . }}
            OPTIONAL {{ <{uri}> <http://dbpedia.org/ontology/genus> ?genus . }}
        }} LIMIT 1
        """

        sparql.setQuery(q)
        sparql.setReturnFormat(JSON)
        for intento in range(2):
            try:
                results = sparql.query().convert()
                bindings = results.get("results", {}).get("bindings", [])
                if bindings:
                    r = bindings[0]
                    def v(key): return r.get(key, {}).get("value", "")

                    labels = {}
                    for lang, key in [("en","labelEn"),("es","labelEs"),
                                       ("fr","labelFr"),("pt","labelPt"),("de","labelDe")]:
                        val = v(key)
                        if val: labels[lang] = val

                    abstract_es = v("abstractEs")
                    abstract_en = v("abstractEn")

                    if not abstract_es and abstract_en:
                        abstract_es = _traducir(abstract_en[:1000])

                    return jsonify({
                        "uri":               uri,
                        "labels":            labels,
                        "abstract":          abstract_es,
                        "thumbnail":         v("thumbnail"),
                        "nombre_cientifico": v("scientificName"),
                        "clasificacion": {
                            "reino":   v("kingdom").split("/")[-1] if v("kingdom") else "",
                            "filo":    v("phylum").split("/")[-1]  if v("phylum")  else "",
                            "orden":   v("order").split("/")[-1]   if v("order")   else "",
                            "familia": v("family").split("/")[-1]  if v("family")  else "",
                            "genero":  v("genus").split("/")[-1]   if v("genus")   else "",
                        },
                        "fuente": "dbpedia"
                    })
                break
            except Exception as e:
                print(f"❌ Intento {intento+1} falló: {e}")

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