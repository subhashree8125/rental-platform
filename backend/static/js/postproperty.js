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
    window.location.href = "/login";
  }
});

// --- File input label update ---
document.getElementById("upload")?.addEventListener("change", function () {
  const fileLabel = document.getElementById("file-name");
  if (fileLabel) {
    const files = Array.from(this.files).map(f => f.name).join(", ");
    fileLabel.textContent = files || "Browse Images";
  }

  // Image preview
  const previewContainer = document.getElementById("preview-container");
  if (previewContainer) {
    previewContainer.innerHTML = "";
    Array.from(this.files).forEach(file => {
      const reader = new FileReader();
      reader.onload = (e) => {
        const img = document.createElement("img");
        img.src = e.target.result;
        img.style.width = "100px";
        img.style.height = "100px";
        img.style.objectFit = "cover";
        img.style.borderRadius = "6px";
        img.style.boxShadow = "0 2px 6px rgba(0,0,0,0.3)";
        previewContainer.appendChild(img);
      };
      reader.readAsDataURL(file);
    });
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
      <p>${p.address}</p>
      <p>${p.city}, ${p.district}</p>
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
    window.location.href = "/login";
    return;
  }

  const form = document.getElementById("postPropertyForm");
  const formData = new FormData(form);

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
      // Show success popup with BROKLINK theme
      showSuccessPopup();
      
      form.reset();
      const fileLabel = document.getElementById("file-name");
      if (fileLabel) fileLabel.textContent = "Browse Images";

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

// --- Success Popup Function ---
function showSuccessPopup() {
  const popup = document.createElement('div');
  popup.style.cssText = `
    position: fixed; top: 0; left: 0; width: 100%; height: 100%;
    background: rgba(0,0,0,0.8); z-index: 10000; display: flex;
    align-items: center; justify-content: center; font-family: 'Poppins', sans-serif;
  `;
  
  popup.innerHTML = `
    <div style="
      background: linear-gradient(135deg, #FFD700, #FFA500);
      padding: 40px; border-radius: 15px; text-align: center;
      box-shadow: 0 10px 30px rgba(0,0,0,0.3);
      max-width: 400px; width: 90%;
    ">
      <div style="font-size: 48px; margin-bottom: 20px;">🎉</div>
      <h2 style="color: #000; margin: 0 0 15px 0; font-size: 24px;">Posted Your Property Successfully!</h2>
      <p style="color: #333; margin: 0 0 20px 0;">Redirecting to explore page...</p>
      <div style="
        width: 40px; height: 40px; border: 4px solid #000;
        border-top: 4px solid transparent; border-radius: 50%;
        animation: spin 1s linear infinite; margin: 0 auto;
      "></div>
    </div>
    <style>
      @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
    </style>
  `;
  
  document.body.appendChild(popup);
  
  setTimeout(() => {
    document.body.removeChild(popup);
    window.location.href = '/explore';
  }, 3000);
}

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
});
