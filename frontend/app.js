const API = "http://127.0.0.1:5000";

const SUGERENCIAS = [
  "perro", "tiburón", "león", "serpiente", "águila",
  "delfín", "oso polar", "mariposa monarca", "cocodrilo", "pingüino"
];

const DOMINIOS = [
  { emoji: "🐾", label: "Mamíferos",     q: "mamiferos" },
  { emoji: "🐦", label: "Aves",          q: "aves" },
  { emoji: "🐍", label: "Reptiles",      q: "reptiles" },
  { emoji: "🐸", label: "Anfibios",      q: "anfibios" },
  { emoji: "🐟", label: "Peces",         q: "peces" },
  { emoji: "🦋", label: "Insectos",      q: "insectos" },
  { emoji: "🦈", label: "Tiburones",     q: "tiburon" },
  { emoji: "🐋", label: "Ballenas",      q: "ballena" },
  { emoji: "🐕", label: "Perros",        q: "perro" },
  { emoji: "🐈", label: "Gatos",         q: "gato" },
  { emoji: "🦁", label: "Felinos",       q: "felinos" },
  { emoji: "🐘", label: "Elefantes",     q: "elefante" },
  { emoji: "🦀", label: "Invertebrados", q: "invertebrados" },
  { emoji: "🐒", label: "Primates",      q: "primates" },
  { emoji: "🐊", label: "Cocodrilos",    q: "cocodrilo" },
  { emoji: "🦅", label: "Águilas",       q: "aguila" },
];

const appEl   = document.getElementById("app");
const form    = document.getElementById("searchForm");
const input   = document.getElementById("query");
const langSel = document.getElementById("langSelect");
const output  = document.getElementById("output");

document.getElementById("chips").innerHTML = SUGERENCIAS.map(s =>
  `<button class="chip" type="button" data-q="${s}">${s}</button>`
).join("");

document.getElementById("domains").innerHTML = DOMINIOS.map(d =>
  `<button class="domain-btn" type="button" data-q="${d.q}">${d.emoji} ${d.label}</button>`
).join("");

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
  const lang = langSel.value;
  appEl.classList.remove("home");
  output.innerHTML = `<div class="loader-wrap"><div class="loader"></div></div>`;
  try {
    const res  = await fetch(`${API}/api/search/?q=${encodeURIComponent(q)}&lang=${lang}`);
    const data = await res.json();
    renderResultados(data, q);
  } catch (err) {
    output.innerHTML = `
      <div class="empty">
        <h3>Error de conexión</h3>
        <p>No se pudo conectar con el servidor. ¿Está corriendo Flask?</p>
      </div>`;
  }
}

function renderResultados(data, q) {
  const total      = data.total || 0;
  const resultados = data.results || [];
  const sugerencia = data.sugerencia;

  let html = `
    <div class="results-header">
      <div class="results-title">Resultados para "${q}"</div>
      <div class="results-count">${total} animal${total !== 1 ? "es" : ""} encontrado${total !== 1 ? "s" : ""}</div>
    </div>`;

  if (sugerencia) {
    const palabra = sugerencia.match(/:\s*(.+)\?/)?.[1] || "";
    html += `<div class="sugerencia">¿Quisiste decir: <span onclick="corregir('${palabra}')">${palabra}</span>?</div>`;
  }

  if (resultados.length === 0) {
    html += `
      <div class="empty">
        <h3>Sin resultados</h3>
        <p>No encontramos animales para "${q}". Intenta con otra palabra.</p>
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

  const sourceClass = fuente === "local" ? "source-local" : "source-dbpedia";
  const sourceLabel = fuente === "local" ? "Local OWL" : "DBpedia";

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

  document.getElementById("modal-overlay").innerHTML = `
    <div class="modal" id="modal-box">
      <button class="modal-close" onclick="cerrarModal()">✕</button>
      <div class="modal-img-placeholder">⏳</div>
      <div class="modal-content">
        <h2 class="modal-nombre">${esc(r.nombre || r.id)}</h2>
        <p style="color:var(--muted); font-size:14px;">Cargando detalles...</p>
      </div>
    </div>`;

  let datos = r;
  try {
    const res = await fetch(`${API}/api/animals/details?uri=${encodeURIComponent(r.uri)}`);
    if (res.ok) {
      const detalle = await res.json();
      datos = {
        ...r,
        abstract:          detalle.abstract          || r.abstract          || "",
        thumbnail:         detalle.thumbnail         || r.thumbnail         || "",
        nombre_cientifico: detalle.nombre_cientifico || r.nombre_cientifico || "",
        labels:            Object.keys(detalle.labels || {}).length > 0 ? detalle.labels : r.labels,
        clasificacion:     detalle.clasificacion     || {},
      };
    }
  } catch(e) {
    console.log("Sin detalles en vivo, usando datos del dump");
  }

  renderModal(datos);
}

function renderModal(r) {
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
          <span class="modal-section-title">🔬 Nombre científico</span>
          <p class="modal-sci">${esc(sci)}</p>
        </div>` : ""}
        ${abstract ? `<div class="modal-section">
          <span class="modal-section-title">📖 Descripción</span>
          <p class="modal-abstract">${esc(abstract)}</p>
        </div>` : ""}
        ${clasifHtml ? `<div class="modal-section">
          <span class="modal-section-title">🧬 Clasificación taxonómica</span>
          <div class="modal-labels">${clasifHtml}</div>
        </div>` : ""}
        <div class="modal-section">
          <span class="modal-section-title">🌍 Nombres en otros idiomas</span>
          <div class="modal-labels">${labelsHtml}</div>
        </div>
        <div class="modal-section">
          <span class="modal-section-title">🔗 URI semántica</span>
          <code class="modal-uri">${esc(uriCorta)}</code>
        </div>
        <div class="modal-section">
          <span class="modal-section-title">📦 Fuente</span>
          <p>${fuente === "local" ? "Ontología OWL local (Grupo 10 UMSS)" : "DBpedia — Linked Open Data"}</p>
        </div>
        ${dbpediaLink}
      </div>
    </div>`;
}

function cerrarModal() {
  document.getElementById("modal-overlay").style.display = "none";
  document.body.style.overflow = "";
}