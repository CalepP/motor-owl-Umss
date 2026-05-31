const API = "http://127.0.0.1:5000";

const SUGERENCIAS = [
  "perro", "tiburón", "león", "serpiente", "águila",
  "delfín", "oso polar", "mariposa monarca", "cocodrilo", "pingüino"
];

const DOMINIOS = [
  { emoji: "🐾", label: "Mamíferos",   q: "mamifero" },
  { emoji: "🐦", label: "Aves",        q: "aguila" },
  { emoji: "🐍", label: "Reptiles",    q: "serpiente" },
  { emoji: "🐸", label: "Anfibios",    q: "rana" },
  { emoji: "🐟", label: "Peces",       q: "salmon" },
  { emoji: "🦋", label: "Insectos",    q: "mariposa" },
  { emoji: "🦈", label: "Tiburones",   q: "tiburon" },
  { emoji: "🐋", label: "Ballenas",    q: "ballena" },
  { emoji: "🐕", label: "Perros",      q: "perro" },
  { emoji: "🐈", label: "Gatos",       q: "gato" },
  { emoji: "🦁", label: "Felinos",     q: "tigre" },
  { emoji: "🐘", label: "Elefantes",   q: "elefante" },
];

const appEl   = document.getElementById("app");
const form    = document.getElementById("searchForm");
const input   = document.getElementById("query");
const langSel = document.getElementById("langSelect");
const output  = document.getElementById("output");

// Chips de sugerencias
document.getElementById("chips").innerHTML = SUGERENCIAS.map(s =>
  `<button class="chip" type="button" data-q="${s}">${s}</button>`
).join("");

// Botones de dominio
document.getElementById("domains").innerHTML = DOMINIOS.map(d =>
  `<button class="domain-btn" type="button" data-q="${d.q}">${d.emoji} ${d.label}</button>`
).join("");

// Eventos clicks en chips y dominios
document.addEventListener("click", e => {
  const btn = e.target.closest("[data-q]");
  if (!btn) return;
  input.value = btn.dataset.q;
  buscar(btn.dataset.q);
});

// Submit del form
form.addEventListener("submit", e => {
  e.preventDefault();
  const q = input.value.trim();
  if (q) buscar(q);
});

async function buscar(q) {
  const lang = langSel.value;

  // Cambiar a modo resultados
  appEl.classList.remove("home");

  // Mostrar loader
  output.innerHTML = `
    <div class="loader-wrap">
      <div class="loader"></div>
    </div>`;

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
    html += `
      <div class="sugerencia">
        ¿Quisiste decir: <span onclick="corregir('${palabra}')">${palabra}</span>?
      </div>`;
  }

  if (resultados.length === 0) {
    html += `
      <div class="empty">
        <h3>Sin resultados</h3>
        <p>No encontramos animales para "${q}". Intenta con otra palabra.</p>
      </div>`;
  } else {
    html += `<div class="cards">`;
    resultados.forEach(r => {
      html += renderCard(r);
    });
    html += `</div>`;
  }

  output.innerHTML = html;
}
function renderCard(r) {
  const nombre    = r.nombre || r.id || "Animal";
  const fuente    = r.fuente || "dbpedia";
  const sci       = r.nombre_cientifico || "";
  const abstract  = r.abstract || "";
  const labels    = r.labels || {};
  const uri       = r.uri || "";
  const thumbnail = r.thumbnail || "";

  const sourceClass = fuente === "local" ? "source-local" : "source-dbpedia";
  const sourceLabel = fuente === "local" ? "Local OWL" : "DBpedia";

  const labelsHtml = Object.entries(labels)
    .filter(([, v]) => v)
    .map(([k, v]) => `<span class="label-tag">${k}: ${esc(v)}</span>`)
    .join("");

  const uriCorta = uri.replace("http://dbpedia.org/resource/", "dbr:")
                      .replace("http://www.semanticweb.org/grupo10/animales#", "animal:");

  const imgHtml = thumbnail
    ? `<img class="card-img" src="${thumbnail}" alt="${esc(nombre)}" loading="lazy" onerror="this.style.display='none'">`
    : `<div class="card-img-placeholder">🐾</div>`;

  return `
    <div class="card">
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