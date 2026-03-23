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

  async function checkAuth() {
    const token = localStorage.getItem("zentra_token");
    const path = window.location.pathname;

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
        clearAuth();

        const expired =
          data &&
          (data.status === "SESSION_EXPIRED" ||
           data.status === "SESSION_INACTIVE" ||
           data.status === "SESSION_NOT_FOUND");

        if (expired) {
          alert("Oturum süresi doldu. Lütfen tekrar giriş yapın.");
        }

        window.location.href = "/platform.html";
        return;
      }

      const role = data.user.role;
      localStorage.setItem("zentra_user", JSON.stringify(data.user));

      const allowedRoles = ROLE_RULES[path];
      if (allowedRoles && !allowedRoles.includes(role)) {
        alert("Bu sayfaya erişim yetkiniz yok.");
        window.location.href = "/platform.html";
        return;
      }

      applyRoleUi(role);
      document.documentElement.style.display = "block";
    } catch (error) {
      clearAuth();
      window.location.href = "/platform.html";
    }
  }

  function applyRoleUi(role) {
    document.body.setAttribute("data-role", role);

    document.querySelectorAll("[data-role-show]").forEach((el) => {
      const roles = (el.getAttribute("data-role-show") || "")
        .split(",")
        .map((r) => r.trim())
        .filter(Boolean);

      el.style.display = roles.includes(role) ? "" : "none";
    });

    document.querySelectorAll("[data-role-disable]").forEach((el) => {
      const roles = (el.getAttribute("data-role-disable") || "")
        .split(",")
        .map((r) => r.trim())
        .filter(Boolean);

      if (roles.includes(role)) {
        el.disabled = true;
        el.style.opacity = "0.5";
        el.style.pointerEvents = "none";
      }
    });
  }

  window.logoutZentra = async function () {
    const token = localStorage.getItem("zentra_token");

    try {
      if (token) {
        await fetch(`${API_BASE}/logout`, {
          method: "POST",
          headers: {
            "Authorization": `Bearer ${token}`
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
