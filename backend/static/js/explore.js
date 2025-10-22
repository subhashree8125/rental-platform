let properties = [];
let images = [];
let currentImageIndex = 0;
let selectedProperty = null;

// ---------------------
// Fetch properties (with optional filters)
// ---------------------
async function fetchProperties(filters = {}) {
  try {
    const query = Object.keys(filters).length
      ? `?filters=${encodeURIComponent(JSON.stringify(filters))}`
      : "";

    const res = await fetch(`/api/properties${query}`);
    const data = await res.json();
    properties = Array.isArray(data) ? data : [];
    renderProperties(properties);

    // Only refill filter panels when no filters are applied (initial load)
    if (Object.keys(filters).length === 0) {
      fillDistricts(properties);
      fillBHK(properties);
      initCitiesPanel();
      initAreasPanel();
      fillCarParking();
      fillPets();
      fillFacing();
      fillFurnishing();
    }
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
  console.log(list);
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
        <h4>${p.full_name} - ${p.property_type} - ${p.house_type}</h4>
        <p><strong>₹${p.rent_price}</strong>/month</p>
        <p>${p.address}</p>
        <p>${p.area}, ${p.city}, ${p.district}</p>
        <p class="desc" style="display:none;">${p.description || ""}</p>
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

  document.getElementById("modalTitle").innerText = `${p.full_name} - ${p.property_type} - ${p.house_type}`;
  document.getElementById("modalType").innerText = p.property_type;
  document.getElementById("modalBHK").innerText = p.house_type;
  document.getElementById("modalPrice").innerText = parseFloat(p.rent_price).toLocaleString();

  document.getElementById("modalCity").innerText = p.city;
  document.getElementById("modalArea").innerText = p.area;
  document.getElementById("modalDistrict").innerText = p.district;
  document.getElementById("modalAddress").innerText = p.address;
  document.getElementById("modalDesc").innerText = p.description || "No description available.";
  document.getElementById("propertyModal").style.display = "flex";
}

document.getElementById("contactBtn").addEventListener("click", async () => {
  if (!selectedProperty) return;
  try {
    const res = await fetch(`/api/property/${selectedProperty.property_id}/contact`);
    const data = await res.json();
    if (res.ok && data.success) {
      // Open phone dialer
      window.location.href = `tel:${data.mobile_number}`;
    } else if (res.status === 401) {
      alert("Please login to contact the owner.");
      window.location.href = "/login";
    } else {
      alert(data.error || "Failed to fetch contact");
    }
  } catch (e) {
    console.error(e);
    alert("Failed to fetch contact");
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

  // Event: when selecting a district → update cities and areas
  panel.querySelectorAll("input[name='district']").forEach((input) => {
    input.addEventListener("change", (e) => {
      updateCities(e.target.value);
      updateAreas(e.target.value);
    });
  });
}

function initCitiesPanel() {
  document.getElementById("cityPanel").innerHTML = "<p>Select a district first</p>";
}

function updateCities(selectedDistrict) {
  const panel = document.getElementById("cityPanel");
  const citiesInDistrict = [...new Set(
    properties
    .filter((p) => p.district === selectedDistrict)
    .map((p) => p.city)
  )].sort();

  if (citiesInDistrict.length === 0) {
    panel.innerHTML = "<p>No cities available for this district</p>";
    return;
  }

  panel.innerHTML = "";
  citiesInDistrict.forEach((city) => {
    const label = document.createElement("label");
    label.innerHTML = `<input type="checkbox" value="${city}"> ${city}`;
    panel.appendChild(label);
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
    .map((p) => p.area);
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

// ---------------------
// New Filter Panels
// ---------------------
function fillCarParking() {
  const panel = document.getElementById("carParkingPanel");
  panel.innerHTML = `
    <label><input type="radio" name="car_parking" value=""> Any</label>
    <label><input type="radio" name="car_parking" value="Available"> Available</label>
    <label><input type="radio" name="car_parking" value="NotAvailable"> Not Available</label>
  `;
}

function fillPets() {
  const panel = document.getElementById("petsPanel");
  panel.innerHTML = `
    <label><input type="radio" name="pets" value=""> Any</label>
    <label><input type="radio" name="pets" value="Allowed"> Allowed</label>
    <label><input type="radio" name="pets" value="Strictly Not Allowed"> Strictly Not Allowed</label>
  `;
}

function fillFacing() {
  const panel = document.getElementById("facingPanel");
  const options = ["East", "West", "North", "South", "Southeast", "Northeast", "Southwest", "Northwest"];
  panel.innerHTML = options.map((o) => `<label><input type="checkbox" value="${o}"> ${o}</label>`).join("");
}

function fillFurnishing() {
  const panel = document.getElementById("furnishingPanel");
  const options = ["Furnished", "Semi-furnished", "Unfurnished"];
  panel.innerHTML = options.map((o) => `<label><input type="checkbox" value="${o}"> ${o}</label>`).join("");
}

// ---------------------
// Apply filter button
// ---------------------
document.getElementById("applyFilterBtn").addEventListener("click", () => {
  const selectedCities = Array.from(document.querySelectorAll("#cityPanel input:checked")).map(el => el.value);
  const selectedDistricts = Array.from(document.querySelectorAll("#districtPanel input:checked")).map(el => el.value);
  const selectedAreas = Array.from(document.querySelectorAll("#areasPanel input:checked")).map(el => el.value);
  const selectedPropertyTypes = Array.from(document.querySelectorAll("input[value=House]:checked, input[value=Flat]:checked, input[value=PG]:checked, input[value=Hostel]:checked")).map(el => el.value);
  const selectedBHK = Array.from(document.querySelectorAll("#bhkPanel input:checked")).map(el => el.value);

  const minBudget = document.getElementById("minBudget").value;
  const maxBudget = document.getElementById("maxBudget").value;

  // New filters
  const carParking = document.querySelector("input[name='car_parking']:checked")?.value || "";
  const pets = document.querySelector("input[name='pets']:checked")?.value || "";
  const facing = Array.from(document.querySelectorAll("#facingPanel input:checked")).map(el => el.value);
  const furnishing = Array.from(document.querySelectorAll("#furnishingPanel input:checked")).map(el => el.value);

  const filters = {
    cities: selectedCities,
    districts: selectedDistricts,
    areas: selectedAreas,
    propertyTypes: selectedPropertyTypes,
    bhk: selectedBHK,
    minBudget,
    maxBudget,
    carParking,
    pets,
    facing,
    furnishing
  };

  fetchProperties(filters);
});

// ---------------------
// Clear filters
// ---------------------
document.getElementById("clearFilterBtn").addEventListener("click", () => {
  // Reset all checkboxes and radio buttons
  document.querySelectorAll("aside input[type='checkbox'], aside input[type='radio']").forEach(cb => cb.checked = false);
  
  // Reset budget sliders
  const minBudget = document.getElementById("minBudget");
  const maxBudget = document.getElementById("maxBudget");
  minBudget.value = minBudget.min;
  maxBudget.value = maxBudget.max;
  updateBudgetLabel(); // update the display

  // Reset select/radio panels for Car Parking / Pets / Facing / Furnishing
  document.querySelectorAll("#carParkingPanel input, #petsPanel input").forEach(cb => cb.checked = false);
  document.querySelectorAll("#facingPanel input, #furnishingPanel input").forEach(cb => cb.checked = false);

  // Reset Cities and Areas panels
  initCitiesPanel();
  initAreasPanel();

  // Render all properties
  renderProperties(properties);
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
