import re
import requests

WIKIDATA_SPARQL = "https://query.wikidata.org/sparql"
HEADERS = {
    "Accept":     "application/sparql-results+json",
    "User-Agent": "MotorOWL/1.0 (UMSS Grupo10; contacto@umss.edu)"
}

# Clases Wikidata para búsquedas directas de tipo/raza
QUERY_CLASE = {
    "perro":  "Q39367", "perros":  "Q39367",
    "dog":    "Q39367", "dogs":    "Q39367",
    "chien":  "Q39367", "hund":    "Q39367", "cao": "Q39367",
    "gato":   "Q146",   "gatos":   "Q146",
    "cat":    "Q146",   "cats":    "Q146",
    "chat":   "Q146",   "katze":   "Q146",
}

# Traducción a español para búsqueda en Wikidata.
# "gato " en ES es exclusivo de felinos; "cat " en EN devuelve "cat snake", "cat shark"…
_A_ES = {
    # EN → ES
    "cat":"gato","cats":"gato","shark":"tiburon","sharks":"tiburon",
    "whale":"ballena","whales":"ballena","snake":"serpiente","snakes":"serpiente",
    "frog":"rana","frogs":"rana","toad":"sapo","eagle":"aguila","eagles":"aguila",
    "owl":"buho","owls":"buho","crocodile":"cocodrilo","turtle":"tortuga",
    "butterfly":"mariposa","lion":"leon","tiger":"tigre","bear":"oso",
    "wolf":"lobo","fox":"zorro","dolphin":"delfin","dolphins":"delfin",
    "penguin":"pinguino","parrot":"loro","bee":"abeja","spider":"arana",
    "octopus":"pulpo","crab":"cangrejo","lobster":"langosta",
    "salmon":"salmon","piranha":"pirana","elephant":"elefante",
    "giraffe":"jirafa","zebra":"cebra","gorilla":"gorila","chimp":"chimpance",
    "chimpanzee":"chimpance","orangutan":"orangutan","monkey":"mono",
    "kangaroo":"canguro","koala":"koala","fish":"peces","bird":"ave",
    "reptile":"reptil","amphibian":"anfibio","insect":"insecto",
    "mammal":"mamifero","primate":"primate","horse":"caballo",
    "rabbit":"conejo","bat":"murcielago","deer":"ciervo",
    "jaguar":"jaguar","puma":"puma","leopard":"leopardo","cheetah":"guepardo",
    "orca":"orca","jellyfish":"medusa","starfish":"estrella",
    "flamingo":"flamenco","toucan":"tucan","hummingbird":"colibri",
    "scorpion":"escorpion","wasp":"avispa","ant":"hormiga",
    "rhinoceros":"rinoceronte","hippopotamus":"hipopotamo","camel":"camello",
    "llama":"llama","alpaca":"alpaca","bison":"bisonte","duck":"pato",
    "hedgehog":"erizo","bat":"murcielago","rat":"rata","mouse":"raton",
    # FR → ES
    "chat":"gato","requin":"tiburon","baleine":"ballena",
    "serpent":"serpiente","grenouille":"rana","aigle":"aguila",
    "hibou":"buho","crocodile":"cocodrilo","tortue":"tortuga",
    "papillon":"mariposa","ours":"oso","loup":"lobo",
    "renard":"zorro","dauphin":"delfin","manchot":"pinguino",
    "perroquet":"loro","abeille":"abeja","araignee":"arana",
    "pieuvre":"pulpo","girafe":"jirafa","gorille":"gorila",
    "kangourou":"canguro","cheval":"caballo","lapin":"conejo",
    "chauve-souris":"murcielago","cerf":"ciervo","rhinoceros":"rinoceronte",
    "hippopotame":"hipopotamo","chameau":"camello","flamant":"flamenco",
    "canard":"pato","lion":"leon","tigre":"tigre",
    # PT → ES
    "tubarao":"tiburon","baleia":"ballena","cobra":"serpiente",
    "sapo":"rana","aguia":"aguila","coruja":"buho",
    "jacare":"cocodrilo","tartaruga":"tortuga","borboleta":"mariposa",
    "leao":"leon","urso":"oso","raposa":"zorro","golfinho":"delfin",
    "pinguim":"pinguino","papagaio":"loro","abelha":"abeja",
    "aranha":"arana","polvo":"pulpo","girafa":"jirafa",
    "macaco":"mono","cavalo":"caballo","coelho":"conejo",
    "morcego":"murcielago","rinoceronte":"rinoceronte","pato":"pato",
    # DE → ES
    "katze":"gato","hai":"tiburon","wal":"ballena",
    "schlange":"serpiente","frosch":"rana","adler":"aguila",
    "eule":"buho","krokodil":"cocodrilo","schildkrote":"tortuga",
    "schmetterling":"mariposa","lowe":"leon","bar":"oso",
    "wolf":"lobo","fuchs":"zorro","pinguin":"pinguino",
    "papagei":"loro","biene":"abeja","spinne":"arana",
    "elefant":"elefante","giraffe":"jirafa","gorilla":"gorila",
    "pferd":"caballo","hase":"conejo","fledermaus":"murcielago",
    "nashorn":"rinoceronte","nilpferd":"hipopotamo","kamel":"camello",
    "ente":"pato",
}


def _normalizar(q: str) -> str:
    q = q.lower().strip()
    for src, dst in zip("áàäéèëíìïóòöúùüñ", "aaaeeeiiioooouuun"):
        q = q.replace(src, dst)
    return q


def _a_espanol(q: str) -> str:
    q_lower = q.lower().strip()
    q_norm  = _normalizar(q_lower)
    return _A_ES.get(q_lower) or _A_ES.get(q_norm) or q_lower


