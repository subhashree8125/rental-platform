const API_URL = "http://127.0.0.1:5000/auth/login";

const quotes = [
  "Your next rental home is just a click away...",
  "Find a space that fits your life...",
  "Turning houses into homes...",
  "From budget-friendly to luxury living..."
];

let index = 0;
setInterval(() => {
  index = (index + 1) % quotes.length;
  document.getElementById("quote-text").innerText = quotes[index];
}, 5000);

async function login() {
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
      body: JSON.stringify({ identifier, password }),
    });

    const data = await res.json();

    if (res.ok) {
      localStorage.setItem("user", JSON.stringify(data.user));
      alert("Login Successful!");
      window.location.href = "/explore";
    } else {
      errorMsg.innerText = data.message || "Login failed!";
    }
  } catch (err) {
    errorMsg.innerText = "Network error!";
    console.error(err);
  }
}
