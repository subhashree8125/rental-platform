document.addEventListener("DOMContentLoaded", async () => {
    let user = {}; // Will store fetched user info

    const profileName = document.getElementById("profileName");
    const profileEmail = document.getElementById("profileEmail");
    const profilePhone = document.getElementById("profilePhone");

    // Fetch user info from backend
    async function fetchUserProfile() {
        try {
            const res = await fetch("/api/profile");
            if (!res.ok) throw new Error("Failed to fetch profile");
            user = await res.json();

            profileName.innerText = user.full_name || "N/A";
            profileEmail.innerText = user.email || "N/A";
            profilePhone.innerText = user.mobile_number || "Not Provided";
        } catch (err) {
            console.error(err);
            profileName.innerText = "N/A";
            profileEmail.innerText = "N/A";
            profilePhone.innerText = "Not Provided";
        }
    }

    await fetchUserProfile();

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
            const res = await fetch("/api/profile", {
                method: "PUT",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ full_name: updatedName, mobile_number: updatedPhone })
            });
            const data = await res.json();
            if (data.success) {
                alert("Profile updated successfully!");
                await fetchUserProfile(); // Refresh user info
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
    window.fetchUserProperties = async function() {
        const propertiesContainer = document.getElementById("userProperties");
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
                    <p>Status: <span id="status-${p.property_id}">${p.status}</span></p>
                    <button onclick="toggleStatus(${p.property_id})">Toggle Status</button>
                `;
                propertiesContainer.appendChild(card);
            });
        } catch (err) {
            console.error(err);
            propertiesContainer.innerHTML = "<p>Error loading properties.</p>";
        }
    };

    await fetchUserProperties();
});

// Make toggleStatus globally accessible
async function toggleStatus(id) {
    const currentStatus = document.getElementById(`status-${id}`).innerText;
    const newStatus = currentStatus === "Available" ? "Unavailable" : "Available";

    try {
        const res = await fetch(`/api/properties/${id}/status`, {
            method: "PATCH",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ status: newStatus })
        });
        const data = await res.json();
        if (data.success) {
            alert(`Property marked as ${newStatus}`);
            window.fetchUserProperties(); // refresh profile property list
            if (typeof fetchProperties === "function") fetchProperties(); // refresh explore page if exists
        } else {
            alert("Failed to update status");
        }
    } catch (err) {
        console.error(err);
        alert("Something went wrong!");
    }
}
