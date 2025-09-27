document.addEventListener("DOMContentLoaded", () => {
    // Load user from localStorage
    let user = JSON.parse(localStorage.getItem("user")) || {};

    const profileName = document.getElementById("profileName");
    const profileEmail = document.getElementById("profileEmail");
    const profilePhone = document.getElementById("profilePhone");

    profileName.innerText = user.full_name || "N/A";
    profileEmail.innerText = user.email || "N/A";
    profilePhone.innerText = user.mobile_number || "N/A";

    // Edit profile modal
    const editBtn = document.getElementById("editProfileBtn");
    const editModal = document.getElementById("editProfileModal");
    const closeModal = document.getElementById("closeModal");
    const editForm = document.getElementById("editProfileForm");
    const editName = document.getElementById("editName");
    const editPhone = document.getElementById("editPhone");

    editBtn.addEventListener("click", () => {
        editName.value = user.full_name || "";
        editPhone.value = user.mobile_number || "";
        editModal.style.display = "flex";
    });

    closeModal.addEventListener("click", () => editModal.style.display = "none");
    window.addEventListener("click", e => { if(e.target === editModal) editModal.style.display="none"; });

    // Update profile submit
    editForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        const updatedName = editName.value.trim();
        const updatedPhone = editPhone.value.trim();

        try {
            const res = await fetch("/api/user/update", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ full_name: updatedName, mobile_number: updatedPhone })
            });
            const data = await res.json();
            if (data.success) {
                alert("Profile updated successfully!");
                user.full_name = updatedName;
                user.mobile_number = updatedPhone;
                localStorage.setItem("user", JSON.stringify(user));

                profileName.innerText = user.full_name || "N/A";
                profilePhone.innerText = user.mobile_number || "N/A";
                editModal.style.display = "none";
            } else {
                alert("Error: " + data.message);
            }
        } catch (err) {
            console.error(err);
            alert("Something went wrong!");
        }
    });

    // Load user's properties
    const propertiesContainer = document.getElementById("userProperties");
    async function fetchUserProperties() {
        try {
            const res = await fetch("/api/user/properties");
            const data = await res.json();
            propertiesContainer.innerHTML = "";
            if (data.length === 0) {
                propertiesContainer.innerHTML = "<p>No properties posted yet.</p>";
                return;
            }
            data.forEach(p => {
                const card = document.createElement("div");
                card.className = "property-card";
                card.innerHTML = `
                    <h4>${p.property_type} - ${p.house_type}</h4>
                    <p>₹${parseInt(p.rent_price).toLocaleString()}</p>
                    <p>${p.address}, ${p.district}</p>
                `;
                propertiesContainer.appendChild(card);
            });
        } catch (err) {
            console.error(err);
            propertiesContainer.innerHTML = "<p>Error loading properties.</p>";
        }
    }

    fetchUserProperties();
});
function toggleStatus(id) {
  const currentStatus = document.getElementById(`status-${id}`).innerText;
  const newStatus = currentStatus === "Available" ? "Unavailable" : "Available";

  fetch(`/api/properties/${id}/status`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ status: newStatus })
  })
  .then(res => res.json())
  .then(data => {
    if (data.success) {
      document.getElementById(`status-${id}`).innerText = newStatus;
      alert(`Property marked as ${newStatus}`);
      fetchUserProperties(); // refresh profile property list
      fetchProperties();     // refresh explore page
    }
  });
}

