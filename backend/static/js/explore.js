let properties = [];
let images = [];
let currentImageIndex = 0;
let selectedProperty = null;

// ---------------------
// Fetch properties
// ---------------------
async function fetchProperties() {
  try {
    const res = await fetch("/api/properties");
    const data = await res.json();
    properties = Array.isArray(data) ? data : [];
    renderProperties(properties);
    fillDistricts(properties);
    fillBHK(properties);
    initAreasPanel(); // show "Select a district first"
  } catch (err) {
    console.error("Failed to load properties:", err);
  }
}

// ---------------------
// Render cards
// ---------------------
function renderProperties(list) {
  const gallery = document.getElementById("propertyGallery");
  gallery.innerHTML = "";
  if (list.length === 0) {
    gallery.innerHTML =
      "<p style='grid-column:1/-1;text-align:center;font-size:18px;color:#555;'>No properties found.</p>";
    return;
  }
  list.forEach((p) => {
    const card = document.createElement("div");
    card.className = "property-card";
    const imageUrl =
      p.images && p.images.length > 0
        ? `/static/uploads/${p.images[0]}`
        : "https://via.placeholder.com/400x250?text=No+Image";
    card.innerHTML = `
      <img src="${imageUrl}" alt="">
      <div class="property-info">
        <h4>${p.property_type} - ${p.house_type}</h4>
        <p><strong>₹${p.rent_price}</strong>/month</p>
        <p>${p.address}, ${p.district}</p>
        <p>${p.description || ""}</p>
      </div>`;
    card.onclick = () => openModal(p);
    gallery.appendChild(card);
  });
}

// ---------------------
// Modal & Carousel
// ---------------------
function openModal(p) {
  selectedProperty = p;
  images = p.images || [];
  currentImageIndex = 0;
  updateCarousel();

  document.getElementById("modalTitle").innerText = `${p.property_type} - ${p.house_type}`;
  document.getElementById("modalType").innerText = p.property_type;
  document.getElementById("modalBHK").innerText = p.house_type;
  document.getElementById("modalPrice").innerText = parseFloat(p.rent_price).toLocaleString();
  document.getElementById("modalDistrict").innerText = p.district;
  document.getElementById("modalAddress").innerText = p.address;
  document.getElementById("modalDesc").innerText = p.description || "No description available.";
  document.getElementById("propertyModal").style.display = "flex";
}

document.getElementById("contactBtn").addEventListener("click", () => {
  if (selectedProperty && selectedProperty.mobile_number) {
    alert("📞 Owner Contact: " + selectedProperty.mobile_number);
  } else {
    alert("Owner contact is only available after login.");
  }
});

function updateCarousel() {
  const carouselImg = document.getElementById("carouselImage");
  if (images.length > 0) {
    carouselImg.src = `/static/uploads/${images[currentImageIndex]}`;
  } else {
    carouselImg.src = "https://via.placeholder.com/400x250?text=No+Image";
  }
}

document.querySelector(".prev-btn").addEventListener("click", () => {
  if (images.length > 0) {
    currentImageIndex = (currentImageIndex - 1 + images.length) % images.length;
    updateCarousel();
  }
});
document.querySelector(".next-btn").addEventListener("click", () => {
  if (images.length > 0) {
    currentImageIndex = (currentImageIndex + 1) % images.length;
    updateCarousel();
  }
});
function closeModal() {
  document.getElementById("propertyModal").style.display = "none";
}
function toggleAccordion(btn) {
  btn.classList.toggle("active");
  const panel = btn.nextElementSibling;
  panel.style.display = panel.style.display === "block" ? "none" : "block";
}

// ---------------------
// Filters
// ---------------------
function fillDistricts(list) {
  const panel = document.getElementById("districtPanel");
  panel.innerHTML = "";
  const districts = [...new Set(list.map((p) => p.district))].sort();
  districts.forEach((d) => {
    const label = document.createElement("label");
    label.innerHTML = `<input type="radio" name="district" value="${d}"> ${d}`;
    panel.appendChild(label);
  });

  // Event: when selecting a district → update areas
  panel.querySelectorAll("input[name='district']").forEach((input) => {
    input.addEventListener("change", (e) => {
      updateAreas(e.target.value);
    });
  });
}

