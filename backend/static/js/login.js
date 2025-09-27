// Backend login API endpoint
const API_URL = "/auth/login";

// Rotating quotes
const quotes = [
  "Your next rental home is just a click away...",
  "Find a space that fits your life...",
  "Turning houses into homes...",
  "From budget-friendly to luxury living..."
];

let index = 0;
setInterval(() => {
  const quoteElem = document.getElementById("quote-text");
  if (quoteElem) {
    index = (index + 1) % quotes.length;
    quoteElem.innerText = quotes[index];
  }
}, 5000);

// Login function
async function login(event) {
  if (event) event.preventDefault();

  const identifier = document.getElementById("identifier").value.trim();
  const password = document.getElementById("password").value.trim();
  const errorMsg = document.getElementById("errorMsg");

  errorMsg.innerText = "";

  if (!identifier || !password) {
    errorMsg.innerText = "Please enter Email/Phone and Password!";
    return;
  }

  try {
    const res = await fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      credentials: "include", // Send session cookies
      body: JSON.stringify({ identifier, password }),
    });

    const data = await res.json();

    if (res.ok && data.success) {
      // Optionally store user in localStorage
      localStorage.setItem("user", JSON.stringify(data.user));

      alert("Login Successful!");
      window.location.href = "/explore"; // Redirect after login
    } else {
      errorMsg.innerText = data.message || "Login failed!";
    }
  } catch (err) {
    errorMsg.innerText = "Network error! Please try again.";
    console.error("Login error:", err);
  }
}

// Attach login function to form submit
document.addEventListener("DOMContentLoaded", () => {
  const loginForm = document.getElementById("loginForm");
  if (loginForm) loginForm.addEventListener("submit", login);
});
