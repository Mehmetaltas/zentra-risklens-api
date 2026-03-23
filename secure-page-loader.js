(function () {
  const API_BASE = "https://zentra-v2-rrgj.vercel.app/api";

  const PAGE_MAP = {
    "/zentra-main.html": "main",
    "/trade-intelligence.html": "intelligence",
    "/trade-action.html": "action",
    "/admin.html": "admin"
  };

  function clearAuth() {
    localStorage.removeItem("zentra_token");
    localStorage.removeItem("zentra_user");
  }

  async function loadProtectedContent() {
    const token = localStorage.getItem("zentra_token");
    const path = window.location.pathname;
    const action = PAGE_MAP[path];
    const app = document.getElementById("app");

    if (!action || !app) return;

    if (!token) {
      window.location.href = "/platform.html";
      return;
    }

    try {
      const response = await fetch(`${API_BASE}/ui?action=${action}`, {
        method: "GET",
        headers: {
          Authorization: `Bearer ${token}`
        }
      });

      const data = await response.json();

      if (!response.ok) {
        clearAuth();

        if (
          data &&
          (
            data.status === "SESSION_EXPIRED" ||
            data.status === "NO_TOKEN" ||
            data.status === "INVALID_TOKEN" ||
            data.status === "SESSION_INACTIVE" ||
            data.status === "SESSION_NOT_FOUND"
          )
        ) {
          alert("Oturum süresi doldu veya erişim geçersiz. Lütfen tekrar giriş yapın.");
        } else if (data && data.status === "FORBIDDEN") {
          alert("Bu sayfaya erişim yetkiniz yok.");
        }

        window.location.href = "/platform.html";
        return;
      }

      app.innerHTML = data.html;
    } catch (error) {
      clearAuth();
      window.location.href = "/platform.html";
    }
  }

  window.addEventListener("DOMContentLoaded", loadProtectedContent);
})();
