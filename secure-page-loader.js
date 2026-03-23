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

  function redirectToPlatform(message) {
    if (message) alert(message);
    window.location.href = "/platform.html";
  }

  function runInjectedScripts(container) {
    const scripts = container.querySelectorAll("script");
    scripts.forEach((oldScript) => {
      const newScript = document.createElement("script");

      if (oldScript.src) {
        newScript.src = oldScript.src;
      } else {
        newScript.textContent = oldScript.textContent;
      }

      Array.from(oldScript.attributes).forEach((attr) => {
        if (attr.name !== "src") {
          newScript.setAttribute(attr.name, attr.value);
        }
      });

      document.body.appendChild(newScript);
      oldScript.remove();
    });
  }

  async function loadProtectedContent() {
    const token = localStorage.getItem("zentra_token");
    const path = window.location.pathname;
    const action = PAGE_MAP[path];
    const app = document.getElementById("app");

    if (!action || !app) return;

    if (!token) {
      redirectToPlatform();
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
          redirectToPlatform("Oturum süresi doldu veya erişim geçersiz. Lütfen tekrar giriş yapın.");
          return;
        }

        if (data && data.status === "FORBIDDEN") {
          redirectToPlatform("Bu sayfaya erişim yetkiniz yok.");
          return;
        }

        redirectToPlatform();
        return;
      }

      app.innerHTML = data.html;
      runInjectedScripts(app);
    } catch (error) {
      clearAuth();
      redirectToPlatform();
    }
  }

  window.addEventListener("DOMContentLoaded", loadProtectedContent);
})();
