import unicodedata
from flask import Blueprint, jsonify, request
from ..ontology.loader import search_local
from ..sparql.fuseki import search_fuseki, search_dbpedia_live

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
    per_page = int(request.args.get("per_page", 50))

    if not query:
        return jsonify({"error": "Parámetro q requerido"}), 400

    # 1. Buscar en Fuseki (offline + dump DBpedia)
    fuseki_results = search_fuseki(query, lang)

    # 2. Buscar en DBpedia en vivo SOLO si Fuseki no encontró nada
    live_results = []
    if not fuseki_results:
        live_results = search_dbpedia_live(query, lang)

    # 3. Combinar sin duplicados (Fuseki primero)
    uris_fuseki = {r["uri"] for r in fuseki_results}
    all_results = fuseki_results + [
        r for r in live_results
        if r["uri"] not in uris_fuseki
    ]

    # 4. Sugerencia ortográfica si no hay resultados
    sugerencia = None
    if not all_results:
        correccion = CORRECCIONES.get(_normalizar(query))
        if correccion:
            sugerencia = f"¿Quisiste decir: {correccion}?"

    # 5. Paginación
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