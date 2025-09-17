// signup.js

// Function to handle signup
async function signup(event) {
    // Prevent default if triggered by form submission in future
    if (event) event.preventDefault();

    // Grab input values from your UI
    const full_name = document.getElementById("fullname").value.trim();
    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value;
    const mobile_number = document.getElementById("mobile").value.trim();

    // Simple frontend validation
    if (!full_name || !email || !password || !mobile_number) {
        document.getElementById("errorMsg").innerText = "All fields are required";
        return;
    }

    try {
        // Make POST request to your backend signup route
        const res = await fetch("/auth/signup", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ full_name, email, password, mobile_number })
        });

        const data = await res.json();

        if (!res.ok) {
            // Display backend error message
            throw new Error(data.error || "Signup failed");
        }

        // Signup successful
        alert(data.message || "Signup successful!");
        window.location.href = "/login"; // redirect to login page

    } catch (err) {
        console.error("Signup error:", err);
        document.getElementById("errorMsg").innerText = err.message;
    }
}

// Optional: allow Enter key to trigger signup
document.addEventListener("keydown", function(e) {
    if (e.key === "Enter") signup();
});
