import unicodedata
from concurrent.futures import ThreadPoolExecutor
from flask import Blueprint, jsonify, request
from ..sparql.fuseki import search_fuseki, search_dbpedia_live
from ..sparql.dbpedia_owl import search_dbpedia_owl
from ..sparql.wikidata_owl import search_wikidata_owl

bp = Blueprint("search", __name__)

def _normalizar(texto):
    return ''.join(
        c for c in unicodedata.normalize('NFD', texto.lower())
        if unicodedata.category(c) != 'Mn'
    )

CORRECCIONES = {
    "aguila":       "águila",
    "buho":         "búho",
    "salmon":       "salmón",
    "delfin":       "delfín",
    "pinguino":     "pingüino",
    "vibora":       "víbora",
    "arana":        "araña",
    "murcielago":   "murciélago",
    "orangutan":    "orangután",
    "colibri":      "colibrí",
    "condor":       "cóndor",
    "hipopotamo":   "hipopótamo",
    "esturion":     "esturión",
    "leon":         "león",
    "aguila real":  "águila real",
    "rana arborea": "rana arbórea",
    "pirana":       "piraña",
    "tucan":        "tucán",
    "chimpance":    "chimpancé",
}

@bp.route("/", methods=["GET"])
def search():
    query    = request.args.get("q", "").strip()
    lang     = request.args.get("lang", "es")
    page     = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 100))
    online   = request.args.get("online", "true").lower() == "true"

    if not query:
        return jsonify({"error": "Parámetro q requerido"}), 400

    # 1. Buscar en Fuseki (offline + dump DBpedia)
    fuseki_results = search_fuseki(query, lang)

    # 2. DBpedia OWL y Wikidata en paralelo, timeout individual 10s cada uno
    owl_results = []
    wikidata_results = []
    if online:
        with ThreadPoolExecutor(max_workers=2) as executor:
            future_owl  = executor.submit(search_dbpedia_owl, query, lang)
            future_wiki = executor.submit(search_wikidata_owl, query, lang)
            try:
                owl_results = future_owl.result(timeout=10)
            except Exception:
                owl_results = []
            try:
                wikidata_results = future_wiki.result(timeout=10)
            except Exception:
                wikidata_results = []
    # 3. Buscar en DBpedia live si no hay resultados en Fuseki
    live_results = []
    if not fuseki_results and online:
        live_results = search_dbpedia_live(query, lang)

    # 4. Combinar sin duplicados (Fuseki primero, luego OWL, Wikidata, luego live)
    uris_vistas = {r["uri"] for r in fuseki_results}
    for r in owl_results + wikidata_results + live_results:
        if r["uri"] not in uris_vistas:
            fuseki_results.append(r)
            uris_vistas.add(r["uri"])

    all_results = fuseki_results
            
    # 5. Sugerencia ortografica si no hay resultados
    sugerencia = None
    if not all_results:
        correccion = CORRECCIONES.get(_normalizar(query))
        if correccion:
            sugerencia = f"¿Quisiste decir: {correccion}?"

    # 6. Paginacion
    total = len(all_results)
    start = (page - 1) * per_page
    end   = start + per_page

    return jsonify({
        "query":      query,
        "lang":       lang,
        "total":      total,
        "page":       page,
        "per_page":   per_page,
        "sugerencia": sugerencia,
        "results":    all_results[start:end]
    })