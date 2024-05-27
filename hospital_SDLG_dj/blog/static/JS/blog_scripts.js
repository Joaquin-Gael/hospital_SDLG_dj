document.addEventListener('DOMContentLoaded', function() {
    const menuToggle = document.getElementById('menu-toggle');
    const navbar = document.getElementById('navbar');

    menuToggle.addEventListener('click', function() {
        navbar.classList.toggle('open'); // Agregar o quitar la clase 'open' al menú
        menuToggle.classList.toggle('active'); // Agregar o quitar la clase 'active' al botón
    });
});