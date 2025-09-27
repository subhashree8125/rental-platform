// --- 🔑 Check session ---
async function checkSession() {
  try {
    const res = await fetch("/api/session");
    if (res.ok) {
      const data = await res.json();
      return data.loggedIn ? data.user : null;
    }
  } catch (err) {
    console.error("Session check failed:", err);
  }
  return null;
}

// --- Redirect if not logged in ---
window.addEventListener("DOMContentLoaded", async () => {
  const user = await checkSession();
  if (!user) {
    alert("Please login first to post a property.");
    window.location.href = "login";
  }
});

// --- File input label update ---
document.getElementById("upload")?.addEventListener("change", function () {
  const fileLabel = document.getElementById("file-name");
  if (fileLabel) {
    const files = Array.from(this.files).map(f => f.name).join(", ");
    fileLabel.textContent = files || "Upload Images";
  }
});

// --- Render Explore Properties dynamically ---
function renderExploreProperties(properties) {
  const container = document.getElementById("explore-container");
  if (!container) return;

  container.innerHTML = ""; // clear previous
  properties.forEach((p) => {
    const card = document.createElement("div");
    card.classList.add("property-card");
    card.innerHTML = `
      <h3>${p.full_name}</h3>
      <p>${p.address}, ${p.district}</p>
      <p>Type: ${p.property_type} | ${p.house_type}</p>
      <p>Rent: ₹${p.rent_price}</p>
      <p>Parking: ${p.car_parking} | Pets: ${p.pets}</p>
      <p>Furnishing: ${p.furnishing} | Facing: ${p.facing}</p>
      <p>${p.description || ""}</p>
      <div class="images">
        ${p.images.map(img => `<img src="/static/uploads/${img}" width="100">`).join("")}
      </div>
    `;
    container.appendChild(card);
  });
}

// --- Form submission ---
async function postProperty(event) {
  event.preventDefault();

  const user = await checkSession();
  if (!user) {
    alert("Please login before posting a property.");
    window.location.href = "login";
    return;
  }

  const form = document.getElementById("postPropertyForm");
  const formData = new FormData(form);

  // Message box
  let msgBox = document.getElementById("property-message");
  if (!msgBox) {
    msgBox = document.createElement("div");
    msgBox.id = "property-message";
    msgBox.style.marginTop = "15px";
    msgBox.style.padding = "12px";
    msgBox.style.borderRadius = "6px";
    msgBox.style.fontSize = "14px";
    msgBox.style.fontWeight = "600";
    msgBox.style.textAlign = "center";
    form.appendChild(msgBox);
  }

  try {
    const response = await fetch("/api/properties", { method: "POST", body: formData });
    
    let data;
    const contentType = response.headers.get("content-type");
    if (contentType && contentType.includes("application/json")) {
      data = await response.json();
    } else {
      const text = await response.text();
      throw new Error("Non-JSON response: " + text.slice(0, 200));
    }

    if (response.ok) {
      msgBox.textContent = "✅ Property posted successfully!";
      msgBox.style.background = "#d4edda";
      msgBox.style.color = "#155724";
      msgBox.style.border = "1px solid #c3e6cb";

      form.reset();
      document.getElementById("file-name").textContent = "Upload Images";

      if (data.properties) renderExploreProperties(data.properties);
    } else {
      msgBox.textContent = `❌ ${data.error || data.message || "Failed to post property"}`;
      msgBox.style.background = "#f8d7da";
      msgBox.style.color = "#721c24";
      msgBox.style.border = "1px solid #f5c6cb";
    }

  } catch (error) {
    console.error("Post Property error:", error);
    msgBox.textContent = "⚠️ " + error.message;
    msgBox.style.background = "#fff3cd";
    msgBox.style.color = "#856404";
    msgBox.style.border = "1px solid #ffeeba";
  }
}

// --- Attach form submit event ---
document.getElementById("postPropertyForm").addEventListener("submit", postProperty);
// --- Initial load of properties ---
window.addEventListener("DOMContentLoaded", async () => {
  try {
    const res = await fetch("/api/properties");
    if (res.ok) {
      const data = await res.json();
      if (data.properties) renderExploreProperties(data.properties);
    }
  } catch (err) {
    console.error("Failed to load properties:", err);
  }
}       );

// --- END ---