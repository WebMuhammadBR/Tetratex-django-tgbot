document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("accesspanel");
  const header = document.getElementById("litheader");
  const submitButton = document.getElementById("go");

  if (!form || !header || !submitButton) {
    return;
  }

  form.addEventListener("submit", () => {
    header.classList.add("poweron");
    submitButton.classList.remove("denied");
    submitButton.value = "Tekshirilmoqda...";
    submitButton.disabled = true;
  });
});
