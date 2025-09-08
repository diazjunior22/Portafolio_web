
// #esto es para que la alerta desaparesca
setTimeout(() => {
    document.querySelectorAll('.alert').forEach(el => el.remove());
  }, 4000); // 4 segundos




// <!-- Script para abrir/cerrar menú -->
const btn = document.getElementById("menu-btn");
const menu = document.getElementById("menu");

  btn.addEventListener("click", () => {
    menu.classList.toggle("hidden");
  });


console.log('hola')