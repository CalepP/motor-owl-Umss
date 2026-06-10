// =====================
// TRADUCCIONES DE INTERFAZ
// =====================
const I18N = {
  es: {
    placeholder: "Busca un animal... ej: perro, tiburón, víbora",
    explorar: "EXPLORAR POR CATEGORÍA",
    resultados: "Resultados para",
    encontrados: "animales encontrados",
    encontrado: "animal encontrado",
    sinResultados: "Sin resultados",
    sinResultadosMsg: "No encontramos animales para",
    intentar: "Intenta con otra palabra.",
    errorConexion: "Error de conexión",
    errorMsg: "No se pudo conectar con el servidor. ¿Está corriendo Flask?",
    cargando: "Cargando detalles...",
    descripcion: "📖 Descripción",
    nombreCientifico: "🔬 Nombre científico",
    clasificacion: "🧬 Clasificación taxonómica",
    nombresIdiomas: "🌍 Nombres en otros idiomas",
    uriSemantica: "🔗 URI semántica",
    fuente: "📦 Fuente",
    fuenteLocal: "Ontología OWL local (Grupo 10 UMSS)",
    fuenteDBpedia: "DBpedia — Linked Open Data",
    verDBpedia: "Ver en DBpedia →",
    sinDescripcion: "Sin descripción disponible en este idioma.",
    localOwl: "Local OWL",
    brandSub: "Motor de búsqueda semántica · UMSS 2026 · Grupo 10",
    categorias: "Mamíferos,Aves,Reptiles,Anfibios,Peces,Insectos,Tiburones,Ballenas,Perros,Gatos,Felinos,Elefantes,Invertebrados,Primates,Cocodrilos,Águilas",
    quisiste: "¿Quisiste decir:",
  },
  en: {
    placeholder: "Search an animal... e.g: dog, shark, viper",
    explorar: "EXPLORE BY CATEGORY",
    resultados: "Results for",
    encontrados: "animals found",
    encontrado: "animal found",
    sinResultados: "No results",
    sinResultadosMsg: "We found no animals for",
    intentar: "Try another word.",
    errorConexion: "Connection error",
    errorMsg: "Could not connect to the server. Is Flask running?",
    cargando: "Loading details...",
    descripcion: "📖 Description",
    nombreCientifico: "🔬 Scientific name",
    clasificacion: "🧬 Taxonomic classification",
    nombresIdiomas: "🌍 Names in other languages",
    uriSemantica: "🔗 Semantic URI",
    fuente: "📦 Source",
    fuenteLocal: "Local OWL Ontology (Group 10 UMSS)",
    fuenteDBpedia: "DBpedia — Linked Open Data",
    verDBpedia: "View on DBpedia →",
    sinDescripcion: "No description available in this language.",
    localOwl: "Local OWL",
    brandSub: "Semantic search engine · UMSS 2026 · Group 10",
    categorias: "Mammals,Birds,Reptiles,Amphibians,Fish,Insects,Sharks,Whales,Dogs,Cats,Felines,Elephants,Invertebrates,Primates,Crocodiles,Eagles",
    quisiste: "Did you mean:",
  },
  fr: {
    placeholder: "Chercher un animal... ex: chien, requin, vipère",
    explorar: "EXPLORER PAR CATÉGORIE",
    resultados: "Résultats pour",
    encontrados: "animaux trouvés",
    encontrado: "animal trouvé",
    sinResultados: "Aucun résultat",
    sinResultadosMsg: "Nous n'avons trouvé aucun animal pour",
    intentar: "Essayez un autre mot.",
    errorConexion: "Erreur de connexion",
    errorMsg: "Impossible de se connecter au serveur. Flask est-il en cours d'exécution?",
    cargando: "Chargement des détails...",
    descripcion: "📖 Description",
    nombreCientifico: "🔬 Nom scientifique",
    clasificacion: "🧬 Classification taxonomique",
    nombresIdiomas: "🌍 Noms dans d'autres langues",
    uriSemantica: "🔗 URI sémantique",
    fuente: "📦 Source",
    fuenteLocal: "Ontologie OWL locale (Groupe 10 UMSS)",
    fuenteDBpedia: "DBpedia — Linked Open Data",
    verDBpedia: "Voir sur DBpedia →",
    sinDescripcion: "Aucune description disponible dans cette langue.",
    localOwl: "OWL Local",
    brandSub: "Moteur de recherche sémantique · UMSS 2026 · Groupe 10",
    categorias: "Mammifères,Oiseaux,Reptiles,Amphibiens,Poissons,Insectes,Requins,Baleines,Chiens,Chats,Félins,Éléphants,Invertébrés,Primates,Crocodiles,Aigles",
    quisiste: "Vouliez-vous dire:",
  }
};

