function toggleMenu() {
  const menu = document.getElementById("menuDrawer");
  if (!menu) return;
  menu.classList.toggle("open");
}

function siteSearch(q) {
  const links = document.querySelectorAll(".nav-link");
  const value = q.toLowerCase().trim();

  links.forEach(link => {
    const text = link.innerText.toLowerCase();
    link.style.display = text.includes(value) ? "block" : "none";
  });
}

function logoutZentra() {
  sessionStorage.removeItem("zentra_private_access");
  window.location.href = "/zentra-entry.html";
}

document.addEventListener("keydown", function (e) {
  if (e.key === "Escape") {
    const menu = document.getElementById("menuDrawer");
    if (menu && menu.classList.contains("open")) {
      menu.classList.remove("open");
    }
  }
});