function initAreasPanel() {
  document.getElementById("areasPanel").innerHTML = "<p>Select a district first</p>";
}

function updateAreas(selectedDistrict) {
  const panel = document.getElementById("areasPanel");
  panel.innerHTML = "";

  const areas = properties
    .filter((p) => p.district === selectedDistrict)
    .map((p) => p.address);
  const uniqueAreas = [...new Set(areas)].sort();

  if (uniqueAreas.length === 0) {
    panel.innerHTML = "<p>No areas available for this district</p>";
    return;
  }

  uniqueAreas.forEach((a) => {
    const label = document.createElement("label");
    label.innerHTML = `<input type="checkbox" value="${a}"> ${a}`;
    panel.appendChild(label);
  });
}

function fillBHK(list) {
  const panel = document.getElementById("bhkPanel");
  panel.innerHTML = "";
  const bhkOrder = ["1HK", "1BHK", "2BHK", "3BHK", "4+ BHK"];
  const bhks = [...new Set(list.map((p) => p.house_type))].filter(Boolean);

  bhkOrder.forEach((b) => {
    if (bhks.includes(b)) {
      const label = document.createElement("label");
      label.innerHTML = `<input type="checkbox" value="${b}"> ${b}`;
      panel.appendChild(label);
    }
  });
}

// Apply filters
document.getElementById("applyFilterBtn").addEventListener("click", () => {
  const selectedDistrict = document.querySelector("#districtPanel input[name='district']:checked")?.value || null;
  const selectedAreas = [...document.querySelectorAll("#areasPanel input:checked")].map((i) => i.value);
  const selectedTypes = [...document.querySelectorAll("div.panel input[type='checkbox']:checked")]
    .map((i) => i.value)
    .filter((v) => !selectedAreas.includes(v) && !["1HK", "1BHK", "2BHK", "3BHK", "4+ BHK"].includes(v)); // exclude BHK/areas
  const selectedBHK = [...document.querySelectorAll("#bhkPanel input:checked")].map((i) => i.value);
  const min = parseInt(document.getElementById("minBudget").value);
  const max = parseInt(document.getElementById("maxBudget").value);

  let filtered = properties.filter((p) => {
    return (!selectedDistrict || p.district === selectedDistrict) &&
      (!selectedAreas.length || selectedAreas.includes(p.address)) &&
      (!selectedTypes.length || selectedTypes.includes(p.property_type)) &&
      (!selectedBHK.length || selectedBHK.includes(p.house_type)) &&
      (parseInt(p.rent_price) >= min && parseInt(p.rent_price) <= max);
  });
  renderProperties(filtered);
});

// Clear filters
document.getElementById("clearFilterBtn").addEventListener("click", () => {
  renderProperties(properties);
  document.querySelectorAll("aside input[type='checkbox'], aside input[type='radio']").forEach((cb) => (cb.checked = false));
  initAreasPanel();
});

// ---------------------
// Budget live label
// ---------------------
const minBudget = document.getElementById("minBudget");
const maxBudget = document.getElementById("maxBudget");
const budgetRange = document.getElementById("budgetRange");
function updateBudgetLabel() {
  budgetRange.innerText = `₹${parseInt(minBudget.value).toLocaleString()} - ₹${parseInt(maxBudget.value).toLocaleString()}`;
}
minBudget.addEventListener("input", updateBudgetLabel);
maxBudget.addEventListener("input", updateBudgetLabel);
updateBudgetLabel();

// ---------------------
// Profile button
// ---------------------
const user = localStorage.getItem("user");
if (user) {
  document.getElementById("loginBtn").style.display = "none";
  document.getElementById("profileBtn").style.display = "inline-block";
}

// Init
fetchProperties();