let uiLang = "es"; // idioma de interfaz actual
function t(key) { return I18N[uiLang][key] || I18N.es[key] || key; }
const API = "http://127.0.0.1:5000";

const SUGERENCIAS = {
  es: ["perro", "tiburón", "león", "serpiente", "águila", "delfín", "oso polar", "mariposa monarca", "cocodrilo", "pingüino"],
  en: ["dog", "shark", "lion", "snake", "eagle", "dolphin", "polar bear", "monarch butterfly", "crocodile", "penguin"],
  fr: ["chien", "requin", "lion", "serpent", "aigle", "dauphin", "ours polaire", "papillon monarque", "crocodile", "manchot"],
  pt: ["cão", "tubarão", "leão", "cobra", "águia", "golfinho", "urso polar", "borboleta monarca", "crocodilo", "pinguim"],
  de: ["Hund", "Hai", "Löwe", "Schlange", "Adler", "Delfin", "Eisbär", "Monarchfalter", "Krokodil", "Pinguin"],
};

// Color único por categoría — se aplica como --btn-c en el botón
const DOMAIN_COLORS = [
  "#f97316", // Mamíferos  – naranja
  "#0ea5e9", // Aves       – cielo
  "#22c55e", // Reptiles   – verde
  "#06b6d4", // Anfibios   – cian
  "#6366f1", // Peces      – índigo
  "#eab308", // Insectos   – amarillo
  "#0891b2", // Tiburones  – cian oscuro
  "#7c3aed", // Ballenas   – violeta
  "#d97706", // Perros     – ámbar
  "#a855f7", // Gatos      – púrpura
  "#dc2626", // Felinos    – rojo
  "#78716c", // Elefantes  – piedra
  "#f43f5e", // Invertebrados – rosa
  "#92400e", // Primates   – marrón
  "#15803d", // Cocodrilos – verde oscuro
  "#ea580c", // Águilas    – naranja intenso
];

const DOMINIOS = [
  { emoji: "🐾", q: { es: "mamiferos",    en: "mammals",       fr: "mammiferes",  pt: "mamiferos",    de: "mammals"    } },
  { emoji: "🐦", q: { es: "aves",         en: "birds",         fr: "oiseaux",     pt: "aves",         de: "vogel"      } },
  { emoji: "🐍", q: { es: "reptiles",     en: "reptiles",      fr: "reptiles",    pt: "repteis",      de: "reptilien"  } },
  { emoji: "🐸", q: { es: "anfibios",     en: "amphibians",    fr: "amphibiens",  pt: "anfibios",     de: "amphibien"  } },
  { emoji: "🐟", q: { es: "peces",        en: "fish",          fr: "poissons",    pt: "peixes",       de: "fische"     } },
  { emoji: "🦋", q: { es: "insectos",     en: "insects",       fr: "insectes",    pt: "insetos",      de: "insekten"   } },
  { emoji: "🦈", q: { es: "tiburon",      en: "shark",         fr: "requin",      pt: "tubarao",      de: "hai"        } },
  { emoji: "🐋", q: { es: "ballena",      en: "whale",         fr: "baleine",     pt: "baleia",       de: "wal"        } },
  { emoji: "🐕", q: { es: "perro",        en: "dog",           fr: "chien",       pt: "cao",          de: "hund"       } },
  { emoji: "🐈", q: { es: "gato",         en: "cat",           fr: "chat",        pt: "gato",         de: "katze"      } },
  { emoji: "🦁", q: { es: "felinos",      en: "felines",       fr: "felins",      pt: "felinos",      de: "felinen"    } },
  { emoji: "🐘", q: { es: "elefante",     en: "elephant",      fr: "elephant",    pt: "elefante",     de: "elefant"    } },
  { emoji: "🦀", q: { es: "invertebrados",en: "invertebrates", fr: "invertebres", pt: "invertebrados",de: "wirbellosen"} },
  { emoji: "🐒", q: { es: "primates",     en: "primates",      fr: "primates",    pt: "primatas",     de: "primaten"   } },
  { emoji: "🐊", q: { es: "cocodrilo",    en: "crocodile",     fr: "crocodile",   pt: "crocodilo",    de: "krokodil"   } },
  { emoji: "🦅", q: { es: "aguila",       en: "eagle",         fr: "aigle",       pt: "aguia",        de: "adler"      } },
];
// Hero animales flotantes
const HERO_EMOJIS = ["🦁", "🐘", "🦈", "🦅", "🐬", "🐍", "🦋"];
document.addEventListener("DOMContentLoaded", () => {
  const hero = document.getElementById("heroAnimals");
  if (hero) {
    hero.innerHTML = HERO_EMOJIS.map(e =>
      `<span class="hero-animal">${e}</span>`
    ).join("");
  }
});
const appEl   = document.getElementById("app");
const form    = document.getElementById("searchForm");
const input   = document.getElementById("query");
const langSel = document.getElementById("langSelect");
const output  = document.getElementById("output");

