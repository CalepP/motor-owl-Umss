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
    "dalmata": "dalmatian",
    "dálmata": "dalmatian",
    "bóxer": "boxer",
    "boxer": "boxer",
    "pomerania": "pomeranian",
    "herviboro":  "herbivore",
    "herviboros": "herbivore",
    "herbivoro":  "herbivore",
    "herbivoros": "herbivore",
    "extincion":             "endangered",
    "en extincion":          "endangered",
    "animales en extincion": "endangered",
    "peligro":               "endangered",
    "en peligro":            "endangered",
    # PT → EN (sin acentos para normalización)
    "leao": "lion", "urso": "bear", "lobo": "wolf", "raposa": "fox",
    "golfinho": "dolphin", "tubarao": "shark", "baleia": "whale",
    "aguia": "eagle", "jacare": "crocodile", "sapo": "frog",
    "tartaruga": "turtle", "borboleta": "butterfly", "abelha": "bee",
    "aranha": "spider", "polvo": "octopus", "girafa": "giraffe",
    "macaco": "monkey", "cavalo": "horse", "coelho": "rabbit",
    "morcego": "bat", "cao": "dog", "pinguim": "penguin",
    "papagaio": "parrot", "rinoceronte": "rhinoceros",
    # DE → EN (sin umlauts para normalización)
    "lowe": "lion", "bar": "bear", "wal": "whale", "hai": "shark",
    "adler": "eagle", "schlange": "snake", "frosch": "frog",
    "krokodil": "crocodile", "pinguin": "penguin", "elefant": "elephant",
    "giraffe": "giraffe", "nashorn": "rhinoceros", "kamel": "camel",
    "hund": "dog", "katze": "cat", "fledermaus": "bat", "hase": "rabbit",
    "schmetterling": "butterfly", "ente": "duck",
    # FR → EN
    "canard": "duck", "renard": "fox", "ours": "bear", "loup": "wolf",
    "dauphin": "dolphin", "baleine": "whale", "requin": "shark",
    "aigle": "eagle", "serpent": "snake", "grenouille": "frog",
    "papillon": "butterfly", "abeille": "bee", "araignee": "spider",
    "pieuvre": "octopus", "girafe": "giraffe", "cheval": "horse",
    "lapin": "rabbit", "chauve-souris": "bat", "manchot": "penguin",
    "perroquet": "parrot", "rhinoceros": "rhinoceros",
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

