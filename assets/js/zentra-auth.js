const ZENTRA_PASSWORD = "ZentraCore";
const ZENTRA_SESSION_KEY = "zentra_private_access";

function loginZentra() {
  const input = document.getElementById("zentraPassword");
  const message = document.getElementById("entryMessage");
  const password = input.value.trim();

  if (password === ZENTRA_PASSWORD) {
    sessionStorage.setItem(ZENTRA_SESSION_KEY, "true");
    message.textContent = "Erişim açıldı. Yönlendiriliyor...";
    message.className = "form-message success";
    setTimeout(() => {
      window.location.href = "/risklens/dashboard.html";
    }, 500);
  } else {
    message.textContent = "Şifre hatalı.";
    message.className = "form-message error";
  }
}