function actualizarChips() {
  const sugs = SUGERENCIAS[uiLang] || SUGERENCIAS.es;
  document.getElementById("chips").innerHTML = sugs.map(s =>
    `<button class="chip" type="button" data-q="${s}">${s}</button>`
  ).join("");
}

function actualizarDominios() {
  const cats = t("categorias").split(",");
  document.getElementById("domains").innerHTML = DOMINIOS.map((d, i) =>
    `<button class="domain-btn" type="button" data-q="${d.q[uiLang] || d.q.es}"
      style="--btn-c:${DOMAIN_COLORS[i] || '#58a6ff'}">${d.emoji} ${cats[i] || ""}</button>`
  ).join("");
}

actualizarChips();
actualizarDominios();

// Sincronizar el selector de idioma con los botones de UI
langSel.addEventListener("change", (e) => {
  cambiarIdiomaUI(e.target.value);
});

document.addEventListener("click", e => {
  const btn = e.target.closest("[data-q]");
  if (!btn) return;
  input.value = btn.dataset.q;
  buscar(btn.dataset.q);
});

form.addEventListener("submit", e => {
  e.preventDefault();
  const q = input.value.trim();
  if (q) buscar(q);
});

async function buscar(q) {
  appEl.classList.remove("home");
  output.innerHTML = `<div class="loader-wrap"><div class="loader"></div></div>`;
  try {
    const lang = langSel.value;
    const res  = await fetch(`${API}/api/search/?q=${encodeURIComponent(q)}&lang=${lang}&online=${modoOnline}&per_page=100`);
    const data = await res.json();
    renderResultados(data, q);
  } catch (err) {
    output.innerHTML = `
      <div class="empty">
        <h3>${t("errorConexion")}</h3>
        <p>${t("errorMsg")}</p>
      </div>`;
  }
}

function renderResultados(data, q) {
  const total      = data.total || 0;
  const resultados = data.results || [];
  const sugerencia = data.sugerencia;

  let html = `
    <div class="results-header">
      <div class="results-title">${t("resultados")} "${esc(q)}"</div>
      <div class="results-count">${total} ${total !== 1 ? t("encontrados") : t("encontrado")}</div>
    </div>`;

  if (sugerencia) {
    const palabra = sugerencia.match(/:\s*(.+)\?/)?.[1] || "";
    html += `<div class="sugerencia">${t("quisiste")} <span onclick="corregir('${esc(palabra)}')">${esc(palabra)}</span>?</div>`;
  }

  if (resultados.length === 0) {
    html += `
      <div class="empty">
        <h3>${t("sinResultados")}</h3>
        <p>${t("sinResultadosMsg")} "${esc(q)}". ${t("intentar")}</p>
      </div>`;
  } else {
    html += `<div class="cards">`;
    resultados.forEach(r => { html += renderCard(r); });
    html += `</div>`;
  }

  output.innerHTML = html;
}

