/* popup.js */

const statusDiv = document.getElementById("connectionStatus");
const urlInput = document.getElementById("backendUrl");
const userInput = document.getElementById("username");
const passInput = document.getElementById("password");

// 1. Load Saved Credentials
browser.storage.local.get(["backendUrl", "auth_user", "auth_pass", "fontEnabled"]).then((res) => {
  if (res.backendUrl) urlInput.value = res.backendUrl;
  if (res.auth_user) userInput.value = res.auth_user;
  if (res.auth_pass) passInput.value = res.auth_pass;
  document.getElementById("fontToggle").checked = res.fontEnabled || false;
});

// 2. Save & Test Connection
document.getElementById("saveBtn").addEventListener("click", () => {
  const url = urlInput.value.trim().replace(/\/$/, "");
  const user = userInput.value.trim();
  const pass = passInput.value.trim();

  browser.storage.local.set({
    backendUrl: url,
    auth_user: user,
    auth_pass: pass
  });

  checkConnection(url, user, pass);
});

// 3. Test Connection
function checkConnection(url, user, pass) {
  statusDiv.textContent = "Connecting...";
  statusDiv.style.color = "#666";

  const headers = { "Content-Type": "application/json" };
  if (user) {
    headers["Authorization"] = "Basic " + btoa(user + ":" + pass);
  }

  fetch(`${url}/status`)
    .then((res) => res.json())
    .then((data) => {
      statusDiv.textContent = "✅ Connected: " + (data.mode || "OK");
      statusDiv.style.color = "green";
    })
    .catch(() => {
      statusDiv.textContent = "❌ Connection Failed. Check URL.";
      statusDiv.style.color = "red";
    });
}

// 4. Trigger Reader Mode
document.getElementById("readerModeBtn").addEventListener("click", () => {
  browser.storage.local.get(["backendUrl", "auth_user", "auth_pass"]).then((res) => {
    if (!res.backendUrl) return alert("Please connect backend first.");

    const headers = { "Content-Type": "application/json" };
    if (res.auth_user) {
      headers["Authorization"] = "Basic " + btoa(res.auth_user + ":" + res.auth_pass);
    }

    browser.tabs.query({ active: true, currentWindow: true }).then((tabs) => {
      fetch(`${res.backendUrl}/view/reader-mode`, {
        method: "POST",
        headers: headers,
        body: JSON.stringify({ url: tabs[0].url })
      })
        .then((r) => r.json())
        .then((data) => {
          const blob = new Blob([data.html], { type: "text/html" });
          const url = URL.createObjectURL(blob);
          browser.tabs.create({ url: url });
        });
    });
  });
});

// 5. Toggle Font (Immediate)
document.getElementById("fontToggle").addEventListener("change", (e) => {
  const isChecked = e.target.checked;
  browser.storage.local.set({ fontEnabled: isChecked });

  browser.tabs.query({ active: true, currentWindow: true }).then((tabs) => {
    browser.tabs.sendMessage(tabs[0].id, {
      command: "toggleFont",
      enable: isChecked
    });
  });
});
