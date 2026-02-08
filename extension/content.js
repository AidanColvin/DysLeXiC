/* content.js */

let CONFIG = {
  url: "",
  user: "",
  pass: ""
};

// 1. Initialize & Listen for Changes
function loadConfig() {
  browser.storage.local.get(["backendUrl", "auth_user", "auth_pass", "fontEnabled"]).then((res) => {
    CONFIG.url = res.backendUrl || "";
    CONFIG.user = res.auth_user || "";
    CONFIG.pass = res.auth_pass || "";

    if (res.fontEnabled) applyDyslexiaFont();
  });
}
loadConfig();

// Listen for updates from popup
browser.storage.onChanged.addListener(loadConfig);

// 2. Listen for Messages (From Popup or Background)
browser.runtime.onMessage.addListener((msg) => {
  if (msg.command === "toggleFont") {
    if (msg.enable) applyDyslexiaFont();
    else removeDyslexiaFont();
  } else if (msg.command === "analyzeSelection") {
    showCondensePanel(msg.text);
  }
});

// --- FEATURES ---

function applyDyslexiaFont() {
  document.body.style.fontFamily = "Arial, sans-serif";
  document.body.style.lineHeight = "1.6";
  document.body.style.letterSpacing = "0.05em";
  document.body.style.backgroundColor = "#FDFBF7";
  document.body.style.color = "#333";
}

function removeDyslexiaFont() {
  document.body.style = "";
}

// 3. Helper to make Authenticated Requests
async function secureFetch(endpoint, body) {
  if (!CONFIG.url) return null;

  const headers = { "Content-Type": "application/json" };

  if (CONFIG.user) {
    headers["Authorization"] = "Basic " + btoa(CONFIG.user + ":" + CONFIG.pass);
  }

  try {
    const response = await fetch(`${CONFIG.url}${endpoint}`, {
      method: "POST",
      headers: headers,
      body: JSON.stringify(body)
    });

    if (response.status === 401) {
      console.error("Dyslexic: Authentication Failed. Check Extension Settings.");
      return null;
    }
    return response.json();
  } catch (e) {
    console.error("Dyslexic: Backend Error", e);
    return null;
  }
}

// 4. Double-Click Handler
document.addEventListener("dblclick", async () => {
  const selection = window.getSelection().toString().trim();
  if (selection.length < 2) return;

  const context = window.getSelection().anchorNode.parentElement.innerText.substring(0, 500);

  const data = await secureFetch("/dyslexia/v2/suggest", {
    sentence: context,
    misspelled_word: selection
  });

  if (data && data.suggestions && data.suggestions.length > 0) {
    showSuggestionBox(data, selection);
  }
});

function showSuggestionBox(data, original) {
  const existing = document.getElementById("dyslexic-tooltip");
  if (existing) existing.remove();

  const box = document.createElement("div");
  box.id = "dyslexic-tooltip";
  box.style.cssText = "position:fixed;top:20px;right:20px;background:#fff;border:2px solid #005a9c;" +
    "border-radius:8px;padding:12px;z-index:99999;font-family:Arial,sans-serif;box-shadow:0 4px 12px rgba(0,0,0,0.15);max-width:280px;";

  const title = document.createElement("strong");
  title.textContent = "Suggestions for \"" + original + "\":";
  box.appendChild(title);
  box.appendChild(document.createElement("br"));

  data.suggestions.forEach((s) => {
    const row = document.createElement("div");
    row.style.cssText = "margin:4px 0;cursor:pointer;padding:4px 8px;border-radius:4px;background:#f0f4ff;";
    row.className = "dyslexic-suggestion";
    row.dataset.word = s.word;
    row.textContent = s.word + " ";
    const conf = document.createElement("span");
    conf.style.cssText = "color:#888;font-size:11px;";
    conf.textContent = "(" + s.confidence + ")";
    row.appendChild(conf);
    row.addEventListener("click", () => {
      secureFetch("/dyslexia/feedback", {
        misspelling: original,
        chosen: s.word,
        action: "accepted"
      });
      box.remove();
    });
    box.appendChild(row);
  });

  const footer = document.createElement("div");
  footer.style.cssText = "margin-top:8px;text-align:right;";
  const closeBtn = document.createElement("button");
  closeBtn.textContent = "Close";
  closeBtn.style.cssText = "border:none;background:#ccc;padding:4px 10px;border-radius:4px;cursor:pointer;";
  closeBtn.addEventListener("click", () => box.remove());
  footer.appendChild(closeBtn);
  box.appendChild(footer);

  document.body.appendChild(box);
}

// 5. Condense / Analyze Selection
function showCondensePanel(text) {
  if (!CONFIG.url) return;

  secureFetch("/view/condense", { text: text }).then((data) => {
    if (data && data.summary_bullets) {
      alert("Key Points:\n" + data.summary_bullets.join("\n"));
    }
  });
}