function getAnimalEmoji(nombre, labelEn) {
  const n = (nombre + " " + (labelEn || "")).toLowerCase();
  if (n.includes("shepherd") || n.includes("retriever") || n.includes("bulldog") ||
      n.includes("beagle") || n.includes("husky") || n.includes("dachshund") ||
      n.includes("rottweiler") || n.includes("chihuahua") || n.includes("collie") ||
      n.includes("dalmatian") || n.includes("dobermann") || n.includes("poodle") ||
      n.includes("terrier") || n.includes("shih tzu") || n.includes("yorkshire") ||
      (n.includes("dog") && !n.includes("hotdog"))) return "🐕";
  if (n.includes("siamese") || n.includes("persian") || n.includes("maine coon") ||
      n.includes("bengal cat") || n.includes("sphynx") || n.includes("british short") ||
      n.includes("scottish fold") || n.includes("gato")) return "🐈";
  if (n.includes("lion") && !n.includes("sea lion") && !n.includes("dandelion")) return "🦁";
  if (n.includes("tiger") || n.includes("tigre")) return "🐯";
  if (n.includes("panda") || n.includes("ailuropoda")) return "🐼";
  if (n.includes("polar bear") || n.includes("oso polar")) return "🐻‍❄️";
  if (n.includes("bear") || n.includes("oso")) return "🐻";
  if (n.includes("shark") || n.includes("tiburón") || n.includes("tiburon")) return "🦈";
  if (n.includes("whale") || n.includes("ballena")) return "🐋";
  if (n.includes("dolphin") || n.includes("delfín") || n.includes("tursiops")) return "🐬";
  if (n.includes("orca") || n.includes("orcinus")) return "🐳";
  if (n.includes("golden eagle") || n.includes("bald eagle") || n.includes("harpy eagle") ||
      n.includes("aquila") || n.includes("águila") || n.includes("aguila") ||
      n.includes("haliaeetus") || n.includes("harpia")) return "🦅";
  if (n.includes("owl") || n.includes("búho") || n.includes("buho") ||
      n.includes("bubo") || n.includes("tyto")) return "🦉";
  if (n.includes("penguin") || n.includes("pingüino") || n.includes("aptenodytes") ||
      n.includes("spheniscus")) return "🐧";
  if (n.includes("flamingo") || n.includes("flamenco") || n.includes("phoenicopterus")) return "🦩";
  if (n.includes("toucan") || n.includes("tucán") || n.includes("ramphastidae")) return "🦜";
  if (n.includes("parrot") || n.includes("loro") || n.includes("macaw") ||
      n.includes("cockatoo") || n.includes("psittac") || n.includes("cacatua")) return "🦜";
  if (n.includes("ostrich") || n.includes("avestruz") || n.includes("struthio")) return "🦚";
  if (n.includes("falcon") || n.includes("halcón") || n.includes("falco")) return "🦅";
  if (n.includes("hummingbird") || n.includes("colibrí") || n.includes("trochilidae")) return "🐦";
  if (n.includes("crocodile") || n.includes("cocodrilo") || n.includes("crocodylus")) return "🐊";
  if (n.includes("iguana") || n.includes("gecko") || n.includes("gekkota") ||
      n.includes("chameleon") || n.includes("camaleón") || n.includes("chamaeleonidae") ||
      n.includes("lizard") || n.includes("monitor") || n.includes("varanus")) return "🦎";
  if (n.includes("komodo")) return "🦎";
  if (n.includes("snake") || n.includes("serpiente") || n.includes("viper") ||
      n.includes("víbora") || n.includes("cobra") || n.includes("anaconda") ||
      n.includes("python") || n.includes("boa") || n.includes("mamba")) return "🐍";
  if (n.includes("turtle") || n.includes("tortuga") || n.includes("chelonia") ||
      n.includes("dermochelys")) return "🐢";
  if (n.includes("frog") || n.includes("rana") || n.includes("toad") ||
      n.includes("dendrobatidae") || n.includes("bullfrog")) return "🐸";
  if (n.includes("axolotl") || n.includes("ajolote") || n.includes("salamander") ||
      n.includes("ambystoma") || n.includes("caudata")) return "🦎";
  if (n.includes("elephant") || n.includes("elefante") || n.includes("loxodonta") ||
      n.includes("elephas")) return "🐘";
  if (n.includes("giraffe") || n.includes("jirafa") || n.includes("giraffa")) return "🦒";
  if (n.includes("zebra") || n.includes("cebra")) return "🦓";
  if (n.includes("hippo") || n.includes("hipopótamo") || n.includes("hippopotamus")) return "🦛";
  if (n.includes("rhino") || n.includes("rinoceronte") || n.includes("ceratotherium") ||
      n.includes("diceros")) return "🦏";
  if (n.includes("gorilla") || n.includes("gorila")) return "🦍";
  if (n.includes("chimpanzee") || n.includes("chimpancé") || n.includes("pan troglodytes")) return "🐒";
  if (n.includes("orangutan") || n.includes("orangután")) return "🦧";
  if (n.includes("gibbon") || n.includes("bonobo") || n.includes("mandrill") ||
      n.includes("baboon") || n.includes("primate")) return "🐒";
  if (n.includes("kangaroo") || n.includes("canguro")) return "🦘";
  if (n.includes("koala")) return "🐨";
  if (n.includes("platypus") || n.includes("ornitorrinco") || n.includes("ornithorhynchus")) return "🦆";
  if (n.includes("wombat") || n.includes("tasmanian")) return "🐾";
  if (n.includes("horse") || n.includes("caballo") || n.includes("equus")) return "🐴";
  if (n.includes("donkey") || n.includes("burro") || n.includes("mule") || n.includes("mula")) return "🫏";
  if (n.includes("camel") || n.includes("camello") || n.includes("dromedary") ||
      n.includes("dromedario") || n.includes("llama") || n.includes("alpaca")) return "🐪";
  if (n.includes("bison") || n.includes("bisonte") || n.includes("buffalo") ||
      n.includes("búfalo")) return "🦬";
  if (n.includes("moose") || n.includes("alce") || n.includes("reindeer") ||
      n.includes("reno") || n.includes("deer")) return "🦌";
  if (n.includes("wolf") || n.includes("lobo") || n.includes("canis lupus")) return "🐺";
  if (n.includes("fox") || n.includes("zorro") || n.includes("vulpes")) return "🦊";
  if (n.includes("coyote") || n.includes("dingo")) return "🐺";
  if (n.includes("hyena") || n.includes("hiena") || n.includes("crocuta")) return "🐾";
  if (n.includes("meerkat") || n.includes("suricata")) return "🐾";
  if (n.includes("rabbit") || n.includes("conejo") || n.includes("hare") ||
      n.includes("liebre")) return "🐰";
  if (n.includes("beaver") || n.includes("castor")) return "🦫";
  if (n.includes("otter") || n.includes("nutria") || n.includes("enhydra") ||
      n.includes("pteronura")) return "🦦";
  if (n.includes("sea lion") || n.includes("león marino") || n.includes("otariinae") ||
      n.includes("seal") || n.includes("foca") || n.includes("walrus") ||
      n.includes("morsa") || n.includes("mirounga")) return "🦭";
  if (n.includes("capybara") || n.includes("capibara") || n.includes("hydrochoerus")) return "🐾";
  if (n.includes("octopus") || n.includes("pulpo") || n.includes("octopoda")) return "🐙";
  if (n.includes("squid") || n.includes("calamar") || n.includes("architeuthis")) return "🦑";
  if (n.includes("nautilus")) return "🐚";
  if (n.includes("clam") || n.includes("tridacna")) return "🐚";
  if (n.includes("crab") || n.includes("cangrejo") || n.includes("macrocheira") ||
      n.includes("limulidae") || n.includes("horseshoe")) return "🦀";
  if (n.includes("lobster") || n.includes("langosta") || n.includes("nephropidae")) return "🦞";
  if (n.includes("shrimp") || n.includes("gamba") || n.includes("stomatopoda")) return "🦐";
  if (n.includes("crayfish") || n.includes("astacus")) return "🦞";
  if (n.includes("jellyfish") || n.includes("medusa") || n.includes("cubozoa")) return "🪼";
  if (n.includes("starfish") || n.includes("estrella") || n.includes("asteroidea")) return "⭐";
  if (n.includes("sea urchin") || n.includes("erizo") || n.includes("echinoidea")) return "🦔";
  if (n.includes("butterfly") || n.includes("mariposa") || n.includes("danaus")) return "🦋";
  if (n.includes("bee") || n.includes("abeja") || n.includes("bombus") ||
      n.includes("xylocopa")) return "🐝";
  if (n.includes("dragonfly") || n.includes("libélula") || n.includes("anisoptera")) return "🪲";
  if (n.includes("ant") || n.includes("hormiga") || n.includes("formicidae")) return "🐜";
  if (n.includes("termite") || n.includes("termita") || n.includes("isoptera")) return "🐜";
  if (n.includes("firefly") || n.includes("luciérnaga") || n.includes("lampyridae")) return "✨";
  if (n.includes("spider") || n.includes("araña") || n.includes("theraphosidae") ||
      n.includes("lycosidae") || n.includes("black widow")) return "🕷️";
  if (n.includes("scorpion") || n.includes("escorpión") || n.includes("scorpiones")) return "🦂";
  if (n.includes("salmon") || n.includes("salmón") || n.includes("salmo")) return "🐟";
  if (n.includes("tuna") || n.includes("atún") || n.includes("thunini")) return "🐟";
  if (n.includes("clownfish") || n.includes("pez payaso") || n.includes("amphiprioninae")) return "🐠";
  if (n.includes("piranha") || n.includes("piraña")) return "🐟";
  if (n.includes("swordfish") || n.includes("pez espada") || n.includes("xiphias")) return "🐟";
  if (n.includes("seahorse") || n.includes("caballito de mar") || n.includes("hippocampus")) return "🐠";
  if (n.includes("manta") || n.includes("stingray") || n.includes("raya") ||
      n.includes("myliobatoidei")) return "🐡";
  if (n.includes("electric eel") || n.includes("anguila") || n.includes("electrophorus")) return "⚡";
  return "🐾";
}

