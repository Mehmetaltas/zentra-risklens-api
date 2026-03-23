(function () {
  const API_BASE = "https://zentra-v2-rrgj.vercel.app/api";

  const ROLE_RULES = {
    "/zentra-main.html": ["viewer", "analyst", "trader", "admin"],
    "/trade-intelligence.html": ["analyst", "admin"],
    "/trade-action.html": ["trader", "admin"],
    "/admin.html": ["admin"]
  };

  function clearAuth() {
    localStorage.removeItem("zentra_token");
    localStorage.removeItem("zentra_user");
  }

  function redirectToPlatform(message) {
    if (message) alert(message);
    window.location.href = "/platform.html";
  }

  async function checkAuth() {
    const token = localStorage.getItem("zentra_token");
    const path = window.location.pathname;

    if (!token) {
      redirectToPlatform();
      return;
    }

    try {
      const response = await fetch(`${API_BASE}/me`, {
        method: "GET",
        headers: {
          Authorization: `Bearer ${token}`
        }
      });

      const data = await response.json();

      if (!response.ok || !data || data.status !== "AUTHORIZED") {
        clearAuth();

        if (
          data &&
          (
            data.status === "SESSION_EXPIRED" ||
            data.status === "SESSION_INACTIVE" ||
            data.status === "SESSION_NOT_FOUND" ||
            data.status === "INVALID_TOKEN" ||
            data.status === "NO_TOKEN"
          )
        ) {
          redirectToPlatform("Oturum süresi doldu. Lütfen tekrar giriş yapın.");
          return;
        }

        redirectToPlatform();
        return;
      }

      const role = data.user.role;
      localStorage.setItem("zentra_user", JSON.stringify(data.user));

      const allowedRoles = ROLE_RULES[path];
      if (allowedRoles && !allowedRoles.includes(role)) {
        redirectToPlatform("Bu sayfaya erişim yetkiniz yok.");
        return;
      }

      document.documentElement.style.display = "block";
    } catch (error) {
      clearAuth();
      redirectToPlatform();
    }
  }

  window.logoutZentra = async function () {
    const token = localStorage.getItem("zentra_token");

    try {
      if (token) {
        await fetch(`${API_BASE}/logout`, {
          method: "POST",
          headers: {
            Authorization: `Bearer ${token}`
          }
        });
      }
    } catch (e) {}

    clearAuth();
    window.location.href = "/platform.html";
  };

  document.documentElement.style.display = "none";
  checkAuth();
})();
