(function () {
  const API_BASE = "https://zentra-v2-rrgj.vercel.app/api";
  const token = localStorage.getItem("zentra_token");

  async function checkAuth() {
    if (!token) {
      window.location.href = "/platform.html";
      return;
    }

    try {
      const response = await fetch(`${API_BASE}/me`, {
        method: "GET",
        headers: {
          "Authorization": `Bearer ${token}`
        }
      });

      const data = await response.json();

      if (!response.ok || !data || data.status !== "AUTHORIZED") {
        localStorage.removeItem("zentra_token");
        window.location.href = "/platform.html";
        return;
      }

      document.documentElement.style.display = "block";
    } catch (error) {
      localStorage.removeItem("zentra_token");
      window.location.href = "/platform.html";
    }
  }

  document.documentElement.style.display = "none";
  checkAuth();
})();
<script src="/auth-guard.js"></script>