function renderCard(r) {
  const nombre    = r.nombre || r.id || "Animal";
  const fuente    = r.fuente || "dbpedia";
  const sci       = r.nombre_cientifico || "";
  const abstract  = r.abstract || "";
  const labels    = r.labels || {};
  const uri       = r.uri || "";
  const thumbnail = r.thumbnail || "";
  const labelEn   = labels["en"] || "";

  const sourceClass = fuente === "local" ? "source-local"
    : fuente === "wikidata" ? "source-wikidata"
    : fuente === "dbpedia_owl" ? "source-dbpedia"
    : "source-dbpedia";
  const sourceLabel = fuente === "local" ? "Local OWL"
    : fuente === "wikidata" ? "Wikidata"
    : fuente === "dbpedia_owl" ? "DBpedia OWL"
    : "DBpedia";
  const labelsHtml = Object.entries(labels)
    .filter(([, v]) => v)
    .map(([k, v]) => `<span class="label-tag">${k}: ${esc(v)}</span>`)
    .join("");

  const uriCorta = uri.replace("http://dbpedia.org/resource/", "dbr:")
                      .replace("http://www.semanticweb.org/grupo10/animales#", "animal:");

  const emoji = getAnimalEmoji(nombre, labelEn);

  const imgHtml = thumbnail
    ? `<div class="card-img-wrap"><img class="card-img" src="${thumbnail}" alt="${esc(nombre)}" loading="lazy" onerror="this.parentElement.innerHTML='<div class=\\'card-img-placeholder\\'>${emoji}</div>'"></div>`
    : `<div class="card-img-placeholder">${emoji}</div>`;

  return `
    <div class="card" onclick='abrirModal(${JSON.stringify(r).replace(/'/g, "&#39;")})'>
      ${imgHtml}
      <div class="card-body">
        <div class="card-header">
          <div class="card-name">${esc(nombre)}</div>
          <span class="card-source ${sourceClass}">${sourceLabel}</span>
        </div>
        ${sci ? `<div class="card-sci">🔬 ${esc(sci)}</div>` : ""}
        ${abstract ? `<div class="card-abstract">${esc(abstract)}</div>` : ""}
        ${labelsHtml ? `<div class="card-labels">${labelsHtml}</div>` : ""}
        <div class="card-uri">${esc(uriCorta)}</div>
      </div>
    </div>`;
}

