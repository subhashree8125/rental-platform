// --- Fetch User Properties ---
async function loadProperties() {
  try {
    const res = await fetch('/api/myproperties');
    if (!res.ok) throw new Error("Failed to fetch properties");
    const data = await res.json();
    const list = document.getElementById('propertiesList');
    list.innerHTML = '';

    window._propsCache = [];
    const properties = data.properties || [];
    
    // Show empty state message if no properties
    if (properties.length === 0) {
      list.innerHTML = `
        <div class="empty-state">
          <p>Your property list is empty — add one to get started!</p>
          <a href="/postproperty" class="post-property-btn">Post Property</a>
        </div>
      `;
      return;
    }
    
    properties.forEach(p => {
      window._propsCache.push(p);
      const card = document.createElement('div');
      card.className = 'property-card';
      card.innerHTML = `
        <h4>${p.address}, ${p.area}, ${p.city}, ${p.district}</h4>
        <p>Type: ${p.property_type} | ${p.house_type}</p>
        <p>Rent: ₹${p.rent_price}</p>
        <p>Parking: ${p.car_parking} | Pets: ${p.pets}</p>
        <p>Furnishing: ${p.furnishing} | Facing: ${p.facing}</p>
        <p>Status: <strong>${p.status}</strong></p>
        <div class="property-actions">
          <div class="status-toggle">
            <label class="switch">
              <input type="checkbox" ${p.status === 'Available' ? 'checked' : ''} onchange="toggleStatus(${p.property_id}, this.checked)">
              <span class="slider"></span>
            </label>
            <span class="status-text">${p.status}</span>
          </div>
          <button class="edit-btn" onclick='openEditModal(${p.property_id})'>Edit</button>
          <button class="delete-btn" onclick="deleteProperty(${p.property_id})">Delete</button>
        </div>
      `;
      list.appendChild(card);
    });
  } catch (err) {
    console.error("Failed to load properties:", err);
  }
}

// --- Edit Property Modal ---
function openEditModal(id) {
  const prop = (window._propsCache || []).find(x => x.property_id === id);
  if (!prop) return;
  
  // Populate form with current values
  document.getElementById('editPropertyId').value = prop.property_id;
  document.getElementById('editFullName').value = prop.full_name;
  document.getElementById('editMobile').value = prop.mobile_number;
  document.getElementById('editAddress').value = prop.address;
  document.getElementById('editCity').value = prop.city;
  document.getElementById('editArea').value = prop.area;
  document.getElementById('editDistrict').value = prop.district;
  document.getElementById('editPropertyType').value = prop.property_type;
  document.getElementById('editHouseType').value = prop.house_type;
  document.getElementById('editRentPrice').value = prop.rent_price;
  document.getElementById('editCarParking').value = prop.car_parking;
  document.getElementById('editPets').value = prop.pets;
  document.getElementById('editFacing').value = prop.facing;
  document.getElementById('editFurnishing').value = prop.furnishing;
  document.getElementById('editDescription').value = prop.description || '';
  
  document.getElementById('editPropertyModal').style.display = 'flex';
}

function closeEditModal() {
  document.getElementById('editPropertyModal').style.display = 'none';
}