# Diccionario inverso EN/otros → ES generado automáticamente + adiciones manuales
TRADUCCIONES_ES = {en: es for es, en in TRADUCCIONES_EN.items()}
TRADUCCIONES_ES.update({
    "dogs": "perro", "cats": "gato", "sharks": "tiburon", "whales": "ballena",
    "bears": "oso", "lions": "leon", "tigers": "tigre", "wolves": "lobo",
    "foxes": "zorro", "horses": "caballo", "dolphins": "delfin",
    "crocodiles": "cocodrilo", "penguins": "pinguino", "monkeys": "mono",
    "snakes": "serpiente", "frogs": "rana", "turtles": "tortuga",
    "reptiles": "reptiles", "amphibians": "anfibios", "fish": "peces",
    "insects": "insectos", "mammals": "mamiferos", "birds": "aves",
    "primates": "primates", "spiders": "aracnidos", "parrots": "loro",
    "owls": "buho", "rabbits": "conejo", "bats": "murcielago",
    "elephants": "elefante", "giraffes": "jirafa", "zebras": "cebra",
    "gorillas": "gorila", "chimpanzees": "chimpance",
    # FR → ES
    "chien": "perro", "chat": "gato", "requin": "tiburon", "baleine": "ballena",
    "ours": "oso", "lion": "leon", "tigre": "tigre", "loup": "lobo",
    "dauphin": "delfin", "aigle": "aguila", "serpent": "serpiente",
    "grenouille": "rana", "crocodile": "cocodrilo", "manchot": "pinguino",
    "papillon": "mariposa", "éléphant": "elefante", "girafe": "jirafa",
    "singe": "mono", "perroquet": "loro", "hibou": "buho",
    # PT → ES
    "cão": "perro", "tubarão": "tiburon", "baleia": "ballena",
    "golfinho": "delfin", "águia": "aguila", "cobra": "serpiente",
    "sapo": "rana", "crocodilo": "cocodrilo", "pinguim": "pinguino",
    "borboleta": "mariposa", "elefante": "elefante", "girafa": "jirafa",
    "macaco": "mono", "papagaio": "loro",
    # DE → ES
    "hund": "perro", "katze": "gato", "hai": "tiburon", "wal": "ballena",
    "bär": "oso", "löwe": "leon", "wolf": "lobo", "delfin": "delfin",
    "adler": "aguila", "schlange": "serpiente", "frosch": "rana",
    "krokodil": "cocodrilo", "pinguin": "pinguino", "schmetterling": "mariposa",
    "elefant": "elefante", "giraffe": "jirafa", "affe": "mono", "papagei": "loro",
    # Categorías EN (chips UI)
    "invertebrates": "invertebrados", "invertebrate": "invertebrado",
    "felines": "felinos", "feline": "felino",
    "vertebrates": "vertebrados", "vertebrate": "vertebrado",
    "carnivores": "carnivoros", "carnivore": "carnivoro",
    "herbivores": "herbivoros", "herbivore": "herbivoro",
    "omnivores": "omnivoros", "omnivore": "omnivoro",
    "arachnids": "aracnidos", "arachnid": "aracnido",
    "crustaceans": "crustaceos", "crustacean": "crustaceo",
    "mollusks": "moluscos", "mollusk": "molusco",
    "cetaceans": "cetaceos", "cetacean": "cetaceo",
    "rodents": "roedores", "rodent": "roedor",
    # Categorías FR (chips UI)
    "invertebres": "invertebrados", "invertébrés": "invertebrados",
    "felins": "felinos", "félins": "felinos",
    "mammiferes": "mamiferos", "mammifères": "mamiferos",
    "oiseaux": "aves", "poissons": "peces", "insectes": "insectos",
    "amphibiens": "anfibios", "reptiles": "reptiles",
    "vertebres": "vertebrados", "vertébrés": "vertebrados",
    "carnivores": "carnivoros", "herbivores": "herbivoros",
    # Categorías DE (chips UI)
    "wirbellosen": "invertebrados", "wirbellose": "invertebrados",
    "felinen": "felinos",
    "saugetiere": "mamiferos", "säugetiere": "mamiferos",
    "vogel": "aves", "vögel": "aves", "fische": "peces",
    "insekten": "insectos", "amphibien": "anfibios", "reptilien": "reptiles",
    "primaten": "primates", "krokodile": "cocodrilos",
    # Categorías PT (chips UI)
    "primatas": "primates", "invertebrados": "invertebrados",
    "mamiferos": "mamiferos", "peixes": "peces", "insetos": "insectos",
    "repteis": "reptiles", "anfibios": "anfibios",
})

def _a_espanol(query):
    """Intenta traducir al español un término en cualquier idioma."""
    q = query.lower().strip()
    q_norm = _normalizar(q)
    return TRADUCCIONES_ES.get(q) or TRADUCCIONES_ES.get(q_norm) or q