function corregir(palabra) {
  input.value = palabra;
  buscar(palabra);
}

function esc(str) {
  return String(str ?? "")
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

// =====================
// MODAL FICHA DETALLADA
// =====================

async function abrirModal(r) {
  document.getElementById("modal-overlay").style.display = "flex";
  document.body.style.overflow = "hidden";

  // Mostrar datos básicos inmediatamente (del dump, funciona offline)
  renderModal(r, langSel.value);

  // Intentar enriquecer con Wikipedia (solo si hay internet)
  try {
    const lang = langSel.value;
    const res = await fetch(
      `${API}/api/animals/details?uri=${encodeURIComponent(r.uri)}&lang=${lang}`,
      { signal: AbortSignal.timeout(8000) }
    );
    if (res.ok) {
      const detalle = await res.json();
      const datos = {
        ...r,
        abstract:          detalle.abstract          || r.abstract || "",
        thumbnail:         detalle.thumbnail         || r.thumbnail || "",
        nombre_cientifico: detalle.nombre_cientifico || r.nombre_cientifico || "",
        labels:            Object.keys(detalle.labels || {}).length > 0 ? detalle.labels : r.labels,
        clasificacion:     detalle.clasificacion     || {},
      };
      renderModal(datos, lang);
    }
  } catch(e) {
    // Sin internet — ya se mostraron los datos del dump
    console.log("Sin internet, usando datos locales del dump");
  }
}

function renderModal(r, lang_actual = "es") {
  const nombre    = r.nombre || r.id || "Animal";
  const fuente    = r.fuente || "dbpedia";
  const sci       = r.nombre_cientifico || "";
  const abstract  = r.abstract || "";
  const labels    = r.labels || {};
  const uri       = r.uri || "";
  const thumbnail = r.thumbnail || "";
  const clasif    = r.clasificacion || {};
  const labelEn   = labels["en"] || "";

  const sourceClass = fuente === "local" ? "source-local" : "source-dbpedia";
  const sourceLabel = fuente === "local" ? "Local OWL" : "DBpedia";

  const labelsHtml = Object.entries(labels)
    .filter(([, v]) => v)
    .map(([k, v]) => `
      <div class="modal-label-item">
        <span class="modal-lang">${k.toUpperCase()}</span>
        <span class="modal-label-val">${esc(v)}</span>
      </div>`).join("");

  const clasifHtml = Object.entries(clasif)
    .filter(([, v]) => v)
    .map(([k, v]) => `
      <div class="modal-label-item">
        <span class="modal-lang">${esc(k)}</span>
        <span class="modal-label-val">${esc(v)}</span>
      </div>`).join("");

  const uriCorta = uri.replace("http://dbpedia.org/resource/", "dbr:")
                      .replace("http://www.semanticweb.org/grupo10/animales#", "animal:");

  const dbpediaLink = uri.includes("dbpedia.org")
    ? `<a class="modal-link" href="${uri}" target="_blank" rel="noreferrer">Ver en DBpedia →</a>` : "";

  const emoji = getAnimalEmoji(nombre, labelEn);

  const imgHtml = thumbnail
    ? `<img class="modal-img" src="${thumbnail}" alt="${esc(nombre)}" onerror="this.style.display='none'">`
    : `<div class="modal-img-placeholder">${emoji}</div>`;

  const IDIOMAS = [
    { code: "es", flag: `<img src="https://flagcdn.com/w20/es.png" alt="ES">`, label: "Español" },
    { code: "en", flag: `<img src="https://flagcdn.com/w20/gb.png" alt="EN">`, label: "English" },
    { code: "fr", flag: `<img src="https://flagcdn.com/w20/fr.png" alt="FR">`, label: "Français" },
    { code: "pt", flag: `<img src="https://flagcdn.com/w20/pt.png" alt="PT">`, label: "Português" },
    { code: "de", flag: `<img src="https://flagcdn.com/w20/de.png" alt="DE">`, label: "Deutsch" },
  ];

  const langBtns = IDIOMAS.map(l => `
    <button class="modal-lang-btn ${lang_actual === l.code ? "active" : ""}"
      onclick="recargarModal('${uri}', '${l.code}')"
      title="${l.label}">
      ${l.flag}
    </button>`).join("");

  window._modalAnimal = r;

  document.getElementById("modal-overlay").innerHTML = `
    <div class="modal" id="modal-box">
      <button class="modal-close" onclick="cerrarModal()">✕</button>
      ${imgHtml}
      <div class="modal-content">
        <div class="modal-header">
          <h2 class="modal-nombre">${esc(nombre)}</h2>
          <span class="card-source ${sourceClass}">${sourceLabel}</span>
        </div>
        ${sci ? `<div class="modal-section">
          <span class="modal-section-title">${t("nombreCientifico")}</span>
          <p class="modal-sci">${esc(sci)}</p>
        </div>` : ""}
        <div class="modal-section">
          <span class="modal-section-title">${t("descripcion")}</span>
          <div class="modal-lang-btns">${langBtns}</div>
          ${abstract
            ? `<p class="modal-abstract" id="modal-abstract-text">${esc(abstract)}</p>`
            : `<p class="modal-abstract" id="modal-abstract-text" style="color:var(--muted);font-style:italic;">${t("sinDescripcion")}</p>`
          }
        </div>
        ${clasifHtml ? `<div class="modal-section">
          <span class="modal-section-title">${t("clasificacion")}</span>
          <div class="modal-labels">${clasifHtml}</div>
        </div>` : ""}
        <div class="modal-section">
          <span class="modal-section-title">${t("nombresIdiomas")}</span>
          <div class="modal-labels">${labelsHtml}</div>
        </div>
        <div class="modal-section">
          <span class="modal-section-title">${t("uriSemantica")}</span>
          <code class="modal-uri">${esc(uriCorta)}</code>
        </div>
        <div class="modal-section">
          <span class="modal-section-title">${t("fuente")}</span>
          <p>${fuente === "local" ? t("fuenteLocal") : t("fuenteDBpedia")}</p>
        </div>
        ${dbpediaLink ? `<a class="modal-link" href="${uri}" target="_blank" rel="noreferrer">${t("verDBpedia")}</a>` : ""}
      </div>
    </div>`;
}

async function recargarModal(uri, lang) {
  document.querySelectorAll(".modal-lang-btn").forEach(btn => btn.classList.remove("active"));
  event.target.classList.add("active");

  const abstractEl = document.getElementById("modal-abstract-text");
  if (abstractEl) abstractEl.innerHTML = `<em style='color:var(--muted)'>${t("cargando")}</em>`;

  try {
    const res = await fetch(`${API}/api/animals/details?uri=${encodeURIComponent(uri)}&lang=${lang}`);
    if (res.ok) {
      const detalle = await res.json();
      const abstract = detalle.abstract || "";
      if (abstractEl) {
        abstractEl.innerHTML = abstract
          ? esc(abstract)
          : "<em style='color:var(--muted)'>Sin descripción disponible en este idioma.</em>";
      }
    }
  } catch(e) {
    if (abstractEl) abstractEl.innerHTML = "<em style='color:var(--muted)'>Error al cargar descripción.</em>";
  }
}
function cerrarModal() {
  document.getElementById("modal-overlay").style.display = "none";
  document.body.style.overflow = "";
}
function cambiarIdiomaUI(lang) {
  uiLang = lang;

  // Sincronizar el selector de búsqueda con el idioma de UI
  langSel.value = lang;

  // Actualizar botones activos (matchea por el onclick attr)
  document.querySelectorAll(".ui-lang-btn").forEach(btn => {
    const m = (btn.getAttribute("onclick") || "").match(/cambiarIdiomaUI\('(\w+)'\)/);
    btn.classList.toggle("active", m && m[1] === lang);
  });

  // Actualizar textos de interfaz
  document.getElementById("query").placeholder = t("placeholder");
  const brandSub = document.getElementById("brandSub");
  if (brandSub) brandSub.textContent = t("brandSub");
  const sectionLabel = document.querySelector(".section-label");
  if (sectionLabel) sectionLabel.textContent = t("explorar");

  // Actualizar chips y dominios con términos del idioma seleccionado
  actualizarChips();
  actualizarDominios();

  // Si hay resultados visibles, re-buscar en el nuevo idioma
  const resultsTitle = document.querySelector(".results-title");
  if (resultsTitle) {
    const q = document.getElementById("query").value;
    if (q) buscar(q);
  }
}
let modoOnline = true;

function volverInicio() {
  appEl.classList.add("home");
  output.innerHTML = "";
  input.value = "";
}

function toggleConexion() {
  modoOnline = document.getElementById("onlineToggle").checked;
  const label = document.getElementById("connLabel");
  if (modoOnline) {
    label.textContent = "🌐 Online";
    label.classList.remove("offline");
  } else {
    label.textContent = "📡 Offline";
    label.classList.add("offline");
  }
}