async function updateProperty(id, payload) {
  try {
    const res = await fetch(`/api/property/${id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    const data = await res.json();
    if (data.success) {
      loadProperties();
      closeEditModal();
      showNotification('Property updated successfully', 'success');
    } else {
      alert(data.error || 'Failed to update property');
    }
  } catch (e) {
    console.error(e);
    alert('Error updating property');
  }
}

// --- Delete Profile ---
async function deleteProfile() {
  if (!confirm("Are you sure you want to delete your account? This action cannot be undone.")) return;
  
  try {
    const res = await fetch('/api/profile', { method: 'DELETE' });
    const data = await res.json();
    if (data.success) {
      alert('Account deleted successfully');
      window.location.href = '/';
    } else {
      alert(data.error || 'Failed to delete account');
    }
  } catch (e) {
    console.error(e);
    alert('Error deleting account');
  }
}

// --- Notification System ---
function showNotification(message, type = 'info') {
  const notification = document.createElement('div');
  notification.className = `notification ${type}`;
  notification.textContent = message;
  notification.style.cssText = `
    position: fixed; top: 20px; right: 20px; z-index: 10000;
    padding: 15px 20px; border-radius: 5px; color: white;
    background: ${type === 'success' ? '#4CAF50' : type === 'error' ? '#f44336' : '#2196F3'};
    box-shadow: 0 2px 10px rgba(0,0,0,0.2);
  `;
  document.body.appendChild(notification);
  setTimeout(() => notification.remove(), 3000);
}

// --- Toggle Property Status ---
async function toggleStatus(id, isAvailable) {
  const status = isAvailable ? 'Available' : 'Unavailable';
  try {
    const res = await fetch(`/api/property/${id}/status`, {
      method: 'PUT',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({status})
    });
    const data = await res.json();
    if(data.success) {
      loadProperties();
      showNotification(`Property status updated to ${status}`, 'success');
    } else {
      alert(data.error || "Failed to update status");
    }
  } catch (err) { 
    console.error(err); 
    alert("Error updating status"); 
  }
}

// --- Delete Property ---
async function deleteProperty(id) {
  if(!confirm("Delete this property?")) return;
  try {
    const res = await fetch(`/api/property/${id}`, { method: 'DELETE' });
    const data = await res.json();
    if(data.success) loadProperties();
    else alert(data.error || "Failed to delete property");
  } catch(err) { console.error(err); alert("Error deleting property"); }
}

// --- Profile Modal ---
function openModal() {
  const modal = document.getElementById('editProfileModal');
  modal.style.display = 'flex';
  document.getElementById('editName').value = document.getElementById('profileName').textContent;
  document.getElementById('editEmail').value = document.getElementById('profileEmail').textContent;
  document.getElementById('editMobile').value = document.getElementById('profileMobile').textContent;
}

function closeModal() { 
  document.getElementById('editProfileModal').style.display = 'none'; 
}
window.onclick = e => { if(e.target == document.getElementById('editProfileModal')) closeModal(); }

// --- Update Profile ---
document.getElementById('editProfileForm').addEventListener('submit', async e => {
  e.preventDefault();
  const data = {
    full_name: document.getElementById('editName').value,
    email: document.getElementById('editEmail').value,
    mobile_number: document.getElementById('editMobile').value,
    password: document.getElementById('editPassword').value
  };
  try {
    const res = await fetch('/api/profile', {
      method: 'PUT',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify(data)
    });
    const result = await res.json();
    if(result.success) {
      document.getElementById('profileName').textContent = data.full_name;
      document.getElementById('profileEmail').textContent = data.email;
      document.getElementById('profileMobile').textContent = data.mobile_number;
      closeModal();
      alert(result.message);
    } else alert(result.error || "Failed to update profile");
  } catch(err) { console.error(err); alert("Error updating profile"); }
});

// --- Logout ---
async function logout() {
  await fetch('/logout');
  window.location.href = '/';
}

// --- Edit Property Form Handler ---
document.getElementById('editPropertyForm').addEventListener('submit', async e => {
  e.preventDefault();
  const id = document.getElementById('editPropertyId').value;
  const data = {
    full_name: document.getElementById('editFullName').value,
    mobile_number: document.getElementById('editMobile').value,
    address: document.getElementById('editAddress').value,
    city: document.getElementById('editCity').value,
    area: document.getElementById('editArea').value,
    district: document.getElementById('editDistrict').value,
    property_type: document.getElementById('editPropertyType').value,
    house_type: document.getElementById('editHouseType').value,
    rent_price: document.getElementById('editRentPrice').value,
    car_parking: document.getElementById('editCarParking').value,
    pets: document.getElementById('editPets').value,
    facing: document.getElementById('editFacing').value,
    furnishing: document.getElementById('editFurnishing').value,
    description: document.getElementById('editDescription').value
  };
  await updateProperty(id, data);
});

// --- Initial Load ---
loadProperties();