def search_fuseki(query, lang="es"):
    """Busca en Fuseki local — funciona offline, multilingüe."""
    query_en       = _a_ingles(query)
    query_es       = _a_espanol(query)      # para búsquedas en EN/FR/PT/DE
    query_lower    = query.lower()
    query_en_lower = query_en.lower()
    query_es_lower = query_es.lower()

    # Para búsquedas de tipo "perro", también buscar por clase/tipo
    CLASES_EXTRA = {
        # Perros
        "perro": ["dog", "shepherd", "retriever", "terrier",
                  "bulldog", "poodle", "husky", "collie",
                  "dachshund", "rottweiler", "chihuahua", "beagle",
                  "dalmatian", "dobermann", "schnauzer", "shih tzu",
                  "yorkshire", "border collie", "great dane"],
        # Gatos
        "gato": ["cat", "persian cat", "siamese cat", "maine coon", "bengal cat",
                 "sphynx cat", "british shorthair", "scottish fold", "abyssinian cat"],
        # Tiburones
        "tiburon":  ["shark"],
        "tiburones":["shark"],
        # Ballenas
        "ballena":  ["whale"],
        "ballenas": ["whale"],
        # Delfines
        "delfin":   ["dolphin", "tursiops", "stenella", "delphinus"],
        "delfines": ["dolphin", "tursiops", "stenella"],
        # Águilas y aves rapaces
        "aguila":  ["golden eagle", "bald eagle", "harpy eagle",
                    "eagle", "aquila", "haliaeetus", "harpia"],
        "aguilas": ["golden eagle", "bald eagle", "harpy eagle",
                    "eagle", "aquila", "haliaeetus", "harpia"],
        # Búhos
        "buho":     ["owl", "bubo", "tyto", "strix"],
        "buhos":    ["owl", "bubo", "tyto"],
        # Serpientes
        "serpiente":  ["snake", "viper", "cobra", "python", "anaconda",
                       "mamba", "boa", "dendroaspis", "ophiophagus",
                       "malayopython"],
        "serpientes": ["snake", "viper", "cobra", "python", "anaconda",
                       "mamba", "boa"],
        # Víboras
        "vibora":  ["viper", "dendroaspis", "cobra"],
        "viboras": ["viper", "dendroaspis"],
        # Osos
        "oso":  ["bear", "ailuropoda", "helarctos", "tremarctos", "ailurus"],
        "osos": ["bear", "ailuropoda", "helarctos"],
        # Monos y primates
        "mono":     ["gorilla", "chimpanzee", "orangutan", "gibbon",
                     "bonobo", "mandrill", "baboon", "hylobatidae",
                     "pan troglodytes", "pan paniscus", "mandrillus", "papio"],
        "monos":    ["gorilla", "chimpanzee", "orangutan", "gibbon",
                     "bonobo", "mandrill"],
        "primate":  ["gorilla", "chimpanzee", "orangutan", "gibbon",
                     "bonobo", "mandrill", "baboon", "hylobatidae",
                     "pan troglodytes", "mandrillus", "papio"],
        "primates": ["gorilla", "chimpanzee", "orangutan", "gibbon",
                     "bonobo", "mandrill", "hylobatidae", "mandrillus"],
        # Pingüinos
        "pinguino":  ["penguin", "aptenodytes", "spheniscus"],
        "pingüino":  ["penguin", "aptenodytes", "spheniscus"],
        "pinguinos": ["penguin", "aptenodytes", "spheniscus"],
        "pingüinos": ["penguin", "aptenodytes", "spheniscus"],
        # Loros
        "loro":  ["parrot", "macaw", "cockatoo", "psittaciformes", "cacatuidae"],
        "loros": ["parrot", "macaw", "cockatoo", "psittaciformes"],
        # Dálmata
        "dalmata":   ["dalmatian"],
        "dalmatian": ["dalmatian"],
        # Carnívoros
        "carnivoro":  ["lion", "tiger", "wolf", "shark", "eagle",
                       "crocodile", "snake", "leopard", "jaguar", "cheetah",
                       "orca", "dolphin", "bear", "fox", "hyena"],
        "carnivoros": ["lion", "tiger", "wolf", "shark", "leopard",
                       "jaguar", "cheetah", "orca", "crocodile"],
        # Herbívoros
        "herbivoro":  ["elephant", "giraffe", "zebra", "horse",
                       "rabbit", "kangaroo", "koala", "bison", "camel",
                       "llama", "alpaca", "donkey", "reindeer", "moose"],
        "herbivoros": ["elephant", "giraffe", "zebra", "horse",
                       "rabbit", "kangaroo", "koala", "bison", "camel"],
        "herviboro":  ["elephant", "giraffe", "zebra", "horse",
                       "rabbit", "kangaroo", "koala", "bison", "camel"],
        "herviboros": ["elephant", "giraffe", "zebra", "horse",
                       "rabbit", "kangaroo", "koala"],
        # Omnívoros
        "omnivoro":  ["bear", "chimpanzee", "gorilla", "bonobo"],
        "omnivoros": ["bear", "chimpanzee", "gorilla"],
        # Mamíferos
        "mamifero":  ["dog", "cat", "lion", "whale", "dolphin", "elephant",
                      "bear", "horse", "gorilla", "wolf", "fox", "kangaroo",
                      "koala", "platypus", "seal", "walrus", "otter",
                      "beaver", "capybara", "llama", "camel", "giraffe",
                      "zebra", "rhinoceros", "hippopotamus", "chimpanzee",
                      "orangutan", "gibbon", "meerkat", "hyena"],
        "mamiferos": ["dog", "cat", "lion", "whale", "dolphin", "elephant",
                      "bear", "horse", "gorilla", "wolf", "kangaroo",
                      "koala", "platypus", "seal", "walrus", "giraffe",
                      "zebra", "rhinoceros", "hippopotamus", "chimpanzee"],
        # Reptiles
        "reptil":   ["crocodile", "iguana", "gecko", "chameleon", "snake",
                     "viper", "anaconda", "komodo", "varanus", "monitor",
                     "heloderma", "boa", "python", "chamaeleonidae",
                     "gekkota", "crocodylus"],
        "reptiles": ["crocodile", "iguana", "gecko", "chameleon", "snake",
                     "anaconda", "komodo", "varanus", "chamaeleonidae",
                     "gekkota", "crocodylus"],
        # Anfibios
        "anfibio":  ["frog", "toad", "axolotl", "salamander", "caudata",
                     "bullfrog", "dendrobatidae", "ambystoma"],
        "anfibios": ["frog", "axolotl", "salamander", "caudata",
                     "bullfrog", "dendrobatidae", "ambystoma"],
        # Aves — SIN "bird" para evitar falsos positivos
        "ave":  ["golden eagle", "bald eagle", "harpy eagle", "great horned owl",
                 "barn owl", "snowy owl", "emperor penguin", "african penguin",
                 "peregrine falcon", "flamingo", "toucan", "ostrich", "macaw",
                 "cockatoo", "hummingbird", "aquila", "haliaeetus", "harpia",
                 "falco", "bubo", "tyto", "phoenicopterus", "ramphastidae",
                 "struthio", "aptenodytes", "spheniscus", "trochilidae",
                 "psittaciformes", "cacatuidae"],
        "aves": ["golden eagle", "bald eagle", "harpy eagle", "great horned owl",
                 "barn owl", "snowy owl", "emperor penguin", "peregrine falcon",
                 "flamingo", "toucan", "macaw", "cockatoo", "hummingbird",
                 "aquila", "haliaeetus", "harpia", "falco", "bubo", "tyto",
                 "phoenicopterus", "ramphastidae", "struthio", "aptenodytes",
                 "spheniscus", "psittaciformes", "cacatuidae"],
        # Peces — SIN "fish" para evitar falsos positivos
        "pez":   ["salmon", "tuna", "clownfish", "piranha", "swordfish",
                  "seahorse", "manta ray", "stingray", "electric eel",
                  "salmo", "amphiprioninae", "xiphias", "hippocampus",
                  "thunini", "myliobatoidei", "electrophorus"],
        "peces": ["salmon", "tuna", "clownfish", "piranha", "swordfish",
                  "seahorse", "salmo", "amphiprioninae", "xiphias",
                  "thunini", "electrophorus"],
        # Insectos — solo términos específicos de insectos
        "insecto":  ["honeybee", "bumblebee", "carpenter bee", "dragonfly",
                     "monarch butterfly", "formicidae", "isoptera",
                     "lampyridae", "anisoptera", "xylocopa", "bombus",
                     "danaus", "butterfly"],
        "insectos": ["honeybee", "bumblebee", "dragonfly", "monarch butterfly",
                     "formicidae", "isoptera", "lampyridae", "anisoptera",
                     "xylocopa", "bombus", "danaus", "butterfly"],
        # Arácnidos
        "aracnido":  ["spider", "tarantula", "scorpion", "theraphosidae",
                      "scorpiones", "lycosidae", "black widow"],
        "aracnidos": ["spider", "tarantula", "scorpion", "theraphosidae",
                      "scorpiones", "lycosidae"],
        # Crustáceos
        "crustaceo":  ["crab", "lobster", "shrimp", "crayfish",
                       "stomatopoda", "limulidae", "macrocheira",
                       "nephropidae", "astacus", "paguroidea"],
        "crustaceos": ["crab", "lobster", "shrimp", "stomatopoda",
                       "macrocheira", "nephropidae", "astacus"],
        # Moluscos
        "molusco":  ["octopus", "squid", "nautilus", "clam",
                     "octopoda", "architeuthis", "nautilina", "tridacna"],
        "moluscos": ["octopus", "squid", "nautilus", "clam",
                     "octopoda", "architeuthis", "nautilina"],
        # Invertebrados
        "invertebrado":  ["octopus", "crab", "bee", "butterfly", "squid",
                          "bumblebee", "jellyfish", "spider", "mantis",
                          "horseshoe", "starfish", "urchin", "lobster",
                          "shrimp", "scorpion", "tarantula", "stomatopoda",
                          "limulidae", "macrocheira", "asteroidea",
                          "echinoidea", "medusa", "cubozoa", "formicidae",
                          "isoptera", "lampyridae", "anisoptera", "bombus"],
        "invertebrados": ["octopus", "crab", "butterfly", "squid",
                          "bumblebee", "jellyfish", "spider", "scorpion",
                          "starfish", "lobster", "shrimp", "stomatopoda",
                          "macrocheira", "asteroidea", "echinoidea",
                          "medusa", "cubozoa", "formicidae", "bombus"],
        # Vertebrados
        "vertebrado":  ["salmon", "eagle", "owl", "penguin", "dolphin",
                        "whale", "lion", "tiger", "bear", "horse", "dog",
                        "cat", "snake", "crocodile", "iguana", "frog",
                        "shark", "gorilla", "elephant", "giraffe", "zebra",
                        "wolf", "fox", "kangaroo", "koala", "chimpanzee"],
        "vertebrados": ["salmon", "eagle", "penguin", "dolphin", "whale",
                        "lion", "tiger", "bear", "horse", "dog", "cat",
                        "snake", "crocodile", "frog", "shark", "gorilla",
                        "elephant", "giraffe", "wolf", "kangaroo"],
        # Felinos
        "felino":  ["lion", "tiger", "cheetah", "leopard", "jaguar",
                    "puma", "snow leopard", "clouded leopard", "caracal",
                    "bengal tiger"],
        "felinos": ["lion", "tiger", "cheetah", "leopard", "jaguar",
                    "puma", "snow leopard", "clouded leopard", "caracal",
                    "bengal tiger"],
        # Roedores
        "roedor":  ["beaver", "capybara", "rabbit", "castor",
                    "hydrochoerus"],
        "roedores":["beaver", "capybara", "rabbit", "castor"],
        # Cetáceos
        "cetaceo":  ["whale", "dolphin", "orca", "narwhal", "beluga",
                     "tursiops", "stenella", "delphinus", "delphinapterus",
                     "monodon", "physeter", "megaptera", "balaenoptera"],
        "cetaceos": ["whale", "dolphin", "orca", "narwhal", "tursiops",
                     "stenella", "delphinapterus", "physeter", "balaenoptera"],
                     "extincion":         ["endangered", "critically", "threatened", "extinct",
                      "gorilla", "tiger", "polar bear", "blue whale",
                      "snow leopard", "orangutan", "chimpanzee", "rhinoceros",
                      "vaquita", "amur leopard", "sumatran"],
"en extincion":      ["endangered", "critically", "threatened",
                      "gorilla", "tiger", "polar bear", "blue whale",
                      "snow leopard", "orangutan", "rhinoceros"],
"animales en extincion": ["endangered", "critically", "threatened",
                          "gorilla", "tiger", "polar bear", "blue whale",
                          "snow leopard", "orangutan", "rhinoceros"],
"peligro":           ["endangered", "critically", "threatened",
                      "gorilla", "tiger", "polar bear", "snow leopard"],
"en peligro":        ["endangered", "critically", "threatened",
                      "gorilla", "tiger", "polar bear", "snow leopard"],
"dalmata":           ["dalmatian"],
"dálmata":           ["dalmatian"],
"perro dalmata":     ["dalmatian"],
    }

    # Construir filtros adicionales (busca en ES y, si es búsqueda no-española, también por equivalente ES)
    extras = CLASES_EXTRA.get(query_lower, CLASES_EXTRA.get(_normalizar(query_lower), []))
    if not extras and query_es_lower != query_lower:
        extras = CLASES_EXTRA.get(query_es_lower, CLASES_EXTRA.get(_normalizar(query_es_lower), []))
    
    # Construir filtros de CLASES_EXTRA con palabras completas
    filtros_extra = ""
    if extras:
        condiciones = []
        for t in extras:
            t_lower = t.lower()
            condiciones.append(
                f'(LCASE(str(?labelEn)) = "{t_lower}" || '
                f'STRSTARTS(LCASE(str(?labelEn)), "{t_lower} ") || '
                f'STRENDS(LCASE(str(?labelEn)), " {t_lower}") || '
                f'CONTAINS(LCASE(str(?labelEn)), " {t_lower} ") || '
                f'STRENDS(LCASE(str(?labelEn)), "({t_lower})"))'
            )
        filtros_extra = "|| " + " ||\n            ".join(condiciones)

    query_norm    = _normalizar(query_lower)
    query_es_norm = _normalizar(query_es_lower)

    # Label opcional en el idioma pedido (solo cuando no es español)
    if lang != "es":
        label_lang_optional = f'OPTIONAL {{ ?animal rdfs:label ?labelLang . FILTER(lang(?labelLang) = "{lang}") }}'
        label_lang_filter   = (f'|| CONTAINS(LCASE(str(?labelLang)), "{query_lower}")'
                               f'|| CONTAINS(LCASE(str(?labelLang)), "{query_norm}")')
    else:
        label_lang_optional = ""
        label_lang_filter   = ""

    sparql_query = f"""
    PREFIX rdfs:  <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX owl:   <http://www.w3.org/2002/07/owl#>
    PREFIX dbo:   <http://dbpedia.org/ontology/>
    PREFIX foaf:  <http://xmlns.com/foaf/0.1/>

    SELECT DISTINCT ?animal ?labelEs ?labelLang ?labelEn ?sci ?abstract ?thumbnail
    WHERE {{
        ?animal a owl:NamedIndividual .
        ?animal rdfs:label ?labelEs .
        FILTER(lang(?labelEs) = "es")
        {label_lang_optional}
        OPTIONAL {{ ?animal rdfs:label ?labelEn . FILTER(lang(?labelEn) = "en") }}
        OPTIONAL {{ ?animal dbo:scientificName ?sci . }}
        OPTIONAL {{ ?animal dbo:abstract ?abstract .
                   FILTER(lang(?abstract) = "{lang}" || (lang(?abstract) = "es" && "{lang}" != "es")) }}
        OPTIONAL {{ ?animal foaf:depiction ?thumbnail . }}
        FILTER(
            CONTAINS(LCASE(str(?labelEs)),  "{query_es_lower}") ||
            CONTAINS(LCASE(str(?labelEs)),  "{query_es_norm}") ||
            CONTAINS(LCASE(str(?labelEn)),  "{query_en_lower}") ||
            CONTAINS(LCASE(str(?labelEn)),  "{query_norm}")
            {label_lang_filter}
            {filtros_extra}
        )
    }}
    ORDER BY ?labelEs
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
        print(f"[Fuseki] '{query}' -> {len(resultados)} resultados")
        return resultados
    except Exception as e:
        print(f"[Fuseki] no disponible: {e}")
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
            print(f"[DBpedia live] '{query_en}' -> {len(animales)} resultados")
            return animales
        except Exception as e:
            if intento == RETRIES:
                print(f"[DBpedia live] fallo: {e}")
                return []
    return []

def _parse_fuseki(data, lang):
    animales = {}  # uri -> datos

    for r in data.get("results", {}).get("bindings", []):
        uri        = r.get("animal",    {}).get("value", "")
        label_es   = r.get("labelEs",   {}).get("value", "")
        label_lang = r.get("labelLang", {}).get("value", "")
        label_en   = r.get("labelEn",   {}).get("value", "")
        sci        = r.get("sci",       {}).get("value", "")
        abstract   = r.get("abstract",  {}).get("value", "")
        thumbnail  = r.get("thumbnail", {}).get("value", "")

        if not uri:
            continue

        # Nombre a mostrar: idioma pedido > español > inglés
        nombre = label_lang or label_es or label_en

        if uri not in animales:
            fuente = "local" if "semanticweb.org" in uri else "dbpedia"
            labels = {"es": label_es} if label_es else {}
            if label_en:
                labels["en"] = label_en
            if label_lang and lang not in labels:
                labels[lang] = label_lang
            animales[uri] = {
                "id":                uri.split("#")[-1].split("/")[-1],
                "uri":               uri,
                "nombre":            nombre,
                "labels":            labels,
                "abstract":          abstract,
                "nombre_cientifico": sci,
                "thumbnail":         thumbnail,
                "same_as":           uri,
                "fuente":            fuente
            }
        else:
            entry = animales[uri]
            if not entry["thumbnail"] and thumbnail:
                entry["thumbnail"] = thumbnail
            if not entry["abstract"] and abstract:
                entry["abstract"] = abstract
            if not entry["nombre_cientifico"] and sci:
                entry["nombre_cientifico"] = sci
            if label_en and "en" not in entry["labels"]:
                entry["labels"]["en"] = label_en
            if label_lang and lang not in entry["labels"]:
                entry["labels"][lang] = label_lang
            # Actualizar nombre si ahora tenemos etiqueta en el idioma pedido
            if label_lang and not (entry["nombre"] and entry["nombre"] != label_es):
                entry["nombre"] = label_lang

    return list(animales.values())

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