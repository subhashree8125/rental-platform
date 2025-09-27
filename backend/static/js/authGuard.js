// Reusable session check
async function checkSession() {
  try {
    const response = await fetch("/api/session");
    if (!response.ok) return null; // not logged in
    const data = await response.json();
    return data; // { loggedIn: true, user: {...} }
  } catch (err) {
    console.error("Session check failed:", err);
    return null;
  }
}
// Redirect if not logged in
window.addEventListener("DOMContentLoaded", async () => {
  const session = await checkSession();
  if (!session || !session.loggedIn) {
    alert("Please login first to access this page.");
    window.location.href = "login";
  }
});

// Optional: Redirect if already logged in (for login/signup pages)
async function redirectIfLoggedIn() {
  const session = await checkSession();
  if (session && session.loggedIn) {
    alert("You are already logged in.");
    window.location.href = "explore"; // or homepage
  }
}

// Call this on login/signup pages
// window.addEventListener("DOMContentLoaded", redirectIfLoggedIn); // Uncomment to enable            