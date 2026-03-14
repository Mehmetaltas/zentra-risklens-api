const ZENTRA_SESSION_KEY = "zentra_private_access";

(function guardDeepLayer() {
  const hasAccess = sessionStorage.getItem(ZENTRA_SESSION_KEY);
  if (hasAccess !== "true") {
    window.location.href = "/zentra-entry.html";
  }
})();