def _es_codigo_tecnico(label: str) -> bool:
    s = label.strip()
    if '_' in s and ' ' not in s:                     return True
    if re.match(r'^[A-Z0-9]{3,}$', s):               return True
    if re.match(r'^[A-Za-z]{1,6}\d+[A-Za-z]?$', s): return True
    return False


WIKIDATA_API = "https://www.wikidata.org/w/api.php"


# Palabras clave en descripciones de Wikidata que indican que es un animal
_ANIMAL_KEYWORDS = {
    "es": ("especie", "ave", "mamifero", "reptil", "pez", "insecto", "anfibio",
           "animal", "raza", "felino", "primate", "cetaceo", "roedor", "arácnido",
           "crustáceo", "molusco", "invertebrado", "vertebrado", "pajaro",
           "pajaro", "aves", "pájaro", "volador", "acuático", "terrestre",
           "can", "felid", "canin"),
    "en": ("species", "bird", "mammal", "reptile", "fish", "insect", "amphibian",
           "animal", "breed", "feline", "primate", "cetacean", "rodent",
           "arachnid", "crustacean", "mollusk", "invertebrate", "vertebrate",
           "fauna", "wildlife", "canine", "felid", "aquatic"),
    "fr": ("espèce", "oiseau", "mammifère", "reptile", "poisson", "insecte",
           "amphibien", "animal", "félin", "primate", "cétacé", "rongeur",
           "race", "volatile"),
}


def _es_animal_por_descripcion(description: str) -> bool:
    """Heurística rápida: si la descripción contiene palabras de animales, es un animal."""
    if not description:
        return False
    desc_lower = description.lower()
    for kws in _ANIMAL_KEYWORDS.values():
        for kw in kws:
            if kw in desc_lower:
                return True
    return False


def _buscar_candidatos(query_es: str, lang: str = "es") -> list:
    """
    wbsearchentities en español + validación por descripción (sin SPARQL).
    Devuelve lista de dicts con los campos necesarios para la tarjeta.
    Ventaja: no depende del endpoint SPARQL de Wikidata (más rápido y fiable).
    """
    # Buscar en español siempre (más preciso que en otros idiomas para animales)
    try:
        resp = requests.get(
            WIKIDATA_API,
            params={
                "action":   "wbsearchentities",
                "search":   query_es,
                "language": "es",
                "uselang":  "es",
                "type":     "item",
                "limit":    "50",
                "format":   "json",
            },
            headers=HEADERS,
            timeout=8,
        )
        if resp.status_code != 200:
            return []

        results     = []
        seen_labels = set()

        for item in resp.json().get("search", []):
            eid         = item.get("id", "")
            label_es    = item.get("label", "")
            description = item.get("description", "")

            if not eid or not label_es:
                continue
            if _es_codigo_tecnico(label_es):
                continue
            if not _es_animal_por_descripcion(description):
                continue

            label_norm = label_es.lower().strip()
            if label_norm in seen_labels:
                continue
            seen_labels.add(label_norm)

            uri    = f"http://www.wikidata.org/entity/{eid}"
            nombre = label_es

            labels = {"es": label_es}
            if lang != "es":
                labels[lang] = label_es  # se enriquece en get_details

            results.append({
                "id":                eid,
                "uri":               uri,
                "nombre":            nombre,
                "labels":            labels,
                "abstract":          description,
                "nombre_cientifico": "",
                "thumbnail":         "",
                "fuente":            "wikidata",
            })

        return results
    except Exception as e:
        print(f"[Wikidata] candidatos error: {e}")
        return []


def search_wikidata_owl(query: str, lang: str = "es") -> list:
    """
    MODO A — perro/dog/chien/katze/gato/cat → instancias de la clase Q39367/Q146.
    MODO B — otros animales: busca en labels ESPAÑOLES para evitar falsos positivos.
      "gato " en ES es exclusivo de felinos; "cat " en EN devolvería "cat snake", etc.
    """
    lang_wd     = lang if lang in ("es", "en", "fr", "pt", "de") else "es"
    query_lower = query.lower().strip()
    query_norm  = _normalizar(query_lower)

    clase_id = QUERY_CLASE.get(query_lower) or QUERY_CLASE.get(query_norm)

    if clase_id:
        # ── MODO A: razas/instancias directas de perro/gato ──────────────────
        query_es_ = _a_espanol(query_lower)
        todos     = _buscar_candidatos(query_es_, lang)

        # Filtrar: label_es debe empezar con la query o ser exactamente la query
        q_norm = _normalizar(query_es_)
        results = [
            r for r in todos
            if (_normalizar(r["labels"].get("es", "")) == q_norm
                or _normalizar(r["labels"].get("es", "")).startswith(q_norm + " "))
        ]
        print(f"[Wikidata] '{query}' ({lang}) -> {len(results)} resultados [MODO A clase:{clase_id}]")
        return results[:30]
    else:
        # ── MODO B: taxón en español → wbsearchentities + filtro por descripción ──
        # No usa SPARQL (evita timeouts en endpoints lentos)
        query_es = _a_espanol(query_lower)
        todos    = _buscar_candidatos(query_es, lang)
        if not todos:
            return []

        # Filtrar: comparar normalizado (sin acentos) para manejar "tiburon"↔"tiburón"
        q_norm = _normalizar(query_es)
        results = [
            r for r in todos
            if (_normalizar(r["labels"].get("es", "")) == q_norm
                or _normalizar(r["labels"].get("es", "")).startswith(q_norm + " "))
        ]
        print(f"[Wikidata] '{query}'->ES:'{query_es}' ({lang}) -> {len(results)} resultados [MODO B]")
        return results[:30]

